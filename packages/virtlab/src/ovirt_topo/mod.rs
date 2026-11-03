//! oVirt topology board (chapters 17, 20, 21, 22–25): the student assembles an environment — engine, data centers, clusters, hosts,
//! logical networks, storage domains, VMs — and connects the objects. The engine ([`evaluate`]) derives the statuses from the links
//! (a host without the required network is NonOperational, a data center without an active master domain is not Up, …), [`trace`]
//! follows the path of an operation (start a VM, migrate it) hop by hop, and the scenario goals ([`TopoGoal`]) are checked on the result.
//!
//! These are the **rules of the lab**, not a copy of oVirt: for example `required` is a flag of the network (in oVirt it belongs to the
//! attachment to a cluster), the master domain is the first attached one, and the SPM is the first Up host of the data center.
//!
//! The solution of a scenario is the whole [`Topology`]; the server checks it with the same functions ([`Scenario::reached`]).
//!
//! Besides the core objects the board has fence agents, affinity groups, backups, users with permissions and storage domain replicas
//! (chapters 18, 19, 22 and 24); their parameters are one table ([`param_specs`]), the permission roles are in `access.rs`, and what happens
//! when a host, a domain or a data center goes away (HA restart, evacuation, backups, replicas) is in `recovery.rs`.

mod access;
mod eval;
mod goals;
mod layout;
mod packs;
mod params;
mod recovery;
mod rules;
mod trace;

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

pub use access::{ancestors, user_can, Action};
pub use eval::{
    affinity_breaks, evaluate, host_load, iscsi_without_network, management_path, missing_domains, missing_networks,
    unplugged_networks, DcEval, DcStatus, DomainEval, DomainStatus, Evaluation, HostEval, HostLoad, HostStatus, VmEval,
    VmStatus, VmWhy, Why,
};
pub use goals::{GoalResult, OpKind, Scenario, TopoGoal};
pub use layout::{column, next_pos, NODE_H, NODE_W};
pub(crate) use params::raw_specs;
pub use params::{
    param_error, param_specs, param_to_text, BackupType, ParamOption, ParamSpec, ParamTy, PermRole, Polarity,
};
pub use recovery::{
    evacuation_possible, ha_restart_ok, restart_target, restorable_after_domain_loss, survives_site_loss,
};
pub use packs::{default_scenarios, default_solution, pack, pack_chapter, pack_ids, PackDef, PACKS};
pub use rules::{add_error, connect_error, problems, prune, rel, Problem, Rel};
pub use trace::{fence_agent, fence_proxy, migration_network, migration_target, trace, Hop, Op, Trace};

/// The most objects on a board (a bound for the server check).
pub const MAX_NODES: usize = 60;
/// The longest object name.
pub const MAX_NAME: usize = 40;

/// Kind of an object.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Kind {
    /// The management engine.
    Engine,
    /// Data center: a pool of resources and a storage namespace.
    DataCenter,
    /// Cluster of hosts with a common CPU type.
    Cluster,
    /// Hypervisor host.
    Host,
    /// Logical network.
    Network,
    /// Storage domain.
    StorageDomain,
    /// Virtual machine.
    Vm,
    /// Power management of a host (a fence agent): the engine fences a host through it.
    FenceAgent,
    /// Affinity group: a rule that keeps VMs on one host or on different hosts.
    AffinityGroup,
    /// A backup of VMs (a snapshot, an incremental or a full backup).
    Backup,
    /// A user of the Administration Portal.
    User,
    /// A permission: a role on an object (and everything under it), granted to a user.
    Permission,
}

impl Kind {
    /// All kinds in the order of the palette.
    pub const ALL: [Kind; 12] = [
        Kind::Engine,
        Kind::DataCenter,
        Kind::Cluster,
        Kind::Host,
        Kind::Network,
        Kind::StorageDomain,
        Kind::Vm,
        Kind::FenceAgent,
        Kind::AffinityGroup,
        Kind::Backup,
        Kind::User,
        Kind::Permission,
    ];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            Kind::Engine => "engine",
            Kind::DataCenter => "data_center",
            Kind::Cluster => "cluster",
            Kind::Host => "host",
            Kind::Network => "network",
            Kind::StorageDomain => "storage_domain",
            Kind::Vm => "vm",
            Kind::FenceAgent => "fence_agent",
            Kind::AffinityGroup => "affinity_group",
            Kind::Backup => "backup",
            Kind::User => "user",
            Kind::Permission => "permission",
        }
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Kind::Engine => i18n::tr("engine"),
            Kind::DataCenter => i18n::tr("data center"),
            Kind::Cluster => i18n::tr("cluster"),
            Kind::Host => i18n::tr("host"),
            Kind::Network => i18n::tr("network"),
            Kind::StorageDomain => i18n::tr("storage domain"),
            Kind::Vm => i18n::tr("VM"),
            Kind::FenceAgent => i18n::tr("fence agent"),
            Kind::AffinityGroup => i18n::tr("affinity group"),
            Kind::Backup => i18n::tr("backup"),
            Kind::User => i18n::tr("user"),
            Kind::Permission => i18n::tr("permission"),
        }
    }
}

