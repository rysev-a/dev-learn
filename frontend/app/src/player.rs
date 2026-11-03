//! Voice-over player. A paragraph with a sound file is played by an `<audio>` element and the slides follow its time; a paragraph without one
//! is "read" silently by a virtual clock at ~14 characters per second. Slides and scene step marks follow the clock either way.
//! The clock is a pure struct ([`Clock`]), the player is a thin wrapper over a timer and the audio element.

use gloo_timers::callback::Interval;
use leptos::prelude::*;
use wasm_bindgen::{closure::Closure, JsValue};
use web_sys::HtmlAudioElement;

pub const CHARS_PER_SECOND: f64 = 14.0;
const TICK_MS: u32 = 100;

/// How many seconds a paragraph is "read" (at least three).
pub fn estimate_seconds(text: &str) -> f64 {
    (text.chars().count() as f64 / CHARS_PER_SECOND).max(3.0)
}

/// Seconds as `m:ss`.
pub fn fmt_time(secs: f64) -> String {
    let s = secs.max(0.0).round() as u64;
    format!("{}:{:02}", s / 60, s % 60)
}

/// Part `pos` seconds from the start of the chapter: the paragraph index and the time inside it (past the end - the end of the last one).
pub fn locate(durations: &[f64], pos: f64) -> (usize, f64) {
    let mut left = pos.max(0.0);
    for (i, d) in durations.iter().enumerate() {
        if left < *d || i + 1 == durations.len() {
            return (i, left.min(*d));
        }
        left -= d;
    }
    (0, 0.0)
}

/// What happened during a clock tick.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Tick {
    Playing,
    /// paragraph finished, the next one started
    NextPart,
    /// the last paragraph finished
    Ended,
}

/// Paragraph queue clock: durations, the current paragraph and the time within it.
#[derive(Clone, Debug, PartialEq)]
pub struct Clock {
    pub durations: Vec<f64>,
    pub index: usize,
    pub t: f64,
}

impl Clock {
    pub fn new(durations: Vec<f64>, start: usize) -> Self {
        Self { index: start.min(durations.len().saturating_sub(1)), durations, t: 0.0 }
    }

    /// Starts `t` seconds into paragraph `start` (not past its end).
    pub fn at(durations: Vec<f64>, start: usize, t: f64) -> Self {
        let mut c = Self::new(durations, start);
        c.t = t.clamp(0.0, c.durations.get(c.index).copied().unwrap_or(0.0));
        c
    }

    /// `dt` seconds passed. At most one transition per tick: the remaining time is lost (a tick is a fraction of a second).
    pub fn tick(&mut self, dt: f64) -> Tick {
        self.t += dt;
        let dur = self.durations.get(self.index).copied().unwrap_or(0.0);
        if self.t < dur {
            return Tick::Playing;
        }
        if self.index + 1 < self.durations.len() {
            self.index += 1;
            self.t = 0.0;
            Tick::NextPart
        } else {
            self.t = dur;
            Tick::Ended
        }
    }
}

#[derive(Clone, Copy)]
pub struct Player {
    /// index of the paragraph (slide) being read now; `None` - the player is stopped
    pub playing: RwSignal<Option<usize>>,
    pub paused: RwSignal<bool>,
    /// seconds since the start of the current paragraph
    pub t: RwSignal<f64>,
    /// volume of the voice-over, 0..1
    pub volume: RwSignal<f64>,
    /// do not play recorded sound (the author is recording the voice over it)
    pub silent: RwSignal<bool>,
    /// sound of the paragraphs; `None` - the paragraph has no file and is read silently
    urls: StoredValue<Vec<Option<String>>>,
    audio: StoredValue<Option<HtmlAudioElement>, LocalStorage>,
    clock: StoredValue<Clock>,
    last: StoredValue<f64>,
    timer: StoredValue<Option<Interval>, LocalStorage>,
}

