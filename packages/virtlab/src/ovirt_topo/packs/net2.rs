//! Chapter 21: networks, second set.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// A VM with a disk on the NFS domain and NICs in the given networks.
fn web(b: &mut B, id: &str, name: &str, host: &str, nets: &[&str]) {
    b.add(id, Kind::Vm, name).link(&[(host, id), ("nfs", id)]);
    for n in nets {
        b.link(&[(*n, id)]);
    }
}

/// Move a storage domain down, so that it does not overlap a long column of networks.
fn lower(b: &mut B, id: &str, y: f64) {
    b.t.nodes.iter_mut().find(|n| n.id == id).expect("object").y = y;
}

/// A network that is defined in the data center and has a VM NIC in it, but is attached to no cluster.
fn unattached_start() -> B {
    let mut b = with_storage();
    b.net("app", "app-net", Role::Vm).link(&[("dc1", "app")]);
    web(&mut b, "vm1", "web-1", "h1", &["app"]);
    b
}

/// Host-3 is an old machine with one NIC and only the management network.
fn console_start() -> B {
    let mut b = with_storage();
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    b
}

/// Cluster-b with host-3 and a VM, and nothing attached to it.
fn second_cluster_start() -> B {
    let mut b = with_storage();
    b.net("vmnet", "vm-net", Role::Vm).link(&[("dc1", "vmnet"), ("vmnet", "cl1"), ("vmnet", "h1"), ("vmnet", "h2")]);
    web(&mut b, "vm1", "web-1", "h1", &["vmnet"]);
    b.add("cl2", Kind::Cluster, "cluster-b")
        .add("h3", Kind::Host, "host-3")
        .link(&[("dc1", "cl2"), ("cl2", "h3"), ("nfs", "h3")]);
    web(&mut b, "vm2", "web-2", "h3", &["vmnet"]);
    b
}

/// Host-3 has neither the management network nor the storage; the management network was made optional.
fn mgmt_start() -> B {
    let mut b = with_storage();
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3")]).param("mgmt", "required", Param::Bool(false));
    b
}

/// A cluster with three required networks and an optional one that only two hosts have.
fn scale_start() -> B {
    let mut b = with_storage();
    b.net("vmnet", "vm-net", Role::Vm)
        .net("dbnet", "db-net", Role::Vm)
        .network("console", "console", Role::Display, false)
        .link(&[
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "dbnet"),
            ("dbnet", "cl1"),
            ("dbnet", "h1"),
            ("dbnet", "h2"),
            ("dc1", "console"),
            ("console", "cl1"),
            ("console", "h1"),
            ("console", "h2"),
        ]);
    lower(&mut b, "nfs", 420.0);
    web(&mut b, "vm1", "web-1", "h1", &["vmnet", "dbnet"]);
    b
}

/// Scenarios of chapter 21 (networks, second set) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let unattached = Scenario {
        id: s("unattached"),
        title: s("Defined, but not attached"),
        story: s("The VM web-1 has a NIC in the app-net network, and both hosts are Up, yet the VM does not start. The network exists in the data center, but something between the data center and the hosts is missing."),
        goal: s("web-1 runs and can be migrated to host-2"),
        hint: s("A network defined in a data center does nothing until it is attached to a cluster and assigned to the NIC of every host that needs it. Select the VM to read why it is down."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: unattached_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::StartVm }, TopoGoal::OpOk { op: OpKind::Migrate }],
    };
    let mut unattached_ref = unattached_start();
    unattached_ref.link(&[("app", "cl1"), ("app", "h1"), ("app", "h2")]);

    let console = Scenario {
        id: s("console-net"),
        title: s("A console network for some hosts"),
        story: s("Operators open VM consoles from their laptops and want the console traffic on a network of its own. Host-3 is an old machine with a single NIC and cannot take one more network."),
        goal: s("A display network is on host-1 and host-2, and all three hosts stay Up"),
        hint: s("Give the new network the display role and clear “required”. A required network has to be on every host of the cluster, an optional one does not."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: console_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::Param { node: Kind::Network, key: s("role"), value: s("display") },
            TopoGoal::Param { node: Kind::Network, key: s("required"), value: s("false") },
            TopoGoal::Link { rel: Rel::Assigned, min: 5 },
        ],
    };
    let mut console_ref = console_start();
    console_ref.network("console", "console", Role::Display, false).link(&[
        ("dc1", "console"),
        ("console", "cl1"),
        ("console", "h1"),
        ("console", "h2"),
    ]);

    let second = Scenario {
        id: s("second-cluster"),
        title: s("A second cluster, the same networks"),
        story: s("Cluster-b was added to the data center with host-3 and a VM web-2, but host-3 is NonResponsive. The networks belong to the data center, yet cluster-b has none of them."),
        goal: s("host-3 is Up and web-2 runs on it"),
        hint: s("Defined in the data center means available, not attached. Every cluster gets the networks it needs on its own, and every host of it still puts them on a NIC."),
        palette: vec![Kind::Network],
        max_nodes: 15,
        start: second_cluster_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::Link { rel: Rel::Attached, min: 4 },
        ],
    };
    let mut second_ref = second_cluster_start();
    second_ref.link(&[("mgmt", "cl2"), ("mgmt", "h3"), ("vmnet", "cl2"), ("vmnet", "h3")]);

    let mgmt = Scenario {
        id: s("mgmt-required"),
        title: s("Management cannot be optional"),
        story: s("Host-3 is NonResponsive. Last week someone made ovirtmgmt optional, hoping that a host without it would simply stay Up, but host-3 is still down, and there is more wrong behind this."),
        goal: s("All three hosts are Up and the management network is required again"),
        hint: s("Without a management network the engine has no way to reach the host at all, so it is NonResponsive whatever the flag says. Fix the path first, then read the status again."),
        palette: vec![Kind::Network],
        max_nodes: 11,
        start: mgmt_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::EngineToHost },
            TopoGoal::Param { node: Kind::Network, key: s("required"), value: s("true") },
        ],
    };
    let mut mgmt_ref = mgmt_start();
    mgmt_ref.param("mgmt", "required", Param::Bool(true)).link(&[("mgmt", "h3"), ("nfs", "h3")]);

    let scale = Scenario {
        id: s("scale-out"),
        title: s("Scale out with a new host"),
        story: s("The cluster is short of capacity. A new host-3 has to join cluster-a, and a fresh host has nothing: no networks and no storage."),
        goal: s("Three hosts are Up and host-3 is a member of the cluster"),
        hint: s("Select the host and read why it is not Up: every missing required network and storage domain is listed. An optional network does not have to be there."),
        palette: vec![Kind::Host],
        max_nodes: 15,
        start: scale_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 3 }, TopoGoal::Link { rel: Rel::Member, min: 3 }],
    };
    let mut scale_ref = scale_start();
    scale_ref
        .add("h3", Kind::Host, "host-3")
        .link(&[("cl1", "h3"), ("mgmt", "h3"), ("vmnet", "h3"), ("dbnet", "h3"), ("nfs", "h3")]);

    let mut solution = BTreeMap::new();
    solution.insert(s("unattached"), unattached_ref.done());
    solution.insert(s("console-net"), console_ref.done());
    solution.insert(s("second-cluster"), second_ref.done());
    solution.insert(s("mgmt-required"), mgmt_ref.done());
    solution.insert(s("scale-out"), scale_ref.done());
    (vec![unattached, console, second, mgmt, scale], solution)
}
