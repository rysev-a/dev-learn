//! Одно упражнение со схемой: доска из вентилей или блоков, таблица истинности или сценарий по шагам, такт и временная
//! диаграмма (`CircuitLab.tsx`). Состояние — сигналы, расчёт — в крейте `archlab`, тот же код проверяет решение на сервере.
//!
//! Схема ученика сохраняется черновиком: пока упражнение не решено — любая; решённое упражнение черновик не затирает
//! неверной схемой (из решённых упражнений собираются блоки других упражнений).

use std::{collections::BTreeMap, sync::Arc};

use archlab::{
    blocks::{BlockInstance, BlockSolution, Dir, Solution},
    check::run_steps,
    exercise::{Build, CircuitSpec, Mode},
    layout::free_spot,
    model::{GateType, InputId, InputState, NodeValue, UidGen, Values},
    progress::{is_composite, is_gate_unlocked},
    registry,
    wave::{build_wave, Sample, HISTORY_MAX},
};
use gloo_timers::callback::Timeout;
use leptos::prelude::*;

use super::{
    block_board::BlockBoard,
    block_logic::BLOCKS_BOARD_W,
    check::{step_met, value_in, CheckPanel, WaveDiagram},
    clock::{rate_label, Clock, CLOCK_RATES},
    common::{Level, Lib, ResultAlert, Scope},
    data::ArchData,
    gate_board::{GateBoard, PaletteItem},
    inspector::Inspector,
    model::Model,
    solution::{next_instance_id, restore},
};
use crate::components::labs::LabProps;

/// Сколько миллисекунд висит всплывающее сообщение под доской.
const FLASH_MS: u32 = 2800;

/// Подсказка над доской.
pub fn board_hint(blocks_mode: bool, steps_mode: bool) -> String {
    let what = if blocks_mode { "Соедините блоки шинами" } else { "Соберите схему" };
    if steps_mode {
        let how = if blocks_mode { "на вход подаётся такт" } else { "сигналы меняются тумблерами" };
        format!("{what} и выполняйте шаги сценария — {how}")
    } else {
        format!("{what} так, чтобы столбцы «Схема» совпали со столбцами «Цель»")
    }
}

/// Заголовок плашки об успехе (без формулы).
pub fn solved_title(steps_mode: bool, matched: usize, total: usize) -> String {
    if steps_mode {
        "Схема работает как надо!".to_string()
    } else {
        format!("Схема работает — {matched} из {total}!")
    }
}

/// Снимок сигналов после очередного изменения — один столбец временной диаграммы.
pub fn sample_of(spec: &CircuitSpec, inputs: &InputState, values: &Values) -> Sample {
    Sample {
        inputs: spec.inputs.iter().map(|id| (*id, inputs.get(*id))).collect::<BTreeMap<_, _>>(),
        outputs: spec.outputs.iter().map(|o| (o.clone(), value_in(values, o))).collect::<BTreeMap<String, NodeValue>>(),
    }
}

/// Добавляет столбец к истории (хранятся последние `HISTORY_MAX`) или заменяет последний, если тумблеры не менялись.
pub fn record_sample(history: &mut Vec<Sample>, sample: Sample, inputs_changed: bool) {
    if inputs_changed {
        history.push(sample);
        if history.len() > HISTORY_MAX {
            history.remove(0);
        }
    } else if let Some(last) = history.last_mut() {
        *last = sample;
    }
}

/// Блок в палитре: название, открыт ли, подсказка о том, что собрать, и краткая сводка портов.
#[derive(Clone, Debug, PartialEq)]
struct BlockItem {
    id: String,
    title: String,
    available: bool,
    hint: String,
    summary: String,
}

