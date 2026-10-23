//! Элементы кадра схемы. Каждый вид — своя структура с понятными полями; в данных элемент записывается объектом с полем
//! `"t"` (вид) и `"id"`. Одинаковый `id` в соседних кадрах — один и тот же объект на экране (он плавно переезжает,
//! меняет цвет и гаснет, когда его нет в кадре). Координаты — в системе холста 360×(высота сцены), (x, y) — центр,
//! если не сказано иное. Любой элемент: `o` — прозрачность (0…1), `s` — масштаб.

use highlight::Lang;
use serde::{Deserialize, Serialize};

use crate::tone::Tone;

fn one() -> f64 {
    1.0
}
fn is_one(v: &f64) -> bool {
    *v == 1.0
}
fn is_false(v: &bool) -> bool {
    !*v
}
fn is_zero(v: &f64) -> bool {
    *v == 0.0
}
fn is_default<T: Default + PartialEq>(v: &T) -> bool {
    *v == T::default()
}

macro_rules! defaults {
    ($($name:ident: $t:ty = $v:expr;)*) => { $(fn $name() -> $t { $v })* };
}
defaults! {
    cell_w: f64 = 30.0;
    cell_h: f64 = 26.0;
    cell_size: f64 = 11.0;
    sub_size: f64 = 8.5;
    dot_r: f64 = 12.0;
    dot_size: f64 = 10.5;
    lnode_w: f64 = 46.0;
    lnode_h: f64 = 24.0;
    text_size: f64 = 10.0;
    ptr_tone: Tone = Tone::Green;
    ptr_size: f64 = 9.5;
    line_width: f64 = 1.6;
    zone_w: f64 = 100.0;
    zone_h: f64 = 40.0;
    zone_tone: Tone = Tone::Outline;
    path_tone: Tone = Tone::Green;
    path_width: f64 = 2.0;
    bar_w: f64 = 16.0;
    bar_max: f64 = 100.0;
    code_size: f64 = 9.5;
    code_lh: f64 = 13.0;
    code_w: f64 = 150.0;
    gate_size: f64 = 8.5;
    lamp_r: f64 = 9.0;
}

macro_rules! common_setters {
    () => {
        /// Прозрачность (0…1).
        pub fn opacity(mut self, o: f64) -> Self {
            self.o = o;
            self
        }
        /// Масштаб относительно центра элемента.
        pub fn scale(mut self, s: f64) -> Self {
            self.s = s;
            self
        }
        /// Задержка перехода, мс: элементы кадра появляются по очереди.
        pub fn delay(mut self, ms: f64) -> Self {
            self.delay = ms;
            self
        }
    };
}
macro_rules! tone_setter {
    () => {
        pub fn tone(mut self, tone: Tone) -> Self {
            self.tone = tone;
            self
        }
    };
}

/// Клетка массива / подписанный прямоугольник.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Cell {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "cell_w")]
    pub w: f64,
    #[serde(default = "cell_h")]
    pub h: f64,
    /// подпись по центру; `\n` — перенос строки
    #[serde(default)]
    pub text: String,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default = "cell_size")]
    pub size: f64,
    /// подпись под клеткой
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "sub_size")]
    pub sub_size: f64,
    #[serde(default, skip_serializing_if = "is_false")]
    pub dash: bool,
    /// цвет подписи (CSS) поверх цвета оттенка
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text_color: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Cell {
    pub fn size(mut self, size: f64) -> Self {
        self.size = size;
        self
    }
    tone_setter!();
    pub fn w(mut self, w: f64) -> Self {
        self.w = w;
        self
    }
    pub fn h(mut self, h: f64) -> Self {
        self.h = h;
        self
    }
    pub fn dash(mut self) -> Self {
        self.dash = true;
        self
    }
    /// Подпись под клеткой.
    pub fn under(mut self, text: impl Into<String>) -> Self {
        self.sub = Some(text.into());
        self
    }
    pub fn text_color(mut self, css: impl Into<String>) -> Self {
        self.text_color = Some(css.into());
        self
    }
    common_setters!();
}

