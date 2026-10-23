//! Состояние лаборатории «Системный дизайн»: схема ученика, выбор, отказы, расчёт и цели, а также действия над схемой
//! (поставить, соединить, удалить, изменить параметр, сбросить). Это набор сигналов, который копируется в компоненты
//! целиком; логика правок лежит в `logic.rs`, расчёт — в крейте `sdlab`.

use std::sync::Arc;

use leptos::prelude::*;
use sdlab::{all_ok, check_goals, evaluate, EvalOptions, EvalResult, FailKind, GoalResult, Kind, ParamValue, Scenario, SdEdge, SdState};

use super::logic;
use crate::components::labs::board_view::Point;

#[derive(Clone, Copy)]
pub struct Lab {
    scenario: StoredValue<Arc<Scenario>>,
    /// подсказка упражнения
    pub hint: StoredValue<String>,
    /// схема ученика: она же черновик и решение
    pub state: RwSignal<SdState>,
    /// выбранный компонент (его параметры — в плавающей карточке)
    pub sel: RwSignal<Option<String>>,
    /// выбранная связь
    pub sel_edge: RwSignal<Option<SdEdge>>,
    /// сообщение под полем (почему связь не поставилась и т. п.)
    pub notice: RwSignal<String>,
    /// компоненты, отключённые вручную
    pub down: RwSignal<Vec<String>>,
    /// проверяемый отказ
    pub fail: RwSignal<Option<FailKind>>,
    pub hint_open: RwSignal<bool>,
    pub help_open: RwSignal<bool>,
    /// схема на весь экран
    pub fs: RwSignal<bool>,
    /// расчёт с отказом и отключёнными узлами (для метрик и загрузки узлов)
    pub result: Memo<EvalResult>,
    /// цели по схеме без отказов
    pub goals: Memo<Vec<GoalResult>>,
    /// выполнены все цели
    pub solved_now: Memo<bool>,
    /// выбранный компонент, если он есть на схеме
    pub selected: Memo<Option<String>>,
    /// отказы по видам компонентов, которые есть на схеме
    pub fail_kinds: Memo<Vec<FailKind>>,
    on_draft: Callback<String>,
}

impl Lab {
    pub fn new(scenario: Arc<Scenario>, initial: SdState, hint: String, on_draft: Callback<String>) -> Self {
        let state = RwSignal::new(initial);
        let down = RwSignal::new(Vec::<String>::new());
        let fail = RwSignal::new(None::<FailKind>);
        let scenario = StoredValue::new(scenario);

        let result = Memo::new(move |_| {
            let opts = EvalOptions { fail: fail.get(), down: down.get() };
            scenario.with_value(|sc| state.with(|s| evaluate(s, &sc.workload, &opts)))
        });
        let base = Memo::new(move |_| scenario.with_value(|sc| state.with(|s| evaluate(s, &sc.workload, &EvalOptions::default()))));
        let goals = Memo::new(move |_| scenario.with_value(|sc| state.with(|s| base.with(|b| check_goals(s, &sc.workload, &sc.goals, Some(b))))));
        let solved_now = Memo::new(move |_| all_ok(&goals.get()) && state.with(|s| !s.nodes.is_empty()));
        let sel = RwSignal::new(None::<String>);
        let selected = Memo::new(move |_| sel.get().filter(|id| state.with(|s| s.node(id).is_some())));
        let fail_kinds = Memo::new(move |_| state.with(logic::fail_kinds));

        // отказ вида, которого на схеме больше нет, не предлагается в списке — и не считается
        Effect::new(move |_| {
            if let Some(f @ FailKind::Component(_)) = fail.get() {
                if !fail_kinds.with(|k| k.contains(&f)) {
                    fail.set(None);
                }
            }
        });

        Self {
            scenario,
            hint: StoredValue::new(hint),
            state,
            sel,
            sel_edge: RwSignal::new(None),
            notice: RwSignal::new(String::new()),
            down,
            fail,
            hint_open: RwSignal::new(false),
            help_open: RwSignal::new(false),
            fs: RwSignal::new(false),
            result,
            goals,
            solved_now,
            selected,
            fail_kinds,
            on_draft,
        }
    }

    pub fn scenario(&self) -> Arc<Scenario> {
        self.scenario.get_value()
    }

