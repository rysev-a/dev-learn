//! Home: overall progress over slides, questions and exercises and section cards with three bars.

use api::dto::Book;
use leptos::prelude::*;
use leptos_router::hooks::use_navigate;

use crate::{
    hooks::use_load,
    progress::ProgressStore,
};

/// Sum of numbers over a book's chapters in a counter set `book -> chapter -> number`.
fn book_total(counts: &api::dto::Counts, book: i64) -> usize {
    counts.get(&book.to_string()).map_or(0, |m| m.values().map(|n| usize::try_from(*n).unwrap_or(0)).sum())
}

/// Progress keys `book:chapter` of this book.
fn of_book<V>(map: &std::collections::HashMap<String, V>, book: i64) -> impl Iterator<Item = &V> + '_ {
    let prefix = format!("{book}:");
    map.iter().filter(move |(k, _)| k.starts_with(&prefix)).map(|(_, v)| v)
}

/// Fill level of a chapter square: 0 - nothing done, 3 - all, 2 - at least half, 1 - started.
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

/// Card progress bar: caption, fill and "done/total".
fn bar(label: &'static str, done: impl Fn() -> usize + Send + Sync + 'static + Copy, total: impl Fn() -> usize + Send + Sync + 'static + Copy) -> impl IntoView {
    view! {
        <div class="dash-bar">
            <span class="dash-bar-label">{label}</span>
            <div class="pr-bar"><i style=move || format!("width: {}%", pct(done(), total()))></i></div>
            <span class="dash-bar-num">{move || format!("{}/{}", done(), total())}</span>
        </div>
    }
}

/// Percentage `done` of `all` (0 if there is nothing).
pub fn pct(done: usize, all: usize) -> usize {
    (done * 100 + all / 2).checked_div(all).unwrap_or(0)
}

#[component]
pub fn Home(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let navigate = use_navigate();
    // how many questions and exercises are in the books: counters from the server
    let quizzes = use_load(|| Some(()), |c, _| async move { c.quiz_counts().await });
    let answers = use_load(|| Some(()), |c, _| async move { c.answer_counts().await });
    let code = use_load(|| Some(()), |c, _| async move { c.code_counts().await });
    let quiz_total = move |book: i64| quizzes.get().ready().map_or(0, |c| book_total(c, book));
    let practice_total = move |book: i64| answers.get().ready().map_or(0, |c| book_total(c, book)) + code.get().ready().map_or(0, |c| book_total(c, book));
    // questions answered and exercises solved (answers and code)
    let quiz_done = move |book: i64| progress.data.with(|d| of_book(&d.quiz, book).map(|picks| picks.iter().flatten().count()).sum::<usize>());
    let practice_done = move |book: i64| {
        progress.data.with(|d| {
            of_book(&d.answers, book).map(|m| m.len()).sum::<usize>() + of_book(&d.code, book).map(|m| m.values().filter(|s| *s == "ok").count()).sum::<usize>()
        })
    };
    // chapters of all books - for the squares on the cards (one request per book, once)
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
    // slides viewed in a book: progress is stored by (book:chapter), so we sum by prefix
    let viewed = move |book: i64| progress.data.with(|d| d.slides.iter().filter(|(k, _)| k.split(':').next() == Some(&book.to_string())).map(|(_, v)| v.len()).sum::<usize>());
    // overall total over three kinds: slides, questions, exercises
    let totals = move || {
        let ids: Vec<i64> = books.get().iter().map(|b| b.id).collect();
        let all: usize = books.get().iter().map(|b| b.parts_count as usize).sum::<usize>() + ids.iter().map(|b| quiz_total(*b) + practice_total(*b)).sum::<usize>();
        let done: usize = ids.iter().map(|b| viewed(*b) + quiz_done(*b) + practice_done(*b)).sum();
        (done, all)
    };
    view! {
        <main class="content home">
            <div class="dash-head">
                <h2>{i18n::tr("Progress")}</h2>
                <span class="dash-all">{move || { let (d, a) = totals(); i18n::trf!("{}% · {} of {}", pct(d, a), d, a) }}</span>
            </div>
            <h2 class="dash-sub">{i18n::tr("Sections")}</h2>
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
                                        {(!b.in_language(i18n::locale().code())).then(|| view! { <span class="lang-tag" title=i18n::tr("Available in Russian only")>"RU"</span> })}
                                        <span class="dash-meta">{format!("{} {}", b.lessons_count, i18n::plural(b.lessons_count as u64, "lesson", "lessons"))}</span>
                                    </button>
                                    {bar(i18n::tr("Slides"), move || viewed(id), move || parts)}
                                    {bar(i18n::tr("Questions"), move || quiz_done(id), move || quiz_total(id))}
                                    {bar(i18n::tr("Exercises"), move || practice_done(id), move || practice_total(id))}
                                    <div class="dash-chapters" aria-label=i18n::tr("Chapters")>
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
                                                            title=i18n::trf!("{}. {} — slides {}/{}, questions {}/{}, exercises {}/{}", ch.num, ch.title, slides, ch.parts_count, quiz, q, ex, a + k)
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
        assert_eq!(super::level(0, 0), 0, "a chapter without content has no fill");
    }

    #[test]
    fn percent_rounds_and_tolerates_empty() {
        assert_eq!(pct(0, 0), 0);
        assert_eq!(pct(1, 3), 33);
        assert_eq!(pct(2, 3), 67);
        assert_eq!(pct(5, 5), 100);
    }
}
