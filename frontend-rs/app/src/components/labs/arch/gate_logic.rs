//! Чистая логика доски с вентилями: куда встанет элемент, как соединяются контакты, что происходит с проводами при
//! удалении. Без интерфейса — проверяется тестами.

use archlab::{
    layout::AutoWire,
    model::{creates_cycle, Circuit, GateInstance, PinKind, PinRef, Wire, GATE_H, GATE_W},
};

use super::view::{clamp_world, Point};

/// Служебный id «призрака» элемента, который несут из палитры: автопроводка считает его уже стоящим на доске.
pub const DROP_ID: &str = "auto-new";

/// Левый верхний угол элемента, центр которого в точке `at` (элемент остаётся в пределах «мира»).
pub fn gate_origin(at: Point) -> Point {
    clamp_world(Point::new(at.x - GATE_W / 2.0, at.y - GATE_H / 2.0), GATE_W, GATE_H)
}

/// Куда ставится элемент, брошенный на палитру: колонкой по центру доски.
pub fn palette_drop_spot(gates_on_board: usize) -> Point {
    Point::new(400.0, 100.0 + (gates_on_board % 4) as f64 * 70.0)
}

/// Предложенные автопроводкой связи, у которых вместо «призрака» теперь настоящий элемент.
pub fn remap_drop(held: &[AutoWire], real_id: &str) -> Vec<AutoWire> {
    let remap = |r: &PinRef| if r.node == DROP_ID { PinRef { node: real_id.to_string(), pin: r.pin } } else { r.clone() };
    held.iter().map(|w| AutoWire { from: remap(&w.from), to: remap(&w.to), a: w.a, b: w.b }).collect()
}

/// Итог попытки соединить два контакта.
#[derive(Debug, Clone, PartialEq)]
pub enum Connect {
    /// нельзя: выход должен идти ко входу другого элемента
    Rejected(&'static str),
    /// замкнулся бы цикл: провод не ставится, а прежний провод на этом входе снят
    Cycle(Vec<Wire>),
    /// провод поставлен (прежний провод на этом входе заменён)
    Added(Vec<Wire>),
}

/// Соединяет контакты `a` и `b` в любом порядке: выход берётся началом, вход — концом. Один вход — один провод.
/// В пошаговом режиме (`steps_mode`) циклы разрешены: это суть защёлок.
pub fn connect(wires: &[Wire], a: &PinRef, b: &PinRef, steps_mode: bool, new_id: impl FnOnce() -> String) -> Connect {
    let (from, to) = if a.pin == PinKind::Out { (a, b) } else { (b, a) };
    if from.pin != PinKind::Out || to.pin == PinKind::Out || from.node == to.node {
        return Connect::Rejected("Соединять нужно выход элемента со входом другого");
    }
    let rest: Vec<Wire> = wires.iter().filter(|w| w.to != *to).cloned().collect();
    if !steps_mode && creates_cycle(&Circuit::new(vec![], rest.clone()), from, to) {
        return Connect::Cycle(rest);
    }
    let mut next = rest;
    next.push(Wire { id: new_id(), from: from.clone(), to: to.clone() });
    Connect::Added(next)
}

/// Убирает элемент и все его провода.
pub fn remove_gate(gates: &mut Vec<GateInstance>, wires: &mut Vec<Wire>, id: &str) {
    gates.retain(|g| g.id != id);
    wires.retain(|w| w.from.node != id && w.to.node != id);
}

/// Можно ли отпустить провод на этом контакте: нужен контакт другого вида (выход ↔ вход) на другом узле.
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
        assert_eq!(gate_origin(Point::new(400.0, 200.0)), Point::new(368.0, 176.0));
        assert_eq!(gate_origin(Point::new(100_000.0, 100_000.0)), Point::new(3936.0, 2952.0));
    }

    #[test]
    fn dropping_on_the_palette_uses_a_column() {
        assert_eq!(palette_drop_spot(0), Point::new(400.0, 100.0));
        assert_eq!(palette_drop_spot(5), Point::new(400.0, 170.0));
        assert_eq!(palette_drop_spot(4), Point::new(400.0, 100.0));
    }

    #[test]
    fn connect_takes_the_output_as_the_start_in_either_order() {
        let from = PinRef::out("A");
        let to = PinRef::inp("g1", PinKind::In0);
        for (a, b) in [(&from, &to), (&to, &from)] {
            match connect(&[], a, b, false, || "w1".into()) {
                Connect::Added(w) => assert_eq!((w[0].from.clone(), w[0].to.clone()), (from.clone(), to.clone())),
                other => panic!("ожидался провод, получено {other:?}"),
            }
        }
    }

    #[test]
    fn connect_rejects_input_to_input_and_self_loops() {
        let (i0, i1) = (PinRef::inp("g1", PinKind::In0), PinRef::inp("g2", PinKind::In0));
        assert!(matches!(connect(&[], &i0, &i1, false, || "w".into()), Connect::Rejected(_)));
        let (o1, o2) = (PinRef::out("g1"), PinRef::out("g2"));
        assert!(matches!(connect(&[], &o1, &o2, false, || "w".into()), Connect::Rejected(_)));
        let own = PinRef::inp("g1", PinKind::In1);
        assert!(matches!(connect(&[], &o1, &own, true, || "w".into()), Connect::Rejected(_)), "элемент не замыкают на себя даже в защёлках");
    }

    #[test]
    fn one_input_takes_one_wire() {
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
        // g1 → g2, теперь g2 → g1 замкнёт круг
        let old = [wire("w1", "g1", "g2", PinKind::In0)];
        let (from, to) = (PinRef::out("g2"), PinRef::inp("g1", PinKind::In0));
        assert!(matches!(connect(&old, &from, &to, false, || "w2".into()), Connect::Cycle(rest) if rest.len() == 1));
        assert!(matches!(connect(&old, &from, &to, true, || "w2".into()), Connect::Added(w) if w.len() == 2));
    }

    #[test]
    fn removing_a_gate_removes_its_wires() {
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
        let a = archlab::model::Point { x: 1.0, y: 2.0 };
        let held = [AutoWire { from: PinRef::out("A"), to: PinRef::inp(DROP_ID, PinKind::In0), a, b: a }, AutoWire { from: PinRef::out(DROP_ID), to: PinRef::inp("Y", PinKind::In0), a, b: a }];
        let real = remap_drop(&held, "g7");
        assert_eq!(real[0].to, PinRef::inp("g7", PinKind::In0));
        assert_eq!(real[1].from, PinRef::out("g7"));
        assert_eq!(real[0].from, PinRef::out("A"));
    }

    #[test]
    fn drop_target_must_be_the_opposite_kind_of_pin_on_another_node() {
        let out = PinRef::out("g1");
        assert!(can_drop(&out, &PinRef::inp("g2", PinKind::In0)));
        assert!(!can_drop(&out, &PinRef::inp("g1", PinKind::In0)));
        assert!(!can_drop(&out, &PinRef::out("g2")));
    }
}
