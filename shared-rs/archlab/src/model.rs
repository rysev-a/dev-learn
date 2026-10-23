//! Модель логической схемы: вентили, провода, входы-тумблеры и геометрия доски.
//!
//! Порт `circuit.model.ts`. Координаты — в системе доски (viewBox 880 × 440).

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Бит: 0 или 1.
pub type Bit = u8;

/// Значение узла: 0, 1 или `None` («?» — не подключён или неизвестен).
pub type NodeValue = Option<Bit>;

/// Значения узлов схемы по имени.
pub type Values = HashMap<String, NodeValue>;

/// Тип вентиля. `Dff` — D-триггер по фронту: вход 0 — данные D, вход 1 — такт CLK, выход — Q.
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

/// Все типы вентилей в порядке палитры.
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
    /// Имя как в данных и на доске: `AND`, `NOR`, …
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

    /// Русское название (`RU_NAMES` из `gate-shapes.ts`).
    pub fn ru_name(self) -> &'static str {
        match self {
            GateType::And => "И",
            GateType::Or => "ИЛИ",
            GateType::Nor => "ИЛИ-НЕ",
            GateType::Not => "НЕ",
            GateType::Nand => "И-НЕ",
            GateType::Xor => "искл. ИЛИ",
            GateType::Xnor => "искл. ИЛИ-НЕ",
            GateType::Dff => "D-триггер по фронту",
        }
    }

    /// Входные пины: у НЕ один, у остальных два.
    pub fn pins(self) -> &'static [PinKind] {
        if self == GateType::Not {
            &[PinKind::In0]
        } else {
            &[PinKind::In0, PinKind::In1]
        }
    }
}

/// Физические входы-тумблеры доски.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum InputId {
    A,
    B,
    C,
    D,
    E,
    F,
}

/// Все входы по порядку.
pub const INPUT_IDS: [InputId; 6] = [
    InputId::A,
    InputId::B,
    InputId::C,
    InputId::D,
    InputId::E,
    InputId::F,
];

impl InputId {
    /// Имя узла: `"A"`…`"F"`.
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

    /// Разбор имени узла.
    pub fn parse(s: &str) -> Option<InputId> {
        INPUT_IDS.iter().copied().find(|i| i.as_str() == s)
    }

    /// Номер 0…5.
    pub fn index(self) -> usize {
        self as usize
    }
}

/// Состояние шести тумблеров.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct InputState(pub [Bit; 6]);

impl InputState {
    /// Все тумблеры в нуле.
    pub fn zero() -> Self {
        InputState([0; 6])
    }
    /// Уровень тумблера.
    pub fn get(&self, id: InputId) -> Bit {
        self.0[id.index()]
    }
    /// Установить уровень (любое ненулевое — единица).
    pub fn set(&mut self, id: InputId, level: Bit) {
        self.0[id.index()] = (level != 0) as Bit;
    }
    /// Число из значений тумблеров `ids`: первый — старший.
    pub fn row(&self, ids: &[InputId]) -> usize {
        ids.iter().fold(0, |acc, id| (acc << 1) | self.get(*id) as usize)
    }
}

/// Значения входов для строки таблицы истинности (`row` — биты активных входов, старший первым).
pub fn inputs_for_row(ids: &[InputId], row: usize) -> InputState {
    let mut state = InputState::zero();
    let n = ids.len();
    for (i, id) in ids.iter().enumerate() {
        state.set(*id, ((row >> (n - 1 - i)) & 1) as Bit);
    }
    state
}

/// Экземпляр вентиля на доске.
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

/// Какой пин: выход или один из входов.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum PinKind {
    Out,
    In0,
    In1,
}

/// Конец провода: узел (`A`…`F`, id вентиля или имя выхода упражнения) и пин.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PinRef {
    pub node: String,
    pub pin: PinKind,
}

impl PinRef {
    /// Выход узла.
    pub fn out(node: impl Into<String>) -> Self {
        PinRef { node: node.into(), pin: PinKind::Out }
    }
    /// Вход узла.
    pub fn inp(node: impl Into<String>, pin: PinKind) -> Self {
        PinRef { node: node.into(), pin }
    }
}

/// Провод от выхода к входу.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Wire {
    pub id: String,
    pub from: PinRef,
    pub to: PinRef,
}

/// Вид встроенной памяти.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum NativeKind {
    Rom,
    Ram,
}

/// Встроенная память — «микросхема» с адресом и данными; содержимое грузится снаружи.
/// Общий симулятор её не умеет — только быстрый ([`crate::cpu8::fast::CompiledSim`]).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NativeInstance {
    pub id: String,
    pub kind: NativeKind,
    /// Узлы-источники адреса, старший бит первым; `None` — не подключён.
    pub addr: Vec<Option<String>>,
    /// Узлы данных на запись (только ram).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub din: Option<Vec<Option<String>>>,
    /// Разрешение записи (только ram).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub we: Option<String>,
    /// Такт (только ram).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub clk: Option<String>,
    /// Имена узлов-выходов, старший бит первым.
    pub dout: Vec<String>,
}

