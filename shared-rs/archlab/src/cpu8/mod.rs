//! Процессор «Мини-8», собранный из вентилей и блоков.
//!
//! * [`builders`] — конструкторы схем (вентили и блоки собираются кодом);
//! * [`blocks`] — каталог блоков: от мультиплексора до процессора;
//! * [`fast`] — быстрый симулятор (схемы без обратных связей, кроме триггеров);
//! * [`machine`] — машина на вентилях с тем же интерфейсом, что у эмулятора [`crate::asm::Machine`].

pub mod blocks;
pub mod builders;
pub mod fast;
pub mod machine;

pub use blocks::{cpu8_blocks, cpu8_def, Cpu8Blocks};
pub use fast::{CombinationalLoopError, CompiledSim};
pub use machine::{cpu_expansion, GateMachine};
