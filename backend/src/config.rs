//! Настройки из окружения. Пути по умолчанию — каталог `data` рядом с бэкендом:
//! учебники, SQL-файлы упражнений/квизов, слайды, данные лабораторий и аудио.

use std::path::PathBuf;

#[derive(Debug, Clone)]
pub struct Config {
    pub bind: String,
    pub surreal_url: String,
    pub data_dir: PathBuf,
    pub audio_dir: PathBuf,
    /// каталог собранного фронтенда (`frontend/dist`); пусто — API без статики
    pub static_dir: Option<PathBuf>,
    /// общий секрет воркеров (`SAY_WORKER_TOKEN`); пусто — внутренний API воркеров недоступен
    pub worker_token: String,
    /// `auto` — пересеять курс, если исходники изменились; `always`; `off`
    pub seed: String,
}

fn env_or(key: &str, default: &str) -> String {
    std::env::var(key).ok().filter(|v| !v.is_empty()).unwrap_or_else(|| default.to_string())
}

impl Config {
    pub fn from_env() -> Self {
        let data_dir = PathBuf::from(env_or("DATA_DIR", "data"));
        let audio_dir = std::env::var("AUDIO_DIR").map(PathBuf::from).unwrap_or_else(|_| data_dir.join("audio"));
        let static_dir = std::env::var("STATIC_DIR").ok().filter(|v| !v.is_empty()).map(PathBuf::from);
        Self {
            bind: env_or("BIND", "0.0.0.0:8001"),
            surreal_url: env_or("SURREALDB_URL", "ws://127.0.0.1:8123"),
            data_dir,
            audio_dir,
            static_dir,
            worker_token: std::env::var("SAY_WORKER_TOKEN").unwrap_or_default(),
            seed: env_or("SEED", "auto"),
        }
    }

    pub fn textbook_dir(&self) -> PathBuf {
        self.data_dir.join("textbook")
    }

    /// Слайды глав: файлы `<книга>-<глава>.json` (их создают генераторы `packages/gen`).
    pub fn slides_dir(&self) -> PathBuf {
        self.data_dir.join("slides")
    }

    /// Упражнения-лаборатории: `labs/<вид>/<книга>-<глава>.json` (их создают крейты `packages/*lab`).
    pub fn labs_dir(&self) -> PathBuf {
        self.data_dir.join("labs")
    }

    pub fn sql_dir(&self) -> PathBuf {
        self.data_dir.join("sql")
    }
}