/// Круглый узел с подписью внутри.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Dot {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "dot_r")]
    pub r: f64,
    #[serde(default)]
    pub text: String,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default = "dot_size")]
    pub size: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub dash: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text_color: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Dot {
    pub fn r(mut self, r: f64) -> Self {
        self.r = r;
        self
    }
    tone_setter!();
    pub fn size(mut self, size: f64) -> Self {
        self.size = size;
        self
    }
    /// Подпись под кружком.
    pub fn under(mut self, text: impl Into<String>) -> Self {
        self.sub = Some(text.into());
        self
    }
    pub fn dash(mut self) -> Self {
        self.dash = true;
        self
    }
    common_setters!();
}

/// Узел связного списка: значение | ссылка; `nil` — пустая ссылка (перечёркнута).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Lnode {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "lnode_w")]
    pub w: f64,
    #[serde(default = "lnode_h")]
    pub h: f64,
    #[serde(default)]
    pub text: String,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default = "cell_size")]
    pub size: f64,
    #[serde(default, skip_serializing_if = "is_false")]
    pub nil: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Lnode {
    tone_setter!();
    pub fn nil(mut self) -> Self {
        self.nil = true;
        self
    }
    common_setters!();
}

/// Выравнивание подписи по горизонтали.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Anchor {
    Start,
    #[default]
    Middle,
    End,
}

impl Anchor {
    pub fn css(self) -> &'static str {
        match self {
            Anchor::Start => "start",
            Anchor::Middle => "middle",
            Anchor::End => "end",
        }
    }
}

/// Подпись; `\n` — перенос строки. Цвет — оттенок (`tone`) или своё значение CSS (`color`).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Text {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default)]
    pub text: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tone: Option<Tone>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub color: Option<String>,
    #[serde(default = "text_size")]
    pub size: f64,
    #[serde(default, skip_serializing_if = "is_false")]
    pub mono: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub bold: bool,
    #[serde(default, skip_serializing_if = "is_default")]
    pub anchor: Anchor,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Text {
    /// Цвет подписи в CSS: свой, иначе цвет оттенка.
    pub fn fill(&self) -> Option<String> {
        self.color.clone().or_else(|| self.tone.and_then(Tone::hue).map(String::from))
    }
    pub fn size(mut self, size: f64) -> Self {
        self.size = size;
        self
    }
    /// Цвет оттенка.
    pub fn tone(mut self, tone: Tone) -> Self {
        self.tone = Some(tone);
        self
    }
    pub fn color(mut self, css: impl Into<String>) -> Self {
        self.color = Some(css.into());
        self
    }
    pub fn mono(mut self) -> Self {
        self.mono = true;
        self
    }
    pub fn bold(mut self) -> Self {
        self.bold = true;
        self
    }
    pub fn anchor(mut self, anchor: Anchor) -> Self {
        self.anchor = anchor;
        self
    }
    common_setters!();
}

/// Направление указателя.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Dir {
    /// стрелка идёт вниз к точке (x, y), имя над ней
    #[default]
    Down,
    /// стрелка идёт вверх к точке (x, y), имя под ней
    Up,
}

/// Указатель: короткая стрелка к точке (x, y) и его имя.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Ptr {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default)]
    pub text: String,
    #[serde(default = "ptr_tone")]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "is_default")]
    pub dir: Dir,
    #[serde(default = "ptr_size")]
    pub size: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Ptr {
    tone_setter!();
    pub fn up(mut self) -> Self {
        self.dir = Dir::Up;
        self
    }
    common_setters!();
}

/// Линия или стрелка; движется плавно (CSS-переход свойства `d`).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Line {
    pub id: String,
    pub x1: f64,
    pub y1: f64,
    pub x2: f64,
    pub y2: f64,
    #[serde(default)]
    pub tone: Tone,
    /// наконечник на конце (x2, y2)
    #[serde(default, skip_serializing_if = "is_false")]
    pub arrow: bool,
    /// штриховка (`stroke-dasharray`): `"3 3"`
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dash: Option<String>,
    /// изгиб дугой: смещение середины перпендикулярно линии
    #[serde(default, skip_serializing_if = "is_zero")]
    pub bend: f64,
    #[serde(default = "line_width")]
    pub width: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Line {
    tone_setter!();
    /// Пунктир по умолчанию.
    pub fn dash(mut self) -> Self {
        self.dash = Some("3 3".into());
        self
    }
    pub fn dash_pattern(mut self, pattern: impl Into<String>) -> Self {
        self.dash = Some(pattern.into());
        self
    }
    /// Изгиб дугой: смещение середины перпендикулярно линии.
    pub fn bend(mut self, bend: f64) -> Self {
        self.bend = bend;
        self
    }
    pub fn width(mut self, w: f64) -> Self {
        self.width = w;
        self
    }
    common_setters!();
}

