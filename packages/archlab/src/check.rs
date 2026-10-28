//! Solution check: what goes to `PUT /api/exercises/14/<chapter>/<id>/solved`.
//!
//! * circuits — a truth table or a step-by-step scenario (in the interface the student walks through them, here an
//!   "ideal student" does, [`run_steps`]); the solution is JSON `{gates, wires}` or `{instances, bus_wires}`;
//! * assembler programs — text: assembled, run on the emulator and the disk is compared with the expected one.
//!
//! [`verify`] takes the submitted solution and returns a [`Verdict`]; no browser state is needed.

use crate::asm::tasks::compare;
use crate::asm::{assemble, Machine};
use crate::blocks::*;
use crate::data::ArchLab;
use crate::eval::{evaluate_circuit, output_value, settle_circuit};
use crate::exercise::*;
use crate::model::*;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// More gates than this in one solution will not be accepted (server protection).
pub const MAX_GATES: usize = 600;
/// More wires.
pub const MAX_WIRES: usize = 2000;
/// More block instances.
pub const MAX_INSTANCES: usize = 64;
/// More buses.
pub const MAX_BUS_WIRES: usize = 512;
/// Program text length.
pub const MAX_SOURCE: usize = 64 * 1024;

/// Solution check verdict.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Verdict {
    /// Solution accepted.
    pub ok: bool,
    /// Matching table rows / passed steps (for programs — 1 or 0).
    pub passed: usize,
    /// Total table rows / steps.
    pub total: usize,
    /// What to tell the student.
    pub message: String,
    /// Table: rows with target and actual values (table mode only).
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub rows: Vec<TableRow>,
    /// Scenario: output values on the checked steps (the last one is where it stopped).
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub step_outputs: Vec<Vec<NodeValue>>,
}

impl Verdict {
    fn fail(message: impl Into<String>) -> Verdict {
        Verdict { ok: false, passed: 0, total: 0, message: message.into(), rows: vec![], step_outputs: vec![] }
    }
}

/// Result of comparison with the truth table.
#[derive(Debug, Clone, PartialEq)]
pub struct TableCheck {
    pub rows: Vec<TableRow>,
    pub matched: usize,
    pub ok: bool,
}

/// Comparing the circuit with the target table (table mode): one row per input combination.
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

/// Result of walking through a scenario.
#[derive(Debug, Clone, PartialEq)]
pub struct StepsCheck {
    pub ok: bool,
    /// How many steps passed in a row.
    pub passed: usize,
    pub total: usize,
    /// Output values on each checked step.
    pub got: Vec<Vec<NodeValue>>,
}

/// Permutations of a list in lexicographic index order.
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

/// "Test bench" state: toggles and the last stable circuit state.
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

/// "Ideal student": walks through the scenario steps in order.
///
/// The circuit starts with toggles at zero. On each step the toggles are set according to the step's condition.
///
/// * With a clock (`ticks`): data changes at CLK = 0 (all at once), then pulses are applied: `pulses` (one by
///   default) if the step has CLK = 1, and none if CLK = 0. Outputs are checked at the moment of the
///   last edge (CLK = 1); after the step the clock returns to 0.
/// * Without a clock: first all changed toggles are switched at once; if the outputs are wrong, every order of
///   switching them one at a time is tried (as the student does with the mouse; up to five toggles) — the step passes if any works.
///
/// The first failed step stops the scenario.
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

/// Flat circuit of the solution: blocks are expanded, a solution of gates is taken as is (`circuitOf`).
pub fn circuit_of(spec: &CircuitSpec, solution: &Solution, lookup: &dyn BlockLookup) -> Circuit {
    match solution {
        Solution::Gate(g) => Circuit::new(g.gates.clone(), g.wires.clone()),
        other => expand(other, &spec.interface(), lookup).circuit,
    }
}

