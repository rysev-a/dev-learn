//! Exercises of the network board: the packs of scenarios, one pack per exercise. A pack lives in its own file and is registered here;
//! a pack without scenarios is not an exercise yet.

mod bond;
mod bridge;
pub(crate) mod builder;
mod nat;

use std::collections::BTreeMap;

use super::{Scenario, Topology};

/// Scenarios of a pack and the reference boards by scenario identifier.
pub type Built = (Vec<Scenario>, BTreeMap<String, Topology>);

/// A pack of scenarios: the exercise identifier, the chapter it belongs to and the function that builds it.
pub struct PackDef {
    /// Exercise identifier (`virt-sim-net-…`).
    pub id: &'static str,
    /// Chapter of the book 19.
    pub chapter: u32,
    build: fn() -> Built,
}

/// All packs, in the order of the chapters.
pub const PACKS: &[PackDef] = &[
    PackDef { id: "virt-sim-net-bridge", chapter: 10, build: bridge::build },
    PackDef { id: "virt-sim-net-bond", chapter: 11, build: bond::build },
    PackDef { id: "virt-sim-net-nat", chapter: 12, build: nat::build },
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
