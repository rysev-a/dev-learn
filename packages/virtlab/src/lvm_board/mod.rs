//! LVM board (book 19, chapters 16 and 20): the student assembles the storage of a server — disks, physical volumes, a volume group,
//! logical volumes, thin pools, snapshots, filesystems and the VM disks on them — and links the objects. The model ([`evaluate`]) derives what
//! follows from the links: how many extents the group has, whether a volume fits, whether the filesystem is as large as its volume, whether a
//! snapshot overflowed under the write load of the scenario, how full a thin pool is, and what a lost disk takes with it.
//!
//! These are the **rules of the lab**, not a copy of LVM. The arithmetic follows the tasks of chapter 16: a physical volume of `S` MiB has
//! `(S - 1) // pe` usable extents (the first MiB holds the label and the metadata area), a volume takes its size rounded up to whole extents,
//! volumes are placed first-fit in the order of the board (a linear volume may span physical volumes, a mirror puts each of its two legs on a
//! physical volume of its own), and a thin pool takes its data and its metadata from the group. Sizes are in GiB, extents in MiB.
//!
//! The solution of a scenario is the whole [`Topology`]; the server checks it with the same functions ([`Scenario::reached`]).

mod eval;
mod goals;
mod judge;
mod layout;
mod packs;
mod params;
mod rules;

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

pub use eval::{
    evaluate, evacuable, lost_by_disk, survives_disk_loss, Evaluation, FsEval, FsStatus, Piece, PoolEval, PoolStatus, PvEval,
    PvStatus, SnapEval, SnapStatus, VgEval, VgStatus, VmEval, VmStatus, VolEval, VolStatus, Why, Workload,
};
pub use goals::{GoalResult, LvmGoal, Scenario};
pub use judge::{find as scenario_of, judge, Judgement};
pub use layout::{auto_layout, column, next_pos, NODE_H, NODE_W};
pub(crate) use params::raw_specs;
pub use packs::{pack, pack_chapter, pack_ids, PackDef, FIX_PACK, PACKS};
pub use params::{param_error, param_specs, param_to_text, ParamOption, ParamSpec, ParamTy};
pub use rules::{add_error, connect_error, problems, prune, rel, Problem, Rel};

/// The most objects on a board (a bound for the server check).
pub const MAX_NODES: usize = 40;
/// The longest object name.
pub const MAX_NAME: usize = 40;

/// Kind of an object.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Kind {
    /// A disk (a block device).
    Disk,
    /// A physical volume: a disk prepared for LVM (`pvcreate`).
    Pv,
    /// A volume group: the pool of extents of its physical volumes.
    Vg,
    /// A logical volume.
    Lv,
    /// A thin pool: a logical volume that thin volumes share.
    ThinPool,
    /// A thin volume: a virtual size over a thin pool.
    ThinLv,
    /// A snapshot of a logical volume (copy-on-write) or of a thin volume.
    Snapshot,
    /// A filesystem on a volume.
    Fs,
    /// A virtual machine that uses volumes as its disks.
    Vm,
}

impl Kind {
    /// All kinds in the order of the palette.
    pub const ALL: [Kind; 9] =
        [Kind::Disk, Kind::Pv, Kind::Vg, Kind::Lv, Kind::ThinPool, Kind::ThinLv, Kind::Snapshot, Kind::Fs, Kind::Vm];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            Kind::Disk => "disk",
            Kind::Pv => "pv",
            Kind::Vg => "vg",
            Kind::Lv => "lv",
            Kind::ThinPool => "thin_pool",
            Kind::ThinLv => "thin_lv",
            Kind::Snapshot => "snapshot",
            Kind::Fs => "fs",
            Kind::Vm => "vm",
        }
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Kind::Disk => i18n::tr("disk"),
            Kind::Pv => i18n::tr("physical volume"),
            Kind::Vg => i18n::tr("volume group"),
            Kind::Lv => i18n::tr("logical volume"),
            Kind::ThinPool => i18n::tr("thin pool"),
            Kind::ThinLv => i18n::tr("thin volume"),
            Kind::Snapshot => i18n::tr("snapshot"),
            Kind::Fs => i18n::tr("filesystem"),
            Kind::Vm => i18n::tr("VM"),
        }
    }

    /// A volume: something a filesystem, a snapshot or a VM can sit on.
    pub fn is_volume(self) -> bool {
        matches!(self, Kind::Lv | Kind::ThinLv)
    }
}

/// Parameter of an object.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Param {
    /// Switch.
    Bool(bool),
    /// Choice from a list.
    Str(String),
}

/// Object on the board.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Node {
    /// Identifier, unique on the board.
    pub id: String,
    /// Kind.
    pub kind: Kind,
    /// Name shown on the board.
    pub name: String,
    /// Position of the centre (boards given as task data have none: `auto_layout` places them).
    #[serde(default)]
    pub x: f64,
    /// Position of the centre.
    #[serde(default)]
    pub y: f64,
    /// Parameters (`size` of a disk, `pe` of a group, …).
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub params: BTreeMap<String, Param>,
}

impl Node {
    /// A node without parameters.
    pub fn new(id: &str, kind: Kind, name: &str, x: f64, y: f64) -> Node {
        Node { id: id.into(), kind, name: name.into(), x, y, params: BTreeMap::new() }
    }

