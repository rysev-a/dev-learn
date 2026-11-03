//! Chapter 17: hierarchy puzzles.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// The scenarios of the pack and the reference boards by scenario identifier.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, reference) in [no_engine(), wrong_dc_net(), foreign_disk(), engine_path(), three_faults()] {
        solution.insert(sc.id.clone(), reference);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// Two configured data centers with no engine on the board.
fn no_engine_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .link(&[
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("dc2", "mgmt2"),
            ("mgmt", "cl1"),
            ("mgmt2", "cl2"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt2", "h3"),
            ("mgmt2", "h4"),
            ("dc1", "nfs"),
            ("dc2", "nfs2"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs2", "h3"),
            ("nfs2", "h4"),
        ]);
    if fixed {
        b.add("engine", Kind::Engine, "engine").link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("engine", "mgmt"),
            ("engine", "mgmt2"),
        ]);
    }
    b
}

fn no_engine() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("no-engine"),
        title: s("Nobody manages this environment"),
        story: s("An existing environment was imported onto the board, but every host is NonResponsive and both data centers are down. Select a host to read the reason."),
        goal: s("Both data centers are Up and the engine reaches every host"),
        hint: s("Hosts are managed through the engine: it has to manage each data center and needs a NIC in the management network of each one."),
        palette: vec![Kind::Engine],
        max_nodes: 14,
        start: no_engine_board(false).done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::EachDcHasUpHosts { min: 1 },
            TopoGoal::OpOk { op: OpKind::EngineToHost },
        ],
    };
    (sc, no_engine_board(true).done())
}

/// web-2 runs in the second data center but its NIC is in a network of the first one.
fn wrong_net_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "web-2")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl2", "h2"),
            ("dc1", "mgmt"),
            ("dc2", "mgmt2"),
            ("mgmt", "cl1"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt"),
            ("engine", "mgmt2"),
            ("mgmt", "h1"),
            ("mgmt2", "h2"),
            ("dc1", "nfs"),
            ("dc2", "nfs2"),
            ("nfs", "h1"),
            ("nfs2", "h2"),
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("h1", "vm1"),
            ("h2", "vm2"),
            ("vmnet", "vm1"),
            ("nfs", "vm1"),
            ("nfs2", "vm2"),
        ]);
    if fixed {
        b.net("vmnet2", "vm-net-2", Role::Vm).link(&[
            ("dc2", "vmnet2"),
            ("vmnet2", "cl2"),
            ("vmnet2", "h2"),
            ("vmnet2", "vm2"),
        ]);
    } else {
        b.link(&[("vmnet", "vm2")]);
    }
    b
}

fn wrong_dc_net() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("wrong-dc-net"),
        title: s("A network in the wrong data center"),
        story: s("web-2 runs in the Remote data center but is Down: its virtual NIC is plugged into vm-net, which is not on host-2, and the board will not let you add it."),
        goal: s("Both VMs run, each with a virtual NIC"),
        hint: s("A logical network belongs to exactly one data center. Define a network in the data center of the host, attach and assign it, and plug the VM into it instead."),
        palette: vec![Kind::Network],
        max_nodes: 16,
        start: wrong_net_board(false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::StartVm }, TopoGoal::Link { rel: Rel::Vnic, min: 2 }],
    };
    (sc, wrong_net_board(true).done())
}

/// web-1 has no host; its NIC is in a network of Default and its disk on a domain of Remote.
fn foreign_disk_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("dc1", "mgmt"),
            ("dc2", "mgmt2"),
            ("dc1", "vmnet"),
            ("mgmt", "cl1"),
            ("mgmt2", "cl2"),
            ("vmnet", "cl1"),
            ("engine", "mgmt"),
            ("engine", "mgmt2"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt2", "h3"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "nfs"),
            ("dc2", "nfs2"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs2", "h3"),
            ("vmnet", "vm1"),
        ]);
    if fixed {
        b.link(&[("h1", "vm1"), ("nfs", "vm1")]);
    } else {
        b.link(&[("nfs2", "vm1")]);
    }
    b
}

