//! Model of placing machines on NUMA nodes (chapter 11).
//!
//! The host has several nodes (in the exercise — two with 8 cores and 32 GiB each). For a machine one chooses where its vCPUs run and where
//! its memory lives: a node, or "spread" (half and half). Remote access share: own node — 0; CPUs and memory on different nodes — 1;
//! one spread and the other not — 0.5; everything spread — 0.5, but with a virtual NUMA topology the guest itself places data
//! closer — 0.25.
//!
//! One goal per scenario: the accepted placement fits into the nodes, and the average (over vCPUs) remote access share
//! is at most [`Scenario::max`].

use std::collections::BTreeMap;
use std::fmt;

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Host node.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Node {
    /// Cores on the node.
    pub cores: u32,
    /// Memory on the node, GiB.
    pub mem: u32,
}

/// Scenario virtual machine.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Vm {
    /// Machine name.
    pub name: String,
    /// Number of vCPUs.
    pub vcpus: u32,
    /// Memory, GiB.
    pub mem: u32,
}

/// Where the machine's CPUs or memory are placed.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub enum Place {
    /// Node with this number.
    Node(u8),
    /// Spread evenly across all nodes.
    Wide,
}

impl From<Place> for String {
    fn from(p: Place) -> String {
        match p {
            Place::Node(i) => i.to_string(),
            Place::Wide => "wide".to_string(),
        }
    }
}

impl TryFrom<String> for Place {
    type Error = String;
    fn try_from(s: String) -> Result<Place, String> {
        if s == "wide" {
            return Ok(Place::Wide);
        }
        s.parse::<u8>().map(Place::Node).map_err(|_| i18n::trf!("placement “{0}”: expected a node number or “wide”", s))
    }
}

impl fmt::Display for Place {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Place::Node(i) => write!(f, "{i}"),
            Place::Wide => f.write_str("wide"),
        }
    }
}

/// Placement of one machine.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Placement {
    /// Where the vCPUs run.
    pub cpu: Place,
    /// Where the memory lives.
    pub mem: Place,
    /// Virtual NUMA topology for a spread machine.
    pub vnuma: bool,
}

/// Placement of all scenario machines: name → placement.
pub type Plan = BTreeMap<String, Placement>;

/// Scenario: machines, goal and allowed remote access share.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (also the goal identifier).
    pub id: String,
    /// Tab title.
    pub title: String,
    /// Machines.
    pub vms: Vec<Vm>,
    /// Goal text.
    pub goal: String,
    /// Allowed average remote access share (0…1).
    pub max: f64,
}

impl Scenario {
    /// Exercise goal for this scenario.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }
}

/// Node load.
#[derive(Clone, Copy, Debug, PartialEq, Serialize, Deserialize)]
pub struct Load {
    /// Cores in use.
    pub cores: f64,
    /// Memory in use, GiB.
    pub mem: f64,
}

/// Placement evaluation.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Evaluation {
    /// Node loads.
    pub load: Vec<Load>,
    /// Some node is overloaded (cores or memory).
    pub over: bool,
    /// Remote access share of each machine (in scenario machine order).
    pub per: Vec<(String, f64)>,
    /// Average remote access share, weighted by vCPUs.
    pub avg: f64,
}

/// Remote access share for a placement (`vnuma` — virtual topology).
pub fn remote(cpu: Place, mem: Place, vnuma: bool) -> f64 {
    match (cpu, mem) {
        (Place::Wide, Place::Wide) => {
            if vnuma {
                0.25
            } else {
                0.5
            }
        }
        (Place::Wide, _) | (_, Place::Wide) => 0.5,
        (a, b) => {
            if a == b {
                0.0
            } else {
                1.0
            }
        }
    }
}

// What share of the machine falls on node `i`.
fn share(nodes: usize, place: Place, i: usize) -> f64 {
    match place {
        Place::Wide => 1.0 / nodes as f64,
        Place::Node(n) => {
            if usize::from(n) == i {
                1.0
            } else {
                0.0
            }
        }
    }
}

