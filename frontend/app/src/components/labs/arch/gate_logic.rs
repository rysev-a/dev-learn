//! Pure logic of the gate board: where an element lands, how pins connect, what happens to wires on
//! deletion. No interface — covered by tests.

use archlab::{
    layout::AutoWire,
    model::{creates_cycle, Circuit, GateInstance, PinKind, PinRef, Wire, GATE_H, GATE_W},
};

use super::common::BOARD;
use crate::components::labs::board_view::Point;

/// Service id of the "ghost" of an element carried from the palette: auto-wiring treats it as already on the board.
pub const DROP_ID: &str = "auto-new";

/// Top-left corner of an element whose center is at `at` (the element stays within the "world").
pub fn gate_origin(at: Point) -> Point {
    BOARD.items.clamp(Point::new(at.x - GATE_W / 2.0, at.y - GATE_H / 2.0), (GATE_W, GATE_H))
}

/// Where an element dropped on the palette goes: a column in the center of the board.
pub fn palette_drop_spot(gates_on_board: usize) -> Point {
    Point::new(400.0, 100.0 + (gates_on_board % 4) as f64 * 70.0)
}

/// Links suggested by auto-wiring, with the real element in place of the "ghost".
pub fn remap_drop(held: &[AutoWire], real_id: &str) -> Vec<AutoWire> {
    let remap = |r: &PinRef| if r.node == DROP_ID { PinRef { node: real_id.to_string(), pin: r.pin } } else { r.clone() };
    held.iter().map(|w| AutoWire { from: remap(&w.from), to: remap(&w.to), a: w.a, b: w.b }).collect()
}

/// Result of an attempt to connect two pins.
#[derive(Debug, Clone, PartialEq)]
pub enum Connect {
    /// not allowed: an output must go to another element's input
    Rejected(&'static str),
    /// a loop would close: the wire is not placed, and the previous wire on this input is removed
    Cycle(Vec<Wire>),
    /// wire placed (the previous wire on this input is replaced)
    Added(Vec<Wire>),
}

/// Connects pins `a` and `b` in either order: the output is the start, the input is the end. One input — one wire.
/// In step mode (`steps_mode`) loops are allowed: that is the point of latches.
pub fn connect(wires: &[Wire], a: &PinRef, b: &PinRef, steps_mode: bool, new_id: impl FnOnce() -> String) -> Connect {
    let (from, to) = if a.pin == PinKind::Out { (a, b) } else { (b, a) };
    if from.pin != PinKind::Out || to.pin == PinKind::Out || from.node == to.node {
        return Connect::Rejected(i18n::tr("Connect a gate's output to another gate's input"));
    }
    let rest: Vec<Wire> = wires.iter().filter(|w| w.to != *to).cloned().collect();
    if !steps_mode && creates_cycle(&Circuit::new(vec![], rest.clone()), from, to) {
        return Connect::Cycle(rest);
    }
    let mut next = rest;
    next.push(Wire { id: new_id(), from: from.clone(), to: to.clone() });
    Connect::Added(next)
}

/// Removes an element and all its wires.
pub fn remove_gate(gates: &mut Vec<GateInstance>, wires: &mut Vec<Wire>, id: &str) {
    gates.retain(|g| g.id != id);
    wires.retain(|w| w.from.node != id && w.to.node != id);
}

/// Whether a wire can be released on this pin: it needs a pin of the other kind (output ↔ input) on another node.
pub fn can_drop(pending: &PinRef, hover: &PinRef) -> bool {
    (pending.pin == PinKind::Out) != (hover.pin == PinKind::Out) && pending.node != hover.node
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::model::GateType;

    fn wire(id: &str, from: &str, to: &str, pin: PinKind) -> Wire {
        Wire { id: id.into(), from: PinRef::out(from), to: PinRef::inp(to, pin) }
    }

    #[test]
    fn new_gate_is_centered_on_the_drop_point() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(gate_origin(Point::new(400.0, 200.0)), Point::new(368.0, 176.0));
        assert_eq!(gate_origin(Point::new(100_000.0, 100_000.0)), Point::new(3936.0, 2952.0));
    }

