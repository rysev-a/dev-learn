//! Квизы: вопросы без ответов, ответ и пояснение — после выбора варианта (как `quizzes/router.py`).

use axum::{
    extract::{Path, State},
    routing::{get, post},
    Extension, Json, Router,
};
use auth::Identity;
use serde::Deserialize;
use serde_json::{json, Map, Value};

use crate::{
    error::{i, iso_now, s, ApiError, ApiResult},
    AppState,
};

pub fn public() -> Router<AppState> {
    Router::new().route("/api/quizzes", get(summary))
}

pub fn private() -> Router<AppState> {
    Router::new().route("/api/quizzes/{book_id}/{chapter}", get(get_quiz)).route("/api/quizzes/{book_id}/{chapter}/answer", post(answer))
}

/// Сколько элементов в каждой главе: `{книга: {глава: число}}` (общий для квизов, ответов и упражнений).
pub async fn counts(db: &crate::db::Db, table: &str) -> ApiResult<Value> {
    let mut res = db.query(format!("SELECT book, chapter, count() AS n FROM {table} GROUP BY book, chapter")).await?;
    let rows: Vec<Value> = res.take(0)?;
    let mut out: Map<String, Value> = Map::new();
    for r in &rows {
        if let Some(map) = out.entry(i(r, "book").to_string()).or_insert_with(|| json!({})).as_object_mut() {
            map.insert(i(r, "chapter").to_string(), json!(i(r, "n")));
        }
    }
    Ok(Value::Object(out))
}

async fn summary(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    Ok(Json(counts(&state.db, "quiz_questions").await?))
}

struct Quiz {
    title: String,
    kind: String,
    questions: Vec<Value>,
}

async fn load(state: &AppState, book: i64, chapter: i64) -> ApiResult<Option<Quiz>> {
    let mut res = state
        .db
        .query("SELECT title, kind FROM quizzes WHERE book = $b AND chapter = $c")
        .query("SELECT q, options, answer, expl FROM quiz_questions WHERE book = $b AND chapter = $c ORDER BY ord")
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let head: Vec<Value> = res.take(0)?;
    let Some(head) = head.into_iter().next() else { return Ok(None) };
    Ok(Some(Quiz { title: s(&head, "title"), kind: s(&head, "kind"), questions: res.take(1)? }))
}

async fn picks_of(state: &AppState, user: &str, book: i64, chapter: i64) -> ApiResult<Vec<Option<i64>>> {
    let mut res = state
        .db
        .query("SELECT VALUE picks FROM quiz_picks WHERE user = $u AND book = $b AND chapter = $c")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(rows.first().and_then(Value::as_array).map(|a| a.iter().map(Value::as_i64).collect()).unwrap_or_default())
}

/// Вопросы с вариантами. `reveal[i]` — ответ и пояснение для вопросов, на которые пользователь уже ответил.
async fn get_quiz(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let quiz = load(&state, book, chapter).await?.ok_or_else(|| ApiError::not_found("У этой главы нет вопросов"))?;
    let picks = picks_of(&state, &me.user.id, book, chapter).await?;
    let reveal: Vec<Value> = quiz
        .questions
        .iter()
        .enumerate()
        .map(|(n, q)| if picks.get(n).copied().flatten().is_some() { json!({ "answer": i(q, "answer"), "expl": s(q, "expl") }) } else { Value::Null })
        .collect();
    Ok(Json(json!({
        "kind": quiz.kind, "title": quiz.title,
        "questions": quiz.questions.iter().map(|q| json!({ "q": s(q, "q"), "options": q.get("options").cloned().unwrap_or_else(|| json!([])) })).collect::<Vec<_>>(),
        "reveal": reveal,
    })))
}

#[derive(Deserialize)]
struct AnswerIn {
    question: i64,
    pick: i64,
}

/// Записать выбор и вернуть верный ответ. На вопрос отвечают один раз: повторный запрос ничего не меняет.
async fn answer(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter)): Path<(i64, i64)>, Json(b): Json<AnswerIn>) -> ApiResult<Json<Value>> {
    crate::progress::check_range("question", b.question, 0, 500)?;
    crate::progress::check_range("pick", b.pick, 0, 50)?;
    let quiz = load(&state, book, chapter).await?;
    let quiz = quiz.filter(|q| (b.question as usize) < q.questions.len()).ok_or_else(|| ApiError::not_found("Вопрос не найден"))?;
    let q = &quiz.questions[b.question as usize];
    if b.pick as usize >= q.get("options").and_then(Value::as_array).map_or(0, Vec::len) {
        return Err(ApiError::invalid("Нет такого варианта"));
    }
    let total = quiz.questions.len();
    let mut picks = picks_of(&state, &me.user.id, book, chapter).await?;
    picks.resize(total, None);
    picks.truncate(total);
    if picks[b.question as usize].is_none() {
        picks[b.question as usize] = Some(b.pick);
        state
            .db
            .query("UPSERT type::record('quiz_picks', $k) SET user = $u, book = $b, chapter = $c, picks = $p, updated_at = $at")
            .bind(("k", format!("{}:{book}:{chapter}", me.user.id)))
            .bind(("u", me.user.id.clone()))
            .bind(("b", book))
            .bind(("c", chapter))
            .bind(("p", picks.iter().map(|p| p.map_or(Value::Null, |v| json!(v))).collect::<Vec<_>>()))
            .bind(("at", iso_now()))
            .await?
            .check()?;
    }
    let right = picks.iter().zip(&quiz.questions).filter(|(p, q)| **p == Some(i(q, "answer"))).count();
    Ok(Json(json!({ "pick": picks[b.question as usize], "answer": i(q, "answer"), "expl": s(q, "expl"), "right": right })))
}
