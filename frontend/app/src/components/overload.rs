//! Окно о перегрузке сервера проверки кода: сервис в стадии развития и пока не выдерживает большую нагрузку.

use leptos::prelude::*;

/// Минимум между показами окна, если его закрыли (мс).
const QUIET_MS: f64 = 60_000.0;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Overload {
    /// сервер проверки не отвечает или отказал в постановке (нет воркера, очередь переполнена)
    Unavailable,
    /// проверка идёт, но очередь длинная
    Busy,
}

/// Состояние окна: что показывать и когда его закрыли в последний раз.
#[derive(Clone, Copy)]
pub struct OverloadState {
    kind: RwSignal<Option<Overload>>,
    closed_at: RwSignal<f64>,
}

impl OverloadState {
    pub fn new() -> Self {
        Self { kind: RwSignal::new(None), closed_at: RwSignal::new(f64::NEG_INFINITY) }
    }

    /// Показать окно (если его не закрывали в последнюю минуту).
    pub fn raise(&self, kind: Overload) {
        if js_sys::Date::now() - self.closed_at.get_untracked() >= QUIET_MS {
            self.kind.set(Some(kind));
        }
    }

    pub fn close(&self) {
        self.kind.set(None);
        self.closed_at.set(js_sys::Date::now());
    }
}

impl Default for OverloadState {
    fn default() -> Self {
        Self::new()
    }
}

#[component]
pub fn OverloadNotice(state: OverloadState) -> impl IntoView {
    move || {
        state.kind.get().map(|kind| {
            let (title, text) = match kind {
                Overload::Unavailable => ("Проверка кода сейчас недоступна", "Сервис в стадии развития и пока не выдерживает большую нагрузку: сервер проверки перегружен или не отвечает."),
                Overload::Busy => ("Много желающих проверить код", "Сервис в стадии развития и пока не выдерживает большую нагрузку: очередь проверок длинная, решение будет проверено, но придётся подождать."),
            };
            view! {
                <aside class="overload" role="alertdialog" aria-labelledby="overload-title">
                    <button type="button" class="overload-x" aria-label="Закрыть" on:click=move |_| state.close()>"×"</button>
                    <h3 id="overload-title">{title}</h3>
                    <p>{text}</p>
                    <p>"Попробуйте чуть позже: мы расширяем мощности. Теория, вопросы и лаборатории в браузере работают как обычно."</p>
                    <div class="overload-actions">
                        <button type="button" class="quiz-btn" on:click=move |_| state.close()>"Понятно"</button>
                    </div>
                </aside>
            }
        })
    }
}
