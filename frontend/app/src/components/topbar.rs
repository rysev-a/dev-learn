//! Шапка: логотип, переключатель темы, пользователь и выход.

use leptos::prelude::*;
use leptos_router::hooks::{use_location, use_navigate};

use crate::{
    hooks::client,
    player::Player,
    session::Session,
    settings::{self, Theme},
};

/// Адрес страницы настроек.
pub const SETTINGS_PATH: &str = "/settings";

#[component]
pub fn ThemeButton(theme: RwSignal<Theme>) -> impl IntoView {
    view! {
        <button
            type="button"
            class="btn-icon"
            title=move || if theme.get() == Theme::Dark { "Светлая тема" } else { "Тёмная тема" }
            aria-label="Переключить тему"
            on:click=move |_| settings::switch_theme(theme, theme.get_untracked().toggled())
        >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                {move || {
                    if theme.get() == Theme::Dark {
                        view! { <circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /> }.into_any()
                    } else {
                        view! { <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" /> }.into_any()
                    }
                }}
            </svg>
        </button>
    }
}

#[component]
pub fn Topbar(theme: RwSignal<Theme>) -> impl IntoView {
    let session = expect_context::<Session>();
    let player = expect_context::<Player>();
    let navigate = use_navigate();
    let go_settings = navigate.clone();
    let location = use_location();
    let on_settings = move || location.pathname.get() == SETTINGS_PATH;
    let login = move || session.identity.get().map(|i| i.user.display()).unwrap_or_default();
    let email = move || session.identity.get().map(|i| i.user.email).unwrap_or_default();
    view! {
        <header class="topbar">
            <button class="logo" title="На главную" on:click=move |_| { player.stop(); navigate("/", Default::default()) }>"CS.Core"</button>
            <div class="topbar-right">
                <button
                    type="button"
                    class="btn-icon"
                    class:on=on_settings
                    title="Настройки"
                    aria-label="Настройки"
                    on:click=move |_| {
                        player.stop();
                        go_settings(SETTINGS_PATH, Default::default())
                    }
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
                        <circle cx="12" cy="12" r="3" />
                    </svg>
                </button>
                <ThemeButton theme=theme />
                <span class="user-chip" title=email>
                    <span class="user-ava">{move || login().chars().next().map(|c| c.to_uppercase().to_string()).unwrap_or_default()}</span>
                    {login}
                </span>
                <button type="button" class="btn-icon" title="Выйти" aria-label="Выйти из аккаунта" on:click=move |_| { player.stop(); session.logout(client()) }>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
                    </svg>
                </button>
            </div>
        </header>
    }
}
