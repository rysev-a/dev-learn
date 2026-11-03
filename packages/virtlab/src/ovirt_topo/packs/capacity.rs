//! Chapter 22: memory and capacity. The scheduler counts the memory that is promised, not the memory in use: a host whose VMs want more than it has
//! runs none of them, a restarted HA VM needs room like any other, and a cluster survives the loss of a host only if the rest can hold its VMs.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// Scenarios of the pack and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [overloaded(), ha_share(), place_new(), rebalance(), n_plus_one()] {
        solution.insert(sc.id.clone(), fixed);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// Moves a VM to another host: a VM sits on one host, so the old link goes and a new one comes.
fn move_vm(b: &mut B, vm: &str, from: &str, to: &str) {
    b.t.edges.retain(|e| !(e.from == from && e.to == vm));
    b.link(&[(to, vm)]);
}

/// [`with_storage`] with a third host in the cluster that has the management network and sees the domain.
fn three_hosts() -> B {
    let mut b = with_storage();
    b.host("h3", "host-3", 32).link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    b
}

/// A 16 GB host promised 20 GB: every VM on it is Down while the host itself is Up.
fn overloaded() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.param("h1", "mem", Param::Str(s("16")))
        .vm("vm1", "erp", 8, false)
        .vm("vm2", "crm", 8, false)
        .vm("vm3", "mail", 4, false)
        .vm("vm4", "web-1", 4, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h1", "vm3"), ("h2", "vm4")]);
    let start = b.done();
    b.param("h1", "mem", Param::Str(s("32")));
    let sc = Scenario {
        id: s("overloaded"),
        title: s("Promised more than it has"),
        story: s("host-1 is Up and nothing is wrong with its networks or storage, but erp, crm and mail on it are all Down, while web-1 on host-2 runs."),
        goal: s("All four VMs are running and both hosts are Up"),
        hint: s("Add up the memory of the VMs placed on host-1 and compare it with the memory of the host: the scheduler counts what is promised, so the VMs run only if the sum fits. Either the host gets more memory or some VMs go elsewhere."),
        palette: vec![Kind::Vm],
        max_nodes: 12,
        start,
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 2 }, TopoGoal::VmRunning { min: 4 }],
    };
    (sc, b.done())
}

/// Everything runs, but when host-1 fails, its two HA VMs compete for the free memory of the only other host.
fn ha_share() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.param("h2", "mem", Param::Str(s("16")))
        .vm("vm1", "ha-1", 8, true)
        .vm("vm2", "ha-2", 8, true)
        .vm("vm3", "batch", 4, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h2", "vm3")])
        .fence("fence-1", "h1");
    let start = b.done();
    b.param("vm2", "mem", Param::Str(s("4")));
    let sc = Scenario {
        id: s("ha-share"),
        title: s("Two HA VMs, one survivor"),
        story: s("Both HA VMs run and host-1 has a fence agent, yet the portal cannot promise that they restart if host-1 is lost: host-2 is smaller and already runs batch."),
        goal: s("If host-1 fails, both HA VMs restart on host-2, and everything keeps running and stays HA"),
        hint: s("Restarted VMs are placed one after the other, so each takes memory the next one needs. Count what is free on host-2 and make the two VMs fit together."),
        palette: vec![Kind::Vm],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::HaRestart,
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::ParamOf { id: s("vm1"), key: s("ha"), value: s("true") },
            TopoGoal::ParamOf { id: s("vm2"), key: s("ha"), value: s("true") },
        ],
    };
    (sc, b.done())
}

