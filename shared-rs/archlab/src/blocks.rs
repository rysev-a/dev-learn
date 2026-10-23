//! Блоки: решённое упражнение становится блоком, у которого есть порты типов интерфейсов.
//! Блоки соединяются шинами; перед симуляцией схема из блоков разворачивается в плоскую схему из
//! вентилей — поэтому симулятор [`crate::eval`] работает без изменений. Порт `blocks.ts`.

use crate::interfaces::{can_connect, slice_of, Iface};
use crate::model::*;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::sync::Arc;

/* ============================================================
   Модель
   ============================================================ */

/// Узел шин для портов самого упражнения (вместо id экземпляра блока).
pub const TOP: &str = "$";

/// Экземпляр блока на доске блоков.
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

/// Конец шины: `node` — id экземпляра блока либо [`TOP`]; `path` — путь к полю внутри типа порта
/// (`""` — весь порт, `"op"`, `"k.D1"`).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BusEnd {
    pub node: String,
    pub port: String,
    #[serde(default)]
    pub path: String,
}

impl BusEnd {
    /// Конец шины: `BusEnd::new("rom", "instr", "op")`.
    pub fn new(node: &str, port: &str, path: &str) -> Self {
        BusEnd { node: node.into(), port: port.into(), path: path.into() }
    }
}

/// Шина — провод на целый интерфейс или его поле.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BusWire {
    pub id: String,
    pub from: BusEnd,
    pub to: BusEnd,
}

/// Решение из вентилей.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GateSolution {
    pub gates: Vec<GateInstance>,
    pub wires: Vec<Wire>,
}

/// Решение из блоков.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockSolution {
    pub instances: Vec<BlockInstance>,
    #[serde(alias = "busWires")]
    pub bus_wires: Vec<BusWire>,
}

/// Встроенная память: в схеме это «чёрный ящик» с адресом и данными, ячейки не из вентилей.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NativeSolution {
    pub native: NativeKind,
    /// Узлы адреса, старший бит первым.
    pub addr: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub din: Option<Vec<String>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub we: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub clk: Option<String>,
    pub dout: Vec<String>,
}

/// Решение упражнения или содержимое блока: вентили, блоки или встроенная память.
/// В JSON — одна из трёх форм: `{gates, wires}`, `{instances, bus_wires}` (также `busWires`), `{native, …}`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Solution {
    Block(BlockSolution),
    Gate(GateSolution),
    Native(NativeSolution),
}

impl Solution {
    /// Разбор присланного решения с понятной ошибкой (TS: `isSolution` + `JSON.parse`).
    pub fn from_json(text: &str) -> Result<Solution, String> {
        let v: serde_json::Value = serde_json::from_str(text).map_err(|e| format!("не JSON: {e}"))?;
        let Some(o) = v.as_object() else {
            return Err("решение должно быть объектом".into());
        };
        let arr = |k: &str| o.get(k).is_some_and(|x| x.is_array());
        if !((arr("gates") && arr("wires")) || (arr("instances") && (arr("bus_wires") || arr("busWires"))) || o.contains_key("native")) {
            return Err("ожидалась схема: {gates, wires} или {instances, bus_wires}".into());
        }
        serde_json::from_value(v).map_err(|e| format!("схема не разобрана: {e}"))
    }

    /// Схема из блоков?
    pub fn is_block(&self) -> bool {
        matches!(self, Solution::Block(_))
    }
}

/// Направление порта.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Dir {
    /// Порт принимает сигнал.
    In,
    /// Порт выдаёт сигнал.
    Out,
}

/// Порт блока: имя, тип интерфейса и узлы схемы по порядку бит (старший — первый).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockPort {
    pub name: String,
    #[serde(rename = "type")]
    pub ty: Iface,
    pub dir: Dir,
    pub nodes: Vec<String>,
}

/// Внешняя «розетка» схемы — те узлы, которыми она торчит наружу.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct BlockInterface {
    pub inputs: Vec<String>,
    pub outputs: Vec<String>,
    /// Подписи входов по порядку `inputs`.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub labels: Option<Vec<String>>,
    pub ports: Vec<BlockPort>,
}

/// Откуда блок взят: упражнение, чьё решение лежит внутри.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockSource {
    pub section_slug: String,
    pub exercise_id: String,
}

/// Описание блока.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockDef {
    pub id: String,
    pub title: String,
    #[serde(flatten)]
    pub iface: BlockInterface,
    /// У встроенных блоков — `None`.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub source: Option<BlockSource>,
}

