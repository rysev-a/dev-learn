//! Voice recordings for slides: the interface sends audio recorded in the browser (`MediaRecorder`, converted to WAV), the server keeps
//! every recording as a separate "take": `records_dir/<book>/<chapter>/<slide>/<take>.<extension>` for the Russian text and
//! `records_dir/en/<book>/<chapter>/…` for the English one (the language is the one the book is served in: a book without a translation
//! into the request language is Russian, and so is its recording). Each "Record" makes a new take; the take that voices the slide is the
//! chosen one (file `selected` next to the takes), by default the first. Only administrators write to or delete from the server disk.
//! The pronunciation check of a take (`speech.rs`) is kept next to it as `<take>.score.json` and goes away with the take.
//! A take made by a machine voice (`voice/synth.py`) is an ordinary take with a marker file `<take>.machine` (the voice's name): the list shows it
//! as "Machine voice", it can be chosen, deleted and replaced like the author's own recordings.

use std::path::{Path as FsPath, PathBuf};

use auth::Identity;
use axum::{
    body::{Body, Bytes},
    extract::{DefaultBodyLimit, Path, Request, State},
    http::{header, HeaderMap},
    response::Response,
    routing::{delete, get, post, put},
    Extension, Json, Router,
};
use serde::Deserialize;
use serde_json::{json, Value};
use tower::ServiceExt;
use tower_http::services::ServeFile;

use crate::{
    error::{ApiError, ApiResult},
    lang::{self, Lang},
    progress::check_range,
    speech, wav, AppState,
};

const MAX_BYTES: usize = 64 * 1024 * 1024;
/// File with the number of the chosen take.
const SELECTED: &str = "selected";

pub fn private() -> Router<AppState> {
    Router::new()
        .route("/api/records/{book}/{chapter}/{slide}", get(list).post(save).layer(DefaultBodyLimit::max(MAX_BYTES)))
        .route("/api/records/{book}/{chapter}/{slide}/selected", put(select))
        .route("/api/records/{book}/{chapter}/{slide}/{take}", delete(remove))
        .route("/api/records/{book}/{chapter}/{slide}/{take}/assess", post(assess))
}

/// Listening to a recording: a plain `<audio>` element cannot send the session header, so this route is public (like the lesson audio).
pub fn public() -> Router<AppState> {
    Router::new().route("/api/records/{book}/{chapter}/{slide}/audio", get(audio))
}

/// Folder of a chapter's recordings in a language: Russian (the base text) is the root, other languages get their own subfolder.
pub fn chapter_dir(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64) -> PathBuf {
    let base = if lang == Lang::Ru { records_dir.to_path_buf() } else { records_dir.join(lang.code()) };
    base.join(book.to_string()).join(chapter.to_string())
}

fn slide_dir(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64) -> PathBuf {
    chapter_dir(records_dir, lang, book, chapter).join(slide.to_string())
}

/// A recorded take of a slide in a format the player can seek in (`wav`; the browser converts its recording to it).
pub struct Take {
    pub id: i64,
    pub path: PathBuf,
    /// time of recording, seconds since the epoch
    pub at: u64,
    /// the name of the voice if the take was read by a machine (`voice/synth.py`), `None` for the author's own recording
    pub machine: Option<String>,
}

/// The takes of a slide, by number.
pub fn takes(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64) -> Vec<Take> {
    let Ok(entries) = std::fs::read_dir(slide_dir(records_dir, lang, book, chapter, slide)) else { return Vec::new() };
    let mut all: Vec<Take> = entries
        .flatten()
        .filter_map(|e| {
            let path = e.path();
            (path.extension()?.to_str()? == "wav").then_some(())?;
            let at = std::fs::metadata(&path).and_then(|m| m.modified()).ok().and_then(|m| m.duration_since(std::time::UNIX_EPOCH).ok()).map_or(0, |d| d.as_secs());
            let machine = std::fs::read_to_string(path.with_extension("machine")).ok().map(|v| v.trim().to_string());
            Some(Take { id: path.file_stem()?.to_str()?.parse().ok()?, path, at, machine })
        })
        .collect();
    all.sort_by_key(|t| t.id);
    all
}

/// The take that voices the slide: the chosen one if it still exists, otherwise the first.
pub fn selected(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64) -> Option<Take> {
    let mut all = takes(records_dir, lang, book, chapter, slide);
    let chosen = std::fs::read_to_string(slide_dir(records_dir, lang, book, chapter, slide).join(SELECTED)).ok().and_then(|s| s.trim().parse::<i64>().ok());
    let at = chosen.and_then(|c| all.iter().position(|t| t.id == c)).unwrap_or(0);
    (!all.is_empty()).then(|| all.swap_remove(at))
}

