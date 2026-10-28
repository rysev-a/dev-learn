//! Errors in the exercise description and data parsing.

use std::fmt;

/// Error in the exercise description (`Spec`) or in the model input data.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SpecError(pub String);

impl SpecError {
    /// Error with a message.
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
