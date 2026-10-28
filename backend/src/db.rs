//! SurrealDB connection and the schema of the course, progress and check-queue tables.
//!
//! Dev: one SurrealDB container (`ws://127.0.0.1:8123`, root/devpass), ns `stack`, db `cs-core`. If the address is unreachable and
//! `DB_STRICT` is not set, the application runs on an in-memory database (data is reseeded on every start).

use std::sync::Arc;

use surrealdb::{
    engine::any::{self, Any},
    opt::auth::Root,
    Surreal,
};

pub type Db = Arc<Surreal<Any>>;

pub const NS: &str = "stack";
pub const DB: &str = "cs-core";

async fn connect_to(url: &str) -> anyhow::Result<Surreal<Any>> {
    let surreal = any::connect(url).await?;
    // the in-memory database has no sign-in; for the server - the root user from the environment (dev: root/devpass)
    if url != "memory" {
        if let (Ok(user), Ok(pass)) = (std::env::var("SURREAL_USER"), std::env::var("SURREAL_PASS")) {
            surreal.signin(Root { username: user, password: pass }).await?;
        }
    }
    let ns = std::env::var("SURREAL_NS").unwrap_or_else(|_| NS.to_string());
    let db = std::env::var("SURREAL_DB").unwrap_or_else(|_| DB.to_string());
    surreal.use_ns(ns).use_db(db).await?;
    Ok(surreal)
}

/// Connect to `url` or (without `DB_STRICT`) to an in-memory database. Returns the shared handle and an "in memory" flag.
/// `Surreal` is not cloned: every clone opens a new session, which the v3 server rejects - everyone shares one `Arc`.
pub async fn connect(url: &str) -> anyhow::Result<(Db, bool)> {
    match connect_to(url).await {
        Ok(db) => {
            tracing::info!("surrealdb connected: {url}");
            Ok((Arc::new(db), false))
        }
        Err(e) => {
            if std::env::var("DB_STRICT").is_ok() {
                anyhow::bail!("surrealdb {url} is required (DB_STRICT is set), not falling back to memory: {e}");
            }
            tracing::warn!("surrealdb {url} is unavailable ({e}); running on an in-memory database");
            let db = connect_to("memory").await?;
            Ok((Arc::new(db), true))
        }
    }
}

/// In-memory database for tests.
pub async fn memory() -> anyhow::Result<Db> {
    Ok(Arc::new(connect_to("memory").await?))
}

const SCHEMA: &str = "
DEFINE TABLE IF NOT EXISTS meta SCHEMALESS;
DEFINE TABLE IF NOT EXISTS counters SCHEMALESS;

DEFINE TABLE IF NOT EXISTS books SCHEMALESS;
DEFINE INDEX IF NOT EXISTS books_bid ON books FIELDS bid UNIQUE;
DEFINE TABLE IF NOT EXISTS sections SCHEMALESS;
DEFINE INDEX IF NOT EXISTS sections_book ON sections FIELDS bid;
DEFINE TABLE IF NOT EXISTS chapters SCHEMALESS;
DEFINE INDEX IF NOT EXISTS chapters_cid ON chapters FIELDS cid UNIQUE;
DEFINE INDEX IF NOT EXISTS chapters_book ON chapters FIELDS bid;
DEFINE TABLE IF NOT EXISTS lessons SCHEMALESS;
DEFINE INDEX IF NOT EXISTS lessons_chapter ON lessons FIELDS cid;
DEFINE INDEX IF NOT EXISTS lessons_lid ON lessons FIELDS lid UNIQUE;

DEFINE TABLE IF NOT EXISTS slide_chapters SCHEMALESS;
DEFINE INDEX IF NOT EXISTS slide_chapters_key ON slide_chapters FIELDS book, chapter UNIQUE;
DEFINE TABLE IF NOT EXISTS slides SCHEMALESS;
DEFINE INDEX IF NOT EXISTS slides_key ON slides FIELDS book, chapter, idx UNIQUE;

DEFINE TABLE IF NOT EXISTS lab_tasks SCHEMALESS;
DEFINE INDEX IF NOT EXISTS lab_tasks_key ON lab_tasks FIELDS book, chapter, tid UNIQUE;

DEFINE TABLE IF NOT EXISTS tasks SCHEMALESS;
DEFINE INDEX IF NOT EXISTS tasks_chapter ON tasks FIELDS book, chapter;
DEFINE INDEX IF NOT EXISTS tasks_key ON tasks FIELDS book, chapter, tid UNIQUE;
DEFINE TABLE IF NOT EXISTS quizzes SCHEMALESS;
DEFINE INDEX IF NOT EXISTS quizzes_key ON quizzes FIELDS book, chapter UNIQUE;
DEFINE TABLE IF NOT EXISTS quiz_questions SCHEMALESS;
DEFINE INDEX IF NOT EXISTS quiz_questions_chapter ON quiz_questions FIELDS book, chapter;
DEFINE TABLE IF NOT EXISTS answer_sets SCHEMALESS;
DEFINE INDEX IF NOT EXISTS answer_sets_key ON answer_sets FIELDS book, chapter UNIQUE;
DEFINE TABLE IF NOT EXISTS answer_tasks SCHEMALESS;
DEFINE INDEX IF NOT EXISTS answer_tasks_chapter ON answer_tasks FIELDS book, chapter;