/// Address of a take for the player: the language and the take are in the query because `<audio src>` sends no headers;
/// `v` (the time of recording) changes when a take number is used again, so the browser does not play a cached older file.
pub fn audio_url(lang: Lang, book: i64, chapter: i64, slide: i64, take: &Take) -> String {
    format!("/api/records/{book}/{chapter}/{slide}/audio?lang={}&take={}&v={}", lang.code(), take.id, take.at)
}

fn score_file(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64, take: i64) -> PathBuf {
    slide_dir(records_dir, lang, book, chapter, slide).join(format!("{take}.score.json"))
}

/// The saved pronunciation check of a take, if it was made.
fn stored_assessment(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64, take: i64) -> Value {
    std::fs::read_to_string(score_file(records_dir, lang, book, chapter, slide, take)).ok().and_then(|s| serde_json::from_str(&s).ok()).unwrap_or(Value::Null)
}

fn rounded(seconds: f64) -> f64 {
    (seconds * 10.0).round() / 10.0
}

/// What the interface needs about a slide's recordings: the takes (number, length, time of recording), the chosen one and its address and length.
fn state_json(records_dir: &FsPath, lang: Lang, book: i64, chapter: i64, slide: i64) -> Value {
    let listed: Vec<Value> = takes(records_dir, lang, book, chapter, slide)
        .iter()
        .map(|t| json!({ "id": t.id, "dur": rounded(wav::duration(&t.path)), "at": t.at, "machine": t.machine, "assessment": stored_assessment(records_dir, lang, book, chapter, slide, t.id) }))
        .collect();
    match selected(records_dir, lang, book, chapter, slide) {
        Some(t) => json!({ "takes": listed, "selected": t.id, "audio": audio_url(lang, book, chapter, slide, &t), "dur": rounded(wav::duration(&t.path)) }),
        None => json!({ "takes": listed, "selected": null, "audio": null, "dur": 0.0 }),
    }
}

/// The language a book is recorded in for the request language: the request one if the book is translated into it, otherwise Russian.
async fn recorded_lang(state: &AppState, lang: Lang, book: i64) -> ApiResult<Lang> {
    Ok(if lang::translated(&state.db, lang, book).await? { lang } else { Lang::Ru })
}

fn admin_only(me: &Identity, book: i64, chapter: i64, slide: i64) -> ApiResult<()> {
    if !me.has_role(Identity::SUPERUSER_ROLE) {
        return Err(ApiError::new(403, "Recording is available to administrators only"));
    }
    check_range("book", book, 1, 1000)?;
    check_range("chapter", chapter, 0, 1000)?;
    check_range("slide", slide, 0, 500)
}

/// `take=<n>` from the query string.
fn query_take(query: Option<&str>) -> Option<i64> {
    query?.split('&').find_map(|kv| kv.strip_prefix("take=")?.parse().ok())
}

/// `GET /api/records/{book}/{chapter}/{slide}/audio?lang=&take=` - the file with `Range` support (seeking in the player);
/// without `take` the chosen take.
async fn audio(State(state): State<AppState>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>, req: Request) -> ApiResult<Response> {
    let dir = &state.cfg.records_dir;
    let take = match query_take(req.uri().query()) {
        Some(id) => takes(dir, lang, book, chapter, slide).into_iter().find(|t| t.id == id),
        None => selected(dir, lang, book, chapter, slide),
    };
    serve(take.ok_or_else(|| ApiError::not_found("Audio not found"))?.path, req).await
}

