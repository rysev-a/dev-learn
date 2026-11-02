//! oVirt scheduler simulator (chapter 22): the scenario gives hosts and VMs, the student chooses the cluster policy — filters and weights.
//! The goal of a scenario is checked on the placement; the exercise is solved when all are reached. The goal data is the policy;
//! the server schedules again.

use leptos::prelude::*;
use virtlab::ovirt_sched::{mistake_text, schedule, Host, Plan, Policy, Scenario, Vm, MAX_FACTOR};

use super::common::{data, Goals, Tab};

/// Result of a run: the placement and whether the scenario goal is reached.
#[derive(Clone, Debug, PartialEq)]
pub struct Run {
    pub plan: Plan,
    pub reached: bool,
}

/// Run a scenario with the policy.
pub fn run(sc: &Scenario, policy: &Policy) -> Run {
    let plan = schedule(&sc.hosts, &sc.vms, policy);
    let reached = sc.check.check(&plan);
    Run { plan, reached }
}

/// Why the goal is not reached: the first failed condition, in words.
pub fn reason(sc: &Scenario, plan: &Plan) -> Option<String> {
    if plan.unplaced() > 0 {
        return Some(i18n::trf!("{0} VM(s) found no host", plan.unplaced()));
    }
    if plan.mistakes() > 0 {
        return Some(i18n::trf!("{0} placement(s) break a constraint", plan.mistakes()));
    }
    if sc.check.max_spread.is_some_and(|m| plan.spread() > m) {
        return Some(i18n::trf!("the hosts differ by {0} VMs, at most {1} allowed", plan.spread(), sc.check.max_spread.unwrap_or(0)));
    }
    if sc.check.max_used.is_some_and(|m| plan.used() as u32 > m) {
        return Some(i18n::trf!("{0} hosts are used, at most {1} allowed", plan.used(), sc.check.max_used.unwrap_or(0)));
    }
    None
}

#[component]
pub fn OvirtSchedLab(scenarios: Vec<Scenario>, goals: Goals) -> impl IntoView {
    let sid = RwSignal::new(0usize);
    let policy = RwSignal::new(Policy::default());
    let result: RwSignal<Option<Run>> = RwSignal::new(None);
    let scenarios = StoredValue::new(scenarios);
    let scenario = move || scenarios.with_value(|ss| ss.get(sid.get()).cloned());

    let pick = Callback::new(move |i: usize| {
        result.set(None);
        sid.set(i);
    });
    let tabs = scenarios.with_value(|ss| {
        ss.iter()
            .enumerate()
            .map(|(i, s)| view! { <Tab title=i18n::tr_dyn(&s.title) id=s.id.clone() index=i active=sid.into() goals=goals on_pick=pick /> })
            .collect_view()
    });

    let start = move |_| {
        let Some(sc) = scenario() else { return };
        let p = policy.get_untracked();
        let r = run(&sc, &p);
        if r.reached {
            goals.mark(&sc.id, data(&p));
        }
        result.set(Some(r));
    };
    let filter = move |f: fn(&mut Policy, bool)| move |ev: web_sys::Event| policy.update(|p| f(p, event_target_checked(&ev)));
    let weight = move |f: fn(&mut Policy, u32)| {
        move |ev: web_sys::Event| {
            if let Ok(v) = event_target_value(&ev).parse::<u32>() {
                policy.update(|p| f(p, v.min(MAX_FACTOR)));
            }
        }
    };
    let options = move |get: fn(&Policy) -> u32| {
        (0..=MAX_FACTOR)
            .map(|n| view! { <option value=n.to_string() selected=move || policy.with(|p| get(p) == n)>{n}</option> })
            .collect_view()
    };

    view! {
        <div class="vl">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            <div class="vl-grid">
                <div class="vl-card">
                    <p class="vl-goal">
                        <span class="s-label">{i18n::tr("goal")}</span>
                        " "
                        {move || scenario().map(|s| i18n::tr_dyn(&s.goal))}
                    </p>
                    {move || scenario().map(|s| view! { <Inventory hosts=s.hosts.clone() vms=s.vms.clone() /> })}

                    <span class="s-label">{i18n::tr("filters (hard conditions)")}</span>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || policy.get().memory on:change=filter(|p, on| p.memory = on) />
                        <span>{i18n::tr("Memory: the host has enough free memory")}</span>
                    </label>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || policy.get().network on:change=filter(|p, on| p.network = on) />
                        <span>{i18n::tr("Network: the host has the networks of the VM's NICs")}</span>
                    </label>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || policy.get().affinity on:change=filter(|p, on| p.affinity = on) />
                        <span>{i18n::tr("Anti-affinity (hard): no second VM of the group on the host")}</span>
                    </label>
                    <span class="s-label">{i18n::tr("weights (preferences, factor 0 = off)")}</span>
                    <label class="vl-check vl-weight">
                        <select on:change=weight(|p, v| p.even = v)>{options(|p| p.even)}</select>
                        <span>{i18n::tr("Even distribution: fewer VMs is better")}</span>
                    </label>
                    <label class="vl-check vl-weight">
                        <select on:change=weight(|p, v| p.free_mem = v)>{options(|p| p.free_mem)}</select>
                        <span>{i18n::tr("Free memory: more is better")}</span>
                    </label>
                    <label class="vl-check vl-weight">
                        <select on:change=weight(|p, v| p.pack = v)>{options(|p| p.pack)}</select>
                        <span>{i18n::tr("Power saving: more VMs is better, pack the hosts")}</span>
                    </label>
                    <div class="vl-actions">
                        <button class="quiz-btn" on:click=start>{i18n::tr("Start the VMs")}</button>
                    </div>
                    <p class="vl-hint">{move || scenario().map(|s| i18n::tr_dyn(&s.hint))}</p>
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">{i18n::tr("where the VMs went")}</span>
                    </div>
                    {move || result.with(Option::is_none).then(|| view! {
                        <p class="pr-empty">{i18n::tr("Press \"Start the VMs\": the scheduler's choices will appear here.")}</p>
                    })}
                    {move || {
                        let r = result.get()?;
                        let sc = scenario()?;
                        Some(view! { <Outcome scenario=sc run=r /> })
                    }}
                </div>
            </div>
        </div>
    }
}

