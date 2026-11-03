//! App root: theme, session, progress, player, routes. Without signing in the app is closed.

use leptos::prelude::*;
use leptos_router::{
    components::{ParentRoute, Route, Router, Routes},
    path,
};

use crate::{
    components::{
        aside::{provide_aside, Aside},
        mobile_menu::{provide_mobile_menu, Drawer},
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
    settings::init_locale();
    let theme = RwSignal::new(settings::read_theme());
    settings::apply_theme(theme.get_untracked());
    let session = provide_session();
    provide_progress(session);
    provide_aside();
    provide_mobile_menu();
    provide_player();
    view! {
        <Router>
            <Gate theme=theme />
        </Router>
    }
}

/// While we find out who signed in, an empty screen; without sign-in, the sign-in form.
#[component]
fn Gate(theme: RwSignal<Theme>) -> impl IntoView {
    let session = expect_context::<Session>();
    view! {
        {move || {
            if !session.checked.get() {
                view! { <div class="boot">{i18n::tr("Loading…")}</div> }.into_any()
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
                        <Drawer books=list />
                        <div class="layout">
                            <Aside books=list />
                            <Routes fallback=|| view! { <main class="content"><p class="empty">{i18n::tr("Page not found")}</p></main> }>
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
                view! { <div class="boot">{i18n::tr("Loading…")}</div> }.into_any()
            }
        }}
        {move || matches!(books.get(), Load::Failed(_)).then(|| view! { <p class="error">{i18n::tr("Could not load the sections")}</p> })}
    }
}
