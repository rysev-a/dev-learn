#![warn(missing_docs)]

//! Лаборатория RISC-V (книга 14 «Архитектура компьютера», главы 16–17).
//!
//! * [`isa`] — набор команд RV32IM: кодирование, декодирование, дизассемблер, разбор по полям;
//! * [`asm`] — ассемблер (метки, директивы, псевдокоманды, сообщения об ошибках на русском);
//! * [`machine`] — эмулятор «мягкого процессора» с памятью 16 КиБ, UART, светодиодами, переключателями и таймером;
//! * [`task`] — упражнения как данные (`LabChapter`, `TaskSpec`) и [`task::verify`] — серверная проверка решения;
//! * [`export`] — перевод выгрузки из TypeScript в файлы данных (бинарь `import`);
//! * [`project`] — проект для сборки на своём компьютере (Makefile, README, zip).
//!
//! Крейт работает и нативно (бэкенд проверяет присланные решения), и в wasm (интерфейс исполняет программу
//! пошагово). Зависимости — только `serde`.

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
