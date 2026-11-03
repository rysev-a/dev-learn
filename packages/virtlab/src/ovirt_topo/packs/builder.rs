//! Shared building blocks of the scenario packs: a board builder and the common starting boards.

use std::collections::BTreeMap;

use super::super::{column, next_pos, DomainType, Edge, Kind, Node, Role, Topology};
// what the scenarios of the new mechanics need next to the builder (a glob import of this module brings them in)
#[allow(unused_imports)]
pub(crate) use super::super::{Action, BackupType, Param, PermRole, Polarity};

/// Place of the `index`-th object of a kind in an empty column (see [`next_pos`], which also steps around objects that are already there).
#[allow(dead_code)]
pub(crate) fn at(kind: Kind, index: usize) -> (f64, f64) {
    let (x, y0) = column(kind);
    (x, y0 + 80.0 * index as f64)
}

/// Board builder: objects get places by their kind, links are added by identifiers.
#[derive(Clone, Default)]
pub(crate) struct B {
    pub(crate) t: Topology,
    pub(crate) count: BTreeMap<Kind, usize>,
}

#[allow(dead_code)]
impl B {
    /// The place of the next object of a kind. The original kinds take the next row of their column (so the boards of the finished packs
    /// keep their places); the kinds added later take the first free place of their column.
    fn place(&mut self, kind: Kind) -> (f64, f64) {
        let i = self.count.entry(kind).or_default();
        let index = *i;
        *i += 1;
        match kind {
            Kind::Engine | Kind::DataCenter | Kind::Cluster | Kind::Host | Kind::Network | Kind::StorageDomain | Kind::Vm => at(kind, index),
            _ => next_pos(&self.t, kind),
        }
    }

    pub(crate) fn add(&mut self, id: &str, kind: Kind, name: &str) -> &mut Self {
        let (x, y) = self.place(kind);
        self.t.nodes.push(Node::new(id, kind, name, x, y));
        self
    }

    pub(crate) fn network(&mut self, id: &str, name: &str, role: Role, required: bool) -> &mut Self {
        let (x, y) = self.place(Kind::Network);
        self.t.nodes.push(Node::network(id, name, x, y, role, required));
        self
    }

    pub(crate) fn net(&mut self, id: &str, name: &str, role: Role) -> &mut Self {
        self.network(id, name, role, true)
    }

    pub(crate) fn domain(&mut self, id: &str, name: &str, ty: DomainType) -> &mut Self {
        let (x, y) = self.place(Kind::StorageDomain);
        self.t.nodes.push(Node::domain(id, name, x, y, ty));
        self
    }

    /// Sets a parameter only when it differs from the default of the kind (the data files and the drafts stay small, and a start board and a
    /// reference board do not differ by a parameter that merely repeats its default).
    fn set_unless_default(n: Node, key: &str, value: Param) -> Node {
        if n.param_text(key) == super::super::param_to_text(&value) {
            n
        } else {
            n.with_param(key, value)
        }
    }

    /// A VM with its memory (GB) and the HA flag (defaults: 4 GB, not HA).
    pub(crate) fn vm(&mut self, id: &str, name: &str, mem: u32, ha: bool) -> &mut Self {
        let (x, y) = self.place(Kind::Vm);
        let n = Self::set_unless_default(Node::new(id, Kind::Vm, name, x, y), "mem", Param::Str(mem.to_string()));
        let n = Self::set_unless_default(n, "ha", Param::Bool(ha));
        self.t.nodes.push(n);
        self
    }

    /// A host with its memory in GB (default 32).
    pub(crate) fn host(&mut self, id: &str, name: &str, mem: u32) -> &mut Self {
        let (x, y) = self.place(Kind::Host);
        let n = Self::set_unless_default(Node::new(id, Kind::Host, name, x, y), "mem", Param::Str(mem.to_string()));
        self.t.nodes.push(n);
        self
    }

    /// A fence agent (power management) of a host.
    pub(crate) fn fence(&mut self, id: &str, host: &str) -> &mut Self {
        self.add(id, Kind::FenceAgent, id).link(&[(id, host)])
    }

    /// An affinity group over VMs: `negative` keeps them apart, `hard` is enforced.
    pub(crate) fn group(&mut self, id: &str, name: &str, negative: bool, hard: bool, vms: &[&str]) -> &mut Self {
        let (x, y) = self.place(Kind::AffinityGroup);
        let pol = if negative { "negative" } else { "positive" };
        let n = Self::set_unless_default(Node::new(id, Kind::AffinityGroup, name, x, y), "polarity", Param::Str(pol.into()));
        self.t.nodes.push(Self::set_unless_default(n, "hard", Param::Bool(hard)));
        for vm in vms {
            self.t.edges.push(Edge::new(id, vm));
        }
        self
    }

    /// A backup of a type that backs up VMs.
    pub(crate) fn backup(&mut self, id: &str, name: &str, ty: BackupType, vms: &[&str]) -> &mut Self {
        let (x, y) = self.place(Kind::Backup);
        let n = Self::set_unless_default(Node::new(id, Kind::Backup, name, x, y), "type", Param::Str(ty.as_str().into()));
        self.t.nodes.push(n);
        for vm in vms {
            self.t.edges.push(Edge::new(vm, id));
        }
        self
    }

