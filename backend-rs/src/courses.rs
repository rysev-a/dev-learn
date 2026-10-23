//! Курс: книги, разделы, главы и аудио уроков (как `books/router.py`).

use std::collections::HashMap;

use axum::{
    extract::{Path, State},
    http::{header, HeaderValue},
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use serde_json::{json, Value};

use crate::{
    error::{i, s, ApiError, ApiResult},
    wav, AppState,
};

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/api/books", get(books))
        .route("/api/books/{book_id}/course", get(book_course))
        .route("/api/chapters/{chapter_id}", get(chapter))
        .route("/api/lesson/{lesson_id}/audio", get(lesson_audio))
        .route("/api/lesson/{lesson_id}/download", get(lesson_download))
        .route("/api/chapters/{chapter_id}/download", get(chapter_download))
}

async fn counts(state: &AppState, table: &str) -> ApiResult<HashMap<i64, i64>> {
    let mut res = state.db.query(format!("SELECT bid, count() AS n FROM {table} GROUP BY bid")).await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(rows.iter().map(|r| (i(r, "bid"), i(r, "n"))).collect())
}

async fn books(State(state): State<AppState>) -> ApiResult<Json<Value>> {
    let mut res = state.db.query("SELECT bid, title, slug, slides_dir, icon, ord FROM books ORDER BY ord").await?;
    let rows: Vec<Value> = res.take(0)?;
    let (sections, chapters, lessons) = (counts(&state, "sections").await?, counts(&state, "chapters").await?, counts(&state, "lessons").await?);
    let out: Vec<Value> = rows
        .iter()
        .map(|b| {
            let id = i(b, "bid");
            json!({
                "id": id, "title": s(b, "title"), "slug": b.get("slug").cloned().unwrap_or(Value::Null),
                "slides_dir": b.get("slides_dir").cloned().unwrap_or(Value::Null), "icon": b.get("icon").cloned().unwrap_or(Value::Null),
                "sections_count": sections.get(&id).copied().unwrap_or(0),
                "lessons_count": chapters.get(&id).copied().unwrap_or(0),
                "parts_count": lessons.get(&id).copied().unwrap_or(0),
            })
        })
        .collect();
    Ok(Json(Value::Array(out)))
}

async fn book_course(State(state): State<AppState>, Path(book_id): Path<i64>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT sid, title, ord FROM sections WHERE bid = $b ORDER BY ord")
        .query("SELECT cid, sid, num, title FROM chapters WHERE bid = $b ORDER BY cid")
        .query("SELECT cid, count() AS n FROM lessons WHERE bid = $b GROUP BY cid")
        .bind(("b", book_id))
        .await?;
    let sections: Vec<Value> = res.take(0)?;
    let chapters: Vec<Value> = res.take(1)?;
    let parts: HashMap<i64, i64> = res.take::<Vec<Value>>(2)?.iter().map(|r| (i(r, "cid"), i(r, "n"))).collect();
    let mut by_section: HashMap<i64, Vec<Value>> = HashMap::new();
    for c in &chapters {
        by_section.entry(i(c, "sid")).or_default().push(json!({
            "id": i(c, "cid"), "num": i(c, "num"), "title": s(c, "title"), "parts_count": parts.get(&i(c, "cid")).copied().unwrap_or(0),
        }));
    }
    Ok(Json(Value::Array(
        sections
            .iter()
            .map(|sec| json!({ "id": i(sec, "sid"), "title": s(sec, "title"), "chapters": by_section.remove(&i(sec, "sid")).unwrap_or_default() }))
            .collect(),
    )))
}

fn audio_path(state: &AppState, id: &str) -> Option<std::path::PathBuf> {
    // id урока — hex от uuid5; всё остальное не пропускаем (никаких «../»)
    if id.is_empty() || !id.chars().all(|c| c.is_ascii_alphanumeric()) {
        return None;
    }
    let p = state.cfg.audio_dir.join(format!("{id}.wav"));
    p.is_file().then_some(p)
}

