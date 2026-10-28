//! Pure logic of the "System design" lab: draft, adding and removing components, wires on the board, fitting the
//! diagram into the viewport and labels. No signals or DOM — everything is checked by ordinary tests; the interface (`board.rs`, `panels.rs`, `lab.rs`)
//! only calls these functions, and takes the calculation and link validity from the `sdlab` crate.

use std::collections::BTreeMap;

use sdlab::{
    jsfmt, kinds,
    layout::{self, BOARD_W},
    ports::{self, in_pos, out_pos, wire_path, Pt, NODE_H, NODE_W},
    reference as r, FailKind, Kind, ParamValue, Scenario, SdEdge, SdNode, SdState, Workload,
};
use serde_json::{json, Value};

use crate::components::labs::board_view::{js_round, BoardConfig, Bounds, Point, View};

/// Identifier of the "ghost" palette component in link lists before it is placed on the board.
pub const GHOST: &str = "__new__";
/// How far from the origin a component may be carried.
pub const WORLD: f64 = 2600.0;
/// Board pan and zoom: 30–300 %, integer pan, components no farther than `WORLD` from the origin.
pub const BOARD: BoardConfig = BoardConfig { items: Bounds::symmetric(WORLD), ..BoardConfig::DEFAULT };
/// Limits of the board height chosen with the grip (px).
pub const MIN_H: f64 = 240.0;
pub const MAX_H: f64 = 1600.0;
/// Component shift (board units) below which a press stays a selection rather than a drag.
pub const MOVE_SLOP: f64 = 6.0;

fn pt(p: Point) -> Pt {
    Pt { x: p.x, y: p.y }
}

// --- exercise and draft ----------------------------------------------------------------------

/// Parses the exercise data. The server does not send the reference solution — the `solution` key is added empty if needed.
pub fn parse_scenario(spec: &Value) -> Result<Scenario, String> {
    let mut value = spec.clone();
    if let Some(obj) = value.as_object_mut() {
        obj.entry("solution").or_insert_with(|| json!({ "nodes": [], "edges": [] }));
    }
    serde_json::from_value(value).map_err(|e| i18n::trf!("Failed to parse the exercise: {0}", e))
}

/// Diagram with components and names laid out.
fn prepared(mut state: SdState) -> SdState {
    state.normalize();
    layout::place(&state)
}

/// Initial diagram of the exercise.
pub fn initial_state(sc: &Scenario) -> SdState {
    prepared(sc.start.clone())
}

/// Old draft with overlapping nodes: lay out by columns again.
fn tidy(state: SdState) -> SdState {
    let crowded = state.nodes.iter().enumerate().any(|(i, a)| state.nodes.iter().skip(i + 1).any(|b| (a.x - b.x).abs() < NODE_W && (a.y - b.y).abs() < NODE_H));
    if !crowded {
        return state;
    }
    let reset = SdState { nodes: state.nodes.iter().map(|n| SdNode { x: -1.0, y: -1.0, ..n.clone() }).collect(), edges: state.edges };
    layout::place(&reset)
}

/// Diagram from a draft; empty, corrupt or without users — the exercise's initial diagram.
pub fn restore(sc: &Scenario, draft: &str) -> SdState {
    if draft.trim().is_empty() {
        return initial_state(sc);
    }
    match serde_json::from_str::<SdState>(draft) {
        Ok(s) if s.nodes.iter().any(|n| n.kind == Kind::Clients) => tidy(prepared(s)),
        _ => initial_state(sc),
    }
}

/// JSON string of the diagram: both the draft in the cabinet and the solution the server re-checks.
pub fn draft_json(state: &SdState) -> String {
    serde_json::to_string(state).unwrap_or_default()
}

// --- diagram edits -------------------------------------------------------------------------------

/// Free identifier for a new component: `<kind><number>`.
pub fn new_node_id(state: &SdState, kind: Kind) -> String {
    (1..).map(|i| format!("{}{i}", kind.as_str())).find(|id| state.node(id).is_none()).unwrap_or_default()
}

/// Places a component: at point `at` or in a free spot of its column, together with links `edges` (the end `GHOST` stands for
/// the new component itself). Returns the new component's identifier.
pub fn add_node(state: &mut SdState, kind: Kind, at: Option<Point>, edges: &[SdEdge]) -> String {
    let id = new_node_id(state, kind);
    let spec = kinds::spec(kind);
    let same = state.nodes.iter().filter(|n| n.kind == kind).count();
    let name = if same > 0 { format!("{} {}", spec.label, same + 1) } else { spec.label.to_owned() };
    let (x, y) = match at {
        Some(p) => (p.x, p.y),
        None => (layout::col_x(spec.col), layout::next_y(state, spec.col)),
    };
    let from_ghost = |s: &str| if s == GHOST { id.clone() } else { s.to_owned() };
    let links: Vec<SdEdge> = edges.iter().map(|e| SdEdge { from: from_ghost(&e.from), to: from_ghost(&e.to) }).collect();
    state.nodes.push(SdNode { id: id.clone(), kind, name, x, y, params: kinds::default_params(kind) });
    for e in links {
        add_edge(state, e);
    }
    id
}

/// Adds a link if there is none yet.
pub fn add_edge(state: &mut SdState, edge: SdEdge) {
    if !state.edges.contains(&edge) {
        state.edges.push(edge);
    }
}

/// Removes a component together with its links.
pub fn remove_node(state: &mut SdState, id: &str) {
    state.nodes.retain(|n| n.id != id);
    state.edges.retain(|e| e.from != id && e.to != id);
}

