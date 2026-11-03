//! Chapter 22: affinity groups. A hard group is a filter (a member that breaks it cannot run), a soft one is only a preference (it never changes a
//! status): five boards on keeping VMs apart or together, on a group that needs more hosts than the cluster has, on telling a soft rule from a hard
//! one and on two rules that contradict each other.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// Scenarios of the pack and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [apart(), together(), third_host(), soft_rule(), conflict()] {
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

/// A negative hard group over two database replicas that sit on one host: the second one is Down.
fn apart() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.vm("vm1", "db-1", 4, false)
        .vm("vm2", "db-2", 4, false)
        .vm("vm3", "web-1", 4, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h2", "vm3")])
        .group("g1", "db-spread", true, true, &["vm1", "vm2"]);
    let start = b.done();
    move_vm(&mut b, "vm2", "h1", "h2");
    let sc = Scenario {
        id: s("apart"),
        title: s("Two replicas on one host"),
        story: s("db-1 and db-2 are replicas and must never share a host, yet one of them is Down although both hosts are Up and have plenty of memory."),
        goal: s("All three VMs are running and the replicas are still in their group"),
        hint: s("Open the Down VM and read why it does not run: a hard group is a filter, not a wish. A VM sits on one host, so to move it delete its link to the host and link it to another one."),
        palette: vec![Kind::AffinityGroup],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::Link { rel: Rel::Affine, min: 2 },
            TopoGoal::Has { node: Kind::AffinityGroup, min: 1 },
        ],
    };
    (sc, b.done())
}

/// A positive hard group over three VMs that are spread over three hosts: only the first member is where the group wants it.
fn together() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.host("h3", "host-3", 32)
        .link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")])
        .vm("vm1", "app-1", 4, false)
        .vm("vm2", "cache-1", 4, false)
        .vm("vm3", "log-1", 4, false)
        .link(&[("h1", "vm1"), ("h2", "vm2"), ("h3", "vm3")])
        .group("g1", "pod", false, true, &["vm1", "vm2", "vm3"]);
    let start = b.done();
    move_vm(&mut b, "vm2", "h2", "h1");
    move_vm(&mut b, "vm3", "h3", "h1");
    let sc = Scenario {
        id: s("together"),
        title: s("A pod that fell apart"),
        story: s("app-1, cache-1 and log-1 are one unit and talk over the loopback of a single host. Two of them are Down on a healthy cluster."),
        goal: s("The three VMs run together and all three hosts are Up"),
        hint: s("A positive hard group keeps its members on the host of the first member that is placed, and every other member elsewhere breaks it. Move the members that stand apart."),
        palette: vec![Kind::AffinityGroup],
        max_nodes: 13,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::Link { rel: Rel::Affine, min: 3 },
        ],
    };
    (sc, b.done())
}

/// Three replicas must stand on three hosts, but the cluster has two: a third host has to be built with everything its cluster demands.
fn third_host() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.net("vmnet", "vm-net", Role::Vm)
        .link(&[("dc1", "vmnet"), ("vmnet", "cl1"), ("vmnet", "h1"), ("vmnet", "h2")])
        .vm("vm1", "etcd-1", 4, false)
        .vm("vm2", "etcd-2", 4, false)
        .vm("vm3", "etcd-3", 4, false)
        .link(&[("h1", "vm1"), ("h2", "vm2"), ("h2", "vm3"), ("vmnet", "vm1"), ("vmnet", "vm2"), ("vmnet", "vm3")])
        .group("g1", "quorum", true, true, &["vm1", "vm2", "vm3"]);
    let start = b.done();
    b.host("h3", "host-3", 32)
        .link(&[("cl1", "h3"), ("mgmt", "h3"), ("vmnet", "h3"), ("nfs", "h3")]);
    move_vm(&mut b, "vm3", "h2", "h3");
    let sc = Scenario {
        id: s("third-host"),
        title: s("Three replicas, two hosts"),
        story: s("The three etcd members must each live on a host of their own, but the cluster has only two hosts, so one member is always Down."),
        goal: s("All three members run, each on its own host, and every host is Up"),
        hint: s("No move helps while there are fewer hosts than members. A new host must be a member of the cluster and have everything the other hosts have: the management network, the VM network and the storage domain."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::Link { rel: Rel::Affine, min: 3 },
        ],
    };
    (sc, b.done())
}

/// Everything is green although two database VMs share a host: their group is soft. Making it hard shows the violation, which then has to be fixed.
fn soft_rule() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.vm("vm1", "db-1", 4, false)
        .vm("vm2", "db-2", 4, false)
        .vm("vm3", "web-1", 4, false)
        .vm("vm4", "cache-1", 4, false)
        .link(&[("h1", "vm1"), ("h1", "vm2"), ("h2", "vm3"), ("h2", "vm4")])
        .group("g1", "db-spread", true, false, &["vm1", "vm2"])
        .group("g2", "web-cache", false, true, &["vm3", "vm4"]);
    let start = b.done();
    b.param("g1", "hard", Param::Bool(true));
    move_vm(&mut b, "vm2", "h1", "h2");
    let sc = Scenario {
        id: s("soft-rule"),
        title: s("The rule that never fires"),
        story: s("The database replicas db-1 and db-2 are in an anti-affinity group, and the board is all green, yet both of them sit on host-1. The team was told the group guarantees they never share a host."),
        goal: s("The db-spread group is enforced and everything is running with the replicas on different hosts"),
        hint: s("Open the group and read its parameters: a soft group is only a preference and never changes a status. Once it is hard, the VM that breaks it goes Down until it is moved."),
        palette: vec![Kind::AffinityGroup],
        max_nodes: 14,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 4 },
            TopoGoal::ParamOf { id: s("g1"), key: s("hard"), value: s("true") },
            TopoGoal::ParamOf { id: s("g2"), key: s("hard"), value: s("true") },
            TopoGoal::Link { rel: Rel::Affine, min: 4 },
        ],
    };
    (sc, b.done())
}

/// Two hard groups over the same two VMs, one wanting them together and one apart: whatever the placement, one of them is broken.
fn conflict() -> (Scenario, Topology) {
    let mut b = with_storage();
    b.vm("vm1", "app-1", 4, false)
        .vm("vm2", "cache-1", 4, false)
        .vm("vm3", "report-1", 4, false)
        .link(&[("h1", "vm1"), ("h2", "vm2"), ("h1", "vm3")])
        .group("g1", "near", false, true, &["vm1", "vm2"])
        .group("g2", "apart", true, true, &["vm1", "vm2"]);
    let start = b.done();
    b.param("g1", "hard", Param::Bool(false));
    let sc = Scenario {
        id: s("conflict"),
        title: s("Together and apart"),
        story: s("app-1 and cache-1 are in two hard groups: near wants them on one host for latency, apart wants them on two hosts so that one host failure takes only one of them. cache-1 is Down, and moving it only swaps which group is broken."),
        goal: s("Everything runs with app-1 and cache-1 on different hosts, the apart rule enforced and both groups still on the board"),
        hint: s("Two hard groups that contradict each other can never both hold. Decide which one is a requirement and which one is only a wish, and relax the wish."),
        palette: vec![Kind::AffinityGroup],
        max_nodes: 12,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::ParamOf { id: s("g1"), key: s("hard"), value: s("false") },
            TopoGoal::ParamOf { id: s("g2"), key: s("hard"), value: s("true") },
            TopoGoal::Link { rel: Rel::Affine, min: 4 },
        ],
    };
    (sc, b.done())
}
