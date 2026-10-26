//! Очередь проверок кода: API кладёт решение в таблицу `exec_jobs`, воркер забирает его, запускает
//! в песочнице и возвращает результат. Сам бэкенд контейнеры не запускает — выполняет внешний воркер (`backend/worker.py`).
//!
//! Жизнь задания: queued → running (аренда `lease_until`, продлевается сердцебиением воркера; не продлилась — задание
//! возвращается в очередь, после `MAX_ATTEMPTS` попыток завершается ошибкой) → done (результат и попытка записаны).
//! Изменения очереди идут под одним замком процесса (`AppState::queue`): бэкенд работает одним экземпляром.

use serde_json::{json, Value};
use sha2::{Digest, Sha256};

use crate::{
    db::Db,
    error::{f, i, now_secs, s, ApiResult},
    practice, AppState,
};

pub const LIGHT: &str = "light";
pub const HEAVY: &str = "heavy";
const LANES: [&str; 2] = [LIGHT, HEAVY];
const QUEUE_LIMIT: i64 = 300;
pub const LEASE_SEC: f64 = 45.0;
const MAX_ATTEMPTS: i64 = 2;
const CACHE_TTL: f64 = 7.0 * 24.0 * 3600.0;
const KEEP_DONE_SEC: f64 = 24.0 * 3600.0;
const WORKER_ALIVE_SEC: f64 = 30.0;
const MAX_RESULT_BYTES: usize = 600_000;
const MAX_TEXT: usize = 20_000;

/// Ошибка постановки в очередь: HTTP-статус и текст для пользователя.
pub struct JobError(pub u16, pub String);

fn lane_of(task: &Value) -> &'static str {
    if matches!(task.get("mode").and_then(Value::as_str), Some("rust" | "c")) {
        HEAVY
    } else {
        LIGHT
    }
}

pub fn cache_key(task: &Value, code: &str) -> String {
    let spec = serde_json::to_string(task).unwrap_or_default();
    let h = Sha256::digest(spec.as_bytes());
    let mut all = h.to_vec();
    all.push(0);
    all.extend_from_slice(code.as_bytes());
    Sha256::digest(&all).iter().map(|b| format!("{b:02x}")).collect()
}

async fn count_where(db: &Db, cond: &str) -> ApiResult<i64> {
    let mut res = db.query(format!("SELECT count() AS n FROM exec_jobs WHERE {cond} GROUP ALL")).await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(rows.first().map_or(0, |r| i(r, "n")))
}

// --- постановка ----------------------------------------------------------------------------

/// Ставит решение в очередь (или сразу отдаёт кэшированный результат); возвращает id задания.
pub async fn submit(state: &AppState, user: &str, book: i64, chapter: i64, task: &Value, code: &str, runner_ok: bool) -> Result<String, JobError> {
    let _guard = state.queue.lock().await;
    let db = &state.db;
    let db_err = |e: surrealdb::Error| {
        tracing::error!("surrealdb: {e}");
        JobError(500, "Ошибка базы данных".into())
    };
    let t = now_secs();
    reap_throttled(state, t).await.map_err(|_| JobError(500, "Ошибка базы данных".into()))?;
    let mut res = db.query("SELECT VALUE jid FROM exec_jobs WHERE user = $u AND status IN ['queued', 'running'] LIMIT 1").bind(("u", user.to_string())).await.map_err(db_err)?;
    let busy: Vec<String> = res.take(0).map_err(db_err)?;
    if !busy.is_empty() {
        return Err(JobError(429, "Предыдущая проверка ещё идёт".into()));
    }
    let key = cache_key(task, code);
    let job_id = uuid::Uuid::new_v4().simple().to_string();
    let lane = lane_of(task);
    let mut res = db.query("SELECT VALUE result FROM exec_cache WHERE key = $k AND created_at > $t").bind(("k", key.clone())).bind(("t", t - CACHE_TTL)).await.map_err(db_err)?;
    let cached: Vec<String> = res.take(0).map_err(db_err)?;
    let cached: Option<Value> = cached.first().and_then(|r| serde_json::from_str(r).ok());
    if cached.is_none() {
        if !runner_ok {
            return Err(JobError(503, "Проверка кода временно недоступна: сервер проверки не отвечает. Попробуйте чуть позже.".into()));
        }
        if count_where(db, "status = 'queued'").await.map_err(|_| JobError(500, "Ошибка базы данных".into()))? >= QUEUE_LIMIT {
            return Err(JobError(503, "Очередь проверок переполнена — попробуйте через минуту.".into()));
        }
    }
    db.query("CREATE exec_jobs CONTENT { jid: $j, user: $u, book: $b, chapter: $c, tid: $t, code: $code, key: $k, lane: $l, status: 'queued', attempts: 0, created_at: $at }")
        .bind(("j", job_id.clone()))
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task.get("id").and_then(Value::as_str).unwrap_or("").to_string()))
        .bind(("code", code.to_string()))
        .bind(("k", key))
        .bind(("l", lane.to_string()))
        .bind(("at", t))
        .await
        .map_err(db_err)?
        .check()
        .map_err(db_err)?;
    if let Some(cached) = cached {
        finish(db, &job_id, cached, false).await.map_err(|_| JobError(500, "Ошибка базы данных".into()))?;
    }
    Ok(job_id)
}

