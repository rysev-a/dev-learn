//! Корень приложения: тема, сессия, прогресс, плеер, маршруты. Без входа приложение закрыто.

use leptos::prelude::*;
use leptos_router::{
    components::{ParentRoute, Route, Router, Routes},
    path,
};

use crate::{
    components::{
        aside::{provide_aside, Aside},
        topbar::Topbar,
    },
    hooks::{use_load, Load},
    pages::{
        auth::AuthPage,
        book::{BookLayout, ChaptersIndex},
        chapter::{ChapterLayout, Practice, Quiz, Theory},
        home::Home,
        settings::SettingsPage,
    },
    player::provide_player,
    progress::provide_progress,
    session::{provide_session, Session},
    settings::{self, Theme},
};

#[component]
pub fn App() -> impl IntoView {
    let theme = RwSignal::new(settings::read_theme());
    settings::apply_theme(theme.get_untracked());
    let session = provide_session();
    provide_progress(session);
    provide_aside();
    provide_player();
    view! {
        <Router>
            <Gate theme=theme />
        </Router>
    }
}

/// Пока узнаём, кто вошёл, — пустой экран; без входа — форма входа.
#[component]
fn Gate(theme: RwSignal<Theme>) -> impl IntoView {
    let session = expect_context::<Session>();
    view! {
        {move || {
            if !session.checked.get() {
                view! { <div class="boot">"Загрузка…"</div> }.into_any()
            } else if session.identity.get().is_none() {
                view! { <AuthPage theme=theme /> }.into_any()
            } else {
                view! { <Shell theme=theme /> }.into_any()
            }
        }}
    }
}

#[component]
fn Shell(theme: RwSignal<Theme>) -> impl IntoView {
    let progress = expect_context::<crate::progress::ProgressStore>();
    let books = use_load(|| Some(()), |c, _| async move { c.books().await });
    let list = Signal::derive(move || books.get().ready().cloned().unwrap_or_default());
    view! {
        {move || {
            if progress.ready.get() {
                view! {
                    <div class="app">
                        <Topbar theme=theme />
                        <div class="layout">
                            <Aside books=list />
                            <Routes fallback=|| view! { <main class="content"><p class="empty">"Страница не найдена"</p></main> }>
                                <Route path=path!("") view=move || view! { <Home books=list /> } />
                                <Route path=path!("settings") view=move || view! { <SettingsPage theme=theme /> } />
                                <ParentRoute path=path!("book/:book") view=move || view! { <BookLayout books=list /> }>
                                    <Route path=path!("") view=ChaptersIndex />
                                    <ParentRoute path=path!("chapter/:chapter") view=ChapterLayout>
                                        <Route path=path!("") view=Theory />
                                        <Route path=path!("questions") view=Quiz />
                                        <Route path=path!("exercises") view=Practice />
                                    </ParentRoute>
                                </ParentRoute>
                            </Routes>
                        </div>
                    </div>
                }
                .into_any()
            } else {
                view! { <div class="boot">"Загрузка…"</div> }.into_any()
            }
        }}
        {move || matches!(books.get(), Load::Failed(_)).then(|| view! { <p class="error">"Не удалось загрузить разделы"</p> })}
    }
}
