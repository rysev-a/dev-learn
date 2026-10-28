//! State of the "Computer Networks" lab: the learner's network, selection and modes, the last probe with its animation, terminals and
//! goals. Actions on the network live here too: editing settings, cables, terminal commands, showing a packet's path for a goal.
//!
//! Rules this file upholds:
//! * any edit of settings or cables goes through [`Lab::edit`]/[`Lab::connect`]/…: they recompute goals, reset
//!   "checked" and send the draft to the host;
//! * dragging a device and simulator caches (ARP, MAC tables) change the network but do not recompute goals.

use std::collections::HashMap;
use std::sync::Arc;

use leptos::prelude::*;
use netlab::check::{run_probe, GoalKind};
use netlab::term::exec;
use netlab::transfer::TransferChart;
use netlab::types::{Device, NetState};
use netlab::{check_goals, NetSpec, Tools};

use super::logic::{self, GoalView, RunView};

/// A terminal line: an entered command or output.
#[derive(Clone, Debug, PartialEq)]
pub struct TermLine {
    pub cmd: bool,
    pub text: String,
}

/// The lab: a set of signals, copied into components as is.
#[derive(Clone, Copy)]
pub struct Lab {
    pub net: RwSignal<NetState>,
    spec: StoredValue<Arc<NetSpec>>,
    tools: StoredValue<Tools>,
    hint: StoredValue<String>,
    on_draft: Callback<String>,
    /// selected device
    pub sel: RwSignal<String>,
    /// cable laying mode is on
    pub cable: RwSignal<bool>,
    /// first device of the future cable
    pub cable_from: RwSignal<Option<String>>,
    /// selected cable (index)
    pub sel_link: RwSignal<Option<usize>>,
    pub notice: RwSignal<String>,
    pub hint_open: RwSignal<bool>,
    /// the learner has already changed something: until then goals are shown as numbers rather than marks
    pub touched: RwSignal<bool>,
    /// "Check" was pressed: if not everything is met, show a hint under the goals
    pub checked: RwSignal<bool>,
    /// settings version: grows on every edit, goals are recomputed from it
    rev: RwSignal<u64>,
    pub terms: RwSignal<HashMap<String, Vec<TermLine>>>,
    pub run: RwSignal<Option<RunView>>,
    /// animation position in "moments"
    pub slot: RwSignal<f64>,
    pub chart: RwSignal<Option<TransferChart>>,
    /// playback number: a new playback cancels the previous animation
    anim: StoredValue<u64>,
    /// goal results
    pub goals: Memo<Vec<GoalView>>,
    /// all goals are met
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

    /// Device by id (a copy).
    pub fn device(&self, id: &str) -> Option<Device> {
        self.net.with(|n| n.devices.get(id).cloned())
    }

    /// Device name for the log: the name, or the id if there is no device.
    pub fn name_of(&self, id: &str) -> String {
        self.net.with(|n| n.devices.get(id).map(|d| d.name.clone())).unwrap_or_else(|| id.to_string())
    }

    /// Network state as the solution JSON.
    pub fn solution_json(&self) -> String {
        self.net.with_untracked(logic::draft_json)
    }

    fn save(&self) {
        self.on_draft.run(self.solution_json());
    }

    /// Settings or cables changed: recompute goals, clear "checked", save the draft.
    fn changed(&self) {
        self.rev.update(|r| *r += 1);
        self.touched.set(true);
        self.checked.set(false);
        self.save();
    }

    /// Change the network with a function and return its result (usually an error text).
    pub fn edit<T>(&self, f: impl FnOnce(&mut NetState) -> T) -> T {
        let mut out = None;
        self.net.update(|n| out = Some(f(n)));
        self.changed();
        out.expect("update always calls the closure")
    }

    /// Change a single device.
    pub fn edit_device<T>(&self, id: &str, f: impl FnOnce(&mut Device) -> T) -> Option<T> {
        self.edit(|n| n.devices.get_mut(id).map(f))
    }

    /// Move a device on the board (goals are not recomputed).
    pub fn move_device(&self, id: &str, x: f64, y: f64) {
        self.net.update(|n| {
            if let Some(d) = n.devices.get_mut(id) {
                d.x = x;
                d.y = y;
            }
        });
    }

    /// End of dragging: save the draft with the new position.
    pub fn moved(&self) {
        self.touched.set(true);
        self.save();
    }

    /* ---- cables ---- */

    /// Select a device and clear the cable selection.
    pub fn select(&self, id: &str) {
        self.sel.set(id.to_string());
        self.sel_link.set(None);
    }

    /// Lay a cable between the first free ports; an error goes to "notice".
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

    /* ---- commands ---- */

    /// Terminal command: output to the device history, probe to the animation, chart under the board.
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

    /// Command from a NAT/firewall/service form: the same as the terminal, but the output is right here under the form.
    pub fn form_exec(&self, dev: &str, line: &str) -> String {
        let mut res = None;
        self.net.update(|n| res = Some(exec(n, dev, line)));
        let Some(res) = res else { return String::new() };
        if res.changed == Some(true) {
            self.changed();
        }
        res.out
    }

