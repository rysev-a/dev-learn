//! Подключение к SurrealDB и схема таблиц курса, прогресса и очереди проверок.
//!
//! Dev: один контейнер SurrealDB (`ws://127.0.0.1:8123`, root/devpass), ns `stack`, db `say`. Если адрес недоступен, а
//! `DB_STRICT` не задан, приложение работает на базе в памяти (данные пересеваются при каждом запуске).

use std::sync::Arc;

use surrealdb::{
    engine::any::{self, Any},
    opt::auth::Root,
    Surreal,
};

pub type Db = Arc<Surreal<Any>>;

pub const NS: &str = "stack";
pub const DB: &str = "say";

async fn connect_to(url: &str) -> anyhow::Result<Surreal<Any>> {
    let surreal = any::connect(url).await?;
    // у базы в памяти входа нет; у сервера — root-пользователь из окружения (dev: root/devpass)
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

/// Подключение к `url` или (без `DB_STRICT`) к базе в памяти. Возвращает общий дескриптор и признак «в памяти».
/// `Surreal` не клонируем: каждый клон открывает новую сессию, которую сервер v3 отвергает — все делят один `Arc`.
pub async fn connect(url: &str) -> anyhow::Result<(Db, bool)> {
    match connect_to(url).await {
        Ok(db) => {
            tracing::info!("surrealdb подключена: {url}");
            Ok((Arc::new(db), false))
        }
        Err(e) => {
            if std::env::var("DB_STRICT").is_ok() {
                anyhow::bail!("surrealdb {url} обязательна (задан DB_STRICT), память не используем: {e}");
            }
            tracing::warn!("surrealdb {url} недоступна ({e}); работаем на базе в памяти");
            let db = connect_to("memory").await?;
            Ok((Arc::new(db), true))
        }
    }
}

/// База в памяти для тестов.
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

/// Идемпотентная схема: таблицы и индексы (`IF NOT EXISTS`).
pub async fn init_schema(db: &Db) -> anyhow::Result<()> {
    db.query(SCHEMA).await?.check()?;
    Ok(())
}
