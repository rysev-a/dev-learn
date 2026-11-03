//! State of one scenario of the oVirt topology board: the student's board, selection, the shown message path, the derived statuses and
//! goals, plus the board actions (place, move, connect, delete, edit, reset, run an operation). It is a set of signals copied into
//! components as a whole; the edit logic lives in `logic.rs`, the rules and statuses in the `virtlab::ovirt_topo` model.

use std::sync::Arc;

use gloo_timers::future::TimeoutFuture;
use leptos::{prelude::*, task::spawn_local};
use virtlab::ovirt_topo::{add_error, evaluate, trace, Edge, Evaluation, GoalResult, Kind, Op, Param, Scenario, Topology, Trace};

use super::logic::{self, PathView};
use crate::components::labs::board_view::Point;

#[derive(Clone, Copy)]
pub struct Lab {
    scenario: StoredValue<Arc<Scenario>>,
    /// the student's board: both the draft and the solution
    pub board: RwSignal<Topology>,
    /// selected object
    pub sel: RwSignal<Option<String>>,
    /// selected link
    pub sel_edge: RwSignal<Option<Edge>>,
    /// message under the board (why a link was refused, what was dropped)
    pub notice: RwSignal<String>,
    pub hint_open: RwSignal<bool>,
    /// operation whose path is shown
    pub op: RwSignal<Option<Op>>,
    /// hop being shown (the path up to it is highlighted); none — the whole path
    pub active: RwSignal<Option<usize>>,
    /// the hops are being played one by one
    pub playing: RwSignal<bool>,
    /// number of the current animation: a running one with another number stops
    generation: StoredValue<u64>,
    /// statuses of the objects
    pub eval: Memo<Evaluation>,
    /// goals of the scenario on the board
    pub results: Memo<Vec<GoalResult>>,
    /// why the board is not acceptable at all
    pub invalid: Memo<Option<String>>,
    /// every goal holds and the board is acceptable
    pub solved_now: Memo<bool>,
    /// selected object, if it is on the board
    pub selected: Memo<Option<String>>,
    /// path of the operation
    pub trace: Memo<Option<Trace>>,
    /// what the shown part of the path highlights
    pub path: Memo<PathView>,
    persist: Callback<()>,
}

impl Lab {
    pub fn new(scenario: Arc<Scenario>, board: RwSignal<Topology>, persist: Callback<()>) -> Self {
        let scenario = StoredValue::new(scenario);
        let eval = Memo::new(move |_| board.with(evaluate));
        let results = Memo::new(move |_| scenario.with_value(|sc| board.with(|t| sc.results(t))));
        let invalid = Memo::new(move |_| scenario.with_value(|sc| board.with(|t| sc.invalid(t))));
        let solved_now = Memo::new(move |_| invalid.with(Option::is_none) && results.with(|r| r.iter().all(|g| g.ok)));
        let sel = RwSignal::new(None::<String>);
        let selected = Memo::new(move |_| sel.get().filter(|id| board.with(|t| t.node(id).is_some())));
        let op = RwSignal::new(None::<Op>);
        let active = RwSignal::new(None::<usize>);
        let trace = Memo::new(move |_| op.get().map(|o| board.with(|t| eval.with(|ev| trace(t, ev, &o)))));
        let path = Memo::new(move |_| match trace.get() {
            Some(tr) => board.with(|t| logic::path_view(t, &tr, active.get())),
            None => PathView::default(),
        });
        let lab = Self {
            scenario,
            board,
            sel,
            sel_edge: RwSignal::new(None),
            notice: RwSignal::new(String::new()),
            hint_open: RwSignal::new(false),
            op,
            active,
            playing: RwSignal::new(false),
            generation: StoredValue::new(0),
            eval,
            results,
            invalid,
            solved_now,
            selected,
            trace,
            path,
            persist,
        };
        on_cleanup(move || {
            let _ = lab.generation.try_update_value(|g| *g += 1);
        });
        lab
    }

    pub fn scenario(&self) -> Arc<Scenario> {
        self.scenario.get_value()
    }

    pub fn id(&self) -> String {
        self.scenario.with_value(|s| s.id.clone())
    }

    /// Edits the board; `save` — write the draft and forget the shown path (while dragging neither happens).
    fn update(&self, f: impl FnOnce(&mut Topology), save: bool) {
        self.board.update(f);
        if save {
            self.clear_path();
            self.persist.run(());
        }
    }

    pub fn select_node(&self, id: Option<String>) {
        if self.sel.get_untracked() != id {
            self.clear_path();
        }
        self.sel.set(id);
        self.sel_edge.set(None);
    }

    pub fn select_edge(&self, edge: Option<Edge>) {
        if edge.is_some() {
            self.clear_path();
            self.sel.set(None);
        }
        self.sel_edge.set(edge);
    }

