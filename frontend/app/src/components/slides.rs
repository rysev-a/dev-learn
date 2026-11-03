//! Chapter slides: slide frame and viewing panel (header with player, scene, dots).

use leptos::prelude::*;

use super::{
    fs_tree::FsItem,
    fullscreen::{FsHead, FsItems, Fullscreen},
};
use crate::{dom, player::fmt_time};

fn play_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <path d="M2.5 1.2v9.6L10.5 6z" />
        </svg>
    }
}

fn pause_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <rect x="2" y="1.5" width="3" height="9" rx="0.8" />
            <rect x="7" y="1.5" width="3" height="9" rx="0.8" />
        </svg>
    }
}

/// "Play + record": plays the slide while recording the voice to a file on the server (author tool, administrators only).
#[derive(Clone, Copy)]
pub struct RecordCtl {
    /// recording in progress
    pub on: Signal<bool>,
    /// start recording the shown slide or stop the one in progress
    pub toggle: Callback<()>,
    /// short status: "Saving...", "Saved: ...", microphone or server error
    pub status: Signal<Option<String>>,
}

fn record_icon() -> impl IntoView {
    view! {
        <svg width="14" height="11" viewBox="0 0 15 12" fill="currentColor">
            <path d="M1 1.2v9.6L8.5 6z" />
            <circle cx="12.2" cy="6" r="2.4" class="rec-dot" />
        </svg>
    }
}

fn stop_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <rect x="2" y="2" width="8" height="8" rx="1" />
        </svg>
    }
}

fn volume_icon(level: f64) -> impl IntoView {
    view! {
        <svg width="14" height="12" viewBox="0 0 14 12" fill="currentColor">
            <path d="M1 4.2h2.4L6.6 1.5v9L3.4 7.8H1z" />
            {(level > 0.0).then(|| view! { <path d="M8.4 4a2.9 2.9 0 0 1 0 4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" /> })}
            {(level > 0.5).then(|| view! { <path d="M10 2.4a5.2 5.2 0 0 1 0 7.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" /> })}
        </svg>
    }
}

/// Slide number after an arrow key press: right and down go forward, left and up go back; other keys give `None`.
pub fn arrow_target(key: &str, idx: usize, count: usize) -> Option<usize> {
    match key {
        "ArrowRight" | "ArrowDown" => Some((idx + 1).min(count.saturating_sub(1))),
        "ArrowLeft" | "ArrowUp" => Some(idx.saturating_sub(1)),
        _ => None,
    }
}

