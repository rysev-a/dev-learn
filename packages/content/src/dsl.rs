//! Short element constructors for scene authors: `cell("a", 90.0, 44.0, "text").tone(B).size(9.0)`.
//! In all constructors (x, y) is the element center; color and sizes are set by a chain of methods.

use highlight::Lang;

use crate::{
    item::{Anchor, Bar, Cell, Circle, Code, Dir, Disc, Dot, Line, Lnode, Path, Ptr, Rect, Region, RegionOp, Text, Zone},
    tone::Tone,
};

/// A 30×26 cell with a monospace label.
pub fn cell(id: impl Into<String>, x: f64, y: f64, text: impl Into<String>) -> Cell {
    Cell { id: id.into(), x, y, w: 30.0, h: 26.0, text: text.into(), tone: Tone::Muted, size: 11.0, sub: None, sub_size: 8.5, dash: false, text_color: None, o: 1.0, delay: 0.0, s: 1.0 }
}

/// A rectangle of the given size with a centered label (font 9.5).
pub fn bx(id: impl Into<String>, x: f64, y: f64, w: f64, h: f64, text: impl Into<String>) -> Cell {
    cell(id, x, y, text).w(w).h(h).size(9.5)
}

/// A cell with a name and a value on two lines (like a variable in memory).
pub fn slot(id: impl Into<String>, x: f64, y: f64, name: &str, value: &str) -> Cell {
    bx(id, x, y, 54.0, 32.0, format!("{name}\n{value}")).size(9.0)
}

pub fn text(id: impl Into<String>, x: f64, y: f64, text: impl Into<String>) -> Text {
    Text { id: id.into(), x, y, text: text.into(), tone: None, color: None, size: 10.0, mono: false, bold: false, anchor: Anchor::Middle, o: 1.0, delay: 0.0, s: 1.0 }
}

pub fn line(id: impl Into<String>, x1: f64, y1: f64, x2: f64, y2: f64) -> Line {
    Line { id: id.into(), x1, y1, x2, y2, tone: Tone::Muted, arrow: false, dash: None, bend: 0.0, width: 1.6, o: 1.0, delay: 0.0, s: 1.0 }
}

/// An arrow with a head at the end.
pub fn arrow(id: impl Into<String>, x1: f64, y1: f64, x2: f64, y2: f64) -> Line {
    Line { arrow: true, ..line(id, x1, y1, x2, y2) }
}

/// A code callout in language `lang`; (x, y) is the top-left corner.
pub fn code(lang: Lang, id: impl Into<String>, x: f64, y: f64, lines: &[&str]) -> Code {
    Code { id: id.into(), x, y, lines: lines.iter().map(|l| (*l).to_string()).collect(), hl: Vec::new(), bad: Vec::new(), lang, size: 9.5, lh: 13.0, w: 200.0, o: 1.0, delay: 0.0 }
}

pub fn py(id: impl Into<String>, x: f64, y: f64, lines: &[&str]) -> Code {
    code(Lang::Python, id, x, y, lines)
}

pub fn c_code(id: impl Into<String>, x: f64, y: f64, lines: &[&str]) -> Code {
    code(Lang::C, id, x, y, lines)
}

pub fn asm(id: impl Into<String>, x: f64, y: f64, lines: &[&str]) -> Code {
    code(Lang::Asm, id, x, y, lines)
}

/// An outlined area.
pub fn zone(id: impl Into<String>, x: f64, y: f64, w: f64, h: f64) -> Zone {
    Zone { id: id.into(), x, y, w, h, tone: Tone::Outline, dash: false, label: None, o: 1.0, delay: 0.0, s: 1.0 }
}

/// A bar of height `hh` (out of 100); (x, y) is the middle of the base.
pub fn bar(id: impl Into<String>, x: f64, y: f64, hh: f64) -> Bar {
    Bar { id: id.into(), x, y, w: 16.0, hh, max: 100.0, tone: Tone::Muted, text: None, o: 1.0, delay: 0.0 }
}

pub fn dot(id: impl Into<String>, x: f64, y: f64, text: impl Into<String>) -> Dot {
    Dot { id: id.into(), x, y, r: 12.0, text: text.into(), tone: Tone::Muted, size: 10.5, sub: None, dash: false, text_color: None, o: 1.0, delay: 0.0, s: 1.0 }
}

/// A linked-list node: value | link.
pub fn lnode(id: impl Into<String>, x: f64, y: f64, text: impl Into<String>) -> Lnode {
    Lnode { id: id.into(), x, y, w: 46.0, h: 24.0, text: text.into(), tone: Tone::Muted, size: 11.0, nil: false, sub: None, o: 1.0, delay: 0.0, s: 1.0 }
}

/// A pointer pointing down at (x, y) with a name.
pub fn ptr(id: impl Into<String>, x: f64, y: f64, text: impl Into<String>) -> Ptr {
    Ptr { id: id.into(), x, y, text: text.into(), tone: Tone::Green, dir: Dir::Down, size: 9.5, o: 1.0, delay: 0.0, s: 1.0 }
}

/// A curve along an SVG path.
pub fn path(id: impl Into<String>, d: impl Into<String>) -> Path {
    Path { id: id.into(), d: d.into(), tone: Tone::Green, width: 2.0, dash: None, fill: None, fill_opacity: None, draw: None, arrow: false, o: 1.0, delay: 0.0 }
}

/// An outlined circle (a set): green stroke, no fill.
pub fn circle(id: impl Into<String>, x: f64, y: f64, r: f64) -> Circle {
    Circle { id: id.into(), x, y, r, tone: Tone::Green, filled: false, dash: None, width: 2.0, o: 1.0, delay: 0.0, s: 1.0 }
}

pub fn disc(x: f64, y: f64, r: f64) -> Disc {
    Disc { x, y, r }
}

fn region(id: impl Into<String>, op: RegionOp, discs: Vec<Disc>, bounds: Option<Rect>) -> Region {
    Region { id: id.into(), op, discs, bounds, tone: Tone::Green, opacity: 0.42, o: 1.0, delay: 0.0 }
}

/// Region "A ∪ B": the union of circles.
pub fn union(id: impl Into<String>, discs: &[Disc]) -> Region {
    region(id, RegionOp::Union, discs.to_vec(), None)
}

/// Region "A ∩ B": the intersection of two circles.
pub fn intersect(id: impl Into<String>, a: Disc, b: Disc) -> Region {
    region(id, RegionOp::Intersect, vec![a, b], None)
}

/// Region "A \ B": the first circle minus the rest.
pub fn minus(id: impl Into<String>, a: Disc, rest: &[Disc]) -> Region {
    let mut discs = vec![a];
    discs.extend_from_slice(rest);
    region(id, RegionOp::Minus, discs, None)
}

/// Complement: everything inside the `bounds` rectangle except the circles.
pub fn outside(id: impl Into<String>, bounds: Rect, discs: &[Disc]) -> Region {
    region(id, RegionOp::Outside, discs.to_vec(), Some(bounds))
}

pub fn rect(x: f64, y: f64, w: f64, h: f64) -> Rect {
    Rect { x, y, w, h }
}
