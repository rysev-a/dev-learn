//! Проверка решения: то, что уходит на `PUT /api/exercises/14/<глава>/<id>/solved`.
//!
//! * схемы — таблица истинности или сценарий по шагам (в интерфейсе их проходит ученик, здесь —
//!   «идеальный ученик» [`run_steps`]); решение — JSON `{gates, wires}` или `{instances, bus_wires}`;
//! * программы ассемблера — текст: собирается, выполняется на эмуляторе и сверяется с ожидаемым диском.
//!
//! [`verify`] принимает присланное решение и возвращает [`Verdict`]; состояние браузера не нужно.

use crate::asm::tasks::compare;
use crate::asm::{assemble, Machine};
use crate::blocks::*;
use crate::data::ArchLab;
use crate::eval::{evaluate_circuit, output_value, settle_circuit};
use crate::exercise::*;
use crate::model::*;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// Больше вентилей в одном решении принимать не станем (защита сервера).
pub const MAX_GATES: usize = 600;
/// Больше проводов.
pub const MAX_WIRES: usize = 2000;
/// Больше экземпляров блоков.
pub const MAX_INSTANCES: usize = 64;
/// Больше шин.
pub const MAX_BUS_WIRES: usize = 512;
/// Длина текста программы.
pub const MAX_SOURCE: usize = 64 * 1024;

/// Итог проверки решения.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Verdict {
    /// Решение принято.
    pub ok: bool,
    /// Совпавших строк таблицы / пройденных шагов (у программ — 1 или 0).
    pub passed: usize,
    /// Строк таблицы / шагов всего.
    pub total: usize,
    /// Что сказать ученику.
    pub message: String,
    /// Таблица: строки с целью и фактом (только режим таблицы).
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub rows: Vec<TableRow>,
    /// Сценарий: значения выходов на проверенных шагах (последний — на котором остановились).
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub step_outputs: Vec<Vec<NodeValue>>,
}

impl Verdict {
    fn fail(message: impl Into<String>) -> Verdict {
        Verdict { ok: false, passed: 0, total: 0, message: message.into(), rows: vec![], step_outputs: vec![] }
    }
}

/// Результат сверки с таблицей истинности.
#[derive(Debug, Clone, PartialEq)]
pub struct TableCheck {
    pub rows: Vec<TableRow>,
    pub matched: usize,
    pub ok: bool,
}

/// Сверка схемы с целевой таблицей (режим таблицы): по строке на каждую комбинацию входов.
pub fn check_table(spec: &CircuitSpec, circuit: &Circuit) -> TableCheck {
    let rows: Vec<TableRow> = spec
        .target
        .iter()
        .enumerate()
        .map(|(row, targets)| {
            let inputs = inputs_for_row(&spec.inputs, row);
            let actuals: Vec<NodeValue> = spec.outputs.iter().map(|o| output_value(circuit, &inputs, o)).collect();
            let ok = actuals.iter().enumerate().all(|(i, a)| *a == targets.get(i).copied());
            TableRow { targets: targets.clone(), actuals, ok }
        })
        .collect();
    let matched = rows.iter().filter(|r| r.ok).count();
    TableCheck { ok: !rows.is_empty() && matched == rows.len(), matched, rows }
}

/// Результат прохождения сценария.
#[derive(Debug, Clone, PartialEq)]
pub struct StepsCheck {
    pub ok: bool,
    /// Сколько шагов пройдено подряд.
    pub passed: usize,
    pub total: usize,
    /// Значения выходов на каждом проверенном шаге.
    pub got: Vec<Vec<NodeValue>>,
}

/// Перестановки списка в лексикографическом порядке индексов.
fn permutations<T: Clone>(items: &[T]) -> Vec<Vec<T>> {
    if items.len() <= 1 {
        return vec![items.to_vec()];
    }
    let mut out = Vec::new();
    for i in 0..items.len() {
        let mut rest = items.to_vec();
        let x = rest.remove(i);
        for mut p in permutations(&rest) {
            p.insert(0, x.clone());
            out.push(p);
        }
    }
    out
}

