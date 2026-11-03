//! What follows from the links: the statuses of the objects of the board.
//!
//! The model in short (the rules of the lab):
//! * a physical volume of `S` MiB has `(S - 1) // pe` usable extents (the first MiB is the label and the metadata area), `pe` is the extent size of
//!   its group (4 MiB while it is in none); a physical volume without a disk has none;
//! * a logical volume takes its size rounded up to whole extents, a thin pool its data plus its metadata, a classic snapshot its size; thin volumes
//!   and thin snapshots take nothing from the group;
//! * they are placed in the order of the board, first-fit over the physical volumes of the group in the order of the board: a linear volume may span
//!   physical volumes, a mirror puts each of its two copies on a physical volume of its own;
//! * a thin pool is used by what the workload of the scenario writes (at most the virtual size of its thin volumes) plus what changes in the origins
//!   of its thin snapshots; its metadata take 1 MiB per GiB used (64 KiB chunks, 64 bytes per chunk); a pool with autoextend grows by 20% while
//!   80% or more of the data or of the metadata is used and the group has room;
//! * a classic snapshot overflows (becomes invalid) when more changed in its origin than the snapshot holds; it can never need more than the origin.

use std::collections::{BTreeMap, BTreeSet};

use serde::{Deserialize, Serialize};

use super::{Kind, Node, Rel, Topology};

/// The write load of a scenario: what happens to the data while the student's layout is in use.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(default)]
pub struct Workload {
    /// GiB that change in a volume while it has a snapshot (the backup window).
    pub changed_gib: u32,
    /// GiB written into the thin volumes of a pool.
    pub written_gib: u32,
}

/// A part of a volume on one physical volume.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Piece {
    /// Physical volume.
    pub pv: String,
    /// Extents on it.
    pub extents: u32,
    /// Which copy of a mirror it belongs to (0 for a linear volume).
    pub leg: u8,
}

/// Status of a physical volume.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PvStatus {
    /// Made of a disk and in a volume group.
    Ok,
    /// Not made of a disk: it has no extents.
    NoDisk,
    /// Not in a volume group: nothing can be carved from it.
    NoGroup,
}

impl PvStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            PvStatus::Ok => i18n::tr("in use"),
            PvStatus::NoDisk => i18n::tr("no disk"),
            PvStatus::NoGroup => i18n::tr("not in a group"),
        }
    }
}

/// Status of a volume group.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VgStatus {
    /// Has no extents.
    Empty,
    /// Has free extents.
    Ok,
    /// Every extent is taken.
    Full,
}

impl VgStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            VgStatus::Empty => i18n::tr("empty"),
            VgStatus::Ok => i18n::tr("has free space"),
            VgStatus::Full => i18n::tr("full"),
        }
    }
}

/// Status of a logical or a thin volume.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VolStatus {
    /// Works.
    Ok,
    /// A logical volume that is not carved from a group.
    NoGroup,
    /// A thin volume that is not in a pool.
    NoPool,
    /// The group has no room for it.
    NoSpace,
    /// A mirror needs two physical volumes with room for a copy each.
    NeedsTwoPvs,
    /// The pool of a thin volume could not be created.
    PoolDown,
    /// The pool of a thin volume is full: writes fail.
    PoolFull,
}

impl VolStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            VolStatus::Ok => i18n::tr("active"),
            VolStatus::NoGroup => i18n::tr("no group"),
            VolStatus::NoPool => i18n::tr("no pool"),
            VolStatus::NoSpace => i18n::tr("no space"),
            VolStatus::NeedsTwoPvs => i18n::tr("needs two physical volumes"),
            VolStatus::PoolDown => i18n::tr("pool down"),
            VolStatus::PoolFull => i18n::tr("pool full"),
        }
    }
}

/// Status of a thin pool.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PoolStatus {
    /// Below 80% used.
    Ok,
    /// 80% or more of the data or of the metadata is used.
    Warn,
    /// The data or the metadata are full: writes fail.
    Full,
    /// The group has no room for the pool.
    NoSpace,
    /// Not carved from a group.
    NoGroup,
}

impl PoolStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            PoolStatus::Ok => i18n::tr("active"),
            PoolStatus::Warn => i18n::tr("nearly full"),
            PoolStatus::Full => i18n::tr("full"),
            PoolStatus::NoSpace => i18n::tr("no space"),
            PoolStatus::NoGroup => i18n::tr("no group"),
        }
    }
}

