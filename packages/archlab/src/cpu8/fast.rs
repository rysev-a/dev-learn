//! Fast simulator for circuits without feedback loops, except flip-flops. Port of `cpu8/sim.ts`.
//!
//! The circuit is "compiled" once: gates are sorted by dependencies, and each evaluation is a single pass
//! over the array. This is hundreds of times faster than the general simulator ([`crate::eval`]) and is needed for the processor of ~1000
//! gates, which runs thousands of clock cycles per program.
//!
//! Values: 0, 1 and "unknown" (X = −1), as in the general simulator.

use crate::model::*;
use std::collections::HashMap;
use std::fmt;

const X: i8 = -1;

/// The circuit has a loop without a flip-flop.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CombinationalLoopError {
    pub nodes: Vec<String>,
}

impl fmt::Display for CombinationalLoopError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let head: Vec<&str> = self.nodes.iter().take(5).map(String::as_str).collect();
        write!(f, "{}", i18n::trf!("The circuit has a loop without a flip-flop: {0}…", head.join(", ")))
    }
}

impl std::error::Error for CombinationalLoopError {}

#[derive(Debug, Clone)]
struct Cell {
    ty: GateType,
    out: usize,
    /// Index of the source of input 0 (−1 — not connected).
    a: i32,
    b: i32,
}

#[derive(Debug, Clone)]
struct Dff {
    out: usize,
    d: i32,
    clk: i32,
    prev: i8,
}

#[derive(Debug, Clone)]
struct Native {
    id: String,
    kind: NativeKind,
    addr: Vec<i32>,
    din: Vec<i32>,
    dout: Vec<usize>,
    we: i32,
    clk: i32,
    prev: i8,
    /// Contents: words (rom: 16 bits) or bytes (ram).
    data: Vec<u16>,
}

#[derive(Debug, Clone, Copy)]
enum Element {
    Gate(usize),
    Native(usize),
}

/// Compiled circuit.
#[derive(Debug, Clone)]
pub struct CompiledSim {
    /// Values of all nodes; index — by the `index` table.
    v: Vec<i8>,
    index: HashMap<String, usize>,
    cells: Vec<Cell>,
    order: Vec<Element>,
    dffs: Vec<Dff>,
    natives: Vec<Native>,
    aliases: Vec<(usize, usize)>,
    /// How many gates are in the circuit (excluding flip-flops).
    pub gate_count: usize,
    /// How many flip-flops.
    pub dff_count: usize,
}

fn get_v(v: &[i8], i: i32) -> i8 {
    if i < 0 {
        X
    } else {
        v.get(i as usize).copied().unwrap_or(X)
    }
}

fn read_bits(v: &[i8], idxs: &[i32]) -> i32 {
    let mut r = 0i32;
    for i in idxs {
        let x = get_v(v, *i);
        if x < 0 {
            return -1;
        }
        r = (r << 1) | x as i32;
    }
    r
}

fn eval_gate(ty: GateType, a: i8, b: i8) -> i8 {
    match ty {
        GateType::Not => {
            if a < 0 {
                X
            } else {
                1 - a
            }
        }
        GateType::And => {
            if a == 0 || b == 0 {
                0
            } else if a < 0 || b < 0 {
                X
            } else {
                1
            }
        }
        GateType::Nand => {
            if a == 0 || b == 0 {
                1
            } else if a < 0 || b < 0 {
                X
            } else {
                0
            }
        }
        GateType::Or => {
            if a == 1 || b == 1 {
                1
            } else if a < 0 || b < 0 {
                X
            } else {
                0
            }
        }
        GateType::Nor => {
            if a == 1 || b == 1 {
                0
            } else if a < 0 || b < 0 {
                X
            } else {
                1
            }
        }
        GateType::Xor => {
            if a < 0 || b < 0 {
                X
            } else {
                a ^ b
            }
        }
        GateType::Xnor => {
            if a < 0 || b < 0 {
                X
            } else {
                1 - (a ^ b)
            }
        }
        GateType::Dff => X,
    }
}

