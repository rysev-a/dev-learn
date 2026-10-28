//! Какие главы книги «Архитектура компьютера» — лаборатории: номер главы → раздел схем или ассемблер.
//! Порт `registry.ts` (главы 6–15; RISC-V и настоящие программы, главы 16–17, — в другом крейте).

use crate::model::GateType;

/// Раздел упражнений со схемами (`sections.ts`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SectionInfo {
    pub slug: &'static str,
    pub title: &'static str,
    pub description: &'static str,
    /// Ключ прогресса в браузере (`progressKey`).
    pub progress_key: &'static str,
    /// Глава книги, в которой лежит раздел.
    pub chapter: u32,
}

/// Разделы со схемами по порядку глав 6–14.
pub const SECTIONS: [SectionInfo; 9] = [
    SectionInfo { slug: "simple-circuits", title: i18n::t!("Simple circuits"), description: i18n::t!("Logic gates and truth tables: from a wire to a multiplexer"), progress_key: "simple", chapter: 6 },
    SectionInfo { slug: "mux", title: i18n::t!("Multiplexers"), description: i18n::t!("Selecting and routing signals: multiplexers, decoders, encoders, buses"), progress_key: "mux", chapter: 7 },
    SectionInfo { slug: "latches", title: i18n::t!("Latches"), description: i18n::t!("First memory built from gates: SR and D latches, register, memory cell"), progress_key: "latches", chapter: 8 },
    SectionInfo { slug: "adders", title: i18n::t!("Adders"), description: i18n::t!("Adding bits: half adder and full adder"), progress_key: "adders", chapter: 9 },
    SectionInfo { slug: "registers", title: i18n::t!("Registers and clock"), description: i18n::t!("Edge-triggered flip-flop, registers, shifting, counters and accumulator — driven by the clock"), progress_key: "registers", chapter: 10 },
    SectionInfo { slug: "alu", title: i18n::t!("ALU"), description: i18n::t!("Arithmetic and logic with operation select: 2-bit ALU, flags and branch conditions"), progress_key: "alu", chapter: 11 },
    SectionInfo { slug: "memory", title: i18n::t!("Memory"), description: i18n::t!("ROM, address map, latch-based cells, RAM and synchronous flip-flop memory"), progress_key: "memory", chapter: 12 },
    SectionInfo { slug: "decoder", title: i18n::t!("Instruction decoder"), description: i18n::t!("From opcode to control signals: conditions, next address and clock phases"), progress_key: "decoder", chapter: 13 },
    SectionInfo { slug: "cpu", title: i18n::t!("Processor from blocks"), description: i18n::t!("Your circuits as blocks with interfaces: buses, looking inside, and assembling a processor"), progress_key: "cpu", chapter: 14 },
];

/// Глава с ассемблером Мини-8.
pub const ASM_CHAPTER: u32 = 15;

/// Тип лаборатории главы.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LabKind {
    /// Схемы из вентилей и блоков; раздел `slug`.
    Circuit(&'static str),
    /// Ассемблер процессора Мини-8.
    Asm,
}

/// Тип лаборатории главы (`LAB_CHAPTERS`); `None` — не лаборатория этого крейта.
pub fn lab_kind(chapter: u32) -> Option<LabKind> {
    if chapter == ASM_CHAPTER {
        return Some(LabKind::Asm);
    }
    section_of_chapter(chapter).map(|s| LabKind::Circuit(s.slug))
}

/// Раздел, лежащий в главе.
pub fn section_of_chapter(chapter: u32) -> Option<&'static SectionInfo> {
    SECTIONS.iter().find(|s| s.chapter == chapter)
}

/// Раздел по slug.
pub fn section_by_slug(slug: &str) -> Option<&'static SectionInfo> {
    SECTIONS.iter().find(|s| s.slug == slug)
}

/// Номер главы, в которой лежит раздел со схемами (`CHAPTER_OF_SLUG`).
pub fn chapter_of_slug(slug: &str) -> Option<u32> {
    section_by_slug(slug).map(|s| s.chapter)
}

/// Все номера глав этого крейта: 6–15.
pub fn chapters() -> impl Iterator<Item = u32> {
    SECTIONS.iter().map(|s| s.chapter).chain(std::iter::once(ASM_CHAPTER))
}

/// Составные элементы: каждый собирается из базовых вентилей. Собрав его вручную в указанном
/// упражнении, ученик открывает готовый блок в палитре (`COMPOSITE_GATES`).
pub fn composite_requirement(ty: GateType) -> Option<(&'static str, &'static str)> {
    match ty {
        GateType::Nand => Some(("simple-circuits", "nand")),
        GateType::Xor => Some(("simple-circuits", "xor")),
        // XNOR — «НЕ от XOR»: открывается вместе с ним
        GateType::Xnor => Some(("simple-circuits", "xor")),
        // триггер по фронту ученик сначала собирает сам — из ведущей и ведомой защёлок
        GateType::Dff => Some(("registers", "dff")),
        _ => None,
    }
}
