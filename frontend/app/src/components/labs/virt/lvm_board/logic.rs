//! Pure logic of the LVM board: the draft, adding and removing objects, links and their direction, wires on the board, fitting, statuses of
//! objects, the tree of disks and volumes and the "if a disk fails" report. No signals or DOM — everything is checked by ordinary tests; the
//! interface (`board.rs`, `panels.rs`, `lab.rs`) only calls these functions, and takes the rules and statuses from the `virtlab::lvm_board`
//! model (shared with the server).

use std::collections::{BTreeMap, BTreeSet};

use serde_json::Value;
use virtlab::lvm_board::{
    connect_error, lost_by_disk, prune, rel, Edge, Evaluation, FsStatus, Kind, Node, PoolStatus, PvStatus, Rel, Scenario, SnapStatus,
    Topology, VgStatus, VmStatus, VolStatus, MAX_NAME,
};

use crate::components::labs::board_view::{js_round, BoardConfig, Bounds, Point, View};


/// Identifier of the "ghost" palette object before it is placed on the board.
pub const GHOST: &str = "__new__";
/// Width and height of an object on the board (board units).
pub const NODE_W: f64 = virtlab::lvm_board::NODE_W;
pub const NODE_H: f64 = virtlab::lvm_board::NODE_H;
/// Window onto the board at zoom 1: width and the default height.
pub const BOARD_W: f64 = 860.0;
pub const BOARD_H: f64 = 520.0;
/// How far from the origin an object may be carried.
pub const WORLD: f64 = 2600.0;
/// Board pan and zoom: 30–300 %, integer pan.
pub const BOARD: BoardConfig = BoardConfig { items: Bounds::symmetric(WORLD), ..BoardConfig::DEFAULT };
/// Object shift (board units) below which a press stays a selection rather than a drag.
pub const MOVE_SLOP: f64 = 6.0;
/// Most characters of a name shown inside an object.
const SHOWN_NAME: usize = 13;

// --- exercise and draft ----------------------------------------------------------------------

/// Boards of the scenarios from a draft (JSON `{scenario id: board}`). Empty, corrupt, unknown or rule-breaking boards are
/// replaced by the starting board of the scenario.
pub fn restore(scenarios: &[Scenario], draft: &str) -> Vec<Topology> {
    let saved: BTreeMap<String, Value> = serde_json::from_str(draft).unwrap_or_default();
    scenarios
        .iter()
        .map(|sc| {
            saved
                .get(&sc.id)
                .and_then(|v| serde_json::from_value::<Topology>(v.clone()).ok())
                .filter(|t| virtlab::lvm_board::problems(t).is_empty())
                .unwrap_or_else(|| sc.start.clone())
        })
        .collect()
}

/// JSON of all boards: the draft in the cabinet (the solution of a scenario is the same board).
pub fn draft_json(boards: &[(String, Topology)]) -> String {
    let map: BTreeMap<&str, &Topology> = boards.iter().map(|(id, t)| (id.as_str(), t)).collect();
    serde_json::to_string(&map).unwrap_or_default()
}

// --- adding and removing -------------------------------------------------------------------------

/// The first free place of a new object in the column of its kind (the columns are the model's: the UI and the scenario builder share them).
pub fn next_pos(t: &Topology, kind: Kind) -> (f64, f64) {
    virtlab::lvm_board::next_pos(t, kind)
}

fn id_prefix(kind: Kind) -> &'static str {
    match kind {
        Kind::Disk => "disk",
        Kind::Pv => "pv",
        Kind::Vg => "vg",
        Kind::Lv => "lv",
        Kind::ThinPool => "pool",
        Kind::ThinLv => "thin",
        Kind::Snapshot => "snap",
        Kind::Fs => "fs",
        Kind::Vm => "vm",
    }
}

/// A free identifier: `<prefix><number>` (`disk1`, `lv2`).
pub fn new_id(t: &Topology, kind: Kind) -> String {
    let prefix = id_prefix(kind);
    (1..).map(|i| format!("{prefix}{i}")).find(|id| t.node(id).is_none()).unwrap_or_default()
}

/// A name with the lowest free running number: `lv-3`.
pub fn new_name(t: &Topology, kind: Kind) -> String {
    let base = id_prefix(kind);
    (1..).map(|i| format!("{base}-{i}")).find(|name| !t.nodes.iter().any(|n| n.name == *name)).unwrap_or_default()
}

/// Puts a new object on the board (at `at`, or in a free place of its column). Returns its identifier.
pub fn add_node(t: &mut Topology, kind: Kind, at: Option<Point>) -> String {
    let id = new_id(t, kind);
    let name = new_name(t, kind);
    let (x, y) = at.map_or_else(|| next_pos(t, kind), |p| (p.x, p.y));
    t.nodes.push(Node::new(&id, kind, &name, x, y));
    id
}


/// Removes an object with its links and the links that no longer make sense; returns how many dependent links were dropped.
pub fn remove_node(t: &mut Topology, id: &str) -> usize {
    t.nodes.retain(|n| n.id != id);
    t.edges.retain(|e| e.from != id && e.to != id);
    prune(t)
}

/// Removes one link and the links that depended on it; returns how many dependent links were dropped.
pub fn remove_edge(t: &mut Topology, edge: &Edge) -> usize {
    t.edges.retain(|e| e != edge);
    prune(t)
}

/// An object name no longer than the limit.
pub fn clamp_name(text: &str) -> String {
    text.chars().take(MAX_NAME).collect()
}

/// The name as shown inside an object: long ones are cut.
pub fn short_name(name: &str) -> String {
    if name.chars().count() <= SHOWN_NAME {
        name.to_owned()
    } else {
        format!("{}…", name.chars().take(SHOWN_NAME - 1).collect::<String>())
    }
}

// --- links ---------------------------------------------------------------------------------------

/// Whether objects of this kind take part in a relation as a target (an input pin).
pub fn has_in(kind: Kind) -> bool {
    Kind::ALL.iter().any(|k| rel(*k, kind).is_some())
}

/// Whether objects of this kind take part in a relation as a source (an output pin).
pub fn has_out(kind: Kind) -> bool {
    Kind::ALL.iter().any(|k| rel(kind, *k).is_some())
}

