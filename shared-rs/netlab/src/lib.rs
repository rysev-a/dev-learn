//! Лаборатория «Компьютерные сети» (книга 15): модель сети, симулятор, мини-терминал Linux, проверка целей и
//! данные упражнений. Общий крейт интерфейса (wasm) и бэкенда (серверная проверка присланного решения).
//!
//! * [`types`], [`model`], [`ip`] — состояние сети (устройства, интерфейсы, кабели, службы) и операции над ним;
//! * [`sim`] — кадры, ARP, коммутаторы и VLAN, маршрутизация, TCP/UDP/ICMP, NAT, файрвол, MTU, туннели,
//!   балансировщик; [`dns`], [`http`], [`tls`], [`ssh`], [`transfer`], [`pageload`], [`capture`], [`attacks`] — службы
//!   и модели поверх неё;
//! * [`term`] — мини-терминал (`exec`) и общие для форм функции настройки;
//! * [`check`] — цели упражнений и шаги решения, [`lab`] — данные упражнений и [`lab::verify`].
//!
//! Всё детерминировано; время — в микросекундах. Крейт не знает о wasm: он собирается и нативно, и под
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
