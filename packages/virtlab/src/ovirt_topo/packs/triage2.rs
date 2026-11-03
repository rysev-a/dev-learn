//! Chapter 25: finding the fault, second set. Harder diagnostic boards (two clusters or two data centers, several VMs): a fault hidden behind another,
//! a symptom that points at the wrong layer, a board whose statuses are all green while the operations fail.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// Scenarios of the second troubleshooting set and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [new_host(), blame_disk(), green_board(), other_site(), wrong_type()] {
        solution.insert(sc.id.clone(), fixed);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// A new host without a cluster: after each fix the next reason appears (No cluster, NonResponsive, NonOperational), and another host misses a network.
fn new_host() -> (Scenario, Topology) {
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
        .net("cachenet", "cache-net", Role::Vm)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "web-2")
        .add("vm3", Kind::Vm, "cache-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h4"),
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "cachenet"),
            ("cachenet", "cl2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h4"),
            ("h1", "vm1"),
            ("vmnet", "vm1"),
            ("nfs", "vm1"),
            ("h2", "vm2"),
            ("vmnet", "vm2"),
            ("nfs", "vm2"),
            ("h4", "vm3"),
            ("cachenet", "vm3"),
            ("nfs", "vm3"),
        ]);
    let start = b.done();
    b.link(&[("cl1", "h3"), ("mgmt", "h3"), ("vmnet", "h3"), ("nfs", "h3"), ("cachenet", "h4")]);
    let sc = Scenario {
        id: s("new-host"),
        title: s("The host that was added yesterday"),
        story: s("host-3 was added to the data center yesterday and still shows No cluster. host-4 is NonOperational, and cache-1, which runs on it, is down."),
        goal: s("All four hosts are Up and all three VMs are running"),
        hint: s("Fix what the status says, then read the status again: a host reports its problems one layer at a time. A new member needs everything the other hosts of its cluster have."),
        palette: vec![Kind::Network, Kind::StorageDomain],
        max_nodes: 17,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// The story blames the new disk domain; the VM itself fails on a network missing on its host. Two real faults sit on other hosts.
fn blame_disk() -> (Scenario, Topology) {
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
        .net("backup", "backup-net", Role::Vm)
        .network("dbnet", "db-net", Role::Vm, false)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("fast", "nfs-fast", DomainType::Nfs)
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
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("dc1", "backup"),
            ("backup", "cl2"),
            ("backup", "h3"),
            ("dc1", "dbnet"),
            ("dbnet", "cl2"),
            ("dbnet", "h4"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("nfs", "h4"),
            ("dc1", "fast"),
            ("fast", "h1"),
            ("fast", "h3"),
            ("fast", "h4"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
            ("h3", "vm2"),
            ("dbnet", "vm2"),
            ("fast", "vm2"),
        ]);
    let start = b.done();
    b.link(&[("dbnet", "h3"), ("backup", "h4"), ("fast", "h2")]);
    let sc = Scenario {
        id: s("blame-disk"),
        title: s("A VM that will not start"),
        story: s("db-1 stopped starting right after its disk was moved to the new nfs-fast domain. host-2 and host-4 are NonOperational as well."),
        goal: s("All four hosts are Up and both VMs are running"),
        hint: s("Do not trust the story: the VM tells you itself why it does not run. The message path of the start shows which hop fails."),
        palette: vec![Kind::Network],
        max_nodes: 17,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::VmRunning { min: 2 },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}

/// Every status is green, but live migration fails three times for three different reasons.
fn green_board() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .network("mgmt", "ovirtmgmt", Role::Management, false)
        .network("mgmtb", "mgmt-b", Role::Management, false)
        .network("dbnet", "db-net", Role::Vm, false)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "db-1")
        .add("vm3", Kind::Vm, "cache-1")
        .link(&[
            ("engine", "dc1"),
            ("dc1", "cl1"),
            ("dc1", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl1", "h3"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("dc1", "mgmtb"),
            ("mgmtb", "cl1"),
            ("engine", "mgmtb"),
            ("mgmtb", "h2"),
            ("dc1", "dbnet"),
            ("dbnet", "cl1"),
            ("dbnet", "h2"),
            ("dbnet", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("nfs", "h4"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
            ("h3", "vm2"),
            ("dbnet", "vm2"),
            ("nfs", "vm2"),
            ("h4", "vm3"),
            ("nfs", "vm3"),
        ]);
    let start = b.done();
    b.add("h5", Kind::Host, "host-5").link(&[("mgmt", "h2"), ("dbnet", "h1"), ("cl2", "h5"), ("mgmt", "h5"), ("nfs", "h5")]);
    let sc = Scenario {
        id: s("green-board"),
        title: s("Green board, failing migration"),
        story: s("Every host is Up and every VM is running, but live migration fails for web-1, db-1 and cache-1. Each of them fails for its own reason."),
        goal: s("Every VM can be live-migrated and everything stays Up"),
        hint: s("Run the migration and read where the path breaks. The target is the first other Up host of the cluster: the VM needs a network shared with it, its own networks there, and a target at all."),
        palette: vec![Kind::Host, Kind::Network],
        max_nodes: 18,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::OpOk { op: OpKind::Migrate },
        ],
    };
    (sc, b.done())
}

/// Two data centers: a host of the remote one does not see its domain, and a VM keeps its disk on the domain of the other data center.
fn other_site() -> (Scenario, Topology) {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .add("h4", Kind::Host, "host-4")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("nfs2", "nfs-remote", DomainType::Nfs)
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "app-1")
        .add("vm3", Kind::Vm, "app-2")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl1", "h2"),
            ("cl2", "h3"),
            ("cl2", "h4"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("dc2", "mgmt2"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt2"),
            ("mgmt2", "h3"),
            ("mgmt2", "h4"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("dc2", "nfs2"),
            ("nfs2", "h3"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
            ("h3", "vm2"),
            ("nfs", "vm2"),
            ("h4", "vm3"),
            ("nfs2", "vm3"),
        ]);
    let start = b.done();
    b.link(&[("nfs2", "h4"), ("nfs2", "vm2")]);
    let mut fixed = b.done();
    fixed.edges.retain(|e| !(e.from == "nfs" && e.to == "vm2"));
    let sc = Scenario {
        id: s("other-site"),
        title: s("A remote host and a remote VM"),
        story: s("In the Remote data center host-4 is NonOperational and the VM app-1 will not start, while the Default data center is all green. app-2 runs on host-4 and is down too."),
        goal: s("Both data centers are Up, all hosts are Up and all three VMs are running"),
        hint: s("Networks and storage domains never cross the border of a data center. Follow the start path of app-1 and see which domain it opens."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 18,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::Link { rel: Rel::Disk, min: 3 },
        ],
    };
    (sc, fixed)
}

/// A domain declared as iSCSI although it is NFS, plus two ordinary faults on single hosts.
fn wrong_type() -> (Scenario, Topology) {
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
        .net("backup", "backup-net", Role::Vm)
        .domain("nfs", "nfs-data", DomainType::Iscsi)
        .domain("nfs2", "nfs-vms", DomainType::Nfs)
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
            ("mgmt", "cl1"),
            ("mgmt", "cl2"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("mgmt", "h2"),
            ("mgmt", "h3"),
            ("mgmt", "h4"),
            ("dc1", "backup"),
            ("backup", "cl2"),
            ("backup", "h3"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("nfs", "h4"),
            ("dc1", "nfs2"),
            ("nfs2", "h1"),
            ("nfs2", "h3"),
            ("nfs2", "h4"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
            ("h3", "vm2"),
            ("nfs", "vm2"),
        ]);
    let start = b.done();
    b.param("nfs", "type", Param::Str(s("nfs"))).link(&[("backup", "h4"), ("nfs2", "h2")]);
    let sc = Scenario {
        id: s("wrong-type"),
        title: s("Every host rejects the storage"),
        story: s("All four hosts are NonOperational, the data center is Non Responsive and nfs-data is Inactive. The storage team says the NFS server is healthy."),
        goal: s("All four hosts are Up and both VMs are running"),
        hint: s("Read the reason common to all hosts and ask what the domain is declared to be. Then deal with what is left on host-2 and host-4."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 16,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 4 },
            TopoGoal::VmRunning { min: 2 },
            TopoGoal::OpOk { op: OpKind::StartVm },
        ],
    };
    (sc, b.done())
}
