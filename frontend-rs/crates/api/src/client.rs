//! Сетевая часть клиента: JSON поверх `fetch` (gloo-net), токен сессии подставляется из функции приложения.

use std::sync::Arc;

use gloo_net::http::{Method, RequestBuilder};
use serde::{de::DeserializeOwned, Serialize};
use serde_json::Value;

use crate::{
    dto::*,
    error::{message_of, ApiError},
};

/// Клиент API. Дешёвый в копировании (общий контекст приложения); токен читается при каждом запросе.
#[derive(Clone)]
pub struct Client {
    token: Arc<dyn Fn() -> Option<String> + Send + Sync>,
    on_unauthorized: Arc<dyn Fn() + Send + Sync>,
}

impl Client {
    /// `token` — текущий токен сессии; `on_unauthorized` вызывается при 401 вне `/api/auth/` (сессия истекла).
    pub fn new(token: impl Fn() -> Option<String> + Send + Sync + 'static, on_unauthorized: impl Fn() + Send + Sync + 'static) -> Self {
        Self { token: Arc::new(token), on_unauthorized: Arc::new(on_unauthorized) }
    }

    async fn send(&self, method: Method, path: &str, body: Option<Value>) -> Result<Value, ApiError> {
        let net = |e: gloo_net::Error| ApiError { status: 0, message: format!("Нет связи с сервером: {e}") };
        let mut rb = RequestBuilder::new(path).method(method);
        if let Some(token) = (self.token)() {
            rb = rb.header("Authorization", &format!("Bearer {token}"));
        }
        let resp = match body {
            Some(b) => rb.json(&b).map_err(net)?.send().await,
            None => rb.send().await,
        }
        .map_err(net)?;
        let status = resp.status();
        if status == 401 && !path.starts_with("/api/auth/") && !path.starts_with("/api/admin/") {
            (self.on_unauthorized)();
        }
        let value: Value = if status == 204 { Value::Null } else { resp.json().await.unwrap_or(Value::Null) };
        if (200..300).contains(&status) {
            Ok(value)
        } else {
            Err(ApiError { status, message: message_of(&value, status) })
        }
    }

    async fn call<T: DeserializeOwned>(&self, method: Method, path: &str, body: Option<Value>) -> Result<T, ApiError> {
        let v = self.send(method, path, body).await?;
        serde_json::from_value(v).map_err(|e| ApiError { status: 0, message: format!("Неожиданный ответ сервера ({path}): {e}") })
    }

    pub async fn get<T: DeserializeOwned>(&self, path: &str) -> Result<T, ApiError> {
        self.call(Method::GET, path, None).await
    }

    pub async fn post<T: DeserializeOwned>(&self, path: &str, body: &impl Serialize) -> Result<T, ApiError> {
        self.call(Method::POST, path, Some(to_value(body))).await
    }

    /// POST без тела в ответе (204).
    pub async fn post_empty(&self, path: &str, body: &impl Serialize) -> Result<(), ApiError> {
        self.send(Method::POST, path, Some(to_value(body))).await.map(|_| ())
    }

    pub async fn put_empty(&self, path: &str, body: &impl Serialize) -> Result<(), ApiError> {
        self.send(Method::PUT, path, Some(to_value(body))).await.map(|_| ())
    }

    pub async fn delete(&self, path: &str) -> Result<(), ApiError> {
        self.send(Method::DELETE, path, None).await.map(|_| ())
    }

    // --- курс ---------------------------------------------------------------------------------

    pub async fn books(&self) -> Result<Vec<Book>, ApiError> {
        self.get("/api/books").await
    }

    pub async fn course(&self, book: i64) -> Result<Vec<Section>, ApiError> {
        self.get(&format!("/api/books/{book}/course")).await
    }

    pub async fn chapter(&self, id: i64) -> Result<Chapter, ApiError> {
        self.get(&format!("/api/chapters/{id}")).await
    }

    // --- слайды -------------------------------------------------------------------------------

    /// Главы, у которых есть слайды: `(книга, глава)`.
    pub async fn slide_index(&self) -> Result<Vec<(i64, i64)>, ApiError> {
        #[derive(serde::Deserialize)]
        struct Info {
            book: i64,
            chapter: i64,
        }
        let list: Vec<Info> = self.get("/api/slides").await?;
        Ok(list.into_iter().map(|i| (i.book, i.chapter)).collect())
    }

    /// Слайды главы (схемы, блоки); `None` — у главы их нет.
    pub async fn slides(&self, book: i64, chapter: i64) -> Result<Option<content::Chapter>, ApiError> {
        match self.get(&format!("/api/slides/{book}/{chapter}")).await {
            Ok(ch) => Ok(Some(ch)),
            Err(e) if e.status == 404 => Ok(None),
            Err(e) => Err(e),
        }
    }

    // --- прогресс -----------------------------------------------------------------------------

    pub async fn progress(&self) -> Result<Progress, ApiError> {
        self.get("/api/progress").await
    }

    pub async fn mark_slide(&self, book: i64, chapter: i64, slide: usize) -> Result<(), ApiError> {
        self.post_empty("/api/progress/slides", &serde_json::json!({ "book": book, "chapter": chapter, "slide": slide })).await
    }

    /// Сбросить упражнения или весь прогресс текущего пользователя.
    pub async fn reset_progress(&self, scope: ResetScope) -> Result<(), ApiError> {
        self.delete(&format!("/api/progress?scope={}", scope.param())).await
    }

