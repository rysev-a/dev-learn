//! oVirt scheduler model (chapter 22): filters, weights and affinity.
//!
//! When a VM starts, the engine takes the cluster's hosts, throws out those that do not fit (**filters**) and ranks the rest (**weights**).
//! Model rules: a filter is a hard condition — memory (the host has enough free memory), network (the host has all the networks of the VM's NICs),
//! affinity (a host already running a VM of the same hard anti-affinity group is dropped). Every weight module ranks the surviving hosts
//! by its key (the best gets rank 0); the host with the lowest sum of `factor × rank` wins, ties go to the lowest host name.
//! A module with factor 0 is off. The VMs are placed one by one in the given order, each placement changes the host.
//!
//! Differences from real oVirt (this is a teaching model): the engine's rank selector also ranks hosts per weight module (a lower raw weight is
//! better), but it inverts the rank so that the best host gets the **highest** rank, multiplies it by the policy factor and the **highest**
//! sum wins; the model uses the mirrored form (best = rank 0, lowest sum wins), which picks the same host. The three weights are simplified
//! stand-ins for oVirt weight modules: `even` (fewer VMs, like `OptimalForEvenGuestDistribution`), `free_mem` (like
//! `OptimalForMemoryEvenDistribution`) and `pack` (more VMs, a simplification of `OptimalForCpuPowerSaving`/`OptimalForMemoryPowerSaving`,
//! which in oVirt work by CPU/memory load, not by VM count).
//!
//! A scenario ([`Scenario`]) gives hosts and VMs; the student chooses the cluster policy ([`Policy`]). A placement that breaks a
//! constraint the policy did not check (no memory, a missing network, a second VM of a group on one host) is counted as a mistake: such a VM
//! would not start or would break the group's rule.

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Host of the cluster.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Host {
    /// Name.
    pub name: String,
    /// Free memory, GiB.
    pub mem: i32,
    /// VMs already running.
    pub vms: u32,
    /// Networks the host has.
    pub nets: Vec<String>,
}

/// VM to start.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Vm {
    /// Name.
    pub name: String,
    /// Memory, GiB.
    pub mem: i32,
    /// Networks of the VM's NICs.
    #[serde(default)]
    pub nets: Vec<String>,
    /// Hard anti-affinity group: VMs of one group must run on different hosts.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub group: Option<String>,
}

/// Cluster scheduling policy: filters and weight factors.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Policy {
    /// Filter: enough free memory.
    pub memory: bool,
    /// Filter: the host has the VM's networks.
    pub network: bool,
    /// Filter: hard anti-affinity.
    pub affinity: bool,
    /// Weight: fewer VMs is better (even distribution of VMs).
    pub even: u32,
    /// Weight: more free memory is better.
    pub free_mem: u32,
    /// Weight: more VMs is better (power saving: pack the VMs).
    pub pack: u32,
}

/// Largest weight factor.
pub const MAX_FACTOR: u32 = 10;

/// Why a placement is wrong.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Mistake {
    /// Not enough memory on the host.
    Memory,
    /// The host lacks a network of the VM.
    Network,
    /// A second VM of the anti-affinity group on the host.
    Affinity,
}

/// Where a VM went.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Placement {
    /// VM name.
    pub vm: String,
    /// Chosen host (`None` — no host passed the filters).
    pub host: Option<String>,
    /// Constraints this placement breaks.
    pub mistakes: Vec<Mistake>,
}

/// Scheduling result.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Plan {
    /// Placements in VM order.
    pub placements: Vec<Placement>,
    /// VMs per host after the run (already running ones included), in host order.
    pub counts: Vec<(String, u32)>,
}

impl Plan {
    /// VMs that found no host.
    pub fn unplaced(&self) -> usize {
        self.placements.iter().filter(|p| p.host.is_none()).count()
    }

    /// Placements with a mistake.
    pub fn mistakes(&self) -> usize {
        self.placements.iter().filter(|p| !p.mistakes.is_empty()).count()
    }

    /// Difference between the busiest and the emptiest host.
    pub fn spread(&self) -> u32 {
        let max = self.counts.iter().map(|c| c.1).max().unwrap_or(0);
        let min = self.counts.iter().map(|c| c.1).min().unwrap_or(0);
        max - min
    }