/// Результат от воркера: только известные поля и разумные размеры.
fn normalize(result: &Value) -> Value {
    let cut = |k: &str| result.get(k).and_then(Value::as_str).unwrap_or("").chars().take(MAX_TEXT).collect::<String>();
    let items: Vec<Value> = result.get("results").and_then(Value::as_array).map(|a| a.iter().filter(|r| r.is_object()).take(100).cloned().collect()).unwrap_or_default();
    let out = json!({ "status": result.get("status").and_then(Value::as_str).unwrap_or("error"), "results": items, "stdout": cut("stdout"), "stderr": cut("stderr") });
    if out.to_string().len() > MAX_RESULT_BYTES {
        return json!({ "status": "error", "results": [], "stdout": "", "stderr": "Результат проверки слишком большой." });
    }
    out
}

/// Записывает попытку и итог; успешные проверки кладёт в кэш.
pub async fn finish(db: &Db, job_id: &str, result: Value, cache: bool) -> ApiResult<Value> {
    let mut res = db.query("SELECT user, book, chapter, tid, code, key FROM exec_jobs WHERE jid = $j").bind(("j", job_id.to_string())).await?;
    let job = res.take::<Vec<Value>>(0)?.into_iter().next();
    let Some(job) = job else { return Ok(Value::Null) };
    let result = normalize(&result);
    let items = result["results"].as_array().cloned().unwrap_or_default();
    let (total, passed) = (items.len() as i64, items.iter().filter(|r| r.get("ok").and_then(Value::as_bool) == Some(true)).count() as i64);
    let solved = result["status"] == "ok" && total > 0 && passed == total;
    let (user, tid, code) = (s(&job, "user"), s(&job, "tid"), s(&job, "code"));
    let attempt = practice::record_attempt(db, practice::Attempt { user: &user, book: i(&job, "book"), chapter: i(&job, "chapter"), task: &tid, code: &code, passed, total, solved }).await?;
    let mut payload = result.clone();
    let obj = payload.as_object_mut().expect("результат — объект");
    obj.insert("passed".into(), json!(passed));
    obj.insert("total".into(), json!(total));
    obj.insert("solved".into(), json!(solved));
    obj.insert("attempt".into(), attempt);
    let t = now_secs();
    db.query("UPDATE exec_jobs SET status = 'done', result = $r, finished_at = $t, lease_until = NONE WHERE jid = $j")
        .bind(("r", payload.to_string()))
        .bind(("t", t))
        .bind(("j", job_id.to_string()))
        .await?
        .check()?;
    if cache && result["status"] == "ok" {
        db.query("UPSERT type::record('exec_cache', $k) SET key = $k, result = $r, created_at = $t").bind(("k", s(&job, "key"))).bind(("r", result.to_string())).bind(("t", t)).await?.check()?;
    }
    Ok(payload)
}

/// Состояние задания для клиента: queued (с местом в очереди), running или done (с результатом).
pub async fn get_for_user(db: &Db, job_id: &str, user: &str) -> ApiResult<Option<Value>> {
    let mut res = db.query("SELECT status, lane, created_at, result FROM exec_jobs WHERE jid = $j AND user = $u").bind(("j", job_id.to_string())).bind(("u", user.to_string())).await?;
    let Some(job) = res.take::<Vec<Value>>(0)?.into_iter().next() else { return Ok(None) };
    match s(&job, "status").as_str() {
        "done" => {
            let mut out = serde_json::from_str::<Value>(&s(&job, "result")).unwrap_or_else(|_| json!({}));
            out.as_object_mut().map(|o| o.insert("state".into(), json!("done")));
            Ok(Some(out))
        }
        "running" => Ok(Some(json!({ "state": "running" }))),
        _ => {
            let mut res = db.query("SELECT count() AS n FROM exec_jobs WHERE status = 'queued' AND lane = $l AND created_at < $c GROUP ALL").bind(("l", s(&job, "lane"))).bind(("c", f(&job, "created_at"))).await?;
            let ahead = res.take::<Vec<Value>>(0)?.first().map_or(0, |r| i(r, "n"));
            Ok(Some(json!({ "state": "queued", "position": ahead + 1 })))
        }
    }
}

// --- воркеры -------------------------------------------------------------------------------

