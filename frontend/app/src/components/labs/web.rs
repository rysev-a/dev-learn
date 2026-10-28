//! HTML and CSS lab (book 11): the student writes markup, styles or a selector, with a live preview on the right and the conditions below.
//!
//! Checking is done by the `weblab` crate (shared with the server): the conditions are recomputed on every edit, and when all are met, the solution
//! is sent to the server once (`LabProps::report`), which re-checks it with the same code. The preview is an `iframe` with an empty
//! `sandbox`: scripts do not run in it.

use highlight::Lang;
use leptos::prelude::*;
use weblab::{Kind, Solution, Task};

use super::LabProps;
use crate::components::code_editor::CodeEditor;

/// Preview window widths: phone, tablet, laptop.
const WIDTHS: [(u32, &str); 3] = [(360, "360"), (768, "768"), (1100, "1100")];

/// Document for the preview.
pub fn preview_doc(task: &Task, s: &Solution) -> String {
    match task.kind {
        Kind::Html => strip_scripts(&s.html),
        Kind::Css => with_style(&task.html, &s.css),
        // elements chosen by the selector are outlined; an invalid selector outlines nothing
        Kind::Selector => {
            let sel = s.css.trim();
            let rule = if sel.is_empty() || weblab::html::selector(sel).is_err() { String::new() } else { format!("{sel} {{ outline: 3px solid #e5484d !important; outline-offset: 2px !important; }}") };
            with_style(&task.html, &rule)
        }
    }
}

/// Scripts do not work in the preview (sandbox), so we strip them to keep the browser from flooding the console with blocking errors.
fn strip_scripts(html: &str) -> String {
    let lower = html.to_lowercase();
    let (mut out, mut at) = (String::new(), 0);
    while let Some(i) = lower[at..].find("<script") {
        out.push_str(&html[at..at + i]);
        match lower[at + i..].find("</script>") {
            Some(j) => at += i + j + "</script>".len(),
            None => {
                at = html.len();
                break;
            }
        }
    }
    out.push_str(&html[at..]);
    out
}

/// Puts `<style>` at the start of the document (after `<head>`, if there is one).
fn with_style(html: &str, css: &str) -> String {
    let style = format!("<style>{css}</style>");
    match html.find("<head>") {
        Some(i) => format!("{}{style}{}", &html[..i + 6], &html[i + 6..]),
        None => format!("{style}{html}"),
    }
}

fn solution_json(s: &Solution) -> String {
    serde_json::to_string(s).unwrap_or_default()
}

