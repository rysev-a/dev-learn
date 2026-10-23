//! Лаборатория «Компьютерные сети» (книга 15): симулятор сети в браузере. Ученик соединяет устройства кабелями, настраивает
//! адреса, маршруты, VLAN, NAT, файрвол, DNS, HTTP, TLS, SSH, VPN, балансировщики и запускает команды Linux в
//! мини-терминале; пакеты бегут по схеме, рядом журнал. Движок — крейт `netlab` (общий с сервером, он же перепроверяет
//! присланное решение); здесь только интерфейс.
//!
//! * `lab.rs` — состояние: сеть, выбор, проба с анимацией, терминалы, цели и действия над сетью;
//! * `logic.rs` — чистая логика (сценарий, черновик, «моменты» анимации, правки форм, история терминала);
//! * `view.rs` — геометрия поля (окно, масштаб, перевод мыши, кабели) без DOM;
//! * `board.rs` — поле: устройства, кабели, пакеты, пометки, перетаскивание, сдвиг и масштаб;
//! * `panel.rs`, `forms.rs`, `services.rs` — карточка устройства и её формы; `terminal.rs` — мини-терминал;
//! * `side.rs` — цели и журнал; `chart.rs` — график передачи файла.
//!
//! Черновик (состояние сети) уходит хозяину при каждой правке, а когда выполнены все цели, решение отправляется на
//! сервер один раз.

use std::sync::Arc;

use leptos::prelude::*;

mod board;
mod chart;
mod forms;
mod lab;
mod logic;
mod panel;
mod services;
mod side;
mod terminal;
mod view;

use super::LabProps;
use board::Board;
use chart::Chart;
use lab::Lab;
use panel::DevicePanel;
use side::{Goals, Log};

/// Лаборатория выбранного упражнения.
#[component]
pub fn NetLab(props: LabProps) -> impl IntoView {
    let spec = match logic::parse_spec(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let initial = logic::restore(&spec, &props.draft.get_untracked());
    let solved_before = props.solved.get_untracked();
    let touched = solved_before || logic::differs_from_start(&spec, &initial);
    let goal_count = spec.goals.len();
    let lab = Lab::new(Arc::new(spec), initial, props.task.hint.clone(), props.on_draft, touched);
    on_cleanup(move || lab.stop());

    // решение отправляется один раз, когда выполнены все цели; если сервер отказал, повтор — после новых правок
    let reported = StoredValue::new(false);
    let (solved, report) = (props.solved, props.report);
    Effect::new(move |_| {
        let ok = lab.solved_now.get();
        if solved.get_untracked() {
            return;
        }
        if !ok {
            reported.set_value(false);
        } else if !reported.get_value() {
            reported.set_value(true);
            report.run(lab.solution_json());
        }
    });

    view! {
        <div class="nl">
            <div class="nl-main">
                <div class="nl-boardcard">
                    <Toolbar lab=lab />
                    {move || lab.hint_open.get().then(|| view! { <p class="nl-hint">{lab.hint()}</p> })}
                    {move || {
                        let n = lab.notice.get();
                        (!n.is_empty()).then(|| view! { <p class="nl-notice">{n}</p> })
                    }}
                    <Board lab=lab />
                    {move || lab.chart.get().map(|c| view! { <Chart chart=c /> })}
                    {move || lab.run.with(|r| r.as_ref().map(|run| logic::caption(run, lab.slot.get()))).map(|c| view! { <p class="nl-caption">{c}</p> })}
                </div>
                <DevicePanel lab=lab />
            </div>
            <div class="nl-bottom">
                <Goals lab=lab count=goal_count solved_before=solved_before solved=props.solved has_next=props.has_next on_next=props.on_next />
                <Log lab=lab />
            </div>
        </div>
    }
    .into_any()
}

/// Панель над полем: кабель (если открыт инструмент), подсказка и «Сбросить».
#[component]
fn Toolbar(lab: Lab) -> impl IntoView {
    let cable_tool = lab.tools().cable;
    view! {
        <div class="nl-toolbar">
            {cable_tool.then(|| view! {
                <button type="button" class=move || if lab.cable.get() { "quiz-btn ghost running" } else { "quiz-btn ghost" } on:click=move |_| lab.toggle_cable()>
                    {move || if lab.cable.get() { "Кабель: выберите два устройства" } else { "Кабель" }}
                </button>
                {move || lab.sel_link.get().is_some().then(|| view! {
                    <button type="button" class="quiz-btn ghost" on:click=move |_| lab.remove_link()>"Удалить кабель"</button>
                })}
            })}
            <span class="nl-spacer"></span>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.hint_open.update(|v| *v = !*v)>"Подсказка"</button>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.reset()>"Сбросить"</button>
        </div>
    }
}
