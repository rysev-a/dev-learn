//! Clock for exercises with latches and registers: a single pulse on a button and an auto-generator (`clock.ts` in React).
//! The clock input is an ordinary board switch: the clock only toggles its level and counts 0 → 1 edges.

use archlab::model::{InputId, InputState};
use gloo_timers::callback::{Interval, Timeout};
use leptos::prelude::*;

/// How many milliseconds the clock holds one for a single tick.
const TICK_MS: u32 = 600;
/// Auto-generator frequencies, Hz.
pub const CLOCK_RATES: [f64; 4] = [0.5, 1.0, 2.0, 4.0];

/// Level toggle period of the auto-generator: half the period of frequency `hz`.
pub fn half_period_ms(hz: f64) -> u32 {
    (500.0 / hz.max(0.01)).round() as u32
}

/// Frequency label: `0.5 Hz`, `1 Hz`.
pub fn rate_label(hz: f64) -> String {
    i18n::trf!("{0} Hz", hz)
}

/// Clock state and control: signals for the interface and timers.
#[derive(Clone, Copy)]
pub struct Clock {
    pub ticking: RwSignal<bool>,
    pub auto: RwSignal<bool>,
    pub rate: RwSignal<f64>,
    /// how many edges (0 → 1) have been applied since the start of the exercise
    pub edges: RwSignal<u32>,
    clock_id: Option<InputId>,
    inputs: RwSignal<InputState>,
    pulse: StoredValue<Option<Timeout>, LocalStorage>,
    interval: StoredValue<Option<Interval>, LocalStorage>,
}

impl Clock {
    pub fn new(clock_id: Option<InputId>, inputs: RwSignal<InputState>) -> Self {
        let clock = Self {
            ticking: RwSignal::new(false),
            auto: RwSignal::new(false),
            rate: RwSignal::new(1.0),
            edges: RwSignal::new(0),
            clock_id,
            inputs,
            pulse: StoredValue::new_local(None),
            interval: StoredValue::new_local(None),
        };
        on_cleanup(move || clock.dispose());
        clock
    }

    pub fn level(&self, id: InputId) -> u8 {
        self.inputs.with_untracked(|s| s.get(id))
    }

    /// Sets the switch level; a rising clock input counts as an edge.
    pub fn set_level(&self, id: InputId, level: u8) {
        if Some(id) == self.clock_id && level != 0 && self.level(id) == 0 {
            self.edges.update(|n| *n += 1);
        }
        self.inputs.update(|s| s.set(id, level));
    }

    /// Toggles the switch to the opposite level.
    pub fn toggle(&self, id: InputId) {
        self.set_level(id, self.level(id) ^ 1);
    }

    /// One tick: CLK rises to 1 and falls back to 0 after a pause.
    pub fn tick(&self) {
        let Some(id) = self.clock_id else { return };
        if self.ticking.get_untracked() || self.auto.get_untracked() || self.level(id) == 1 {
            return;
        }
        self.ticking.set(true);
        self.set_level(id, 1);
        let me = *self;
        self.pulse.set_value(Some(Timeout::new(TICK_MS, move || {
            me.set_level(id, 0);
            me.ticking.set(false);
        })));
    }

    pub fn toggle_auto(&self) {
        if self.auto.get_untracked() {
            self.stop();
        } else if self.clock_id.is_some() && !self.ticking.get_untracked() {
            self.auto.set(true);
            self.start_auto();
        }
    }

    pub fn set_rate(&self, hz: f64) {
        self.rate.set(hz);
        if self.auto.get_untracked() {
            self.start_auto();
        }
    }

    /// Stop the clock; if CLK stayed at one, lower it.
    pub fn stop(&self) {
        self.pulse.set_value(None);
        self.interval.set_value(None);
        let was = self.auto.get_untracked() || self.ticking.get_untracked();
        self.auto.set(false);
        self.ticking.set(false);
        if let Some(id) = self.clock_id {
            if was && self.level(id) == 1 {
                self.set_level(id, 0);
            }
        }
    }

    fn start_auto(&self) {
        let Some(id) = self.clock_id else { return };
        let me = *self;
        self.interval.set_value(Some(Interval::new(half_period_ms(self.rate.get_untracked()), move || me.toggle(id))));
    }

    fn dispose(&self) {
        let _ = self.pulse.try_set_value(None);
        let _ = self.interval.try_set_value(None);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn auto_generator_toggles_twice_per_period() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(half_period_ms(1.0), 500);
        assert_eq!(half_period_ms(0.5), 1000);
        assert_eq!(half_period_ms(4.0), 125);
        assert_eq!(half_period_ms(0.0), 50_000);
    }

    #[test]
    fn rate_labels_are_short() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(rate_label(1.0), "1 Гц");
        assert_eq!(rate_label(0.5), "0.5 Гц");
    }
}
