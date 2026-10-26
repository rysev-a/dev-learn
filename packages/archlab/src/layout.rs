//! Геометрия досок: контуры вентилей, прямоугольники блоков с портами и автопроводка.
//! Порт `gate-shapes.ts`, `block-layout.ts`, `auto-wire.ts` — чистая арифметика без интерфейса.

use crate::blocks::{BlockPort, BusEnd, Dir, TOP};
use crate::interfaces::{child_fields, slice_of};
use crate::model::*;
use std::collections::HashSet;

/* ============================================================
   Контуры вентилей
   ============================================================ */

/// Контур вентиля (атрибут `d` SVG).
pub fn gate_body_path(ty: GateType) -> &'static str {
    match ty {
        GateType::And | GateType::Nand => "M0 0 H40 A24 24 0 0 1 40 48 H0 Z",
        GateType::Or | GateType::Nor | GateType::Xor | GateType::Xnor => "M0 0 Q34 2 64 24 Q34 46 0 48 Q18 24 0 0 Z",
        GateType::Not => "M0 0 L48 24 L0 48 Z",
        GateType::Dff => "M0 0 H64 V48 H0 Z",
    }
}

/// Путь второй входной дуги XOR/XNOR или метки такта триггера, если они есть.
pub fn gate_extra_arc(ty: GateType) -> Option<&'static str> {
    match ty {
        GateType::Dff => Some("M0 27 L9 34 L0 41"),
        GateType::Xor | GateType::Xnor => Some("M-8 0 Q10 24 -8 48"),
        _ => None,
    }
}

/// `cx` пузырька инверсии, если он есть у этого типа.
pub fn gate_bubble_cx(ty: GateType) -> Option<f64> {
    match ty {
        GateType::Nor | GateType::Nand | GateType::Xnor => Some(GATE_W + 6.0),
        GateType::Not => Some(53.0),
        _ => None,
    }
}

/// Y входного пина относительно верха вентиля.
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
   Блоки на доске
   ============================================================ */

pub const BLOCK_W: f64 = 176.0;
pub const HEAD_H: f64 = 28.0;
pub const ROW_H: f64 = 24.0;
pub const PAD: f64 = 6.0;
/// Ширина боковых колонок с портами самого упражнения.
pub const SIDE_W: f64 = 132.0;

/// С какой стороны прямоугольника пин.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PinSide {
    In,
    Out,
}

/// Строка порта (или его поля).
#[derive(Debug, Clone)]
pub struct PinRow {
    /// Уникальный ключ строки: `узел|порт|поле` — им же помечается раскрытие.
    pub key: String,
    pub end: BusEnd,
    pub port: BlockPort,
    pub name: String,
    pub ty: crate::interfaces::Iface,
    /// Глубина вложенности: 0 — порт целиком, 1 — его поле и т. д.
    pub depth: usize,
    pub side: PinSide,
    /// Смещение центра строки от верха прямоугольника.
    pub y: f64,
    pub expandable: bool,
    pub expanded: bool,
    /// Узлы схемы, которые несёт эта строка (по порядку бит).
    pub nodes: Vec<String>,
}

/// Вид прямоугольника.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BoxKind {
    TopIn,
    TopOut,
    Block,
}

/// Раскладка прямоугольника с портами.
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

/// Ключ строки по концу шины.
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

/// Раскладка прямоугольника с портами: слева — входы, справа — выходы.
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
        // порты самого упражнения: вход — источник, поэтому его пин справа; выход — слева
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

/// Центр пина строки в координатах доски.
pub fn pin_center(b: &BoxLayout, row: &PinRow) -> Point {
    Point { x: if row.side == PinSide::In { b.x } else { b.x + b.w }, y: b.y + row.y }
}

/// Прямоугольники колонок с портами самого упражнения: (входы, выходы).
pub fn side_boxes(ports: &[BlockPort], expanded: &HashSet<String>, board_w: f64, y: f64) -> (BoxLayout, BoxLayout) {
    let ins: Vec<BlockPort> = ports.iter().filter(|p| p.dir == Dir::In).cloned().collect();
    let outs: Vec<BlockPort> = ports.iter().filter(|p| p.dir == Dir::Out).cloned().collect();
    (
        layout_box(TOP, "Входы", &ins, expanded, (6.0, y, SIDE_W), BoxKind::TopIn),
        layout_box(TOP, "Выходы", &outs, expanded, (board_w - SIDE_W - 6.0, y, SIDE_W), BoxKind::TopOut),
    )
}

