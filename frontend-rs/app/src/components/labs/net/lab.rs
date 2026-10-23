//! Состояние лаборатории «Компьютерные сети»: сеть ученика, выбор и режимы, последняя проба с анимацией, терминалы и
//! цели. Здесь же действия над сетью: правка настроек, кабели, команды терминала, показ пути пакета по цели.
//!
//! Правила, которые держит этот файл:
//! * любая правка настроек или кабелей — через [`Lab::edit`]/[`Lab::connect`]/…: они считают цели заново, сбрасывают
//!   «проверено» и отправляют черновик хозяину;
//! * перетаскивание устройства и кэши симулятора (ARP, таблицы MAC) меняют сеть, но цели не пересчитывают.

use std::collections::HashMap;
use std::sync::Arc;

use leptos::prelude::*;
use netlab::check::{run_probe, GoalKind};
use netlab::term::exec;
use netlab::transfer::TransferChart;
use netlab::types::{Device, NetState};
use netlab::{check_goals, NetSpec, Tools};

use super::logic::{self, GoalView, RunView};

/// Строка терминала: введённая команда или вывод.
#[derive(Clone, Debug, PartialEq)]
pub struct TermLine {
    pub cmd: bool,
    pub text: String,
}

/// Лаборатория: набор сигналов, копируется в компоненты как есть.
#[derive(Clone, Copy)]
pub struct Lab {
    pub net: RwSignal<NetState>,
    spec: StoredValue<Arc<NetSpec>>,
    tools: StoredValue<Tools>,
    hint: StoredValue<String>,
    on_draft: Callback<String>,
    /// выбранное устройство
    pub sel: RwSignal<String>,
    /// включён режим прокладки кабеля
    pub cable: RwSignal<bool>,
    /// первое устройство будущего кабеля
    pub cable_from: RwSignal<Option<String>>,
    /// выбранный кабель (индекс)
    pub sel_link: RwSignal<Option<usize>>,
    pub notice: RwSignal<String>,
    pub hint_open: RwSignal<bool>,
    /// ученик уже что-то менял: до этого цели показаны номерами, а не отметками
    pub touched: RwSignal<bool>,
    /// нажали «Проверить»: если не всё выполнено, показать подсказку под целями
    pub checked: RwSignal<bool>,
    /// версия настроек: растёт при каждой правке, по ней пересчитываются цели
    rev: RwSignal<u64>,
    pub terms: RwSignal<HashMap<String, Vec<TermLine>>>,
    pub run: RwSignal<Option<RunView>>,
    /// положение анимации в «моментах»
    pub slot: RwSignal<f64>,
    pub chart: RwSignal<Option<TransferChart>>,
    /// номер показа: новый показ отменяет предыдущую анимацию
    anim: StoredValue<u64>,
    /// итоги по целям
    pub goals: Memo<Vec<GoalView>>,
    /// все цели выполнены
    pub solved_now: Memo<bool>,
}

impl Lab {
    pub fn new(spec: Arc<NetSpec>, initial: NetState, hint: String, on_draft: Callback<String>, touched: bool) -> Lab {
        let first = initial.devices.iter().next().map(|d| d.id.clone()).unwrap_or_default();
        let net = RwSignal::new(initial);
        let rev = RwSignal::new(0u64);
        let goals_spec = spec.clone();
        let goals = Memo::new(move |_| {
            rev.track();
            net.with_untracked(|n| check_goals(n, &goals_spec.goals).into_iter().map(GoalView::from).collect::<Vec<_>>())
        });
        let solved_now = Memo::new(move |_| goals.with(|g| logic::all_ok(g)));
        let tools = spec.tools.clone();
        Lab {
            net,
            spec: StoredValue::new(spec),
            tools: StoredValue::new(tools),
            hint: StoredValue::new(hint),
            on_draft,
            sel: RwSignal::new(first),
            cable: RwSignal::new(false),
            cable_from: RwSignal::new(None),
            sel_link: RwSignal::new(None),
            notice: RwSignal::new(String::new()),
            hint_open: RwSignal::new(false),
            touched: RwSignal::new(touched),
            checked: RwSignal::new(false),
            rev,
            terms: RwSignal::new(HashMap::new()),
            run: RwSignal::new(None),
            slot: RwSignal::new(0.0),
            chart: RwSignal::new(None),
            anim: StoredValue::new(0),
            goals,
            solved_now,
        }
    }

