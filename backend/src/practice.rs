//! Упражнения с кодом в кабинете: статусы, черновики и история попыток (как `accounts/practice.py`).

use serde_json::{json, Value};

use crate::{
    db::Db,
    error::{i, iso_now, s, ApiResult},
};

pub const HISTORY_LIMIT: i64 = 50;

fn key(user: &str, book: i64, chapter: i64, task: &str) -> String {
    format!("{user}:{book}:{chapter}:{task}")
}

/// Записывает попытку и обновляет статус. Решённое остаётся решённым навсегда: неудачная попытка статус «ok» не снимает.
/// Что записывается в историю: чей код, по какой задаче, сколько тестов пройдено.
pub struct Attempt<'a> {
    pub user: &'a str,
    pub book: i64,
    pub chapter: i64,
    pub task: &'a str,
    pub code: &'a str,
    pub passed: i64,
    pub total: i64,
    pub solved: bool,
}

pub async fn record_attempt(db: &Db, a: Attempt<'_>) -> ApiResult<Value> {
    let Attempt { user, book, chapter, task, code, passed, total, solved } = a;
    let status = if solved { "ok" } else { "bad" };
    let created = iso_now();
    let mut res = db.query("UPSERT counters:attempts SET n += 1 RETURN VALUE n").await?;
    let n: Vec<i64> = res.take(0)?;
    let n = n.first().copied().unwrap_or(1);
    db.query("CREATE code_attempts CONTENT { user: $u, book: $b, chapter: $c, tid: $t, n: $n, code: $code, status: $st, passed: $p, total: $tot, created_at: $at }")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task.to_string()))
        .bind(("n", n))
        .bind(("code", code.to_string()))
        .bind(("st", status.to_string()))
        .bind(("p", passed))
        .bind(("tot", total))
        .bind(("at", created.clone()))
        .await?
        .check()?;
    db.query(
        "UPSERT type::record('code_status', $k) SET user = $u, book = $b, chapter = $c, tid = $t, \
         status = IF status = 'ok' THEN 'ok' ELSE $st END, updated_at = $at",
    )
    .bind(("k", key(user, book, chapter, task)))
    .bind(("u", user.to_string()))
    .bind(("b", book))
    .bind(("c", chapter))
    .bind(("t", task.to_string()))
    .bind(("st", status.to_string()))
    .bind(("at", created.clone()))
    .await?
    .check()?;
    // хранится не больше HISTORY_LIMIT последних попыток по задаче
    let mut res = db
        .query("SELECT VALUE n FROM code_attempts WHERE user = $u AND book = $b AND chapter = $c AND tid = $t ORDER BY n DESC LIMIT 1 START $lim")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task.to_string()))
        .bind(("lim", HISTORY_LIMIT))
        .await?;
    let old: Vec<i64> = res.take(0)?;
    if let Some(threshold) = old.first() {
        db.query("DELETE code_attempts WHERE user = $u AND book = $b AND chapter = $c AND tid = $t AND n <= $n")
            .bind(("u", user.to_string()))
            .bind(("b", book))
            .bind(("c", chapter))
            .bind(("t", task.to_string()))
            .bind(("n", *threshold))
            .await?
            .check()?;
    }
    Ok(json!({ "id": n, "status": status, "created_at": created }))
}

pub async fn save_draft(db: &Db, user: &str, book: i64, chapter: i64, task: &str, code: &str) -> ApiResult<()> {
    db.query("UPSERT type::record('code_drafts', $k) SET user = $u, book = $b, chapter = $c, tid = $t, code = $code, updated_at = $at")
        .bind(("k", key(user, book, chapter, task)))
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task.to_string()))
        .bind(("code", code.to_string()))
        .bind(("at", iso_now()))
        .await?
        .check()?;
    Ok(())
}

/// Статусы и черновики пользователя по задачам главы.
pub async fn chapter_state(db: &Db, user: &str, book: i64, chapter: i64) -> ApiResult<Value> {
    let mut res = db
        .query("SELECT tid, status FROM code_status WHERE user = $u AND book = $b AND chapter = $c")
        .query("SELECT tid, code FROM code_drafts WHERE user = $u AND book = $b AND chapter = $c")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .await?;
    let st: Vec<Value> = res.take(0)?;
    let dr: Vec<Value> = res.take(1)?;
    let status: serde_json::Map<String, Value> = st.iter().map(|r| (s(r, "tid"), json!(s(r, "status")))).collect();
    let drafts: serde_json::Map<String, Value> = dr.iter().map(|r| (s(r, "tid"), json!(s(r, "code")))).collect();
    Ok(json!({ "status": status, "drafts": drafts }))
}

/// История попыток: от новых к старым, с кодом.
pub async fn attempts(db: &Db, user: &str, book: i64, chapter: i64, task: &str) -> ApiResult<Vec<Value>> {
    let mut res = db
        .query("SELECT n, code, status, passed, total, created_at FROM code_attempts WHERE user = $u AND book = $b AND chapter = $c AND tid = $t ORDER BY n DESC LIMIT $lim")
        .bind(("u", user.to_string()))
        .bind(("b", book))
        .bind(("c", chapter))
        .bind(("t", task.to_string()))
        .bind(("lim", HISTORY_LIMIT))
        .await?;
    let rows: Vec<Value> = res.take(0)?;
    Ok(rows
        .iter()
        .map(|r| json!({ "id": i(r, "n"), "code": s(r, "code"), "status": s(r, "status"), "passed": i(r, "passed"), "total": i(r, "total"), "created_at": s(r, "created_at") }))
        .collect())
}
