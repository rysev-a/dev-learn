//! Симулятор виртуальной очереди virtio (глава 6): гость кладёт буферы, устройство их обрабатывает, гость забирает результат.
//! Считаются оповещения — выходы в гипервизор. В данных цели — `{trace}`: записанные действия, по ним сервер воспроизводит
//! сессию.

use leptos::prelude::*;
use serde_json::Value;
use virtlab::virtq::{free, Action, Note, QueueState, Session, VirtqGoal};

use super::common::{trace_data, GoalItem, GoalList, Goals};

/// Клетка дескриптора на схеме.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Cell {
    /// Свободен.
    Free,
    /// Ждёт устройство (доступное кольцо).
    Avail,
    /// Обработан, ждёт гостя (использованное кольцо).
    Used,
}

impl Cell {
    fn class(self) -> &'static str {
        match self {
            Cell::Free => "free",
            Cell::Avail => "avail",
            Cell::Used => "used",
        }
    }

    fn glyph(self) -> &'static str {
        match self {
            Cell::Free => "",
            Cell::Avail => "→",
            Cell::Used => "✓",
        }
    }
}

/// Клетки очереди: сначала обработанные, затем ждущие устройство, остальные свободны.
pub fn cells(size: u32, s: &QueueState) -> Vec<Cell> {
    (0..size)
        .map(|i| {
            if i < s.used {
                Cell::Used
            } else if i < s.used + s.avail {
                Cell::Avail
            } else {
                Cell::Free
            }
        })
        .collect()
}

/// Подпись под схемой по тому, что произошло (`None` — подпись не меняется).
pub fn note_text(n: &Note) -> Option<String> {
    Some(match n {
        Note::Overflow { need, free } => {
            i18n::trf!("Free descriptors: {0}, but {1} needed: the queue is full, the guest waits.", free, need)
        }
        Note::Notified { n } => i18n::trf!("Posted {0}; notification sent (exit to the hypervisor).", n),
        Note::Quiet { n } => i18n::trf!("Posted {0}; the device is busy and will see the buffers itself, no notification needed.", n),
        Note::DeviceIdle => i18n::tr("The device is asleep: until the guest notifies it, it processes nothing.").to_string(),
        Note::Processed => i18n::tr("The device processed one buffer and put it on the used ring.").to_string(),
        Note::Reaped => i18n::tr("The guest reaped the finished buffers: the descriptors are free.").to_string(),
        Note::Reset => i18n::tr("The queue was reset.").to_string(),
        Note::SuppressSet => return None,
    })
}

/// Ход упражнения: сессия модели, запись действий и подпись.
#[derive(Clone)]
pub struct VirtqRun {
    session: Session,
    trace: Vec<Action>,
    note: String,
    /// сколько целей из `session.done()` уже передано наружу
    seen: usize,
}

impl VirtqRun {
    pub fn new(size: u32, goals: &[VirtqGoal]) -> Self {
        Self {
            session: Session::new(size, goals),
            trace: vec![],
            note: i18n::trf!("The queue is empty: {0} free descriptors.", size),
            seen: 0,
        }
    }

    pub fn state(&self) -> &QueueState {
        self.session.state()
    }

    pub fn suppress(&self) -> bool {
        self.session.suppress()
    }

    pub fn note(&self) -> &str {
        &self.note
    }

    /// Выполнить действие. Возвращает цели, достигнутые только что, с данными для сервера (запись действий на этот момент).
    pub fn act(&mut self, a: Action) -> Vec<(String, Value)> {
        let note = self.session.act(&a);
        // «устройство спит» ничего не меняет: в запись не попадает (воспроизведение дало бы то же)
        if note != Note::DeviceIdle {
            self.trace.push(a);
        }
        if let Some(text) = note_text(&note) {
            self.note = text;
        }
        let fresh: Vec<(String, Value)> =
            self.session.done()[self.seen..].iter().map(|id| (id.clone(), trace_data(&self.trace))).collect();
        self.seen = self.session.done().len();
        fresh
    }
}

