//! Плеер «озвучки без звука»: пока wav-файлов нет, каждый абзац «читается» по виртуальным часам со скоростью ~14 символов в секунду;
//! слайды и метки шагов сцен идут по этим часам. Часы — чистая структура ([`Clock`]), плеер — тонкая обёртка над таймером.

use gloo_timers::callback::Interval;
use leptos::prelude::*;

pub const CHARS_PER_SECOND: f64 = 14.0;
const TICK_MS: u32 = 100;

/// Сколько секунд «читается» абзац (не меньше трёх).
pub fn estimate_seconds(text: &str) -> f64 {
    (text.chars().count() as f64 / CHARS_PER_SECOND).max(3.0)
}

/// Секунды как `м:сс`.
pub fn fmt_time(secs: f64) -> String {
    let s = secs.max(0.0).round() as u64;
    format!("{}:{:02}", s / 60, s % 60)
}

/// Что произошло за тик часов.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Tick {
    Playing,
    /// абзац дочитан, начался следующий
    NextPart,
    /// дочитан последний абзац
    Ended,
}

/// Часы очереди абзацев: длительности, текущий абзац и время внутри него.
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

    /// Прошло `dt` секунд. За один тик не больше одного перехода: остаток времени теряется (тик — доли секунды).
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
    /// номер абзаца (слайда), который сейчас читается; `None` — плеер остановлен
    pub playing: RwSignal<Option<usize>>,
    pub paused: RwSignal<bool>,
    /// секунды от начала текущего абзаца
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
    /// Начать чтение с абзаца `from`: длительности всех абзацев главы.
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
            self.last.set_value(js_sys::Date::now()); // пауза не засчитывается как время чтения
        }
        self.paused.set(!paused);
    }

    pub fn stop(&self) {
        self.timer.set_value(None);
        self.playing.set(None);
        self.paused.set(false);
        self.t.set(0.0);
    }

    /// Время озвучки слайда `idx` — секунды от начала абзаца, пока он читается (в том числе на паузе), иначе `None`.
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
        assert_eq!(estimate_seconds(&"я".repeat(140)), 10.0);
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
