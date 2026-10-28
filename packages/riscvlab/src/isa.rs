//! RISC-V RV32IM: real 32-bit instructions.
//! Encoding follows the "RISC-V Unprivileged ISA" specification (formats R, I, S, B, U, J).

use serde::{Deserialize, Serialize};

/// ABI names of registers x0…x31.
pub const ABI_NAMES: [&str; 32] = [
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2",
    "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
];

/// Register number by name: x5, t0, fp…
pub fn reg_num(name: &str) -> Option<u8> {
    let n = crate::js::trim(name).to_lowercase();
    if let Some(d) = n.strip_prefix('x') {
        // x0…x31 without leading zeros
        let ok = !d.is_empty()
            && d.len() <= 2
            && d.bytes().all(|b| b.is_ascii_digit())
            && (d.len() == 1 || !d.starts_with('0'));
        if ok {
            if let Ok(v) = d.parse::<u8>() {
                if v < 32 {
                    return Some(v);
                }
            }
        }
    }
    if n == "fp" {
        return Some(8);
    }
    ABI_NAMES.iter().position(|a| *a == n).map(|i| i as u8)
}

/// ABI name of a register by number.
pub fn reg_name(n: u8) -> &'static str {
    ABI_NAMES.get(usize::from(n)).copied().unwrap_or("?")
}

/// Instruction format.
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
pub enum Fmt {
    /// format R: three registers
    R,
    /// format I: immediate from the instruction
    I,
    /// shifts by an immediate: the upper seven bits are f7
    SH,
    /// load from memory (format I)
    L,
    /// format S: store to memory
    S,
    /// format B: conditional branch
    B,
    /// format U: long immediate
    U,
    /// format J: `jal` jump
    J,
    /// jalr
    JR,
    /// ecall, ebreak
    SYS,
}

/// Instruction set extension.
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
pub enum Ext {
    /// base set
    I,
    /// multiplication and division
    M,
}

/// Description of one instruction.
#[derive(Clone, Copy, Debug)]
pub struct OpInfo {
    /// instruction
    pub op: Op,
    /// mnemonic (lowercase)
    pub mnemonic: &'static str,
    /// instruction format
    pub fmt: Fmt,
    /// opcode (low 7 bits of the word)
    pub opcode: u32,
    /// f3 field, if any
    pub f3: Option<u32>,
    /// f7 field, if any
    pub f7: Option<u32>,
    /// instruction set extension
    pub ext: Ext,
    /// what it does (for the reference)
    pub meaning: &'static str,
    /// example of syntax
    pub example: &'static str,
}