/// The link between two objects with the direction the model needs (`None`: no relation in either direction).
pub fn normalize_link(t: &Topology, a: &str, b: &str) -> Option<(String, String)> {
    let (na, nb) = (t.node(a)?, t.node(b)?);
    if rel(na.kind, nb.kind).is_some() {
        Some((a.to_owned(), b.to_owned()))
    } else if rel(nb.kind, na.kind).is_some() {
        Some((b.to_owned(), a.to_owned()))
    } else {
        None
    }
}

/// The link `from → to` that joining `a` and `b` would add, or the reason why it cannot be added.
pub fn link_check(t: &Topology, a: &str, b: &str) -> Result<(String, String), String> {
    match normalize_link(t, a, b) {
        Some((from, to)) => match connect_error(t, &from, &to) {
            Some(e) => Err(e),
            None => Ok((from, to)),
        },
        None => Err(connect_error(t, a, b).unwrap_or_else(|| i18n::tr("in LVM these objects are not linked directly").to_owned())),
    }
}

/// Relation of a link.
pub fn edge_rel(t: &Topology, e: &Edge) -> Option<Rel> {
    rel(t.node(&e.from)?.kind, t.node(&e.to)?.kind)
}

// --- the board: pins, wires, fitting ------------------------------------------------------------------------

/// Where a wire is dragged from: an output pin or an input pin.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Pin {
    In,
    Out,
}

/// Wire dragged from a pin of object `id`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Pending {
    pub id: String,
    pub pin: Pin,
}

/// How the pins of an object look while a wire is being dragged.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PortState {
    Idle,
    Ok,
    Bad,
}

impl PortState {
    pub fn class(self) -> &'static str {
        match self {
            PortState::Idle => "",
            PortState::Ok => "ok",
            PortState::Bad => "bad",
        }
    }
}

/// Output pin of an object (right side).
pub fn out_pos(n: &Node) -> Point {
    Point::new(n.x + NODE_W / 2.0, n.y)
}

/// Input pin of an object (left side).
pub fn in_pos(n: &Node) -> Point {
    Point::new(n.x - NODE_W / 2.0, n.y)
}

/// Path of a wire from an output pin `a` to an input pin `b` and the point halfway along it (for a label). A link between objects of
/// one row that skips columns arches over the objects in between.
pub fn wire(a: Point, b: Point) -> (String, Point) {
    let dx = b.x - a.x;
    let lift = if dx > 190.0 && (b.y - a.y).abs() < 40.0 { 40.0 + 0.1 * dx } else { 0.0 };
    let k = (dx.abs() * 0.5).max(36.0);
    let (c1, c2) = (Point::new(a.x + k, a.y - lift), Point::new(b.x - k, b.y - lift));
    let mid = Point::new((a.x + 3.0 * c1.x + 3.0 * c2.x + b.x) / 8.0, (a.y + 3.0 * c1.y + 3.0 * c2.y + b.y) / 8.0);
    let f = |p: Point| format!("{:.1} {:.1}", p.x, p.y);
    (format!("M{} C{} {} {}", f(a), f(c1), f(c2), f(b)), mid)
}

/// Path and middle point of a link between two objects.
pub fn edge_geom(t: &Topology, e: &Edge) -> Option<(String, Point)> {
    Some(wire(out_pos(t.node(&e.from)?), in_pos(t.node(&e.to)?)))
}

/// A ghost object of the palette under the cursor.
pub fn ghost_node(kind: Kind, at: Point) -> Node {
    Node::new(GHOST, kind, kind.label(), js_round(at.x), js_round(at.y))
}

/// Object under point `p` (frame with a margin of 10): the nearest one, other than the one the wire is dragged from.
pub fn node_at(t: &Topology, from: &str, p: Point) -> Option<String> {
    let dist = |n: &Node| (p.x - n.x).hypot(p.y - n.y);
    t.nodes
        .iter()
        .filter(|n| n.id != from && (p.x - n.x).abs() <= NODE_W / 2.0 + 10.0 && (p.y - n.y).abs() <= NODE_H / 2.0 + 10.0)
        .min_by(|a, b| dist(a).total_cmp(&dist(b)))
        .map(|n| n.id.clone())
}

/// The link a wire from `pend` to object `other` would make.
pub fn pin_link(t: &Topology, pend: &Pending, other: &str) -> Result<(String, String), String> {
    link_check(t, &pend.id, other)
}

/// How the pins of object `node` look while a wire is dragged.
pub fn port_state(t: &Topology, pend: Option<&Pending>, node: &str) -> PortState {
    let Some(p) = pend else { return PortState::Idle };
    if node == p.id {
        return PortState::Idle;
    }
    if pin_link(t, p, node).is_ok() {
        PortState::Ok
    } else {
        PortState::Bad
    }
}

/// Highlight of the object under the end of the wire.
pub fn hover_class(t: &Topology, pend: Option<&Pending>, hover: &str) -> &'static str {
    match pend.map(|p| pin_link(t, p, hover)) {
        Some(Ok(_)) => "hover-ok",
        _ => "hover-bad",
    }
}

/// The wire being dragged now: path and tone ("ok" — can connect, "bad" — cannot, empty — the end is at the cursor). Over an object the wire
/// takes the direction the link would have.
pub fn pending_wire(t: &Topology, pend: &Pending, hover: Option<&str>, cursor: Option<Point>) -> Option<(String, &'static str)> {
    let own = t.node(&pend.id)?;
    let own_pin = match pend.pin {
        Pin::Out => out_pos(own),
        Pin::In => in_pos(own),
    };
    if let Some(h) = hover.and_then(|h| t.node(h)) {
        return Some(match pin_link(t, pend, &h.id) {
            Ok((from, to)) => {
                let (a, b) = (t.node(&from)?, t.node(&to)?);
                (wire(out_pos(a), in_pos(b)).0, "ok")
            }
            Err(_) => {
                let d = match pend.pin {
                    Pin::Out => wire(own_pin, in_pos(h)).0,
                    Pin::In => wire(out_pos(h), own_pin).0,
                };
                (d, "bad")
            }
        });
    }
    let end = cursor?;
    let d = match pend.pin {
        Pin::Out => wire(own_pin, end).0,
        Pin::In => wire(end, own_pin).0,
    };
    Some((d, ""))
}

