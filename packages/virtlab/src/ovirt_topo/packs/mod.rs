//! Exercises of the topology board: the packs of scenarios, one pack per exercise. A pack lives in its own file and is registered here;
//! a pack without scenarios is not an exercise yet.

mod affinity;
mod backup;
pub(crate) mod builder;
mod capacity;
mod clusters;
mod dr;
mod evacuate;
mod fencing;
mod ha;
mod net;
mod net2;
mod net3;
mod perms;
mod puzzles;
mod storage;
mod storage2;
mod storage3;
mod topo;
mod triage;
mod triage2;

use std::collections::BTreeMap;

use super::{Scenario, Topology};

/// Scenarios of a pack and the reference boards by scenario identifier.
pub type Built = (Vec<Scenario>, BTreeMap<String, Topology>);

/// A pack of scenarios: the exercise identifier, the chapter it belongs to and the function that builds it.
pub struct PackDef {
    /// Exercise identifier (`virt-sim-ovirt-…`).
    pub id: &'static str,
    /// Chapter of the book 17.
    pub chapter: u32,
    build: fn() -> Built,
}

/// All packs, in the order of the chapters.
pub const PACKS: &[PackDef] = &[
    PackDef { id: "virt-sim-ovirt-topo", chapter: 17, build: topo::build },
    PackDef { id: "virt-sim-ovirt-storage", chapter: 20, build: storage::build },
    PackDef { id: "virt-sim-ovirt-net", chapter: 21, build: net::build },
    PackDef { id: "virt-sim-ovirt-clusters", chapter: 17, build: clusters::build },
    PackDef { id: "virt-sim-ovirt-puzzles", chapter: 17, build: puzzles::build },
    PackDef { id: "virt-sim-ovirt-perms", chapter: 18, build: perms::build },
    PackDef { id: "virt-sim-ovirt-fencing", chapter: 19, build: fencing::build },
    PackDef { id: "virt-sim-ovirt-ha", chapter: 19, build: ha::build },
    PackDef { id: "virt-sim-ovirt-storage-2", chapter: 20, build: storage2::build },
    PackDef { id: "virt-sim-ovirt-storage-3", chapter: 20, build: storage3::build },
    PackDef { id: "virt-sim-ovirt-net-2", chapter: 21, build: net2::build },
    PackDef { id: "virt-sim-ovirt-net-3", chapter: 21, build: net3::build },
    PackDef { id: "virt-sim-ovirt-affinity", chapter: 22, build: affinity::build },
    PackDef { id: "virt-sim-ovirt-capacity", chapter: 22, build: capacity::build },
    PackDef { id: "virt-sim-ovirt-evacuate", chapter: 22, build: evacuate::build },
    PackDef { id: "virt-sim-ovirt-backup", chapter: 24, build: backup::build },
    PackDef { id: "virt-sim-ovirt-dr", chapter: 24, build: dr::build },
    PackDef { id: "virt-sim-ovirt-triage", chapter: 25, build: triage::build },
    PackDef { id: "virt-sim-ovirt-triage-2", chapter: 25, build: triage2::build },
];

/// The scenarios of a pack by the exercise identifier and the reference boards (never sent to the client); `None` for an unknown or empty pack.
pub fn pack(id: &str) -> Option<Built> {
    let def = PACKS.iter().find(|p| p.id == id)?;
    let built = (def.build)();
    (!built.0.is_empty()).then_some(built)
}

/// Identifiers of the packs that have scenarios, in the order of the chapters.
pub fn pack_ids() -> Vec<&'static str> {
    PACKS.iter().filter(|p| pack(p.id).is_some()).map(|p| p.id).collect()
}

/// The chapter of a pack.
pub fn pack_chapter(id: &str) -> Option<u32> {
    PACKS.iter().find(|p| p.id == id).map(|p| p.chapter)
}

/// Scenarios of chapter 17 (the first pack).
pub fn default_scenarios() -> Vec<Scenario> {
    topo::build().0
}

/// Reference boards of chapter 17 by the scenario identifier.
pub fn default_solution() -> BTreeMap<String, Topology> {
    topo::build().1
}
