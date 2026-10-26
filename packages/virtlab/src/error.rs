//! Ошибки описания упражнения и разбора данных.

use std::fmt;

/// Ошибка в описании упражнения (`Spec`) или во входных данных модели.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SpecError(pub String);

impl SpecError {
    /// Ошибка с сообщением.
    pub fn new(msg: impl Into<String>) -> Self {
        SpecError(msg.into())
    }
}

impl fmt::Display for SpecError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for SpecError {}
