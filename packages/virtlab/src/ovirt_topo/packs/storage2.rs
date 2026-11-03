//! Chapter 20, level 2: attaching and connecting domains, one domain per data center, reading the real cause, spares of both kinds.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// Scenarios of "Board: storage, level 2" and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut solution = BTreeMap::new();

    // 1. A domain is attached to the data center, but no host is connected to it.
    let mut unseen = B::default();
    unseen
        .add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
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
            ("mgmt", "h3"),
            ("dc1", "nfs"),
        ]);
    let mut unseen_ref = unseen.clone();
    unseen_ref.link(&[("nfs", "h1"), ("nfs", "h2"), ("nfs", "h3")]);
    let no_connection = Scenario {
        id: s("no-connection"),
        title: s("Attached, but nobody sees it"),
        story: s("The NFS domain is attached to the data center, yet the domain shows Inactive, the data center is NonResponsive and all three hosts are NonOperational. Select a host and read its status."),
        goal: s("All three hosts are Up and the data center has an SPM"),
        hint: s("Attaching a domain to the data center is only half of the job: every host of that data center has to be connected to the domain as well."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 10,
        start: unseen.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::Spm { min: 1 },
            TopoGoal::Link { rel: Rel::Sees, min: 3 },
        ],
    };
    solution.insert(s("no-connection"), unseen_ref.done());

    // 2. A domain with the disk of a VM exists, but it is not attached to the data center.
    let mut archive = with_storage();
    archive
        .add("arch", Kind::StorageDomain, "nfs-archive")
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "db-1")
        .link(&[("h1", "vm1"), ("nfs", "vm1"), ("h2", "vm2"), ("arch", "vm2")]);
    let mut archive_ref = archive.clone();
    archive_ref.link(&[("dc1", "arch"), ("arch", "h1"), ("arch", "h2")]);
    let unattached = Scenario {
        id: s("unattached"),
        title: s("A domain nobody attached"),
        story: s("The VM db-1 keeps its disk on the domain nfs-archive. The domain exists, but it is Unattached, so db-1 stays down while web-1 on the other domain runs fine."),
        goal: s("Both VMs run and can be started, and both domains serve the data center"),
        hint: s("A domain serves a data center only after it is attached to it, and then every host of that data center has to be connected to it, otherwise that host turns NonOperational."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 12,
        start: archive.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::VmRunning { min: 2 },
            TopoGoal::Link { rel: Rel::Domain, min: 2 },
        ],
    };
    solution.insert(s("unattached"), archive_ref.done());

    // 3. A second data center cannot use the domain of the first one.
    let mut two = B::default();
    two.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Paris")
        .add("dc2", Kind::DataCenter, "Berlin")
        .add("cl1", Kind::Cluster, "cluster-paris")
        .add("cl2", Kind::Cluster, "cluster-berlin")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt1", "mgmt-paris", Role::Management)
        .net("mgmt2", "mgmt-berlin", Role::Management)
        .add("nfs", Kind::StorageDomain, "nfs-paris")
        .add("vm1", Kind::Vm, "web-1")
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl2", "h2"),
            ("dc1", "mgmt1"),
            ("dc2", "mgmt2"),
            ("mgmt1", "cl1"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt1"),
            ("engine", "mgmt2"),
            ("mgmt1", "h1"),
            ("mgmt2", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("h2", "vm1"),
            ("nfs", "vm1"),
        ]);
    let mut two_ref = two.clone();
    two_ref.add("nfs2", Kind::StorageDomain, "nfs-berlin").link(&[("dc2", "nfs2"), ("nfs2", "h2"), ("nfs2", "vm1")]);
    two_ref.t.edges.retain(|e| !(e.from == "nfs" && e.to == "vm1"));
    let own_domain = Scenario {
        id: s("own-domain"),
        title: s("A domain belongs to one data center"),
        story: s("The Berlin data center has a host but no storage of its own and shows Uninitialized. The VM web-1 runs in Berlin, but its disk is on the domain of the Paris data center, so it cannot start."),
        goal: s("Both data centers are Up and web-1 runs from a domain of its own data center"),
        hint: s("A storage domain is attached to one data center only and cannot be shared. Look at which data center the domain of the disk belongs to."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 14,
        start: two.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::Has { node: Kind::StorageDomain, min: 2 },
            TopoGoal::Link { rel: Rel::Disk, min: 1 },
        ],
    };
    solution.insert(s("own-domain"), two_ref.done());

    // 4. The domain is Inactive although it is attached and connected: the hosts fail for reasons that are not storage.
    let mut cause = B::default();
    cause
        .add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
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
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("nfs", "h2"),
        ]);
    let mut cause_ref = cause.clone();
    cause_ref.link(&[("vmnet", "h1"), ("mgmt", "h2")]);
    let inactive = Scenario {
        id: s("inactive-cause"),
        title: s("Connected, yet Inactive"),
        story: s("The domain is attached and connected to both hosts, yet it shows Inactive and the data center is NonResponsive. The storage itself looks fine, and the two hosts have different statuses."),
        goal: s("Both hosts are Up with every network of the cluster, and the data center has an SPM"),
        hint: s("A domain is Active only while an Up host sees it, and every host is judged on its own. Read the reason of each host separately."),
        palette: vec![Kind::Network],
        max_nodes: 9,
        start: cause.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::Spm { min: 1 }, TopoGoal::Link { rel: Rel::Assigned, min: 4 }],
    };
    solution.insert(s("inactive-cause"), cause_ref.done());

    // 5. One host and one domain: both are single points of failure.
    let mut single = one_host();
    single.add("vm1", Kind::Vm, "web-1").link(&[("h1", "vm1"), ("nfs", "vm1")]);
    let mut single_ref = single.clone();
    single_ref
        .add("h2", Kind::Host, "host-2")
        .link(&[("cl1", "h2"), ("mgmt", "h2"), ("nfs", "h2")])
        .add("nfs2", Kind::StorageDomain, "nfs-spare")
        .link(&[("dc1", "nfs2"), ("nfs2", "h1"), ("nfs2", "h2")]);
    let spares = Scenario {
        id: s("spares"),
        title: s("Spare hosts and spare domains"),
        story: s("The data center runs web-1 on one host and one domain. Either of them is a single point of failure: lose it, and the data center and the VM go down."),
        goal: s("web-1 runs, and after losing any single host or any single domain the data center stays Up with an SPM"),
        hint: s("A new host needs the cluster, the management network and every domain. A new domain must be attached and connected to every host. Count what is left after each loss."),
        palette: vec![Kind::Host, Kind::StorageDomain],
        max_nodes: 12,
        start: single.done(),
        goals: vec![
            TopoGoal::HostsUp { min: 2 },
            TopoGoal::VmRunning { min: 1 },
            TopoGoal::SurviveLoss { node: Kind::Host },
            TopoGoal::SurviveLoss { node: Kind::StorageDomain },
        ],
    };
    solution.insert(s("spares"), single_ref.done());

    (vec![no_connection, unattached, own_domain, inactive, spares], solution)
}
