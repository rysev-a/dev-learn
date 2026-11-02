//! Host fencing model of oVirt (chapter 19).
//!
//! The engine lost contact with a host and decides what to do. Model rules (the order follows the chapter): the host becomes a fencing
//! candidate; if **soft fencing** is on and the host answers over SSH, VDSM is restarted and the host returns to Up; otherwise the **cluster
//! policy** may skip fencing (a live storage lease, or the engine lost contact with at least the given share of the cluster); otherwise **power
//! management** switches the host off and on. Highly available VMs are restarted elsewhere only when the host is known to be off
//! (fencing succeeded) or when they hold a VM lease on storage and the host is really dead.
//!
//! A scenario ([`Scenario`]) fixes the physical situation; the student sets the policy ([`FenceConfig`]). The scenario goal is checked
//! against the simulation result, so the server re-runs the same simulation from the submitted settings.

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Fencing settings of the cluster and of the VMs.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FenceConfig {
    /// Soft fencing: restart VDSM over SSH before anything else.
    pub soft: bool,
    /// Power management (a fence agent) is configured on the hosts.
    pub power: bool,
    /// Policy: skip fencing if the host has a live lease on storage.
    pub skip_lease: bool,
    /// Policy: skip fencing on cluster connectivity issues.
    pub skip_connectivity: bool,
    /// Share of unreachable hosts (percent) at which fencing is skipped.
    pub threshold: u32,
    /// Highly available VMs hold a VM lease on storage.
    pub vm_leases: bool,
}

impl Default for FenceConfig {
    fn default() -> Self {
        FenceConfig {
            soft: false,
            power: false,
            skip_lease: false,
            skip_connectivity: false,
            threshold: 50,
            vm_leases: false,
        }
    }
}

/// What the engine ended up doing with the host.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    /// Soft fencing worked: the host is Up again, nothing was rebooted.
    Recovered,
    /// Fencing skipped: the host holds a live storage lease.
    SkippedLease,
    /// Fencing skipped: too many hosts of the cluster are unreachable.
    SkippedConnectivity,
    /// The host was switched off and on through power management.
    Fenced,
    /// A power management command was sent but did not work (the controller is unreachable).
    FenceFailed,
    /// No power management: the administrator has to confirm that the host was rebooted.
    Manual,
}

/// A step of the engine, in order.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "step", rename_all = "snake_case")]
pub enum Step {
    /// The host became a fencing candidate.
    Candidate,
    /// Soft fencing worked.
    SoftOk,
    /// Soft fencing did not help (SSH is unreachable).
    SoftFail,
    /// Policy: live lease.
    SkipLease,
    /// Policy: connectivity.
    SkipConnectivity {
        /// Unreachable hosts.
        down: u32,
        /// Hosts in the cluster.
        hosts: u32,
        /// Threshold, percent.
        threshold: u32,
    },
    /// Power cycle done.
    PowerCycled,
    /// Power management failed.
    PowerFailed,
    /// Waiting for the administrator.
    ManualConfirm,
    /// Running VMs died with the reboot.
    VmsKilled,
    /// Running VMs keep running.
    VmsKeepRunning,
    /// The HA VM was restarted on another host.
    HaRestarted,
    /// The HA VM stays down.
    HaWaits,
}

/// Simulation result.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Simulation {
    /// Final outcome.
    pub outcome: Outcome,
    /// What happened, in order.
    pub steps: Vec<Step>,
    /// The HA VM was started on another host.
    pub ha_restarted: bool,
    /// Working VMs were killed by a reboot of a live host.
    pub vms_killed: bool,
}

/// Physical situation: what really happened to the host and the cluster.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Situation {
    /// Hosts in the cluster.
    pub hosts: u32,
    /// Hosts the engine lost contact with (including the faulty one).
    pub down: u32,
    /// The host is alive and its VMs keep working.
    pub alive: bool,
    /// The host still renews its storage lease.
    pub lease: bool,
    /// The host answers over SSH, so restarting VDSM brings it back.
    pub ssh: bool,
    /// The power controller (BMC) answers.
    pub bmc: bool,
}