/// Рамка-область с подписью над левым краем.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Zone {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "zone_w")]
    pub w: f64,
    #[serde(default = "zone_h")]
    pub h: f64,
    #[serde(default = "zone_tone")]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "is_false")]
    pub dash: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub label: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Zone {
    tone_setter!();
    pub fn dash(mut self) -> Self {
        self.dash = true;
        self
    }
    pub fn label(mut self, label: impl Into<String>) -> Self {
        self.label = Some(label.into());
        self
    }
    common_setters!();
}

/// Кривая по пути SVG (`d`); `draw` 0…1 — доля «прорисованной» линии (плавно растёт между кадрами).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Path {
    pub id: String,
    pub d: String,
    #[serde(default = "path_tone")]
    pub tone: Tone,
    #[serde(default = "path_width")]
    pub width: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dash: Option<String>,
    /// заливка (CSS)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fill: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fill_opacity: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub draw: Option<f64>,
    /// наконечник стрелки на конце пути
    #[serde(default, skip_serializing_if = "is_false")]
    pub arrow: bool,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
}

impl Path {
    tone_setter!();
    pub fn arrow(mut self) -> Self {
        self.arrow = true;
        self
    }
    pub fn width(mut self, w: f64) -> Self {
        self.width = w;
        self
    }
    pub fn draw(mut self, share: f64) -> Self {
        self.draw = Some(share);
        self
    }
    pub fn fill(mut self, css: impl Into<String>) -> Self {
        self.fill = Some(css.into());
        self
    }
    pub fn opacity(mut self, o: f64) -> Self {
        self.o = o;
        self
    }
    /// Задержка перехода, мс.
    pub fn delay(mut self, ms: f64) -> Self {
        self.delay = ms;
        self
    }
}

/// Столбик: (x, y) — середина основания, `hh` — высота из `max`; растёт плавно (масштаб по вертикали).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Bar {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "bar_w")]
    pub w: f64,
    #[serde(default)]
    pub hh: f64,
    #[serde(default = "bar_max")]
    pub max: f64,
    #[serde(default)]
    pub tone: Tone,
    /// подпись под основанием
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
}

impl Bar {
    pub fn w(mut self, w: f64) -> Self {
        self.w = w;
        self
    }
    tone_setter!();
    pub fn max(mut self, max: f64) -> Self {
        self.max = max;
        self
    }
    /// Подпись под основанием.
    pub fn label(mut self, text: impl Into<String>) -> Self {
        self.text = Some(text.into());
        self
    }
    pub fn opacity(mut self, o: f64) -> Self {
        self.o = o;
        self
    }
    /// Задержка перехода, мс.
    pub fn delay(mut self, ms: f64) -> Self {
        self.delay = ms;
        self
    }
}

/// Строки кода с подсветкой; (x, y) — левый верхний угол первой строки.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Code {
    pub id: String,
    pub x: f64,
    pub y: f64,
    pub lines: Vec<String>,
    /// подсвеченные строки (номера с нуля)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub hl: Vec<usize>,
    /// ошибочные строки (красные)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub bad: Vec<usize>,
    #[serde(default)]
    pub lang: Lang,
    #[serde(default = "code_size")]
    pub size: f64,
    #[serde(default = "code_lh")]
    pub lh: f64,
    #[serde(default = "code_w")]
    pub w: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
}