/// Status of a snapshot.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SnapStatus {
    /// Holds the changes of its origin.
    Valid,
    /// More changed than it can hold: it is lost.
    Invalid,
    /// The group has no room for it.
    NoSpace,
    /// Has no origin.
    Orphan,
    /// Its origin does not work.
    OriginDown,
    /// The pool of a thin snapshot is full.
    PoolFull,
}

impl SnapStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            SnapStatus::Valid => i18n::tr("valid"),
            SnapStatus::Invalid => i18n::tr("invalid"),
            SnapStatus::NoSpace => i18n::tr("no space"),
            SnapStatus::Orphan => i18n::tr("no origin"),
            SnapStatus::OriginDown => i18n::tr("origin down"),
            SnapStatus::PoolFull => i18n::tr("pool full"),
        }
    }
}

/// Status of a filesystem.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum FsStatus {
    /// As large as its volume.
    Ok,
    /// Smaller than its volume: the volume grew and the filesystem did not.
    NotGrown,
    /// Larger than its volume.
    TooBig,
    /// On no volume.
    Detached,
    /// Its volume does not work.
    VolumeDown,
}

impl FsStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            FsStatus::Ok => i18n::tr("mounted"),
            FsStatus::NotGrown => i18n::tr("not grown"),
            FsStatus::TooBig => i18n::tr("larger than the volume"),
            FsStatus::Detached => i18n::tr("no volume"),
            FsStatus::VolumeDown => i18n::tr("volume down"),
        }
    }
}

/// Status of a VM.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VmStatus {
    /// Every disk works.
    Ok,
    /// A disk does not work.
    Down,
    /// Has no disk.
    NoDisk,
}

impl VmStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            VmStatus::Ok => i18n::tr("running"),
            VmStatus::Down => i18n::tr("down"),
            VmStatus::NoDisk => i18n::tr("no disk"),
        }
    }
}

/// Why an object is not well.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Why {
    /// The physical volume has no disk.
    PvNoDisk,
    /// The physical volume is in no group.
    PvNoGroup,
    /// The volume or the pool is not carved from a group.
    NoGroup,
    /// The thin volume is in no pool.
    NoPool,
    /// The group lacks extents.
    NoSpace {
        /// Extents needed.
        need: u32,
        /// Extents free in the group.
        free: u32,
    },
    /// A mirror cannot put its copies on two physical volumes.
    NeedsTwoPvs,
    /// The snapshot overflowed.
    Overflow {
        /// GiB that changed.
        changed_gib: u32,
        /// GiB the snapshot holds.
        holds_gib: u32,
    },
    /// The snapshot has no origin.
    NoOrigin,
    /// The pool is full.
    PoolFull {
        /// The metadata are full (otherwise the data).
        meta: bool,
    },
    /// The pool could not be created.
    PoolDown,
    /// The volume under it does not work.
    VolumeDown,
    /// The filesystem is smaller than its volume.
    FsSmaller {
        /// Filesystem GiB.
        fs: u64,
        /// Volume GiB.
        volume: u64,
    },
    /// The filesystem is larger than its volume.
    FsLarger {
        /// Filesystem GiB.
        fs: u64,
        /// Volume GiB.
        volume: u64,
    },
    /// The filesystem sits on no volume.
    FsDetached,
    /// The VM has no disk.
    NoDisk,
}

impl Why {
    /// The explanation for the student.
    pub fn text(&self) -> String {
        match self {
            Why::PvNoDisk => i18n::tr("the physical volume is made of no disk, so it has no extents").to_string(),
            Why::PvNoGroup => i18n::tr("the physical volume is in no volume group, so nothing is carved from it").to_string(),
            Why::NoGroup => i18n::tr("it is not carved from a volume group").to_string(),
            Why::NoPool => i18n::tr("it is not in a thin pool").to_string(),
            Why::NoSpace { need, free } => i18n::trf!("it needs {0} extents and the group has {1} free", need, free),
            Why::NeedsTwoPvs => {
                i18n::tr("a mirror needs two physical volumes of the group, each with room for a copy").to_string()
            }
            Why::Overflow { changed_gib, holds_gib } => {
                i18n::trf!("{0} GiB changed but the snapshot holds {1} GiB: it overflowed and is lost", changed_gib, holds_gib)
            }
            Why::NoOrigin => i18n::tr("the snapshot is taken of no volume").to_string(),
            Why::PoolFull { meta: false } => i18n::tr("the data of the pool are full: writes fail").to_string(),
            Why::PoolFull { meta: true } => i18n::tr("the metadata of the pool are full: writes fail").to_string(),
            Why::PoolDown => i18n::tr("the thin pool does not work").to_string(),
            Why::VolumeDown => i18n::tr("the volume under it does not work").to_string(),
            Why::FsSmaller { fs, volume } => {
                i18n::trf!("the filesystem is {0} GiB and the volume {1} GiB: grow the filesystem (lvextend -r does both)", fs, volume)
            }
            Why::FsLarger { fs, volume } => {
                i18n::trf!("the filesystem is {0} GiB but the volume is only {1} GiB", fs, volume)
            }
            Why::FsDetached => i18n::tr("the filesystem sits on no volume").to_string(),
            Why::NoDisk => i18n::tr("the VM has no disk").to_string(),
        }
    }
}

