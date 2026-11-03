//! Chapter 19: highly available VMs. After a host is fenced, its HA VMs restart on other hosts of the cluster: the host needs a fence agent,
//! the target needs the networks, storage and memory of the VM, and a VM that is not marked HA is not restarted at all.

use std::collections::BTreeMap;

use super::super::{Kind, Param, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// A VM with its disk on `nfs`, placed on a host.
fn vm_on(b: &mut B, id: &str, name: &str, mem: u32, ha: bool, host: &str) {
    b.vm(id, name, mem, ha).link(&[(host, id), ("nfs", id)]);
}

/// A third host in cluster-a with the management network and the storage.
fn third_host(b: &mut B) {
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
}

/// Two HA VMs on two hosts and a non-HA VM on the third; only host-1 has power management.
fn agent_start() -> B {
    let mut b = with_storage();
    third_host(&mut b);
    vm_on(&mut b, "vm1", "web-1", 4, true, "h1");
    vm_on(&mut b, "vm2", "db-1", 4, true, "h2");
    vm_on(&mut b, "vm3", "batch-1", 4, false, "h3");
    b.fence("fence-1", "h1");
    b
}

/// web-1 is HA on host-1. Host-2 is the only other host; it does not see the domain and has no `front-net`.
fn target_start() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .network("front", "front-net", Role::Vm, false)
        .add("nfs", Kind::StorageDomain, "nfs-data")
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
            ("dc1", "front"),
            ("front", "cl1"),
            ("front", "h1"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
        ]);
    b.vm("vm1", "web-1", 4, true).link(&[("h1", "vm1"), ("front", "vm1"), ("nfs", "vm1")]);
    b.vm("vm2", "db-1", 4, false).link(&[("h2", "vm2")]);
    b.fence("fence-1", "h1");
    b
}

/// host-1 runs two 16 GB HA VMs. host-2 has 16 GB and a small VM of its own.
fn memory_start() -> B {
    let mut b = base();
    b.t.nodes.iter_mut().find(|n| n.id == "h2").expect("host").params.insert("mem".into(), Param::Str(s("16")));
    b.add("nfs", Kind::StorageDomain, "nfs-data").link(&[("dc1", "nfs"), ("nfs", "h1"), ("nfs", "h2")]);
    vm_on(&mut b, "vm1", "web-1", 16, true, "h1");
    vm_on(&mut b, "vm2", "web-2", 16, true, "h1");
    vm_on(&mut b, "vm3", "batch-1", 4, false, "h2");
    b.fence("fence-1", "h1");
    b
}

/// Three hosts with power management and four VMs; only web-1 is marked HA.
fn flag_start() -> B {
    let mut b = with_storage();
    third_host(&mut b);
    vm_on(&mut b, "vm1", "web-1", 4, true, "h1");
    vm_on(&mut b, "vm2", "web-2", 4, false, "h1");
    vm_on(&mut b, "vm3", "db-1", 4, false, "h2");
    vm_on(&mut b, "vm4", "batch-1", 4, false, "h3");
    b.fence("fence-1", "h1").fence("fence-2", "h2").fence("fence-3", "h3");
    b
}

/// Two clusters: cluster-a has host-1 with two HA VMs, cluster-b has the spare capacity.
fn border_start() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl2", "h2"),
            ("cl2", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
        ]);
    vm_on(&mut b, "vm1", "web-1", 8, true, "h1");
    vm_on(&mut b, "vm2", "web-2", 8, true, "h1");
    vm_on(&mut b, "vm3", "batch-1", 4, false, "h2");
    b.fence("fence-1", "h1");
    b
}

