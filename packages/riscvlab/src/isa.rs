//! RISC-V RV32IM: настоящие 32-битные команды.
//! Кодирование — по спецификации «RISC-V Unprivileged ISA» (форматы R, I, S, B, U, J).

use serde::{Deserialize, Serialize};

/// ABI-имена регистров x0…x31.
pub const ABI_NAMES: [&str; 32] = [
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2",
    "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
];

/// Номер регистра по имени: x5, t0, fp…
pub fn reg_num(name: &str) -> Option<u8> {
    let n = crate::js::trim(name).to_lowercase();
    if let Some(d) = n.strip_prefix('x') {
        // x0…x31 без ведущих нулей
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

/// ABI-имя регистра по номеру.
pub fn reg_name(n: u8) -> &'static str {
    ABI_NAMES.get(usize::from(n)).copied().unwrap_or("?")
}

/// Формат команды.
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
pub enum Fmt {
    /// формат R: три регистра
    R,
    /// формат I: число из команды
    I,
    /// сдвиги на число: старшие семь бит — f7
    SH,
    /// загрузка из памяти (формат I)
    L,
    /// формат S: запись в память
    S,
    /// формат B: условный переход
    B,
    /// формат U: длинное число
    U,
    /// формат J: переход `jal`
    J,
    /// jalr
    JR,
    /// ecall, ebreak
    SYS,
}

/// Расширение набора команд.
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
pub enum Ext {
    /// базовый набор
    I,
    /// умножение и деление
    M,
}

/// Описание одной команды.
#[derive(Clone, Copy, Debug)]
pub struct OpInfo {
    /// команда
    pub op: Op,
    /// мнемоника (строчными буквами)
    pub mnemonic: &'static str,
    /// формат команды
    pub fmt: Fmt,
    /// код операции (младшие 7 бит слова)
    pub opcode: u32,
    /// поле f3, если есть
    pub f3: Option<u32>,
    /// поле f7, если есть
    pub f7: Option<u32>,
    /// расширение набора команд
    pub ext: Ext,
    /// что делает (для справочника)
    pub meaning: &'static str,
    /// пример записи
    pub example: &'static str,
}

macro_rules! ops {
    ($( $v:ident, $name:literal, $fmt:ident, $opc:expr, $f3:expr, $f7:expr, $ext:ident, $meaning:literal, $example:literal; )*) => {
        /// Команды RV32IM.
        #[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Serialize, Deserialize)]
        #[serde(rename_all = "lowercase")]
        pub enum Op { $( #[doc = concat!("`", $name, "`: ", $meaning)] $v ),* }

        /// Таблица команд (порядок — как в справочнике; индекс совпадает с номером варианта `Op`).
        pub const OPS: &[OpInfo] = &[
            $( OpInfo { op: Op::$v, mnemonic: $name, fmt: Fmt::$fmt, opcode: $opc, f3: $f3, f7: $f7, ext: Ext::$ext,
                        meaning: $meaning, example: $example } ),*
        ];
    };
}

ops! {
    // --- арифметика и логика между регистрами (opcode 0110011) ---
    Add, "add", R, 0x33, Some(0), Some(0x00), I, "rd = rs1 + rs2", "add a0, a1, a2";
    Sub, "sub", R, 0x33, Some(0), Some(0x20), I, "rd = rs1 − rs2", "sub a0, a1, a2";
    Sll, "sll", R, 0x33, Some(1), Some(0x00), I, "rd = rs1 << rs2[4:0]", "sll a0, a1, a2";
    Slt, "slt", R, 0x33, Some(2), Some(0x00), I, "rd = (rs1 < rs2) со знаком", "slt a0, a1, a2";
    Sltu, "sltu", R, 0x33, Some(3), Some(0x00), I, "rd = (rs1 < rs2) без знака", "sltu a0, a1, a2";
    Xor, "xor", R, 0x33, Some(4), Some(0x00), I, "rd = rs1 XOR rs2", "xor a0, a1, a2";
    Srl, "srl", R, 0x33, Some(5), Some(0x00), I, "rd = rs1 >> rs2[4:0] (логически)", "srl a0, a1, a2";
    Sra, "sra", R, 0x33, Some(5), Some(0x20), I, "rd = rs1 >> rs2[4:0] (с сохранением знака)", "sra a0, a1, a2";
    Or, "or", R, 0x33, Some(6), Some(0x00), I, "rd = rs1 ИЛИ rs2", "or a0, a1, a2";
    And, "and", R, 0x33, Some(7), Some(0x00), I, "rd = rs1 И rs2", "and a0, a1, a2";
    // --- умножение и деление (расширение M) ---
    Mul, "mul", R, 0x33, Some(0), Some(0x01), M, "rd = младшие 32 бита rs1 · rs2", "mul a0, a1, a2";
    Mulh, "mulh", R, 0x33, Some(1), Some(0x01), M, "rd = старшие 32 бита rs1 · rs2 (оба со знаком)", "mulh a0, a1, a2";
    Mulhsu, "mulhsu", R, 0x33, Some(2), Some(0x01), M, "rd = старшие 32 бита (rs1 со знаком, rs2 без)", "mulhsu a0, a1, a2";
    Mulhu, "mulhu", R, 0x33, Some(3), Some(0x01), M, "rd = старшие 32 бита rs1 · rs2 (без знака)", "mulhu a0, a1, a2";
    Div, "div", R, 0x33, Some(4), Some(0x01), M, "rd = rs1 / rs2 (со знаком)", "div a0, a1, a2";
    Divu, "divu", R, 0x33, Some(5), Some(0x01), M, "rd = rs1 / rs2 (без знака)", "divu a0, a1, a2";
    Rem, "rem", R, 0x33, Some(6), Some(0x01), M, "rd = остаток rs1 / rs2 (со знаком)", "rem a0, a1, a2";
    Remu, "remu", R, 0x33, Some(7), Some(0x01), M, "rd = остаток rs1 / rs2 (без знака)", "remu a0, a1, a2";
    // --- с числом из команды (0010011) ---
    Addi, "addi", I, 0x13, Some(0), None, I, "rd = rs1 + число (−2048…2047)", "addi a0, a0, -1";
    Slti, "slti", I, 0x13, Some(2), None, I, "rd = (rs1 < число) со знаком", "slti a0, a1, 10";
    Sltiu, "sltiu", I, 0x13, Some(3), None, I, "rd = (rs1 < число) без знака", "sltiu a0, a1, 10";
    Xori, "xori", I, 0x13, Some(4), None, I, "rd = rs1 XOR число", "xori a0, a1, -1";
    Ori, "ori", I, 0x13, Some(6), None, I, "rd = rs1 ИЛИ число", "ori a0, a1, 0x0f";
    Andi, "andi", I, 0x13, Some(7), None, I, "rd = rs1 И число", "andi a0, a1, 0xff";
    Slli, "slli", SH, 0x13, Some(1), Some(0x00), I, "rd = rs1 << число (0…31)", "slli a0, a1, 2";
    Srli, "srli", SH, 0x13, Some(5), Some(0x00), I, "rd = rs1 >> число (логически)", "srli a0, a1, 2";
    Srai, "srai", SH, 0x13, Some(5), Some(0x20), I, "rd = rs1 >> число (со знаком)", "srai a0, a1, 2";
    // --- память (0000011 / 0100011) ---
    Lb, "lb", L, 0x03, Some(0), None, I, "rd = байт [rs1+смещение] со знаком", "lb a0, 0(a1)";
    Lh, "lh", L, 0x03, Some(1), None, I, "rd = полуслово [rs1+смещение] со знаком", "lh a0, 0(a1)";
    Lw, "lw", L, 0x03, Some(2), None, I, "rd = слово [rs1+смещение]", "lw a0, 4(a1)";
    Lbu, "lbu", L, 0x03, Some(4), None, I, "rd = байт [rs1+смещение] без знака", "lbu a0, 0(a1)";
    Lhu, "lhu", L, 0x03, Some(5), None, I, "rd = полуслово [rs1+смещение] без знака", "lhu a0, 0(a1)";
    Sb, "sb", S, 0x23, Some(0), None, I, "байт [rs1+смещение] = rs2", "sb a0, 0(a1)";
    Sh, "sh", S, 0x23, Some(1), None, I, "полуслово [rs1+смещение] = rs2", "sh a0, 0(a1)";
    Sw, "sw", S, 0x23, Some(2), None, I, "слово [rs1+смещение] = rs2", "sw a0, 4(a1)";
    // --- переходы (1100011) ---
    Beq, "beq", B, 0x63, Some(0), None, I, "если rs1 = rs2 — перейти", "beq a0, a1, метка";
    Bne, "bne", B, 0x63, Some(1), None, I, "если rs1 ≠ rs2 — перейти", "bne a0, a1, метка";
    Blt, "blt", B, 0x63, Some(4), None, I, "если rs1 < rs2 (со знаком) — перейти", "blt a0, a1, метка";
    Bge, "bge", B, 0x63, Some(5), None, I, "если rs1 ≥ rs2 (со знаком) — перейти", "bge a0, a1, метка";
    Bltu, "bltu", B, 0x63, Some(6), None, I, "если rs1 < rs2 (без знака) — перейти", "bltu a0, a1, метка";
    Bgeu, "bgeu", B, 0x63, Some(7), None, I, "если rs1 ≥ rs2 (без знака) — перейти", "bgeu a0, a1, метка";
    Jal, "jal", J, 0x6f, None, None, I, "rd = pc + 4; перейти на метку", "jal ra, функция";
    Jalr, "jalr", JR, 0x67, Some(0), None, I, "rd = pc + 4; перейти на rs1 + смещение", "jalr ra, 0(t0)";
    // --- длинные числа и адреса ---
    Lui, "lui", U, 0x37, None, None, I, "rd = число << 12", "lui a0, 0x12345";
    Auipc, "auipc", U, 0x17, None, None, I, "rd = pc + (число << 12)", "auipc a0, 1";
    // --- система ---
    Ecall, "ecall", SYS, 0x73, None, None, I, "вызов системы (номер в a7)", "ecall";
    Ebreak, "ebreak", SYS, 0x73, None, None, I, "остановка (точка останова)", "ebreak";
}

impl Op {
    /// Описание команды.
    pub fn info(self) -> &'static OpInfo {
        &OPS[self as usize]
    }
    /// Мнемоника.
    pub fn mnemonic(self) -> &'static str {
        self.info().mnemonic
    }
}

/// Команда по мнемонике (строчными буквами).
pub fn op_by_mnemonic(m: &str) -> Option<&'static OpInfo> {
    OPS.iter().find(|o| o.mnemonic == m)
}

