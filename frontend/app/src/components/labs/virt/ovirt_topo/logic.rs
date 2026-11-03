//! Pure logic of the oVirt topology board: the draft, adding and removing objects, links and their direction, wires on the board,
//! fitting, statuses of objects, the hierarchy tree and the highlighted message path. No signals or DOM — everything is checked by ordinary
//! tests; the interface (`board.rs`, `panels.rs`, `lab.rs`) only calls these functions, and takes the rules, statuses and paths from the
//! `virtlab::ovirt_topo` model (shared with the server).

use std::collections::{BTreeMap, BTreeSet};

use serde_json::Value;
use virtlab::ovirt_topo::{
    affinity_breaks, connect_error, fence_agent, host_load, prune, rel, DcStatus, DomainStatus, Edge, Evaluation, HostStatus, Kind, Node, Op, Polarity, Rel,
    Role, Scenario, Topology, Trace, VmStatus, MAX_NAME,
};

use crate::components::labs::board_view::{js_round, BoardConfig, Bounds, Point, View};

/// Identifier of the "ghost" palette object before it is placed on the board.
pub const GHOST: &str = "__new__";
/// Width and height of an object on the board (board units).
pub const NODE_W: f64 = virtlab::ovirt_topo::NODE_W;
pub const NODE_H: f64 = virtlab::ovirt_topo::NODE_H;
/// Window onto the board at zoom 1: width and the default height.
pub const BOARD_W: f64 = 860.0;
pub const BOARD_H: f64 = 520.0;
/// How far from the origin an object may be carried.
pub const WORLD: f64 = 2600.0;
/// Board pan and zoom: 30–300 %, integer pan.
pub const BOARD: BoardConfig = BoardConfig { items: Bounds::symmetric(WORLD), ..BoardConfig::DEFAULT };
/// Object shift (board units) below which a press stays a selection rather than a drag.
pub const MOVE_SLOP: f64 = 6.0;
/// Pause between the hops of an animated path (ms).
pub const HOP_MS: u32 = 700;
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
                .filter(|t| virtlab::ovirt_topo::problems(t).is_empty())
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
    virtlab::ovirt_topo::next_pos(t, kind)
}

fn id_prefix(kind: Kind) -> &'static str {
    match kind {
        Kind::Engine => "engine",
        Kind::DataCenter => "dc",
        Kind::Cluster => "cl",
        Kind::Host => "h",
        Kind::Network => "net",
        Kind::StorageDomain => "dom",
        Kind::Vm => "vm",
        Kind::FenceAgent => "fence-",
        Kind::AffinityGroup => "group-",
        Kind::Backup => "backup-",
        Kind::User => "user-",
        Kind::Permission => "perm-",
    }
}

fn name_base(kind: Kind) -> &'static str {
    match kind {
        Kind::Engine => "engine",
        Kind::DataCenter => "dc",
        Kind::Cluster => "cluster",
        Kind::Host => "host",
        Kind::Network => "net",
        Kind::StorageDomain => "domain",
        Kind::Vm => "vm",
        Kind::FenceAgent => "fence",
        Kind::AffinityGroup => "group",
        Kind::Backup => "backup",
        Kind::User => "user",
        Kind::Permission => "perm",
    }
}

/// A free identifier: `<prefix><number>` (`h1`, `fence-1`), the engine is just `engine` while it is free.
pub fn new_id(t: &Topology, kind: Kind) -> String {
    let prefix = id_prefix(kind);
    if kind == Kind::Engine && t.node(prefix).is_none() {
        return prefix.to_owned();
    }
    (1..).map(|i| format!("{prefix}{i}")).find(|id| t.node(id).is_none()).unwrap_or_default()
}

/// A name with the lowest free running number: `host-3`.
pub fn new_name(t: &Topology, kind: Kind) -> String {
    let base = name_base(kind);
    if kind == Kind::Engine && !t.nodes.iter().any(|n| n.name == base) {
        return base.to_owned();
    }
    (1..).map(|i| format!("{base}-{i}")).find(|name| !t.nodes.iter().any(|n| n.name == *name)).unwrap_or_default()
}

