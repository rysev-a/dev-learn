//! Pure logic of the Linux network board: the draft, adding and removing objects, links and their direction, wires on the board, fitting, statuses of
//! objects, the tree of namespaces and interfaces and the path of a message. No signals or DOM — everything is checked by ordinary tests; the
//! interface (`board.rs`, `panels.rs`, `lab.rs`) only calls these functions, and takes the rules and statuses from the `virtlab::net_board`
//! model (shared with the server).

use std::collections::{BTreeMap, BTreeSet};

use serde_json::Value;
use virtlab::net_board::{
    connect_error, net_label, prune, rel, Edge, Evaluation, IfaceStatus, Kind, Node, Op, Rel, Scenario, Topology, Trace, MAX_NAME,
};

use crate::components::labs::board_view::{js_round, BoardConfig, Bounds, Point, View};


/// Identifier of the "ghost" palette object before it is placed on the board.
pub const GHOST: &str = "__new__";
/// Width and height of an object on the board (board units).
pub const NODE_W: f64 = virtlab::net_board::NODE_W;
pub const NODE_H: f64 = virtlab::net_board::NODE_H;
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
                .filter(|t| virtlab::net_board::problems(t).is_empty())
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
    virtlab::net_board::next_pos(t, kind)
}

fn id_prefix(kind: Kind) -> &'static str {
    match kind {
        Kind::Netns => "ns",
        Kind::Eth => "eth",
        Kind::Veth => "veth",
        Kind::Bridge => "br",
        Kind::Bond => "bond",
        Kind::Vlan => "vlan",
        Kind::Vm => "vm",
        Kind::External => "net",
        Kind::Nat => "nat",
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
        None => Err(connect_error(t, a, b).unwrap_or_else(|| i18n::tr("these objects are not linked directly").to_owned())),
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

/// The straight line of a link the path needs but the board lacks.
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
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub struct NodeInfo {
    pub chip: Option<Chip>,
    /// the text in the corner: the address, the VLAN tag, `ip_forward`, the network
    pub badge: String,
    /// the badge is a warning: an interface without a link
    pub warn: bool,
}

fn iface_chip(s: IfaceStatus) -> Chip {
    let class = match s {
        IfaceStatus::Ok => "ok",
        IfaceStatus::Down => "warn",
        IfaceStatus::NoCarrier => "bad",
    };
    Chip { class, text: s.name() }
}

fn tag_text(n: &Node) -> String {
    match n.access_vlan() {
        0 => String::new(),
        v => i18n::trf!("VLAN {0}", v),
    }
}

/// Chip and badge of an object.
pub fn node_info(t: &Topology, ev: &Evaluation, id: &str) -> NodeInfo {
    let Some(n) = t.node(id) else { return NodeInfo::default() };
    match n.kind {
        Kind::Netns => NodeInfo { badge: if n.flag("forward") { i18n::tr("forwarding").to_owned() } else { String::new() }, ..NodeInfo::default() },
        Kind::External => NodeInfo { badge: net_label(&n.net()).to_owned(), ..NodeInfo::default() },
        Kind::Nat => NodeInfo { badge: if n.param_text("kind") == "dnat" { i18n::tr("DNAT").to_owned() } else { i18n::tr("masquerade").to_owned() }, ..NodeInfo::default() },
        _ => ev.iface(id).map_or_else(NodeInfo::default, |i| {
            let badge = match (&i.addr, i.enslaved) {
                (Some(a), _) => format!("{a}/24"),
                (None, true) => tag_text(n),
                (None, false) => String::new(),
            };
            NodeInfo { chip: Some(iface_chip(i.status)), badge, warn: i.status != IfaceStatus::Ok }
        }),
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
        Kind::Netns => i18n::tr("A network namespace is an isolated set of interfaces, addresses and routes; the host itself is one."),
        Kind::Eth => i18n::tr("A physical interface: it has a link only when it is up and cabled to the outside network."),
        Kind::Veth => i18n::tr("One end of a veth pair: a virtual cable. Both ends must be up, otherwise neither has a link."),
        Kind::Bridge => i18n::tr("A bridge is a software switch: its ports share one segment (ports with different VLAN tags do not)."),
        Kind::Bond => i18n::tr("A bond joins physical interfaces into one: it has a link while one slave has (an 802.3ad bond needs one switch)."),
        Kind::Vlan => i18n::tr("A VLAN interface sits on the tagged frames of its parent interface."),
        Kind::Vm => i18n::tr("A VM: its tap device is a port of a bridge, and the guest holds the address."),
        Kind::External => i18n::tr("The outside network: it answers only addresses it knows, so private networks need NAT."),
        Kind::Nat => i18n::tr("A NAT rule of a namespace: masquerade lets private hosts out, DNAT lets a published port in."),
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

fn names(nodes: &[&Node]) -> String {
    nodes.iter().map(|n| n.name.clone()).collect::<Vec<_>>().join(", ")
}

/// Everything the inspector says about an object besides its name and parameters.
pub fn explain(t: &Topology, ev: &Evaluation, id: &str) -> Explain {
    let info = node_info(t, ev, id);
    let Some(n) = t.node(id) else { return Explain { info, lines: vec![] } };
    let mut lines = vec![about(n.kind).to_owned()];
    match n.kind {
        Kind::Netns => {
            let inside = t.targets(id, Rel::Lives);
            lines.push(if inside.is_empty() { i18n::tr("No interfaces in it yet.").to_owned() } else { i18n::trf!("Interfaces: {0}.", names(&inside)) });
            lines.push(if n.flag("forward") {
                i18n::tr("Forwarding is on: it can pass packets between its networks (a router).").to_owned()
            } else {
                i18n::tr("Forwarding is off: it answers only packets addressed to itself.").to_owned()
            });
        }
        Kind::External => {
            lines.push(i18n::trf!("Network {0}; the address of the outside host is .254.", net_label(&n.net())));
        }
        Kind::Nat => {
            if let Some(ns) = t.targets(id, Rel::On).first() {
                lines.push(i18n::trf!("Rule of the namespace “{0}”.", ns.name));
            } else {
                lines.push(i18n::tr("The rule belongs to no namespace yet.").to_owned());
            }
            if n.param_text("kind") == "dnat" {
                let to = t.targets(id, Rel::Forwards);
                lines.push(if to.is_empty() { i18n::tr("It forwards to nobody yet: link it to the host inside.").to_owned() } else { i18n::trf!("Forwards the published port to “{0}”.", names(&to)) });
            }
        }
        _ => {
            if let Some(i) = ev.iface(id) {
                lines.extend(i.why.iter().map(|w| w.text()));
                lines.push(match (&i.addr, i.enslaved) {
                    (Some(a), _) => i18n::trf!("Address {0}/24 in the segment {1}.", a, i.segment),
                    (None, true) => i18n::tr("It is a port or a slave: the address belongs to the bridge or the bond.").to_owned(),
                    (None, false) => i18n::tr("No address that works.").to_owned(),
                });
            }
            lines.push(match t.netns_of(id) {
                Some(ns) => i18n::trf!("Lives in the namespace “{0}”.", ns.name),
                None if n.kind == Kind::Vm => i18n::tr("The guest has its own namespace.").to_owned(),
                None => i18n::tr("Lives in no namespace yet.").to_owned(),
            });
            if let Some(br) = t.bridge_of(id) {
                lines.push(i18n::trf!("Port of the bridge “{0}”.", br.name));
            }
            if let Some(bond) = t.bond_of(id) {
                lines.push(i18n::trf!("Slave of the bond “{0}”.", bond.name));
            }
            if n.kind == Kind::Veth {
                lines.push(match t.peer_of(id) {
                    Some(p) => i18n::trf!("The other end of the pair: “{0}”.", p.name),
                    None => i18n::tr("The other end of the pair is not on the board.").to_owned(),
                });
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

// --- the tree of namespaces and interfaces -----------------------------------------------------------------------

/// A row of the tree.
#[derive(Clone, Debug, PartialEq)]
pub enum TreeItem {
    /// A heading over objects that are not in a namespace yet.
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

    /// An interface with what hangs on it: the ports of a bridge, the slaves of a bond, the VLAN interfaces on a NIC or a bond.
    fn iface(&mut self, depth: usize, n: &Node) {
        let t = self.t;
        self.node(depth, n);
        let members: Vec<&Node> = match n.kind {
            Kind::Bridge => t.sources(&n.id, Rel::Port).into_iter().chain(t.sources(&n.id, Rel::Tap)).collect(),
            Kind::Bond => t.sources(&n.id, Rel::Slave).into_iter().chain(t.targets(&n.id, Rel::Parent)).collect(),
            Kind::Eth => t.targets(&n.id, Rel::Parent),
            _ => vec![],
        };
        for m in members {
            self.iface(depth + 1, m);
        }
    }
}

/// The tree derived from the links: namespace › its interfaces (with the ports, slaves and VLAN interfaces under them) and rules; the outside network,
/// VMs and objects that are in no namespace yet are listed at the end.
pub fn tree(t: &Topology, ev: &Evaluation) -> Vec<TreeItem> {
    let mut b = TreeBuilder { t, ev, out: vec![], seen: BTreeSet::new() };
    for ns in t.of_kind(Kind::Netns) {
        b.node(0, ns);
        for i in t.targets(&ns.id, Rel::Lives) {
            // a port is listed under its bridge or bond, not twice
            if t.bridge_of(&i.id).is_none() && t.bond_of(&i.id).is_none() {
                b.iface(1, i);
            }
        }
        for rule in t.sources(&ns.id, Rel::On) {
            b.node(1, rule);
        }
    }
    let loose: Vec<&Node> = t.nodes.iter().filter(|n| !b.seen.contains(&n.id)).collect();
    if !loose.is_empty() {
        b.out.push(TreeItem::Heading(i18n::tr("Outside the namespaces")));
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

/// The hosts a message can be sent from or to: namespaces, VMs and the outside network.
pub fn hosts(t: &Topology) -> Vec<(String, String)> {
    t.nodes.iter().filter(|n| n.kind.is_host()).map(|n| (n.id.clone(), n.name.clone())).collect()
}

/// The published ports of the board: the outside network and the target of every DNAT rule that forwards somewhere.
pub fn publications(t: &Topology) -> Vec<Op> {
    let Some(external) = t.of_kind(Kind::External).next() else { return vec![] };
    t.of_kind(Kind::Nat)
        .filter(|r| r.param_text("kind") == "dnat")
        .flat_map(|r| t.targets(&r.id, Rel::Forwards))
        .map(|target| Op::Publish { external: external.id.clone(), target: target.id.clone() })
        .collect()
}

/// `data-op` of an operation button.
pub fn op_name(op: &Op) -> &'static str {
    match op {
        Op::Ping { .. } => "ping",
        Op::Publish { .. } => "publish",
    }
}

/// Text of an operation button for a publication.
pub fn publish_label(t: &Topology, op: &Op) -> String {
    match op {
        Op::Publish { external, target } => i18n::trf!("Connect from “{0}” to “{1}”", name_of(t, external), name_of(t, target)),
        Op::Ping { from, to } => i18n::trf!("Ping from “{0}” to “{1}”", name_of(t, from), name_of(t, to)),
    }
}

#[cfg(test)]
mod tests {
    use virtlab::net_board::{evaluate as evaluated, pack, problems, trace, Param};

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
        let sc = scenarios("virt-sim-net-bridge");
        let mut boards = restore(&sc, "");
        for (b, s) in boards.iter().zip(&sc) {
            assert_eq!(*b, s.start, "{}", s.id);
        }
        let id = add_node(&mut boards[0], Kind::Netns, None);
        let text = draft_json(&sc.iter().zip(&boards).map(|(s, b)| (s.id.clone(), b.clone())).collect::<Vec<_>>());
        let back = restore(&sc, &text);
        assert_eq!(back, boards);
        assert!(back[0].node(&id).is_some());
    }

    #[test]
    fn restore_tolerates_garbage_and_unknown_ids() {
        let _ru = ru();
        let sc = scenarios("virt-sim-net-bridge");
        let starts: Vec<Topology> = sc.iter().map(|s| s.start.clone()).collect();
        let first = sc[0].id.clone();
        for draft in ["", "null", "[]", "42", "not json", "{", r#"{"nope": {"nodes": [], "edges": []}}"#] {
            assert_eq!(restore(&sc, draft), starts, "{draft:?}");
        }
        let broken = format!(r#"{{"{first}": {{"nodes": 1}}}}"#);
        assert_eq!(restore(&sc, &broken), starts);
    }

    #[test]
    fn restore_drops_boards_that_break_the_rules_and_keeps_the_references() {
        let _ru = ru();
        let sc = scenarios("virt-sim-net-nat");
        let mut t = Topology::default();
        add_node(&mut t, Kind::Netns, None);
        t.edges.push(Edge::new("ns1", "nobody"));
        let text = draft_json(&[(sc[0].id.clone(), t)]);
        assert_eq!(restore(&sc, &text)[0], sc[0].start);
        let all: Vec<(String, Topology)> = pack("virt-sim-net-nat").map(|p| p.1.into_iter().collect()).unwrap_or_default();
        let back = restore(&sc, &draft_json(&all));
        for (s, b) in sc.iter().zip(&back) {
            assert!(s.reached(b), "{}", s.id);
        }
    }

    #[test]
    fn new_objects_get_free_places_ids_and_names() {
        let _en = en();
        let mut t = Topology::default();
        let a = add_node(&mut t, Kind::Veth, None);
        let b = add_node(&mut t, Kind::Veth, None);
        assert_eq!((a.as_str(), b.as_str()), ("veth1", "veth2"));
        assert_eq!(t.nodes[0].name, "veth-1");
        assert_ne!((t.nodes[0].x, t.nodes[0].y), (t.nodes[1].x, t.nodes[1].y));
        let c = add_node(&mut t, Kind::Eth, Some(Point::new(5.0, 6.0)));
        assert_eq!(t.node(&c).map(|n| (n.x, n.y)), Some((5.0, 6.0)));
        let mut all = Topology::default();
        for k in Kind::ALL.into_iter().chain([Kind::Veth, Kind::Netns]) {
            add_node(&mut all, k, None);
        }
        for (i, a) in all.nodes.iter().enumerate() {
            for b in &all.nodes[i + 1..] {
                assert!((a.x - b.x).abs() >= NODE_W || (a.y - b.y).abs() >= NODE_H, "{} and {} overlap", a.id, b.id);
            }
        }
        assert!(problems(&all).is_empty());
        assert!(all.nodes.iter().all(|n| n.params.is_empty()));
        remove_node(&mut all, "veth1");
        assert_eq!(new_id(&all, Kind::Veth), "veth1");
    }

    #[test]
    fn the_inspector_keeps_the_field_order_the_e2e_relies_on() {
        let _en = en();
        use virtlab::net_board::{param_specs, ParamTy};
        let keys = |k: Kind| param_specs(k).into_iter().map(|s| s.key).collect::<Vec<_>>();
        assert_eq!(keys(Kind::Netns), ["forward"]);
        assert_eq!(keys(Kind::Eth), ["net", "up", "access_vlan", "default_route"]);
        assert_eq!(keys(Kind::Bond)[0], "mode");
        assert!(matches!(param_specs(Kind::Netns)[0].ty, ParamTy::Bool));
        assert_eq!(keys(Kind::Nat), ["kind"]);
    }

    #[test]
    fn links_are_normalised_to_the_direction_of_the_model() {
        let _ru = ru();
        let t = solution("virt-sim-net-nat", "build");
        assert_eq!(normalize_link(&t, "br0", "masq"), None, "a bridge and a NAT rule are not linked");
        assert_eq!(normalize_link(&t, "host", "eth0"), Some(("host".to_owned(), "eth0".to_owned())));
        assert_eq!(normalize_link(&t, "eth0", "host"), Some(("host".to_owned(), "eth0".to_owned())));
        assert!(link_check(&t, "host", "eth0").is_err(), "the interface already lives in the namespace");
        assert!(link_check(&t, "ns1", "eth0").is_err(), "an interface lives in one namespace");
        assert!(link_check(&t, "br0", "masq").is_err());
        assert!(link_check(&t, "nobody", "br0").is_err());
        for k in [Kind::Eth, Kind::Veth, Kind::Vlan] {
            assert!(has_in(k) && has_out(k), "{k:?}");
        }
        assert!(has_in(Kind::Bridge) && !has_out(Kind::Bridge));
        assert!(has_out(Kind::Netns) && has_in(Kind::Netns), "the rules of a namespace link to it");
        assert!(has_in(Kind::External) && !has_out(Kind::External));
    }

    #[test]
    fn a_wire_follows_the_link_it_would_make() {
        let _ru = ru();
        let t = solution("virt-sim-net-nat", "build");
        let from_eth = Pending { id: "eth0".into(), pin: Pin::Out };
        assert_eq!(port_state(&t, Some(&from_eth), "eth0"), PortState::Idle);
        assert_eq!(port_state(&t, None, "br0"), PortState::Idle);
        let (d, tone) = pending_wire(&t, &from_eth, Some("masq"), None).expect("wire");
        assert_eq!(tone, "bad");
        assert!(d.starts_with('M'));
        assert_eq!(pending_wire(&t, &from_eth, None, Some(Point::new(1.0, 2.0))).map(|w| w.1), Some(""));
        assert_eq!(pending_wire(&t, &from_eth, None, None), None);
    }

    #[test]
    fn deleting_reports_the_dependent_links() {
        let _ru = ru();
        let mut t = solution("virt-sim-net-nat", "build");
        let before = t.edges.len();
        remove_node(&mut t, "br0");
        assert!(t.node("br0").is_none() && t.edges.iter().all(|e| e.from != "br0" && e.to != "br0"));
        assert!(t.edges.len() < before);
        assert!(problems(&t).is_empty());
    }

    #[test]
    fn long_links_arch_and_short_ones_do_not() {
        let _ru = ru();
        let (flat, mid) = wire(Point::new(0.0, 100.0), Point::new(100.0, 100.0));
        assert!(flat.starts_with("M0.0 100.0 C"));
        assert_eq!(mid.y, 100.0);
        let (_, arch) = wire(Point::new(0.0, 100.0), Point::new(240.0, 100.0));
        assert!(arch.y < 100.0 - 28.0, "{}", arch.y);
    }

    #[test]
    fn fit_shows_every_object() {
        let _ru = ru();
        assert_eq!(fit_view(&[], 520.0), BOARD.home_view());
        for pack_id in ["virt-sim-net-bridge", "virt-sim-net-bond", "virt-sim-net-nat"] {
            for sc in scenarios(pack_id) {
                let pts: Vec<Point> = sc.start.nodes.iter().map(|n| Point::new(n.x, n.y)).collect();
                let v = fit_view(&pts, 520.0);
                assert!(v.zoom >= BOARD.zoom_min && v.zoom <= 1.6, "{}", sc.id);
                for p in &pts {
                    let (x, y) = ((p.x - v.pan.x) * v.zoom, (p.y - v.pan.y) * v.zoom);
                    assert!(x > 0.0 && x < BOARD_W && y > 0.0 && y < 520.0, "{}: {p:?} -> {x} {y}", sc.id);
                }
            }
        }
        assert_eq!(world_height(0.0, 0.0), BOARD_H);
    }

    #[test]
    fn statuses_and_badges_come_from_the_evaluation() {
        let _en = en();
        let t = solution("virt-sim-net-nat", "build");
        let ev = evaluated(&t);
        let info = |id: &str| node_info(&t, &ev, id);
        assert_eq!(info("host").badge, "forwarding");
        assert_eq!(info("masq").badge, "masquerade");
        assert_eq!(info("net").badge, "10.0.1.0/24");
        assert_eq!(info("v1c").chip.map(|c| c.class), Some("ok"));
        assert!(info("v1c").badge.ends_with("/24"), "{}", info("v1c").badge);
        assert_eq!(status_class(&info("v1c")), "ok");
        assert_eq!(status_class(&info("host")), "idle");
        // an interface that is down
        let mut down = t.clone();
        if let Some(n) = down.nodes.iter_mut().find(|n| n.id == "v1h") {
            n.params.insert("up".into(), Param::Bool(false));
        }
        let ev = evaluated(&down);
        assert_eq!(node_info(&down, &ev, "v1h").chip.map(|c| c.class), Some("warn"));
        // every object kind of every scenario explains itself
        for pack_id in ["virt-sim-net-bridge", "virt-sim-net-bond", "virt-sim-net-nat"] {
            for sc in scenarios(pack_id) {
                let ev = sc.evaluate(&sc.start);
                for n in &sc.start.nodes {
                    assert!(explain(&sc.start, &ev, &n.id).lines.len() >= 2, "{}: {}", sc.id, n.id);
                }
            }
        }
        assert!(explain(&t, &ev, "nobody").lines.is_empty());
    }

    #[test]
    fn the_tree_follows_the_links_and_lists_the_rest() {
        let _en = en();
        let t = solution("virt-sim-net-nat", "build");
        let ev = evaluated(&t);
        let rows = tree(&t, &ev);
        let depth_of = |id: &str| {
            rows.iter().find_map(|r| match r {
                TreeItem::Node { depth, id: i, .. } if i == id => Some(*depth),
                _ => None,
            })
        };
        assert_eq!(depth_of("host"), Some(0));
        assert_eq!(depth_of("eth0"), Some(1));
        assert_eq!(depth_of("br0"), Some(1));
        assert_eq!(depth_of("v1h"), Some(2), "a port is listed under its bridge");
        assert_eq!(depth_of("ns1"), Some(0));
        assert_eq!(depth_of("v1c"), Some(1));
        assert_eq!(depth_of("masq"), Some(1));
        assert_eq!(rows.iter().filter(|r| matches!(r, TreeItem::Node { .. })).count(), t.nodes.len(), "each object once");
        let mut half = Topology::default();
        add_node(&mut half, Kind::Netns, None);
        add_node(&mut half, Kind::Veth, None);
        let rows = tree(&half, &evaluated(&half));
        assert!(matches!(rows[0], TreeItem::Node { depth: 0, kind: Kind::Netns, .. }));
        assert!(matches!(rows[1], TreeItem::Heading(_)));
    }

    #[test]
    fn the_path_marks_what_works_and_what_is_missing() {
        let _en = en();
        let t = solution("virt-sim-net-nat", "build");
        let ev = evaluated(&t);
        let tr = trace(&t, &ev, &Op::Ping { from: "ns1".into(), to: "net".into() });
        assert!(tr.ok);
        let all = path_view(&t, &tr, None);
        assert!(all.nodes.values().all(|ok| *ok) && !all.nodes.is_empty());
        assert!(all.missing.is_empty());
        let first = path_view(&t, &tr, Some(0));
        assert!(first.nodes.len() <= all.nodes.len());
        // the same ping on a board without the masquerade rule breaks at the router
        let mut broken = t.clone();
        broken.nodes.retain(|n| n.id != "masq");
        broken.edges.retain(|e| e.from != "masq" && e.to != "masq");
        let ev = evaluated(&broken);
        let tr = trace(&broken, &ev, &Op::Ping { from: "ns1".into(), to: "net".into() });
        assert!(!tr.ok);
        let v = path_view(&broken, &tr, None);
        assert!(v.nodes.values().any(|ok| !*ok), "{v:?}");
        assert_eq!(shown_hops(&tr, None), tr.hops.len());
        assert_eq!(shown_hops(&tr, Some(0)), 1);
        assert_eq!(shown_hops(&tr, Some(99)), tr.hops.len());
    }

    #[test]
    fn operations_come_from_the_board() {
        let _en = en();
        let t = solution("virt-sim-net-nat", "publish");
        let hosts = hosts(&t);
        assert!(hosts.iter().any(|(id, _)| id == "ns1") && hosts.iter().any(|(id, _)| id == "net"));
        assert!(!hosts.iter().any(|(id, _)| id == "eth0"));
        let pubs = publications(&t);
        assert_eq!(pubs, [Op::Publish { external: "net".into(), target: "v1c".into() }]);
        assert_eq!(op_name(&pubs[0]), "publish");
        assert_eq!(op_name(&Op::Ping { from: "a".into(), to: "b".into() }), "ping");
        assert!(publish_label(&t, &pubs[0]).contains("v1c") || publish_label(&t, &pubs[0]).contains("veth"));
        assert!(publications(&solution("virt-sim-net-nat", "build")).is_empty());
        assert!(publications(&Topology::default()).is_empty());
        let ev = evaluated(&t);
        assert!(trace(&t, &ev, &pubs[0]).ok);
    }

    #[test]
    fn names_are_cut_for_the_board_and_limited_for_the_model() {
        let _ru = ru();
        assert_eq!(short_name("eth0"), "eth0");
        assert_eq!(short_name("a-very-long-host-name"), "a-very-long-…");
        assert_eq!(short_name("a-very-long-host-name").chars().count(), 13);
        assert_eq!(clamp_name(&"x".repeat(100)).chars().count(), MAX_NAME);
    }

    #[test]
    fn nodes_under_the_cursor_exclude_the_origin() {
        let _ru = ru();
        let t = solution("virt-sim-net-nat", "build");
        let br = t.node("br0").cloned().unwrap_or_else(|| Node::new("", Kind::Eth, "", 0.0, 0.0));
        assert_eq!(node_at(&t, "eth0", Point::new(br.x + 5.0, br.y)).as_deref(), Some("br0"));
        assert_eq!(node_at(&t, "br0", Point::new(br.x + 5.0, br.y)), None);
        assert_eq!(node_at(&t, "eth0", Point::new(-500.0, -500.0)), None);
    }
}
