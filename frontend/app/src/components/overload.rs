//! Окно о перегрузке сервера проверки кода: объясняет, что произошло, и зовёт запустить систему у себя (инструкция в репозитории).

use leptos::prelude::*;

/// Репозиторий проекта: README с разделом «Запуск у себя».
pub const REPO_URL: &str = "https://github.com/rysev-a/dev-learn";
const GUIDE_URL: &str = "https://github.com/rysev-a/dev-learn#запуск-у-себя";

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
                Overload::Unavailable => (
                    "Проверка кода сейчас недоступна",
                    "Сервер проверки перегружен или не отвечает. Это тестовый запуск на одной небольшой машине.",
                ),
                Overload::Busy => (
                    "Много желающих проверить код",
                    "Очередь проверок длинная, решение будет проверено, но придётся подождать. Это тестовый запуск на одной небольшой машине.",
                ),
            };
            view! {
                <aside class="overload" role="alertdialog" aria-labelledby="overload-title">
                    <button type="button" class="overload-x" aria-label="Закрыть" on:click=move |_| state.close()>"×"</button>
                    <h3 id="overload-title">{title}</h3>
                    <p>{text}</p>
                    <p>"Систему можно запустить у себя: всё открыто, а проверка кода и лаборатории тогда работают без очереди."</p>
                    <div class="overload-actions">
                        <a class="quiz-btn" href=GUIDE_URL target="_blank" rel="noopener noreferrer">"Как запустить у себя"</a>
                        <a class="quiz-btn ghost" href=REPO_URL target="_blank" rel="noopener noreferrer">"Репозиторий"</a>
                    </div>
                </aside>
            }
        })
    }
}
