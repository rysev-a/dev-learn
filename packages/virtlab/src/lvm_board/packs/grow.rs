//! Chapter 16: from raw disks to a volume, and growing it.

use std::collections::BTreeMap;

use super::super::{Kind, LvmGoal, Scenario, Topology, Workload};
use super::builder::*;

/// Scenarios of the pack "grow" (chapter 16) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut raw = B::default();
    raw.disk("d1", "sdb", 50).disk("d2", "sdc", 50);
    let build = Scenario {
        id: s("build"),
        title: s("Disks into a volume"),
        story: s("Two empty 50 GiB disks have just been added to the server. Make physical volumes of them, put them into one volume group, carve a volume of 50 GiB and put a filesystem on it. A physical volume is a little smaller than its disk: the first MiB holds the label and the metadata."),
        goal: s("A working volume of 50 GiB with a filesystem of the same size"),
        hint: s("The extents of one 50 GiB disk are just short of 50 GiB, so a volume of 50 GiB needs both disks in the group. Choose the size of the volume, then the same size for the filesystem."),
        palette: vec![Kind::Pv, Kind::Vg, Kind::Lv, Kind::Fs],
        max_nodes: 12,
        start: raw.done(),
        workload: Workload::default(),
        goals: vec![
            LvmGoal::Healthy,
            LvmGoal::Has { node: Kind::Pv, min: 2 },
            LvmGoal::LvSize { lv: None, min_gib: 50, count: 1 },
            LvmGoal::FsFits,
        ],
    };
    let mut build_ref = raw.clone();
    build_ref.pv("pv1", "pv1", "d1").pv("pv2", "pv2", "d2").vg("vg", "vg0", 4, &["pv1", "pv2"]).lv("data", "data", "vg", 50, 1).fs(
        "fs", "ext4", "data", "ext4", 50,
    );

    let mut small = B::default();
    small.disk("d1", "sda", 100).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("data", "data", "vg", 20, 1).fs(
        "fs-data", "ext4", "data", "ext4", 20,
    );
    let extend = Scenario {
        id: s("extend"),
        title: s("Room to grow"),
        story: s("The data volume is 20 GiB and almost full. The group has plenty of free space. Make the volume 50 GiB; a bigger volume is no use until the filesystem on it grows too (lvextend -r does both)."),
        goal: s("The data volume is 50 GiB and its filesystem has grown with it"),
        hint: s("Set the size of the volume, then the size of the filesystem on it."),
        palette: vec![Kind::Lv, Kind::Fs],
        max_nodes: 12,
        start: small.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::LvSize { lv: Some(s("data")), min_gib: 50, count: 1 }, LvmGoal::FsFits],
    };
    let mut extend_ref = small.clone();
    extend_ref.param("data", "size", "50").param("fs-data", "size", "50");

    let mut full = B::default();
    full.disk("d1", "sda", 50).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("data", "data", "vg", 20, 1).lv(
        "logs", "logs", "vg", 20, 1,
    ).fs("fs-data", "ext4", "data", "ext4", 20);
    let add_disk = Scenario {
        id: s("add-disk"),
        title: s("The group is full"),
        story: s("The only disk is almost fully used: data and logs take 20 GiB each and about 10 GiB are free. The data volume has to be 50 GiB. Bring in a new disk and add it to the group, then grow the volume and its filesystem."),
        goal: s("The data volume is 50 GiB, its filesystem has grown with it, and everything works"),
        hint: s("A new disk becomes a physical volume, and the physical volume joins the group. Only then does the group have room for the bigger volume."),
        palette: vec![Kind::Disk, Kind::Pv],
        max_nodes: 14,
        start: full.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::LvSize { lv: Some(s("data")), min_gib: 50, count: 1 }, LvmGoal::FsFits],
    };
    let mut add_ref = full.clone();
    add_ref.disk("d2", "sdb", 100).pv("pv2", "pv2", "d2").link(&[("pv2", "vg")]);
    add_ref.param("data", "size", "50").param("fs-data", "size", "50");

    let mut orphan = B::default();
    orphan.disk("d1", "sda", 50).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("data", "data", "vg", 20, 1).fs(
        "fs-data", "ext4", "data", "ext4", 20,
    ).disk("d2", "sdb", 50).pv("pv2", "pv2", "d2");
    let orphan_pv = Scenario {
        id: s("orphan-pv"),
        title: s("The new disk is not in the group"),
        story: s("A second disk was prepared with pvcreate, but nobody ran vgextend: its physical volume belongs to no group, so the group still has one disk. The data volume has to grow to 50 GiB."),
        goal: s("The new physical volume is in the group, and the data volume is 50 GiB with a filesystem that has grown with it"),
        hint: s("Link the physical volume to the group. A physical volume in no group gives the group nothing."),
        palette: vec![Kind::Pv, Kind::Lv, Kind::Fs],
        max_nodes: 14,
        start: orphan.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::LvSize { lv: Some(s("data")), min_gib: 50, count: 1 }, LvmGoal::FsFits],
    };
    let mut orphan_ref = orphan.clone();
    orphan_ref.link(&[("pv2", "vg")]).param("data", "size", "50").param("fs-data", "size", "50");

    let mut solution = BTreeMap::new();
    solution.insert(s("build"), build_ref.done());
    solution.insert(s("extend"), extend_ref.done());
    solution.insert(s("add-disk"), add_ref.done());
    solution.insert(s("orphan-pv"), orphan_ref.done());
    (vec![build, extend, add_disk, orphan_pv], solution)
}
