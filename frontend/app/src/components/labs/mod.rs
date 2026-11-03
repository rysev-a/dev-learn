//! Lab exercises in chapter practice: the statement and scenario come from the backend (`GET /api/labs/{book}/{chapter}`), the calculation is
//! in the lab engine crate (shared with the server), and the server re-checks a solved exercise with the same engine.
//!
//! [`LabHost`] loads the chapter scenarios, picks the interface by lab kind and accepts a solution from it: `LabProps::report`
//! sends the solution to the server and marks the exercise solved only after the server agrees.

use api::dto::LabTask;
use leptos::{prelude::*, task::spawn_local};

use crate::hooks::{client, use_load, Load};

pub mod board_view;

mod arch;
mod net;
mod riscv;
mod sd;
mod virt;
pub use virt::TaskBoards;
mod web;

/// What the interface of a particular lab receives.
#[derive(Clone)]
pub struct LabProps {
    /// the exercise: statement, hint and scenario (`spec` is the lab data)
    pub task: LabTask,
    /// the learner's saved state (draft), a JSON/text string; empty means start from the initial one
    pub draft: Signal<String>,
    /// save the draft (sent to the server with a pause)
    pub on_draft: Callback<String>,
    /// the exercise is already solved (earlier or just now)
    pub solved: Signal<bool>,
    /// report a solution: the server checks it with the engine; on refusal the reason appears under the lab
    pub report: Callback<String>,
    /// go to the next exercise
    pub on_next: Callback<()>,
    /// whether there is a next exercise
    pub has_next: Signal<bool>,
}

/// The lab of the selected exercise.
#[component]
pub fn LabHost(
    book: i64,
    num: i64,
    task_id: String,
    #[prop(into)] draft: Signal<String>,
    on_draft: Callback<String>,
    #[prop(into)] solved: Signal<bool>,
    /// the exercise was accepted by the server
    on_solved: Callback<()>,
    on_next: Callback<()>,
    #[prop(into)] has_next: Signal<bool>,
) -> impl IntoView {
    let chapter = use_load(move || Some(()), move |c, _| async move { c.lab_chapter(book, num).await });
    let error = RwSignal::new(String::new());
    move || match chapter.get() {
        Load::Loading => view! { <p class="empty">{i18n::tr("Loading…")}</p> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Ready(ch) => {
            let Some(task) = ch.tasks.iter().find(|t| t.id == task_id).cloned() else {
                return view! { <p class="empty">{i18n::tr("Exercise not found")}</p> }.into_any();
            };
            let id = task.id.clone();
            let report = Callback::new(move |solution: String| {
                let id = id.clone();
                spawn_local(async move {
                    match client().mark_lab_solved(book, num, &id, &solution).await {
                        Ok(()) => {
                            error.set(String::new());
                            on_solved.run(());
                        }
                        Err(e) => error.set(e.message),
                    }
                });
            });
            let props = LabProps { task, draft, on_draft, solved, report, on_next, has_next };
            let lab = match ch.lab.as_str() {
                "sd" => view! { <sd::SdLab props=props /> }.into_any(),
                "virt" => view! { <virt::VirtLab props=props /> }.into_any(),
                "net" => view! { <net::NetLab props=props /> }.into_any(),
                "arch" => view! { <arch::ArchLab props=props /> }.into_any(),
                "riscv" => view! { <riscv::RiscvLab props=props /> }.into_any(),
                "web" => view! { <web::WebLab props=props /> }.into_any(),
                other => view! { <p class="empty">{i18n::trf!("Unknown lab “{0}”", other)}</p> }.into_any(),
            };
            view! {
                {lab}
                {move || (!error.get().is_empty()).then(|| view! { <p class="error">{i18n::trf!("Solution rejected: {0}", error.get())}</p> })}
            }
            .into_any()
        }
    }
}
