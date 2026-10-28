//! Упражнения-лаборатории (схемы, симуляторы): условия и сценарии хранятся данными, решение проверяет сервер движком лаборатории.
//!
//! Данные — файлы `labs/<вид>/<книга>-<глава>.json` (`{book, chapter, lab, tasks: [{id, title, statement, hint, spec}]}`),
//! в базе — таблица `lab_tasks`. Клиент получает сценарий без эталонного решения (`spec.solution` / `spec.reference`).

use std::path::{Path as FsPath, PathBuf};

use anyhow::Context;
use axum::{
    extract::{Path, State},
    routing::get,
    Json, Router,
};
use serde_json::{json, Value};

use crate::{
    db::Db,
    error::{i, s, ApiError, ApiResult},
    AppState,
};

pub fn routes() -> Router<AppState> {
    Router::new().route("/api/labs/{book}/{chapter}", get(chapter))
}

/// Строки `lab_tasks` из файлов данных; содержимое файлов входит в хеш пересева.
pub fn load(dir: &FsPath, raw: &mut Vec<u8>) -> anyhow::Result<Vec<Value>> {
    let mut rows = Vec::new();
    if !dir.is_dir() {
        return Ok(rows);
    }
    let mut files: Vec<PathBuf> = Vec::new();
    for kind in std::fs::read_dir(dir)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.is_dir()) {
        files.extend(std::fs::read_dir(kind)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")));
    }
    files.sort();
    for f in files {
        let bytes = std::fs::read(&f)?;
        raw.extend_from_slice(f.to_string_lossy().as_bytes());
        raw.extend_from_slice(&bytes);
        let ch: Value = serde_json::from_slice(&bytes).with_context(|| format!("лаборатория {}", f.display()))?;
        let (book, chapter, lab) = (i(&ch, "book"), i(&ch, "chapter"), s(&ch, "lab"));
        for (ord, t) in ch.get("tasks").and_then(Value::as_array).context("нет tasks")?.iter().enumerate() {
            rows.push(json!({
                "book": book, "chapter": chapter, "lab": lab, "tid": s(t, "id"), "ord": ord,
                "title": s(t, "title"), "statement": s(t, "statement"), "hint": s(t, "hint"),
                "spec": t.get("spec").cloned().unwrap_or(Value::Null),
            }));
        }
    }
    Ok(rows)
}

/// Переведённые тексты упражнений: `<язык>/labs/<вид>/<книга>-<глава>.json` с теми же полями `id`, `title`, `statement`, `hint`;
/// сценарий (`spec`), цели и эталоны — русские, общие для всех языков.
pub fn load_texts(dir: &FsPath, raw: &mut Vec<u8>) -> anyhow::Result<Vec<Value>> {
    let mut rows = Vec::new();
    if !dir.is_dir() {
        return Ok(rows);
    }
    let mut files: Vec<PathBuf> = Vec::new();
    for kind in std::fs::read_dir(dir)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.is_dir()) {
        files.extend(std::fs::read_dir(kind)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")));
    }
    files.sort();
    for f in files {
        let bytes = std::fs::read(&f)?;
        raw.extend_from_slice(f.to_string_lossy().as_bytes());
        raw.extend_from_slice(&bytes);
        let ch: Value = serde_json::from_slice(&bytes).with_context(|| format!("лаборатория {}", f.display()))?;
        let (book, chapter) = (i(&ch, "book"), i(&ch, "chapter"));
        for t in ch.get("tasks").and_then(Value::as_array).context("нет tasks")? {
            // `spec_text`: переведённые подписи внутри сценария по путям JSON (`/goals/0/text`); остальное в сценарии общее
            rows.push(json!({
                "book": book, "chapter": chapter, "tid": s(t, "id"), "title": s(t, "title"), "statement": s(t, "statement"), "hint": s(t, "hint"),
                "spec_text": t.get("spec_text").cloned().unwrap_or_else(|| json!({})),
            }));
        }
    }
    Ok(rows)
}

/// Подставляет переведённые подписи сценария: `texts` — объект «путь JSON → текст».
fn apply_spec_text(spec: &mut Value, texts: &Value) {
    for (path, text) in texts.as_object().into_iter().flatten() {
        if let (Some(slot), true) = (spec.pointer_mut(path), text.is_string()) {
            *slot = text.clone();
        }
    }
}

