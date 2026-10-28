//! Симулятор живой миграции (глава 10): сценарий задаёт скорость записи гостя и сети, ученик подбирает допустимый простой,
//! замедление, сжатие и момент перехода на post-copy. Цель каждого сценария проверяется по результату запуска; упражнение
//! решено, когда достигнуты все. В данных цели — параметры запуска; сервер симулирует заново.

use gloo_timers::future::TimeoutFuture;
use leptos::{prelude::*, task::spawn_local};
use virtlab::migration::{MigrationInput, Outcome, Scenario, Simulation, MEM_MIB};

use super::common::{data, fmt_ru, Goals, Tab};

/// Пауза между кругами при показе.
const STEP_MS: u32 = 380;

/// Запуск: результат симуляции и сколько кругов уже показано.
#[derive(Clone)]
struct Playing {
    result: Simulation,
    shown: usize,
}

impl Playing {
    /// Все круги показаны (и ещё один «тик» на итог), как в React.
    fn finished(&self) -> bool {
        self.shown > self.result.rounds.len()
    }
}

/// Настройки ученика.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Settings {
    pub downtime_ms: f64,
    pub auto_converge: bool,
    pub compress: bool,
    /// включён ли переход на post-copy
    pub hybrid: bool,
    /// после скольких кругов pre-copy
    pub after: u32,
}

impl Default for Settings {
    fn default() -> Self {
        Self { downtime_ms: 300.0, auto_converge: false, compress: false, hybrid: false, after: 3 }
    }
}

/// Параметры запуска сценария с настройками ученика.
pub fn params(sc: &Scenario, s: &Settings) -> MigrationInput {
    sc.input(s.downtime_ms, s.auto_converge, s.compress, s.hybrid.then_some(s.after))
}

/// Имя класса итогового блока по исходу.
fn outcome_class(o: Outcome) -> &'static str {
    match o {
        Outcome::Precopy => "precopy",
        Outcome::Postcopy => "postcopy",
        Outcome::Failed => "failed",
    }
}

/// Ширина столбика круга в процентах от всей памяти.
pub fn bar_percent(sent: f64) -> f64 {
    sent / MEM_MIB * 100.0
}

/// Круг «почти вся память» — столбик красится как заполненный.
pub fn bar_full(sent: f64) -> bool {
    sent >= MEM_MIB * 0.98
}

