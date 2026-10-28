//! NUMA placement simulator (chapter 11): for each machine the processor and memory nodes are chosen. Node load
//! and the share of remote accesses are shown. A scenario's goal is checked by the "Accept placement" button; solved when all
//! scenarios are accepted. The goal data is the placement `{machine: {cpu, mem, vnuma}}`; the server evaluates it again.

use leptos::prelude::*;
use virtlab::numa::{self, Accept, Evaluation, Node, Place, Plan, Scenario};

use super::common::{data, pct, Goals, Tab};

/// Message under the table: red — rejection, green — accepted.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Msg {
    pub bad: bool,
    pub text: String,
}

/// Placement options: each node and "stretch" (the value is as in the data: a node number or `wide`).
pub fn place_options(nodes: usize) -> Vec<(String, String)> {
    let mut v: Vec<(String, String)> = (0..nodes).map(|i| (i.to_string(), i18n::trf!("node {0}", i))).collect();
    v.push(("wide".to_string(), i18n::tr("span").to_string()));
    v
}

fn parse_place(s: &str) -> Option<Place> {
    Place::try_from(s.to_string()).ok()
}

/// Outcome of the "Accept placement" button: a message and, if accepted, the goal data.
pub fn accept_outcome(nodes: &[Node], sc: &Scenario, plan: &Plan) -> (Msg, bool) {
    match numa::accept(nodes, sc, plan) {
        Ok(Accept::Over) => (
            Msg { bad: true, text: i18n::tr("The placement does not fit: some node lacks cores or memory.").to_string() },
            false,
        ),
        Ok(Accept::TooRemote { avg, max }) => (
            Msg { bad: true, text: i18n::trf!("Remote accesses {0} exceed the allowed {1}.", pct(avg), pct(max)) },
            false,
        ),
        Ok(Accept::Ok { avg }) => (Msg { bad: false, text: i18n::trf!("✓ Accepted: remote accesses {0}.", pct(avg)) }, true),
        Err(e) => (Msg { bad: true, text: e.to_string() }, false),
    }
}

/// Scale fill percentage (at most 100).
pub fn fill_percent(used: f64, max: u32) -> f64 {
    if max == 0 {
        return 100.0;
    }
    (used / f64::from(max) * 100.0).min(100.0)
}

/// Change of one field of a machine's placement.
fn set_place(plan: &mut Plan, vm: &str, cpu: bool, place: Place) {
    if let Some(p) = plan.get_mut(vm) {
        if cpu {
            p.cpu = place;
        } else {
            p.mem = place;
        }
    }
}

