//! Chapter 20: storage and the SPM.

use std::collections::BTreeMap;

use super::super::{DomainType, Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// Scenarios of chapter 20 (storage and the SPM) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let master = Scenario {
        id: s("master"),
        title: s("Lose the master domain"),
        story: s("The data center lives on one NFS domain, and it is the master. If that domain fails, the data center goes down. When there is a second domain, the next attached one takes over as the master."),
        goal: s("After losing any single storage domain the data center stays Up and keeps an SPM"),
        hint: s("Add a second domain, attach it to the data center and connect it to every host: a host that does not see an attached domain becomes NonOperational."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 12,
        start: with_storage().done(),
        goals: vec![TopoGoal::HostsUp { min: 2 }, TopoGoal::SurviveLoss { node: Kind::StorageDomain }],
    };
    let spm = Scenario {
        id: s("spm"),
        title: s("The SPM needs a successor"),
        story: s("One host in the data center runs the SPM role and is the only one to change the storage metadata. With a single host, losing it takes the whole data center down. Add a second host."),
        goal: s("After losing any single host the data center stays Up and keeps an SPM"),
        hint: s("A new host needs everything the first one has: membership in the cluster, the management network and the storage domain."),
        palette: vec![Kind::Host],
        max_nodes: 12,
        start: one_host().done(),
        goals: vec![TopoGoal::HostsUp { min: 2 }, TopoGoal::SurviveLoss { node: Kind::Host }],
    };
    let mut disk = with_storage();
    disk.add("nfs2", Kind::StorageDomain, "nfs-vms").add("vm1", Kind::Vm, "web-1").link(&[
        ("dc1", "nfs2"),
        ("nfs2", "h1"),
        ("h2", "vm1"),
        ("nfs2", "vm1"),
    ]);
    let mut disk_fixed = disk.clone();
    disk_fixed.link(&[("nfs2", "h2")]);
    let vm_disk = Scenario {
        id: s("vm-disk"),
        title: s("The VM does not start"),
        story: s("The VM keeps its disk on the second domain. Its host does not see that domain: the host is NonOperational and the VM is down. Select the host to read the reason."),
        goal: s("Everything works and the VM can be started"),
        hint: s("A host has to see every domain attached to its data center, not only the master."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 14,
        start: disk.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::StartVm }],
    };
    let iscsi = Scenario {
        id: s("iscsi"),
        title: s("An iSCSI domain needs a storage network"),
        story: s("Add a block domain over iSCSI. Unlike NFS it needs a path of its own: the hosts have to have a network with the storage role, otherwise they cannot log in to the target and become NonOperational."),
        goal: s("An iSCSI domain is attached and everything keeps working"),
        hint: s("Select the new domain and set its type to iSCSI. Then give the hosts a network with the storage role: define it in the data center, attach it to the cluster and assign it to every host."),
        palette: vec![Kind::StorageDomain, Kind::Network],
        max_nodes: 14,
        start: with_storage().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::Param { node: Kind::StorageDomain, key: s("type"), value: s("iscsi") },
            TopoGoal::Link { rel: Rel::Domain, min: 2 },
            TopoGoal::HostsUp { min: 2 },
        ],
    };

    let mut solution = BTreeMap::new();
    let mut master_ref = with_storage();
    master_ref.add("nfs2", Kind::StorageDomain, "nfs-backup").link(&[("dc1", "nfs2"), ("nfs2", "h1"), ("nfs2", "h2")]);
    solution.insert(s("master"), master_ref.done());
    let mut spm_ref = one_host();
    spm_ref.add("h2", Kind::Host, "host-2").link(&[("cl1", "h2"), ("mgmt", "h2"), ("nfs", "h2")]);
    solution.insert(s("spm"), spm_ref.done());
    solution.insert(s("vm-disk"), disk_fixed.done());
    let mut iscsi_ref = with_storage();
    iscsi_ref.domain("iscsi", "iscsi-lun", DomainType::Iscsi).net("stor", "storage", Role::Storage).link(&[
        ("dc1", "iscsi"),
        ("iscsi", "h1"),
        ("iscsi", "h2"),
        ("dc1", "stor"),
        ("stor", "cl1"),
        ("stor", "h1"),
        ("stor", "h2"),
    ]);
    solution.insert(s("iscsi"), iscsi_ref.done());
    (vec![master, spm, vm_disk, iscsi], solution)
}
