//! Страница главы: заголовок и три вкладки (теория, вопросы, практика), каждая со своим адресом. Данные главы грузятся один раз
//! и отдаются вкладкам через контекст; при смене главы страница пересоздаётся целиком.

mod answers;
mod code;
mod practice;
mod quiz;
mod theory;

use api::dto::{Chapter, ChapterTasks};
use leptos::{portal::Portal, prelude::*};
use leptos_router::{
    components::{Outlet, A},
    hooks::{use_location, use_navigate, use_params_map},
};

use crate::{
    components::{
        fs_tree::FsTree,
        fullscreen::{chapter_href, provide_fullscreen, Fullscreen, Slots},
    },
    hooks::{use_load, Load},
    player::Player,
    progress::ProgressStore,
};

pub use answers::Answers;
pub use practice::Practice;
pub use quiz::Quiz;
pub use theory::Theory;

/// Данные открытой главы для вкладок.
#[derive(Clone, Copy)]
pub struct ChapterCtx {
    pub book: i64,
    pub chapter: ReadSignal<Load<Chapter>>,
    /// код-задачи главы по её номеру (404 — задач нет)
    pub tasks: ReadSignal<Load<ChapterTasks>>,
    pub quiz_count: Signal<usize>,
    pub answer_count: Signal<usize>,
}

fn count_of(counts: ReadSignal<Load<api::dto::Counts>>, book: i64, num: Option<i64>) -> usize {
    match (counts.get(), num) {
        (Load::Ready(c), Some(num)) => c.get(&book.to_string()).and_then(|b| b.get(&num.to_string())).copied().unwrap_or(0) as usize,
        _ => 0,
    }
}

/// Вкладка главы: адрес относительно главы, название, значок.
pub type Tab = (&'static str, &'static str, Option<String>);

/// Вкладки главы по её содержимому.
pub fn tabs(theory: bool, quiz: usize, practice: bool, solved: Option<(usize, usize)>) -> Vec<Tab> {
    let mut out = Vec::new();
    if theory {
        out.push(("", "Теория", None));
    }
    if quiz > 0 {
        out.push(("questions", "Вопросы", Some(quiz.to_string())));
    }
    if practice {
        out.push(("exercises", "Практика", solved.map(|(done, all)| format!("{done}/{all}"))));
    }
    out
}

#[component]
pub fn ChapterLayout() -> impl IntoView {
    // состояние полного экрана живёт, пока открыта любая глава: смена главы не выводит из полного экрана
    provide_fullscreen();
    let params = use_params_map();
    let book = Memo::new(move |_| params.read().get("book").and_then(|b| b.parse::<i64>().ok()).unwrap_or_default());
    let id = Memo::new(move |_| params.read().get("chapter").and_then(|c| c.parse::<i64>().ok()).unwrap_or_default());
    // пересоздаём всё внутри при смене книги или главы: у вкладок свежее состояние
    move || {
        let (book, id) = (book.get(), id.get());
        view! { <ChapterInner book=book id=id /> }
    }
}

#[component]
fn ChapterInner(book: i64, id: i64) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let fs = expect_context::<Fullscreen>();
    let chapter = use_load(move || Some(id), |c, id| async move { c.chapter(id).await });
    let quizzes = use_load(|| Some(()), |c, _| async move { c.quiz_counts().await });
    let answers = use_load(|| Some(()), |c, _| async move { c.answer_counts().await });
    let slide_chapters = use_load(|| Some(()), |c, _| async move { c.slide_index().await });
    let tasks = use_load(
        move || chapter.get().ready().map(|ch| ch.num),
        move |c, num| async move { c.code_tasks(book, num).await },
    );
    let num = Signal::derive(move || chapter.get().ready().map(|ch| ch.num));
    let quiz_count = Signal::derive(move || count_of(quizzes, book, num.get()));
    let answer_count = Signal::derive(move || count_of(answers, book, num.get()));
    provide_context(ChapterCtx { book, chapter, tasks, quiz_count, answer_count });
    Slots::provide();

    let tab_list = Memo::new(move |_| {
        let Some(ch) = chapter.get().ready().cloned() else { return Vec::new() };
        let solved = tasks.get().ready().map(|t| {
            let done = progress.data.with(|d| d.code.get(&api::dto::progress_key(book, ch.num)).map(|m| t.tasks.iter().filter(|x| m.get(&x.id).map(String::as_str) == Some("ok")).count()).unwrap_or(0));
            (done, t.tasks.len())
        });
        let practice = solved.is_some_and(|(_, all)| all > 0) || answer_count.get() > 0;
        tabs(slide_chapters.get().ready().is_some_and(|list| list.contains(&(book, ch.num))), quiz_count.get(), practice, solved.filter(|(_, all)| *all > 0))
    });
    view! {
        {move || {
            if fs.is_on() {
                // оболочка полного экрана поверх всей страницы, как `createPortal(…, document.body)` в React
                view! { <Portal><FsShell book=book id=id tabs=tab_list /></Portal> }.into_any()
            } else {
                view! { <PlainChapter book=book id=id tabs=tab_list /> }.into_any()
            }
        }}
    }
}