/// Window height for the board: by the proportions of the element on screen, otherwise the default.
pub fn world_height(width_px: f64, height_px: f64) -> f64 {
    if width_px > 0.0 && height_px > 0.0 {
        BOARD_W * height_px / width_px
    } else {
        BOARD_H
    }
}

/// Pan and zoom that make the whole board visible in a window of height `world_h` with margins; an empty board — the initial view.
pub fn fit_view(nodes: &[Point], world_h: f64) -> View {
    if nodes.is_empty() {
        return BOARD.home_view();
    }
    let pad = 30.0;
    let fold = |f: fn(f64, f64) -> f64, init: f64, g: fn(&Point) -> f64| nodes.iter().map(g).fold(init, f);
    let min_x = fold(f64::min, f64::INFINITY, |p| p.x) - NODE_W / 2.0 - pad;
    let max_x = fold(f64::max, f64::NEG_INFINITY, |p| p.x) + NODE_W / 2.0 + pad;
    // links that skip a column arch above the row
    let min_y = fold(f64::min, f64::INFINITY, |p| p.y) - NODE_H / 2.0 - pad - 40.0;
    let max_y = fold(f64::max, f64::NEG_INFINITY, |p| p.y) + NODE_H / 2.0 + pad;
    let (bw, bh) = (max_x - min_x, max_y - min_y);
    let zoom = 1.6_f64.min(BOARD_W / bw).min(world_h / bh).max(BOARD.zoom_min);
    View { zoom, pan: Point::new(js_round(min_x + bw / 2.0 - BOARD_W / zoom / 2.0), js_round(min_y + bh / 2.0 - world_h / zoom / 2.0)) }
}

// --- statuses -------------------------------------------------------------------------------------

/// A status chip: the class (`ok`, `warn`, `bad` or empty) and the text.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Chip {
    pub class: &'static str,
    pub text: &'static str,
}

/// What the board shows on an object besides its name.
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub struct NodeInfo {
    pub chip: Option<Chip>,
    /// the text in the corner: size, free space, how full, the filesystem
    pub badge: String,
    /// the badge is a warning: a group without room, a pool or a snapshot that is nearly full
    pub warn: bool,
}

fn gib(n: u64) -> String {
    i18n::trf!("{0} GiB", n)
}

fn pv_chip(s: PvStatus) -> Chip {
    let class = match s {
        PvStatus::Ok => "ok",
        PvStatus::NoGroup => "warn",
        PvStatus::NoDisk => "bad",
    };
    Chip { class, text: s.name() }
}

fn vg_chip(s: VgStatus) -> Chip {
    let class = if s == VgStatus::Ok { "ok" } else { "warn" };
    Chip { class, text: s.name() }
}

fn vol_chip(s: VolStatus) -> Chip {
    let class = match s {
        VolStatus::Ok => "ok",
        VolStatus::NoGroup | VolStatus::NoPool => "warn",
        VolStatus::NoSpace | VolStatus::NeedsTwoPvs | VolStatus::PoolDown | VolStatus::PoolFull => "bad",
    };
    Chip { class, text: s.name() }
}

fn pool_chip(s: PoolStatus) -> Chip {
    let class = match s {
        PoolStatus::Ok => "ok",
        PoolStatus::Warn | PoolStatus::NoGroup => "warn",
        PoolStatus::Full | PoolStatus::NoSpace => "bad",
    };
    Chip { class, text: s.name() }
}

fn snap_chip(s: SnapStatus) -> Chip {
    let class = match s {
        SnapStatus::Valid => "ok",
        SnapStatus::Orphan => "warn",
        SnapStatus::Invalid | SnapStatus::NoSpace | SnapStatus::OriginDown | SnapStatus::PoolFull => "bad",
    };
    Chip { class, text: s.name() }
}

fn fs_chip(s: FsStatus) -> Chip {
    let class = match s {
        FsStatus::Ok => "ok",
        FsStatus::NotGrown | FsStatus::Detached => "warn",
        FsStatus::TooBig | FsStatus::VolumeDown => "bad",
    };
    Chip { class, text: s.name() }
}

fn vm_chip(s: VmStatus) -> Chip {
    let class = match s {
        VmStatus::Ok => "ok",
        VmStatus::NoDisk => "warn",
        VmStatus::Down => "bad",
    };
    Chip { class, text: s.name() }
}

/// Chip and badge of an object.
pub fn node_info(t: &Topology, ev: &Evaluation, id: &str) -> NodeInfo {
    let Some(n) = t.node(id) else { return NodeInfo::default() };
    let plain = NodeInfo::default();
    match n.kind {
        Kind::Disk => NodeInfo { badge: gib(n.size_gib()), ..plain },
        Kind::Pv => ev.pv(id).map_or(plain, |p| NodeInfo {
            chip: Some(pv_chip(p.status)),
            badge: if p.extents > 0 { format!("{}%", (u64::from(p.used) * 100).div_ceil(u64::from(p.extents))) } else { String::new() },
            warn: false,
        }),
        Kind::Vg => ev.vg(id).map_or(plain, |v| NodeInfo {
            chip: Some(vg_chip(v.status)),
            badge: i18n::trf!("{0} GiB free", v.free_gib()),
            warn: v.status != VgStatus::Ok,
        }),
        Kind::Lv => ev.volume(id).map_or(plain, |v| NodeInfo {
            chip: Some(vol_chip(v.status)),
            badge: if n.mirrored() { format!("{} · {}", gib(v.size_gib), i18n::tr("mirror")) } else { gib(v.size_gib) },
            warn: false,
        }),
        Kind::ThinLv => ev.volume(id).map_or(plain, |v| NodeInfo { chip: Some(vol_chip(v.status)), badge: gib(v.size_gib), warn: false }),
        Kind::ThinPool => ev.pool(id).map_or(plain, |p| NodeInfo {
            chip: Some(pool_chip(p.status)),
            badge: format!("{}% · {}%", p.data_pct, p.meta_pct),
            warn: p.status != PoolStatus::Ok,
        }),
        Kind::Snapshot => ev.snapshot(id).map_or(plain, |s| NodeInfo {
            chip: Some(snap_chip(s.status)),
            badge: if s.thin { i18n::tr("thin").to_owned() } else { format!("{}%", s.pct) },
            warn: !s.thin && s.pct >= 80,
        }),
        Kind::Fs => ev.fs(id).map_or(plain, |f| NodeInfo {
            chip: Some(fs_chip(f.status)),
            badge: format!("{} · {}", n.param_text("type"), gib(f.fs_gib)),
            warn: false,
        }),
        Kind::Vm => ev.vm(id).map_or(plain, |v| NodeInfo { chip: Some(vm_chip(v.status)), ..NodeInfo::default() }),
    }
}