/// Check of a submitted circuit: form, allowed elements, sizes.
fn validate(spec: &CircuitSpec, solution: &Solution, lib: &BlockLibrary) -> Result<(), String> {
    match (spec.build, solution) {
        (Build::Gates, Solution::Gate(g)) => validate_gates(spec, g),
        (Build::Blocks, Solution::Block(b)) => validate_blocks(spec, b, lib),
        (Build::Gates, _) => Err(i18n::tr("Expected a gate circuit: {gates, wires}").into()),
        (Build::Blocks, _) => Err(i18n::tr("Expected a block circuit: {instances, bus_wires}").into()),
    }
}

fn validate_gates(spec: &CircuitSpec, g: &GateSolution) -> Result<(), String> {
    if g.gates.len() > MAX_GATES || g.wires.len() > MAX_WIRES {
        return Err(i18n::trf!("Circuit too large: at most {0} elements and {1} wires", MAX_GATES, MAX_WIRES));
    }
    let mut ids: HashSet<&str> = HashSet::new();
    for gate in &g.gates {
        if !spec.allowed.contains(&gate.ty) {
            return Err(i18n::trf!("Element {0} is not available in this exercise", gate.ty.name()));
        }
        if InputId::parse(&gate.id).is_some() || spec.outputs.contains(&gate.id) {
            return Err(i18n::trf!("Element name “{0}” is already used by an input or output", gate.id));
        }
        if !ids.insert(gate.id.as_str()) {
            return Err(i18n::trf!("Two elements are named “{0}”", gate.id));
        }
    }
    let active: HashSet<&str> = spec.inputs.iter().map(|i| i.as_str()).collect();
    let is_not = |id: &str| g.gates.iter().any(|x| x.id == id && x.ty == GateType::Not);
    for w in &g.wires {
        if w.from.pin != PinKind::Out {
            return Err(i18n::tr("A wire must start at an output").into());
        }
        if !active.contains(w.from.node.as_str()) && !ids.contains(w.from.node.as_str()) {
            return Err(i18n::trf!("The wire starts at “{0}”, but there is no such input or element", w.from.node));
        }
        let to_gate = ids.contains(w.to.node.as_str());
        let to_output = spec.outputs.contains(&w.to.node);
        if !(to_gate || to_output) {
            return Err(i18n::trf!("The wire goes to “{0}”, but there is no such element or output", w.to.node));
        }
        match w.to.pin {
            PinKind::Out => return Err(i18n::tr("A wire must end at an input").into()),
            PinKind::In1 if to_output || is_not(&w.to.node) => return Err(i18n::trf!("“{0}” has no second input", w.to.node)),
            _ => {}
        }
    }
    Ok(())
}

fn validate_blocks(spec: &CircuitSpec, b: &BlockSolution, lib: &BlockLibrary) -> Result<(), String> {
    if b.instances.len() > MAX_INSTANCES || b.bus_wires.len() > MAX_BUS_WIRES {
        return Err(i18n::trf!("Circuit too large: at most {0} blocks and {1} buses", MAX_INSTANCES, MAX_BUS_WIRES));
    }
    let mut ids: HashSet<&str> = HashSet::new();
    for inst in &b.instances {
        if inst.id == TOP || !ids.insert(inst.id.as_str()) {
            return Err(i18n::trf!("Invalid or duplicate block name “{0}”", inst.id));
        }
        if !spec.blocks.contains(&inst.block_id) {
            return Err(i18n::trf!("Block “{0}” is not available in this exercise", inst.block_id));
        }
        if !lib.available(&inst.block_id) {
            let hint = lib.lock_hint(&inst.block_id);
            return Err(i18n::trf!("Block “{0}” is locked. {1}", inst.block_id, hint));
        }
    }
    Ok(())
}

