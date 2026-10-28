//! Exercise goal: identifier and text shown to the student.

use serde::{Deserialize, Serialize};

/// Exercise goal. `id` is the key in the submitted solution (JSON `{id: data, …}`), `text` is the goal statement.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Goal {
    /// Goal identifier (in hv, numa and migration it equals the program or scenario id).
    pub id: String,
    /// Goal text.
    pub text: String,
}

impl Goal {
    /// Goal from an identifier and text.
    pub fn new(id: impl Into<String>, text: impl Into<String>) -> Self {
        Goal { id: id.into(), text: text.into() }
    }
}