macro_rules! ops {
    ($( $v:ident, $name:literal, $fmt:ident, $opc:expr, $f3:expr, $f7:expr, $ext:ident, $meaning:literal, $example:literal; )*) => {
        /// RV32IM instructions.
        #[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Serialize, Deserialize)]
        #[serde(rename_all = "lowercase")]
        pub enum Op { $( #[doc = concat!("`", $name, "`: ", $meaning)] $v ),* }

        /// Instruction table (order as in the reference; the index matches the `Op` variant number).
        pub const OPS: &[OpInfo] = &[
            $( OpInfo { op: Op::$v, mnemonic: $name, fmt: Fmt::$fmt, opcode: $opc, f3: $f3, f7: $f7, ext: Ext::$ext,
                        meaning: $meaning, example: $example } ),*
        ];
    };
}

ops! {
    // --- register-to-register arithmetic and logic (opcode 0110011) ---
    Add, "add", R, 0x33, Some(0), Some(0x00), I, "rd = rs1 + rs2", "add a0, a1, a2";
    Sub, "sub", R, 0x33, Some(0), Some(0x20), I, "rd = rs1 − rs2", "sub a0, a1, a2";
    Sll, "sll", R, 0x33, Some(1), Some(0x00), I, "rd = rs1 << rs2[4:0]", "sll a0, a1, a2";
    Slt, "slt", R, 0x33, Some(2), Some(0x00), I, "rd = (rs1 < rs2), signed", "slt a0, a1, a2";
    Sltu, "sltu", R, 0x33, Some(3), Some(0x00), I, "rd = (rs1 < rs2), unsigned", "sltu a0, a1, a2";
    Xor, "xor", R, 0x33, Some(4), Some(0x00), I, "rd = rs1 XOR rs2", "xor a0, a1, a2";
    Srl, "srl", R, 0x33, Some(5), Some(0x00), I, "rd = rs1 >> rs2[4:0] (logical)", "srl a0, a1, a2";
    Sra, "sra", R, 0x33, Some(5), Some(0x20), I, "rd = rs1 >> rs2[4:0] (arithmetic, keeps the sign)", "sra a0, a1, a2";
    Or, "or", R, 0x33, Some(6), Some(0x00), I, "rd = rs1 OR rs2", "or a0, a1, a2";
    And, "and", R, 0x33, Some(7), Some(0x00), I, "rd = rs1 AND rs2", "and a0, a1, a2";
    // --- multiplication and division (extension M) ---
    Mul, "mul", R, 0x33, Some(0), Some(0x01), M, "rd = low 32 bits of rs1 · rs2", "mul a0, a1, a2";
    Mulh, "mulh", R, 0x33, Some(1), Some(0x01), M, "rd = high 32 bits of rs1 · rs2 (both signed)", "mulh a0, a1, a2";
    Mulhsu, "mulhsu", R, 0x33, Some(2), Some(0x01), M, "rd = high 32 bits (rs1 signed, rs2 unsigned)", "mulhsu a0, a1, a2";
    Mulhu, "mulhu", R, 0x33, Some(3), Some(0x01), M, "rd = high 32 bits of rs1 · rs2 (unsigned)", "mulhu a0, a1, a2";
    Div, "div", R, 0x33, Some(4), Some(0x01), M, "rd = rs1 / rs2 (signed)", "div a0, a1, a2";
    Divu, "divu", R, 0x33, Some(5), Some(0x01), M, "rd = rs1 / rs2 (unsigned)", "divu a0, a1, a2";
    Rem, "rem", R, 0x33, Some(6), Some(0x01), M, "rd = remainder of rs1 / rs2 (signed)", "rem a0, a1, a2";
    Remu, "remu", R, 0x33, Some(7), Some(0x01), M, "rd = remainder of rs1 / rs2 (unsigned)", "remu a0, a1, a2";
    // --- with an immediate from the instruction (0010011) ---
    Addi, "addi", I, 0x13, Some(0), None, I, "rd = rs1 + imm (−2048…2047)", "addi a0, a0, -1";
    Slti, "slti", I, 0x13, Some(2), None, I, "rd = (rs1 < imm), signed", "slti a0, a1, 10";
    Sltiu, "sltiu", I, 0x13, Some(3), None, I, "rd = (rs1 < imm), unsigned", "sltiu a0, a1, 10";
    Xori, "xori", I, 0x13, Some(4), None, I, "rd = rs1 XOR imm", "xori a0, a1, -1";
    Ori, "ori", I, 0x13, Some(6), None, I, "rd = rs1 OR imm", "ori a0, a1, 0x0f";
    Andi, "andi", I, 0x13, Some(7), None, I, "rd = rs1 AND imm", "andi a0, a1, 0xff";
    Slli, "slli", SH, 0x13, Some(1), Some(0x00), I, "rd = rs1 << imm (0…31)", "slli a0, a1, 2";
    Srli, "srli", SH, 0x13, Some(5), Some(0x00), I, "rd = rs1 >> imm (logical)", "srli a0, a1, 2";
    Srai, "srai", SH, 0x13, Some(5), Some(0x20), I, "rd = rs1 >> imm (arithmetic)", "srai a0, a1, 2";
    // --- memory (0000011 / 0100011) ---
    Lb, "lb", L, 0x03, Some(0), None, I, "rd = signed byte [rs1+offset]", "lb a0, 0(a1)";
    Lh, "lh", L, 0x03, Some(1), None, I, "rd = signed halfword [rs1+offset]", "lh a0, 0(a1)";
    Lw, "lw", L, 0x03, Some(2), None, I, "rd = word [rs1+offset]", "lw a0, 4(a1)";
    Lbu, "lbu", L, 0x03, Some(4), None, I, "rd = unsigned byte [rs1+offset]", "lbu a0, 0(a1)";
    Lhu, "lhu", L, 0x03, Some(5), None, I, "rd = unsigned halfword [rs1+offset]", "lhu a0, 0(a1)";
    Sb, "sb", S, 0x23, Some(0), None, I, "byte [rs1+offset] = rs2", "sb a0, 0(a1)";
    Sh, "sh", S, 0x23, Some(1), None, I, "halfword [rs1+offset] = rs2", "sh a0, 0(a1)";
    Sw, "sw", S, 0x23, Some(2), None, I, "word [rs1+offset] = rs2", "sw a0, 4(a1)";
    // --- branches (1100011) ---
    Beq, "beq", B, 0x63, Some(0), None, I, "if rs1 = rs2, branch", "beq a0, a1, label";
    Bne, "bne", B, 0x63, Some(1), None, I, "if rs1 ≠ rs2, branch", "bne a0, a1, label";
    Blt, "blt", B, 0x63, Some(4), None, I, "if rs1 < rs2 (signed), branch", "blt a0, a1, label";
    Bge, "bge", B, 0x63, Some(5), None, I, "if rs1 ≥ rs2 (signed), branch", "bge a0, a1, label";
    Bltu, "bltu", B, 0x63, Some(6), None, I, "if rs1 < rs2 (unsigned), branch", "bltu a0, a1, label";
    Bgeu, "bgeu", B, 0x63, Some(7), None, I, "if rs1 ≥ rs2 (unsigned), branch", "bgeu a0, a1, label";
    Jal, "jal", J, 0x6f, None, None, I, "rd = pc + 4; jump to label", "jal ra, function";
    Jalr, "jalr", JR, 0x67, Some(0), None, I, "rd = pc + 4; jump to rs1 + offset", "jalr ra, 0(t0)";
    // --- long immediates and addresses ---
    Lui, "lui", U, 0x37, None, None, I, "rd = imm << 12", "lui a0, 0x12345";
    Auipc, "auipc", U, 0x17, None, None, I, "rd = pc + (imm << 12)", "auipc a0, 1";
    // --- system ---
    Ecall, "ecall", SYS, 0x73, None, None, I, "system call (number in a7)", "ecall";
    Ebreak, "ebreak", SYS, 0x73, None, None, I, "halt (breakpoint)", "ebreak";
}

impl Op {
    /// Instruction description.
    pub fn info(self) -> &'static OpInfo {
        &OPS[self as usize]
    }
    /// Mnemonic.
    pub fn mnemonic(self) -> &'static str {
        self.info().mnemonic
    }
}

