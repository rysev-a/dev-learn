//! Settings page: appearance is stored in the browser (`localStorage`) and applied immediately, progress and account - in the cabinet.

use api::dto::ResetScope;
use leptos::{prelude::*, task::spawn_local};

use crate::{
    components::aside::AsideState,
    hooks::client,
    player::Player,
    progress::ProgressStore,
    session::Session,
    settings::{self, Flag, Theme},
    themes,
};
use highlight::{highlight, Lang};

/// Texts of the reset row: title, explanation, confirmation question and button caption.
#[derive(Clone, Copy)]
struct ResetCopy {
    title: &'static str,
    text: &'static str,
    confirm: &'static str,
    button: &'static str,
}

fn reset_copy(scope: ResetScope) -> ResetCopy {
    match scope {
        ResetScope::Practice => ResetCopy {
            title: i18n::tr("Reset exercise progress"),
            text: i18n::tr("Deletes task statuses, code drafts and attempt history. Quiz answers and slides are not affected."),
            confirm: i18n::tr("Delete solutions, drafts and attempt history in all exercises?"),
            button: i18n::tr("Reset"),
        },
        ResetScope::All => ResetCopy {
            title: i18n::tr("Reset all progress"),
            text: i18n::tr("Resets the dashboard on the home page: viewed slides, quiz answers and exercises."),
            confirm: i18n::tr("Reset all progress: slides, quiz answers and exercises?"),
            button: i18n::tr("Reset everything"),
        },
    }
}

/// Browser confirmation; without a dialog (or on refusal) - "no".
fn confirm(question: &str) -> bool {
    web_sys::window().and_then(|w| w.confirm_with_message(question).ok()).unwrap_or(false)
}

#[component]
pub fn SettingsPage(theme: RwSignal<Theme>) -> impl IntoView {
    let aside = expect_context::<AsideState>();
    // which reset was just performed and how an unsuccessful one ended
    let done = RwSignal::new(None::<ResetScope>);
    let failure = RwSignal::new(None::<String>);
    view! {
        <main class="set-page">
            <section class="set-card">
                <h2>{i18n::tr("Settings")}</h2>
                <p class="set-sub">{i18n::tr("Appearance is stored in this browser and applied immediately; progress is stored in your account on the server.")}</p>

                <h3 class="set-group">{i18n::tr("Account")}</h3>
                <AccountRow />

                <h3 class="set-group">{i18n::tr("Appearance")}</h3>
                <SwitchRow
                    title=i18n::tr("Light theme")
                    text=i18n::tr("Switches the interface and slides between the dark and light palettes.")
                    on=Signal::derive(move || theme.get() == Theme::Light)
                    on_toggle=Callback::new(move |()| settings::switch_theme(theme, theme.get_untracked().toggled()))
                />
                <PalettePicker theme=theme />
                <SwitchRow
                    title=i18n::tr("Collapsed sections menu")
                    text=i18n::tr("Shows a column of icons instead of titles in the left menu. You can also toggle it with the button above the menu.")
                    on=Signal::derive(move || aside.is_collapsed())
                    on_toggle=Callback::new(move |()| aside.set(!aside.is_collapsed()))
                />

                <h3 class="set-group">{i18n::tr("Slides")}</h3>
                <FlagRow
                    flag=settings::ANIM_FLAG
                    title=i18n::tr("Autoplay animations")
                    text=i18n::tr("Diagrams on slides step through on a timer while the voice-over is off. If disabled, a diagram shows the final result at once and steps are switched by hand.")
                />

                <h3 class="set-group">{i18n::tr("Exercises")}</h3>
                <FlagRow
                    flag=settings::AUTO_NEXT_FLAG
                    title=i18n::tr("Auto-advance to the next exercise")
                    text=i18n::tr("When a code check passes, the next exercise opens after a second (after the last one — the first exercise of the next chapter). Off by default: the solution stays on screen and you move on with the button or Ctrl+Enter.")
                />

                <h3 class="set-group">{i18n::tr("Diagrams")}</h3>
                <FlagRow
                    flag=settings::AUTOWIRE_LAB_FLAG
                    title=i18n::tr("Auto-wiring in “Computer Architecture”")
                    text=i18n::tr("While you drag a gate or block, matching pins of its neighbours are shown dashed and connect on their own when you release. If disabled, wires are drawn by hand only.")
                />
                <FlagRow
                    flag=settings::AUTOWIRE_SD_FLAG
                    title=i18n::tr("Auto-wiring in “System Design”")
                    text=i18n::tr("A new or dragged component connects to suitable neighbours by itself (dashed hint). If disabled, links are drawn from an output port to an input port by hand.")
                />

                <h3 class="set-group">{i18n::tr("Progress")}</h3>
                <ResetRow scope=ResetScope::Practice done=done failure=failure />
                <ResetRow scope=ResetScope::All done=done failure=failure />
                {move || failure.get().map(|e| view! { <p class="error">{e}</p> })}
            </section>
        </main>
    }
}

/// Who is signed in and the "Sign out" button.
#[component]
fn AccountRow() -> impl IntoView {
    let session = expect_context::<Session>();
    let player = expect_context::<Player>();
    let name = move || session.identity.get().map(|i| i.user.display()).unwrap_or_default();
    let email = move || session.identity.get().map(|i| i.user.email).unwrap_or_default();
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{name}</span>
                <span class="set-row-desc">{email}{i18n::tr(". Progress, answers and attempt history are stored in your account and available from any browser.")}</span>
            </div>
            <button
                class="quiz-btn ghost"
                on:click=move |_| {
                    player.stop();
                    session.logout(client());
                }
            >
                {i18n::tr("Sign out")}
            </button>
        </div>
    }
}

