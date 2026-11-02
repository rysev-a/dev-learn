//! Bringing up an oVirt data center (chapter 17): the order of operations and the states of the objects.
//!
//! The student builds a small environment with the same actions an administrator performs in the Administration Portal: a cluster, hosts,
//! a logical network, a storage domain, a VM. Model rules:
//! * a host becomes Up when it is added; if the cluster has a required network the host does not have, it is NonOperational until the network
//!   is assigned to its NIC (Setup Host Networks);
//! * a storage domain is created by an Up host of the data center, then attached (it is inactive) and activated; the first active domain is the master;
//! * the data center is Up when its master domain is active and at least one host is Up; before that it is Uninitialized;
//! * a VM needs an active domain for its disk and a Up data center to run; it runs on an Up host that has the network of its NIC;
//! * a host with a running VM goes into maintenance only after the VM migrates; if there is no suitable host, the host stays in Preparing for
//!   Maintenance until one appears.
//!
//! The session mirrors the UI handlers: every accepted action is recorded, refused actions change nothing and are not recorded. The server replays the record.

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Hosts that can be added.
pub const HOSTS: u8 = 2;

/// Network of a VM's NIC.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Net {
    /// The management network, present on every host.
    Mgmt,
    /// The logical network `vm-net`, which must be created and assigned to host NICs.
    VmNet,
}

/// Host status.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HostStatus {
    /// Works.
    Up,
    /// The host lacks a required network.
    NonOperational,
    /// Waiting for its VM to migrate away.
    Preparing,
    /// In maintenance.
    Maintenance,
}

/// Host.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Host {
    /// Status.
    pub status: HostStatus,
    /// `vm-net` is assigned to the host's NIC.
    pub vm_net: bool,
}

/// Storage domain state.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Domain {
    /// Not created.
    #[default]
    Absent,
    /// Created, not attached to the data center.
    Unattached,
    /// Attached, inactive.
    Maintenance,
    /// Active (the first one is the master).
    Active,
}

/// Data center status.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DcStatus {
    /// No active master domain.
    Uninitialized,
    /// Works.
    Up,
    /// The domain is active, but no host is Up.
    NonResponsive,
}

/// VM.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Vm {
    /// Network of its NIC.
    pub net: Net,
    /// Host index (from 1) it runs on.
    pub host: Option<u8>,
}

/// State of the whole environment.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct State {
    /// The cluster is created.
    pub cluster: bool,
    /// Hosts 1 and 2.
    pub hosts: [Option<Host>; 2],
    /// The logical network `vm-net` is created and required in the cluster.
    pub net: bool,
    /// Storage domain.
    pub domain: Domain,
    /// The VM.
    pub vm: Option<Vm>,
}

/// Student action (an Administration Portal operation).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Action {
    /// Create the cluster.
    AddCluster,
    /// Add a host to the cluster.
    AddHost {
        /// Host number, 1 or 2.
        host: u8,
    },
    /// Create the logical network `vm-net` and make it required in the cluster.
    CreateNetwork,
    /// Assign `vm-net` to a host NIC.
    AssignNetwork {
        /// Host number.
        host: u8,
    },
    /// Create an NFS storage domain through an Up host.
    CreateDomain,
    /// Attach the domain to the data center.
    AttachDomain,
    /// Activate the domain.
    ActivateDomain,
    /// Create a VM with a disk on the domain.
    CreateVm {
        /// Network of the NIC.
        net: Net,
    },
    /// Run the VM.
    RunVm,
    /// Put a host into maintenance.
    Maintenance {
        /// Host number.
        host: u8,
    },
    /// Activate a host.
    ActivateHost {
        /// Host number.
        host: u8,
    },
}