-- content translations: the same tables with the _i18n suffix and a lang field; keys (cid, sid, chapter numbers) are shared with the Russian rows
DEFINE TABLE IF NOT EXISTS books_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS books_i18n_key ON books_i18n FIELDS bid, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS sections_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS sections_i18n_book ON sections_i18n FIELDS bid, lang;
DEFINE TABLE IF NOT EXISTS chapters_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS chapters_i18n_key ON chapters_i18n FIELDS cid, lang UNIQUE;
DEFINE INDEX IF NOT EXISTS chapters_i18n_book ON chapters_i18n FIELDS bid, lang;
DEFINE TABLE IF NOT EXISTS lessons_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS lessons_i18n_chapter ON lessons_i18n FIELDS cid, lang;
DEFINE TABLE IF NOT EXISTS slide_chapters_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS slide_chapters_i18n_key ON slide_chapters_i18n FIELDS book, chapter, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS slides_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS slides_i18n_key ON slides_i18n FIELDS book, chapter, idx, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS quizzes_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS quizzes_i18n_key ON quizzes_i18n FIELDS book, chapter, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS quiz_questions_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS quiz_questions_i18n_chapter ON quiz_questions_i18n FIELDS book, chapter, lang;
DEFINE TABLE IF NOT EXISTS answer_sets_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS answer_sets_i18n_key ON answer_sets_i18n FIELDS book, chapter, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS answer_tasks_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS answer_tasks_i18n_chapter ON answer_tasks_i18n FIELDS book, chapter, lang;
DEFINE TABLE IF NOT EXISTS tasks_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS tasks_i18n_key ON tasks_i18n FIELDS book, chapter, tid, lang UNIQUE;
DEFINE TABLE IF NOT EXISTS lab_tasks_i18n SCHEMALESS;
DEFINE INDEX IF NOT EXISTS lab_tasks_i18n_key ON lab_tasks_i18n FIELDS book, chapter, tid, lang UNIQUE;

DEFINE TABLE IF NOT EXISTS slide_views SCHEMALESS;
DEFINE INDEX IF NOT EXISTS slide_views_user ON slide_views FIELDS user;
DEFINE TABLE IF NOT EXISTS quiz_picks SCHEMALESS;
DEFINE INDEX IF NOT EXISTS quiz_picks_user ON quiz_picks FIELDS user;
DEFINE TABLE IF NOT EXISTS answer_solved SCHEMALESS;
DEFINE INDEX IF NOT EXISTS answer_solved_user ON answer_solved FIELDS user;
DEFINE TABLE IF NOT EXISTS code_status SCHEMALESS;
DEFINE INDEX IF NOT EXISTS code_status_user ON code_status FIELDS user;
DEFINE TABLE IF NOT EXISTS code_drafts SCHEMALESS;
DEFINE INDEX IF NOT EXISTS code_drafts_chapter ON code_drafts FIELDS user, book, chapter;
DEFINE TABLE IF NOT EXISTS code_attempts SCHEMALESS;
DEFINE INDEX IF NOT EXISTS code_attempts_task ON code_attempts FIELDS user, book, chapter, tid;

DEFINE TABLE IF NOT EXISTS exec_jobs SCHEMALESS;
DEFINE INDEX IF NOT EXISTS exec_jobs_jid ON exec_jobs FIELDS jid UNIQUE;
DEFINE INDEX IF NOT EXISTS exec_jobs_queue ON exec_jobs FIELDS status, lane, created_at;
DEFINE INDEX IF NOT EXISTS exec_jobs_user ON exec_jobs FIELDS user, status;
DEFINE TABLE IF NOT EXISTS exec_cache SCHEMALESS;
DEFINE INDEX IF NOT EXISTS exec_cache_key ON exec_cache FIELDS key UNIQUE;
DEFINE TABLE IF NOT EXISTS exec_workers SCHEMALESS;
DEFINE INDEX IF NOT EXISTS exec_workers_name ON exec_workers FIELDS name UNIQUE;
";

/// Idempotent schema: tables and indexes (`IF NOT EXISTS`).
pub async fn init_schema(db: &Db) -> anyhow::Result<()> {
    db.query(SCHEMA).await?.check()?;
    Ok(())
}
