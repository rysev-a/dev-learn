//! Данные курса, общие для бэкенда, фронтенда и генераторов содержимого.
//!
//! * [`tone`], [`item`], [`scene`], [`dsl`] — анимированные схемы (покадровые сцены);
//! * [`slide`] — слайды, главы и блоки тела слайда.
//!
//! Всё — обычные структуры с `serde`: бэкенд хранит их в базе как документы, клиент рисует, генераторы создают.
//! Ошибка в данных находится при компиляции сцены ([`Scene::compile`]) и проверке главы ([`slide::Chapter::check`]).

pub mod dsl;
pub mod item;
pub mod scene;
pub mod slide;
pub mod tone;

pub use highlight::Lang;
pub use item::Item;
pub use scene::{Frame, Scene, SceneError, SceneSpec};
pub use slide::{Block, Chapter, Slide};
pub use tone::{Tone, B, G, M, R, V, Y};
