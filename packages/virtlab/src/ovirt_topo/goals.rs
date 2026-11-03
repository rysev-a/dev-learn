//! Goals and scenarios of the topology board.

use serde::{Deserialize, Serialize};

use super::eval::{DcStatus, HostStatus, VmStatus};
use super::{
    evacuation_possible, evaluate, ha_restart_ok, migration_network, migration_target, problems, restorable_after_domain_loss,
    survives_site_loss, trace, user_can, Action, Evaluation, Kind, Op, Rel, Role, Topology,
};
use crate::goal::Goal;

/// The kind of operation a goal wants to succeed.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum OpKind {
    /// The engine reaches every host.
    EngineToHost,
    /// Every VM can be started.
    StartVm,
    /// Every VM can be migrated to another host of its cluster.
    Migrate,
    /// Every host can be fenced (it has a fence agent and a fence proxy).
    Fence,
}

impl OpKind {
    /// The operations of this kind that exist on the board.
    pub fn ops(self, t: &Topology) -> Vec<Op> {
        match self {
            OpKind::EngineToHost => t.of_kind(Kind::Host).map(|h| Op::EngineToHost { host: h.id.clone() }).collect(),
            OpKind::StartVm => t.of_kind(Kind::Vm).map(|v| Op::StartVm { vm: v.id.clone() }).collect(),
            OpKind::Migrate => t.of_kind(Kind::Vm).map(|v| Op::Migrate { vm: v.id.clone() }).collect(),
            OpKind::Fence => t.of_kind(Kind::Host).map(|h| Op::Fence { host: h.id.clone() }).collect(),
        }
    }
}

