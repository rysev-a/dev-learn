//! Расчётная часть упражнения со схемой: схема ученика → плоская схема → значения узлов → сверка с целью.
//! Только сигналы и мемо, без DOM: тот же расчёт крутится в тестах на настоящих сценариях.

use std::sync::Arc;

use archlab::{
    blocks::{expand, BlockInterface, BlockSolution, Solution},
    check::{check_table, TableCheck},
    eval::{evaluate_circuit, settle_circuit},
    exercise::{Build, CircuitSpec, Mode},
    model::{Circuit, InputState, Values},
};
use leptos::prelude::*;

use super::{
    check::value_in,
    common::{Exp, Lib, Scope},
    solution::Drawing,
};

/// Схема ученика и всё, что из неё считается.
#[derive(Clone, Copy)]
pub struct Model {
    pub gates: RwSignal<Vec<archlab::model::GateInstance>>,
    pub wires: RwSignal<Vec<archlab::model::Wire>>,
    pub instances: RwSignal<Vec<archlab::blocks::BlockInstance>>,
    pub bus_wires: RwSignal<Vec<archlab::blocks::BusWire>>,
    pub input_state: RwSignal<InputState>,
    /// плоская схема: вентили как есть, блоки развёрнуты в вентили (при открытии новых блоков — заново)
    pub expansion: Memo<Exp>,
    pub circuit: Memo<Circuit>,
    /// значения узлов: комбинационный расчёт или (в сценарии) пошаговый с обратными связями и триггерами
    pub values: Memo<Values>,
    /// сверка с таблицей истинности (в сценарии пустая)
    pub table: Memo<TableCheck>,
    last_stable: StoredValue<Values>,
}

impl Model {
    pub fn new(spec: Arc<CircuitSpec>, iface: Arc<BlockInterface>, library: Signal<Lib>, init: Drawing) -> Self {
        let build = spec.build;
        let steps_mode = spec.mode == Mode::Steps;
        let gates = RwSignal::new(init.gates);
        let wires = RwSignal::new(init.wires);
        let instances = RwSignal::new(init.instances);
        let bus_wires = RwSignal::new(init.bus_wires);
        let input_state = RwSignal::new(InputState::zero());
        let expansion = Memo::new(move |_| {
            let solution = match build {
                Build::Blocks => Solution::Block(BlockSolution { instances: instances.get(), bus_wires: bus_wires.get() }),
                Build::Gates => Drawing { gates: gates.get(), wires: wires.get(), ..Drawing::default() }.solution(build),
            };
            let lib = library.get();
            Exp(Arc::new(expand(&solution, &iface, lib.0.as_ref())))
        });
        let circuit = Memo::new(move |_| expansion.with(|e| e.0.circuit.clone()));
        let last_stable = StoredValue::new(Values::new());
        let values = Memo::new(move |_| {
            circuit.with(|c| {
                input_state.with(|inputs| {
                    if steps_mode {
                        let r = settle_circuit(c, inputs, &last_stable.get_value());
                        last_stable.set_value(if r.stable { r.values.clone() } else { Values::new() });
                        r.values
                    } else {
                        evaluate_circuit(c, inputs)
                    }
                })
            })
        });
        let table = Memo::new(move |_| if steps_mode { TableCheck { rows: vec![], matched: 0, ok: false } } else { circuit.with(|c| check_table(&spec, c)) });
        Self { gates, wires, instances, bus_wires, input_state, expansion, circuit, values, table, last_stable }
    }

    /// Схема на доске сейчас.
    pub fn drawing(&self) -> Drawing {
        Drawing { gates: self.gates.get_untracked(), wires: self.wires.get_untracked(), instances: self.instances.get_untracked(), bus_wires: self.bus_wires.get_untracked() }
    }

    /// Выставить тумблер.
    #[cfg(test)]
    pub fn set_input(&self, id: archlab::model::InputId, level: u8) {
        self.input_state.update(|s| s.set(id, level));
    }

    /// Очистить доску и забыть устойчивое состояние защёлок.
    pub fn clear(&self) {
        self.gates.set(vec![]);
        self.wires.set(vec![]);
        self.instances.set(vec![]);
        self.bus_wires.set(vec![]);
        self.last_stable.set_value(Values::new());
    }