    /// Правит схему; `save` — записать черновик (при перетаскивании пишется только в конце).
    fn update(&self, f: impl FnOnce(&mut SdState), save: bool) {
        self.state.update(f);
        if save {
            self.persist();
        }
    }

    /// Отдаёт черновик хозяину (он отправит его на сервер с паузой).
    pub fn persist(&self) {
        self.on_draft.run(self.state.with_untracked(logic::draft_json));
    }

    pub fn select_node(&self, id: Option<String>) {
        self.sel.set(id);
        self.sel_edge.set(None);
    }

    pub fn select_edge(&self, edge: Option<SdEdge>) {
        if edge.is_some() {
            self.sel.set(None);
        }
        self.sel_edge.set(edge);
    }

    /// Ставит компонент (`at` — точка поля, иначе свободное место колонки) со связями `edges`; `false` — на схеме уже предел.
    pub fn add(&self, kind: Kind, at: Option<Point>, edges: &[SdEdge]) -> bool {
        let max = self.scenario().max_nodes();
        if self.state.with_untracked(|s| s.nodes.len()) >= max {
            self.notice.set(format!("На схеме не больше {max} компонентов."));
            return false;
        }
        self.notice.set(String::new());
        let mut id = String::new();
        self.update(|s| id = logic::add_node(s, kind, at, edges), true);
        self.select_node(Some(id));
        true
    }

    pub fn move_node(&self, id: &str, x: f64, y: f64, done: bool) {
        self.update(
            |s| {
                if let Some(n) = s.nodes.iter_mut().find(|n| n.id == id) {
                    n.x = x;
                    n.y = y;
                }
            },
            done,
        );
    }

    /// Соединяет `from → to`; причина отказа попадает в сообщение под полем.
    pub fn connect(&self, from: &str, to: &str) {
        let error = self.state.with_untracked(|s| match (s.node(from), s.node(to)) {
            (Some(a), Some(b)) => sdlab::ports::connect_error(s, a, b),
            _ => Some("Компонент не найден.".to_owned()),
        });
        match error {
            Some(e) => self.notice.set(e),
            None => {
                self.notice.set(String::new());
                self.update(|s| logic::add_edge(s, SdEdge::new(from, to)), true);
            }
        }
    }

    /// Добавляет связи, подставленные после перетаскивания существующего компонента.
    pub fn apply_edges(&self, edges: &[SdEdge]) {
        self.update(|s| edges.iter().cloned().for_each(|e| logic::add_edge(s, e)), true);
    }

    /// Можно ли «Удалить»: выбрана связь или компонент, кроме пользователей.
    pub fn can_delete(&self) -> bool {
        self.sel_edge.with(Option::is_some) || self.selected.get().is_some_and(|id| self.state.with(|s| logic::deletable(s, &id)))
    }

    /// Удаляет выбранную связь или компонент (без подписки на сигналы: вызывается из обработчиков событий).
    pub fn remove_selected(&self) {
        if let Some(edge) = self.sel_edge.get_untracked() {
            self.update(|s| s.edges.retain(|e| *e != edge), true);
            self.sel_edge.set(None);
            return;
        }
        let Some(id) = self.selected.get_untracked() else { return };
        if !self.state.with_untracked(|s| logic::deletable(s, &id)) {
            return;
        }
        self.update(|s| logic::remove_node(s, &id), true);
        self.sel.set(None);
        self.down.update(|d| d.retain(|x| *x != id));
    }

    pub fn set_param(&self, id: &str, key: &str, value: ParamValue) {
        self.update(
            |s| {
                if let Some(n) = s.nodes.iter_mut().find(|n| n.id == id) {
                    n.params.insert(key.to_owned(), value);
                }
            },
            true,
        );
    }

    /// Отключает или включает компонент (проверка отказа вручную).
    pub fn set_down(&self, id: &str, on: bool) {
        self.down.update(|d| {
            d.retain(|x| x != id);
            if on {
                d.push(id.to_owned());
            }
        });
    }

    /// Возвращает исходную схему упражнения.
    pub fn reset(&self) {
        let start = logic::initial_state(&self.scenario());
        self.state.set(start);
        self.persist();
        self.sel.set(None);
        self.sel_edge.set(None);
        self.down.set(Vec::new());
        self.fail.set(None);
        self.notice.set(String::new());
    }
}