    /// Hosts that received at least one VM.
    pub fn used(&self) -> usize {
        let mut hosts: Vec<&str> = self.placements.iter().filter_map(|p| p.host.as_deref()).collect();
        hosts.sort_unstable();
        hosts.dedup();
        hosts.len()
    }
}

/// Place the VMs one by one according to the policy.
pub fn schedule(hosts: &[Host], vms: &[Vm], policy: &Policy) -> Plan {
    let mut state: Vec<Host> = hosts.to_vec();
    let mut groups: Vec<Vec<String>> = vec![vec![]; state.len()]; // anti-affinity groups present on each host
    let mut placements = vec![];
    for vm in vms {
        let fits = |i: usize, h: &Host| -> bool {
            (!policy.memory || h.mem >= vm.mem)
                && (!policy.network || vm.nets.iter().all(|n| h.nets.contains(n)))
                && (!policy.affinity || vm.group.as_ref().is_none_or(|g| !groups[i].contains(g)))
        };
        let candidates: Vec<usize> = state.iter().enumerate().filter(|(i, h)| fits(*i, h)).map(|(i, _)| i).collect();
        if candidates.is_empty() {
            placements.push(Placement { vm: vm.name.clone(), host: None, mistakes: vec![] });
            continue;
        }
        let rank = |key: &dyn Fn(&Host) -> i32, i: usize| -> u32 {
            let mine = key(&state[i]);
            candidates.iter().filter(|&&j| key(&state[j]) < mine).count() as u32
        };
        let total = |i: usize| -> u32 {
            policy.even * rank(&|h| h.vms as i32, i)
                + policy.free_mem * rank(&|h| -h.mem, i)
                + policy.pack * rank(&|h| -(h.vms as i32), i)
        };
        let best = candidates
            .iter()
            .copied()
            .min_by(|&a, &b| (total(a), &state[a].name).cmp(&(total(b), &state[b].name)))
            .unwrap_or(0);
        let mut mistakes = vec![];
        if state[best].mem < vm.mem {
            mistakes.push(Mistake::Memory);
        }
        if !vm.nets.iter().all(|n| state[best].nets.contains(n)) {
            mistakes.push(Mistake::Network);
        }
        if vm.group.as_ref().is_some_and(|g| groups[best].contains(g)) {
            mistakes.push(Mistake::Affinity);
        }
        placements.push(Placement { vm: vm.name.clone(), host: Some(state[best].name.clone()), mistakes });
        state[best].mem -= vm.mem;
        state[best].vms += 1;
        if let Some(g) = &vm.group {
            groups[best].push(g.clone());
        }
    }
    Plan { placements, counts: state.iter().map(|h| (h.name.clone(), h.vms)).collect() }
}

/// Condition on the result: always no mistakes and no unplaced VMs, plus the optional limits.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SchedGoal {
    /// Spread between the busiest and the emptiest host at most.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_spread: Option<u32>,
    /// Hosts used by the new VMs at most.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_used: Option<u32>,
}

impl SchedGoal {
    /// Whether the goal is reached on plan `p`.
    pub fn check(&self, p: &Plan) -> bool {
        p.unplaced() == 0
            && p.mistakes() == 0
            && self.max_spread.is_none_or(|m| p.spread() <= m)
            && self.max_used.is_none_or(|m| p.used() as u32 <= m)
    }
}

/// Scenario: hosts and VMs are given, the policy is chosen by the student.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (also the goal identifier).
    pub id: String,
    /// Tab title.
    pub title: String,
    /// Goal text.
    pub goal: String,
    /// Scenario hint.
    pub hint: String,
    /// Cluster hosts.
    pub hosts: Vec<Host>,
    /// VMs to start, in order.
    pub vms: Vec<Vm>,
    /// Goal condition.
    pub check: SchedGoal,
}

impl Scenario {
    /// Exercise goal for this scenario.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Run the scenario with `policy`.
    pub fn run(&self, policy: &Policy) -> Plan {
        schedule(&self.hosts, &self.vms, policy)
    }

    /// Whether the goal is reached with `policy`.
    pub fn reached(&self, policy: &Policy) -> bool {
        self.check.check(&self.run(policy))
    }
}

