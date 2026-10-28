//! Blocks: a solved exercise becomes a block that has ports of interface types.
//! Blocks are connected by buses; before simulation a block circuit is expanded into a flat circuit of
//! gates — so the simulator [`crate::eval`] works unchanged. Port of `blocks.ts`.

use crate::interfaces::{can_connect, slice_of, Iface};
use crate::model::*;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::sync::Arc;

/* ============================================================
   Model
   ============================================================ */

/// Bus node for the ports of the exercise itself (instead of a block instance id).
pub const TOP: &str = "$";

/// Block instance on the block board.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockInstance {
    pub id: String,
    #[serde(alias = "blockId")]
    pub block_id: String,
    #[serde(default)]
    pub x: f64,
    #[serde(default)]
    pub y: f64,
}

/// Bus end: `node` — block instance id or [`TOP`]; `path` — path to a field inside the port type
/// (`""` — the whole port, `"op"`, `"k.D1"`).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BusEnd {
    pub node: String,
    pub port: String,
    #[serde(default)]
    pub path: String,
}

impl BusEnd {
    /// Bus end: `BusEnd::new("rom", "instr", "op")`.
    pub fn new(node: &str, port: &str, path: &str) -> Self {
        BusEnd { node: node.into(), port: port.into(), path: path.into() }
    }
}

/// Bus — a wire for a whole interface or its field.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BusWire {
    pub id: String,
    pub from: BusEnd,
    pub to: BusEnd,
}

/// Solution made of gates.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GateSolution {
    pub gates: Vec<GateInstance>,
    pub wires: Vec<Wire>,
}

/// Solution made of blocks.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockSolution {
    pub instances: Vec<BlockInstance>,
    #[serde(alias = "busWires")]
    pub bus_wires: Vec<BusWire>,
}

/// Built-in memory: in the circuit it is a "black box" with address and data, cells are not made of gates.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NativeSolution {
    pub native: NativeKind,
    /// Address nodes, most significant bit first.
    pub addr: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub din: Option<Vec<String>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub we: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub clk: Option<String>,
    pub dout: Vec<String>,
}

/// Exercise solution or block contents: gates, blocks or built-in memory.
/// In JSON — one of three forms: `{gates, wires}`, `{instances, bus_wires}` (also `busWires`), `{native, …}`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Solution {
    Block(BlockSolution),
    Gate(GateSolution),
    Native(NativeSolution),
}

impl Solution {
    /// Parse a submitted solution with a clear error (TS: `isSolution` + `JSON.parse`).
    pub fn from_json(text: &str) -> Result<Solution, String> {
        let v: serde_json::Value = serde_json::from_str(text).map_err(|e| i18n::trf!("not JSON: {0}", e))?;
        let Some(o) = v.as_object() else {
            return Err(i18n::tr("the solution must be an object").into());
        };
        let arr = |k: &str| o.get(k).is_some_and(|x| x.is_array());
        if !((arr("gates") && arr("wires")) || (arr("instances") && (arr("bus_wires") || arr("busWires"))) || o.contains_key("native")) {
            return Err(i18n::tr("expected a circuit: {gates, wires} or {instances, bus_wires}").into());
        }
        serde_json::from_value(v).map_err(|e| i18n::trf!("circuit could not be parsed: {0}", e))
    }

    /// Is it a block circuit?
    pub fn is_block(&self) -> bool {
        matches!(self, Solution::Block(_))
    }
}

/// Port direction.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Dir {
    /// The port receives a signal.
    In,
    /// The port emits a signal.
    Out,
}

/// Block port: name, interface type and circuit nodes in bit order (most significant first).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockPort {
    pub name: String,
    #[serde(rename = "type")]
    pub ty: Iface,
    pub dir: Dir,
    pub nodes: Vec<String>,
}

/// External "socket" of a circuit — the nodes it exposes to the outside.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct BlockInterface {
    pub inputs: Vec<String>,
    pub outputs: Vec<String>,
    /// Input labels in `inputs` order.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub labels: Option<Vec<String>>,
    pub ports: Vec<BlockPort>,
}

/// Where the block comes from: the exercise whose solution is inside.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockSource {
    pub section_slug: String,
    pub exercise_id: String,
}

/// Block description.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockDef {
    pub id: String,
    pub title: String,
    #[serde(flatten)]
    pub iface: BlockInterface,
    /// `None` for built-in blocks.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub source: Option<BlockSource>,
}

