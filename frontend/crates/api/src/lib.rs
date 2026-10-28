//! Course API client without UI: typed calls and DTOs (books, chapters, progress, quizzes, answers, exercises, check queue).
//!
//! Works with both backends (Python and axum): errors arrive as `{"detail": …}` or `{"error": …}`, the session token goes in the
//! `Authorization: Bearer` header. Pure functions (error parsing, DTOs) are covered by ordinary tests; the network part lives in [`Client`].

mod client;
pub mod dto;
mod error;

pub use client::Client;
pub use error::ApiError;
