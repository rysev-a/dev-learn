//! Scenarios for the Python tasks of level 3 (`fix(board)` in the chapter 16): not an exercise of the board, so the pack is not listed in
//! [`PACKS`](super::PACKS) and has no lab data. Each scenario is a reference board of a real pack with some links taken away: the code has to put
//! the links back by a rule (see the statement of the task `lvb16-wire-stack`), and the goals are the ones of the source scenario.

use super::{grow, resilience, snapshots, Built};
use crate::lvm_board::{Scenario, Topology};

/// The identifier a task names in its `board_check`.
pub const ID: &str = "virt-fix-lvm";

/// `(new id, source pack, source scenario, links taken away)`.
type Source = (&'static str, fn() -> Built, &'static str, &'static [(&'static str, &'static str)]);

const SOURCES: &[Source] = &[
    ("loose-disk", grow::build, "build", &[("d2", "pv2"), ("pv2", "vg"), ("vg", "data")]),
    ("vm-group", resilience::build, "vm-disks", &[("d2", "pv2"), ("pv2", "vg"), ("vg", "vm2-disk")]),
    ("thin-stack", snapshots::build, "thin-snapshot", &[("d1", "pv1"), ("vg", "pool"), ("pool", "vm-disk"), ("vm-disk", "snap")]),
    ("cow-origin", snapshots::build, "cow-size", &[("d1", "pv1"), ("pv1", "vg"), ("data", "snap")]),
];

/// The scenarios and the reference boards (the boards of the source scenarios).
pub fn build() -> Built {
    let mut scenarios: Vec<Scenario> = Vec::new();
    let mut solutions = std::collections::BTreeMap::new();
    for (id, source, from, drop) in SOURCES {
        let (scs, sols) = source();
        let Some(sc) = scs.into_iter().find(|s| s.id == *from) else { continue };
        let solution: Topology = sols[*from].clone();
        let mut start = solution.clone();
        start.edges.retain(|e| !drop.iter().any(|(a, b)| e.from == *a && e.to == *b));
        let mut s = sc;
        s.id = (*id).to_string();
        s.start = start;
        scenarios.push(s);
        solutions.insert((*id).to_string(), solution);
    }
    (scenarios, solutions)
}
