//! «Устройство процессора»: схема процессора Мини-8 из блоков, в которую можно спускаться вплоть до отдельных
//! вентилей. Значения на проводах — живые, по текущему такту (`CpuInspector.tsx`).

use std::sync::{Arc, OnceLock};

use archlab::cpu8::{cpu8_blocks, cpu_expansion};
use leptos::prelude::*;

use super::{
    asm_lab::Sim,
    common::{Level, Lib, Scope},
    inspector::Inspector,
};

/// Блок процессора верхнего уровня.
const CPU_BLOCK: &str = "c8-cpu";

/// Библиотека блоков процессора (только просмотр); собирается один раз.
fn cpu_library() -> Lib {
    static LIB: OnceLock<Lib> = OnceLock::new();
    LIB.get_or_init(|| Lib(Arc::new(cpu8_blocks().library()))).clone()
}

/// Верхний уровень просмотра: схема процессора со значениями из машины на вентилях; `None` — каталога блоков нет.
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

/// Просмотр устройства процессора; значения узлов читает у машины на вентилях `sim`.
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
        None => view! { <p class="lab-muted">"Каталог блоков процессора недоступен."</p> }.into_any(),
    }
}