/// Псевдокоманда: пример записи и во что она разворачивается.
#[derive(Clone, Copy, Debug)]
pub struct Pseudo {
    /// пример записи
    pub example: &'static str,
    /// во что разворачивается
    pub becomes: &'static str,
}

/// Псевдокоманды — сокращения, которые разворачивает ассемблер.
pub const PSEUDO: &[Pseudo] = &[
    Pseudo { example: "nop", becomes: "addi zero, zero, 0" },
    Pseudo { example: "li a0, 1000", becomes: "addi a0, zero, 1000  (длинное число — lui + addi)" },
    Pseudo { example: "la a0, метка", becomes: "auipc a0, … ; addi a0, a0, …  (адрес метки)" },
    Pseudo { example: "mv a0, a1", becomes: "addi a0, a1, 0" },
    Pseudo { example: "not a0, a1", becomes: "xori a0, a1, -1" },
    Pseudo { example: "neg a0, a1", becomes: "sub a0, zero, a1" },
    Pseudo { example: "seqz a0, a1", becomes: "sltiu a0, a1, 1" },
    Pseudo { example: "snez a0, a1", becomes: "sltu a0, zero, a1" },
    Pseudo { example: "j метка", becomes: "jal zero, метка" },
    Pseudo { example: "jal метка", becomes: "jal ra, метка" },
    Pseudo { example: "jr a0", becomes: "jalr zero, 0(a0)" },
    Pseudo { example: "ret", becomes: "jalr zero, 0(ra)" },
    Pseudo { example: "call функция", becomes: "auipc ra, … ; jalr ra, …(ra)" },
    Pseudo { example: "beqz a0, метка", becomes: "beq a0, zero, метка" },
    Pseudo { example: "bnez a0, метка", becomes: "bne a0, zero, метка" },
    Pseudo { example: "blez a0, метка", becomes: "bge zero, a0, метка" },
    Pseudo { example: "bgez a0, метка", becomes: "bge a0, zero, метка" },
    Pseudo { example: "bltz a0, метка", becomes: "blt a0, zero, метка" },
    Pseudo { example: "bgtz a0, метка", becomes: "blt zero, a0, метка" },
    Pseudo { example: "bgt a0, a1, метка", becomes: "blt a1, a0, метка" },
    Pseudo { example: "ble a0, a1, метка", becomes: "bge a1, a0, метка" },
    Pseudo { example: "bgtu a0, a1, метка", becomes: "bltu a1, a0, метка" },
    Pseudo { example: "bleu a0, a1, метка", becomes: "bgeu a1, a0, метка" },
];

