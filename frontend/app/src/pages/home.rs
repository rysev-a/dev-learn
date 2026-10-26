//! Главная: общий прогресс по слайдам, вопросам и упражнениям и карточки разделов с тремя полосами.

use api::dto::Book;
use leptos::prelude::*;
use leptos_router::hooks::use_navigate;

use crate::{
    hooks::use_load,
    progress::ProgressStore,
};

/// Сумма чисел по главам книги в наборе счётчиков `книга → глава → число`.
fn book_total(counts: &api::dto::Counts, book: i64) -> usize {
    counts.get(&book.to_string()).map_or(0, |m| m.values().map(|n| usize::try_from(*n).unwrap_or(0)).sum())
}

/// Ключи прогресса `книга:глава` этой книги.
fn of_book<V>(map: &std::collections::HashMap<String, V>, book: i64) -> impl Iterator<Item = &V> + '_ {
    let prefix = format!("{book}:");
    map.iter().filter(move |(k, _)| k.starts_with(&prefix)).map(|(_, v)| v)
}

/// Уровень закраски квадратика главы: 0 — ничего не сделано, 3 — всё, 2 — не меньше половины, 1 — начато.
pub fn level(done: usize, all: usize) -> u8 {
    if done == 0 {
        0
    } else if done >= all {
        3
    } else if done * 2 >= all {
        2
    } else {
        1
    }
}

/// Полоса прогресса карточки: подпись, заполнение и «сделано/всего».
fn bar(label: &'static str, done: impl Fn() -> usize + Send + Sync + 'static + Copy, total: impl Fn() -> usize + Send + Sync + 'static + Copy) -> impl IntoView {
    view! {
        <div class="dash-bar">
            <span class="dash-bar-label">{label}</span>
            <div class="pr-bar"><i style=move || format!("width: {}%", pct(done(), total()))></i></div>
            <span class="dash-bar-num">{move || format!("{}/{}", done(), total())}</span>
        </div>
    }
}

/// Процент `done` от `all` (0, если всего нет).
pub fn pct(done: usize, all: usize) -> usize {
    (done * 100 + all / 2).checked_div(all).unwrap_or(0)
}