/// Содержимое открытой вкладки; пока глава грузится — заглушка.
#[component]
fn TabBody() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    move || match ctx.chapter.get() {
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
        Load::Failed(_) => view! { <p class="error">"Урок не найден"</p> }.into_any(),
        Load::Ready(_) => view! { <Outlet /> }.into_any(),
    }
}

/// Обычный вид: заголовок, вкладки (с кнопкой «Весь экран») и содержимое.
#[component]
fn PlainChapter(book: i64, id: i64, tabs: Memo<Vec<Tab>>) -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    view! {
        <div>
            {move || {
                ctx.chapter
                    .get()
                    .ready()
                    .cloned()
                    .map(|ch| view! {
                        <p class="crumbs">{ch.section}</p>
                        <h2>{format!("Урок {}. {}", ch.num, ch.title)}</h2>
                        <ChapterTabs book=book id=id tabs=tabs expand=true />
                    })
            }}
            <TabBody />
        </div>
    }
}

/// Полный экран: слева дерево содержания, справа шапка (название, вкладки, кнопки вкладки, «Свернуть») и содержимое.
#[component]
fn FsShell(book: i64, id: i64, tabs: Memo<Vec<Tab>>) -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    let fs = expect_context::<Fullscreen>();
    let slots = expect_context::<Slots>();
    let player = expect_context::<Player>();
    let navigate = use_navigate();
    let caption = move || ctx.chapter.get().ready().map(|ch| format!("Урок {}. {}", ch.num, ch.title)).unwrap_or_else(|| "…".to_string());
    // другая глава открывается с теории
    let open_chapter = Callback::new(move |target: i64| {
        player.stop();
        navigate(&chapter_href(book, target, "", true), Default::default());
    });
    view! {
        <div class="slide-fs">
            <FsTree chapter=id items=slots.items on_open=open_chapter />
            <div class="slide-fs-main">
                <div class="slide-fs-head">
                    <span class="slide-fs-caption">{caption}</span>
                    <ChapterTabs book=book id=id tabs=tabs expand=false />
                    <span class="slide-fs-slot" node_ref=slots.head></span>
                    <button class="slide-btn" title="Свернуть (Esc)" on:click=move |_| fs.set(false)>
                        <svg width="11" height="11" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
                            <path d="M2 2l10 10M12 2L2 12" />
                        </svg>
                        <span>"Свернуть"</span>
                    </button>
                </div>
                <div class="slide-fs-body">
                    <TabBody />
                </div>
            </div>
        </div>
    }
}

/// Вкладки главы; ссылки сохраняют полный экран. `expand` — кнопка «Весь экран» (только в обычном виде).
#[component]
fn ChapterTabs(book: i64, id: i64, tabs: Memo<Vec<Tab>>, expand: bool) -> impl IntoView {
    let fs = expect_context::<Fullscreen>();
    let location = use_location();
    let on_tab = move |sub: &'static str| {
        let path = location.pathname.get();
        let base = format!("/book/{book}/chapter/{id}");
        path.strip_prefix(&base).unwrap_or("").trim_matches('/') == sub
    };
    view! {
        <nav class="ch-tabs" aria-label="Разделы урока">
            {move || {
                tabs.get()
                    .into_iter()
                    .map(|(sub, label, badge)| {
                        let href = chapter_href(book, id, sub, fs.is_on());
                        view! { <A href=href attr:class=move || format!("ch-tab {}", if on_tab(sub) { "on" } else { "" })>{label}{badge.map(|b| view! { <span class="ch-tab-badge">{b}</span> })}</A> }
                    })
                    .collect_view()
            }}
            {expand.then(|| view! {
                <button class="ch-expand" title="Весь экран" aria-label="Развернуть на весь экран" on:click=move |_| fs.set(true)>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M5 1H1v4M9 1h4v4M5 13H1V9M9 13h4V9" />
                    </svg>
                </button>
            })}
        </nav>
    }
}

#[cfg(test)]
mod tests {
    use super::tabs;

    #[test]
    fn tabs_show_only_what_the_chapter_has() {
        assert!(tabs(false, 0, false, None).is_empty());
        let all = tabs(true, 5, true, Some((2, 9)));
        let names: Vec<_> = all.iter().map(|t| t.1).collect();
        assert_eq!(names, ["Теория", "Вопросы", "Практика"]);
        assert_eq!(all[1].2.as_deref(), Some("5"));
        assert_eq!(all[2].2.as_deref(), Some("2/9"));
        assert_eq!(tabs(false, 0, true, None)[0].2, None, "у практики без код-задач значка нет");
    }
}
