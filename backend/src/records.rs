//! Voice recordings for slides: the interface sends audio recorded in the browser (`MediaRecorder`), the server puts the file into
//! `records_dir/<book>/<chapter>/<slide>.<extension>` (a slide has one file: an earlier recording with another extension is deleted).
//! This is an author tool, not student progress: only administrators may write to the server disk.

use auth::Identity;
use axum::{
    body::{Body, Bytes},
    extract::{DefaultBodyLimit, Path, Request, State},
    http::{header, HeaderMap},
    response::Response,
    routing::{get, post},
    Extension, Json, Router,
};
use tower::ServiceExt;
use tower_http::services::ServeFile;
use serde_json::{json, Value};

use crate::{
    error::{ApiError, ApiResult},
    progress::check_range,
    AppState,
};

const MAX_BYTES: usize = 64 * 1024 * 1024;

pub fn private() -> Router<AppState> {
    Router::new().route("/api/records/{book}/{chapter}/{slide}", post(save).layer(DefaultBodyLimit::max(MAX_BYTES)))
}

/// Listening to a recording: a plain `<audio>` element cannot send the session header, so this route is public (like the lesson audio).
pub fn public() -> Router<AppState> {
    Router::new().route("/api/records/{book}/{chapter}/{slide}/audio", get(audio))
}

/// The recorded voice-over of a slide, if there is one in a format the player can seek in (`wav`; the browser converts its recording to it).
pub fn wav_path(records_dir: &std::path::Path, book: i64, chapter: i64, slide: i64) -> Option<std::path::PathBuf> {
    let p = records_dir.join(book.to_string()).join(chapter.to_string()).join(format!("{slide}.wav"));
    p.is_file().then_some(p)
}

/// `GET /api/records/{book}/{chapter}/{slide}/audio` - the file with `Range` support (seeking in the player).
async fn audio(State(state): State<AppState>, Path((book, chapter, slide)): Path<(i64, i64, i64)>, req: Request) -> ApiResult<Response> {
    let path = wav_path(&state.cfg.records_dir, book, chapter, slide).ok_or_else(|| ApiError::not_found("Audio not found"))?;
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
async fn save(State(state): State<AppState>, Extension(me): Extension<Identity>, Path((book, chapter, slide)): Path<(i64, i64, i64)>, headers: HeaderMap, body: Bytes) -> ApiResult<Json<Value>> {
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

    let dir = state.cfg.records_dir.join(book.to_string()).join(chapter.to_string());
    let path = dir.join(format!("{slide}.{ext}"));
    let bytes = body.len();
    let written = path.clone();
    tokio::task::spawn_blocking(move || -> std::io::Result<()> {
        std::fs::create_dir_all(&dir)?;
        let stale = format!("{slide}.");
        for entry in std::fs::read_dir(&dir)?.flatten() {
            let name = entry.file_name();
            if name.to_string_lossy().starts_with(&stale) && entry.path() != written {
                std::fs::remove_file(entry.path())?;
            }
        }
        std::fs::write(&written, &body)
    })
    .await
    .map_err(|e| anyhow::anyhow!("writing file: {e}"))?
    .map_err(|e| anyhow::anyhow!("writing file {}: {e}", path.display()))?;
    tracing::info!("slide recording {book}/{chapter}/{slide}: {} ({bytes} bytes)", path.display());
    Ok(Json(json!({ "path": path.to_string_lossy(), "bytes": bytes })))
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
