//! The "HTML and CSS" lab (book 11, "Modern Frontend").
//!
//! The student writes markup or styles; the solution is checked **without a browser**, by the same code in the UI (wasm) and on the server:
//! * [`html`] — structural checks of markup (elements, nesting, attributes, text, headings, field labels, `alt`);
//! * [`css`] — stylesheet parsing, the cascade (specificity, order, `!important`, `@media`), inheritance, `var()` and computed values;
//! * [`selector`] — specificity and "write a selector" tasks;
//! * [`verify`] — the whole task: data ([`spec::Task`]) + solution ([`spec::Solution`]) → report ([`spec::Report`]).
//!
//! Geometry and pixels (flex/grid layout, screenshots) are not computed here: they need a real engine.

pub mod css;
pub mod html;
pub mod selector;
pub mod spec;
pub mod verify;

pub use spec::{Check, Item, Kind, Report, Solution, Task};
pub use verify::verify;
