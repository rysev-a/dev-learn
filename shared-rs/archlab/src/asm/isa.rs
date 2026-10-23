//! Набор команд «Мини-8»: 8-битные данные, 8 регистров, команда — 16 бит.
//!
//! ```text
//!   15..12   11..9   8..6   5..0
//!   опкод      A      B      C
//! ```
//!
//! Поля A, B, C трактуются по-разному в зависимости от формата команды. Порт `isa.ts`.

pub const REG_COUNT: usize = 8;
pub const MEM_SIZE: usize = 256;
pub const PROGRAM_MAX: usize = 256;

/// Формат команды.
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
    /// `beq ra, rb, метка`
    Branch,
    /// `jmp метка`
    Jump,
}

/// Описание команды.
#[derive(Debug, Clone, Copy)]
pub struct OpDef {
    pub mnemonic: &'static str,
    pub opcode: u16,
    pub format: Format,
    /// Что делает — одной строкой.
    pub meaning: &'static str,
    pub example: &'static str,
}

const fn op(mnemonic: &'static str, opcode: u16, format: Format, meaning: &'static str, example: &'static str) -> OpDef {
    OpDef { mnemonic, opcode, format, meaning, example }
}

/// Все команды.
pub const OPS: [OpDef; 15] = [
    op("hlt", 0x0, Format::None, "остановить процессор", "hlt"),
    op("li", 0x1, Format::Li, "rd = число (0…255)", "li r1, 72"),
    op("add", 0x2, Format::R, "rd = rs + rt", "add r1, r2, r3"),
    op("sub", 0x3, Format::R, "rd = rs − rt", "sub r1, r2, r3"),
    op("and", 0x4, Format::R, "rd = rs И rt (побитово)", "and r1, r2, r3"),
    op("or", 0x5, Format::R, "rd = rs ИЛИ rt (побитово)", "or r1, r2, r3"),
    op("xor", 0x6, Format::R, "rd = rs XOR rt (побитово)", "xor r1, r2, r3"),
    op("addi", 0x7, Format::I, "rd = rs + число (−32…31)", "addi r1, r1, 1"),
    op("lb", 0x8, Format::Mem, "rd = байт из памяти [rs + смещение]", "lb r1, 0(r2)"),
    op("sb", 0x9, Format::Mem, "память [rs + смещение] = rd", "sb r1, 0(r2)"),
    op("beq", 0xa, Format::Branch, "если ra = rb — перейти на метку", "beq r1, r2, конец"),
    op("bne", 0xb, Format::Branch, "если ra ≠ rb — перейти на метку", "bne r1, r2, цикл"),
    op("bltu", 0xc, Format::Branch, "если ra < rb (без знака) — перейти", "bltu r1, r2, дальше"),
    op("bgeu", 0xd, Format::Branch, "если ra ≥ rb (без знака) — перейти", "bgeu r1, r2, дальше"),
    op("jmp", 0xe, Format::Jump, "безусловный переход на метку", "jmp цикл"),
];

/// Псевдокоманда: сокращение, которое ассемблер сам заменяет настоящей.
#[derive(Debug, Clone, Copy)]
pub struct Pseudo {
    pub name: &'static str,
    pub example: &'static str,
    pub becomes: &'static str,
}

/// Все псевдокоманды.
pub const PSEUDO: [Pseudo; 9] = [
    Pseudo { name: "nop", example: "nop", becomes: "addi r0, r0, 0" },
    Pseudo { name: "mv", example: "mv r1, r2", becomes: "addi r1, r2, 0" },
    Pseudo { name: "inc", example: "inc r1", becomes: "addi r1, r1, 1" },
    Pseudo { name: "dec", example: "dec r1", becomes: "addi r1, r1, -1" },
    Pseudo { name: "beqz", example: "beqz r1, метка", becomes: "beq r1, r0, метка" },
    Pseudo { name: "bnez", example: "bnez r1, метка", becomes: "bne r1, r0, метка" },
    Pseudo { name: "bgtu", example: "bgtu r1, r2, метка", becomes: "bltu r2, r1, метка" },
    Pseudo { name: "bleu", example: "bleu r1, r2, метка", becomes: "bgeu r2, r1, метка" },
    Pseudo { name: "j", example: "j метка", becomes: "jmp метка" },
];

/// Команда по мнемонике.
pub fn op_by_mnemonic(m: &str) -> Option<&'static OpDef> {
    OPS.iter().find(|o| o.mnemonic == m)
}

/// Команда по коду операции.
pub fn op_by_opcode(c: u16) -> Option<&'static OpDef> {
    OPS.iter().find(|o| o.opcode == c)
}

/// Число из `bits` бит → со знаком.
pub fn to_signed(value: i32, bits: u32) -> i32 {
    let mask = (1i32 << bits) - 1;
    let v = value & mask;
    if v & (1 << (bits - 1)) != 0 {
        v - (1 << bits)
    } else {
        v
    }
}

/// Собрать слово из полей.
pub fn pack(opcode: u16, a: u16, b: u16, c: i32) -> u16 {
    ((opcode & 0xf) << 12) | ((a & 7) << 9) | ((b & 7) << 6) | (c as u16 & 0x3f)
}

/// Слово команды, разобранное по полям.
#[derive(Debug, Clone, Copy)]
pub struct Decoded {
    pub word: u16,
    pub opcode: u16,
    pub a: u16,
    pub b: u16,
    pub c: u16,
    pub def: Option<&'static OpDef>,
}

/// Разобрать слово.
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

/// Команда обратно в текст — для списка машинного кода.
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

/// Двоичная запись слова по полям — для «как устроена команда».
pub fn fields(word: u16) -> (String, String, String, String) {
    let d = decode(word);
    (format!("{:04b}", d.opcode), format!("{:03b}", d.a), format!("{:03b}", d.b), format!("{:06b}", d.c))
}