/// Отдаёт воркеру самое старое задание из его полос или `None`; аренда выдаётся под замком очереди.
pub async fn claim(state: &AppState, worker: &str, lanes: &[String]) -> ApiResult<Option<Value>> {
    let lanes: Vec<String> = lanes.iter().filter(|l| LANES.contains(&l.as_str())).cloned().collect();
    if lanes.is_empty() {
        return Ok(None);
    }
    let _guard = state.queue.lock().await;
    let db = &state.db;
    let t = now_secs();
    reap_throttled(state, t).await?;
    let mut res = db.query("SELECT jid, book, chapter, tid, code, lane, created_at FROM exec_jobs WHERE status = 'queued' AND lane IN $lanes ORDER BY created_at LIMIT 1").bind(("lanes", lanes)).await?;
    let Some(job) = res.take::<Vec<Value>>(0)?.into_iter().next() else { return Ok(None) };
    let jid = s(&job, "jid");
    db.query("UPDATE exec_jobs SET status = 'running', worker = $w, started_at = $t, lease_until = $l, attempts += 1 WHERE jid = $j")
        .bind(("w", worker.to_string()))
        .bind(("t", t))
        .bind(("l", t + LEASE_SEC))
        .bind(("j", jid.clone()))
        .await?
        .check()?;
    let Some(task) = crate::exercises::find_task(db, i(&job, "book"), i(&job, "chapter"), &s(&job, "tid")).await? else {
        finish(db, &jid, json!({ "status": "error", "stderr": "Задача удалена." }), false).await?;
        return Ok(None);
    };
    Ok(Some(json!({ "id": jid, "lane": s(&job, "lane"), "task": task, "code": s(&job, "code"), "lease": LEASE_SEC as i64 })))
}

/// Принимает результат от воркера, которому задание выдано; чужой или просроченный ответ отклоняется.
pub async fn complete(state: &AppState, job_id: &str, worker: &str, result: Value) -> ApiResult<bool> {
    let _guard = state.queue.lock().await;
    let mut res = state.db.query("SELECT status, worker FROM exec_jobs WHERE jid = $j").bind(("j", job_id.to_string())).await?;
    let Some(row) = res.take::<Vec<Value>>(0)?.into_iter().next() else { return Ok(false) };
    if s(&row, "status") != "running" || s(&row, "worker") != worker {
        return Ok(false);
    }
    finish(&state.db, job_id, result, true).await?;
    Ok(true)
}

/// Сердцебиение воркера: отмечает, что он жив, и продлевает аренду выполняющихся заданий.
pub async fn ping(state: &AppState, name: &str, lanes: &[String], slots: i64, jobs: &[String]) -> ApiResult<()> {
    // запись одной и той же строки воркера из нескольких долгих опросов сразу даёт конфликт транзакций SurrealDB — идём под замком очереди
    let _guard = state.queue.lock().await;
    let t = now_secs();
    state
        .db
        .query("UPSERT type::record('exec_workers', $n) SET name = $n, lanes = $l, slots = $s, seen = $t")
        .bind(("n", name.to_string()))
        .bind(("l", lanes.join(",")))
        .bind(("s", slots))
        .bind(("t", t))
        .await?
        .check()?;
    for job in jobs.iter().take(100) {
        state
            .db
            .query("UPDATE exec_jobs SET lease_until = $l WHERE jid = $j AND worker = $w AND status = 'running'")
            .bind(("l", t + LEASE_SEC))
            .bind(("j", job.clone()))
            .bind(("w", name.to_string()))
            .await?
            .check()?;
    }
    Ok(())
}

/// Возвращает в очередь задания с просроченной арендой (воркер пропал) и чистит старые записи.
pub async fn reap(db: &Db, t: f64) -> ApiResult<()> {
    let mut res = db.query("SELECT jid, attempts FROM exec_jobs WHERE status = 'running' AND lease_until < $t").bind(("t", t)).await?;
    for job in res.take::<Vec<Value>>(0)? {
        let jid = s(&job, "jid");
        if i(&job, "attempts") >= MAX_ATTEMPTS {
            finish(db, &jid, json!({ "status": "error", "stderr": "Сервер проверки не ответил. Попробуйте ещё раз." }), false).await?;
        } else {
            db.query("UPDATE exec_jobs SET status = 'queued', worker = NONE, lease_until = NONE WHERE jid = $j").bind(("j", jid)).await?.check()?;
        }
    }
    db.query("DELETE exec_jobs WHERE status = 'done' AND finished_at < $a")
        .query("DELETE exec_cache WHERE created_at < $b")
        .query("DELETE exec_workers WHERE seen < $c")
        .bind(("a", t - KEEP_DONE_SEC))
        .bind(("b", t - CACHE_TTL))
        .bind(("c", t - 3600.0))
        .await?
        .check()?;
    Ok(())
}

/// То же, но не чаще раза в секунду (воркеры опрашивают очередь каждые 0,4 с).
async fn reap_throttled(state: &AppState, t: f64) -> ApiResult<()> {
    {
        let mut last = state.last_reap.lock().expect("замок last_reap");
        if t - *last < 1.0 {
            return Ok(());
        }
        *last = t;
    }
    reap(&state.db, t).await
}

pub async fn workers_alive(db: &Db) -> ApiResult<i64> {
    let mut res = db.query("SELECT count() AS n FROM exec_workers WHERE seen > $t GROUP ALL").bind(("t", now_secs() - WORKER_ALIVE_SEC)).await?;
    Ok(res.take::<Vec<Value>>(0)?.first().map_or(0, |r| i(r, "n")))
}

pub async fn status(db: &Db) -> ApiResult<Value> {
    Ok(json!({
        "queued": count_where(db, "status = 'queued'").await?,
        "running": count_where(db, "status = 'running'").await?,
        "workers": workers_alive(db).await?,
    }))
}
