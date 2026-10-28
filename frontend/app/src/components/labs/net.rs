//! The "Computer Networks" lab (book 15): a network simulator in the browser. The learner connects devices with cables, configures
//! addresses, routes, VLAN, NAT, firewall, DNS, HTTP, TLS, SSH, VPN, load balancers and runs Linux commands in a
//! mini terminal; packets run along the diagram with a log beside it. The engine is the `netlab` crate (shared with the server, which also re-checks
//! the submitted solution); only the interface is here.
//!
//! * `lab.rs` — state: network, selection, animated probe, terminals, goals and actions on the network;
//! * `logic.rs` — pure logic (scenario, draft, animation "moments", form edits, terminal history);
//! * `geom.rs` — board geometry (window settings, cables, device under the cursor) without DOM; pan and zoom are the shared `board_view.rs`;
//! * `board.rs` — the board: devices, cables, packets, marks, dragging, pan and zoom;
//! * `panel.rs`, `forms.rs`, `services.rs` — the device card and its forms; `terminal.rs` — the mini terminal;
//! * `side.rs` — goals and log; `chart.rs` — the file transfer chart.
//!
//! The draft (network state) goes to the host on every edit, and when all goals are met, the solution is sent to the
//! server once.

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
mod geom;

use super::LabProps;
use board::Board;
use chart::Chart;
use lab::Lab;
use panel::DevicePanel;
use side::{Goals, Log};

/// The lab of the selected exercise.
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

    // the solution is sent once, when all goals are met; if the server refused, a retry comes after new edits
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

/// The panel above the board: the cable (if the tool is open), a hint and "Reset".
#[component]
fn Toolbar(lab: Lab) -> impl IntoView {
    let cable_tool = lab.tools().cable;
    view! {
        <div class="nl-toolbar">
            {cable_tool.then(|| view! {
                <button type="button" class=move || if lab.cable.get() { "quiz-btn ghost running" } else { "quiz-btn ghost" } on:click=move |_| lab.toggle_cable()>
                    {move || if lab.cable.get() { i18n::tr("Cable: pick two devices") } else { i18n::tr("Cable") }}
                </button>
                {move || lab.sel_link.get().is_some().then(|| view! {
                    <button type="button" class="quiz-btn ghost" on:click=move |_| lab.remove_link()>{i18n::tr("Delete cable")}</button>
                })}
            })}
            <span class="nl-spacer"></span>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.hint_open.update(|v| *v = !*v)>{i18n::tr("Hint")}</button>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.reset()>{i18n::tr("Reset")}</button>
        </div>
    }
}
