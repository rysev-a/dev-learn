//! Scenarios for the Python tasks of level 3 (`fix(board)` in the chapter 12): not an exercise of the board, so the pack is not listed in
//! [`PACKS`](super::PACKS) and has no lab data. Each scenario is a reference board of a real pack with some links taken away: the code has to put
//! the links back by the naming rules of the statement of the task `nb12-wire-network`, and the goals are the ones of the source scenario.

use super::{bond, bridge, nat, Built};
use crate::net_board::{Scenario, Topology};

/// The identifier a task names in its `board_check`.
pub const ID: &str = "virt-fix-net";

/// `(new id, source pack, source scenario, links taken away)`.
type Source = (&'static str, fn() -> Built, &'static str, &'static [(&'static str, &'static str)]);

const SOURCES: &[Source] = &[
    ("veth-pair", bridge::build, "two-namespaces", &[("host", "v2h"), ("v2h", "v2c"), ("v2h", "br0"), ("ns2", "v2c")]),
    ("container", nat::build, "build", &[("host", "br0"), ("host", "v1h"), ("v1h", "br0"), ("ns1", "v1c"), ("v1h", "v1c")]),
    ("bond-slaves", bond::build, "build-bond", &[("host", "bond0"), ("eth2", "bond0"), ("host", "eth2")]),
    ("vm-on-bond", bond::build, "bond-bridge", &[("host", "br0"), ("vm1", "br0"), ("bond0", "br0"), ("eth1", "bond0")]),
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
