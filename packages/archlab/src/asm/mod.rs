//! The "Mini-8" processor: instruction set, assembler, emulator and the chapter 15 tasks.
//!
//! * [`isa`] — instructions, formats, encoding and decoding of words;
//! * [`assembler`] — program text → machine words, all errors are collected rather than just the first;
//! * [`machine`] — emulator with instruction memory separate from the disk (256 bytes);
//! * [`tasks`] — comparing the disk with the expected one and explaining the mismatch in plain language.
//!
//! The same processor built from gates — [`crate::cpu8`].

pub mod assembler;
pub mod isa;
pub mod machine;
pub mod tasks;

pub use assembler::{assemble, AsmError, AsmLine, AsmResult};
pub use machine::{Machine, MachineView};