    pub fn tools(&self) -> Tools {
        self.tools.get_value()
    }

    pub fn hint(&self) -> String {
        self.hint.get_value()
    }

    /// Устройство по id (копия).
    pub fn device(&self, id: &str) -> Option<Device> {
        self.net.with(|n| n.devices.get(id).cloned())
    }

    /// Название устройства для журнала: имя, а если устройства нет — id.
    pub fn name_of(&self, id: &str) -> String {
        self.net.with(|n| n.devices.get(id).map(|d| d.name.clone())).unwrap_or_else(|| id.to_string())
    }

    /// Состояние сети как JSON решения.
    pub fn solution_json(&self) -> String {
        self.net.with_untracked(logic::draft_json)
    }

    fn save(&self) {
        self.on_draft.run(self.solution_json());
    }

    /// Настройки или кабели изменились: пересчитать цели, снять «проверено», сохранить черновик.
    fn changed(&self) {
        self.rev.update(|r| *r += 1);
        self.touched.set(true);
        self.checked.set(false);
        self.save();
    }

    /// Изменить сеть функцией и вернуть её результат (обычно — текст ошибки).
    pub fn edit<T>(&self, f: impl FnOnce(&mut NetState) -> T) -> T {
        let mut out = None;
        self.net.update(|n| out = Some(f(n)));
        self.changed();
        out.expect("update всегда вызывает замыкание")
    }

    /// Изменить одно устройство.
    pub fn edit_device<T>(&self, id: &str, f: impl FnOnce(&mut Device) -> T) -> Option<T> {
        self.edit(|n| n.devices.get_mut(id).map(f))
    }

    /// Сдвинуть устройство на поле (цели не пересчитываются).
    pub fn move_device(&self, id: &str, x: f64, y: f64) {
        self.net.update(|n| {
            if let Some(d) = n.devices.get_mut(id) {
                d.x = x;
                d.y = y;
            }
        });
    }

    /// Конец перетаскивания: сохранить черновик с новым положением.
    pub fn moved(&self) {
        self.touched.set(true);
        self.save();
    }

    /* ---- кабели ---- */

    /// Выбрать устройство и снять выбор кабеля.
    pub fn select(&self, id: &str) {
        self.sel.set(id.to_string());
        self.sel_link.set(None);
    }

    /// Проложить кабель между первыми свободными портами; ошибка — в «notice».
    pub fn connect(&self, a: &str, b: &str) -> bool {
        let mut res = Ok(());
        self.net.update(|n| res = n.connect(a, b, None));
        match res {
            Ok(()) => {
                self.notice.set(String::new());
                self.changed();
                true
            }
            Err(e) => {
                self.notice.set(e);
                false
            }
        }
    }

    pub fn remove_link(&self) {
        let Some(i) = self.sel_link.get_untracked() else { return };
        self.net.update(|n| n.disconnect(i));
        self.sel_link.set(None);
        self.changed();
    }

    pub fn toggle_cable(&self) {
        self.cable.update(|c| *c = !*c);
        self.cable_from.set(None);
        self.notice.set(String::new());
    }

    /* ---- команды ---- */

    /// Команда терминала: вывод в историю устройства, проба — в анимацию, график — под поле.
    pub fn terminal_run(&self, dev: &str, line: &str) {
        let mut res = None;
        self.net.update(|n| res = Some(exec(n, dev, line)));
        let Some(res) = res else { return };
        if res.changed == Some(true) {
            self.changed();
        }
        self.terms.update(|t| {
            let lines = t.entry(dev.to_string()).or_default();
            if res.clear {
                lines.clear();
                return;
            }
            lines.push(TermLine { cmd: true, text: line.to_string() });
            if !res.out.is_empty() {
                lines.extend(res.out.split('\n').map(|l| TermLine { cmd: false, text: l.to_string() }));
            }
        });
        if let Some(p) = res.probe {
            self.play(RunView::new(p.hops, p.events, line));
        }
        if let Some(c) = res.chart {
            self.chart.set(Some(c));
        }
    }

