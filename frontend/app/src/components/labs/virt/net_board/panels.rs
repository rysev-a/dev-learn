//! Panels of the Linux network lab around the board: the story, the inspector of the selected object, the path of a message, the tree of namespaces
//! and interfaces and the goals. All of them read the shared [`Lab`] state.

use leptos::prelude::*;
use virtlab::net_board::{param_specs, Op, Param, ParamSpec, ParamTy, Trace, MAX_NAME};

use super::{
    lab::Lab,
    logic::{self, TreeItem},
};

fn chip_view(chip: Option<logic::Chip>) -> impl IntoView {
    chip.map(|c| view! { <span class=format!("vl-chip {}", c.class)>{c.text}</span> })
}

// --- story ------------------------------------------------------------------------------------

/// What is going on, what to achieve, and the hint.
#[component]
pub fn Story(lab: Lab) -> impl IntoView {
    let sc = lab.scenario();
    let (story, goal, hint) = (sc.story.clone(), sc.goal.clone(), sc.hint.clone());
    view! {
        <div class="vl-card vl-net-story">
            <p class="vl-goal">{i18n::tr_dyn(&story)}</p>
            <p class="vl-goal">
                <span class="s-label">{i18n::tr("goal")}</span>
                " "
                {i18n::tr_dyn(&goal)}
            </p>
            <div class="vl-actions">
                <button type="button" class="quiz-btn ghost" aria-pressed=move || lab.hint_open.get().to_string() on:click=move |_| lab.hint_open.update(|v| *v = !*v)>
                    {i18n::tr("Hint")}
                </button>
            </div>
            {move || lab.hint_open.get().then(|| view! { <p class="vl-hint">{i18n::tr_dyn(&hint)}</p> })}
        </div>
    }
}

// --- inspector -------------------------------------------------------------------------------

/// The selected object or link: its parameters and the derived state with the reasons.
#[component]
pub fn Inspector(lab: Lab) -> impl IntoView {
    view! {
        <div class="vl-card vl-net-inspector">
            <span class="s-label">{i18n::tr("selected")}</span>
            {move || match (lab.selected.get(), lab.sel_edge.get()) {
                (Some(id), _) => view! { <NodeInspector lab=lab id=id /> }.into_any(),
                (None, Some(edge)) => {
                    let (rel, names) = lab.board.with(|t| {
                        let name = |id: &str| t.node(id).map(|n| n.name.clone()).unwrap_or_default();
                        (logic::edge_rel(t, &edge).map(|r| r.label()).unwrap_or_default(), (name(&edge.from), name(&edge.to)))
                    });
                    view! {
                        <p class="vl-net-kind">{i18n::tr("Link")}</p>
                        <p>{i18n::trf!("“{0}” → “{1}”: {2}", names.0, names.1, rel)}</p>
                        <p class="vl-muted">{i18n::tr("Delete removes the link and every link that depends on it.")}</p>
                    }
                    .into_any()
                }
                _ => view! { <p class="vl-muted">{i18n::tr("Select an object or a link on the board to see its state and change it.")}</p> }.into_any(),
            }}
        </div>
    }
}

#[component]
fn NodeInspector(lab: Lab, id: String) -> impl IntoView {
    let Some(first) = lab.board.with_untracked(|t| t.node(&id).cloned()) else { return ().into_any() };
    let kind = first.kind;
    let node = {
        let id = id.clone();
        Memo::new(move |_| lab.board.with(|t| t.node(&id).cloned()))
    };
    let explain = {
        let id = id.clone();
        Memo::new(move |_| lab.board.with(|t| lab.eval.with(|ev| logic::explain(t, ev, &id))))
    };
    let rename_id = id.clone();
    let params = param_specs(kind).into_iter().map(|spec| view! { <ParamField lab=lab id=id.clone() node=node spec=spec /> }).collect_view();
    view! {
        <p class="vl-net-kind">{kind.label()}</p>
        <label class="vl-net-field">
            <span>{i18n::tr("Name")}</span>
            <input type="text" maxlength=MAX_NAME.to_string() value=first.name on:input=move |e| lab.rename(&rename_id, &event_target_value(&e)) />
        </label>
        {params}
        <p class="vl-net-state">{move || chip_view(explain.get().info.chip)}</p>
        <ul class="vl-net-why">{move || explain.get().lines.into_iter().map(|l| view! { <li>{l}</li> }).collect_view()}</ul>
    }
    .into_any()
}

