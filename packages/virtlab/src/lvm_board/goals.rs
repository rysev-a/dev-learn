//! Goals and scenarios of the LVM board.

use serde::{Deserialize, Serialize};

use super::eval::{FsStatus, PoolStatus, PvStatus, SnapStatus, VmStatus, VolStatus};
use super::{evacuable, evaluate, problems, survives_disk_loss, Evaluation, Kind, Topology, Workload};
use crate::goal::Goal;

fn one() -> u32 {
    1
}

/// A condition on the board that the scenario wants.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum LvmGoal {
    /// A volume group (the named one, or any) has at least this much free space.
    VgFree {
        /// Identifier of the group; any group counts when unset.
        #[serde(default, skip_serializing_if = "Option::is_none")]
        vg: Option<String>,
        /// GiB.
        min_gib: u32,
    },
    /// A working volume (the named one, or `count` of any) is at least this large.
    LvSize {
        /// Identifier of the volume; any volumes count when unset.
        #[serde(default, skip_serializing_if = "Option::is_none")]
        lv: Option<String>,
        /// GiB.
        min_gib: u32,
        /// How many volumes (when no identifier is given).
        #[serde(default = "one")]
        count: u32,
    },
    /// There is a filesystem, and every filesystem is as large as its volume.
    FsFits,
    /// There is a snapshot, and no snapshot is lost (overflowed, without an origin, without room, on a full pool).
    SnapshotValid,
    /// There is a thin pool, and every pool is below 80% used (data and metadata).
    PoolFits,
    /// After the loss of any single disk no volume, pool or snapshot is lost.
    SurviveDiskLoss,
    /// The data of the physical volume fit on the other physical volumes of its group (`pvmove` can empty it).
    Evacuable {
        /// Physical volume identifier.
        pv: String,
    },
    /// Everything on the board works: there is a volume, every physical volume is made of a disk and in a group, every volume, pool, snapshot,
    /// filesystem and VM works.
    Healthy,
    /// At least this many objects of the kind.
    Has {
        /// Kind.
        node: Kind,
        /// Minimum.
        min: u32,
    },
    /// At most this many objects of the kind.
    AtMost {
        /// Kind.
        node: Kind,
        /// Maximum.
        max: u32,
    },
    /// No object of the kind.
    Lacks {
        /// Kind.
        node: Kind,
    },
    /// The object has the parameter value (`param_text` of the object: the default counts).
    ParamOf {
        /// Object identifier.
        id: String,
        /// Parameter.
        key: String,
        /// Value as text.
        value: String,
    },
    /// The link `from → to` exists (the direction of the model: see [`rel`](super::rel)).
    Linked {
        /// Source identifier.
        from: String,
        /// Target identifier.
        to: String,
    },
}

/// Verdict on one goal.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GoalResult {
    /// The goal holds.
    pub ok: bool,
    /// The goal text.
    pub text: String,
}

/// The name of an object on the board, or its identifier when the board has no such object.
fn nm(t: &Topology, id: &str) -> String {
    t.node(id).map_or_else(|| id.to_string(), |n| n.name.clone())
}

impl LvmGoal {
    /// The goal as a sentence (objects are named by their identifiers; see [`LvmGoal::describe_for`]).
    pub fn describe(&self) -> String {
        self.describe_for(&Topology::default())
    }

    /// The goal as a sentence; the objects it names are shown by their names on the board.
    pub fn describe_for(&self, t: &Topology) -> String {
        match self {
            LvmGoal::VgFree { vg: None, min_gib } => i18n::trf!("a volume group has at least {0} GiB free", min_gib),
            LvmGoal::VgFree { vg: Some(vg), min_gib } => i18n::trf!("“{0}” has at least {1} GiB free", nm(t, vg), min_gib),
            LvmGoal::LvSize { lv: Some(lv), min_gib, .. } => {
                i18n::trf!("“{0}” is a working volume of at least {1} GiB", nm(t, lv), min_gib)
            }
            LvmGoal::LvSize { lv: None, min_gib, count: 1 } => i18n::trf!("a working volume of at least {0} GiB", min_gib),
            LvmGoal::LvSize { lv: None, min_gib, count } => i18n::trf!("at least {0} working volumes of {1} GiB or more", count, min_gib),
            LvmGoal::FsFits => i18n::tr("every filesystem is as large as its volume").to_string(),
            LvmGoal::SnapshotValid => i18n::tr("there is a snapshot and none of them is lost").to_string(),
            LvmGoal::PoolFits => i18n::tr("there is a thin pool and its data and metadata are below 80% used").to_string(),
            LvmGoal::SurviveDiskLoss => i18n::tr("after losing any single disk no volume is lost").to_string(),
            LvmGoal::Evacuable { pv } => {
                i18n::trf!("the data of “{0}” fit on the other physical volumes (pvmove can empty it)", nm(t, pv))
            }
            LvmGoal::Healthy => {
                i18n::tr("everything works: physical volumes in a group, volumes, pools, snapshots, filesystems and VMs").to_string()
            }
            LvmGoal::Has { node, min } => i18n::trf!("at least {0} × {1}", min, node.label()),
            LvmGoal::AtMost { node, max } => i18n::trf!("at most {0} × {1}", max, node.label()),
            LvmGoal::Lacks { node } => i18n::trf!("no {0}", node.label()),
            LvmGoal::ParamOf { id, key, value } => i18n::trf!("“{0}” has {1} = {2}", nm(t, id), key, value),
            LvmGoal::Linked { from, to } => i18n::trf!("“{0}” → “{1}” are linked", nm(t, from), nm(t, to)),
        }
    }