/// Code sample on the theme card: colors come from the card's variables (`data-palette`), as in the editor.
const SAMPLE: [&str; 3] = ["def total(xs):  # sum", "    return sum(xs) + 42", "print(\"total\", total([1, 2]))"];

/// Color theme choice: interface, slides and code editor. Cards show the theme live, the choice switches the light or dark mode too.
#[component]
fn PalettePicker(theme: RwSignal<Theme>) -> impl IntoView {
    let dark = RwSignal::new(settings::read_palette(Theme::Dark));
    let light = RwSignal::new(settings::read_palette(Theme::Light));
    let group = move |title: &'static str, mode: Theme, chosen: RwSignal<String>| {
        let cards = themes::of_mode(mode)
            .map(|p| {
                let id = p.id;
                let active = move || theme.get() == mode && chosen.get() == id;
                let code = SAMPLE
                    .iter()
                    .map(|line| {
                        let tokens = highlight(Lang::Python, line)
                            .into_iter()
                            .map(|t| match t.kind.css() {
                                Some(color) => view! { <span style=format!("color: {color}")>{t.text}</span> }.into_any(),
                                None => t.text.into_any(),
                            })
                            .collect_view();
                        view! { <div>{tokens}" "</div> }
                    })
                    .collect_view();
                view! {
                    <button
                        type="button"
                        class="palette-card"
                        class:on=active
                        data-palette=themes::card_id(p)
                        aria-pressed=move || active().to_string()
                        on:click=move |_| {
                            chosen.set(id.to_string());
                            settings::choose_palette(theme, mode, id);
                        }
                    >
                        <span class="palette-name">{i18n::tr(p.name)}</span>
                        <span class="palette-code">{code}</span>
                        <span class="palette-chips"><i style="background: var(--accent)"></i><i style="background: var(--green)"></i><i style="background: var(--amber)"></i><i style="background: var(--error)"></i><i style="background: var(--syn-keyword, var(--s-blue))"></i><i style="background: var(--syn-string, var(--s-amber))"></i></span>
                    </button>
                }
            })
            .collect_view();
        view! {
            <div class="palette-group">
                <span class="set-row-title">{title}</span>
                <div class="palette-grid">{cards}</div>
            </div>
        }
    };
    view! {
        <div class="set-row palette-row">
            <div class="set-row-text">
                <span class="set-row-title">{i18n::tr("Color theme")}</span>
                <span class="set-row-desc">{i18n::tr("Colors of the interface, slides and code editor. Picking a theme switches between light and dark mode; the theme is remembered separately for each mode.")}</span>
            </div>
            {group(i18n::tr("Dark themes"), Theme::Dark, dark)}
            {group(i18n::tr("Light themes"), Theme::Light, light)}
        </div>
    }
}

/// Row with a switch.
#[component]
fn SwitchRow(title: &'static str, text: &'static str, #[prop(into)] on: Signal<bool>, on_toggle: Callback<()>) -> impl IntoView {
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{title}</span>
                <span class="set-row-desc">{text}</span>
            </div>
            <button
                type="button"
                role="switch"
                aria-checked=move || on.get().to_string()
                aria-label=title
                class="set-switch"
                class:on=move || on.get()
                on:click=move |_| on_toggle.run(())
            >
                <i></i>
            </button>
        </div>
    }
}

/// Switch for a `localStorage` setting: the value is read on open, written on every click.
#[component]
fn FlagRow(flag: Flag, title: &'static str, text: &'static str) -> impl IntoView {
    let on = RwSignal::new(flag.read());
    let toggle = Callback::new(move |()| {
        let next = !on.get_untracked();
        flag.write(next);
        on.set(next);
    });
    view! { <SwitchRow title=title text=text on=on on_toggle=toggle /> }
}

/// Progress reset row: confirmation, server request, "Done" mark.
#[component]
fn ResetRow(scope: ResetScope, done: RwSignal<Option<ResetScope>>, failure: RwSignal<Option<String>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let copy = reset_copy(scope);
    let busy = RwSignal::new(false);
    let reset = move |_| {
        if busy.get_untracked() || !confirm(copy.confirm) {
            return;
        }
        busy.set(true);
        failure.set(None);
        spawn_local(async move {
            match progress.reset(scope).await {
                Ok(()) => done.set(Some(scope)),
                Err(e) => failure.set(Some(e.message)),
            }
            busy.set(false);
        });
    };
    view! {
        <div class="set-row">
            <div class="set-row-text">
                <span class="set-row-title">{copy.title}</span>
                <span class="set-row-desc">
                    {copy.text}
                    {move || (done.get() == Some(scope)).then(|| view! { <b class="set-done">{i18n::tr(" Done.")}</b> })}
                </span>
            </div>
            <button class="quiz-btn ghost" disabled=move || busy.get() on:click=reset>{copy.button}</button>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn each_reset_has_its_own_wording_and_asks_before_deleting() {
        let (practice, all) = (reset_copy(ResetScope::Practice), reset_copy(ResetScope::All));
        assert_ne!(practice.title, all.title);
        assert_ne!(practice.confirm, all.confirm);
        assert!(practice.confirm.ends_with('?') && all.confirm.ends_with('?'));
        assert!(practice.text.contains("Quiz answers and slides are not affected"), "exercise reset does not touch questions and slides");
    }
}