/// Class of the object frame by its status.
pub fn status_class(info: &NodeInfo) -> &'static str {
    match info.chip {
        Some(c) if !c.class.is_empty() => c.class,
        _ => "idle",
    }
}

fn about(kind: Kind) -> &'static str {
    match kind {
        Kind::Disk => i18n::tr("A disk is a block device: it gives LVM nothing until it becomes a physical volume."),
        Kind::Pv => i18n::tr("A physical volume is a disk prepared for LVM (pvcreate): it gives its extents to a volume group."),
        Kind::Vg => i18n::tr("A volume group is the pool of the extents of its physical volumes; volumes are carved from it."),
        Kind::Lv => i18n::tr("A logical volume is carved from a volume group and takes whole extents."),
        Kind::ThinPool => i18n::tr("A thin pool takes its space from the group and lends it to thin volumes that may promise more than it has."),
        Kind::ThinLv => i18n::tr("A thin volume has a virtual size and takes space from its pool only when data is written."),
        Kind::Snapshot => i18n::tr("A snapshot keeps the state of a volume; a classic one stores the changes in its own space and is lost when that space runs out."),
        Kind::Fs => i18n::tr("A filesystem sits on a volume; after the volume grows, the filesystem must grow too (lvextend -r does both)."),
        Kind::Vm => i18n::tr("A VM uses volumes as its disks (an oVirt block storage domain is a volume group with one volume per disk)."),
    }
}

/// The derived state of an object for the inspector: a chip and the sentences that explain it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Explain {
    pub info: NodeInfo,
    pub lines: Vec<String>,
}

fn name_of(t: &Topology, id: &str) -> String {
    t.node(id).map(|n| n.name.clone()).unwrap_or_default()
}

fn names(t: &Topology, ids: &[String]) -> String {
    ids.iter().map(|id| name_of(t, id)).collect::<Vec<_>>().join(", ")
}

/// Everything the inspector says about an object besides its name and parameters.
pub fn explain(t: &Topology, ev: &Evaluation, id: &str) -> Explain {
    let info = node_info(t, ev, id);
    let Some(n) = t.node(id) else { return Explain { info, lines: vec![] } };
    let mut lines = vec![about(n.kind).to_owned()];
    match n.kind {
        Kind::Disk => lines.push(match ev.pvs.iter().find(|p| p.disk.as_deref() == Some(id)) {
            Some(p) => i18n::trf!("Used as the physical volume “{0}”.", name_of(t, &p.id)),
            None => i18n::tr("Not used by LVM yet: make a physical volume of it.").to_owned(),
        }),
        Kind::Pv => {
            if let Some(p) = ev.pv(id) {
                lines.extend(p.why.iter().map(|w| w.text()));
                lines.push(i18n::trf!("Extents: {0} used of {1}.", p.used, p.extents));
                if let Some(vg) = &p.vg {
                    lines.push(i18n::trf!("Member of the volume group “{0}”.", name_of(t, vg)));
                }
            }
        }
        Kind::Vg => {
            if let Some(v) = ev.vg(id) {
                lines.push(i18n::trf!("Extent size {0} MiB: {1} of {2} extents are taken, {3} GiB free.", v.pe_mib, v.used, v.total, v.free_gib()));
                if !v.pvs.is_empty() {
                    lines.push(i18n::trf!("Physical volumes: {0}.", names(t, &v.pvs)));
                }
            }
        }
        Kind::Lv | Kind::ThinLv => {
            if let Some(v) = ev.volume(id) {
                lines.extend(v.why.iter().map(|w| w.text()));
                lines.push(if n.kind == Kind::Lv {
                    i18n::trf!("Takes {0} extents ({1} GiB) of the group.", v.extents, v.size_gib)
                } else {
                    i18n::trf!("Virtual size {0} GiB: space is taken from the pool when data is written.", v.size_gib)
                });
            }
            if n.mirrored() {
                lines.push(i18n::tr("Two copies of the data on different physical volumes.").to_owned());
            }
            if let Some(pieces) = ev.placement.get(id) {
                let mut pvs: Vec<String> = pieces.iter().map(|p| p.pv.clone()).collect();
                pvs.dedup();
                let pvs: BTreeSet<String> = pvs.into_iter().collect();
                lines.push(i18n::trf!("Lies on: {0}.", names(t, &pvs.into_iter().collect::<Vec<_>>())));
            }
        }
        Kind::ThinPool => {
            if let Some(p) = ev.pool(id) {
                lines.extend(p.why.iter().map(|w| w.text()));
                lines.push(i18n::trf!("Data {0}% used ({1} of {2} GiB), metadata {3}% used.", p.data_pct, p.used_gib, p.data_gib, p.meta_pct));
                lines.push(i18n::trf!("The thin volumes promise {0} GiB, {1}% of the data space.", p.virtual_gib, p.overprovision_pct()));
                if p.extended > 0 {
                    lines.push(i18n::trf!("Autoextend added {0} extents.", p.extended));
                }
            }
        }
        Kind::Snapshot => {
            if let Some(s) = ev.snapshot(id) {
                lines.extend(s.why.iter().map(|w| w.text()));
                lines.push(if s.thin {
                    i18n::tr("A thin snapshot shares the space of its pool.").to_owned()
                } else {
                    i18n::trf!("{0} GiB changed in the origin; the snapshot holds {1} GiB ({2}% used).", s.changed_gib, s.holds_gib, s.pct)
                });
            }
        }
        Kind::Fs => {
            if let Some(f) = ev.fs(id) {
                lines.extend(f.why.iter().map(|w| w.text()));
                lines.push(i18n::trf!("Filesystem of {0} GiB on a volume of {1} GiB.", f.fs_gib, f.volume_gib));
            }
        }
        Kind::Vm => {
            if let Some(v) = ev.vm(id) {
                lines.extend(v.why.iter().map(|w| w.text()));
                lines.push(if v.volumes.is_empty() { i18n::tr("No disks yet.").to_owned() } else { i18n::trf!("Disks: {0}.", names(t, &v.volumes)) });
            }
        }
    }
    Explain { info, lines }
}