/// Block together with its contents.
pub type BlockEntry = (Arc<BlockDef>, Arc<Solution>);

/// Block lookup by id: what [`expand`] uses to fetch the contents of nested blocks.
pub trait BlockLookup {
    fn lookup(&self, id: &str) -> Option<BlockEntry>;
}

impl<F: Fn(&str) -> Option<BlockEntry>> BlockLookup for F {
    fn lookup(&self, id: &str) -> Option<BlockEntry> {
        self(id)
    }
}

fn simple_wire(id: String, from: &str, to: &str) -> Wire {
    Wire { id, from: PinRef::out(from), to: PinRef::inp(to, PinKind::In0) }
}

/// Adapter between types: a circuit made of wires only (D1 → A1, D0 → A0).
fn adapter(id: &str, title: &str, in_ty: Iface, out_ty: Iface, in_nodes: [&str; 2], out_nodes: [&str; 2]) -> (BlockDef, Solution) {
    let nodes = |n: [&str; 2]| n.iter().map(|s| s.to_string()).collect::<Vec<_>>();
    let def = BlockDef {
        id: id.into(),
        title: title.into(),
        iface: BlockInterface {
            inputs: nodes(in_nodes),
            outputs: nodes(out_nodes),
            labels: None,
            ports: vec![
                BlockPort { name: "in".into(), ty: in_ty, dir: Dir::In, nodes: nodes(in_nodes) },
                BlockPort { name: "out".into(), ty: out_ty, dir: Dir::Out, nodes: nodes(out_nodes) },
            ],
        },
        source: None,
    };
    let wires = in_nodes.iter().enumerate().map(|(i, n)| simple_wire(format!("w{i}"), n, out_nodes[i])).collect();
    (def, Solution::Gate(GateSolution { gates: vec![], wires }))
}

/// Block library: definitions, their contents (if the block is "unlocked") and hints for locked ones.
#[derive(Debug, Clone, Default)]
pub struct BlockLibrary {
    order: Vec<String>,
    defs: HashMap<String, Arc<BlockDef>>,
    solutions: HashMap<String, Arc<Solution>>,
    hints: HashMap<String, String>,
}

impl BlockLibrary {
    /// Library with built-in blocks (word ↔ address adapters are available right away).
    pub fn builtin() -> Self {
        let mut lib = BlockLibrary::default();
        for (def, sol) in [
            adapter("adapter-w2a", i18n::tr("Word → address"), Iface::Word2, Iface::Addr2, ["A", "B"], ["Y1", "Y0"]),
            adapter("adapter-a2w", i18n::tr("Address → word"), Iface::Addr2, Iface::Word2, ["A", "B"], ["Y1", "Y0"]),
        ] {
            lib.insert(def, Some(sol), String::new());
        }
        lib
    }

    /// Add a block; `solution = None` — the block is still locked (exercise not solved).
    pub fn insert(&mut self, def: BlockDef, solution: Option<Solution>, lock_hint: String) {
        let id = def.id.clone();
        if !self.defs.contains_key(&id) {
            self.order.push(id.clone());
        }
        self.defs.insert(id.clone(), Arc::new(def));
        match solution {
            Some(s) => {
                self.solutions.insert(id.clone(), Arc::new(s));
            }
            None => {
                self.solutions.remove(&id);
            }
        }
        self.hints.insert(id, lock_hint);
    }

    /// Block description.
    pub fn def(&self, id: &str) -> Option<&Arc<BlockDef>> {
        self.defs.get(id)
    }

    /// All blocks in insertion order.
    pub fn defs(&self) -> impl Iterator<Item = &Arc<BlockDef>> {
        self.order.iter().filter_map(|id| self.defs.get(id))
    }

    /// Circuit inside the block; `None` for a block not yet solved.
    pub fn solution(&self, id: &str) -> Option<&Arc<Solution>> {
        self.solutions.get(id)
    }

    /// Is the block unlocked?
    pub fn available(&self, id: &str) -> bool {
        self.solutions.contains_key(id)
    }

    /// What must be done for the block to unlock.
    pub fn lock_hint(&self, id: &str) -> &str {
        self.hints.get(id).map_or("", String::as_str)
    }
}

impl BlockLookup for BlockLibrary {
    fn lookup(&self, id: &str) -> Option<BlockEntry> {
        Some((self.defs.get(id)?.clone(), self.solutions.get(id)?.clone()))
    }
}

/* ============================================================
   Bus ends: ports and slices
   ============================================================ */

