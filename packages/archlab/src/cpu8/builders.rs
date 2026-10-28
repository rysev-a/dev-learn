//! Processor circuit constructors: gates, wires and blocks are assembled by code rather than drawn by hand.
//! Port of `cpu8/builders.ts`: the order of gate creation and their names (`and12`, `or7`…) match TS.

use crate::blocks::*;
use crate::interfaces::{leaf_paths, Iface};
use crate::model::*;
use std::cell::RefCell;
use std::collections::HashMap;

/// Types whose nodes are named by bit numbers: `Byte` → `a7…a0`.
fn numbered(ty: Iface) -> bool {
    matches!(ty, Iface::Byte | Iface::Reg3 | Iface::Op4 | Iface::Imm6 | Iface::Instr16 | Iface::Word2 | Iface::Addr2 | Iface::Op2)
}

/// Node names of a port in bit order (most significant first).
pub fn nodes_of(name: &str, ty: Iface) -> Vec<String> {
    let leaves = leaf_paths(ty, "");
    if leaves.len() == 1 {
        return vec![name.to_string()];
    }
    if numbered(ty) {
        return (0..leaves.len()).map(|i| format!("{name}{}", leaves.len() - 1 - i)).collect();
    }
    leaves.iter().map(|p| format!("{name}_{}", p.replace('.', "_"))).collect()
}

/// Node of bit number `i` (0 — least significant) of a numeric port.
pub fn bit(name: &str, i: usize) -> String {
    format!("{name}{i}")
}

/// Field node of a non-numeric port (`Ctrl`, `Oh8`): `field("ctl", "isBeq")`.
pub fn field(name: &str, f: &str) -> String {
    format!("{name}_{f}")
}

/// Port description: name, type, direction.
pub type PortSpec = (String, Iface, Dir);

/// Input port.
pub fn pin(name: impl Into<String>, ty: Iface) -> PortSpec {
    (name.into(), ty, Dir::In)
}

/// Output port.
pub fn pout(name: impl Into<String>, ty: Iface) -> PortSpec {
    (name.into(), ty, Dir::Out)
}

/// Block description by ports.
pub fn make_def(id: &str, title: &str, specs: &[PortSpec]) -> BlockDef {
    let ports: Vec<BlockPort> = specs
        .iter()
        .map(|(name, ty, dir)| BlockPort { name: name.clone(), ty: *ty, dir: *dir, nodes: nodes_of(name, *ty) })
        .collect();
    BlockDef {
        id: id.into(),
        title: title.into(),
        iface: BlockInterface {
            inputs: ports.iter().filter(|p| p.dir == Dir::In).flat_map(|p| p.nodes.clone()).collect(),
            outputs: ports.iter().filter(|p| p.dir == Dir::Out).flat_map(|p| p.nodes.clone()).collect(),
            labels: None,
            ports,
        },
        source: None,
    }
}

/// Block with contents.
#[derive(Debug, Clone)]
pub struct GeneratedBlock {
    pub def: BlockDef,
    pub solution: Solution,
}

fn wire(id: String, from: &str, to: &str, pin: PinKind) -> Wire {
    Wire { id, from: PinRef::out(from), to: PinRef::inp(to, pin) }
}

#[derive(Default)]
struct GbInner {
    gates: Vec<GateInstance>,
    wires: Vec<Wire>,
    n: usize,
    depth: HashMap<String, usize>,
}

/// Gate circuit constructor: each method creates a gate and returns its name as a source.
/// Methods take `&self` (state in an interior cell) so that calls can be nested:
/// `g.or(g.and(a, b), g.and(c, d))`.
#[derive(Default)]
pub struct GateBuilder {
    inner: RefCell<GbInner>,
}