/// Role of a logical network.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Role {
    /// VM traffic.
    Vm,
    /// Management: the engine talks to VDSM over it.
    Management,
    /// Live migration traffic.
    Migration,
    /// Storage traffic.
    Storage,
    /// Console (display) traffic.
    Display,
}

impl Role {
    /// All roles.
    pub const ALL: [Role; 5] = [Role::Vm, Role::Management, Role::Migration, Role::Storage, Role::Display];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            Role::Vm => "vm",
            Role::Management => "management",
            Role::Migration => "migration",
            Role::Storage => "storage",
            Role::Display => "display",
        }
    }

    /// Parse the name from a data file.
    pub fn parse(s: &str) -> Option<Role> {
        Role::ALL.into_iter().find(|r| r.as_str() == s)
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Role::Vm => i18n::tr("VM network"),
            Role::Management => i18n::tr("management"),
            Role::Migration => i18n::tr("migration"),
            Role::Storage => i18n::tr("storage"),
            Role::Display => i18n::tr("display"),
        }
    }
}

/// Kind of a storage domain.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DomainType {
    /// File storage over NFS.
    Nfs,
    /// Block storage over iSCSI: the hosts need a network with the storage role.
    Iscsi,
}

impl DomainType {
    /// All types.
    pub const ALL: [DomainType; 2] = [DomainType::Nfs, DomainType::Iscsi];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            DomainType::Nfs => "nfs",
            DomainType::Iscsi => "iscsi",
        }
    }

    /// Parse the name from a data file.
    pub fn parse(s: &str) -> Option<DomainType> {
        DomainType::ALL.into_iter().find(|t| t.as_str() == s)
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            DomainType::Nfs => "NFS",
            DomainType::Iscsi => "iSCSI",
        }
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
    /// Position of the centre.
    pub x: f64,
    /// Position of the centre.
    pub y: f64,
    /// Parameters (`role` and `required` of a network).
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub params: BTreeMap<String, Param>,
}

impl Node {
    /// A node without parameters.
    pub fn new(id: &str, kind: Kind, name: &str, x: f64, y: f64) -> Node {
        Node { id: id.into(), kind, name: name.into(), x, y, params: BTreeMap::new() }
    }

    /// A network with a role; `required` is true unless set.
    pub fn network(id: &str, name: &str, x: f64, y: f64, role: Role, required: bool) -> Node {
        let mut n = Node::new(id, Kind::Network, name, x, y);
        n.params.insert("role".into(), Param::Str(role.as_str().into()));
        n.params.insert("required".into(), Param::Bool(required));
        n
    }

    /// Role of a network (VM network if unset).
    pub fn role(&self) -> Role {
        match self.params.get("role") {
            Some(Param::Str(s)) => Role::parse(s).unwrap_or(Role::Vm),
            _ => Role::Vm,
        }
    }

    /// Type of a storage domain (NFS if unset).
    pub fn domain_type(&self) -> DomainType {
        match self.params.get("type") {
            Some(Param::Str(s)) => DomainType::parse(s).unwrap_or(DomainType::Nfs),
            _ => DomainType::Nfs,
        }
    }

