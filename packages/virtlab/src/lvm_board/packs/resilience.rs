//! Chapter 16: moving data off a disk, mirrors, VM disks.

use std::collections::BTreeMap;

use super::super::{Kind, LvmGoal, Scenario, Topology, Workload};
use super::builder::*;

/// Scenarios of the pack "resilience" (chapter 16) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut two = B::default();
    two.disk("d1", "sda", 50).disk("d2", "sdb", 50).pv("pv1", "pv1", "d1").pv("pv2", "pv2", "d2").vg("vg", "vg0", 4, &["pv1", "pv2"]).lv(
        "data", "data", "vg", 20, 1,
    ).lv("db", "db", "vg", 50, 1);
    let evacuate = Scenario {
        id: s("evacuate"),
        title: s("Empty a disk"),
        story: s("The first disk has to be retired. pvmove can empty a physical volume only if the other physical volumes of the group have room for its extents. Right now the second disk is too full for that."),
        goal: s("The data of the first physical volume fit on the other physical volumes"),
        hint: s("Add a disk, make a physical volume of it and put it into the group: the group gets free extents that pvmove can use."),
        palette: vec![Kind::Disk, Kind::Pv],
        max_nodes: 12,
        start: two.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::Evacuable { pv: s("pv1") }, LvmGoal::Has { node: Kind::Pv, min: 3 }],
    };
    let mut evacuate_ref = two.clone();
    evacuate_ref.disk("d3", "sdc", 50).pv("pv3", "pv3", "d3").link(&[("pv3", "vg")]);

    let mut single = B::default();
    single.disk("d1", "sda", 50).disk("d2", "sdb", 50).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("db", "db", "vg", 20, 1).lv(
        "web", "web", "vg", 10, 1,
    );
    let mirror = Scenario {
        id: s("mirror"),
        title: s("Survive a disk failure"),
        story: s("Both volumes live on one disk, so the loss of that disk loses both. A second disk is in the server but unused. A mirror keeps a copy of a volume on each of two physical volumes."),
        goal: s("After losing any single disk no volume is lost"),
        hint: s("A mirror needs two physical volumes in the group: prepare the second disk and add it to the group. Then ask for two copies on each volume."),
        palette: vec![Kind::Pv],
        max_nodes: 10,
        start: single.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::SurviveDiskLoss, LvmGoal::Has { node: Kind::Pv, min: 2 }],
    };
    let mut mirror_ref = single.clone();
    mirror_ref.pv("pv2", "pv2", "d2").link(&[("pv2", "vg")]).param("db", "mirror", "2").param("web", "mirror", "2");

    let mut vms = B::default();
    vms.disk("d1", "mpatha", 200).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("vm1-disk", "vm1-disk", "vg", 100, 1).lv(
        "vm2-disk", "vm2-disk", "vg", 50, 1,
    ).vm("vm1", "vm1", &["vm1-disk"]).vm("vm2", "vm2", &["vm2-disk"]);
    let vm_disks = Scenario {
        id: s("vm-disks"),
        title: s("Disks for a third VM"),
        story: s("A block storage domain is a volume group on a LUN, and every VM disk is a logical volume in it. Two VMs run on a 200 GiB LUN and about 50 GiB are free. The third VM needs a 50 GiB disk."),
        goal: s("Three VMs run, each with a disk of 50 GiB or more"),
        hint: s("A 50 GiB volume needs a little more than the 50 GiB that are free. Bring another LUN into the group, carve the volume and attach it to the new VM."),
        palette: vec![Kind::Disk, Kind::Pv, Kind::Lv, Kind::Vm],
        max_nodes: 16,
        start: vms.done(),
        workload: Workload::default(),
        goals: vec![LvmGoal::Healthy, LvmGoal::Has { node: Kind::Vm, min: 3 }, LvmGoal::LvSize { lv: None, min_gib: 50, count: 3 }],
    };
    let mut vms_ref = vms.clone();
    vms_ref.disk("d2", "mpathb", 100).pv("pv2", "pv2", "d2").link(&[("pv2", "vg")]).lv("vm3-disk", "vm3-disk", "vg", 50, 1).vm("vm3", "vm3", &["vm3-disk"]);

    let mut old = B::default();
    old.disk("d-old", "sda", 50).disk("d-new", "sdb", 20).pv("pv-old", "pv-old", "d-old").pv("pv-new", "pv-new", "d-new").vg("vg", "vg0", 4, &["pv-old", "pv-new"]).lv(
        "data", "data", "vg", 20, 1,
    );
    let retire = Scenario {
        id: s("retire"),
        title: s("Remove the old disk"),
        story: s("The old 50 GiB disk goes away, and only the new disk stays. Before the old physical volume can be removed, everything on it must fit on the new one. A 20 GiB volume needs 5120 extents, and a 20 GiB disk gives 5119: the first MiB is metadata."),
        goal: s("One disk and one physical volume are left, and the 20 GiB data volume still works"),
        hint: s("Make the new disk larger, then remove the old physical volume and its disk from the board."),
        palette: vec![Kind::Disk, Kind::Pv],
        max_nodes: 10,
        start: old.done(),
        workload: Workload::default(),
        goals: vec![
            LvmGoal::Healthy,
            LvmGoal::AtMost { node: Kind::Disk, max: 1 },
            LvmGoal::AtMost { node: Kind::Pv, max: 1 },
            LvmGoal::LvSize { lv: Some(s("data")), min_gib: 20, count: 1 },
        ],
    };
    let mut retire_ref = B { t: old.t.without("d-old").without("pv-old") };
    retire_ref.param("d-new", "size", "50");

    let mut solution = BTreeMap::new();
    solution.insert(s("evacuate"), evacuate_ref.done());
    solution.insert(s("mirror"), mirror_ref.done());
    solution.insert(s("vm-disks"), vms_ref.done());
    solution.insert(s("retire"), retire_ref.done());
    (vec![evacuate, mirror, vm_disks, retire], solution)
}
