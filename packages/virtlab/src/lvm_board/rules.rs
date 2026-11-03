//! Which objects may be linked and what a link means; the checks of the board state.

use std::collections::{BTreeMap, BTreeSet};

use super::{param_error, Edge, Kind, Topology, MAX_NAME, MAX_NODES};

/// Relation a link stands for. The direction follows the table in [`rel`].
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Rel {
    /// A physical volume is made of a disk (`pvcreate`).
    Backs,
    /// A physical volume is a member of a volume group (`vgextend`).
    Member,
    /// A logical volume is carved from a volume group (`lvcreate`).
    Carves,
    /// A thin pool is carved from a volume group.
    Pool,
    /// A thin volume lives in a thin pool.
    Thin,
    /// A snapshot is taken of a volume (its origin).
    SnapshotOf,
    /// A filesystem sits on a volume.
    Holds,
    /// A volume is a disk of a VM.
    VmDisk,
}

impl Rel {
    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Rel::Backs => i18n::tr("made of the disk"),
            Rel::Member => i18n::tr("member of the volume group"),
            Rel::Carves => i18n::tr("carved from the volume group"),
            Rel::Pool => i18n::tr("thin pool of the volume group"),
            Rel::Thin => i18n::tr("thin volume of the pool"),
            Rel::SnapshotOf => i18n::tr("snapshot of"),
            Rel::Holds => i18n::tr("holds the filesystem"),
            Rel::VmDisk => i18n::tr("disk of the VM"),
        }
    }
}

/// Relation of a link from an object of one kind to an object of another (`None`: the objects are not linked directly).
pub fn rel(from: Kind, to: Kind) -> Option<Rel> {
    Some(match (from, to) {
        (Kind::Disk, Kind::Pv) => Rel::Backs,
        (Kind::Pv, Kind::Vg) => Rel::Member,
        (Kind::Vg, Kind::Lv) => Rel::Carves,
        (Kind::Vg, Kind::ThinPool) => Rel::Pool,
        (Kind::ThinPool, Kind::ThinLv) => Rel::Thin,
        (Kind::Lv | Kind::ThinLv, Kind::Snapshot) => Rel::SnapshotOf,
        (Kind::Lv | Kind::ThinLv, Kind::Fs) => Rel::Holds,
        (Kind::Lv | Kind::ThinLv, Kind::Vm) => Rel::VmDisk,
        _ => return None,
    })
}

/// Relations where an object of the target kind has exactly one source.
fn single_parent(r: Rel) -> bool {
    matches!(r, Rel::Backs | Rel::Carves | Rel::Pool | Rel::Thin | Rel::SnapshotOf | Rel::Holds)
}

/// Relations where an object of the source kind has exactly one target.
fn single_target(r: Rel) -> bool {
    matches!(r, Rel::Backs | Rel::Member | Rel::Holds | Rel::VmDisk)
}

/// A violated rule: the link it is about (index in `edges`) or the board as a whole, and the explanation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Problem {
    /// Index of the link, if the problem is about one.
    pub edge: Option<usize>,
    /// What is wrong, for the student.
    pub text: String,
}

fn about(edge: usize, text: &str) -> Problem {
    Problem { edge: Some(edge), text: text.to_string() }
}

fn single_parent_text(r: Rel) -> &'static str {
    match r {
        Rel::Backs => i18n::tr("a physical volume is made of one disk"),
        Rel::Carves => i18n::tr("a logical volume belongs to one volume group"),
        Rel::Pool => i18n::tr("a thin pool belongs to one volume group"),
        Rel::Thin => i18n::tr("a thin volume belongs to one thin pool"),
        Rel::SnapshotOf => i18n::tr("a snapshot has one origin"),
        _ => i18n::tr("a filesystem sits on one volume"),
    }
}

