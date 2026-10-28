//! Chapter slides: diagrams (scenes made of frames) and slide body blocks - data that the client draws.

use axum::{
    extract::{Path, State},
    routing::get,
    Json, Router,
};
use serde_json::{json, Value};

use crate::{
    error::{i, s, ApiError, ApiResult},
    lang::{self, Lang},
    AppState,
};

pub fn routes() -> Router<AppState> {
    Router::new().route("/api/slides", get(list)).route("/api/slides/{book}/{chapter}", get(chapter))
}

/// Chapters that have slides: `[{book, chapter, slides}]` (the client uses it to decide whether to show the "Theory" tab).
async fn list(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    let mut res = state.db.query("SELECT book, chapter, slides FROM slide_chapters ORDER BY book, chapter").await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(Json(Value::Array(rows.iter().map(|r| json!({ "book": i(r, "book"), "chapter": i(r, "chapter"), "slides": i(r, "slides") })).collect())))
}

/// A chapter's slides: rubric and slides in order (`title`, `sub`, `short`, `main`, `body` - blocks).
async fn chapter(State(state): State<AppState>, lang: Lang, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let tr = lang::translated(&state.db, lang, book).await?;
    let (chapters_t, cond) = lang::source("slide_chapters", tr);
    let (slides_t, _) = lang::source("slides", tr);
    let mut res = state
        .db
        .query(format!("SELECT rubric FROM {chapters_t} WHERE book = $b AND chapter = $c{cond}; SELECT title, sub, short, main, body, idx FROM {slides_t} WHERE book = $b AND chapter = $c{cond} ORDER BY idx"))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("l", lang.code()))
        .await?;
    let head: Vec<Value> = res.take(0)?;
    let rows: Vec<Value> = res.take(1)?;
    let Some(head) = head.first() else { return Err(ApiError::not_found("This chapter has no slides")) };
    let slides: Vec<Value> = rows
        .iter()
        .map(|r| {
            let mut o = serde_json::Map::new();
            o.insert("title".into(), json!(s(r, "title")));
            for k in ["sub", "short"] {
                if let Some(v) = r.get(k).filter(|v| !v.is_null()) {
                    o.insert(k.into(), v.clone());
                }
            }
            o.insert("main".into(), json!(s(r, "main")));
            o.insert("body".into(), r.get("body").cloned().unwrap_or_else(|| json!([])));
            Value::Object(o)
        })
        .collect();
    Ok(Json(json!({ "book": book, "chapter": chapter, "rubric": s(head, "rubric"), "slides": slides })))
}