    /* ---- animation ---- */

    /// Show a packet's path: `None` removes it.
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

    /// Start the packets running; outside the browser (in tests) playback goes straight to the end.
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

    /// Stop the animation (when leaving the page).
    pub fn stop(&self) {
        self.anim.try_update_value(|a| *a += 1);
    }

    /// Show a packet's path for a goal (the ▶ button): the probe runs on a copy of the network, and its caches (ARP, MAC) stay in the network.
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

    /// Restore the initial network and clear everything the learner sees.
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
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/net");
        let mut out = Vec::new();
        let Ok(entries) = std::fs::read_dir(&dir) else { return out };
        for e in entries.filter_map(Result::ok) {
            let v: Value = serde_json::from_str(&std::fs::read_to_string(e.path()).expect("data file")).expect("JSON");
            for t in v["tasks"].as_array().expect("exercises") {
                let spec: NetSpec = serde_json::from_value(t["spec"].clone()).expect("scenario");
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
        let on_draft = Callback::new(move |d: String| sink.lock().expect("lock").push(d));
        let lab = Lab::new(Arc::new(spec.clone()), spec.start_state(), String::new(), on_draft, false);
        (owner, lab, drafts)
    }

    /// For every exercise the initial network does not meet the goals and the reference does: the solution assembled by the lab is accepted
    /// by the server check too.
    #[test]
    fn every_exercise_goes_from_unsolved_to_solved_and_the_server_accepts_it() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let all = specs();
        assert!(all.is_empty() || all.len() >= 70, "expected ≈79 exercises, found {}", all.len());
        for (id, spec) in all {
            let (_owner, lab, drafts) = lab_of(&spec);
            assert!(!lab.solved_now.get_untracked(), "{id}: the initial network must not meet the goals");
            let solved = spec.solved_state().unwrap_or_else(|e| panic!("{id}: {e}"));
            lab.net.set(solved);
            lab.edit(|_| ());
            assert!(lab.solved_now.get_untracked(), "{id}: the reference must meet the goals: {:?}", lab.goals.get_untracked());
            assert!(lab.touched.get_untracked());
            assert_eq!(drafts.lock().expect("lock").len(), 1, "{id}: an edit saves the draft");
            let verdict = verify_json(&spec, &lab.solution_json());
            assert!(verdict.ok, "{id}: the server did not accept the solution: {verdict:?}");
            // "Reset" restores the initial network and the goals are unmet again
            lab.reset();
            assert!(!lab.solved_now.get_untracked(), "{id}");
            assert!(!lab.touched.get_untracked());
        }
    }

    #[test]
    fn cable_and_terminal_commands_change_the_network_and_goals() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let Some((id, spec)) = specs().into_iter().find(|(_, s)| s.tools.cable) else { return };
        let (_owner, lab, drafts) = lab_of(&spec);
        let before = lab.net.with_untracked(|n| n.links.len());
        // a device with no free ports, or with itself, is an error; the network does not change
        let first = lab.net.with_untracked(|n| n.devices.iter().next().map(|d| d.id.clone())).expect("device");
        assert!(!lab.connect(&first, &first), "{id}");
        assert!(!lab.notice.get_untracked().is_empty());
        assert_eq!(lab.net.with_untracked(|n| n.links.len()), before);
        assert!(drafts.lock().expect("lock").is_empty());
        // a terminal command writes the device history
        lab.terminal_run(&first, "hostname");
        let lines = lab.terms.with_untracked(|t| t.get(&first).cloned().unwrap_or_default());
        assert_eq!(lines.len(), 2);
        assert!(lines[0].cmd && !lines[1].cmd);
        lab.terminal_run(&first, "clear");
        assert!(lab.terms.with_untracked(|t| t.get(&first).cloned().unwrap_or_default()).is_empty());
        // removing a cable
        if before > 0 {
            lab.sel_link.set(Some(0));
            lab.remove_link();
            assert_eq!(lab.net.with_untracked(|n| n.links.len()), before - 1);
            assert!(lab.sel_link.get_untracked().is_none());
        }
    }

    #[test]
    fn ping_goal_plays_a_run_and_keeps_caches() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let Some((_, spec)) = specs().into_iter().find(|(_, s)| s.goals.iter().any(|g| matches!(g.kind, netlab::GoalKind::Ping(_)))) else { return };
        let (_owner, lab, _) = lab_of(&spec);
        let idx = spec.goals.iter().position(|g| matches!(g.kind, netlab::GoalKind::Ping(_))).expect("ping goal");
        lab.play_goal(idx);
        assert!(lab.run.with_untracked(|r| r.is_some()), "packet path is shown");
        assert!(lab.slot.get_untracked() > 0.0);
        let title = lab.run.with_untracked(|r| r.as_ref().map(|r| r.title.clone())).unwrap_or_default();
        assert_eq!(title, spec.goals[idx].text);
    }
}
