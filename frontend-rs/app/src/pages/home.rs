//! Главная: общий прогресс по слайдам и карточки разделов.

use api::dto::Book;
use leptos::prelude::*;
use leptos_router::hooks::use_navigate;

use crate::progress::ProgressStore;

/// Процент `done` от `all` (0, если всего нет).
pub fn pct(done: usize, all: usize) -> usize {
    (done * 100 + all / 2).checked_div(all).unwrap_or(0)
}

#[component]
pub fn Home(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let navigate = use_navigate();
    // просмотрено слайдов в книге: прогресс хранится по (книга:глава), поэтому суммируем по префиксу
    let viewed = move |book: i64| progress.data.with(|d| d.slides.iter().filter(|(k, _)| k.split(':').next() == Some(&book.to_string())).map(|(_, v)| v.len()).sum::<usize>());
    let totals = move || {
        let all: usize = books.get().iter().map(|b| b.parts_count as usize).sum();
        let done: usize = books.get().iter().map(|b| viewed(b.id)).sum();
        (done, all)
    };
    view! {
        <main class="content home">
            <div class="dash-head">
                <h2>"Прогресс"</h2>
                <span class="dash-all">{move || { let (d, a) = totals(); format!("{}% · {d} из {a} слайдов", pct(d, a)) }}</span>
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
                            view! {
                                <section class="dash-card">
                                    <button class="dash-card-head" on:click=move |_| navigate(&format!("/book/{id}"), Default::default())>
                                        <span class="dash-title">{b.title.clone()}</span>
                                        <span class="dash-meta">{format!("{} уроков", b.lessons_count)}</span>
                                    </button>
                                    <div class="dash-bar">
                                        <span class="dash-bar-label">"Слайды"</span>
                                        <div class="pr-bar"><i style=move || format!("width: {}%", pct(viewed(id), parts))></i></div>
                                        <span class="dash-bar-num">{move || format!("{}/{parts}", viewed(id))}</span>
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
    fn percent_rounds_and_tolerates_empty() {
        assert_eq!(pct(0, 0), 0);
        assert_eq!(pct(1, 3), 33);
        assert_eq!(pct(2, 3), 67);
        assert_eq!(pct(5, 5), 100);
    }
}