    /// A user with one permission: a role on an object (`<user>` and `<perm>` are identifiers).
    pub(crate) fn grant(&mut self, user: &str, perm: &str, role: PermRole, on: &str) -> &mut Self {
        if self.t.node(user).is_none() {
            self.add(user, Kind::User, user);
        }
        let (x, y) = self.place(Kind::Permission);
        let n = Self::set_unless_default(Node::new(perm, Kind::Permission, perm, x, y), "role", Param::Str(role.as_str().into()));
        self.t.nodes.push(n);
        self.link(&[(user, perm), (perm, on)])
    }

    /// A storage domain replicated to another one.
    pub(crate) fn replica(&mut self, primary: &str, copy: &str) -> &mut Self {
        self.link(&[(primary, copy)])
    }

    /// Change a parameter of an object.
    pub(crate) fn param(&mut self, id: &str, key: &str, value: Param) -> &mut Self {
        self.t.nodes.iter_mut().find(|n| n.id == id).expect("object").params.insert(key.into(), value);
        self
    }

    pub(crate) fn link(&mut self, pairs: &[(&str, &str)]) -> &mut Self {
        for (a, b) in pairs {
            self.t.edges.push(Edge::new(a, b));
        }
        self
    }

    pub(crate) fn done(&self) -> Topology {
        self.t.clone()
    }
}

/// One data center with an engine, a cluster, two hosts and the management network: both hosts are Up, there is no storage yet.
pub(crate) fn base() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
        ]);
    b
}

/// [`base`] with an NFS domain attached to the data center and seen by both hosts: the data center is Up.
pub(crate) fn with_storage() -> B {
    let mut b = base();
    b.add("nfs", Kind::StorageDomain, "nfs-data").link(&[("dc1", "nfs"), ("nfs", "h1"), ("nfs", "h2")]);
    b
}

pub(crate) fn s(text: &str) -> String {
    text.to_string()
}

/// A data center with an engine, a cluster, the management network and an NFS domain, but one host only.
pub(crate) fn one_host() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
        ]);
    b
}

#[cfg(test)]
mod tests {
    use super::super::super::{evaluate, problems, DcStatus, HostStatus, Rel, VmStatus};
    use super::*;

    #[test]
    fn the_helpers_build_valid_boards_and_leave_defaults_unset() {
        let mut b = base();
        b.host("h3", "host-3", 16)
            .link(&[("cl1", "h3"), ("mgmt", "h3")])
            .add("nfs", Kind::StorageDomain, "nfs")
            .link(&[("dc1", "nfs"), ("nfs", "h1"), ("nfs", "h2"), ("nfs", "h3")])
            .vm("vm1", "web", 8, true)
            .vm("vm2", "db", 4, false)
            .link(&[("h1", "vm1"), ("h2", "vm2"), ("nfs", "vm1"), ("nfs", "vm2")])
            .fence("fence-1", "h1")
            .group("g1", "apart", true, false, &["vm1", "vm2"])
            .group("g2", "together", false, true, &["vm1", "vm2"])
            .backup("b1", "nightly", BackupType::Full, &["vm1", "vm2"])
            .backup("b2", "snap", BackupType::Snapshot, &["vm2"])
            .grant("alice", "p1", PermRole::ClusterAdmin, "cl1")
            .grant("alice", "p2", PermRole::UserRole, "vm2");
        let t = b.done();
        assert!(problems(&t).is_empty(), "{:?}", problems(&t).into_iter().map(|p| p.text).collect::<Vec<_>>());
        let params = |id: &str| t.node(id).map(|n| n.params.len());
        assert_eq!(params("h3"), Some(1), "16 GB differs from the default 32");
        assert_eq!(params("vm1"), Some(2), "8 GB and HA differ from the defaults");
        assert_eq!(params("vm2"), Some(0), "4 GB and not HA are the defaults");
        assert_eq!(params("g1"), Some(1), "negative is the default, soft is not");
        assert_eq!(params("g2"), Some(1), "hard is the default, positive is not");
        assert_eq!(params("b1"), Some(1));
        assert_eq!(params("b2"), Some(0), "a snapshot is the default");
        assert_eq!(params("p1"), Some(1));
        assert_eq!(params("p2"), Some(0), "UserRole is the default");
        // one user for both permissions
        assert_eq!(t.of_kind(Kind::User).count(), 1);
        assert_eq!(t.targets("alice", Rel::Grants).count(), 2);
        // the evaluation sees what was built
        let ev = evaluate(&t);
        assert_eq!(ev.host("h3").map(|h| h.status), Some(HostStatus::Up));
        assert_eq!(ev.dc("dc1").map(|d| d.status), Some(DcStatus::Up));
        assert_eq!(ev.vm("vm1").map(|v| v.status), Some(VmStatus::Running));
        // the new objects do not sit on top of anything
        for (i, a) in t.nodes.iter().enumerate() {
            for n in &t.nodes[i + 1..] {
                assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
            }
        }
    }

    #[test]
    fn a_long_column_of_networks_does_not_run_into_the_domains() {
        let mut b = B::default();
        b.add("dc1", Kind::DataCenter, "dc");
        for i in 0..7 {
            b.net(&format!("n{i}"), &format!("net-{i}"), Role::Vm);
        }
        for i in 0..3 {
            b.domain(&format!("d{i}"), &format!("dom-{i}"), DomainType::Nfs);
        }
        let t = b.done();
        for (i, a) in t.nodes.iter().enumerate() {
            for n in &t.nodes[i + 1..] {
                assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
            }
        }
    }
}
