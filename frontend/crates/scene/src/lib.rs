//! Rendering of frame-by-frame slide scenes in Leptos. Scene data (elements, frames, compilation) lives in the `content` crate; here:
//!
//! * [`view`] — components: the scene shell ([`Stage`]), smooth SVG nodes, rendering of every element kind, [`SceneView`];
//! * [`paint`] — per-shape color override for scenes with custom rendering;
//! * [`env`] — environment (voice-over time, "no motion").
//!
//! For scene data and its checks (`cargo test`) see `content` and the generators (`packages/gen`).

pub mod env;
pub mod paint;
pub mod view;

pub use ::highlight::Lang;
pub use content::{dsl, Frame, Item, Scene, SceneSpec, Tone, B, G, M, R, V, Y};
pub use env::{provide_env, SceneEnv};
pub use paint::{Paint, ACC, AMB, BLU, MUTED, PANEL, RED};
pub use view::{use_reveal, use_steps, DotView, Pill, SceneView, Stage, StepsCtl, Txt, G as Group};