#[component]
pub fn NumaLab(nodes: Vec<Node>, scenarios: Vec<Scenario>, goals: Goals) -> impl IntoView {
    let sid = RwSignal::new(0usize);
    let plans = RwSignal::new(scenarios.iter().map(|s| numa::default_plan(&s.vms)).collect::<Vec<Plan>>());
    let msg: RwSignal<Option<Msg>> = RwSignal::new(None);
    let nodes = StoredValue::new(nodes);
    let scenarios = StoredValue::new(scenarios);

    let pick = Callback::new(move |i: usize| {
        sid.set(i);
        msg.set(None);
    });
    let tabs = scenarios.with_value(|ss| {
        ss.iter()
            .enumerate()
            .map(|(i, s)| view! { <Tab title=s.title.clone() id=s.id.clone() index=i active=sid.into() goals=goals on_pick=pick /> })
            .collect_view()
    });

    let scenario = move || scenarios.with_value(|ss| ss.get(sid.get()).cloned());
    let plan = move || plans.with(|p| p.get(sid.get()).cloned().unwrap_or_default());
    let evaluation = move || -> Option<Evaluation> {
        let sc = scenario()?;
        let plan = plan();
        nodes.with_value(|n| numa::evaluate(n, &sc.vms, &plan).ok())
    };
    let edit = move |vm: String, cpu: bool, place: Place| {
        plans.update(|p| {
            if let Some(plan) = p.get_mut(sid.get_untracked()) {
                set_place(plan, &vm, cpu, place);
            }
        });
        msg.set(None);
    };
    let set_vnuma = move |on: bool| {
        plans.update(|p| {
            if let Some(plan) = p.get_mut(sid.get_untracked()) {
                for placement in plan.values_mut() {
                    placement.vnuma = on;
                }
            }
        });
        msg.set(None);
    };
    let accept = move |_| {
        let Some(sc) = scenario() else { return };
        let plan = plan();
        let (m, ok) = nodes.with_value(|n| accept_outcome(n, &sc, &plan));
        msg.set(Some(m));
        if ok {
            goals.mark(&sc.id, data(&plan));
        }
    };
    let options = nodes.with_value(|n| place_options(n.len()));

    view! {
        <div class="vl">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            <div class="vl-grid">
                <div class="vl-card">
                    <p class="vl-goal">
                        <span class="s-label">{i18n::tr("goal")}</span>
                        " "
                        {move || scenario().map(|s| s.goal)}
                    </p>
                    <table class="vl-vms">
                        <thead>
                            <tr>
                                <th>{i18n::tr("VM")}</th>
                                <th>{i18n::tr("CPUs")}</th>
                                <th>{i18n::tr("memory")}</th>
                                <th>{i18n::tr("remote")}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {move || {
                                let sc = scenario()?;
                                let ev = evaluation();
                                let plan = plan();
                                Some(sc.vms.iter().map(|vm| {
                                    let remote = ev.as_ref()
                                        .and_then(|e| e.per.iter().find(|(n, _)| *n == vm.name))
                                        .map(|(_, r)| pct(*r))
                                        .unwrap_or_else(|| "—".to_string());
                                    let current = plan.get(&vm.name).copied();
                                    let selects = [true, false].map(|cpu| {
                                        let selected = current.map(|p| if cpu { p.cpu } else { p.mem });
                                        let name = vm.name.clone();
                                        let opts = options.iter().map(|(v, t)| {
                                            let is_sel = selected.is_some_and(|p| p.to_string() == *v);
                                            view! { <option value=v.clone() selected=is_sel>{t.clone()}</option> }
                                        }).collect_view();
                                        view! {
                                            <td>
                                                <select on:change=move |ev| {
                                                    if let Some(place) = parse_place(&event_target_value(&ev)) {
                                                        edit(name.clone(), cpu, place);
                                                    }
                                                }>{opts}</select>
                                            </td>
                                        }
                                    });
                                    view! {
                                        <tr>
                                            <td>
                                                <b>{vm.name.clone()}</b>
                                                <br />
                                                <span class="vl-hint">{i18n::trf!("{0} vCPU · {1} GiB", vm.vcpus, vm.mem)}</span>
                                            </td>
                                            {selects}
                                            <td>{remote}</td>
                                        </tr>
                                    }
                                }).collect_view())
                            }}
                        </tbody>
                    </table>
                    <label class="vl-check">
                        <input
                            type="checkbox"
                            prop:checked=move || plan().values().any(|p| p.vnuma)
                            on:change=move |ev| set_vnuma(event_target_checked(&ev))
                        />
                        <span>{i18n::tr("virtual NUMA topology for spanning VMs")}</span>
                    </label>
                    <div class="vl-actions">
                        <button class="quiz-btn" on:click=accept>{i18n::tr("Accept placement")}</button>
                    </div>
                    {move || msg.get().map(|m| view! { <p class={if m.bad { "vl-no" } else { "vl-yes" }}>{m.text}</p> })}
                </div>

                <div class="vl-card">
                    <span class="s-label">{i18n::tr("host nodes")}</span>
                    {move || {
                        let ev = evaluation();
                        nodes.with_value(|ns| {
                            ns.iter().enumerate().map(|(i, n)| {
                                let load = ev.as_ref().and_then(|e| e.load.get(i).copied());
                                let (cores, mem) = load.map_or((0.0, 0.0), |l| (l.cores, l.mem));
                                view! {
                                    <div class="vl-node">
                                        <b>{i18n::trf!("node {0}", i)}</b>
                                        <Meter label=i18n::tr("cores") used=cores max=n.cores />
                                        <Meter label=i18n::tr("memory, GiB") used=mem max=n.mem />
                                    </div>
                                }
                            }).collect_view()
                        })
                    }}
                    <table class="vl-stat">
                        <tbody>
                            <tr>
                                <td><b>{i18n::tr("average share of remote accesses")}</b></td>
                                <td><b>{move || evaluation().map(|e| pct(e.avg)).unwrap_or_else(|| "—".to_string())}</b></td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="vl-hint">
                        {i18n::tr("Own memory is 0%, another node is 100%, spanning is 50% (with virtual NUMA, a fully spanning VM gets 25%).")}
                    </p>
                </div>
            </div>
        </div>
    }
}

