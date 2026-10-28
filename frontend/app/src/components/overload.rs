//! Dialog about code-checking server overload: the service is under development and cannot yet handle a heavy load.

use leptos::prelude::*;

/// Minimum interval between showings of the dialog if it was closed (ms).
const QUIET_MS: f64 = 60_000.0;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Overload {
    /// the checking server does not respond or refused to enqueue (no worker, queue full)
    Unavailable,
    /// checking is running, but the queue is long
    Busy,
}

/// Dialog state: what to show and when it was last closed.
#[derive(Clone, Copy)]
pub struct OverloadState {
    kind: RwSignal<Option<Overload>>,
    closed_at: RwSignal<f64>,
}

impl OverloadState {
    pub fn new() -> Self {
        Self { kind: RwSignal::new(None), closed_at: RwSignal::new(f64::NEG_INFINITY) }
    }

    /// Show the dialog (unless it was closed within the last minute).
    pub fn raise(&self, kind: Overload) {
        if js_sys::Date::now() - self.closed_at.get_untracked() >= QUIET_MS {
            self.kind.set(Some(kind));
        }
    }

    pub fn close(&self) {
        self.kind.set(None);
        self.closed_at.set(js_sys::Date::now());
    }
}

impl Default for OverloadState {
    fn default() -> Self {
        Self::new()
    }
}

#[component]
pub fn OverloadNotice(state: OverloadState) -> impl IntoView {
    move || {
        state.kind.get().map(|kind| {
            let (title, text) = match kind {
                Overload::Unavailable => (i18n::tr("Code checking is unavailable right now"), i18n::tr("The service is still under development and cannot handle heavy load yet: the checking server is overloaded or not responding.")),
                Overload::Busy => (i18n::tr("Many people are checking code right now"), i18n::tr("The service is still under development and cannot handle heavy load yet: the queue is long, your solution will be checked, but you will have to wait.")),
            };
            view! {
                <aside class="overload" role="alertdialog" aria-labelledby="overload-title">
                    <button type="button" class="overload-x" aria-label=i18n::tr("Close") on:click=move |_| state.close()>"×"</button>
                    <h3 id="overload-title">{title}</h3>
                    <p>{text}</p>
                    <p>{i18n::tr("Please try again a little later: we are adding capacity. Theory, quizzes and in-browser labs work as usual.")}</p>
                    <div class="overload-actions">
                        <button type="button" class="quiz-btn" on:click=move |_| state.close()>{i18n::tr("Got it")}</button>
                    </div>
                </aside>
            }
        })
    }
}
