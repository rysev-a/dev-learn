//! oVirt host fencing simulator (chapter 19): the scenario fixes what happened to a host, the student sets soft fencing, power management and the
//! cluster policy. The goal of a scenario is checked on the run result; the exercise is solved when all are reached. The goal data is the settings;
//! the server simulates again.

use leptos::prelude::*;
use virtlab::ovirt_fence::{simulate, step_text, FenceConfig, Outcome, Scenario, Simulation};

use super::common::{data, Goals, Tab};

/// Run result: the simulation and whether the scenario goal is reached.
#[derive(Clone, Debug, PartialEq)]
pub struct Run {
    pub sim: Simulation,
    pub reached: bool,
}

/// Run a scenario with the settings.
pub fn run(sc: &Scenario, cfg: &FenceConfig) -> Run {
    let sim = simulate(cfg, &sc.situation);
    let reached = sc.check.check(&sim);
    Run { sim, reached }
}

/// What the engine ended up doing, in words.
pub fn outcome_text(o: Outcome) -> &'static str {
    match o {
        Outcome::Recovered => i18n::tr("the host is Up again, nothing was rebooted"),
        Outcome::SkippedLease => i18n::tr("fencing skipped: live lease"),
        Outcome::SkippedConnectivity => i18n::tr("fencing skipped: connectivity issues"),
        Outcome::Fenced => i18n::tr("the host was power-cycled"),
        Outcome::FenceFailed => i18n::tr("power management failed"),
        Outcome::Manual => i18n::tr("waiting for the administrator's confirmation"),
    }
}

#[component]
pub fn OvirtFenceLab(scenarios: Vec<Scenario>, goals: Goals) -> impl IntoView {
    let sid = RwSignal::new(0usize);
    let cfg = RwSignal::new(FenceConfig::default());
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
        let settings = cfg.get_untracked();
        let r = run(&sc, &settings);
        if r.reached {
            goals.mark(&sc.id, data(&settings));
        }
        result.set(Some(r));
    };
    let toggle = move |f: fn(&mut FenceConfig, bool)| move |ev: web_sys::Event| cfg.update(|c| f(c, event_target_checked(&ev)));

    view! {
        <div class="vl">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            <div class="vl-grid">
                <div class="vl-card">
                    <p class="vl-goal">{move || scenario().map(|s| i18n::tr_dyn(&s.story))}</p>
                    <div class="vl-facts">
                        <span>
                            {move || scenario().map(|s| i18n::trf!("{0} of {1} hosts do not answer", s.situation.down, s.situation.hosts))}
                        </span>
                    </div>
                    <p class="vl-goal">
                        <span class="s-label">{i18n::tr("goal")}</span>
                        " "
                        {move || scenario().map(|s| i18n::tr_dyn(&s.goal))}
                    </p>

                    <span class="s-label">{i18n::tr("host settings")}</span>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || cfg.get().soft on:change=toggle(|c, on| c.soft = on) />
                        <span>{i18n::tr("soft fencing: restart VDSM over SSH")}</span>
                    </label>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || cfg.get().power on:change=toggle(|c, on| c.power = on) />
                        <span>{i18n::tr("power management: a fence agent is configured")}</span>
                    </label>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || cfg.get().vm_leases on:change=toggle(|c, on| c.vm_leases = on) />
                        <span>{i18n::tr("the highly available VM has a lease on storage")}</span>
                    </label>
                    <span class="s-label">{i18n::tr("cluster fencing policy")}</span>
                    <label class="vl-check">
                        <input type="checkbox" prop:checked=move || cfg.get().skip_lease on:change=toggle(|c, on| c.skip_lease = on) />
                        <span>{i18n::tr("skip fencing if the host has a live lease on storage")}</span>
                    </label>
                    <label class="vl-check">
                        <input
                            type="checkbox"
                            prop:checked=move || cfg.get().skip_connectivity
                            on:change=toggle(|c, on| c.skip_connectivity = on)
                        />
                        <span>{i18n::tr("skip fencing on cluster connectivity issues")}</span>
                    </label>
                    <label class="vl-field">
                        <span>{i18n::tr("threshold: ")}<b>{move || format!("{}%", cfg.get().threshold)}</b></span>
                        <input
                            type="range"
                            min="1"
                            max="100"
                            step="1"
                            prop:disabled=move || !cfg.get().skip_connectivity
                            prop:value=move || cfg.get().threshold.to_string()
                            on:input=move |ev| {
                                if let Ok(v) = event_target_value(&ev).parse::<u32>() {
                                    cfg.update(|c| c.threshold = v.clamp(1, 100));
                                }
                            }
                        />
                    </label>
                    <div class="vl-actions">
                        <button class="quiz-btn" on:click=start>{i18n::tr("Run the scenario")}</button>
                    </div>
                    <p class="vl-hint">{move || scenario().map(|s| i18n::tr_dyn(&s.hint))}</p>
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">{i18n::tr("what the engine did")}</span>
                    </div>
                    {move || result.with(Option::is_none).then(|| view! {
                        <p class="pr-empty">{i18n::tr("Press \"Run the scenario\": the engine's steps will appear here.")}</p>
                    })}
                    {move || result.get().map(|r| view! { <Log run=r /> })}
                </div>
            </div>
        </div>
    }
}

/// The engine's steps and the verdict on the scenario's goal.
#[component]
fn Log(run: Run) -> impl IntoView {
    let steps = run.sim.steps.iter().map(|s| view! { <li>{step_text(s)}</li> }).collect_view();
    let reached = run.reached;
    view! {
        <ol class="vl-steps">{steps}</ol>
        <div class="vl-final">
            <p>{i18n::tr("Result: ")}<b>{outcome_text(run.sim.outcome)}</b></p>
            <p class={if reached { "vl-yes" } else { "vl-no" }}>
                {if reached { i18n::tr("✓ Scenario goal reached") } else { i18n::tr("Scenario goal not reached — change the settings") }}
            </p>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::ovirt_fence::default_scenarios;

    use super::*;

    fn scenario(id: &str) -> Scenario {
        default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
    }

    fn all_on() -> FenceConfig {
        FenceConfig { soft: true, power: true, skip_lease: true, skip_connectivity: true, threshold: 50, vm_leases: true }
    }

    #[test]
    fn starting_settings_reach_no_goal() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for sc in default_scenarios() {
            assert!(!run(&sc, &FenceConfig::default()).reached, "{}", sc.id);
        }
    }

    #[test]
    fn log_is_in_russian_and_goal_data_is_accepted_by_server() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let sc = scenario("hung");
        let r = run(&sc, &all_on());
        assert!(r.reached);
        assert_eq!(r.sim.steps.len(), 2);
        assert_eq!(step_text(&r.sim.steps[1]), "Мягкое ограждение: VDSM перезапущен по SSH, хост отвечает и в статусе Up. Ничего не перезагружалось.");
        assert_eq!(outcome_text(r.sim.outcome), "хост снова Up, ничего не перезагружалось");
        let spec = virtlab::Spec::OvirtFence { scenarios: default_scenarios() };
        let mut solution = serde_json::Map::new();
        solution.insert("hung".into(), data(&all_on()));
        let v = virtlab::verify(&spec, &serde_json::Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "hung").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }
}
