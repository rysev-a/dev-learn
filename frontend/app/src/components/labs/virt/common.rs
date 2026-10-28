//! Shared by the simulators: exercise goals (marking reached ones and one-time solution submission), the goal list,
//! number formatting.

use std::collections::BTreeMap;

use leptos::prelude::*;
use serde::Serialize;
use serde_json::Value;

/// Reached goals of the exercise: `id → data` (the same as `useGoals` in React).
///
/// When all goals are reached and the exercise is not solved yet, the solution is sent to the server once.
#[derive(Clone, Copy)]
pub struct Goals {
    done: RwSignal<BTreeMap<String, Value>>,
    reported: StoredValue<bool>,
    ids: StoredValue<Vec<String>>,
    solved: Signal<bool>,
    report: Callback<String>,
}

impl Goals {
    pub fn new(ids: Vec<String>, solved: Signal<bool>, report: Callback<String>) -> Self {
        Self {
            done: RwSignal::new(BTreeMap::new()),
            reported: StoredValue::new(false),
            ids: StoredValue::new(ids),
            solved,
            report,
        }
    }

    /// The goal is reached (or the exercise was already solved earlier).
    pub fn is_done(&self, id: &str) -> bool {
        self.solved.get() || self.done.with(|d| d.contains_key(id))
    }

    /// Mark a goal as reached; `info` is its data for server re-checking.
    pub fn mark(&self, id: &str, info: Value) {
        let mut solution = None;
        self.done.update(|d| {
            if !insert_goal(d, id, info) {
                return;
            }
            let all = self.ids.with_value(|ids| all_reached(ids, d));
            if all && !self.solved.get_untracked() && !self.reported.get_value() {
                self.reported.set_value(true);
                solution = Some(solution_json(d));
            }
        });
        if let Some(s) = solution {
            self.report.run(s);
        }
    }
}

/// Record a goal; `false` — it was already reached (the data does not change).
pub fn insert_goal(done: &mut BTreeMap<String, Value>, id: &str, info: Value) -> bool {
    if done.contains_key(id) {
        return false;
    }
    done.insert(id.to_string(), info);
    true
}

/// Whether all goals from the list are reached.
pub fn all_reached(ids: &[String], done: &BTreeMap<String, Value>) -> bool {
    ids.iter().all(|id| done.contains_key(id))
}

/// Solution for the server: JSON `{goal id: data}`.
pub fn solution_json(done: &BTreeMap<String, Value>) -> String {
    serde_json::to_string(done).unwrap_or_else(|_| "{}".to_string())
}

/// Goal data from any serializable value (on failure — `true`, like the "old client").
pub fn data<T: Serialize>(value: &T) -> Value {
    serde_json::to_value(value).unwrap_or(Value::Bool(true))
}

/// Goal data of simulators that record actions: `{trace: [...]}`.
pub fn trace_data<T: Serialize>(trace: &[T]) -> Value {
    data(&serde_json::json!({ "trace": trace }))
}

/// A goal in the "goals" list: text and an optional italic note.
#[derive(Clone)]
pub struct GoalItem {
    pub id: String,
    pub text: String,
    pub note: Option<String>,
}

impl GoalItem {
    pub fn new(id: impl Into<String>, text: impl Into<String>) -> Self {
        Self { id: id.into(), text: text.into(), note: None }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.note = Some(note.into());
        self
    }
}

/// Goal list with ✓ / ○ marks.
#[component]
pub fn GoalList(goals: Goals, items: Vec<GoalItem>) -> impl IntoView {
    let rows = items
        .into_iter()
        .map(|g| {
            let (a, b) = (g.id.clone(), g.id);
            view! {
                <li class:ok=move || goals.is_done(&a)>
                    <span class="vl-gm">{move || if goals.is_done(&b) { "✓" } else { "○" }}</span>
                    <span>{g.text} {g.note.map(|n| view! { <em>{format!(" — {n}")}</em> })}</span>
                </li>
            }
        })
        .collect_view();
    view! {
        <span class="s-label">{i18n::tr("goals")}</span>
        <ul class="vl-goals">{rows}</ul>
    }
}

/// Tab with its own number, a reached-goal mark and a name.
#[component]
pub fn Tab(
    title: String,
    id: String,
    index: usize,
    active: Signal<usize>,
    goals: Goals,
    on_pick: Callback<usize>,
) -> impl IntoView {
    let (a, b) = (id.clone(), id);
    view! {
        <button
            role="tab"
            aria-selected=move || if active.get() == index { "true" } else { "false" }
            class="vl-tab"
            class:on=move || active.get() == index
            class:ok=move || goals.is_done(&a)
            on:click=move |_| on_pick.run(index)
        >
            <span class="vl-tab-mark">{move || if goals.is_done(&b) { "✓" } else { "" }}</span>
            {title}
        </button>
    }
}

/// Integer in the Russian style: thousands separated by a non-breaking space, like `toLocaleString("ru-RU")`.
pub fn fmt_ru(n: f64) -> String {
    let r = n.round();
    let digits = format!("{}", r.abs() as u64);
    let mut out = String::new();
    for (i, c) in digits.chars().enumerate() {
        if i > 0 && (digits.len() - i) % 3 == 0 {
            out.push('\u{a0}');
        }
        out.push(c);
    }
    if r < 0.0 && r != 0.0 {
        out.insert(0, '-');
    }
    out
}

/// Percentage: `0.25` → `25%`.
pub fn pct(x: f64) -> String {
    format!("{}%", (x * 100.0).round() as i64)
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::*;

    #[test]
    fn solution_contains_every_goal_once() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mut done = BTreeMap::new();
        assert!(insert_goal(&mut done, "a", json!({"x": 1})));
        assert!(!insert_goal(&mut done, "a", json!({"x": 2})), "a repeated mark does not change the data");
        assert!(insert_goal(&mut done, "b", Value::Bool(true)));
        assert_eq!(solution_json(&done), r#"{"a":{"x":1},"b":true}"#);
    }

    #[test]
    fn reached_requires_all_ids() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let ids = vec!["a".to_string(), "b".to_string()];
        let mut done = BTreeMap::new();
        insert_goal(&mut done, "a", Value::Bool(true));
        assert!(!all_reached(&ids, &done));
        insert_goal(&mut done, "b", Value::Bool(true));
        assert!(all_reached(&ids, &done));
        assert!(!all_reached(&["c".to_string()], &done));
    }

    #[test]
    fn trace_goes_into_data() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let v = trace_data(&[virtlab::virtq::Action::Reap, virtlab::virtq::Action::Post { n: 3 }]);
        assert_eq!(v, json!({"trace": [{"op": "reap"}, {"op": "post", "n": 3}]}));
    }

    #[test]
    fn numbers_are_grouped_with_nbsp() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(fmt_ru(0.0), "0");
        assert_eq!(fmt_ru(999.0), "999");
        assert_eq!(fmt_ru(1000.0), "1\u{a0}000");
        assert_eq!(fmt_ru(1234567.4), "1\u{a0}234\u{a0}567");
        assert_eq!(fmt_ru(-15000.0), "-15\u{a0}000");
    }

    #[test]
    fn percent_rounds() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(pct(0.0), "0%");
        assert_eq!(pct(0.25), "25%");
        assert_eq!(pct(0.5), "50%");
        assert_eq!(pct(1.0), "100%");
    }
}