/// Why an action is refused.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Refusal {
    /// No cluster.
    NoCluster,
    /// Cluster already exists.
    ClusterExists,
    /// Host number out of range.
    BadHost,
    /// No such host yet.
    NoHost,
    /// Host already added.
    HostExists,
    /// Network missing.
    NoNetwork,
    /// Network already created.
    NetworkExists,
    /// The data center has no Up host.
    NoUpHost,
    /// The domain exists.
    DomainExists,
    /// The domain is not in the state the operation needs.
    DomainState,
    /// No active domain for the VM's disk.
    NoActiveDomain,
    /// The VM exists.
    VmExists,
    /// No VM.
    NoVm,
    /// The VM is already running.
    AlreadyRunning,
    /// The data center is not Up.
    DcNotUp,
    /// No Up host with the VM's network.
    NoSuitableHost,
    /// The host is already in maintenance.
    AlreadyMaintenance,
    /// The host is not in maintenance.
    NotInMaintenance,
    /// The host is still preparing for maintenance.
    Preparing,
}

/// What an accepted action did (for the caption).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Note {
    /// Cluster created.
    ClusterAdded,
    /// Host added with this status.
    HostAdded(HostStatus),
    /// Network created; this many hosts became NonOperational.
    NetworkCreated(usize),
    /// Network assigned, the host has this status now.
    NetworkAssigned(HostStatus),
    /// Domain created.
    DomainCreated,
    /// Domain attached.
    DomainAttached,
    /// Domain activated, data center status.
    DomainActivated(DcStatus),
    /// VM created.
    VmCreated,
    /// VM started on host.
    VmStarted(u8),
    /// The host went into maintenance; the VM migrated to the given host (if there was one).
    HostInMaintenance(Option<u8>),
    /// The host is waiting for the VM to migrate.
    HostPreparing,
    /// The host was activated and got this status.
    HostActivated(HostStatus),
}

fn idx(host: u8) -> Result<usize, Refusal> {
    if (1..=HOSTS).contains(&host) {
        Ok(usize::from(host) - 1)
    } else {
        Err(Refusal::BadHost)
    }
}

impl State {
    /// Data center status.
    pub fn dc_status(&self) -> DcStatus {
        let up = self.hosts.iter().flatten().any(|h| h.status == HostStatus::Up);
        match (self.domain == Domain::Active, up) {
            (false, _) => DcStatus::Uninitialized,
            (true, true) => DcStatus::Up,
            (true, false) => DcStatus::NonResponsive,
        }
    }

    fn has_up_host(&self) -> bool {
        self.hosts.iter().flatten().any(|h| h.status == HostStatus::Up)
    }

    /// Host status after (re)checking the required network.
    fn working(&self, h: &Host) -> HostStatus {
        if self.net && !h.vm_net {
            HostStatus::NonOperational
        } else {
            HostStatus::Up
        }
    }

    fn refresh(&mut self) {
        for i in 0..self.hosts.len() {
            if let Some(h) = self.hosts[i] {
                if matches!(h.status, HostStatus::Up | HostStatus::NonOperational) {
                    let st = self.working(&h);
                    if let Some(h) = &mut self.hosts[i] {
                        h.status = st;
                    }
                }
            }
        }
    }

    /// Up host (index from 1) that can run a VM with the given network, other than `skip`.
    fn target(&self, net: Net, skip: Option<u8>) -> Option<u8> {
        (1..=HOSTS).find(|&n| {
            Some(n) != skip
                && self.hosts[usize::from(n) - 1]
                    .is_some_and(|h| h.status == HostStatus::Up && (net == Net::Mgmt || h.vm_net))
        })
    }

    /// A host waiting for maintenance finishes it as soon as its VM can migrate. Returns the target if a migration happened.
    fn settle(&mut self) -> Option<u8> {
        let vm = self.vm?;
        let from = vm.host?;
        if self.hosts[usize::from(from) - 1]?.status != HostStatus::Preparing {
            return None;
        }
        let to = self.target(vm.net, Some(from))?;
        self.vm = Some(Vm { host: Some(to), ..vm });
        if let Some(h) = &mut self.hosts[usize::from(from) - 1] {
            h.status = HostStatus::Maintenance;
        }
        Some(to)
    }

