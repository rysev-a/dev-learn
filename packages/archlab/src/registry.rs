//! Which chapters of the "Computer Architecture" book are labs: chapter number → circuit section or assembler.
//! Port of `registry.ts` (chapters 6–15; RISC-V and real programs, chapters 16–17, are in another crate).

use crate::model::GateType;

/// Section of circuit exercises (`sections.ts`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SectionInfo {
    pub slug: &'static str,
    pub title: &'static str,
    pub description: &'static str,
    /// Progress key in the browser (`progressKey`).
    pub progress_key: &'static str,
    /// Book chapter the section lives in.
    pub chapter: u32,
}

/// Circuit sections in the order of chapters 6–14.
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

/// Chapter with the Mini-8 assembler.
pub const ASM_CHAPTER: u32 = 15;

/// Lab type of a chapter.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LabKind {
    /// Circuits from gates and blocks; section `slug`.
    Circuit(&'static str),
    /// Assembler of the Mini-8 processor.
    Asm,
}

/// Lab type of a chapter (`LAB_CHAPTERS`); `None` — not a lab of this crate.
pub fn lab_kind(chapter: u32) -> Option<LabKind> {
    if chapter == ASM_CHAPTER {
        return Some(LabKind::Asm);
    }
    section_of_chapter(chapter).map(|s| LabKind::Circuit(s.slug))
}

/// Section that lives in the chapter.
pub fn section_of_chapter(chapter: u32) -> Option<&'static SectionInfo> {
    SECTIONS.iter().find(|s| s.chapter == chapter)
}

/// Section by slug.
pub fn section_by_slug(slug: &str) -> Option<&'static SectionInfo> {
    SECTIONS.iter().find(|s| s.slug == slug)
}

/// Number of the chapter the circuit section lives in (`CHAPTER_OF_SLUG`).
pub fn chapter_of_slug(slug: &str) -> Option<u32> {
    section_by_slug(slug).map(|s| s.chapter)
}

/// All chapter numbers of this crate: 6–15.
pub fn chapters() -> impl Iterator<Item = u32> {
    SECTIONS.iter().map(|s| s.chapter).chain(std::iter::once(ASM_CHAPTER))
}

/// Composite elements: each is built from basic gates. By building one by hand in the given
/// exercise, the student unlocks the ready-made block in the palette (`COMPOSITE_GATES`).
pub fn composite_requirement(ty: GateType) -> Option<(&'static str, &'static str)> {
    match ty {
        GateType::Nand => Some(("simple-circuits", "nand")),
        GateType::Xor => Some(("simple-circuits", "xor")),
        // XNOR — "NOT of XOR": unlocks together with it
        GateType::Xnor => Some(("simple-circuits", "xor")),
        // the student first builds the edge-triggered flip-flop by hand — from master and slave latches
        GateType::Dff => Some(("registers", "dff")),
        _ => None,
    }
}
