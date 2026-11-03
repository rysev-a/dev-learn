//! Panels of the LVM lab around the board: the story, the inspector of the selected object, "if a disk fails", the summary, the tree of disks
//! and volumes and the goals. All of them read the shared [`Lab`] state.

use leptos::prelude::*;
use virtlab::lvm_board::{param_specs, Param, ParamSpec, ParamTy, MAX_NAME};

use super::{
    lab::Lab,
    logic::{self, TreeItem},
};

fn chip_view(chip: Option<logic::Chip>) -> impl IntoView {
    chip.map(|c| view! { <span class=format!("vl-chip {}", c.class)>{c.text}</span> })
}

// --- story ------------------------------------------------------------------------------------

/// What is going on, what to achieve, what the load is, and the hint.
#[component]
pub fn Story(lab: Lab) -> impl IntoView {
    let sc = lab.scenario();
    let (story, goal, hint) = (sc.story.clone(), sc.goal.clone(), sc.hint.clone());
    let (changed, written) = (sc.workload.changed_gib, sc.workload.written_gib);
    view! {
        <div class="vl-card vl-lvm-story">
            <p class="vl-goal">{i18n::tr_dyn(&story)}</p>
            <p class="vl-goal">
                <span class="s-label">{i18n::tr("goal")}</span>
                " "
                {i18n::tr_dyn(&goal)}
            </p>
            {(changed > 0 || written > 0).then(|| view! {
                <p class="vl-goal vl-lvm-workload">
                    <span class="s-label">{i18n::tr("load")}</span>
                    " "
                    {(changed > 0).then(|| i18n::trf!("{0} GiB change in a volume while it has a snapshot.", changed))}
                    " "
                    {(written > 0).then(|| i18n::trf!("{0} GiB are written into the thin volumes.", written))}
                </p>
            })}
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
        <div class="vl-card vl-lvm-inspector">
            <span class="s-label">{i18n::tr("selected")}</span>
            {move || match (lab.selected.get(), lab.sel_edge.get()) {
                (Some(id), _) => view! { <NodeInspector lab=lab id=id /> }.into_any(),
                (None, Some(edge)) => {
                    let (rel, names) = lab.board.with(|t| {
                        let name = |id: &str| t.node(id).map(|n| n.name.clone()).unwrap_or_default();
                        (logic::edge_rel(t, &edge).map(|r| r.label()).unwrap_or_default(), (name(&edge.from), name(&edge.to)))
                    });
                    view! {
                        <p class="vl-lvm-kind">{i18n::tr("Link")}</p>
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
        <p class="vl-lvm-kind">{kind.label()}</p>
        <label class="vl-lvm-field">
            <span>{i18n::tr("Name")}</span>
            <input type="text" maxlength=MAX_NAME.to_string() value=first.name on:input=move |e| lab.rename(&rename_id, &event_target_value(&e)) />
        </label>
        {params}
        <p class="vl-lvm-state">{move || chip_view(explain.get().info.chip)}</p>
        <ul class="vl-lvm-why">{move || explain.get().lines.into_iter().map(|l| view! { <li>{l}</li> }).collect_view()}</ul>
    }
    .into_any()
}

/// One parameter of the selected object, drawn from the model's table: a select for a choice, a checkbox for a switch.
#[component]
fn ParamField(lab: Lab, id: String, node: Memo<Option<virtlab::lvm_board::Node>>, spec: ParamSpec) -> impl IntoView {
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
                <label class="vl-lvm-field" data-param=key data-default=default>
                    <span>{label}</span>
                    <select on:change=move |e| lab.set_param(&id, key, Param::Str(event_target_value(&e)))>{options}</select>
                </label>
            }
            .into_any()
        }
        ParamTy::Bool => view! {
            <label class="vl-lvm-field row" data-param=key data-default=default>
                <input type="checkbox" prop:checked=move || node.get().is_some_and(|n| n.param_text(key) == "true") on:change=move |e| lab.set_param(&id, key, Param::Bool(event_target_checked(&e))) />
                <span>{label}</span>
            </label>
        }
        .into_any(),
    }
}

// --- if a disk fails -------------------------------------------------------------------------

/// Choose a disk and see what its loss takes with it.
#[component]
pub fn LossPanel(lab: Lab) -> impl IntoView {
    let disks = Memo::new(move |_| lab.board.with(logic::disks));
    view! {
        <div class="vl-card vl-lvm-loss">
            <span class="s-label">{i18n::tr("if a disk fails")}</span>
            {move || {
                let list = disks.get();
                if list.is_empty() {
                    view! { <p class="vl-muted">{i18n::tr("Add a disk to see what its loss would take with it.")}</p> }.into_any()
                } else {
                    let chosen = lab.loss_disk.get().filter(|d| list.iter().any(|(id, _)| id == d)).unwrap_or_else(|| list[0].0.clone());
                    let options = list
                        .into_iter()
                        .map(|(id, name)| {
                            let value = id.clone();
                            view! { <option value=value selected=id == chosen>{name}</option> }
                        })
                        .collect_view();
                    view! {
                        <div class="vl-lvm-ops">
                            <select
                                aria-label=i18n::tr("Disk")
                                on:change=move |e| lab.choose_disk(Some(event_target_value(&e)))
                            >
                                {options}
                            </select>
                            <button
                                type="button"
                                class="quiz-btn ghost vl-lvm-op"
                                data-op="loss"
                                class:on=move || lab.loss_on.get()
                                on:click=move |_| {
                                    if lab.loss_disk.get_untracked().is_none() {
                                        lab.choose_disk(lab.board.with_untracked(|t| logic::disks(t).first().map(|d| d.0.clone())));
                                    }
                                    lab.show_loss();
                                }
                            >
                                {i18n::tr("Fail this disk")}
                            </button>
                        </div>
                    }
                    .into_any()
                }
            }}
            {move || lab.loss.get().map(|l| {
                let lost = !l.lost.is_empty();
                let rows = l
                    .lines
                    .into_iter()
                    .map(|line| {
                        view! {
                            <li class:ok=line.ok class:bad=!line.ok>
                                <span class="vl-gm">{if line.ok { "✓" } else { "✗" }}</span>
                                <span>{line.text}</span>
                            </li>
                        }
                    })
                    .collect_view();
                view! {
                    <p class=if lost { "vl-no" } else { "vl-yes" }>
                        {if lost { i18n::tr("Data is lost.") } else { i18n::tr("Nothing is lost.") }}
                    </p>
                    <ul class="vl-lvm-hops">{rows}</ul>
                }
            })}
        </div>
    }
}

// --- summary ---------------------------------------------------------------------------------

/// The numbers of the groups, the thin pools and the snapshots.
#[component]
pub fn SummaryPanel(lab: Lab) -> impl IntoView {
    let lines = Memo::new(move |_| lab.board.with(|t| lab.eval.with(|ev| logic::summary(t, ev))));
    view! {
        <div class="vl-card vl-lvm-summary">
            <span class="s-label">{i18n::tr("space")}</span>
            {move || lines.with(Vec::is_empty).then(|| view! { <p class="vl-muted">{i18n::tr("There is no volume group yet: make physical volumes of the disks and put them into one.")}</p> })}
            <ul class="vl-lvm-why">{move || lines.get().into_iter().map(|l| view! { <li>{l}</li> }).collect_view()}</ul>
        </div>
    }
}

// --- tree ------------------------------------------------------------------------------------

/// The tree derived from the links: volume group › physical volumes and disks, volumes and what stands on them, thin pools.
#[component]
pub fn TreePanel(lab: Lab) -> impl IntoView {
    let items = Memo::new(move |_| lab.board.with(|t| lab.eval.with(|ev| logic::tree(t, ev))));
    view! {
        <div class="vl-card">
            <span class="s-label">{i18n::tr("disks and volumes")}</span>
            {move || items.with(Vec::is_empty).then(|| view! { <p class="vl-muted">{i18n::tr("The board is empty: add a disk first.")}</p> })}
            <ul class="vl-lvm-tree">
                {move || {
                    items
                        .get()
                        .into_iter()
                        .map(|item| match item {
                            TreeItem::Heading(text) => view! { <li class="vl-lvm-tree-head">{text}</li> }.into_any(),
                            TreeItem::Node { depth, id, kind, name, info } => {
                                let (mine, pick, data) = (id.clone(), id.clone(), id);
                                view! {
                                    <li
                                        class=format!("vl-lvm-tree-row {}", kind.as_str())
                                        class:on=move || lab.sel.with(|s| s.as_deref() == Some(mine.as_str()))
                                        data-id=data
                                        style=format!("padding-left: {}px", 8 + depth * 16)
                                        on:click=move |_| lab.select_node(Some(pick.clone()))
                                    >
                                        <i class="vl-lvm-dotk"></i>
                                        <span class="vl-lvm-nm">{name}</span>
                                        <span class="vl-lvm-kd">{kind.label()}</span>
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
            {move || lab.invalid.get().map(|t| view! { <p class="vl-no vl-lvm-invalid">{t}</p> })}
            {move || lab.solved_now.get().then(|| view! { <p class="vl-yes vl-final">{i18n::tr("✓ Scenario goal reached")}</p> })}
        </div>
    }
}