impl GateBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    fn add(&self, ty: GateType, a: &str, b: Option<&str>, named: Option<&str>) -> String {
        let mut s = self.inner.borrow_mut();
        let id = match named {
            Some(n) => n.to_string(),
            None => {
                s.n += 1;
                format!("{}{}", ty.name().to_lowercase(), s.n)
            }
        };
        s.gates.push(GateInstance { id: id.clone(), ty, x: 0.0, y: 0.0 });
        s.wires.push(wire(format!("{id}a"), a, &id, PinKind::In0));
        if let Some(b) = b {
            s.wires.push(wire(format!("{id}b"), b, &id, PinKind::In1));
        }
        let da = s.depth.get(a).copied().unwrap_or(0);
        let db = b.map_or(0, |b| s.depth.get(b).copied().unwrap_or(0));
        s.depth.insert(id.clone(), 1 + da.max(db));
        id
    }

    pub fn not(&self, a: impl AsRef<str>) -> String {
        self.add(GateType::Not, a.as_ref(), None, None)
    }
    pub fn and(&self, a: impl AsRef<str>, b: impl AsRef<str>) -> String {
        self.add(GateType::And, a.as_ref(), Some(b.as_ref()), None)
    }
    pub fn or(&self, a: impl AsRef<str>, b: impl AsRef<str>) -> String {
        self.add(GateType::Or, a.as_ref(), Some(b.as_ref()), None)
    }
    pub fn xor(&self, a: impl AsRef<str>, b: impl AsRef<str>) -> String {
        self.add(GateType::Xor, a.as_ref(), Some(b.as_ref()), None)
    }
    pub fn xnor(&self, a: impl AsRef<str>, b: impl AsRef<str>) -> String {
        self.add(GateType::Xnor, a.as_ref(), Some(b.as_ref()), None)
    }

    /// Flip-flop with a predefined name — so the circuit can refer to its output before it is created.
    pub fn dff_at(&self, id: &str, d: impl AsRef<str>, clk: impl AsRef<str>) -> String {
        self.add(GateType::Dff, d.as_ref(), Some(clk.as_ref()), Some(id))
    }

    /// AND of several signals — a tree of two-input gates.
    pub fn and_all<S: AsRef<str>>(&self, xs: &[S]) -> String {
        self.tree(xs, |a, b| self.and(a, b))
    }

    /// OR of several signals — a tree of two-input gates.
    pub fn or_all<S: AsRef<str>>(&self, xs: &[S]) -> String {
        self.tree(xs, |a, b| self.or(a, b))
    }

    fn tree<S: AsRef<str>>(&self, xs: &[S], op: impl Fn(&str, &str) -> String) -> String {
        let mut layer: Vec<String> = xs.iter().map(|s| s.as_ref().to_string()).collect();
        while layer.len() > 1 {
            let mut next = Vec::new();
            let mut i = 0;
            while i < layer.len() {
                next.push(if i + 1 < layer.len() { op(&layer[i], &layer[i + 1]) } else { layer[i].clone() });
                i += 2;
            }
            layer = next;
        }
        layer.pop().unwrap_or_default() // an empty tree is never created: the lists in the catalog are fixed
    }

    /// Route a source to an output node of the block.
    pub fn out(&self, node: impl AsRef<str>, src: impl AsRef<str>) {
        let node = node.as_ref();
        self.inner.borrow_mut().wires.push(wire(format!("out_{node}"), src.as_ref(), node, PinKind::In0));
    }

    /// Layout by layers: the farther from the input, the further right.
    pub fn build(self) -> GateSolution {
        let GbInner { mut gates, wires, depth, .. } = self.inner.into_inner();
        let mut columns: Vec<(usize, Vec<usize>)> = Vec::new();
        for (i, g) in gates.iter().enumerate() {
            let d = depth.get(&g.id).copied().unwrap_or(1);
            match columns.iter_mut().find(|(cd, _)| *cd == d) {
                Some((_, list)) => list.push(i),
                None => columns.push((d, vec![i])),
            }
        }
        let max_depth = columns.iter().map(|(d, _)| *d).max().unwrap_or(1).max(1);
        let x_step = 110f64.min(540.0 / max_depth.max(1) as f64);
        for (d, list) in &columns {
            for (k, gi) in list.iter().enumerate() {
                gates[*gi].x = 150.0 + (*d as f64 - 1.0) * x_step;
                gates[*gi].y = 20.0 + k as f64 * 62.0;
            }
        }
        GateSolution { gates, wires }
    }
}

