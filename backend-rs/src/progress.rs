//! Прогресс пользователя: слайды, вопросы, упражнения (как `accounts/progress.py`). Всё привязано к (книга, номер главы).

use std::collections::HashMap;

use axum::{
    extract::{Query, State},
    http::StatusCode,
    routing::{delete, get, post},
    Extension, Json, Router,
};
use auth::Identity;
use serde::Deserialize;
use serde_json::{json, Map, Value};

use crate::{
    error::{i, s, ApiError, ApiResult},
    AppState,
};

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/api/progress", get(get_progress).delete(reset_progress))
        .route("/api/progress/slides", post(mark_slide))
        .route("/api/progress/quiz", delete(reset_quiz))
}

pub fn check_range(name: &str, v: i64, lo: i64, hi: i64) -> ApiResult<()> {
    if (lo..=hi).contains(&v) {
        Ok(())
    } else {
        Err(ApiError::invalid(format!("{name}: от {lo} до {hi}")))
    }
}

async fn get_progress(State(state): State<AppState>, Extension(me): Extension<Identity>) -> ApiResult<Json<Value>> {
    let uid = me.user.id;
    let mut res = state
        .db
        .query("SELECT book, chapter, slide FROM slide_views WHERE user = $u ORDER BY slide")
        .query("SELECT book, chapter, picks FROM quiz_picks WHERE user = $u")
        .query("SELECT book, chapter, idx, answer FROM answer_solved WHERE user = $u")
        .query("SELECT book, chapter, tid, status FROM code_status WHERE user = $u")
        .query("SELECT book, chapter, ord, answer FROM quiz_questions ORDER BY book, chapter, ord")
        .bind(("u", uid))
        .await?;
    let views: Vec<Value> = res.take(0)?;
    let picks: Vec<Value> = res.take(1)?;
    let solved: Vec<Value> = res.take(2)?;
    let code: Vec<Value> = res.take(3)?;
    let correct: Vec<Value> = res.take(4)?;

    let key = |r: &Value| format!("{}:{}", i(r, "book"), i(r, "chapter"));
    let mut slides: Map<String, Value> = Map::new();
    for r in &views {
        if let Some(list) = slides.entry(key(r)).or_insert_with(|| json!([])).as_array_mut() {
            list.push(json!(i(r, "slide")));
        }
    }
    let mut answers_of: HashMap<String, Vec<i64>> = HashMap::new();
    for r in &correct {
        answers_of.entry(key(r)).or_default().push(i(r, "answer"));
    }
    let mut quiz = Map::new();
    let mut quiz_right = Map::new();
    for r in &picks {
        let k = key(r);
        let list = r.get("picks").cloned().unwrap_or_else(|| json!([]));
        let right = list
            .as_array()
            .map(|a| a.iter().zip(answers_of.get(&k).map(Vec::as_slice).unwrap_or(&[])).filter(|(p, ans)| p.as_i64() == Some(**ans)).count())
            .unwrap_or(0);
        quiz_right.insert(k.clone(), json!(right));
        quiz.insert(k, list);
    }
    let mut answers: Map<String, Value> = Map::new();
    for r in &solved {
        if let Some(map) = answers.entry(key(r)).or_insert_with(|| json!({})).as_object_mut() {
            map.insert(i(r, "idx").to_string(), json!(s(r, "answer")));
        }
    }
    let mut codes: Map<String, Value> = Map::new();
    for r in &code {
        if let Some(map) = codes.entry(key(r)).or_insert_with(|| json!({})).as_object_mut() {
            map.insert(s(r, "tid"), json!(s(r, "status")));
        }
    }
    Ok(Json(json!({ "slides": slides, "quiz": quiz, "quizRight": quiz_right, "answers": answers, "code": codes })))
}

#[derive(Deserialize)]
struct SlideIn {
    book: i64,
    chapter: i64,
    slide: i64,
}

async fn mark_slide(State(state): State<AppState>, Extension(me): Extension<Identity>, Json(b): Json<SlideIn>) -> ApiResult<StatusCode> {
    check_range("book", b.book, 1, 1000)?;
    check_range("chapter", b.chapter, 0, 1000)?;
    check_range("slide", b.slide, 0, 500)?;
    state
        .db
        .query("UPSERT type::record('slide_views', $k) SET user = $u, book = $b, chapter = $c, slide = $s")
        .bind(("k", format!("{}:{}:{}:{}", me.user.id, b.book, b.chapter, b.slide)))
        .bind(("u", me.user.id))
        .bind(("b", b.book))
        .bind(("c", b.chapter))
        .bind(("s", b.slide))
        .await?
        .check()?;
    Ok(StatusCode::NO_CONTENT)
}

#[derive(Deserialize)]
struct BookChapter {
    book: i64,
    chapter: i64,
}

/// Пройти квиз заново. Выбранные варианты записывает только POST /api/quizzes/…/answer, здесь их можно лишь стереть.
async fn reset_quiz(State(state): State<AppState>, Extension(me): Extension<Identity>, Query(q): Query<BookChapter>) -> ApiResult<StatusCode> {
    check_range("book", q.book, 1, 1000)?;
    check_range("chapter", q.chapter, 0, 1000)?;
    state
        .db
        .query("DELETE quiz_picks WHERE user = $u AND book = $b AND chapter = $c")
        .bind(("u", me.user.id))
        .bind(("b", q.book))
        .bind(("c", q.chapter))
        .await?
        .check()?;
    Ok(StatusCode::NO_CONTENT)
}

#[derive(Deserialize)]
struct Scope {
    scope: String,
}

/// Сбросить упражнения (статусы, черновики, история) или весь прогресс.
async fn reset_progress(State(state): State<AppState>, Extension(me): Extension<Identity>, Query(q): Query<Scope>) -> ApiResult<StatusCode> {
    let mut tables = vec!["code_status", "code_drafts", "code_attempts", "answer_solved"];
    match q.scope.as_str() {
        "practice" => {}
        "all" => tables.extend(["slide_views", "quiz_picks"]),
        _ => return Err(ApiError::invalid("scope: practice или all")),
    }
    for t in tables {
        state.db.query(format!("DELETE {t} WHERE user = $u")).bind(("u", me.user.id.clone())).await?.check()?;
    }
    Ok(StatusCode::NO_CONTENT)
}
