//! Симулятор схем из вентилей: комбинационный расчёт и пошаговая симуляция с обратными связями
//! (защёлки) и триггерами. Порт `evaluateCircuit` и `settleCircuit` из `circuit.model.ts` с тем же
//! порядком вычислений: результаты совпадают с TypeScript бит в бит (в том числе «?» и неустойчивость).

use crate::model::*;
use std::collections::{HashMap, HashSet};

/// Двухзначный вентиль: неизвестный вход даёт неизвестный выход (`gateValue`).
/// У триггера значения нет — он считается только в [`settle_circuit`].
pub fn gate_value(ty: GateType, a: NodeValue, b: NodeValue) -> NodeValue {
    let a = a?;
    match ty {
        GateType::And => b.map(|b| a & b),
        GateType::Nand => b.map(|b| (a & b) ^ 1),
        GateType::Or => b.map(|b| a | b),
        GateType::Nor => b.map(|b| (a | b) ^ 1),
        GateType::Xor => b.map(|b| a ^ b),
        GateType::Xnor => b.map(|b| a ^ b ^ 1),
        GateType::Not => Some(a ^ 1),
        GateType::Dff => None,
    }
}

/// Трёхзначная логика (0, 1, «?»): неопределённость не заражает выход, если ответ и так ясен —
/// И с нулём всегда 0, ИЛИ с единицей всегда 1 (`gateValueX`).
pub fn gate_value_x(ty: GateType, a: NodeValue, b: NodeValue) -> NodeValue {
    let not = |v: NodeValue| v.map(|v| v ^ 1);
    let and = || {
        if a == Some(0) || b == Some(0) {
            Some(0)
        } else if a.is_none() || b.is_none() {
            None
        } else {
            Some(1)
        }
    };
    let or = || {
        if a == Some(1) || b == Some(1) {
            Some(1)
        } else if a.is_none() || b.is_none() {
            None
        } else {
            Some(0)
        }
    };
    let xor = || match (a, b) {
        (Some(a), Some(b)) => Some(a ^ b),
        _ => None,
    };
    match ty {
        GateType::And => and(),
        GateType::Nand => not(and()),
        GateType::Or => or(),
        GateType::Nor => not(or()),
        GateType::Xor => xor(),
        GateType::Xnor => not(xor()),
        GateType::Not => not(a),
        GateType::Dff => None,
    }
}

/// Ключ скрытого состояния триггера: предыдущий уровень тактового входа (для поиска фронта).
pub fn clk_key(gate_id: &str) -> String {
    format!("{gate_id}#clk")
}

/// Откуда приходит сигнал на входной пин (последний провод побеждает, как `Map.set`).
fn source_map(circuit: &Circuit) -> HashMap<(&str, PinKind), &PinRef> {
    let mut sources = HashMap::new();
    for w in &circuit.wires {
        sources.insert((w.to.node.as_str(), w.to.pin), &w.from);
    }
    sources
}

fn put_inputs(values: &mut Values, inputs: &InputState) {
    for id in INPUT_IDS {
        values.insert(id.as_str().to_string(), Some(inputs.get(id)));
    }
}

/// Дописывает значения выходных узлов (Y, Q, nQ…): каждый — зеркало подключённого источника.
fn with_output_nodes(values: &Values, circuit: &Circuit) -> Values {
    let gate_ids: HashSet<&str> = circuit.gates.iter().map(|g| g.id.as_str()).collect();
    let mut res = values.clone();
    for w in &circuit.wires {
        let is_source = InputId::parse(&w.to.node).is_some() || gate_ids.contains(w.to.node.as_str());
        if !is_source {
            let v = res.get(&w.from.node).copied().flatten();
            res.insert(w.to.node.clone(), v);
        }
    }
    res
}

struct Calc<'a> {
    gates: HashMap<&'a str, &'a GateInstance>,
    sources: HashMap<(&'a str, PinKind), &'a PinRef>,
    values: Values,
    in_progress: HashSet<String>,
}

impl Calc<'_> {
    fn calc(&mut self, node: &str) -> NodeValue {
        if let Some(v) = self.values.get(node) {
            return *v;
        }
        if self.in_progress.contains(node) {
            return None; // защита от цикла
        }
        self.in_progress.insert(node.to_string());
        let mut v = None;
        if let Some(gate) = self.gates.get(node).copied() {
            let a = match self.sources.get(&(node, PinKind::In0)).copied() {
                Some(s) => self.calc(&s.node),
                None => None,
            };
            let mut b = None;
            if gate.ty != GateType::Not {
                b = match self.sources.get(&(node, PinKind::In1)).copied() {
                    Some(s) => self.calc(&s.node),
                    None => None,
                };
            }
            v = gate_value(gate.ty, a, b);
        }
        self.in_progress.remove(node);
        self.values.insert(node.to_string(), v);
        v
    }
}