/// Evaluate placement `plan` of machines `vms` on nodes `nodes`.
/// Error — a machine has no placement or it points to a nonexistent node.
pub fn evaluate(nodes: &[Node], vms: &[Vm], plan: &Plan) -> Result<Evaluation, SpecError> {
    let mut load = vec![Load { cores: 0.0, mem: 0.0 }; nodes.len()];
    let mut weighted = 0.0;
    let mut total = 0.0;
    let mut per = Vec::with_capacity(vms.len());
    for vm in vms {
        let p = plan.get(&vm.name).ok_or_else(|| SpecError::new(i18n::trf!("no placement for machine {0}", vm.name)))?;
        for place in [p.cpu, p.mem] {
            if let Place::Node(n) = place {
                if usize::from(n) >= nodes.len() {
                    return Err(SpecError::new(i18n::trf!("machine {0}: no node {1}", vm.name, n)));
                }
            }
        }
        for (i, l) in load.iter_mut().enumerate() {
            l.cores += f64::from(vm.vcpus) * share(nodes.len(), p.cpu, i);
            l.mem += f64::from(vm.mem) * share(nodes.len(), p.mem, i);
        }
        let r = remote(p.cpu, p.mem, p.vnuma);
        per.push((vm.name.clone(), r));
        weighted += r * f64::from(vm.vcpus);
        total += f64::from(vm.vcpus);
    }
    let over = load.iter().zip(nodes).any(|(l, n)| l.cores > f64::from(n.cores) || l.mem > f64::from(n.mem));
    Ok(Evaluation { load, over, per, avg: if total != 0.0 { weighted / total } else { 0.0 } })
}

/// Default placement: everything on node 0.
pub fn default_plan(vms: &[Vm]) -> Plan {
    vms.iter().map(|v| (v.name.clone(), Placement { cpu: Place::Node(0), mem: Place::Node(0), vnuma: false })).collect()
}

/// Outcome of the "Accept placement" button.
#[derive(Clone, Debug, PartialEq)]
pub enum Accept {
    /// Does not fit: some node lacks cores or memory.
    Over,
    /// Too many remote accesses.
    TooRemote {
        /// Remote access share.
        avg: f64,
        /// Allowed share.
        max: f64,
    },
    /// Accepted.
    Ok {
        /// Remote access share.
        avg: f64,
    },
}

/// Accept the scenario placement: the goal is reached on [`Accept::Ok`].
pub fn accept(nodes: &[Node], sc: &Scenario, plan: &Plan) -> Result<Accept, SpecError> {
    let ev = evaluate(nodes, &sc.vms, plan)?;
    Ok(if ev.over {
        Accept::Over
    } else if ev.avg > sc.max + 1e-9 {
        Accept::TooRemote { avg: ev.avg, max: sc.max }
    } else {
        Accept::Ok { avg: ev.avg }
    })
}

/// Default exercise nodes: two with 8 cores and 32 GiB each.
pub fn default_nodes() -> Vec<Node> {
    vec![Node { cores: 8, mem: 32 }; 2]
}

/// Default scenarios (chapter 11 exercise).
pub fn default_scenarios() -> Vec<Scenario> {
    let vm = |name: &str, vcpus: u32, mem: u32| Vm { name: name.into(), vcpus, mem };
    vec![
        Scenario {
            id: "small".into(),
            title: i18n::tr("Four small machines").into(),
            vms: vec![vm("A", 4, 16), vm("B", 4, 12), vm("C", 4, 16), vm("D", 4, 12)],
            goal: i18n::tr("Everything fits, and there are no remote accesses at all (0%)").into(),
            max: 0.0,
        },
        Scenario {
            id: "wide".into(),
            title: i18n::tr("A large machine").into(),
            vms: vec![vm("E", 12, 40), vm("F", 2, 8), vm("G", 2, 8)],
            goal: i18n::tr("Everything fits, and the average share of remote accesses (per vCPU) is at most 20%").into(),
            max: 0.2,
        },
    ]
}