impl CompiledSim {
    /// Compiles the circuit; a loop without a flip-flop is an error.
    pub fn new(circuit: &Circuit) -> Result<CompiledSim, CombinationalLoopError> {
        let mut ix = Indexer::default();

        let gate_ids: std::collections::HashSet<&str> = circuit.gates.iter().map(|g| g.id.as_str()).collect();
        let native_outs: std::collections::HashSet<&str> =
            circuit.natives.iter().flat_map(|n| n.dout.iter().map(String::as_str)).collect();

        // input source: wire.to → wire.from
        let mut source: HashMap<(&str, PinKind), &str> = HashMap::new();
        for w in &circuit.wires {
            source.insert((w.to.node.as_str(), w.to.pin), w.from.node.as_str());
        }

        for g in &circuit.gates {
            ix.idx(&g.id);
        }
        for n in &circuit.natives {
            for d in &n.dout {
                ix.idx(d);
            }
        }

        // exercise output nodes (neither a gate nor an input) simply repeat their source
        let mut aliases = Vec::new();
        for w in &circuit.wires {
            if !gate_ids.contains(w.to.node.as_str()) && !native_outs.contains(w.to.node.as_str()) {
                let out = ix.idx(&w.to.node);
                let src = ix.idx(&w.from.node);
                aliases.push((out, src));
            }
        }

        let mut cells: Vec<Cell> = Vec::new();
        let mut dffs: Vec<Dff> = Vec::new();
        for g in &circuit.gates {
            let a = source.get(&(g.id.as_str(), PinKind::In0)).copied();
            let b = if g.ty == GateType::Not { None } else { source.get(&(g.id.as_str(), PinKind::In1)).copied() };
            let out = ix.idx(&g.id);
            let (a, b) = (ix.reference(a), ix.reference(b));
            if g.ty == GateType::Dff {
                dffs.push(Dff { out, d: a, clk: b, prev: X });
            } else {
                cells.push(Cell { ty: g.ty, out, a, b });
            }
        }

        let mut natives: Vec<Native> = Vec::new();
        for inst in &circuit.natives {
            natives.push(Native {
                id: inst.id.clone(),
                kind: inst.kind,
                addr: inst.addr.iter().map(|a| ix.reference(a.as_deref())).collect(),
                din: inst.din.iter().flatten().map(|a| ix.reference(a.as_deref())).collect(),
                dout: inst.dout.iter().map(|d| ix.idx(d)).collect(),
                we: ix.reference(inst.we.as_deref()),
                clk: ix.reference(inst.clk.as_deref()),
                prev: X,
                data: vec![0; 1usize << inst.addr.len()],
            });
        }

        // all nodes referenced by anything must exist before the value array is created
        let index = ix.map;
        let mut v = vec![X; index.len() + 1];
        // input nodes (sources without a gate) start at zero, not at "unknown"
        for w in &circuit.wires {
            let n = w.from.node.as_str();
            if !gate_ids.contains(n) && !native_outs.contains(n) {
                if let Some(i) = index.get(n) {
                    v[*i] = 0;
                }
            }
        }
        for d in &dffs {
            v[d.out] = 0; // at power-on the flip-flops are zero
        }

        let gate_count = cells.len();
        let dff_count = dffs.len();
        let mut sim = CompiledSim { v, index, cells, order: Vec::new(), dffs, natives, aliases, gate_count, dff_count };
        sim.order = sim.sort()?;
        sim.settle();
        Ok(sim)
    }

