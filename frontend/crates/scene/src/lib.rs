//! Отрисовка покадровых схем слайдов на Leptos. Данные сцены (элементы, кадры, компиляция) — в crate `content`; здесь:
//!
//! * [`view`] — компоненты: оболочка сцены ([`Stage`]), плавные узлы SVG, отрисовка каждого вида элемента, [`SceneView`];
//! * [`paint`] — точечная смена цвета фигур для сцен со своей отрисовкой;
//! * [`env`] — среда (время озвучки, «без движения»).
//!
//! Данные сцен и их проверку (`cargo test`) см. в `content` и в генераторах (`packages/gen`).

pub mod env;
pub mod paint;
pub mod view;

pub use ::highlight::Lang;
pub use content::{dsl, Frame, Item, Scene, SceneSpec, Tone, B, G, M, R, V, Y};
pub use env::{provide_env, SceneEnv};
pub use paint::{Paint, ACC, AMB, BLU, MUTED, PANEL, RED};
pub use view::{use_reveal, use_steps, DotView, Pill, SceneView, Stage, StepsCtl, Txt, G as Group};