/// Tooltip of an object.
pub fn describe_node(n: &Node, info: &NodeInfo) -> String {
    match info.chip {
        Some(c) => format!("{} ({}) — {}", n.name, n.kind.label(), c.text),
        None => format!("{} ({})", n.name, n.kind.label()),
    }
}

// --- the tree of disks and volumes -------------------------------------------------------------------------

/// A row of the tree.
#[derive(Clone, Debug, PartialEq)]
pub enum TreeItem {
    /// A heading over objects that are not in a group yet.
    Heading(&'static str),
    /// An object at a depth.
    Node { depth: usize, id: String, kind: Kind, name: String, info: NodeInfo },
}

struct TreeBuilder<'a> {
    t: &'a Topology,
    ev: &'a Evaluation,
    out: Vec<TreeItem>,
    seen: BTreeSet<String>,
}

impl TreeBuilder<'_> {
    fn node(&mut self, depth: usize, n: &Node) {
        if self.seen.insert(n.id.clone()) {
            self.out.push(TreeItem::Node { depth, id: n.id.clone(), kind: n.kind, name: n.name.clone(), info: node_info(self.t, self.ev, &n.id) });
        }
    }

    /// A volume with what stands on it: snapshots, the filesystem, the VM that uses it.
    fn volume(&mut self, depth: usize, v: &Node) {
        let t = self.t;
        self.node(depth, v);
        for r in [Rel::SnapshotOf, Rel::Holds, Rel::VmDisk] {
            for x in t.targets(&v.id, r) {
                self.node(depth + 1, x);
            }
        }
    }

    fn group(&mut self, vg: &Node) {
        let t = self.t;
        self.node(0, vg);
        for pv in t.sources(&vg.id, Rel::Member) {
            self.node(1, pv);
            for d in t.sources(&pv.id, Rel::Backs) {
                self.node(2, d);
            }
        }
        for lv in t.targets(&vg.id, Rel::Carves) {
            self.volume(1, lv);
        }
        for pool in t.targets(&vg.id, Rel::Pool) {
            self.node(1, pool);
            for thin in t.targets(&pool.id, Rel::Thin) {
                self.volume(2, thin);
            }
        }
    }
}

/// The tree derived from the links: volume group › physical volumes (with their disks), volumes (with snapshots, filesystems and VMs), thin pools
/// (with their thin volumes); objects that are in no group yet are listed at the end.
pub fn tree(t: &Topology, ev: &Evaluation) -> Vec<TreeItem> {
    let mut b = TreeBuilder { t, ev, out: vec![], seen: BTreeSet::new() };
    for vg in t.of_kind(Kind::Vg) {
        b.group(vg);
    }
    let loose: Vec<&Node> = t.nodes.iter().filter(|n| !b.seen.contains(&n.id)).collect();
    if !loose.is_empty() {
        b.out.push(TreeItem::Heading(i18n::tr("Not in a volume group yet")));
        for n in loose {
            b.node(1, n);
        }
    }
    b.out
}

// --- if a disk fails -----------------------------------------------------------------------------------------

/// One line of the "if a disk fails" report.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct LossLine {
    pub ok: bool,
    pub text: String,
}

/// What the loss of a disk takes with it.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Loss {
    /// identifiers of the objects that are lost
    pub lost: BTreeSet<String>,
    pub lines: Vec<LossLine>,
}

/// The report for the loss of `disk`: the volumes, pools and snapshots that are gone, and those that survive on a copy elsewhere.
pub fn loss(t: &Topology, ev: &Evaluation, disk: &str) -> Loss {
    let lost: Vec<String> = lost_by_disk(t, ev, disk);
    let lost_set: BTreeSet<String> = lost.iter().cloned().collect();
    let on_disk: BTreeSet<&str> = ev.pvs.iter().filter(|p| p.disk.as_deref() == Some(disk)).map(|p| p.id.as_str()).collect();
    let mut lines: Vec<LossLine> = lost
        .iter()
        .filter_map(|id| t.node(id))
        .map(|n| LossLine { ok: false, text: i18n::trf!("“{0}” ({1}) is lost.", n.name, n.kind.label()) })
        .collect();
    for n in &t.nodes {
        let touched = ev.placement.get(&n.id).is_some_and(|ps| ps.iter().any(|p| on_disk.contains(p.pv.as_str())));
        if touched && !lost_set.contains(&n.id) {
            lines.push(LossLine { ok: true, text: i18n::trf!("“{0}” ({1}) survives on its other copy.", n.name, n.kind.label()) });
        }
    }
    if lines.is_empty() {
        lines.push(LossLine { ok: true, text: i18n::tr("The disk holds no data: nothing is lost.").to_owned() });
    }
    Loss { lost: lost_set, lines }
}

/// The disks of the board: identifier and name.
pub fn disks(t: &Topology) -> Vec<(String, String)> {
    t.of_kind(Kind::Disk).map(|d| (d.id.clone(), d.name.clone())).collect()
}

// --- the summary -------------------------------------------------------------------------------------------------

/// The sentences of the summary card: the groups, the pools and the snapshots with their numbers.
pub fn summary(t: &Topology, ev: &Evaluation) -> Vec<String> {
    let mut out = vec![];
    for v in &ev.vgs {
        out.push(i18n::trf!("“{0}”: {1} GiB free of {2} GiB, extent {3} MiB.", name_of(t, &v.id), v.free_gib(), v.total_gib(), v.pe_mib));
    }
    for p in &ev.pools {
        out.push(i18n::trf!(
            "“{0}”: data {1}%, metadata {2}%, {3} GiB promised over {4} GiB.",
            name_of(t, &p.id),
            p.data_pct,
            p.meta_pct,
            p.virtual_gib,
            p.data_gib
        ));
    }
    for s in ev.snapshots.iter().filter(|s| !s.thin) {
        out.push(i18n::trf!("“{0}”: {1}% of its space used by the changes.", name_of(t, &s.id), s.pct));
    }
    out
}