    /// Ordering by dependencies; a loop without a flip-flop is an error.
    fn sort(&self) -> Result<Vec<Element>, CombinationalLoopError> {
        let elements: Vec<Element> = (0..self.cells.len())
            .map(Element::Gate)
            .chain((0..self.natives.len()).map(Element::Native))
            .collect();
        let mut producer: HashMap<usize, usize> = HashMap::new();
        for (i, e) in elements.iter().enumerate() {
            match e {
                Element::Gate(c) => {
                    producer.insert(self.cells[*c].out, i);
                }
                Element::Native(n) => {
                    for o in &self.natives[*n].dout {
                        producer.insert(*o, i);
                    }
                }
            }
        }
        let deps = |e: &Element| -> Vec<usize> {
            let list: Vec<i32> = match e {
                Element::Gate(c) => vec![self.cells[*c].a, self.cells[*c].b],
                Element::Native(n) => self.natives[*n].addr.clone(),
            };
            list.into_iter().filter(|x| *x >= 0).map(|x| x as usize).collect()
        };
        let names = || {
            let mut names = vec![String::new(); self.index.len()];
            for (k, i) in &self.index {
                names[*i] = k.clone();
            }
            names
        };

        let mut state = vec![0u8; elements.len()]; // 0 — not seen, 1 — in progress, 2 — done
        let mut result = Vec::with_capacity(elements.len());

        // depth-first traversal without recursion: the circuit may be hundreds of levels deep
        struct Frame {
            i: usize,
            next: usize,
            d: Vec<usize>,
        }
        for start in 0..elements.len() {
            if state[start] != 0 {
                continue;
            }
            let mut stack = vec![Frame { i: start, next: 0, d: deps(&elements[start]) }];
            state[start] = 1;
            while let Some(top) = stack.last_mut() {
                if top.next < top.d.len() {
                    let dep = top.d[top.next];
                    top.next += 1;
                    let Some(p) = producer.get(&dep).copied() else { continue };
                    if state[p] == 2 {
                        continue;
                    }
                    if state[p] == 1 {
                        let names = names();
                        let nodes = stack
                            .iter()
                            .map(|f| match elements[f.i] {
                                Element::Gate(c) => names[self.cells[c].out].clone(),
                                Element::Native(n) => names[self.natives[n].dout.first().copied().unwrap_or(0)].clone(),
                            })
                            .collect();
                        return Err(CombinationalLoopError { nodes });
                    }
                    state[p] = 1;
                    let d = deps(&elements[p]);
                    stack.push(Frame { i: p, next: 0, d });
                } else {
                    state[top.i] = 2;
                    result.push(elements[top.i]);
                    stack.pop();
                }
            }
        }
        Ok(result)
    }

    /* ---------- values ---------- */

    /// Does such a node exist.
    pub fn has(&self, node: &str) -> bool {
        self.index.contains_key(node)
    }

    /// Node value; `None` — "unknown" or no such node.
    pub fn get(&self, node: &str) -> NodeValue {
        let i = *self.index.get(node)?;
        match self.v[i] {
            X => None,
            x => Some(x as Bit),
        }
    }

    /// Set an input value: any non-zero number — one.
    pub fn set(&mut self, node: &str, value: i32) {
        if let Some(i) = self.index.get(node) {
            self.v[*i] = (value != 0) as i8;
        }
    }

    /// Evaluation of the whole combinational part: a single pass.
    pub fn settle(&mut self) {
        for k in 0..self.order.len() {
            match self.order[k] {
                Element::Gate(c) => {
                    let Cell { ty, out, a, b } = self.cells[c].clone();
                    let x = get_v(&self.v, a);
                    let y = get_v(&self.v, b);
                    self.v[out] = eval_gate(ty, x, y);
                }
                Element::Native(ni) => {
                    let n = &self.natives[ni];
                    let addr = read_bits(&self.v, &n.addr);
                    let word: i32 = if addr < 0 { -1 } else { n.data.get(addr as usize).copied().unwrap_or(0) as i32 };
                    let w = n.dout.len();
                    for (k, o) in n.dout.iter().enumerate() {
                        self.v[*o] = if word < 0 { X } else { ((word >> (w - 1 - k)) & 1) as i8 };
                    }
                }
            }
        }
        for (out, src) in &self.aliases {
            self.v[*out] = self.v[*src];
        }
    }