/// Ports of a circuit node: for [`TOP`] — the exercise's own ports, for an instance — its block's ports.
pub type PortsOf<'a> = dyn Fn(&str) -> Option<&'a [BlockPort]> + 'a;

/// Bus end resolved to ports.
#[derive(Debug, Clone, Copy)]
pub struct EndInfo<'a> {
    pub port: &'a BlockPort,
    /// Type of the selected field and its position inside the port.
    pub ty: Iface,
    pub offset: usize,
    pub length: usize,
}

/// Port and field a bus end points to.
pub fn end_info<'a>(end: &BusEnd, ports_of: &PortsOf<'a>) -> Option<EndInfo<'a>> {
    let port = ports_of(&end.node)?.iter().find(|p| p.name == end.port)?;
    let s = slice_of(port.ty, &end.path)?;
    Some(EndInfo { port, ty: s.ty, offset: s.offset, length: s.length })
}

/// Circuit nodes corresponding to the selected port field.
pub fn end_nodes<'a>(info: &EndInfo<'a>) -> &'a [String] {
    let nodes: &'a [String] = &info.port.nodes;
    let start = info.offset.min(nodes.len());
    let end = (info.offset + info.length).min(nodes.len());
    &nodes[start..end]
}

/// Where the signal comes from: for [`TOP`] — an exercise input (`In`), for a block — its output (`Out`).
pub fn is_source_end(end: &BusEnd, info: &EndInfo) -> bool {
    if end.node == TOP {
        info.port.dir == Dir::In
    } else {
        info.port.dir == Dir::Out
    }
}

/// Can they be connected: returns the reason for refusal.
pub fn connection_error(from: &BusEnd, to: &BusEnd, ports_of: &PortsOf) -> Option<String> {
    let (Some(a), Some(b)) = (end_info(from, ports_of), end_info(to, ports_of)) else {
        return Some(i18n::tr("No such port").into());
    };
    if !is_source_end(from, &a) {
        return Some(i18n::tr("A wire must start at an output").into());
    }
    if is_source_end(to, &b) {
        return Some(i18n::tr("A wire must end at an input").into());
    }
    if from.node == to.node && from.node != TOP {
        return Some(i18n::tr("A block cannot be wired to itself").into());
    }
    if !can_connect(a.ty, b.ty) {
        return Some(i18n::trf!("Type {0} does not fit {1} — an adapter is needed", a.ty.name(), b.ty.name()));
    }
    None
}

/// Adds a bus; old buses occupying the same input bits are replaced.
pub fn add_bus_wire(wires: &[BusWire], next: BusWire, ports_of: &PortsOf) -> Vec<BusWire> {
    let Some(target) = end_info(&next.to, ports_of) else {
        return wires.to_vec();
    };
    let mine: HashSet<&String> = end_nodes(&target).iter().collect();
    let mut kept: Vec<BusWire> = wires
        .iter()
        .filter(|w| {
            if w.to.node != next.to.node || w.to.port != next.to.port {
                return true;
            }
            match end_info(&w.to, ports_of) {
                None => true,
                Some(info) => !end_nodes(&info).iter().any(|n| mine.contains(n)),
            }
        })
        .cloned()
        .collect();
    kept.push(next);
    kept
}

/* ============================================================
   Expansion into a flat circuit
   ============================================================ */

/// Value of a flat-circuit node by its name.
pub type ValueScope<'a> = &'a dyn Fn(&str) -> NodeValue;

/// Nested block after expansion.
#[derive(Debug, Clone)]
pub struct SubExpansion {
    pub def: Arc<BlockDef>,
    pub solution: Arc<Solution>,
    pub expansion: Expansion,
}

/// Expanded solution: the flat circuit and information on where the block signals in it come from.
#[derive(Debug, Clone)]
pub struct Expansion {
    /// Flat circuit: gates (for nested blocks — prefixed with `instance__`) and wires.
    pub circuit: Circuit,
    subs: Vec<(String, SubExpansion)>,
    sub_index: HashMap<String, usize>,
    /// Who drives the leaf `instance|node`.
    driver: HashMap<String, (String, String)>,
    /// "Internal sources" of each block: its gates and the outputs of built-in memory.
    is_gate_of: HashMap<String, HashSet<String>>,
    /// For a solution of gates or memory, sources are not computed (always `None`).
    resolving: bool,
}

impl Expansion {
    fn flat(circuit: Circuit) -> Self {
        Expansion {
            circuit,
            subs: Vec::new(),
            sub_index: HashMap::new(),
            driver: HashMap::new(),
            is_gate_of: HashMap::new(),
            resolving: false,
        }
    }