impl Code {
    /// Подсвеченные строки (номера с нуля).
    pub fn hl(mut self, lines: impl IntoIterator<Item = usize>) -> Self {
        self.hl = lines.into_iter().collect();
        self
    }
    /// Ошибочные строки (красные).
    pub fn bad(mut self, lines: impl IntoIterator<Item = usize>) -> Self {
        self.bad = lines.into_iter().collect();
        self
    }
    pub fn size(mut self, size: f64) -> Self {
        self.size = size;
        self
    }
    pub fn lh(mut self, lh: f64) -> Self {
        self.lh = lh;
        self
    }
    pub fn w(mut self, w: f64) -> Self {
        self.w = w;
        self
    }
    pub fn opacity(mut self, o: f64) -> Self {
        self.o = o;
        self
    }
    /// Задержка перехода, мс.
    pub fn delay(mut self, ms: f64) -> Self {
        self.delay = ms;
        self
    }
}

/// Логический вентиль.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum GateKind {
    #[default]
    And,
    Nand,
    Or,
    Nor,
    Xor,
    Xnor,
    Not,
    Buf,
}

impl GateKind {
    /// Один вход (НЕ, повторитель).
    pub fn single_input(self) -> bool {
        matches!(self, GateKind::Not | GateKind::Buf)
    }
    /// Инверсия на выходе: кружок.
    pub fn bubble(self) -> bool {
        matches!(self, GateKind::Nand | GateKind::Nor | GateKind::Xnor | GateKind::Not)
    }
    /// «Или»-образное тело (И — прямое).
    pub fn or_shaped(self) -> bool {
        matches!(self, GateKind::Or | GateKind::Nor | GateKind::Xor | GateKind::Xnor)
    }
}

/// Вентиль; (x, y) — центр, входы слева (`a` сверху, `b` снизу), выход справа.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Gate {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default)]
    pub gate: GateKind,
    #[serde(default)]
    pub tone: Tone,
    /// подпись внутри
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text: Option<String>,
    #[serde(default = "gate_size")]
    pub size: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Gate {
    tone_setter!();
    common_setters!();
}

/// Тип канала транзистора.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Channel {
    #[default]
    N,
    P,
}

/// Транзистор (КМОП): `on` — канал открыт.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Transistor {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default)]
    pub channel: Channel,
    #[serde(default, skip_serializing_if = "is_false")]
    pub on: bool,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

/// Выключатель: `on` — замкнут.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Switch {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default, skip_serializing_if = "is_false")]
    pub on: bool,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

/// Лампочка: `on` — горит.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Lamp {
    pub id: String,
    pub x: f64,
    pub y: f64,
    #[serde(default = "lamp_r")]
    pub r: f64,
    #[serde(default, skip_serializing_if = "is_false")]
    pub on: bool,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

/// Круг-контур множества или области: рамка цветом оттенка, при `filled` — ещё и лёгкая заливка.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Circle {
    pub id: String,
    pub x: f64,
    pub y: f64,
    pub r: f64,
    #[serde(default)]
    pub tone: Tone,
    #[serde(default, skip_serializing_if = "is_false")]
    pub filled: bool,
    /// штриховка рамки (`stroke-dasharray`)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dash: Option<String>,
    #[serde(default = "path_width")]
    pub width: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub s: f64,
}

impl Circle {
    tone_setter!();
    pub fn filled(mut self) -> Self {
        self.filled = true;
        self
    }
    pub fn dash(mut self) -> Self {
        self.dash = Some("5 4".into());
        self
    }
    pub fn width(mut self, w: f64) -> Self {
        self.width = w;
        self
    }
    common_setters!();
}

/// Круг без привязки к рисунку: часть описания области ([`Region`]).
#[derive(Clone, Copy, Debug, PartialEq, Serialize, Deserialize)]
pub struct Disc {
    pub x: f64,
    pub y: f64,
    pub r: f64,
}

/// Как область получается из кругов.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RegionOp {
    /// объединение всех кругов
    #[default]
    Union,
    /// пересечение первых двух кругов
    Intersect,
    /// первый круг без остальных
    Minus,
    /// всё внутри рамки `bounds`, кроме кругов (дополнение)
    Outside,
}

/// Прямоугольник (x, y — левый верхний угол).
#[derive(Clone, Copy, Debug, PartialEq, Serialize, Deserialize)]
pub struct Rect {
    pub x: f64,
    pub y: f64,
    pub w: f64,
    pub h: f64,
}