fn foreign_disk() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("foreign-disk"),
        title: s("A VM with no host and a foreign disk"),
        story: s("web-1 is not placed on a host. Its NIC is in a network of the Default data center, but its disk is on a storage domain of the Remote data center."),
        goal: s("web-1 runs and can be started, with a disk and a NIC"),
        hint: s("A VM runs on a host of one data center and can use only the networks and domains of that data center. Choose the data center that has the network, then give the VM a disk there."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 16,
        start: foreign_disk_board(false).done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::Link { rel: Rel::Disk, min: 1 },
            TopoGoal::Link { rel: Rel::Vnic, min: 1 },
        ],
    };
    (sc, foreign_disk_board(true).done())
}

/// Three data centers under one engine, no storage yet. Remote: the engine's NIC is in a VM network instead of the management one.
/// Branch: the management network misses one host.
fn engine_path_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("dc3", Kind::DataCenter, "Branch")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("cl3", Kind::Cluster, "cluster-c")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .add("h5", Kind::Host, "host-5")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .net("lab", "lab-net", Role::Vm)
        .net("mgmt3", "ovirtmgmt-3", Role::Management)
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("engine", "dc3"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("dc3", "cl3"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl3", "h4"),
            ("cl3", "h5"),
            ("dc1", "mgmt"),
            ("dc2", "mgmt2"),
            ("dc2", "lab"),
            ("dc3", "mgmt3"),
            ("mgmt", "cl1"),
            ("mgmt2", "cl2"),
            ("lab", "cl2"),
            ("mgmt3", "cl3"),
            ("engine", "mgmt"),
            ("engine", "lab"),
            ("engine", "mgmt3"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt2", "h3"),
            ("lab", "h3"),
            ("mgmt3", "h4"),
        ]);
    if fixed {
        b.link(&[("engine", "mgmt2"), ("mgmt3", "h5")]);
    }
    b
}

fn engine_path() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("engine-path"),
        title: s("Two data centers out of reach"),
        story: s("The engine manages three data centers, but the hosts of two of them are NonResponsive. There is no storage yet; for now only the reach of the engine matters."),
        goal: s("All five hosts are Up and the engine reaches every one of them"),
        hint: s("A command goes from the engine through a NIC and a management network to the host. Run the check and read which hop breaks for each host."),
        palette: vec![Kind::Network],
        max_nodes: 18,
        start: engine_path_board(false).done(),
        goals: vec![TopoGoal::HostsUp { min: 5 }, TopoGoal::OpOk { op: OpKind::EngineToHost }],
    };
    (sc, engine_path_board(true).done())
}

/// One data center, two clusters; three faults in three layers: a network, a storage domain and the placement of a VM.
fn faults_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "db-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("dc1", "vmnet"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("vmnet", "cl1"),
            ("vmnet", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("vmnet", "h1"),
            ("vmnet", "h3"),
            ("vmnet", "h4"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("h1", "vm1"),
            ("vmnet", "vm1"),
            ("vmnet", "vm2"),
            ("nfs", "vm1"),
            ("nfs", "vm2"),
        ]);
    if fixed {
        b.link(&[("vmnet", "h2"), ("nfs", "h4"), ("h3", "vm2")]);
    }
    b
}

fn three_faults() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("three-faults"),
        title: s("Three faults in one environment"),
        story: s("The environment is not healthy: some hosts are NonOperational and a VM does not run. The faults are in different layers. Select the objects to read the reasons."),
        goal: s("Everything works and every VM can be started"),
        hint: s("Each reason points at a different layer: networks, storage, placement. Fix them one at a time and watch the statuses change."),
        palette: vec![Kind::Network],
        max_nodes: 16,
        start: faults_board(false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::StartVm }, TopoGoal::Has { node: Kind::Host, min: 4 }],
    };
    (sc, faults_board(true).done())
}