    /// Perform an action. The error means the state did not change.
    pub fn apply(&mut self, a: Action) -> Result<Note, Refusal> {
        let note = match a {
            Action::AddCluster => {
                if self.cluster {
                    return Err(Refusal::ClusterExists);
                }
                self.cluster = true;
                Note::ClusterAdded
            }
            Action::AddHost { host } => {
                let i = idx(host)?;
                if !self.cluster {
                    return Err(Refusal::NoCluster);
                }
                if self.hosts[i].is_some() {
                    return Err(Refusal::HostExists);
                }
                let h = Host { status: HostStatus::Up, vm_net: false };
                let status = self.working(&h);
                self.hosts[i] = Some(Host { status, ..h });
                Note::HostAdded(status)
            }
            Action::CreateNetwork => {
                if !self.cluster {
                    return Err(Refusal::NoCluster);
                }
                if self.net {
                    return Err(Refusal::NetworkExists);
                }
                self.net = true;
                let before = self.hosts.iter().flatten().filter(|h| h.status == HostStatus::NonOperational).count();
                self.refresh();
                let after = self.hosts.iter().flatten().filter(|h| h.status == HostStatus::NonOperational).count();
                Note::NetworkCreated(after - before)
            }
            Action::AssignNetwork { host } => {
                let i = idx(host)?;
                if !self.net {
                    return Err(Refusal::NoNetwork);
                }
                let Some(h) = &mut self.hosts[i] else {
                    return Err(Refusal::NoHost);
                };
                h.vm_net = true;
                self.refresh();
                Note::NetworkAssigned(self.hosts[i].map_or(HostStatus::Up, |h| h.status))
            }
            Action::CreateDomain => {
                if self.domain != Domain::Absent {
                    return Err(Refusal::DomainExists);
                }
                if !self.has_up_host() {
                    return Err(Refusal::NoUpHost);
                }
                self.domain = Domain::Unattached;
                Note::DomainCreated
            }
            Action::AttachDomain => {
                if self.domain != Domain::Unattached {
                    return Err(Refusal::DomainState);
                }
                self.domain = Domain::Maintenance;
                Note::DomainAttached
            }
            Action::ActivateDomain => {
                if self.domain != Domain::Maintenance {
                    return Err(Refusal::DomainState);
                }
                if !self.has_up_host() {
                    return Err(Refusal::NoUpHost);
                }
                self.domain = Domain::Active;
                Note::DomainActivated(self.dc_status())
            }
            Action::CreateVm { net } => {
                if !self.cluster {
                    return Err(Refusal::NoCluster);
                }
                if self.vm.is_some() {
                    return Err(Refusal::VmExists);
                }
                if self.domain != Domain::Active {
                    return Err(Refusal::NoActiveDomain);
                }
                if net == Net::VmNet && !self.net {
                    return Err(Refusal::NoNetwork);
                }
                self.vm = Some(Vm { net, host: None });
                Note::VmCreated
            }
            Action::RunVm => {
                let vm = self.vm.ok_or(Refusal::NoVm)?;
                if vm.host.is_some() {
                    return Err(Refusal::AlreadyRunning);
                }
                if self.dc_status() != DcStatus::Up {
                    return Err(Refusal::DcNotUp);
                }
                let to = self.target(vm.net, None).ok_or(Refusal::NoSuitableHost)?;
                self.vm = Some(Vm { host: Some(to), ..vm });
                Note::VmStarted(to)
            }
            Action::Maintenance { host } => {
                let i = idx(host)?;
                let h = self.hosts[i].ok_or(Refusal::NoHost)?;
                match h.status {
                    HostStatus::Maintenance => return Err(Refusal::AlreadyMaintenance),
                    HostStatus::Preparing => return Err(Refusal::Preparing),
                    _ => {}
                }
                let runs = self.vm.filter(|v| v.host == Some(host));
                let mut moved = None;
                let mut status = HostStatus::Maintenance;
                if let Some(vm) = runs {
                    match self.target(vm.net, Some(host)) {
                        Some(to) => {
                            self.vm = Some(Vm { host: Some(to), ..vm });
                            moved = Some(to);
                        }
                        None => status = HostStatus::Preparing,
                    }
                }
                if let Some(h) = &mut self.hosts[i] {
                    h.status = status;
                }
                if status == HostStatus::Preparing {
                    Note::HostPreparing
                } else {
                    Note::HostInMaintenance(moved)
                }
            }
            Action::ActivateHost { host } => {
                let i = idx(host)?;
                let h = self.hosts[i].ok_or(Refusal::NoHost)?;
                match h.status {
                    HostStatus::Maintenance => {}
                    HostStatus::Preparing => return Err(Refusal::Preparing),
                    _ => return Err(Refusal::NotInMaintenance),
                }
                let st = self.working(&h);
                if let Some(h) = &mut self.hosts[i] {
                    h.status = st;
                }
                Note::HostActivated(st)
            }
        };
        Ok(note)
    }
}

