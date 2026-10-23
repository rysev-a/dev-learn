//! Симулятор слоёв qcow2 (глава 9): снимки, запись с копированием, чтение вниз по цепочке, слияние и откат. Решено, когда
//! выполнены все цели. В данных цели — `{trace}`: записанные действия, по ним сервер воспроизводит сессию.

use std::collections::BTreeMap;

use leptos::prelude::*;
use serde_json::Value;
use virtlab::{
    qcow2::{Action, Layer, Note, Qcow2Goal, Session},
    spec::{base_map, BaseCluster},
};

use super::common::{trace_data, GoalItem, GoalList, Goals};

/// Буквы данных для записи.
const LETTERS: &str = "EFGHIJKLMNOPQRSTUVWXYZ";

/// Подпись под цепочкой по тому, что произошло; `cluster` и `data` — параметры записи или чтения.
pub fn note_text(note: &Note, cluster: u32, data: &str) -> String {
    match note {
        Note::Snapshot => "Снимок: сверху добавлен пустой слой, прежний заморожен. Ничего не копировалось.".to_string(),
        Note::Write { copy_up: true } => format!(
            "Запись «{data}» в кластер {cluster}: кластер лежит в нижнем слое, новая версия появилась только в верхнем (копирование при записи)."
        ),
        Note::Write { copy_up: false } => format!("Запись «{data}» в кластер {cluster}: кластер выделен в верхнем слое."),
        Note::Read(r) => match (&r.value, &r.layer) {
            (Some(v), Some(layer)) => {
                format!("Кластер {cluster} = «{v}», найден в слое «{layer}», обращений к таблицам: {}.", r.lookups)
            }
            _ => format!("Кластера {cluster} нет ни в одном слое: читаются нули (проверено слоёв: {}).", r.lookups),
        },
        Note::Committed => "Слияние: кластеры верхнего слоя перенесены в нижний, цепочка стала короче.".to_string(),
        Note::CommitImpossible => "Слияние невозможно: слой всего один.".to_string(),
        Note::Reverted { had_data: true } => {
            "Откат: верхний слой с записями отброшен. Прочитайте кластер, который вы в него писали.".to_string()
        }
        Note::Reverted { had_data: false } => "Откат: пустой верхний слой отброшен.".to_string(),
        Note::RevertImpossible => "Откат невозможен: слой всего один.".to_string(),
    }
}

/// Прочитанный путь: кластер и глубина слоя, на котором чтение остановилось.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Path {
    pub cluster: u32,
    pub depth: usize,
}

/// Слой цепочки подсвечен как пройденный чтением.
pub fn walked(path: Option<Path>, depth: usize, chain_len: usize) -> bool {
    path.is_some_and(|p| depth <= p.depth && depth < chain_len)
}

/// Ход упражнения: сессия модели, запись действий, путь чтения и подпись.
#[derive(Clone)]
pub struct Qcow2Run {
    session: Session,
    trace: Vec<Action>,
    path: Option<Path>,
    msg: String,
    seen: usize,
}

impl Qcow2Run {
    pub fn new(base: &BTreeMap<u32, String>, goals: &[Qcow2Goal]) -> Self {
        Self {
            session: Session::new(base, goals),
            trace: vec![],
            path: None,
            msg: "Цепочка из одного слоя: база с кластерами 0–3.".to_string(),
            seen: 0,
        }
    }

    pub fn chain(&self) -> &[Layer] {
        self.session.chain()
    }

    pub fn path(&self) -> Option<Path> {
        self.path
    }

    pub fn msg(&self) -> &str {
        &self.msg
    }

    /// Выполнить действие. Возвращает цели, достигнутые только что, с данными для сервера (запись действий на этот момент).
    pub fn act(&mut self, a: Action) -> Vec<(String, Value)> {
        let (cluster, data) = match &a {
            Action::Write { cluster, data } => (*cluster, data.as_str()),
            Action::Read { cluster } => (*cluster, ""),
            _ => (0, ""),
        };
        let note = self.session.act(&a);
        let impossible = matches!(note, Note::CommitImpossible | Note::RevertImpossible);
        self.msg = note_text(&note, cluster, data);
        if !impossible {
            // невозможное действие ничего не меняет и в запись не попадает; путь чтения сбрасывается любым действием
            self.path = match &note {
                Note::Read(r) => Some(Path { cluster, depth: r.depth.unwrap_or(self.session.chain().len()) }),
                _ => None,
            };
            self.trace.push(a);
        }
        let fresh: Vec<(String, Value)> =
            self.session.done()[self.seen..].iter().map(|id| (id.clone(), trace_data(&self.trace))).collect();
        self.seen = self.session.done().len();
        fresh
    }
}

