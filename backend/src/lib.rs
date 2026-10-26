//! Бэкенд «say»: axum + SurrealDB. Auth:
//! вход, регистрация и админка — общие crates lab (`auth`, `auth_api`, `admin_api`, `system_tasks`, `mail`).
//! Проверка кода выполняется внешним воркером (`worker/worker.py`): бэкенд ведёт очередь и отдаёт задания по `/internal/worker/*`.

pub mod answers;
pub mod config;
pub mod courses;
pub mod db;
pub mod error;
pub mod exercises;
pub mod jobs;
pub mod labs;
pub mod practice;
pub mod progress;
pub mod quizzes;
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
    /// замок очереди проверок: бэкенд работает одним экземпляром (см. `jobs.rs`)
    pub queue: Arc<tokio::sync::Mutex<()>>,
    pub last_reap: Arc<Mutex<f64>>,
    /// описания учебных баз SQL-задач: ключ набора → схема и данные
    pub datasets: Arc<Mutex<HashMap<String, Value>>>,
    /// движок лаборатории «Архитектура компьютера» (главы 6–15), загруженный из файлов данных
    pub arch: Arc<archlab::ArchLab>,
}

impl AppState {
    pub fn new(db: Db, cfg: Config) -> Self {
        let arch = archlab::ArchLab::load_dir(&cfg.labs_dir().join("arch")).unwrap_or_else(|e| {
            tracing::error!("лаборатория архитектуры не загружена: {e}");
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

/// Роутер всего бэкенда: общие маршруты, защищённые сессией (`Bearer`) и публичные, `/api/auth`, `/api/admin`, воркеры, статика.
pub fn router(state: AppState, auth: Auth, tasks: Tasks) -> Router {
    let require = from_fn_with_state(auth::guard::Require::authenticated(auth.clone()), auth::guard::require::<Any>);
    let private = Router::new()
        .merge(progress::routes())
        .merge(quizzes::private())
        .merge(answers::private())
        .merge(exercises::private())
        .layer(require);
    let public = Router::new().merge(courses::routes()).merge(slides::routes()).merge(labs::routes()).merge(quizzes::public()).merge(answers::public()).merge(exercises::public()).merge(worker_api::routes(state.clone()));

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
        // собранный фронтенд: файлы как есть, остальные пути — index.html (клиентская маршрутизация)
        app = app.fallback_service(ServeDir::new(dir).fallback(ServeFile::new(dir.join("index.html"))));
    }
    app
}

/// Схема, сид содержимого, auth, фоновые задачи; возвращает готовый роутер.
pub async fn build(db: Db, cfg: Config) -> anyhow::Result<(Router, AppState)> {
    db::init_schema(&db).await?;
    if let Err(e) = seed::run(&db, &cfg).await {
        tracing::error!("сид содержимого не удался: {e:#}");
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
        tracing::warn!("ADMIN_EMAIL / ADMIN_PASSWORD не заданы: начального администратора нет");
    } else {
        auth.ensure_admin(&email, &password).await?;
        tracing::info!("администратор {email} готов");
    }
    // демо-пользователь с коротким известным паролем — только для локальной проверки, на сервере не задавать
    let (demo_email, demo_password) = (std::env::var("DEMO_USER_EMAIL").unwrap_or_default(), std::env::var("DEMO_USER_PASSWORD").unwrap_or_default());
    if !demo_email.trim().is_empty() && !demo_password.is_empty() {
        auth.ensure_demo_user(&demo_email, &demo_password).await?;
        tracing::warn!("демо-пользователь {demo_email} готов (DEMO_USER_*): на рабочем сервере не задавать");
    }

    let (demo_admin, demo_admin_password) = (std::env::var("DEMO_ADMIN_EMAIL").unwrap_or_default(), std::env::var("DEMO_ADMIN_PASSWORD").unwrap_or_default());
    if !demo_admin.trim().is_empty() && !demo_admin_password.is_empty() {
        auth.ensure_demo_admin(&demo_admin, &demo_admin_password).await?;
        tracing::warn!("демо-администратор {demo_admin} готов (DEMO_ADMIN_*): на рабочем сервере не задавать");
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

/// Ежечасная чистка: просроченные сессии, старые попытки входа, использованные токены и письма.
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
