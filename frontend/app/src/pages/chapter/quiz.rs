//! Квиз на теорию: ответ проверяется на сервере сразу при выборе; верный ответ и пояснение приходят только после выбора.

use api::dto::{Quiz as QuizData, Reveal};
use leptos::{prelude::*, task::spawn_local};

use super::ChapterCtx;
use crate::{
    components::{
        fs_tree::{FsItem, ItemState},
        fullscreen::FsItems,
    },
    hooks::{client, use_load, Load},
    progress::ProgressStore,
};

/// Класс варианта после ответа: верный подсвечивается всегда, неверный выбор — красным.
pub fn option_class(reveal: Option<&Reveal>, pick: Option<usize>, option: usize) -> &'static str {
    match reveal {
        Some(r) if r.answer == option => "right",
        Some(_) if pick == Some(option) => "wrong",
        _ => "",
    }
}

/// Состояние вопроса в дереве полного экрана: без ответа — номер, верный ответ — ✓, неверный — ✗.
pub fn item_state(reveal: Option<&Reveal>, pick: Option<usize>) -> ItemState {
    match reveal {
        None => ItemState::Open,
        Some(r) if pick == Some(r.answer) => ItemState::Ok,
        Some(_) => ItemState::Bad,
    }
}

/// Прокручивает страницу к вопросу.
fn scroll_to_question(qi: usize) {
    if let Some(el) = web_sys::window().and_then(|w| w.document()).and_then(|d| d.get_element_by_id(&format!("quiz-q-{qi}"))) {
        el.scroll_into_view_with_bool(true);
    }
}

#[component]
pub fn Quiz() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    move || match ctx.chapter.get() {
        Load::Ready(ch) => view! { <QuizLoaded book=ctx.book num=ch.num /> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

#[component]
fn QuizLoaded(book: i64, num: i64) -> impl IntoView {
    let data = use_load(move || Some(()), move |c, _| async move { c.quiz(book, num).await });
    move || match data.get() {
        Load::Ready(q) => view! { <QuizBody book=book num=num quiz=q /> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

#[component]
fn QuizBody(book: i64, num: i64, quiz: QuizData) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let total = quiz.questions.len();
    let reveal = RwSignal::new(quiz.reveal.clone());
    let busy = RwSignal::new(false);
    let picks = Signal::derive(move || progress.quiz_picks(book, num));
    let answered = move || picks.get().iter().flatten().count();
    let score = move || progress.quiz_right(book, num);
    let pick = move |qi: usize, oi: usize| {
        if busy.get_untracked() || reveal.with_untracked(|r| r.get(qi).is_some_and(Option::is_some)) {
            return; // на вопрос уже ответили
        }
        busy.set(true);
        spawn_local(async move {
            if let Ok(r) = client().quiz_answer(book, num, qi, oi).await {
                reveal.update(|v| v[qi] = Some(Reveal { answer: r.answer, expl: r.expl }));
                progress.record_quiz_pick(book, num, qi, total, r.pick, r.right);
            }
            busy.set(false);
        });
    };
    let questions = quiz
        .questions
        .into_iter()
        .enumerate()
        .map(|(qi, q)| {
            let options = q
                .options
                .into_iter()
                .enumerate()
                .map(|(oi, text)| {
                    let class = move || format!("quiz-opt {}", option_class(reveal.with(|r| r[qi].clone()).as_ref(), picks.get().get(qi).copied().flatten(), oi));
                    view! { <button class=class disabled=move || busy.get() || reveal.with(|r| r[qi].is_some()) on:click=move |_| pick(qi, oi)>{text}</button> }
                })
                .collect_view();
            view! {
                <div class="quiz-q" id=format!("quiz-q-{qi}")>
                    <p class="quiz-q-text">{format!("{}. {}", qi + 1, q.q)}</p>
                    <div class="quiz-opts">{options}</div>
                    {move || reveal.with(|r| r[qi].clone()).filter(|r| !r.expl.is_empty()).map(|r| view! { <p class="quiz-q-expl">{r.expl}</p> })}
                </div>
            }
        })
        .collect_view();
    view! {
        <section class="quiz">
            <FsItems>
                {(0..total)
                    .map(|qi| {
                        let state = Signal::derive(move || item_state(reveal.with(|r| r[qi].clone()).as_ref(), picks.get().get(qi).copied().flatten()));
                        view! { <FsItem num=qi + 1 state=state on_click=Callback::new(move |()| scroll_to_question(qi))>{format!("Вопрос {}", qi + 1)}</FsItem> }
                    })
                    .collect_view()}
            </FsItems>
            <div class="quiz-head">
                <h3>{quiz.title}</h3>
                <span class="quiz-lang">{move || if answered() > 0 { format!("теория · {}/{}", score(), answered()) } else { "теория".to_string() }}</span>
            </div>
            {questions}
            {move || (answered() > 0).then(|| view! {
                <div class="quiz-actions">
                    <button class="quiz-btn ghost" on:click=move |_| { progress.reset_quiz(book, num); reveal.set(vec![None; total]) }>"Пройти ещё раз"</button>
                </div>
            })}
            {move || (answered() == total).then(|| view! {
                <div class=format!("quiz-result {}", if score() == total { "ok" } else { "fail" })>
                    <p class="quiz-ok-line">{if score() == total { format!("✓ Отлично: {}/{total}", score()) } else { format!("Результат: {}/{total}", score()) }}</p>
                </div>
            })}
        </section>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn question_item_shows_right_or_wrong_only_after_an_answer() {
        let r = Reveal { answer: 1, expl: String::new() };
        assert_eq!(item_state(None, None), ItemState::Open);
        assert_eq!(item_state(Some(&r), Some(1)), ItemState::Ok);
        assert_eq!(item_state(Some(&r), Some(0)), ItemState::Bad);
        assert_eq!(item_state(Some(&r), None), ItemState::Bad, "ответ раскрыт, а выбора в копии прогресса нет — не засчитываем");
    }

    #[test]
    fn right_option_is_always_marked_and_a_wrong_pick_is_red() {
        let r = Reveal { answer: 2, expl: String::new() };
        assert_eq!(option_class(Some(&r), Some(0), 2), "right");
        assert_eq!(option_class(Some(&r), Some(0), 0), "wrong");
        assert_eq!(option_class(Some(&r), Some(0), 1), "");
        assert_eq!(option_class(None, Some(0), 0), "", "пока не ответили — без подсветки");
    }
}
