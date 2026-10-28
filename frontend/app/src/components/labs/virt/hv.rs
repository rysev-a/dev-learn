//! Mini-hypervisor simulator (chapter 2): the guest runs a program, and the student is the monitor: at each trap they pick the correct
//! emulation over the virtual state. The POPF instruction does not trap until binary translation is enabled.
//! Solved when all programs are passed. The goal data is `{translate, mistakes, trace}`: the server replays the run
//! from the action record.

use leptos::prelude::*;
use serde::Serialize;
use serde_json::Value;
use virtlab::{
    error::SpecError,
    hv::{Choice, Inspection, Program, Session, Step, Stepped, TrapOption},
};

use super::common::{data, Goals, Tab};

/// Message under the trap: a wrong choice or a "silent" instruction — red, the rest — green.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Notice {
    pub bad: bool,
    pub text: String,
}

/// Data of a reached goal.
#[derive(Serialize)]
struct GoalData<'a> {
    translate: bool,
    mistakes: u32,
    trace: &'a [Step],
}

/// The student's run of one program: model session, action record and message.
#[derive(Clone)]
pub struct HvRun {
    session: Session,
    trace: Vec<Step>,
    notice: Option<Notice>,
    /// length of the program identifier — an addition to the option shuffle seed (as in React)
    id_len: u64,
}

impl HvRun {
    pub fn new(program: &Program, translate: bool) -> Result<Self, SpecError> {
        Ok(Self {
            session: Session::new(&program.code, translate)?,
            trace: vec![],
            notice: None,
            id_len: program.id.chars().count() as u64,
        })
    }

    pub fn session(&self) -> &Session {
        &self.session
    }

    pub fn notice(&self) -> Option<&Notice> {
        self.notice.as_ref()
    }

    /// Whether "Step" can be pressed: there is an instruction and it does not trap.
    pub fn can_step(&self) -> bool {
        matches!(self.session.inspect(), Some(Inspection::Direct | Inspection::Silent { .. }))
    }

    /// "Step" button.
    pub fn step(&mut self) {
        match self.session.step() {
            Stepped::Blocked => {}
            Stepped::Direct => {
                self.trace.push(Step::Direct);
                self.notice = None;
            }
            Stepped::Silent { why } => {
                self.trace.push(Step::Silent);
                self.notice = Some(Notice { bad: true, text: why });
            }
        }
    }

    /// Choosing an option at a trap. `Some(goal data)` — the program ran to the end correctly.
    pub fn choose(&mut self, label: &str) -> Option<Value> {
        let choice = self.session.choose(label);
        match choice {
            Choice::Invalid => None,
            Choice::Wrong { why } => {
                self.trace.push(Step::Trap { label: label.to_string() });
                self.notice = Some(Notice { bad: true, text: i18n::trf!("No: {0}.", why) });
                None
            }
            Choice::Applied => {
                self.trace.push(Step::Trap { label: label.to_string() });
                self.notice = None;
                None
            }
            Choice::Finished(f) => {
                self.trace.push(Step::Trap { label: label.to_string() });
                self.notice = None;
                f.ok.then(|| {
                    data(&GoalData { translate: self.session.translate(), mistakes: f.mistakes, trace: &self.trace })
                })
            }
        }
    }

    /// Start over (translation is kept).
    pub fn reset(&mut self) {
        self.session.reset();
        self.trace.clear();
        self.notice = None;
    }

    /// Turn translation on or off — before the run.
    pub fn set_translate(&mut self, on: bool) {
        self.session.set_translate(on);
    }

    /// Options at the current trap, shuffled by instruction number (so the correct one is not always first).
    pub fn options(&self) -> Vec<TrapOption> {
        match self.session.inspect() {
            Some(Inspection::Trap { options, .. }) => {
                shuffle(&options, self.session.state().pc as u64 * 7 + self.id_len)
            }
            _ => vec![],
        }
    }
}

/// Seeded shuffle (linear congruential generator): the same order on every render.
pub fn shuffle<T: Clone>(items: &[T], seed: u64) -> Vec<T> {
    let mut a = items.to_vec();
    let mut x = seed;
    for i in (1..a.len()).rev() {
        x = (x.wrapping_mul(1_103_515_245).wrapping_add(12_345)) & 0x7fff_ffff;
        let j = (x % (i as u64 + 1)) as usize;
        a.swap(i, j);
    }
    a
}