    /// Nested blocks in instance order.
    pub fn subs(&self) -> &[(String, SubExpansion)] {
        &self.subs
    }

    /// Nested block by instance id.
    pub fn sub(&self, id: &str) -> Option<&SubExpansion> {
        self.sub_index.get(id).map(|i| &self.subs[*i].1)
    }

    /// Flat-circuit node whose value goes to the output node of a block instance.
    pub fn out_source(&self, inst: &str, out_node: &str) -> Option<String> {
        if !self.resolving {
            return None;
        }
        self.resolve_out(inst, out_node, &mut HashSet::new())
    }

    /// Flat-circuit node that drives the input node of a block instance.
    pub fn in_source(&self, inst: &str, in_node: &str) -> Option<String> {
        if !self.resolving {
            return None;
        }
        self.resolve_in(inst, in_node, &mut HashSet::new())
    }

    fn resolve_out(&self, inst: &str, out_node: &str, seen: &mut HashSet<String>) -> Option<String> {
        if inst == TOP {
            return Some(out_node.to_string()); // input of the exercise itself
        }
        let sub = self.sub(inst)?;
        let w = sub.expansion.circuit.wires.iter().find(|x| x.to.node == out_node)?;
        if self.is_gate_of.get(inst).is_some_and(|s| s.contains(&w.from.node)) {
            return Some(format!("{inst}__{}", w.from.node));
        }
        self.resolve_in(inst, &w.from.node, seen) // the output simply repeats the input
    }

    fn resolve_in(&self, inst: &str, in_node: &str, seen: &mut HashSet<String>) -> Option<String> {
        let key = format!("{inst}|{in_node}");
        if !seen.insert(key.clone()) {
            return None; // combinational loop made of wires only
        }
        let (node, leaf) = self.driver.get(&key)?;
        self.resolve_out(node, leaf, seen)
    }
}

/// All gates and memory outputs inside the flat circuit.
fn internal_sources(c: &Circuit) -> HashSet<String> {
    c.gates.iter().map(|g| g.id.clone()).chain(c.natives.iter().flat_map(|n| n.dout.iter().cloned())).collect()
}

