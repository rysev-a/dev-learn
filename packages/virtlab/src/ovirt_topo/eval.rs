//! Statuses derived from the links of the board.

use super::{DomainType, Kind, Node, Rel, Role, Topology};


/// Status of a host as the Administration Portal shows it.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum HostStatus {
    /// The host works.
    Up,
    /// The engine cannot reach VDSM: there is no management network between them.
    NonResponsive,
    /// The host answers but misses a required network or a storage domain.
    NonOperational,
    /// The host is not in a cluster of a data center yet.
    NoCluster,
    /// The administrator put the host into maintenance: it runs no VMs and does not count as Up.
    Maintenance,
}

impl HostStatus {
    /// Name as the portal writes it.
    pub fn name(self) -> &'static str {
        match self {
            HostStatus::Up => "Up",
            HostStatus::NonResponsive => "NonResponsive",
            HostStatus::NonOperational => "NonOperational",
            HostStatus::NoCluster => "No cluster",
            HostStatus::Maintenance => "Maintenance",
        }
    }
}

/// Why a host is not Up.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Why {
    /// The host is not in a cluster.
    NoCluster,
    /// The cluster is not in a data center.
    NoDataCenter,
    /// No management network connects the engine to the host.
    NoManagementPath,
    /// A required network of the cluster is not assigned to the host (the network name).
    MissingNetwork(String),
    /// The host does not see a storage domain of its data center (the domain name).
    MissingStorage(String),
    /// An iSCSI domain of its data center needs a network with the storage role on the host (the domain name).
    NoStorageNetwork(String),
    /// The host is in maintenance mode.
    Maintenance,
}

impl Why {
    /// Explanation for the student.
    pub fn text(&self) -> String {
        match self {
            Why::NoCluster => i18n::tr("the host is not a member of a cluster").to_string(),
            Why::NoDataCenter => i18n::tr("the cluster is not in a data center").to_string(),
            Why::NoManagementPath => {
                i18n::tr("the engine cannot reach the host: no management network between them").to_string()
            }
            Why::MissingNetwork(n) => i18n::trf!("the required network “{0}” is not assigned to the host", n),
            Why::MissingStorage(d) => i18n::trf!("the host does not see the storage domain “{0}”", d),
            Why::NoStorageNetwork(d) => {
                i18n::trf!("the domain “{0}” is iSCSI: the host needs a network with the storage role", d)
            }
            Why::Maintenance => i18n::tr("the host is in maintenance mode: it runs no VMs").to_string(),
        }
    }
}

/// State of a host.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HostEval {
    /// Object identifier.
    pub id: String,
    /// Status.
    pub status: HostStatus,
    /// Why it is not Up.
    pub why: Vec<Why>,
}

/// Status of a storage domain.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum DomainStatus {
    /// Not attached to a data center.
    Unattached,
    /// Attached, but no Up host sees it.
    Inactive,
    /// Attached and seen by an Up host.
    Active,
}

impl DomainStatus {
    /// Name as the portal writes it.
    pub fn name(self) -> &'static str {
        match self {
            DomainStatus::Unattached => "Unattached",
            DomainStatus::Inactive => "Inactive",
            DomainStatus::Active => "Active",
        }
    }
}

/// State of a storage domain.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DomainEval {
    /// Object identifier.
    pub id: String,
    /// Status.
    pub status: DomainStatus,
    /// The first domain attached to the data center is its master.
    pub master: bool,
}

/// Status of a data center.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum DcStatus {
    /// An Up host and an active master domain.
    Up,
    /// There is an Up host, but no active master domain.
    Uninitialized,
    /// No Up host.
    NonResponsive,
}

impl DcStatus {
    /// Name as the portal writes it.
    pub fn name(self) -> &'static str {
        match self {
            DcStatus::Up => "Up",
            DcStatus::Uninitialized => "Uninitialized",
            DcStatus::NonResponsive => "Non Responsive",
        }
    }
}

/// State of a data center.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DcEval {
    /// Object identifier.
    pub id: String,
    /// Status.
    pub status: DcStatus,
    /// Storage pool manager: the first Up host of an Up data center.
    pub spm: Option<String>,
}

