//! Laboratory "Computer Architecture" (book 14), the part "circuits from gates, the Mini-8 processor and its
//! assembler" (chapters 6–15). One crate for everyone: the interface (wasm) draws the board and computes the circuit,
//! the backend verifies the submitted solution itself. RISC-V (chapters 16–17) is a separate crate.
//!
//! * [`model`], [`eval`] — gates, wires, simulator (combinational and with feedback loops);
//! * [`interfaces`], [`blocks`] — port types, blocks, buses, expanding blocks into a flat circuit;
//! * [`exercise`], [`data`], [`registry`], [`progress`] — exercises as data and access to them;
//! * [`check`] — solution check: [`check::verify`] → [`check::Verdict`];
//! * [`cpu8`] — the "Mini-8" processor made of blocks and gates; [`asm`] — its instructions, assembler and emulator;
//! * [`wave`], [`layout`] — timing diagram, board geometry and auto-wiring.
//!
//! No wasm specifics: builds natively and for `wasm32-unknown-unknown`; the only dependency is `serde`.

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
