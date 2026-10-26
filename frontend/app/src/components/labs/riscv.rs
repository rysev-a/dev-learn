//! Лаборатория «RISC-V» (главы 16 «RISC-V» и 17 «Настоящие программы» книги 14): редактор программы на ассемблере,
//! листинг машинного кода, пошаговый «мягкий процессор» RV32IM с памятью и периферией.
//!
//! Движок — крейт `riscvlab` (общий с сервером): ассемблер, машина и проверка. Здесь только интерфейс. Когда запуск
//! выполняет задание, текст программы уходит на сервер (`LabProps::report`), и тот перепроверяет её тем же `riscvlab::verify`.
//! В отличие от React-версии эталонное решение клиенту не отдаётся, поэтому кнопки «Показать решение» нет.

use leptos::prelude::*;
use riscvlab::task::{Profile, TaskSpec};

use super::LabProps;

mod download;
mod extras;
mod format;
mod machine;
mod program;
mod session;

use extras::{ProjectCard, ReferenceCard};
use machine::{CpuCard, MemoryCard, OutputCard, PeripheralsCard, ResultAlert};
use program::{ListingCard, ProgramCard, TaskData};
use session::Session;

/// Описание упражнения из `spec` задачи (эталона в нём нет, поэтому `reference` пуст).
fn parse_spec(raw: &serde_json::Value) -> Result<TaskSpec, String> {
    serde_json::from_value(raw.clone()).map_err(|e| format!("Неверное описание упражнения: {e}"))
}

/// Лаборатория выбранного упражнения.
#[component]
pub fn RiscvLab(props: LabProps) -> impl IntoView {
    let spec = match parse_spec(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let real = spec.profile == Profile::Linux;
    let data = spec.data.clone();
    let hint = props.task.hint.clone();
    // черновик ученика, а если его нет — заготовка
    let draft = props.draft.get_untracked();
    let initial = if draft.is_empty() { spec.starter.clone() } else { draft };
    let session = Session::new(spec, initial, props.solved, props.report, props.on_draft);
    let on_next = props.on_next;
    view! {
        <div class="lab lab-asm lab-rv">
            <TaskData data=data />
            <div class="lab-asm-grid">
                <section class="lab-col">
                    <ProgramCard session=session hint=hint solved=props.solved />
                    <ListingCard session=session />
                </section>
                <section class="lab-col">
                    <CpuCard session=session />
                    <ResultAlert result=session.result on_next=on_next has_next=props.has_next />
                    {if real {
                        view! { <OutputCard session=session /> }.into_any()
                    } else {
                        view! { <PeripheralsCard session=session /> }.into_any()
                    }}
                    <MemoryCard session=session />
                </section>
            </div>
            {real.then(|| view! { <ProjectCard session=session /> })}
            <ReferenceCard />
        </div>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::parse_spec;
    use riscvlab::task::Profile;
    use serde_json::json;

    #[test]
    fn spec_from_server_has_no_reference() {
        let raw = json!({
            "profile": "linux", "starter": "_start:\n", "data": "msg: .asciz \"x\"\n", "max_steps": 1000,
            "tests": [{ "check": { "kind": "run", "stdout": "x", "code": 0, "ok": "ок" } }],
        });
        let spec = parse_spec(&raw).expect("разбирается без эталона");
        assert_eq!((spec.profile, spec.reference.as_str(), spec.max_steps), (Profile::Linux, "", 1000));
    }

    #[test]
    fn broken_spec_is_reported_in_russian() {
        let err = parse_spec(&json!({ "profile": "mars" })).expect_err("профиля «mars» нет");
        assert!(err.starts_with("Неверное описание упражнения"), "{err}");
    }
}
