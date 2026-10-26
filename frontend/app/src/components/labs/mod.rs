//! Упражнения-лаборатории в практике главы: условие и сценарий приходят с бэкенда (`GET /api/labs/{книга}/{глава}`), расчёт —
//! в крейте движка лаборатории (общем с сервером), а решённое упражнение сервер перепроверяет тем же движком.
//!
//! [`LabHost`] загружает сценарии главы, выбирает интерфейс по виду лаборатории и принимает от него решение: `LabProps::report`
//! отправляет решение на сервер и отмечает упражнение решённым только после его согласия.

use api::dto::LabTask;
use leptos::{prelude::*, task::spawn_local};

use crate::hooks::{client, use_load, Load};

pub mod board_view;

mod arch;
mod net;
mod riscv;
mod sd;
mod virt;

/// Что получает интерфейс конкретной лаборатории.
#[derive(Clone)]
pub struct LabProps {
    /// упражнение: условие, подсказка и сценарий (`spec` — данные лаборатории)
    pub task: LabTask,
    /// сохранённое состояние ученика (черновик), строка JSON/текст; пусто — начать с исходного
    pub draft: Signal<String>,
    /// сохранить черновик (отправляется на сервер с паузой)
    pub on_draft: Callback<String>,
    /// упражнение уже решено (раньше или только что)
    pub solved: Signal<bool>,
    /// сообщить решение: сервер проверит его движком; при отказе под лабораторией появится причина
    pub report: Callback<String>,
    /// перейти к следующему упражнению
    pub on_next: Callback<()>,
    /// есть ли следующее упражнение
    pub has_next: Signal<bool>,
}

/// Лаборатория выбранного упражнения.
#[component]
pub fn LabHost(
    book: i64,
    num: i64,
    task_id: String,
    #[prop(into)] draft: Signal<String>,
    on_draft: Callback<String>,
    #[prop(into)] solved: Signal<bool>,
    /// упражнение принято сервером
    on_solved: Callback<()>,
    on_next: Callback<()>,
    #[prop(into)] has_next: Signal<bool>,
) -> impl IntoView {
    let chapter = use_load(move || Some(()), move |c, _| async move { c.lab_chapter(book, num).await });
    let error = RwSignal::new(String::new());
    move || match chapter.get() {
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Ready(ch) => {
            let Some(task) = ch.tasks.iter().find(|t| t.id == task_id).cloned() else {
                return view! { <p class="empty">"Упражнение не найдено"</p> }.into_any();
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
                other => view! { <p class="empty">{format!("Неизвестная лаборатория «{other}»")}</p> }.into_any(),
            };
            view! {
                {lab}
                {move || (!error.get().is_empty()).then(|| view! { <p class="error">{format!("Решение не принято: {}", error.get())}</p> })}
            }
            .into_any()
        }
    }
}
