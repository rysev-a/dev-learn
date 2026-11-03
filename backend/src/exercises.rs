//! Exercises API: the chapter's task list, queueing a check, attempt history (like `exercises/router.py`).

use axum::{
    extract::{Path, State},
    http::StatusCode,
    routing::{get, post, put},
    Extension, Json, Router,
};
use auth::Identity;
use crate::lang::Lang;
use serde::Deserialize;
use serde_json::{json, Value};

use crate::{
    db::Db,
    error::{s, ApiError, ApiResult},
    jobs, practice, schema_view, AppState,
};

const MAX_CODE: usize = 20_000; // characters in one solution
const MAX_DRAFT: usize = 200_000; // draft: for gate circuits the solution is JSON and can be large

pub fn public() -> Router<AppState> {
    Router::new().route("/api/exercises", get(summary)).route("/api/exercises/runner/status", get(runner_status)).route("/api/exercises/{book_id}/{chapter}", get(list_tasks))
}

pub fn private() -> Router<AppState> {
    Router::new()
        .route("/api/exercises/run", post(run_code))
        .route("/api/exercises/run/{job_id}", get(run_state))
        .route("/api/exercises/{book_id}/{chapter}/state", get(chapter_state))
        .route("/api/exercises/{book_id}/{chapter}/{task_id}/draft", put(save_draft))
        .route("/api/exercises/{book_id}/{chapter}/{task_id}/attempts", get(task_attempts))
        .route("/api/exercises/{book_id}/{chapter}/{task_id}/solved", put(mark_lab_solved))
}

/// Task definition as in the source modules: public fields and everything else from `spec` (tuples - `{"__tuple__": [...]}`).
fn join_task(row: &Value) -> Value {
    let mut task = serde_json::Map::new();
    task.insert("id".into(), json!(s(row, "tid")));
    for k in ["mode", "title", "statement", "starter", "hint"] {
        if let Some(v) = row.get(k).filter(|v| !v.is_null()) {
            task.insert(k.into(), v.clone());
        }
    }
    if let Some(Value::Object(spec)) = row.get("spec").and_then(Value::as_str).and_then(|t| serde_json::from_str(t).ok()) {
        for (k, v) in spec {
            task.insert(k, v);
        }
    }
    Value::Object(task)
}

pub async fn find_task(db: &Db, book: i64, chapter: i64, task_id: &str) -> ApiResult<Option<Value>> {
    let mut res = db
        .query("SELECT tid, mode, title, statement, starter, hint, spec FROM tasks WHERE book = $b AND chapter = $c AND tid = $t")
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task_id.to_string()))
        .await?;
    Ok(res.take::<Vec<Value>>(0)?.first().map(join_task))
}

async fn summary(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    Ok(Json(crate::quizzes::counts(&state.db, "tasks").await?))
}

/// Whether code checking works and how many jobs are in the queue (the interface shows "temporarily unavailable").
async fn runner_status(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    let mut st = jobs::status(&state.db).await?;
    let available = st["workers"].as_i64().unwrap_or(0) > 0;
    st["available"] = json!(available);
    Ok(Json(st))
}

#[derive(Deserialize)]
struct RunIn {
    book: i64,
    chapter: i64,
    task: String,
    code: String,
}

/// Puts a solution in the check queue: the result comes via GET /run/{id} (a user has at most one check running).
async fn run_code(State(state): State<AppState>, Extension(me): Extension<Identity>, Json(b): Json<RunIn>) -> ApiResult<(StatusCode, Json<Value>)> {
    if b.code.chars().count() > MAX_CODE {
        return Err(ApiError::invalid(format!("code: at most {MAX_CODE} characters")));
    }
    let task = find_task(&state.db, b.book, b.chapter, &b.task).await?.ok_or_else(|| ApiError::not_found("Task not found"))?;
    if task.get("mode").and_then(Value::as_str) == Some("lab") {
        return Err(ApiError::invalid("This exercise is checked in the browser, not in the sandbox"));
    }
    if b.code.trim().is_empty() {
        return Err(ApiError::invalid("Empty code — nothing to check"));
    }
    let ok = jobs::workers_alive(&state.db).await? > 0;
    let job_id = jobs::submit(&state, &me.user.id, b.book, b.chapter, &task, &b.code, ok).await.map_err(|e| ApiError::new(e.0, e.1))?;
    let mut out = jobs::get_for_user(&state.db, &job_id, &me.user.id).await?.unwrap_or_else(|| json!({}));
    out["id"] = json!(job_id);
    Ok((StatusCode::ACCEPTED, Json(out)))
}

async fn run_state(State(state): State<AppState>, Extension(me): Extension<Identity>, Path(job_id): Path<String>) -> ApiResult<Json<Value>> {
    jobs::get_for_user(&state.db, &job_id, &me.user.id).await?.map(Json).ok_or_else(|| ApiError::not_found("Check not found"))
}