/// Check of a circuit submitted as a parsed solution.
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
                i18n::trf!("The circuit works — {0} of {1}! Formula: {2}", t.matched, total, spec.formula)
            } else {
                i18n::trf!("The circuit matches the goal in {0} of {1} rows", t.matched, total)
            };
            Verdict { ok: t.ok, passed: t.matched, total, message, rows: t.rows, step_outputs: vec![] }
        }
        Mode::Steps => {
            let s = run_steps(spec, &circuit);
            let message = if s.ok {
                i18n::trf!("The circuit works as required! Formula: {0}", spec.formula)
            } else if s.total == 0 {
                i18n::tr("The exercise has no check steps").to_string()
            } else {
                let text = spec.steps.get(s.passed).map_or("", |st| st.text.as_str());
                i18n::trf!("Step {0} of {1} failed: {2}", s.passed + 1, s.total, text)
            };
            Verdict { ok: s.ok, passed: s.passed, total: s.total, message, rows: vec![], step_outputs: s.got }
        }
    }
}

/// Check of an assembler program: assemble, run until halt, compare the disk.
pub fn verify_asm(spec: &AsmSpec, source: &str) -> Verdict {
    if source.len() > MAX_SOURCE {
        return Verdict::fail(i18n::tr("Program too long"));
    }
    let asm = assemble(source);
    if let Some(e) = asm.errors.first() {
        return Verdict::fail(i18n::trf!("Line {0}: {1}", e.line, e.message));
    }
    let mut m = Machine::new(&asm.words, &spec.disk.0);
    m.run(crate::asm::machine::RUN_LIMIT);
    let view = m.view();
    if let Some(err) = view.error {
        return Verdict::fail(err);
    }
    if !view.halted {
        return Verdict::fail(i18n::tr("The program did not halt"));
    }
    let r = compare(&view.mem, &spec.expected.0);
    Verdict { ok: r.ok, passed: r.ok as usize, total: 1, message: r.message, rows: vec![], step_outputs: vec![] }
}

/// Check of a submitted exercise solution.
///
/// `submitted` — circuit JSON (`{gates, wires}` or `{instances, bus_wires}`; `busWires`/`blockId` of the
/// old client are also allowed) or program text. `lib` — block library (for block circuits): the reference one
/// ([`ArchLab::reference_library`]) or one built from the student's solutions ([`ArchLab::library`] with [`crate::data::DraftStore`]).
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
    /// Check of the solution of task `task_id` in chapter `chapter`. Without `lib` the blocks are unlocked by reference solutions.
    pub fn verify(&self, chapter: u32, task_id: &str, submitted: &str, lib: Option<&BlockLibrary>) -> Verdict {
        let Some(task) = self.task(chapter, task_id) else {
            return Verdict::fail(i18n::trf!("No exercise “{0}” in chapter {1}", task_id, chapter));
        };
        match lib {
            Some(l) => verify(task, submitted, l),
            None => verify(task, submitted, &self.reference_library()),
        }
    }
}

impl ArchLab {
    /// Check taking into account what the student has unlocked: blocks are built from their solutions, and composite gates (NAND, XOR, XNOR, flip-flop)
    /// are allowed only after being built by hand — like locked elements in the interface palette.
    pub fn verify_unlocked(&self, chapter: u32, task_id: &str, submitted: &str, store: &dyn crate::data::SolutionStore) -> Verdict {
        if let Some(Spec::Circuit(c)) = self.task(chapter, task_id).map(|t| &t.spec) {
            if let (Build::Gates, Ok(Solution::Gate(g))) = (c.build, Solution::from_json(submitted)) {
                let solved = |slug: &str, id: &str| store.load(slug, id).is_some();
                if let Some(gate) = g.gates.iter().find(|x| !crate::progress::is_gate_unlocked(x.ty, &solved)) {
                    return Verdict::fail(i18n::trf!("Element {0} is locked. {1}", gate.ty.name(), self.gate_lock_hint(gate.ty)));
                }
            }
        }
        self.verify(chapter, task_id, submitted, Some(&self.library(store)))
    }
}

/// Values of all circuit nodes (convenient for the client): combinational evaluation without memory.
pub fn node_values(circuit: &Circuit, inputs: &InputState) -> Values {
    evaluate_circuit(circuit, inputs)
}
