//! Leptos (CSR) frontend of "cs-core": styles are `styles/app.css` and the lab styles.
//! Chapter 1 of "Discrete Mathematics" and chapter 0 of "Python as a First Language" are ported (slides - crate `course`); quizzes, answers and
//! code exercises work for any chapter.

mod app;
pub mod components;
mod dom;
mod hooks;
pub mod pages;
pub mod player;
pub mod progress;
pub mod recorder;
pub mod session;
pub mod settings;
pub mod themes;

pub use app::App;
