//! Header: logo, theme switch, user and sign out.

use leptos::prelude::*;
use leptos_router::hooks::{use_location, use_navigate};

use crate::{
    hooks::client,
    player::Player,
    session::Session,
    settings::{self, Theme},
};

/// Settings page address.
pub const SETTINGS_PATH: &str = "/settings";

#[component]
pub fn ThemeButton(theme: RwSignal<Theme>) -> impl IntoView {
    view! {
        <button
            type="button"
            class="btn-icon"
            title=move || if theme.get() == Theme::Dark { i18n::tr("Light theme") } else { i18n::tr("Dark theme") }
            aria-label=i18n::tr("Toggle theme")
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

/// Interface language switch: reloads the page because the texts are built once.
#[component]
pub fn LangSwitch() -> impl IntoView {
    let current = i18n::locale();
    view! {
        <div class="lang-switch" role="group" aria-label=i18n::tr("Language")>
            {i18n::Locale::ALL
                .map(|l| {
                    view! {
                        <button
                            type="button"
                            class="lang-btn"
                            class:on=move || l == current
                            title=l.native_name()
                            aria-pressed=move || (l == current).to_string()
                            on:click=move |_| {
                                if l != current {
                                    settings::switch_locale(l)
                                }
                            }
                        >
                            {l.code().to_uppercase()}
                        </button>
                    }
                })}
        </div>
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
            <button class="logo" title=i18n::tr("Home") on:click=move |_| { player.stop(); navigate("/", Default::default()) }>"CS.Core"</button>
            <div class="topbar-right">
                <button
                    type="button"
                    class="btn-icon"
                    class:on=on_settings
                    title=i18n::tr("Settings")
                    aria-label=i18n::tr("Settings")
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
                <LangSwitch />
                <ThemeButton theme=theme />
                <span class="user-chip" title=email>
                    <span class="user-ava">{move || login().chars().next().map(|c| c.to_uppercase().to_string()).unwrap_or_default()}</span>
                    {login}
                </span>
                <button type="button" class="btn-icon" title=i18n::tr("Sign out") aria-label=i18n::tr("Sign out of your account") on:click=move |_| { player.stop(); session.logout(client()) }>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
                    </svg>
                </button>
            </div>
        </header>
    }
}
