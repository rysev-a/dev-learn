//! The boards of a Python task beside its results (levels 2 and 3 of the board tasks): the tabs, the choice of the shown test and the
//! dispatch on the board model the task belongs to (`kind` of the task data). The pictures and the judging of the repaired boards are per model
//! (`<board>/picture.rs`).
//!
//! * level 2 — a task whose answer is data: the board of every test with the statuses the model derives;
//! * level 3 — a `fix(board)` task: the starting board of every scenario, and after a run the board the code returned.

use leptos::prelude::*;

use super::{lvm_board, net_board, ovirt_topo};

/// The boards of a task beside its results. Renders nothing for a task without boards.
#[component]
pub fn TaskBoards(boards: api::dto::TaskBoards, res: Signal<Option<api::dto::RunResult>>) -> impl IntoView {
    let fix = !boards.checks.is_empty();
    let count = if fix { boards.checks.len() } else { boards.boards.len() };
    let shown = RwSignal::new(0usize);
    let after = RwSignal::new(true);

    // level 2: after a run the first failing test is shown
    Effect::new(move |_| {
        if let Some(r) = res.get() {
            if let Some(i) = r.results.iter().position(|t| !t.ok) {
                shown.set(i.min(count.saturating_sub(1)));
            }
        }
    });

    let tabs = (0..count)
        .map(|i| {
            let mark = move || match res.get().and_then(|r| r.results.get(i).map(|t| t.ok)) {
                Some(true) => "✓".to_string(),
                Some(false) => "✗".to_string(),
                None => (i + 1).to_string(),
            };
            view! {
                <button type="button" class="vl-tab" class:on=move || shown.get() == i class:ok=move || res.get().and_then(|r| r.results.get(i).map(|t| t.ok)) == Some(true) on:click=move |_| shown.set(i)>
                    <span class="vl-tab-mark">{mark}</span>
                    {if fix { i18n::tr("Board").to_string() } else { i18n::tr("Test").to_string() }}
                </button>
            }
        })
        .collect_view();

    let for_view = boards.clone();
    let body = move || {
        let i = shown.get();
        match for_view.kind.as_str() {
            "lvm_board" => lvm_board::task_body(&for_view, i, after, res),
            "net_board" => net_board::task_body(&for_view, i, after, res),
            _ => ovirt_topo::task_body(&for_view, i, after, res),
        }
    };
    (count > 0).then(|| {
        view! {
            <div class="vl-pic">
                <span class="s-label">{if fix { i18n::tr("Boards") } else { i18n::tr("Board of the test") }}</span>
                <div class="vl-tabs">{tabs}</div>
                {body}
            </div>
        }
    })
}
