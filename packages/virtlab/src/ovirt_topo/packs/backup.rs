//! Chapter 24: backups. A snapshot lives on the domain of the disk and is lost with it; only an incremental or a full backup survives the
//! loss of the disk domain. Five boards: a snapshot job to retype, the type per kind of disk, the VMs of a second domain, one forgotten VM and a
//! new VM that has neither a disk nor a backup.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// The scenarios of the pack and the reference boards by scenario identifier.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [snapshot_only(), right_type(), two_domains(), forgotten_vm(), new_vm()] {
        solution.insert(sc.id.clone(), fixed);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// One data center with `hosts` hosts (`h1`, `h2`, …) that all see every given NFS domain (identifier, name); everything is Up.
fn lab(hosts: usize, domains: &[(&str, &str)]) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("cl1", Kind::Cluster, "cluster-a")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .link(&[("engine", "dc1"), ("dc1", "cl1"), ("dc1", "mgmt"), ("mgmt", "cl1"), ("engine", "mgmt")]);
    for i in 1..=hosts {
        let h = format!("h{i}");
        b.host(&h, &format!("host-{i}"), 32).link(&[("cl1", &h), ("mgmt", &h)]);
    }
    for (id, name) in domains {
        b.domain(id, name, DomainType::Nfs).link(&[("dc1", id)]);
        for i in 1..=hosts {
            b.link(&[(id, &format!("h{i}"))]);
        }
    }
    b
}

/// A VM on a host with its disk on a domain.
fn put_vm(b: &mut B, id: &str, name: &str, host: &str, domain: &str) {
    b.vm(id, name, 4, false).link(&[(host, id), (domain, id)]);
}

/// Every VM is backed up, but only by snapshots: they die with the domain.
fn snapshot_only() -> (Scenario, Topology) {
    let mut b = lab(2, &[("nfs", "nfs-data")]);
    put_vm(&mut b, "vm1", "web-1", "h1", "nfs");
    put_vm(&mut b, "vm2", "web-2", "h2", "nfs");
    put_vm(&mut b, "vm3", "db-1", "h2", "nfs");
    b.backup("bk1", "nightly", BackupType::Snapshot, &["vm1", "vm2", "vm3"]);
    let start = b.done();
    b.param("bk1", "type", Param::Str(s("incremental")));
    let sc = Scenario {
        id: s("snapshot-only"),
        title: s("Snapshots are not backups"),
        story: s("Every night all three VMs get a snapshot, and the audit still fails the setup: when nfs-data is lost, the snapshots are lost with it."),
        goal: s("Every VM has a copy that survives the loss of its disk domain"),
        hint: s("A snapshot lives on the same storage domain as the disk it was taken from. Look at the type of the backup."),
        palette: vec![Kind::Backup],
        max_nodes: 13,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 3 },
            TopoGoal::Link { rel: Rel::BackupOf, min: 3 },
            TopoGoal::AllVmsBackedUp,
            TopoGoal::RestorableAfterDomainLoss,
        ],
    };
    (sc, b.done())
}

/// Three jobs: one is right, two still make snapshots; the raw disk of the database allows a full copy only.
fn right_type() -> (Scenario, Topology) {
    let mut b = lab(2, &[("nfs", "nfs-data")]);
    put_vm(&mut b, "vm1", "app-1", "h1", "nfs");
    put_vm(&mut b, "vm2", "app-2", "h1", "nfs");
    put_vm(&mut b, "vm3", "db-1", "h2", "nfs");
    put_vm(&mut b, "vm4", "mail-1", "h2", "nfs");
    b.backup("bk1", "app-backup", BackupType::Snapshot, &["vm1", "vm2"])
        .backup("bk2", "db-backup", BackupType::Snapshot, &["vm3"])
        .backup("bk3", "mail-backup", BackupType::Incremental, &["vm4"]);
    let start = b.done();
    b.param("bk1", "type", Param::Str(s("incremental"))).param("bk2", "type", Param::Str(s("full")));
    let sc = Scenario {
        id: s("right-type"),
        title: s("Full or incremental"),
        story: s("db-1 keeps its data on a raw disk, while app-1, app-2 and mail-1 use qcow2 disks. Two of the three backup jobs still make snapshots, which do not survive the loss of nfs-data."),
        goal: s("Every VM is backed up off its domain: the raw disk with full copies, the qcow2 disks incrementally"),
        hint: s("Incremental backup tracks changed blocks in a qcow2 disk, so a raw disk can only be copied whole. Set the type of each job to match its disks."),
        palette: vec![Kind::Backup],
        max_nodes: 15,
        start,
        goals: vec![
            TopoGoal::AllVmsBackedUp,
            TopoGoal::RestorableAfterDomainLoss,
            TopoGoal::ParamOf { id: s("bk1"), key: s("type"), value: s("incremental") },
            TopoGoal::ParamOf { id: s("bk2"), key: s("type"), value: s("full") },
        ],
    };
    (sc, b.done())
}