/// Goal rule.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum DcRule {
    /// The data center is Up.
    DcUp,
    /// The VM runs and its NIC is on the given network.
    VmRunning {
        /// Network of the NIC.
        net: Net,
    },
    /// A host with the running VM went into maintenance and the VM migrated away.
    Migrated,
}

/// Exercise goal.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DcGoal {
    /// Goal identifier.
    pub id: String,
    /// Goal text.
    pub text: String,
    /// Rule.
    pub rule: DcRule,
}

impl DcGoal {
    /// Goal for display.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Exercise progress: environment state and achieved goals.
#[derive(Clone, Debug)]
pub struct Session {
    goals: Vec<DcGoal>,
    state: State,
    done: Vec<String>,
}

impl Session {
    /// New exercise: an empty environment.
    pub fn new(goals: &[DcGoal]) -> Session {
        Session { goals: goals.to_vec(), state: State::default(), done: vec![] }
    }

    /// Environment state.
    pub fn state(&self) -> &State {
        &self.state
    }

    /// Identifiers of achieved goals (in order of achievement).
    pub fn done(&self) -> &[String] {
        &self.done
    }

    /// Whether all goals are achieved.
    pub fn solved(&self) -> bool {
        self.goals.iter().all(|g| self.done.contains(&g.id))
    }

