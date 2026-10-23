//! Среда сцены: время озвучки показанного слайда и режим «без движения». Приложение кладёт её в контекст
//! ([`provide_env`]), сцены только читают; без контекста сцены идут по собственным таймерам.

use leptos::prelude::*;

#[derive(Clone, Copy)]
pub struct SceneEnv {
    /// секунды от начала абзаца, пока слайд озвучивается (и на паузе), иначе `None`
    pub audio_time: Signal<Option<f64>>,
    /// сцены сразу показывают итог без движения (настройка или `prefers-reduced-motion`)
    pub motion_off: bool,
}

pub fn provide_env(env: SceneEnv) {
    provide_context(env);
}

/// Среда текущего слайда; без неё — «звука нет, движение включено».
pub fn use_env() -> SceneEnv {
    use_context::<SceneEnv>().unwrap_or(SceneEnv { audio_time: Signal::stored(None), motion_off: false })
}