    /// Значения узлов для досок и проверки.
    pub fn scope(&self) -> Scope {
        let values = self.values;
        Arc::new(move |node: &str| values.with(|v| value_in(v, node)))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::components::labs::arch::{data::build_lab, solution::restore};
    use archlab::{exercise::Spec, ArchLab, DraftStore};

    fn data_dir() -> std::path::PathBuf {
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/arch")
    }

    #[test]
    fn every_table_exercise_is_solved_by_the_reference_drawing_through_the_same_reactive_chain() {
        let reference = ArchLab::load_dir(&data_dir()).expect("данные лаборатории");
        // библиотека блоков — как её собрал бы клиент из решений ученика (здесь — эталонных)
        let lab = ArchLab::from_chapters(reference.chapters().filter(|c| c.chapter <= 14).map(|c| archlab::exercise::LabChapter { tasks: c.tasks.iter().map(|t| archlab::Task { spec: strip(&t.spec), ..t.clone() }).collect(), ..c.clone() }).collect()).expect("клиентский движок");
        let mut drafts = Vec::new();
        for ch in reference.chapters().filter(|c| c.chapter <= 14) {
            for t in &ch.tasks {
                if let Spec::Circuit(c) = &t.spec {
                    if let Some(sol) = &c.solution {
                        drafts.push((ch.chapter, t.id.clone(), serde_json::to_string(sol).expect("JSON")));
                    }
                }
            }
        }
        let store = DraftStore::from_drafts(&lab, drafts.iter().map(|(c, i, d)| (*c, i.as_str(), d.as_str())));
        let owner = Owner::new();
        owner.with(|| {
            let library = Signal::stored(Lib(Arc::new(lab.library(&store))));
            let mut checked = 0;
            for ch in reference.chapters().filter(|c| c.chapter <= 14) {
                for t in &ch.tasks {
                    let Spec::Circuit(spec) = &t.spec else { continue };
                    if spec.mode != Mode::Table {
                        continue;
                    }
                    let Some(sol) = &spec.solution else { continue };
                    let json = serde_json::to_string(sol).expect("JSON");
                    let drawing = restore(&json, spec.build);
                    let model = Model::new(Arc::new(spec.clone()), Arc::new(spec.interface()), library, drawing);
                    assert!(model.table.with(|t| t.ok), "{}: схема не прошла таблицу ({} из {})", t.id, model.table.with(|t| t.matched), spec.target.len());
                    checked += 1;
                }
            }
            assert!(checked > 40, "проверено слишком мало упражнений: {checked}");
        });
    }

    /// Сценарий без эталона — каким его получает клиент.
    fn strip(spec: &Spec) -> Spec {
        let mut s = spec.clone();
        if let Spec::Circuit(c) = &mut s {
            c.solution = None;
        }
        s
    }

    /// Проходит сценарий так, как это делает ученик у доски: выставляет тумблеры, подаёт такты, смотрит на выходы.
    /// Возвращает число пройденных шагов.
    fn walk_steps(model: &Model, spec: &CircuitSpec) -> usize {
        use crate::components::labs::arch::check::step_met;
        use archlab::model::InputId;
        let met = |i: usize| model.input_state.with_untracked(|inp| model.values.with_untracked(|v| step_met(spec, i, inp, v)));
        let clock = spec.clock.filter(|_| spec.ticks);
        let mut passed = 0;
        for (i, st) in spec.steps.iter().enumerate() {
            if let Some(c) = clock {
                for id in spec.inputs.iter().filter(|id| **id != c) {
                    if let Some(l) = st.inputs.get(id) {
                        model.set_input(*id, *l);
                    }
                }
                model.set_input(c, 0);
                model.values.get_untracked();
                let n = if st.inputs.get(&c) == Some(&1) { st.pulses.unwrap_or(1) } else { 0 };
                for p in 1..=n {
                    model.set_input(c, 1);
                    model.values.get_untracked();
                    if p < n {
                        model.set_input(c, 0);
                        model.values.get_untracked();
                    }
                }
                if !met(i) {
                    return passed;
                }
                passed += 1;
                model.set_input(c, 0);
                model.values.get_untracked();
                continue;
            }
            let start = model.input_state.get_untracked();
            let changed: Vec<InputId> = spec.inputs.iter().copied().filter(|id| st.inputs.get(id).is_some_and(|l| *l != start.get(*id))).collect();
            for id in &changed {
                model.set_input(*id, st.inputs[id]);
            }
            model.values.get_untracked();
            if !met(i) {
                // по одному, в разном порядке — как пробует ученик, возвращая тумблеры на место
                let orders = permutations(&changed);
                let mut done = false;
                for order in orders {
                    for id in &changed {
                        model.set_input(*id, start.get(*id));
                        model.values.get_untracked();
                    }
                    for id in &order {
                        model.set_input(*id, st.inputs[id]);
                        model.values.get_untracked();
                    }
                    if met(i) {
                        done = true;
                        break;
                    }
                }
                if !done {
                    return passed;
                }
            }
            passed += 1;
        }
        passed
    }

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

    #[test]
    fn every_scenario_exercise_is_passed_step_by_step_on_the_reference_drawing() {
        let reference = ArchLab::load_dir(&data_dir()).expect("данные лаборатории");
        let lab = ArchLab::from_chapters(reference.chapters().filter(|c| c.chapter <= 14).map(|c| archlab::exercise::LabChapter { tasks: c.tasks.iter().map(|t| archlab::Task { spec: strip(&t.spec), ..t.clone() }).collect(), ..c.clone() }).collect()).expect("клиентский движок");
        let drafts: Vec<(u32, String, String)> = reference
            .chapters()
            .filter(|c| c.chapter <= 14)
            .flat_map(|ch| ch.tasks.iter().filter_map(move |t| match &t.spec { Spec::Circuit(c) => c.solution.as_ref().map(|s| (ch.chapter, t.id.clone(), serde_json::to_string(s).expect("JSON"))), _ => None }))
            .collect();
        let store = DraftStore::from_drafts(&lab, drafts.iter().map(|(c, i, d)| (*c, i.as_str(), d.as_str())));
        let owner = Owner::new();
        owner.with(|| {
            let library = Signal::stored(Lib(Arc::new(lab.library(&store))));
            let mut checked = 0;
            for ch in reference.chapters().filter(|c| c.chapter <= 14) {
                for t in &ch.tasks {
                    let Spec::Circuit(spec) = &t.spec else { continue };
                    if spec.mode != Mode::Steps {
                        continue;
                    }
                    let Some(sol) = &spec.solution else { continue };
                    let drawing = restore(&serde_json::to_string(sol).expect("JSON"), spec.build);
                    let model = Model::new(Arc::new(spec.clone()), Arc::new(spec.interface()), library, drawing);
                    let passed = walk_steps(&model, spec);
                    assert_eq!(passed, spec.steps.len(), "{}: пройдено шагов {passed} из {}", t.id, spec.steps.len());
                    checked += 1;
                }
            }
            assert!(checked >= 10, "проверено слишком мало сценариев: {checked}");
        });
    }

    #[test]
    fn clearing_the_board_empties_the_drawing_and_the_result() {
        let chapters = {
            // без обращения к серверу: данные из файлов в виде, который отдаёт API
            let dir = data_dir();
            let text = std::fs::read_to_string(dir.join("14-06.json")).expect("глава 6");
            let ch: api::dto::LabChapter = serde_json::from_str(&text).expect("глава как её читает клиент");
            vec![(6u32, ch)]
        };
        let lab = build_lab(chapters).expect("движок");
        let (_, spec) = lab.circuit_task("simple-circuits", "not").expect("НЕ");
        let owner = Owner::new();
        owner.with(|| {
            let library = Signal::stored(Lib(Arc::new(lab.library(&DraftStore::new()))));
            let model = Model::new(Arc::new(spec.clone()), Arc::new(spec.interface()), library, Drawing::default());
            assert!(!model.table.with(|t| t.ok), "пустая доска не решает упражнение");
            model.clear();
            assert!(model.drawing().gates.is_empty() && model.drawing().wires.is_empty());
        });
    }
}
