//! Упражнения с вводом ответа: верные ответы знает только сервер, он же проверяет введённое; ответ показать нельзя, только подсказку.

use api::dto::PracticeSet;
use leptos::{prelude::*, task::spawn_local};

use super::ChapterCtx;
use crate::{
    hooks::{client, use_load, Load},
    progress::ProgressStore,
};

#[derive(Clone, Copy, PartialEq)]
enum Verdict {
    Open,
    Right,
    Wrong,
}

#[component]
pub fn Answers() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    move || match ctx.chapter.get() {
        Load::Ready(ch) => view! { <AnswersLoaded book=ctx.book num=ch.num /> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

#[component]
fn AnswersLoaded(book: i64, num: i64) -> impl IntoView {
    let data = use_load(move || Some(()), move |c, _| async move { c.practice_set(book, num).await });
    move || match data.get() {
        Load::Ready(set) => view! { <AnswersBody book=book num=num set=set /> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

#[component]
fn AnswersBody(book: i64, num: i64, set: PracticeSet) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let total = set.tasks.len();
    let solved_of = |i: usize| set.solved.get(&i.to_string()).cloned();
    let values = RwSignal::new((0..total).map(|i| solved_of(i).unwrap_or_default()).collect::<Vec<_>>());
    let verdicts = RwSignal::new((0..total).map(|i| if solved_of(i).is_some() { Verdict::Right } else { Verdict::Open }).collect::<Vec<_>>());
    let hints = RwSignal::new(vec![false; total]);
    let busy = RwSignal::new(false);
    let solved = move || verdicts.with(|v| v.iter().filter(|x| **x == Verdict::Right).count());

    let check = move |i: usize| {
        if busy.get_untracked() || verdicts.with_untracked(|v| v[i] == Verdict::Right) {
            return;
        }
        let value = values.with_untracked(|v| v[i].clone());
        if value.trim().is_empty() {
            return;
        }
        busy.set(true);
        spawn_local(async move {
            if let Ok(ok) = client().check_answer(book, num, i, &value).await {
                verdicts.update(|v| v[i] = if ok { Verdict::Right } else { Verdict::Wrong });
                if ok {
                    progress.record_answer(book, num, i, value.trim());
                }
            }
            busy.set(false);
        });
    };
    let rows = set
        .tasks
        .into_iter()
        .enumerate()
        .map(|(i, t)| {
            let hint = t.hint.clone();
            let class = move || {
                let tone = match verdicts.with(|v| v[i]) {
                    Verdict::Right => "right",
                    Verdict::Wrong => "wrong",
                    Verdict::Open => "",
                };
                format!("ex-input {tone}")
            };
            view! {
                <div class="quiz-q">
                    <p class="quiz-q-text">{format!("{}. {}", i + 1, t.q)}</p>
                    <div class="ex-row">
                        <input
                            class=class
                            placeholder="Ответ"
                            prop:value=move || values.with(|v| v[i].clone())
                            disabled=move || verdicts.with(|v| v[i] == Verdict::Right)
                            on:input=move |ev| {
                                values.update(|v| v[i] = event_target_value(&ev));
                                if verdicts.with_untracked(|v| v[i] == Verdict::Wrong) {
                                    verdicts.update(|v| v[i] = Verdict::Open); // новая правка снимает «неверно»
                                }
                            }
                            on:keydown=move |ev| if ev.key() == "Enter" { check(i) }
                        />
                        <button class="quiz-btn" title="Проверить" disabled=move || busy.get() || verdicts.with(|v| v[i] == Verdict::Right) on:click=move |_| check(i)>
                            {move || if verdicts.with(|v| v[i] == Verdict::Right) { "✓" } else { "Проверить" }}
                        </button>
                    </div>
                    {move || (verdicts.with(|v| v[i] == Verdict::Wrong)).then(|| view! { <p class="ex-note">"Пока неверно — попробуй ещё раз или загляни в подсказку."</p> })}
                    {(!hint.is_empty()).then(|| {
                        let hint = hint.clone();
                        view! {
                            <div class="ex-hint-row">
                                <button class="quiz-btn ghost small" on:click=move |_| hints.update(|h| h[i] = !h[i])>{move || if hints.with(|h| h[i]) { "Скрыть подсказку" } else { "Подсказка" }}</button>
                                {move || hints.with(|h| h[i]).then(|| view! { <p class="ex-hint">{hint.clone()}</p> })}
                            </div>
                        }
                    })}
                </div>
            }
        })
        .collect_view();
    view! {
        <section class="quiz">
            <div class="quiz-head">
                <h3>{set.title}</h3>
                <span class="quiz-lang">{move || if solved() > 0 { format!("упражнения · решено {}/{total}", solved()) } else { "упражнения".to_string() }}</span>
            </div>
            {rows}
            {move || (solved() > 0).then(|| view! {
                <div class="quiz-actions">
                    <button class="quiz-btn ghost" on:click=move |_| {
                        progress.reset_answers(book, num);
                        values.set(vec![String::new(); total]);
                        verdicts.set(vec![Verdict::Open; total]);
                        hints.set(vec![false; total]);
                    }>"Начать заново"</button>
                </div>
            })}
            {move || (solved() == total).then(|| view! { <div class="quiz-result ok"><p class="quiz-ok-line">{format!("✓ Все задачи решены: {}/{total}", solved())}</p></div> })}
        </section>
    }
}