/// Condition on the simulation result (unspecified fields are not checked).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FenceGoal {
    /// Required outcome.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub outcome: Option<Outcome>,
    /// The HA VM must (or must not) be restarted.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ha_restarted: Option<bool>,
}

impl FenceGoal {
    /// Whether the goal is reached on result `r`.
    pub fn check(&self, r: &Simulation) -> bool {
        self.outcome.is_none_or(|o| o == r.outcome) && self.ha_restarted.is_none_or(|h| h == r.ha_restarted)
    }
}

/// Scenario: the situation is given, the settings are chosen by the student.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (also the goal identifier).
    pub id: String,
    /// Tab title.
    pub title: String,
    /// What happened (shown above the settings).
    pub story: String,
    /// Goal text.
    pub goal: String,
    /// Scenario hint.
    pub hint: String,
    /// Physical situation.
    pub situation: Situation,
    /// Goal condition.
    pub check: FenceGoal,
}

impl Scenario {
    /// Exercise goal for this scenario.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Whether the goal is reached with settings `cfg`.
    pub fn reached(&self, cfg: &FenceConfig) -> bool {
        self.check.check(&simulate(cfg, &self.situation))
    }
}

/// Whether the settings are in the allowed range.
pub fn valid(cfg: &FenceConfig) -> bool {
    (1..=100).contains(&cfg.threshold)
}

/// Run the engine's reaction to a non-responsive host.
pub fn simulate(cfg: &FenceConfig, s: &Situation) -> Simulation {
    let mut steps = vec![Step::Candidate];
    // HA by VM lease: the host is really dead, its lease expires and the VM can be started elsewhere without fencing
    let ha_by_lease = cfg.vm_leases && !s.alive;
    if cfg.soft {
        if s.ssh {
            steps.push(Step::SoftOk);
            return Simulation { outcome: Outcome::Recovered, steps, ha_restarted: false, vms_killed: false };
        }
        steps.push(Step::SoftFail);
    }
    if cfg.skip_lease && s.lease {
        steps.push(Step::SkipLease);
        steps.push(Step::VmsKeepRunning);
        return Simulation { outcome: Outcome::SkippedLease, steps, ha_restarted: false, vms_killed: false };
    }
    if cfg.skip_connectivity && 100 * s.down >= cfg.threshold * s.hosts {
        steps.push(Step::SkipConnectivity { down: s.down, hosts: s.hosts, threshold: cfg.threshold });
        steps.push(if s.alive { Step::VmsKeepRunning } else { Step::HaWaits });
        return Simulation { outcome: Outcome::SkippedConnectivity, steps, ha_restarted: false, vms_killed: false };
    }
    let (outcome, ha) = if !cfg.power {
        steps.push(Step::ManualConfirm);
        (Outcome::Manual, ha_by_lease)
    } else if s.bmc {
        steps.push(Step::PowerCycled);
        (Outcome::Fenced, true)
    } else {
        steps.push(Step::PowerFailed);
        (Outcome::FenceFailed, ha_by_lease)
    };
    let killed = outcome == Outcome::Fenced && s.alive;
    if killed {
        steps.push(Step::VmsKilled);
    }
    steps.push(if ha { Step::HaRestarted } else { Step::HaWaits });
    Simulation { outcome, steps, ha_restarted: ha, vms_killed: killed }
}

