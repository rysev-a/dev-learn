//! Результаты проверки кода: тесты, логи, история попыток.

use api::dto::{Attempt, RunResult, TestResult};
use leptos::prelude::*;
use serde_json::Value;

use super::sql_diff::SqlDiff;

/// Значение теста как текст: строки без кавычек, остальное — JSON.
pub fn show(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Null => String::new(),
        other => other.to_string(),
    }
}

/// Дата попытки `ДД.ММ, ЧЧ:ММ` из `2026-10-22T16:18:00+00:00`.
pub fn fmt_date(iso: &str) -> String {
    let (date, time) = iso.split_once('T').unwrap_or((iso, ""));
    let mut d = date.split('-').skip(1);
    let (month, day) = (d.next().unwrap_or(""), d.next().unwrap_or(""));
    format!("{day}.{month}, {}", time.chars().take(5).collect::<String>())
}

#[component]
pub fn Results(res: Signal<Option<RunResult>>, running: Signal<bool>, phase: Signal<String>) -> impl IntoView {
    view! {
        <div class="pr-res">
            {move || {
                if running.get() {
                    let p = phase.get();
                    return view! { <p class="pr-empty">{if p.is_empty() { i18n::tr("Queuing…").to_string() } else { p }}</p> }.into_any();
                }
                match res.get() {
                    None => view! {
                        <p class="pr-empty">
                            {i18n::tr("Press “Check” (Ctrl/Cmd+Enter): tests and run logs will appear here. Once a solution is accepted, Ctrl/Cmd+Enter goes to the next exercise.")}
                        </p>
                    }
                    .into_any(),
                    Some(r) => result_view(r).into_any(),
                }
            }}
        </div>
    }
}

fn test_view(k: usize, r: TestResult) -> impl IntoView {
    let details = (!r.ok).then(|| match &r.error {
        Some(e) => view! { <pre class="cx-error">{e.clone()}</pre> }.into_any(),
        None if r.is_rows() => view! { <SqlDiff rows=r.rows.clone() /> }.into_any(),
        None => {
            let got = show(&r.got);
            view! {
                <div class="pr-diff">
                    <div><span class="s-label">{i18n::tr("expected")}</span><pre>{show(&r.expected)}</pre></div>
                    <div><span class="s-label">{i18n::tr("got")}</span><pre>{if got.is_empty() { i18n::tr("(empty)").to_string() } else { got }}</pre></div>
                </div>
            }
            .into_any()
        }
    });
    view! {
        <li class=format!("pr-test {}", if r.ok { "ok" } else { "bad" })>
            <div class="pr-test-head">
                <span class="cx-mark">{if r.ok { "✓" } else { "✗" }}</span>
                <span>{i18n::trf!("test {}", k + 1)}</span>
                {r.args.clone().map(|a| view! { <code class="cx-args">{i18n::trf!("call {}", a)}</code> })}
            </div>
            {details}
        </li>
    }
}

fn result_view(res: RunResult) -> impl IntoView {
    let total = res.results.len();
    let passed = res.results.iter().filter(|r| r.ok).count();
    // в режиме «вывод» программа печатает в перехваченный поток: её вывод лежит в got единственного теста
    let program = if !res.stdout.is_empty() {
        res.stdout.clone()
    } else {
        match res.results.as_slice() {
            [one] if one.args.is_none() && one.error.is_none() => one.got.as_str().unwrap_or("").to_string(),
            _ => String::new(),
        }
    };
    let timeout = res.status == "timeout";
    let tests = res.results.into_iter().enumerate().map(|(k, r)| test_view(k, r)).collect_view();
    view! {
        <div class="pr-res-block">
            <div class="pr-res-head">
                <span class="s-label">{i18n::tr("tests")}</span>
                {(total > 0).then(|| view! { <span class=format!("pr-res-sum {}", if res.solved { "ok" } else { "bad" })>{i18n::trf!("{} of {}", passed, total)}</span> })}
            </div>
            {timeout.then(|| view! { <p class="ex-note">{i18n::tr("The check ran out of time — the code may contain an infinite loop.")}</p> })}
            {(total == 0 && !timeout).then(|| view! { <p class="pr-empty">{i18n::tr("The tests did not run — see the logs below.")}</p> })}
            <ul class="pr-tests">{tests}</ul>
        </div>
        <div class="pr-res-block">
            <div class="pr-res-head"><span class="s-label">{i18n::tr("run logs")}</span></div>
            {if program.is_empty() { view! { <p class="pr-empty">{i18n::tr("the program printed nothing")}</p> }.into_any() } else { view! { <pre class="pr-log">{program}</pre> }.into_any() }}
            {(!res.stderr.is_empty() && !timeout).then(|| view! { <pre class="cx-error">{i18n::tr_dyn(&res.stderr)}</pre> })}
        </div>
    }
}

/// История попыток: клик возвращает код в редактор.
#[component]
pub fn History(#[prop(into)] items: Signal<Vec<Attempt>>, #[prop(into)] current: Signal<String>, on_pick: Callback<String>) -> impl IntoView {
    move || {
        let list = items.get();
        if list.is_empty() {
            return ().into_any();
        }
        let n = list.len();
        let rows = list
            .into_iter()
            .enumerate()
            .map(|(i, a)| {
                let code = a.code.clone();
                let first = a.code.lines().find(|l| !l.trim().is_empty()).unwrap_or("").to_string();
                let on = {
                    let code = a.code.clone();
                    move || code == current.get()
                };
                view! {
                    <li>
                        <button class=format!("pr-hist-item {}", a.status) class:on=on title=i18n::tr("Restore this code in the editor") on:click=move |_| on_pick.run(code.clone())>
                            <span class="pr-hist-n">{format!("#{}", n - i)}</span>
                            <span class="pr-hist-mark">{if a.status == "ok" { "✓" } else { "✗" }}</span>
                            <span class="pr-hist-score">{format!("{}/{}", a.passed, a.total)}</span>
                            <span class="pr-hist-code">{first}</span>
                            <span class="pr-hist-time">{fmt_date(&a.created_at)}</span>
                        </button>
                    </li>
                }
            })
            .collect_view();
        view! {
            <div class="pr-hist">
                <div class="pr-res-head"><span class="s-label">{i18n::tr("attempt history")}</span><span class="pr-res-time">{n}</span></div>
                <ul class="pr-hist-list">{rows}</ul>
            </div>
        }
        .into_any()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn values_are_shown_without_json_quotes_for_strings() {
        assert_eq!(show(&json!("1991\n")), "1991\n");
        assert_eq!(show(&json!([1, 2])), "[1,2]");
        assert_eq!(show(&Value::Null), "");
    }

    #[test]
    fn attempt_date_is_day_month_and_time() {
        assert_eq!(fmt_date("2026-10-22T16:18:00+00:00"), "22.10, 16:18");
    }
}