/// Viewing panel: slide number, chapter time, "Play/Pause", the slide itself and switching dots. In fullscreen the header
/// moves into the shell header, slide titles into the left tree, and the scene takes the whole area; arrows flip slides.
#[component]
pub fn SlidePanel(
    /// the slide shown
    #[prop(into)]
    idx: Signal<usize>,
    count: usize,
    /// slide titles for the fullscreen list
    titles: Vec<String>,
    /// position and length of the chapter, seconds
    #[prop(into)]
    time: Signal<(f64, f64)>,
    #[prop(into)] playing: Signal<bool>,
    on_play: Callback<()>,
    on_pause: Callback<()>,
    on_pick: Callback<usize>,
    /// slide `i` on screen (recreated when the slide changes, like `key` in React)
    stage: Callback<usize, AnyView>,
    /// "Play + record" button next to "Play"; `None` - do not show
    record: Option<RecordCtl>,
    /// rewind to a place in the chapter, seconds from its start
    on_seek: Callback<f64>,
    /// voice-over volume 0..1 and its change
    #[prop(into)]
    volume: Signal<f64>,
    on_volume: Callback<f64>,
) -> impl IntoView {
    // while the slider is dragged it shows the finger, and the rewind happens on release
    let scrub = RwSignal::new(None::<f64>);
    // the volume before mute: the speaker button returns to it
    let loud = StoredValue::new(1.0_f64);
    let controls = move || {
        view! {
            <span class="slide-panel-num">{move || format!("{:02} / {count:02}", idx.get() + 1)}</span>
            <input
                class="slide-seek"
                type="range"
                min="0"
                max=move || time.get().1.to_string()
                step="0.1"
                aria-label=i18n::tr("Position in the chapter")
                prop:value=move || scrub.get().unwrap_or_else(|| time.get().0).to_string()
                on:input=move |ev| scrub.set(event_target_value(&ev).parse().ok())
                on:change=move |ev| {
                    scrub.set(None);
                    if let Ok(v) = event_target_value(&ev).parse() {
                        on_seek.run(v);
                    }
                }
            />
            <span class="s-time-mono">{move || { let (t, d) = time.get(); format!("{} / {}", fmt_time(t), fmt_time(d)) }}</span>
            {record.map(|r| view! {
                <span class="slide-rec-status" title=move || r.status.get().unwrap_or_default()>{move || r.status.get()}</span>
                <button class="slide-btn slide-rec" class:on=move || r.on.get() on:click=move |_| r.toggle.run(()) title=move || if r.on.get() { i18n::tr("Stop recording") } else { i18n::tr("Play and record the voice-over of this slide") }>
                    {move || if r.on.get() { stop_icon().into_any() } else { record_icon().into_any() }}
                    <span>{move || if r.on.get() { i18n::tr("Stop") } else { i18n::tr("Record") }}</span>
                </button>
            })}
            <button class="slide-btn" on:click=move |_| if playing.get() { on_pause.run(()) } else { on_play.run(()) } title=move || if playing.get() { i18n::tr("Pause") } else { i18n::tr("Play") }>
                {move || if playing.get() { pause_icon().into_any() } else { play_icon().into_any() }}
                <span>{move || if playing.get() { i18n::tr("Pause") } else { i18n::tr("Play") }}</span>
            </button>
            <span class="slide-vol">
                <button
                    class="slide-vol-btn"
                    title=move || { if volume.get() > 0.0 { i18n::tr("Mute") } else { i18n::tr("Unmute") } }
                    on:click=move |_| {
                        let v = volume.get_untracked();
                        if v > 0.0 {
                            loud.set_value(v);
                            on_volume.run(0.0);
                        } else {
                            on_volume.run(loud.get_value());
                        }
                    }
                >
                    {move || volume_icon(volume.get())}
                </button>
                <input
                    class="slide-vol-range"
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    aria-label=i18n::tr("Volume")
                    prop:value=move || volume.get().to_string()
                    on:input=move |ev| {
                        if let Ok(v) = event_target_value(&ev).parse() {
                            on_volume.run(v);
                        }
                    }
                />
            </span>
        }
    };
    // the mode is chosen at creation: when fullscreen changes the tab is recreated
    if expect_context::<Fullscreen>().is_on_untracked() {
        dom::on_window(leptos::ev::keydown, move |ev| {
            let typing = ev.target().and_then(|t| wasm_bindgen::JsCast::dyn_into::<web_sys::HtmlElement>(t).ok()).is_some_and(|el| matches!(el.tag_name().as_str(), "INPUT" | "TEXTAREA") || el.is_content_editable());
            if let (false, Some(i)) = (typing, arrow_target(&ev.key(), idx.get_untracked(), count)) {
                ev.prevent_default();
                on_pick.run(i);
            }
        });
        return view! {
            <FsHead>{controls()}</FsHead>
            <FsItems>
                {titles
                    .iter()
                    .enumerate()
                    .map(|(i, title)| {
                        let title = title.clone();
                        view! { <FsItem num=i + 1 on=Signal::derive(move || idx.get() == i) on_click=Callback::new(move |()| on_pick.run(i))>{title}</FsItem> }
                    })
                    .collect_view()}
            </FsItems>
            <div class="slide-fs-stage">{move || stage.run(idx.get())}</div>
        }
        .into_any();
    }
    let dots = (0..count)
        .map(|i| view! { <button class="slide-dot" class:on=move || idx.get() == i on:click=move |_| on_pick.run(i) title=i18n::trf!("Slide {}", i + 1)></button> })
        .collect_view();
    view! {
        <aside class="slide-panel">
            <div class="slide-panel-head">{controls()}</div>
            <div class="slide-stage">{move || stage.run(idx.get())}</div>
            <div class="slide-dots">{dots}</div>
        </aside>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::arrow_target;

    #[test]
    fn arrows_move_one_slide_and_stop_at_the_ends() {
        assert_eq!(arrow_target("ArrowRight", 2, 5), Some(3));
        assert_eq!(arrow_target("ArrowDown", 4, 5), Some(4), "do not go past the last");
        assert_eq!(arrow_target("ArrowLeft", 2, 5), Some(1));
        assert_eq!(arrow_target("ArrowUp", 0, 5), Some(0), "do not go before the first");
        assert_eq!(arrow_target("Enter", 2, 5), None);
        assert_eq!(arrow_target("ArrowRight", 0, 0), Some(0));
    }
}
