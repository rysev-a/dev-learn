//! Лаборатория «Архитектура компьютера» (книга 14), часть «схемы из вентилей, процессор Мини-8 и его
//! ассемблер» (главы 6–15). Один крейт для всех: интерфейс (wasm) рисует доску и считает схему,
//! бэкенд сам проверяет присланное решение. RISC-V (главы 16–17) — отдельный крейт.
//!
//! * [`model`], [`eval`] — вентили, провода, симулятор (комбинационный и с обратными связями);
//! * [`interfaces`], [`blocks`] — типы портов, блоки, шины, разворачивание блоков в плоскую схему;
//! * [`exercise`], [`data`], [`registry`], [`progress`] — упражнения как данные и доступ к ним;
//! * [`check`] — проверка решения: [`check::verify`] → [`check::Verdict`];
//! * [`cpu8`] — процессор «Мини-8» из блоков и вентилей; [`asm`] — его команды, ассемблер и эмулятор;
//! * [`wave`], [`layout`] — временная диаграмма, геометрия досок и автопроводка.
//!
//! Без wasm-специфики: собирается нативно и под `wasm32-unknown-unknown`; зависимости — только `serde`.

pub mod asm;
pub mod blocks;
pub mod check;
pub mod cpu8;
pub mod data;
pub mod eval;
pub mod exercise;
pub mod format;
pub mod interfaces;
pub mod layout;
pub mod model;
pub mod progress;
pub mod registry;
pub mod wave;

pub use blocks::{BlockLibrary, Solution};
pub use check::{verify, Verdict};
pub use data::{ArchLab, DraftStore, ReferenceStore, SolutionStore};
pub use exercise::{LabChapter, Spec, Task};