/// A file as a response with `Range`, `Content-Type` and `Last-Modified` (without it the browser cannot seek in the audio).
pub async fn serve(path: PathBuf, req: Request) -> ApiResult<Response> {
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

/// `GET /api/records/{book}/{chapter}/{slide}` - the slide's takes in the request language (administrators only).
async fn list(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>) -> ApiResult<Json<Value>> {
    admin_only(&me, book, chapter, slide)?;
    let lang = recorded_lang(&state, lang, book).await?;
    Ok(Json(state_json(&state.cfg.records_dir, lang, book, chapter, slide)))
}

/// `POST /api/records/{book}/{chapter}/{slide}` - the whole request body is a new take, type in `Content-Type`; the response is the slide's state
/// plus the new take's `id`, `path` and `bytes`. The new take does not replace the chosen one (the first take voices the slide until another is chosen).
async fn save(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>, headers: HeaderMap, body: Bytes) -> ApiResult<Json<Value>> {
    admin_only(&me, book, chapter, slide)?;
    let content_type = headers.get(header::CONTENT_TYPE).and_then(|v| v.to_str().ok()).unwrap_or("");
    let ext = extension(content_type).ok_or_else(|| ApiError::invalid("Unsupported recording format"))?;
    if body.is_empty() {
        return Err(ApiError::invalid("The recording is empty"));
    }

    let lang = recorded_lang(&state, lang, book).await?;
    let records = state.cfg.records_dir.clone();
    let dir = slide_dir(&records, lang, book, chapter, slide);
    let bytes = body.len();
    let (id, path) = tokio::task::spawn_blocking(move || -> std::io::Result<(i64, PathBuf)> {
        std::fs::create_dir_all(&dir)?;
        let last = std::fs::read_dir(&dir)?.flatten().filter_map(|e| e.path().file_stem()?.to_str()?.parse::<i64>().ok()).max().unwrap_or(0);
        let path = dir.join(format!("{}.{ext}", last + 1));
        std::fs::write(&path, &body)?;
        Ok((last + 1, path))
    })
    .await
    .map_err(|e| anyhow::anyhow!("writing file: {e}"))?
    .map_err(|e| anyhow::anyhow!("writing recording: {e}"))?;
    tracing::info!("slide recording {lang:?} {book}/{chapter}/{slide}: take {id}, {} ({bytes} bytes)", path.display());
    let mut out = state_json(&records, lang, book, chapter, slide);
    out["id"] = json!(id);
    out["path"] = json!(path.to_string_lossy());
    out["bytes"] = json!(bytes);
    Ok(Json(out))
}

#[derive(Deserialize)]
struct Choice {
    id: i64,
}

/// `PUT /api/records/{book}/{chapter}/{slide}/selected` `{id}` - the take that voices the slide.
async fn select(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide)): Path<(i64, i64, i64)>, Json(choice): Json<Choice>) -> ApiResult<Json<Value>> {
    admin_only(&me, book, chapter, slide)?;
    let lang = recorded_lang(&state, lang, book).await?;
    let records = state.cfg.records_dir.clone();
    if !takes(&records, lang, book, chapter, slide).iter().any(|t| t.id == choice.id) {
        return Err(ApiError::not_found("Recording not found"));
    }
    let file = slide_dir(&records, lang, book, chapter, slide).join(SELECTED);
    std::fs::write(&file, choice.id.to_string()).map_err(|e| anyhow::anyhow!("writing {}: {e}", file.display()))?;
    Ok(Json(state_json(&records, lang, book, chapter, slide)))
}

/// `DELETE /api/records/{book}/{chapter}/{slide}/{take}` - deletes one take (administrators only); 404 if there is none.
/// The response is the slide's state: if the chosen take was deleted, the first one voices the slide.
async fn remove(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide, take)): Path<(i64, i64, i64, i64)>) -> ApiResult<Json<Value>> {
    admin_only(&me, book, chapter, slide)?;
    let lang = recorded_lang(&state, lang, book).await?;
    let records = state.cfg.records_dir.clone();
    let dir = slide_dir(&records, lang, book, chapter, slide);
    let removed = tokio::task::spawn_blocking(move || -> std::io::Result<usize> {
        let Ok(entries) = std::fs::read_dir(&dir) else { return Ok(0) };
        let mut removed = 0;
        for entry in entries.flatten() {
            if entry.path().file_stem().and_then(|s| s.to_str()).and_then(|s| s.parse::<i64>().ok()) == Some(take) {
                std::fs::remove_file(entry.path())?;
                removed += 1;
            }
        }
        let _ = std::fs::remove_file(dir.join(format!("{take}.score.json")));
        let chosen = std::fs::read_to_string(dir.join(SELECTED)).ok().and_then(|s| s.trim().parse::<i64>().ok());
        if chosen == Some(take) {
            let _ = std::fs::remove_file(dir.join(SELECTED));
        }
        let _ = std::fs::remove_dir(&dir); // only when it is empty
        Ok(removed)
    })
    .await
    .map_err(|e| anyhow::anyhow!("deleting file: {e}"))?
    .map_err(|e| anyhow::anyhow!("deleting recording: {e}"))?;
    if removed == 0 {
        return Err(ApiError::not_found("Recording not found"));
    }
    tracing::info!("slide recording deleted {lang:?} {book}/{chapter}/{slide}: take {take}");
    Ok(Json(state_json(&records, lang, book, chapter, slide)))
}

/// The slide's paragraph in the language of the recording: what the author reads, and the text the pronunciation is checked against.
async fn lesson_text(state: &AppState, lang: Lang, book: i64, chapter: i64, slide: i64) -> ApiResult<String> {
    let (lessons, cond) = lang::source("lessons", lang != Lang::Ru);
    let mut res = state.db.query("SELECT VALUE cid FROM chapters WHERE bid = $b AND num = $n").bind(("b", book)).bind(("n", chapter)).await?;
    let cid: Vec<i64> = res.take(0)?;
    let cid = cid.first().copied().ok_or_else(|| ApiError::not_found("Chapter not found"))?;
    let mut res = state.db.query(format!("SELECT VALUE text FROM {lessons} WHERE cid = $c AND ord = $o{cond}")).bind(("c", cid)).bind(("o", slide)).bind(("l", lang.code())).await?;
    let text: Vec<String> = res.take(0)?;
    text.into_iter().next().ok_or_else(|| ApiError::not_found("Slide not found"))
}

