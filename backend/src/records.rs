//! Voice recordings for slides: the interface sends audio recorded in the browser (`MediaRecorder`), the server puts the file into
//! `records_dir/<book>/<chapter>/<slide>.<extension>` for the Russian text and `records_dir/en/<book>/<chapter>/…` for the English one
//! (a slide has one file per language: an earlier recording with another extension is deleted). The language is the one the book is served in:
//! a book without a translation into the request language is Russian, and so is its recording.
//! This is an author tool, not student progress: only administrators may write to or delete from the server disk.

use auth::Identity;
use axum::{
    body::{Body, Bytes},
    extract::{DefaultBodyLimit, Path, Request, State},
    http::{header, HeaderMap, StatusCode},
    response::Response,
    routing::{get, post},
    Extension, Json, Router,
};
use tower::ServiceExt;
use tower_http::services::ServeFile;
use serde_json::{json, Value};

use crate::{
    error::{ApiError, ApiResult},
    lang::{self, Lang},
    progress::check_range,
    AppState,
};

const MAX_BYTES: usize = 64 * 1024 * 1024;

pub fn private() -> Router<AppState> {
    Router::new().route("/api/records/{book}/{chapter}/{slide}", post(save).layer(DefaultBodyLimit::max(MAX_BYTES)).delete(remove))
}

/// Listening to a recording: a plain `<audio>` element cannot send the session header, so this route is public (like the lesson audio).
pub fn public() -> Router<AppState> {
    Router::new().route("/api/records/{book}/{chapter}/{slide}/audio", get(audio))
}

/// Folder of a chapter's recordings in a language: Russian (the base text) keeps the original layout, other languages get their own subfolder.
pub fn chapter_dir(records_dir: &std::path::Path, lang: Lang, book: i64, chapter: i64) -> std::path::PathBuf {
    let base = if lang == Lang::Ru { records_dir.to_path_buf() } else { records_dir.join(lang.code()) };
    base.join(book.to_string()).join(chapter.to_string())
}

/// The recorded voice-over of a slide, if there is one in a format the player can seek in (`wav`; the browser converts its recording to it).
pub fn wav_path(records_dir: &std::path::Path, lang: Lang, book: i64, chapter: i64, slide: i64) -> Option<std::path::PathBuf> {
    let p = chapter_dir(records_dir, lang, book, chapter).join(format!("{slide}.wav"));
    p.is_file().then_some(p)
}

/// Address of a slide's recording for the player: the language is in the query because `<audio src>` sends no headers.
pub fn audio_url(lang: Lang, book: i64, chapter: i64, slide: i64) -> String {
    format!("/api/records/{book}/{chapter}/{slide}/audio?lang={}", lang.code())
}

/// The language a book is recorded in for the request language: the request one if the book is translated into it, otherwise Russian.
async fn recorded_lang(state: &AppState, lang: Lang, book: i64) -> ApiResult<Lang> {
    Ok(if lang::translated(&state.db, lang, book).await? { lang } else { Lang::Ru })
}

/// `GET /api/records/{book}/{chapter}/{slide}/audio?lang=` - the file with `Range` support (seeking in the player).
async fn audio(State(state): State<AppState>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>, req: Request) -> ApiResult<Response> {
    let path = wav_path(&state.cfg.records_dir, lang, book, chapter, slide).ok_or_else(|| ApiError::not_found("Audio not found"))?;
    serve(path, req).await
}

/// A file as a response with `Range`, `Content-Type` and `Last-Modified` (without it the browser cannot seek in the audio).
pub async fn serve(path: std::path::PathBuf, req: Request) -> ApiResult<Response> {
    let res = ServeFile::new(path).oneshot(req).await.map_err(|_| ApiError::not_found("Audio not found"))?;
    Ok(res.map(Body::new))
}

/// File extension by the recording content type (`audio/webm;codecs=opus` -> `webm`); an unknown type is not accepted.
pub fn extension(content_type: &str) -> Option<&'static str> {
    let mime = content_type.split(';').next().unwrap_or("").trim().to_ascii_lowercase();
    match mime.as_str() {
        "audio/webm" | "video/webm" => Some("webm"),
        "audio/ogg" => Some("ogg"),
        "audio/mp4" | "audio/x-m4a" => Some("m4a"),
        "video/mp4" => Some("mp4"),
        "audio/wav" | "audio/x-wav" | "audio/wave" => Some("wav"),
        "audio/mpeg" => Some("mp3"),
        _ => None,
    }
}