/// Puts a new object on the board (at `at`, or in a free place of its column). Returns its identifier.
pub fn add_node(t: &mut Topology, kind: Kind, at: Option<Point>) -> String {
    let id = new_id(t, kind);
    let name = new_name(t, kind);
    let (x, y) = at.map_or_else(|| next_pos(t, kind), |p| (p.x, p.y));
    t.nodes.push(if kind == Kind::Network { Node::network(&id, &name, x, y, Role::Vm, true) } else { Node::new(&id, kind, &name, x, y) });
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
        None => Err(connect_error(t, a, b).unwrap_or_else(|| i18n::tr("in oVirt these objects are not linked directly").to_owned())),
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

/// Straight line between the centres of two objects (a link that is missing on the board).
pub fn missing_line(t: &Topology, from: &str, to: &str) -> Option<(Point, Point)> {
    let (a, b) = (t.node(from)?, t.node(to)?);
    Some((Point::new(a.x, a.y), Point::new(b.x, b.y)))
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
#[derive(Clone, Copy, Debug, PartialEq, Eq, Default)]
pub struct NodeInfo {
    pub chip: Option<Chip>,
    /// the host is the storage pool manager of its data center
    pub spm: bool,
    /// the storage domain is the master of its data center
    pub master: bool,
    /// the type of a storage domain (NFS, iSCSI); empty for other objects
    pub ty: &'static str,
    /// the storage domain is the replica copy of another one
    pub replica: bool,
    /// the VM is highly available
    pub ha: bool,
    /// memory in GB: what a VM needs, what a host has (0 for other objects)
    pub mem: u32,
    /// memory in GB the VMs placed on the host need (hosts only)
    pub used: Option<u32>,
    /// the rule of an affinity group is soft
    pub soft: bool,
}

impl NodeInfo {
    /// The VMs placed on the host need more memory than it has.
    pub fn over(&self) -> bool {
        self.used.is_some_and(|u| u > self.mem)
    }
}

fn host_chip(s: HostStatus) -> Chip {
    let class = match s {
        HostStatus::Up => "ok",
        HostStatus::NonResponsive => "bad",
        HostStatus::NonOperational | HostStatus::NoCluster => "warn",
        HostStatus::Maintenance => "",
    };
    Chip { class, text: s.name() }
}

fn dc_chip(s: DcStatus) -> Chip {
    let class = match s {
        DcStatus::Up => "ok",
        DcStatus::Uninitialized => "warn",
        DcStatus::NonResponsive => "bad",
    };
    Chip { class, text: s.name() }
}

fn domain_chip(s: DomainStatus) -> Chip {
    let class = if s == DomainStatus::Active { "ok" } else { "warn" };
    Chip { class, text: s.name() }
}

fn vm_chip(s: VmStatus) -> Chip {
    match s {
        VmStatus::Running => Chip { class: "ok", text: "Running" },
        VmStatus::Down => Chip { class: "warn", text: "Down" },
    }
}

/// Chip and badges of an object.
pub fn node_info(t: &Topology, ev: &Evaluation, id: &str) -> NodeInfo {
    let Some(n) = t.node(id) else { return NodeInfo::default() };
    let plain = NodeInfo::default();
    match n.kind {
        Kind::Host => {
            let load = host_load(t, id);
            NodeInfo {
                chip: ev.host(id).map(|h| host_chip(h.status)),
                spm: ev.dcs.iter().any(|d| d.spm.as_deref() == Some(id)),
                mem: load.capacity,
                used: Some(load.used),
                ..plain
            }
        }
        Kind::DataCenter => NodeInfo { chip: ev.dc(id).map(|d| dc_chip(d.status)), ..plain },
        Kind::StorageDomain => NodeInfo {
            chip: ev.domain(id).map(|d| domain_chip(d.status)),
            master: ev.domain(id).is_some_and(|d| d.master),
            ty: n.domain_type().label(),
            replica: t.sources(id, Rel::Replica).next().is_some(),
            ..plain
        },
        Kind::Vm => NodeInfo { chip: ev.vm(id).map(|v| vm_chip(v.status)), ha: n.ha(), mem: n.mem_gb(), ..plain },
        Kind::Network => NodeInfo { chip: Some(Chip { class: "", text: n.role().label() }), ..plain },
        Kind::AffinityGroup => NodeInfo {
            chip: Some(Chip { class: "", text: polarity_label(n.polarity()) }),
            soft: !n.flag("hard"),
            ..plain
        },
        Kind::Backup => NodeInfo { chip: Some(Chip { class: "", text: n.backup_type().label() }), ..plain },
        Kind::Permission => NodeInfo { chip: Some(Chip { class: "", text: n.perm_role().as_str() }), ..plain },
        Kind::Engine | Kind::Cluster | Kind::FenceAgent | Kind::User => plain,
    }
}

/// Short name of the polarity of an affinity group, for the chip.
pub fn polarity_label(p: Polarity) -> &'static str {
    match p {
        Polarity::Positive => i18n::tr("affinity"),
        Polarity::Negative => i18n::tr("anti-affinity"),
    }
}

/// The text of the badge in the corner of an object (types, SPM, HA, memory), parts joined with a dot.
pub fn badge_text(info: &NodeInfo) -> String {
    let mut parts: Vec<String> = vec![];
    if !info.ty.is_empty() {
        parts.push(info.ty.to_owned());
    }
    if info.replica {
        parts.push(i18n::tr("replica").to_owned());
    }
    if info.spm {
        parts.push(i18n::tr("SPM").to_owned());
    } else if info.master {
        parts.push(i18n::tr("master").to_owned());
    }
    if info.ha {
        parts.push(i18n::tr("HA").to_owned());
    }
    if info.soft {
        parts.push(i18n::tr("soft").to_owned());
    }
    if info.mem > 0 {
        parts.push(match info.used {
            Some(used) => i18n::trf!("{0}/{1} GB", used, info.mem),
            None => i18n::trf!("{0} GB", info.mem),
        });
    }
    parts.join(" · ")
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
        Kind::Engine => i18n::tr("The management engine: it talks to the hosts through VDSM and manages the data centers."),
        Kind::DataCenter => i18n::tr("A data center is a pool of clusters, logical networks and storage domains."),
        Kind::Cluster => i18n::tr("A cluster groups hosts with a common CPU type; a VM migrates only inside its cluster."),
        Kind::Host => i18n::tr("A hypervisor host that runs VMs; VDSM is its agent."),
        Kind::Network => i18n::tr("A logical network: defined in a data center, attached to clusters, assigned to host NICs."),
        Kind::StorageDomain => i18n::tr("A storage domain holds VM disks; the first one attached to a data center is its master."),
        Kind::Vm => i18n::tr("A virtual machine: it runs on a host and uses networks and storage domains."),
        Kind::FenceAgent => i18n::tr("A fence agent is the power management of a host: through it the engine switches a host that does not answer off and on."),
        Kind::AffinityGroup => i18n::tr("An affinity group keeps its VMs on one host (positive) or on different hosts (negative); a hard group is enforced."),
        Kind::Backup => i18n::tr("A backup of VMs: a snapshot lives on the storage domain of the disk, an incremental or a full backup is stored off the data center."),
        Kind::User => i18n::tr("A user of the Administration Portal: what the user may do comes from the permissions granted."),
        Kind::Permission => i18n::tr("A permission is a role on an object; it applies to the object and everything under it."),
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

/// Everything the inspector says about an object besides its name and parameters.
pub fn explain(t: &Topology, ev: &Evaluation, id: &str) -> Explain {
    let info = node_info(t, ev, id);
    let Some(n) = t.node(id) else { return Explain { info, lines: vec![] } };
    let mut lines = vec![about(n.kind).to_owned()];
    match n.kind {
        Kind::Host => {
            if let Some(h) = ev.host(id) {
                if h.why.is_empty() {
                    lines.push(i18n::tr("The host is Up: the engine reaches it, and it has every required network and storage domain.").to_owned());
                }
                lines.extend(h.why.iter().map(|w| w.text()));
            }
            if info.spm {
                lines.push(i18n::tr("It is the SPM: the first Up host of an Up data center manages the storage metadata.").to_owned());
            }
            let load = host_load(t, id);
            if load.used > 0 || load.over() {
                lines.push(i18n::trf!("Memory: the VMs placed on the host need {0} of {1} GB.", load.used, load.capacity));
            }
            if load.over() {
                lines.push(i18n::tr("That is more than the host has: none of its VMs can run.").to_owned());
            }
            match fence_agent(t, id) {
                Some(a) => lines.push(i18n::trf!("Power management: the fence agent “{0}”.", a.name)),
                None if t.targets(id, Rel::Runs).any(Node::ha) => {
                    lines.push(i18n::tr("No fence agent: the engine cannot power-cycle this host, so its HA VMs would not be restarted.").to_owned());
                }
                None => {}
            }
        }
        Kind::DataCenter => {
            lines.push(
                match ev.dc(id).map(|d| d.status) {
                    Some(DcStatus::Up) => i18n::tr("The data center works: it has an Up host and an active master storage domain."),
                    Some(DcStatus::Uninitialized) => i18n::tr("There is an Up host, but no active master storage domain yet."),
                    _ => i18n::tr("No host of the data center is Up."),
                }
                .to_owned(),
            );
            if let Some(spm) = ev.dc(id).and_then(|d| d.spm.as_deref()) {
                lines.push(i18n::trf!("The SPM is “{0}”.", name_of(t, spm)));
            }
        }
        Kind::StorageDomain => {
            lines.push(
                match ev.domain(id).map(|d| d.status) {
                    Some(DomainStatus::Active) => i18n::tr("An Up host of the data center sees the domain."),
                    Some(DomainStatus::Inactive) => i18n::tr("No Up host of the data center sees the domain."),
                    _ => i18n::tr("Attach the domain to a data center first."),
                }
                .to_owned(),
            );
            if info.master {
                lines.push(i18n::tr("It is the master domain of its data center.").to_owned());
            }
            if let Some(p) = t.sources(id, Rel::Replica).next() {
                lines.push(i18n::trf!("It is the replica copy of the domain “{0}”.", p.name));
            }
            let copies: Vec<String> = t.targets(id, Rel::Replica).map(|r| r.name.clone()).collect();
            if !copies.is_empty() {
                lines.push(i18n::trf!("Replicated to: {0}.", copies.join(", ")));
            }
        }
        Kind::Vm => {
            if let Some(v) = ev.vm(id) {
                if v.why.is_empty() {
                    lines.push(i18n::tr("The VM can run on its host.").to_owned());
                }
                lines.extend(v.why.iter().map(|w| w.text()));
            }
            lines.push(i18n::trf!("The VM needs {0} GB of memory.", n.mem_gb()));
            if n.ha() {
                lines.push(i18n::tr("Highly available: when its host fails, the engine fences the host and restarts the VM on another host of the cluster.").to_owned());
            }
            for g in t.sources(id, Rel::Affine) {
                let broken = affinity_breaks(t, &g.id).iter().any(|v| v == id);
                let rule = if g.polarity() == Polarity::Positive { i18n::tr("positive") } else { i18n::tr("negative") };
                let strength = if g.flag("hard") { i18n::tr("hard") } else { i18n::tr("soft") };
                lines.push(if broken {
                    i18n::trf!("Breaks the affinity group “{0}” ({1}, {2}).", g.name, strength, rule)
                } else {
                    i18n::trf!("Follows the affinity group “{0}” ({1}, {2}).", g.name, strength, rule)
                });
            }
            let backups: Vec<String> = t.targets(id, Rel::BackupOf).map(|b| format!("{} ({})", b.name, b.backup_type().label())).collect();
            if !backups.is_empty() {
                lines.push(i18n::trf!("Backups: {0}.", backups.join(", ")));
            }
        }
        Kind::Network => {
            lines.push(match t.sources(id, Rel::Defined).next() {
                Some(dc) => i18n::trf!("Defined in “{0}”.", dc.name),
                None => i18n::tr("Not defined in a data center yet.").to_owned(),
            });
            lines.push(i18n::trf!(
                "Attached to {0} cluster(s), assigned to {1} host(s), used by {2} VM(s).",
                t.targets(id, Rel::Attached).count(),
                t.targets(id, Rel::Assigned).count(),
                t.targets(id, Rel::Vnic).count()
            ));
        }
        Kind::Engine => {
            let hosts: Vec<&Node> = t.of_kind(Kind::Host).collect();
            let reached = hosts.iter().filter(|h| virtlab::ovirt_topo::trace(t, ev, &Op::EngineToHost { host: h.id.clone() }).ok).count();
            lines.push(i18n::trf!("The engine reaches {0} of {1} host(s).", reached, hosts.len()));
        }
        Kind::Cluster => {
            lines.push(i18n::trf!(
                "Hosts: {0}. Networks attached: {1}.",
                t.targets(id, Rel::Member).count(),
                t.sources(id, Rel::Attached).count()
            ));
        }
        Kind::FenceAgent => {
            let hosts: Vec<String> = t.targets(id, Rel::Fence).map(|h| h.name.clone()).collect();
            lines.push(if hosts.is_empty() { i18n::tr("Not linked to a host yet.").to_owned() } else { i18n::trf!("Power management of: {0}.", hosts.join(", ")) });
        }
        Kind::AffinityGroup => {
            let members: Vec<String> = t.targets(id, Rel::Affine).map(|v| v.name.clone()).collect();
            lines.push(if members.is_empty() { i18n::tr("No VMs in the group yet.").to_owned() } else { i18n::trf!("VMs: {0}.", members.join(", ")) });
            lines.push(match (n.polarity(), n.flag("hard")) {
                (Polarity::Positive, true) => i18n::tr("Hard positive: a VM that is not on the host of the first VM cannot run."),
                (Polarity::Positive, false) => i18n::tr("Soft positive: the VMs should share a host, but a status never changes."),
                (Polarity::Negative, true) => i18n::tr("Hard negative: a later VM on a host that already has one of the group cannot run."),
                (Polarity::Negative, false) => i18n::tr("Soft negative: the VMs should be apart, but a status never changes."),
            }
            .to_owned());
            let broken: Vec<String> = affinity_breaks(t, id).iter().filter_map(|v| t.node(v)).map(|v| v.name.clone()).collect();
            if !broken.is_empty() {
                lines.push(i18n::trf!("Breaking the rule now: {0}.", broken.join(", ")));
            }
        }
        Kind::Backup => {
            let vms: Vec<String> = t.sources(id, Rel::BackupOf).map(|v| v.name.clone()).collect();
            lines.push(if vms.is_empty() { i18n::tr("Backs up no VM yet.").to_owned() } else { i18n::trf!("Backs up: {0}.", vms.join(", ")) });
            lines.push(
                if n.backup_type().off_site() {
                    i18n::tr("It is stored off the data center: it survives the loss of a storage domain or of the whole site.")
                } else {
                    i18n::tr("A snapshot lives on the storage domain of the disk: it is lost together with the domain.")
                }
                .to_owned(),
            );
        }
        Kind::User => {
            let perms: Vec<String> = t.targets(id, Rel::Grants).map(|p| format!("{} ({})", p.name, p.perm_role().as_str())).collect();
            lines.push(if perms.is_empty() { i18n::tr("No permissions granted yet: the user can do nothing.").to_owned() } else { i18n::trf!("Permissions: {0}.", perms.join(", ")) });
        }
        Kind::Permission => {
            lines.push(match t.sources(id, Rel::Grants).next() {
                Some(u) => i18n::trf!("Granted to “{0}”.", u.name),
                None => i18n::tr("Not granted to a user yet.").to_owned(),
            });
            lines.push(match t.targets(id, Rel::OnObject).next() {
                Some(o) => i18n::trf!("Applies to “{0}” ({1}) and everything under it.", o.name, o.kind.label()),
                None => i18n::tr("Applies to no object yet: it grants nothing.").to_owned(),
            });
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

// --- the hierarchy tree ---------------------------------------------------------------------------------

/// A row of the hierarchy tree.
#[derive(Clone, Debug, PartialEq)]
pub enum TreeItem {
    /// A heading over objects that are not in the hierarchy yet.
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

    fn data_center(&mut self, depth: usize, dc: &Node) {
        let t = self.t;
        self.node(depth, dc);
        for cl in t.targets(&dc.id, Rel::Contains) {
            self.node(depth + 1, cl);
            for h in t.targets(&cl.id, Rel::Member) {
                self.node(depth + 2, h);
                for agent in t.sources(&h.id, Rel::Fence) {
                    self.node(depth + 3, agent);
                }
                for vm in t.targets(&h.id, Rel::Runs) {
                    self.node(depth + 3, vm);
                }
            }
        }
        for n in t.targets(&dc.id, Rel::Defined) {
            self.node(depth + 1, n);
        }
        for d in t.targets(&dc.id, Rel::Domain) {
            self.node(depth + 1, d);
        }
    }
}

/// The hierarchy derived from the links: engine › data center › cluster › host › VM, with the networks and storage domains under their
/// data center; objects that are not reachable yet are listed at the end.
pub fn tree(t: &Topology, ev: &Evaluation) -> Vec<TreeItem> {
    let mut b = TreeBuilder { t, ev, out: vec![], seen: BTreeSet::new() };
    for e in t.of_kind(Kind::Engine) {
        b.node(0, e);
        for dc in t.targets(&e.id, Rel::Manages) {
            b.data_center(1, dc);
        }
    }
    for dc in t.of_kind(Kind::DataCenter) {
        if !b.seen.contains(&dc.id) {
            b.data_center(0, dc);
        }
    }
    // users with their permissions, affinity groups and backups hang from no data center: they get their own headings
    let users: Vec<&Node> = t.of_kind(Kind::User).collect();
    if !users.is_empty() {
        b.out.push(TreeItem::Heading(i18n::tr("Users and permissions")));
        for u in users {
            b.node(1, u);
            for p in t.targets(&u.id, Rel::Grants) {
                b.node(2, p);
            }
        }
    }
    for (kind, heading) in [(Kind::AffinityGroup, i18n::tr("Affinity groups")), (Kind::Backup, i18n::tr("Backups"))] {
        let items: Vec<&Node> = t.of_kind(kind).collect();
        if !items.is_empty() {
            b.out.push(TreeItem::Heading(heading));
            for n in items {
                b.node(1, n);
            }
        }
    }
    let loose: Vec<&Node> = t.nodes.iter().filter(|n| !b.seen.contains(&n.id)).collect();
    if !loose.is_empty() {
        b.out.push(TreeItem::Heading(i18n::tr("Not in the hierarchy yet")));
        for n in loose {
            b.node(1, n);
        }
    }
    b.out
}

// --- the path of a message ---------------------------------------------------------------------------

/// What a shown path highlights on the board.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct PathView {
    /// links of the board the messages go over: `(source, target) → works`
    pub edges: BTreeMap<(String, String), bool>,
    /// objects that take part: `id → works`
    pub nodes: BTreeMap<String, bool>,
    /// links a failed step needs but the board lacks: `(from, to)`
    pub missing: Vec<(String, String)>,
}

/// The hops of a trace that are shown: all of them, or the first up to and including hop `active`.
pub fn shown_hops(trace: &Trace, active: Option<usize>) -> usize {
    active.map_or(trace.hops.len(), |i| (i + 1).min(trace.hops.len()))
}

/// What to highlight for the hops of `trace` that are shown.
pub fn path_view(t: &Topology, trace: &Trace, active: Option<usize>) -> PathView {
    let mut v = PathView::default();
    for hop in trace.hops.iter().take(shown_hops(trace, active)) {
        for (a, b) in &hop.links {
            if t.linked(a, b) {
                let e = v.edges.entry((a.clone(), b.clone())).or_insert(true);
                *e &= hop.ok;
            } else if !hop.ok {
                v.missing.push((a.clone(), b.clone()));
            }
        }
        if !hop.ok && hop.links.is_empty() && hop.from != hop.to {
            v.missing.push((hop.from.clone(), hop.to.clone()));
        }
        for id in [&hop.from, &hop.to] {
            if t.node(id).is_some() {
                let n = v.nodes.entry(id.clone()).or_insert(true);
                *n &= hop.ok;
            }
        }
    }
    v.missing.retain(|(a, b)| t.node(a).is_some() && t.node(b).is_some());
    v.missing.sort();
    v.missing.dedup();
    v
}

/// Operations offered for the selected object.
pub fn ops_for(t: &Topology, selected: Option<&str>) -> Vec<Op> {
    match selected.and_then(|id| t.node(id)) {
        Some(n) if n.kind == Kind::Host => vec![Op::EngineToHost { host: n.id.clone() }, Op::Fence { host: n.id.clone() }],
        Some(n) if n.kind == Kind::Vm => vec![Op::StartVm { vm: n.id.clone() }, Op::Migrate { vm: n.id.clone() }],
        _ => vec![],
    }
}

/// `data-op` of an operation button.
pub fn op_name(op: &Op) -> &'static str {
    match op {
        Op::EngineToHost { .. } => "engine_to_host",
        Op::StartVm { .. } => "start_vm",
        Op::Migrate { .. } => "migrate",
        Op::Fence { .. } => "fence",
    }
}

/// Text of an operation button.
pub fn op_label(op: &Op) -> &'static str {
    match op {
        Op::EngineToHost { .. } => i18n::tr("Engine → host"),
        Op::StartVm { .. } => i18n::tr("Start the VM"),
        Op::Migrate { .. } => i18n::tr("Migrate"),
        Op::Fence { .. } => i18n::tr("Fence"),
    }
}

#[cfg(test)]
mod tests {
    use virtlab::ovirt_topo::{default_scenarios, default_solution, evaluate as evaluated, problems, trace};

    use super::*;

    fn ru() -> i18n::LocaleGuard {
        locales::guard(i18n::Locale::Ru)
    }

    fn en() -> i18n::LocaleGuard {
        locales::guard(i18n::Locale::En)
    }

    fn scenarios() -> Vec<Scenario> {
        default_scenarios()
    }

    #[test]
    fn draft_round_trips_every_board() {
        let _ru = ru();
        let sc = scenarios();
        let mut boards = restore(&sc, "");
        // an empty or corrupt draft is the starting boards
        for (b, s) in boards.iter().zip(&sc) {
            assert_eq!(*b, s.start, "{}", s.id);
        }
        // edit two boards and write them down
        add_node(&mut boards[0], Kind::Engine, None);
        let id = add_node(&mut boards[1], Kind::Host, None);
        let text = draft_json(&sc.iter().zip(&boards).map(|(s, b)| (s.id.clone(), b.clone())).collect::<Vec<_>>());
        let back = restore(&sc, &text);
        assert_eq!(back, boards);
        assert!(back[1].node(&id).is_some());
    }

    #[test]
    fn restore_tolerates_garbage_and_unknown_ids() {
        let _ru = ru();
        let sc = scenarios();
        let starts: Vec<Topology> = sc.iter().map(|s| s.start.clone()).collect();
        for draft in ["", "null", "[]", "42", "not json", "{", r#"{"build": 5}"#, r#"{"nope": {"nodes": [], "edges": []}}"#, r#"{"build": {"nodes": 1}}"#] {
            assert_eq!(restore(&sc, draft), starts, "{draft:?}");
        }
        // a known id next to an unknown one: the known board is restored, the others start over
        let mut t = Topology::default();
        add_node(&mut t, Kind::Engine, None);
        let text = format!(r#"{{"build": {}, "other": {{"nodes": [], "edges": []}}}}"#, serde_json::to_string(&t).unwrap_or_default());
        let back = restore(&sc, &text);
        assert_eq!(back[0], t);
        assert_eq!(back[1], starts[1]);
    }

    #[test]
    fn restore_drops_boards_that_break_the_rules() {
        let _ru = ru();
        let sc = scenarios();
        let mut t = Topology::default();
        add_node(&mut t, Kind::Host, None);
        t.edges.push(Edge::new("h1", "nobody"));
        let text = draft_json(&[("build".to_owned(), t)]);
        assert_eq!(restore(&sc, &text)[0], sc[0].start);
        // the reference boards are fine
        let refs = default_solution();
        let all: Vec<(String, Topology)> = refs.into_iter().collect();
        let back = restore(&sc, &draft_json(&all));
        for (s, b) in sc.iter().zip(&back) {
            assert!(s.reached(b), "{}", s.id);
        }
    }

    #[test]
    fn new_objects_get_free_places_ids_and_names() {
        let _ru = ru();
        let sc = scenarios();
        let mut t = sc.iter().find(|s| s.id == "repair").map(|s| s.start.clone()).unwrap_or_default();
        let h = add_node(&mut t, Kind::Host, None);
        // the start board has host-1..3 on rows 0..2 of the host column
        assert_eq!(t.node(&h).map(|n| n.name.as_str()), Some("host-4"));
        assert_eq!(t.node(&h).map(|n| (n.x, n.y)), Some((590.0, 300.0)));
        let h2 = add_node(&mut t, Kind::Host, None);
        assert_ne!(h, h2);
        assert_eq!(t.node(&h2).map(|n| n.y), Some(380.0));
        // a network starts as a required VM network, a placed object lands where it was dropped
        let n = add_node(&mut t, Kind::Network, Some(Point::new(5.0, 6.0)));
        let net = t.node(&n).cloned().unwrap_or_else(|| Node::new("", Kind::Host, "", 0.0, 0.0));
        assert_eq!((net.role(), net.required(), net.x, net.y), (Role::Vm, true, 5.0, 6.0));
        assert!(problems(&t).is_empty());
        // one engine is named plainly, the second would be numbered
        let mut e = Topology::default();
        let first = add_node(&mut e, Kind::Engine, None);
        assert_eq!((first.as_str(), e.nodes[0].name.as_str()), ("engine", "engine"));
        assert_eq!(new_id(&e, Kind::Engine), "engine1");
        // the placement of the empty board follows the columns
        let mut b = Topology::default();
        for kind in [Kind::Engine, Kind::DataCenter, Kind::Cluster, Kind::Host, Kind::Vm, Kind::Network, Kind::StorageDomain] {
            add_node(&mut b, kind, None);
        }
        let xs: Vec<f64> = b.nodes.iter().map(|n| n.x).collect();
        // the storage domains sit under the clusters, so a long column of networks never runs into them
        assert_eq!(xs, [70.0, 190.0, 450.0, 590.0, 730.0, 310.0, 450.0]);
        assert_eq!(b.nodes[6].y, 380.0);
    }

    #[test]
    fn the_new_kinds_get_readable_ids_names_and_places() {
        let _en = en();
        let mut t = Topology::default();
        let ids: Vec<String> = [Kind::FenceAgent, Kind::AffinityGroup, Kind::Backup, Kind::User, Kind::Permission, Kind::FenceAgent]
            .into_iter()
            .map(|k| add_node(&mut t, k, None))
            .collect();
        assert_eq!(ids, ["fence-1", "group-1", "backup-1", "user-1", "perm-1", "fence-2"]);
        let names: Vec<&str> = t.nodes.iter().map(|n| n.name.as_str()).collect();
        assert_eq!(names, ["fence-1", "group-1", "backup-1", "user-1", "perm-1", "fence-2"]);
        // every kind has a column, and nothing lands on top of anything else
        for (i, a) in t.nodes.iter().enumerate() {
            for b in &t.nodes[i + 1..] {
                assert!((a.x - b.x).abs() >= NODE_W || (a.y - b.y).abs() >= NODE_H, "{} and {} overlap", a.id, b.id);
            }
        }
        assert!(problems(&t).is_empty());
        // six networks and a domain: the domain is in another column
        let mut t = Topology::default();
        for _ in 0..6 {
            add_node(&mut t, Kind::Network, None);
        }
        add_node(&mut t, Kind::StorageDomain, None);
        let dom = t.nodes.last().cloned().unwrap_or_else(|| Node::new("", Kind::Host, "", 0.0, 0.0));
        assert!(t.nodes.iter().filter(|n| n.kind == Kind::Network).all(|n| (n.x - dom.x).abs() >= NODE_W || (n.y - dom.y).abs() >= NODE_H));
        // the new objects keep their defaults unset, so the draft stays small
        assert!(t.nodes.iter().all(|n| n.kind == Kind::Network || n.params.is_empty()));
    }

    #[test]
    fn the_inspector_keeps_the_field_order_the_e2e_relies_on() {
        let _en = en();
        use virtlab::ovirt_topo::{param_specs, ParamTy};
        let first_select = |k: Kind| param_specs(k).into_iter().find(|s| matches!(s.ty, ParamTy::Select(_))).map(|s| s.key);
        let first_switch = |k: Kind| param_specs(k).into_iter().find(|s| matches!(s.ty, ParamTy::Bool)).map(|s| s.key);
        assert_eq!(first_select(Kind::Network), Some("role"));
        assert_eq!(first_switch(Kind::Network), Some("required"));
        assert_eq!(first_select(Kind::StorageDomain), Some("type"));
        assert_eq!(first_switch(Kind::StorageDomain), None);
        // the role select lists the roles by value, in the order of the model, with their captions
        let roles = param_specs(Kind::Network)[0].options().iter().map(|o| (o.value, o.label)).collect::<Vec<_>>();
        assert_eq!(roles[0].0, "vm");
        assert!(roles.iter().any(|(v, l)| *v == "management" && *l == Role::Management.label()));
        // a host and a VM have a memory choice and a switch; the rest have none or their own
        assert_eq!(first_select(Kind::Host), Some("mem"));
        assert_eq!(first_switch(Kind::Vm), Some("ha"));
    }

    #[test]
    fn links_are_normalised_to_the_direction_of_the_model() {
        let _ru = ru();
        let t = default_solution().remove("storage").unwrap_or_default();
        // the pair is given in either order: the model direction wins
        assert_eq!(normalize_link(&t, "h1", "cl1"), Some(("cl1".to_owned(), "h1".to_owned())));
        assert_eq!(normalize_link(&t, "cl1", "h1"), Some(("cl1".to_owned(), "h1".to_owned())));
        assert_eq!(normalize_link(&t, "h1", "h2"), None);
        assert_eq!(normalize_link(&t, "h1", "nobody"), None);
        // refusals carry the model's reason
        assert!(link_check(&t, "h1", "cl1").is_err(), "the host is already in the cluster");
        assert!(link_check(&t, "h1", "h2").is_err());
        // a new host joins a cluster from the host side as well
        let mut t = t;
        let h = add_node(&mut t, Kind::Host, None);
        assert_eq!(link_check(&t, &h, "cl1"), Ok(("cl1".to_owned(), h.clone())));
        // pins: who has an input and who has an output
        assert!(has_out(Kind::Engine) && !has_in(Kind::Engine));
        assert!(has_in(Kind::Vm) && has_out(Kind::Vm), "a VM points at its backups now");
        for k in [Kind::DataCenter, Kind::Cluster, Kind::Host, Kind::Network, Kind::StorageDomain] {
            assert!(has_in(k) && has_out(k), "{k:?}");
        }
        // the new kinds: agents, groups and users only point; backups and permissions are pointed at and point on
        assert!(has_out(Kind::FenceAgent) && !has_in(Kind::FenceAgent));
        assert!(has_out(Kind::AffinityGroup) && !has_in(Kind::AffinityGroup));
        assert!(has_out(Kind::User) && !has_in(Kind::User));
        assert!(has_in(Kind::Backup) && !has_out(Kind::Backup));
        assert!(has_in(Kind::Permission) && has_out(Kind::Permission));
        assert!(has_in(Kind::StorageDomain) && has_out(Kind::StorageDomain), "a replica link joins two domains");
    }

    #[test]
    fn a_wire_follows_the_link_it_would_make() {
        let _ru = ru();
        let t = default_solution().remove("build").unwrap_or_default();
        let from_host = Pending { id: "h1".into(), pin: Pin::In };
        // dragging from the input of a host over the data center is refused, over a cluster that already holds it is refused too
        assert_eq!(port_state(&t, Some(&from_host), "dc1"), PortState::Bad);
        assert_eq!(port_state(&t, Some(&from_host), "h1"), PortState::Idle);
        assert_eq!(port_state(&t, None, "dc1"), PortState::Idle);
        let (d, tone) = pending_wire(&t, &from_host, Some("dc1"), None).expect("wire");
        assert_eq!(tone, "bad");
        assert!(d.starts_with('M'));
        // the network is not yet seen by the host: the wire goes network → host even if it was started at the host
        let mut t2 = t;
        add_node(&mut t2, Kind::Network, None);
        let id = t2.nodes.last().map(|n| n.id.clone()).unwrap_or_default();
        let pend = Pending { id: "h1".into(), pin: Pin::Out };
        assert_eq!(pin_link(&t2, &pend, &id).map_err(|e| e.len() > 0), Err(true), "not defined in a data center yet");
        assert_eq!(pending_wire(&t2, &pend, None, Some(Point::new(1.0, 2.0))).map(|w| w.1), Some(""));
        assert_eq!(pending_wire(&t2, &pend, None, None), None);
    }

    #[test]
    fn deleting_reports_the_dependent_links() {
        let _ru = ru();
        let mut t = default_solution().remove("storage").unwrap_or_default();
        let before = t.edges.len();
        // detaching the network from the cluster also drops the assignments to both hosts
        assert_eq!(remove_edge(&mut t, &Edge::new("mgmt", "cl1")), 2);
        assert_eq!(t.edges.len(), before - 3);
        assert!(problems(&t).is_empty());
        // removing the cluster drops its own links without counting them, and the dependants
        let mut t = default_solution().remove("storage").unwrap_or_default();
        let dropped = remove_node(&mut t, "cl1");
        assert!(t.node("cl1").is_none() && t.edges.iter().all(|e| e.from != "cl1" && e.to != "cl1"));
        assert_eq!(dropped, 4, "the network assignments and the storage connections of both hosts");
        assert!(problems(&t).is_empty());
    }

    #[test]
    fn long_links_arch_and_short_ones_do_not() {
        let _ru = ru();
        let (flat, mid) = wire(Point::new(0.0, 100.0), Point::new(100.0, 100.0));
        assert!(flat.starts_with("M0.0 100.0 C"));
        assert_eq!(mid.y, 100.0);
        let (_, arch) = wire(Point::new(0.0, 100.0), Point::new(240.0, 100.0));
        assert!(arch.y < 100.0 - 28.0, "the link between columns two apart clears the object in between: {}", arch.y);
        let (_, diagonal) = wire(Point::new(0.0, 100.0), Point::new(240.0, 300.0));
        assert!(diagonal.y > 100.0 && diagonal.y < 300.0);
    }

    #[test]
    fn fit_shows_every_object() {
        let _ru = ru();
        assert_eq!(fit_view(&[], 520.0), BOARD.home_view());
        let t = default_solution().remove("storage").unwrap_or_default();
        let pts: Vec<Point> = t.nodes.iter().map(|n| Point::new(n.x, n.y)).collect();
        let v = fit_view(&pts, 520.0);
        assert!(v.zoom >= BOARD.zoom_min && v.zoom <= 1.6);
        for p in &pts {
            let (x, y) = ((p.x - v.pan.x) * v.zoom, (p.y - v.pan.y) * v.zoom);
            assert!(x > 0.0 && x < BOARD_W && y > 0.0 && y < 520.0, "{p:?} -> {x} {y}");
        }
        assert_eq!(world_height(0.0, 0.0), BOARD_H);
        assert_eq!(world_height(860.0, 430.0), 430.0);
    }

    #[test]
    fn statuses_and_badges_come_from_the_evaluation() {
        let _ru = ru();
        let t = default_solution().remove("storage").unwrap_or_default();
        let ev = evaluated(&t);
        let info = |id: &str| node_info(&t, &ev, id);
        assert_eq!(info("h1").chip, Some(Chip { class: "ok", text: "Up" }));
        assert!(info("h1").spm && !info("h2").spm);
        assert!(info("nfs").master);
        assert_eq!(info("nfs").chip, Some(Chip { class: "ok", text: "Active" }));
        assert_eq!(info("dc1").chip, Some(Chip { class: "ok", text: "Up" }));
        assert_eq!(info("mgmt").chip, Some(Chip { class: "", text: Role::Management.label() }));
        assert_eq!(info("engine"), NodeInfo::default());
        assert_eq!(status_class(&info("h1")), "ok");
        assert_eq!(status_class(&info("mgmt")), "idle");
        assert_eq!(status_class(&info("cl1")), "idle");
        // a broken board shows the reasons
        let broken = default_scenarios().into_iter().find(|s| s.id == "repair").map(|s| s.start).unwrap_or_default();
        let ev = evaluated(&broken);
        assert_eq!(node_info(&broken, &ev, "h2").chip, Some(Chip { class: "warn", text: "NonOperational" }));
        assert_eq!(node_info(&broken, &ev, "h3").chip, Some(Chip { class: "bad", text: "NonResponsive" }));
        let why = explain(&broken, &ev, "h2");
        assert!(why.lines.iter().any(|l| l.contains("vm-net")), "{:?}", why.lines);
        let vm = explain(&broken, &ev, "vm1");
        assert_eq!(vm.info.chip.map(|c| c.text), Some("Down"));
        assert!(vm.lines.len() >= 2);
        // every object kind explains itself
        for n in &broken.nodes {
            assert!(!explain(&broken, &ev, &n.id).lines.is_empty(), "{}", n.id);
        }
    }

    #[test]
    fn the_tree_follows_the_links_and_lists_the_rest() {
        let _ru = ru();
        let t = default_solution().remove("repair").unwrap_or_default();
        let ev = evaluated(&t);
        let rows = tree(&t, &ev);
        let depth_of = |id: &str| {
            rows.iter().find_map(|r| match r {
                TreeItem::Node { depth, id: i, .. } if i == id => Some(*depth),
                _ => None,
            })
        };
        assert_eq!(depth_of("engine"), Some(0));
        assert_eq!(depth_of("dc1"), Some(1));
        assert_eq!(depth_of("cl1"), Some(2));
        assert_eq!(depth_of("h1"), Some(3));
        assert_eq!(depth_of("vm1"), Some(4), "the VM runs on host-2");
        assert_eq!(depth_of("mgmt"), Some(2), "networks and domains hang from the data center");
        assert_eq!(depth_of("nfs"), Some(2));
        assert!(!rows.iter().any(|r| matches!(r, TreeItem::Heading(_))));
        // each object once
        assert_eq!(rows.len(), t.nodes.len());
        // a half-built board: loose objects come last under a heading
        let mut half = Topology::default();
        add_node(&mut half, Kind::Host, None);
        add_node(&mut half, Kind::DataCenter, None);
        let rows = tree(&half, &evaluated(&half));
        assert!(matches!(rows[0], TreeItem::Node { depth: 0, kind: Kind::DataCenter, .. }));
        assert!(matches!(rows[1], TreeItem::Heading(_)));
        assert!(matches!(rows[2], TreeItem::Node { depth: 1, kind: Kind::Host, .. }));
    }

    #[test]
    fn a_path_highlights_the_links_it_goes_over() {
        let _ru = ru();
        let t = default_solution().remove("migrate").unwrap_or_default();
        let ev = evaluated(&t);
        let tr = trace(&t, &ev, &Op::StartVm { vm: "vm1".into() });
        assert!(tr.ok);
        let all = path_view(&t, &tr, None);
        assert_eq!(all.edges.get(&("engine".to_owned(), "mgmt".to_owned())), Some(&true));
        assert_eq!(all.edges.get(&("mgmt".to_owned(), "h1".to_owned())), Some(&true));
        assert!(all.missing.is_empty());
        assert_eq!(all.nodes.get("engine"), Some(&true));
        // stepping: only the first hop
        let first = path_view(&t, &tr, Some(0));
        assert!(first.edges.len() < all.edges.len());
        assert_eq!(shown_hops(&tr, Some(0)), 1);
        assert_eq!(shown_hops(&tr, None), tr.hops.len());
        assert_eq!(shown_hops(&tr, Some(99)), tr.hops.len());
        // a failing path marks the missing link and the objects red
        let broken = default_scenarios().into_iter().find(|s| s.id == "repair").map(|s| s.start).unwrap_or_default();
        let ev = evaluated(&broken);
        let tr = trace(&broken, &ev, &Op::EngineToHost { host: "h3".into() });
        assert!(!tr.ok);
        let v = path_view(&broken, &tr, None);
        assert_eq!(v.missing, [("engine".to_owned(), "h3".to_owned())]);
        assert_eq!(v.nodes.get("h3"), Some(&false));
    }

    #[test]
    fn operations_are_offered_by_the_selected_kind() {
        let _ru = ru();
        let t = default_solution().remove("migrate").unwrap_or_default();
        let names = |sel: Option<&str>| ops_for(&t, sel).iter().map(op_name).collect::<Vec<_>>();
        assert_eq!(names(Some("h1")), ["engine_to_host", "fence"]);
        assert_eq!(names(Some("vm1")), ["start_vm", "migrate"]);
        assert!(names(Some("dc1")).is_empty());
        assert!(names(Some("nobody")).is_empty());
        assert!(names(None).is_empty());
        // a host can also be fenced
        let fence = ops_for(&t, Some("h1")).pop().unwrap_or(Op::EngineToHost { host: String::new() });
        assert_eq!((op_name(&fence), op_label(&fence)), ("fence", "Оградить"));
    }

    // ---- the new mechanics: memory, maintenance, HA, affinity, backups, permissions ----------------------------

    use virtlab::ovirt_topo::Param;

    fn put(t: &mut Topology, id: &str, kind: Kind, params: &[(&str, Param)]) {
        let mut n = Node::new(id, kind, id, 0.0, 0.0);
        for (k, v) in params {
            n.params.insert((*k).into(), v.clone());
        }
        t.nodes.push(n);
    }

    fn links(t: &mut Topology, pairs: &[(&str, &str)]) {
        t.edges.extend(pairs.iter().map(|(a, b)| Edge::new(a, b)));
    }

    /// An environment of one data center with two 16 GB hosts, a HA VM of 8 GB and a plain one of 4 GB on `h1`, an agent for `h1`,
    /// a negative group over both, a full backup of the HA VM, a user with a permission on the cluster, and a replica pair of domains.
    fn busy() -> Topology {
        let mut t = Topology::default();
        let mem = |gb: &str| Param::Str(gb.into());
        for (id, kind) in [("engine", Kind::Engine), ("dc1", Kind::DataCenter), ("cl1", Kind::Cluster), ("nfs", Kind::StorageDomain), ("copy", Kind::StorageDomain)] {
            put(&mut t, id, kind, &[]);
        }
        put(&mut t, "mgmt", Kind::Network, &[("role", Param::Str("management".into()))]);
        put(&mut t, "h1", Kind::Host, &[("mem", mem("16"))]);
        put(&mut t, "h2", Kind::Host, &[("mem", mem("16"))]);
        put(&mut t, "ha", Kind::Vm, &[("mem", mem("8")), ("ha", Param::Bool(true))]);
        put(&mut t, "plain", Kind::Vm, &[("mem", mem("4"))]);
        put(&mut t, "fence-1", Kind::FenceAgent, &[]);
        put(&mut t, "group-1", Kind::AffinityGroup, &[("polarity", Param::Str("negative".into())), ("hard", Param::Bool(false))]);
        put(&mut t, "backup-1", Kind::Backup, &[("type", Param::Str("full".into()))]);
        put(&mut t, "user-1", Kind::User, &[]);
        put(&mut t, "perm-1", Kind::Permission, &[("role", Param::Str("ClusterAdmin".into()))]);
        links(
            &mut t,
            &[
                ("engine", "dc1"), ("dc1", "cl1"), ("dc1", "mgmt"), ("mgmt", "cl1"), ("engine", "mgmt"), ("dc1", "nfs"), ("cl1", "h1"), ("cl1", "h2"),
                ("mgmt", "h1"), ("mgmt", "h2"), ("nfs", "h1"), ("nfs", "h2"), ("h1", "ha"), ("h1", "plain"), ("nfs", "ha"), ("nfs", "plain"), ("dc1", "copy"), ("copy", "h1"), ("copy", "h2"),
                ("fence-1", "h1"), ("group-1", "ha"), ("group-1", "plain"), ("ha", "backup-1"), ("user-1", "perm-1"), ("perm-1", "cl1"), ("nfs", "copy"),
            ],
        );
        t
    }

    #[test]
    fn badges_and_chips_show_the_new_mechanics() {
        let _en = en();
        let mut t = busy();
        assert!(problems(&t).is_empty(), "{:?}", problems(&t).into_iter().map(|p| p.text).collect::<Vec<_>>());
        let info = |t: &Topology, id: &str| node_info(t, &evaluated(t), id);
        // a HA VM with its memory; a host with its load and the SPM
        let ha = info(&t, "ha");
        assert!(ha.ha && ha.mem == 8 && ha.used.is_none());
        assert_eq!(badge_text(&ha), "HA · 8 GB");
        assert_eq!(badge_text(&info(&t, "plain")), "4 GB");
        let h1 = info(&t, "h1");
        assert_eq!((h1.mem, h1.used, h1.over()), (16, Some(12), false));
        assert_eq!(badge_text(&h1), "SPM · 12/16 GB");
        assert_eq!(badge_text(&info(&t, "h2")), "0/16 GB");
        // the domains: the type and the replica mark
        assert_eq!(badge_text(&info(&t, "nfs")), "NFS · master");
        assert_eq!(badge_text(&info(&t, "copy")), "NFS · replica");
        // the chips of the new kinds
        assert_eq!(info(&t, "group-1").chip, Some(Chip { class: "", text: "anti-affinity" }));
        assert_eq!(badge_text(&info(&t, "group-1")), "soft");
        assert_eq!(info(&t, "backup-1").chip, Some(Chip { class: "", text: "full" }));
        assert_eq!(info(&t, "perm-1").chip, Some(Chip { class: "", text: "ClusterAdmin" }));
        assert_eq!(info(&t, "fence-1"), NodeInfo::default());
        assert_eq!(info(&t, "user-1"), NodeInfo::default());
        assert_eq!(status_class(&info(&t, "perm-1")), "idle");
        // a host over its memory is marked; the VMs on it are Down
        t.nodes.iter_mut().find(|n| n.id == "ha").map(|n| n.params.insert("mem".into(), Param::Str("16".into())));
        let h1 = info(&t, "h1");
        assert!(h1.over());
        assert_eq!(badge_text(&h1), "SPM · 20/16 GB");
        assert_eq!(info(&t, "ha").chip, Some(Chip { class: "warn", text: "Down" }));
        // maintenance: a neutral chip, not a failure
        t.nodes.iter_mut().find(|n| n.id == "h2").map(|n| n.params.insert("maintenance".into(), Param::Bool(true)));
        assert_eq!(info(&t, "h2").chip, Some(Chip { class: "", text: "Maintenance" }));
        assert_eq!(status_class(&info(&t, "h2")), "idle");
    }

    #[test]
    fn the_inspector_explains_every_new_status_and_reason() {
        let _en = en();
        let mut t = busy();
        let lines = |t: &Topology, id: &str| explain(t, &evaluated(t), id).lines;
        // every kind explains itself, also on a board that uses all of them
        for n in &t.nodes {
            assert!(lines(&t, &n.id).len() >= 2 || matches!(n.kind, Kind::Engine), "{}: {:?}", n.id, lines(&t, &n.id));
        }
        let has = |t: &Topology, id: &str, part: &str| lines(t, id).iter().any(|l| l.contains(part));
        // host: memory, agent
        assert!(has(&t, "h1", "need 12 of 16 GB"));
        assert!(has(&t, "h1", "fence agent “fence-1”"));
        assert!(!has(&t, "h2", "fence"), "no noise on a host without HA VMs");
        // VM: memory, HA, the group it follows, backups
        assert!(has(&t, "ha", "needs 8 GB"));
        assert!(has(&t, "ha", "Highly available"));
        assert!(has(&t, "ha", "Backups: backup-1 (full)"));
        assert!(has(&t, "plain", "Breaks the affinity group “group-1” (soft, negative)"), "{:?}", lines(&t, "plain"));
        assert!(has(&t, "ha", "Follows the affinity group “group-1” (soft, negative)"));
        // out of memory is said on the host and on the VMs
        t.nodes.iter_mut().find(|n| n.id == "ha").map(|n| n.params.insert("mem".into(), Param::Str("16".into())));
        assert!(has(&t, "h1", "more than the host has"));
        assert!(has(&t, "ha", "need more memory than it has"));
        // maintenance
        t.nodes.iter_mut().find(|n| n.id == "h2").map(|n| n.params.insert("maintenance".into(), Param::Bool(true)));
        assert!(has(&t, "h2", "maintenance mode"));
        // a hard group says which VM breaks it
        t.nodes.iter_mut().find(|n| n.id == "group-1").map(|n| n.params.insert("hard".into(), Param::Bool(true)));
        assert!(has(&t, "group-1", "Breaking the rule now: plain"));
        assert!(has(&t, "plain", "Breaks the affinity group “group-1” (hard, negative)"));
        assert!(has(&t, "plain", "breaks the hard affinity group"));
        assert!(has(&t, "group-1", "Hard negative"));
        // the others
        assert!(has(&t, "fence-1", "Power management of: h1"));
        assert!(has(&t, "backup-1", "Backs up: ha"));
        assert!(has(&t, "backup-1", "off the data center"));
        assert!(has(&t, "user-1", "Permissions: perm-1 (ClusterAdmin)"));
        assert!(has(&t, "perm-1", "Granted to “user-1”"));
        assert!(has(&t, "perm-1", "Applies to “cl1” (cluster) and everything under it"));
        assert!(has(&t, "copy", "replica copy of the domain “nfs”"));
        assert!(has(&t, "nfs", "Replicated to: copy"));
        // empty objects say what is missing
        put(&mut t, "u2", Kind::User, &[]);
        put(&mut t, "p2", Kind::Permission, &[]);
        put(&mut t, "snap", Kind::Backup, &[]);
        put(&mut t, "f2", Kind::FenceAgent, &[]);
        put(&mut t, "g2", Kind::AffinityGroup, &[]);
        assert!(has(&t, "u2", "can do nothing"));
        assert!(has(&t, "p2", "Not granted to a user yet") && has(&t, "p2", "grants nothing"));
        assert!(has(&t, "snap", "Backs up no VM") && has(&t, "snap", "lost together with the domain"));
        assert!(has(&t, "f2", "Not linked to a host yet"));
        assert!(has(&t, "g2", "No VMs in the group"));
    }

    #[test]
    fn the_tree_lists_users_groups_and_backups_under_headings() {
        let _en = en();
        let t = busy();
        let rows = tree(&t, &evaluated(&t));
        let at = |id: &str| rows.iter().position(|r| matches!(r, TreeItem::Node { id: i, .. } if i == id));
        let depth = |id: &str| rows.iter().find_map(|r| match r {
            TreeItem::Node { depth, id: i, .. } if i == id => Some(*depth),
            _ => None,
        });
        // the agent hangs from its host, before the host's VMs
        assert_eq!(depth("fence-1"), Some(depth("h1").map_or(99, |d| d + 1)));
        assert!(at("fence-1") < at("ha"));
        let headings: Vec<&str> = rows.iter().filter_map(|r| if let TreeItem::Heading(h) = r { Some(*h) } else { None }).collect();
        assert_eq!(headings, ["Users and permissions", "Affinity groups", "Backups"]);
        // user, then its permission one level deeper; groups and backups under their headings
        assert_eq!(depth("user-1"), Some(1));
        assert_eq!(depth("perm-1"), Some(2));
        assert!(at("user-1") > at("plain"));
        assert!(at("group-1") > at("perm-1") && at("backup-1") > at("group-1"));
        // each object once, nothing left over
        assert_eq!(rows.iter().filter(|r| matches!(r, TreeItem::Node { .. })).count(), t.nodes.len());
        // a permission nobody is granted is loose
        let mut t2 = busy();
        t2.edges.retain(|e| !(e.from == "user-1"));
        let rows = tree(&t2, &evaluated(&t2));
        let loose = rows.iter().position(|r| matches!(r, TreeItem::Heading(h) if *h == "Not in the hierarchy yet"));
        assert!(loose.is_some());
        assert!(rows.iter().position(|r| matches!(r, TreeItem::Node { id, .. } if id == "perm-1")) > loose);
    }

    #[test]
    fn a_fence_path_highlights_the_agent_and_the_proxy() {
        let _en = en();
        let t = busy();
        let ev = evaluated(&t);
        let tr = trace(&t, &ev, &Op::Fence { host: "h1".into() });
        assert!(tr.ok);
        let v = path_view(&t, &tr, None);
        assert_eq!(v.edges.get(&("fence-1".to_owned(), "h1".to_owned())), Some(&true), "the agent → host link lights up");
        assert_eq!(v.edges.get(&("mgmt".to_owned(), "h2".to_owned())), Some(&true), "the engine reaches the proxy over the management network");
        assert_eq!(v.nodes.get("h2"), Some(&true));
        assert!(!v.nodes.contains_key("h1") || v.nodes.get("h1") == Some(&true));
        // without an agent the path breaks at the host: a missing line
        let mut bare = t.clone();
        bare.edges.retain(|e| e.from != "fence-1");
        let tr = trace(&bare, &evaluated(&bare), &Op::Fence { host: "h1".into() });
        assert!(!tr.ok);
        assert!(tr.hops.last().is_some_and(|h| !h.ok && h.text.contains("no fence agent")));
        let v = path_view(&bare, &tr, None);
        assert_eq!(v.nodes.get("h1"), Some(&false));
        assert!(!v.missing.is_empty());
    }

    #[test]
    fn edges_of_the_new_relations_have_labels_and_take_their_direction_from_the_model() {
        let _en = en();
        let t = busy();
        let label = |a: &str, b: &str| edge_rel(&t, &Edge::new(a, b)).map(|r| r.label());
        assert_eq!(label("fence-1", "h1"), Some("power management of the host"));
        assert_eq!(label("group-1", "ha"), Some("member of the affinity group"));
        assert_eq!(label("ha", "backup-1"), Some("backed up by"));
        assert_eq!(label("user-1", "perm-1"), Some("granted"));
        assert_eq!(label("perm-1", "cl1"), Some("applies to"));
        assert_eq!(label("nfs", "copy"), Some("replicated to"));
        // joining from either end gives the model direction
        assert_eq!(normalize_link(&t, "h1", "fence-1"), Some(("fence-1".to_owned(), "h1".to_owned())));
        assert_eq!(normalize_link(&t, "backup-1", "plain"), Some(("plain".to_owned(), "backup-1".to_owned())));
        assert_eq!(link_check(&t, "plain", "backup-1"), Ok(("plain".to_owned(), "backup-1".to_owned())));
        assert_eq!(link_check(&t, "h2", "fence-1"), Ok(("fence-1".to_owned(), "h2".to_owned())), "an agent may serve several hosts");
        assert!(link_check(&t, "h1", "ha").is_err(), "already placed");
        // a replica link between two domains: both ends are domains, the pin order decides
        let mut t = t;
        put(&mut t, "dom3", Kind::StorageDomain, &[]);
        assert_eq!(link_check(&t, "nfs", "dom3"), Ok(("nfs".to_owned(), "dom3".to_owned())));
        assert!(link_check(&t, "copy", "dom3").is_err(), "a replica is not replicated further");
    }

    #[test]
    fn names_are_cut_for_the_board_and_limited_for_the_model() {
        let _ru = ru();
        assert_eq!(short_name("host-1"), "host-1");
        assert_eq!(short_name("a-very-long-host-name"), "a-very-long-…");
        assert_eq!(short_name("a-very-long-host-name").chars().count(), 13);
        assert_eq!(clamp_name(&"x".repeat(100)).chars().count(), MAX_NAME);
        assert_eq!(clamp_name("héllo"), "héllo");
    }

    #[test]
    fn nodes_under_the_cursor_exclude_the_origin() {
        let _ru = ru();
        let t = default_solution().remove("storage").unwrap_or_default();
        let dc = t.node("dc1").cloned().unwrap_or_else(|| Node::new("", Kind::Host, "", 0.0, 0.0));
        assert_eq!(node_at(&t, "h1", Point::new(dc.x + 5.0, dc.y)).as_deref(), Some("dc1"));
        assert_eq!(node_at(&t, "dc1", Point::new(dc.x + 5.0, dc.y)), None);
        assert_eq!(node_at(&t, "h1", Point::new(-500.0, -500.0)), None);
    }
}