/// Program tabs and the selected program.
#[component]
pub fn HvLab(programs: Vec<Program>, goals: Goals) -> impl IntoView {
    let pid = RwSignal::new(0usize);
    // pressing an already open tab — "start over"
    let restart = RwSignal::new(0u32);
    let tabs = programs
        .iter()
        .enumerate()
        .map(|(i, p)| {
            view! { <Tab title=p.title.clone() id=p.id.clone() index=i active=pid.into() goals=goals on_pick=Callback::new(move |i| {
                if pid.get_untracked() == i {
                    restart.update(|n| *n += 1);
                } else {
                    pid.set(i);
                }
            }) /> }
        })
        .collect_view();
    let programs = StoredValue::new(programs);
    view! {
        <div class="vl">
            <div class="vl-tabs" role="tablist">{tabs}</div>
            {move || {
                programs
                    .with_value(|ps| ps.get(pid.get()).cloned())
                    .map(|program| view! { <HvProgram program=program goals=goals restart=restart /> })
            }}
        </div>
    }
}

/// One program: code, controls and guest state.
#[component]
fn HvProgram(program: Program, goals: Goals, restart: RwSignal<u32>) -> impl IntoView {
    match HvRun::new(&program, false) {
        Ok(run) => hv_body(program, goals, RwSignal::new(run), restart).into_any(),
        Err(e) => view! { <p class="error">{e.to_string()}</p> }.into_any(),
    }
}