#[component]
pub fn MigrationLab(scenarios: Vec<Scenario>, goals: Goals) -> impl IntoView {
    let sid = RwSignal::new(0usize);
    let settings = RwSignal::new(Settings::default());
    let run: RwSignal<Option<Playing>> = RwSignal::new(None);
    // «поколение» показа: смена сценария, новый запуск и уход со страницы обрывают прежний цикл кругов
    let generation = StoredValue::new(0u64);
    on_cleanup(move || generation.update_value(|g| *g += 1));
    let scenarios = StoredValue::new(scenarios);
    let scenario = move || scenarios.with_value(|ss| ss.get(sid.get()).cloned());

    let pick = Callback::new(move |i: usize| {
        generation.update_value(|g| *g += 1);
        run.set(None);
        sid.set(i);
    });
    let tabs = scenarios.with_value(|ss| {
        ss.iter()
            .enumerate()
            .map(|(i, s)| view! { <Tab title=s.title.clone() id=s.id.clone() index=i active=sid.into() goals=goals on_pick=pick /> })
            .collect_view()
    });

    let start = move |_| {
        let Some(sc) = scenario() else { return };
        let input = params(&sc, &settings.get_untracked());
        let result = virtlab::migration::simulate(&input);
        let rounds = result.rounds.len();
        let reached = sc.check.check(&result);
        run.set(Some(Playing { result, shown: 0 }));
        generation.update_value(|g| *g += 1);
        let mine = generation.get_value();
        spawn_local(async move {
            loop {
                TimeoutFuture::new(STEP_MS).await;
                if generation.try_get_value() != Some(mine) {
                    return;
                }
                let Some(shown) = run.try_update(|r| r.as_mut().map(|p| {
                    p.shown += 1;
                    p.shown
                })).flatten() else {
                    return;
                };
                if shown > rounds {
                    if reached {
                        goals.mark(&sc.id, data(&input));
                    }
                    return;
                }
            }
        });
    };

    let toggle = move |f: fn(&mut Settings, bool)| {
        move |ev: web_sys::Event| settings.update(|s| f(s, event_target_checked(&ev)))
    };
    let after_options = (1..=6u32)
        .map(|n| view! { <option value=n.to_string() selected=move || settings.with(|s| s.after == n)>{n}</option> })
        .collect_view();

    view! {
        <div class="vl">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            <div class="vl-grid">
                <div class="vl-card">
                    <div class="vl-facts">
                        <span><b>{i18n::trf!("{0} GiB", MEM_MIB / 1024.0)}</b>{i18n::tr(" of guest memory")}</span>
                        <span>{i18n::tr("guest writes ")}<b>{move || scenario().map(|s| i18n::trf!("{0} MiB/s", fmt_ru(s.dirty)))}</b></span>
                        <span>{i18n::tr("network ")}<b>{move || scenario().map(|s| i18n::trf!("{0} MiB/s", fmt_ru(s.bw)))}</b>{i18n::tr(" (≈10 Gbit/s)")}</span>
                    </div>
                    <p class="vl-goal">
                        <span class="s-label">{i18n::tr("goal")}</span>
                        " "
                        {move || scenario().map(|s| s.goal)}
                    </p>

                    <label class="vl-field">
                        <span>{i18n::tr("allowed downtime: ")}<b>{move || i18n::trf!("{0} ms", settings.get().downtime_ms)}</b></span>
                        <input
                            type="range"
                            min="20"
                            max="1000"
                            step="10"
                            prop:value=move || settings.get().downtime_ms.to_string()
                            on:input=move |ev| {
                                if let Ok(v) = event_target_value(&ev).parse::<f64>() {
                                    settings.update(|s| s.downtime_ms = v);
                                }
                            }
                        />
                    </label>
                    <label class="vl-check">
                        <input
                            type="checkbox"
                            prop:checked=move || settings.get().auto_converge
                            on:change=toggle(|s, on| s.auto_converge = on)
                        />
                        <span>{i18n::tr("auto-converge: throttle the vCPUs (20%, then +10% per round)")}</span>
                    </label>
                    <label class="vl-check">
                        <input
                            type="checkbox"
                            prop:checked=move || settings.get().compress
                            on:change=toggle(|s, on| s.compress = on)
                        />
                        <span>{i18n::tr("page compression (link ×1.5)")}</span>
                    </label>
                    <label class="vl-check row">
                        <input
                            type="checkbox"
                            prop:checked=move || settings.get().hybrid
                            on:change=toggle(|s, on| s.hybrid = on)
                        />
                        <span>{i18n::tr("hybrid: switch to post-copy after")}</span>
                        <select
                            prop:disabled=move || !settings.get().hybrid
                            on:change=move |ev| {
                                if let Ok(n) = event_target_value(&ev).parse::<u32>() {
                                    settings.update(|s| s.after = n);
                                }
                            }
                        >
                            {after_options}
                        </select>
                        <span>{i18n::tr("rounds")}</span>
                    </label>
                    <div class="vl-actions">
                        <button class="quiz-btn" on:click=start>{i18n::tr("Start migration")}</button>
                    </div>
                    <p class="vl-hint">{move || scenario().map(|s| s.hint)}</p>
                </div>

                <div class="vl-card">
                    <div class="pr-res-head">
                        <span class="s-label">{i18n::tr("pre-copy rounds")}</span>
                        {move || run.with(|r| r.as_ref().map(|p| i18n::trf!("stop threshold ≈ {0} MiB", fmt_ru(p.result.limit))))
                            .map(|t| view! { <span class="pr-res-time">{t}</span> })}
                    </div>
                    {move || run.with(Option::is_none).then(|| view! {
                        <p class="pr-empty">
                            {i18n::tr("Press \"Start migration\": the remaining memory will shrink here round by round.")}
                        </p>
                    })}
                    {move || run.get().map(|p| view! { <Rounds playing=p /> })}
                    {move || {
                        let p = run.get().filter(Playing::finished)?;
                        let reached = scenario()?.check.check(&p.result);
                        Some(view! { <Final result=p.result reached=reached /> })
                    }}
                </div>
            </div>
        </div>
    }
}

/// Показанные круги: столбик остатка, размер и время.
#[component]
fn Rounds(playing: Playing) -> impl IntoView {
    let rows = playing
        .result
        .rounds
        .iter()
        .take(playing.shown)
        .map(|r| {
            let tail = i18n::trf!("{0} MiB · {1} s{2}", fmt_ru(r.sent), format!("{:.1}", r.secs), if r.throttle > 0.0 { i18n::trf!(" · throttle {0}%", r.throttle) } else { String::new() });
            view! {
                <li>
                    <span class="vl-rk">{i18n::trf!("round {0}", r.k)}</span>
                    <div class="vl-bar">
                        <i style=format!("width: {}%", bar_percent(r.sent)) class:full=bar_full(r.sent)></i>
                    </div>
                    <span class="vl-rv">{tail}</span>
                </li>
            }
        })
        .collect_view();
    view! { <ul class="vl-rounds">{rows}</ul> }
}

