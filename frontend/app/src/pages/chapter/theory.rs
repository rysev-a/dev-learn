//! "Theory" tab: chapter slides with the player and the "Voice-over" window. For chapters not yet ported to Leptos - the lesson text.

use std::sync::Arc;

use api::dto::Chapter;
use content::Chapter as SlideChapter;
use leptos::{prelude::*, task::spawn_local};
use leptos_router::hooks::query_signal;
use scene::{provide_env, SceneEnv};

use super::ChapterCtx;
use crate::{
    components::{
        blocks::DataSlide,
        slides::{RecordCtl, SlidePanel},
        voice_popup::VoicePopup,
    },
    hooks::{client, use_load, Load},
    player::{estimate_seconds, locate, Player},
    progress::ProgressStore,
    recorder,
    session::Session,
    settings,
};

/// Chapter paragraph durations: voice-over if the file exists, otherwise the virtual clock.
pub fn durations(ch: &Chapter) -> Vec<f64> {
    ch.lessons.iter().map(|l| if l.dur > 0.0 { l.dur } else { estimate_seconds(&l.text) }).collect()
}

/// Sound of the paragraphs: the file address if it exists (the server gives `dur` > 0 only for a file), otherwise `None` - the paragraph is read silently.
pub fn sounds(ch: &Chapter) -> Vec<Option<String>> {
    ch.lessons.iter().map(|l| (l.dur > 0.0).then(|| l.audio.clone())).collect()
}

/// Position in the chapter: sum of paragraphs before the shown one plus the time within it.
pub fn chapter_position(durations: &[f64], shown: usize, inside: Option<f64>) -> f64 {
    durations.iter().take(shown).sum::<f64>() + inside.unwrap_or(0.0)
}

/// Chapter slides: data from the backend; a chapter without slides shows the lesson text.
#[component]
pub fn Theory() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    let book = ctx.book;
    let chapter = ctx.chapter;
    let slides = use_load(
        move || chapter.get().ready().map(|c| c.num),
        move |client, num| async move { client.slides(book, num).await },
    );
    move || match (chapter.get(), slides.get()) {
        (Load::Ready(ch), Load::Ready(Some(data))) => view! { <Slides book=book chapter=ch deck=Deck::data(data) /> }.into_any(),
        (Load::Ready(ch), Load::Ready(None)) => view! { <PlainText chapter=ch /> }.into_any(),
        (Load::Failed(e), _) | (_, Load::Failed(e)) => view! { <p class="error">{e}</p> }.into_any(),
        _ => view! { <p class="empty">{i18n::tr("Loading…")}</p> }.into_any(),
    }
}

/// Slide title in the fullscreen list: the short one (`short`) if set, otherwise the heading.
pub fn fs_title(short: Option<&str>, title: &str) -> String {
    short.filter(|s| !s.trim().is_empty()).unwrap_or(title).to_string()
}

/// Chapter slide deck: slide count, their titles for the fullscreen list, and the "slide i -> view" function.
#[derive(Clone)]
struct Deck {
    count: usize,
    titles: Vec<String>,
    frame: Arc<dyn Fn(usize) -> AnyView + Send + Sync>,
}

impl Deck {
    fn data(ch: SlideChapter) -> Self {
        let (rubric, slides) = (ch.rubric, ch.slides);
        let count = slides.len();
        Deck {
            count,
            titles: slides.iter().map(|s| fs_title(s.short.as_deref(), &s.title)).collect(),
            frame: Arc::new(move |i| view! { <DataSlide rubric=rubric.clone() n=i + 1 total=count slide=slides[i].clone() /> }.into_any()),
        }
    }
}

/// Chapter without slides on Leptos: the lesson text itself, by paragraphs.
#[component]
fn PlainText(chapter: Chapter) -> impl IntoView {
    let paragraphs = chapter.lessons.into_iter().map(|l| view! { <p class="s-hint">{l.text}</p> }).collect_view();
    view! {
        <p class="empty">{i18n::tr("This chapter has no slides yet. The lesson text:")}</p>
        {paragraphs}
    }
}

