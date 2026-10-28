//! State of the "System design" lab: the student's diagram, selection, failures, calculation and goals, plus the diagram actions
//! (place, connect, delete, change a parameter, reset). It is a set of signals copied into components
//! as a whole; the edit logic lives in `logic.rs`, the calculation in the `sdlab` crate.

use std::sync::Arc;

use leptos::prelude::*;
use sdlab::{all_ok, check_goals, evaluate, EvalOptions, EvalResult, FailKind, GoalResult, Kind, ParamValue, Scenario, SdEdge, SdState};

use super::logic;
use crate::components::labs::board_view::Point;

#[derive(Clone, Copy)]
pub struct Lab {
    scenario: StoredValue<Arc<Scenario>>,
    /// exercise hint
    pub hint: StoredValue<String>,
    /// student's diagram: both the draft and the solution
    pub state: RwSignal<SdState>,
    /// selected component (its parameters are in the floating card)
    pub sel: RwSignal<Option<String>>,
    /// selected link
    pub sel_edge: RwSignal<Option<SdEdge>>,
    /// message under the board (why a link was not placed, etc.)
    pub notice: RwSignal<String>,
    /// components disabled by hand
    pub down: RwSignal<Vec<String>>,
    /// failure being checked
    pub fail: RwSignal<Option<FailKind>>,
    pub hint_open: RwSignal<bool>,
    pub help_open: RwSignal<bool>,
    /// diagram in fullscreen
    pub fs: RwSignal<bool>,
    /// calculation with the failure and disabled nodes (for metrics and node load)
    pub result: Memo<EvalResult>,
    /// goals for the diagram without failures
    pub goals: Memo<Vec<GoalResult>>,
    /// all goals are met
    pub solved_now: Memo<bool>,
    /// selected component, if it is on the diagram
    pub selected: Memo<Option<String>>,
    /// failures by the component kinds present on the diagram
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

        // a failure of a kind no longer on the diagram is not offered in the list — and is not counted
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

    /// Edits the diagram; `save` — write the draft (while dragging it is written only at the end).
    fn update(&self, f: impl FnOnce(&mut SdState), save: bool) {
        self.state.update(f);
        if save {
            self.persist();
        }
    }

    /// Hands the draft to the owner (who will send it to the server after a pause).
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

    /// Places a component (`at` — a board point, otherwise a free spot in its column) with links `edges`; `false` — the diagram is already at the limit.
    pub fn add(&self, kind: Kind, at: Option<Point>, edges: &[SdEdge]) -> bool {
        let max = self.scenario().max_nodes();
        if self.state.with_untracked(|s| s.nodes.len()) >= max {
            self.notice.set(i18n::trf!("The diagram holds at most {0} components.", max));
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

    /// Connects `from → to`; the rejection reason goes to the message under the board.
    pub fn connect(&self, from: &str, to: &str) {
        let error = self.state.with_untracked(|s| match (s.node(from), s.node(to)) {
            (Some(a), Some(b)) => sdlab::ports::connect_error(s, a, b),
            _ => Some(i18n::tr("Component not found.").to_owned()),
        });
        match error {
            Some(e) => self.notice.set(e),
            None => {
                self.notice.set(String::new());
                self.update(|s| logic::add_edge(s, SdEdge::new(from, to)), true);
            }
        }
    }

    /// Adds links suggested after dragging an existing component.
    pub fn apply_edges(&self, edges: &[SdEdge]) {
        self.update(|s| edges.iter().cloned().for_each(|e| logic::add_edge(s, e)), true);
    }

    /// Whether "Delete" is available: a link or a component other than users is selected.
    pub fn can_delete(&self) -> bool {
        self.sel_edge.with(Option::is_some) || self.selected.get().is_some_and(|id| self.state.with(|s| logic::deletable(s, &id)))
    }

    /// Deletes the selected link or component (no signal subscription: called from event handlers).
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

    /// Disables or enables a component (manual failure check).
    pub fn set_down(&self, id: &str, on: bool) {
        self.down.update(|d| {
            d.retain(|x| x != id);
            if on {
                d.push(id.to_owned());
            }
        });
    }

    /// Returns the exercise's initial diagram.
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