#[component]
pub fn VirtqLab(size: u32, targets: Vec<VirtqGoal>, goals: Goals) -> impl IntoView {
    let items: Vec<GoalItem> = targets.iter().map(|g| GoalItem::new(g.id.clone(), g.text.clone())).collect();
    let run = RwSignal::new(VirtqRun::new(size, &targets));
    let act = move |a: Action| {
        for (id, info) in run.try_update(|r| r.act(a)).unwrap_or_default() {
            goals.mark(&id, info);
        }
    };
    let used = move || run.with(|r| r.state().clone());
    view! {
        <div class="vl">
            <div class="vl-grid">
                <div class="vl-card">
                    <label class="vl-check">
                        <input
                            type="checkbox"
                            prop:checked=move || run.with(VirtqRun::suppress)
                            on:change=move |ev| act(Action::Suppress { on: event_target_checked(&ev) })
                        />
                        <span>{i18n::tr("notification suppression: ring only if the device is asleep")}</span>
                    </label>
                    <div class="vl-actions wrap">
                        <button class="quiz-btn" on:click=move |_| act(Action::Post { n: 1 })>{i18n::tr("Guest: post 1 buffer")}</button>
                        <button class="quiz-btn" on:click=move |_| act(Action::Post { n: 3 })>{i18n::tr("Guest: post a batch of 3")}</button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Device)>{i18n::tr("Device: process 1")}</button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Reap)>{i18n::tr("Guest: reap finished")}</button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Reset)>{i18n::tr("Reset")}</button>
                    </div>
                    <GoalList goals=goals items=items />
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">{i18n::tr("queue descriptors")}</span>
                        <span class="pr-res-time">{move || i18n::trf!("{0} of {1} free", free(size, &used()), size)}</span>
                    </div>
                    <div class="vl-desc">
                        {move || {
                            cells(size, &used())
                                .into_iter()
                                .map(|c| view! { <i class=c.class()>{c.glyph()}</i> })
                                .collect_view()
                        }}
                    </div>
                    <p class="vl-hint">
                        {i18n::tr("gray are free, blue wait for the device (available ring), green are processed and wait for the guest (used ring).")}
                    </p>
                    <table class="vl-stat">
                        <tbody>
                            <tr><td>{i18n::tr("device")}</td><td>{move || if used().busy { i18n::tr("busy") } else { i18n::tr("asleep") }}</td></tr>
                            <tr><td>{i18n::tr("buffers posted")}</td><td>{move || used().posted}</td></tr>
                            <tr><td>{i18n::tr("processed")}</td><td>{move || used().processed}</td></tr>
                            <tr><td><b>{i18n::tr("notifications (exits)")}</b></td><td><b>{move || used().notifies}</b></td></tr>
                        </tbody>
                    </table>
                    <p class="vl-final">{move || run.with(|r| r.note().to_string())}</p>
                </div>
            </div>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;
    use virtlab::virtq::{default_goals, SIZE};

    use super::*;

    fn run() -> VirtqRun {
        VirtqRun::new(SIZE, &default_goals())
    }

    fn ids(v: Vec<(String, Value)>) -> Vec<String> {
        v.into_iter().map(|(id, _)| id).collect()
    }

    #[test]
    fn cells_layout() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let s = QueueState { avail: 2, used: 1, ..QueueState::default() };
        let c = cells(4, &s);
        assert_eq!(c, [Cell::Used, Cell::Avail, Cell::Avail, Cell::Free]);
        assert_eq!(cells(SIZE, &QueueState::default()), vec![Cell::Free; SIZE as usize]);
    }

    #[test]
    fn overflow_goal_and_note() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let mut r = run();
        for _ in 0..2 {
            r.act(Action::Post { n: 3 });
        }
        let got = ids(r.act(Action::Post { n: 3 }));
        assert_eq!(got, ["overflow"]);
        assert_eq!(r.note(), "Свободных дескрипторов 2, а нужно 3: очередь переполнена, гость ждёт.");
    }

    #[test]
    fn batch_goal_trace_replays_on_server() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let mut r = run();
        r.act(Action::Post { n: 3 });
        let got = r.act(Action::Post { n: 3 });
        assert_eq!(ids(got.clone()), ["batch"]);
        // данные цели — запись действий до этого момента
        let (_, info) = got.into_iter().next().expect("цель");
        assert_eq!(info, json!({"trace": [{"op": "post", "n": 3}, {"op": "post", "n": 3}]}));
        let spec = virtlab::Spec::Virtq { size: SIZE, goals: default_goals() };
        let mut solution = serde_json::Map::new();
        solution.insert("batch".into(), info);
        let v = virtlab::verify(&spec, &Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "batch").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }

    #[test]
    fn idle_device_is_not_traced_and_goals_are_reported_once() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let mut r = run();
        r.act(Action::Device);
        assert_eq!(r.note(), "Устройство спит: пока гость не оповестит, оно ничего не обрабатывает.");
        assert!(r.trace.is_empty());
        r.act(Action::Suppress { on: true });
        assert_eq!(r.note(), "Устройство спит: пока гость не оповестит, оно ничего не обрабатывает.", "подпись не меняется");
        assert!(r.suppress());
        // два раза: пачка, ещё пачка (устройство занято — без оповещения), устройство разбирает всё, гость забирает
        let mut all = vec![];
        for _ in 0..2 {
            all.extend(ids(r.act(Action::Post { n: 3 })));
            all.extend(ids(r.act(Action::Post { n: 3 })));
            for _ in 0..6 {
                all.extend(ids(r.act(Action::Device)));
            }
            all.extend(ids(r.act(Action::Reap)));
        }
        assert_eq!((r.state().posted, r.state().notifies), (12, 2));
        all.sort();
        all.dedup();
        assert_eq!(all, ["suppress"], "цель достигнута и сообщена один раз");
    }

    #[test]
    fn reset_clears_queue_but_keeps_suppress() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let mut r = run();
        r.act(Action::Suppress { on: true });
        r.act(Action::Post { n: 3 });
        r.act(Action::Reset);
        assert_eq!(r.state().posted, 0);
        assert!(r.suppress());
        assert_eq!(r.note(), "Очередь сброшена.");
    }
}
