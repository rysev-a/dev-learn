//! The "RISC-V" lab (chapters 16 "RISC-V" and 17 "Real programs" of book 14): an assembly program editor,
//! a machine code listing, a step-by-step "soft processor" RV32IM with memory and peripherals.
//!
//! The engine is the `riscvlab` crate (shared with the server): assembler, machine and checking. Only the interface is here. When a run
//! completes the task, the program text goes to the server (`LabProps::report`), which re-checks it with the same `riscvlab::verify`.
//! Unlike the React version, the reference solution is not sent to the client, so there is no "Show solution" button.

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

/// Exercise description from the task `spec` (it has no reference, so `reference` is empty).
fn parse_spec(raw: &serde_json::Value) -> Result<TaskSpec, String> {
    serde_json::from_value(raw.clone()).map_err(|e| i18n::trf!("Invalid exercise description: {0}", e))
}

/// The lab of the selected exercise.
#[component]
pub fn RiscvLab(props: LabProps) -> impl IntoView {
    let spec = match parse_spec(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let real = spec.profile == Profile::Linux;
    let data = spec.data.clone();
    let hint = props.task.hint.clone();
    // the learner's draft, or the starter if there is none
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
        let _ru = locales::guard(i18n::Locale::Ru);
        let raw = json!({
            "profile": "linux", "starter": "_start:\n", "data": "msg: .asciz \"x\"\n", "max_steps": 1000,
            "tests": [{ "check": { "kind": "run", "stdout": "x", "code": 0, "ok": "ok" } }],
        });
        let spec = parse_spec(&raw).expect("parses without a reference");
        assert_eq!((spec.profile, spec.reference.as_str(), spec.max_steps), (Profile::Linux, "", 1000));
    }

    #[test]
    fn broken_spec_is_reported_in_russian() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let err = parse_spec(&json!({ "profile": "mars" })).expect_err("there is no mars profile");
        assert!(err.starts_with("Неверное описание упражнения"), "{err}");
    }
}