/// Lab for the selected exercise.
#[component]
pub fn WebLab(props: LabProps) -> impl IntoView {
    let task: Task = match serde_json::from_value(props.task.spec.clone()) {
        Ok(t) => t,
        Err(e) => return view! { <p class="error">{i18n::trf!("Invalid exercise description: {0}", e)}</p> }.into_any(),
    };
    let kind = task.kind;
    let draft: Solution = serde_json::from_str(&props.draft.get_untracked()).unwrap_or_else(|_| Solution { html: task.starter_html.clone(), css: task.starter_css.clone() });
    let draft = if props.draft.get_untracked().is_empty() { Solution { html: task.starter_html.clone(), css: task.starter_css.clone() } } else { draft };
    let sol = RwSignal::new(draft);
    let width = RwSignal::new(WIDTHS[2].0);
    let hint_open = RwSignal::new(false);
    let reported = StoredValue::new(false);
    let task = StoredValue::new(task);
    let report = Memo::new(move |_| task.with_value(|t| sol.with(|s| weblab::verify(t, s))));
    let (solved, on_draft, on_report) = (props.solved, props.on_draft, props.report);
    // solved - send to the server once
    Effect::new(move |_| {
        let ok = report.with(|r| r.ok());
        if ok && !solved.get_untracked() && !reported.get_value() {
            reported.set_value(true);
            on_report.run(sol.with_untracked(solution_json));
        }
    });
    let edit_html = Callback::new(move |text: String| {
        sol.update(|s| s.html = text);
        on_draft.run(sol.with_untracked(solution_json));
    });
    let edit_css = Callback::new(move |text: String| {
        sol.update(|s| s.css = text);
        on_draft.run(sol.with_untracked(solution_json));
    });
    let restart = move |_| {
        let start = task.with_value(|t| Solution { html: t.starter_html.clone(), css: t.starter_css.clone() });
        sol.set(start);
        on_draft.run(sol.with_untracked(solution_json));
    };
    let (title, lang, editor_value): (&str, Lang, Signal<String>) = match kind {
        Kind::Html => (i18n::tr("Markup"), Lang::Html, Signal::derive(move || sol.with(|s| s.html.clone()))),
        Kind::Css => (i18n::tr("Styles"), Lang::Css, Signal::derive(move || sol.with(|s| s.css.clone()))),
        Kind::Selector => (i18n::tr("Selector"), Lang::Css, Signal::derive(move || sol.with(|s| s.css.clone()))),
    };
    let on_input = if kind == Kind::Html { edit_html } else { edit_css };
    let hint = props.task.hint.clone();
    let has_hint = !hint.is_empty();
    let srcdoc = move || task.with_value(|t| sol.with(|s| preview_doc(t, s)));
    let items = move || {
        report
            .get()
            .items
            .into_iter()
            .map(|i| {
                let ok = i.ok;
                view! {
                    <li class:ok=ok>
                        <span class="vl-gm">{if ok { "✓" } else { "○" }}</span>
                        <span>{i.text}{(!ok && !i.detail.is_empty()).then(|| view! { <em>{format!(" — {}", i.detail)}</em> })}</span>
                    </li>
                }
            })
            .collect_view()
    };
    let on_next = props.on_next;
    let has_next = props.has_next;
    view! {
        <div class="lab lab-web">
            <div class="lab-web-grid">
                    <div class="lab-card web-ed">
                        <div class="lab-card-head">
                            <h3>{title}</h3>
                            <div class="lab-actions">
                                {has_hint.then(|| view! {
                                    <button type="button" class="quiz-btn ghost" on:click=move |_| hint_open.update(|o| *o = !*o)>
                                        {move || if hint_open.get() { i18n::tr("Hide hint") } else { i18n::tr("Hint") }}
                                    </button>
                                })}
                                <button type="button" class="quiz-btn ghost" on:click=restart>{i18n::tr("Start over")}</button>
                            </div>
                        </div>
                        {move || (has_hint && hint_open.get()).then(|| view! { <p class="ex-hint">{hint.clone()}</p> })}
                        <CodeEditor value=editor_value on_input=on_input on_run=Callback::new(|()| ()) lang=lang accepted=solved autofocus=false />
                    </div>
                    <div class="lab-card web-co">
                        <div class="lab-card-head"><h3>{i18n::tr("Requirements")}</h3></div>
                        <ul class="vl-goals">{items}</ul>
                        {move || solved.get().then(|| view! {
                            <p class="lab-ok">
                                {i18n::tr("Solved. ")}
                                {move || has_next.get().then(|| view! { <button type="button" class="quiz-btn" on:click=move |_| on_next.run(())>{i18n::tr("Next →")}</button> })}
                            </p>
                        })}
                    </div>
                    <div class="lab-card web-pv">
                        <div class="lab-card-head">
                            <h3>{i18n::tr("Preview")}</h3>
                            <div class="lab-actions">
                                {WIDTHS.iter().map(|(w, label)| {
                                    let w = *w;
                                    view! {
                                        <button type="button" class="quiz-btn ghost" class:on=move || width.get() == w on:click=move |_| width.set(w)>{*label}</button>
                                    }
                                }).collect_view()}
                            </div>
                        </div>
                        <div class="web-frame-wrap">
                            <iframe class="web-frame" sandbox="" title=i18n::tr("Preview") style=move || format!("width: {}px", width.get()) srcdoc=srcdoc></iframe>
                        </div>
                    </div>
            </div>
        </div>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::strip_scripts;

    #[test]
    fn scripts_are_removed_from_the_preview() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(strip_scripts("<p>a</p><script src=x></script><p>b</p>"), "<p>a</p><p>b</p>");
        assert_eq!(strip_scripts("<SCRIPT>alert(1)</SCRIPT>here"), "here");
        assert_eq!(strip_scripts("<p>no scripts</p>"), "<p>no scripts</p>");
        assert_eq!(strip_scripts("before<script>unclosed"), "before");
    }
}