    /// Команда от формы NAT/файрвола/службы: то же, что терминал, но вывод — тут же под формой.
    pub fn form_exec(&self, dev: &str, line: &str) -> String {
        let mut res = None;
        self.net.update(|n| res = Some(exec(n, dev, line)));
        let Some(res) = res else { return String::new() };
        if res.changed == Some(true) {
            self.changed();
        }
        res.out
    }

    /* ---- анимация ---- */

    /// Показать путь пакета: `None` — убрать.
    pub fn play(&self, run: Option<RunView>) {
        self.anim.update_value(|a| *a += 1);
        let Some(run) = run else {
            self.run.set(None);
            return;
        };
        let total = run.total_slots();
        self.run.set(Some(run));
        self.slot.set(0.0);
        self.animate(total);
    }

    /// Запустить бег пакетов; вне браузера (в тестах) показ сразу доходит до конца.
    #[cfg(target_arch = "wasm32")]
    fn animate(&self, total: f64) {
        self.tick(self.anim.get_value(), js_sys::Date::now(), total);
    }

    #[cfg(not(target_arch = "wasm32"))]
    fn animate(&self, total: f64) {
        self.slot.set(total);
    }

    #[cfg(target_arch = "wasm32")]
    fn tick(&self, gen: u64, start: f64, total: f64) {
        let lab = *self;
        leptos::leptos_dom::helpers::request_animation_frame(move || {
            if lab.anim.try_get_value() != Some(gen) {
                return;
            }
            let s = (js_sys::Date::now() - start) / logic::SLOT_MS;
            lab.slot.try_set(s.min(total));
            if s < total {
                lab.tick(gen, start, total);
            }
        });
    }

    /// Остановить анимацию (при уходе со страницы).
    pub fn stop(&self) {
        self.anim.try_update_value(|a| *a += 1);
    }

    /// Показать путь пакета по цели (кнопка ▶): проба идёт на копии сети, а её кэши (ARP, MAC) остаются в сети.
    pub fn play_goal(&self, idx: usize) {
        let spec = self.spec.get_value();
        let Some(goal) = spec.goals.get(idx) else { return };
        match &goal.kind {
            GoalKind::Ping(_) | GoalKind::Udp(_) | GoalKind::Tcp(_) => {
                let mut copy = self.net.get_untracked();
                let out = run_probe(&mut copy, goal);
                self.play(RunView::new(out.hops, out.events, &goal.text));
                self.net.update(|n| n.rt = copy.rt);
            }
            _ => {
                let state = self.net.get_untracked();
                let Some(res) = check_goals(&state, std::slice::from_ref(goal)).into_iter().next() else { return };
                if let Some(c) = res.run.chart {
                    self.chart.set(Some(c));
                    if res.run.hops.is_empty() && res.run.events.is_empty() {
                        return;
                    }
                }
                self.play(RunView::new(res.run.hops, res.run.events, &goal.text));
            }
        }
    }