#[component]
pub fn Qcow2Lab(clusters: u32, base: Vec<BaseCluster>, targets: Vec<Qcow2Goal>, goals: Goals) -> impl IntoView {
    let items: Vec<GoalItem> = targets.iter().map(|g| GoalItem::new(g.id.clone(), g.text.clone())).collect();
    let run = RwSignal::new(Qcow2Run::new(&base_map(&base), &targets));
    let cluster = RwSignal::new(0u32);
    let letter = RwSignal::new("E".to_string());
    let act = move |a: Action| {
        for (id, info) in run.try_update(|r| r.act(a)).unwrap_or_default() {
            goals.mark(&id, info);
        }
    };
    let picks = (0..clusters)
        .map(|i| {
            view! {
                <button class="vl-segbtn" class:on=move || cluster.get() == i on:click=move |_| cluster.set(i)>
                    {i}
                </button>
            }
        })
        .collect_view();
    let letters = LETTERS
        .chars()
        .map(|l| {
            let key = l.to_string();
            let k = key.clone();
            view! { <option value=key selected=move || letter.get() == k>{l.to_string()}</option> }
        })
        .collect_view();
    view! {
        <div class="vl">
            <div class="vl-grid">
                <div class="vl-card">
                    <div class="vl-field">
                        <span>"кластер"</span>
                        <div class="vl-seg">{picks}</div>
                    </div>
                    <label class="vl-field">
                        <span>"данные для записи"</span>
                        <select on:change=move |ev| letter.set(event_target_value(&ev))>{letters}</select>
                    </label>
                    <div class="vl-actions wrap">
                        <button
                            class="quiz-btn"
                            on:click=move |_| act(Action::Write { cluster: cluster.get_untracked(), data: letter.get_untracked() })
                        >
                            "Записать"
                        </button>
                        <button class="quiz-btn" on:click=move |_| act(Action::Read { cluster: cluster.get_untracked() })>
                            "Прочитать"
                        </button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Snapshot)>"Снимок"</button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Commit)>"Слить верхний слой"</button>
                        <button class="quiz-btn ghost" on:click=move |_| act(Action::Revert)>"Откатить верхний слой"</button>
                    </div>
                    <GoalList goals=goals items=items />
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">"цепочка слоёв (сверху вниз)"</span>
                        <span class="pr-res-time">{move || format!("{} сл.", run.with(|r| r.chain().len()))}</span>
                    </div>
                    <div class="vl-layers">{move || run.with(|r| layers_view(r.chain(), r.path(), clusters))}</div>
                    <p class="vl-hint">{format!("Клетки — кластеры 0…{}; подсвечены слои, которые прошло чтение.", clusters.saturating_sub(1))}</p>
                    <p class="vl-final">{move || run.with(|r| r.msg().to_string())}</p>
                </div>
            </div>
        </div>
    }
}

/// Слои цепочки с клетками кластеров.
fn layers_view(chain: &[Layer], path: Option<Path>, clusters: u32) -> impl IntoView {
    let len = chain.len();
    chain
        .iter()
        .enumerate()
        .map(|(depth, l)| {
            let cells = (0..clusters)
                .map(|c| {
                    let value = l.data.get(&c);
                    let hit = path.is_some_and(|p| p.cluster == c && p.depth == depth);
                    view! { <i class:has=value.is_some() class:hit=hit>{value.cloned().unwrap_or_default()}</i> }
                })
                .collect_view();
            view! {
                <div class="vl-layer" class:walk=walked(path, depth, len)>
                    <span class="vl-lname">{l.name.clone()}</span>
                    <div class="vl-cells">{cells}</div>
                </div>
            }
        })
        .collect_view()
}

#[cfg(test)]
mod tests {
    use virtlab::qcow2::{default_base, default_goals};

    use super::*;

