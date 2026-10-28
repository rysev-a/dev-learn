//! Logic circuit model: gates, wires, toggle inputs and board geometry.
//!
//! Port of `circuit.model.ts`. Coordinates are in board space (viewBox 880 × 440).

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Bit: 0 or 1.
pub type Bit = u8;

/// Node value: 0, 1 or `None` ("?" — not connected or unknown).
pub type NodeValue = Option<Bit>;

/// Values of circuit nodes by name.
pub type Values = HashMap<String, NodeValue>;

/// Gate type. `Dff` — edge-triggered D flip-flop: input 0 — data D, input 1 — clock CLK, output — Q.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "UPPERCASE")]
pub enum GateType {
    And,
    Or,
    Nor,
    Not,
    Nand,
    Xor,
    Xnor,
    Dff,
}

/// All gate types in palette order.
pub const GATE_TYPES: [GateType; 8] = [
    GateType::And,
    GateType::Or,
    GateType::Nor,
    GateType::Not,
    GateType::Nand,
    GateType::Xor,
    GateType::Xnor,
    GateType::Dff,
];

impl GateType {
    /// Name as in the data and on the board: `AND`, `NOR`, …
    pub fn name(self) -> &'static str {
        match self {
            GateType::And => "AND",
            GateType::Or => "OR",
            GateType::Nor => "NOR",
            GateType::Not => "NOT",
            GateType::Nand => "NAND",
            GateType::Xor => "XOR",
            GateType::Xnor => "XNOR",
            GateType::Dff => "DFF",
        }
    }

    /// Russian name (`RU_NAMES` from `gate-shapes.ts`).
    pub fn ru_name(self) -> &'static str {
        match self {
            GateType::And => i18n::tr("AND"),
            GateType::Or => i18n::tr("OR"),
            GateType::Nor => i18n::tr("NOR"),
            GateType::Not => i18n::tr("NOT"),
            GateType::Nand => i18n::tr("NAND"),
            GateType::Xor => i18n::tr("XOR"),
            GateType::Xnor => i18n::tr("XNOR"),
            GateType::Dff => i18n::tr("Edge-triggered D flip-flop"),
        }
    }

    /// Input pins: NOT has one, the rest have two.
    pub fn pins(self) -> &'static [PinKind] {
        if self == GateType::Not {
            &[PinKind::In0]
        } else {
            &[PinKind::In0, PinKind::In1]
        }
    }
}

/// Physical toggle inputs of the board.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum InputId {
    A,
    B,
    C,
    D,
    E,
    F,
}

/// All inputs in order.
pub const INPUT_IDS: [InputId; 6] = [
    InputId::A,
    InputId::B,
    InputId::C,
    InputId::D,
    InputId::E,
    InputId::F,
];

impl InputId {
    /// Node name: `"A"`…`"F"`.
    pub fn as_str(self) -> &'static str {
        match self {
            InputId::A => "A",
            InputId::B => "B",
            InputId::C => "C",
            InputId::D => "D",
            InputId::E => "E",
            InputId::F => "F",
        }
    }

    /// Parse a node name.
    pub fn parse(s: &str) -> Option<InputId> {
        INPUT_IDS.iter().copied().find(|i| i.as_str() == s)
    }

    /// Number 0…5.
    pub fn index(self) -> usize {
        self as usize
    }
}

/// State of the six toggles.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct InputState(pub [Bit; 6]);

impl InputState {
    /// All toggles at zero.
    pub fn zero() -> Self {
        InputState([0; 6])
    }
    /// Toggle level.
    pub fn get(&self, id: InputId) -> Bit {
        self.0[id.index()]
    }
    /// Set the level (any non-zero — one).
    pub fn set(&mut self, id: InputId, level: Bit) {
        self.0[id.index()] = (level != 0) as Bit;
    }
    /// Number from the toggle values `ids`: the first is the most significant.
    pub fn row(&self, ids: &[InputId]) -> usize {
        ids.iter().fold(0, |acc, id| (acc << 1) | self.get(*id) as usize)
    }
}

/// Input values for a truth-table row (`row` — bits of the active inputs, most significant first).
pub fn inputs_for_row(ids: &[InputId], row: usize) -> InputState {
    let mut state = InputState::zero();
    let n = ids.len();
    for (i, id) in ids.iter().enumerate() {
        state.set(*id, ((row >> (n - 1 - i)) & 1) as Bit);
    }
    state
}

