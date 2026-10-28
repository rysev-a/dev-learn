//! "System design" lab (book 18): a high-load service diagram on the board, a calculation under a given load and
//! the exercise goals. The calculation, goals and link validity come from the `sdlab` crate (shared with the server, which also re-checks the solution);
//! this module is the interface only.
//!
//! * `lab.rs` — state: the diagram, selection, failures, calculation and diagram actions;
//! * `logic.rs` — pure logic (draft, edits, wires, fitting, labels) with tests;
//! * `board.rs` — the board: palette, components, links, ports, auto-wiring, pan and zoom (`board_view.rs`);
//! * `panels.rs` — parameter card, help, tools, goals and metrics;
//! * `icons.rs` — component icons.
//!
//! The draft (diagram) goes to the owner on every edit, and once all goals are met the solution is sent to the server exactly once.

use std::sync::Arc;

use leptos::{ev, portal::Portal, prelude::*};

mod board;
mod icons;
mod lab;
mod logic;
mod panels;

use board::Board;
use lab::Lab;
use panels::{Chips, Corner, Goals, Metrics, Overlay, Toolbar};

use super::LabProps;
use crate::dom;

/// What to write as the outcome: solved earlier, accepted just now, or the solution is still being checked on the server.
fn verdict_text(solved_before: bool, solved: bool) -> &'static str {
    if solved_before {
        i18n::tr("The exercise was already solved.")
    } else if solved {
        i18n::tr("Exercise accepted.")
    } else {
        i18n::tr("Checking the solution on the server…")
    }
}

/// Lab of the selected exercise.
#[component]
pub fn SdLab(props: LabProps) -> impl IntoView {
    let scenario = match logic::parse_scenario(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let initial = logic::restore(&scenario, &props.draft.get_untracked());
    let lab = Lab::new(Arc::new(scenario), initial, props.task.hint.clone(), props.on_draft);

    // the solution is sent once, when all goals are met; if the server rejects it, a retry happens after new edits
    let solved_before = props.solved.get_untracked();
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
            report.run(lab.state.with_untracked(logic::draft_json));
        }
    });

    // fullscreen: the page under the diagram does not scroll, Esc closes
    let page_overflow = StoredValue::new_local(None::<String>);
    Effect::new(move |_| {
        let Some(body) = web_sys::window().and_then(|w| w.document()).and_then(|d| d.body()) else { return };
        let style = body.style();
        if lab.fs.get() {
            page_overflow.set_value(Some(style.get_property_value("overflow").unwrap_or_default()));
            let _ = style.set_property("overflow", "hidden");
        } else if let Some(old) = page_overflow.try_update_value(Option::take).flatten() {
            let _ = style.set_property("overflow", &old);
        }
    });
    on_cleanup(move || {
        if let (Some(old), Some(body)) = (page_overflow.try_update_value(Option::take).flatten(), web_sys::window().and_then(|w| w.document()).and_then(|d| d.body())) {
            let _ = body.style().set_property("overflow", &old);
        }
    });
    dom::on_window(ev::keydown, move |e| {
        if e.key() == "Escape" && lab.fs.get_untracked() {
            lab.fs.set(false);
        }
    });

    let verdict = Signal::derive(move || verdict_text(solved_before, solved.get()).to_owned());
    let (has_next, on_next) = (props.has_next, props.on_next);
    let side = move || view! { <Goals lab=lab verdict=verdict has_next=has_next on_next=on_next /> <Metrics lab=lab /> };
    view! {
        {move || {
            if lab.fs.get() {
                // fullscreen — above the page, outside its layout
                view! {
                    <Portal>
                        <div class="sd fs">
                            <div class="sd-fs-main">
                                <BoardCard lab=lab fullscreen=true />
                            </div>
                            <div class="sd-side">{side()}</div>
                        </div>
                    </Portal>
                }
                .into_any()
            } else {
                view! {
                    <div class="sd">
                        <div class="sd-work">
                            <BoardCard lab=lab fullscreen=false />
                        </div>
                        <div class="sd-bottom">{side()}</div>
                    </div>
                }
                .into_any()
            }
        }}
    }
    .into_any()
}

/// Board card: load, tools, hint, the board itself and messages under it.
#[component]
fn BoardCard(lab: Lab, fullscreen: bool) -> impl IntoView {
    let edge_hint = move || {
        let e = lab.sel_edge.get()?;
        let name = |id: &str| lab.state.with(|s| s.node(id).map_or_else(|| id.to_owned(), |n| n.name.clone()));
        Some(i18n::trf!("Link “{0} → {1}” selected — “Delete” will remove it.", name(&e.from), name(&e.to)))
    };
    view! {
        <div class="sd-boardcard">
            <Chips lab=lab />
            <Toolbar lab=lab />
            {move || lab.hint_open.get().then(|| view! { <p class="sd-hint">{lab.hint.get_value()}</p> })}
            <Board lab=lab fullscreen=fullscreen corner=move || view! { <Corner lab=lab /> } overlay=move || view! { <Overlay lab=lab /> } />
            {move || {
                let n = lab.notice.get();
                (!n.is_empty()).then(|| view! { <p class="sd-notice">{n}</p> })
            }}
            {move || edge_hint().map(|t| view! { <p class="sd-hint">{t}</p> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn verdict_distinguishes_old_new_and_pending_solutions() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(verdict_text(true, true), "Упражнение уже было решено.");
        assert_eq!(verdict_text(false, true), "Упражнение засчитано.");
        assert_eq!(verdict_text(false, false), "Проверяю решение на сервере…");
    }
}