    fn run() -> Qcow2Run {
        Qcow2Run::new(&default_base(), &default_goals())
    }

    fn ids(v: Vec<(String, Value)>) -> Vec<String> {
        v.into_iter().map(|(id, _)| id).collect()
    }

    fn write(c: u32, d: &str) -> Action {
        Action::Write { cluster: c, data: d.to_string() }
    }

    #[test]
    fn deep_read_goal_with_path() {
        let mut r = run();
        for _ in 0..3 {
            r.act(Action::Snapshot);
        }
        assert_eq!(r.chain().len(), 4);
        let got = ids(r.act(Action::Read { cluster: 0 }));
        assert_eq!(got, ["deep"]);
        assert_eq!(r.path(), Some(Path { cluster: 0, depth: 3 }));
        assert_eq!(r.msg(), "Кластер 0 = «A», найден в слое «база», обращений к таблицам: 4.");
        // любое другое действие сбрасывает путь
        r.act(Action::Snapshot);
        assert_eq!(r.path(), None);
    }

    #[test]
    fn read_of_missing_cluster_walks_whole_chain() {
        let mut r = run();
        r.act(Action::Snapshot);
        r.act(Action::Read { cluster: 7 });
        assert_eq!(r.path(), Some(Path { cluster: 7, depth: 2 }));
        assert_eq!(r.msg(), "Кластера 7 нет ни в одном слое: читаются нули (проверено слоёв: 2).");
    }

    #[test]
    fn rollback_goal_and_trace_replays_on_server() {
        let mut r = run();
        r.act(Action::Snapshot);
        r.act(write(1, "Z"));
        r.act(Action::Revert);
        assert_eq!(r.msg(), "Откат: верхний слой с записями отброшен. Прочитайте кластер, который вы в него писали.");
        let got = r.act(Action::Read { cluster: 1 });
        assert_eq!(ids(got.clone()), ["rollback"]);
        let (_, info) = got.into_iter().next().expect("цель");
        assert_eq!(info["trace"].as_array().map(Vec::len), Some(4));
        let spec = virtlab::Spec::Qcow2 {
            clusters: virtlab::qcow2::CLUSTERS,
            base: default_base().into_iter().map(|(cluster, data)| BaseCluster { cluster, data }).collect(),
            goals: default_goals(),
        };
        let mut solution = serde_json::Map::new();
        solution.insert("rollback".into(), info);
        let v = virtlab::verify(&spec, &Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "rollback").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }

    #[test]
    fn squash_goal_after_commits() {
        let mut r = run();
        for _ in 0..3 {
            r.act(Action::Snapshot);
        }
        assert!(ids(r.act(Action::Commit)).is_empty(), "из четырёх слоёв осталось три");
        assert_eq!(ids(r.act(Action::Commit)), ["squash"]);
        assert_eq!(r.chain().len(), 2);
    }

    #[test]
    fn impossible_actions_are_not_traced_and_keep_path() {
        let mut r = run();
        r.act(Action::Read { cluster: 0 });
        let traced = r.trace.len();
        r.act(Action::Commit);
        assert_eq!(r.msg(), "Слияние невозможно: слой всего один.");
        r.act(Action::Revert);
        assert_eq!(r.msg(), "Откат невозможен: слой всего один.");
        assert_eq!(r.trace.len(), traced);
        assert_eq!(r.path(), Some(Path { cluster: 0, depth: 0 }));
    }

    #[test]
    fn copy_up_write_note() {
        let mut r = run();
        r.act(Action::Snapshot);
        r.act(write(0, "F"));
        assert_eq!(
            r.msg(),
            "Запись «F» в кластер 0: кластер лежит в нижнем слое, новая версия появилась только в верхнем (копирование при записи)."
        );
        r.act(write(5, "G"));
        assert_eq!(r.msg(), "Запись «G» в кластер 5: кластер выделен в верхнем слое.");
    }

    #[test]
    fn walked_layers() {
        let p = Some(Path { cluster: 0, depth: 1 });
        assert!(walked(p, 0, 3) && walked(p, 1, 3) && !walked(p, 2, 3));
        assert!(!walked(None, 0, 3));
        // чтение «в никуда» проходит все слои
        assert!(walked(Some(Path { cluster: 0, depth: 3 }), 2, 3));
    }
}
