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
async fn chapter(State(state): State<AppState>, Path((book, chapter)): Path<(i64, i64)>) -> ApiResult<Json<Value>> {
    let mut res = state
        .db
        .query("SELECT tid, lab, title, statement, hint, spec, ord FROM lab_tasks WHERE book = $b AND chapter = $c ORDER BY ord")
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let rows: Vec<Value> = res.take(0)?;
    let Some(first) = rows.first() else { return Err(ApiError::not_found("У этой главы нет лабораторных упражнений")) };
    let lab = s(first, "lab");
    let tasks: Vec<Value> = rows
        .iter()
        .map(|r| json!({ "id": s(r, "tid"), "title": s(r, "title"), "statement": s(r, "statement"), "hint": s(r, "hint"), "spec": public_spec(r.get("spec").unwrap_or(&Value::Null)) }))
        .collect();
    Ok(Json(json!({ "lab": lab, "tasks": tasks })))
}

/// Проверка решения упражнения-лаборатории. `None` — решение верное (или у упражнения нет данных лаборатории: старые задачи
/// принимаются как раньше); `Some(причина)` — отказ.
pub async fn check(state: &AppState, user: &str, book: i64, chapter: i64, tid: &str, solution: &str) -> ApiResult<Option<String>> {
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
    let spec = row.get("spec").cloned().unwrap_or(Value::Null);
    let solution = solution.to_string();
    let lab = s(row, "lab");
    // составные блоки схем собираются из решений самого ученика (черновики главы — как `hydrate.ts` в React)
    let drafts = if lab == "arch" { drafts(&state.db, user, book).await? } else { Vec::new() };
    let arch = state.arch.clone();
    let chapter = u32::try_from(chapter).unwrap_or(0);
    let tid = tid.to_string();
    // расчёт движка — блокирующая работа
    tokio::task::spawn_blocking(move || match lab.as_str() {
        "arch" => {
            let rows: Vec<(u32, &str, &str)> = drafts.iter().map(|(c, id, code)| (*c, id.as_str(), code.as_str())).collect();
            let store = archlab::DraftStore::from_drafts(&arch, rows);
            let verdict = arch.verify_unlocked(chapter, &tid, &solution, &store);
            (!verdict.ok).then_some(verdict.message)
        }
        _ => verify(&lab, spec, &solution),
    })
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
                Err(e) => return Some(format!("сценарий повреждён: {e}")),
            };
            match sdlab::verify_raw(&scenario, solution) {
                Ok(v) if v.ok => None,
                Ok(v) => Some(v.reason().unwrap_or_else(|| "решение не засчитано".into())),
                Err(e) => Some(e.to_string()),
            }
        }
        "virt" => {
            let spec: virtlab::Spec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(format!("сценарий повреждён: {e}")),
            };
            let submitted: Value = match serde_json::from_str(solution) {
                Ok(v) => v,
                Err(e) => return Some(format!("решение не разобрано: {e}")),
            };
            // строго: цель без записи действий (trace), которую нечем перепроверить, не засчитывается — клиент присылает записи
            let verdict = virtlab::verify_with(&spec, &submitted, virtlab::Strictness::Strict);
            (!verdict.solved).then(|| verdict.first_rejection().unwrap_or_else(|| "решение не засчитано".into()))
        }
        "net" => {
            let spec: netlab::NetSpec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(format!("сценарий повреждён: {e}")),
            };
            let verdict = netlab::verify_json(&spec, solution);
            (!verdict.ok).then(|| {
                verdict
                    .error
                    .clone()
                    .or_else(|| verdict.goals.iter().find(|g| !g.ok).map(|g| format!("цель не выполнена: {}", g.text)))
                    .unwrap_or_else(|| "решение не засчитано".into())
            })
        }
        "riscv" => {
            let spec: riscvlab::task::TaskSpec = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(format!("сценарий повреждён: {e}")),
            };
            let verdict = riscvlab::task::verify(&spec, solution);
            (!verdict.ok).then_some(verdict.message)
        }
        "web" => {
            let task: weblab::Task = match serde_json::from_value(spec) {
                Ok(v) => v,
                Err(e) => return Some(format!("задание повреждено: {e}")),
            };
            let submitted: weblab::Solution = match serde_json::from_str(solution) {
                Ok(v) => v,
                Err(e) => return Some(format!("решение не разобрано: {e}")),
            };
            let report = weblab::verify(&task, &submitted);
            (!report.ok()).then(|| report.reason().unwrap_or_else(|| "решение не засчитано".into()))
        }
        other => {
            tracing::warn!("вид лаборатории «{other}»: проверки на сервере пока нет, решение принято");
            None
        }
    }
}
