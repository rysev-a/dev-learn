//! Chapter 17: the first board exercise.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// Scenarios of chapter 17 and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let build = Scenario {
        id: s("build"),
        title: s("Assemble the hierarchy"),
        story: s("An empty board. The engine has to manage a data center with a cluster of two hosts. Hosts are managed over a network: without it the engine cannot reach VDSM."),
        goal: s("Two hosts are Up and the engine reaches both of them"),
        hint: s("engine → data center → cluster → hosts. The network is defined in the data center, attached to the cluster, assigned to every host and given a NIC on the engine; its role is “management”."),
        palette: vec![Kind::Engine, Kind::DataCenter, Kind::Cluster, Kind::Host, Kind::Network],
        max_nodes: 12,
        start: Topology::default(),
        goals: vec![TopoGoal::HostsUp { min: 2 }, TopoGoal::OpOk { op: OpKind::EngineToHost }],
    };
    let storage = Scenario {
        id: s("storage"),
        title: s("Bring the data center Up"),
        story: s("The hosts are Up, but the data center is not: it has no storage. Add an NFS domain. Beware: once a domain is attached to the data center, every host of it has to see the domain."),
        goal: s("The data center is Up, has an SPM, and both hosts stay Up"),
        hint: s("Attach the domain to the data center, then connect it to both hosts. The first attached domain becomes the master."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 12,
        start: base().done(),
        goals: vec![TopoGoal::HostsUp { min: 2 }, TopoGoal::DcUp { min: 1 }, TopoGoal::Spm { min: 1 }],
    };
    let two = Scenario {
        id: s("two"),
        title: s("A second data center"),
        story: s("One engine can manage several data centers, but networks and storage domains never cross their borders. Add a second data center with its own cluster, host, network and domain."),
        goal: s("Two data centers are Up, each with an Up host"),
        hint: s("A network and a storage domain belong to one data center only: the second one needs its own, with the same roles."),
        palette: vec![Kind::DataCenter, Kind::Cluster, Kind::Host, Kind::Network, Kind::StorageDomain],
        max_nodes: 20,
        start: with_storage().done(),
        goals: vec![TopoGoal::DcUp { min: 2 }, TopoGoal::EachDcHasUpHosts { min: 1 }],
    };
    let (repair, repair_fix) = repair();
    let migrate = Scenario {
        id: s("migrate"),
        title: s("A VM stays in its cluster"),
        story: s("A VM runs on the only host of cluster-a. The second host sits in another cluster, so the VM has nowhere to go: live migration is possible only inside a cluster."),
        goal: s("The VM can be live-migrated, and everything keeps working"),
        hint: s("Add a host to the cluster of the VM. It needs the same networks and the same storage as the others."),
        palette: vec![Kind::Host],
        max_nodes: 16,
        start: migrate_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }],
    };

    let mut solution = BTreeMap::new();
    solution.insert(s("build"), base().done());
    solution.insert(s("storage"), with_storage().done());
    let mut second = with_storage();
    second
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .link(&[
            ("engine", "dc2"),
            ("dc2", "cl2"),
            ("cl2", "h3"),
            ("dc2", "mgmt2"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt2"),
            ("mgmt2", "h3"),
            ("dc2", "nfs2"),
            ("nfs2", "h3"),
        ]);
    solution.insert(s("two"), second.done());
    solution.insert(s("repair"), repair_fix);
    let mut fixed = migrate_start();
    fixed.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    solution.insert(s("migrate"), fixed.done());
    (vec![build, storage, two, repair, migrate], solution)
}

/// The VM on the only host of its cluster; the other cluster has the second host.
fn migrate_start() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl2", "h2"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
        ]);
    b
}

/// A broken environment (a host misses the VM network, another has no path to the engine) and the board with the links added.
fn repair() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
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
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("h2", "vm1"),
            ("vmnet", "vm1"),
            ("nfs", "vm1"),
        ]);
    let start = b.done();
    b.link(&[("vmnet", "h2"), ("vmnet", "h3"), ("mgmt", "h3")]);
    let sc = Scenario {
        id: s("repair"),
        title: s("Why are the hosts not Up?"),
        story: s("The environment was built by hand and two hosts do not work: one reports NonOperational, the other NonResponsive. A VM sits on the first of them. Select a host to read the reasons."),
        goal: s("Everything works and the VM can be migrated"),
        hint: s("NonResponsive: the engine has no management network to the host. NonOperational: a required network is not assigned to the host."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start,
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }],
    };
    (sc, b.done())
}
