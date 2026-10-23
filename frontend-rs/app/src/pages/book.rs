//! Раздел (книга): меню уроков слева и вложенные страницы — список глав или глава.

use api::dto::{Book, Section};
use leptos::prelude::*;
use leptos_router::{
    components::Outlet,
    hooks::{use_navigate, use_params_map},
};

use crate::{
    hooks::{use_load, Load},
    player::Player,
};

/// Курс открытой книги — для вложенных страниц.
#[derive(Clone, Copy)]
pub struct BookCtx {
    pub book: Memo<i64>,
    pub course: ReadSignal<Load<Vec<Section>>>,
}

#[component]
pub fn BookLayout(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let params = use_params_map();
    let book = Memo::new(move |_| params.read().get("book").and_then(|b| b.parse::<i64>().ok()));
    let chapter_id = Memo::new(move |_| params.read().get("chapter").and_then(|c| c.parse::<i64>().ok()));
    let course = use_load(move || book.get(), |c, b| async move { c.course(b).await });
    let player = expect_context::<Player>();
    let navigate = use_navigate();
    provide_context(BookCtx { book: Memo::new(move |_| book.get().unwrap_or_default()), course });
    let title = move || books.get().into_iter().find(|b| Some(b.id) == book.get()).map(|b| b.title).unwrap_or_default();
    let menu = move || match course.get() {
        Load::Ready(sections) if !sections.is_empty() => {
            let groups = sections
                .into_iter()
                .map(|sec| {
                    let items = sec
                        .chapters
                        .into_iter()
                        .map(|ch| {
                            let (id, navigate) = (ch.id, navigate.clone());
                            view! {
                                <button
                                    class="slide-fs-toc-item"
                                    class:on=move || chapter_id.get() == Some(id)
                                    on:click=move |_| {
                                        player.stop();
                                        navigate(&format!("/book/{}/chapter/{id}", book.get_untracked().unwrap_or_default()), Default::default());
                                    }
                                >
                                    <span class="slide-fs-toc-num">{format!("{:02}", ch.num)}</span>
                                    <span class="slide-fs-toc-name">{ch.title}</span>
                                </button>
                            }
                        })
                        .collect_view();
                    view! { <div class="lessons-group"><div class="s-label lessons-sec">{sec.title}</div>{items}</div> }
                })
                .collect_view();
            view! { <aside class="lessons-menu"><div class="s-label">{title()}</div>{groups}</aside> }.into_any()
        }
        _ => ().into_any(),
    };
    view! {
        {menu}
        <main class="content"><Outlet /></main>
    }
}

/// Корень раздела: карточки глав по подразделам.
#[component]
pub fn ChaptersIndex() -> impl IntoView {
    let ctx = expect_context::<BookCtx>();
    let navigate = use_navigate();
    view! {
        {move || match ctx.course.get() {
            Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
            Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
            Load::Ready(sections) => sections
                .into_iter()
                .map(|sec| {
                    let cards = sec
                        .chapters
                        .into_iter()
                        .map(|ch| {
                            let (id, navigate) = (ch.id, navigate.clone());
                            view! {
                                <button class="topic-card" on:click=move |_| navigate(&format!("/book/{}/chapter/{id}", ctx.book.get_untracked()), Default::default())>
                                    <span class="topic-num">{format!("{:02}", ch.num)}</span>
                                    <span class="topic-name">{ch.title}</span>
                                    <span class="topic-meta">{format!("{} слайдов", ch.parts_count)}</span>
                                </button>
                            }
                        })
                        .collect_view();
                    view! { <section class="topics-sec"><h2 class="topics-title">{sec.title}</h2><div class="topics-grid">{cards}</div></section> }
                })
                .collect_view()
                .into_any(),
        }}
    }
}
