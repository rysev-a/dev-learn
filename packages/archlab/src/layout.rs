//! Board geometry: gate outlines, block rectangles with ports and auto-wiring.
//! Port of `gate-shapes.ts`, `block-layout.ts`, `auto-wire.ts` — pure arithmetic without the interface.

use crate::blocks::{BlockPort, BusEnd, Dir, TOP};
use crate::interfaces::{child_fields, slice_of};
use crate::model::*;
use std::collections::HashSet;

/* ============================================================
   Gate outlines
   ============================================================ */

/// Gate outline (SVG `d` attribute).
pub fn gate_body_path(ty: GateType) -> &'static str {
    match ty {
        GateType::And | GateType::Nand => "M0 0 H40 A24 24 0 0 1 40 48 H0 Z",
        GateType::Or | GateType::Nor | GateType::Xor | GateType::Xnor => "M0 0 Q34 2 64 24 Q34 46 0 48 Q18 24 0 0 Z",
        GateType::Not => "M0 0 L48 24 L0 48 Z",
        GateType::Dff => "M0 0 H64 V48 H0 Z",
    }
}

/// Path of the second input arc of XOR/XNOR or the clock mark of a flip-flop, if present.
pub fn gate_extra_arc(ty: GateType) -> Option<&'static str> {
    match ty {
        GateType::Dff => Some("M0 27 L9 34 L0 41"),
        GateType::Xor | GateType::Xnor => Some("M-8 0 Q10 24 -8 48"),
        _ => None,
    }
}

/// `cx` of the inversion bubble, if this type has one.
pub fn gate_bubble_cx(ty: GateType) -> Option<f64> {
    match ty {
        GateType::Nor | GateType::Nand | GateType::Xnor => Some(GATE_W + 6.0),
        GateType::Not => Some(53.0),
        _ => None,
    }
}

/// Y of an input pin relative to the top of the gate.
pub fn gate_pin_y(ty: GateType, pin: PinKind) -> f64 {
    if ty == GateType::Not {
        24.0
    } else if pin == PinKind::In0 {
        14.0
    } else {
        34.0
    }
}

/* ============================================================
   Blocks on the board
   ============================================================ */

pub const BLOCK_W: f64 = 176.0;
pub const HEAD_H: f64 = 28.0;
pub const ROW_H: f64 = 24.0;
pub const PAD: f64 = 6.0;
/// Width of the side columns with the exercise's own ports.
pub const SIDE_W: f64 = 132.0;

/// Which side of the rectangle the pin is on.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PinSide {
    In,
    Out,
}

/// Row of a port (or its field).
#[derive(Debug, Clone)]
pub struct PinRow {
    /// Unique row key: `node|port|field` — the same key marks expansion.
    pub key: String,
    pub end: BusEnd,
    pub port: BlockPort,
    pub name: String,
    pub ty: crate::interfaces::Iface,
    /// Nesting depth: 0 — the whole port, 1 — its field, and so on.
    pub depth: usize,
    pub side: PinSide,
    /// Offset of the row center from the top of the rectangle.
    pub y: f64,
    pub expandable: bool,
    pub expanded: bool,
    /// Circuit nodes carried by this row (in bit order).
    pub nodes: Vec<String>,
}

/// Kind of rectangle.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BoxKind {
    TopIn,
    TopOut,
    Block,
}

/// Layout of a rectangle with ports.
#[derive(Debug, Clone)]
pub struct BoxLayout {
    pub node: String,
    pub title: String,
    pub x: f64,
    pub y: f64,
    pub w: f64,
    pub h: f64,
    pub kind: BoxKind,
    pub rows: Vec<PinRow>,
}

/// Row key from a bus end.
pub fn row_key(end: &BusEnd) -> String {
    format!("{}|{}|{}", end.node, end.port, end.path)
}

fn rows_of_port(node: &str, port: &BlockPort, side: PinSide, expanded: &HashSet<String>, start_y: f64) -> Vec<PinRow> {
    #[allow(clippy::too_many_arguments)]
    fn add(
        rows: &mut Vec<PinRow>,
        y: &mut f64,
        node: &str,
        port: &BlockPort,
        side: PinSide,
        expanded: &HashSet<String>,
        path: &str,
        name: &str,
        ty: crate::interfaces::Iface,
        depth: usize,
    ) {
        let end = BusEnd { node: node.to_string(), port: port.name.clone(), path: path.to_string() };
        let key = row_key(&end);
        let slice = slice_of(port.ty, path);
        let expandable = !ty.is_simple();
        let is_open = expandable && expanded.contains(&key);
        let nodes = slice
            .map(|s| port.nodes.iter().skip(s.offset).take(s.length).cloned().collect())
            .unwrap_or_default();
        rows.push(PinRow {
            key,
            end,
            port: port.clone(),
            name: name.to_string(),
            ty,
            depth,
            side,
            y: *y + ROW_H / 2.0,
            expandable,
            expanded: is_open,
            nodes,
        });
        *y += ROW_H;
        if is_open {
            for f in child_fields(port.ty, path) {
                add(rows, y, node, port, side, expanded, &f.path, f.name, f.ty, depth + 1);
            }
        }
    }
    let mut rows = Vec::new();
    let mut y = start_y;
    add(&mut rows, &mut y, node, port, side, expanded, "", &port.name, port.ty, 0);
    rows
}

