//! Цель упражнения: идентификатор и текст для показа ученику.

use serde::{Deserialize, Serialize};

/// Цель упражнения. `id` — ключ в присылаемом решении (JSON `{id: данные, …}`), `text` — условие цели.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Goal {
    /// Идентификатор цели (в hv, numa и migration совпадает с id программы или сценария).
    pub id: String,
    /// Текст цели.
    pub text: String,
}

impl Goal {
    /// Цель из идентификатора и текста.
    pub fn new(id: impl Into<String>, text: impl Into<String>) -> Self {
        Goal { id: id.into(), text: text.into() }
    }
}