/// Schema and data of the teaching databases - the SQLite description is built once per set and cached.
async fn dataset(state: &AppState, setup: String) -> ApiResult<Value> {
    let key = schema_view::dataset_key(&setup);
    if let Some(v) = state.datasets.lock().expect("datasets lock").get(&key) {
        return Ok(v.clone());
    }
    let v = tokio::task::spawn_blocking(move || schema_view::describe(&setup)).await.map_err(|e| ApiError::from(anyhow::anyhow!(e)))??;
    state.datasets.lock().expect("datasets lock").insert(key, v.clone());
    Ok(v)
}

async fn list_tasks(State(state): State<AppState>, lang: Lang, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT tid, mode, title, statement, starter, hint, spec, ord FROM tasks WHERE book = $b AND chapter = $c ORDER BY ord")
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let mut rows: Vec<Value> = res.take(0)?;
    if rows.is_empty() {
        return Err(ApiError::not_found("This chapter has no code exercises"));
    }
    crate::lang::overlay(&state.db, "tasks_i18n", lang, book, chapter, &mut rows, &["title", "statement", "starter", "hint"]).await?;
    let (mut items, mut datasets) = (Vec::new(), serde_json::Map::new());
    for r in &rows {
        let mut item = json!({ "id": s(r, "tid"), "mode": s(r, "mode"), "title": s(r, "title"), "statement": s(r, "statement"), "starter": s(r, "starter"), "hint": s(r, "hint") });
        if s(r, "mode") == "sql" {
            let setup = join_task(r).get("setup").and_then(Value::as_str).unwrap_or("").to_string();
            if !setup.is_empty() {
                let key = schema_view::dataset_key(&setup);
                item["dataset"] = json!(key);
                if !datasets.contains_key(&key) {
                    datasets.insert(key, dataset(&state, setup).await?);
                }
            }
        }
        if let Some(board) = crate::board_tasks::view(&join_task(r)) {
            item["board"] = board;
        }
        items.push(item);
    }
    Ok(Json(json!({ "tasks": items, "datasets": datasets })))
}

/// The user's statuses and drafts for the chapter's tasks.
async fn chapter_state(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    Ok(Json(practice::chapter_state(&state.db, &me.user.id, book, chapter).await?))
}

#[derive(Deserialize)]
struct DraftIn {
    code: String,
}

async fn save_draft(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter, task)): Path<(i64, i64, String)>, Json(b): Json<DraftIn>) -> ApiResult<StatusCode> {
    if b.code.chars().count() > MAX_DRAFT {
        return Err(ApiError::invalid(format!("code: at most {MAX_DRAFT} characters")));
    }
    find_task(&state.db, book, chapter, &task).await?.ok_or_else(|| ApiError::not_found("Task not found"))?;
    practice::save_draft(&state.db, &me.user.id, book, chapter, &task, &b.code).await?;
    Ok(StatusCode::NO_CONTENT)
}

/// The user's attempt history for a task: newest first, with code.
async fn task_attempts(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter, task)): Path<(i64, i64, String)>) -> ApiResult<Json<Value>> {
    find_task(&state.db, book, chapter, &task).await?.ok_or_else(|| ApiError::not_found("Task not found"))?;
    Ok(Json(json!({ "attempts": practice::attempts(&state.db, &me.user.id, book, chapter, &task).await? })))
}

#[derive(Deserialize)]
struct SolvedIn {
    #[serde(default)]
    solution: String,
}

/// An interactive exercise (circuit, assembler) is solved - the check passed in the browser; accepted only for tasks of mode lab.
async fn mark_lab_solved(State(state): State<AppState>, lang: Lang, Extension(me): Extension<Identity>, Path((book, chapter, task_id)): Path<(i64, i64, String)>, Json(b): Json<SolvedIn>) -> ApiResult<StatusCode> {
    if b.solution.chars().count() > MAX_DRAFT {
        return Err(ApiError::invalid(format!("solution: at most {MAX_DRAFT} characters")));
    }
    find_task(&state.db, book, chapter, &task_id).await?.filter(|t| t.get("mode").and_then(Value::as_str) == Some("lab")).ok_or_else(|| ApiError::not_found("Task not found"))?;
    // the lab solution is re-verified by the server with the lab engine: the client's word for "solved" cannot be trusted
    if let Some(reason) = crate::labs::check(&state, lang, &me.user.id, book, chapter, &task_id, &b.solution).await? {
        return Err(ApiError::invalid(reason));
    }
    practice::record_attempt(&state.db, practice::Attempt { user: &me.user.id, book, chapter, task: &task_id, code: &b.solution, passed: 1, total: 1, solved: true }).await?;
    if !b.solution.is_empty() {
        // the solution itself is the "draft": it returns to the board on sign-in
        practice::save_draft(&state.db, &me.user.id, book, chapter, &task_id, &b.solution).await?;
    }
    Ok(StatusCode::NO_CONTENT)
}