/* ============================================================
Кодирование
============================================================ */

fn f3(o: &OpInfo) -> i32 {
    o.f3.unwrap_or(0) as i32
}
fn f7(o: &OpInfo) -> i32 {
    o.f7.unwrap_or(0) as i32
}

/// Формат R: `op rd, rs1, rs2`.
pub fn enc_r(o: &OpInfo, rd: u8, rs1: u8, rs2: u8) -> u32 {
    ((f7(o) << 25)
        | (i32::from(rs2) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Формат I: `op rd, rs1, число`.
pub fn enc_i(o: &OpInfo, rd: u8, rs1: u8, imm: i32) -> u32 {
    (((imm & 0xfff) << 20) | (i32::from(rs1) << 15) | (f3(o) << 12) | (i32::from(rd) << 7) | o.opcode as i32) as u32
}

/// Сдвиги: в старших семи битах — f7, в пяти младших полях числа — величина сдвига.
pub fn enc_sh(o: &OpInfo, rd: u8, rs1: u8, shamt: i32) -> u32 {
    ((f7(o) << 25)
        | ((shamt & 31) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Формат S: `op rs2, число(rs1)`.
pub fn enc_s(o: &OpInfo, rs2: u8, rs1: u8, imm: i32) -> u32 {
    ((((imm >> 5) & 0x7f) << 25)
        | (i32::from(rs2) << 20)
        | (i32::from(rs1) << 15)
        | (f3(o) << 12)
        | ((imm & 0x1f) << 7)
        | o.opcode as i32) as u32
}

/// Формат B: `op rs1, rs2, смещение`.
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

/// Формат U: `op rd, число20`.
pub fn enc_u(o: &OpInfo, rd: u8, imm20: i32) -> u32 {
    (((imm20 & 0xfffff) << 12) | (i32::from(rd) << 7) | o.opcode as i32) as u32
}

/// Формат J: `jal rd, смещение`.
pub fn enc_j(o: &OpInfo, rd: u8, off: i32) -> u32 {
    ((((off >> 20) & 1) << 31)
        | (((off >> 1) & 0x3ff) << 21)
        | (((off >> 11) & 1) << 20)
        | (((off >> 12) & 0xff) << 12)
        | (i32::from(rd) << 7)
        | o.opcode as i32) as u32
}

/// Слово команды `ecall`.
pub const ECALL: u32 = 0x0000_0073;
/// Слово команды `ebreak`.
pub const EBREAK: u32 = 0x0010_0073;

/* ============================================================
Декодирование
============================================================ */

/// Разобранное слово команды.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Decoded {
    /// слово команды
    pub word: u32,
    /// `None` — слово не является командой RV32IM
    pub op: Option<Op>,
    /// номер регистра-приёмника
    pub rd: u8,
    /// номер первого регистра-источника
    pub rs1: u8,
    /// номер второго регистра-источника
    pub rs2: u8,
    /// число из команды со знаком (для U — 20 бит как есть, без знака)
    pub imm: i32,
}

/// Поиск по ключу «код|f3|f7» (−1 — поля нет), как в таблице декодера.
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

/// Разбор слова команды.
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
        // обычные команды различаются по f3, сдвиги — ещё и по старшим семи битам (srli и srai)
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

/// Команда обратно в текст (имена регистров — как в ABI).
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
Разбор команды по полям — для учебного списка
============================================================ */

/// Цвет поля в листинге (css-класс).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum FieldClass {
    /// код операции
    Op,
    /// старшие семь бит (f7)
    F7,
    /// второй регистр-источник
    Rs2,
    /// первый регистр-источник
    Rs1,
    /// поле f3
    F3,
    /// регистр-приёмник
    Rd,
    /// число из команды
    Imm,
}

impl FieldClass {
    /// Имя css-класса.
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

/// Формат слова при разборе по полям.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum FieldFmt {
    /// формат R: три регистра
    R,
    /// формат I: число из команды
    I,
    /// формат S: запись в память
    S,
    /// формат B: условный переход
    B,
    /// формат U: длинное число
    U,
    /// формат J: переход `jal`
    J,
    /// системная команда (`ecall`, `ebreak`)
    Sys,
    /// не команда
    Unknown,
}

impl FieldFmt {
    /// Буква формата, как в справочнике.
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

/// Поле слова команды: название, биты (строка из 0 и 1, старший слева) и цвет.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BitField {
    /// название поля
    pub name: String,
    /// биты поля: строка из 0 и 1, старший слева
    pub bits: String,
    /// цвет поля
    pub cls: FieldClass,
}

/// Слово команды по полям.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Fields {
    /// формат слова при разборе по полям
    pub fmt: FieldFmt,
    /// поля слова, от старшего к младшему
    pub fields: Vec<BitField>,
}

/// Биты hi…lo слова, `hi - lo + 1` символов. Для ширины 32 маска нулевая (как в прежней версии на JavaScript,
/// где `1 << 32 === 1`), поэтому поле «слово» у не-команды — 32 нуля.
fn bin(w: u32, hi: u32, lo: u32) -> String {
    let width = hi - lo + 1;
    let mask: u32 = if width >= 32 { 0 } else { (1u32 << width) - 1 };
    let v = (w >> lo) & mask;
    format!("{v:0width$b}", width = width as usize)
}

/// Разбор слова команды по полям.
pub fn fields_of(word: u32) -> Fields {
    let d = decode(word);
    let f = |name: &str, hi: u32, lo: u32, cls: FieldClass| BitField {
        name: name.to_string(),
        bits: bin(word, hi, lo),
        cls,
    };
    let opcode = || f("код", 6, 0, FieldClass::Op);
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
                f("число [11:0]", 31, 20, FieldClass::Imm),
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
                f("сдвиг", 24, 20, FieldClass::Imm),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("rd", 11, 7, FieldClass::Rd),
                opcode(),
            ],
        },
        Some(Fmt::S) => Fields {
            fmt: FieldFmt::S,
            fields: vec![
                f("число [11:5]", 31, 25, FieldClass::Imm),
                f("rs2", 24, 20, FieldClass::Rs2),
                f("rs1", 19, 15, FieldClass::Rs1),
                f("f3", 14, 12, FieldClass::F3),
                f("число [4:0]", 11, 7, FieldClass::Imm),
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
            fields: vec![f("число [31:12]", 31, 12, FieldClass::Imm), f("rd", 11, 7, FieldClass::Rd), opcode()],
        },
        Some(Fmt::J) => Fields {
            fmt: FieldFmt::J,
            fields: vec![f("[20|10:1|11|19:12]", 31, 12, FieldClass::Imm), f("rd", 11, 7, FieldClass::Rd), opcode()],
        },
        Some(Fmt::SYS) => {
            Fields { fmt: FieldFmt::Sys, fields: vec![f("номер", 31, 7, FieldClass::Imm), opcode()] }
        }
        None => Fields { fmt: FieldFmt::Unknown, fields: vec![f("слово", 31, 0, FieldClass::Imm)] },
    }
}