async fn chapter(State(state): State<AppState>, Path(chapter_id): Path<i64>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT cid, sid, num, title FROM chapters WHERE cid = $c")
        .query("SELECT lid, ord, text FROM lessons WHERE cid = $c ORDER BY ord")
        .bind(("c", chapter_id))
        .await?;
    let ch: Vec<Value> = res.take(0)?;
    let ch = ch.into_iter().next().ok_or_else(|| ApiError::not_found("Chapter not found"))?;
    let lessons: Vec<Value> = res.take(1)?;
    let mut sec = state.db.query("SELECT VALUE title FROM sections WHERE sid = $s").bind(("s", i(&ch, "sid"))).await?;
    let section: Vec<String> = sec.take(0)?;
    let lessons: Vec<Value> = lessons
        .iter()
        .map(|l| {
            let id = s(l, "lid");
            let dur = audio_path(&state, &id).map(|p| wav::duration(&p)).unwrap_or(0.0);
            json!({ "id": id, "ord": i(l, "ord"), "text": s(l, "text"), "audio": format!("/api/lesson/{id}/audio"), "dur": (dur * 10.0).round() / 10.0 })
        })
        .collect();
    Ok(Json(json!({
        "id": i(&ch, "cid"), "num": i(&ch, "num"), "title": s(&ch, "title"),
        "section": section.first().cloned().unwrap_or_default(), "lessons": lessons,
    })))
}

fn wav_response(bytes: Vec<u8>, filename: Option<&str>) -> Response {
    let mut res = ([(header::CONTENT_TYPE, "audio/wav")], bytes).into_response();
    if let Some(name) = filename {
        let encoded: String = name.bytes().map(|b| if b.is_ascii_alphanumeric() || b"-_.~".contains(&b) { (b as char).to_string() } else { format!("%{b:02X}") }).collect();
        if let Ok(v) = HeaderValue::from_str(&format!("attachment; filename*=UTF-8''{encoded}")) {
            res.headers_mut().insert(header::CONTENT_DISPOSITION, v);
        }
    }
    res
}

fn safe_filename(v: &str) -> String {
    let cleaned: String = v.chars().map(|c| if "\\/:*?\"<>|".contains(c) { ' ' } else { c }).collect();
    cleaned.trim().chars().take(80).collect()
}

async fn lesson_audio(State(state): State<AppState>, Path(lesson_id): Path<String>) -> ApiResult<Response> {
    let path = audio_path(&state, &lesson_id).ok_or_else(|| ApiError::not_found("Audio not found"))?;
    let bytes = tokio::fs::read(path).await.map_err(|_| ApiError::not_found("Audio not found"))?;
    Ok(wav_response(bytes, None))
}

async fn lesson_download(State(state): State<AppState>, Path(lesson_id): Path<String>) -> ApiResult<Response> {
    let path = audio_path(&state, &lesson_id).ok_or_else(|| ApiError::not_found("Audio not found"))?;
    let mut res = state.db.query("SELECT cid, ord FROM lessons WHERE lid = $l").bind(("l", lesson_id.clone())).await?;
    let lesson = res.take::<Vec<Value>>(0)?.into_iter().next().ok_or_else(|| ApiError::not_found("Audio not found"))?;
    let mut res = state.db.query("SELECT num, title FROM chapters WHERE cid = $c").bind(("c", i(&lesson, "cid"))).await?;
    let ch = res.take::<Vec<Value>>(0)?.into_iter().next().ok_or_else(|| ApiError::not_found("Audio not found"))?;
    let name = format!("Урок {}. {} — часть {}.wav", i(&ch, "num"), safe_filename(&s(&ch, "title")), i(&lesson, "ord") + 1);
    let bytes = tokio::fs::read(path).await.map_err(|_| ApiError::not_found("Audio not found"))?;
    Ok(wav_response(bytes, Some(&name)))
}

async fn chapter_download(State(state): State<AppState>, Path(chapter_id): Path<i64>) -> ApiResult<Response> {
    let mut res = state
        .db
        .query("SELECT num, title FROM chapters WHERE cid = $c")
        .query("SELECT lid FROM lessons WHERE cid = $c ORDER BY ord")
        .bind(("c", chapter_id))
        .await?;
    let ch = res.take::<Vec<Value>>(0)?.into_iter().next().ok_or_else(|| ApiError::not_found("Chapter not found"))?;
    let lessons: Vec<Value> = res.take(1)?;
    let paths: Vec<std::path::PathBuf> = lessons.iter().filter_map(|l| audio_path(&state, &s(l, "lid"))).collect();
    if paths.is_empty() {
        return Err(ApiError::not_found("Audio not found"));
    }
    let bytes = tokio::task::spawn_blocking(move || wav::concat(&paths))
        .await
        .map_err(|_| ApiError::new(500, "Failed to assemble audio"))?
        .map_err(|e| ApiError::new(500, if e == "форматы различаются" { "Mismatched audio formats" } else { "Failed to assemble audio" }))?;
    let name = format!("Урок {}. {}.wav", i(&ch, "num"), safe_filename(&s(&ch, "title")));
    Ok(wav_response(bytes, Some(&name)))
}