/// Status of a VM.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VmStatus {
    /// Running.
    Running,
    /// Cannot run.
    Down,
}

/// Why a VM does not run.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum VmWhy {
    /// The VM is not placed on a host.
    NoHost,
    /// The host is not Up (the host name).
    HostNotUp(String),
    /// The data center is not Up.
    DcNotUp,
    /// The network of the virtual NIC is not assigned to the host (the network name).
    NetworkMissing(String),
    /// The disk is on a domain that is not active in the host's data center (the domain name).
    DiskInactive(String),
    /// The host is in maintenance mode (the host name).
    HostMaintenance(String),
    /// The VMs placed on the host need more memory than it has (the host name).
    NoMemory(String),
    /// The VM breaks a hard affinity group (the group name).
    AffinityViolated(String),
}

impl VmWhy {
    /// Explanation for the student.
    pub fn text(&self) -> String {
        match self {
            VmWhy::NoHost => i18n::tr("the VM is not placed on a host").to_string(),
            VmWhy::HostNotUp(h) => i18n::trf!("the host “{0}” is not Up", h),
            VmWhy::DcNotUp => i18n::tr("the data center is not Up").to_string(),
            VmWhy::NetworkMissing(n) => {
                i18n::trf!("the network “{0}” of the virtual NIC is not assigned to the host", n)
            }
            VmWhy::DiskInactive(d) => {
                i18n::trf!("the disk is on “{0}”, which is not an active domain of the host's data center", d)
            }
            VmWhy::HostMaintenance(h) => i18n::trf!("the host “{0}” is in maintenance mode", h),
            VmWhy::NoMemory(h) => i18n::trf!("the VMs placed on the host “{0}” need more memory than it has", h),
            VmWhy::AffinityViolated(g) => i18n::trf!("the VM breaks the hard affinity group “{0}”", g),
        }
    }
}

/// State of a VM.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct VmEval {
    /// Object identifier.
    pub id: String,
    /// Status.
    pub status: VmStatus,
    /// Why it does not run.
    pub why: Vec<VmWhy>,
}

/// Statuses of all objects of a board.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Evaluation {
    /// Hosts, in board order.
    pub hosts: Vec<HostEval>,
    /// Storage domains.
    pub domains: Vec<DomainEval>,
    /// Data centers.
    pub dcs: Vec<DcEval>,
    /// VMs.
    pub vms: Vec<VmEval>,
}

impl Evaluation {
    /// Host state.
    pub fn host(&self, id: &str) -> Option<&HostEval> {
        self.hosts.iter().find(|h| h.id == id)
    }

    /// Domain state.
    pub fn domain(&self, id: &str) -> Option<&DomainEval> {
        self.domains.iter().find(|d| d.id == id)
    }

    /// Data center state.
    pub fn dc(&self, id: &str) -> Option<&DcEval> {
        self.dcs.iter().find(|d| d.id == id)
    }

    /// VM state.
    pub fn vm(&self, id: &str) -> Option<&VmEval> {
        self.vms.iter().find(|v| v.id == id)
    }

    /// The host is Up.
    pub fn host_up(&self, id: &str) -> bool {
        self.host(id).is_some_and(|h| h.status == HostStatus::Up)
    }
}

/// The management network that connects the engine of the host's data center to the host: `(engine, network)`.
pub fn management_path<'a>(t: &'a Topology, host: &str) -> Option<(&'a str, &'a str)> {
    let dc = t.dc_of_host(host)?;
    t.sources(&dc.id, Rel::Manages).find_map(|e| {
        t.targets(&e.id, Rel::EngineNic)
            .find(|n| n.role() == Role::Management && t.linked(&n.id, host))
            .map(|n| (e.id.as_str(), n.id.as_str()))
    })
}

