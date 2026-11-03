//! Chapter 17: clusters and placement.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// The scenarios of the pack and the reference boards by scenario identifier.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, reference) in [place_vms(), three_clusters(), move_host(), orphan_cluster(), move_cluster()] {
        solution.insert(sc.id.clone(), reference);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// Three VMs without a host; the second cluster has a single host.
fn place_board(placed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "web-2")
        .add("vm3", Kind::Vm, "app-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "cl2"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("vmnet", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("vmnet", "vm1"),
            ("vmnet", "vm2"),
            ("vmnet", "vm3"),
            ("nfs", "vm1"),
            ("nfs", "vm2"),
            ("nfs", "vm3"),
        ]);
    if placed {
        b.link(&[("h1", "vm1"), ("h2", "vm2"), ("h1", "vm3")]);
    }
    b
}

fn place_vms() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("place-vms"),
        title: s("Place the VMs"),
        story: s("Three VMs were created and their disks and NICs are in place, but none of them runs: they are not placed on any host. The hosts, networks and storage are fine."),
        goal: s("Every VM runs and every VM can be live-migrated"),
        hint: s("A VM runs on one host, and live migration needs a second Up host in the same cluster. Count the hosts of each cluster before you choose."),
        palette: vec![Kind::Vm],
        max_nodes: 16,
        start: place_board(false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }],
    };
    (sc, place_board(true).done())
}

/// Three clusters in one data center; vm-net is attached to the first one only, the VMs of the others have a NIC in it.
fn three_board(fixed: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("cl3", Kind::Cluster, "cluster-c")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "web-2")
        .add("vm3", Kind::Vm, "web-3")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("dc1", "cl3"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl3", "h4"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("mgmt", "cl3"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("nfs", "h4"),
            ("h1", "vm1"),
            ("h3", "vm2"),
            ("h4", "vm3"),
            ("vmnet", "vm1"),
            ("vmnet", "vm2"),
            ("vmnet", "vm3"),
            ("nfs", "vm1"),
            ("nfs", "vm2"),
            ("nfs", "vm3"),
        ]);
    if fixed {
        b.link(&[("vmnet", "cl2"), ("vmnet", "cl3"), ("vmnet", "h3"), ("vmnet", "h4")]);
    }
    b
}

fn three_clusters() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("three-clusters"),
        title: s("A network in every cluster"),
        story: s("web-2 and web-3 are Down although their hosts are Up. Select a VM to read why: the VM network was set up for cluster-a only."),
        goal: s("All three VMs run and vm-net is attached to every cluster"),
        hint: s("A network reaches a host only through its cluster: attach it to the cluster first, then assign it to the hosts. A required network has to be on every host of the cluster."),
        palette: vec![Kind::Network],
        max_nodes: 18,
        start: three_board(false).done(),
        // the management network and vm-net are attached to three clusters each
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::Link { rel: Rel::Attached, min: 6 },
        ],
    };
    (sc, three_board(true).done())
}

/// Cluster-b has a single host and a VM; cluster-a has a spare third host. After the move the host takes the networks of its new cluster.
fn move_host_board(moved: bool) -> B {
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
        .net("dbnet", "db-net", Role::Vm)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "db-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("dc1", "vmnet"),
            ("dc1", "dbnet"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("vmnet", "cl1"),
            ("dbnet", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dbnet", "h4"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("nfs", "h4"),
            ("h1", "vm1"),
            ("h4", "vm2"),
            ("vmnet", "vm1"),
            ("dbnet", "vm2"),
            ("nfs", "vm1"),
            ("nfs", "vm2"),
        ]);
    if moved {
        b.link(&[("cl2", "h3"), ("dbnet", "h3")]);
    } else {
        b.link(&[("cl1", "h3"), ("vmnet", "h3")]);
    }
    b
}

fn move_host() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("move-host"),
        title: s("Move a host to another cluster"),
        story: s("db-1 is the only VM of cluster-b and runs on its only host, so it cannot be live-migrated, while cluster-a keeps three hosts for a single VM. db-1 has to stay in cluster-b, where db-net lives."),
        goal: s("Every VM can be live-migrated and all four hosts work"),
        hint: s("A host belongs to one cluster: remove the link and make a new one. Leaving a cluster drops the networks and storage of the host, and the new cluster has required networks of its own."),
        palette: vec![Kind::Network],
        max_nodes: 16,
        start: move_host_board(false).done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::Migrate },
            TopoGoal::Has { node: Kind::Host, min: 4 },
            TopoGoal::Has { node: Kind::Vm, min: 2 },
        ],
    };
    (sc, move_host_board(true).done())
}

/// Cluster-b has two hosts but is not in any data center.
fn orphan_board(fixed: bool) -> B {
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
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
        ]);
    if fixed {
        b.link(&[
            ("dc1", "cl2"),
            ("mgmt", "cl2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("nfs", "h3"),
            ("nfs", "h4"),
        ]);
    }
    b
}

fn orphan_cluster() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("orphan-cluster"),
        title: s("A cluster outside the data center"),
        story: s("host-3 and host-4 were added to cluster-b, but both show the status No cluster. Select a host to read the reason."),
        goal: s("All four hosts are Up and the engine reaches each of them"),
        hint: s("A cluster has to be in a data center before a network can be attached to it. Then the new hosts need the same networks and the same storage as the old ones."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: orphan_board(false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 4 }, TopoGoal::OpOk { op: OpKind::EngineToHost }],
    };
    (sc, orphan_board(true).done())
}

/// Two data centers: Default has three hosts in two clusters, Remote a single host. The cluster-b of Default is the one to move.
fn move_cluster_board(moved: bool) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("cl3", Kind::Cluster, "cluster-c")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl3"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl3", "h4"),
            ("dc1", "mgmt"),
            ("dc2", "mgmt2"),
            ("mgmt", "cl1"),
            ("mgmt2", "cl3"),
            ("engine", "mgmt"),
            ("engine", "mgmt2"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt2", "h4"),
            ("dc1", "nfs"),
            ("dc2", "nfs2"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs2", "h4"),
        ]);
    if moved {
        b.link(&[("dc2", "cl2"), ("cl2", "h3"), ("mgmt2", "cl2"), ("mgmt2", "h3"), ("nfs2", "h3")]);
    } else {
        b.link(&[("dc1", "cl2"), ("cl2", "h3"), ("mgmt", "cl2"), ("mgmt", "h3"), ("nfs", "h3")]);
    }
    b
}

fn move_cluster() -> (Scenario, Topology) {
    let sc = Scenario {
        id: s("move-cluster"),
        title: s("Move a cluster to another data center"),
        story: s("Remote has a single host, so the whole data center would stop if that host failed. Default has more hosts than it needs."),
        goal: s("Both data centers stay Up when any single host fails, and all four hosts work"),
        hint: s("A cluster belongs to one data center. Moving it drops its networks and storage, because those belong to the old data center; the new one has its own."),
        palette: vec![Kind::Network],
        max_nodes: 17,
        start: move_cluster_board(false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::SurviveLoss { node: Kind::Host }, TopoGoal::HostsUp { min: 4 }],
    };
    (sc, move_cluster_board(true).done())
}