/// Переведённые подписи сценариев главы: `tid` → `spec_text` (пусто, если книга не переведена на язык).
async fn spec_texts(db: &Db, lang: crate::lang::Lang, book: i64, chapter: i64) -> Result<std::collections::HashMap<String, Value>, surrealdb::Error> {
    let mut out = std::collections::HashMap::new();
    if !crate::lang::translated(db, lang, book).await? {
        return Ok(out);
    }
    let mut res = db.query("SELECT tid, spec_text FROM lab_tasks_i18n WHERE book = $b AND chapter = $c AND lang = $l").bind(("b", book)).bind(("c", chapter)).bind(("l", lang.code())).await?;
    let rows: Vec<Value> = res.take(0)?;
    for r in rows {
        out.insert(s(&r, "tid"), r.get("spec_text").cloned().unwrap_or(Value::Null));
    }
    Ok(out)
}

/// Копия сценария для клиента: без эталонного решения.
fn public_spec(spec: &Value) -> Value {
    let mut spec = spec.clone();
    if let Some(o) = spec.as_object_mut() {
        // эталон: у схем и сетей — `solution`, у программ RISC-V — `reference`
        for key in ["solution", "reference"] {
            o.remove(key);
        }
    }
    spec
}

/// Упражнения-лаборатории главы: условия и сценарии без эталонов.
async fn chapter(State(state): State<AppState>, lang: crate::lang::Lang, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT tid, lab, title, statement, hint, spec, ord FROM lab_tasks WHERE book = $b AND chapter = $c ORDER BY ord")
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let mut rows: Vec<Value> = res.take(0)?;
    let Some(first) = rows.first() else { return Err(ApiError::not_found("This chapter has no lab exercises")) };
    let lab = s(first, "lab");
    crate::lang::overlay(&state.db, "lab_tasks_i18n", lang, book, chapter, &mut rows, &["title", "statement", "hint"]).await?;
    let texts = spec_texts(&state.db, lang, book, chapter).await?;
    let tasks: Vec<Value> = rows
        .iter()
        .map(|r| {
            let mut spec = public_spec(r.get("spec").unwrap_or(&Value::Null));
            if let Some(t) = texts.get(&s(r, "tid")) {
                apply_spec_text(&mut spec, t);
            }
            json!({ "id": s(r, "tid"), "title": s(r, "title"), "statement": s(r, "statement"), "hint": s(r, "hint"), "spec": spec })
        })
        .collect();
    Ok(Json(json!({ "lab": lab, "tasks": tasks })))
}

/// Проверка решения упражнения-лаборатории. `None` — решение верное (или у упражнения нет данных лаборатории: старые задачи
/// принимаются как раньше); `Some(причина)` — отказ.
pub async fn check(state: &AppState, lang: crate::lang::Lang, user: &str, book: i64, chapter: i64, tid: &str, solution: &str) -> ApiResult<Option<String>> {
    let mut res = state
        .db
        .query("SELECT lab, spec FROM lab_tasks WHERE book = $b AND chapter = $c AND tid = $t")
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", tid.to_string()))
        .await?;
    let rows: Vec<Value> = res.take(0)?;
    let Some(row) = rows.first() else {
        tracing::warn!("лаборатория {book}:{chapter}/{tid}: нет данных, решение принято без проверки");
        return Ok(None);
    };
    let mut spec = row.get("spec").cloned().unwrap_or(Value::Null);
    // подписи целей в причинах отказа — на языке запроса
    if let Some(t) = spec_texts(&state.db, lang, book, chapter).await?.get(tid) {
        apply_spec_text(&mut spec, t);
    }
    let solution = solution.to_string();
    let lab = s(row, "lab");
    // составные блоки схем собираются из решений самого ученика (черновики главы — как `hydrate.ts` в React)
    let drafts = if lab == "arch" { drafts(&state.db, user, book).await? } else { Vec::new() };
    let arch = state.arch.clone();
    let chapter = u32::try_from(chapter).unwrap_or(0);
    let tid = tid.to_string();
    let locale = lang.locale();
    // расчёт движка — блокирующая работа; причины отказа — на языке запроса
    tokio::task::spawn_blocking(move || i18n::with_locale(locale, || match lab.as_str() {
        "arch" => {
            let rows: Vec<(u32, &str, &str)> = drafts.iter().map(|(c, id, code)| (*c, id.as_str(), code.as_str())).collect();
            let store = archlab::DraftStore::from_drafts(&arch, rows);
            let verdict = arch.verify_unlocked(chapter, &tid, &solution, &store);
            (!verdict.ok).then_some(verdict.message)
        }
        _ => verify(&lab, spec, &solution),
    }))
    .await
    .map_err(|e| ApiError::from(anyhow::anyhow!(e)))
}