/// Required networks of the cluster of a host that are not assigned to the host (a host outside a cluster misses none).
pub fn missing_networks<'a>(t: &'a Topology, host: &str) -> Vec<&'a Node> {
    let Some(cluster) = t.cluster_of_host(host) else {
        return vec![];
    };
    t.sources(&cluster.id, Rel::Attached).filter(|n| n.required() && !t.linked(&n.id, host)).collect()
}

/// Storage domains attached to the data center of a host that the host does not see.
pub fn missing_domains<'a>(t: &'a Topology, host: &str) -> Vec<&'a Node> {
    let Some(dc) = t.dc_of_host(host) else {
        return vec![];
    };
    t.targets(&dc.id, Rel::Domain).filter(|d| !t.linked(&d.id, host)).collect()
}

/// iSCSI domains attached to the data center of a host when the host has no network with the storage role assigned (none otherwise).
pub fn iscsi_without_network<'a>(t: &'a Topology, host: &str) -> Vec<&'a Node> {
    let Some(dc) = t.dc_of_host(host) else {
        return vec![];
    };
    if t.of_kind(Kind::Network).any(|n| n.role() == Role::Storage && t.linked(&n.id, host)) {
        return vec![];
    }
    t.targets(&dc.id, Rel::Domain).filter(|d| d.domain_type() == DomainType::Iscsi).collect()
}

/// Networks of the virtual NICs of a VM that are not assigned to the host the VM runs on (none without a host).
pub fn unplugged_networks<'a>(t: &'a Topology, vm: &str) -> Vec<&'a Node> {
    let Some(host) = t.host_of_vm(vm) else {
        return vec![];
    };
    t.sources(vm, Rel::Vnic).filter(|n| !t.linked(&n.id, &host.id)).collect()
}

/// Memory of a host: what the VMs placed on it need and what it has (GB).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct HostLoad {
    /// Sum of the memory of the VMs placed on the host.
    pub used: u32,
    /// Memory of the host.
    pub capacity: u32,
}

impl HostLoad {
    /// The VMs need more than the host has: none of them can run.
    pub fn over(self) -> bool {
        self.used > self.capacity
    }
}

/// The memory load of a host: every VM linked to it counts, running or not.
pub fn host_load(t: &Topology, host: &str) -> HostLoad {
    HostLoad {
        used: t.targets(host, Rel::Runs).map(Node::mem_gb).sum(),
        capacity: t.node(host).map_or(0, Node::mem_gb),
    }
}

/// The members of an affinity group that break its rule (only placed VMs count; the first placed member sets the example):
/// in a negative group a member on a host an earlier member is on, in a positive group a member not on the host of the first one.
pub fn affinity_breaks(t: &Topology, group: &str) -> Vec<String> {
    let Some(g) = t.node(group) else { return vec![] };
    let positive = g.polarity() == super::Polarity::Positive;
    let mut out = vec![];
    let mut hosts: Vec<&str> = vec![];
    for vm in t.targets(group, Rel::Affine) {
        let Some(host) = t.host_of_vm(&vm.id) else { continue };
        let broken = if positive { hosts.first().is_some_and(|h| *h != host.id) } else { hosts.contains(&host.id.as_str()) };
        if broken {
            out.push(vm.id.clone());
        }
        hosts.push(&host.id);
    }
    out
}

