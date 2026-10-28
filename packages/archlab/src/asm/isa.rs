//! The "Mini-8" instruction set: 8-bit data, 8 registers, a 16-bit instruction.
//!
//! ```text
//!   15..12   11..9   8..6   5..0
//!   opcode     A      B      C
//! ```
//!
//! Fields A, B, C are interpreted differently depending on the instruction format. Port of `isa.ts`.

pub const REG_COUNT: usize = 8;
pub const MEM_SIZE: usize = 256;
pub const PROGRAM_MAX: usize = 256;

/// Instruction format.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Format {
    /// `hlt`
    None,
    /// `li rd, imm8`
    Li,
    /// `add rd, rs, rt`
    R,
    /// `addi rd, rs, imm6`
    I,
    /// `lb rd, imm6(rs)`
    Mem,
    /// `beq ra, rb, label`
    Branch,
    /// `jmp label`
    Jump,
}

/// Instruction description.
#[derive(Debug, Clone, Copy)]
pub struct OpDef {
    pub mnemonic: &'static str,
    pub opcode: u16,
    pub format: Format,
    /// What it does — in one line.
    pub meaning: &'static str,
    pub example: &'static str,
}

const fn op(mnemonic: &'static str, opcode: u16, format: Format, meaning: &'static str, example: &'static str) -> OpDef {
    OpDef { mnemonic, opcode, format, meaning, example }
}

/// All instructions.
pub const OPS: [OpDef; 15] = [
    op("hlt", 0x0, Format::None, i18n::t!("halt the processor"), "hlt"),
    op("li", 0x1, Format::Li, i18n::t!("rd = number (0…255)"), "li r1, 72"),
    op("add", 0x2, Format::R, "rd = rs + rt", "add r1, r2, r3"),
    op("sub", 0x3, Format::R, "rd = rs − rt", "sub r1, r2, r3"),
    op("and", 0x4, Format::R, i18n::t!("rd = rs AND rt (bitwise)"), "and r1, r2, r3"),
    op("or", 0x5, Format::R, i18n::t!("rd = rs OR rt (bitwise)"), "or r1, r2, r3"),
    op("xor", 0x6, Format::R, i18n::t!("rd = rs XOR rt (bitwise)"), "xor r1, r2, r3"),
    op("addi", 0x7, Format::I, i18n::t!("rd = rs + number (−32…31)"), "addi r1, r1, 1"),
    op("lb", 0x8, Format::Mem, i18n::t!("rd = byte from memory [rs + offset]"), "lb r1, 0(r2)"),
    op("sb", 0x9, Format::Mem, i18n::t!("memory [rs + offset] = rd"), "sb r1, 0(r2)"),
    op("beq", 0xa, Format::Branch, i18n::t!("if ra = rb, jump to label"), i18n::t!("beq r1, r2, end")),
    op("bne", 0xb, Format::Branch, i18n::t!("if ra ≠ rb, jump to label"), i18n::t!("bne r1, r2, loop")),
    op("bltu", 0xc, Format::Branch, i18n::t!("if ra < rb (unsigned), jump"), i18n::t!("bltu r1, r2, next")),
    op("bgeu", 0xd, Format::Branch, i18n::t!("if ra ≥ rb (unsigned), jump"), i18n::t!("bgeu r1, r2, next")),
    op("jmp", 0xe, Format::Jump, i18n::t!("unconditional jump to label"), i18n::t!("jmp loop")),
];

/// Pseudo-instruction: a shorthand the assembler itself replaces with a real one.
#[derive(Debug, Clone, Copy)]
pub struct Pseudo {
    pub name: &'static str,
    pub example: &'static str,
    pub becomes: &'static str,
}

