//! State of one scenario of the LVM board: the student's board, selection, the disk whose loss is shown, the derived statuses and goals, plus the
//! board actions (place, move, connect, delete, edit, reset). It is a set of signals copied into components as a whole; the edit logic lives in
//! `logic.rs`, the rules and statuses in the `virtlab::lvm_board` model.

use std::{collections::BTreeSet, sync::Arc};

use leptos::prelude::*;
use virtlab::lvm_board::{add_error, Edge, Evaluation, GoalResult, Kind, Param, Scenario, Topology};

use super::logic::{self, Loss};
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
    /// disk chosen in the "if a disk fails" panel
    pub loss_disk: RwSignal<Option<String>>,
    /// the loss of the chosen disk is shown
    pub loss_on: RwSignal<bool>,
    /// statuses of the objects under the workload of the scenario
    pub eval: Memo<Evaluation>,
    /// goals of the scenario on the board
    pub results: Memo<Vec<GoalResult>>,
    /// why the board is not acceptable at all
    pub invalid: Memo<Option<String>>,
    /// every goal holds and the board is acceptable
    pub solved_now: Memo<bool>,
    /// selected object, if it is on the board
    pub selected: Memo<Option<String>>,
    /// what the loss of the chosen disk takes with it (while it is shown)
    pub loss: Memo<Option<Loss>>,
    /// objects the shown loss takes (and the disk itself)
    pub lost: Memo<BTreeSet<String>>,
    persist: Callback<()>,
}

impl Lab {
    pub fn new(scenario: Arc<Scenario>, board: RwSignal<Topology>, persist: Callback<()>) -> Self {
        let scenario = StoredValue::new(scenario);
        let eval = Memo::new(move |_| scenario.with_value(|sc| board.with(|t| sc.evaluate(t))));
        let results = Memo::new(move |_| scenario.with_value(|sc| board.with(|t| sc.results(t))));
        let invalid = Memo::new(move |_| scenario.with_value(|sc| board.with(|t| sc.invalid(t))));
        let solved_now = Memo::new(move |_| invalid.with(Option::is_none) && results.with(|r| r.iter().all(|g| g.ok)));
        let sel = RwSignal::new(None::<String>);
        let selected = Memo::new(move |_| sel.get().filter(|id| board.with(|t| t.node(id).is_some())));
        let loss_disk = RwSignal::new(None::<String>);
        let loss_on = RwSignal::new(false);
        let loss = Memo::new(move |_| {
            let disk = loss_disk.get().filter(|_| loss_on.get())?;
            board.with(|t| t.node(&disk).is_some().then(|| eval.with(|ev| logic::loss(t, ev, &disk))))
        });
        let lost = Memo::new(move |_| {
            let mut set = loss.with(|l| l.as_ref().map(|l| l.lost.clone()).unwrap_or_default());
            if loss.with(Option::is_some) {
                set.extend(loss_disk.get());
            }
            set
        });
        Self {
            scenario,
            board,
            sel,
            sel_edge: RwSignal::new(None),
            notice: RwSignal::new(String::new()),
            hint_open: RwSignal::new(false),
            loss_disk,
            loss_on,
            eval,
            results,
            invalid,
            solved_now,
            selected,
            loss,
            lost,
            persist,
        }
    }

    pub fn scenario(&self) -> Arc<Scenario> {
        self.scenario.get_value()
    }

    pub fn id(&self) -> String {
        self.scenario.with_value(|s| s.id.clone())
    }

    /// Edits the board; `save` — write the draft and forget the shown loss (while dragging neither happens).
    fn update(&self, f: impl FnOnce(&mut Topology), save: bool) {
        self.board.update(f);
        if save {
            self.hide_loss();
            self.persist.run(());
        }
    }

    pub fn select_node(&self, id: Option<String>) {
        if let Some(disk) = id.as_deref().filter(|id| self.board.with_untracked(|t| t.node(id).is_some_and(|n| n.kind == Kind::Disk))) {
            if self.loss_disk.get_untracked().as_deref() != Some(disk) {
                self.loss_disk.set(Some(disk.to_owned()));
                self.hide_loss();
            }
        }
        self.sel.set(id);
        self.sel_edge.set(None);
    }

    pub fn select_edge(&self, edge: Option<Edge>) {
        if edge.is_some() {
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

    /// Sets a parameter of an object (any parameter of the model's table, see `virtlab::lvm_board::param_specs`).
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
        self.hide_loss();
        self.persist.run(());
        self.sel.set(None);
        self.sel_edge.set(None);
        self.notice.set(String::new());
    }

    // --- if a disk fails ---

    /// Chooses the disk of the "if a disk fails" panel (the shown loss goes away).
    pub fn choose_disk(&self, id: Option<String>) {
        self.loss_disk.set(id);
        self.hide_loss();
    }

    /// Shows what the loss of the chosen disk takes with it.
    pub fn show_loss(&self) {
        if self.loss_disk.get_untracked().is_some() {
            self.loss_on.set(true);
        }
    }

    /// Forgets the shown loss.
    pub fn hide_loss(&self) {
        if self.loss_on.get_untracked() {
            self.loss_on.set(false);
        }
    }
}