/// Whether the factors are in the allowed range.
pub fn valid(policy: &Policy) -> bool {
    [policy.even, policy.free_mem, policy.pack].iter().all(|&f| f <= MAX_FACTOR)
}

/// Text of a mistake for the result table.
pub fn mistake_text(m: Mistake) -> &'static str {
    match m {
        Mistake::Memory => i18n::tr("not enough memory"),
        Mistake::Network => i18n::tr("no network on the host"),
        Mistake::Affinity => i18n::tr("two VMs of the group on one host"),
    }
}

fn host(name: &str, mem: i32, vms: u32, nets: &[&str]) -> Host {
    Host { name: name.into(), mem, vms, nets: nets.iter().map(|n| n.to_string()).collect() }
}

fn vm(name: &str, mem: i32, nets: &[&str], group: Option<&str>) -> Vm {
    Vm { name: name.into(), mem, nets: nets.iter().map(|n| n.to_string()).collect(), group: group.map(str::to_string) }
}

/// Default scenarios (chapter 22 exercise).
pub fn default_scenarios() -> Vec<Scenario> {
    vec![
        Scenario {
            id: "even".into(),
            title: i18n::tr("Even load").into(),
            goal: i18n::tr("Start 6 VMs so that hosts differ by at most one VM").into(),
            hint: i18n::tr("Without weights all hosts look the same and the first by name wins every time. Weights rank the hosts.").into(),
            hosts: vec![host("host1", 32, 0, &["ovirtmgmt"]), host("host2", 32, 0, &["ovirtmgmt"]), host("host3", 32, 0, &["ovirtmgmt"])],
            vms: (1..=6).map(|i| vm(&format!("vm{i}"), 2, &["ovirtmgmt"], None)).collect(),
            check: SchedGoal { max_spread: Some(1), max_used: None },
        },
        Scenario {
            id: "nets".into(),
            title: i18n::tr("Networks").into(),
            goal: i18n::tr("Start 4 VMs on hosts that have their networks, with a spread of at most one VM").into(),
            hint: i18n::tr("Not every host has every VLAN. A VM that lands on a host without its network starts with a dead NIC — the network filter prevents that.").into(),
            hosts: vec![
                host("host1", 32, 0, &["ovirtmgmt", "vlan10"]),
                host("host2", 32, 0, &["ovirtmgmt", "vlan10", "vlan20"]),
                host("host3", 32, 0, &["ovirtmgmt", "vlan20"]),
            ],
            vms: vec![
                vm("web1", 4, &["vlan20"], None),
                vm("web2", 4, &["vlan20"], None),
                vm("db1", 4, &["vlan10"], None),
                vm("db2", 4, &["vlan10"], None),
            ],
            check: SchedGoal { max_spread: Some(1), max_used: None },
        },
        Scenario {
            id: "anti".into(),
            title: i18n::tr("Anti-affinity").into(),
            goal: i18n::tr("Start two database replicas on different hosts and two application VMs").into(),
            hint: i18n::tr("The scheduler loves the emptiest host: without the affinity filter both replicas land there.").into(),
            hosts: vec![host("host1", 32, 0, &["ovirtmgmt"]), host("host2", 32, 3, &["ovirtmgmt"]), host("host3", 32, 3, &["ovirtmgmt"])],
            vms: vec![
                vm("db1", 8, &["ovirtmgmt"], Some("db")),
                vm("db2", 8, &["ovirtmgmt"], Some("db")),
                vm("app1", 4, &["ovirtmgmt"], None),
                vm("app2", 4, &["ovirtmgmt"], None),
            ],
            check: SchedGoal { max_spread: None, max_used: None },
        },
        Scenario {
            id: "pack".into(),
            title: i18n::tr("Power saving").into(),
            goal: i18n::tr("Start 5 VMs on at most two hosts so that every VM fits").into(),
            hint: i18n::tr("Power saving is the opposite of an even load. But packing without the memory filter overfills the first host.").into(),
            hosts: vec![host("host1", 16, 0, &["ovirtmgmt"]), host("host2", 16, 0, &["ovirtmgmt"]), host("host3", 16, 0, &["ovirtmgmt"])],
            vms: (1..=5).map(|i| vm(&format!("vm{i}"), 4, &["ovirtmgmt"], None)).collect(),
            check: SchedGoal { max_spread: None, max_used: Some(2) },
        },
    ]
}
