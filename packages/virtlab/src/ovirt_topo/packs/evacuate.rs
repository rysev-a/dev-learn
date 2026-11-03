//! Chapter 22: maintenance and evacuation. Putting a host into maintenance moves its VMs to other hosts of the cluster, one after the other,
//! to a host where each would run: Up, with the networks of the VM and the memory for it.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// A VM with a disk on the NFS domain, placed on a host.
fn vm_on(b: &mut B, id: &str, name: &str, mem: u32, host: &str) {
    b.vm(id, name, mem, false).link(&[(host, id), ("nfs", id)]);
}

/// Host-1 is the only host of cluster-a and runs billing-1; host-2 is Up and idle, but in cluster-b.
fn lone_start() -> B {
    let mut b = with_storage();
    b.add("cl2", Kind::Cluster, "cluster-b");
    b.link(&[("dc1", "cl2"), ("mgmt", "cl2")]);
    b.t.edges.retain(|e| !(e.from == "cl1" && e.to == "h2"));
    b.link(&[("cl2", "h2")]);
    vm_on(&mut b, "vm1", "billing-1", 4, "h1");
    b
}

/// Three hosts, a VM on each; host-2 is in maintenance, but db-1 is still placed on it.
fn forgot_start() -> B {
    let mut b = with_storage();
    b.host("h3", "host-3", 32).link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    vm_on(&mut b, "vm1", "web-1", 4, "h1");
    vm_on(&mut b, "vm2", "db-1", 4, "h2");
    vm_on(&mut b, "vm3", "cache-1", 4, "h3");
    b.param("h2", "maintenance", Param::Bool(true));
    b
}

/// Two hosts, each running a VM whose own optional network is on that host only.
fn network_start() -> B {
    let mut b = with_storage();
    b.network("front", "front-net", Role::Vm, false).network("db", "db-net", Role::Vm, false).link(&[
        ("dc1", "front"),
        ("front", "cl1"),
        ("front", "h1"),
        ("dc1", "db"),
        ("db", "cl1"),
        ("db", "h2"),
    ]);
    vm_on(&mut b, "vm1", "web-1", 4, "h1");
    vm_on(&mut b, "vm2", "db-1", 4, "h2");
    b.link(&[("front", "vm1"), ("db", "vm2")]);
    b
}

/// A 32 GB host with 24 GB of VMs and a small 16 GB host with one VM.
fn memory_start() -> B {
    let mut b = with_storage();
    b.param("h2", "mem", Param::Str(s("16")));
    vm_on(&mut b, "vm1", "analytics-1", 16, "h1");
    vm_on(&mut b, "vm2", "web-1", 8, "h1");
    vm_on(&mut b, "vm3", "web-2", 8, "h2");
    b
}

/// A three-host cluster in the middle of patching: host-2 is done and empty, but still in maintenance; hosts 1 and 3 carry the VMs.
fn rotation_start() -> B {
    let mut b = with_storage();
    b.host("h3", "host-3", 32).link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    vm_on(&mut b, "vm1", "web-1", 8, "h1");
    vm_on(&mut b, "vm2", "db-1", 16, "h3");
    vm_on(&mut b, "vm3", "db-2", 16, "h3");
    b.param("h2", "maintenance", Param::Bool(true));
    b
}

