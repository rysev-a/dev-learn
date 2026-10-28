//! API errors: body `{"detail": "..."}` - like FastAPI, so the client parses both backends the same way.

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::{json, Value};

#[derive(Debug)]
pub struct ApiError(pub StatusCode, pub String);

pub type ApiResult<T> = Result<T, ApiError>;

impl ApiError {
    pub fn new(code: u16, msg: impl Into<String>) -> Self {
        Self(StatusCode::from_u16(code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR), msg.into())
    }
    pub fn not_found(msg: impl Into<String>) -> Self {
        Self::new(404, msg)
    }
    pub fn invalid(msg: impl Into<String>) -> Self {
        Self::new(422, msg)
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        (self.0, Json(json!({ "detail": self.1 }))).into_response()
    }
}

impl From<surrealdb::Error> for ApiError {
    fn from(e: surrealdb::Error) -> Self {
        tracing::error!("surrealdb: {e}");
        Self::new(500, "Database error")
    }
}

impl From<anyhow::Error> for ApiError {
    fn from(e: anyhow::Error) -> Self {
        tracing::error!("{e:#}");
        Self::new(500, "Internal error")
    }
}

// --- access to the fields of JSON rows returned by SurrealDB ---------------------------------

pub fn s(v: &Value, k: &str) -> String {
    v.get(k).and_then(Value::as_str).unwrap_or("").to_string()
}

pub fn i(v: &Value, k: &str) -> i64 {
    v.get(k).and_then(|x| x.as_i64().or_else(|| x.as_f64().map(|f| f as i64))).unwrap_or(0)
}

pub fn f(v: &Value, k: &str) -> f64 {
    v.get(k).and_then(Value::as_f64).unwrap_or(0.0)
}

/// Current time in seconds (fractional) - for leases and the queue cache.
pub fn now_secs() -> f64 {
    std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_secs_f64()).unwrap_or(0.0)
}

/// Time in ISO 8601 format with a time zone: `2026-10-22T16:18:00+00:00`.
pub fn iso_now() -> String {
    chrono::Utc::now().format("%Y-%m-%dT%H:%M:%S+00:00").to_string()
}