/// Instruction by mnemonic (lowercase).
pub fn op_by_mnemonic(m: &str) -> Option<&'static OpInfo> {
    OPS.iter().find(|o| o.mnemonic == m)
}

/// Pseudo-instruction: example of syntax and what it expands to.
#[derive(Clone, Copy, Debug)]
pub struct Pseudo {
    /// example of syntax
    pub example: &'static str,
    /// what it expands to
    pub becomes: &'static str,
}

/// Pseudo-instructions — shorthands expanded by the assembler.
pub const PSEUDO: &[Pseudo] = &[
    Pseudo { example: "nop", becomes: "addi zero, zero, 0" },
    Pseudo { example: "li a0, 1000", becomes: i18n::t!("addi a0, zero, 1000  (large number — lui + addi)") },
    Pseudo { example: i18n::t!("la a0, label"), becomes: i18n::t!("auipc a0, … ; addi a0, a0, …  (label address)") },
    Pseudo { example: "mv a0, a1", becomes: "addi a0, a1, 0" },
    Pseudo { example: "not a0, a1", becomes: "xori a0, a1, -1" },
    Pseudo { example: "neg a0, a1", becomes: "sub a0, zero, a1" },
    Pseudo { example: "seqz a0, a1", becomes: "sltiu a0, a1, 1" },
    Pseudo { example: "snez a0, a1", becomes: "sltu a0, zero, a1" },
    Pseudo { example: i18n::t!("j label"), becomes: i18n::t!("jal zero, label") },
    Pseudo { example: i18n::t!("jal label"), becomes: i18n::t!("jal ra, label") },
    Pseudo { example: "jr a0", becomes: "jalr zero, 0(a0)" },
    Pseudo { example: "ret", becomes: "jalr zero, 0(ra)" },
    Pseudo { example: i18n::t!("call function"), becomes: "auipc ra, … ; jalr ra, …(ra)" },
    Pseudo { example: i18n::t!("beqz a0, label"), becomes: i18n::t!("beq a0, zero, label") },
    Pseudo { example: i18n::t!("bnez a0, label"), becomes: i18n::t!("bne a0, zero, label") },
    Pseudo { example: i18n::t!("blez a0, label"), becomes: i18n::t!("bge zero, a0, label") },
    Pseudo { example: i18n::t!("bgez a0, label"), becomes: i18n::t!("bge a0, zero, label") },
    Pseudo { example: i18n::t!("bltz a0, label"), becomes: i18n::t!("blt a0, zero, label") },
    Pseudo { example: i18n::t!("bgtz a0, label"), becomes: i18n::t!("blt zero, a0, label") },
    Pseudo { example: i18n::t!("bgt a0, a1, label"), becomes: i18n::t!("blt a1, a0, label") },
    Pseudo { example: i18n::t!("ble a0, a1, label"), becomes: i18n::t!("bge a1, a0, label") },
    Pseudo { example: i18n::t!("bgtu a0, a1, label"), becomes: i18n::t!("bltu a1, a0, label") },
    Pseudo { example: i18n::t!("bleu a0, a1, label"), becomes: i18n::t!("bgeu a1, a0, label") },
];