    /// The value of a parameter as text, with the default when it is unset or not allowed (`true` / `false` for a switch). A key the kind
    /// does not have reads as the stored value, or as an empty text.
    pub fn param_text(&self, key: &str) -> String {
        let stored = self.params.get(key);
        match raw_specs(self.kind).iter().find(|s| s.key == key) {
            Some(spec) => match stored {
                Some(p) if spec.accepts(p) => param_to_text(p),
                _ => spec.default.to_string(),
            },
            None => stored.map(param_to_text).unwrap_or_default(),
        }
    }

    /// A switch parameter (the default of the kind when unset).
    pub fn flag(&self, key: &str) -> bool {
        self.param_text(key) == "true"
    }

    /// A numeric parameter (0 when it is not a number).
    pub fn num(&self, key: &str) -> u64 {
        self.param_text(key).parse().unwrap_or(0)
    }

    /// Set a parameter (builder style).
    pub fn with_param(mut self, key: &str, value: Param) -> Node {
        self.params.insert(key.into(), value);
        self
    }

    /// Size in GiB: the capacity of a disk, a volume, a pool, a snapshot or a filesystem (0 for other kinds).
    pub fn size_gib(&self) -> u64 {
        match self.kind {
            Kind::Disk | Kind::Lv | Kind::ThinPool | Kind::ThinLv | Kind::Snapshot | Kind::Fs => self.num("size"),
            _ => 0,
        }
    }

    /// Extent size of a group in MiB (4 unless set).
    pub fn pe_mib(&self) -> u64 {
        if self.kind == Kind::Vg {
            self.num("pe").max(1)
        } else {
            4
        }
    }

    /// A volume keeps two copies of its data on different physical volumes.
    pub fn mirrored(&self) -> bool {
        self.kind == Kind::Lv && self.num("mirror") == 2
    }
}

/// Link between two objects; the direction is fixed by the kinds (see [`rel`]).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Edge {
    /// Identifier of the source object.
    pub from: String,
    /// Identifier of the target object.
    pub to: String,
}

impl Edge {
    /// A link.
    pub fn new(from: &str, to: &str) -> Edge {
        Edge { from: from.into(), to: to.into() }
    }
}

/// What the student builds: objects and links. It is also the draft and the solution.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct Topology {
    /// Objects.
    pub nodes: Vec<Node>,
    /// Links.
    pub edges: Vec<Edge>,
}

impl Topology {
    /// Object by identifier.
    pub fn node(&self, id: &str) -> Option<&Node> {
        self.nodes.iter().find(|n| n.id == id)
    }

    /// Objects of a kind, in board order.
    pub fn of_kind(&self, kind: Kind) -> impl Iterator<Item = &Node> {
        self.nodes.iter().filter(move |n| n.kind == kind)
    }

    /// The link exists.
    pub fn linked(&self, from: &str, to: &str) -> bool {
        self.edges.iter().any(|e| e.from == from && e.to == to)
    }

    /// Targets of the links of a relation that start at `from`, in board order.
    pub fn targets(&self, from: &str, r: Rel) -> Vec<&Node> {
        let Some(from_kind) = self.node(from).map(|n| n.kind) else { return vec![] };
        self.nodes
            .iter()
            .filter(|n| self.linked(from, &n.id) && rel(from_kind, n.kind) == Some(r))
            .collect()
    }

    /// Sources of the links of a relation that end at `to`, in board order.
    pub fn sources(&self, to: &str, r: Rel) -> Vec<&Node> {
        let Some(to_kind) = self.node(to).map(|n| n.kind) else { return vec![] };
        self.nodes.iter().filter(|n| self.linked(&n.id, to) && rel(n.kind, to_kind) == Some(r)).collect()
    }

    /// The board without an object and the links of it (the object is gone: a disk that failed, a volume that was removed).
    pub fn without(&self, id: &str) -> Topology {
        Topology {
            nodes: self.nodes.iter().filter(|n| n.id != id).cloned().collect(),
            edges: self.edges.iter().filter(|e| e.from != id && e.to != id).cloned().collect(),
        }
    }

    /// Volume group of a physical volume.
    pub fn vg_of_pv(&self, pv: &str) -> Option<&Node> {
        self.targets(pv, Rel::Member).into_iter().next()
    }

    /// Volume group a volume, a pool or a snapshot takes its extents from: a logical volume or a pool is carved from it directly, a snapshot
    /// of a logical volume from the group of its origin; thin volumes and thin snapshots take theirs from the pool, so they have none.
    pub fn vg_of(&self, id: &str) -> Option<&Node> {
        match self.node(id)?.kind {
            Kind::Lv => self.sources(id, Rel::Carves).into_iter().next(),
            Kind::ThinPool => self.sources(id, Rel::Pool).into_iter().next(),
            Kind::Snapshot => {
                let origin = self.origin_of(id)?;
                if origin.kind == Kind::Lv {
                    self.vg_of(&origin.id)
                } else {
                    None
                }
            }
            _ => None,
        }
    }

    /// Origin of a snapshot.
    pub fn origin_of(&self, snapshot: &str) -> Option<&Node> {
        self.sources(snapshot, Rel::SnapshotOf).into_iter().next()
    }

    /// Pool of a thin volume.
    pub fn pool_of(&self, thin: &str) -> Option<&Node> {
        self.sources(thin, Rel::Thin).into_iter().next()
    }
}