/// `POST /api/records/{book}/{chapter}/{slide}/{take}/assess` - checks the pronunciation of a take against the slide's text with the speech
/// service, saves the result next to the take and returns it (administrators only). A new check replaces the previous one.
async fn assess(State(state): State<AppState>, Extension(me): Extension<Identity>, lang: Lang, Path((book, chapter, slide, take)): Path<(i64, i64, i64, i64)>) -> ApiResult<Json<Value>> {
    admin_only(&me, book, chapter, slide)?;
    let service = state.cfg.speech.clone().ok_or_else(|| ApiError::new(503, "The pronunciation service is not configured"))?;
    let lang = recorded_lang(&state, lang, book).await?;
    let records = state.cfg.records_dir.clone();
    let found = takes(&records, lang, book, chapter, slide).into_iter().find(|t| t.id == take).ok_or_else(|| ApiError::not_found("Recording not found"))?;
    if wav::duration(&found.path) > speech::MAX_SECONDS {
        return Err(ApiError::invalid("The recording is longer than two minutes"));
    }
    let text = lesson_text(&state, lang, book, chapter, slide).await?;
    let path = found.path.clone();
    let samples = tokio::task::spawn_blocking(move || wav::speech_samples(&path))
        .await
        .map_err(|e| anyhow::anyhow!("converting recording: {e}"))?
        .ok_or_else(|| ApiError::invalid("The recording cannot be read"))?;
    let now = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_secs());
    let result = service.assess(&samples, &text, lang, now).await?;
    let file = score_file(&records, lang, book, chapter, slide, take);
    std::fs::write(&file, result.to_string()).map_err(|e| anyhow::anyhow!("writing {}: {e}", file.display()))?;
    tracing::info!("slide recording checked {lang:?} {book}/{chapter}/{slide}: take {take}, pronunciation {}", result["pron"]);
    Ok(Json(result))
}

/// One-time move of the earlier layout (one file per slide, `<chapter>/<slide>.<ext>`) into takes (`<chapter>/<slide>/1.<ext>`);
/// it runs at start and does nothing when there is nothing to move.
pub fn migrate(records_dir: &FsPath) {
    let numbered = |dir: &FsPath| -> Vec<PathBuf> {
        let Ok(entries) = std::fs::read_dir(dir) else { return Vec::new() };
        entries.flatten().map(|e| e.path()).filter(|p| p.is_dir() && p.file_name().and_then(|n| n.to_str()).is_some_and(|n| n.parse::<i64>().is_ok())).collect()
    };
    let bases = std::iter::once(records_dir.to_path_buf()).chain(Lang::ALL.into_iter().filter(|l| *l != Lang::Ru).map(|l| records_dir.join(l.code())));
    for base in bases {
        for chapter in numbered(&base).iter().flat_map(|book| numbered(book)) {
            let Ok(entries) = std::fs::read_dir(&chapter) else { continue };
            for entry in entries.flatten() {
                let path = entry.path();
                let (Some(stem), Some(ext)) = (path.file_stem().and_then(|s| s.to_str()), path.extension().and_then(|e| e.to_str())) else { continue };
                if !path.is_file() || stem.parse::<i64>().is_err() {
                    continue;
                }
                let dir = chapter.join(stem);
                let target = dir.join(format!("1.{ext}"));
                match std::fs::create_dir_all(&dir).and_then(|_| std::fs::rename(&path, &target)) {
                    Ok(()) => tracing::info!("slide recording moved: {} -> {}", path.display(), target.display()),
                    Err(e) => tracing::warn!("slide recording {} was not moved: {e}", path.display()),
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{extension, query_take};

    #[test]
    fn extension_follows_the_container_and_ignores_codecs() {
        assert_eq!(extension("audio/webm;codecs=opus"), Some("webm"));
        assert_eq!(extension("audio/mp4"), Some("m4a"));
        assert_eq!(extension("AUDIO/OGG; codecs=opus"), Some("ogg"));
        assert_eq!(extension("text/plain"), None);
        assert_eq!(extension(""), None);
    }

    #[test]
    fn the_take_is_read_from_the_query() {
        assert_eq!(query_take(Some("lang=en&take=3")), Some(3));
        assert_eq!(query_take(Some("take=12")), Some(12));
        assert_eq!(query_take(Some("lang=en")), None);
        assert_eq!(query_take(Some("take=x")), None);
        assert_eq!(query_take(None), None);
    }
}