/// Layout of a rectangle with ports: inputs on the left, outputs on the right.
pub fn layout_box(
    node: &str,
    title: &str,
    ports: &[BlockPort],
    expanded: &HashSet<String>,
    at: (f64, f64, f64),
    kind: BoxKind,
) -> BoxLayout {
    let top = HEAD_H + PAD;
    let mut rows = Vec::new();
    let (mut left_y, mut right_y) = (top, top);
    for port in ports {
        // the exercise's own ports: an input is a source, so its pin is on the right; an output — on the left
        let side = match kind {
            BoxKind::TopIn => PinSide::Out,
            BoxKind::TopOut => PinSide::In,
            BoxKind::Block => {
                if port.dir == Dir::In {
                    PinSide::In
                } else {
                    PinSide::Out
                }
            }
        };
        let start_y = if side == PinSide::In { left_y } else { right_y };
        let added = rows_of_port(node, port, side, expanded, start_y);
        let next = start_y + added.len() as f64 * ROW_H;
        rows.extend(added);
        if side == PinSide::In {
            left_y = next;
        } else {
            right_y = next;
        }
    }
    BoxLayout { node: node.into(), title: title.into(), x: at.0, y: at.1, w: at.2, h: left_y.max(right_y) + PAD, kind, rows }
}

/// Center of a row's pin in board coordinates.
pub fn pin_center(b: &BoxLayout, row: &PinRow) -> Point {
    Point { x: if row.side == PinSide::In { b.x } else { b.x + b.w }, y: b.y + row.y }
}

/// Rectangles of the columns with the exercise's own ports: (inputs, outputs).
pub fn side_boxes(ports: &[BlockPort], expanded: &HashSet<String>, board_w: f64, y: f64) -> (BoxLayout, BoxLayout) {
    let ins: Vec<BlockPort> = ports.iter().filter(|p| p.dir == Dir::In).cloned().collect();
    let outs: Vec<BlockPort> = ports.iter().filter(|p| p.dir == Dir::Out).cloned().collect();
    (
        layout_box(TOP, i18n::tr("Inputs"), &ins, expanded, (6.0, y, SIDE_W), BoxKind::TopIn),
        layout_box(TOP, i18n::tr("Outputs"), &outs, expanded, (board_w - SIDE_W - 6.0, y, SIDE_W), BoxKind::TopOut),
    )
}

/// Free place for a new block: the first grid cell not occupied by others.
pub fn free_spot(taken: &[(f64, f64)], board_w: f64) -> (f64, f64) {
    let cols = 1.0f64.max(((board_w - 2.0 * (SIDE_W + 30.0)) / (BLOCK_W + 30.0)).floor());
    let x0 = SIDE_W + 30.0;
    for i in 0..40 {
        let x = x0 + (i as f64 % cols) * (BLOCK_W + 30.0);
        let y = 20.0 + (i as f64 / cols).floor() * 150.0;
        if !taken.iter().any(|t| (t.0 - x).abs() < 40.0 && (t.1 - y).abs() < 60.0) {
            return (x, y);
        }
    }
    (x0, 20.0)
}

/* ============================================================
   Auto-wiring
   ============================================================ */

/// Auto-wiring radius: multiplier, bounds and the default value.
pub const AUTO_WIRE_RADIUS_FACTOR: f64 = 4.0;
pub const AUTO_WIRE_RADIUS_MIN: f64 = 16.0;
pub const AUTO_WIRE_RADIUS_MAX: f64 = 108.0;
pub const AUTO_WIRE_RADIUS_DEFAULT: f64 = 56.0;
/// At what distance (in board units) contacts count as "close".
pub const AUTO_WIRE_RADIUS: f64 = AUTO_WIRE_RADIUS_DEFAULT * AUTO_WIRE_RADIUS_FACTOR;
/// How much an already shown connection "sticks": a closer pair must win by at least this much.
pub const AUTO_WIRE_STICK: f64 = 6.0;

/// Suggested connection: the wire ends and their positions on the board (for the dashed preview).
#[derive(Debug, Clone, PartialEq)]
pub struct AutoWire {
    pub from: PinRef,
    pub to: PinRef,
    pub a: Point,
    pub b: Point,
}

/// Auto-wiring input.
pub struct AutoWireInput<'a> {
    /// The element being moved or placed (it may not be in `gates` yet).
    pub gate: &'a GateInstance,
    /// The other elements on the board.
    pub gates: &'a [GateInstance],
    pub wires: &'a [Wire],
    pub input_y: &'a YMap,
    pub output_y: &'a YMap,
    /// In step mode cycles are allowed — that is the essence of latches.
    pub steps_mode: bool,
    pub radius: Option<f64>,
    /// Connections suggested earlier in the same drag: kept until a closer pair takes them over.
    pub keep: &'a [AutoWire],
}

