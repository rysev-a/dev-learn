//! Mobile menu: on a narrow screen the books list and the chapter list are not drawn in the page; the burger in the header opens
//! a drawer with the books, and the open book shows its sections and chapters. On a wide screen the drawer and the burger are hidden by style.

use api::dto::Book;
use leptos::prelude::*;
use leptos_router::hooks::{use_location, use_navigate};

use super::aside::book_in_path;
use crate::{
    dom,
    hooks::{use_load, Load},
    player::Player,
};

/// The drawer state, shared by the burger and the drawer.
#[derive(Clone, Copy)]
pub struct MobileMenu {
    open: RwSignal<bool>,
}

impl MobileMenu {
    pub fn is_open(&self) -> bool {
        self.open.get()
    }

    pub fn toggle(&self) {
        self.open.update(|o| *o = !*o);
    }

    pub fn close(&self) {
        self.open.set(false);
    }
}

/// Creates the state (closed) and puts it into the context.
pub fn provide_mobile_menu() -> MobileMenu {
    let menu = MobileMenu { open: RwSignal::new(false) };
    provide_context(menu);
    menu
}

/// Chapter number from the address `/book/<id>/chapter/<chapter>/…` (the chapter id, not its order).
pub fn chapter_in_path(path: &str) -> Option<i64> {
    path.strip_prefix("/book/")?.split('/').nth(2)?.parse().ok()
}

/// Three-line button in the header; visible only on a narrow screen.
#[component]
pub fn Burger() -> impl IntoView {
    let menu = expect_context::<MobileMenu>();
    view! {
        <button type="button" class="btn-icon burger" title=i18n::tr("Menu") aria-label=i18n::tr("Menu") aria-expanded=move || menu.is_open().to_string() on:click=move |_| menu.toggle()>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M4 6h16M4 12h16M4 18h16" />
            </svg>
        </button>
    }
}

/// The drawer: books; the open book shows its chapters by section. A tap on a chapter opens it and closes the drawer.
#[component]
pub fn Drawer(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let menu = expect_context::<MobileMenu>();
    let player = expect_context::<Player>();
    let navigate = use_navigate();
    let location = use_location();
    let expanded = RwSignal::new(None::<i64>);
    let course = use_load(move || if menu.is_open() { expanded.get() } else { None }, |c, b| async move { c.course(b).await });

    // any navigation closes the drawer; opening it expands the current book
    Effect::new(move |_| {
        location.pathname.track();
        menu.close();
    });
    Effect::new(move |_| {
        if menu.is_open() {
            expanded.set(book_in_path(&location.pathname.get_untracked()));
        }
    });
    dom::on_window(leptos::ev::keydown, move |ev| {
        if ev.key() == "Escape" {
            menu.close();
        }
    });

    let chapters = move |book: i64| match course.get() {
        Load::Loading => view! { <p class="mm-note">{i18n::tr("Loading…")}</p> }.into_any(),
        Load::Failed(e) => view! { <p class="mm-note error">{e}</p> }.into_any(),
        Load::Ready(sections) => {
            let current = chapter_in_path(&location.pathname.get());
            sections
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
                                    class:on=current == Some(id)
                                    on:click=move |_| {
                                        player.stop();
                                        navigate(&format!("/book/{book}/chapter/{id}"), Default::default());
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
                .collect_view()
                .into_any()
        }
    };

    let rows = move || {
        books
            .get()
            .into_iter()
            .enumerate()
            .map(|(i, b)| {
                let id = b.id;
                let chapters = chapters.clone();
                let open = move || expanded.get() == Some(id);
                view! {
                    <div class="mm-book">
                        <button
                            class="slide-fs-toc-item mm-book-head"
                            class:on=move || book_in_path(&location.pathname.get()) == Some(id)
                            aria-expanded=move || open().to_string()
                            on:click=move |_| expanded.set(if open() { None } else { Some(id) })
                        >
                            <span class="slide-fs-toc-num">{format!("{:02}", i + 1)}</span>
                            <span class="slide-fs-toc-name">{b.title.clone()}</span>
                            {(!b.in_language(i18n::locale().code())).then(|| view! { <span class="lang-tag" title=i18n::tr("Available in Russian only")>"RU"</span> })}
                            <span class="fst-chev" class:open=open>"›"</span>
                        </button>
                        {move || open().then(|| view! { <div class="mm-chapters">{chapters(id)}</div> })}
                    </div>
                }
            })
            .collect_view()
    };

    view! {
        <div class="mm" class:open=move || menu.is_open()>
            <div class="mm-backdrop" on:click=move |_| menu.close()></div>
            <nav class="mm-panel" aria-label=i18n::tr("Contents")>
                <div class="mm-head">
                    <div class="s-label">{i18n::tr("Sections")}</div>
                    <button type="button" class="btn-icon mm-close" title=i18n::tr("Close menu") aria-label=i18n::tr("Close menu") on:click=move |_| menu.close()>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                            <path d="M6 6l12 12M18 6 6 18" />
                        </svg>
                    </button>
                </div>
                <div class="mm-body">{rows}</div>
            </nav>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::chapter_in_path;

    #[test]
    fn chapter_is_read_from_the_path() {
        assert_eq!(chapter_in_path("/book/12/chapter/159"), Some(159));
        assert_eq!(chapter_in_path("/book/13/chapter/161/questions"), Some(161));
        assert_eq!(chapter_in_path("/book/12"), None);
        assert_eq!(chapter_in_path("/settings"), None);
    }
}