/// Block made of gates: port description and a build function.
pub fn gate_block(id: &str, title: &str, specs: &[PortSpec], make: impl FnOnce(&GateBuilder)) -> GeneratedBlock {
    let def = make_def(id, title, specs);
    let g = GateBuilder::new();
    make(&g);
    GeneratedBlock { def, solution: Solution::Gate(g.build()) }
}

/// Block made of wires only (renaming, field layout, sign extension).
pub fn wire_block(id: &str, title: &str, specs: &[PortSpec], links: &[(String, String)]) -> GeneratedBlock {
    let def = make_def(id, title, specs);
    let wires = links.iter().enumerate().map(|(i, (f, t))| wire(format!("w{i}"), f, t, PinKind::In0)).collect();
    GeneratedBlock { def, solution: Solution::Gate(GateSolution { gates: vec![], wires }) }
}

/// Built-in memory.
pub fn native_block(id: &str, title: &str, specs: &[PortSpec], make: impl FnOnce(&BlockDef) -> NativeSolution) -> GeneratedBlock {
    let def = make_def(id, title, specs);
    let solution = Solution::Native(make(&def));
    GeneratedBlock { def, solution }
}

/// Block circuit constructor: place instances and run buses.
#[derive(Default)]
pub struct HierBuilder {
    instances: Vec<BlockInstance>,
    bus_wires: Vec<BusWire>,
    n: usize,
}

impl HierBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    /// Place a block; without coordinates — on a three-column grid, top to bottom.
    pub fn inst(&mut self, id: &str, block_id: &str) -> &mut Self {
        let i = self.instances.len();
        self.inst_at(id, block_id, 150.0 + (i % 3) as f64 * 196.0, 20.0 + (i / 3) as f64 * 190.0)
    }

    /// Place a block at the given position.
    pub fn inst_at(&mut self, id: &str, block_id: &str, x: f64, y: f64) -> &mut Self {
        self.instances.push(BlockInstance { id: id.into(), block_id: block_id.into(), x, y });
        self
    }

    /// Wire: `link("alu.res", "wb.d0")`, `link("$.clk", "pc.clk")`, with a field: `link("rom.word.op", "dec.op")`.
    pub fn link(&mut self, from: &str, to: &str) -> &mut Self {
        self.n += 1;
        let id = format!("b{}", self.n);
        self.bus_wires.push(BusWire { id, from: end(from), to: end(to) });
        self
    }

    pub fn build(self) -> BlockSolution {
        BlockSolution { instances: self.instances, bus_wires: self.bus_wires }
    }
}

/// Bus end from the notation `node.port[.field…]`; `$` — the ports of the block itself. Malformed notation
/// (no port) is a catalog programmer's error: the port name comes out empty and the bus will not connect.
fn end(r: &str) -> BusEnd {
    let mut it = r.split('.');
    let node = it.next().unwrap_or("");
    let port = it.next().unwrap_or("");
    let path: Vec<&str> = it.collect();
    BusEnd { node: if node == "$" { TOP.to_string() } else { node.to_string() }, port: port.to_string(), path: path.join(".") }
}

/// Block made of blocks.
pub fn hier_block(id: &str, title: &str, specs: &[PortSpec], make: impl FnOnce(&mut HierBuilder)) -> GeneratedBlock {
    let def = make_def(id, title, specs);
    let mut h = HierBuilder::new();
    make(&mut h);
    GeneratedBlock { def, solution: Solution::Block(h.build()) }
}
