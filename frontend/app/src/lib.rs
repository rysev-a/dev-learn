//! Фронтенд «say» на Leptos (CSR): стили — `styles/app.css` и стили лабораторий.
//! Перенесены главы 1 «Дискретной математики» и 0 «Python как первый язык» (слайды — crate `course`); квизы, ответы и
//! упражнения с кодом работают для любой главы.

mod app;
pub mod components;
mod dom;
mod hooks;
pub mod pages;
pub mod player;
pub mod progress;
pub mod session;
pub mod settings;
pub mod themes;

pub use app::App;