    /// One clock period: CLK = 0, then the edge 0 → 1 and back to 0. Flip-flops and memory writes take
    /// the values computed BEFORE the edge. No clock node — an error with a clear message.
    pub fn pulse(&mut self, clk_node: &str) -> Result<(), String> {
        let c = *self.index.get(clk_node).ok_or_else(|| i18n::trf!("No clock node “{0}”", clk_node))?;
        self.v[c] = 0;
        self.settle();
        for d in &mut self.dffs {
            d.prev = get_v(&self.v, d.clk);
        }
        for n in &mut self.natives {
            n.prev = get_v(&self.v, n.clk);
        }

        self.v[c] = 1;
        self.settle(); // the clock has risen: gates on the clock path (if any) have been recomputed

        // what needs to be "latched" — choose while nothing has changed yet
        let mut latched: Vec<(usize, i8)> = Vec::new();
        for d in &self.dffs {
            if d.prev == 0 && d.clk >= 0 && get_v(&self.v, d.clk) == 1 {
                latched.push((d.out, get_v(&self.v, d.d)));
            }
        }
        let mut writes: Vec<(usize, usize, u16)> = Vec::new();
        for (ni, n) in self.natives.iter().enumerate() {
            if n.kind != NativeKind::Ram || !(n.prev == 0 && n.clk >= 0 && get_v(&self.v, n.clk) == 1) || get_v(&self.v, n.we) != 1 {
                continue;
            }
            let addr = read_bits(&self.v, &n.addr);
            let value = read_bits(&self.v, &n.din);
            if addr >= 0 && value >= 0 {
                writes.push((ni, addr as usize, value as u16));
            }
        }
        for (out, value) in latched {
            self.v[out] = value;
        }
        for (ni, addr, value) in writes {
            if let Some(slot) = self.natives[ni].data.get_mut(addr) {
                *slot = value;
            }
        }

        self.settle();
        self.v[c] = 0;
        self.settle();
        Ok(())
    }

    /* ---------- memory ---------- */

    fn native_mut(&mut self, id: &str, kind: NativeKind) -> Result<&mut Native, String> {
        match self.natives.iter_mut().find(|n| n.id == id && n.kind == kind) {
            Some(n) => Ok(n),
            None => Err(i18n::trf!("No memory “{0}” of kind {1}", id, if kind == NativeKind::Rom { "rom" } else { "ram" })),
        }
    }

    /// Load a program into ROM (16-bit words).
    pub fn load_rom(&mut self, id: &str, words: &[u16]) -> Result<(), String> {
        let n = self.native_mut(id, NativeKind::Rom)?;
        n.data.fill(0);
        for (i, w) in words.iter().enumerate() {
            if let Some(slot) = n.data.get_mut(i) {
                *slot = *w;
            }
        }
        self.settle();
        Ok(())
    }

    /// Load a disk into RAM (bytes).
    pub fn load_ram(&mut self, id: &str, bytes: &[u8]) -> Result<(), String> {
        let n = self.native_mut(id, NativeKind::Ram)?;
        n.data.fill(0);
        for (i, b) in bytes.iter().enumerate() {
            if let Some(slot) = n.data.get_mut(i) {
                *slot = *b as u16;
            }
        }
        self.settle();
        Ok(())
    }

    /// Copy of memory contents.
    pub fn memory(&self, id: &str) -> Result<Vec<u16>, String> {
        self.natives.iter().find(|n| n.id == id).map(|n| n.data.clone()).ok_or_else(|| i18n::trf!("No memory “{0}”", id))
    }

    /// Is there a memory with this id.
    pub fn has_native(&self, id: &str) -> bool {
        self.natives.iter().any(|n| n.id == id)
    }

    /// Number from node values (most significant first); `None` if something is "unknown".
    pub fn read(&self, nodes: &[String]) -> Option<u32> {
        let mut r = 0u32;
        for n in nodes {
            r = (r << 1) | self.get(n)? as u32;
        }
        Some(r)
    }
}

/// Numbering of nodes by name.
#[derive(Default)]
struct Indexer {
    map: HashMap<String, usize>,
}

impl Indexer {
    fn idx(&mut self, name: &str) -> usize {
        let n = self.map.len();
        *self.map.entry(name.to_string()).or_insert(n)
    }

    /// Reference to a node: index or −1 if the node is not given.
    fn reference(&mut self, node: Option<&str>) -> i32 {
        match node {
            Some(n) => self.idx(n) as i32,
            None => -1,
        }
    }
}