/// All pseudo-instructions.
pub const PSEUDO: [Pseudo; 9] = [
    Pseudo { name: "nop", example: "nop", becomes: "addi r0, r0, 0" },
    Pseudo { name: "mv", example: "mv r1, r2", becomes: "addi r1, r2, 0" },
    Pseudo { name: "inc", example: "inc r1", becomes: "addi r1, r1, 1" },
    Pseudo { name: "dec", example: "dec r1", becomes: "addi r1, r1, -1" },
    Pseudo { name: "beqz", example: i18n::t!("beqz r1, label"), becomes: i18n::t!("beq r1, r0, label") },
    Pseudo { name: "bnez", example: i18n::t!("bnez r1, label"), becomes: i18n::t!("bne r1, r0, label") },
    Pseudo { name: "bgtu", example: i18n::t!("bgtu r1, r2, label"), becomes: i18n::t!("bltu r2, r1, label") },
    Pseudo { name: "bleu", example: i18n::t!("bleu r1, r2, label"), becomes: i18n::t!("bgeu r2, r1, label") },
    Pseudo { name: "j", example: i18n::t!("j label"), becomes: i18n::t!("jmp label") },
];

/// Instruction by mnemonic.
pub fn op_by_mnemonic(m: &str) -> Option<&'static OpDef> {
    OPS.iter().find(|o| o.mnemonic == m)
}

/// Instruction by opcode.
pub fn op_by_opcode(c: u16) -> Option<&'static OpDef> {
    OPS.iter().find(|o| o.opcode == c)
}

/// Number of `bits` bits → signed.
pub fn to_signed(value: i32, bits: u32) -> i32 {
    let mask = (1i32 << bits) - 1;
    let v = value & mask;
    if v & (1 << (bits - 1)) != 0 {
        v - (1 << bits)
    } else {
        v
    }
}

/// Assemble a word from fields.
pub fn pack(opcode: u16, a: u16, b: u16, c: i32) -> u16 {
    ((opcode & 0xf) << 12) | ((a & 7) << 9) | ((b & 7) << 6) | (c as u16 & 0x3f)
}

/// Instruction word split into fields.
#[derive(Debug, Clone, Copy)]
pub struct Decoded {
    pub word: u16,
    pub opcode: u16,
    pub a: u16,
    pub b: u16,
    pub c: u16,
    pub def: Option<&'static OpDef>,
}

/// Decode a word.
pub fn decode(word: u16) -> Decoded {
    Decoded {
        word,
        opcode: word >> 12,
        a: (word >> 9) & 7,
        b: (word >> 6) & 7,
        c: word & 0x3f,
        def: op_by_opcode(word >> 12),
    }
}

fn signed_str(n: i32) -> String {
    if n >= 0 {
        format!("+{n}")
    } else {
        n.to_string()
    }
}

/// Instruction back to text — for the machine code listing.
pub fn disassemble(word: u16) -> String {
    let d = decode(word);
    let Some(def) = d.def else {
        return format!(".word 0x{:04x}", d.word);
    };
    match def.format {
        Format::None => "hlt".to_string(),
        Format::Li => format!("li r{}, {}", d.a, word & 0xff),
        Format::R => format!("{} r{}, r{}, r{}", def.mnemonic, d.a, d.b, d.c & 7),
        Format::I => format!("{} r{}, r{}, {}", def.mnemonic, d.a, d.b, to_signed(d.c as i32, 6)),
        Format::Mem => format!("{} r{}, {}(r{})", def.mnemonic, d.a, to_signed(d.c as i32, 6), d.b),
        Format::Branch => format!("{} r{}, r{}, {}", def.mnemonic, d.a, d.b, signed_str(to_signed(d.c as i32, 6))),
        Format::Jump => format!("jmp {}", signed_str(to_signed((word & 0xfff) as i32, 12))),
    }
}

/// Binary notation of a word by fields — for "how an instruction is structured".
pub fn fields(word: u16) -> (String, String, String, String) {
    let d = decode(word);
    (format!("{:04b}", d.opcode), format!("{:03b}", d.a), format!("{:03b}", d.b), format!("{:06b}", d.c))
}