/// `POST /api/records/{book}/{chapter}/{slide}` - the whole request body, type in `Content-Type`; the response - the file path and size.
async fn save(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>, headers: HeaderMap, body: Bytes) -> ApiResult<Json<Value>> {
    if !me.has_role(Identity::SUPERUSER_ROLE) {
        return Err(ApiError::new(403, "Recording is available to administrators only"));
    }
    check_range("book", book, 1, 1000)?;
    check_range("chapter", chapter, 0, 1000)?;
    check_range("slide", slide, 0, 500)?;
    let content_type = headers.get(header::CONTENT_TYPE).and_then(|v| v.to_str().ok()).unwrap_or("");
    let ext = extension(content_type).ok_or_else(|| ApiError::invalid("Unsupported recording format"))?;
    if body.is_empty() {
        return Err(ApiError::invalid("The recording is empty"));
    }

    let lang = recorded_lang(&state, lang, book).await?;
    let dir = chapter_dir(&state.cfg.records_dir, lang, book, chapter);
    let path = dir.join(format!("{slide}.{ext}"));
    let bytes = body.len();
    let written = path.clone();
    tokio::task::spawn_blocking(move || -> std::io::Result<()> {
        std::fs::create_dir_all(&dir)?;
        remove_slide_files(&dir, slide, Some(&written))?;
        std::fs::write(&written, &body)
    })
    .await
    .map_err(|e| anyhow::anyhow!("writing file: {e}"))?
    .map_err(|e| anyhow::anyhow!("writing file {}: {e}", path.display()))?;
    tracing::info!("slide recording {lang:?} {book}/{chapter}/{slide}: {} ({bytes} bytes)", path.display());
    Ok(Json(json!({ "path": path.to_string_lossy(), "bytes": bytes, "audio": audio_url(lang, book, chapter, slide), "lang": lang.code() })))
}

/// Deletes the files of a slide (any extension) in a chapter folder, except `keep`; returns how many were removed.
fn remove_slide_files(dir: &std::path::Path, slide: i64, keep: Option<&std::path::Path>) -> std::io::Result<usize> {
    let prefix = format!("{slide}.");
    let mut removed = 0;
    for entry in std::fs::read_dir(dir)?.flatten() {
        if entry.file_name().to_string_lossy().starts_with(&prefix) && Some(entry.path().as_path()) != keep {
            std::fs::remove_file(entry.path())?;
            removed += 1;
        }
    }
    Ok(removed)
}

/// `DELETE /api/records/{book}/{chapter}/{slide}` - deletes the slide's recording in the request language (administrators only); 404 if there is none.
async fn remove(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>) -> ApiResult<StatusCode> {
    if !me.has_role(Identity::SUPERUSER_ROLE) {
        return Err(ApiError::new(403, "Recording is available to administrators only"));
    }
    check_range("book", book, 1, 1000)?;
    check_range("chapter", chapter, 0, 1000)?;
    check_range("slide", slide, 0, 500)?;
    let lang = recorded_lang(&state, lang, book).await?;
    let dir = chapter_dir(&state.cfg.records_dir, lang, book, chapter);
    let removed = tokio::task::spawn_blocking(move || if dir.is_dir() { remove_slide_files(&dir, slide, None) } else { Ok(0) })
        .await
        .map_err(|e| anyhow::anyhow!("deleting file: {e}"))?
        .map_err(|e| anyhow::anyhow!("deleting recording: {e}"))?;
    if removed == 0 {
        return Err(ApiError::not_found("Recording not found"));
    }
    tracing::info!("slide recording deleted {lang:?} {book}/{chapter}/{slide}");
    Ok(StatusCode::NO_CONTENT)
}

#[cfg(test)]
mod tests {
    use super::extension;

    #[test]
    fn extension_follows_the_container_and_ignores_codecs() {
        assert_eq!(extension("audio/webm;codecs=opus"), Some("webm"));
        assert_eq!(extension("audio/mp4"), Some("m4a"));
        assert_eq!(extension("AUDIO/OGG; codecs=opus"), Some("ogg"));
        assert_eq!(extension("text/plain"), None);
        assert_eq!(extension(""), None);
    }
}