/// A physical volume.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PvEval {
    /// Identifier.
    pub id: String,
    /// Disk it is made of.
    pub disk: Option<String>,
    /// Group it belongs to.
    pub vg: Option<String>,
    /// Usable extents.
    pub extents: u32,
    /// Extents taken.
    pub used: u32,
    /// Status.
    pub status: PvStatus,
    /// Why it is not in use.
    pub why: Option<Why>,
}

impl PvEval {
    /// Extents free.
    pub fn free(&self) -> u32 {
        self.extents - self.used
    }
}

/// A volume group.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct VgEval {
    /// Identifier.
    pub id: String,
    /// Extent size in MiB.
    pub pe_mib: u64,
    /// Physical volumes that belong to it.
    pub pvs: Vec<String>,
    /// Extents in total.
    pub total: u32,
    /// Extents taken.
    pub used: u32,
    /// Status.
    pub status: VgStatus,
}

impl VgEval {
    /// Extents free.
    pub fn free(&self) -> u32 {
        self.total - self.used
    }

    /// Free space in GiB (whole GiB).
    pub fn free_gib(&self) -> u64 {
        u64::from(self.free()) * self.pe_mib / 1024
    }

    /// Total space in GiB (whole GiB).
    pub fn total_gib(&self) -> u64 {
        u64::from(self.total) * self.pe_mib / 1024
    }
}

/// A logical or a thin volume.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct VolEval {
    /// Identifier.
    pub id: String,
    /// Group (logical volumes) or the group of the pool (thin volumes).
    pub vg: Option<String>,
    /// Size in GiB (the virtual size of a thin volume).
    pub size_gib: u64,
    /// Extents taken from the group (0 for a thin volume).
    pub extents: u32,
    /// Status.
    pub status: VolStatus,
    /// Why it does not work.
    pub why: Option<Why>,
}

/// A thin pool.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PoolEval {
    /// Identifier.
    pub id: String,
    /// Group.
    pub vg: Option<String>,
    /// Extents of the data (after autoextend).
    pub data_extents: u32,
    /// Extents of the metadata (after autoextend).
    pub meta_extents: u32,
    /// Extents added by autoextend.
    pub extended: u32,
    /// Capacity of the data in GiB.
    pub data_gib: u64,
    /// GiB used.
    pub used_gib: u64,
    /// Percent of the data used (rounded up).
    pub data_pct: u64,
    /// Percent of the metadata used (rounded up).
    pub meta_pct: u64,
    /// Sum of the virtual sizes of its thin volumes in GiB.
    pub virtual_gib: u64,
    /// Status.
    pub status: PoolStatus,
    /// Why it does not work.
    pub why: Option<Why>,
}

impl PoolEval {
    /// How many times the virtual sizes exceed the data, in percent (150: one and a half times).
    pub fn overprovision_pct(&self) -> u64 {
        (self.virtual_gib * 100).checked_div(self.data_gib).unwrap_or(0)
    }
}

/// A snapshot.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SnapEval {
    /// Identifier.
    pub id: String,
    /// Origin.
    pub origin: Option<String>,
    /// A snapshot of a thin volume (it shares the pool).
    pub thin: bool,
    /// GiB that changed in the origin under the workload.
    pub changed_gib: u64,
    /// GiB the snapshot holds (0 for a thin snapshot).
    pub holds_gib: u64,
    /// Percent of its space used (rounded up, a classic snapshot only).
    pub pct: u64,
    /// Status.
    pub status: SnapStatus,
    /// Why it does not work.
    pub why: Option<Why>,
}

/// A filesystem.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FsEval {
    /// Identifier.
    pub id: String,
    /// Volume it sits on.
    pub volume: Option<String>,
    /// Size of the filesystem in GiB.
    pub fs_gib: u64,
    /// Size of the volume in GiB.
    pub volume_gib: u64,
    /// Status.
    pub status: FsStatus,
    /// Why it is not well.
    pub why: Option<Why>,
}

/// A VM.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct VmEval {
    /// Identifier.
    pub id: String,
    /// Its disks.
    pub volumes: Vec<String>,
    /// Status.
    pub status: VmStatus,
    /// Why it is not running.
    pub why: Option<Why>,
}