/// Состояние «стенда»: тумблеры и последнее устойчивое состояние схемы.
#[derive(Clone)]
struct Bench {
    inputs: InputState,
    last: Values,
}

impl Bench {
    fn settle(&mut self, circuit: &Circuit) -> Values {
        let r = settle_circuit(circuit, &self.inputs, &self.last);
        self.last = if r.stable { r.values.clone() } else { Values::new() };
        r.values
    }
}

/// «Идеальный ученик»: проходит шаги сценария по порядку.
///
/// Схема стартует с тумблерами в нуле. На каждом шаге тумблеры выставляются по условию шага.
///
/// * С тактом (`ticks`): данные меняются при CLK = 0 (все сразу), затем подаются импульсы: `pulses` (по
///   умолчанию один), если в шаге CLK = 1, и ни одного, если CLK = 0. Выходы проверяются в момент
///   последнего фронта (CLK = 1); после шага такт возвращается в 0.
/// * Без такта: сначала все изменившиеся тумблеры переключаются сразу; если выходы не те, пробуются все порядки
///   переключения по одному (как это делает ученик мышью; до пяти тумблеров) — шаг пройден, если подошёл любой.
///
/// Первый непройденный шаг останавливает сценарий.
pub fn run_steps(spec: &CircuitSpec, circuit: &Circuit) -> StepsCheck {
    let mut bench = Bench { inputs: InputState::zero(), last: Values::new() };
    bench.settle(circuit);
    let clock = spec.clock.filter(|_| spec.ticks);
    let meets = |st: &Step, values: &Values| {
        spec.outputs.iter().all(|o| match st.expect.get(o) {
            None => true,
            Some(e) => values.get(o).copied().flatten() == Some(*e),
        })
    };
    let mut passed = 0;
    let mut got = Vec::new();
    for st in &spec.steps {
        let (ok, values);
        if let Some(c) = clock {
            for id in &spec.inputs {
                if *id != c {
                    if let Some(level) = st.inputs.get(id) {
                        bench.inputs.set(*id, *level);
                    }
                }
            }
            bench.inputs.set(c, 0);
            let mut v = bench.settle(circuit);
            let n = if st.inputs.get(&c) == Some(&1) { st.pulses.unwrap_or(1) } else { 0 };
            for p in 1..=n {
                bench.inputs.set(c, 1);
                v = bench.settle(circuit);
                if p < n {
                    bench.inputs.set(c, 0);
                    bench.settle(circuit);
                }
            }
            ok = meets(st, &v);
            values = v;
        } else {
            let start = bench.clone();
            let changed: Vec<InputId> = spec
                .inputs
                .iter()
                .copied()
                .filter(|id| st.inputs.get(id).is_some_and(|l| *l != start.inputs.get(*id)))
                .collect();
            for id in &changed {
                bench.inputs.set(*id, st.inputs[id]);
            }
            let first = bench.settle(circuit);
            let mut res = (meets(st, &first), first);
            if !res.0 && (2..=5).contains(&changed.len()) {
                for order in permutations(&changed) {
                    let mut b = start.clone();
                    let mut v = Values::new();
                    for id in &order {
                        b.inputs.set(*id, st.inputs[id]);
                        v = b.settle(circuit);
                    }
                    if meets(st, &v) {
                        bench = b;
                        res = (true, v);
                        break;
                    }
                }
            }
            (ok, values) = res;
        }
        got.push(spec.outputs.iter().map(|o| values.get(o).copied().flatten()).collect());
        if !ok {
            break;
        }
        passed += 1;
        if let Some(c) = clock {
            bench.inputs.set(c, 0);
            bench.settle(circuit);
        }
    }
    let total = spec.steps.len();
    StepsCheck { ok: total > 0 && passed == total, passed, total, got }
}

