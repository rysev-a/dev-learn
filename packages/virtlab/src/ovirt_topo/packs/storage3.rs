//! Chapter 20, level 3: iSCSI domains and the storage network across hosts, roles, new hosts, VM disks and type changes.

use std::collections::BTreeMap;

use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// Scenarios of "Board: storage, level 3" and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut solution = BTreeMap::new();

    // 1. Two iSCSI domains next to an NFS one: one storage network per host serves them all; the network is not attached to the cluster yet.
    let mut shared = B::default();
    shared
        .add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("stor", "storage", Role::Storage)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("lun1", "lun-db", DomainType::Iscsi)
        .domain("lun2", "lun-logs", DomainType::Iscsi)
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
            ("dc1", "stor"),
            ("dc1", "nfs"),
            ("dc1", "lun1"),
            ("dc1", "lun2"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("lun1", "h1"),
            ("lun1", "h2"),
            ("lun1", "h3"),
            ("lun2", "h1"),
            ("lun2", "h2"),
            ("lun2", "h3"),
        ]);
    let mut shared_ref = shared.clone();
    shared_ref.link(&[("stor", "cl1"), ("stor", "h1"), ("stor", "h2"), ("stor", "h3")]);
    let one_network = Scenario {
        id: s("one-network"),
        title: s("One storage network for every LUN"),
        story: s("Two iSCSI domains were attached next to the NFS one and all three hosts went NonOperational. A storage network is defined in the data center, but the hosts do not use it yet."),
        goal: s("All three hosts are Up and the iSCSI domains keep their type"),
        hint: s("A host needs a network with the storage role, not one network per domain: a single one serves every iSCSI domain. A network can be assigned to a host only after it is attached to the cluster."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: shared.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::Param { node: Kind::StorageDomain, key: s("type"), value: s("iscsi") },
            TopoGoal::Link { rel: Rel::Assigned, min: 6 },
        ],
    };
    solution.insert(s("one-network"), shared_ref.done());

    // 2. The network is assigned, but its role is wrong, and the second host lacks it.
    let mut role = with_storage();
    role.net("stor", "iscsi-net", Role::Vm)
        .domain("lun", "lun-data", DomainType::Iscsi)
        .link(&[("dc1", "stor"), ("stor", "cl1"), ("stor", "h1"), ("dc1", "lun"), ("lun", "h1"), ("lun", "h2")]);
    let mut role_ref = role.clone();
    role_ref.param("stor", "role", Param::Str(s("storage"))).link(&[("stor", "h2")]);
    let wrong_role = Scenario {
        id: s("wrong-role"),
        title: s("The network has the wrong role"),
        story: s("An iSCSI domain was added and its network iscsi-net is attached to the cluster. Host-1 has the network assigned, yet both hosts are NonOperational."),
        goal: s("Both hosts are Up and the iSCSI domain works"),
        hint: s("For an iSCSI domain a host needs a network with the storage role, not just any network: check the properties of the network. Then check which hosts it is assigned to."),
        palette: vec![Kind::Network],
        max_nodes: 10,
        start: role.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::Param { node: Kind::Network, key: s("role"), value: s("storage") },
            TopoGoal::Link { rel: Rel::Assigned, min: 4 },
        ],
    };
    solution.insert(s("wrong-role"), role_ref.done());

    // 3. A fresh host has to get everything the working hosts have.
    let mut out = B::default();
    out.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("vmnet", "vm-net", Role::Vm)
        .net("stor", "storage", Role::Storage)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("lun", "lun-data", DomainType::Iscsi)
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
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "stor"),
            ("stor", "cl1"),
            ("stor", "h1"),
            ("stor", "h2"),
            ("dc1", "nfs"),
            ("dc1", "lun"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("lun", "h1"),
            ("lun", "h2"),
        ]);
    let mut out_ref = out.clone();
    out_ref.link(&[("cl1", "h3"), ("mgmt", "h3"), ("vmnet", "h3"), ("stor", "h3"), ("nfs", "h3"), ("lun", "h3")]);
    let scale_out = Scenario {
        id: s("scale-out"),
        title: s("A new host needs everything"),
        story: s("A third host has just been installed and added to the board, but it belongs to no cluster. The other two hosts work and the data center is Up."),
        goal: s("All three hosts are Up"),
        hint: s("Compare the new host with a working one: it needs the cluster, every network of the cluster and every storage domain. After each step, the status of the host lists what is still missing."),
        palette: vec![Kind::Host],
        max_nodes: 12,
        start: out.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::HostsUp { min: 3 }],
    };
    solution.insert(s("scale-out"), out_ref.done());

    // 4. A VM whose disk is on the iSCSI domain starts only when the whole chain works on its host.
    let mut chain = with_storage();
    chain
        .net("stor", "storage", Role::Storage)
        .domain("lun", "lun-data", DomainType::Iscsi)
        .add("vm1", Kind::Vm, "web-1")
        .add("vm2", Kind::Vm, "db-1")
        .link(&[
            ("dc1", "stor"),
            ("stor", "cl1"),
            ("stor", "h1"),
            ("dc1", "lun"),
            ("lun", "h1"),
            ("h1", "vm1"),
            ("nfs", "vm1"),
            ("h2", "vm2"),
            ("lun", "vm2"),
        ]);
    let mut chain_ref = chain.clone();
    chain_ref.link(&[("lun", "h2"), ("stor", "h2")]);
    let iscsi_disk = Scenario {
        id: s("iscsi-disk"),
        title: s("The VM on a LUN will not start"),
        story: s("The VM db-1 keeps its disk on the iSCSI domain lun-data and refuses to start. Its host is NonOperational, while host-1 and web-1 are fine."),
        goal: s("Both VMs run and every VM can be started"),
        hint: s("Follow the start of the VM hop by hop: the first failing step is not the only one. A host that works with an iSCSI domain needs the domain and also a storage network."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: chain.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::StartVm },
            TopoGoal::VmRunning { min: 2 },
            TopoGoal::Param { node: Kind::StorageDomain, key: s("type"), value: s("iscsi") },
        ],
    };
    solution.insert(s("iscsi-disk"), chain_ref.done());

    // 5. Changing the type of a domain to iSCSI breaks the host that never worked with that array.
    let mut convert = B::default();
    convert
        .add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .add("h3", Kind::Host, "host-3")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .network("stor", "storage", Role::Storage, false)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("arch", "nfs-archive", DomainType::Nfs)
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
            ("dc1", "stor"),
            ("stor", "cl1"),
            ("stor", "h1"),
            ("stor", "h2"),
            ("dc1", "nfs"),
            ("dc1", "arch"),
            ("nfs", "h1"),
            ("nfs", "h2"),
            ("nfs", "h3"),
            ("arch", "h1"),
            ("arch", "h2"),
            ("arch", "h3"),
        ]);
    let mut convert_ref = convert.clone();
    convert_ref.param("arch", "type", Param::Str(s("iscsi"))).link(&[("stor", "h3")]);
    let type_change = Scenario {
        id: s("type-change"),
        title: s("Converting a domain to iSCSI"),
        story: s("The archive array moves from NFS to iSCSI. An optional storage network is already prepared on the two hosts that work with the archive, and the third host only runs VMs from the other domain."),
        goal: s("The archive domain is iSCSI and all three hosts stay Up"),
        hint: s("Change the type of the domain in the inspector, then watch the host statuses: the storage network requirement applies to every host of the data center, also to the ones that never touch that domain."),
        palette: vec![Kind::Network],
        max_nodes: 11,
        start: convert.done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::Param { node: Kind::StorageDomain, key: s("type"), value: s("iscsi") },
            TopoGoal::Link { rel: Rel::Assigned, min: 6 },
        ],
    };
    solution.insert(s("type-change"), convert_ref.done());

    (vec![one_network, wrong_role, scale_out, iscsi_disk, type_change], solution)
}