fn region_opacity() -> f64 {
    0.42
}
fn is_region_opacity(v: &f64) -> bool {
    *v == 0.42
}

/// Залитая область диаграммы Эйлера — Венна: результат операции над кругами (∪, ∩, \, дополнение). Рисуется заливкой
/// цветом оттенка с прозрачностью `opacity`; прозрачность элемента `o` включает и гасит область.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Region {
    pub id: String,
    pub op: RegionOp,
    pub discs: Vec<Disc>,
    /// рамка для [`RegionOp::Outside`]
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub bounds: Option<Rect>,
    #[serde(default = "path_tone")]
    pub tone: Tone,
    /// непрозрачность заливки, когда область включена
    #[serde(default = "region_opacity", skip_serializing_if = "is_region_opacity")]
    pub opacity: f64,
    #[serde(default = "one", skip_serializing_if = "is_one")]
    pub o: f64,
    /// задержка перехода, мс (поочерёдное появление элементов)
    #[serde(default, skip_serializing_if = "is_zero")]
    pub delay: f64,
}

impl Region {
    tone_setter!();
    pub fn fill_opacity(mut self, v: f64) -> Self {
        self.opacity = v;
        self
    }
    pub fn shown(mut self, o: f64) -> Self {
        self.o = o;
        self
    }
    /// Задержка перехода, мс.
    pub fn delay(mut self, ms: f64) -> Self {
        self.delay = ms;
        self
    }
}

/// Элемент кадра: у каждого вида — свои поля.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Item {
    Cell(Cell),
    Dot(Dot),
    Lnode(Lnode),
    Text(Text),
    Ptr(Ptr),
    Line(Line),
    Zone(Zone),
    Path(Path),
    Bar(Bar),
    Code(Code),
    Gate(Gate),
    Transistor(Transistor),
    Switch(Switch),
    Lamp(Lamp),
    Circle(Circle),
    Region(Region),
}

macro_rules! each_item {
    ($self:expr, $i:ident => $body:expr) => {
        match $self {
            Item::Cell($i) => $body,
            Item::Dot($i) => $body,
            Item::Lnode($i) => $body,
            Item::Text($i) => $body,
            Item::Ptr($i) => $body,
            Item::Line($i) => $body,
            Item::Zone($i) => $body,
            Item::Path($i) => $body,
            Item::Bar($i) => $body,
            Item::Code($i) => $body,
            Item::Gate($i) => $body,
            Item::Transistor($i) => $body,
            Item::Switch($i) => $body,
            Item::Lamp($i) => $body,
            Item::Circle($i) => $body,
            Item::Region($i) => $body,
        }
    };
}

impl Item {
    pub fn id(&self) -> &str {
        each_item!(self, i => &i.id)
    }

    pub fn set_id(&mut self, id: String) {
        each_item!(self, i => i.id = id)
    }