/// Плоская схема решения: блоки разворачиваются, решение из вентилей берётся как есть (`circuitOf`).
pub fn circuit_of(spec: &CircuitSpec, solution: &Solution, lookup: &dyn BlockLookup) -> Circuit {
    match solution {
        Solution::Gate(g) => Circuit::new(g.gates.clone(), g.wires.clone()),
        other => expand(other, &spec.interface(), lookup).circuit,
    }
}

/// Проверка присланной схемы: форма, допустимые элементы, размеры.
fn validate(spec: &CircuitSpec, solution: &Solution, lib: &BlockLibrary) -> Result<(), String> {
    match (spec.build, solution) {
        (Build::Gates, Solution::Gate(g)) => validate_gates(spec, g),
        (Build::Blocks, Solution::Block(b)) => validate_blocks(spec, b, lib),
        (Build::Gates, _) => Err("Ожидалась схема из вентилей: {gates, wires}".into()),
        (Build::Blocks, _) => Err("Ожидалась схема из блоков: {instances, bus_wires}".into()),
    }
}

fn validate_gates(spec: &CircuitSpec, g: &GateSolution) -> Result<(), String> {
    if g.gates.len() > MAX_GATES || g.wires.len() > MAX_WIRES {
        return Err(format!("Слишком большая схема: не больше {MAX_GATES} элементов и {MAX_WIRES} проводов"));
    }
    let mut ids: HashSet<&str> = HashSet::new();
    for gate in &g.gates {
        if !spec.allowed.contains(&gate.ty) {
            return Err(format!("Элемент {} недоступен в этом упражнении", gate.ty.name()));
        }
        if InputId::parse(&gate.id).is_some() || spec.outputs.contains(&gate.id) {
            return Err(format!("Имя элемента «{}» занято входом или выходом", gate.id));
        }
        if !ids.insert(gate.id.as_str()) {
            return Err(format!("Два элемента с именем «{}»", gate.id));
        }
    }
    let active: HashSet<&str> = spec.inputs.iter().map(|i| i.as_str()).collect();
    let is_not = |id: &str| g.gates.iter().any(|x| x.id == id && x.ty == GateType::Not);
    for w in &g.wires {
        if w.from.pin != PinKind::Out {
            return Err("Провод должен начинаться с выхода".into());
        }
        if !active.contains(w.from.node.as_str()) && !ids.contains(w.from.node.as_str()) {
            return Err(format!("Провод идёт от «{}», а такого входа или элемента нет", w.from.node));
        }
        let to_gate = ids.contains(w.to.node.as_str());
        let to_output = spec.outputs.contains(&w.to.node);
        if !(to_gate || to_output) {
            return Err(format!("Провод идёт к «{}», а такого элемента или выхода нет", w.to.node));
        }
        match w.to.pin {
            PinKind::Out => return Err("Провод должен заканчиваться на входе".into()),
            PinKind::In1 if to_output || is_not(&w.to.node) => return Err(format!("У «{}» нет второго входа", w.to.node)),
            _ => {}
        }
    }
    Ok(())
}

fn validate_blocks(spec: &CircuitSpec, b: &BlockSolution, lib: &BlockLibrary) -> Result<(), String> {
    if b.instances.len() > MAX_INSTANCES || b.bus_wires.len() > MAX_BUS_WIRES {
        return Err(format!("Слишком большая схема: не больше {MAX_INSTANCES} блоков и {MAX_BUS_WIRES} шин"));
    }
    let mut ids: HashSet<&str> = HashSet::new();
    for inst in &b.instances {
        if inst.id == TOP || !ids.insert(inst.id.as_str()) {
            return Err(format!("Неверное или повторное имя блока «{}»", inst.id));
        }
        if !spec.blocks.contains(&inst.block_id) {
            return Err(format!("Блок «{}» недоступен в этом упражнении", inst.block_id));
        }
        if !lib.available(&inst.block_id) {
            let hint = lib.lock_hint(&inst.block_id);
            return Err(format!("Блок «{}» закрыт. {hint}", inst.block_id));
        }
    }
    Ok(())
}

