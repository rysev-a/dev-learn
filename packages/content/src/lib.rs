//! Course data shared by the backend, the frontend and the content generators.
//!
//! * [`tone`], [`item`], [`scene`], [`dsl`] — animated diagrams (frame-by-frame scenes);
//! * [`slide`] — slides, chapters and the blocks of a slide body.
//!
//! Everything is plain `serde` structs: the backend stores them in the database as documents, the client renders them, the generators create them.
//! Errors in the data are caught when a scene is compiled ([`Scene::compile`]) and a chapter is checked ([`slide::Chapter::check`]).

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