    /// Вид элемента: у одного `id` он не может меняться от кадра к кадру.
    pub fn kind(&self) -> &'static str {
        match self {
            Item::Cell(_) => "cell",
            Item::Dot(_) => "dot",
            Item::Lnode(_) => "lnode",
            Item::Text(_) => "text",
            Item::Ptr(_) => "ptr",
            Item::Line(_) => "line",
            Item::Zone(_) => "zone",
            Item::Path(_) => "path",
            Item::Bar(_) => "bar",
            Item::Code(_) => "code",
            Item::Gate(_) => "gate",
            Item::Transistor(_) => "transistor",
            Item::Switch(_) => "switch",
            Item::Lamp(_) => "lamp",
            Item::Circle(_) => "circle",
            Item::Region(_) => "region",
        }
    }

    /// Прозрачность элемента.
    pub fn opacity(&self) -> f64 {
        each_item!(self, i => i.o)
    }

    /// Тот же элемент, но невидимый — так он «гаснет» на месте.
    pub fn hidden(&self) -> Item {
        let mut it = self.clone();
        each_item!(&mut it, i => i.o = 0.0);
        it
    }

    /// Все числа, которые должны быть конечными (проверка данных: координата не может быть NaN).
    pub fn numbers(&self) -> Vec<(&'static str, f64)> {
        match self {
            Item::Cell(i) => vec![("x", i.x), ("y", i.y), ("w", i.w), ("h", i.h), ("o", i.o), ("s", i.s)],
            Item::Dot(i) => vec![("x", i.x), ("y", i.y), ("r", i.r), ("o", i.o), ("s", i.s)],
            Item::Lnode(i) => vec![("x", i.x), ("y", i.y), ("w", i.w), ("h", i.h), ("o", i.o), ("s", i.s)],
            Item::Text(i) => vec![("x", i.x), ("y", i.y), ("o", i.o), ("s", i.s)],
            Item::Ptr(i) => vec![("x", i.x), ("y", i.y), ("o", i.o), ("s", i.s)],
            Item::Line(i) => vec![("x1", i.x1), ("y1", i.y1), ("x2", i.x2), ("y2", i.y2), ("o", i.o)],
            Item::Zone(i) => vec![("x", i.x), ("y", i.y), ("w", i.w), ("h", i.h), ("o", i.o), ("s", i.s)],
            Item::Path(i) => vec![("o", i.o)],
            Item::Bar(i) => vec![("x", i.x), ("y", i.y), ("w", i.w), ("hh", i.hh), ("max", i.max), ("o", i.o)],
            Item::Code(i) => vec![("x", i.x), ("y", i.y), ("o", i.o)],
            Item::Gate(i) => vec![("x", i.x), ("y", i.y), ("o", i.o), ("s", i.s)],
            Item::Transistor(i) => vec![("x", i.x), ("y", i.y), ("o", i.o), ("s", i.s)],
            Item::Switch(i) => vec![("x", i.x), ("y", i.y), ("o", i.o), ("s", i.s)],
            Item::Lamp(i) => vec![("x", i.x), ("y", i.y), ("r", i.r), ("o", i.o), ("s", i.s)],
            Item::Circle(i) => vec![("x", i.x), ("y", i.y), ("r", i.r), ("o", i.o), ("s", i.s)],
            Item::Region(i) => {
                let mut v = vec![("o", i.o), ("opacity", i.opacity)];
                for d in &i.discs {
                    v.extend([("x", d.x), ("y", d.y), ("r", d.r)]);
                }
                v
            }
        }
    }
}

macro_rules! into_item {
    ($($t:ident => $v:ident),*) => {$(impl From<$t> for Item { fn from(v: $t) -> Item { Item::$v(v) } })*};
}
into_item!(Cell => Cell, Dot => Dot, Lnode => Lnode, Text => Text, Ptr => Ptr, Line => Line, Zone => Zone, Path => Path, Bar => Bar, Code => Code, Gate => Gate, Transistor => Transistor, Switch => Switch, Lamp => Lamp, Circle => Circle, Region => Region);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn items_round_trip_and_omit_defaults() {
        let it: Item = serde_json::from_str(r#"{"t":"cell","id":"a","x":10,"y":20,"text":"7","tone":"green"}"#).unwrap();
        match &it {
            Item::Cell(c) => assert_eq!((c.w, c.h, c.size, c.o), (30.0, 26.0, 11.0, 1.0), "значения по умолчанию"),
            other => panic!("{other:?}"),
        }
        let back = serde_json::to_value(&it).unwrap();
        assert!(back.get("o").is_none() && back.get("dash").is_none(), "умолчания не пишутся: {back}");
        assert_eq!(back["t"], "cell");
        assert_eq!(serde_json::from_value::<Item>(back).unwrap(), it);
    }

    #[test]
    fn hidden_keeps_everything_but_opacity() {
        let it: Item = Cell { id: "a".into(), x: 1.0, y: 2.0, w: 30.0, h: 26.0, text: "x".into(), tone: Tone::Blue, size: 11.0, sub: None, sub_size: 8.5, dash: false, text_color: None, o: 1.0, s: 1.0, delay: 0.0 }.into();
        let h = it.hidden();
        assert_eq!(h.opacity(), 0.0);
        assert_eq!(h.id(), "a");
        assert_eq!(h.kind(), "cell");
    }
}