/// Hosts and VMs of the scenario.
#[component]
fn Inventory(hosts: Vec<Host>, vms: Vec<Vm>) -> impl IntoView {
    let hosts = hosts
        .into_iter()
        .map(|h| {
            view! {
                <tr>
                    <td>{h.name}</td>
                    <td>{i18n::trf!("{0} GiB free", h.mem)}</td>
                    <td>{i18n::trf!("{0} VM(s)", h.vms)}</td>
                    <td>{h.nets.join(", ")}</td>
                </tr>
            }
        })
        .collect_view();
    let vms = vms
        .into_iter()
        .map(|v| {
            let group = v.group.map(|g| i18n::trf!("group {0}", g)).unwrap_or_default();
            view! {
                <tr>
                    <td>{v.name}</td>
                    <td>{i18n::trf!("{0} GiB", v.mem)}</td>
                    <td>{v.nets.join(", ")}</td>
                    <td>{group}</td>
                </tr>
            }
        })
        .collect_view();
    view! {
        <span class="s-label">{i18n::tr("hosts")}</span>
        <table class="vl-tbl"><tbody>{hosts}</tbody></table>
        <span class="s-label">{i18n::tr("VMs to start, in order")}</span>
        <table class="vl-tbl"><tbody>{vms}</tbody></table>
    }
}

/// The placement, the load of hosts and the verdict on the scenario's goal.
#[component]
fn Outcome(scenario: Scenario, run: Run) -> impl IntoView {
    let rows = run
        .plan
        .placements
        .iter()
        .map(|p| {
            let bad = p.mistakes.iter().map(|m| mistake_text(*m)).collect::<Vec<_>>().join(", ");
            let wrong = !bad.is_empty() || p.host.is_none();
            let host = p.host.clone().unwrap_or_else(|| i18n::tr("no host").to_string());
            view! {
                <tr class:bad=wrong>
                    <td>{p.vm.clone()}</td>
                    <td>"→ " {host}</td>
                    <td>{bad}</td>
                </tr>
            }
        })
        .collect_view();
    let max = run.plan.counts.iter().map(|c| c.1).max().unwrap_or(1).max(1);
    let bars = run
        .plan
        .counts
        .iter()
        .map(|(name, n)| {
            view! {
                <li>
                    <span class="vl-rk">{name.clone()}</span>
                    <div class="vl-bar"><i style=format!("width: {}%", f64::from(*n) / f64::from(max) * 100.0)></i></div>
                    <span class="vl-rv">{i18n::trf!("{0} VM(s)", n)}</span>
                </li>
            }
        })
        .collect_view();
    let why = reason(&scenario, &run.plan);
    let reached = run.reached;
    view! {
        <table class="vl-tbl"><tbody>{rows}</tbody></table>
        <span class="s-label">{i18n::tr("VMs per host")}</span>
        <ul class="vl-rounds">{bars}</ul>
        <div class="vl-final">
            <p class={if reached { "vl-yes" } else { "vl-no" }}>
                {if reached { i18n::tr("✓ Scenario goal reached") } else { i18n::tr("Scenario goal not reached — change the policy") }}
            </p>
            {why.map(|w| view! { <p class="vl-no">{w}</p> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::ovirt_sched::default_scenarios;

    use super::*;

    fn scenario(id: &str) -> Scenario {
        default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
    }

    #[test]
    fn reasons_follow_the_order_of_conditions() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario("pack");
        // without weights and filters everything lands on the first host, which overflows
        let r = run(&sc, &Policy::default());
        assert!(!r.reached);
        assert_eq!(reason(&sc, &r.plan).as_deref(), Some("Размещений с нарушенным ограничением: 1"));
        // an even load fits everything but uses three hosts
        let r = run(&sc, &Policy { memory: true, even: 1, ..Policy::default() });
        assert_eq!(reason(&sc, &r.plan).as_deref(), Some("Используется хостов: 3, допустимо не больше 2"));
        // the goal is reached: no reason
        let r = run(&sc, &Policy { memory: true, ..Policy::default() });
        assert!(r.reached && reason(&sc, &r.plan).is_none());
    }

    #[test]
    fn goal_data_is_accepted_by_server() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario("anti");
        let policy = Policy { affinity: true, even: 2, ..Policy::default() };
        assert!(run(&sc, &policy).reached);
        let spec = virtlab::Spec::OvirtSched { scenarios: default_scenarios() };
        let mut solution = serde_json::Map::new();
        solution.insert("anti".into(), data(&policy));
        let v = virtlab::verify(&spec, &serde_json::Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "anti").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }

    #[test]
    fn unplaced_vms_are_reported_first() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut sc = scenario("pack");
        sc.vms[0].mem = 64;
        let r = run(&sc, &Policy { memory: true, ..Policy::default() });
        assert_eq!(reason(&sc, &r.plan).as_deref(), Some("Машин без хоста: 1"));
    }
}