/// One parameter of the selected object, drawn from the model's table: a select for a choice, a checkbox for a switch.
#[component]
fn ParamField(lab: Lab, id: String, node: Memo<Option<virtlab::net_board::Node>>, spec: ParamSpec) -> impl IntoView {
    let key = spec.key;
    let label = spec.label;
    let default = spec.default_text();
    match spec.ty {
        ParamTy::Select(options) => {
            let options = options
                .into_iter()
                .map(|o| view! { <option value=o.value prop:selected=move || node.get().is_some_and(|n| n.param_text(key) == o.value)>{o.label}</option> })
                .collect_view();
            view! {
                <label class="vl-net-field" data-param=key data-default=default>
                    <span>{label}</span>
                    <select on:change=move |e| lab.set_param(&id, key, Param::Str(event_target_value(&e)))>{options}</select>
                </label>
            }
            .into_any()
        }
        ParamTy::Bool => view! {
            <label class="vl-net-field row" data-param=key data-default=default>
                <input type="checkbox" prop:checked=move || node.get().is_some_and(|n| n.param_text(key) == "true") on:change=move |e| lab.set_param(&id, key, Param::Bool(event_target_checked(&e))) />
                <span>{label}</span>
            </label>
        }
        .into_any(),
    }
}

// --- the path of a message -------------------------------------------------------------------

/// A message between two hosts (or into a published port) and the hops of its path.
#[component]
pub fn PathPanel(lab: Lab) -> impl IntoView {
    let hosts = Memo::new(move |_| lab.board.with(logic::hosts));
    let publications = Memo::new(move |_| lab.board.with(logic::publications));
    let from = RwSignal::new(None::<String>);
    let to = RwSignal::new(None::<String>);
    // the choice survives while the object is on the board; otherwise the first host and the next one
    let pick_from = Memo::new(move |_| {
        let list = hosts.get();
        from.get().filter(|f| list.iter().any(|h| &h.0 == f)).or_else(|| list.first().map(|h| h.0.clone()))
    });
    let pick_to = Memo::new(move |_| {
        let list = hosts.get();
        let first = pick_from.get();
        to.get().filter(|t| list.iter().any(|h| &h.0 == t)).or_else(|| list.iter().find(|h| Some(&h.0) != first.as_ref()).map(|h| h.0.clone()))
    });
    let ping = move || match (pick_from.get_untracked(), pick_to.get_untracked()) {
        (Some(from), Some(to)) if from != to => lab.run_op(Op::Ping { from, to }),
        _ => {}
    };
    let can_ping = Memo::new(move |_| matches!((pick_from.get(), pick_to.get()), (Some(a), Some(b)) if a != b));
    let select = move |role: &'static str, label: &'static str, value: Memo<Option<String>>, set: RwSignal<Option<String>>| {
        view! {
            <label class="vl-net-field">
                <span>{label}</span>
                <select data-role=role on:change=move |e| set.set(Some(event_target_value(&e)))>
                    {move || {
                        let chosen = value.get();
                        hosts
                            .get()
                            .into_iter()
                            .map(|(id, name)| {
                                let selected = chosen.as_deref() == Some(id.as_str());
                                view! { <option value=id selected=selected>{name}</option> }
                            })
                            .collect_view()
                    }}
                </select>
            </label>
        }
    };
    view! {
        <div class="vl-card vl-net-path">
            <span class="s-label">{i18n::tr("message path")}</span>
            {move || {
                if hosts.with(|h| h.len() < 2) {
                    view! { <p class="vl-muted">{i18n::tr("Add two hosts (namespaces, VMs or the outside network) to follow a message between them.")}</p> }.into_any()
                } else {
                    view! {
                        <div class="vl-net-ops">
                            {select("from", i18n::tr("From"), pick_from, from)}
                            {select("to", i18n::tr("To"), pick_to, to)}
                            <button
                                type="button"
                                class="quiz-btn ghost vl-net-op"
                                data-op="ping"
                                disabled=move || !can_ping.get()
                                class:on=move || lab.op.with(|o| matches!(o, Some(Op::Ping { .. })))
                                on:click=move |_| ping()
                            >
                                {i18n::tr("Ping")}
                            </button>
                        </div>
                    }
                    .into_any()
                }
            }}
            <div class="vl-net-ops">
                {move || {
                    publications
                        .get()
                        .into_iter()
                        .map(|op| {
                            let current = op.clone();
                            let label = lab.board.with(|t| logic::publish_label(t, &op));
                            view! {
                                <button
                                    type="button"
                                    class="quiz-btn ghost vl-net-op"
                                    data-op=logic::op_name(&op)
                                    class:on=move || lab.op.with(|o| o.as_ref() == Some(&current))
                                    on:click=move |_| lab.run_op(op.clone())
                                >
                                    {label}
                                </button>
                            }
                        })
                        .collect_view()
                }}
            </div>
            {move || lab.trace.get().map(|tr| view! { <Hops lab=lab trace=tr /> })}
        </div>
    }
}