    /// Вернуть исходную сеть и очистить всё, что видно ученику.
    pub fn reset(&self) {
        let start = self.spec.with_value(|s| s.start_state());
        self.net.set(start);
        self.play(None);
        self.chart.set(None);
        self.terms.set(HashMap::new());
        self.sel_link.set(None);
        self.cable.set(false);
        self.cable_from.set(None);
        self.notice.set(String::new());
        self.changed();
        self.touched.set(false);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use netlab::verify_json;
    use serde_json::Value;

    fn specs() -> Vec<(String, NetSpec)> {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/net");
        let mut out = Vec::new();
        let Ok(entries) = std::fs::read_dir(&dir) else { return out };
        for e in entries.filter_map(Result::ok) {
            let v: Value = serde_json::from_str(&std::fs::read_to_string(e.path()).expect("файл данных")).expect("JSON");
            for t in v["tasks"].as_array().expect("упражнения") {
                let spec: NetSpec = serde_json::from_value(t["spec"].clone()).expect("сценарий");
                out.push((t["id"].as_str().unwrap_or("?").to_string(), spec));
            }
        }
        out
    }

    fn lab_of(spec: &NetSpec) -> (Owner, Lab, std::sync::Arc<std::sync::Mutex<Vec<String>>>) {
        let owner = Owner::new();
        owner.set();
        let drafts = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
        let sink = drafts.clone();
        let on_draft = Callback::new(move |d: String| sink.lock().expect("замок").push(d));
        let lab = Lab::new(Arc::new(spec.clone()), spec.start_state(), String::new(), on_draft, false);
        (owner, lab, drafts)
    }

    /// У каждого упражнения исходная сеть не решает цели, а эталон решает: решение, собранное лабораторией, принимает
    /// и серверная проверка.
    #[test]
    fn every_exercise_goes_from_unsolved_to_solved_and_the_server_accepts_it() {
        let all = specs();
        assert!(all.is_empty() || all.len() >= 70, "ожидалось ≈79 упражнений, найдено {}", all.len());
        for (id, spec) in all {
            let (_owner, lab, drafts) = lab_of(&spec);
            assert!(!lab.solved_now.get_untracked(), "{id}: исходная сеть не должна решать цели");
            let solved = spec.solved_state().unwrap_or_else(|e| panic!("{id}: {e}"));
            lab.net.set(solved);
            lab.edit(|_| ());
            assert!(lab.solved_now.get_untracked(), "{id}: эталон должен решать цели: {:?}", lab.goals.get_untracked());
            assert!(lab.touched.get_untracked());
            assert_eq!(drafts.lock().expect("замок").len(), 1, "{id}: правка сохраняет черновик");
            let verdict = verify_json(&spec, &lab.solution_json());
            assert!(verdict.ok, "{id}: сервер не принял решение: {verdict:?}");
            // «Сбросить» возвращает исходную сеть и цели снова не выполнены
            lab.reset();
            assert!(!lab.solved_now.get_untracked(), "{id}");
            assert!(!lab.touched.get_untracked());
        }
    }

    #[test]
    fn cable_and_terminal_commands_change_the_network_and_goals() {
        let Some((id, spec)) = specs().into_iter().find(|(_, s)| s.tools.cable) else { return };
        let (_owner, lab, drafts) = lab_of(&spec);
        let before = lab.net.with_untracked(|n| n.links.len());
        // устройство без свободных портов или с самим собой — ошибка, сеть не меняется
        let first = lab.net.with_untracked(|n| n.devices.iter().next().map(|d| d.id.clone())).expect("устройство");
        assert!(!lab.connect(&first, &first), "{id}");
        assert!(!lab.notice.get_untracked().is_empty());
        assert_eq!(lab.net.with_untracked(|n| n.links.len()), before);
        assert!(drafts.lock().expect("замок").is_empty());
        // команда терминала пишет историю устройства
        lab.terminal_run(&first, "hostname");
        let lines = lab.terms.with_untracked(|t| t.get(&first).cloned().unwrap_or_default());
        assert_eq!(lines.len(), 2);
        assert!(lines[0].cmd && !lines[1].cmd);
        lab.terminal_run(&first, "clear");
        assert!(lab.terms.with_untracked(|t| t.get(&first).cloned().unwrap_or_default()).is_empty());
        // удаление кабеля
        if before > 0 {
            lab.sel_link.set(Some(0));
            lab.remove_link();
            assert_eq!(lab.net.with_untracked(|n| n.links.len()), before - 1);
            assert!(lab.sel_link.get_untracked().is_none());
        }
    }

    #[test]
    fn ping_goal_plays_a_run_and_keeps_caches() {
        let Some((_, spec)) = specs().into_iter().find(|(_, s)| s.goals.iter().any(|g| matches!(g.kind, netlab::GoalKind::Ping(_)))) else { return };
        let (_owner, lab, _) = lab_of(&spec);
        let idx = spec.goals.iter().position(|g| matches!(g.kind, netlab::GoalKind::Ping(_))).expect("цель ping");
        lab.play_goal(idx);
        assert!(lab.run.with_untracked(|r| r.is_some()), "путь пакета показан");
        assert!(lab.slot.get_untracked() > 0.0);
        let title = lab.run.with_untracked(|r| r.as_ref().map(|r| r.title.clone())).unwrap_or_default();
        assert_eq!(title, spec.goals[idx].text);
    }
}