/// Значения всех узлов схемы для заданного состояния входов. Вход вентиля без провода даёт «?»,
/// и он «протекает» до выхода. Обратные связи и триггеры здесь не поддерживаются (см. [`settle_circuit`]).
pub fn evaluate_circuit(circuit: &Circuit, inputs: &InputState) -> Values {
    let mut gates: HashMap<&str, &GateInstance> = HashMap::new();
    for g in &circuit.gates {
        gates.entry(g.id.as_str()).or_insert(g);
    }
    let mut values = Values::new();
    put_inputs(&mut values, inputs);
    let mut c = Calc { gates, sources: source_map(circuit), values, in_progress: HashSet::new() };
    for g in &circuit.gates {
        c.calc(&g.id);
    }
    with_output_nodes(&c.values, circuit)
}

/// Значение одного выхода по имени узла выхода (`Y`, `Q`…): `None`, если выход не подключён.
pub fn output_value(circuit: &Circuit, inputs: &InputState, output: &str) -> NodeValue {
    let wire = circuit.wires.iter().find(|w| w.to.node == output)?;
    evaluate_circuit(circuit, inputs).get(&wire.from.node).copied().flatten()
}

/// Результат пошаговой симуляции.
#[derive(Debug, Clone)]
pub struct SettleResult {
    pub values: Values,
    /// Схема устоялась (не генерирует).
    pub stable: bool,
}

fn get(values: &Values, key: &str) -> NodeValue {
    values.get(key).copied().flatten()
}

/// Пошаговая симуляция схемы с обратными связями (защёлки) и триггерами.
///
/// На каждом шаге все элементы пересчитываются одновременно из предыдущего состояния; если состояние
/// перестало меняться — схема устоялась. Всё неизвестное — «?» ([`gate_value_x`]). Триггер `Dff`
/// запоминает вход D в момент перехода такта 0 → 1; при включении он в нуле. Если из предыдущего
/// состояния схема не устоялась, пробуем «свежий запуск»; если и это не помогает (генерация) —
/// возвращаем неопределённые значения.
pub fn settle_circuit(circuit: &Circuit, inputs: &InputState, prev: &Values) -> SettleResult {
    let sources = source_map(circuit);
    let dffs: Vec<&GateInstance> = circuit.gates.iter().filter(|g| g.ty == GateType::Dff).collect();
    let clk_keys: Vec<String> = dffs.iter().map(|g| clk_key(&g.id)).collect();

    let compute_next = |cur: &Values| -> Values {
        let mut next = cur.clone();
        for g in &circuit.gates {
            let a = match sources.get(&(g.id.as_str(), PinKind::In0)) {
                Some(s) => get(cur, &s.node),
                None => None,
            };
            let mut b = None;
            if g.ty != GateType::Not {
                b = match sources.get(&(g.id.as_str(), PinKind::In1)) {
                    Some(s) => get(cur, &s.node),
                    None => None,
                };
            }
            if g.ty == GateType::Dff {
                let edge = get(cur, &clk_key(&g.id)) == Some(0) && b == Some(1);
                if edge {
                    next.insert(g.id.clone(), a);
                }
                next.insert(clk_key(&g.id), b);
            } else {
                next.insert(g.id.clone(), gate_value_x(g.ty, a, b));
            }
        }
        next
    };

    let state_of = |state: &Values| -> Vec<NodeValue> {
        circuit
            .gates
            .iter()
            .map(|g| get(state, &g.id))
            .chain(clk_keys.iter().map(|k| get(state, k)))
            .collect()
    };

    let attempt = |from: &Values| -> SettleResult {
        let mut cur = Values::new();
        put_inputs(&mut cur, inputs);
        for g in &circuit.gates {
            if let Some(v) = from.get(&g.id) {
                cur.insert(g.id.clone(), *v);
            } else {
                cur.insert(g.id.clone(), if g.ty == GateType::Dff { Some(0) } else { None });
            }
        }
        for k in &clk_keys {
            cur.insert(k.clone(), get(from, k));
        }
        let mut seen: HashSet<Vec<NodeValue>> = HashSet::new();
        for _ in 0..60 {
            let key = state_of(&cur);
            if !seen.insert(key.clone()) {
                return SettleResult { values: cur, stable: false }; // генерация
            }
            let next = compute_next(&cur);
            if state_of(&next) == key {
                return SettleResult { values: with_output_nodes(&next, circuit), stable: true };
            }
            cur = next;
        }
        SettleResult { values: cur, stable: false }
    };

    let r0 = attempt(prev);
    if r0.stable {
        return r0;
    }
    let r1 = attempt(&Values::new());
    if r1.stable {
        return r1;
    }
    let mut unknown = Values::new();
    put_inputs(&mut unknown, inputs);
    for g in &circuit.gates {
        unknown.insert(g.id.clone(), None);
    }
    SettleResult { values: with_output_nodes(&unknown, circuit), stable: false }
}