#[component]
fn Hops(lab: Lab, trace: Trace) -> impl IntoView {
    let ok = trace.ok;
    let rows = trace
        .hops
        .into_iter()
        .enumerate()
        .map(|(i, h)| {
            view! {
                <li
                    class:ok=h.ok
                    class:bad=!h.ok
                    class:cur=move || lab.active.get() == Some(i)
                    class:later=move || lab.active.get().is_some_and(|a| i > a)
                    role="button"
                    tabindex="0"
                    on:click=move |_| lab.show_hop(i)
                    on:keydown=move |e| {
                        if e.key() == "Enter" || e.key() == " " {
                            e.prevent_default();
                            lab.show_hop(i);
                        }
                    }
                >
                    <span class="vl-gm">{if h.ok { "✓" } else { "✗" }}</span>
                    <span>{h.text}</span>
                </li>
            }
        })
        .collect_view();
    view! {
        <div class="vl-net-hophead">
            <p class=if ok { "vl-yes" } else { "vl-no" }>
                {if ok { i18n::tr("The message gets through.") } else { i18n::tr("The message does not get through.") }}
            </p>
            <button type="button" class="quiz-btn ghost vl-net-play" on:click=move |_| if lab.playing.get_untracked() { lab.stop() } else { lab.play() }>
                {move || if lab.playing.get() { i18n::tr("Stop") } else { i18n::tr("Play") }}
            </button>
        </div>
        <ul class="vl-net-hops">{rows}</ul>
    }
}

// --- tree ------------------------------------------------------------------------------------

/// The tree derived from the links: namespace › its interfaces, the ports of a bridge, the slaves of a bond, the VLAN interfaces and the rules.
#[component]
pub fn TreePanel(lab: Lab) -> impl IntoView {
    let items = Memo::new(move |_| lab.board.with(|t| lab.eval.with(|ev| logic::tree(t, ev))));
    view! {
        <div class="vl-card">
            <span class="s-label">{i18n::tr("namespaces and interfaces")}</span>
            {move || items.with(Vec::is_empty).then(|| view! { <p class="vl-muted">{i18n::tr("The board is empty: add a namespace first.")}</p> })}
            <ul class="vl-net-tree">
                {move || {
                    items
                        .get()
                        .into_iter()
                        .map(|item| match item {
                            TreeItem::Heading(text) => view! { <li class="vl-net-tree-head">{text}</li> }.into_any(),
                            TreeItem::Node { depth, id, kind, name, info } => {
                                let (mine, pick, data) = (id.clone(), id.clone(), id);
                                view! {
                                    <li
                                        class=format!("vl-net-tree-row {}", kind.as_str())
                                        class:on=move || lab.sel.with(|s| s.as_deref() == Some(mine.as_str()))
                                        data-id=data
                                        style=format!("padding-left: {}px", 8 + depth * 16)
                                        on:click=move |_| lab.select_node(Some(pick.clone()))
                                    >
                                        <i class="vl-net-dotk"></i>
                                        <span class="vl-net-nm">{name}</span>
                                        <span class="vl-net-kd">{kind.label()}</span>
                                        {chip_view(info.chip)}
                                    </li>
                                }
                                .into_any()
                            }
                        })
                        .collect_view()
                }}
            </ul>
        </div>
    }
}

// --- goals -----------------------------------------------------------------------------------

/// Goals of the scenario with marks, and the verdict on the board.
#[component]
pub fn GoalsPanel(lab: Lab) -> impl IntoView {
    view! {
        <div class="vl-card">
            <span class="s-label">{i18n::tr("goals")}</span>
            <ul class="vl-goals">
                {move || {
                    lab.results
                        .get()
                        .into_iter()
                        .map(|g| {
                            view! {
                                <li class:ok=g.ok>
                                    <span class="vl-gm">{if g.ok { "✓" } else { "○" }}</span>
                                    <span>{i18n::tr_dyn(&g.text)}</span>
                                </li>
                            }
                        })
                        .collect_view()
                }}
            </ul>
            {move || lab.invalid.get().map(|t| view! { <p class="vl-no vl-net-invalid">{t}</p> })}
            {move || lab.solved_now.get().then(|| view! { <p class="vl-yes vl-final">{i18n::tr("✓ Scenario goal reached")}</p> })}
        </div>
    }
}