/// The evaluation of the whole board.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Evaluation {
    /// Physical volumes.
    pub pvs: Vec<PvEval>,
    /// Volume groups.
    pub vgs: Vec<VgEval>,
    /// Logical and thin volumes.
    pub volumes: Vec<VolEval>,
    /// Thin pools.
    pub pools: Vec<PoolEval>,
    /// Snapshots.
    pub snapshots: Vec<SnapEval>,
    /// Filesystems.
    pub filesystems: Vec<FsEval>,
    /// VMs.
    pub vms: Vec<VmEval>,
    /// Where the logical volumes, the pools and the classic snapshots are placed.
    pub placement: BTreeMap<String, Vec<Piece>>,
}

impl Evaluation {
    /// A physical volume.
    pub fn pv(&self, id: &str) -> Option<&PvEval> {
        self.pvs.iter().find(|x| x.id == id)
    }

    /// A volume group.
    pub fn vg(&self, id: &str) -> Option<&VgEval> {
        self.vgs.iter().find(|x| x.id == id)
    }

    /// A logical or a thin volume.
    pub fn volume(&self, id: &str) -> Option<&VolEval> {
        self.volumes.iter().find(|x| x.id == id)
    }

    /// A thin pool.
    pub fn pool(&self, id: &str) -> Option<&PoolEval> {
        self.pools.iter().find(|x| x.id == id)
    }

    /// A snapshot.
    pub fn snapshot(&self, id: &str) -> Option<&SnapEval> {
        self.snapshots.iter().find(|x| x.id == id)
    }

    /// A filesystem.
    pub fn fs(&self, id: &str) -> Option<&FsEval> {
        self.filesystems.iter().find(|x| x.id == id)
    }

    /// A VM.
    pub fn vm(&self, id: &str) -> Option<&VmEval> {
        self.vms.iter().find(|x| x.id == id)
    }
}

/// Usable extents of a physical volume made of a disk of `size_gib` GiB when the extent size is `pe_mib` MiB.
pub fn pv_extents(size_gib: u64, pe_mib: u64) -> u32 {
    u32::try_from((size_gib * 1024).saturating_sub(1) / pe_mib.max(1)).unwrap_or(u32::MAX)
}

/// Extents a size of `mib` MiB takes (rounded up).
pub fn extents_of(mib: u64, pe_mib: u64) -> u32 {
    u32::try_from(mib.div_ceil(pe_mib.max(1))).unwrap_or(u32::MAX)
}

/// Percent of `part` in `whole`, rounded up (100 for an empty whole).
fn pct(part: u64, whole: u64) -> u64 {
    if whole == 0 {
        100
    } else {
        (part * 100).div_ceil(whole)
    }
}

#[derive(Debug)]
enum Fail {
    NoSpace,
    NeedsTwoPvs,
}

/// Free extents of the physical volumes of the groups, handed out first-fit.
struct Alloc {
    free: BTreeMap<String, u32>,
    members: BTreeMap<String, Vec<String>>,
}

impl Alloc {
    fn free_of(&self, vg: &str) -> u32 {
        self.members.get(vg).map_or(0, |pvs| pvs.iter().map(|p| self.free[p]).sum())
    }

    fn linear(&mut self, vg: &str, want: u32) -> Option<Vec<Piece>> {
        if want == 0 || self.free_of(vg) < want {
            return None;
        }
        let mut left = want;
        let mut out = vec![];
        for pv in self.members.get(vg)?.clone() {
            let take = self.free[&pv].min(left);
            if take > 0 {
                *self.free.get_mut(&pv)? -= take;
                out.push(Piece { pv, extents: take, leg: 0 });
                left -= take;
            }
            if left == 0 {
                break;
            }
        }
        Some(out)
    }

    fn mirror(&mut self, vg: &str, want: u32) -> Result<Vec<Piece>, Fail> {
        let pvs = self.members.get(vg).cloned().unwrap_or_default();
        if pvs.len() < 2 {
            return Err(Fail::NeedsTwoPvs);
        }
        let first = pvs.iter().find(|p| self.free[*p] >= want);
        let second = first.and_then(|f| pvs.iter().find(|p| *p != f && self.free[*p] >= want));
        match (first, second) {
            (Some(a), Some(b)) => {
                let (a, b) = (a.clone(), b.clone());
                *self.free.get_mut(&a).ok_or(Fail::NoSpace)? -= want;
                *self.free.get_mut(&b).ok_or(Fail::NoSpace)? -= want;
                Ok(vec![Piece { pv: a, extents: want, leg: 0 }, Piece { pv: b, extents: want, leg: 1 }])
            }
            _ => Err(Fail::NoSpace),
        }
    }
}