#[cfg(test)]
mod tests {
    use virtlab::lvm_board::{evaluate as evaluated, pack, problems, Param, Workload};

    use super::*;

    fn ru() -> i18n::LocaleGuard {
        locales::guard(i18n::Locale::Ru)
    }

    fn en() -> i18n::LocaleGuard {
        locales::guard(i18n::Locale::En)
    }

    fn scenarios(pack_id: &str) -> Vec<Scenario> {
        pack(pack_id).map(|p| p.0).unwrap_or_default()
    }

    fn solution(pack_id: &str, scenario: &str) -> Topology {
        pack(pack_id).and_then(|mut p| p.1.remove(scenario)).unwrap_or_default()
    }

    #[test]
    fn draft_round_trips_every_board() {
        let _ru = ru();
        let sc = scenarios("virt-sim-lvm-grow");
        let mut boards = restore(&sc, "");
        for (b, s) in boards.iter().zip(&sc) {
            assert_eq!(*b, s.start, "{}", s.id);
        }
        let id = add_node(&mut boards[0], Kind::Disk, None);
        let text = draft_json(&sc.iter().zip(&boards).map(|(s, b)| (s.id.clone(), b.clone())).collect::<Vec<_>>());
        let back = restore(&sc, &text);
        assert_eq!(back, boards);
        assert!(back[0].node(&id).is_some());
    }