/// Итог миграции и вердикт по цели сценария.
#[component]
fn Final(result: Simulation, reached: bool) -> impl IntoView {
    let text = match result.outcome {
        Outcome::Precopy => view! {
            <p>
                {i18n::trf!("The remaining {0} MiB fits the threshold: the VM was stopped for ", fmt_ru(result.remaining))}
                <b>{i18n::trf!("{0} ms", result.downtime)}</b>
                {i18n::tr(", the migration took ")}
                <b>{i18n::trf!("{0} s", result.total)}</b>
                "."
            </p>
        }
        .into_any(),
        Outcome::Postcopy => view! {
            <p>
                {i18n::tr("The guest was switched to the target with a downtime of ")}
                <b>{i18n::trf!("{0} ms", result.downtime)}</b>
                {i18n::trf!(", the remaining {0} MiB is pulled on demand (≈{1} page faults). Total ", fmt_ru(result.remaining), result.faults)}
                <b>{i18n::trf!("{0} s", result.total)}</b>
                {i18n::tr(". While memory is scattered across servers, a network failure would lose the VM.")}
            </p>
        }
        .into_any(),
        Outcome::Failed => view! {
            <p>
                {i18n::trf!("Migration did not converge in {0} rounds: remaining {1} MiB, the stop would last ", virtlab::migration::MAX_ROUNDS, fmt_ru(result.remaining))}
                <b>{i18n::trf!("{0} ms", fmt_ru(result.downtime as f64))}</b>
                {i18n::tr(". The guest writes faster than the network can send.")}
            </p>
        }
        .into_any(),
    };
    view! {
        <div class=format!("vl-final {}", outcome_class(result.outcome))>
            {text}
            <p class={if reached { "vl-yes" } else { "vl-no" }}>
                {if reached { i18n::tr("✓ Scenario goal reached") } else { i18n::tr("Scenario goal not reached — change the settings") }}
            </p>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::migration::default_scenarios;

    use super::*;

    fn scenario(id: &str) -> Scenario {
        default_scenarios().into_iter().find(|s| s.id == id).expect("сценарий")
    }

    #[test]
    fn params_take_speeds_from_scenario() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let sc = scenario("busy");
        let p = params(&sc, &Settings { downtime_ms: 250.0, auto_converge: true, ..Settings::default() });
        assert_eq!((p.dirty, p.bw, p.downtime_ms), (2000.0, 1250.0, 250.0));
        assert!(p.auto_converge && !p.compress);
        assert_eq!(p.postcopy_after, None, "гибрид выключен");
        let p = params(&sc, &Settings { hybrid: true, after: 2, ..Settings::default() });
        assert_eq!(p.postcopy_after, Some(2));
    }

    #[test]
    fn default_settings_reach_calm_goal_only() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        // спокойный гость сходится с настройками по умолчанию и укладывается в 100 мс при малом простое
        let sc = scenario("calm");
        let small = Settings { downtime_ms: 100.0, ..Settings::default() };
        let r = virtlab::migration::simulate(&params(&sc, &small));
        assert_eq!(r.outcome, Outcome::Precopy);
        assert!(sc.check.check(&r), "простой {} мс", r.downtime);
        // активный гость без притормаживания не сходится
        let busy = scenario("busy");
        let r = virtlab::migration::simulate(&params(&busy, &Settings::default()));
        assert!(!busy.check.check(&r));
    }

    #[test]
    fn goal_data_is_accepted_by_server() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        // сценарий «wild»: гибрид после первого круга
        let sc = scenario("wild");
        let s = Settings { downtime_ms: 100.0, hybrid: true, after: 1, ..Settings::default() };
        let input = params(&sc, &s);
        assert!(sc.reached(&input));
        let spec = virtlab::Spec::Migration { scenarios: default_scenarios() };
        let mut solution = serde_json::Map::new();
        solution.insert("wild".into(), data(&input));
        let v = virtlab::verify(&spec, &serde_json::Value::Object(solution));
        assert_eq!(v.goals.iter().find(|g| g.id == "wild").map(|g| g.status.clone()), Some(virtlab::GoalStatus::Verified));
    }

    #[test]
    fn playback_finishes_one_tick_after_last_round() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        let sc = scenario("calm");
        let result = virtlab::migration::simulate(&params(&sc, &Settings::default()));
        let n = result.rounds.len();
        let mut p = Playing { result, shown: 0 };
        assert!(!p.finished());
        p.shown = n;
        assert!(!p.finished());
        p.shown = n + 1;
        assert!(p.finished());
    }

    #[test]
    fn bars() {
        let _ru = i18n::guard(i18n::Locale::Ru);
        assert_eq!(bar_percent(MEM_MIB), 100.0);
        assert!(bar_full(MEM_MIB) && !bar_full(MEM_MIB / 2.0));
        assert_eq!(outcome_class(Outcome::Failed), "failed");
    }
}
