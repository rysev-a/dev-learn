//! Chapter 19: host failures and fencing. A host can be fenced only if it has a fence agent and another Up host of its data center
//! can act as the proxy.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Param, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// A VM with its disk on `nfs`, placed on a host.
fn vm_on(b: &mut B, id: &str, name: &str, host: &str) {
    b.vm(id, name, 4, false).link(&[(host, id), ("nfs", id)]);
}

/// A data center with one host that has power management and runs a VM.
fn lone_start() -> B {
    let mut b = one_host();
    b.fence("fence-1", "h1");
    vm_on(&mut b, "vm1", "web-1", "h1");
    b
}

/// Three hosts, a VM each, and a fence agent on host-1 only.
fn agents_start() -> B {
    let mut b = with_storage();
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    vm_on(&mut b, "vm1", "web-1", "h1");
    vm_on(&mut b, "vm2", "db-1", "h2");
    vm_on(&mut b, "vm3", "cache-1", "h3");
    b.fence("fence-1", "h1");
    b
}

/// Three hosts with power management each: host-1 is Up, host-2 lacks the VM network, host-3 has no management network at all.
fn proxy_start() -> B {
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
        ]);
    for (id, name, host) in [("vm1", "web-1", "h1"), ("vm2", "web-2", "h3")] {
        b.add(id, Kind::Vm, name).link(&[(host, id), ("vmnet", id), ("nfs", id)]);
    }
    b.fence("fence-1", "h1").fence("fence-2", "h2").fence("fence-3", "h3");
    b
}

/// Two data centers: Default has two hosts, Remote has one. Every host has a fence agent.
fn site_start() -> B {
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
        .add("nfs", Kind::StorageDomain, "nfs-data")
        .add("nfs2", Kind::StorageDomain, "nfs-remote")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc2", "mgmt2"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt2"),
            ("mgmt2", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("dc2", "nfs2"),
            ("nfs2", "h3"),
        ]);
    b.vm("vm1", "app-1", 4, false).link(&[("h3", "vm1"), ("nfs2", "vm1")]);
    b.fence("fence-1", "h1").fence("fence-2", "h2").fence("fence-3", "h3");
    b
}

/// Three hosts with power management; two of them were left in maintenance after the upgrade round.
fn upgrade_start() -> B {
    let mut b = with_storage();
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    vm_on(&mut b, "vm1", "web-1", "h1");
    vm_on(&mut b, "vm2", "db-1", "h1");
    b.fence("fence-1", "h1").fence("fence-2", "h2").fence("fence-3", "h3");
    b.param("h2", "maintenance", Param::Bool(true)).param("h3", "maintenance", Param::Bool(true));
    b
}

/// Scenarios of chapter 19 (host failures and fencing) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let lone = Scenario {
        id: s("lone-host"),
        title: s("Nobody can fence the only host"),
        story: s("The data center has one host and it has power management. When it hangs, the engine cannot switch it off: the command has to be sent by another host."),
        goal: s("Every host can be fenced and the data center survives the loss of any single host"),
        hint: s("The fence command is run by a proxy: another Up host of the same data center. Follow the path of the fence and see which hop fails; then remember that a new host needs its own agent."),
        palette: vec![Kind::Host, Kind::FenceAgent],
        max_nodes: 12,
        start: lone_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 2 },
            TopoGoal::OpOk { op: OpKind::Fence },
            TopoGoal::SurviveLoss { node: Kind::Host },
        ],
    };
    let mut lone_ref = lone_start();
    lone_ref
        .add("h2", Kind::Host, "host-2")
        .link(&[("cl1", "h2"), ("mgmt", "h2"), ("nfs", "h2")])
        .fence("fence-2", "h2");

    let agents = Scenario {
        id: s("no-agents"),
        title: s("Power management on every host"),
        story: s("Only host-1 has power management. If host-2 or host-3 stops answering, the engine cannot switch it off, and its VM stays stuck."),
        goal: s("Every host has a fence agent and can be fenced"),
        hint: s("Fencing needs two things: a fence agent on the host and another Up host as the proxy. Hosts and the proxy are fine here; select a host and check whether the fence path reaches its agent."),
        palette: vec![Kind::FenceAgent],
        max_nodes: 14,
        start: agents_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Fence }, TopoGoal::Link { rel: super::super::Rel::Fence, min: 3 }],
    };
    let mut agents_ref = agents_start();
    agents_ref.fence("fence-2", "h2").fence("fence-3", "h3");

    let proxy = Scenario {
        id: s("dead-proxy"),
        title: s("The proxy must be Up"),
        story: s("Every host has power management, yet host-1 cannot be fenced. host-2 is NonOperational, host-3 is NonResponsive and web-2 on it is down."),
        goal: s("All hosts are Up, both VMs run and every host can be fenced"),
        hint: s("The proxy has to be an Up host, so a host that is itself broken cannot help. Read the reason of each host: fix the one that the engine cannot reach first, then the next reason appears."),
        palette: vec![Kind::Network],
        max_nodes: 15,
        start: proxy_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::VmRunning { min: 2 },
            TopoGoal::OpOk { op: OpKind::Fence },
        ],
    };
    let mut proxy_ref = proxy_start();
    proxy_ref.link(&[("vmnet", "h2"), ("mgmt", "h3"), ("vmnet", "h3")]);

    let site = Scenario {
        id: s("other-site"),
        title: s("The proxy stays in the data center"),
        story: s("The engine manages three hosts with power management, and two of them are in Default. The only host of the Remote data center cannot be fenced all the same."),
        goal: s("Every host can be fenced and both data centers are Up"),
        hint: s("A proxy is always a host of the same data center as the host being fenced. The hosts of another data center do not count, however many there are."),
        palette: vec![Kind::Host, Kind::FenceAgent],
        max_nodes: 20,
        start: site_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::OpOk { op: OpKind::Fence },
        ],
    };
    let mut site_ref = site_start();
    site_ref
        .add("h4", Kind::Host, "host-4")
        .link(&[("cl2", "h4"), ("mgmt2", "h4"), ("nfs2", "h4")])
        .fence("fence-4", "h4");

    let upgrade = Scenario {
        id: s("left-in-maintenance"),
        title: s("The upgrade round that did not end"),
        story: s("After the upgrade round host-2 and host-3 are still in maintenance. The board looks healthy, because they run nothing, but host-1 cannot be fenced."),
        goal: s("All three hosts are Up and every host can be fenced"),
        hint: s("A host in maintenance is not Up, so it cannot serve as a proxy. Select the hosts and look at their parameters."),
        palette: vec![Kind::Host],
        max_nodes: 14,
        start: upgrade_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 3 }, TopoGoal::OpOk { op: OpKind::Fence }],
    };
    let mut upgrade_ref = upgrade_start();
    upgrade_ref.param("h2", "maintenance", Param::Bool(false)).param("h3", "maintenance", Param::Bool(false));

    let mut solution = BTreeMap::new();
    solution.insert(s("lone-host"), lone_ref.done());
    solution.insert(s("no-agents"), agents_ref.done());
    solution.insert(s("dead-proxy"), proxy_ref.done());
    solution.insert(s("other-site"), site_ref.done());
    solution.insert(s("left-in-maintenance"), upgrade_ref.done());
    (vec![lone, agents, proxy, site, upgrade], solution)
}
