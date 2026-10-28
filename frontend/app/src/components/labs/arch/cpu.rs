//! "Processor internals": the Mini-8 processor circuit made of blocks, which can be descended into down to individual
//! gates. Wire values are live, for the current clock (`CpuInspector.tsx`).

use std::sync::{Arc, OnceLock};

use archlab::cpu8::{cpu8_blocks, cpu_expansion};
use leptos::prelude::*;

use super::{
    asm_lab::Sim,
    common::{Level, Lib, Scope},
    inspector::Inspector,
};

/// Top-level processor block.
const CPU_BLOCK: &str = "c8-cpu";

/// Processor block library (view only); built once.
fn cpu_library() -> Lib {
    static LIB: OnceLock<Lib> = OnceLock::new();
    LIB.get_or_init(|| Lib(Arc::new(cpu8_blocks().library()))).clone()
}

/// Top view level: the processor circuit with values from the gate-level machine; `None` means there is no block catalog.
fn top_level(scope: Scope) -> Option<Level> {
    let cpu = cpu8_blocks().get(CPU_BLOCK)?;
    let expansion = cpu_expansion()?;
    Some(Level {
        title: cpu.def.title.clone(),
        iface: Arc::new(cpu.def.iface.clone()),
        solution: Arc::new(cpu.solution.clone()),
        expansion: Arc::new(expansion.clone()),
        scope,
    })
}

/// Processor internals view; node values are read from the gate-level machine `sim`.
#[component]
pub fn CpuInspector(sim: RwSignal<Option<Sim>>) -> impl IntoView {
    let path = RwSignal::new(Vec::<String>::new());
    let scope: Scope = Arc::new(move |node: &str| {
        sim.with(|s| match s {
            Some(Sim::Gates(m)) => m.sim.get(node),
            _ => None,
        })
    });
    match top_level(scope) {
        Some(level) => view! { <Inspector top=Signal::stored(level) library=Signal::stored(cpu_library()) path=path cpu=true /> }.into_any(),
        None => view! { <p class="lab-muted">{i18n::tr("The processor block catalog is unavailable.")}</p> }.into_any(),
    }
}
