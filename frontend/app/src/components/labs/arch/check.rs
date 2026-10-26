//! Проверка решения на экране: таблица истинности или сценарий по шагам и временная диаграмма
//! (`CheckPanel.tsx`, `WaveDiagram.tsx`).

use std::sync::Arc;

use archlab::{
    check::TableCheck,
    exercise::CircuitSpec,
    model::{inputs_for_row, InputId, InputState, Values},
    wave::{wave_width, Wave, STEP},
};
use leptos::prelude::*;

/// Значение узла по имени в таблице значений (`None` — «?» или узла нет).
pub fn value_in(values: &Values, node: &str) -> Option<u8> {
    values.get(node).copied().flatten()
}

/// Шаг сценария выполнен: тумблеры стоят как в условии шага, а выходы, которые шаг проверяет, равны ожидаемым.
pub fn step_met(spec: &CircuitSpec, index: usize, inputs: &InputState, values: &Values) -> bool {
    let Some(step) = spec.steps.get(index) else { return false };
    spec.inputs.iter().all(|id| step.inputs.get(id) == Some(&inputs.get(*id)))
        && spec.outputs.iter().all(|o| step.expect.get(o).is_none_or(|e| value_in(values, o) == Some(*e)))
}

/// Номер шага, который показывается как текущий: не дальше последнего.
pub fn shown_step(passed: usize, total: usize) -> usize {
    (passed + 1).min(total)
}

/// Карточка проверки: сценарий по шагам или таблица истинности.
#[component]
pub fn CheckPanel(
    spec: Arc<CircuitSpec>,
    input_state: RwSignal<InputState>,
    values: Memo<Values>,
    passed: RwSignal<usize>,
    #[prop(into)] solved: Signal<bool>,
    table: Memo<TableCheck>,
) -> impl IntoView {
    if spec.mode == archlab::exercise::Mode::Steps {
        view! { <StepsCard spec=spec input_state=input_state values=values passed=passed solved=solved /> }.into_any()
    } else {
        view! { <TableCard spec=spec input_state=input_state table=table solved=solved /> }.into_any()
    }
}

#[component]
fn StepsCard(spec: Arc<CircuitSpec>, input_state: RwSignal<InputState>, values: Memo<Values>, passed: RwSignal<usize>, solved: Signal<bool>) -> impl IntoView {
    let total = spec.steps.len();
    let steps = spec
        .steps
        .iter()
        .enumerate()
        .map(|(i, st)| {
            let pulses = st.pulses.filter(|p| *p > 1);
            let in_chips = spec
                .inputs
                .iter()
                .map(|id| {
                    let (id, want, label) = (*id, st.inputs.get(id).copied(), spec.label_of(*id));
                    let shown = want.map_or_else(|| "—".to_string(), |w| w.to_string());
                    view! {
                        <span class="lab-chip" class:hit=move || want.is_some_and(|w| input_state.with(|s| s.get(id)) == w)>{format!("{label} = {shown}")}</span>
                    }
                })
                .collect_view();
            let out_chips = spec
                .outputs
                .iter()
                .filter_map(|o| {
                    let want = *st.expect.get(o)?;
                    let o = o.clone();
                    let name = o.clone();
                    Some(view! {
                        <span class="lab-chip out" class:hit=move || values.with(|v| value_in(v, &o)) == Some(want)>{format!("{name} = {want}")}</span>
                    })
                })
                .collect_view();
            let none_checked = spec.outputs.iter().all(|o| !st.expect.contains_key(o));
            view! {
                <div class="lab-step" class:done=move || i < passed.get() class:active=move || i == passed.get()>
                    <span class="lab-step-no">{move || if i < passed.get() { "✓".to_string() } else { (i + 1).to_string() }}</span>
                    <div>
                        <p class="lab-step-text">{st.text.clone()}</p>
                        <div class="lab-step-req">
                            {pulses.map(|p| view! { <span class="lab-chip pulses">{format!("тактов: {p}")}</span> })}
                            {in_chips}
                            <span class="lab-chip-sep">"→"</span>
                            {out_chips}
                            {none_checked.then(|| view! { <span class="lab-chip out hit">"выход пока не проверяется"</span> })}
                        </div>
                    </div>
                </div>
            }
        })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>"Сценарий проверки"</h3>
                    <p>"Выполняйте шаги по порядку: устанавливайте тумблеры и добивайтесь нужных значений на выходах"</p>
                </div>
                <span class="lab-badge" class:ok=move || solved.get()>{move || format!("Шаг {} / {total}", shown_step(passed.get(), total))}</span>
            </div>
            <div class="lab-steps">{steps}</div>
        </div>
    }
}