/// Плоская схема: вентили, провода и (у процессора) встроенная память.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Circuit {
    pub gates: Vec<GateInstance>,
    pub wires: Vec<Wire>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub natives: Vec<NativeInstance>,
}

impl Circuit {
    /// Схема без памяти.
    pub fn new(gates: Vec<GateInstance>, wires: Vec<Wire>) -> Self {
        Circuit { gates, wires, natives: Vec::new() }
    }
}

/// Строка таблицы истинности после расчёта.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TableRow {
    pub targets: Vec<Bit>,
    pub actuals: Vec<NodeValue>,
    pub ok: bool,
}

/* ============================================================
   Геометрия доски
   ============================================================ */

pub const BOARD_W: f64 = 880.0;
pub const BOARD_H: f64 = 440.0;
pub const GATE_W: f64 = 64.0;
pub const GATE_H: f64 = 48.0;
/// X выходного пина входа-тумблера.
pub const INPUT_X: f64 = 100.0;
/// X входных пинов выходов (Y, Q, …).
pub const OUT_X: f64 = 780.0;
pub const GATE_MIN_X: f64 = 140.0;
pub const GATE_MAX_X: f64 = 690.0;
pub const GATE_MIN_Y: f64 = 12.0;
pub const GATE_MAX_Y: f64 = BOARD_H - GATE_H - 12.0;

const LEGACY_INPUT_Y: [f64; 3] = [80.0, 200.0, 320.0];

/// Точка на доске.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

/// Y-координаты узлов по именам в порядке добавления (порядок важен: от него зависит автопроводка).
#[derive(Debug, Clone, Default, PartialEq)]
pub struct YMap(pub Vec<(String, f64)>);

impl YMap {
    /// Y узла.
    pub fn get(&self, node: &str) -> Option<f64> {
        self.0.iter().find(|(n, _)| n == node).map(|(_, y)| *y)
    }

    /// Имена узлов по порядку.
    pub fn keys(&self) -> impl Iterator<Item = &str> {
        self.0.iter().map(|(n, _)| n.as_str())
    }

    /// Пары «имя — Y».
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

/// Y входов на левом краю: до трёх — 80/200/320, больше — равномерно по высоте.
pub fn input_ys(ids: &[InputId]) -> YMap {
    if ids.len() <= 3 {
        return YMap(ids.iter().enumerate().map(|(i, id)| (id.as_str().to_string(), LEGACY_INPUT_Y[i])).collect());
    }
    let names: Vec<&str> = ids.iter().map(|i| i.as_str()).collect();
    spread(&names, 50.0, 390.0)
}

/// Y выходов на правом краю: один — по центру, до четырёх — как раньше, больше — по всей высоте.
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

/// X выходного пина вентиля (у вентилей с инверсией правее — там пузырёк).
pub fn out_pin_x(ty: GateType) -> f64 {
    match ty {
        GateType::And | GateType::Or | GateType::Xor | GateType::Dff => GATE_W + 8.0,
        GateType::Nor | GateType::Nand | GateType::Xnor => GATE_W + 16.0,
        GateType::Not => 64.0,
    }
}

/// Координаты пина на доске. `output_y` — Y выходных узлов, `input_y` — Y входов.
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

/// Входы по умолчанию (A, B, C) для [`pin_pos`].
pub fn legacy_input_ys() -> YMap {
    YMap(["A", "B", "C"].iter().zip(LEGACY_INPUT_Y).map(|(n, y)| (n.to_string(), y)).collect())
}

/// Путь провода — кубическая кривая Безье (атрибут `d` SVG).
pub fn wire_path(a: Point, b: Point) -> String {
    let dx = 110f64.min(36f64.max((b.x - a.x).abs() / 2.0));
    format!("M {} {} C {} {}, {} {}, {} {}", a.x, a.y, a.x + dx, a.y, b.x - dx, b.y, b.x, b.y)
}

/// Создаст ли новое соединение from → to цикл: из целевого узла можно «дойти» до источника.
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

/// Выдача новых id (`g3`, `w7`, …): после загрузки сохранённой схемы новые не совпадут со старыми.
#[derive(Debug, Default, Clone)]
pub struct UidGen {
    seq: u64,
}

impl UidGen {
    /// Начать счёт с нуля.
    pub fn new() -> Self {
        Self::default()
    }

    /// Занять id вида `префикс<число>`: счёт продолжится после наибольшего числа.
    pub fn reserve<S: AsRef<str>>(&mut self, ids: &[S]) {
        for id in ids {
            let s = id.as_ref();
            let digits: String = s.chars().rev().take_while(|c| c.is_ascii_digit()).collect::<Vec<_>>().into_iter().rev().collect();
            if let Ok(n) = digits.parse::<u64>() {
                self.seq = self.seq.max(n);
            }
        }
    }

    /// Новый id с префиксом.
    pub fn next(&mut self, prefix: &str) -> String {
        self.seq += 1;
        format!("{prefix}{}", self.seq)
    }
}