fn hv_body(program: Program, goals: Goals, run: RwSignal<HvRun>, restart: RwSignal<u32>) -> impl IntoView {
    Effect::new(move |first: Option<()>| {
        restart.track();
        if first.is_some() {
            run.update(HvRun::reset);
        }
    });
    let pc = move || run.with(|r| r.session().state().pc);
    let halted = move || run.with(|r| r.session().state().halted);
    let code = program
        .code
        .iter()
        .enumerate()
        .map(|(i, c)| {
            view! {
                <li class:cur=move || i == pc() && !halted() class:past=move || i < pc()>
                    <span class="vl-ln">{i + 1}</span>
                    <code>{c.clone()}</code>
                </li>
            }
        })
        .collect_view();
    let pid = program.id.clone();
    let choose = Callback::new(move |label: String| {
        if let Some(info) = run.try_update(|r| r.choose(&label)).flatten() {
            goals.mark(&pid, info);
        }
    });
    let state = move |f: fn(&virtlab::hv::GuestState) -> String| run.with(|r| f(r.session().state()));
    let list = |v: &[i64]| if v.is_empty() { "—".to_string() } else { v.iter().map(i64::to_string).collect::<Vec<_>>().join(", ") };
    view! {
        <div class="vl-grid">
            <div class="vl-card">
                <p class="vl-goal">
                    <span class="s-label">{i18n::tr("goal")}</span>
                    " "
                    {program.goal.clone()}
                </p>
                <ol class="vl-code">{code}</ol>
                <label class="vl-check">
                    <input
                        type="checkbox"
                        prop:checked=move || run.with(|r| r.session().translate())
                        prop:disabled=move || run.with(|r| r.session().started())
                        on:change=move |ev| {
                            let on = event_target_checked(&ev);
                            run.update(|r| r.set_translate(on));
                        }
                    />
                    <span>{i18n::tr("binary translation of the guest kernel (before it runs)")}</span>
                </label>
                <div class="vl-actions">
                    <button class="quiz-btn" prop:disabled=move || !run.with(HvRun::can_step) on:click=move |_| run.update(HvRun::step)>
                        {i18n::tr("Step")}
                    </button>
                    <button class="quiz-btn ghost" on:click=move |_| run.update(HvRun::reset)>
                        {i18n::tr("Restart")}
                    </button>
                </div>
            </div>

            <div class="vl-card">
                <div class="vl-state">
                    <div>
                        <span class="s-label">{i18n::tr("guest sees")}</span>
                        <table class="vl-stat">
                            <tbody>
                                <tr><td>"acc"</td><td>{move || state(|s| s.acc.to_string())}</td></tr>
                                <tr><td>{i18n::tr("vif (virtual IF)")}</td><td>{move || state(|s| s.vif.to_string())}</td></tr>
                                <tr><td>"vcr3"</td><td>{move || state(|s| s.vcr3.to_string())}</td></tr>
                                <tr><td>{i18n::tr("IRQ queue")}</td><td>{move || run.with(|r| list(&r.session().state().queue))}</td></tr>
                                <tr><td>{i18n::tr("delivered")}</td><td>{move || run.with(|r| list(&r.session().state().delivered))}</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div>
                        <span class="s-label">{i18n::tr("real CPU")}</span>
                        <table class="vl-stat">
                            <tbody>
                                <tr><td>"IF"</td><td>{i18n::tr("always 1")}</td></tr>
                                <tr><td>"CR3"</td><td>{i18n::tr("monitor")}</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                {move || {
                    let title = run.with(|r| match r.session().inspect() {
                        Some(Inspection::Trap { title, .. }) => Some(title),
                        _ => None,
                    })?;
                    let options = run.with(HvRun::options);
                    Some(view! {
                        <div class="vl-trap">
                            <div class="vl-trap-t">{i18n::trf!("⚡ Trap: {0}", title)}</div>
                            <div class="vl-opts">
                                {options
                                    .into_iter()
                                    .map(|o| {
                                        let label = o.label.clone();
                                        view! { <button class="vl-opt" on:click=move |_| choose.run(label.clone())>{o.label}</button> }
                                    })
                                    .collect_view()}
                            </div>
                        </div>
                    })
                }}
                {move || run.with(|r| r.notice().cloned()).map(|n| view! { <p class={if n.bad { "vl-no" } else { "vl-yes" }}>{n.text}</p> })}
                {move || {
                    run.with(|r| r.session().finish().cloned())
                        .map(|f| {
                            let text = if f.ok {
                                i18n::trf!("✓ The program ran correctly (wrong choices: {0}).", f.mistakes)
                            } else {
                                i18n::tr("The program gave a wrong result: the monitor missed the POPF instruction and vif stayed 0. Enable binary translation and start over.")
                                    .to_string()
                            };
                            view! { <p class={if f.ok { "vl-yes" } else { "vl-no" }}>{text}</p> }
                        })
                }}
                {move || {
                    let log = run.with(|r| r.session().state().log.clone());
                    (!log.is_empty())
                        .then(|| view! { <ul class="vl-log">{log.into_iter().map(|l| view! { <li>{l}</li> }).collect_view()}</ul> })
                }}
            </div>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use virtlab::hv::default_programs;

    use super::*;

    fn program(id: &str) -> Program {
        default_programs().into_iter().find(|p| p.id == id).expect("program")
    }

    /// Passes a program with the correct options; returns the goal data.
    fn solve(run: &mut HvRun) -> Option<Value> {
        for _ in 0..40 {
            match run.session().inspect() {
                None => break,
                Some(Inspection::Direct | Inspection::Silent { .. }) => run.step(),
                Some(Inspection::Trap { options, .. }) => {
                    let ok = options.into_iter().find(|o| o.ok).expect("correct option");
                    if let Some(d) = run.choose(&ok.label) {
                        return Some(d);
                    }
                }
            }
        }
        None
    }

    #[test]
    fn ideal_run_reaches_goal_with_replayable_trace() {
        let _ru = locales::guard(i18n::Locale::Ru);
        for p in default_programs() {
            let mut run = HvRun::new(&p, p.id == "popf").expect("run");
            let info = solve(&mut run).unwrap_or_else(|| panic!("{}: goal not reached", p.id));
            // the solution, as the server reads it, is confirmed by replay
            let spec = virtlab::Spec::Hv { programs: default_programs() };
            let mut solution = serde_json::Map::new();
            solution.insert(p.id.clone(), info);
            let verdict = virtlab::verify(&spec, &Value::Object(solution));
            let status = verdict.goals.iter().find(|g| g.id == p.id).map(|g| g.status.clone());
            assert_eq!(status, Some(virtlab::GoalStatus::Verified), "{}", p.id);
        }
    }

    #[test]
    fn mistakes_are_counted_and_traced() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let p = program("base");
        let mut run = HvRun::new(&p, false).expect("run");
        run.step(); // ADD 3
        let Some(Inspection::Trap { options, .. }) = run.session().inspect() else { panic!("expected a trap") };
        let bad = options.iter().find(|o| !o.ok).expect("wrong option").clone();
        assert!(run.choose(&bad.label).is_none());
        assert_eq!(run.session().state().mistakes, 1);
        assert!(run.notice().is_some_and(|n| n.bad && n.text.starts_with("Нет: ")));
        let info = solve(&mut run).expect("goal");
        assert_eq!(info["mistakes"], 1);
        assert_eq!(info["translate"], false);
    }

    #[test]
    fn popf_without_translation_is_silent_and_not_a_goal() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let p = program("popf");
        let mut run = HvRun::new(&p, false).expect("run");
        assert!(solve(&mut run).is_none());
        assert!(run.session().finish().is_some_and(|f| !f.ok));
        // start over: translation stays off, the record and message are cleared
        run.reset();
        assert!(run.notice().is_none());
        assert!(!run.session().translate());
        assert!(run.session().current().is_some());
        // with translation the goal is reached
        run.set_translate(true);
        assert!(solve(&mut run).is_some());
    }

    #[test]
    fn step_is_blocked_on_trap() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut run = HvRun::new(&program("irq"), false).expect("run");
        assert!(!run.can_step(), "the first instruction is CLI, a trap");
        run.step();
        assert_eq!(run.session().state().pc, 0);
    }

    #[test]
    fn shuffle_is_a_stable_permutation() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let v: Vec<u32> = (0..6).collect();
        for seed in 0..20 {
            let s = shuffle(&v, seed);
            assert_eq!(s, shuffle(&v, seed));
            let mut sorted = s.clone();
            sorted.sort_unstable();
            assert_eq!(sorted, v);
        }
        assert!((0..20).any(|seed| shuffle(&v, seed) != v));
    }
}