/// Whether a component can be deleted: users cannot be removed from the diagram.
pub fn deletable(state: &SdState, id: &str) -> bool {
    state.node(id).is_some_and(|n| n.kind != Kind::Clients)
}

/// Value of an integer parameter within limits, as in the component panel (0 to 1e9 by default); `None` — not a number.
pub fn clamp_int(text: &str, min: Option<f64>, max: Option<f64>) -> Option<f64> {
    let x = js_round(text.trim().parse::<f64>().ok().filter(|x| x.is_finite())?);
    Some(x.min(max.unwrap_or(1e9)).max(min.unwrap_or(0.0)))
}

// --- board: fitting, wires --------------------------------------------------------------------

/// Window height for the board: fullscreen and with a chosen height — by viewport proportions, otherwise as the regular board.
pub fn world_height(sized: bool, width_px: f64, height_px: f64) -> f64 {
    if sized && width_px > 0.0 && height_px > 0.0 {
        BOARD_W * height_px / width_px
    } else {
        layout::BOARD_H
    }
}

/// Pan and zoom that make the whole diagram visible in a window of height `world_h` with margins; an empty diagram — the initial view.
pub fn fit_view(nodes: &[Point], world_h: f64) -> View {
    if nodes.is_empty() {
        return BOARD.home_view();
    }
    let pad = 30.0;
    let fold = |f: fn(f64, f64) -> f64, init: f64, g: fn(&Point) -> f64| nodes.iter().map(g).fold(init, f);
    let min_x = fold(f64::min, f64::INFINITY, |p| p.x) - NODE_W / 2.0 - pad;
    let max_x = fold(f64::max, f64::NEG_INFINITY, |p| p.x) + NODE_W / 2.0 + pad;
    let min_y = fold(f64::min, f64::INFINITY, |p| p.y) - NODE_H / 2.0 - pad;
    let max_y = fold(f64::max, f64::NEG_INFINITY, |p| p.y) + NODE_H / 2.0 + pad;
    let (bw, bh) = (max_x - min_x, max_y - min_y);
    let zoom = 1.6_f64.min(BOARD_W / bw).min(world_h / bh).max(BOARD.zoom_min);
    View { zoom, pan: Point::new(js_round(min_x + bw / 2.0 - BOARD_W / zoom / 2.0), js_round(min_y + bh / 2.0 - world_h / zoom / 2.0)) }
}

/// Where a wire is dragged from: an output port or an input port.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Pin {
    In,
    Out,
}

/// Wire dragged from a port of component `id`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Pending {
    pub id: String,
    pub pin: Pin,
}

/// How a port looks while a wire is being dragged.
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

/// Link `from → to` for a wire from `pend` to component `other`.
pub fn pin_edge(pend: &Pending, other: &str) -> (String, String) {
    match pend.pin {
        Pin::Out => (pend.id.clone(), other.to_owned()),
        Pin::In => (other.to_owned(), pend.id.clone()),
    }
}

/// Reason why a wire from `pend` cannot be connected to `other`; `None` — it can (or there are no components).
pub fn link_error(state: &SdState, pend: &Pending, other: &str) -> Option<String> {
    let (me, other) = (state.node(&pend.id)?, state.node(other)?);
    match pend.pin {
        Pin::Out => ports::connect_error(state, me, other),
        Pin::In => ports::connect_error(state, other, me),
    }
}

/// Component under point `p` (frame with a margin of 10): the nearest one, other than the one the wire is dragged from.
pub fn node_at(state: &SdState, from: &str, p: Point) -> Option<String> {
    let dist = |n: &SdNode| (p.x - n.x).hypot(p.y - n.y);
    state
        .nodes
        .iter()
        .filter(|n| n.id != from && (p.x - n.x).abs() <= NODE_W / 2.0 + 10.0 && (p.y - n.y).abs() <= NODE_H / 2.0 + 10.0)
        .min_by(|a, b| dist(a).total_cmp(&dist(b)))
        .map(|n| n.id.clone())
}

/// Whether port `pin` of component `node` can be connected to the one the wire is dragged from.
pub fn port_state(state: &SdState, pend: Option<&Pending>, node: &str, pin: Pin) -> PortState {
    let Some(p) = pend else { return PortState::Idle };
    if node == p.id {
        return PortState::Idle;
    }
    if pin == p.pin || link_error(state, p, node).is_some() {
        return PortState::Bad;
    }
    PortState::Ok
}

/// Highlight of the component under the end of the wire.
pub fn hover_class(state: &SdState, pend: Option<&Pending>, hover: &str) -> &'static str {
    match pend.and_then(|p| link_error(state, p, hover)) {
        Some(_) => "hover-bad",
        None => "hover-ok",
    }
}

/// The wire being dragged now: path and tone ("ok" — can connect, "bad" — cannot, empty — end at the cursor).
pub fn pending_wire(state: &SdState, pend: &Pending, hover: Option<&str>, cursor: Option<Point>) -> Option<(String, &'static str)> {
    let own_node = state.node(&pend.id)?;
    let hover_node = hover.and_then(|h| state.node(h));
    let own = match pend.pin {
        Pin::Out => out_pos(own_node.pt()),
        Pin::In => in_pos(own_node.pt()),
    };
    let end = match hover_node {
        Some(h) => match pend.pin {
            Pin::Out => in_pos(h.pt()),
            Pin::In => out_pos(h.pt()),
        },
        None => pt(cursor?),
    };
    let d = match pend.pin {
        Pin::Out => wire_path(own, end),
        Pin::In => wire_path(end, own),
    };
    let tone = match hover_node {
        Some(h) if link_error(state, pend, &h.id).is_some() => "bad",
        Some(_) => "ok",
        None => "",
    };
    Some((d, tone))
}