/// Gate instance on the board.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GateInstance {
    pub id: String,
    #[serde(rename = "type")]
    pub ty: GateType,
    #[serde(default)]
    pub x: f64,
    #[serde(default)]
    pub y: f64,
}

/// Which pin: the output or one of the inputs.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum PinKind {
    Out,
    In0,
    In1,
}

/// Wire end: node (`A`…`F`, gate id or exercise output name) and pin.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PinRef {
    pub node: String,
    pub pin: PinKind,
}

impl PinRef {
    /// Node output.
    pub fn out(node: impl Into<String>) -> Self {
        PinRef { node: node.into(), pin: PinKind::Out }
    }
    /// Node input.
    pub fn inp(node: impl Into<String>, pin: PinKind) -> Self {
        PinRef { node: node.into(), pin }
    }
}

/// Wire from an output to an input.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Wire {
    pub id: String,
    pub from: PinRef,
    pub to: PinRef,
}

/// Kind of built-in memory.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum NativeKind {
    Rom,
    Ram,
}

/// Built-in memory — a "chip" with address and data; the contents are loaded from outside.
/// The general simulator does not support it — only the fast one ([`crate::cpu8::fast::CompiledSim`]).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NativeInstance {
    pub id: String,
    pub kind: NativeKind,
    /// Address source nodes, most significant bit first; `None` — not connected.
    pub addr: Vec<Option<String>>,
    /// Data nodes for writing (ram only).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub din: Option<Vec<Option<String>>>,
    /// Write enable (ram only).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub we: Option<String>,
    /// Clock (ram only).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub clk: Option<String>,
    /// Output node names, most significant bit first.
    pub dout: Vec<String>,
}

/// Flat circuit: gates, wires and (for the processor) built-in memory.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Circuit {
    pub gates: Vec<GateInstance>,
    pub wires: Vec<Wire>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub natives: Vec<NativeInstance>,
}

impl Circuit {
    /// Circuit without memory.
    pub fn new(gates: Vec<GateInstance>, wires: Vec<Wire>) -> Self {
        Circuit { gates, wires, natives: Vec::new() }
    }
}

/// Truth-table row after evaluation.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TableRow {
    pub targets: Vec<Bit>,
    pub actuals: Vec<NodeValue>,
    pub ok: bool,
}

/* ============================================================
   Board geometry
   ============================================================ */

pub const BOARD_W: f64 = 880.0;
pub const BOARD_H: f64 = 440.0;
pub const GATE_W: f64 = 64.0;
pub const GATE_H: f64 = 48.0;
/// X of the output pin of a toggle input.
pub const INPUT_X: f64 = 100.0;
/// X of the input pins of outputs (Y, Q, …).
pub const OUT_X: f64 = 780.0;
pub const GATE_MIN_X: f64 = 140.0;
pub const GATE_MAX_X: f64 = 690.0;
pub const GATE_MIN_Y: f64 = 12.0;
pub const GATE_MAX_Y: f64 = BOARD_H - GATE_H - 12.0;

const LEGACY_INPUT_Y: [f64; 3] = [80.0, 200.0, 320.0];

/// Point on the board.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

/// Y coordinates of nodes by name in insertion order (the order matters: auto-wiring depends on it).
#[derive(Debug, Clone, Default, PartialEq)]
pub struct YMap(pub Vec<(String, f64)>);

impl YMap {
    /// Y of a node.
    pub fn get(&self, node: &str) -> Option<f64> {
        self.0.iter().find(|(n, _)| n == node).map(|(_, y)| *y)
    }

    /// Node names in order.
    pub fn keys(&self) -> impl Iterator<Item = &str> {
        self.0.iter().map(|(n, _)| n.as_str())
    }

    /// "name — Y" pairs.
    pub fn iter(&self) -> impl Iterator<Item = (&str, f64)> {
        self.0.iter().map(|(n, y)| (n.as_str(), *y))
    }
}

fn spread<S: AsRef<str>>(names: &[S], top: f64, bottom: f64) -> YMap {
    let n = names.len();
    YMap(
        names
            .iter()
            .enumerate()
            .map(|(i, name)| (name.as_ref().to_string(), top + (i as f64 * (bottom - top)) / (n as f64 - 1.0)))
            .collect(),
    )
}

/// Y of inputs on the left edge: up to three — 80/200/320, more — evenly over the height.
pub fn input_ys(ids: &[InputId]) -> YMap {
    if ids.len() <= 3 {
        return YMap(ids.iter().enumerate().map(|(i, id)| (id.as_str().to_string(), LEGACY_INPUT_Y[i])).collect());
    }
    let names: Vec<&str> = ids.iter().map(|i| i.as_str()).collect();
    spread(&names, 50.0, 390.0)
}

