//! "Recordings of this slide" window (author tool, administrators only): the takes of the shown slide in the interface language, a choice of the
//! one that voices the slide (by default the first), a pronunciation check of each take (scores, the weak words and sounds) and a trash
//! button for each (it deletes at once, without a confirmation).

use api::dto::{AssessedWord, Assessment, Take, Takes};
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

fn check_icon() -> impl IntoView {
    view! {
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 12h3l3-8 4 16 3-8h5" />
        </svg>
    }
}

/// Below this score a word or a sound needs work; below `GOOD` it is acceptable but not good.
const WEAK: f64 = 60.0;
const GOOD: f64 = 80.0;

/// Colour class of a score.
fn level(score: f64) -> &'static str {
    if score >= GOOD {
        "ok"
    } else if score >= WEAK {
        "mid"
    } else {
        "low"
    }
}

/// What the speech service found wrong with a word, in words (`None` - nothing).
fn faults(w: &AssessedWord) -> Vec<&'static str> {
    let error = match w.error.as_str() {
        "Omission" => Some(i18n::tr("Skipped")),
        "Insertion" => Some(i18n::tr("Added")),
        "Mispronunciation" => Some(i18n::tr("Mispronounced")),
        _ => None,
    };
    let pause = match w.pause.as_str() {
        "UnexpectedBreak" => Some(i18n::tr("Pause in the wrong place")),
        "MissingBreak" => Some(i18n::tr("Pause missing")),
        _ => None,
    };
    error.into_iter().chain(pause).collect()
}