fn single_target_text(r: Rel) -> &'static str {
    match r {
        Rel::Backs => i18n::tr("a disk is used as one physical volume"),
        Rel::Member => i18n::tr("a physical volume belongs to one volume group"),
        Rel::Holds => i18n::tr("a volume holds one filesystem"),
        _ => i18n::tr("a volume is the disk of one VM"),
    }
}

/// Every rule the board state breaks. A state built with [`connect_error`] and [`prune`] has no problems; the server rejects a hand-made one.
pub fn problems(t: &Topology) -> Vec<Problem> {
    let mut out = vec![];
    let mut ids = BTreeSet::new();
    for n in &t.nodes {
        if n.id.is_empty() || !ids.insert(n.id.as_str()) {
            out.push(Problem { edge: None, text: i18n::tr("object identifiers must be unique and not empty").to_string() });
        }
        if n.name.chars().count() > MAX_NAME || !n.x.is_finite() || !n.y.is_finite() {
            out.push(Problem { edge: None, text: i18n::tr("an object has an invalid name or position").to_string() });
        }
        if let Some(text) = param_error(n) {
            out.push(Problem { edge: None, text });
        }
    }
    if t.nodes.len() > MAX_NODES {
        out.push(Problem { edge: None, text: i18n::trf!("at most {0} objects are allowed", MAX_NODES) });
    }
    if t.edges.len() > MAX_NODES * 3 {
        out.push(Problem { edge: None, text: i18n::tr("too many links").to_string() });
        return out;
    }
    let mut seen: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut seen_from: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut pairs = BTreeSet::new();
    for (i, Edge { from, to }) in t.edges.iter().enumerate() {
        let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
            out.push(about(i, i18n::tr("a link leads to an unknown object")));
            continue;
        };
        if from == to {
            out.push(about(i, i18n::tr("an object cannot be linked to itself")));
            continue;
        }
        let Some(r) = rel(a.kind, b.kind) else {
            out.push(about(i, i18n::tr("in LVM these objects are not linked directly")));
            continue;
        };
        if !pairs.insert((from.as_str(), to.as_str())) {
            out.push(about(i, i18n::tr("these objects are already linked")));
            continue;
        }
        if single_parent(r) && seen.insert((r, to.as_str()), i).is_some() {
            out.push(about(i, single_parent_text(r)));
            continue;
        }
        if single_target(r) && seen_from.insert((r, from.as_str()), i).is_some() {
            out.push(about(i, single_target_text(r)));
        }
    }
    out
}

/// Why the link `from → to` cannot be added to the board (`None`: it can). The direction is the one of [`rel`].
pub fn connect_error(t: &Topology, from: &str, to: &str) -> Option<String> {
    if from == to {
        return Some(i18n::tr("an object cannot be linked to itself").to_string());
    }
    let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
        return Some(i18n::tr("a link leads to an unknown object").to_string());
    };
    if rel(a.kind, b.kind).is_none() {
        return Some(i18n::tr("in LVM these objects are not linked directly").to_string());
    }
    let mut next = t.clone();
    next.edges.push(Edge::new(from, to));
    let index = next.edges.len() - 1;
    problems(&next).into_iter().find(|p| p.edge == Some(index)).map(|p| p.text)
}

/// Why an object of this kind cannot be added to the board (`None`: it can).
pub fn add_error(t: &Topology, _kind: Kind, max_nodes: usize) -> Option<String> {
    if t.nodes.len() >= max_nodes.min(MAX_NODES) {
        return Some(i18n::trf!("at most {0} objects are allowed", max_nodes.min(MAX_NODES)));
    }
    None
}

/// Drop the links that no longer make sense (after an object or a link was removed). Returns how many were dropped.
pub fn prune(t: &mut Topology) -> usize {
    let mut dropped = 0;
    loop {
        let bad = problems(t).into_iter().find_map(|p| p.edge);
        match bad {
            Some(i) => {
                t.edges.remove(i);
                dropped += 1;
            }
            None => return dropped,
        }
    }
}
