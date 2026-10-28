//! "Computer Networks" lab (book 15): network model, simulator, Linux mini-terminal, goal checking and
//! exercise data. Shared crate of the interface (wasm) and the backend (server-side check of a submitted solution).
//!
//! * [`types`], [`model`], [`ip`]: network state (devices, interfaces, cables, services) and operations on it;
//! * [`sim`]: frames, ARP, switches and VLAN, routing, TCP/UDP/ICMP, NAT, firewall, MTU, tunnels,
//!   load balancer; [`dns`], [`http`], [`tls`], [`ssh`], [`transfer`], [`pageload`], [`capture`], [`attacks`]: services
//!   and models on top of it;
//! * [`term`]: mini-terminal (`exec`) and the configuration functions shared with the forms;
//! * [`check`]: exercise goals and solution steps, [`lab`]: exercise data and [`lab::verify`].
//!
//! Everything is deterministic; time is in microseconds. The crate knows nothing about wasm: it builds natively and for
//! `wasm32-unknown-unknown`.

#![allow(clippy::result_large_err, clippy::too_many_arguments, clippy::large_enum_variant)]

pub mod attacks;
pub mod capture;
pub mod check;
pub mod dns;
pub mod export;
pub mod http;
pub mod ip;
pub mod lab;
pub mod model;
pub mod pageload;
pub mod sim;
pub mod ssh;
pub mod term;
pub mod tls;
pub mod transfer;
pub mod types;
pub mod util;

pub use check::{apply_ops, check_goals, Goal, GoalKind, GoalResult, Step};
pub use lab::{verify, verify_json, LabChapter, NetSpec, Task, Tools, Verdict};
pub use model::{state_from_json, MacGen};
pub use term::{exec, CmdResult};
pub use types::NetState;