/// Блок вместе с содержимым.
pub type BlockEntry = (Arc<BlockDef>, Arc<Solution>);

/// Поиск блока по id: то, чем [`expand`] достаёт содержимое вложенных блоков.
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

/// Переходник между типами: схема из одних проводов (D1 → A1, D0 → A0).
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

/// Библиотека блоков: определения, их содержимое (если блок «открыт») и подсказки для закрытых.
#[derive(Debug, Clone, Default)]
pub struct BlockLibrary {
    order: Vec<String>,
    defs: HashMap<String, Arc<BlockDef>>,
    solutions: HashMap<String, Arc<Solution>>,
    hints: HashMap<String, String>,
}

impl BlockLibrary {
    /// Библиотека со встроенными блоками (переходники слово ↔ адрес — доступны сразу).
    pub fn builtin() -> Self {
        let mut lib = BlockLibrary::default();
        for (def, sol) in [
            adapter("adapter-w2a", "Слово → адрес", Iface::Word2, Iface::Addr2, ["A", "B"], ["Y1", "Y0"]),
            adapter("adapter-a2w", "Адрес → слово", Iface::Addr2, Iface::Word2, ["A", "B"], ["Y1", "Y0"]),
        ] {
            lib.insert(def, Some(sol), String::new());
        }
        lib
    }

    /// Добавить блок; `solution = None` — блок ещё закрыт (упражнение не решено).
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

    /// Описание блока.
    pub fn def(&self, id: &str) -> Option<&Arc<BlockDef>> {
        self.defs.get(id)
    }

    /// Все блоки в порядке добавления.
    pub fn defs(&self) -> impl Iterator<Item = &Arc<BlockDef>> {
        self.order.iter().filter_map(|id| self.defs.get(id))
    }

    /// Схема внутри блока; у ещё не решённого блока — `None`.
    pub fn solution(&self, id: &str) -> Option<&Arc<Solution>> {
        self.solutions.get(id)
    }

    /// Блок открыт?
    pub fn available(&self, id: &str) -> bool {
        self.solutions.contains_key(id)
    }

    /// Что нужно сделать, чтобы блок открылся.
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
   Концы шин: порты и срезы
   ============================================================ */

/// Порты узла схемы: у [`TOP`] — порты самого упражнения, у экземпляра — порты его блока.
pub type PortsOf<'a> = dyn Fn(&str) -> Option<&'a [BlockPort]> + 'a;

/// Конец шины, разобранный по портам.
#[derive(Debug, Clone, Copy)]
pub struct EndInfo<'a> {
    pub port: &'a BlockPort,
    /// Тип выбранного поля и его положение внутри порта.
    pub ty: Iface,
    pub offset: usize,
    pub length: usize,
}

/// Порт и поле, на которые указывает конец шины.
pub fn end_info<'a>(end: &BusEnd, ports_of: &PortsOf<'a>) -> Option<EndInfo<'a>> {
    let port = ports_of(&end.node)?.iter().find(|p| p.name == end.port)?;
    let s = slice_of(port.ty, &end.path)?;
    Some(EndInfo { port, ty: s.ty, offset: s.offset, length: s.length })
}

/// Узлы схемы, соответствующие выбранному полю порта.
pub fn end_nodes<'a>(info: &EndInfo<'a>) -> &'a [String] {
    let nodes: &'a [String] = &info.port.nodes;
    let start = info.offset.min(nodes.len());
    let end = (info.offset + info.length).min(nodes.len());
    &nodes[start..end]
}

/// Откуда идёт сигнал: у [`TOP`] — вход упражнения (`In`), у блока — его выход (`Out`).
pub fn is_source_end(end: &BusEnd, info: &EndInfo) -> bool {
    if end.node == TOP {
        info.port.dir == Dir::In
    } else {
        info.port.dir == Dir::Out
    }
}

/// Можно ли соединить: возвращает причину отказа.
pub fn connection_error(from: &BusEnd, to: &BusEnd, ports_of: &PortsOf) -> Option<String> {
    let (Some(a), Some(b)) = (end_info(from, ports_of), end_info(to, ports_of)) else {
        return Some("Такого порта нет".into());
    };
    if !is_source_end(from, &a) {
        return Some("Провод должен начинаться с выхода".into());
    }
    if is_source_end(to, &b) {
        return Some("Провод должен заканчиваться на входе".into());
    }
    if from.node == to.node && from.node != TOP {
        return Some("Нельзя замыкать блок на самого себя".into());
    }
    if !can_connect(a.ty, b.ty) {
        return Some(format!("Тип {} не подходит к {} — нужен переходник", a.ty.name(), b.ty.name()));
    }
    None
}

