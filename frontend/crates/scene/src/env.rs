//! Scene environment: the voice-over time of the shown slide and the "no motion" mode. The app puts it into the context
//! ([`provide_env`]); scenes only read it; without a context scenes run on their own timers.

use leptos::prelude::*;

#[derive(Clone, Copy)]
pub struct SceneEnv {
    /// seconds from the start of the paragraph while the slide is being voiced (and on pause), otherwise `None`
    pub audio_time: Signal<Option<f64>>,
    /// scenes show the final result at once without motion (setting or `prefers-reduced-motion`)
    pub motion_off: bool,
}

pub fn provide_env(env: SceneEnv) {
    provide_context(env);
}

/// Environment of the current slide; without it — "no sound, motion on".
pub fn use_env() -> SceneEnv {
    use_context::<SceneEnv>().unwrap_or(SceneEnv { audio_time: Signal::stored(None), motion_off: false })
}
