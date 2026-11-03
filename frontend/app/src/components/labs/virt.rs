//! "Virtualization" lab: ten simulators of book 17. The models, goals and solution re-check live in the `virtlab` crate
//! (shared with the server); here is only the interface: a simulator is chosen from the exercise description (`Spec`), and once
//! all goals are reached, the solution (JSON `{goal id: data}`) is sent to the server once through `LabProps::report`.
//!
//! For simulators with an action history (`hv`, `virtq`, `qcow2`, `ovirt_dc`) the goal data also holds a `trace` — the student's recorded actions:
//! the server replays the run from it and confirms the goal (`virtlab::verify`).

use leptos::prelude::*;
use serde_json::Value;
use virtlab::Spec;

use super::LabProps;

mod common;
mod ept;
mod hv;
mod lvm_board;
mod migration;
mod net_board;
mod numa;
mod ovirt_dc;
mod ovirt_fence;
mod ovirt_sched;
mod ovirt_topo;
pub use ovirt_topo::TaskBoards;
mod qcow2;
mod virtq;

use common::Goals;

/// Exercise description: from the task's `spec`, and if it is empty — the built-in one by identifier (`virt-sim-…`).
fn parse_spec(id: &str, raw: &Value) -> Result<Spec, String> {
    let empty = raw.is_null() || raw.as_object().is_some_and(|o| o.is_empty());
    if empty {
        return virtlab::builtin(id).ok_or_else(|| i18n::trf!("Unknown exercise “{0}”", id));
    }
    let spec: Spec = serde_json::from_value(raw.clone()).map_err(|e| i18n::trf!("Invalid exercise description: {0}", e))?;
    spec.validate().map_err(|e| i18n::trf!("Invalid exercise description: {0}", e))?;
    Ok(spec)
}

/// Simulator of the selected exercise.
#[component]
pub fn VirtLab(props: LabProps) -> impl IntoView {
    let spec = match parse_spec(&props.task.id, &props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let ids = spec.goals().into_iter().map(|g| g.id).collect();
    let goals = Goals::new(ids, props.solved, props.report);
    match spec {
        Spec::Hv { programs } => view! { <hv::HvLab programs=programs goals=goals /> }.into_any(),
        Spec::Ept { workloads, goals: targets } => {
            view! { <ept::EptLab workloads=workloads targets=targets goals=goals /> }.into_any()
        }
        Spec::Virtq { size, goals: targets } => {
            view! { <virtq::VirtqLab size=size targets=targets goals=goals /> }.into_any()
        }
        Spec::Numa { nodes, scenarios } => {
            view! { <numa::NumaLab nodes=nodes scenarios=scenarios goals=goals /> }.into_any()
        }
        Spec::Qcow2 { clusters, base, goals: targets } => {
            view! { <qcow2::Qcow2Lab clusters=clusters base=base targets=targets goals=goals /> }.into_any()
        }
        Spec::Migration { scenarios } => view! { <migration::MigrationLab scenarios=scenarios goals=goals /> }.into_any(),
        Spec::OvirtDc { goals: targets } => view! { <ovirt_dc::OvirtDcLab targets=targets goals=goals /> }.into_any(),
        Spec::OvirtFence { scenarios } => view! { <ovirt_fence::OvirtFenceLab scenarios=scenarios goals=goals /> }.into_any(),
        Spec::OvirtSched { scenarios } => view! { <ovirt_sched::OvirtSchedLab scenarios=scenarios goals=goals /> }.into_any(),
        // the reference boards are never sent to the client; the draft holds the student's boards, one per scenario
        Spec::OvirtTopo { scenarios, .. } => {
            view! { <ovirt_topo::OvirtTopoLab scenarios=scenarios goals=goals draft=props.draft on_draft=props.on_draft /> }.into_any()
        }
        Spec::LvmBoard { scenarios, .. } => {
            view! { <lvm_board::LvmBoardLab scenarios=scenarios goals=goals draft=props.draft on_draft=props.on_draft /> }.into_any()
        }
        Spec::NetBoard { scenarios, .. } => {
            view! { <net_board::NetBoardLab scenarios=scenarios goals=goals draft=props.draft on_draft=props.on_draft /> }.into_any()
        }
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::*;

    #[test]
    fn empty_spec_falls_back_to_builtin() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for id in virtlab::lab_ids() {
            assert!(parse_spec(id, &Value::Null).is_ok(), "{id}");
            assert!(parse_spec(id, &json!({})).is_ok(), "{id}");
        }
        assert!(parse_spec("virt-sim-none", &Value::Null).is_err());
    }

    #[test]
    fn spec_from_json_roundtrip() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for id in virtlab::lab_ids() {
            let Some(spec) = virtlab::builtin(id) else { panic!("{id}") };
            let raw = serde_json::to_value(&spec).expect("serialization");
            assert_eq!(parse_spec(id, &raw).expect("parse"), spec, "{id}");
        }
    }

    #[test]
    fn broken_spec_is_reported() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let err = parse_spec("virt-sim-hv", &json!({"sim": "hv", "programs": 5})).expect_err("error");
        assert!(err.starts_with("Неверное описание"), "{err}");
    }
}