/// Решения ученика по книге: (глава, id упражнения, JSON/текст) — только решённые упражнения (статус `ok`):
/// черновик нерешённого упражнения блоков и составных элементов не открывает.
async fn drafts(db: &Db, user: &str, book: i64) -> ApiResult<Vec<(u32, String, String)>> {
    let mut res = db
        .query("SELECT chapter, tid, code FROM code_drafts WHERE user = $u AND book = $b; SELECT chapter, tid FROM code_status WHERE user = $u AND book = $b AND status = 'ok'")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .await?;
    let (rows, solved): (Vec<Value>, Vec<Value>) = (res.take(0)?, res.take(1)?);
    let done: std::collections::HashSet<(i64, String)> = solved.iter().map(|r| (i(r, "chapter"), s(r, "tid"))).collect();
    Ok(rows.iter().filter(|r| done.contains(&(i(r, "chapter"), s(r, "tid")))).map(|r| (u32::try_from(i(r, "chapter")).unwrap_or(0), s(r, "tid"), s(r, "code"))).collect())
}

/// Диспетчер по виду лаборатории.
fn verify(lab: &str, spec: Value, solution: &str) -> Option<String> {
    match lab {
        "sd" => {
            let scenario: sdlab::Scenario = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Scenario is damaged: {0}", e)),
            };
            match sdlab::verify_raw(&scenario, solution) {
                Ok(v) if v.ok => None,
                Ok(v) => Some(v.reason().unwrap_or_else(|| i18n::tr("Solution not accepted").into())),
                Err(e) => Some(e.to_string()),
            }
        }
        "virt" => {
            let spec: virtlab::Spec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Scenario is damaged: {0}", e)),
            };
            let submitted: Value = match serde_json::from_str(solution) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Solution could not be parsed: {0}", e)),
            };
            // строго: цель без записи действий (trace), которую нечем перепроверить, не засчитывается — клиент присылает записи
            let verdict = virtlab::verify_with(&spec, &submitted, virtlab::Strictness::Strict);
            (!verdict.solved).then(|| verdict.first_rejection().unwrap_or_else(|| i18n::tr("Solution not accepted").into()))
        }
        "net" => {
            let spec: netlab::NetSpec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Scenario is damaged: {0}", e)),
            };
            let verdict = netlab::verify_json(&spec, solution);
            (!verdict.ok).then(|| {
                verdict
                    .error
                    .clone()
                    .or_else(|| verdict.goals.iter().find(|g| !g.ok).map(|g| i18n::trf!("Goal not met: {0}", g.text)))
                    .unwrap_or_else(|| i18n::tr("Solution not accepted").into())
            })
        }
        "riscv" => {
            let spec: riscvlab::task::TaskSpec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Scenario is damaged: {0}", e)),
            };
            let verdict = riscvlab::task::verify(&spec, solution);
            (!verdict.ok).then_some(verdict.message)
        }
        "web" => {
            let task: weblab::Task = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Exercise is damaged: {0}", e)),
            };
            let submitted: weblab::Solution = match serde_json::from_str(solution) {
                Ok(v) => v,
                Err(e) => return Some(i18n::trf!("Solution could not be parsed: {0}", e)),
            };
            let report = weblab::verify(&task, &submitted);
            (!report.ok()).then(|| report.reason().unwrap_or_else(|| i18n::tr("Solution not accepted").into()))
        }
        other => {
            tracing::warn!("вид лаборатории «{other}»: проверки на сервере пока нет, решение принято");
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::apply_spec_text;

    #[test]
    fn spec_text_replaces_only_the_named_strings() {
        let mut spec = json!({ "goals": [{ "id": "g1", "text": "ПК 1 пингует ПК 2" }], "start": { "devices": [{ "name": "ПК 1" }] } });
        apply_spec_text(&mut spec, &json!({ "/goals/0/text": "PC 1 pings PC 2", "/start/devices/0/name": "PC 1", "/missing/0": "x" }));
        assert_eq!(spec, json!({ "goals": [{ "id": "g1", "text": "PC 1 pings PC 2" }], "start": { "devices": [{ "name": "PC 1" }] } }));
    }
}