/* ============================================================
Encoding
============================================================ */

fn f3(o: &OpInfo) -> i32 {
    o.f3.unwrap_or(0) as i32
}
fn f7(o: &OpInfo) -> i32 {
    o.f7.unwrap_or(0) as i32
}

/// Format R: `op rd, rs1, rs2`.
pub fn enc_r(o: &OpInfo, rd: u8, rs1: u8, rs2: u8) -> u32 {
    ((f7(o) << 25)
        | (i32::from(rs2) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Format I: `op rd, rs1, imm`.
pub fn enc_i(o: &OpInfo, rd: u8, rs1: u8, imm: i32) -> u32 {
    (((imm & 0xfff) << 20) | (i32::from(rs1) << 15) | (f3(o) << 12) | (i32::from(rd) << 7) | o.opcode as i32) as u32
}

/// Shifts: f7 in the upper seven bits, the shift amount in the five low bits of the immediate.
pub fn enc_sh(o: &OpInfo, rd: u8, rs1: u8, shamt: i32) -> u32 {
    ((f7(o) << 25)
        | ((shamt & 31) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Format S: `op rs2, imm(rs1)`.
pub fn enc_s(o: &OpInfo, rs2: u8, rs1: u8, imm: i32) -> u32 {
    ((((imm >> 5) & 0x7f) << 25)
        | (i32::from(rs2) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | ((imm & 0x1f) << 7)
        | o.opcode as i32) as u32
}

/// Format B: `op rs1, rs2, offset`.
pub fn enc_b(o: &OpInfo, rs1: u8, rs2: u8, off: i32) -> u32 {
    ((((off >> 12) & 1) << 31)
        | (((off >> 5) & 0x3f) << 25)
        | (i32::from(rs2) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | (((off >> 1) & 0xf) << 8)
        | (((off >> 11) & 1) << 7)
        | o.opcode as i32) as u32
}

/// Format U: `op rd, imm20`.
pub fn enc_u(o: &OpInfo, rd: u8, imm20: i32) -> u32 {
    (((imm20 & 0xfffff) << 12) | (i32::from(rd) << 7) | o.opcode as i32) as u32
}

/// Format J: `jal rd, offset`.
pub fn enc_j(o: &OpInfo, rd: u8, off: i32) -> u32 {
    ((((off >> 20) & 1) << 31)
        | (((off >> 1) & 0x3ff) << 21)
        | (((off >> 11) & 1) << 20)
        | (((off >> 12) & 0xff) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Word of the `ecall` instruction.
pub const ECALL: u32 = 0x0000_0073;
/// Word of the `ebreak` instruction.
pub const EBREAK: u32 = 0x0010_0073;

/* ============================================================
Decoding
============================================================ */

/// Decoded instruction word.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Decoded {
    /// instruction word
    pub word: u32,
    /// `None` — the word is not an RV32IM instruction
    pub op: Option<Op>,
    /// destination register number
    pub rd: u8,
    /// first source register number
    pub rs1: u8,
    /// second source register number
    pub rs2: u8,
    /// signed immediate from the instruction (for U — 20 bits as is, unsigned)
    pub imm: i32,
}

/// Lookup by key "opcode|f3|f7" (−1 — the field is absent), as in the decoder table.
fn lookup(opcode: u32, f3k: i32, f7k: i32) -> Option<&'static OpInfo> {
    OPS.iter().find(|o| {
        if o.fmt == Fmt::SYS {
            return false;
        }
        let f3o = o.f3.map_or(-1, |v| v as i32);
        let f7o = if matches!(o.fmt, Fmt::R | Fmt::SH) { o.f7.map_or(-1, |v| v as i32) } else { -1 };
        o.opcode == opcode && f3o == f3k && f7o == f7k
    })
}

/// Decoding of an instruction word.
pub fn decode(word: u32) -> Decoded {
    let w = word as i32;
    let opcode = word & 0x7f;
    let f3k = (w >> 12) & 7;
    let f7k = (w >> 25) & 0x7f;
    let rd = ((w >> 7) & 31) as u8;
    let rs1 = ((w >> 15) & 31) as u8;
    let rs2 = ((w >> 20) & 31) as u8;

    let op: Option<&'static OpInfo> = if opcode == 0x73 {
        if word == ECALL {
            op_by_mnemonic("ecall")
        } else if word == EBREAK {
            op_by_mnemonic("ebreak")
        } else {
            None
        }
    } else if opcode == 0x37 || opcode == 0x17 || opcode == 0x6f {
        lookup(opcode, -1, -1)
    } else if opcode == 0x33 {
        lookup(opcode, f3k, f7k)
    } else if opcode == 0x13 {
        // ordinary instructions differ by f3, shifts also by the upper seven bits (srli and srai)
        lookup(opcode, f3k, -1).or_else(|| lookup(opcode, f3k, f7k))
    } else {
        lookup(opcode, f3k, -1)
    };

    let mut imm = 0i32;
    if let Some(o) = op {
        imm = match o.fmt {
            Fmt::I | Fmt::L | Fmt::JR => w >> 20,
            Fmt::SH => i32::from(rs2),
            Fmt::S => ((w >> 25) << 5) | ((w >> 7) & 0x1f),
            Fmt::B => {
                ((w >> 31) << 12)
                    | ((((word >> 7) & 1) as i32) << 11)
                    | ((((word >> 25) & 0x3f) as i32) << 5)
                    | ((((word >> 8) & 0xf) as i32) << 1)
            }
            Fmt::U => ((word >> 12) & 0xfffff) as i32,
            Fmt::J => {
                ((w >> 31) << 20)
                    | ((((word >> 12) & 0xff) as i32) << 12)
                    | ((((word >> 20) & 1) as i32) << 11)
                    | ((((word >> 21) & 0x3ff) as i32) << 1)
            }
            Fmt::R | Fmt::SYS => 0,
        };
    }
    Decoded { word, op: op.map(|o| o.op), rd, rs1, rs2, imm }
}

fn signed(n: i32) -> String {
    if n >= 0 {
        format!("+{n}")
    } else {
        format!("{n}")
    }
}

/// Instruction back to text (register names as in the ABI).
pub fn disassemble(word: u32) -> String {
    let d = decode(word);
    let Some(op) = d.op else {
        return format!(".word 0x{word:08x}");
    };
    let o = op.info();
    let r = reg_name;
    match o.fmt {
        Fmt::R => format!("{} {}, {}, {}", o.mnemonic, r(d.rd), r(d.rs1), r(d.rs2)),
        Fmt::I | Fmt::SH => format!("{} {}, {}, {}", o.mnemonic, r(d.rd), r(d.rs1), d.imm),
        Fmt::L => format!("{} {}, {}({})", o.mnemonic, r(d.rd), d.imm, r(d.rs1)),
        Fmt::S => format!("{} {}, {}({})", o.mnemonic, r(d.rs2), d.imm, r(d.rs1)),
        Fmt::B => format!("{} {}, {}, {}", o.mnemonic, r(d.rs1), r(d.rs2), signed(d.imm)),
        Fmt::U => format!("{} {}, 0x{:x}", o.mnemonic, r(d.rd), d.imm),
        Fmt::J => format!("jal {}, {}", r(d.rd), signed(d.imm)),
        Fmt::JR => format!("jalr {}, {}({})", r(d.rd), d.imm, r(d.rs1)),
        Fmt::SYS => o.mnemonic.to_string(),
    }
}

/* ============================================================
Splitting an instruction into fields, for the teaching listing
============================================================ */

/// Field colour in the listing (css class).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum FieldClass {
    /// opcode
    Op,
    /// upper seven bits (f7)
    F7,
    /// second source register
    Rs2,
    /// first source register
    Rs1,
    /// f3 field
    F3,
    /// destination register
    Rd,
    /// immediate from the instruction
    Imm,
}

impl FieldClass {
    /// Name of the css class.
    pub fn css(self) -> &'static str {
        match self {
            FieldClass::Op => "op",
            FieldClass::F7 => "f7",
            FieldClass::Rs2 => "rs2",
            FieldClass::Rs1 => "rs1",
            FieldClass::F3 => "f3",
            FieldClass::Rd => "rd",
            FieldClass::Imm => "imm",
        }
    }
}

/// Word format in the field-level parse.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum FieldFmt {
    /// format R: three registers
    R,
    /// format I: immediate from the instruction
    I,
    /// format S: store to memory
    S,
    /// format B: conditional branch
    B,
    /// format U: long immediate
    U,
    /// format J: `jal` jump
    J,
    /// system instruction (`ecall`, `ebreak`)
    Sys,
    /// not an instruction
    Unknown,
}

impl FieldFmt {
    /// Format letter, as in the reference.
    pub fn letter(self) -> &'static str {
        match self {
            FieldFmt::R => "R",
            FieldFmt::I => "I",
            FieldFmt::S => "S",
            FieldFmt::B => "B",
            FieldFmt::U => "U",
            FieldFmt::J => "J",
            FieldFmt::Sys => "SYS",
            FieldFmt::Unknown => "?",
        }
    }
}

/// Field of an instruction word: name, bits (string of 0 and 1, most significant first) and colour.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BitField {
    /// field name
    pub name: String,
    /// field bits: string of 0 and 1, most significant first
    pub bits: String,
    /// field colour
    pub cls: FieldClass,
}

/// Instruction word by fields.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Fields {
    /// word format in the field-level parse
    pub fmt: FieldFmt,
    /// fields of the word, from most to least significant
    pub fields: Vec<BitField>,
}

/// Bits hi…lo of the word, `hi - lo + 1` characters. For width 32 the mask is zero (as in the previous JavaScript version,
/// where `1 << 32 === 1`), so the "word" field of a non-instruction is 32 zeros.
fn bin(w: u32, hi: u32, lo: u32) -> String {
    let width = hi - lo + 1;
    let mask: u32 = if width >= 32 { 0 } else { (1u32 << width) - 1 };
    let v = (w >> lo) & mask;
    format!("{v:0width$b}", width = width as usize)
}

/// Field-level parse of an instruction word.
pub fn fields_of(word: u32) -> Fields {
    let d = decode(word);
    let f = |name: &str, hi: u32, lo: u32, cls: FieldClass| BitField {
        name: name.to_string(),
        bits: bin(word, hi, lo),
        cls,
    };
    let opcode = || f(i18n::tr("opcode field"), 6, 0, FieldClass::Op);
    let fmt = d.op.map(|o| o.info().fmt);
    match fmt {
        Some(Fmt::R) => Fields {
            fmt: FieldFmt::R,
            fields: vec![
                f("f7", 31, 25, FieldClass::F7),
                f("rs2", 24, 20, FieldClass::Rs2),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("rd", 11, 7, FieldClass::Rd),
                opcode(),
            ],
        },
        Some(Fmt::I | Fmt::L | Fmt::JR) => Fields {
            fmt: FieldFmt::I,
            fields: vec![
                f(i18n::tr("imm [11:0]"), 31, 20, FieldClass::Imm),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("rd", 11, 7, FieldClass::Rd),
                opcode(),
            ],
        },
        Some(Fmt::SH) => Fields {
            fmt: FieldFmt::I,
            fields: vec![
                f("f7", 31, 25, FieldClass::F7),
                f(i18n::tr("shift"), 24, 20, FieldClass::Imm),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("rd", 11, 7, FieldClass::Rd),
                opcode(),
            ],
        },
        Some(Fmt::S) => Fields {
            fmt: FieldFmt::S,
            fields: vec![
                f(i18n::tr("imm [11:5]"), 31, 25, FieldClass::Imm),
                f("rs2", 24, 20, FieldClass::Rs2),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f(i18n::tr("imm [4:0]"), 11, 7, FieldClass::Imm),
                opcode(),
            ],
        },
        Some(Fmt::B) => Fields {
            fmt: FieldFmt::B,
            fields: vec![
                f("[12|10:5]", 31, 25, FieldClass::Imm),
                f("rs2", 24, 20, FieldClass::Rs2),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("[4:1|11]", 11, 7, FieldClass::Imm),
                opcode(),
            ],
        },
        Some(Fmt::U) => Fields {
            fmt: FieldFmt::U,
            fields: vec![f(i18n::tr("imm [31:12]"), 31, 12, FieldClass::Imm), f("rd", 11, 7, FieldClass::Rd), opcode()],
        },
        Some(Fmt::J) => Fields {
            fmt: FieldFmt::J,
            fields: vec![f("[20|10:1|11|19:12]", 31, 12, FieldClass::Imm), f("rd", 11, 7, FieldClass::Rd), opcode()],
        },
        Some(Fmt::SYS) => {
            Fields { fmt: FieldFmt::Sys, fields: vec![f(i18n::tr("number"), 31, 7, FieldClass::Imm), opcode()] }
        }
        None => Fields { fmt: FieldFmt::Unknown, fields: vec![f(i18n::tr("word"), 31, 0, FieldClass::Imm)] },
    }
}