pub fn provide_player() -> Player {
    let p = Player {
        playing: RwSignal::new(None),
        paused: RwSignal::new(false),
        t: RwSignal::new(0.0),
        volume: RwSignal::new(crate::settings::read(crate::settings::VOLUME).and_then(|v| v.parse::<f64>().ok()).map_or(1.0, |v| v.clamp(0.0, 1.0))),
        silent: RwSignal::new(false),
        urls: StoredValue::new(Vec::new()),
        audio: StoredValue::new_local(None),
        clock: StoredValue::new(Clock::new(Vec::new(), 0)),
        last: StoredValue::new(0.0),
        timer: StoredValue::new_local(None),
    };
    provide_context(p);
    p
}

impl Player {
    /// Start reading from paragraph `from`: durations of all paragraphs in the chapter and their sound files (`None` - silent).
    pub fn start(&self, durations: Vec<f64>, urls: Vec<Option<String>>, from: usize) {
        self.start_at(durations, urls, from, 0.0);
    }

    /// The same from `t` seconds into the paragraph (rewinding).
    pub fn start_at(&self, durations: Vec<f64>, urls: Vec<Option<String>>, from: usize, t: f64) {
        let clock = Clock::at(durations, from, t);
        self.playing.set(Some(clock.index));
        self.t.set(clock.t);
        self.paused.set(false);
        self.urls.set_value(urls);
        self.sync_audio(clock.index, clock.t);
        self.clock.set_value(clock);
        self.last.set_value(js_sys::Date::now());
        let me = *self;
        self.timer.set_value(Some(Interval::new(TICK_MS, move || me.on_tick())));
    }

    /// The audio element, created on first use.
    fn element(&self) -> Option<HtmlAudioElement> {
        if let Some(a) = self.audio.get_value() {
            return Some(a);
        }
        let a = HtmlAudioElement::new().ok()?;
        a.set_preload("auto");
        self.audio.set_value(Some(a.clone()));
        Some(a)
    }

    /// Plays paragraph `index` from `t` if it has a sound file (otherwise stops the sound: the paragraph is read silently).
    fn sync_audio(&self, index: usize, t: f64) {
        let url = self.urls.with_value(|u| u.get(index).cloned().flatten());
        let Some(a) = self.audio.get_value().or_else(|| url.as_ref().and_then(|_| self.element())) else { return };
        let Some(url) = url.filter(|_| !self.silent.get_untracked()) else {
            let _ = a.pause();
            return;
        };
        a.set_volume(self.volume.get_untracked());
        // a short path is compared by the attribute: `src()` returns the absolute address
        if a.get_attribute("src").as_deref() != Some(&url) {
            a.set_src(&url);
        }
        a.set_current_time(t);
        if let Ok(p) = a.play() {
            // autoplay refused or the file is missing: the clock goes on by itself
            let ignore = Closure::once(|_: JsValue| {});
            let _ = p.catch(&ignore);
            ignore.forget();
        }
    }

    /// The sound is really playing now (not ended, not refused): then the slides follow its time.
    fn audio_running(&self, index: usize) -> Option<f64> {
        let has = self.urls.with_value(|u| u.get(index).is_some_and(Option::is_some)) && !self.silent.get_untracked();
        let a = self.audio.get_value().filter(|_| has)?;
        (!a.paused() && !a.ended()).then(|| a.current_time())
    }

    /// Sets the volume (0..1) and remembers it.
    pub fn set_volume(&self, v: f64) {
        let v = v.clamp(0.0, 1.0);
        self.volume.set(v);
        if let Some(a) = self.audio.get_value() {
            a.set_volume(v);
        }
        crate::settings::write(crate::settings::VOLUME, Some(&v.to_string()));
    }

