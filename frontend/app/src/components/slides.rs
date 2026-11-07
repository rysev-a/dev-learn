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
    /// recording in progress (or about to start: the jumps are off)
    pub on: Signal<bool>,
    /// the first moments of a recording: the microphone is on, the slide has not started - the button shows "loading"
    pub starting: Signal<bool>,
    /// start recording the shown slide or stop the one in progress
    pub toggle: Callback<()>,
    /// short status: "Saving...", "Saved: ...", microphone or server error
    pub status: Signal<Option<String>>,
    /// the "Recordings of this slide" window (opened by the burger next to "Play")
    pub menu: RwSignal<bool>,
    /// seconds left of the recording (the slide is shown for its reading time); `None` - not recording
    pub left: Signal<Option<f64>>,
}

fn record_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <circle cx="6" cy="6" r="4.5" class="rec-dot" />
        </svg>
    }
}

fn spinner_icon() -> impl IntoView {
    view! {
        <svg class="rec-spinner" width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
            <path d="M6 1.2a4.8 4.8 0 1 1-4.8 4.8" />
        </svg>
    }
}

fn back_icon() -> impl IntoView {
    view! {
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <rect x="1.5" y="1.5" width="1.6" height="9" rx="0.5" />
            <path d="M10.5 1.6v8.8L4.6 6z" />
        </svg>
    }
}

fn forward_icon() -> impl IntoView {
    view! {
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <path d="M1.5 1.6v8.8L7.4 6z" />
            <rect x="8.9" y="1.5" width="1.6" height="9" rx="0.5" />
        </svg>
    }
}

fn menu_icon() -> impl IntoView {
    view! {
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
            <path d="M4 6h16M4 12h16M4 18h16" />
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
    /// "Back": to the start of the slide, or to the previous one when already at the start
    on_back: Callback<()>,
    /// "Forward": to the next slide
    on_forward: Callback<()>,
    /// voice-over volume 0..1 and its change
    #[prop(into)]
    volume: Signal<f64>,
    on_volume: Callback<f64>,
) -> impl IntoView {
    // while the slider is dragged it shows the finger, and the rewind happens on release
    let scrub = RwSignal::new(None::<f64>);
    // the volume before mute: the speaker button returns to it
    let loud = StoredValue::new(1.0_f64);
    // pop-up at the top right while recording: the countdown to the end of the slide
    let timer = move || {
        record.map(|r| {
            view! {
                {move || {
                    r.left.get().map(|left| {
                        view! {
                            <div class="rec-timer" role="timer">
                                <span class="rec-timer-dot"></span>
                                <span class="rec-timer-label">{i18n::tr("Recording")}</span>
                                <span class="rec-timer-time">{fmt_time(left.ceil())}</span>
                            </div>
                        }
                    })
                }}
            }
        })
    };
    // the jumps are off while a slide is being recorded (they would break the recording)
    let recording = move || record.is_some_and(|r| r.on.get());
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
                <button
                    class="slide-btn slide-rec"
                    class:on=move || r.on.get() && !r.starting.get()
                    class:loading=move || r.starting.get()
                    disabled=move || r.starting.get()
                    aria-busy=move || r.starting.get().to_string()
                    on:click=move |_| r.toggle.run(())
                    title=move || if r.starting.get() { i18n::tr("Starting the recording…").to_string() } else if r.on.get() { i18n::tr("Stop recording").to_string() } else { i18n::trf!("Play and record a new voice-over of this slide ({})", i18n::locale().code().to_uppercase()) }
                >
                    {move || if r.starting.get() { spinner_icon().into_any() } else if r.on.get() { stop_icon().into_any() } else { record_icon().into_any() }}
                    <span>{move || if r.on.get() && !r.starting.get() { i18n::tr("Stop") } else { i18n::tr("Record") }}</span>
                </button>
                <button class="slide-btn slide-rec-menu" disabled=move || r.on.get() on:click=move |_| r.menu.set(true) title=i18n::tr("Recordings of this slide") aria-label=i18n::tr("Recordings of this slide")>
                    {menu_icon()}
                </button>
            })}
            <button class="slide-btn slide-skip" disabled=recording on:click=move |_| on_back.run(()) title=i18n::tr("Back: to the start of the slide, or to the previous one") aria-label=i18n::tr("Back: to the start of the slide, or to the previous one")>
                {back_icon()}
            </button>
            <button class="slide-btn" on:click=move |_| if playing.get() { on_pause.run(()) } else { on_play.run(()) } title=move || if playing.get() { i18n::tr("Pause") } else { i18n::tr("Play") }>
                {move || if playing.get() { pause_icon().into_any() } else { play_icon().into_any() }}
                <span>{move || if playing.get() { i18n::tr("Pause") } else { i18n::tr("Play") }}</span>
            </button>
            <button class="slide-btn slide-skip" disabled=move || { recording() || idx.get() + 1 >= count } on:click=move |_| on_forward.run(()) title=i18n::tr("Forward: to the next slide") aria-label=i18n::tr("Forward: to the next slide")>
                {forward_icon()}
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
            {timer()}
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
            {timer()}
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
