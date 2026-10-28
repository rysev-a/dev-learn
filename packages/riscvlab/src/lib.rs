#![warn(missing_docs)]

//! RISC-V lab (book 14 "Computer Architecture", chapters 16–17).
//!
//! * [`isa`] — the RV32IM instruction set: encoding, decoding, disassembler, field-level parsing;
//! * [`asm`] — the assembler (labels, directives, pseudo-instructions, error messages in Russian);
//! * [`machine`] — emulator of a "soft processor" with 16 KiB of memory, UART, LEDs, switches and a timer;
//! * [`task`] — exercises as data (`LabChapter`, `TaskSpec`) and [`task::verify`] — server-side solution check;
//! * [`export`] — conversion of the TypeScript export into data files (the `import` binary);
//! * [`project`] — a project for building on your own computer (Makefile, README, zip).
//!
//! The crate works both natively (the backend checks submitted solutions) and in wasm (the UI runs the program
//! step by step). The only dependency is `serde`.

pub mod asm;
pub mod export;
pub mod isa;
pub mod js;
pub mod machine;
pub mod project;
pub mod task;

pub use asm::{assemble, AsmError, AsmLine, AsmResult, DATA_BASE, RAM_SIZE, STACK_RESERVE, STACK_TOP, TEXT_BASE};
pub use machine::{Machine, Options, TraceStep, View};
pub use task::{verify, Check, LabChapter, Task, TaskSpec, Verdict};
