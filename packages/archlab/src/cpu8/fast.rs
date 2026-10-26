//! Быстрый симулятор схем без обратных связей, кроме триггеров. Порт `cpu8/sim.ts`.
//!
//! Схема «компилируется» один раз: вентили упорядочиваются по зависимостям, и каждый расчёт — один проход
//! по массиву. Это в сотни раз быстрее общего симулятора ([`crate::eval`]) и нужно для процессора на ~1000
//! вентилей, который за программу делает тысячи тактов.
//!
//! Значения: 0, 1 и «неизвестно» (X = −1), как в общем симуляторе.

use crate::model::*;
use std::collections::HashMap;
use std::fmt;

const X: i8 = -1;

/// В схеме есть петля без триггера.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CombinationalLoopError {
    pub nodes: Vec<String>,
}

impl fmt::Display for CombinationalLoopError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let head: Vec<&str> = self.nodes.iter().take(5).map(String::as_str).collect();
        write!(f, "В схеме есть петля без триггера: {}…", head.join(", "))
    }
}

impl std::error::Error for CombinationalLoopError {}

#[derive(Debug, Clone)]
struct Cell {
    ty: GateType,
    out: usize,
    /// Индекс источника входа 0 (−1 — не подключён).
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
    /// Содержимое: слова (rom: 16 бит) или байты (ram).
    data: Vec<u16>,
}

#[derive(Debug, Clone, Copy)]
enum Element {
    Gate(usize),
    Native(usize),
}

/// Скомпилированная схема.
#[derive(Debug, Clone)]
pub struct CompiledSim {
    /// Значения всех узлов; индекс — по таблице `index`.
    v: Vec<i8>,
    index: HashMap<String, usize>,
    cells: Vec<Cell>,
    order: Vec<Element>,
    dffs: Vec<Dff>,
    natives: Vec<Native>,
    aliases: Vec<(usize, usize)>,
    /// Сколько вентилей в схеме (без триггеров).
    pub gate_count: usize,
    /// Сколько триггеров.
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
    /// Компилирует схему; петля без триггера — ошибка.
    pub fn new(circuit: &Circuit) -> Result<CompiledSim, CombinationalLoopError> {
        let mut ix = Indexer::default();

        let gate_ids: std::collections::HashSet<&str> = circuit.gates.iter().map(|g| g.id.as_str()).collect();
        let native_outs: std::collections::HashSet<&str> =
            circuit.natives.iter().flat_map(|n| n.dout.iter().map(String::as_str)).collect();

        // источник входа: wire.to → wire.from
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

        // выходные узлы упражнения (не вентиль и не вход) — просто повторяют источник
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

        // все узлы, на которые что-то ссылается, должны существовать до создания массива значений
        let index = ix.map;
        let mut v = vec![X; index.len() + 1];
        // узлы-входы (источники без вентиля) стартуют с нуля, а не с «неизвестно»
        for w in &circuit.wires {
            let n = w.from.node.as_str();
            if !gate_ids.contains(n) && !native_outs.contains(n) {
                if let Some(i) = index.get(n) {
                    v[*i] = 0;
                }
            }
        }
        for d in &dffs {
            v[d.out] = 0; // при включении триггеры в нуле
        }

        let gate_count = cells.len();
        let dff_count = dffs.len();
        let mut sim = CompiledSim { v, index, cells, order: Vec::new(), dffs, natives, aliases, gate_count, dff_count };
        sim.order = sim.sort()?;
        sim.settle();
        Ok(sim)
    }

    /// Упорядочивание по зависимостям; петля без триггера — ошибка.
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

        let mut state = vec![0u8; elements.len()]; // 0 — не видели, 1 — внутри, 2 — готово
        let mut result = Vec::with_capacity(elements.len());

        // обход в глубину без рекурсии: схема может быть глубиной в сотни уровней
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

    /* ---------- значения ---------- */

    /// Есть ли такой узел.
    pub fn has(&self, node: &str) -> bool {
        self.index.contains_key(node)
    }

    /// Значение узла; `None` — «неизвестно» или узла нет.
    pub fn get(&self, node: &str) -> NodeValue {
        let i = *self.index.get(node)?;
        match self.v[i] {
            X => None,
            x => Some(x as Bit),
        }
    }

    /// Задать значение входа: любое ненулевое число — единица.
    pub fn set(&mut self, node: &str, value: i32) {
        if let Some(i) = self.index.get(node) {
            self.v[*i] = (value != 0) as i8;
        }
    }

    /// Расчёт всей комбинационной части: один проход.
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

    /// Один период такта: CLK = 0, затем фронт 0 → 1 и снова 0. Триггеры и запись в память берут
    /// значения, посчитанные ДО фронта. Нет узла такта — ошибка с понятным текстом.
    pub fn pulse(&mut self, clk_node: &str) -> Result<(), String> {
        let c = *self.index.get(clk_node).ok_or_else(|| format!("Нет узла такта «{clk_node}»"))?;
        self.v[c] = 0;
        self.settle();
        for d in &mut self.dffs {
            d.prev = get_v(&self.v, d.clk);
        }
        for n in &mut self.natives {
            n.prev = get_v(&self.v, n.clk);
        }

        self.v[c] = 1;
        self.settle(); // такт поднялся: вентили на пути такта (если есть) пересчитались

        // что нужно «защёлкнуть» — выбираем, пока ничего не изменилось
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

    /* ---------- память ---------- */

    fn native_mut(&mut self, id: &str, kind: NativeKind) -> Result<&mut Native, String> {
        match self.natives.iter_mut().find(|n| n.id == id && n.kind == kind) {
            Some(n) => Ok(n),
            None => Err(format!("Нет памяти «{id}» вида {}", if kind == NativeKind::Rom { "rom" } else { "ram" })),
        }
    }

    /// Загрузить программу в ПЗУ (слова по 16 бит).
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

    /// Загрузить диск в ОЗУ (байты).
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

    /// Копия содержимого памяти.
    pub fn memory(&self, id: &str) -> Result<Vec<u16>, String> {
        self.natives.iter().find(|n| n.id == id).map(|n| n.data.clone()).ok_or_else(|| format!("Нет памяти «{id}»"))
    }

    /// Есть ли память с таким id.
    pub fn has_native(&self, id: &str) -> bool {
        self.natives.iter().any(|n| n.id == id)
    }

    /// Число из значений узлов (старший первым); `None`, если где-то «неизвестно».
    pub fn read(&self, nodes: &[String]) -> Option<u32> {
        let mut r = 0u32;
        for n in nodes {
            r = (r << 1) | self.get(n)? as u32;
        }
        Some(r)
    }
}

/// Нумерация узлов по именам.
#[derive(Default)]
struct Indexer {
    map: HashMap<String, usize>,
}

impl Indexer {
    fn idx(&mut self, name: &str) -> usize {
        let n = self.map.len();
        *self.map.entry(name.to_string()).or_insert(n)
    }

    /// Ссылка на узел: индекс или −1, если узел не задан.
    fn reference(&mut self, node: Option<&str>) -> i32 {
        match node {
            Some(n) => self.idx(n) as i32,
            None => -1,
        }
    }
}
