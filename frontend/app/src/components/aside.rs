//! Левое меню разделов (книг курса).

use api::dto::Book;
use leptos::prelude::*;
use leptos_router::hooks::{use_location, use_navigate};

use crate::{player::Player, settings};

/// Номер книги из адреса `/book/<id>/…`.
pub fn book_in_path(path: &str) -> Option<i64> {
    path.strip_prefix("/book/")?.split('/').next()?.parse().ok()
}

/// Меню свёрнуто в колонку иконок. Состояние общее: его меняют кнопка над меню и страница настроек.
#[derive(Clone, Copy)]
pub struct AsideState {
    collapsed: RwSignal<bool>,
}

impl AsideState {
    pub fn is_collapsed(&self) -> bool {
        self.collapsed.get()
    }

    /// Применяет сразу и запоминает в настройках.
    pub fn set(&self, collapsed: bool) {
        self.collapsed.set(collapsed);
        settings::ASIDE_FLAG.write(collapsed);
    }
}

/// Создаёт состояние меню из сохранённой настройки и кладёт его в контекст.
pub fn provide_aside() -> AsideState {
    let state = AsideState { collapsed: RwSignal::new(settings::ASIDE_FLAG.read()) };
    provide_context(state);
    state
}

#[component]
pub fn Aside(#[prop(into)] books: Signal<Vec<Book>>) -> impl IntoView {
    let navigate = use_navigate();
    let location = use_location();
    let player = expect_context::<Player>();
    let active = Memo::new(move |_| book_in_path(&location.pathname.get()));
    let aside = expect_context::<AsideState>();
    let collapsed = Memo::new(move |_| aside.is_collapsed());
    let items = move || {
        books
            .get()
            .into_iter()
            .enumerate()
            .map(|(i, b)| {
                let id = b.id;
                let navigate = navigate.clone();
                let open = move |_| {
                    player.stop();
                    navigate(&format!("/book/{id}"), Default::default());
                };
                if collapsed.get() {
                    let initial = b.title.chars().next().map(|c| c.to_uppercase().to_string()).unwrap_or_default();
                    view! { <button class="aside-icon" class:on=move || active.get() == Some(id) on:click=open title=b.title.clone()>{initial}</button> }.into_any()
                } else {
                    view! {
                        <button class="slide-fs-toc-item" class:on=move || active.get() == Some(id) on:click=open>
                            <span class="slide-fs-toc-num">{format!("{:02}", i + 1)}</span>
                            <span class="slide-fs-toc-name">{b.title}</span>
                        </button>
                    }
                    .into_any()
                }
            })
            .collect_view()
    };
    view! {
        <aside class="sidebar" class:collapsed=move || collapsed.get()>
            <div class="aside-head">
                {move || (!collapsed.get()).then(|| view! { <div class="s-label">"Разделы"</div> })}
                <button
                    class="aside-toggle"
                    title=move || if collapsed.get() { "Развернуть меню" } else { "Свернуть меню" }
                    aria-label="Свернуть или развернуть меню разделов"
                    on:click=move |_| aside.set(!collapsed.get_untracked())
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" />
                        <path d="M9 3v18" />
                        {move || if collapsed.get() { view! { <path d="m14 9 3 3-3 3" /> }.into_any() } else { view! { <path d="m16 15-3-3 3-3" /> }.into_any() }}
                    </svg>
                </button>
            </div>
            <nav class="menu">{items}</nav>
        </aside>
    }
}

#[cfg(test)]
mod tests {
    use super::book_in_path;

    #[test]
    fn book_is_read_from_the_path() {
        assert_eq!(book_in_path("/book/12"), Some(12));
        assert_eq!(book_in_path("/book/13/chapter/161/questions"), Some(13));
        assert_eq!(book_in_path("/"), None);
        assert_eq!(book_in_path("/book/x"), None);
    }
}
