//! The "Mini-8" processor built from gates and blocks.
//!
//! * [`builders`] — circuit constructors (gates and blocks are assembled by code);
//! * [`blocks`] — block catalog: from a multiplexer up to the processor;
//! * [`fast`] — fast simulator (circuits without feedback loops, except flip-flops);
//! * [`machine`] — gate-level machine with the same interface as the emulator [`crate::asm::Machine`].

pub mod blocks;
pub mod builders;
pub mod fast;
pub mod machine;

pub use blocks::{cpu8_blocks, cpu8_def, Cpu8Blocks};
pub use fast::{CombinationalLoopError, CompiledSim};
pub use machine::{cpu_expansion, GateMachine};
