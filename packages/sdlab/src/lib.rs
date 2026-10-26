//! Лаборатория «Системный дизайн» (книга 18): схема высоконагруженного сервиса из компонентов и расчёт под заданной
//! нагрузкой. Общий crate: фронтенд (wasm) рисует поле и считает метрики на лету, бэкенд хранит упражнения как данные
//! и сам проверяет присланные решения ([`verify`]).
//!
//! * [`types`] — схема, нагрузка, результат расчёта, цели, упражнения и файлы данных;
//! * [`kinds`] — справочник компонентов и параметров, [`reference`] — числа модели (ёмкость, цены, задержки);
//! * [`engine`] — детерминированный расчёт ([`evaluate`]), точный порт TypeScript-версии;
//! * [`checks`] — цели упражнения ([`check_goals`], [`describe`]);
//! * [`layout`], [`ports`] — раскладка по колонкам, порты, допустимость связей и автосвязи (для поля схемы);
//! * [`verify`] — серверная проверка решения;
//! * [`data`] — чтение файлов данных глав.
//!
//! Зависимости — только `serde`; собирается нативно и под `wasm32-unknown-unknown`.

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