/// Derive the statuses of every object.
pub fn evaluate(t: &Topology) -> Evaluation {
    let mut ev = Evaluation::default();
    for h in t.of_kind(Kind::Host) {
        ev.hosts.push(host_eval(t, &h.id));
    }
    for d in t.of_kind(Kind::StorageDomain) {
        let dc = t.sources(&d.id, Rel::Domain).next();
        let status = match dc {
            None => DomainStatus::Unattached,
            Some(dc) => {
                if t.hosts_of_dc(&dc.id).any(|h| ev.host_up(&h.id) && t.linked(&d.id, &h.id)) {
                    DomainStatus::Active
                } else {
                    DomainStatus::Inactive
                }
            }
        };
        let master = dc.is_some_and(|dc| t.targets(&dc.id, Rel::Domain).next().is_some_and(|first| first.id == d.id));
        ev.domains.push(DomainEval { id: d.id.clone(), status, master });
    }
    for dc in t.of_kind(Kind::DataCenter) {
        let first_up = t.hosts_of_dc(&dc.id).find(|h| ev.host_up(&h.id)).map(|h| h.id.clone());
        let master_active = t
            .targets(&dc.id, Rel::Domain)
            .next()
            .is_some_and(|m| ev.domain(&m.id).is_some_and(|d| d.status == DomainStatus::Active));
        let status = match (&first_up, master_active) {
            (None, _) => DcStatus::NonResponsive,
            (Some(_), false) => DcStatus::Uninitialized,
            (Some(_), true) => DcStatus::Up,
        };
        let spm = if status == DcStatus::Up { first_up } else { None };
        ev.dcs.push(DcEval { id: dc.id.clone(), status, spm });
    }
    for vm in t.of_kind(Kind::Vm) {
        let vm_eval = vm_eval(t, &ev, &vm.id);
        ev.vms.push(vm_eval);
    }
    ev
}

fn host_eval(t: &Topology, id: &str) -> HostEval {
    let mut why = vec![];
    let Some(cluster) = t.cluster_of_host(id) else {
        return HostEval { id: id.into(), status: HostStatus::NoCluster, why: vec![Why::NoCluster] };
    };
    if t.dc_of_cluster(&cluster.id).is_none() {
        return HostEval { id: id.into(), status: HostStatus::NoCluster, why: vec![Why::NoDataCenter] };
    }
    if t.node(id).is_some_and(|h| h.flag("maintenance")) {
        return HostEval { id: id.into(), status: HostStatus::Maintenance, why: vec![Why::Maintenance] };
    }
    if management_path(t, id).is_none() {
        return HostEval { id: id.into(), status: HostStatus::NonResponsive, why: vec![Why::NoManagementPath] };
    }
    why.extend(missing_networks(t, id).into_iter().map(|n| Why::MissingNetwork(n.name.clone())));
    why.extend(missing_domains(t, id).into_iter().map(|d| Why::MissingStorage(d.name.clone())));
    why.extend(iscsi_without_network(t, id).into_iter().map(|d| Why::NoStorageNetwork(d.name.clone())));
    let status = if why.is_empty() { HostStatus::Up } else { HostStatus::NonOperational };
    HostEval { id: id.into(), status, why }
}

fn vm_eval(t: &Topology, ev: &Evaluation, id: &str) -> VmEval {
    let mut why = vec![];
    match t.host_of_vm(id) {
        None => why.push(VmWhy::NoHost),
        Some(host) => {
            match ev.host(&host.id).map(|h| h.status) {
                Some(HostStatus::Up) => {}
                Some(HostStatus::Maintenance) => why.push(VmWhy::HostMaintenance(host.name.clone())),
                _ => why.push(VmWhy::HostNotUp(host.name.clone())),
            }
            let dc = t.dc_of_host(&host.id);
            if !dc.is_some_and(|d| ev.dc(&d.id).is_some_and(|e| e.status == DcStatus::Up)) {
                why.push(VmWhy::DcNotUp);
            }
            why.extend(unplugged_networks(t, id).into_iter().map(|n| VmWhy::NetworkMissing(n.name.clone())));
            for d in t.sources(id, Rel::Disk) {
                let same_dc = dc.is_some_and(|dc| t.linked(&dc.id, &d.id));
                let active = ev.domain(&d.id).is_some_and(|e| e.status == DomainStatus::Active);
                if !(same_dc && active) {
                    why.push(VmWhy::DiskInactive(d.name.clone()));
                }
            }
            if host_load(t, &host.id).over() {
                why.push(VmWhy::NoMemory(host.name.clone()));
            }
            for g in t.sources(id, Rel::Affine).filter(|g| g.flag("hard")) {
                if affinity_breaks(t, &g.id).iter().any(|v| v == id) {
                    why.push(VmWhy::AffinityViolated(g.name.clone()));
                }
            }
        }
    }
    let status = if why.is_empty() { VmStatus::Running } else { VmStatus::Down };
    VmEval { id: id.into(), status, why }
}
