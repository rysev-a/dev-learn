//! Chapter 20: snapshots for backups and thin pools.

use std::collections::BTreeMap;

use super::super::{Kind, LvmGoal, Scenario, Topology, Workload};
use super::builder::*;

/// Scenarios of the pack "snapshots" (chapter 20) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let base = one_disk();
    let cow = Scenario {
        id: s("cow-size"),
        title: s("A snapshot for the backup"),
        story: s("The backup reads the data volume for a while, and about 8 GiB change in it meanwhile. A classic snapshot keeps the old blocks in its own area; if that area fills up, the snapshot is lost and the backup with it."),
        goal: s("The data volume has a snapshot that holds the changes of the backup window"),
        hint: s("Take a snapshot of the volume and give it more room than the changes: 8 GiB need at least a 10 GiB snapshot."),
        palette: vec![Kind::Snapshot],
        max_nodes: 10,
        start: base.done(),
        workload: Workload { changed_gib: 8, written_gib: 0 },
        goals: vec![LvmGoal::Healthy, LvmGoal::SnapshotValid],
    };
    let mut cow_ref = base.clone();
    cow_ref.snap("snap", "data-snap", "data", 10);

    let heavy = Scenario {
        id: s("heavy-writes"),
        title: s("Heavy writes"),
        story: s("A busy database changes about 40 GiB of the 50 GiB volume during the backup. The snapshot has to hold all of it, and the group has just under 50 GiB free."),
        goal: s("The snapshot survives the backup window and everything works"),
        hint: s("Only a snapshot of 50 GiB holds 40 GiB of changes, and the group has a little less than that. Add a disk to the group first."),
        palette: vec![Kind::Disk, Kind::Pv, Kind::Snapshot],
        max_nodes: 12,
        start: base.done(),
        workload: Workload { changed_gib: 40, written_gib: 0 },
        goals: vec![LvmGoal::Healthy, LvmGoal::SnapshotValid],
    };
    let mut heavy_ref = base.clone();
    heavy_ref.disk("d2", "sdb", 100).pv("pv2", "pv2", "d2").link(&[("pv2", "vg")]).snap("snap", "data-snap", "data", 50);

    let mut grow = B::default();
    grow.disk("d1", "sda", 200).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).pool("pool", "pool0", "vg", 50, 128).thin("t1", "vm-a", "pool", 50).thin(
        "t2", "vm-b", "pool", 50,
    ).thin("t3", "vm-c", "pool", 50);
    let thin_grow = Scenario {
        id: s("thin-grow"),
        title: s("An overprovisioned pool"),
        story: s("Three thin volumes of 50 GiB share a thin pool of 50 GiB: the pool promises three times what it has. Together they already hold 45 GiB of real data, so the pool is 90% full. When it reaches 100%, writes fail."),
        goal: s("The thin pool is below 80% used"),
        hint: s("Make the pool larger. The group has room, and a pool that grows by itself (autoextend) would also keep up."),
        palette: vec![Kind::ThinLv],
        max_nodes: 12,
        start: grow.done(),
        workload: Workload { changed_gib: 0, written_gib: 45 },
        goals: vec![LvmGoal::Healthy, LvmGoal::PoolFits],
    };
    let mut grow_ref = grow.clone();
    grow_ref.param("pool", "size", "100");

    let mut meta = B::default();
    meta.disk("d1", "sda", 500).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).pool("pool", "pool0", "vg", 200, 64).thin("t1", "vm-a", "pool", 500);
    let thin_meta = Scenario {
        id: s("thin-meta"),
        title: s("The metadata run out first"),
        story: s("Only a third of the data space of the pool is used, but writes fail: a thin pool keeps a map of its blocks in a separate metadata area, and in this lab it takes 1 MiB per GiB written. 70 GiB are written and the area is 64 MiB."),
        goal: s("The thin pool is below 80% used, data and metadata"),
        hint: s("Watch Meta% as well as Data%. Choose a larger metadata size for the pool."),
        palette: vec![Kind::ThinLv],
        max_nodes: 10,
        start: meta.done(),
        workload: Workload { changed_gib: 0, written_gib: 70 },
        goals: vec![LvmGoal::Healthy, LvmGoal::PoolFits],
    };
    let mut meta_ref = meta.clone();
    meta_ref.param("pool", "meta", "128");

    let mut thin = B::default();
    thin.disk("d1", "sda", 100).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).pool("pool", "pool0", "vg", 20, 128).thin("vm-disk", "vm-disk", "pool", 50);
    let thin_snapshot = Scenario {
        id: s("thin-snapshot"),
        title: s("A snapshot of a thin volume"),
        story: s("A snapshot of a thin volume needs no size of its own: it shares the pool, and only the blocks that change take new space. 15 GiB are written already, and 10 GiB will change while the snapshot exists. The pool is 20 GiB."),
        goal: s("The thin volume has a snapshot and the pool stays below 80% used"),
        hint: s("15 GiB plus 10 GiB of changes do not fit into 20 GiB. Take the snapshot and make the pool larger."),
        palette: vec![Kind::Snapshot],
        max_nodes: 10,
        start: thin.done(),
        workload: Workload { changed_gib: 10, written_gib: 15 },
        goals: vec![LvmGoal::Healthy, LvmGoal::SnapshotValid, LvmGoal::PoolFits],
    };
    let mut thin_ref = thin.clone();
    thin_ref.snap("snap", "vm-disk-snap", "vm-disk", 5).param("pool", "size", "50");

    let mut solution = BTreeMap::new();
    solution.insert(s("cow-size"), cow_ref.done());
    solution.insert(s("heavy-writes"), heavy_ref.done());
    solution.insert(s("thin-grow"), grow_ref.done());
    solution.insert(s("thin-meta"), meta_ref.done());
    solution.insert(s("thin-snapshot"), thin_ref.done());
    (vec![cow, heavy, thin_grow, thin_meta, thin_snapshot], solution)
}