    #[test]
    fn restore_tolerates_garbage_and_unknown_ids() {
        let _ru = ru();
        let sc = scenarios("virt-sim-lvm-grow");
        let starts: Vec<Topology> = sc.iter().map(|s| s.start.clone()).collect();
        let first = sc[0].id.clone();
        for draft in ["", "null", "[]", "42", "not json", "{", r#"{"nope": {"nodes": [], "edges": []}}"#] {
            assert_eq!(restore(&sc, draft), starts, "{draft:?}");
        }
        let broken = format!(r#"{{"{first}": {{"nodes": 1}}}}"#);
        assert_eq!(restore(&sc, &broken), starts);
        // a known id next to an unknown one: the known board is restored, the others start over
        let mut t = Topology::default();
        add_node(&mut t, Kind::Disk, None);
        let text = format!(r#"{{"{first}": {}, "other": {{"nodes": [], "edges": []}}}}"#, serde_json::to_string(&t).unwrap_or_default());
        let back = restore(&sc, &text);
        assert_eq!(back[0], t);
        assert_eq!(back[1], starts[1]);
    }

    #[test]
    fn restore_drops_boards_that_break_the_rules() {
        let _ru = ru();
        let sc = scenarios("virt-sim-lvm-grow");
        let mut t = Topology::default();
        add_node(&mut t, Kind::Disk, None);
        t.edges.push(Edge::new("disk1", "nobody"));
        let text = draft_json(&[(sc[0].id.clone(), t)]);
        assert_eq!(restore(&sc, &text)[0], sc[0].start);
        // the reference boards are fine
        let all: Vec<(String, Topology)> = pack("virt-sim-lvm-grow").map(|p| p.1.into_iter().collect()).unwrap_or_default();
        let back = restore(&sc, &draft_json(&all));
        for (s, b) in sc.iter().zip(&back) {
            assert!(s.reached(b), "{}", s.id);
        }
    }

    #[test]
    fn new_objects_get_free_places_ids_and_names() {
        let _en = en();
        let mut t = Topology::default();
        let a = add_node(&mut t, Kind::Disk, None);
        let b = add_node(&mut t, Kind::Disk, None);
        assert_eq!((a.as_str(), b.as_str()), ("disk1", "disk2"));
        assert_eq!(t.nodes[0].name, "disk-1");
        assert_ne!((t.nodes[0].x, t.nodes[0].y), (t.nodes[1].x, t.nodes[1].y));
        let c = add_node(&mut t, Kind::Lv, Some(Point::new(5.0, 6.0)));
        assert_eq!(t.node(&c).map(|n| (n.x, n.y)), Some((5.0, 6.0)));
        // every kind lands somewhere and nothing lands on top of anything else
        let mut all = Topology::default();
        for k in Kind::ALL.into_iter().chain([Kind::Lv, Kind::Disk]) {
            add_node(&mut all, k, None);
        }
        for (i, a) in all.nodes.iter().enumerate() {
            for b in &all.nodes[i + 1..] {
                assert!((a.x - b.x).abs() >= NODE_W || (a.y - b.y).abs() >= NODE_H, "{} and {} overlap", a.id, b.id);
            }
        }
        assert!(problems(&all).is_empty());
        // the new objects keep their defaults unset, so the draft stays small
        assert!(all.nodes.iter().all(|n| n.params.is_empty()));
        // removing frees a name
        remove_node(&mut all, "disk1");
        assert_eq!(new_id(&all, Kind::Disk), "disk1");
    }

    #[test]
    fn the_inspector_keeps_the_field_order_the_e2e_relies_on() {
        let _en = en();
        use virtlab::lvm_board::{param_specs, ParamTy};
        let keys = |k: Kind| param_specs(k).into_iter().map(|s| s.key).collect::<Vec<_>>();
        assert_eq!(keys(Kind::Disk), ["size"]);
        assert_eq!(keys(Kind::Vg), ["pe"]);
        assert_eq!(keys(Kind::Lv), ["size", "mirror"]);
        assert_eq!(keys(Kind::Fs), ["type", "size"]);
        assert_eq!(keys(Kind::ThinPool), ["size", "meta", "autoextend"]);
        assert!(matches!(param_specs(Kind::ThinPool)[2].ty, ParamTy::Bool));
        assert!(keys(Kind::Pv).is_empty() && keys(Kind::Vm).is_empty());
    }

    #[test]
    fn links_are_normalised_to_the_direction_of_the_model() {
        let _ru = ru();
        let t = solution("virt-sim-lvm-grow", "build");
        assert_eq!(normalize_link(&t, "vg", "data"), Some(("vg".to_owned(), "data".to_owned())));
        assert_eq!(normalize_link(&t, "data", "vg"), Some(("vg".to_owned(), "data".to_owned())));
        assert_eq!(normalize_link(&t, "d1", "d2"), None);
        assert_eq!(normalize_link(&t, "d1", "nobody"), None);
        // refusals carry the model's reason
        assert!(link_check(&t, "pv1", "vg").is_err(), "the physical volume is already in the group");
        assert!(link_check(&t, "d1", "d2").is_err());
        // a new volume joins the group from the volume side as well
        let mut t = t;
        let lv = add_node(&mut t, Kind::Lv, None);
        assert_eq!(link_check(&t, &lv, "vg"), Ok(("vg".to_owned(), lv.clone())));
        // pins: who has an input and who has an output
        assert!(has_out(Kind::Disk) && !has_in(Kind::Disk));
        assert!(has_in(Kind::Vm) && !has_out(Kind::Vm));
        assert!(has_in(Kind::Snapshot) && !has_out(Kind::Snapshot));
        for k in [Kind::Pv, Kind::Vg, Kind::Lv, Kind::ThinPool, Kind::ThinLv] {
            assert!(has_in(k) && has_out(k), "{k:?}");
        }
    }

    #[test]
    fn a_wire_follows_the_link_it_would_make() {
        let _ru = ru();
        let t = solution("virt-sim-lvm-grow", "build");
        let from_pv = Pending { id: "pv1".into(), pin: Pin::In };
        // dragging from the input of a physical volume over a volume is refused
        assert_eq!(port_state(&t, Some(&from_pv), "data"), PortState::Bad);
        assert_eq!(port_state(&t, Some(&from_pv), "pv1"), PortState::Idle);
        assert_eq!(port_state(&t, None, "data"), PortState::Idle);
        let (d, tone) = pending_wire(&t, &from_pv, Some("data"), None).expect("wire");
        assert_eq!(tone, "bad");
        assert!(d.starts_with('M'));
        assert_eq!(pending_wire(&t, &from_pv, None, Some(Point::new(1.0, 2.0))).map(|w| w.1), Some(""));
        assert_eq!(pending_wire(&t, &from_pv, None, None), None);
    }

    #[test]
    fn deleting_reports_the_dependent_links() {
        let _ru = ru();
        let mut t = solution("virt-sim-lvm-grow", "build");
        let before = t.edges.len();
        // the volume goes with its link to the group and its filesystem's link
        let dropped = remove_node(&mut t, "data");
        assert!(t.node("data").is_none() && t.edges.iter().all(|e| e.from != "data" && e.to != "data"));
        assert!(t.edges.len() < before);
        assert!(problems(&t).is_empty());
        let _ = dropped;
        // a link that depended on another one goes with it
        let mut t = solution("virt-sim-lvm-grow", "build");
        let n = remove_edge(&mut t, &Edge::new("d1", "pv1"));
        assert!(problems(&t).is_empty());
        assert!(n <= t.edges.len());
    }

    #[test]
    fn long_links_arch_and_short_ones_do_not() {
        let _ru = ru();
        let (flat, mid) = wire(Point::new(0.0, 100.0), Point::new(100.0, 100.0));
        assert!(flat.starts_with("M0.0 100.0 C"));
        assert_eq!(mid.y, 100.0);
        let (_, arch) = wire(Point::new(0.0, 100.0), Point::new(240.0, 100.0));
        assert!(arch.y < 100.0 - 28.0, "{}", arch.y);
        let (_, diagonal) = wire(Point::new(0.0, 100.0), Point::new(240.0, 300.0));
        assert!(diagonal.y > 100.0 && diagonal.y < 300.0);
    }

    #[test]
    fn fit_shows_every_object() {
        let _ru = ru();
        assert_eq!(fit_view(&[], 520.0), BOARD.home_view());
        for sc in scenarios("virt-sim-lvm-resilience").iter().chain(scenarios("virt-sim-lvm-snapshots").iter()) {
            let pts: Vec<Point> = sc.start.nodes.iter().map(|n| Point::new(n.x, n.y)).collect();
            let v = fit_view(&pts, 520.0);
            assert!(v.zoom >= BOARD.zoom_min && v.zoom <= 1.6, "{}", sc.id);
            for p in &pts {
                let (x, y) = ((p.x - v.pan.x) * v.zoom, (p.y - v.pan.y) * v.zoom);
                assert!(x > 0.0 && x < BOARD_W && y > 0.0 && y < 520.0, "{}: {p:?} -> {x} {y}", sc.id);
            }
        }
        assert_eq!(world_height(0.0, 0.0), BOARD_H);
        assert_eq!(world_height(860.0, 430.0), 430.0);
    }

    #[test]
    fn statuses_and_badges_come_from_the_evaluation() {
        let _en = en();
        let t = solution("virt-sim-lvm-grow", "build");
        let ev = evaluated(&t, &Workload::default());
        let info = |id: &str| node_info(&t, &ev, id);
        assert_eq!(info("d1").chip, None);
        assert_eq!(info("d1").badge, "50 GiB");
        assert_eq!(info("pv1").chip.map(|c| c.class), Some("ok"));
        assert_eq!(info("vg").chip.map(|c| c.class), Some("ok"));
        assert!(info("vg").badge.ends_with("GiB free"), "{}", info("vg").badge);
        assert_eq!(info("data").chip, Some(Chip { class: "ok", text: "active" }));
        assert_eq!(info("data").badge, "50 GiB");
        assert_eq!(info("fs").badge, "ext4 · 50 GiB");
        assert_eq!(status_class(&info("data")), "ok");
        assert_eq!(status_class(&info("d1")), "idle");
        // a group without room, a volume that does not fit
        let mut big = t.clone();
        if let Some(n) = big.nodes.iter_mut().find(|n| n.id == "data") {
            n.params.insert("size".into(), Param::Str("200".into()));
        }
        let ev = evaluated(&big, &Workload::default());
        assert_eq!(node_info(&big, &ev, "data").chip, Some(Chip { class: "bad", text: "no space" }));
        // every object kind of every scenario explains itself
        for pack_id in ["virt-sim-lvm-grow", "virt-sim-lvm-resilience", "virt-sim-lvm-snapshots"] {
            for sc in scenarios(pack_id) {
                let ev = sc.evaluate(&sc.start);
                for n in &sc.start.nodes {
                    assert!(explain(&sc.start, &ev, &n.id).lines.len() >= 2 || n.kind == Kind::Pv, "{}: {}", sc.id, n.id);
                }
            }
        }
    }

    #[test]
    fn the_inspector_explains_the_reasons() {
        let _en = en();
        let sc = scenarios("virt-sim-lvm-grow").into_iter().find(|s| s.id == "extend").unwrap_or_else(|| panic!("extend"));
        // the volume grew and the filesystem did not
        let mut t = sc.start.clone();
        if let Some(n) = t.nodes.iter_mut().find(|n| n.id == "data") {
            n.params.insert("size".into(), Param::Str("50".into()));
        }
        let ev = sc.evaluate(&t);
        let fs = explain(&t, &ev, "fs-data");
        assert_eq!(fs.info.chip.map(|c| c.text), Some("not grown"));
        assert!(fs.lines.iter().any(|l| l.contains("grow the filesystem")), "{:?}", fs.lines);
        let vg = explain(&t, &ev, "vg");
        assert!(vg.lines.iter().any(|l| l.contains("extents are taken")), "{:?}", vg.lines);
        assert!(explain(&t, &ev, "nobody").lines.is_empty());
    }

    #[test]
    fn the_tree_follows_the_links_and_lists_the_rest() {
        let _en = en();
        let t = solution("virt-sim-lvm-grow", "build");
        let ev = evaluated(&t, &Workload::default());
        let rows = tree(&t, &ev);
        let depth_of = |id: &str| {
            rows.iter().find_map(|r| match r {
                TreeItem::Node { depth, id: i, .. } if i == id => Some(*depth),
                _ => None,
            })
        };
        assert_eq!(depth_of("vg"), Some(0));
        assert_eq!(depth_of("pv1"), Some(1));
        assert_eq!(depth_of("d1"), Some(2));
        assert_eq!(depth_of("data"), Some(1));
        assert_eq!(depth_of("fs"), Some(2));
        assert!(!rows.iter().any(|r| matches!(r, TreeItem::Heading(_))));
        assert_eq!(rows.len(), t.nodes.len(), "each object once");
        // a half-built board: loose objects come last under a heading
        let mut half = Topology::default();
        add_node(&mut half, Kind::Disk, None);
        add_node(&mut half, Kind::Vg, None);
        let rows = tree(&half, &evaluated(&half, &Workload::default()));
        assert!(matches!(rows[0], TreeItem::Node { depth: 0, kind: Kind::Vg, .. }));
        assert!(matches!(rows[1], TreeItem::Heading(_)));
        assert!(matches!(rows[2], TreeItem::Node { depth: 1, kind: Kind::Disk, .. }));
    }

    #[test]
    fn the_loss_of_a_disk_lists_what_goes_and_what_survives() {
        let _en = en();
        // a mirror survives the loss of either disk; a linear volume does not
        let sc = scenarios("virt-sim-lvm-resilience").into_iter().find(|s| s.id == "mirror").unwrap_or_else(|| panic!("mirror"));
        let reference = solution("virt-sim-lvm-resilience", "mirror");
        let ev = sc.evaluate(&reference);
        for d in reference.of_kind(Kind::Disk) {
            let l = loss(&reference, &ev, &d.id);
            assert!(l.lost.is_empty(), "{}: {:?}", d.id, l.lines);
            assert!(l.lines.iter().all(|x| x.ok));
        }
        let start_ev = sc.evaluate(&sc.start);
        let broken = sc.start.of_kind(Kind::Disk).map(|d| loss(&sc.start, &start_ev, &d.id)).collect::<Vec<_>>();
        assert!(broken.iter().any(|l| !l.lost.is_empty()), "{broken:?}");
        for l in &broken {
            assert!(!l.lines.is_empty());
        }
        // a disk that holds nothing
        let mut t = Topology::default();
        add_node(&mut t, Kind::Disk, None);
        let ev = evaluated(&t, &Workload::default());
        let l = loss(&t, &ev, "disk1");
        assert!(l.lost.is_empty());
        assert_eq!(l.lines, [LossLine { ok: true, text: "The disk holds no data: nothing is lost.".to_owned() }]);
        assert_eq!(disks(&t), [("disk1".to_owned(), "disk-1".to_owned())]);
    }

    #[test]
    fn the_summary_names_the_groups_pools_and_snapshots() {
        let _en = en();
        let sc = scenarios("virt-sim-lvm-snapshots").into_iter().find(|s| s.id == "thin-grow").unwrap_or_else(|| panic!("thin-grow"));
        let ev = sc.evaluate(&sc.start);
        let lines = summary(&sc.start, &ev);
        assert!(lines.iter().any(|l| l.contains("GiB free of")), "{lines:?}");
        assert!(lines.iter().any(|l| l.contains("metadata")), "{lines:?}");
        let cow = scenarios("virt-sim-lvm-snapshots").into_iter().find(|s| s.id == "cow-size").unwrap_or_else(|| panic!("cow-size"));
        let lines = summary(&cow.start, &cow.evaluate(&cow.start));
        assert!(lines.iter().any(|l| l.contains("used by the changes")) || cow.start.of_kind(Kind::Snapshot).next().is_none(), "{lines:?}");
    }

    #[test]
    fn names_are_cut_for_the_board_and_limited_for_the_model() {
        let _ru = ru();
        assert_eq!(short_name("lv-1"), "lv-1");
        assert_eq!(short_name("a-very-long-host-name"), "a-very-long-…");
        assert_eq!(short_name("a-very-long-host-name").chars().count(), 13);
        assert_eq!(clamp_name(&"x".repeat(100)).chars().count(), MAX_NAME);
        assert_eq!(clamp_name("héllo"), "héllo");
    }

    #[test]
    fn nodes_under_the_cursor_exclude_the_origin() {
        let _ru = ru();
        let t = solution("virt-sim-lvm-grow", "build");
        let vg = t.node("vg").cloned().unwrap_or_else(|| Node::new("", Kind::Disk, "", 0.0, 0.0));
        assert_eq!(node_at(&t, "pv1", Point::new(vg.x + 5.0, vg.y)).as_deref(), Some("vg"));
        assert_eq!(node_at(&t, "vg", Point::new(vg.x + 5.0, vg.y)), None);
        assert_eq!(node_at(&t, "pv1", Point::new(-500.0, -500.0)), None);
    }
}
