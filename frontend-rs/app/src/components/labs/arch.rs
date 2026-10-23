//! Лаборатория «Архитектура компьютера» (книга 14, главы 6–15): схемы из вентилей и блоков, процессор Мини-8 на
//! вентилях и ассемблер Мини-8. Расчёт и проверка — в крейте `archlab`, общем с бэкендом; здесь — интерфейс.
//!
//! [`ArchLab`] разбирает сценарий упражнения (`spec`), загружает данные лаборатории (сценарии других глав и решённое
//! учеником — из них собираются блоки, см. `data.rs`) и открывает нужный интерфейс: `CircuitLab` для схем,
//! `AsmLab` для программ.

use std::sync::Arc;

use archlab::Spec;
use leptos::prelude::*;

use super::LabProps;
use crate::hooks::Load;

mod asm_lab;
mod block_board;
mod block_logic;
mod check;
mod circuit_lab;
mod clock;
mod common;
mod cpu;
mod data;
mod gate_board;
mod gate_logic;
mod inspector;
mod model;
mod solution;
mod view;

/// Разбор сценария упражнения, который прислал сервер (без эталонного решения).
fn parse_spec(value: &serde_json::Value) -> Result<Spec, String> {
    serde_json::from_value(value.clone()).map_err(|e| format!("Сценарий упражнения не разобран: {e}"))
}

/// Лаборатория выбранного упражнения.
#[component]
pub fn ArchLab(props: LabProps) -> impl IntoView {
    let spec = match parse_spec(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let data = data::use_arch_data();
    let spec = StoredValue::new(Arc::new(spec));
    let props = StoredValue::new(props);
    (move || match data.get() {
        Load::Loading => view! { <p class="empty">"Загрузка лаборатории…"</p> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Ready(d) => {
            let props = props.get_value();
            match &*spec.get_value() {
                Spec::Circuit(c) => view! { <circuit_lab::CircuitLab props=props spec=Arc::new(c.clone()) data=d /> }.into_any(),
                Spec::Asm(a) => view! { <asm_lab::AsmLab props=props spec=Arc::new(a.clone()) /> }.into_any(),
            }
        }
    })
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn spec_without_the_reference_solution_is_readable() {
        // сервер убирает `solution` из сценария для клиента: движок обязан читать и такой
        let circuit = json!({
            "kind": "circuit", "section": "simple-circuits", "mode": "table", "build": "gates", "inputs": ["A"],
            "outputs": ["Y"], "target": [[1], [0]], "allowed": ["NOT"], "formula": "Y = НЕ A", "success": "ок"
        });
        match parse_spec(&circuit) {
            Ok(Spec::Circuit(c)) => assert!(c.solution.is_none() && c.outputs == ["Y"]),
            other => panic!("{other:?}"),
        }
        let asm = json!({
            "kind": "asm", "starter": "hlt", "disk": "00ff", "expected": "00ff",
            "regions": [{"name": "вход", "from": 0, "length": 2}]
        });
        match parse_spec(&asm) {
            Ok(Spec::Asm(a)) => assert!(a.solution.is_empty() && a.disk.0 == [0, 255]),
            other => panic!("{other:?}"),
        }
        assert!(parse_spec(&json!({"kind": "net"})).is_err());
    }
}
