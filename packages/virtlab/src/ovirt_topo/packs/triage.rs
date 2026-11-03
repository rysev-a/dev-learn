//! Chapter 25: finding the fault, first set. Diagnostic scenarios on one data center: the story names symptoms only, the student reads the reasons on
//! the objects and the message path, finds the layer and repairs the board.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// Scenarios of the first troubleshooting set and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [silent_host(), no_master(), iscsi_hosts(), lost_cluster(), engine_blind()] {
        solution.insert(sc.id.clone(), fixed);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// A host without the management network on its NIC and a VM whose network is missing on its host.
fn silent_host() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .network("vmnet", "vm-net", Role::Vm, false)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl1", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h3"),
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h2"),
            ("vmnet", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("h1", "vm1"),
            ("vmnet", "vm1"),
            ("nfs", "vm1"),
        ]);
    let start = b.done();
    b.link(&[("mgmt", "h2"), ("vmnet", "h1")]);
    let sc = Scenario {
        id: s("silent-host"),
        title: s("A silent host and a stuck VM"),
        story: s("The engine reports timeouts for host-2, and web-1 will not start although its host, host-1, is Up. Everything else looks fine."),
        goal: s("All three hosts are Up, the engine reaches them and web-1 can be started"),
        hint: s("Select host-2 and web-1 and read the reasons, then run the start. The engine talks to a host over the management network; a VM needs the network of its virtual NIC on the host it runs on."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::OpOk { op: OpKind::EngineToHost },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// No domain is attached (the data center is Uninitialized) and a host lacks a required network.
fn no_master() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("backup", "backup", Role::Vm)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
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
            ("dc1", "backup"),
            ("backup", "cl1"),
            ("backup", "h1"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
        ]);
    let start = b.done();
    b.link(&[("dc1", "nfs"), ("nfs", "h1"), ("nfs", "h2"), ("backup", "h2")]);
    let sc = Scenario {
        id: s("no-master"),
        title: s("The data center never comes Up"),
        story: s("The Default data center is Uninitialized, host-2 is NonOperational and web-1 is down. The nfs-data domain was created last week."),
        goal: s("The data center is Up with an SPM, both hosts are Up and web-1 can be started"),
        hint: s("A data center needs an active master domain, and once a domain is attached every host has to see it. Read the reason on host-2 as well: it is a different problem."),
        palette: vec![Kind::StorageDomain, Kind::Network],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 2 },
            TopoGoal::Spm { min: 1 },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// An iSCSI domain whose storage network has the wrong role, is missing on one host, and a host that does not see the LUN.
fn iscsi_hosts() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("istor", "iscsi-net", Role::Vm)
        .domain("lun", "iscsi-lun", DomainType::Iscsi)
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl1", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("dc1", "istor"),
            ("istor", "cl1"),
            ("istor", "h1"),
            ("istor", "h2"),
            ("dc1", "lun"),
            ("lun", "h1"),
            ("lun", "h3"),
            ("h1", "vm1"),
            ("lun", "vm1"),
        ]);
    let start = b.done();
    b.param("istor", "role", Param::Str(s("storage"))).link(&[("istor", "h3"), ("lun", "h2")]);
    let sc = Scenario {
        id: s("iscsi-hosts"),
        title: s("Hosts fail after adding iSCSI"),
        story: s("After the iSCSI LUN iscsi-lun was added, every host is NonOperational, the data center is Non Responsive and the domain is Inactive. Each host reports a slightly different reason."),
        goal: s("All three hosts are Up and web-1 can be started from the iSCSI domain"),
        hint: s("An iSCSI domain needs a network with the storage role on every host. Compare the reasons of the hosts to see what they share and what differs."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// A cluster that is not in the data center (its host shows No cluster) and a host that misses a required network.
fn lost_cluster() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("backup", "backup", Role::Vm)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc1", "backup"),
            ("backup", "cl1"),
            ("backup", "h1"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("h3", "vm1"),
            ("nfs", "vm1"),
        ]);
    let start = b.done();
    b.link(&[("dc1", "cl2"), ("mgmt", "cl2"), ("mgmt", "h3"), ("nfs", "h3"), ("backup", "h2")]);
    let sc = Scenario {
        id: s("lost-cluster"),
        title: s("Where did cluster-b go?"),
        story: s("host-3 shows No cluster, and web-1, which runs on it, is down. host-2 is NonOperational, while host-1 and the data center are fine."),
        goal: s("All three hosts are Up and web-1 can be started"),
        hint: s("The reason on host-3 names a problem one level above the host. A host that joins a data center needs the same management network and storage as the others."),
        palette: vec![Kind::Network],
        max_nodes: 13,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::OpOk { op: OpKind::EngineToHost },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// The engine has no NIC in the management network, and behind the red hosts the VM has its own two problems.
fn engine_blind() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .network("vmnet", "vm-net", Role::Vm, false)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("nfs2", "nfs-vms", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc1", "vmnet"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("h1", "vm1"),
            ("vmnet", "vm1"),
            ("nfs2", "vm1"),
        ]);
    let start = b.done();
    b.link(&[
        ("engine", "mgmt"),
        ("vmnet", "cl1"),
        ("vmnet", "h1"),
        ("dc1", "nfs2"),
        ("nfs2", "h1"),
        ("nfs2", "h2"),
    ]);
    let sc = Scenario {
        id: s("engine-blind"),
        title: s("Everything is red"),
        story: s("Both hosts are NonResponsive, the data center is Non Responsive, nfs-data is Inactive and web-1 is down. Nobody touched the storage this week."),
        goal: s("Both hosts are Up, the engine reaches them and web-1 can be started"),
        hint: s("An Inactive domain and a Non Responsive data center are consequences: look at the hosts first. Then read every reason of web-1, because a VM needs its networks and its disk domain too."),
        palette: vec![Kind::Network, Kind::StorageDomain],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 2 },
            TopoGoal::OpOk { op: OpKind::EngineToHost },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}