/// Проверка схемы, присланной как разобранное решение.
pub fn verify_circuit(spec: &CircuitSpec, solution: &Solution, lib: &BlockLibrary) -> Verdict {
    if let Err(e) = validate(spec, solution, lib) {
        return Verdict::fail(e);
    }
    let circuit = circuit_of(spec, solution, lib);
    match spec.mode {
        Mode::Table => {
            let t = check_table(spec, &circuit);
            let total = t.rows.len();
            let message = if t.ok {
                format!("Схема работает — {} из {}! Формула: {}", t.matched, total, spec.formula)
            } else {
                format!("Схема совпала с целью в {} строках из {}", t.matched, total)
            };
            Verdict { ok: t.ok, passed: t.matched, total, message, rows: t.rows, step_outputs: vec![] }
        }
        Mode::Steps => {
            let s = run_steps(spec, &circuit);
            let message = if s.ok {
                format!("Схема работает как надо! Формула: {}", spec.formula)
            } else if s.total == 0 {
                "В упражнении нет шагов проверки".to_string()
            } else {
                let text = spec.steps.get(s.passed).map_or("", |st| st.text.as_str());
                format!("Шаг {} из {} не пройден: {}", s.passed + 1, s.total, text)
            };
            Verdict { ok: s.ok, passed: s.passed, total: s.total, message, rows: vec![], step_outputs: s.got }
        }
    }
}

/// Проверка программы ассемблера: сборка, запуск до остановки, сверка диска.
pub fn verify_asm(spec: &AsmSpec, source: &str) -> Verdict {
    if source.len() > MAX_SOURCE {
        return Verdict::fail("Слишком длинная программа");
    }
    let asm = assemble(source);
    if let Some(e) = asm.errors.first() {
        return Verdict::fail(format!("Строка {}: {}", e.line, e.message));
    }
    let mut m = Machine::new(&asm.words, &spec.disk.0);
    m.run(crate::asm::machine::RUN_LIMIT);
    let view = m.view();
    if let Some(err) = view.error {
        return Verdict::fail(err);
    }
    if !view.halted {
        return Verdict::fail("Программа не остановилась");
    }
    let r = compare(&view.mem, &spec.expected.0);
    Verdict { ok: r.ok, passed: r.ok as usize, total: 1, message: r.message, rows: vec![], step_outputs: vec![] }
}

/// Проверка присланного решения упражнения.
///
/// `submitted` — JSON схемы (`{gates, wires}` или `{instances, bus_wires}`; допустимы и `busWires`/`blockId`
/// прежнего клиента) или текст программы. `lib` — библиотека блоков (для схем из блоков): эталонная
/// ([`ArchLab::reference_library`]) или собранная из решений ученика ([`ArchLab::library`] с [`crate::data::DraftStore`]).
pub fn verify(task: &Task, submitted: &str, lib: &BlockLibrary) -> Verdict {
    match &task.spec {
        Spec::Circuit(c) => match Solution::from_json(submitted) {
            Ok(sol) => verify_circuit(c, &sol, lib),
            Err(e) => Verdict::fail(e),
        },
        Spec::Asm(a) => verify_asm(a, submitted),
    }
}

impl ArchLab {
    /// Проверка решения упражнения `task_id` главы `chapter`. Без `lib` блоки открыты эталонными решениями.
    pub fn verify(&self, chapter: u32, task_id: &str, submitted: &str, lib: Option<&BlockLibrary>) -> Verdict {
        let Some(task) = self.task(chapter, task_id) else {
            return Verdict::fail(format!("Нет упражнения «{task_id}» в главе {chapter}"));
        };
        match lib {
            Some(l) => verify(task, submitted, l),
            None => verify(task, submitted, &self.reference_library()),
        }
    }
}

/// Значения всех узлов схемы (удобно клиенту): комбинационный расчёт без памяти.
pub fn node_values(circuit: &Circuit, inputs: &InputState) -> Values {
    evaluate_circuit(circuit, inputs)
}
