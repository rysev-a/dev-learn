//! Chapter 21: networks, third set.

use std::collections::BTreeMap;

use super::super::{DomainType, Kind, OpKind, Param, Rel, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

/// A VM with a disk on the NFS domain and NICs in the given networks.
fn web(b: &mut B, id: &str, name: &str, host: &str, nets: &[&str]) {
    b.add(id, Kind::Vm, name).link(&[(host, id), ("nfs", id)]);
    for n in nets {
        b.link(&[(*n, id)]);
    }
}

/// Host-3 in cluster-a with the management network and storage.
fn third_host(b: &mut B) {
    b.add("h3", Kind::Host, "host-3").link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
}

/// Move an object down, so that it does not overlap a long column of networks.
fn lower(b: &mut B, id: &str, y: f64) {
    b.t.nodes.iter_mut().find(|n| n.id == id).expect("object").y = y;
}

/// A VM with two NICs: the network `back-net` is required, `front-net` is not; both are on host-1 only.
fn nics_start() -> B {
    let mut b = with_storage();
    b.network("front", "front-net", Role::Vm, false)
        .net("back", "back-net", Role::Vm)
        .link(&[
            ("dc1", "front"),
            ("front", "cl1"),
            ("front", "h1"),
            ("dc1", "back"),
            ("back", "cl1"),
            ("back", "h1"),
        ]);
    web(&mut b, "vm1", "web-1", "h1", &["front", "back"]);
    b
}

/// Three hosts with a VM each; the migration network is on host-1 only.
fn fallback_start() -> B {
    let mut b = with_storage();
    third_host(&mut b);
    b.network("migr", "migration-net", Role::Migration, false).link(&[("dc1", "migr"), ("migr", "cl1"), ("migr", "h1")]);
    web(&mut b, "vm1", "web-1", "h1", &[]);
    web(&mut b, "vm2", "web-2", "h2", &[]);
    web(&mut b, "vm3", "web-3", "h3", &[]);
    b
}

/// A network called migration-net that has the VM role by mistake, on both hosts.
fn role_start() -> B {
    let mut b = with_storage();
    b.network("migr", "migration-net", Role::Vm, false).link(&[
        ("dc1", "migr"),
        ("migr", "cl1"),
        ("migr", "h1"),
        ("migr", "h2"),
    ]);
    web(&mut b, "vm1", "web-1", "h1", &[]);
    b
}

/// A running cluster of three hosts and a VM.
fn grow_start() -> B {
    let mut b = with_storage();
    third_host(&mut b);
    web(&mut b, "vm1", "web-1", "h1", &[]);
    b
}

/// An environment with an iSCSI domain and a VM network, and nothing for storage, migration or consoles yet.
fn tour_start() -> B {
    let mut b = with_storage();
    b.net("vmnet", "vm-net", Role::Vm)
        .domain("san", "iscsi-lun", DomainType::Iscsi)
        .link(&[
            ("dc1", "vmnet"),
            ("vmnet", "cl1"),
            ("vmnet", "h1"),
            ("vmnet", "h2"),
            ("dc1", "san"),
            ("san", "h1"),
            ("san", "h2"),
        ]);
    lower(&mut b, "nfs", 480.0);
    lower(&mut b, "san", 560.0);
    web(&mut b, "vm1", "web-1", "h1", &["vmnet"]);
    b
}

/// Scenarios of chapter 21 (networks, third set) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let nics = Scenario {
        id: s("two-nics"),
        title: s("A VM with two NICs migrates"),
        story: s("web-1 has two NICs, one in front-net and one in back-net, and runs on host-1. Host-2 is NonOperational, and the VM cannot be migrated anywhere."),
        goal: s("Everything works and web-1 can be migrated to host-2 with both NICs"),
        hint: s("A VM keeps all its NICs when it moves, so the target host needs the network of every one of them. One of the two networks is not required, so the portal does not complain about it."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: nics_start().done(),
        goals: vec![TopoGoal::Healthy, TopoGoal::OpOk { op: OpKind::Migrate }, TopoGoal::Link { rel: Rel::Vnic, min: 2 }],
    };
    let mut nics_ref = nics_start();
    nics_ref.link(&[("back", "h2"), ("front", "h2")]);

    let fallback = Scenario {
        id: s("silent-fallback"),
        title: s("Migration over the wrong network"),
        story: s("Every host is Up and every VM can be migrated, yet the migration network is hardly used: the memory of web-1, web-2 and web-3 still travels over the management network."),
        goal: s("The memory of every migration goes over the migration network"),
        hint: s("Live migration uses a migration network only if both the source and the target host have it. Follow the path of a migration to see which network it takes."),
        palette: vec![Kind::Network],
        max_nodes: 14,
        start: fallback_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::Migrate },
            TopoGoal::MigrateOverRole { role: Role::Migration },
        ],
    };
    let mut fallback_ref = fallback_start();
    fallback_ref.link(&[("migr", "h2"), ("migr", "h3")]);

    let role = Scenario {
        id: s("wrong-role"),
        title: s("The name is not the role"),
        story: s("The migration-net network is attached to the cluster and assigned to both hosts, but migrations still go over the management network."),
        goal: s("The memory of a migration goes over a network with the migration role"),
        hint: s("The engine chooses the network for a migration by its role, not by its name. Select the network and look at its parameters."),
        palette: vec![Kind::Network],
        max_nodes: 10,
        start: role_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::Migrate },
            TopoGoal::MigrateOverRole { role: Role::Migration },
        ],
    };
    let mut role_ref = role_start();
    role_ref.param("migr", "role", Param::Str(s("migration")));

    let grow = Scenario {
        id: s("grow-required"),
        title: s("A required network for a live cluster"),
        story: s("The application moves to a second network, db-net, and web-1 needs a NIC in it. Three hosts are Up and web-1 is running."),
        goal: s("db-net is on every host, web-1 has a NIC in it, and everything works"),
        hint: s("A new network is required by default: as soon as it is attached to the cluster, every host without it becomes NonOperational. Assign it to all hosts."),
        palette: vec![Kind::Network],
        max_nodes: 12,
        start: grow_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::Migrate },
            TopoGoal::Link { rel: Rel::Vnic, min: 1 },
            TopoGoal::Link { rel: Rel::Assigned, min: 6 },
        ],
    };
    let mut grow_ref = grow_start();
    grow_ref.net("dbnet", "db-net", Role::Vm).link(&[
        ("dc1", "dbnet"),
        ("dbnet", "cl1"),
        ("dbnet", "h1"),
        ("dbnet", "h2"),
        ("dbnet", "h3"),
        ("dbnet", "vm1"),
    ]);

    let tour = Scenario {
        id: s("role-tour"),
        title: s("One network for each role"),
        story: s("A new environment must separate its traffic: iSCSI storage, VM migration and consoles each get a network of their own, next to the management and VM networks. For now the hosts are NonOperational."),
        goal: s("Management, VM, storage, migration and display networks all work on both hosts"),
        hint: s("Every network is defined in the data center, attached to the cluster and assigned to both hosts, and the role is a parameter of the network. The iSCSI domain needs the storage role, and migrations use the migration one."),
        palette: vec![Kind::Network],
        max_nodes: 16,
        start: tour_start().done(),
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::OpOk { op: OpKind::Migrate },
            TopoGoal::MigrateOverRole { role: Role::Migration },
            TopoGoal::Param { node: Kind::Network, key: s("role"), value: s("storage") },
            TopoGoal::Param { node: Kind::Network, key: s("role"), value: s("display") },
            TopoGoal::Link { rel: Rel::Assigned, min: 10 },
        ],
    };
    let mut tour_ref = tour_start();
    tour_ref
        .network("migr", "migration-net", Role::Migration, false)
        .net("stor", "storage-net", Role::Storage)
        .network("disp", "console-net", Role::Display, false);
    for n in ["migr", "stor", "disp"] {
        tour_ref.link(&[("dc1", n), (n, "cl1"), (n, "h1"), (n, "h2")]);
    }

    let mut solution = BTreeMap::new();
    solution.insert(s("two-nics"), nics_ref.done());
    solution.insert(s("silent-fallback"), fallback_ref.done());
    solution.insert(s("wrong-role"), role_ref.done());
    solution.insert(s("grow-required"), grow_ref.done());
    solution.insert(s("role-tour"), tour_ref.done());
    (vec![nics, fallback, role, grow, tour], solution)
}