/// Упражнение со схемой из вентилей или блоков.
#[component]
pub fn CircuitLab(props: LabProps, spec: Arc<CircuitSpec>, data: ArchData) -> impl IntoView {
    let LabProps { task, draft, on_draft, solved: props_solved, report, on_next, has_next } = props;
    let build = spec.build;
    let blocks_mode = build == Build::Blocks;
    let steps_mode = spec.mode == Mode::Steps;
    let chapter = registry::chapter_of_slug(&spec.section).unwrap_or(0);
    let slug = StoredValue::new(spec.section.clone());
    let task_id = StoredValue::new(task.id.clone());
    let task_title = task.title.clone();

    // схема: сохранённое решение или пустая доска
    let init = restore(&draft.get_untracked(), build);
    let uid = StoredValue::new({
        let mut u = UidGen::new();
        init.reserve_ids(&mut u);
        u
    });
    let iface = Arc::new(spec.interface());
    let library: Signal<Lib> = data.library.into();
    let model = Model::new(spec.clone(), iface.clone(), library, init);
    let Model { gates, wires, instances, bus_wires, input_state, expansion, circuit, values, table, .. } = model;
    let passed = RwSignal::new(0usize);
    let history = RwSignal::new(Vec::<Sample>::new());
    let hint_open = RwSignal::new(false);
    let inspect_path = RwSignal::new(Vec::<String>::new());
    let flash = RwSignal::new(None::<String>);
    let flash_timer: StoredValue<Option<Timeout>, LocalStorage> = StoredValue::new_local(None);
    let clock = Clock::new(spec.clock, input_state);

    on_cleanup(move || {
        flash_timer.try_set_value(None);
    });
    let notify = Callback::new(move |text: String| {
        flash.set(Some(text));
        flash_timer.set_value(Some(Timeout::new(FLASH_MS, move || {
            flash.try_set(None);
        })));
    });

    // --- расчёт: значения узлов и сверка с целью — в `Model` ---------------------------------------
    let scope: Scope = model.scope();
    let total_steps = spec.steps.len();
    let solved_now = Memo::new(move |_| if steps_mode { total_steps > 0 && passed.get() == total_steps } else { table.with(|t| t.ok) });

    // сценарий: если стоят нужные тумблеры и выходы верны — шаг пройден, проверяется следующий
    {
        let spec = spec.clone();
        Effect::new(move |_| {
            if !steps_mode {
                return;
            }
            let p = passed.get();
            if input_state.with(|i| values.with(|v| step_met(&spec, p, i, v))) {
                passed.set(p + 1);
            }
        });
    }

    // временная диаграмма: новый столбец — после каждого изменения тумблеров, иначе последний обновляется
    {
        let spec = spec.clone();
        let last_inputs = StoredValue::new(None::<InputState>);
        Effect::new(move |_| {
            if !steps_mode {
                return;
            }
            let inputs = input_state.get();
            let sample = values.with(|v| sample_of(&spec, &inputs, v));
            let changed = last_inputs.get_value() != Some(inputs);
            last_inputs.set_value(Some(inputs));
            history.update(|h| record_sample(h, sample, changed));
        });
    }
    let wave = {
        let spec = spec.clone();
        Memo::new(move |_| history.with(|h| build_wave(h, &spec)))
    };

    // --- сохранение и отчёт о решении -----------------------------------------------------------
    // верна ли схема сейчас: так её проверит сервер (для сценария — «идеальным учеником»)
    let valid_now = {
        let spec = spec.clone();
        move || if steps_mode { circuit.with_untracked(|c| run_steps(&spec, c).ok) } else { table.with_untracked(|t| t.ok) }
    };
    let reported = StoredValue::new(props_solved.get_untracked());
    let persist = {
        Callback::new(move |()| {
            let json = model.drawing().json(build);
            let solved_before = props_solved.get_untracked();
            // верность считаем, только когда она что-то решает (дорого для сценариев)
            let ok = (solved_before || reported.get_value()) && valid_now();
            if solved_before && !ok {
                return; // решённое не затираем: из него собираются блоки других упражнений
            }
            if ok && reported.get_value() {
                data.mark_solved(chapter, &slug.get_value(), &task_id.get_value(), &json);
            }
            on_draft.run(json);
        })
    };
    Effect::new(move |_| {
        if !solved_now.get() {
            // схему сломали, а сервер её ещё не принимал (или отказал) — следующее решение уйдёт заново
            if !props_solved.get_untracked() {
                reported.set_value(false);
            }
            return;
        }
        if reported.get_value() {
            return;
        }
        reported.set_value(true);
        let json = model.drawing().json(build);
        data.mark_solved(chapter, &slug.get_value(), &task_id.get_value(), &json);
        on_draft.run(json.clone());
        report.run(json);
    });

    // --- действия -------------------------------------------------------------------------------
    let reset = move |_| {
        clock.stop();
        model.clear();
        inspect_path.set(vec![]);
        passed.set(0);
        reported.set_value(false);
        persist.run(());
    };
    let toggle_input = Callback::new(move |id: InputId| clock.toggle(id));
    let spec_inputs = spec.inputs.clone();
    let toggle_node = Callback::new(move |node: String| {
        if let Some(id) = InputId::parse(&node).filter(|id| spec_inputs.contains(id)) {
            clock.toggle(id);
        }
    });

    // --- палитры --------------------------------------------------------------------------------
    let palette = {
        let spec = spec.clone();
        Memo::new(move |_| {
            spec.allowed
                .iter()
                .map(|ty| {
                    let locked = !is_gate_unlocked(*ty, &|slug, id| data.is_solved(slug, id));
                    let title = if locked {
                        data.lab().gate_lock_hint(*ty)
                    } else {
                        format!("{} — {}{}", ty.name(), ty.ru_name(), if is_composite(*ty) { " (составной)" } else { "" })
                    };
                    PaletteItem { ty: *ty, locked, title, label: format!("Добавить элемент {}, {}", ty.name(), ty.ru_name()) }
                })
                .collect::<Vec<_>>()
        })
    };
    let on_locked_pick = Callback::new(move |ty: GateType| {
        notify.run(format!("{} — и элемент откроется", data.lab().gate_lock_hint(ty)));
        hint_open.set(true);
    });
    let block_palette = {
        let spec = spec.clone();
        Memo::new(move |_| {
            let lib = data.library.get();
            spec.blocks
                .iter()
                .filter_map(|id| {
                    let def = lib.0.def(id)?;
                    let names = |dir: Dir| def.iface.ports.iter().filter(|p| p.dir == dir).map(|p| p.name.clone()).collect::<Vec<_>>().join(", ");
                    Some(BlockItem { id: id.clone(), title: def.title.clone(), available: lib.0.available(id), hint: lib.0.lock_hint(id).to_string(), summary: format!("{} → {}", names(Dir::In), names(Dir::Out)) })
                })
                .collect::<Vec<_>>()
        })
    };
    let add_block = move |item: BlockItem| {
        if !item.available {
            notify.run(format!("{} — и блок откроется", item.hint));
            return;
        }
        instances.update(|list| {
            let taken: Vec<(f64, f64)> = list.iter().map(|i| (i.x, i.y)).collect();
            let (x, y) = free_spot(&taken, BLOCKS_BOARD_W);
            let id = next_instance_id(list);
            list.push(BlockInstance { id, block_id: item.id.clone(), x, y });
        });
        persist.run(());
    };

    // --- вид ------------------------------------------------------------------------------------
    let board = {
        let (spec, iface, scope) = (spec.clone(), iface.clone(), scope.clone());
        move || -> AnyView {
            if !blocks_mode {
                return view! {
                    <GateBoard
                        gates=gates
                        wires=wires
                        spec=spec.clone()
                        input_state=input_state
                        steps_mode=steps_mode
                        values=values
                        palette=palette
                        uid=uid
                        on_toggle_input=toggle_input
                        on_edited=persist
                        on_message=notify
                        on_locked_pick=on_locked_pick
                    />
                }
                .into_any();
            }
            if inspect_path.with(Vec::is_empty) {
                return view! {
                    <BlockBoard
                        iface=iface.clone()
                        library=library
                        instances=instances
                        bus_wires=bus_wires
                        expansion=Signal::derive(move || Some(expansion.get()))
                        scope=scope.clone()
                        clock_node=spec.clock.map(|c| c.as_str().to_string())
                        on_toggle=toggle_node
                        on_edited=persist
                        on_message=notify
                    />
                }
                .into_any();
            }
            let top = {
                let (iface, scope, title) = (iface.clone(), scope.clone(), task_title.clone());
                Signal::derive(move || Level {
                    title: title.clone(),
                    iface: iface.clone(),
                    solution: Arc::new(Solution::Block(BlockSolution { instances: instances.get(), bus_wires: bus_wires.get() })),
                    expansion: expansion.get().0,
                    scope: scope.clone(),
                })
            };
            view! { <Inspector top=top library=library path=inspect_path /> }.into_any()
        }
    };
    let clock_panel = spec.clock.map(|clock_id| {
        let level = move || input_state.with(|s| s.get(clock_id));
        let rates = CLOCK_RATES
            .iter()
            .map(|hz| {
                let hz = *hz;
                view! { <option value=hz.to_string() selected=move || clock.rate.get() == hz>{rate_label(hz)}</option> }
            })
            .collect_view();
        view! {
            <div class="lab-clock" role="group" aria-label="Тактовый генератор">
                <button
                    type="button"
                    class="quiz-btn"
                    on:click=move |_| clock.tick()
                    disabled=move || clock.ticking.get() || clock.auto.get() || level() == 1
                    title=move || if level() == 1 && !clock.ticking.get() && !clock.auto.get() { "Сначала опустите CLK в 0" } else { "Один такт: CLK поднимается в 1 и опускается в 0" }
                >
                    "Такт ▸"
                </button>
                <button
                    type="button"
                    class="quiz-btn ghost"
                    class:running=move || clock.auto.get()
                    on:click=move |_| clock.toggle_auto()
                    disabled=move || clock.ticking.get()
                    title="Автоматический генератор тактов"
                >
                    {move || if clock.auto.get() { "⏸ Пауза" } else { "▶ Авто" }}
                </button>
                <select
                    aria-label="Частота генератора"
                    title="Частота генератора"
                    on:change=move |e| {
                        if let Ok(hz) = event_target_value(&e).parse::<f64>() {
                            clock.set_rate(hz);
                        }
                    }
                >
                    {rates}
                </select>
                <span class="lab-edges" title="Сколько фронтов (0 → 1) подано с начала упражнения">{move || format!("тактов: {}", clock.edges.get())}</span>
            </div>
        }
    });

    let hint_text = task.hint.clone();
    let success = spec.success.clone();
    let formula = spec.formula.clone();
    let total_rows = spec.target.len();
    let blocks_bar = blocks_mode.then(|| {
        view! {
            <div class="lab-blocks" role="toolbar" aria-label="Блоки: кликните, чтобы добавить на доску">
                <For
                    each=move || block_palette.get()
                    key=|b| (b.id.clone(), b.available)
                    children=move |b| {
                        let item = b.clone();
                        view! {
                            <button type="button" class="lab-block-item" class:locked=!b.available title=if b.available { b.summary.clone() } else { b.hint.clone() } on:click=move |_| add_block(item.clone())>
                                <span class="lab-block-name">{if b.available { String::new() } else { "🔒 ".to_string() }}{b.title.clone()}</span>
                                <span class="lab-block-sub">{if b.available { b.summary.clone() } else { b.hint.clone() }}</span>
                            </button>
                        }
                    }
                />
            </div>
        }
    });

    view! {
        <div class="lab">
            <div class="lab-work">
                <div class="lab-card lab-board-card">
                    <div class="lab-card-head">
                        <div>
                            <h3>"Доска"</h3>
                            <p>{board_hint(blocks_mode, steps_mode)}</p>
                        </div>
                        <div class="lab-actions">
                            {clock_panel}
                            <button type="button" class="quiz-btn ghost" on:click=move |_| hint_open.update(|v| *v = !*v)>
                                {move || if hint_open.get() { "Скрыть подсказку" } else { "Подсказка" }}
                            </button>
                            <button type="button" class="quiz-btn ghost" on:click=reset title="Очистить доску">"Очистить"</button>
                        </div>
                    </div>
                    {move || hint_open.get().then(|| {
                        let locks = if blocks_mode { Vec::new() } else { palette.with(|p| p.iter().filter(|i| i.locked).map(|i| i.title.clone()).collect::<Vec<_>>()) };
                        view! {
                            <p class="ex-hint">
                                {hint_text.clone()}
                                {locks.into_iter().map(|t| view! { <span class="lab-lock-hint"><br />{format!("🔒 {t}")}</span> }).collect_view()}
                            </p>
                        }
                    })}
                    {blocks_bar}
                    <div class="lab-board-wrap">
                        {board}
                        {move || flash.get().map(|text| view! { <div class="lab-flash" role="alert">{text}</div> })}
                    </div>
                </div>
                <CheckPanel spec=spec.clone() input_state=input_state values=values passed=passed solved=solved_now table=table />
            </div>
            {move || solved_now.get().then(|| {
                let matched = table.with(|t| t.matched);
                let title = solved_title(steps_mode, matched, total_rows);
                let formula = formula.clone();
                view! {
                    <ResultAlert
                        title=move || view! { {title.clone()} " Формула: " <strong>{formula.clone()}</strong> }
                        text=success.clone()
                        on_next=has_next.get().then_some(on_next)
                    />
                }
            })}
            {steps_mode.then(|| view! { <WaveDiagram wave=wave on_clear=Callback::new(move |()| history.set(vec![])) /> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::model::InputId;

    fn spec() -> CircuitSpec {
        CircuitSpec {
            section: "latches".into(),
            mode: Mode::Steps,
            build: Build::Gates,
            inputs: vec![InputId::A, InputId::B],
            labels: vec![],
            outputs: vec!["Q".into()],
            target: vec![],
            allowed: vec![],
            steps: vec![],
            ports: vec![],
            block: None,
            blocks: vec![],
            clock: None,
            ticks: false,
            formula: String::new(),
            success: String::new(),
            solution: None,
        }
    }

    #[test]
    fn hints_follow_the_kind_of_exercise() {
        assert_eq!(board_hint(false, false), "Соберите схему так, чтобы столбцы «Схема» совпали со столбцами «Цель»");
        assert_eq!(board_hint(false, true), "Соберите схему и выполняйте шаги сценария — сигналы меняются тумблерами");
        assert_eq!(board_hint(true, true), "Соедините блоки шинами и выполняйте шаги сценария — на вход подаётся такт");
        assert_eq!(board_hint(true, false), "Соедините блоки шинами так, чтобы столбцы «Схема» совпали со столбцами «Цель»");
    }

    #[test]
    fn success_title_counts_rows_only_for_tables() {
        assert_eq!(solved_title(false, 4, 4), "Схема работает — 4 из 4!");
        assert_eq!(solved_title(true, 0, 0), "Схема работает как надо!");
    }

    #[test]
    fn sample_holds_active_inputs_and_outputs() {
        let mut inputs = InputState::zero();
        inputs.set(InputId::B, 1);
        let values = Values::from([("Q".to_string(), Some(1))]);
        let s = sample_of(&spec(), &inputs, &values);
        assert_eq!(s.inputs.get(&InputId::A), Some(&0));
        assert_eq!(s.inputs.get(&InputId::B), Some(&1));
        assert_eq!(s.outputs.get("Q"), Some(&Some(1)));
        // выход, которого нет в значениях, — «?»
        assert_eq!(sample_of(&spec(), &inputs, &Values::new()).outputs.get("Q"), Some(&None));
    }

    #[test]
    fn history_adds_a_column_per_input_change_and_keeps_the_latest_ones() {
        let mut h = Vec::new();
        let s = |q: u8| Sample { inputs: BTreeMap::new(), outputs: BTreeMap::from([("Q".to_string(), Some(q))]) };
        record_sample(&mut h, s(0), true);
        record_sample(&mut h, s(1), false);
        assert_eq!(h, vec![s(1)], "без смены тумблеров столбец обновляется");
        for _ in 0..40 {
            record_sample(&mut h, s(0), true);
        }
        assert_eq!(h.len(), HISTORY_MAX);
        // на пустой истории обновлять нечего
        let mut empty = Vec::new();
        record_sample(&mut empty, s(1), false);
        assert!(empty.is_empty());
    }
}