    /// A storage domain of a type.
    pub fn domain(id: &str, name: &str, x: f64, y: f64, ty: DomainType) -> Node {
        let mut n = Node::new(id, Kind::StorageDomain, name, x, y);
        n.params.insert("type".into(), Param::Str(ty.as_str().into()));
        n
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

    /// Set a parameter (builder style).
    pub fn with_param(mut self, key: &str, value: Param) -> Node {
        self.params.insert(key.into(), value);
        self
    }

    /// Memory in GB: what a host has or a VM needs (a host 32, a VM 4 unless set; 0 for other kinds).
    pub fn mem_gb(&self) -> u32 {
        match self.kind {
            Kind::Host | Kind::Vm => self.param_text("mem").parse().unwrap_or(0),
            _ => 0,
        }
    }

    /// A VM is highly available: it is restarted on another host when its host fails.
    pub fn ha(&self) -> bool {
        self.kind == Kind::Vm && self.flag("ha")
    }

    /// Type of a backup (snapshot if unset).
    pub fn backup_type(&self) -> BackupType {
        BackupType::parse(&self.param_text("type")).unwrap_or(BackupType::Snapshot)
    }

    /// Role of a permission (`UserRole` if unset).
    pub fn perm_role(&self) -> PermRole {
        PermRole::parse(&self.param_text("role")).unwrap_or(PermRole::UserRole)
    }

    /// Polarity of an affinity group (negative if unset).
    pub fn polarity(&self) -> Polarity {
        if self.param_text("polarity") == "positive" {
            Polarity::Positive
        } else {
            Polarity::Negative
        }
    }

    /// The network must be present on every host of the cluster (true if unset).
    pub fn required(&self) -> bool {
        !matches!(self.params.get("required"), Some(Param::Bool(false)))
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

    /// Targets of the links of a relation that start at `from`.
    pub fn targets(&self, from: &str, r: Rel) -> impl Iterator<Item = &Node> + '_ {
        let from_kind = self.node(from).map(|n| n.kind);
        let from = from.to_string();
        self.edges
            .iter()
            .filter(move |e| e.from == from)
            .filter_map(|e| self.node(&e.to))
            .filter(move |n| from_kind.and_then(|k| rel(k, n.kind)) == Some(r))
    }

    /// Sources of the links of a relation that end at `to`.
    pub fn sources(&self, to: &str, r: Rel) -> impl Iterator<Item = &Node> + '_ {
        let to_kind = self.node(to).map(|n| n.kind);
        let to = to.to_string();
        self.edges
            .iter()
            .filter(move |e| e.to == to)
            .filter_map(|e| self.node(&e.from))
            .filter(move |n| to_kind.and_then(|k| rel(n.kind, k)) == Some(r))
    }

    /// Cluster of a host.
    pub fn cluster_of_host(&self, host: &str) -> Option<&Node> {
        self.sources(host, Rel::Member).next()
    }

    /// Data center of a cluster.
    pub fn dc_of_cluster(&self, cluster: &str) -> Option<&Node> {
        self.sources(cluster, Rel::Contains).next()
    }

    /// Data center of a host (through its cluster).
    pub fn dc_of_host(&self, host: &str) -> Option<&Node> {
        let c = self.cluster_of_host(host)?;
        self.dc_of_cluster(&c.id)
    }

    /// The board without an object and the links of it (a failure of that object).
    pub fn without(&self, id: &str) -> Topology {
        Topology {
            nodes: self.nodes.iter().filter(|n| n.id != id).cloned().collect(),
            edges: self.edges.iter().filter(|e| e.from != id && e.to != id).cloned().collect(),
        }
    }

    /// The board without a data center and everything under it (a failure of the whole site): its clusters, their hosts (and the fence
    /// agents of those hosts), the logical networks defined in it and the storage domains attached to it. The VMs stay as objects, but
    /// lose their host, networks and disks.
    pub fn without_dc(&self, dc: &str) -> Topology {
        let mut gone: std::collections::BTreeSet<String> = std::iter::once(dc.to_string()).collect();
        for cl in self.targets(dc, Rel::Contains) {
            gone.insert(cl.id.clone());
            for h in self.targets(&cl.id, Rel::Member) {
                gone.insert(h.id.clone());
                gone.extend(self.sources(&h.id, Rel::Fence).map(|a| a.id.clone()));
            }
        }
        gone.extend(self.targets(dc, Rel::Defined).map(|n| n.id.clone()));
        gone.extend(self.targets(dc, Rel::Domain).map(|d| d.id.clone()));
        Topology {
            nodes: self.nodes.iter().filter(|n| !gone.contains(&n.id)).cloned().collect(),
            edges: self.edges.iter().filter(|e| !gone.contains(&e.from) && !gone.contains(&e.to)).cloned().collect(),
        }
    }

    /// Hosts of a data center, in board order.
    pub fn hosts_of_dc<'a>(&'a self, dc: &'a str) -> impl Iterator<Item = &'a Node> + 'a {
        self.of_kind(Kind::Host).filter(move |h| self.dc_of_host(&h.id).is_some_and(|d| d.id == dc))
    }

    /// Host a VM runs on.
    pub fn host_of_vm(&self, vm: &str) -> Option<&Node> {
        self.sources(vm, Rel::Runs).next()
    }
}
