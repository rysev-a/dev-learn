//! Порты и связи на поле схемы (по образцу досок лаборатории «Архитектура компьютера»): у компонента слева —
//! входной порт, справа — выходной. Связь идёт от выхода к входу; допустимость задаёт [`crate::engine::can_link`].
//! Автоподстановка: компонент, который двигают или ставят, сам «тянется» к ближайшим подходящим соседям.

use crate::engine::can_link;
use crate::jsfmt;
use crate::types::{Kind, SdEdge, SdNode, SdState};

pub const NODE_W: f64 = 124.0;
pub const NODE_H: f64 = 60.0;
/// На каком расстоянии (в единицах поля) соседние порты считаются «близкими».
pub const AUTO_RADIUS: f64 = 230.0;
/// «Залипание» уже показанной связи, чтобы пунктир не дрожал.
const STICK: f64 = 14.0;

/// Точка на поле.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Pt {
    pub x: f64,
    pub y: f64,
}

/// Есть ли у вида компонента выходной порт.
pub fn has_out(k: Kind) -> bool {
    Kind::ALL.iter().any(|&t| can_link(k, t))
}

/// Есть ли у вида компонента входной порт.
pub fn has_in(k: Kind) -> bool {
    Kind::ALL.iter().any(|&t| can_link(t, k))
}

pub fn out_pos(n: Pt) -> Pt {
    Pt { x: n.x + NODE_W / 2.0, y: n.y }
}

pub fn in_pos(n: Pt) -> Pt {
    Pt { x: n.x - NODE_W / 2.0, y: n.y }
}

impl SdNode {
    pub fn pt(&self) -> Pt {
        Pt { x: self.x, y: self.y }
    }
}

/// Кривая связи от точки `a` (выход) к `b` (вход): значение атрибута `d` у SVG-пути.
pub fn wire_path(a: Pt, b: Pt) -> String {
    let dx = f64::max(36.0, (b.x - a.x).abs() / 2.0);
    let n = jsfmt::num;
    format!("M{} {} C{} {} {} {} {} {}", n(a.x), n(a.y), n(a.x + dx), n(a.y), n(b.x - dx), n(b.y), n(b.x), n(b.y))
}

/// Есть ли путь по связям из `a` в `b`.
pub fn reaches(edges: &[SdEdge], a: &str, b: &str) -> bool {
    let mut seen: Vec<&str> = Vec::new();
    let mut stack: Vec<&str> = vec![a];
    while let Some(cur) = stack.pop() {
        if cur == b {
            return true;
        }
        if seen.contains(&cur) {
            continue;
        }
        seen.push(cur);
        for e in edges {
            if e.from == cur {
                stack.push(&e.to);
            }
        }
    }
    false
}

/// Причина, по которой связь `a → b` поставить нельзя; `None` — можно.
pub fn connect_error(state: &SdState, a: &SdNode, b: &SdNode) -> Option<String> {
    if a.id == b.id {
        return Some("Компонент нельзя соединить с самим собой.".into());
    }
    if !can_link(a.kind, b.kind) {
        return Some(format!("«{}» не соединяется с «{}»: так в этой модели не устроено.", a.name, b.name));
    }
    if state.edges.iter().any(|e| e.from == a.id && e.to == b.id) {
        return Some("Такая связь уже есть.".into());
    }
    if reaches(&state.edges, &b.id, &a.id) {
        return Some("Так схема замкнётся в цикл — запросы будут ходить по кругу.".into());
    }
    None
}

fn dist(p: Pt, q: Pt) -> f64 {
    (p.x - q.x).hypot(p.y - q.y)
}

/// Какие связи стоит подставить для компонента `node` на его месте: вход тянется к ближайшему подходящему
/// источнику слева, а выход — к ближайшему подходящему приёмнику справа (по одному на вид компонента).
/// Уже существующие связи и циклы пропускаются; `keep` — связи, показанные в прошлый раз (чтобы пунктир не дрожал).
pub fn suggest_edges(state: &SdState, node: &SdNode, keep: &[SdEdge], radius: f64) -> Vec<SdEdge> {
    let others: Vec<&SdNode> = state.nodes.iter().filter(|n| n.id != node.id).collect();
    let have = |from: &str, to: &str| state.edges.iter().any(|e| e.from == from && e.to == to);
    let kept = |from: &str, to: &str| keep.iter().any(|e| e.from == from && e.to == to);
    let score = |d: f64, from: &str, to: &str| d - if kept(from, to) { STICK } else { 0.0 };
    let mut planned: Vec<SdEdge> = Vec::new();
    let mut result: Vec<SdEdge> = Vec::new();
    let edges_now = |planned: &[SdEdge]| -> Vec<SdEdge> { state.edges.iter().chain(planned.iter()).cloned().collect() };

    // вход ← ближайший источник
    if has_in(node.kind) {
        let mut best: Option<(&SdNode, f64)> = None;
        for &s in &others {
            if !can_link(s.kind, node.kind) || have(&s.id, &node.id) {
                continue;
            }
            if s.x > node.x + NODE_W / 2.0 {
                continue;
            }
            let d = dist(out_pos(s.pt()), in_pos(node.pt()));
            if d > radius && !kept(&s.id, &node.id) {
                continue;
            }
            let sc = score(d, &s.id, &node.id);
            if best.is_none_or(|(_, b)| sc < b) {
                best = Some((s, sc));
            }
        }
        if let Some((b, _)) = best {
            if !reaches(&edges_now(&planned), &node.id, &b.id) {
                let e = SdEdge { from: b.id.clone(), to: node.id.clone() };
                planned.push(e.clone());
                result.push(e);
            }
        }
    }

    // выход → ближайшие приёмники по одному на вид
    if has_out(node.kind) {
        let mut by_kind: Vec<(Kind, &SdNode, f64)> = Vec::new();
        for &t in &others {
            if !can_link(node.kind, t.kind) || have(&node.id, &t.id) {
                continue;
            }
            if t.x < node.x - NODE_W / 2.0 {
                continue;
            }
            let d = dist(out_pos(node.pt()), in_pos(t.pt()));
            if d > radius && !kept(&node.id, &t.id) {
                continue;
            }
            let sc = score(d, &node.id, &t.id);
            match by_kind.iter_mut().find(|(k, _, _)| *k == t.kind) {
                Some(cur) => {
                    if sc < cur.2 {
                        *cur = (t.kind, t, sc);
                    }
                }
                None => by_kind.push((t.kind, t, sc)),
            }
        }
        for (_, n, _) in by_kind {
            if reaches(&edges_now(&planned), &n.id, &node.id) {
                continue;
            }
            let e = SdEdge { from: node.id.clone(), to: n.id.clone() };
            planned.push(e.clone());
            result.push(e);
        }
    }
    result
}
