//! Точка входа: окружение, подключение к SurrealDB, сид, роутер, запуск сервера.

use say_backend::{build, config::Config, db};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenvy::dotenv().ok();
    let otel = observability::init("say-backend");
    let cfg = Config::from_env();

    let (database, in_memory) = db::connect(&cfg.surreal_url).await?;
    let bind = cfg.bind.clone();
    let url = cfg.surreal_url.clone();
    let (app, _state) = build(database, cfg).await?;
    let app = app.layer(axum::middleware::from_fn(observability::track_http_metrics)).layer(observability::OtelAxumLayer::default());

    let listener = tokio::net::TcpListener::bind(&bind).await?;
    tracing::info!("say-backend слушает http://{bind} (db: {})", if in_memory { "memory" } else { &url });
    axum::serve(listener, app).await?;
    otel.shutdown();
    Ok(())
}
