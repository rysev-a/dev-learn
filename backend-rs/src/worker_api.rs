//! Внутренний API воркеров проверки (как `exercises/worker_api.py`): забрать задание, подтвердить жизнь, вернуть результат.
//! Закрыт токеном `SAY_WORKER_TOKEN` (`Authorization: Bearer …`); без токена в окружении недоступен вовсе (404).

use std::time::{Duration, Instant};

use axum::{
    extract::{Path, Request, State},
    http::{header, HeaderMap, StatusCode},
    middleware::{from_fn_with_state, Next},
    response::{IntoResponse, Response},
    routing::post,
    Json, Router,
};
use serde::Deserialize;
use serde_json::Value;

use crate::{error::ApiError, error::ApiResult, jobs, AppState};

const MAX_WAIT: u64 = 25;

pub fn routes(state: AppState) -> Router<AppState> {
    // токен проверяется до разбора тела: без токена в окружении маршруты не существуют (404), с неверным — 401
    Router::new()
        .route("/internal/worker/claim", post(claim))
        .route("/internal/worker/ping", post(ping))
        .route("/internal/worker/jobs/{job_id}/result", post(result))
        .layer(from_fn_with_state(state, gate))
}

async fn gate(State(state): State<AppState>, req: Request, next: Next) -> Response {
    match authorize(&state, req.headers()) {
        Ok(()) => next.run(req).await,
        Err(e) => e.into_response(),
    }
}

fn constant_eq(a: &[u8], b: &[u8]) -> bool {
    a.len() == b.len() && a.iter().zip(b).fold(0u8, |acc, (x, y)| acc | (x ^ y)) == 0
}

fn authorize(state: &AppState, headers: &HeaderMap) -> ApiResult<()> {
    let token = &state.cfg.worker_token;
    if token.is_empty() {
        return Err(ApiError::not_found("Not found"));
    }
    let given = headers.get(header::AUTHORIZATION).and_then(|v| v.to_str().ok()).unwrap_or("").trim_start_matches("Bearer ").trim();
    if constant_eq(given.as_bytes(), token.as_bytes()) {
        Ok(())
    } else {
        Err(ApiError::new(401, "Неверный токен воркера"))
    }
}

#[derive(Deserialize)]
struct ClaimIn {
    name: String,
    lanes: Vec<String>,
    #[serde(default = "one")]
    slots: i64,
    #[serde(default = "twenty")]
    wait: u64,
}
fn one() -> i64 {
    1
}
fn twenty() -> u64 {
    20
}

#[derive(Deserialize)]
struct PingIn {
    name: String,
    lanes: Vec<String>,
    #[serde(default = "one")]
    slots: i64,
    #[serde(default)]
    jobs: Vec<String>,
}

#[derive(Deserialize)]
struct ResultIn {
    name: String,
    result: Value,
}

fn check_name(name: &str) -> ApiResult<()> {
    if name.is_empty() || name.chars().count() > 64 {
        return Err(ApiError::invalid("name: от 1 до 64 символов"));
    }
    Ok(())
}

/// Долгий опрос: до `wait` секунд ждёт задание из полос воркера; пусто — 204.
async fn claim(State(state): State<AppState>, Json(b): Json<ClaimIn>) -> ApiResult<Response> {
    check_name(&b.name)?;
    let deadline = Instant::now() + Duration::from_secs(b.wait.min(MAX_WAIT));
    loop {
        jobs::ping(&state, &b.name, &b.lanes, b.slots.clamp(1, 256), &[]).await?;
        if let Some(job) = jobs::claim(&state, &b.name, &b.lanes).await? {
            return Ok(Json(job).into_response());
        }
        if Instant::now() >= deadline {
            return Ok(StatusCode::NO_CONTENT.into_response());
        }
        tokio::time::sleep(Duration::from_millis(400)).await;
    }
}

async fn ping(State(state): State<AppState>, Json(b): Json<PingIn>) -> ApiResult<StatusCode> {
    check_name(&b.name)?;
    jobs::ping(&state, &b.name, &b.lanes, b.slots.clamp(1, 256), &b.jobs).await?;
    Ok(StatusCode::NO_CONTENT)
}

async fn result(State(state): State<AppState>, Path(job_id): Path<String>, Json(b): Json<ResultIn>) -> ApiResult<StatusCode> {
    check_name(&b.name)?;
    if jobs::complete(&state, &job_id, &b.name, b.result).await? {
        Ok(StatusCode::NO_CONTENT)
    } else {
        Err(ApiError::new(409, "Задание уже не за этим воркером (аренда истекла или результат принят)"))
    }
}