/// Two new VMs without a host, three hosts with different room: a host that has no room breaks the VMs already on it.
fn place_new() -> (Scenario, Topology) {
    let mut b = three_hosts();
    b.param("h1", "mem", Param::Str(s("16")))
        .param("h3", "mem", Param::Str(s("64")))
        .vm("vm1", "crm", 8, false)
        .vm("vm2", "mail", 4, false)
        .vm("vm3", "erp", 16, false)
        .vm("vm4", "db-1", 8, false)
        .vm("vm5", "bi", 16, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h2", "vm3"), ("h2", "vm4"), ("h3", "vm5")]);
    // the two new VMs are the last ones in the column, without a host yet
    b.vm("vm6", "report-1", 16, false).vm("vm7", "batch-1", 8, false);
    let start = b.done();
    b.link(&[("h3", "vm6"), ("h3", "vm7")]);
    let sc = Scenario {
        id: s("place-new"),
        title: s("Where does it fit"),
        story: s("report-1 and batch-1 were just created and have no host. The hosts are different: host-1 has 16 GB, host-2 has 32 GB and host-3 has 64 GB, and each already runs VMs."),
        goal: s("All seven VMs are running, the new ones included, and every host is Up"),
        hint: s("Free memory of a host is its memory minus the memory of the VMs placed on it. A VM that does not fit does not just stay down: it makes every VM on that host Down."),
        palette: vec![Kind::Vm],
        max_nodes: 16,
        start,
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 3 }, TopoGoal::VmRunning { min: 7 }],
    };
    (sc, b.done())
}

/// The cluster has memory in total but two hosts are over: VMs have to be moved to the host that has room.
fn rebalance() -> (Scenario, Topology) {
    let mut b = three_hosts();
    b.param("h1", "mem", Param::Str(s("16")))
        .param("h2", "mem", Param::Str(s("16")))
        .vm("vm1", "erp", 8, false)
        .vm("vm2", "crm", 8, false)
        .vm("vm3", "mail", 4, false)
        .vm("vm4", "db-1", 8, false)
        .vm("vm5", "db-2", 8, false)
        .vm("vm6", "bi", 8, false)
        .vm("vm7", "log-1", 4, false)
        .link(&[
            ("h1", "vm1"),
            ("h1", "vm2"),
            ("h1", "vm3"),
            ("h2", "vm4"),
            ("h2", "vm5"),
            ("h2", "vm6"),
            ("h3", "vm7"),
        ]);
    let start = b.done();
    move_vm(&mut b, "vm3", "h1", "h3");
    move_vm(&mut b, "vm6", "h2", "h3");
    let sc = Scenario {
        id: s("rebalance"),
        title: s("Room in the wrong place"),
        story: s("The cluster has memory to spare, but the VMs were placed badly: host-1 and host-2 are both promised more than they have, so six VMs are Down, while host-3 is almost empty."),
        goal: s("All seven VMs are running and all three hosts are Up"),
        hint: s("Several VMs have to leave their hosts, so find the smallest set that brings each host under its memory. A VM sits on one host: delete the link to the old host, then link it to the new one."),
        palette: vec![Kind::Host],
        max_nodes: 16,
        start,
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 3 }, TopoGoal::VmRunning { min: 7 }],
    };
    (sc, b.done())
}

/// N+1: every host fences, but cache-1 is not HA yet, and once it is, the loss of host-3 leaves no room anywhere for it.
fn n_plus_one() -> (Scenario, Topology) {
    let mut b = three_hosts();
    b.vm("vm1", "db-1", 16, true)
        .vm("vm2", "web-1", 8, true)
        .vm("vm3", "db-2", 16, true)
        .vm("vm4", "web-2", 8, true)
        .vm("vm5", "cache-1", 16, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h2", "vm3"), ("h2", "vm4"), ("h3", "vm5")])
        .fence("fence-1", "h1")
        .link(&[("fence-1", "h2"), ("fence-1", "h3")]);
    let start = b.done();
    b.param("vm5", "ha", Param::Bool(true)).param("h1", "mem", Param::Str(s("64")));
    let sc = Scenario {
        id: s("n-plus-one"),
        title: s("Survive the loss of any host"),
        story: s("db-1, db-2, web-1 and web-2 are HA, and a fence agent serves every host. cache-1 is critical too but is not HA, and the three hosts are full enough that nobody is sure what happens to a 16 GB VM when a host dies."),
        goal: s("cache-1 is HA, and after the loss of any single host every HA VM restarts on the others"),
        hint: s("Make cache-1 HA first, then lose each host in your head: the VMs of the lost host must find room, one after the other, on the hosts that remain. Look for the host whose failure leaves no 16 GB gap."),
        palette: vec![Kind::Host],
        max_nodes: 16,
        start,
        goals: vec![
            TopoGoal::HaRestart,
            TopoGoal::ParamOf { id: s("vm5"), key: s("ha"), value: s("true") },
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::VmRunning { min: 5 },
        ],
    };
    (sc, b.done())
}
