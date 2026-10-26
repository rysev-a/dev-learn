//! Лаборатория «HTML и CSS» (книга 11): ученик пишет разметку, стили или селектор, справа — живой предпросмотр, внизу — условия.
//!
//! Проверка — крейт `weblab` (общий с сервером): условия пересчитываются при каждой правке, а когда выполнены все, решение
//! один раз уходит на сервер (`LabProps::report`), и тот перепроверяет его тем же кодом. Предпросмотр — `iframe` с пустым
//! `sandbox`: скрипты в нём не выполняются.

use highlight::Lang;
use leptos::prelude::*;
use weblab::{Kind, Solution, Task};

use super::LabProps;
use crate::components::code_editor::CodeEditor;

/// Ширины окна предпросмотра: телефон, планшет, ноутбук.
const WIDTHS: [(u32, &str); 3] = [(360, "360"), (768, "768"), (1100, "1100")];

/// Документ для предпросмотра.
pub fn preview_doc(task: &Task, s: &Solution) -> String {
    match task.kind {
        Kind::Html => strip_scripts(&s.html),
        Kind::Css => with_style(&task.html, &s.css),
        // выбранные селектором элементы обводятся; неверный селектор ничего не обводит
        Kind::Selector => {
            let sel = s.css.trim();
            let rule = if sel.is_empty() || weblab::html::selector(sel).is_err() { String::new() } else { format!("{sel} {{ outline: 3px solid #e5484d !important; outline-offset: 2px !important; }}") };
            with_style(&task.html, &rule)
        }
    }
}

/// Скрипты в предпросмотре не работают (песочница) — вырезаем их, чтобы браузер не сыпал ошибками о блокировке.
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

/// `<style>` в начало документа (после `<head>`, если он есть).
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

/// Лаборатория выбранного упражнения.
#[component]
pub fn WebLab(props: LabProps) -> impl IntoView {
    let task: Task = match serde_json::from_value(props.task.spec.clone()) {
        Ok(t) => t,
        Err(e) => return view! { <p class="error">{format!("Неверное описание упражнения: {e}")}</p> }.into_any(),
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
    // решено — один раз отправить на сервер
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
        Kind::Html => ("Разметка", Lang::Html, Signal::derive(move || sol.with(|s| s.html.clone()))),
        Kind::Css => ("Стили", Lang::Css, Signal::derive(move || sol.with(|s| s.css.clone()))),
        Kind::Selector => ("Селектор", Lang::Css, Signal::derive(move || sol.with(|s| s.css.clone()))),
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
                <section class="lab-col">
                    <div class="lab-card">
                        <div class="lab-card-head">
                            <h3>{title}</h3>
                            <div class="lab-actions">
                                {has_hint.then(|| view! {
                                    <button type="button" class="quiz-btn ghost" on:click=move |_| hint_open.update(|o| *o = !*o)>
                                        {move || if hint_open.get() { "Скрыть подсказку" } else { "Подсказка" }}
                                    </button>
                                })}
                                <button type="button" class="quiz-btn ghost" on:click=restart>"Начать заново"</button>
                            </div>
                        </div>
                        {move || (has_hint && hint_open.get()).then(|| view! { <p class="ex-hint">{hint.clone()}</p> })}
                        <CodeEditor value=editor_value on_input=on_input on_run=Callback::new(|()| ()) lang=lang accepted=solved autofocus=false />
                    </div>
                    <div class="lab-card">
                        <div class="lab-card-head"><h3>"Условия"</h3></div>
                        <ul class="vl-goals">{items}</ul>
                        {move || solved.get().then(|| view! {
                            <p class="lab-ok">
                                "Решено. "
                                {move || has_next.get().then(|| view! { <button type="button" class="quiz-btn" on:click=move |_| on_next.run(())>"Дальше →"</button> })}
                            </p>
                        })}
                    </div>
                </section>
                <section class="lab-col">
                    <div class="lab-card">
                        <div class="lab-card-head">
                            <h3>"Предпросмотр"</h3>
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
                            <iframe class="web-frame" sandbox="" title="Предпросмотр" style=move || format!("width: {}px", width.get()) srcdoc=srcdoc></iframe>
                        </div>
                    </div>
                </section>
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
        assert_eq!(strip_scripts("<p>a</p><script src=x></script><p>b</p>"), "<p>a</p><p>b</p>");
        assert_eq!(strip_scripts("<SCRIPT>alert(1)</SCRIPT>тут"), "тут");
        assert_eq!(strip_scripts("<p>без скриптов</p>"), "<p>без скриптов</p>");
        assert_eq!(strip_scripts("до<script>не закрыт"), "до");
    }
}