    /// Places an object (`at` — a board point, otherwise a free spot in its column); `false` — the model refused it.
    pub fn add(&self, kind: Kind, at: Option<Point>) -> bool {
        let max = self.scenario.with_value(|s| s.max_nodes as usize);
        if let Some(e) = self.board.with_untracked(|t| add_error(t, kind, max)) {
            self.notice.set(e);
            return false;
        }
        self.notice.set(String::new());
        let mut id = String::new();
        self.update(|t| id = logic::add_node(t, kind, at), true);
        self.select_node(Some(id));
        true
    }

    pub fn move_node(&self, id: &str, x: f64, y: f64, done: bool) {
        self.update(
            |t| {
                if let Some(n) = t.nodes.iter_mut().find(|n| n.id == id) {
                    n.x = x;
                    n.y = y;
                }
            },
            done,
        );
    }

    /// Joins two objects (the direction comes from the model); the refusal reason goes to the message under the board.
    pub fn connect(&self, a: &str, b: &str) -> bool {
        match self.board.with_untracked(|t| logic::link_check(t, a, b)) {
            Err(e) => {
                self.notice.set(e);
                false
            }
            Ok((from, to)) => {
                self.notice.set(String::new());
                self.update(|t| t.edges.push(Edge::new(&from, &to)), true);
                true
            }
        }
    }

    /// Whether "Delete" is available: an object or a link is selected.
    pub fn can_delete(&self) -> bool {
        self.sel_edge.with(Option::is_some) || self.selected.get().is_some()
    }

    fn dropped_notice(&self, dropped: usize) {
        self.notice.set(if dropped > 0 { i18n::trf!("{0} dependent link(s) were removed as well.", dropped) } else { String::new() });
    }

    /// Deletes the selected link or object (no signal subscription: called from event handlers).
    pub fn remove_selected(&self) {
        let mut dropped = 0;
        if let Some(edge) = self.sel_edge.get_untracked() {
            self.update(|t| dropped = logic::remove_edge(t, &edge), true);
            self.sel_edge.set(None);
        } else if let Some(id) = self.selected.get_untracked() {
            self.update(|t| dropped = logic::remove_node(t, &id), true);
            self.sel.set(None);
        } else {
            return;
        }
        self.dropped_notice(dropped);
    }

    pub fn rename(&self, id: &str, name: &str) {
        let name = logic::clamp_name(name);
        self.update(
            |t| {
                if let Some(n) = t.nodes.iter_mut().find(|n| n.id == id) {
                    n.name = name;
                }
            },
            true,
        );
    }

    /// Sets a parameter of an object (any parameter of the model's table, see `virtlab::ovirt_topo::param_specs`).
    pub fn set_param(&self, id: &str, key: &str, value: Param) {
        self.update(
            |t| {
                if let Some(n) = t.nodes.iter_mut().find(|n| n.id == id) {
                    n.params.insert(key.to_owned(), value);
                }
            },
            true,
        );
    }

    /// Returns the scenario's starting board.
    pub fn reset(&self) {
        let start = self.scenario.with_value(|s| s.start.clone());
        self.board.set(start);
        self.clear_path();
        self.persist.run(());
        self.sel.set(None);
        self.sel_edge.set(None);
        self.notice.set(String::new());
    }

    // --- the path of a message ---

    /// Follows an operation over the board: the whole path is shown.
    pub fn run_op(&self, op: Op) {
        self.stop();
        self.active.set(None);
        self.op.set(Some(op));
    }

    /// Forgets the shown path.
    pub fn clear_path(&self) {
        self.stop();
        self.active.set(None);
        if self.op.get_untracked().is_some() {
            self.op.set(None);
        }
    }

    /// Shows the path up to hop `i` (a click on a hop of the list).
    pub fn show_hop(&self, i: usize) {
        self.stop();
        self.active.set(Some(i));
    }

    /// Stops the animation (the shown part of the path stays).
    pub fn stop(&self) {
        self.generation.update_value(|g| *g += 1);
        if self.playing.get_untracked() {
            self.playing.set(false);
        }
    }

    /// Plays the hops one by one from the first.
    pub fn play(&self) {
        let Some(n) = self.trace.with_untracked(|t| t.as_ref().map(|t| t.hops.len())).filter(|n| *n > 0) else { return };
        self.stop();
        self.active.set(Some(0));
        if n < 2 {
            return;
        }
        self.playing.set(true);
        let (lab, mine) = (*self, self.generation.get_value());
        spawn_local(async move {
            for i in 1..n {
                TimeoutFuture::new(logic::HOP_MS).await;
                if lab.generation.try_get_value() != Some(mine) {
                    return;
                }
                lab.active.set(Some(i));
            }
            lab.playing.set(false);
        });
    }
}