    fn on_tick(&self) {
        if self.paused.get_untracked() {
            return;
        }
        let now = js_sys::Date::now();
        let mut dt = (now - self.last.get_value()) / 1000.0;
        self.last.set_value(now);
        let mut clock = self.clock.get_value();
        // the sound sets the time (the file is the source of truth); until it has started, the clock waits for it
        if let Some(ct) = self.audio_running(clock.index) {
            dt = (ct - clock.t).max(0.0);
        }
        let before = clock.index;
        let tick = clock.tick(dt);
        self.t.set(clock.t);
        self.playing.set(Some(clock.index));
        if clock.index != before {
            self.sync_audio(clock.index, 0.0);
        }
        self.clock.set_value(clock);
        if tick == Tick::Ended {
            self.stop();
        }
    }

    pub fn toggle_pause(&self) {
        if self.playing.get_untracked().is_none() {
            return;
        }
        let paused = self.paused.get_untracked();
        if paused {
            self.last.set_value(js_sys::Date::now()); // a pause does not count as reading time
        }
        self.paused.set(!paused);
        if let Some(a) = self.audio.get_value() {
            if paused {
                let index = self.clock.with_value(|c| c.index);
                if self.urls.with_value(|u| u.get(index).is_some_and(Option::is_some)) && !self.silent.get_untracked() {
                    if let Ok(p) = a.play() {
                        let ignore = Closure::once(|_: JsValue| {});
                        let _ = p.catch(&ignore);
                        ignore.forget();
                    }
                }
            } else {
                let _ = a.pause();
            }
        }
    }

    pub fn stop(&self) {
        self.timer.set_value(None);
        if let Some(a) = self.audio.get_value() {
            let _ = a.pause();
        }
        self.playing.set(None);
        self.paused.set(false);
        self.t.set(0.0);
    }

    /// Voice-over time of slide `idx` - seconds since the start of the paragraph while it is being read (including on pause), otherwise `None`.
    pub fn audio_time(&self, idx: usize) -> Option<f64> {
        (self.playing.get() == Some(idx)).then(|| self.t.get())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn estimate_is_by_characters_with_a_floor() {
        assert_eq!(estimate_seconds("ab"), 3.0);
        assert_eq!(estimate_seconds(&"é".repeat(140)), 10.0);
    }

    #[test]
    fn time_is_minutes_and_two_digit_seconds() {
        assert_eq!(fmt_time(0.0), "0:00");
        assert_eq!(fmt_time(65.4), "1:05");
        assert_eq!(fmt_time(-3.0), "0:00");
    }

    #[test]
    fn clock_moves_through_parts_and_ends_on_the_last() {
        let mut c = Clock::new(vec![1.0, 2.0], 0);
        assert_eq!(c.tick(0.5), Tick::Playing);
        assert_eq!(c.tick(0.6), Tick::NextPart);
        assert_eq!((c.index, c.t), (1, 0.0));
        assert_eq!(c.tick(1.9), Tick::Playing);
        assert_eq!(c.tick(0.2), Tick::Ended);
        assert_eq!(c.t, 2.0);
    }

    #[test]
    fn a_chapter_position_is_found_in_its_paragraph() {
        let d = [10.0, 20.0, 30.0];
        assert_eq!(locate(&d, 0.0), (0, 0.0));
        assert_eq!(locate(&d, 9.5), (0, 9.5));
        assert_eq!(locate(&d, 10.0), (1, 0.0));
        assert_eq!(locate(&d, 34.0), (2, 4.0));
        assert_eq!(locate(&d, 600.0), (2, 30.0), "past the end - the end of the last paragraph");
        assert_eq!(locate(&d, -5.0), (0, 0.0));
        assert_eq!(locate(&[], 3.0), (0, 0.0));
    }

    #[test]
    fn clock_can_start_inside_a_paragraph() {
        let c = Clock::at(vec![4.0, 8.0], 1, 5.0);
        assert_eq!((c.index, c.t), (1, 5.0));
        assert_eq!(Clock::at(vec![4.0], 0, 99.0).t, 4.0);
    }

    #[test]
    fn clock_start_is_clamped_to_the_queue() {
        assert_eq!(Clock::new(vec![1.0, 1.0], 9).index, 1);
        assert_eq!(Clock::new(vec![], 3).index, 0);
    }
}