    #[test]
    fn dropping_on_the_palette_uses_a_column() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(palette_drop_spot(0), Point::new(400.0, 100.0));
        assert_eq!(palette_drop_spot(5), Point::new(400.0, 170.0));
        assert_eq!(palette_drop_spot(4), Point::new(400.0, 100.0));
    }

    #[test]
    fn connect_takes_the_output_as_the_start_in_either_order() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let from = PinRef::out("A");
        let to = PinRef::inp("g1", PinKind::In0);
        for (a, b) in [(&from, &to), (&to, &from)] {
            match connect(&[], a, b, false, || "w1".into()) {
                Connect::Added(w) => assert_eq!((w[0].from.clone(), w[0].to.clone()), (from.clone(), to.clone())),
                other => panic!("expected a wire, got {other:?}"),
            }
        }
    }

    #[test]
    fn connect_rejects_input_to_input_and_self_loops() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let (i0, i1) = (PinRef::inp("g1", PinKind::In0), PinRef::inp("g2", PinKind::In0));
        assert!(matches!(connect(&[], &i0, &i1, false, || "w".into()), Connect::Rejected(_)));
        let (o1, o2) = (PinRef::out("g1"), PinRef::out("g2"));
        assert!(matches!(connect(&[], &o1, &o2, false, || "w".into()), Connect::Rejected(_)));
        let own = PinRef::inp("g1", PinKind::In1);
        assert!(matches!(connect(&[], &o1, &own, true, || "w".into()), Connect::Rejected(_)), "an element is not wired to itself even in latches");
    }

    #[test]
    fn one_input_takes_one_wire() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let old = [wire("w1", "A", "g1", PinKind::In0), wire("w2", "B", "g1", PinKind::In1)];
        match connect(&old, &PinRef::out("C"), &PinRef::inp("g1", PinKind::In0), false, || "w3".into()) {
            Connect::Added(w) => {
                let ids: Vec<&str> = w.iter().map(|x| x.id.as_str()).collect();
                assert_eq!(ids, ["w2", "w3"]);
            }
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn cycles_are_refused_outside_step_mode_and_allowed_inside_it() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // g1 → g2, now g2 → g1 would close a loop
        let old = [wire("w1", "g1", "g2", PinKind::In0)];
        let (from, to) = (PinRef::out("g2"), PinRef::inp("g1", PinKind::In0));
        assert!(matches!(connect(&old, &from, &to, false, || "w2".into()), Connect::Cycle(rest) if rest.len() == 1));
        assert!(matches!(connect(&old, &from, &to, true, || "w2".into()), Connect::Added(w) if w.len() == 2));
    }

    #[test]
    fn removing_a_gate_removes_its_wires() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut gates = vec![
            GateInstance { id: "g1".into(), ty: GateType::Not, x: 0.0, y: 0.0 },
            GateInstance { id: "g2".into(), ty: GateType::And, x: 0.0, y: 0.0 },
        ];
        let mut wires = vec![wire("w1", "A", "g1", PinKind::In0), wire("w2", "g1", "g2", PinKind::In0), wire("w3", "B", "g2", PinKind::In1)];
        remove_gate(&mut gates, &mut wires, "g1");
        assert_eq!(gates.len(), 1);
        assert_eq!(wires.iter().map(|w| w.id.as_str()).collect::<Vec<_>>(), ["w3"]);
    }

    #[test]
    fn auto_wires_of_the_ghost_move_to_the_real_gate() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let a = archlab::model::Point { x: 1.0, y: 2.0 };
        let held = [AutoWire { from: PinRef::out("A"), to: PinRef::inp(DROP_ID, PinKind::In0), a, b: a }, AutoWire { from: PinRef::out(DROP_ID), to: PinRef::inp("Y", PinKind::In0), a, b: a }];
        let real = remap_drop(&held, "g7");
        assert_eq!(real[0].to, PinRef::inp("g7", PinKind::In0));
        assert_eq!(real[1].from, PinRef::out("g7"));
        assert_eq!(real[0].from, PinRef::out("A"));
    }

    #[test]
    fn drop_target_must_be_the_opposite_kind_of_pin_on_another_node() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let out = PinRef::out("g1");
        assert!(can_drop(&out, &PinRef::inp("g2", PinKind::In0)));
        assert!(!can_drop(&out, &PinRef::inp("g1", PinKind::In0)));
        assert!(!can_drop(&out, &PinRef::out("g2")));
    }
}
