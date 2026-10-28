//! Answer-entry tasks: statements and hints without answers; the server checks the answer (like `answers/router.py`).

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    routing::{delete, get, post},
    Extension, Json, Router,
};
use auth::Identity;
use serde::Deserialize;
use serde_json::{json, Map, Value};

use crate::{
    error::{i, s, ApiError, ApiResult},
    lang::{self, Lang},
    progress::check_range,
    AppState,
};

pub fn public() -> Router<AppState> {
    Router::new().route("/api/answers", get(summary))
}

pub fn private() -> Router<AppState> {
    Router::new().route("/api/answers", delete(reset)).route("/api/answers/{book_id}/{chapter}", get(get_set)).route("/api/answers/{book_id}/{chapter}/check", post(check))
}

async fn summary(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    Ok(Json(crate::quizzes::counts(&state.db, "answer_tasks").await?))
}

/// Whitespace, case, comma as the decimal separator (the first comma before a digit).
fn normalize(v: &str) -> String {
    let s = v.split_whitespace().collect::<Vec<_>>().join(" ").to_lowercase();
    let chars: Vec<char> = s.chars().collect();
    let mut out = String::new();
    let mut replaced = false;
    for (n, c) in chars.iter().enumerate() {
        if !replaced && *c == ',' && chars.get(n + 1).is_some_and(char::is_ascii_digit) {
            out.push('.');
            replaced = true;
        } else {
            out.push(*c);
        }
    }
    out
}

fn as_number(v: &str) -> Option<f64> {
    let t = v.strip_prefix('-').unwrap_or(v);
    let (int, frac) = match t.split_once('.') {
        Some((a, b)) => (a, Some(b)),
        None => (t, None),
    };
    let digits = |x: &str| !x.is_empty() && x.chars().all(|c| c.is_ascii_digit());
    (digits(int) && frac.is_none_or(digits)).then(|| v.parse().ok()).flatten()
}

pub fn is_correct(given: &str, answers: &[String]) -> bool {
    let a = normalize(given);
    if a.is_empty() {
        return false;
    }
    answers.iter().any(|ans| {
        let b = normalize(ans);
        match (as_number(&a), as_number(&b)) {
            (Some(x), Some(y)) => (x - y).abs() < 1e-9,
            _ => a == b,
        }
    })
}

async fn load(state: &AppState, lang: Lang, book: i64, chapter: i64) -> ApiResult<Option<(String, Vec<Value>)>> {
    let tr = lang::translated(&state.db, lang, book).await?;
    let (sets_t, cond) = lang::source("answer_sets", tr);
    let (tasks_t, _) = lang::source("answer_tasks", tr);
    let mut res = state
        .db
        .query(format!("SELECT title FROM {sets_t} WHERE book = $b AND chapter = $c{cond}"))
        .query(format!("SELECT q, answers, hint FROM {tasks_t} WHERE book = $b AND chapter = $c{cond} ORDER BY ord"))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("l", lang.code()))
        .await?;
    let head: Vec<Value> = res.take(0)?;
    let Some(head) = head.into_iter().next() else { return Ok(None) };
    Ok(Some((s(&head, "title"), res.take(1)?)))
}

/// Statements and hints; `solved` - the tasks the user has solved with an accepted answer.
async fn get_set(State(state): State<AppState>, lang: Lang, Extension(me): Extension<Identity>, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let (title, tasks) = load(&state, lang, book, chapter).await?.ok_or_else(|| ApiError::not_found("This chapter has no answer-entry exercises"))?;
    let mut res = state
        .db
        .query("SELECT idx, answer FROM answer_solved WHERE user = $u AND book = $b AND chapter = $c")
        .bind(("u", me.user.id))
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let rows: Vec<Value> = res.take(0)?;
    let solved: Map<String, Value> = rows.iter().map(|r| (i(r, "idx").to_string(), json!(s(r, "answer")))).collect();
    Ok(Json(json!({
        "kind": "practice", "title": title,
        "tasks": tasks.iter().map(|t| json!({ "q": s(t, "q"), "hint": s(t, "hint") })).collect::<Vec<_>>(),
        "solved": solved,
    })))
}

#[derive(Deserialize)]
struct CheckIn {
    task: i64,
    value: String,
}

/// Check an answer. A correct one is recorded as solved; a wrong one changes nothing and does not reveal the right answer.
async fn check(State(state): State<AppState>, lang: Lang, Extension(me): Extension<Identity>, Path((book, chapter)): Path<(i64, i64)>, Json(b): Json<CheckIn>) -> ApiResult<Json<Value>> {
    check_range("task", b.task, 0, 500)?;
    if b.value.chars().count() > 200 {
        return Err(ApiError::invalid("value: at most 200 characters"));
    }
    let (_, tasks) = load(&state, lang, book, chapter).await?.filter(|(_, t)| (b.task as usize) < t.len()).ok_or_else(|| ApiError::not_found("Task not found"))?;
    let answers: Vec<String> = tasks[b.task as usize].get("answers").and_then(Value::as_array).map(|a| a.iter().filter_map(|x| x.as_str().map(String::from)).collect()).unwrap_or_default();
    let ok = is_correct(&b.value, &answers);
    if ok {
        state
            .db
            .query("UPSERT type::record('answer_solved', $k) SET user = $u, book = $b, chapter = $c, idx = $i, answer = $a")
            .bind(("k", format!("{}:{book}:{chapter}:{}", me.user.id, b.task)))
            .bind(("u", me.user.id))
            .bind(("b", book))
            .bind(("c", chapter))
            .bind(("i", b.task))
            .bind(("a", b.value.trim().to_string()))
            .await?
            .check()?;
    }
    Ok(Json(json!({ "ok": ok })))
}

#[derive(Deserialize)]
struct BookChapter {
    book: i64,
    chapter: i64,
}

/// Start the chapter's exercises over.
async fn reset(State(state): State<AppState>, Extension(me): Extension<Identity>, Query(q): Query<BookChapter>) -> ApiResult<StatusCode> {
    check_range("book", q.book, 1, 1000)?;
    check_range("chapter", q.chapter, 0, 1000)?;
    state.db.query("DELETE answer_solved WHERE user = $u AND book = $b AND chapter = $c").bind(("u", me.user.id)).bind(("b", q.book)).bind(("c", q.chapter)).await?.check()?;
    Ok(StatusCode::NO_CONTENT)
}

#[cfg(test)]
mod tests {
    use super::is_correct;

    #[test]
    fn compares_ignoring_case_and_spaces() {
        assert!(is_correct(" 3,5 ", &["3.5".into()]));
        assert!(is_correct("É", &["é".into()]));
        assert!(is_correct("2.0", &["2".into()]));
        assert!(!is_correct("", &["".into()]));
        assert!(!is_correct("12", &["21".into()]));
        assert!(is_correct("a  b", &["a b".into()]));
    }
}
