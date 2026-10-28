//! Ports and links on the design board (modeled on the "Computer architecture" lab boards): a component has an input
//! port on the left and an output port on the right. A link goes from an output to an input; validity is defined by [`crate::engine::can_link`].
//! Auto-linking: a component being moved or placed "reaches" for the nearest suitable neighbours by itself.

use crate::engine::can_link;
use crate::jsfmt;
use crate::types::{Kind, SdEdge, SdNode, SdState};

pub const NODE_W: f64 = 124.0;
pub const NODE_H: f64 = 60.0;
/// Distance (in board units) at which neighbouring ports count as "close".
pub const AUTO_RADIUS: f64 = 230.0;
/// "Stickiness" of an already shown link so that the dashed line does not jitter.
const STICK: f64 = 14.0;

/// Point on the board.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Pt {
    pub x: f64,
    pub y: f64,
}

/// Whether a component kind has an output port.
pub fn has_out(k: Kind) -> bool {
    Kind::ALL.iter().any(|&t| can_link(k, t))
}

/// Whether a component kind has an input port.
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

/// Link curve from point `a` (output) to `b` (input): the `d` attribute value of an SVG path.
pub fn wire_path(a: Pt, b: Pt) -> String {
    let dx = f64::max(36.0, (b.x - a.x).abs() / 2.0);
    let n = jsfmt::num;
    format!("M{} {} C{} {} {} {} {} {}", n(a.x), n(a.y), n(a.x + dx), n(a.y), n(b.x - dx), n(b.y), n(b.x), n(b.y))
}

/// Whether there is a path along links from `a` to `b`.
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

/// Reason why the link `a → b` cannot be placed; `None` — it can.
pub fn connect_error(state: &SdState, a: &SdNode, b: &SdNode) -> Option<String> {
    if a.id == b.id {
        return Some(i18n::tr("A component cannot be linked to itself.").into());
    }
    if !can_link(a.kind, b.kind) {
        return Some(i18n::trf!("“{0}” cannot be linked to “{1}”: this model does not work that way.", a.name, b.name));
    }
    if state.edges.iter().any(|e| e.from == a.id && e.to == b.id) {
        return Some(i18n::tr("This link already exists.").into());
    }
    if reaches(&state.edges, &b.id, &a.id) {
        return Some(i18n::tr("This would close the diagram into a cycle — requests would go in circles.").into());
    }
    None
}

fn dist(p: Pt, q: Pt) -> f64 {
    (p.x - q.x).hypot(p.y - q.y)
}

/// Which links to suggest for component `node` at its position: the input reaches for the nearest suitable
/// source on the left, and the output for the nearest suitable sinks on the right (one per component kind).
/// Existing links and cycles are skipped; `keep` — links shown last time (so the dashed line does not jitter).
pub fn suggest_edges(state: &SdState, node: &SdNode, keep: &[SdEdge], radius: f64) -> Vec<SdEdge> {
    let others: Vec<&SdNode> = state.nodes.iter().filter(|n| n.id != node.id).collect();
    let have = |from: &str, to: &str| state.edges.iter().any(|e| e.from == from && e.to == to);
    let kept = |from: &str, to: &str| keep.iter().any(|e| e.from == from && e.to == to);
    let score = |d: f64, from: &str, to: &str| d - if kept(from, to) { STICK } else { 0.0 };
    let mut planned: Vec<SdEdge> = Vec::new();
    let mut result: Vec<SdEdge> = Vec::new();
    let edges_now = |planned: &[SdEdge]| -> Vec<SdEdge> { state.edges.iter().chain(planned.iter()).cloned().collect() };

    // input ← nearest source
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

    // output → nearest sinks, one per kind
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