/// The result of a check: the scores, the text with the weak words marked, and the list of what to work on (the words with their weak sounds).
fn assessment_view(a: &Assessment, again: impl Fn() + Copy + 'static, busy: Signal<bool>) -> impl IntoView {
    let metrics: Vec<(&'static str, f64)> = [Some((i18n::tr("Pronunciation"), a.pron)), Some((i18n::tr("Accuracy"), a.accuracy)), Some((i18n::tr("Fluency"), a.fluency)), Some((i18n::tr("Completeness"), a.completeness)), a.prosody.map(|p| (i18n::tr("Prosody"), p))]
        .into_iter()
        .flatten()
        .collect();
    let scores = metrics.into_iter().map(|(name, v)| view! { <div class="rd-metric"><dt>{name}</dt><dd class=level(v)>{v.round().to_string()}</dd></div> }).collect_view();
    let text = a
        .words
        .iter()
        .map(|w| {
            let class = match (w.error.as_str(), level(w.accuracy)) {
                ("Omission", _) => "rd-w skip",
                ("Insertion", _) => "rd-w extra",
                (_, "ok") => "rd-w ok",
                (_, "mid") => "rd-w mid",
                _ => "rd-w low",
            };
            view! { <span class=class>{w.word.clone()}</span>" " }
        })
        .collect_view();
    let weak: Vec<AssessedWord> = a.words.iter().filter(|w| w.accuracy < GOOD || !faults(w).is_empty()).cloned().collect();
    let list = if weak.is_empty() {
        view! { <p class="rd-note">{i18n::tr("Nothing to fix: every word scores 80 or more.")}</p> }.into_any()
    } else {
        let items = weak
            .into_iter()
            .map(|w| {
                let tags = faults(&w).into_iter().map(|t| view! { <span class="rd-tag">{t}</span> }).collect_view();
                let sounds = w.phonemes.iter().filter(|p| p.accuracy < GOOD).map(|p| format!("/{}/ {}", p.phoneme, p.accuracy.round())).collect::<Vec<_>>().join("  ");
                let score = (w.error != "Omission").then(|| view! { <span class=format!("rd-weak-score {}", level(w.accuracy))>{w.accuracy.round().to_string()}</span> });
                view! {
                    <li class="rd-weak">
                        <span class="rd-weak-word">{w.word.clone()}</span>
                        {score}
                        {tags}
                        <span class="rd-weak-sounds">{sounds}</span>
                    </li>
                }
            })
            .collect_view();
        view! {
            <h4 class="rd-sub">{i18n::tr("Words to work on")}</h4>
            <ul class="rd-weak-list">{items}</ul>
        }
        .into_any()
    };
    view! {
        <div class="rd-detail">
            <dl class="rd-metrics">{scores}</dl>
            <p class="rd-text">{text}</p>
            {list}
            <button type="button" class="rd-again" disabled=move || busy.get() on:click=move |_| again()>{i18n::tr("Check again")}</button>
        </div>
    }
}

/// The window. `open` is shared with the button that opens it; `on_change` gets the slide and its state after every choice or deletion
/// (the page updates the sound of the slide from it).
#[component]
pub fn RecordsDialog(open: RwSignal<bool>, book: i64, chapter: i64, #[prop(into)] slide: Signal<usize>, on_change: Callback<(usize, Takes)>) -> impl IntoView {
    let state = RwSignal::new(None::<Takes>);
    let error = RwSignal::new(None::<String>);
    let busy = RwSignal::new(false);
    // the take whose check is running, and the one whose result is open
    let checking = RwSignal::new(None::<i64>);
    let expanded = RwSignal::new(None::<i64>);

    // the list is loaded when the window opens and when the shown slide changes
    Effect::new(move |_| {
        if !open.get() {
            return;
        }
        let i = slide.get();
        state.set(None);
        error.set(None);
        expanded.set(None);
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

    // the pronunciation check of a take: the result is saved with the take and opened under it
    let check = move |id: i64| {
        let i = slide.get_untracked();
        checking.set(Some(id));
        error.set(None);
        spawn_local(async move {
            match client().assess_record(book, chapter, i, id).await {
                Ok(a) => {
                    if slide.get_untracked() == i {
                        let _ = state.try_update(|s| s.iter_mut().flat_map(|s| s.takes.iter_mut()).filter(|t| t.id == id).for_each(|t| t.assessment = Some(a.clone())));
                        let _ = expanded.try_set(Some(id));
                    }
                }
                Err(e) => {
                    let _ = error.try_set(Some(e.message));
                }
            }
            let _ = checking.try_set(None);
        });
    };

    let rows = move || {
        let Some(Takes { takes, selected, .. }) = state.get() else { return view! { <p class="rd-note">{i18n::tr("Loading…")}</p> }.into_any() };
        if takes.is_empty() {
            return view! { <p class="rd-note">{i18n::tr("No recordings yet. Press Record to make one.")}</p> }.into_any();
        }
        takes
            .into_iter()
            .map(|Take { id, dur, at, assessment }| {
                let on = selected == Some(id);
                let running = move || checking.get() == Some(id);
                let open = move || expanded.get() == Some(id);
                let score = assessment.as_ref().map(|a| a.pron);
                let detail = assessment.map(|a| move || open().then(|| assessment_view(&a, move || check(id), Signal::derive(move || checking.get().is_some()))));
                view! {
                    <li class="rd-item">
                        <div class="rd-row" class:on=on>
                            <button class="rd-pick" disabled=move || busy.get() aria-pressed=on.to_string() title=i18n::tr("Use this recording for the voice-over") on:click=move |_| if !on { choose(id) }>
                                <span class="rd-radio" class:on=on></span>
                                <span class="rd-name">{i18n::trf!("Recording {}", id)}</span>
                                <span class="rd-meta">{fmt_time(dur)}" · "{when(at)}</span>
                            </button>
                            <button
                                class="rd-check"
                                class:open=open
                                disabled=move || busy.get() || checking.get().is_some()
                                aria-expanded=move || open().to_string()
                                title=i18n::tr("Check pronunciation")
                                aria-label=i18n::tr("Check pronunciation")
                                on:click=move |_| match score {
                                    Some(_) => expanded.update(|e| *e = if *e == Some(id) { None } else { Some(id) }),
                                    None => check(id),
                                }
                            >
                                {move || match (running(), score) {
                                    (true, _) => view! { <span class="rd-check-label">{i18n::tr("Checking…")}</span> }.into_any(),
                                    (false, Some(s)) => view! { <span class=format!("rd-score {}", level(s))>{s.round().to_string()}</span> }.into_any(),
                                    (false, None) => view! { {check_icon()}<span class="rd-check-label">{i18n::tr("Check pronunciation")}</span> }.into_any(),
                                }}
                            </button>
                            <button class="rd-del" disabled=move || busy.get() title=i18n::tr("Delete the recording") aria-label=i18n::tr("Delete the recording") on:click=move |_| remove(id)>
                                {trash_icon()}
                            </button>
                        </div>
                        {detail}
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