#[component]
pub fn Home(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let navigate = use_navigate();
    // сколько вопросов и упражнений в книгах: счётчики с сервера
    let quizzes = use_load(|| Some(()), |c, _| async move { c.quiz_counts().await });
    let answers = use_load(|| Some(()), |c, _| async move { c.answer_counts().await });
    let code = use_load(|| Some(()), |c, _| async move { c.code_counts().await });
    let quiz_total = move |book: i64| quizzes.get().ready().map_or(0, |c| book_total(c, book));
    let practice_total = move |book: i64| answers.get().ready().map_or(0, |c| book_total(c, book)) + code.get().ready().map_or(0, |c| book_total(c, book));
    // отвечено вопросов и решено упражнений (ответы и код)
    let quiz_done = move |book: i64| progress.data.with(|d| of_book(&d.quiz, book).map(|picks| picks.iter().flatten().count()).sum::<usize>());
    let practice_done = move |book: i64| {
        progress.data.with(|d| {
            of_book(&d.answers, book).map(|m| m.len()).sum::<usize>() + of_book(&d.code, book).map(|m| m.values().filter(|s| *s == "ok").count()).sum::<usize>()
        })
    };
    // главы всех книг — для квадратиков на карточках (по одному запросу на книгу, один раз)
    let courses = use_load(
        move || Some(books.get().iter().map(|b| b.id).collect::<Vec<_>>()).filter(|ids| !ids.is_empty()),
        |c, ids| async move {
            let mut out = Vec::new();
            for id in ids {
                out.push((id, c.course(id).await?));
            }
            Ok(out)
        },
    );
    // просмотрено слайдов в книге: прогресс хранится по (книга:глава), поэтому суммируем по префиксу
    let viewed = move |book: i64| progress.data.with(|d| d.slides.iter().filter(|(k, _)| k.split(':').next() == Some(&book.to_string())).map(|(_, v)| v.len()).sum::<usize>());
    // общий итог по трём видам: слайды, вопросы, упражнения
    let totals = move || {
        let ids: Vec<i64> = books.get().iter().map(|b| b.id).collect();
        let all: usize = books.get().iter().map(|b| b.parts_count as usize).sum::<usize>() + ids.iter().map(|b| quiz_total(*b) + practice_total(*b)).sum::<usize>();
        let done: usize = ids.iter().map(|b| viewed(*b) + quiz_done(*b) + practice_done(*b)).sum();
        (done, all)
    };
    view! {
        <main class="content home">
            <div class="dash-head">
                <h2>"Прогресс"</h2>
                <span class="dash-all">{move || { let (d, a) = totals(); format!("{}% · {d} из {a}", pct(d, a)) }}</span>
            </div>
            <h2 class="dash-sub">"Разделы"</h2>
            <div class="dash-grid">
                {move || {
                    books
                        .get()
                        .into_iter()
                        .map(|b| {
                            let (id, parts) = (b.id, b.parts_count as usize);
                            let navigate = navigate.clone();
                            let head_navigate = navigate.clone();
                            view! {
                                <section class="dash-card">
                                    <button class="dash-card-head" on:click=move |_| head_navigate(&format!("/book/{id}"), Default::default())>
                                        <span class="dash-title">{b.title.clone()}</span>
                                        <span class="dash-meta">{format!("{} уроков", b.lessons_count)}</span>
                                    </button>
                                    {bar("Слайды", move || viewed(id), move || parts)}
                                    {bar("Вопросы", move || quiz_done(id), move || quiz_total(id))}
                                    {bar("Упражнения", move || practice_done(id), move || practice_total(id))}
                                    <div class="dash-chapters" aria-label="Главы">
                                        {move || {
                                            let chapters = courses.get().ready().and_then(|all| all.iter().find(|(book, _)| *book == id)).map(|(_, sections)| sections.iter().flat_map(|s| s.chapters.clone()).collect::<Vec<_>>()).unwrap_or_default();
                                            chapters
                                                .into_iter()
                                                .map(|ch| {
                                                    let key = format!("{id}:{}", ch.num);
                                                    let count = |c: &Option<api::dto::Counts>| c.as_ref().and_then(|m| m.get(&id.to_string())).and_then(|m| m.get(&ch.num.to_string())).map_or(0, |n| usize::try_from(*n).unwrap_or(0));
                                                    let (q, a, k) = (count(&quizzes.get().ready().cloned()), count(&answers.get().ready().cloned()), count(&code.get().ready().cloned()));
                                                    let (slides, quiz, ex) = progress.data.with(|d| {
                                                        (
                                                            d.slides.get(&key).map_or(0, Vec::len),
                                                            d.quiz.get(&key).map_or(0, |p| p.iter().flatten().count()),
                                                            d.answers.get(&key).map_or(0, |m| m.len()) + d.code.get(&key).map_or(0, |m| m.values().filter(|s| *s == "ok").count()),
                                                        )
                                                    });
                                                    let (done, all) = (slides + quiz + ex, usize::try_from(ch.parts_count).unwrap_or(0) + q + a + k);
                                                    let navigate = navigate.clone();
                                                    let (chapter_id, num) = (ch.id, ch.num);
                                                    view! {
                                                        <button
                                                            class=format!("dash-ch l{}", level(done, all))
                                                            title=format!("{}. {} — слайды {slides}/{}, вопросы {quiz}/{q}, упражнения {ex}/{}", ch.num, ch.title, ch.parts_count, a + k)
                                                            on:click=move |_| navigate(&format!("/book/{id}/chapter/{chapter_id}"), Default::default())
                                                        >
                                                            {num}
                                                        </button>
                                                    }
                                                })
                                                .collect_view()
                                        }}
                                    </div>
                                </section>
                            }
                        })
                        .collect_view()
                }}
            </div>
        </main>
    }
}

#[cfg(test)]
mod tests {
    use super::pct;

    #[test]
    fn chapter_square_level_follows_the_share_done() {
        assert_eq!(super::level(0, 10), 0);
        assert_eq!(super::level(3, 10), 1);
        assert_eq!(super::level(5, 10), 2);
        assert_eq!(super::level(10, 10), 3);
        assert_eq!(super::level(0, 0), 0, "у главы без содержимого закраски нет");
    }

    #[test]
    fn percent_rounds_and_tolerates_empty() {
        assert_eq!(pct(0, 0), 0);
        assert_eq!(pct(1, 3), 33);
        assert_eq!(pct(2, 3), 67);
        assert_eq!(pct(5, 5), 100);
    }
}