/// Свободное место для нового блока: первая ячейка сетки, не занятая другими.
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
   Автопроводка
   ============================================================ */

/// Радиус автопроводки: множитель, границы и значение по умолчанию.
pub const AUTO_WIRE_RADIUS_FACTOR: f64 = 4.0;
pub const AUTO_WIRE_RADIUS_MIN: f64 = 16.0;
pub const AUTO_WIRE_RADIUS_MAX: f64 = 108.0;
pub const AUTO_WIRE_RADIUS_DEFAULT: f64 = 56.0;
/// На каком расстоянии (в единицах доски) контакты считаются «близкими».
pub const AUTO_WIRE_RADIUS: f64 = AUTO_WIRE_RADIUS_DEFAULT * AUTO_WIRE_RADIUS_FACTOR;
/// Насколько уже показанная связь «липнет»: более близкая пара должна выиграть хотя бы на столько.
pub const AUTO_WIRE_STICK: f64 = 6.0;

/// Предложенная связь: концы провода и их положение на доске (для пунктирного предпросмотра).
#[derive(Debug, Clone, PartialEq)]
pub struct AutoWire {
    pub from: PinRef,
    pub to: PinRef,
    pub a: Point,
    pub b: Point,
}

/// Вход автопроводки.
pub struct AutoWireInput<'a> {
    /// Элемент, который двигают или ставят (его ещё может не быть в `gates`).
    pub gate: &'a GateInstance,
    /// Остальные элементы доски.
    pub gates: &'a [GateInstance],
    pub wires: &'a [Wire],
    pub input_y: &'a YMap,
    pub output_y: &'a YMap,
    /// В пошаговом режиме циклы разрешены — это суть защёлок.
    pub steps_mode: bool,
    pub radius: Option<f64>,
    /// Связи, предложенные раньше в этом же перетаскивании: держатся, пока их не перехватит более близкая пара.
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

/// Какие провода стоит подставить для элемента на его месте: каждый свободный вход тянется к ближайшему
/// выходу (тумблер или другой элемент), а каждый выход — к ближайшему свободному входу (элемента или
/// выхода схемы). Занятые входы не трогаем.
pub fn suggest_wires(input: &AutoWireInput) -> Vec<AutoWire> {
    let gate = input.gate;
    let radius = input.radius.unwrap_or(AUTO_WIRE_RADIUS);
    let kept = |from: &PinRef, to: &PinRef| input.keep.iter().any(|k| k.from == *from && k.to == *to);
    let others: Vec<&GateInstance> = input.gates.iter().filter(|g| g.id != gate.id).collect();
    let mut all: Vec<GateInstance> = others.iter().map(|g| (*g).clone()).collect();
    all.push(gate.clone());
    let mut result: Vec<AutoWire> = Vec::new();
    // провода, которые мы уже решили добавить, тоже учитываются при поиске циклов
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

    // источники сигнала: тумблеры входов и выходы других элементов
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

    // приёмники сигнала: свободные входы других элементов и выходы схемы
    let mut sinks: Vec<PinRef> = others.iter().flat_map(|g| g.ty.pins().iter().map(|p| PinRef::inp(g.id.clone(), *p))).collect();
    sinks.extend(input.output_y.keys().map(|n| PinRef::inp(n, PinKind::In0)));
    let out = PinRef::out(gate.id.clone());
    for to in &sinks {
        if !driven(to, &planned) {
            consider(out.clone(), to.clone(), &to.node, "out", &mut cands);
        }
    }

    // как магнит: берём самые короткие связи, а у уже показанной есть небольшой «залипающий» запас, чтобы
    // пунктир не дрожал. Если два контакта тянутся к одному и тому же элементу, пунктир остаётся у ближнего,
    // а второй контакт ищет себе другого соседа
    let pull = |c: &Candidate| c.d - if c.held { AUTO_WIRE_STICK } else { 0.0 };
    cands.sort_by(|p, q| pull(p).partial_cmp(&pull(q)).unwrap_or(std::cmp::Ordering::Equal));
    let mut used_groups: HashSet<String> = HashSet::new();
    let mut used_pins: HashSet<String> = HashSet::new();
    for c in &cands {
        // у выхода — одна связь, у каждого входа — тоже одна
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
