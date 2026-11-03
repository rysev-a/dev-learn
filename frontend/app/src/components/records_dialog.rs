//! "Recordings of this slide" window (author tool, administrators only): the takes of the shown slide in the interface language, a choice of the
//! one that voices the slide (by default the first) and a trash button for each (it deletes at once, without a confirmation).

use api::dto::{Take, Takes};
use leptos::{prelude::*, task::spawn_local};

use crate::{dom, hooks::client, player::fmt_time};

/// Date and time of a recording in the browser's format for the interface language.
fn when(at: u64) -> String {
    let date = js_sys::Date::new(&wasm_bindgen::JsValue::from_f64(at as f64 * 1000.0));
    date.to_locale_string(i18n::locale().code(), &wasm_bindgen::JsValue::UNDEFINED).into()
}

fn trash_icon() -> impl IntoView {
    view! {
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2M19 6l-1 14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1L5 6M10 11v6M14 11v6" />
        </svg>
    }
}

/// The window. `open` is shared with the button that opens it; `on_change` gets the slide and its state after every choice or deletion
/// (the page updates the sound of the slide from it).
#[component]
pub fn RecordsDialog(open: RwSignal<bool>, book: i64, chapter: i64, #[prop(into)] slide: Signal<usize>, on_change: Callback<(usize, Takes)>) -> impl IntoView {
    let state = RwSignal::new(None::<Takes>);
    let error = RwSignal::new(None::<String>);
    let busy = RwSignal::new(false);

    // the list is loaded when the window opens and when the shown slide changes
    Effect::new(move |_| {
        if !open.get() {
            return;
        }
        let i = slide.get();
        state.set(None);
        error.set(None);
        spawn_local(async move {
            let res = client().records(book, chapter, i).await;
            if slide.get_untracked() != i {
                return;
            }
            match res {
                Ok(t) => {
                    let _ = state.try_set(Some(t));
                }
                Err(e) => {
                    let _ = error.try_set(Some(e.message));
                }
            }
        });
    });
    dom::on_window(leptos::ev::keydown, move |ev| {
        if ev.key() == "Escape" && open.get_untracked() {
            open.set(false);
        }
    });

    // a request on a take: the result is the slide's new state
    let act = move |request: std::pin::Pin<Box<dyn std::future::Future<Output = Result<Takes, api::ApiError>>>>| {
        let i = slide.get_untracked();
        busy.set(true);
        error.set(None);
        spawn_local(async move {
            match request.await {
                Ok(t) => {
                    let _ = state.try_set(Some(t.clone()));
                    on_change.run((i, t));
                }
                Err(e) => {
                    let _ = error.try_set(Some(e.message));
                }
            }
            let _ = busy.try_set(false);
        });
    };
    let choose = move |id: i64| {
        let i = slide.get_untracked();
        act(Box::pin(async move { client().select_record(book, chapter, i, id).await }));
    };
    let remove = move |id: i64| {
        let i = slide.get_untracked();
        act(Box::pin(async move { client().delete_record(book, chapter, i, id).await }));
    };

    let rows = move || {
        let Some(Takes { takes, selected, .. }) = state.get() else { return view! { <p class="rd-note">{i18n::tr("Loading…")}</p> }.into_any() };
        if takes.is_empty() {
            return view! { <p class="rd-note">{i18n::tr("No recordings yet. Press Record to make one.")}</p> }.into_any();
        }
        takes
            .into_iter()
            .map(|Take { id, dur, at }| {
                let on = selected == Some(id);
                view! {
                    <li class="rd-row" class:on=on>
                        <button class="rd-pick" disabled=move || busy.get() aria-pressed=on.to_string() title=i18n::tr("Use this recording for the voice-over") on:click=move |_| if !on { choose(id) }>
                            <span class="rd-radio" class:on=on></span>
                            <span class="rd-name">{i18n::trf!("Recording {}", id)}</span>
                            <span class="rd-meta">{fmt_time(dur)}" · "{when(at)}</span>
                        </button>
                        <button class="rd-del" disabled=move || busy.get() title=i18n::tr("Delete the recording") aria-label=i18n::tr("Delete the recording") on:click=move |_| remove(id)>
                            {trash_icon()}
                        </button>
                    </li>
                }
            })
            .collect_view()
            .into_any()
    };

    view! {
        <div class="rd" class:open=move || open.get() role="dialog" aria-modal="true" aria-label=i18n::tr("Recordings of this slide")>
            <div class="rd-backdrop" on:click=move |_| open.set(false)></div>
            <div class="rd-panel">
                <div class="rd-head">
                    <h3>{i18n::tr("Recordings of this slide")}</h3>
                    <button type="button" class="btn-icon" title=i18n::tr("Close") aria-label=i18n::tr("Close") on:click=move |_| open.set(false)>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                            <path d="M6 6l12 12M18 6 6 18" />
                        </svg>
                    </button>
                </div>
                <ul class="rd-list">{rows}</ul>
                {move || error.get().map(|e| view! { <p class="rd-note error">{e}</p> })}
            </div>
        </div>
    }
}