    /// Perform an action and mark goals.
    pub fn act(&mut self, a: Action) -> Result<Note, Refusal> {
        let note = self.state.apply(a)?;
        // a host waiting for maintenance leaves as soon as the VM can move
        let late = self.state.settle();
        let migrated = late.is_some() || matches!(note, Note::HostInMaintenance(Some(_)));
        for g in &self.goals {
            let hit = match g.rule {
                DcRule::DcUp => self.state.dc_status() == DcStatus::Up,
                DcRule::VmRunning { net } => self.state.vm.is_some_and(|v| v.host.is_some() && v.net == net),
                DcRule::Migrated => migrated,
            };
            if hit && !self.done.contains(&g.id) {
                self.done.push(g.id.clone());
            }
        }
        Ok(note)
    }
}

/// Replay recorded actions and return the achieved goals (refused actions are skipped, as in the interface).
pub fn replay(goals: &[DcGoal], actions: &[Action]) -> Vec<String> {
    let mut s = Session::new(goals);
    for a in actions {
        let _ = s.act(*a);
    }
    s.done
}

/// Text of the caption after an accepted action.
pub fn note_text(n: &Note) -> String {
    match n {
        Note::ClusterAdded => i18n::tr("Cluster created: a group of hosts with the same CPU type and one set of networks.").into(),
        Note::HostAdded(HostStatus::Up) => i18n::tr("Host added and Up: the engine installed VDSM and the host reports to it.").into(),
        Note::HostAdded(_) => i18n::tr("Host added, but NonOperational: it lacks the cluster's required network.").into(),
        Note::NetworkCreated(0) => i18n::tr("Network vm-net created and required in the cluster.").into(),
        Note::NetworkCreated(n) => {
            i18n::trf!("Network vm-net is required in the cluster: {0} host(s) without it became NonOperational. Assign the network to their NICs.", n)
        }
        Note::NetworkAssigned(HostStatus::Up) => i18n::tr("vm-net is assigned to the NIC: the host is Up.").into(),
        Note::NetworkAssigned(_) => i18n::tr("vm-net is assigned to the NIC.").into(),
        Note::DomainCreated => i18n::tr("Domain created through an Up host (Use Host), it is not attached to the data center yet.").into(),
        Note::DomainAttached => i18n::tr("Domain attached to the data center, it is inactive (Maintenance).").into(),
        Note::DomainActivated(DcStatus::Up) => i18n::tr("Domain active — it became the master. The data center is Up.").into(),
        Note::DomainActivated(_) => i18n::tr("Domain is active, but the data center has no Up host.").into(),
        Note::VmCreated => i18n::tr("VM created: the disk is on the active domain, the NIC is on the chosen network.").into(),
        Note::VmStarted(h) => i18n::trf!("The scheduler started the VM on host {0}.", h),
        Note::HostInMaintenance(Some(to)) => i18n::trf!("Host in maintenance: its VM was migrated to host {0}.", to),
        Note::HostInMaintenance(None) => i18n::tr("Host in maintenance.").into(),
        Note::HostPreparing => {
            i18n::tr("Preparing for maintenance: the VM has nowhere to migrate. Add a suitable host — the maintenance will finish by itself.").into()
        }
        Note::HostActivated(HostStatus::Up) => i18n::tr("Host activated and Up.").into(),
        Note::HostActivated(_) => i18n::tr("Host activated, but NonOperational: it lacks a required network.").into(),
    }
}

/// Text of the refusal.
pub fn refusal_text(r: Refusal) -> &'static str {
    match r {
        Refusal::NoCluster => i18n::tr("There is no cluster yet."),
        Refusal::ClusterExists => i18n::tr("The cluster already exists."),
        Refusal::BadHost => i18n::tr("No such host number."),
        Refusal::NoHost => i18n::tr("This host has not been added yet."),
        Refusal::HostExists => i18n::tr("This host has already been added."),
        Refusal::NoNetwork => i18n::tr("The network vm-net has not been created yet."),
        Refusal::NetworkExists => i18n::tr("The network vm-net already exists."),
        Refusal::NoUpHost => {
            i18n::tr("The data center has no Up host: someone has to perform the operation on the storage.")
        }
        Refusal::DomainExists => i18n::tr("The storage domain already exists."),
        Refusal::DomainState => {
            i18n::tr("The domain is not in the right state for this operation: create, attach, then activate.")
        }
        Refusal::NoActiveDomain => i18n::tr("There is no active storage domain for the VM's disk."),
        Refusal::VmExists => i18n::tr("The VM already exists."),
        Refusal::NoVm => i18n::tr("There is no VM yet."),
        Refusal::AlreadyRunning => i18n::tr("The VM is already running."),
        Refusal::DcNotUp => i18n::tr("The data center is not Up: a VM cannot run."),
        Refusal::NoSuitableHost => i18n::tr("No Up host has the network of the VM's NIC."),
        Refusal::AlreadyMaintenance => i18n::tr("The host is already in maintenance."),
        Refusal::NotInMaintenance => i18n::tr("The host is not in maintenance."),
        Refusal::Preparing => i18n::tr("The host is preparing for maintenance: wait for the VM to migrate."),
    }
}

/// Default goals (chapter 17 exercise).
pub fn default_goals() -> Vec<DcGoal> {
    vec![
        DcGoal {
            id: "dc_up".into(),
            text: i18n::tr("Bring the data center to Up: a host and the master storage domain are active").into(),
            rule: DcRule::DcUp,
        },
        DcGoal {
            id: "vm_net".into(),
            text: i18n::tr("Run a VM whose NIC is on the vm-net network").into(),
            rule: DcRule::VmRunning { net: Net::VmNet },
        },
        DcGoal {
            id: "migrate".into(),
            text: i18n::tr("Put the host running the VM into maintenance so that the VM migrates to another host")
                .into(),
            rule: DcRule::Migrated,
        },
    ]
}