/// Node load scale.
#[component]
fn Meter(label: &'static str, used: f64, max: u32) -> impl IntoView {
    let over = used > f64::from(max);
    view! {
        <div class="vl-meter">
            <span>{format!("{label}: {used} / {max}")}</span>
            <div class="vl-bar">
                <i style=format!("width: {}%", fill_percent(used, max)) class:full=over></i>
            </div>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::numa::{default_nodes, default_plan, default_scenarios, Placement};

    use super::*;

    fn scenario(id: &str) -> Scenario {
        default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
    }

    fn at(cpu: u8, mem: u8) -> Placement {
        Placement { cpu: Place::Node(cpu), mem: Place::Node(mem), vnuma: false }
    }

    #[test]
    fn options_cover_nodes_and_wide() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let o = place_options(2);
        assert_eq!(o.iter().map(|(v, _)| v.as_str()).collect::<Vec<_>>(), ["0", "1", "wide"]);
        assert_eq!(o[2].1, "растянуть");
        for (v, _) in &o {
            assert!(parse_place(v).is_some_and(|p| p.to_string() == *v));
        }
        assert!(parse_place("x").is_none());
    }

    #[test]
    fn default_plan_does_not_fit() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario("small");
        let (m, ok) = accept_outcome(&default_nodes(), &sc, &default_plan(&sc.vms));
        assert!(!ok && m.bad);
        assert_eq!(m.text, "Размещение не помещается: на каком-то узле не хватает ядер или памяти.");
    }

    #[test]
    fn too_remote_and_accepted_messages() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let nodes = default_nodes();
        let sc = scenario("small");
        // everything fits, but A and C have memory on a foreign node: half of the accesses are remote
        let mut plan = default_plan(&sc.vms);
        plan.insert("A".into(), at(0, 1));
        plan.insert("B".into(), at(0, 0));
        plan.insert("C".into(), at(1, 0));
        plan.insert("D".into(), at(1, 1));
        let (m, ok) = accept_outcome(&nodes, &sc, &plan);
        assert!(!ok);
        assert_eq!(m.text, "Удалённых обращений 50% — больше допустимых 0%.");
        plan.insert("A".into(), at(0, 0));
        plan.insert("C".into(), at(1, 1));
        // A(16)+B(12) = 28 GiB on node 0, C(16)+D(12) = 28 GiB on node 1
        let (m, ok) = accept_outcome(&nodes, &sc, &plan);
        assert!(ok && !m.bad, "{}", m.text);
        assert_eq!(m.text, "✓ Принято: удалённых обращений 0%.");
    }

    #[test]
    fn accepted_plan_is_verified_by_server_model() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let (nodes, sc) = (default_nodes(), scenario("small"));
        let mut plan = default_plan(&sc.vms);
        for (name, node) in [("A", 0), ("B", 0), ("C", 1), ("D", 1)] {
            plan.insert(name.into(), at(node, node));
        }
        let spec = virtlab::Spec::Numa { nodes: nodes.clone(), scenarios: default_scenarios() };
        let mut solution = serde_json::Map::new();
        solution.insert("small".into(), data(&plan));
        let v = virtlab::verify(&spec, &serde_json::Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "small").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }

    #[test]
    fn set_place_edits_one_field() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario("small");
        let mut plan = default_plan(&sc.vms);
        set_place(&mut plan, "B", true, Place::Node(1));
        set_place(&mut plan, "B", false, Place::Wide);
        assert_eq!(plan["B"].cpu, Place::Node(1));
        assert_eq!(plan["B"].mem, Place::Wide);
        assert_eq!(plan["A"], at(0, 0));
        set_place(&mut plan, "no such", true, Place::Wide); // does not panic
    }

    #[test]
    fn meter_fill_is_capped() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(fill_percent(4.0, 8), 50.0);
        assert_eq!(fill_percent(12.0, 8), 100.0);
        assert_eq!(fill_percent(1.0, 0), 100.0);
    }
}