/// Two domains: the web VMs are covered, the databases on the other domain have no job; a new job starts as a snapshot.
fn two_domains() -> (Scenario, Topology) {
    let mut b = lab(2, &[("nfs-a", "nfs-a"), ("nfs-b", "nfs-b")]);
    put_vm(&mut b, "vm1", "web-1", "h1", "nfs-a");
    put_vm(&mut b, "vm2", "web-2", "h1", "nfs-a");
    put_vm(&mut b, "vm3", "db-1", "h2", "nfs-b");
    put_vm(&mut b, "vm4", "db-2", "h2", "nfs-b");
    b.backup("bk1", "web-nightly", BackupType::Incremental, &["vm1", "vm2"]);
    let start = b.done();
    b.backup("bk2", "db-nightly", BackupType::Incremental, &["vm3", "vm4"]);
    let sc = Scenario {
        id: s("two-domains"),
        title: s("Two domains, two backup jobs"),
        story: s("web-nightly protects web-1 and web-2 on nfs-a. db-1 and db-2 live on nfs-b and have no backup at all, and every group of VMs is supposed to have a job of its own."),
        goal: s("Every VM is backed up off its domain, with a separate job for the databases"),
        hint: s("A new backup job starts as a snapshot. Check that the VMs of each domain are covered by a job that survives losing that domain."),
        palette: vec![Kind::Backup],
        max_nodes: 15,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::Has { node: Kind::Backup, min: 2 },
            TopoGoal::Link { rel: Rel::BackupOf, min: 4 },
            TopoGoal::AllVmsBackedUp,
            TopoGoal::RestorableAfterDomainLoss,
        ],
    };
    (sc, b.done())
}

/// Eight VMs, two good jobs, one VM that is in none of them.
fn forgotten_vm() -> (Scenario, Topology) {
    let mut b = lab(3, &[("nfs", "nfs-data")]);
    let vms = [
        ("vm1", "web-1", "h1"),
        ("vm2", "web-2", "h1"),
        ("vm3", "web-3", "h2"),
        ("vm4", "app-1", "h2"),
        ("vm5", "db-1", "h3"),
        ("vm6", "db-2", "h3"),
        ("vm7", "mail-1", "h3"),
        ("vm8", "report-1", "h2"),
    ];
    for (id, name, host) in vms {
        put_vm(&mut b, id, name, host, "nfs");
    }
    b.backup("bk1", "tier-1", BackupType::Incremental, &["vm1", "vm2", "vm3", "vm4"])
        .backup("bk2", "tier-2", BackupType::Full, &["vm5", "vm6", "vm7"]);
    let start = b.done();
    b.link(&[("vm8", "bk1")]);
    let sc = Scenario {
        id: s("forgotten-vm"),
        title: s("The VM nobody backed up"),
        story: s("The audit counted eight VMs and only seven are covered by a backup job. Nobody remembers which one was left out."),
        goal: s("All eight VMs are backed up off their domain"),
        hint: s("Follow the backup links of every VM. A VM that was added later than the others is the usual suspect."),
        palette: vec![Kind::Backup],
        max_nodes: 20,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::VmRunning { min: 8 },
            TopoGoal::Link { rel: Rel::BackupOf, min: 8 },
            TopoGoal::AllVmsBackedUp,
            TopoGoal::RestorableAfterDomainLoss,
        ],
    };
    (sc, b.done())
}

/// A VM that was created and never finished: no disk, no backup. A backup of a diskless VM would protect nothing.
fn new_vm() -> (Scenario, Topology) {
    let mut b = lab(2, &[("nfs", "nfs-data")]);
    put_vm(&mut b, "vm1", "web-1", "h1", "nfs");
    put_vm(&mut b, "vm2", "web-2", "h1", "nfs");
    put_vm(&mut b, "vm3", "db-1", "h2", "nfs");
    b.vm("vm4", "report-1", 4, false).link(&[("h2", "vm4")]);
    b.backup("bk1", "nightly", BackupType::Incremental, &["vm1", "vm2", "vm3"]);
    let start = b.done();
    b.link(&[("nfs", "vm4"), ("vm4", "bk1")]);
    let sc = Scenario {
        id: s("new-vm"),
        title: s("The VM created last week"),
        story: s("report-1 was created last week on host-2 and nobody finished it: it has no disk and no backup."),
        goal: s("report-1 has a disk on nfs-data, and every VM is backed up off its domain"),
        hint: s("Compare report-1 with the other VMs: it is missing everything they have. Once it has a disk, the backup has to cover it as well."),
        palette: vec![Kind::Backup],
        max_nodes: 14,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::Link { rel: Rel::Disk, min: 4 },
            TopoGoal::AllVmsBackedUp,
            TopoGoal::RestorableAfterDomainLoss,
        ],
    };
    (sc, b.done())
}