/// Text of a step for the log.
pub fn step_text(step: &Step) -> String {
    match step {
        Step::Candidate => i18n::tr("The host does not answer: two failures in a row and 60 seconds — it is a fencing candidate.").into(),
        Step::SoftOk => i18n::tr("Soft fencing: VDSM was restarted over SSH, the host answers and is Up. Nothing was rebooted.").into(),
        Step::SoftFail => i18n::tr("Soft fencing: the host is unreachable over SSH, restarting VDSM did not help.").into(),
        Step::SkipLease => i18n::tr("Policy: the host holds a live lease on storage — it is alive, fencing is skipped.").into(),
        Step::SkipConnectivity { down, hosts, threshold } => i18n::trf!(
            "Policy: contact is lost with {0} of {1} hosts (threshold {2}%) — most likely the engine's network is broken, fencing is skipped.",
            down,
            hosts,
            threshold
        ),
        Step::PowerCycled => i18n::tr("Power management: the host was switched off, checked to be off and switched on again.").into(),
        Step::PowerFailed => i18n::tr("Power management: the controller does not answer, the host could not be switched off.").into(),
        Step::ManualConfirm => i18n::tr("No power management: the administrator has to confirm that the host was rebooted.").into(),
        Step::VmsKilled => i18n::tr("The host was alive: its working VMs were killed by the reboot.").into(),
        Step::VmsKeepRunning => i18n::tr("The VMs on the host keep running.").into(),
        Step::HaRestarted => i18n::tr("The highly available VM was restarted on another host.").into(),
        Step::HaWaits => i18n::tr("The highly available VM stays down: the engine does not know whether the host is off.").into(),
    }
}

/// Default scenarios (chapter 19 exercise).
pub fn default_scenarios() -> Vec<Scenario> {
    let sit = |hosts, down, alive, lease, ssh, bmc| Situation { hosts, down, alive, lease, ssh, bmc };
    let goal = |outcome, ha_restarted| FenceGoal { outcome, ha_restarted };
    vec![
        Scenario {
            id: "hung".into(),
            title: i18n::tr("VDSM hung").into(),
            story: i18n::tr("One host of four stopped answering because the vdsmd process hung. The server itself works, its VMs run, SSH answers.").into(),
            goal: i18n::tr("Bring the host back to Up without a reboot").into(),
            hint: i18n::tr("The cheapest step comes first: restart the service, not the whole server.").into(),
            situation: sit(4, 1, true, true, true, true),
            check: goal(Some(Outcome::Recovered), None),
        },
        Scenario {
            id: "dead".into(),
            title: i18n::tr("The server died").into(),
            story: i18n::tr("One host of four lost power. Its VMs are down, one of them is highly available. SSH does not answer, the controller works.").into(),
            goal: i18n::tr("Switch the host off and on through power management and restart the highly available VM elsewhere").into(),
            hint: i18n::tr("A VM may be started elsewhere only after the engine is sure the host is off. A threshold that is too low would also skip this case.").into(),
            situation: sit(4, 1, false, false, false, true),
            check: goal(Some(Outcome::Fenced), Some(true)),
        },
        Scenario {
            id: "mgmt".into(),
            title: i18n::tr("Management network down").into(),
            story: i18n::tr("The management network cable of one host is broken. The host is alive, its VMs work and write to storage over another network, SSH is unreachable.").into(),
            goal: i18n::tr("Do not touch the host: fencing is skipped because of the live lease").into(),
            hint: i18n::tr("A reboot of a working host would kill its VMs. The lease on storage proves the host is alive.").into(),
            situation: sit(4, 1, true, true, false, true),
            check: goal(Some(Outcome::SkippedLease), None),
        },
        Scenario {
            id: "switch".into(),
            title: i18n::tr("The switch failed").into(),
            story: i18n::tr("The management switch failed: the engine lost contact with 3 of 4 hosts. The hosts are alive, but the storage runs through the same switch, so leases cannot be read.").into(),
            goal: i18n::tr("Skip fencing because of connectivity issues, without a storm of reboots").into(),
            hint: i18n::tr("Three of four is 75%. The threshold must be low enough to skip this, but high enough not to skip one dead host out of four.").into(),
            situation: sit(4, 3, true, false, false, true),
            check: goal(Some(Outcome::SkippedConnectivity), None),
        },
        Scenario {
            id: "bmc".into(),
            title: i18n::tr("The controller died too").into(),
            story: i18n::tr("A host lost power together with its management controller: power management cannot reach it. A highly available VM was running on it.").into(),
            goal: i18n::tr("Restart the highly available VM even though the host cannot be fenced").into(),
            hint: i18n::tr("A VM with a lease on storage can be started elsewhere once the dead host stops renewing it.").into(),
            situation: sit(4, 1, false, false, false, false),
            check: goal(None, Some(true)),
        },
    ]
}