/// Scenarios of chapter 19 (highly available VMs) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let agent = Scenario {
        id: s("agent-per-host"),
        title: s("HA without power management"),
        story: s("web-1 and db-1 are marked highly available and run on different hosts. Only host-1 has a fence agent, so if host-2 fails, db-1 will not be restarted."),
        goal: s("Both HA VMs would restart after the loss of their host"),
        hint: s("The engine restarts an HA VM only after it knows its host is off, and that needs power management. Check every host that runs an HA VM; a host with no HA VM does not need an agent."),
        palette: vec![Kind::FenceAgent],
        max_nodes: 14,
        start: agent_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HaRestart, TopoGoal::Link { rel: Rel::Fence, min: 2 }],
    };
    let mut agent_ref = agent_start();
    agent_ref.fence("fence-2", "h2");

    let target = Scenario {
        id: s("good-target"),
        title: s("A target that cannot run the VM"),
        story: s("web-1 is highly available and host-1 has power management. host-2 is NonOperational, and even when it comes Up, the VM could not start there."),
        goal: s("Everything works and web-1 would restart on host-2 after the loss of host-1"),
        hint: s("A restart target has to be Up and has to offer everything the VM uses: its networks and its storage. Read the reason on host-2, then check the network of web-1 on it."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: target_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HaRestart, TopoGoal::Link { rel: Rel::Assigned, min: 4 }],
    };
    let mut target_ref = target_start();
    target_ref.link(&[("nfs", "h2"), ("front", "h2")]);

    let memory = Scenario {
        id: s("memory-room"),
        title: s("Room for the restarted VMs"),
        story: s("host-1 runs web-1 and web-2, 16 GB each, both highly available. Everything is Up, but host-2 has 16 GB and a small VM of its own, so it cannot take them."),
        goal: s("Both web VMs would restart after the loss of host-1 and everything keeps running"),
        hint: s("The restarted VMs share the memory of the target. Add up what is already on it and what comes; a host with more memory or another host will do."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: memory_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HaRestart],
    };
    let mut memory_ref = memory_start();
    memory_ref.param("h2", "mem", Param::Str(s("64")));

    let flag = Scenario {
        id: s("not-marked"),
        title: s("Only the marked VMs come back"),
        story: s("Three hosts have power management. When host-1 failed in a test, web-1 came back by itself, but web-2 did not. db-1 on host-2 would be left the same way."),
        goal: s("web-2 and db-1 are highly available too, and all HA VMs would restart"),
        hint: s("A VM that is not marked highly available is only marked down when its host is fenced. Select the VM and look at its parameters."),
        palette: vec![Kind::Host],
        max_nodes: 16,
        start: flag_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HaRestart,
            TopoGoal::ParamOf { id: s("vm2"), key: s("ha"), value: s("true") },
            TopoGoal::ParamOf { id: s("vm3"), key: s("ha"), value: s("true") },
        ],
    };
    let mut flag_ref = flag_start();
    flag_ref.param("vm2", "ha", Param::Bool(true)).param("vm3", "ha", Param::Bool(true));

    let border = Scenario {
        id: s("cluster-border"),
        title: s("The spare host is in another cluster"),
        story: s("host-1 alone is in cluster-a, with two HA VMs. cluster-b has two hosts and room to spare, but the engine has nowhere to restart the VMs."),
        goal: s("Both HA VMs would restart after the loss of host-1 and everything keeps running"),
        hint: s("An HA VM restarts only inside its own cluster. A host belongs to one cluster, so a host that is needed in cluster-a must first leave the other one."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: border_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HaRestart, TopoGoal::HostsUp { min: 3 }],
    };
    let mut border_ref = border_start();
    border_ref.t.edges.retain(|e| !(e.from == "cl2" && e.to == "h2"));
    border_ref.link(&[("cl1", "h2")]);

    let mut solution = BTreeMap::new();
    solution.insert(s("agent-per-host"), agent_ref.done());
    solution.insert(s("good-target"), target_ref.done());
    solution.insert(s("memory-room"), memory_ref.done());
    solution.insert(s("not-marked"), flag_ref.done());
    solution.insert(s("cluster-border"), border_ref.done());
    (vec![agent, target, memory, flag, border], solution)
}