#[component]
fn Slides(book: i64, chapter: Chapter, deck: Deck) -> impl IntoView {
    let player = expect_context::<Player>();
    let progress = expect_context::<ProgressStore>();
    let count = deck.count;
    let titles = deck.titles;
    let (manual, set_manual) = query_signal::<usize>("slide");
    // durations and sound files of the paragraphs: a fresh recording replaces its entry without reloading the chapter
    let parts = RwSignal::new(durations(&chapter).into_iter().zip(sounds(&chapter)).collect::<Vec<(f64, Option<String>)>>());
    let durs = Signal::derive(move || parts.with(|p| p.iter().map(|x| x.0).collect::<Vec<f64>>()));
    let total = Signal::derive(move || durs.with(|d| d.iter().sum::<f64>()));
    let num = chapter.num;
    on_cleanup(move || player.stop());

    // the slide follows the paragraph being read, otherwise manual choice (it lives in the address: reload returns to the same slide)
    let idx = Memo::new(move |_| player.playing.get().or_else(|| manual.get()).unwrap_or(0).min(count - 1));
    let playing = Signal::derive(move || player.playing.get().is_some() && !player.paused.get());
    // the viewed slide goes to progress (dashboard on the home page)
    Effect::new(move |_| progress.mark_slide(book, num, idx.get()));

    let start_from = move |i: usize| {
        let (d, u): (Vec<f64>, Vec<Option<String>>) = parts.get_untracked().into_iter().unzip();
        player.start(d, u, i);
        set_manual.set(None);
    };
    // rewind to a place in the chapter: a stopped player starts from there, a paused one stays paused
    let on_seek = Callback::new(move |pos: f64| {
        let (d, u): (Vec<f64>, Vec<Option<String>>) = parts.get_untracked().into_iter().unzip();
        let (i, t) = locate(&d, pos);
        let was_paused = player.playing.get_untracked().is_some() && player.paused.get_untracked();
        player.start_at(d, u, i, t);
        set_manual.set(None);
        if was_paused {
            player.toggle_pause();
        }
    });
    // click on a slide: if the chapter is playing - start from this part, otherwise just show the slide
    let on_pick = {
        Callback::new(move |i: usize| {
            if player.playing.get_untracked().is_some() {
                if player.playing.get_untracked() == Some(i) && player.paused.get_untracked() {
                    player.toggle_pause();
                } else {
                    start_from(i);
                }
            } else {
                set_manual.set(Some(i));
            }
        })
    };
    // "Play + record" (administrators only): the slide plays from the current place, the microphone is recorded to a file on the server
    // (`media/records/<book>/<chapter>/<slide>`); recording ends with the "Stop" button or when the player leaves this slide -
    // then the player stops and the slide stays in place
    let record = {
        let session = expect_context::<Session>();
        let is_admin = session.identity.get_untracked().is_some_and(|i| i.roles.iter().any(|r| r == "admin"));
        let recording = RwSignal::new(None::<usize>);
        let status = RwSignal::new(None::<String>);
        let live = StoredValue::new_local(None::<recorder::Recording>);
        on_cleanup(move || {
            if let Some(Some(r)) = live.try_update_value(|v| v.take()) {
                r.cancel();
            }
        });
        let finish = move || {
            let Some(i) = recording.get_untracked() else { return };
            recording.set(None);
            // the end of a paragraph (or chapter) returns to the recorded slide; the choice of another slide is respected
            let back = match player.playing.get_untracked() {
                Some(j) if j != i + 1 => j,
                _ => i,
            };
            set_manual.set(Some(back));
            player.stop();
            player.silent.set(false);
            let Some(Some(rec)) = live.try_update_value(|v| v.take()) else { return };
            status.set(Some(i18n::tr("Saving the recording…").to_string()));
            rec.stop(move |blob| {
                // a WAV is rewound exactly and has a known length; from now on the slide is played with this sound
                recorder::to_wav(blob, move |file, secs| {
                    spawn_local(async move {
                        let msg = match client().upload_record(book, num, i, &file).await {
                            Ok((path, audio)) => {
                                if let Some(secs) = secs.filter(|s| *s > 0.0).filter(|_| !audio.is_empty()) {
                                    // the address already has `?lang=`; `v` makes the browser fetch the new file
                                    let url = format!("{audio}&v={}", js_sys::Date::now() as u64);
                                    let _ = parts.try_update(|p| {
                                        if let Some(x) = p.get_mut(i) {
                                            *x = ((secs * 10.0).round() / 10.0, Some(url));
                                        }
                                    });
                                }
                                i18n::trf!("Saved: {}", path)
                            }
                            Err(e) => e.message,
                        };
                        let _ = status.try_set(Some(msg));
                    })
                });
            });
        };
        Effect::new(move |_| {
            if let Some(i) = recording.get() {
                if player.playing.get() != Some(i) {
                    finish();
                }
            }
        });
        let start_from = start_from.clone();
        let toggle = Callback::new(move |()| {
            if recording.get_untracked().is_some() {
                return finish();
            }
            let i = idx.get_untracked();
            let start_from = start_from.clone();
            status.set(Some(i18n::tr("Microphone…").to_string()));
            recorder::start(move |res| match res {
                Ok(rec) => {
                    live.set_value(Some(rec));
                    status.set(None);
                    player.silent.set(true); // the old sound must not leak into the microphone
                    start_from(i);
                    recording.set(Some(i));
                }
                Err(e) => status.set(Some(e)),
            });
        });
        // the shown slide has an author's recording (not the generated voice-over) in the interface language
        let has = Signal::derive(move || parts.with(|p| p.get(idx.get()).and_then(|x| x.1.as_deref()).is_some_and(|u| u.starts_with("/api/records/"))));
        let delete = Callback::new(move |()| {
            let i = idx.get_untracked();
            let asked = web_sys::window().and_then(|w| w.confirm_with_message(i18n::tr("Delete the recording of this slide?")).ok()).unwrap_or(false);
            if !asked {
                return;
            }
            player.stop();
            status.set(None);
            spawn_local(async move {
                let msg = match client().delete_record(book, num, i).await {
                    Ok(()) => {
                        let _ = parts.try_update(|p| {
                            if let Some(x) = p.get_mut(i) {
                                *x = (0.0, None);
                            }
                        });
                        i18n::tr("Recording deleted").to_string()
                    }
                    Err(e) => e.message,
                };
                let _ = status.try_set(Some(msg));
            });
        });
        is_admin.then_some(RecordCtl { on: Signal::derive(move || recording.get().is_some()), toggle, status: status.into(), has, delete })
    };
    let on_play = Callback::new(move |()| {
        if player.playing.get_untracked().is_some() {
            if player.paused.get_untracked() {
                player.toggle_pause();
            }
        } else {
            start_from(manual.get_untracked().unwrap_or(0).min(count - 1));
        }
    });
    let on_pause = Callback::new(move |()| {
        if playing.get_untracked() {
            player.toggle_pause();
        }
    });

    let time = Signal::derive(move || {
        let shown = idx.get();
        let inside = player.audio_time(shown);
        (durs.with(|d| chapter_position(d, shown, inside)), total.get())
    });
    let stage = {
        let frame = deck.frame.clone();
        Callback::new(move |i: usize| {
            // scene environment: this slide's voice-over time and "no motion" mode
            provide_env(SceneEnv { audio_time: Signal::derive(move || player.audio_time(i)), motion_off: settings::motion_off() });
            frame(i)
        })
    };
    let lessons = chapter.lessons;
    let popup = move || {
        let i = idx.get();
        let lesson = lessons.iter().find(|l| l.ord == i)?;
        // the words go at the reading speed (14 characters per second), not at the speed of the recording: a recorded paragraph is
        // shorter or longer than the estimate, but the highlight runs the same way with and without sound
        let (text, d) = (lesson.text.clone(), estimate_seconds(&lesson.text));
        Some(view! { <VoicePopup text=text t=Signal::derive(move || player.audio_time(i)) d=d /> })
    };
    view! {
        <div>
            {popup}
            <SlidePanel idx=idx count=count titles=titles time=time playing=playing on_play=on_play on_pause=on_pause on_pick=on_pick stage=stage record=record on_seek=on_seek volume=player.volume on_volume=Callback::new(move |v| player.set_volume(v)) />
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn full_screen_list_prefers_the_short_title() {
        assert_eq!(fs_title(Some("Brief"), "Long slide title"), "Brief");
        assert_eq!(fs_title(None, "Title"), "Title");
        assert_eq!(fs_title(Some("  "), "Title"), "Title", "an empty short title is not shown");
    }

    #[test]
    fn position_is_the_sum_of_earlier_parts_plus_time_inside() {
        let d = [10.0, 20.0, 30.0];
        assert_eq!(chapter_position(&d, 0, None), 0.0);
        assert_eq!(chapter_position(&d, 2, None), 30.0);
        assert_eq!(chapter_position(&d, 2, Some(4.5)), 34.5);
        assert_eq!(chapter_position(&d, 9, None), 60.0, "a slide past the end does not break the sum");
    }
}