    pub async fn reset_quiz(&self, book: i64, chapter: i64) -> Result<(), ApiError> {
        self.delete(&format!("/api/progress/quiz?book={book}&chapter={chapter}")).await
    }

    // --- квизы и ответы -----------------------------------------------------------------------

    /// Сколько вопросов в квизе каждой главы: `{книга: {глава: число}}`.
    pub async fn quiz_counts(&self) -> Result<Counts, ApiError> {
        self.get("/api/quizzes").await
    }

    pub async fn quiz(&self, book: i64, chapter: i64) -> Result<Quiz, ApiError> {
        self.get(&format!("/api/quizzes/{book}/{chapter}")).await
    }

    pub async fn quiz_answer(&self, book: i64, chapter: i64, question: usize, pick: usize) -> Result<QuizAnswer, ApiError> {
        self.post(&format!("/api/quizzes/{book}/{chapter}/answer"), &serde_json::json!({ "question": question, "pick": pick })).await
    }

    pub async fn answer_counts(&self) -> Result<Counts, ApiError> {
        self.get("/api/answers").await
    }

    pub async fn practice_set(&self, book: i64, chapter: i64) -> Result<PracticeSet, ApiError> {
        self.get(&format!("/api/answers/{book}/{chapter}")).await
    }

    pub async fn check_answer(&self, book: i64, chapter: i64, task: usize, value: &str) -> Result<bool, ApiError> {
        let r: Verdict = self.post(&format!("/api/answers/{book}/{chapter}/check"), &serde_json::json!({ "task": task, "value": value })).await?;
        Ok(r.ok)
    }

    pub async fn reset_answers(&self, book: i64, chapter: i64) -> Result<(), ApiError> {
        self.delete(&format!("/api/answers?book={book}&chapter={chapter}")).await
    }

    // --- упражнения с кодом -------------------------------------------------------------------

    pub async fn code_counts(&self) -> Result<Counts, ApiError> {
        self.get("/api/exercises").await
    }

    /// Задачи главы (по номеру главы); 404 — упражнений нет.
    pub async fn code_tasks(&self, book: i64, chapter: i64) -> Result<ChapterTasks, ApiError> {
        self.get(&format!("/api/exercises/{book}/{chapter}")).await
    }

    pub async fn chapter_state(&self, book: i64, chapter: i64) -> Result<ChapterState, ApiError> {
        self.get(&format!("/api/exercises/{book}/{chapter}/state")).await
    }

    pub async fn save_draft(&self, book: i64, chapter: i64, task: &str, code: &str) -> Result<(), ApiError> {
        self.put_empty(&format!("/api/exercises/{book}/{chapter}/{task}/draft"), &serde_json::json!({ "code": code })).await
    }

    /// Лабораторные упражнения главы с их сценариями (без эталонов).
    pub async fn lab_chapter(&self, book: i64, chapter: i64) -> Result<LabChapter, ApiError> {
        self.get(&format!("/api/labs/{book}/{chapter}")).await
    }

    /// Решение лаборатории: сервер перепроверяет его движком лаборатории; отказ приходит ошибкой с причиной.
    pub async fn mark_lab_solved(&self, book: i64, chapter: i64, task: &str, solution: &str) -> Result<(), ApiError> {
        self.put_empty(&format!("/api/exercises/{book}/{chapter}/{task}/solved"), &serde_json::json!({ "solution": solution })).await
    }

    pub async fn attempts(&self, book: i64, chapter: i64, task: &str) -> Result<Vec<Attempt>, ApiError> {
        let r: Attempts = self.get(&format!("/api/exercises/{book}/{chapter}/{task}/attempts")).await?;
        Ok(r.attempts)
    }

    /// Ставит решение в очередь проверки; ответ — первое состояние задания.
    pub async fn run(&self, book: i64, chapter: i64, task: &str, code: &str) -> Result<(String, RunState), ApiError> {
        let v: Value = self.post("/api/exercises/run", &serde_json::json!({ "book": book, "chapter": chapter, "task": task, "code": code })).await?;
        let id = v.get("id").and_then(Value::as_str).unwrap_or_default().to_string();
        let state = serde_json::from_value(v).map_err(|e| ApiError { status: 0, message: format!("Неожиданный ответ сервера: {e}") })?;
        Ok((id, state))
    }

    pub async fn run_state(&self, job: &str) -> Result<RunState, ApiError> {
        self.get(&format!("/api/exercises/run/{job}")).await
    }

    // --- вход ---------------------------------------------------------------------------------

    /// Вход по email и паролю: токен сессии и личность (crates lab: `/api/auth/login`).
    pub async fn login(&self, email: &str, password: &str) -> Result<Identity, ApiError> {
        self.post("/api/auth/login", &serde_json::json!({ "email": email, "password": password })).await
    }

    pub async fn signup(&self, email: &str, password: &str, name: &str) -> Result<(), ApiError> {
        self.post_empty("/api/auth/signup", &serde_json::json!({ "email": email, "password": password, "name": name })).await
    }

    pub async fn me(&self) -> Result<Identity, ApiError> {
        self.get("/api/auth/me").await
    }

    pub async fn logout(&self) -> Result<(), ApiError> {
        self.post_empty("/api/auth/logout", &serde_json::json!({})).await
    }
}

fn to_value(body: &impl Serialize) -> Value {
    serde_json::to_value(body).unwrap_or(Value::Null)
}
