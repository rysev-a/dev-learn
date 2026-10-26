//! Слайды глав: схемы (сцены из кадров) и блоки тела слайда — данные, которые рисует клиент.

use axum::{
    extract::{Path, State},
    routing::get,
    Json, Router,
};
use serde_json::{json, Value};

use crate::{
    error::{i, s, ApiError, ApiResult},
    AppState,
};

pub fn routes() -> Router<AppState> {
    Router::new().route("/api/slides", get(list)).route("/api/slides/{book}/{chapter}", get(chapter))
}

/// Главы, у которых есть слайды: `[{book, chapter, slides}]` (по нему клиент решает, показывать ли вкладку «Теория»).
async fn list(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    let mut res = state.db.query("SELECT book, chapter, slides FROM slide_chapters ORDER BY book, chapter").await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(Json(Value::Array(rows.iter().map(|r| json!({ "book": i(r, "book"), "chapter": i(r, "chapter"), "slides": i(r, "slides") })).collect())))
}

/// Слайды главы: рубрика и слайды по порядку (`title`, `sub`, `short`, `main`, `body` — блоки).
async fn chapter(State(state): State<AppState>, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT rubric FROM slide_chapters WHERE book = $b AND chapter = $c; SELECT title, sub, short, main, body, idx FROM slides WHERE book = $b AND chapter = $c ORDER BY idx")
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let head: Vec<Value> = res.take(0)?;
    let rows: Vec<Value> = res.take(1)?;
    let Some(head) = head.first() else { return Err(ApiError::not_found("У этой главы нет слайдов")) };
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
