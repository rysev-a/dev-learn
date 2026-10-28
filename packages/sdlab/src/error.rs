//! Lab data parse error: a clear human-readable message.

use std::fmt;

/// Error reading a design or a data file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SdError(pub String);

impl SdError {
    pub fn new(msg: impl Into<String>) -> SdError {
        SdError(msg.into())
    }
}

impl fmt::Display for SdError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for SdError {}

impl From<serde_json::Error> for SdError {
    fn from(e: serde_json::Error) -> SdError {
        SdError(i18n::trf!("invalid JSON: {0}", e))
    }
}
