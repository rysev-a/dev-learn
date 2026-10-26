//! Вход и регистрация (по email; имя — для профиля). Без входа приложение закрыто.

use leptos::{prelude::*, task::spawn_local};

use crate::{
    components::topbar::ThemeButton,
    hooks::client,
    session::Session,
    settings::Theme,
};

#[derive(Clone, Copy, PartialEq)]
enum Mode {
    Login,
    Register,
}

/// Временные пользователи — только в dev-сборке (`trunk serve`): в релизной сборке ни предзаполнения, ни кнопок.
const DEV: bool = cfg!(debug_assertions);
const QUICK: [&str; 2] = ["student", "programmer"];

#[component]
pub fn AuthPage(theme: RwSignal<Theme>) -> impl IntoView {
    let session = expect_context::<Session>();
    let mode = RwSignal::new(Mode::Login);
    let busy = RwSignal::new(false);
    let error = RwSignal::new(String::new());
    let email = RwSignal::new(if DEV { "student@mail.com".to_string() } else { String::new() });
    let password = RwSignal::new(if DEV { "student".to_string() } else { String::new() });
    let name = RwSignal::new(String::new());

    let submit = move |login_mode: bool, email: String, password: String, name: String| {
        if busy.get_untracked() {
            return;
        }
        busy.set(true);
        error.set(String::new());
        spawn_local(async move {
            let c = client();
            let res = if login_mode { session.login(&c, &email, &password).await } else { session.register(&c, &email, &name, &password).await };
            if let Err(e) = res {
                error.set(e.message);
            }
            busy.set(false);
        });
    };
    let on_submit = move |ev: leptos::ev::SubmitEvent| {
        ev.prevent_default();
        submit(mode.get_untracked() == Mode::Login, email.get_untracked(), password.get_untracked(), name.get_untracked());
    };
    let quick = move |who: &'static str| {
        let addr = format!("{who}@mail.com");
        email.set(addr.clone());
        password.set(who.to_string());
        submit(true, addr, who.to_string(), String::new());
    };
    let tab = move |m: Mode, label: &'static str| {
        view! {
            <button role="tab" aria-selected=move || (mode.get() == m).to_string() class="auth-tab" class:on=move || mode.get() == m on:click=move |_| { mode.set(m); error.set(String::new()) }>{label}</button>
        }
    };
    view! {
        <div class="auth-page">
            <header class="auth-top">
                <span class="auth-logo">"CS.Core"</span>
                <ThemeButton theme=theme />
            </header>
            <main class="auth-card">
                <div class="auth-tabs" role="tablist">{tab(Mode::Login, "Вход")}{tab(Mode::Register, "Регистрация")}</div>
                <form class="auth-form" on:submit=on_submit>
                    <label class="auth-field">
                        <span>"Email"</span>
                        <input type="email" autocomplete="email" required prop:value=move || email.get() on:input=move |ev| email.set(event_target_value(&ev)) />
                    </label>
                    {move || (mode.get() == Mode::Register).then(|| view! {
                        <label class="auth-field">
                            <span>"Имя"</span>
                            <input autocomplete="nickname" prop:value=move || name.get() on:input=move |ev| name.set(event_target_value(&ev)) />
                        </label>
                    })}
                    <label class="auth-field">
                        <span>"Пароль (не короче 8 символов)"</span>
                        <input type="password" autocomplete="current-password" required prop:value=move || password.get() on:input=move |ev| password.set(event_target_value(&ev)) />
                    </label>
                    {move || { let e = error.get(); (!e.is_empty()).then(|| view! { <p class="auth-error">{e}</p> }) }}
                    <button class="quiz-btn auth-submit" disabled=move || busy.get()>
                        {move || match (busy.get(), mode.get()) {
                            (true, Mode::Login) => "Входим…",
                            (true, Mode::Register) => "Регистрируем…",
                            (false, Mode::Login) => "Войти",
                            (false, Mode::Register) => "Зарегистрироваться",
                        }}
                    </button>
                    {DEV.then(|| view! {
                        <div class="auth-quick">
                            <span class="auth-quick-label">"Временно, для разработки"</span>
                            {QUICK.map(|who| view! { <button type="button" class="quiz-btn ghost" disabled=move || busy.get() on:click=move |_| quick(who)>{format!("войти как {who}")}</button> })}
                        </div>
                    })}
                </form>
            </main>
        </div>
    }
}
