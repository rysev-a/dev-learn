//! The "cs-core" backend: axum + SurrealDB. Auth:
//! sign-in, registration and admin - shared lab crates (`auth`, `auth_api`, `admin_api`, `system_tasks`, `mail`).
//! Code checking is done by an external worker (`worker/worker.py`): the backend keeps the queue and hands out jobs via `/internal/worker/*`.

pub mod answers;
pub mod config;
pub mod board_tasks;
pub mod courses;
pub mod db;
pub mod error;
pub mod exercises;
pub mod jobs;
pub mod lang;
pub mod labs;
pub mod practice;
pub mod progress;
pub mod quizzes;
pub mod records;
pub mod schema_view;
pub mod seed;
pub mod slides;
pub mod wav;
pub mod worker_api;

use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
};

use axum::{
    http::StatusCode,
    middleware::from_fn_with_state,
    response::IntoResponse,
    routing::any,
    Json, Router,
};
use serde_json::{json, Value};
use surrealdb::engine::any::Any;
use tower_http::services::{ServeDir, ServeFile};

use crate::{config::Config, db::Db};

#[derive(Clone)]
pub struct AppState {
    pub db: Db,
    pub cfg: Arc<Config>,
    /// lock of the check queue: the backend runs as one instance (see `jobs.rs`)
    pub queue: Arc<tokio::sync::Mutex<()>>,
    pub last_reap: Arc<Mutex<f64>>,
    /// descriptions of the teaching SQL databases of tasks: set key -> schema and data
    pub datasets: Arc<Mutex<HashMap<String, Value>>>,
    /// engine of the "Computer Architecture" lab (chapters 6-15), loaded from the data files
    pub arch: Arc<archlab::ArchLab>,
}

impl AppState {
    pub fn new(db: Db, cfg: Config) -> Self {
        let arch = archlab::ArchLab::load_dir(&cfg.labs_dir().join("arch")).unwrap_or_else(|e| {
            tracing::error!("architecture lab not loaded: {e}");
            archlab::ArchLab::default()
        });
        Self { db, cfg: Arc::new(cfg), queue: Arc::new(tokio::sync::Mutex::new(())), last_reap: Arc::new(Mutex::new(0.0)), datasets: Arc::new(Mutex::new(HashMap::new())), arch: Arc::new(arch) }
    }
}

type Auth = auth::Auth<Any>;
type Tasks = system_tasks::SystemTasks<Any>;

async fn api_not_found() -> impl IntoResponse {
    (StatusCode::NOT_FOUND, Json(json!({ "detail": "Not Found" })))
}

/// Router of the whole backend: shared routes protected by a session (`Bearer`) and public ones, `/api/auth`, `/api/admin`, workers, static files.
pub fn router(state: AppState, auth: Auth, tasks: Tasks) -> Router {
    let require = from_fn_with_state(auth::guard::Require::authenticated(auth.clone()), auth::guard::require::<Any>);
    let private = Router::new()
        .merge(progress::routes())
        .merge(quizzes::private())
        .merge(answers::private())
        .merge(exercises::private())
        .merge(records::private())
        .layer(require);
    let public = Router::new().merge(courses::routes()).merge(records::public()).merge(slides::routes()).merge(labs::routes()).merge(quizzes::public()).merge(answers::public()).merge(exercises::public()).merge(worker_api::routes(state.clone()));

    let auth_api = auth_api::routes(auth.clone(), tasks.clone(), auth_api::Config::from_env());
    let admin = admin_api::routes(auth.clone()).merge(admin_api::task_routes(auth, tasks));

    let mut app = Router::new()
        .merge(private)
        .merge(public)
        .with_state(state.clone())
        .nest("/api/auth", auth_api)
        .nest("/api/admin", admin)
        .route("/api/{*rest}", any(api_not_found));
    if let Some(dir) = &state.cfg.static_dir {
        // built frontend: files as is, other paths - index.html (client-side routing)
        app = app.fallback_service(ServeDir::new(dir).fallback(ServeFile::new(dir.join("index.html"))));
    }
    app
}

/// Schema, content seed, auth, background tasks; returns the ready router.
pub async fn build(db: Db, cfg: Config) -> anyhow::Result<(Router, AppState)> {
    locales::install(); // Russian lab engine messages (checking solutions in the request language)
    db::init_schema(&db).await?;
    if let Err(e) = seed::run(&db, &cfg).await {
        tracing::error!("content seed failed: {e:#}");
        if std::env::var("DB_STRICT").is_ok() {
            return Err(e);
        }
    }

    let auth = Auth::new(db.clone());
    auth.init().await?;
    auth.seed_defaults().await?;
    let email = std::env::var("ADMIN_EMAIL").unwrap_or_default();
    let password = std::env::var("ADMIN_PASSWORD").unwrap_or_default();
    if email.trim().is_empty() || password.is_empty() {
        tracing::warn!("ADMIN_EMAIL / ADMIN_PASSWORD not set: no initial administrator");
    } else {
        auth.ensure_admin(&email, &password).await?;
        tracing::info!("administrator {email} ready");
    }
    // demo user with a short well-known password - for local checks only, do not set on the server
    let (demo_email, demo_password) = (std::env::var("DEMO_USER_EMAIL").unwrap_or_default(), std::env::var("DEMO_USER_PASSWORD").unwrap_or_default());
    if !demo_email.trim().is_empty() && !demo_password.is_empty() {
        auth.ensure_demo_user(&demo_email, &demo_password).await?;
        tracing::warn!("demo user {demo_email} ready (DEMO_USER_*): do not set on a production server");
    }

    let (demo_admin, demo_admin_password) = (std::env::var("DEMO_ADMIN_EMAIL").unwrap_or_default(), std::env::var("DEMO_ADMIN_PASSWORD").unwrap_or_default());
    if !demo_admin.trim().is_empty() && !demo_admin_password.is_empty() {
        auth.ensure_demo_admin(&demo_admin, &demo_admin_password).await?;
        tracing::warn!("demo administrator {demo_admin} ready (DEMO_ADMIN_*): do not set on a production server");
    }

    let tasks = Tasks::new(db.clone());
    tasks.init().await?;
    mail::register(&tasks, mail::MailConfig::from_env());
    register_cleanup(&tasks, &auth);
    if tasks.count().await? == 0 {
        tasks
            .create(system_tasks::NewTask {
                name: "Expired sessions cleanup".into(),
                description: "Hourly: expired sessions, old login attempts, used tokens, old emails".into(),
                handler: "sessions.cleanup".into(),
                payload: json!({}),
                schedule: Some(system_tasks::Schedule::Interval(3600)),
            })
            .await?;
    }
    tasks.start();

    let state = AppState::new(db, cfg);
    Ok((router(state.clone(), auth, tasks), state))
}

/// Hourly cleanup: expired sessions, old sign-in attempts, used tokens and emails.
fn register_cleanup(tasks: &Tasks, auth: &Auth) {
    let (auth, tasks_for_mail) = (auth.clone(), tasks.clone());
    tasks.register("sessions.cleanup", "Cleanup: expired sessions, old login attempts, used tokens, old emails", move |ctx| {
        let (auth, tasks) = (auth.clone(), tasks_for_mail.clone());
        async move {
            let report = auth.purge_stale().await?;
            let mails = tasks.purge_finished(mail::HANDLER, chrono::Duration::days(7)).await?;
            ctx.report(
                1.0,
                json!([{ "name": format!("removed: sessions {}, login attempts {}, tokens {}, emails {}", report.sessions, report.rate_events, report.tokens, mails), "done": true }]),
            )
            .await;
            Ok(())
        }
    });
}
