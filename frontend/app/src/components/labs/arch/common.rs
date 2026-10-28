//! Shared types and small components of the "Computer Architecture" lab: node values, wrappers over engine data
//! (so they can be held in a `Memo`), the gate outline and the result banner.

use std::sync::Arc;

use archlab::{
    blocks::{BlockDef, BlockInterface, BlockLibrary, Expansion, Solution},
    layout::{gate_body_path, gate_bubble_cx, gate_extra_arc},
    model::{GateType, NodeValue, GATE_W},
};
use leptos::prelude::*;

use crate::components::labs::board_view::{BoardConfig, Bounds};

/// Pan and zoom of the lab boards: 30–300 %, integer pan; elements stay within the 8000×6000 "world" around the origin.
pub const BOARD: BoardConfig = BoardConfig { items: Bounds::new((-4000.0, 4000.0), (-3000.0, 3000.0)), ..BoardConfig::DEFAULT };

/// Circuit node value by its name (reading subscribes the caller to value changes).
pub type Scope = Arc<dyn Fn(&str) -> NodeValue + Send + Sync>;

/// Block library; compared by pointer: a new library is a new value.
#[derive(Clone)]
pub struct Lib(pub Arc<BlockLibrary>);

impl PartialEq for Lib {
    fn eq(&self, other: &Self) -> bool {
        Arc::ptr_eq(&self.0, &other.0)
    }
}

/// Expanded circuit of blocks; compared by pointer.
#[derive(Clone)]
pub struct Exp(pub Arc<Expansion>);

impl PartialEq for Exp {
    fn eq(&self, other: &Self) -> bool {
        Arc::ptr_eq(&self.0, &other.0)
    }
}

/// Class by signal value: `v1`, `v0` or `vx` ("?").
pub fn node_class(v: NodeValue) -> &'static str {
    match v {
        Some(1) => "v1",
        Some(_) => "v0",
        None => "vx",
    }
}

/// Signal value as text: `0`, `1` or `?`.
pub fn node_text(v: NodeValue) -> String {
    v.map_or_else(|| "?".to_string(), |b| b.to_string())
}

/// Values inside a block instance from the parent circuit's values: its inputs come from the parent, and the nodes
/// inside the block live in the flat circuit with the prefix `instance__`. The owning variant is `archlab::blocks::child_scope`.
pub fn child_scope(parent_scope: Scope, parent: Arc<Expansion>, inst: String, def: Arc<BlockDef>) -> Scope {
    Arc::new(move |node: &str| {
        let iface = &def.iface;
        let source = if iface.inputs.iter().any(|n| n == node) {
            parent.in_source(&inst, node)
        } else if iface.outputs.iter().any(|n| n == node) {
            parent.out_source(&inst, node)
        } else {
            Some(format!("{inst}__{node}"))
        };
        source.and_then(|s| parent_scope(&s))
    })
}

/// One view level: the exercise circuit or a block that was "looked into".
#[derive(Clone)]
pub struct Level {
    pub title: String,
    pub iface: Arc<BlockInterface>,
    pub solution: Arc<Solution>,
    pub expansion: Arc<Expansion>,
    pub scope: Scope,
}

impl Level {
    /// Level of the nested block `inst` (by this level's expanded circuit).
    pub fn descend(&self, inst: &str, with_id: bool) -> Option<Level> {
        let sub = self.expansion.sub(inst)?;
        let title = if with_id { format!("{} ({inst})", sub.def.title) } else { sub.def.title.clone() };
        Some(Level {
            title,
            iface: Arc::new(sub.def.iface.clone()),
            solution: sub.solution.clone(),
            expansion: Arc::new(sub.expansion.clone()),
            scope: child_scope(self.scope.clone(), self.expansion.clone(), inst.to_string(), sub.def.clone()),
        })
    }
}

/// Descent levels along a path of instance ids: from the top to the deepest reachable one.
pub fn levels_along(top: Level, path: &[String], with_id: bool) -> Vec<Level> {
    let mut out = vec![top];
    for id in path {
        let next = out.last().and_then(|cur| cur.descend(id, with_id));
        match next {
            Some(l) => out.push(l),
            None => break,
        }
    }
    out
}

/// Gate outline: body, extra arc (XOR), inversion bubble and (by default) the type label.
#[component]
pub fn GateShape(ty: GateType, #[prop(default = true)] label: bool) -> impl IntoView {
    let arc = gate_extra_arc(ty);
    let bubble = gate_bubble_cx(ty);
    let is_not = ty == GateType::Not;
    view! {
        <path class="gate-body" d=gate_body_path(ty)></path>
        {arc.map(|d| view! { <path class="gate-extra" d=d></path> })}
        {bubble.map(|cx| view! { <circle class="gate-bubble" cx=cx cy="24" r="5"></circle> })}
        {label.then(|| view! {
            <text class=if is_not { "gate-label small" } else { "gate-label" } x=if is_not { 13.0 } else { GATE_W / 2.0 } y="29">{ty.name()}</text>
        })}
    }
}

/// Check result in the app's style: a compact banner — icon, title, explanation, "next" button.
#[component]
pub fn ResultAlert(
    #[prop(default = true)] ok: bool,
    #[prop(into)] title: ViewFn,
    #[prop(optional, into)] text: String,
    #[prop(default = None)] on_next: Option<Callback<()>>,
) -> impl IntoView {
    view! {
        <div class=if ok { "lab-alert ok" } else { "lab-alert bad" } role="status">
            <span class="lab-alert-ico" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                    {if ok { view! { <path d="M20 6 9 17l-5-5"></path> }.into_any() } else { view! { <path d="M18 6 6 18M6 6l12 12"></path> }.into_any() }}
                </svg>
            </span>
            <div class="lab-alert-body">
                <p class="lab-alert-title">{title.run()}</p>
                {(!text.is_empty()).then(|| view! { <p class="lab-alert-text">{text}</p> })}
            </div>
            {on_next.map(|next| view! {
                <button type="button" class="lab-alert-next" on:click=move |_| next.run(())>
                    {i18n::tr("Next")}
                    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
                </button>
            })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn signal_value_classes_and_text() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!((node_class(Some(1)), node_class(Some(0)), node_class(None)), ("v1", "v0", "vx"));
        assert_eq!((node_text(Some(1)), node_text(Some(0)), node_text(None)), ("1".to_string(), "0".to_string(), "?".to_string()));
    }
}
