//! "Computer Architecture" lab (book 14, chapters 6–15): circuits of gates and blocks, the Mini-8 processor built from
//! gates, and the Mini-8 assembler. Computation and verification are in the `archlab` crate shared with the backend; this is the interface.
//!
//! [`ArchLab`] parses the exercise scenario (`spec`), loads the lab data (scenarios of other chapters and what the student
//! has solved — blocks are built from them, see `data.rs`) and opens the right interface: `CircuitLab` for circuits,
//! `AsmLab` for programs.

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

/// Parsing of the exercise scenario sent by the server (without the reference solution).
fn parse_spec(value: &serde_json::Value) -> Result<Spec, String> {
    serde_json::from_value(value.clone()).map_err(|e| i18n::trf!("Exercise scenario could not be parsed: {0}", e))
}

/// Lab of the selected exercise.
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
        Load::Loading => view! { <p class="empty">{i18n::tr("Loading the lab…")}</p> }.into_any(),
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
        let _ru = locales::guard(i18n::Locale::Ru);
        // the server removes `solution` from the scenario for the client: the engine must be able to read such a one too
        let circuit = json!({
            "kind": "circuit", "section": "simple-circuits", "mode": "table", "build": "gates", "inputs": ["A"],
            "outputs": ["Y"], "target": [[1], [0]], "allowed": ["NOT"], "formula": "Y = NOT A", "success": "ok"
        });
        match parse_spec(&circuit) {
            Ok(Spec::Circuit(c)) => assert!(c.solution.is_none() && c.outputs == ["Y"]),
            other => panic!("{other:?}"),
        }
        let asm = json!({
            "kind": "asm", "starter": "hlt", "disk": "00ff", "expected": "00ff",
            "regions": [{"name": "input", "from": 0, "length": 2}]
        });
        match parse_spec(&asm) {
            Ok(Spec::Asm(a)) => assert!(a.solution.is_empty() && a.disk.0 == [0, 255]),
            other => panic!("{other:?}"),
        }
        assert!(parse_spec(&json!({"kind": "net"})).is_err());
    }
}
