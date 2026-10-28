//! "Voiceless voice-over" player: while there are no wav files, each paragraph is "read" by a virtual clock at ~14 characters per second;
//! slides and scene step marks follow this clock. The clock is a pure struct ([`Clock`]), the player is a thin wrapper over a timer.

use gloo_timers::callback::Interval;
use leptos::prelude::*;

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
    clock: StoredValue<Clock>,
    last: StoredValue<f64>,
    timer: StoredValue<Option<Interval>, LocalStorage>,
}

pub fn provide_player() -> Player {
    let p = Player {
        playing: RwSignal::new(None),
        paused: RwSignal::new(false),
        t: RwSignal::new(0.0),
        clock: StoredValue::new(Clock::new(Vec::new(), 0)),
        last: StoredValue::new(0.0),
        timer: StoredValue::new_local(None),
    };
    provide_context(p);
    p
}

impl Player {
    /// Start reading from paragraph `from`: durations of all paragraphs in the chapter.
    pub fn start(&self, durations: Vec<f64>, from: usize) {
        let clock = Clock::new(durations, from);
        self.playing.set(Some(clock.index));
        self.t.set(0.0);
        self.paused.set(false);
        self.clock.set_value(clock);
        self.last.set_value(js_sys::Date::now());
        let me = *self;
        self.timer.set_value(Some(Interval::new(TICK_MS, move || me.on_tick())));
    }

    fn on_tick(&self) {
        if self.paused.get_untracked() {
            return;
        }
        let now = js_sys::Date::now();
        let dt = (now - self.last.get_value()) / 1000.0;
        self.last.set_value(now);
        let mut clock = self.clock.get_value();
        let tick = clock.tick(dt);
        self.t.set(clock.t);
        self.playing.set(Some(clock.index));
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
    }

    pub fn stop(&self) {
        self.timer.set_value(None);
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
    fn clock_start_is_clamped_to_the_queue() {
        assert_eq!(Clock::new(vec![1.0, 1.0], 9).index, 1);
        assert_eq!(Clock::new(vec![], 3).index, 0);
    }
}