struct Candidate {
    from: PinRef,
    to: PinRef,
    group: String,
    d: f64,
    held: bool,
}

fn dist(p: Point, q: Point) -> f64 {
    (p.x - q.x).hypot(p.y - q.y)
}

/// Which wires are worth suggesting for an element at its place: every free input reaches for the nearest
/// output (a toggle or another element), and every output — for the nearest free input (of an element or
/// a circuit output). Occupied inputs are left alone.
pub fn suggest_wires(input: &AutoWireInput) -> Vec<AutoWire> {
    let gate = input.gate;
    let radius = input.radius.unwrap_or(AUTO_WIRE_RADIUS);
    let kept = |from: &PinRef, to: &PinRef| input.keep.iter().any(|k| k.from == *from && k.to == *to);
    let others: Vec<&GateInstance> = input.gates.iter().filter(|g| g.id != gate.id).collect();
    let mut all: Vec<GateInstance> = others.iter().map(|g| (*g).clone()).collect();
    all.push(gate.clone());
    let mut result: Vec<AutoWire> = Vec::new();
    // wires we have already decided to add are also taken into account when looking for cycles
    let mut planned: Vec<Wire> = Vec::new();

    let pos_of = |r: &PinRef| pin_pos(r, &all, input.output_y, input.input_y);
    let driven = |to: &PinRef, planned: &[Wire]| input.wires.iter().any(|w| w.to == *to) || planned.iter().any(|w| w.to == *to);

    let accept = |from: &PinRef, to: &PinRef, planned: &mut Vec<Wire>, result: &mut Vec<AutoWire>| -> bool {
        if from.node == to.node {
            return false;
        }
        if !input.steps_mode {
            let mut wires = input.wires.to_vec();
            wires.extend(planned.iter().cloned());
            let circuit = Circuit::new(all.clone(), wires);
            if creates_cycle(&circuit, from, to) {
                return false;
            }
        }
        planned.push(Wire { id: format!("auto{}", planned.len()), from: from.clone(), to: to.clone() });
        result.push(AutoWire { from: from.clone(), to: to.clone(), a: pos_of(from), b: pos_of(to) });
        true
    };

    let mut cands: Vec<Candidate> = Vec::new();
    let consider = |from: PinRef, to: PinRef, other: &str, dir: &str, cands: &mut Vec<Candidate>| {
        let held = kept(&from, &to);
        let d = dist(pos_of(&from), pos_of(&to));
        if held || d <= radius {
            cands.push(Candidate { from, to, group: format!("{dir}:{other}"), d, held });
        }
    };

    // signal sources: input toggles and outputs of other elements
    let mut sources: Vec<PinRef> = input.input_y.keys().map(PinRef::out).collect();
    sources.extend(others.iter().map(|g| PinRef::out(g.id.clone())));
    for pin in gate.ty.pins() {
        let to = PinRef::inp(gate.id.clone(), *pin);
        if driven(&to, &planned) {
            continue;
        }
        for from in &sources {
            consider(from.clone(), to.clone(), &from.node, "in", &mut cands);
        }
    }

    // signal sinks: free inputs of other elements and circuit outputs
    let mut sinks: Vec<PinRef> = others.iter().flat_map(|g| g.ty.pins().iter().map(|p| PinRef::inp(g.id.clone(), *p))).collect();
    sinks.extend(input.output_y.keys().map(|n| PinRef::inp(n, PinKind::In0)));
    let out = PinRef::out(gate.id.clone());
    for to in &sinks {
        if !driven(to, &planned) {
            consider(out.clone(), to.clone(), &to.node, "out", &mut cands);
        }
    }

    // like a magnet: we take the shortest connections, and an already shown one has a small "sticky" margin so
    // the dashed line does not jitter. If two contacts reach for the same element, the dashed line stays with the nearer one,
    // and the other contact looks for a different neighbor
    let pull = |c: &Candidate| c.d - if c.held { AUTO_WIRE_STICK } else { 0.0 };
    cands.sort_by(|p, q| pull(p).partial_cmp(&pull(q)).unwrap_or(std::cmp::Ordering::Equal));
    let mut used_groups: HashSet<String> = HashSet::new();
    let mut used_pins: HashSet<String> = HashSet::new();
    for c in &cands {
        // an output has one connection, each input has one too
        let pin_key = if c.from.node == gate.id { "out".to_string() } else { format!("{:?}", c.to.pin) };
        if used_pins.contains(&pin_key) || used_groups.contains(&c.group) {
            continue;
        }
        if !accept(&c.from, &c.to, &mut planned, &mut result) {
            continue;
        }
        used_pins.insert(pin_key);
        used_groups.insert(c.group.clone());
    }
    result
}