fn add_pieces(into: &mut Vec<Piece>, more: Vec<Piece>) {
    for p in more {
        match into.iter_mut().find(|q| q.pv == p.pv && q.leg == p.leg) {
            Some(q) => q.extents += p.extents,
            None => into.push(p),
        }
    }
}

fn why_for(fail: Fail, need: u32, free: u32) -> (VolStatus, Why) {
    match fail {
        Fail::NoSpace => (VolStatus::NoSpace, Why::NoSpace { need, free }),
        Fail::NeedsTwoPvs => (VolStatus::NeedsTwoPvs, Why::NeedsTwoPvs),
    }
}

/// Evaluates the board under a workload.
pub fn evaluate(t: &Topology, w: &Workload) -> Evaluation {
    let mut ev = Evaluation::default();

    // physical volumes and groups
    let mut alloc = Alloc { free: BTreeMap::new(), members: BTreeMap::new() };
    for pv in t.of_kind(Kind::Pv) {
        let disk = t.sources(&pv.id, Rel::Backs).first().map(|d| (*d).clone());
        let vg = t.vg_of_pv(&pv.id);
        let pe = vg.map_or(4, Node::pe_mib);
        let extents = disk.as_ref().map_or(0, |d| pv_extents(d.size_gib(), pe));
        let (status, why) = match (&disk, vg) {
            (None, _) => (PvStatus::NoDisk, Some(Why::PvNoDisk)),
            (_, None) => (PvStatus::NoGroup, Some(Why::PvNoGroup)),
            _ => (PvStatus::Ok, None),
        };
        if let (Some(_), Some(vg)) = (&disk, vg) {
            alloc.free.insert(pv.id.clone(), extents);
            alloc.members.entry(vg.id.clone()).or_default().push(pv.id.clone());
        }
        ev.pvs.push(PvEval {
            id: pv.id.clone(),
            disk: disk.map(|d| d.id),
            vg: vg.map(|v| v.id.clone()),
            extents,
            used: 0,
            status,
            why,
        });
    }

    // volumes, pools and classic snapshots take extents in the order of the board
    let mut pool_alloc: BTreeMap<String, Result<(), (PoolStatus, Why)>> = BTreeMap::new();
    let mut snap_alloc: BTreeMap<String, Result<(), (SnapStatus, Why)>> = BTreeMap::new();
    for n in &t.nodes {
        match n.kind {
            Kind::Lv => {
                let Some(vg) = t.vg_of(&n.id) else {
                    ev.volumes.push(VolEval {
                        id: n.id.clone(),
                        vg: None,
                        size_gib: n.size_gib(),
                        extents: 0,
                        status: VolStatus::NoGroup,
                        why: Some(Why::NoGroup),
                    });
                    continue;
                };
                let want = extents_of(n.size_gib() * 1024, vg.pe_mib());
                let free = alloc.free_of(&vg.id);
                let placed =
                    if n.mirrored() { alloc.mirror(&vg.id, want) } else { alloc.linear(&vg.id, want).ok_or(Fail::NoSpace) };
                let (status, why) = match placed {
                    Ok(pieces) => {
                        ev.placement.insert(n.id.clone(), pieces);
                        (VolStatus::Ok, None)
                    }
                    Err(f) => {
                        let (s, w) = why_for(f, want * if n.mirrored() { 2 } else { 1 }, free);
                        (s, Some(w))
                    }
                };
                ev.volumes.push(VolEval {
                    id: n.id.clone(),
                    vg: Some(vg.id.clone()),
                    size_gib: n.size_gib(),
                    extents: want,
                    status,
                    why,
                });
            }
            Kind::ThinPool => {
                let result = match t.vg_of(&n.id) {
                    None => Err((PoolStatus::NoGroup, Why::NoGroup)),
                    Some(vg) => {
                        let want = extents_of(n.size_gib() * 1024, vg.pe_mib()) + extents_of(n.num("meta"), vg.pe_mib());
                        let free = alloc.free_of(&vg.id);
                        match alloc.linear(&vg.id, want) {
                            Some(pieces) => {
                                ev.placement.insert(n.id.clone(), pieces);
                                Ok(())
                            }
                            None => Err((PoolStatus::NoSpace, Why::NoSpace { need: want, free })),
                        }
                    }
                };
                pool_alloc.insert(n.id.clone(), result);
            }
            Kind::Snapshot => {
                let result = match t.origin_of(&n.id) {
                    None => Err((SnapStatus::Orphan, Why::NoOrigin)),
                    Some(o) if o.kind == Kind::ThinLv => Ok(()),
                    Some(_) => match t.vg_of(&n.id) {
                        None => Err((SnapStatus::NoSpace, Why::NoGroup)),
                        Some(vg) => {
                            let want = extents_of(n.size_gib() * 1024, vg.pe_mib());
                            let free = alloc.free_of(&vg.id);
                            match alloc.linear(&vg.id, want) {
                                Some(pieces) => {
                                    ev.placement.insert(n.id.clone(), pieces);
                                    Ok(())
                                }
                                None => Err((SnapStatus::NoSpace, Why::NoSpace { need: want, free })),
                            }
                        }
                    },
                };
                snap_alloc.insert(n.id.clone(), result);
            }
            _ => {}
        }
    }

    // thin pools: the load, autoextend, the status
    for n in t.of_kind(Kind::ThinPool) {
        let vg = t.vg_of(&n.id);
        let pe = vg.map_or(4, Node::pe_mib);
        let thins = t.targets(&n.id, Rel::Thin);
        let virtual_gib: u64 = thins.iter().map(|x| x.size_gib()).sum();
        let written = u64::from(w.written_gib).min(virtual_gib);
        let snap_changes: u64 = thins
            .iter()
            .map(|x| t.targets(&x.id, Rel::SnapshotOf).len() as u64 * u64::from(w.changed_gib).min(x.size_gib()))
            .sum();
        let used_gib = written + snap_changes;
        let mut data_ext = extents_of(n.size_gib() * 1024, pe);
        let mut meta_ext = extents_of(n.num("meta"), pe);
        let mut extended = 0;
        let created = matches!(pool_alloc.get(&n.id), Some(Ok(())));
        if created && n.flag("autoextend") {
            if let Some(vg) = vg {
                for _ in 0..24 {
                    let data_hot = pct(used_gib * 1024, u64::from(data_ext) * pe) >= 80;
                    let meta_hot = pct(used_gib, u64::from(meta_ext) * pe) >= 80;
                    if !data_hot && !meta_hot {
                        break;
                    }
                    let add_data = if data_hot { (data_ext * 20).div_ceil(100).max(1) } else { 0 };
                    let add_meta = if meta_hot { (meta_ext * 20).div_ceil(100).max(1) } else { 0 };
                    let Some(pieces) = alloc.linear(&vg.id, add_data + add_meta) else { break };
                    add_pieces(ev.placement.entry(n.id.clone()).or_default(), pieces);
                    data_ext += add_data;
                    meta_ext += add_meta;
                    extended += add_data + add_meta;
                }
            }
        }
        let data_mib = u64::from(data_ext) * pe;
        let meta_mib = u64::from(meta_ext) * pe;
        let data_pct = pct(used_gib * 1024, data_mib);
        let meta_pct = pct(used_gib, meta_mib);
        let (status, why) = match pool_alloc.remove(&n.id) {
            Some(Err((s, w))) => (s, Some(w)),
            _ if data_pct >= 100 || meta_pct >= 100 => (PoolStatus::Full, Some(Why::PoolFull { meta: data_pct < 100 })),
            _ if data_pct >= 80 || meta_pct >= 80 => (PoolStatus::Warn, None),
            _ => (PoolStatus::Ok, None),
        };
        ev.pools.push(PoolEval {
            id: n.id.clone(),
            vg: vg.map(|v| v.id.clone()),
            data_extents: data_ext,
            meta_extents: meta_ext,
            extended,
            data_gib: data_mib / 1024,
            used_gib,
            data_pct,
            meta_pct,
            virtual_gib,
            status,
            why,
        });
    }

    // thin volumes follow their pool
    for n in t.of_kind(Kind::ThinLv) {
        let pool = t.pool_of(&n.id);
        let pool_eval = pool.and_then(|p| ev.pool(&p.id));
        let vg = pool_eval.and_then(|p| p.vg.clone());
        let (status, why) = match pool_eval {
            None => (VolStatus::NoPool, Some(Why::NoPool)),
            Some(p) => match p.status {
                PoolStatus::Ok | PoolStatus::Warn => (VolStatus::Ok, None),
                PoolStatus::Full => (VolStatus::PoolFull, p.why.clone()),
                PoolStatus::NoSpace | PoolStatus::NoGroup => (VolStatus::PoolDown, Some(Why::PoolDown)),
            },
        };
        ev.volumes.push(VolEval { id: n.id.clone(), vg, size_gib: n.size_gib(), extents: 0, status, why });
    }

    // snapshots
    for n in t.of_kind(Kind::Snapshot) {
        let origin = t.origin_of(&n.id);
        let origin_eval = origin.and_then(|o| ev.volume(&o.id));
        let thin = origin.is_some_and(|o| o.kind == Kind::ThinLv);
        let origin_gib = origin.map_or(0, Node::size_gib);
        let changed = u64::from(w.changed_gib).min(origin_gib);
        let mut holds_gib = 0;
        let mut share = 0;
        let (status, why) = match snap_alloc.remove(&n.id) {
            Some(Err((s, w))) => (s, Some(w)),
            _ if thin && origin_eval.is_some_and(|o| o.status == VolStatus::PoolFull) => {
                (SnapStatus::PoolFull, origin_eval.and_then(|o| o.why.clone()))
            }
            _ if origin_eval.is_some_and(|o| o.status != VolStatus::Ok) => (SnapStatus::OriginDown, Some(Why::VolumeDown)),
            _ if thin => (SnapStatus::Valid, None),
            _ => {
                let vg = t.vg_of(&n.id);
                let ext = extents_of(n.size_gib() * 1024, vg.map_or(4, Node::pe_mib));
                let cow_mib = u64::from(ext) * vg.map_or(4, Node::pe_mib);
                holds_gib = cow_mib / 1024;
                share = pct(changed * 1024, cow_mib);
                if changed * 1024 > cow_mib {
                    (SnapStatus::Invalid, Some(Why::Overflow { changed_gib: u32::try_from(changed).unwrap_or(u32::MAX), holds_gib: u32::try_from(holds_gib).unwrap_or(u32::MAX) }))
                } else {
                    (SnapStatus::Valid, None)
                }
            }
        };
        // a thin snapshot lives or dies with the pool of its origin
        let (status, why) = if thin && status == SnapStatus::Valid {
            let pool = origin.and_then(|o| t.pool_of(&o.id)).and_then(|p| ev.pool(&p.id));
            match pool {
                Some(p) if p.status == PoolStatus::Full => (SnapStatus::PoolFull, p.why.clone()),
                _ => (status, why),
            }
        } else {
            (status, why)
        };
        ev.snapshots.push(SnapEval {
            id: n.id.clone(),
            origin: origin.map(|o| o.id.clone()),
            thin,
            changed_gib: changed,
            holds_gib,
            pct: share,
            status,
            why,
        });
    }

    // filesystems
    for n in t.of_kind(Kind::Fs) {
        let vol = t.sources(&n.id, Rel::Holds).first().map(|v| (*v).clone());
        let vol_eval = vol.as_ref().and_then(|v| ev.volume(&v.id));
        let (fs_gib, volume_gib) = (n.size_gib(), vol.as_ref().map_or(0, Node::size_gib));
        let (status, why) = match (&vol, vol_eval) {
            (None, _) | (_, None) => (FsStatus::Detached, Some(Why::FsDetached)),
            (_, Some(v)) if v.status != VolStatus::Ok => (FsStatus::VolumeDown, Some(Why::VolumeDown)),
            _ if fs_gib < volume_gib => (FsStatus::NotGrown, Some(Why::FsSmaller { fs: fs_gib, volume: volume_gib })),
            _ if fs_gib > volume_gib => (FsStatus::TooBig, Some(Why::FsLarger { fs: fs_gib, volume: volume_gib })),
            _ => (FsStatus::Ok, None),
        };
        ev.filesystems.push(FsEval { id: n.id.clone(), volume: vol.map(|v| v.id), fs_gib, volume_gib, status, why });
    }

    // VMs
    for n in t.of_kind(Kind::Vm) {
        let volumes: Vec<String> =
            t.nodes.iter().filter(|v| v.kind.is_volume() && t.linked(&v.id, &n.id)).map(|v| v.id.clone()).collect();
        let (status, why) = if volumes.is_empty() {
            (VmStatus::NoDisk, Some(Why::NoDisk))
        } else if volumes.iter().all(|v| ev.volume(v).is_some_and(|x| x.status == VolStatus::Ok)) {
            (VmStatus::Ok, None)
        } else {
            (VmStatus::Down, Some(Why::VolumeDown))
        };
        ev.vms.push(VmEval { id: n.id.clone(), volumes, status, why });
    }

    // the groups: what is taken after everything was placed
    for pv in &mut ev.pvs {
        if let Some(free) = alloc.free.get(&pv.id) {
            pv.used = pv.extents - free;
        }
    }
    for vg in t.of_kind(Kind::Vg) {
        let pvs: Vec<String> = t.sources(&vg.id, Rel::Member).iter().map(|p| p.id.clone()).collect();
        let (total, used) = ev
            .pvs
            .iter()
            .filter(|p| pvs.contains(&p.id) && p.disk.is_some())
            .fold((0, 0), |(t, u), p| (t + p.extents, u + p.used));
        let status = if total == 0 {
            VgStatus::Empty
        } else if used >= total {
            VgStatus::Full
        } else {
            VgStatus::Ok
        };
        ev.vgs.push(VgEval { id: vg.id.clone(), pe_mib: vg.pe_mib(), pvs, total, used, status });
    }
    ev
}