/// Scenarios of chapter 22 (maintenance and evacuation) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let lone = Scenario {
        id: s("lone-host"),
        title: s("A spare host in the wrong cluster"),
        story: s("Billing-1 runs on host-1, the only host of cluster-a. Host-2 is Up and idle, but it sits in cluster-b, and the patch window for host-1 is tonight."),
        goal: s("Everything works and billing-1 has another Up host in its own cluster to move to"),
        hint: s("A VM never leaves its cluster, so a host in another cluster is no help. A host belongs to one cluster, and a host that joins a cluster needs the networks and storage of that cluster."),
        palette: vec![Kind::Host],
        max_nodes: 13,
        start: lone_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::EvacuationPossible, TopoGoal::OpOk { op: OpKind::Migrate }],
    };
    let mut lone_ref = lone_start();
    lone_ref.t.edges.retain(|e| !(e.from == "cl2" && e.to == "h2"));
    lone_ref.link(&[("cl1", "h2")]);

    let forgot = Scenario {
        id: s("forgot-to-move"),
        title: s("Maintenance with a VM left behind"),
        story: s("Host-2 was switched to maintenance for a memory upgrade, but db-1 is still placed on it. The portal shows db-1 as down and the environment is not healthy."),
        goal: s("Host-2 stays in maintenance and all three VMs run on other hosts"),
        hint: s("A host in maintenance runs nothing, and switching the flag does not move the VMs by itself on this board. Place the VM on another host of the cluster."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: forgot_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::ParamOf { id: s("h2"), key: s("maintenance"), value: s("true") },
        ],
    };
    let mut forgot_ref = forgot_start();
    forgot_ref.t.edges.retain(|e| !(e.from == "h2" && e.to == "vm2"));
    forgot_ref.link(&[("h3", "vm2")]);

    let network = Scenario {
        id: s("missing-network"),
        title: s("Green board, blocked evacuation"),
        story: s("Both hosts are Up and both VMs run, yet neither host can be put into maintenance: the portal says there is nowhere to move the VMs. Web-1 uses front-net and db-1 uses db-net, and each of those networks is optional."),
        goal: s("Everything works and each host can be evacuated to the other one"),
        hint: s("A VM moves only to a host that has the network of its NIC, and an optional network may be missing without any warning. Check which hosts have which network."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start: network_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::EvacuationPossible, TopoGoal::Link { rel: Rel::Vnic, min: 2 }],
    };
    let mut network_ref = network_start();
    network_ref.link(&[("front", "h2"), ("db", "h1")]);

    let memory = Scenario {
        id: s("not-enough-memory"),
        title: s("Room on the target host"),
        story: s("Host-1 runs analytics-1 and web-1, host-2 runs web-2. Everything is Up, but host-1 cannot be put into maintenance: host-2 is an old machine with 16 GB."),
        goal: s("Everything works, every host can be evacuated and the VMs keep their size"),
        hint: s("A VM moves to a host only if the memory of all VMs already there plus its own fits into the memory of that host. A host that is exactly full is still fine."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: memory_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::EvacuationPossible,
            TopoGoal::Has { node: Kind::Vm, min: 3 },
            TopoGoal::ParamOf { id: s("vm1"), key: s("mem"), value: s("16") },
        ],
    };
    let mut memory_ref = memory_start();
    memory_ref.param("h2", "mem", Param::Str(s("32")));

    let rotation = Scenario {
        id: s("patch-rotation"),
        title: s("Patching one host at a time"),
        story: s("The cluster is patched host by host. Host-2 is finished and empty, but nobody took it out of maintenance, so now host-1 and host-3 have nowhere to go."),
        goal: s("All three hosts are Up and every host that runs VMs can be evacuated"),
        hint: s("A host in maintenance is not a target for evacuation. Finish the previous step before you start the next one."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: rotation_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::EvacuationPossible,
            TopoGoal::Has { node: Kind::Vm, min: 3 },
        ],
    };
    let mut rotation_ref = rotation_start();
    rotation_ref.param("h2", "maintenance", Param::Bool(false));

    let mut solution = BTreeMap::new();
    solution.insert(s("lone-host"), lone_ref.done());
    solution.insert(s("forgot-to-move"), forgot_ref.done());
    solution.insert(s("missing-network"), network_ref.done());
    solution.insert(s("not-enough-memory"), memory_ref.done());
    solution.insert(s("patch-rotation"), rotation_ref.done());
    (vec![lone, forgot, network, memory, rotation], solution)
}