/// Path of a link between two components.
pub fn edge_path(state: &SdState, e: &SdEdge) -> Option<String> {
    Some(wire_path(out_pos(state.node(&e.from)?.pt()), in_pos(state.node(&e.to)?.pt())))
}

/// Path of an auto-wired link; the end `GHOST` stands for the ghost component.
pub fn auto_edge_path(state: &SdState, ghost: Option<&SdNode>, e: &SdEdge) -> Option<String> {
    let find = |id: &str| if id == GHOST { ghost } else { state.node(id) };
    Some(wire_path(out_pos(find(&e.from)?.pt()), in_pos(find(&e.to)?.pt())))
}

// --- labels --------------------------------------------------------------------------------------

/// Component name in one or two lines: about 17 characters fit in a frame line.
pub fn name_lines(name: &str) -> Vec<String> {
    const MAX: usize = 17;
    let cut = |s: &str| format!("{}…", s.chars().take(MAX - 1).collect::<String>());
    if name.chars().count() <= MAX {
        return vec![name.to_owned()];
    }
    let words: Vec<&str> = name.split(' ').collect();
    let mut first = String::new();
    let mut i = 0;
    while i < words.len() {
        let next = format!("{first} {}", words[i]).trim().to_owned();
        if next.chars().count() > MAX {
            break;
        }
        first = next;
        i += 1;
    }
    if first.is_empty() {
        return vec![cut(name)];
    }
    let rest = words[i..].join(" ");
    if rest.is_empty() {
        vec![first]
    } else if rest.chars().count() > MAX {
        vec![first, cut(&rest)]
    } else {
        vec![first, rest]
    }
}

/// Short parameters under the component name.
pub fn summary(n: &SdNode) -> String {
    let t = |k: &str| n.text(k).into_owned();
    let replicas = |k: &str| if n.num(k) > 0.0 { i18n::trf!(" +{0}r", t(k)) } else { String::new() };
    match n.kind {
        Kind::App | Kind::Worker => format!("×{} · {}", t("instances"), t("size")),
        Kind::Lb | Kind::Gateway | Kind::Ws | Kind::Auth | Kind::Geo | Kind::Ml | Kind::Pay | Kind::Notify | Kind::Analytics => format!("×{}", t("instances")),
        Kind::Stream | Kind::Queue => i18n::trf!("{0} part.", t("partitions")),
        Kind::Blob => match t("tier").as_str() {
            "cold" => i18n::tr("cold").into(),
            "mix" => i18n::tr("hot+cold").into(),
            _ => i18n::tr("hot").into(),
        },
        Kind::Cache => i18n::trf!("{0} GB{1}", t("size_gb"), replicas("replicas")),
        Kind::Db => format!("{}{}{}", t("size"), if n.num("shards") > 1.0 { i18n::trf!(" ·{0}sh", t("shards")) } else { String::new() }, replicas("replicas")),
        Kind::Limiter => i18n::trf!("{0}/s", t("limit")),
        Kind::Cdn => format!("TTL {}", t("ttl")),
        Kind::Search => i18n::trf!("{0}sh ×{1}r", t("shards"), t("replicas")),
        Kind::Clients | Kind::Monitor => String::new(),
    }
}

/// Full component label for the tooltip: the name and all parameters.
pub fn describe_node(n: &SdNode) -> String {
    let parts = kinds::spec(n.kind).params.iter().map(|p| {
        let v = n.params.get(p.key).unwrap_or(&p.default);
        let shown = match p.ty {
            kinds::ParamType::Bool => (if v.is_true() { i18n::tr("yes") } else { i18n::tr("no") }).to_owned(),
            _ => p.options.iter().find(|o| o.value == *v).map_or_else(|| v.as_text().into_owned(), |o| o.label.to_owned()),
        };
        format!("{}: {shown}", p.label)
    });
    std::iter::once(n.name.clone()).chain(parts).collect::<Vec<_>>().join("\n")
}

/// What to show for a number, as JavaScript does: `0` and empty are "false".
fn truthy(x: f64) -> bool {
    x != 0.0 && !x.is_nan()
}

/// Exercise load as short chips above the board.
pub fn workload_chips(w: &Workload) -> Vec<String> {
    let n = jsfmt::num;
    let mut out = Vec::new();
    if truthy(w.static_rps) {
        out.push(i18n::trf!("static {0}/s", n(w.static_rps)));
    }
    if truthy(w.read_rps) {
        out.push(i18n::trf!("reads {0}/s", n(w.read_rps)));
    }
    if truthy(w.write_rps) {
        out.push(i18n::trf!("writes {0}/s", n(w.write_rps)));
    }
    out.push(i18n::trf!("data {0} GB", n(w.data_gb)));
    out.push(i18n::trf!("working set {0}%", n(js_round(w.hot_set * 100.0))));
    let some = |x: Option<f64>| x.filter(|v| truthy(*v));
    if let Some(x) = some(w.search_share) {
        out.push(i18n::trf!("search {0}% of reads", n(js_round(x * 100.0))));
    }
    if let Some(x) = some(w.hot_key) {
        out.push(i18n::trf!("hot key {0}%", n(js_round(x * 100.0))));
    }
    if let Some(x) = some(w.connections) {
        out.push(i18n::trf!("connections {0}", n(x)));
    }
    if let Some(x) = some(w.msg_per_conn) {
        out.push(i18n::trf!("{0} msg/s per connection", n(x)));
    }
    if let Some(x) = some(w.spike_sec) {
        out.push(i18n::trf!("peak {0} s", n(x)));
    }
    out
}