/// What a disk takes with it when it is lost: the volumes, pools and snapshots that have no copy left, and everything built on them (the thin
/// volumes of a lost pool, the snapshots of a lost origin). In the order of the board.
pub fn lost_by_disk(t: &Topology, ev: &Evaluation, disk: &str) -> Vec<String> {
    let lost_pvs: BTreeSet<&str> =
        ev.pvs.iter().filter(|p| p.disk.as_deref() == Some(disk)).map(|p| p.id.as_str()).collect();
    if lost_pvs.is_empty() {
        return vec![];
    }
    let mut lost: BTreeSet<String> = BTreeSet::new();
    for (id, pieces) in &ev.placement {
        let legs: BTreeSet<u8> = pieces.iter().map(|p| p.leg).collect();
        let lost_legs: BTreeSet<u8> = pieces.iter().filter(|p| lost_pvs.contains(p.pv.as_str())).map(|p| p.leg).collect();
        if !legs.is_empty() && lost_legs.len() == legs.len() {
            lost.insert(id.clone());
        }
    }
    // what stands on what was lost (twice: a snapshot of a thin volume of a lost pool)
    for _ in 0..2 {
        for n in &t.nodes {
            let gone = match n.kind {
                Kind::ThinLv => t.pool_of(&n.id).is_some_and(|p| lost.contains(&p.id)),
                Kind::Snapshot => t.origin_of(&n.id).is_some_and(|o| lost.contains(&o.id)),
                _ => false,
            };
            if gone {
                lost.insert(n.id.clone());
            }
        }
    }
    t.nodes.iter().filter(|n| lost.contains(&n.id)).map(|n| n.id.clone()).collect()
}

