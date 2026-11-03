//! Chapter 21: networks.

use std::collections::BTreeMap;

use super::super::{Kind, OpKind, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// Scenarios of chapter 21 (networks) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    // a network that only one host has
    let mut three = with_storage();
    three
        .add("h3", Kind::Host, "host-3")
        .link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")])
        .net("backup", "backup", Role::Vm)
        .link(&[("dc1", "backup"), ("backup", "cl1"), ("backup", "h1")]);
    let mut three_fixed = three.clone();
    three_fixed.param("backup", "required", super::super::Param::Bool(false));
    let optional = Scenario {
        id: s("optional"),
        title: s("A network only one host has"),
        story: s("The backup network is attached to the cluster, but only host-1 has a NIC for it. The network is required, so host-2 and host-3 are NonOperational: a required network has to be on every host of the cluster."),
        goal: s("Every host works and the backup network is optional"),
        hint: s("Select the backup network and clear “required”. An optional network may be missing on some hosts."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start: three.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::Param { node: Kind::Network, key: s("required"), value: s("false") }],
    };

    let mut vm = with_storage();
    vm.add("vm1", Kind::Vm, "web-1").link(&[("h1", "vm1"), ("nfs", "vm1")]);
    let mut migration_ref = vm.clone();
    migration_ref.net("migr", "migration", Role::Migration).link(&[
        ("dc1", "migr"),
        ("migr", "cl1"),
        ("migr", "h1"),
        ("migr", "h2"),
    ]);
    let migration = Scenario {
        id: s("migration-net"),
        title: s("A migration network of its own"),
        story: s("Live migration pushes the whole memory of a VM through the network. Without a dedicated network it shares the management network with the commands of the engine. Give migration a network of its own."),
        goal: s("The VM can be migrated and its memory goes over a migration network"),
        hint: s("Define a network with the migration role in the data center, attach it to the cluster and assign it to both hosts. Migration prefers such a network to the management one."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start: vm.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }, TopoGoal::MigrateOverRole { role: Role::Migration }],
    };

    let second = |role: Role, nic: bool| {
        let mut b = with_storage();
        b.add("dc2", Kind::DataCenter, "Remote")
            .add("cl2", Kind::Cluster, "cluster-b")
            .add("h3", Kind::Host, "host-3")
            .net("mgmt2", "ovirtmgmt-2", role)
            .add("nfs2", Kind::StorageDomain, "nfs-remote")
            .link(&[
                ("engine", "dc2"),
                ("dc2", "cl2"),
                ("cl2", "h3"),
                ("dc2", "mgmt2"),
                ("mgmt2", "cl2"),
                ("mgmt2", "h3"),
                ("dc2", "nfs2"),
                ("nfs2", "h3"),
            ]);
        if nic {
            b.link(&[("engine", "mgmt2")]);
        }
        b
    };
    let mgmt = Scenario {
        id: s("mgmt-dc"),
        title: s("A management network for each data center"),
        story: s("A second data center was added. Its host is NonResponsive: the engine has no way in. Each data center needs a network that has the management role and a NIC of the engine."),
        goal: s("Both data centers are Up"),
        hint: s("Two things are wrong with the new network: its role and the engine's NIC in it."),
        palette: vec![Kind::Network],
        max_nodes: 20,
        start: second(Role::Vm, false).done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::EachDcHasUpHosts { min: 1 }],
    };

    let mut optional_vm = with_storage();
    optional_vm.add("vm1", Kind::Vm, "web-1").network("vmnet", "vm-net", Role::Vm, false).link(&[
        ("dc1", "vmnet"),
        ("vmnet", "cl1"),
        ("vmnet", "h1"),
        ("h1", "vm1"),
        ("vmnet", "vm1"),
        ("nfs", "vm1"),
    ]);
    let mut optional_vm_fixed = optional_vm.clone();
    optional_vm_fixed.link(&[("vmnet", "h2")]);
    let vm_optional = Scenario {
        id: s("vm-optional"),
        title: s("An optional network and a VM"),
        story: s("The vm-net network is optional: a host without it stays Up. But a VM with a NIC in vm-net can only run where the network is assigned, so it cannot move to host-2."),
        goal: s("The VM can be migrated and vm-net stays optional"),
        hint: s("The host needs the network of the VM's NIC, even though the network does not have to be there for the host to be Up."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start: optional_vm.done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }, TopoGoal::Param { node: Kind::Network, key: s("required"), value: s("false") }],
    };

    let mut solution = BTreeMap::new();
    solution.insert(s("optional"), three_fixed.done());
    solution.insert(s("migration-net"), migration_ref.done());
    solution.insert(s("mgmt-dc"), second(Role::Management, true).done());
    solution.insert(s("vm-optional"), optional_vm_fixed.done());
    (vec![optional, migration, mgmt, vm_optional], solution)
}