/// Percentage for metrics: the closer to 100 %, the more digits.
pub fn fmt_pct(x: f64) -> String {
    let digits = if x >= 0.9999 {
        4
    } else if x >= 0.999 {
        3
    } else {
        1
    };
    format!("{}%", jsfmt::fixed(x * 100.0, digits))
}

/// What breaks, in words for choosing a failure; `None` — no failure is offered for this kind.
pub fn fail_text(f: FailKind) -> Option<&'static str> {
    Some(match f {
        FailKind::Zone => i18n::tr("availability zone failure"),
        FailKind::Region => i18n::tr("region failure"),
        FailKind::Deploy => i18n::tr("new version rollout"),
        FailKind::Component(k) => match k {
            Kind::App => i18n::tr("app server crashes"),
            Kind::Lb => i18n::tr("load balancer crashes"),
            Kind::Db => i18n::tr("database leader crashes"),
            Kind::Cache => i18n::tr("cache crashes"),
            Kind::Cdn => i18n::tr("CDN crashes"),
            Kind::Queue => i18n::tr("queue crashes"),
            Kind::Worker => i18n::tr("worker crashes"),
            Kind::Gateway => i18n::tr("gateway crashes"),
            Kind::Search => i18n::tr("search replica crashes"),
            Kind::Ws => i18n::tr("WebSocket gateway crashes"),
            Kind::Auth => i18n::tr("auth service crashes"),
            Kind::Geo => i18n::tr("geo service crashes"),
            Kind::Ml => i18n::tr("ranking service crashes"),
            Kind::Pay => i18n::tr("payment channel crashes"),
            Kind::Stream => i18n::tr("event stream crashes"),
            Kind::Notify => i18n::tr("notification service crashes"),
            Kind::Analytics => i18n::tr("analytics node crashes"),
            Kind::Clients | Kind::Monitor | Kind::Limiter | Kind::Blob => return None,
        },
    })
}

/// Failures by the component kinds present on the diagram, in the order they appear on it.
pub fn fail_kinds(state: &SdState) -> Vec<FailKind> {
    let mut out: Vec<FailKind> = Vec::new();
    for n in &state.nodes {
        let f = FailKind::Component(n.kind);
        if fail_text(f).is_some() && !out.contains(&f) {
            out.push(f);
        }
    }
    out
}

/// Rows of the model number reference (request counts, prices and availability).
pub fn reference_lines() -> Vec<String> {
    let n = jsfmt::num;
    let by = |b: r::BySize| format!("{}/{}/{}", n(b.s), n(b.m), n(b.l));
    vec![
        i18n::trf!("App server: S/M/L = {0} req/s, ${1}; a static request counts as {2}.", by(r::APP_CAP), by(r::APP_COST), n(r::STATIC_WEIGHT)),
        i18n::trf!("Database: reads {0}/s, writes {1}/s per node; ${2} per node; NoSQL ×{3}.", by(r::DB_READ), by(r::DB_WRITE), by(r::DB_COST), n(r::DB_NOSQL)),
        i18n::trf!("Cache: {0} req/s, ${1} per GB; CDN ${2}; load balancer {3} req/s, ${4}.", n(r::CACHE_CAP), n(r::CACHE_COST_PER_GB), n(r::CDN.cost), n(r::LB.cap), n(r::LB.cost)),
        i18n::trf!("Queue: {0} msg/s per partition; worker S/M: {1}/{2} records/s.", n(r::QUEUE_CAP_PER_PARTITION), n(r::WORKER_CAP.s), n(r::WORKER_CAP.m)),
        i18n::trf!("Search: {0} req/s per replica, at most {1} GB per shard, ${2} per node.", n(r::SEARCH_CAP), n(r::SEARCH_MAX_GB_PER_SHARD), n(r::SEARCH_COST)),
        i18n::trf!("WebSocket gateway: {0} connections per instance, ${1}.", n(r::WS.cap), n(r::WS.cost)),
        i18n::tr("Availability of one instance: server 99.5%, database 99.9%, load balancer 99.95%; n instances: 1 − (1 − a)ⁿ.").to_owned(),
    ]
}

/// Parameter value from the text of the selected list option.
pub fn option_value(p: &kinds::ParamSpec, text: &str) -> Option<ParamValue> {
    p.options.iter().find(|o| o.value.as_text() == text).map(|o| o.value.clone())
}