/// Y of outputs on the right edge: one — centered, up to four — as before, more — over the full height.
pub fn output_ys<S: AsRef<str>>(outputs: &[S]) -> YMap {
    if outputs.len() == 1 {
        return YMap(vec![(outputs[0].as_ref().to_string(), 200.0)]);
    }
    if outputs.len() <= 4 {
        spread(outputs, 80.0, 320.0)
    } else {
        spread(outputs, 40.0, 400.0)
    }
}

/// X of a gate's output pin (further right for inverting gates — the bubble is there).
pub fn out_pin_x(ty: GateType) -> f64 {
    match ty {
        GateType::And | GateType::Or | GateType::Xor | GateType::Dff => GATE_W + 8.0,
        GateType::Nor | GateType::Nand | GateType::Xnor => GATE_W + 16.0,
        GateType::Not => 64.0,
    }
}

/// Pin coordinates on the board. `output_y` — Y of output nodes, `input_y` — Y of inputs.
pub fn pin_pos(r: &PinRef, gates: &[GateInstance], output_y: &YMap, input_y: &YMap) -> Point {
    if r.pin != PinKind::Out {
        if let Some(oy) = output_y.get(&r.node) {
            return Point { x: OUT_X, y: oy };
        }
    }
    if r.pin == PinKind::Out {
        if let Some(iy) = input_y.get(&r.node) {
            return Point { x: INPUT_X, y: iy };
        }
    }
    let Some(gate) = gates.iter().find(|g| g.id == r.node) else {
        return Point { x: 0.0, y: 0.0 };
    };
    match r.pin {
        PinKind::Out => Point { x: gate.x + out_pin_x(gate.ty), y: gate.y + 24.0 },
        PinKind::In0 => Point { x: gate.x - 8.0, y: gate.y + 14.0 },
        PinKind::In1 => Point { x: gate.x - 8.0, y: gate.y + 34.0 },
    }
}

/// Default inputs (A, B, C) for [`pin_pos`].
pub fn legacy_input_ys() -> YMap {
    YMap(["A", "B", "C"].iter().zip(LEGACY_INPUT_Y).map(|(n, y)| (n.to_string(), y)).collect())
}

/// Wire path — cubic Bézier curve (SVG `d` attribute).
pub fn wire_path(a: Point, b: Point) -> String {
    let dx = 110f64.min(36f64.max((b.x - a.x).abs() / 2.0));
    format!("M {} {} C {} {}, {} {}, {} {}", a.x, a.y, a.x + dx, a.y, b.x - dx, b.y, b.x, b.y)
}

/// Would a new connection from → to create a cycle: the source is reachable from the target node.
pub fn creates_cycle(circuit: &Circuit, from: &PinRef, to: &PinRef) -> bool {
    if to.node == from.node {
        return true;
    }
    let mut adjacency: HashMap<&str, Vec<&str>> = HashMap::new();
    for w in &circuit.wires {
        adjacency.entry(w.from.node.as_str()).or_default().push(w.to.node.as_str());
    }
    let mut seen: std::collections::HashSet<&str> = std::collections::HashSet::from([to.node.as_str()]);
    let mut stack = vec![to.node.as_str()];
    while let Some(n) = stack.pop() {
        if n == from.node {
            return true;
        }
        for next in adjacency.get(n).into_iter().flatten() {
            if seen.insert(next) {
                stack.push(next);
            }
        }
    }
    false
}

/// Allocation of new ids (`g3`, `w7`, …): after loading a saved circuit, new ids will not collide with old ones.
#[derive(Debug, Default, Clone)]
pub struct UidGen {
    seq: u64,
}

impl UidGen {
    /// Start counting from zero.
    pub fn new() -> Self {
        Self::default()
    }

    /// Reserve an id of the form `prefix<number>`: counting continues after the largest number.
    pub fn reserve<S: AsRef<str>>(&mut self, ids: &[S]) {
        for id in ids {
            let s = id.as_ref();
            let digits: String = s.chars().rev().take_while(|c| c.is_ascii_digit()).collect::<Vec<_>>().into_iter().rev().collect();
            if let Ok(n) = digits.parse::<u64>() {
                self.seq = self.seq.max(n);
            }
        }
    }

    /// New id with a prefix.
    pub fn next(&mut self, prefix: &str) -> String {
        self.seq += 1;
        format!("{prefix}{}", self.seq)
    }
}