/// Expands a solution into a flat circuit with the same external nodes (inputs A–F, output names).
/// A solution made of gates is returned as is.
pub fn expand(solution: &Solution, iface: &BlockInterface, lookup: &dyn BlockLookup) -> Expansion {
    let sol = match solution {
        Solution::Native(n) => {
            // the block's output nodes are the memory outputs; inside the block there is a single "chip"
            let id = "mem";
            let dout: Vec<String> = n.dout.iter().map(|d| format!("{id}.{d}")).collect();
            let wires = n.dout.iter().enumerate().map(|(i, d)| simple_wire(format!("w{i}"), &dout[i], d)).collect();
            return Expansion::flat(Circuit {
                gates: vec![],
                wires,
                natives: vec![NativeInstance {
                    id: id.into(),
                    kind: n.native,
                    addr: n.addr.iter().cloned().map(Some).collect(),
                    din: n.din.as_ref().map(|d| d.iter().cloned().map(Some).collect()),
                    we: n.we.clone(),
                    clk: n.clk.clone(),
                    dout,
                }],
            });
        }
        Solution::Gate(g) => return Expansion::flat(Circuit::new(g.gates.clone(), g.wires.clone())),
        Solution::Block(b) => b,
    };

    let mut subs: Vec<(String, SubExpansion)> = Vec::new();
    let mut sub_index: HashMap<String, usize> = HashMap::new();
    for inst in &sol.instances {
        if let Some((def, solution)) = lookup.lookup(&inst.block_id) {
            let sub = SubExpansion { expansion: expand(&solution, &def.iface, lookup), def, solution };
            match sub_index.get(&inst.id) {
                Some(i) => subs[*i].1 = sub,
                None => {
                    sub_index.insert(inst.id.clone(), subs.len());
                    subs.push((inst.id.clone(), sub));
                }
            }
        }
    }

    let ports_of = |node: &str| -> Option<&[BlockPort]> {
        if node == TOP {
            Some(&iface.ports)
        } else {
            sub_index.get(node).map(|i| subs[*i].1.def.iface.ports.as_slice())
        }
    };

    let mut driver: HashMap<String, (String, String)> = HashMap::new();
    for w in &sol.bus_wires {
        if connection_error(&w.from, &w.to, &ports_of).is_some() {
            continue;
        }
        let (Some(fi), Some(ti)) = (end_info(&w.from, &ports_of), end_info(&w.to, &ports_of)) else {
            continue;
        };
        let (src, dst) = (end_nodes(&fi), end_nodes(&ti));
        if src.len() != dst.len() {
            continue;
        }
        for (i, d) in dst.iter().enumerate() {
            driver.insert(format!("{}|{d}", w.to.node), (w.from.node.clone(), src[i].clone()));
        }
    }

    let is_gate_of: HashMap<String, HashSet<String>> =
        subs.iter().map(|(id, s)| (id.clone(), internal_sources(&s.expansion.circuit))).collect();

    // Next we need the source-resolution methods: build a "draft" expansion.
    let mut exp = Expansion {
        circuit: Circuit::default(),
        subs,
        sub_index,
        driver,
        is_gate_of,
        resolving: true,
    };

    let mut gates: Vec<GateInstance> = Vec::new();
    let mut wires: Vec<Wire> = Vec::new();
    let mut natives: Vec<NativeInstance> = Vec::new();

    for (inst, sub) in &exp.subs {
        let outs: HashSet<&String> = sub.def.iface.outputs.iter().collect();
        let internal = &exp.is_gate_of[inst];
        // node inside the block → flat-circuit node (own source — prefixed, block input — its driver)
        let map = |node: &str| -> Option<String> {
            if internal.contains(node) {
                Some(format!("{inst}__{node}"))
            } else {
                exp.resolve_in(inst, node, &mut HashSet::new())
            }
        };
        for n in &sub.expansion.circuit.natives {
            natives.push(NativeInstance {
                id: format!("{inst}__{}", n.id),
                kind: n.kind,
                addr: n.addr.iter().map(|a| a.as_deref().and_then(&map)).collect(),
                din: n.din.as_ref().map(|d| d.iter().map(|a| a.as_deref().and_then(&map)).collect()),
                we: n.we.as_deref().and_then(&map),
                clk: n.clk.as_deref().and_then(&map),
                dout: n.dout.iter().map(|d| format!("{inst}__{d}")).collect(),
            });
        }
        for g in &sub.expansion.circuit.gates {
            gates.push(GateInstance { id: format!("{inst}__{}", g.id), ..g.clone() });
        }
        for w in &sub.expansion.circuit.wires {
            if outs.contains(&w.to.node) {
                continue; // driving the output nodes is the block's internals
            }
            let Some(from) = map(&w.from.node) else {
                continue; // the block input is not connected to anything
            };
            wires.push(Wire {
                id: format!("{inst}__{}", w.id),
                from: PinRef::out(from),
                to: PinRef::inp(format!("{inst}__{}", w.to.node), w.to.pin),
            });
        }
    }

    for o in &iface.outputs {
        let src = exp
            .driver
            .get(&format!("{TOP}|{o}"))
            .and_then(|(node, leaf)| exp.resolve_out(node, leaf, &mut HashSet::new()));
        if let Some(src) = src {
            wires.push(simple_wire(format!("{TOP}out_{o}"), &src, o));
        }
    }

    exp.circuit = Circuit { gates, wires, natives };
    exp
}

/// Values inside a block instance from the values of the parent circuit.
pub fn child_scope<'a>(
    scope: ValueScope<'a>,
    parent: &'a Expansion,
    inst_id: &'a str,
    def: &'a BlockInterface,
) -> impl Fn(&str) -> NodeValue + 'a {
    move |node: &str| {
        let source = if def.inputs.iter().any(|n| n == node) {
            parent.in_source(inst_id, node)
        } else if def.outputs.iter().any(|n| n == node) {
            parent.out_source(inst_id, node)
        } else {
            Some(format!("{inst_id}__{node}"))
        };
        source.and_then(|s| scope(&s))
    }
}

/// Values of a port (or its field) in bit order.
pub fn port_values(scope: ValueScope, expansion: &Expansion, end: &BusEnd, ports_of: &PortsOf) -> Vec<NodeValue> {
    let Some(info) = end_info(end, ports_of) else {
        return Vec::new();
    };
    end_nodes(&info)
        .iter()
        .map(|node| {
            if end.node == TOP {
                scope(node)
            } else {
                let source = if info.port.dir == Dir::Out {
                    expansion.out_source(&end.node, node)
                } else {
                    expansion.in_source(&end.node, node)
                };
                source.and_then(|s| scope(&s))
            }
        })
        .collect()
}
