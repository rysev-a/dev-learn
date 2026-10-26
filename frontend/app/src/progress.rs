//! Прогресс пользователя: копия на клиенте (для дашборда и вкладок) и точечные записи на сервер.

use api::{
    dto::{progress_key, Progress, ResetScope},
    ApiError,
};
use leptos::{prelude::*, task::spawn_local};

#[derive(Clone, Copy)]
pub struct ProgressStore {
    pub data: RwSignal<Progress>,
    pub ready: RwSignal<bool>,
}

/// Загружает прогресс при входе и сбрасывает при выходе.
pub fn provide_progress(session: crate::session::Session) -> ProgressStore {
    let store = ProgressStore { data: RwSignal::new(Progress::default()), ready: RwSignal::new(false) };
    provide_context(store);
    Effect::new(move |_| {
        if session.identity.get().is_some() {
            spawn_local(async move {
                store.reload().await;
                store.ready.set(true);
            });
        } else {
            store.data.set(Progress::default());
            store.ready.set(false);
        }
    });
    store
}

impl ProgressStore {
    /// Перечитывает прогресс с сервера (при ошибке остаётся прежняя копия).
    async fn reload(self) {
        if let Ok(p) = crate::hooks::client().progress().await {
            self.data.set(p);
        }
    }

    /// Сбрасывает прогресс на сервере и перечитывает копию: дашборд и вкладки сразу показывают чистое состояние.
    pub async fn reset(&self, scope: ResetScope) -> Result<(), ApiError> {
        crate::hooks::client().reset_progress(scope).await?;
        self.reload().await;
        Ok(())
    }

    pub fn viewed_slides(&self, book: i64, chapter: i64) -> usize {
        self.data.with(|d| d.slides.get(&progress_key(book, chapter)).map_or(0, Vec::len))
    }

    /// Просмотренный слайд: сразу в копию, на сервер — без ожидания.
    pub fn mark_slide(&self, book: i64, chapter: i64, slide: usize) {
        let key = progress_key(book, chapter);
        let new = self.data.with_untracked(|d| d.slides.get(&key).is_none_or(|v| !v.contains(&slide)));
        if !new {
            return;
        }
        self.data.update(|d| {
            let v = d.slides.entry(key).or_default();
            v.push(slide);
            v.sort_unstable();
        });
        let client = crate::hooks::client();
        spawn_local(async move {
            let _ = client.mark_slide(book, chapter, slide).await;
        });
    }

    pub fn quiz_picks(&self, book: i64, chapter: i64) -> Vec<Option<usize>> {
        self.data.with(|d| d.quiz.get(&progress_key(book, chapter)).cloned().unwrap_or_default())
    }

    pub fn quiz_right(&self, book: i64, chapter: i64) -> usize {
        self.data.with(|d| d.quiz_right.get(&progress_key(book, chapter)).copied().unwrap_or(0))
    }

    /// Выбор варианта (после ответа сервера): `right` — сколько верных теперь в главе.
    pub fn record_quiz_pick(&self, book: i64, chapter: i64, question: usize, total: usize, pick: usize, right: usize) {
        let key = progress_key(book, chapter);
        self.data.update(|d| {
            let picks = d.quiz.entry(key.clone()).or_default();
            picks.resize(total, None);
            picks[question] = Some(pick);
            d.quiz_right.insert(key, right);
        });
    }

    pub fn reset_quiz(&self, book: i64, chapter: i64) {
        let key = progress_key(book, chapter);
        self.data.update(|d| {
            d.quiz.remove(&key);
            d.quiz_right.remove(&key);
        });
        let client = crate::hooks::client();
        spawn_local(async move {
            let _ = client.reset_quiz(book, chapter).await;
        });
    }

    pub fn record_answer(&self, book: i64, chapter: i64, task: usize, value: &str) {
        self.data.update(|d| {
            d.answers.entry(progress_key(book, chapter)).or_default().insert(task.to_string(), value.to_string());
        });
    }

    pub fn reset_answers(&self, book: i64, chapter: i64) {
        self.data.update(|d| {
            d.answers.remove(&progress_key(book, chapter));
        });
        let client = crate::hooks::client();
        spawn_local(async move {
            let _ = client.reset_answers(book, chapter).await;
        });
    }

    /// Статус кодовой задачи: решённое остаётся решённым.
    pub fn set_code_status(&self, book: i64, chapter: i64, task: &str, status: &str) {
        self.data.update(|d| {
            let m = d.code.entry(progress_key(book, chapter)).or_default();
            if m.get(task).map(String::as_str) != Some("ok") {
                m.insert(task.to_string(), status.to_string());
            }
        });
    }
}