/// After the loss of any single disk nothing is lost: there is at least one disk with a physical volume and at least one working volume,
/// and no disk takes a volume, a pool or a snapshot with it.
pub fn survives_disk_loss(t: &Topology, ev: &Evaluation) -> bool {
    let disks: Vec<&Node> = t.of_kind(Kind::Disk).collect();
    let used = disks.iter().any(|d| ev.pvs.iter().any(|p| p.disk.as_deref() == Some(d.id.as_str())));
    used && ev.volumes.iter().any(|v| v.status == VolStatus::Ok) && disks.iter().all(|d| lost_by_disk(t, ev, &d.id).is_empty())
}

/// The data of a physical volume fits on the other physical volumes of its group, so `pvmove` can empty it: every part of every volume that lies
/// on it finds room elsewhere (a copy of a mirror only on a physical volume that does not hold the other copy).
pub fn evacuable(t: &Topology, ev: &Evaluation, pv: &str) -> bool {
    let Some(source) = ev.pv(pv) else { return false };
    let Some(vg) = source.vg.as_deref() else { return false };
    let mut free: BTreeMap<&str, u32> = BTreeMap::new();
    let mut order: Vec<&str> = vec![];
    for p in &ev.pvs {
        if p.id != pv && p.vg.as_deref() == Some(vg) && p.disk.is_some() {
            free.insert(p.id.as_str(), p.free());
            order.push(p.id.as_str());
        }
    }
    if order.is_empty() {
        return false;
    }
    for n in &t.nodes {
        let Some(pieces) = ev.placement.get(&n.id) else { continue };
        for piece in pieces.iter().filter(|p| p.pv == pv) {
            let mut left = piece.extents;
            let mirror = pieces.iter().any(|p| p.leg != piece.leg);
            if mirror {
                let holds: BTreeSet<&str> = pieces.iter().filter(|p| p.leg != piece.leg).map(|p| p.pv.as_str()).collect();
                let Some(target) = order.iter().find(|p| !holds.contains(**p) && free[**p] >= left) else { return false };
                if let Some(f) = free.get_mut(*target) {
                    *f -= left;
                }
            } else {
                for p in &order {
                    let take = free[*p].min(left);
                    if let Some(f) = free.get_mut(*p) {
                        *f -= take;
                    }
                    left -= take;
                }
                if left > 0 {
                    return false;
                }
            }
        }
    }
    true
}