/// Parameters of a new component without values (palette ghost).
pub fn ghost_node(kind: Kind, at: Point) -> SdNode {
    SdNode { id: GHOST.to_owned(), kind, name: kinds::spec(kind).label.to_owned(), x: js_round(at.x), y: js_round(at.y), params: BTreeMap::new() }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn node(id: &str, kind: Kind, x: f64, y: f64) -> SdNode {
        SdNode { x, y, ..SdNode::new(id, kind, &[]) }
    }

    fn sample() -> SdState {
        SdState {
            nodes: vec![node("users", Kind::Clients, 70.0, 235.0), node("app", Kind::App, 670.0, 235.0), node("db", Kind::Db, 1120.0, 235.0)],
            edges: vec![SdEdge::new("users", "app")],
        }
    }

    fn scenario(start: SdState) -> Scenario {
        Scenario { workload: Workload::new(0.0, 50.0, 10.0), palette: vec![Kind::App, Kind::Db], start, goals: vec![], solution: SdState::default(), max_nodes: None, show: vec![] }
    }

    #[test]
    fn spec_without_solution_still_parses() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let spec = json!({
            "workload": { "static_rps": 0, "read_rps": 50, "write_rps": 10, "data_gb": 5, "hot_set": 0.2 },
            "palette": ["app", "db"],
            "start": { "nodes": [{ "id": "users", "kind": "clients", "x": 70, "y": 235, "params": {} }], "edges": [] },
            "goals": [{ "type": "link", "from": "clients", "to": "app" }]
        });
        let sc = parse_scenario(&spec).expect("exercise without the reference parses");
        assert_eq!(sc.palette, vec![Kind::App, Kind::Db]);
        assert_eq!(sc.max_nodes(), 14);
        assert!(sc.solution.nodes.is_empty());
        assert!(parse_scenario(&json!({ "palette": 5 })).is_err());
    }

    #[test]
    fn draft_restores_the_schema_or_falls_back_to_the_start() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario(sample());
        let mut changed = sample();
        changed.nodes[1].x = 400.0;
        let restored = restore(&sc, &draft_json(&changed));
        assert_eq!(restored.nodes[1].x, 400.0);
        // empty, garbage and a diagram without users — the initial diagram
        for bad in ["", "  ", "not json", "{}", r#"{"nodes":[{"id":"a","kind":"app"}],"edges":[]}"#] {
            assert_eq!(restore(&sc, bad), initial_state(&sc), "draft {bad:?}");
        }
    }

    #[test]
    fn unplaced_nodes_are_laid_out_into_columns() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let start = SdState { nodes: vec![SdNode::new("users", Kind::Clients, &[]), SdNode::new("app", Kind::App, &[])], edges: vec![] };
        let s = initial_state(&scenario(start));
        assert!(s.nodes.iter().all(|n| n.x >= 0.0 && n.y >= 0.0));
        assert!(s.nodes[0].x < s.nodes[1].x, "users are left of the servers");
    }

    #[test]
    fn crowded_draft_is_tidied_and_loose_one_is_kept() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut crowded = sample();
        crowded.nodes[1].x = 80.0;
        crowded.nodes[1].y = 240.0;
        let tidy_state = tidy(crowded);
        assert!(tidy_state.nodes[0].x != tidy_state.nodes[1].x);
        let loose = sample();
        assert_eq!(tidy(loose.clone()), loose);
    }

    #[test]
    fn new_nodes_get_free_ids_numbered_names_and_default_params() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut s = sample();
        let id = add_node(&mut s, Kind::App, Some(Point::new(500.0, 300.0)), &[]);
        assert_eq!(id, "app1", "id from kind and number, \"app\" is taken by an earlier node with a different id");
        let second = add_node(&mut s, Kind::App, None, &[]);
        assert_eq!(second, "app2");
        let names: Vec<&str> = s.nodes.iter().filter(|n| n.kind == Kind::App).map(|n| n.name.as_str()).collect();
        assert_eq!(names, ["Сервер приложения", "Сервер приложения 2", "Сервер приложения 3"]);
        assert_eq!((s.node("app1").map(|n| (n.x, n.y))), Some((500.0, 300.0)));
        assert!(s.node("app2").is_some_and(|n| n.x == layout::col_x(kinds::spec(Kind::App).col) && n.params.contains_key("instances")));
    }

    #[test]
    fn placed_node_takes_the_suggested_edges_without_duplicates() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut s = sample();
        let edges = [SdEdge::new("users", GHOST), SdEdge::new(GHOST, "db"), SdEdge::new("users", GHOST)];
        let id = add_node(&mut s, Kind::Cache, None, &edges);
        assert!(s.edges.contains(&SdEdge::new("users", &id)) && s.edges.contains(&SdEdge::new(&id, "db")));
        assert_eq!(s.edges.iter().filter(|e| e.from == "users" && e.to == id).count(), 1);
    }

    #[test]
    fn removing_a_node_drops_its_edges_and_clients_are_not_deletable() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut s = sample();
        add_edge(&mut s, SdEdge::new("app", "db"));
        add_edge(&mut s, SdEdge::new("app", "db"));
        assert_eq!(s.edges.len(), 2);
        assert!(deletable(&s, "app") && !deletable(&s, "users") && !deletable(&s, "zzz"));
        remove_node(&mut s, "app");
        assert!(s.edges.is_empty() && s.nodes.len() == 2);
    }

    #[test]
    fn int_parameters_are_rounded_and_clamped() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(clamp_int("5", Some(1.0), Some(40.0)), Some(5.0));
        assert_eq!(clamp_int("0", Some(1.0), Some(40.0)), Some(1.0));
        assert_eq!(clamp_int("99", Some(1.0), Some(40.0)), Some(40.0));
        assert_eq!(clamp_int("2.6", Some(1.0), Some(40.0)), Some(3.0));
        assert_eq!(clamp_int(" 7 ", None, None), Some(7.0));
        assert_eq!(clamp_int("-4", None, None), Some(0.0));
        assert_eq!(clamp_int("", None, None), None);
        assert_eq!(clamp_int("abc", None, None), None);
        assert_eq!(clamp_int("inf", None, None), None);
    }

    #[test]
    fn board_height_follows_the_window_only_when_sized() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(world_height(false, 1000.0, 400.0), layout::BOARD_H);
        assert_eq!(world_height(true, 0.0, 400.0), layout::BOARD_H);
        assert_eq!(world_height(true, 780.0, 390.0), 390.0);
        assert_eq!(world_height(true, 1560.0, 390.0), 195.0);
    }

    #[test]
    fn fit_shows_every_node_with_margins() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(fit_view(&[], 560.0), BOARD.home_view());
        let pts = [Point::new(70.0, 235.0), Point::new(1120.0, 235.0)];
        let v = fit_view(&pts, 560.0);
        // diagram width 1050 + 124 + 60 = 1234 → scale 780/1234
        assert!((v.zoom - 780.0 / 1234.0).abs() < 1e-9);
        let (w, h) = (780.0 / v.zoom, 560.0 / v.zoom);
        for p in pts {
            assert!(p.x - NODE_W / 2.0 >= v.pan.x - 1.0 && p.x + NODE_W / 2.0 <= v.pan.x + w + 1.0);
            assert!(p.y - NODE_H / 2.0 >= v.pan.y && p.y + NODE_H / 2.0 <= v.pan.y + h);
        }
        // one component — at most 160 % and centered in the window
        let one = fit_view(&[Point::new(300.0, 200.0)], 560.0);
        assert_eq!(one.zoom, 1.6);
        assert!((one.pan.x + 780.0 / 1.6 / 2.0 - 300.0).abs() <= 1.0);
        // a very wide diagram — at least 30 %
        assert_eq!(fit_view(&[Point::new(0.0, 0.0), Point::new(9000.0, 0.0)], 560.0).zoom, 0.3);
    }

    #[test]
    fn wire_ends_are_resolved_for_both_pins() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let out = Pending { id: "app".into(), pin: Pin::Out };
        let inn = Pending { id: "app".into(), pin: Pin::In };
        assert_eq!(pin_edge(&out, "db"), ("app".to_owned(), "db".to_owned()));
        assert_eq!(pin_edge(&inn, "users"), ("users".to_owned(), "app".to_owned()));
    }

    #[test]
    fn node_under_the_cursor_is_the_nearest_other_one() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let s = sample();
        assert_eq!(node_at(&s, "users", Point::new(680.0, 240.0)).as_deref(), Some("app"));
        assert_eq!(node_at(&s, "app", Point::new(680.0, 240.0)), None, "the component itself does not count");
        assert_eq!(node_at(&s, "users", Point::new(900.0, 100.0)), None);
        // margin of 10 units beyond the frame
        assert_eq!(node_at(&s, "users", Point::new(670.0 + NODE_W / 2.0 + 10.0, 235.0)).as_deref(), Some("app"));
        assert_eq!(node_at(&s, "users", Point::new(670.0 + NODE_W / 2.0 + 11.0, 235.0)), None);
    }

    #[test]
    fn ports_light_up_by_what_can_be_connected() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let s = sample();
        let from_app = Pending { id: "app".into(), pin: Pin::Out };
        // from the server's output: the database input fits, the users input does not (the model has no such link)
        assert_eq!(port_state(&s, Some(&from_app), "db", Pin::In), PortState::Ok);
        assert_eq!(port_state(&s, Some(&from_app), "users", Pin::In), PortState::Bad);
        // output to output — not allowed
        assert_eq!(port_state(&s, Some(&from_app), "db", Pin::Out), PortState::Bad);
        // the component itself and no wire — no highlight
        assert_eq!(port_state(&s, Some(&from_app), "app", Pin::In), PortState::Idle);
        assert_eq!(port_state(&s, None, "db", Pin::In), PortState::Idle);
        // a link already exists — not allowed
        let from_users = Pending { id: "users".into(), pin: Pin::Out };
        assert_eq!(port_state(&s, Some(&from_users), "app", Pin::In), PortState::Bad);
        // wire from an input: the source may be a user but not the database
        let to_app = Pending { id: "db".into(), pin: Pin::In };
        assert_eq!(port_state(&s, Some(&to_app), "app", Pin::Out), PortState::Ok);
    }

    #[test]
    fn hover_and_pending_wire_tones() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let s = sample();
        let p = Pending { id: "app".into(), pin: Pin::Out };
        assert_eq!(hover_class(&s, Some(&p), "db"), "hover-ok");
        assert_eq!(hover_class(&s, Some(&p), "users"), "hover-bad");
        let (d, tone) = pending_wire(&s, &p, Some("db"), None).expect("wire to a component");
        assert_eq!(tone, "ok");
        assert!(d.starts_with("M732 235"), "from the server's output: {d}");
        assert_eq!(pending_wire(&s, &p, Some("users"), None).map(|w| w.1), Some("bad"));
        assert_eq!(pending_wire(&s, &p, None, Some(Point::new(900.0, 300.0))).map(|w| w.1), Some(""));
        assert_eq!(pending_wire(&s, &p, None, None), None, "no wire without a cursor and a target");
        // a wire from an input is drawn from the target to the port
        let inn = Pending { id: "db".into(), pin: Pin::In };
        let (d, _) = pending_wire(&s, &inn, Some("app"), None).expect("wire from an input");
        assert!(d.starts_with("M732 235") && d.ends_with("1058 235"), "{d}");
    }

    #[test]
    fn edge_paths_follow_the_nodes_and_the_ghost() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let s = sample();
        assert!(edge_path(&s, &SdEdge::new("users", "app")).is_some());
        assert_eq!(edge_path(&s, &SdEdge::new("users", "zzz")), None);
        let ghost = ghost_node(Kind::Cache, Point::new(900.4, 100.6));
        assert_eq!((ghost.x, ghost.y), (900.0, 101.0));
        assert!(auto_edge_path(&s, Some(&ghost), &SdEdge::new("app", GHOST)).is_some());
        assert_eq!(auto_edge_path(&s, None, &SdEdge::new("app", GHOST)), None);
    }

    #[test]
    fn long_names_wrap_into_two_lines() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(name_lines("Кэш"), ["Кэш"]);
        assert_eq!(name_lines("Сервер приложения"), ["Сервер приложения"]);
        assert_eq!(name_lines("Сервер приложения 2"), ["Сервер приложения", "2"]);
        assert_eq!(name_lines("Объектное хранилище"), ["Объектное", "хранилище"]);
        assert_eq!(name_lines("Сервис ранжирования"), ["Сервис", "ранжирования"]);
        let long = name_lines("Очень_длинное_название_без_пробелов");
        assert_eq!(long.len(), 1);
        assert_eq!(long[0].chars().count(), 17);
        assert!(long[0].ends_with('…'));
        let tail = name_lines("Платёжный шлюз-посредник очень длинный хвост");
        assert_eq!(tail.len(), 2);
        assert!(tail[1].chars().count() <= 17);
    }

    #[test]
    fn node_summary_reads_the_main_parameters() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let app = SdNode::new("a", Kind::App, &[("instances", 3.into()), ("size", "M".into())]);
        assert_eq!(summary(&app), "×3 · M");
        let cache = SdNode::new("c", Kind::Cache, &[("size_gb", 8.into()), ("replicas", 1.into())]);
        assert_eq!(summary(&cache), "8 ГБ +1р");
        assert_eq!(summary(&SdNode::new("c", Kind::Cache, &[])), "4 ГБ");
        let db = SdNode::new("d", Kind::Db, &[("shards", 4.into()), ("replicas", 2.into())]);
        assert_eq!(summary(&db), "S ·4ш +2р");
        assert_eq!(summary(&SdNode::new("d", Kind::Db, &[])), "S");
        assert_eq!(summary(&SdNode::new("l", Kind::Limiter, &[])), "2000/с");
        assert_eq!(summary(&SdNode::new("q", Kind::Queue, &[])), "1 парт.");
        assert_eq!(summary(&SdNode::new("b", Kind::Blob, &[("tier", "cold".into())])), "холодное");
        assert_eq!(summary(&SdNode::new("u", Kind::Clients, &[])), "");
        for k in Kind::ALL {
            let s = summary(&SdNode::new("x", k, &[]));
            assert!(!s.contains("undefined") && !s.contains("NaN"), "{k}: {s}");
        }
    }

    #[test]
    fn node_tooltip_lists_name_and_every_parameter() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let app = SdNode::new("a", Kind::App, &[("size", "L".into()), ("breaker", true.into())]);
        let text = describe_node(&app);
        let lines: Vec<&str> = text.lines().collect();
        assert_eq!(lines[0], "Сервер приложения");
        assert!(lines.contains(&"Размер: L — большой"), "{text}");
        assert!(lines.contains(&"Автомат разрыва: да"), "{text}");
        assert!(lines.contains(&"Экземпляры: 1"), "{text}");
        assert_eq!(lines.len(), 1 + kinds::spec(Kind::App).params.len());
    }

    #[test]
    fn workload_chips_skip_zero_values() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let w = Workload { search_share: Some(0.25), hot_key: Some(0.0), connections: Some(5000.0), ..Workload::new(0.0, 50.0, 10.0) };
        assert_eq!(workload_chips(&w), ["чтения 50/с", "записи 10/с", "данные 10 ГБ", "рабочий набор 20%", "поиск 25% чтений", "соединений 5000"]);
    }

    #[test]
    fn percentages_gain_digits_near_one() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(fmt_pct(0.5), "50.0%");
        assert_eq!(fmt_pct(0.9995), "99.950%");
        assert_eq!(fmt_pct(0.99995), "99.9950%");
        assert_eq!(fmt_pct(1.0), "100.0000%");
        assert_eq!(fmt_pct(0.9), "90.0%");
    }

    #[test]
    fn failures_offered_for_kinds_on_the_schema_only() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut s = sample();
        add_node(&mut s, Kind::Monitor, None, &[]);
        add_node(&mut s, Kind::Blob, None, &[]);
        add_node(&mut s, Kind::App, None, &[]);
        assert_eq!(fail_kinds(&s), [FailKind::Component(Kind::App), FailKind::Component(Kind::Db)]);
        assert_eq!(fail_text(FailKind::Zone), Some("отказ зоны доступности"));
        assert_eq!(fail_text(FailKind::Component(Kind::Db)), Some("падает лидер базы"));
        assert_eq!(fail_text(FailKind::Component(Kind::Clients)), None);
        // for every kind with a failure and a label, the select value parses
        for k in Kind::ALL {
            let f = FailKind::Component(k);
            assert_eq!(f.as_str().parse::<FailKind>(), Ok(f));
        }
    }

    #[test]
    fn reference_lists_the_model_numbers() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let lines = reference_lines();
        assert_eq!(lines.len(), 7);
        assert_eq!(lines[0], "Сервер приложения: S/M/L = 300/700/1500 запр/с, $60/120/240; статика — 0.1 запроса.");
        assert!(lines[1].contains("чтения 1000/3000/8000") && lines[1].contains("NoSQL ×1.8"), "{}", lines[1]);
        assert!(lines[2].contains("60000 запр/с") && lines[2].contains("20000 запр/с"), "{}", lines[2]);
        assert!(lines[5].contains("15000 соединений"), "{}", lines[5]);
    }

    /// Real chapter data: each exercise parses, its start is non-empty, and the reference passes all goals through a draft.
    #[test]
    fn every_real_exercise_loads_and_its_solution_survives_the_draft_round_trip() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/sd");
        let Ok(files) = std::fs::read_dir(&dir) else { return };
        let mut tasks = 0;
        for file in files.flatten().filter(|f| f.path().extension().is_some_and(|e| e == "json")) {
            let chapter: Value = serde_json::from_str(&std::fs::read_to_string(file.path()).expect("file is readable")).expect("file is JSON");
            for task in chapter["tasks"].as_array().expect("exercise list") {
                let id = task["id"].as_str().unwrap_or("?");
                let sc = parse_scenario(&task["spec"]).unwrap_or_else(|e| panic!("{id}: {e}"));
                assert!(!initial_state(&sc).nodes.is_empty(), "{id}: empty initial diagram");
                let solved = restore(&sc, &draft_json(&sc.solution));
                assert_eq!(solved.nodes.len(), sc.solution.nodes.len(), "{id}");
                let goals = sdlab::check_goals(&solved, &sc.workload, &sc.goals, None);
                assert!(sdlab::all_ok(&goals), "{id}: reference does not pass the goals after a draft: {goals:?}");
                tasks += 1;
            }
        }
        assert!(tasks == 0 || tasks > 100, "exercises read: {tasks}");
    }

    /// Fitting is by node bounds, like `Board.fit` in React: `max(0.3, min(1.6, BOARD_W / bw, wh / bh))`, margins 30.
    /// For the initial diagram of "Vertical growth" (users 70, server 670, database 1120, all at y = 235) the bounds width is
    /// 1120 + 62 + 30 − (70 − 62 − 30) = 1234, so the scale is 780 / 1234 ≈ 0.632 — both in React and here.
    #[test]
    fn fit_of_the_vertical_growth_start_matches_the_react_formula() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/sd/18-02.json");
        let Ok(text) = std::fs::read_to_string(path) else { return };
        let chapter: Value = serde_json::from_str(&text).expect("file is JSON");
        let task = chapter["tasks"].as_array().and_then(|t| t.iter().find(|t| t["id"] == "sd02-vertical")).expect("exercise exists");
        let sc = parse_scenario(&task["spec"]).expect("parses");
        let nodes: Vec<Point> = initial_state(&sc).nodes.iter().map(|n| Point::new(n.x, n.y)).collect();
        assert_eq!(nodes, [Point::new(70.0, 235.0), Point::new(670.0, 235.0), Point::new(1120.0, 235.0)]);
        let v = fit_view(&nodes, 560.0);
        assert!((v.zoom - 780.0 / 1234.0).abs() < 1e-12, "{}", v.zoom);
        // window at full screen height (1400×1000 → window height 780·1000/1400 ≈ 557): the width still limits the scale
        assert!((fit_view(&nodes, 780.0 * 1000.0 / 1400.0).zoom - v.zoom).abs() < 1e-12);
        assert_eq!(v.pan, Point::new(-22.0, js_round(235.0 - 560.0 / v.zoom / 2.0)));
    }

    /// For all real exercises: fitting stays within the scale limits and shows all nodes.
    #[test]
    fn fit_shows_every_node_of_every_real_start_scheme() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/sd");
        let Ok(files) = std::fs::read_dir(&dir) else { return };
        for file in files.flatten().filter(|f| f.path().extension().is_some_and(|e| e == "json")) {
            let chapter: Value = serde_json::from_str(&std::fs::read_to_string(file.path()).expect("file is readable")).expect("file is JSON");
            for task in chapter["tasks"].as_array().expect("exercise list") {
                let id = task["id"].as_str().unwrap_or("?");
                let sc = parse_scenario(&task["spec"]).expect("parses");
                let nodes: Vec<Point> = initial_state(&sc).nodes.iter().map(|n| Point::new(n.x, n.y)).collect();
                for world_h in [560.0, 400.0, 900.0] {
                    let v = fit_view(&nodes, world_h);
                    assert!((0.3..=1.6).contains(&v.zoom), "{id}: zoom {}", v.zoom);
                    let (w, h) = (780.0 / v.zoom, world_h / v.zoom);
                    // the whole diagram is in the window unless the scale hit the lower limit
                    if v.zoom > 0.3 {
                        for p in &nodes {
                            assert!(p.x - NODE_W / 2.0 >= v.pan.x - 1.0 && p.x + NODE_W / 2.0 <= v.pan.x + w + 1.0, "{id}: x");
                            assert!(p.y - NODE_H / 2.0 >= v.pan.y - 1.0 && p.y + NODE_H / 2.0 <= v.pan.y + h + 1.0, "{id}: y");
                        }
                    }
                }
            }
        }
    }

    /// A draft in the form React saves it (`JSON.stringify` of the diagram) is read without loss.
    #[test]
    fn draft_written_by_react_is_restored_with_positions() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario(sample());
        let react = r#"{"nodes":[{"id":"users","kind":"clients","name":"Пользователи","x":70,"y":235,"params":{}},
            {"id":"app","kind":"app","name":"Сервер приложения","x":220,"y":235,"params":{"instances":1,"size":"L","sessions":"local","zone":"single","weight":1,"idempotency":false,"retries":0,"breaker":false,"feed":"pull","deploy":"all","pricing":"ondemand"}},
            {"id":"cache1","kind":"cache","name":"Кэш","x":370,"y":120,"params":{"sizeGB":8,"ttl":300}}],
            "edges":[{"from":"users","to":"app"}]}"#;
        let s = restore(&sc, react);
        assert_eq!(s.nodes.len(), 3);
        assert_eq!((s.nodes[1].x, s.nodes[1].y), (220.0, 235.0));
        assert_eq!(s.node("cache1").map(|n| n.num("size_gb")), Some(8.0), "sizeGB from React is read as size_gb");
    }

    #[test]
    fn select_option_text_maps_back_to_a_typed_value() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let ttl = kinds::param_spec(Kind::Cdn, "ttl").expect("ttl parameter");
        assert_eq!(option_value(ttl, "300"), Some(ParamValue::Num(300.0)), "a number stays a number");
        let size = kinds::param_spec(Kind::App, "size").expect("size parameter");
        assert_eq!(option_value(size, "M"), Some(ParamValue::Str("M".into())));
        assert_eq!(option_value(size, "XL"), None);
    }
}