/// A condition on the board that the scenario wants.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum TopoGoal {
    /// At least this many hosts are Up.
    HostsUp {
        /// Minimum.
        min: u32,
    },
    /// At least this many data centers are Up.
    DcUp {
        /// Minimum.
        min: u32,
    },
    /// Every data center has at least this many Up hosts, and there are at least two data centers.
    EachDcHasUpHosts {
        /// Minimum per data center.
        min: u32,
    },
    /// At least this many VMs run.
    VmRunning {
        /// Minimum.
        min: u32,
    },
    /// At least this many data centers have an SPM.
    Spm {
        /// Minimum.
        min: u32,
    },
    /// Everything on the board works: there is at least one host and one data center, every host is Up, every data center is Up,
    /// every VM runs.
    Healthy,
    /// An operation of this kind succeeds on every object it applies to (there must be at least one).
    OpOk {
        /// Operation.
        op: OpKind,
    },
    /// At least this many objects of the kind.
    Has {
        /// Kind.
        node: Kind,
        /// Minimum.
        min: u32,
    },
    /// No object of the kind.
    Lacks {
        /// Kind.
        node: Kind,
    },
    /// An object of the kind has the parameter with this value (`role`, `required`, `type`; booleans as `true` / `false`).
    Param {
        /// Kind.
        node: Kind,
        /// Parameter.
        key: String,
        /// Value as text.
        value: String,
    },
    /// After losing any single object of the kind, every data center stays Up and keeps an SPM (there is at least one object of the kind).
    SurviveLoss {
        /// Kind of the failing object (a host or a storage domain).
        node: Kind,
    },
    /// The memory of every VM goes over a network of this role when the VM is migrated.
    MigrateOverRole {
        /// Role.
        role: Role,
    },
    /// At least this many links of the relation.
    Link {
        /// Relation.
        rel: Rel,
        /// Minimum.
        min: u32,
    },
    /// There is an HA VM placed on a host, and after the loss of any host that runs HA VMs they all restart on other hosts of the cluster:
    /// the lost host had a fence agent, another Up host of its data center can act as the fence proxy, and the memory, networks, disks and
    /// hard affinity groups let each HA VM run on one of the other hosts (the first one in link order where it would run).
    HaRestart,
    /// There is a host that runs VMs, and every host that runs VMs can be put into maintenance: each of its VMs moves to another host of the
    /// cluster where it would run.
    EvacuationPossible,
    /// There is a VM, and every VM has a backup that is incremental or full.
    AllVmsBackedUp,
    /// After the loss of any storage domain that holds a VM disk, each VM that had a disk on it has an incremental or full backup
    /// (a snapshot is lost with the domain).
    RestorableAfterDomainLoss,
    /// There are at least two data centers and a VM, and after the loss of any data center that hosts VMs (with everything under it) every
    /// VM that was on it has a disk replica: each of its disk domains has a replica that is Active in another data center that is Up.
    SurviveSiteLoss,
    /// The user may do the action on the object (the identifiers of a user and of any object).
    UserCan {
        /// User identifier.
        user: String,
        /// Action.
        action: Action,
        /// Object identifier.
        object: String,
    },
    /// The user may not do the action on the object (both objects exist).
    UserCannot {
        /// User identifier.
        user: String,
        /// Action.
        action: Action,
        /// Object identifier.
        object: String,
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
    /// The host is a member of the cluster.
    HostInCluster {
        /// Host identifier.
        host: String,
        /// Cluster identifier.
        cluster: String,
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

impl TopoGoal {
    /// The goal as a sentence (objects are named by their identifiers; see [`TopoGoal::describe_for`]).
    pub fn describe(&self) -> String {
        self.describe_for(&Topology::default())
    }

    /// The goal as a sentence; the objects it names are shown by their names on the board.
    pub fn describe_for(&self, t: &Topology) -> String {
        match self {
            TopoGoal::HostsUp { min } => i18n::trf!("at least {0} host(s) are Up", min),
            TopoGoal::DcUp { min } => i18n::trf!("at least {0} data center(s) are Up", min),
            TopoGoal::EachDcHasUpHosts { min } => {
                i18n::trf!("two or more data centers, each with at least {0} Up host(s)", min)
            }
            TopoGoal::VmRunning { min } => i18n::trf!("at least {0} VM(s) are running", min),
            TopoGoal::Spm { min } => i18n::trf!("at least {0} data center(s) have an SPM", min),
            TopoGoal::Healthy => {
                i18n::tr("everything works: all hosts Up, all data centers Up, all VMs running").to_string()
            }
            TopoGoal::OpOk { op: OpKind::EngineToHost } => i18n::tr("the engine reaches every host").to_string(),
            TopoGoal::OpOk { op: OpKind::StartVm } => i18n::tr("every VM can be started").to_string(),
            TopoGoal::OpOk { op: OpKind::Migrate } => {
                i18n::tr("every VM can be live-migrated within its cluster").to_string()
            }
            TopoGoal::OpOk { op: OpKind::Fence } => i18n::tr("every host can be fenced").to_string(),
            TopoGoal::Has { node, min } => i18n::trf!("at least {0} × {1}", min, node.label()),
            TopoGoal::Lacks { node } => i18n::trf!("no {0}", node.label()),
            TopoGoal::Link { rel, min } => i18n::trf!("at least {0} link(s): {1}", min, rel.label()),
            TopoGoal::Param { node, key, value } => i18n::trf!("a {0} with {1} = {2}", node.label(), key, value),
            TopoGoal::SurviveLoss { node } => {
                i18n::trf!("after losing any single {0}, every data center stays Up and keeps an SPM", node.label())
            }
            TopoGoal::MigrateOverRole { role } => {
                i18n::trf!("the memory of a migration goes over a {0} network", role.label())
            }
            TopoGoal::HaRestart => i18n::tr(
                "after the loss of a host, its HA VMs restart on other hosts of the cluster (a fence agent, a fence proxy and room for them)",
            )
            .to_string(),
            TopoGoal::EvacuationPossible => {
                i18n::tr("every host that runs VMs can be put into maintenance: its VMs move to other hosts of the cluster").to_string()
            }
            TopoGoal::AllVmsBackedUp => i18n::tr("every VM has an incremental or a full backup").to_string(),
            TopoGoal::RestorableAfterDomainLoss => {
                i18n::tr("after the loss of any storage domain with VM disks, every VM can be restored from an incremental or a full backup")
                    .to_string()
            }
            TopoGoal::SurviveSiteLoss => {
                i18n::tr("after the loss of any data center with VMs, every VM has a disk replica in another Up data center").to_string()
            }
            TopoGoal::UserCan { user, action, object } => {
                i18n::trf!("“{0}” can {1} on “{2}”", nm(t, user), action.label(), nm(t, object))
            }
            TopoGoal::UserCannot { user, action, object } => {
                i18n::trf!("“{0}” cannot {1} on “{2}”", nm(t, user), action.label(), nm(t, object))
            }
            TopoGoal::ParamOf { id, key, value } => i18n::trf!("“{0}” has {1} = {2}", nm(t, id), key, value),
            TopoGoal::Linked { from, to } => i18n::trf!("“{0}” → “{1}” are linked", nm(t, from), nm(t, to)),
            TopoGoal::HostInCluster { host, cluster } => {
                i18n::trf!("the host “{0}” is a member of the cluster “{1}”", nm(t, host), nm(t, cluster))
            }
        }
    }

    /// The goal holds on the board.
    pub fn check(&self, t: &Topology, ev: &Evaluation) -> bool {
        let count = |n: usize| n as u64;
        match self {
            TopoGoal::HostsUp { min } => {
                count(ev.hosts.iter().filter(|h| h.status == HostStatus::Up).count()) >= u64::from(*min)
            }
            TopoGoal::DcUp { min } => {
                count(ev.dcs.iter().filter(|d| d.status == DcStatus::Up).count()) >= u64::from(*min)
            }
            TopoGoal::EachDcHasUpHosts { min } => {
                ev.dcs.len() >= 2
                    && ev
                        .dcs
                        .iter()
                        .all(|d| count(t.hosts_of_dc(&d.id).filter(|h| ev.host_up(&h.id)).count()) >= u64::from(*min))
            }
            TopoGoal::VmRunning { min } => {
                count(ev.vms.iter().filter(|v| v.status == VmStatus::Running).count()) >= u64::from(*min)
            }
            TopoGoal::Spm { min } => count(ev.dcs.iter().filter(|d| d.spm.is_some()).count()) >= u64::from(*min),
            TopoGoal::Healthy => {
                // a host in maintenance is healthy only while it has nothing to run: no VM is placed on it
                let rests = |h: &super::HostEval| {
                    h.status == HostStatus::Up
                        || (h.status == HostStatus::Maintenance && t.targets(&h.id, Rel::Runs).next().is_none())
                };
                !ev.hosts.is_empty()
                    && !ev.dcs.is_empty()
                    && ev.hosts.iter().all(rests)
                    && ev.dcs.iter().all(|d| d.status == DcStatus::Up)
                    && ev.vms.iter().all(|v| v.status == VmStatus::Running)
            }
            TopoGoal::OpOk { op } => {
                let ops = op.ops(t);
                !ops.is_empty() && ops.iter().all(|o| trace(t, ev, o).ok)
            }
            TopoGoal::Has { node, min } => count(t.of_kind(*node).count()) >= u64::from(*min),
            TopoGoal::Lacks { node } => t.of_kind(*node).next().is_none(),
            TopoGoal::Param { node, key, value } => t.of_kind(*node).any(|n| &n.param_text(key) == value),
            TopoGoal::SurviveLoss { node } => {
                let victims: Vec<String> = t.of_kind(*node).map(|n| n.id.clone()).collect();
                !victims.is_empty()
                    && victims.iter().all(|id| {
                        let after = evaluate(&t.without(id));
                        !after.dcs.is_empty() && after.dcs.iter().all(|d| d.status == DcStatus::Up && d.spm.is_some())
                    })
            }
            TopoGoal::MigrateOverRole { role } => {
                let vms: Vec<&str> = t.of_kind(Kind::Vm).map(|v| v.id.as_str()).collect();
                !vms.is_empty()
                    && vms.iter().all(|vm| {
                        let Some(src) = t.host_of_vm(vm) else { return false };
                        let Some(dst) = migration_target(t, ev, &src.id) else { return false };
                        migration_network(t, &src.id, &dst.id).is_some_and(|n| n.role() == *role)
                    })
            }
            TopoGoal::Link { rel, min } => {
                count(
                    t.edges
                        .iter()
                        .filter(|e| {
                            t.node(&e.from).zip(t.node(&e.to)).and_then(|(a, b)| super::rel(a.kind, b.kind))
                                == Some(*rel)
                        })
                        .count(),
                ) >= u64::from(*min)
            }
            TopoGoal::HaRestart => ha_restart_ok(t),
            TopoGoal::EvacuationPossible => evacuation_possible(t),
            TopoGoal::AllVmsBackedUp => {
                t.of_kind(Kind::Vm).next().is_some()
                    && t.of_kind(Kind::Vm).all(|v| t.targets(&v.id, Rel::BackupOf).any(|b| b.backup_type().off_site()))
            }
            TopoGoal::RestorableAfterDomainLoss => restorable_after_domain_loss(t),
            TopoGoal::SurviveSiteLoss => survives_site_loss(t),
            TopoGoal::UserCan { user, action, object } => t.node(object).is_some() && user_can(t, user, *action, object),
            TopoGoal::UserCannot { user, action, object } => {
                t.node(object).is_some()
                    && t.node(user).is_some_and(|u| u.kind == Kind::User)
                    && !user_can(t, user, *action, object)
            }
            TopoGoal::ParamOf { id, key, value } => t.node(id).is_some_and(|n| &n.param_text(key) == value),
            TopoGoal::Linked { from, to } => t.linked(from, to),
            TopoGoal::HostInCluster { host, cluster } => t.linked(cluster, host),
        }
    }
}

fn default_max_nodes() -> u32 {
    24
}

/// One exercise of the board: a story, a starting board and the goals.
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
    /// Goals; all must hold.
    pub goals: Vec<TopoGoal>,
}

impl Scenario {
    /// The scenario as an exercise goal.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.title.clone())
    }

    /// Results of every goal on the board.
    pub fn results(&self, t: &Topology) -> Vec<GoalResult> {
        let ev = evaluate(t);
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
