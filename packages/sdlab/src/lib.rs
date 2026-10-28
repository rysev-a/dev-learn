//! "System design" lab (book 18): a design of a high-load service built from components and its evaluation under a given
//! workload. Shared crate: the frontend (wasm) draws the board and computes metrics on the fly, the backend stores exercises as data
//! and verifies submitted solutions itself ([`verify`]).
//!
//! * [`types`] — design, workload, evaluation result, goals, exercises and data files;
//! * [`kinds`] — catalog of components and parameters, [`reference`] — model numbers (capacity, prices, latencies);
//! * [`engine`] — deterministic evaluation ([`evaluate`]), an exact port of the TypeScript version;
//! * [`checks`] — exercise goals ([`check_goals`], [`describe`]);
//! * [`layout`], [`ports`] — column layout, ports, link validity and auto-links (for the design board);
//! * [`verify`] — server-side solution verification;
//! * [`data`] — reading chapter data files.
//!
//! The only dependency is `serde`; builds natively and for `wasm32-unknown-unknown`.

pub mod checks;
pub mod data;
pub mod engine;
pub mod error;
pub mod import;
pub mod jsfmt;
pub mod kinds;
pub mod layout;
pub mod ports;
pub mod pretty;
pub mod reference;
pub mod types;
pub mod verify;

pub use checks::{all_ok, check_goals, describe, fail_label};
pub use engine::{can_link, evaluate};
pub use error::SdError;
pub use kinds::{default_params, spec, KindSpec, ParamSpec, ParamType};
pub use types::*;
pub use verify::{parse_solution, verify, verify_raw, Problem, Verdict};