#[component]
fn TableCard(spec: Arc<CircuitSpec>, input_state: RwSignal<InputState>, table: Memo<TableCheck>, solved: Signal<bool>) -> impl IntoView {
    let labels = spec.labels_or_ids();
    let total = spec.target.len();
    let heads_in = labels.iter().map(|l| view! { <th>{l.clone()}</th> }).collect_view();
    let heads_target = spec.outputs.iter().map(|o| view! { <th class="sep">{format!("Цель {o}")}</th> }).collect_view();
    let heads_actual = spec.outputs.iter().map(|o| view! { <th>{format!("Схема {o}")}</th> }).collect_view();
    let inputs = spec.inputs.clone();
    let current = {
        let inputs = inputs.clone();
        Memo::new(move |_| input_state.with(|s| s.row(&inputs)))
    };
    let rows = (0..total)
        .map(|i| {
            let state = inputs_for_row(&spec.inputs, i);
            let ins = spec.inputs.iter().map(|id: &InputId| view! { <td class="in">{state.get(*id)}</td> }).collect_view();
            let targets = spec.target.get(i).cloned().unwrap_or_default();
            let target_cells = targets.iter().map(|t| view! { <td class="sep target">{*t}</td> }).collect_view();
            let outputs = spec.outputs.len();
            let actual_cells = (0..outputs)
                .map(|k| {
                    let want = targets.get(k).copied();
                    let actual = move || table.with(|t| t.rows.get(i).and_then(|r| r.actuals.get(k).copied()).flatten());
                    view! {
                        <td class=move || {
                            let a = actual();
                            format!("actual {}", if a.is_some() && a == want { "ok" } else if a.is_some() { "bad" } else { "na" })
                        }>{move || actual().map_or_else(|| "—".to_string(), |a| a.to_string())}</td>
                    }
                })
                .collect_view();
            let mark = move || {
                table.with(|t| match t.rows.get(i) {
                    Some(r) if r.actuals.first().copied().flatten().is_none() => view! { <span class="na-mark">"·"</span> }.into_any(),
                    Some(r) if r.ok => view! { <span class="ok-mark">"✓"</span> }.into_any(),
                    _ => view! { <span class="bad-mark">"✕"</span> }.into_any(),
                })
            };
            view! {
                <tr class:current=move || current.get() == i>
                    {ins}
                    {target_cells}
                    {actual_cells}
                    <td class="mark">{mark}</td>
                </tr>
            }
        })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <h3 title="Строка с подсветкой — текущее положение тумблеров на доске">"Таблица истинности"</h3>
                <span class="lab-badge" class:ok=move || solved.get()>{move || format!("{} / {total}", table.with(|t| t.matched))}</span>
            </div>
            <div class="lab-tt-scroll">
                <table class="lab-tt">
                    <thead>
                        <tr>{heads_in}{heads_target}{heads_actual}<th></th></tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>
    }
}

/// Временная диаграмма: история сигналов в упражнениях с защёлками и регистрами.
#[component]
pub fn WaveDiagram(wave: Memo<Wave>, on_clear: Callback<()>) -> impl IntoView {
    let width = wave_width();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>"Временная диаграмма"</h3>
                    <p>"История сигналов: каждый столбец — одно изменение. Пунктир — значение пока не определено"</p>
                </div>
                <button type="button" class="quiz-btn ghost" on:click=move |_| on_clear.run(())>"Очистить"</button>
            </div>
            <svg class="lab-wave" viewBox=move || format!("0 0 {width} {}", wave.with(|w| w.height)) role="img" aria-label="Временная диаграмма сигналов">
                {move || wave.with(|w| {
                    let h = w.height;
                    let grid = w.cols.iter().map(|x| view! { <line class="wave-grid" x1=*x x2=*x y1="0" y2=h></line> }).collect_view();
                    let now = (!w.cols.is_empty()).then(|| view! { <rect class="wave-now" x=w.last_x y="0" width=STEP height=h></rect> });
                    let rows = w.rows.iter().map(|r| {
                        let kind = match r.kind {
                            archlab::wave::RowKind::In => "in",
                            archlab::wave::RowKind::Clk => "clk",
                            archlab::wave::RowKind::Out => "out",
                        };
                        view! {
                            <g class=format!("wave-row {kind}")>
                                <text class="wave-label" x="0" y=r.top + 18.0>{r.label.clone()}</text>
                                <path class="wave-x" d=r.dx.clone()></path>
                                <path class="wave-line" d=r.d.clone()></path>
                            </g>
                        }
                    }).collect_view();
                    view! { {grid} {now} {rows} }
                })}
            </svg>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::exercise::{Build, Mode, Step};
    use std::collections::BTreeMap;

    fn spec() -> CircuitSpec {
        let step = |a: u8, y: u8| Step {
            inputs: BTreeMap::from([(InputId::A, a)]),
            expect: BTreeMap::from([("Q".to_string(), y)]),
            text: String::new(),
            pulses: None,
        };
        CircuitSpec {
            section: "latches".into(),
            mode: Mode::Steps,
            build: Build::Gates,
            inputs: vec![InputId::A],
            labels: vec![],
            outputs: vec!["Q".into()],
            target: vec![],
            allowed: vec![],
            steps: vec![step(1, 1), step(0, 1)],
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

    fn values(q: Option<u8>) -> Values {
        Values::from([("Q".to_string(), q)])
    }

    #[test]
    fn step_is_met_only_with_the_right_switches_and_outputs() {
        let sp = spec();
        let mut on = InputState::zero();
        on.set(InputId::A, 1);
        assert!(step_met(&sp, 0, &on, &values(Some(1))));
        assert!(!step_met(&sp, 0, &on, &values(Some(0))), "выход не тот");
        assert!(!step_met(&sp, 0, &on, &values(None)), "«?» не равно ожидаемому");
        assert!(!step_met(&sp, 0, &InputState::zero(), &values(Some(1))), "тумблер не тот");
        assert!(!step_met(&sp, 5, &on, &values(Some(1))), "шага нет");
    }

    #[test]
    fn unchecked_output_does_not_block_a_step() {
        let mut sp = spec();
        sp.steps[0].expect.clear();
        let mut on = InputState::zero();
        on.set(InputId::A, 1);
        assert!(step_met(&sp, 0, &on, &values(None)));
    }

    #[test]
    fn shown_step_never_runs_past_the_last() {
        assert_eq!(shown_step(0, 3), 1);
        assert_eq!(shown_step(2, 3), 3);
        assert_eq!(shown_step(3, 3), 3);
    }
}
