//! Exercise description as data: which simulator, its scenarios and goals.
//!
//! [`Spec`] lives in the `spec` field of a task in the chapter file ([`crate::LabChapter`]); the UI builds the simulator from it,
//! and the server re-checks the submitted solution against it ([`mod@crate::verify`]).

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;
use crate::{ept, hv, migration, numa, qcow2, virtq};

/// Exercise identifiers of book 17 (also `Task::id`).
pub const LAB_IDS: [&str; 6] =
    ["virt-sim-hv", "virt-sim-ept", "virt-sim-virtqueue", "virt-sim-qcow2", "virt-sim-migration", "virt-sim-numa"];

/// Cluster of the qcow2 base layer (stored as a list, not a map: numeric keys as JSON strings are unwanted).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BaseCluster {
    /// Cluster number.
    pub cluster: u32,
    /// Data.
    pub data: String,
}

/// Exercise simulator description (the `sim` field selects the module).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "sim", rename_all = "snake_case")]
pub enum Spec {
    /// Mini-hypervisor (chapter 2): guest programs.
    Hv {
        /// Programs; the goal is to pass each one.
        programs: Vec<hv::Program>,
    },
    /// Address translation (chapter 4): workloads and goals.
    Ept {
        /// Workloads.
        workloads: Vec<ept::Workload>,
        /// Goals.
        goals: Vec<ept::EptGoal>,
    },
    /// virtio queue (chapter 6).
    Virtq {
        /// Number of descriptors.
        size: u32,
        /// Goals.
        goals: Vec<virtq::VirtqGoal>,
    },
    /// Placement on NUMA nodes (chapter 11).
    Numa {
        /// Host nodes.
        nodes: Vec<numa::Node>,
        /// Scenarios; the goal is to get each placement accepted.
        scenarios: Vec<numa::Scenario>,
    },
    /// qcow2 layers (chapter 9).
    Qcow2 {
        /// Number of clusters.
        clusters: u32,
        /// Base layer clusters.
        base: Vec<BaseCluster>,
        /// Goals.
        goals: Vec<qcow2::Qcow2Goal>,
    },
    /// Live migration (chapter 10).
    Migration {
        /// Scenarios; the goal is to meet the condition of each one.
        scenarios: Vec<migration::Scenario>,
    },
}

/// qcow2 base layer as a list → map.
pub fn base_map(base: &[BaseCluster]) -> BTreeMap<u32, String> {
    base.iter().map(|c| (c.cluster, c.data.clone())).collect()
}

fn unique(kind: &str, ids: impl Iterator<Item = String>) -> Result<(), SpecError> {
    let mut seen = std::collections::BTreeSet::new();
    for id in ids {
        if id.is_empty() {
            return Err(SpecError::new(i18n::trf!("{0}: empty identifier", kind)));
        }
        if !seen.insert(id.clone()) {
            return Err(SpecError::new(i18n::trf!("{0}: duplicate identifier “{1}”", kind, id)));
        }
    }
    Ok(())
}

impl Spec {
    /// Simulator name (value of the `sim` field).
    pub fn sim(&self) -> &'static str {
        match self {
            Spec::Hv { .. } => "hv",
            Spec::Ept { .. } => "ept",
            Spec::Virtq { .. } => "virtq",
            Spec::Numa { .. } => "numa",
            Spec::Qcow2 { .. } => "qcow2",
            Spec::Migration { .. } => "migration",
        }
    }

    /// Exercise goals in order. The exercise is solved when all are achieved.
    pub fn goals(&self) -> Vec<Goal> {
        match self {
            Spec::Hv { programs } => programs.iter().map(hv::Program::as_goal).collect(),
            Spec::Ept { goals, .. } => goals.iter().map(ept::EptGoal::as_goal).collect(),
            Spec::Virtq { goals, .. } => goals.iter().map(virtq::VirtqGoal::as_goal).collect(),
            Spec::Numa { scenarios, .. } => scenarios.iter().map(numa::Scenario::as_goal).collect(),
            Spec::Qcow2 { goals, .. } => goals.iter().map(qcow2::Qcow2Goal::as_goal).collect(),
            Spec::Migration { scenarios, .. } => scenarios.iter().map(migration::Scenario::as_goal).collect(),
        }
    }

    /// Data integrity check: identifiers are unique, workload references exist, instructions parse.
    pub fn validate(&self) -> Result<(), SpecError> {
        unique(i18n::tr("goals"), self.goals().into_iter().map(|g| g.id))?;
        if self.goals().is_empty() {
            return Err(SpecError::new(i18n::tr("no goals")));
        }
        match self {
            Spec::Hv { programs } => {
                for p in programs {
                    p.validate()?;
                }
            }
            Spec::Ept { workloads, goals } => {
                unique(i18n::tr("workloads"), workloads.iter().map(|w| w.id.clone()))?;
                for g in goals {
                    if !workloads.iter().any(|w| w.id == g.workload) {
                        return Err(SpecError::new(i18n::trf!("goal {0}: no workload “{1}”", g.id, g.workload)));
                    }
                }
            }
            Spec::Virtq { size, .. } => {
                if *size == 0 {
                    return Err(SpecError::new(i18n::tr("queue without descriptors")));
                }
            }
            Spec::Numa { nodes, scenarios } => {
                if nodes.is_empty() || nodes.len() > 255 {
                    return Err(SpecError::new(i18n::tr("the number of nodes must be from 1 to 255")));
                }
                for s in scenarios {
                    unique(i18n::tr("machines"), s.vms.iter().map(|v| v.name.clone()))?;
                    if !s.max.is_finite() || s.max < 0.0 {
                        return Err(SpecError::new(i18n::trf!("scenario {0}: invalid fraction", s.id)));
                    }
                }
            }
            Spec::Qcow2 { clusters, base, .. } => {
                if base.iter().any(|c| c.cluster >= *clusters) {
                    return Err(SpecError::new(i18n::tr("base layer cluster out of range")));
                }
            }
            Spec::Migration { scenarios } => {
                for s in scenarios {
                    if !(s.dirty.is_finite() && s.bw.is_finite() && s.bw > 0.0 && s.dirty >= 0.0) {
                        return Err(SpecError::new(i18n::trf!("scenario {0}: invalid rates", s.id)));
                    }
                }
            }
        }
        Ok(())
    }
}

/// Default exercise description by its identifier (`virt-sim-…`).
pub fn builtin(id: &str) -> Option<Spec> {
    Some(match id {
        "virt-sim-hv" => Spec::Hv { programs: hv::default_programs() },
        "virt-sim-ept" => Spec::Ept { workloads: ept::default_workloads(), goals: ept::default_goals() },
        "virt-sim-virtqueue" => Spec::Virtq { size: virtq::SIZE, goals: virtq::default_goals() },
        "virt-sim-qcow2" => Spec::Qcow2 {
            clusters: qcow2::CLUSTERS,
            base: qcow2::default_base().into_iter().map(|(cluster, data)| BaseCluster { cluster, data }).collect(),
            goals: qcow2::default_goals(),
        },
        "virt-sim-migration" => Spec::Migration { scenarios: migration::default_scenarios() },
        "virt-sim-numa" => Spec::Numa { nodes: numa::default_nodes(), scenarios: numa::default_scenarios() },
        _ => return None,
    })
}
