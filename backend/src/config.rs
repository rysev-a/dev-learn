//! Settings from the environment. Default paths - the `data` directory next to the backend:
//! textbooks, SQL files of exercises/quizzes, slides, lab data and audio.

use std::path::PathBuf;

#[derive(Debug, Clone)]
pub struct Config {
    pub bind: String,
    pub surreal_url: String,
    pub data_dir: PathBuf,
    pub audio_dir: PathBuf,
    /// voice recordings for slides from the interface (`RECORDS_DIR`): `<book>/<chapter>/<slide>.<extension>`
    pub records_dir: PathBuf,
    /// directory of the built frontend (`frontend/dist`); empty - API without static files
    pub static_dir: Option<PathBuf>,
    /// shared secret of the workers (`CS_CORE_WORKER_TOKEN`); empty - the internal worker API is unavailable
    pub worker_token: String,
    /// `auto` - reseed the course if the sources changed; `always`; `off`
    pub seed: String,
    /// pronunciation check of the recordings (`AZURE_SPEECH_KEY`/`AZURE_SPEECH_KEY_1`/`_2`, `AZURE_SPEECH_REGION`); `None` - not configured
    pub speech: Option<crate::speech::Speech>,
}

fn env_or(key: &str, default: &str) -> String {
    std::env::var(key).ok().filter(|v| !v.is_empty()).unwrap_or_else(|| default.to_string())
}

impl Config {
    pub fn from_env() -> Self {
        let data_dir = PathBuf::from(env_or("DATA_DIR", "data"));
        let audio_dir = std::env::var("AUDIO_DIR").map(PathBuf::from).unwrap_or_else(|_| data_dir.join("audio"));
        let static_dir = std::env::var("STATIC_DIR").ok().filter(|v| !v.is_empty()).map(PathBuf::from);
        // by default - `media/records` in the repository root (the backend is run from `backend/`)
        let records_dir = PathBuf::from(env_or("RECORDS_DIR", "../media/records"));
        Self {
            bind: env_or("BIND", "0.0.0.0:8001"),
            surreal_url: env_or("SURREALDB_URL", "ws://127.0.0.1:8123"),
            data_dir,
            audio_dir,
            records_dir,
            static_dir,
            worker_token: std::env::var("CS_CORE_WORKER_TOKEN").unwrap_or_default(),
            seed: env_or("SEED", "auto"),
            speech: crate::speech::Speech::from_env(),
        }
    }

    /// Translation directory: `data/<language>/` with the same layout as the Russian content.
    pub fn lang_dir(&self, lang: crate::lang::Lang) -> PathBuf {
        self.data_dir.join(lang.code())
    }

    pub fn textbook_dir(&self) -> PathBuf {
        self.data_dir.join("textbook")
    }

    /// Chapter slides: files `<book>-<chapter>.json` (created by the `packages/gen` generators).
    pub fn slides_dir(&self) -> PathBuf {
        self.data_dir.join("slides")
    }

    /// Lab exercises: `labs/<kind>/<book>-<chapter>.json` (created by the `packages/*lab` crates).
    pub fn labs_dir(&self) -> PathBuf {
        self.data_dir.join("labs")
    }

    pub fn sql_dir(&self) -> PathBuf {
        self.data_dir.join("sql")
    }
}