    /// The goal holds on the board.
    pub fn check(&self, t: &Topology, ev: &Evaluation) -> bool {
        let count = |k: Kind| t.of_kind(k).count() as u64;
        match self {
            LvmGoal::VgFree { vg, min_gib } => ev
                .vgs
                .iter()
                .filter(|v| vg.as_deref().is_none_or(|id| v.id == id))
                .any(|v| v.free_gib() >= u64::from(*min_gib)),
            LvmGoal::LvSize { lv: Some(id), min_gib, .. } => {
                ev.volume(id).is_some_and(|v| v.status == VolStatus::Ok && v.size_gib >= u64::from(*min_gib))
            }
            LvmGoal::LvSize { lv: None, min_gib, count } => {
                ev.volumes.iter().filter(|v| v.status == VolStatus::Ok && v.size_gib >= u64::from(*min_gib)).count() as u64
                    >= u64::from(*count)
            }
            LvmGoal::FsFits => !ev.filesystems.is_empty() && ev.filesystems.iter().all(|f| f.status == FsStatus::Ok),
            LvmGoal::SnapshotValid => !ev.snapshots.is_empty() && ev.snapshots.iter().all(|s| s.status == SnapStatus::Valid),
            LvmGoal::PoolFits => !ev.pools.is_empty() && ev.pools.iter().all(|p| p.status == PoolStatus::Ok),
            LvmGoal::SurviveDiskLoss => survives_disk_loss(t, ev),
            LvmGoal::Evacuable { pv } => evacuable(t, ev, pv),
            LvmGoal::Healthy => {
                !ev.volumes.is_empty()
                    && ev.pvs.iter().all(|p| p.status == PvStatus::Ok)
                    && ev.volumes.iter().all(|v| v.status == VolStatus::Ok)
                    && ev.pools.iter().all(|p| matches!(p.status, PoolStatus::Ok | PoolStatus::Warn))
                    && ev.snapshots.iter().all(|s| s.status == SnapStatus::Valid)
                    && ev.filesystems.iter().all(|f| f.status == FsStatus::Ok)
                    && ev.vms.iter().all(|v| v.status == VmStatus::Ok)
            }
            LvmGoal::Has { node, min } => count(*node) >= u64::from(*min),
            LvmGoal::AtMost { node, max } => count(*node) <= u64::from(*max),
            LvmGoal::Lacks { node } => count(*node) == 0,
            LvmGoal::ParamOf { id, key, value } => t.node(id).is_some_and(|n| &n.param_text(key) == value),
            LvmGoal::Linked { from, to } => t.linked(from, to),
        }
    }
}

fn default_max_nodes() -> u32 {
    24
}

/// One exercise of the board: a story, a starting board, the write load and the goals.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (the key of the solution).
    pub id: String,
    /// Title (an English key; shown with `tr_dyn`).
    pub title: String,
    /// What is going on.
    pub story: String,
    /// What the student has to achieve, in a sentence.
    pub goal: String,
    /// A hint.
    pub hint: String,
    /// Kinds the student may add.
    pub palette: Vec<Kind>,
    /// The most objects on the board.
    #[serde(default = "default_max_nodes")]
    pub max_nodes: u32,
    /// The board at the start.
    pub start: Topology,
    /// What happens to the data while the layout is in use (snapshot overflow and thin pool usage depend on it).
    #[serde(default)]
    pub workload: Workload,
    /// Goals; all must hold.
    pub goals: Vec<LvmGoal>,
}

impl Scenario {
    /// The scenario as an exercise goal.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.title.clone())
    }

    /// The board evaluated under the workload of the scenario.
    pub fn evaluate(&self, t: &Topology) -> Evaluation {
        evaluate(t, &self.workload)
    }

    /// Results of every goal on the board.
    pub fn results(&self, t: &Topology) -> Vec<GoalResult> {
        let ev = self.evaluate(t);
        self.goals.iter().map(|g| GoalResult { ok: g.check(t, &ev), text: g.describe_for(t) }).collect()
    }

    /// Why the board cannot be accepted at all (broken rules, kinds outside the palette, too many objects).
    pub fn invalid(&self, t: &Topology) -> Option<String> {
        if let Some(p) = problems(t).into_iter().next() {
            return Some(p.text);
        }
        if t.nodes.len() > self.max_nodes as usize {
            return Some(i18n::trf!("at most {0} objects are allowed", self.max_nodes));
        }
        for n in &t.nodes {
            let from_start = self.start.node(&n.id).is_some_and(|s| s.kind == n.kind);
            if !from_start && !self.palette.contains(&n.kind) {
                return Some(i18n::trf!("“{0}” is not available in this exercise", n.kind.label()));
            }
        }
        None
    }

    /// The board is acceptable and every goal holds.
    pub fn reached(&self, t: &Topology) -> bool {
        self.invalid(t).is_none() && self.results(t).iter().all(|r| r.ok)
    }
}