/// Добавляет шину; старые шины, занимающие те же биты входа, заменяются.
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
   Разворачивание в плоскую схему
   ============================================================ */

/// Значение узла плоской схемы по его имени.
pub type ValueScope<'a> = &'a dyn Fn(&str) -> NodeValue;

/// Вложенный блок после разворачивания.
#[derive(Debug, Clone)]
pub struct SubExpansion {
    pub def: Arc<BlockDef>,
    pub solution: Arc<Solution>,
    pub expansion: Expansion,
}

/// Развёрнутое решение: плоская схема и сведения, откуда в ней берутся сигналы блоков.
#[derive(Debug, Clone)]
pub struct Expansion {
    /// Плоская схема: вентили (у вложенных блоков — с префиксами `экземпляр__`) и провода.
    pub circuit: Circuit,
    subs: Vec<(String, SubExpansion)>,
    sub_index: HashMap<String, usize>,
    /// Кто подаёт сигнал на лист `экземпляр|узел`.
    driver: HashMap<String, (String, String)>,
    /// «Внутренние источники» каждого блока: его вентили и выходы встроенной памяти.
    is_gate_of: HashMap<String, HashSet<String>>,
    /// У решения из вентилей и памяти источники не вычисляются (всегда `None`).
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

    /// Вложенные блоки в порядке экземпляров.
    pub fn subs(&self) -> &[(String, SubExpansion)] {
        &self.subs
    }

    /// Вложенный блок по id экземпляра.
    pub fn sub(&self, id: &str) -> Option<&SubExpansion> {
        self.sub_index.get(id).map(|i| &self.subs[*i].1)
    }

    /// Узел плоской схемы, чьё значение выходит на выходной узел экземпляра блока.
    pub fn out_source(&self, inst: &str, out_node: &str) -> Option<String> {
        if !self.resolving {
            return None;
        }
        self.resolve_out(inst, out_node, &mut HashSet::new())
    }

    /// Узел плоской схемы, который подаёт сигнал на входной узел экземпляра блока.
    pub fn in_source(&self, inst: &str, in_node: &str) -> Option<String> {
        if !self.resolving {
            return None;
        }
        self.resolve_in(inst, in_node, &mut HashSet::new())
    }

    fn resolve_out(&self, inst: &str, out_node: &str, seen: &mut HashSet<String>) -> Option<String> {
        if inst == TOP {
            return Some(out_node.to_string()); // вход самого упражнения
        }
        let sub = self.sub(inst)?;
        let w = sub.expansion.circuit.wires.iter().find(|x| x.to.node == out_node)?;
        if self.is_gate_of.get(inst).is_some_and(|s| s.contains(&w.from.node)) {
            return Some(format!("{inst}__{}", w.from.node));
        }
        self.resolve_in(inst, &w.from.node, seen) // выход прямо повторяет вход
    }

    fn resolve_in(&self, inst: &str, in_node: &str, seen: &mut HashSet<String>) -> Option<String> {
        let key = format!("{inst}|{in_node}");
        if !seen.insert(key.clone()) {
            return None; // комбинационная петля из одних проводов
        }
        let (node, leaf) = self.driver.get(&key)?;
        self.resolve_out(node, leaf, seen)
    }
}

/// Все вентили и выходы памяти внутри плоской схемы.
fn internal_sources(c: &Circuit) -> HashSet<String> {
    c.gates.iter().map(|g| g.id.clone()).chain(c.natives.iter().flat_map(|n| n.dout.iter().cloned())).collect()
}

/// Разворачивает решение в плоскую схему с теми же внешними узлами (входы A–F, имена выходов).
/// Решение из вентилей возвращается как есть.
pub fn expand(solution: &Solution, iface: &BlockInterface, lookup: &dyn BlockLookup) -> Expansion {
    let sol = match solution {
        Solution::Native(n) => {
            // выходные узлы блока — выходы памяти; внутри блока одна «микросхема»
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

    // Дальше нужны методы разрешения источников: собираем «черновое» развёртывание.
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
        // узел внутри блока → узел плоской схемы (свой источник — с префиксом, вход блока — его драйвер)
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
                continue; // питание выходных узлов — это внутренность блока
            }
            let Some(from) = map(&w.from.node) else {
                continue; // вход блока ни к чему не подключён
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

/// Значения внутри экземпляра блока по значениям родительской схемы.
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

/// Значения порта (или его поля) по порядку бит.
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
