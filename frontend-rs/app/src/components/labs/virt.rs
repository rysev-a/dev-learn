//! Лаборатория «виртуализация»: шесть симуляторов книги 17. Модели, цели и перепроверка решения — в крейте `virtlab`
//! (общем с сервером), здесь только интерфейс: по описанию упражнения (`Spec`) выбирается симулятор, а когда достигнуты
//! все цели, решение (JSON `{id цели: данные}`) один раз уходит на сервер через `LabProps::report`.
//!
//! Для симуляторов с историей действий (`hv`, `virtq`, `qcow2`) в данных цели лежит ещё и `trace` — записанные действия
//! ученика: по ним сервер воспроизводит прогон и подтверждает достижение цели (`virtlab::verify`).

use leptos::prelude::*;
use serde_json::Value;
use virtlab::Spec;

use super::LabProps;

mod common;
mod ept;
mod hv;
mod migration;
mod numa;
mod qcow2;
mod virtq;

use common::Goals;

/// Описание упражнения: из `spec` задачи, а если оно пусто — встроенное по идентификатору (`virt-sim-…`).
fn parse_spec(id: &str, raw: &Value) -> Result<Spec, String> {
    let empty = raw.is_null() || raw.as_object().is_some_and(|o| o.is_empty());
    if empty {
        return virtlab::builtin(id).ok_or_else(|| format!("Неизвестное упражнение «{id}»"));
    }
    let spec: Spec = serde_json::from_value(raw.clone()).map_err(|e| format!("Неверное описание упражнения: {e}"))?;
    spec.validate().map_err(|e| format!("Неверное описание упражнения: {e}"))?;
    Ok(spec)
}

/// Симулятор выбранного упражнения.
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
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::*;

    #[test]
    fn empty_spec_falls_back_to_builtin() {
        for id in virtlab::LAB_IDS {
            assert!(parse_spec(id, &Value::Null).is_ok(), "{id}");
            assert!(parse_spec(id, &json!({})).is_ok(), "{id}");
        }
        assert!(parse_spec("virt-sim-none", &Value::Null).is_err());
    }

    #[test]
    fn spec_from_json_roundtrip() {
        for id in virtlab::LAB_IDS {
            let Some(spec) = virtlab::builtin(id) else { panic!("{id}") };
            let raw = serde_json::to_value(&spec).expect("сериализация");
            assert_eq!(parse_spec(id, &raw).expect("разбор"), spec, "{id}");
        }
    }

    #[test]
    fn broken_spec_is_reported() {
        let err = parse_spec("virt-sim-hv", &json!({"sim": "hv", "programs": 5})).expect_err("ошибка");
        assert!(err.starts_with("Неверное описание"), "{err}");
    }
}
