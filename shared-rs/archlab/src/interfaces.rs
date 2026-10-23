//! Типы интерфейсов блоков. Порт блока — не один бит, а именованный набор бит с полями: так выходы
//! одного блока подключаются ко входам другого одним проводом. Типы совместимы только по ИМЕНИ:
//! `Addr2` и `Word2` оба из двух бит, но это разные вещи — между ними нужен явный переходник.
//! Порт `interfaces.ts`.

use crate::model::NodeValue;
use serde::{Deserialize, Serialize};

/// Тип интерфейса порта (конечный набор).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Iface {
    Bit,
    Clk,
    Word2,
    Addr2,
    Op2,
    Instr,
    Flags,
    Ctl,
    Phases,
    // процессор «Мини-8»
    Byte,
    Reg3,
    Op4,
    Imm6,
    Instr16,
    Oh8,
    Ctrl,
}

/// Поле составного типа: имя и тип.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Field {
    pub name: &'static str,
    pub ty: Iface,
}

const fn bit(name: &'static str) -> Field {
    Field { name, ty: Iface::Bit }
}
const fn sub(name: &'static str, ty: Iface) -> Field {
    Field { name, ty }
}

const WORD2: [Field; 2] = [bit("D1"), bit("D0")];
const ADDR2: [Field; 2] = [bit("A1"), bit("A0")];
const OP2: [Field; 2] = [bit("Op1"), bit("Op0")];
const INSTR: [Field; 2] = [sub("op", Iface::Op2), sub("k", Iface::Word2)];
const FLAGS: [Field; 3] = [bit("Z"), bit("N"), bit("Pe")];
const CTL: [Field; 5] = [bit("AccLoad"), bit("UseAdd"), bit("Take"), bit("PcLoad"), bit("Stop")];
const PHASES: [Field; 4] = [bit("Fe"), bit("De"), bit("Ex"), bit("Wb")];
const BYTE: [Field; 8] = [bit("B7"), bit("B6"), bit("B5"), bit("B4"), bit("B3"), bit("B2"), bit("B1"), bit("B0")];
const REG3: [Field; 3] = [bit("R2"), bit("R1"), bit("R0")];
const OP4: [Field; 4] = [bit("O3"), bit("O2"), bit("O1"), bit("O0")];
const IMM6: [Field; 6] = [bit("I5"), bit("I4"), bit("I3"), bit("I2"), bit("I1"), bit("I0")];
const INSTR16: [Field; 4] = [
    sub("op", Iface::Op4),
    sub("a", Iface::Reg3),
    sub("b", Iface::Reg3),
    sub("c", Iface::Imm6),
];
const OH8: [Field; 8] = [bit("H7"), bit("H6"), bit("H5"), bit("H4"), bit("H3"), bit("H2"), bit("H1"), bit("H0")];
const CTRL: [Field; 18] = [
    bit("regWrite"),
    bit("selAdd"),
    bit("selAnd"),
    bit("selOr"),
    bit("selXor"),
    bit("selB"),
    bit("sub"),
    bit("useImm6"),
    bit("useImm8"),
    bit("load"),
    bit("store"),
    bit("isBeq"),
    bit("isBne"),
    bit("isBltu"),
    bit("isBgeu"),
    bit("isJmp"),
    bit("isHlt"),
    bit("isR"),
];

impl Iface {
    /// Имя типа.
    pub fn name(self) -> &'static str {
        match self {
            Iface::Bit => "Bit",
            Iface::Clk => "Clk",
            Iface::Word2 => "Word2",
            Iface::Addr2 => "Addr2",
            Iface::Op2 => "Op2",
            Iface::Instr => "Instr",
            Iface::Flags => "Flags",
            Iface::Ctl => "Ctl",
            Iface::Phases => "Phases",
            Iface::Byte => "Byte",
            Iface::Reg3 => "Reg3",
            Iface::Op4 => "Op4",
            Iface::Imm6 => "Imm6",
            Iface::Instr16 => "Instr16",
            Iface::Oh8 => "Oh8",
            Iface::Ctrl => "Ctrl",
        }
    }

    /// Короткое пояснение для подсказок на доске.
    pub fn title(self) -> &'static str {
        match self {
            Iface::Bit => "один бит",
            Iface::Clk => "такт",
            Iface::Word2 => "двухбитное слово",
            Iface::Addr2 => "двухбитный адрес",
            Iface::Op2 => "код операции",
            Iface::Instr => "команда: код операции и операнд",
            Iface::Flags => "флаги результата",
            Iface::Ctl => "управляющие сигналы",
            Iface::Phases => "фазы такта",
            Iface::Byte => "байт (8 бит)",
            Iface::Reg3 => "номер регистра (3 бита)",
            Iface::Op4 => "код операции (4 бита)",
            Iface::Imm6 => "число из команды (6 бит)",
            Iface::Instr16 => "команда (16 бит)",
            Iface::Oh8 => "один из восьми",
            Iface::Ctrl => "сигналы управления процессора",
        }
    }

    /// Поля по порядку: старшее — первое. У простых типов (`Bit`, `Clk`) полей нет — это один бит.
    pub fn fields(self) -> &'static [Field] {
        match self {
            Iface::Bit | Iface::Clk => &[],
            Iface::Word2 => &WORD2,
            Iface::Addr2 => &ADDR2,
            Iface::Op2 => &OP2,
            Iface::Instr => &INSTR,
            Iface::Flags => &FLAGS,
            Iface::Ctl => &CTL,
            Iface::Phases => &PHASES,
            Iface::Byte => &BYTE,
            Iface::Reg3 => &REG3,
            Iface::Op4 => &OP4,
            Iface::Imm6 => &IMM6,
            Iface::Instr16 => &INSTR16,
            Iface::Oh8 => &OH8,
            Iface::Ctrl => &CTRL,
        }
    }

    /// Простой тип — один бит.
    pub fn is_simple(self) -> bool {
        self.fields().is_empty()
    }

    /// Сколько бит в типе.
    pub fn width(self) -> usize {
        if self.is_simple() {
            1
        } else {
            self.fields().iter().map(|f| f.ty.width()).sum()
        }
    }

    /// Разбор имени типа.
    pub fn parse(name: &str) -> Option<Iface> {
        ALL.iter().copied().find(|t| t.name() == name)
    }
}

/// Все типы интерфейсов.
pub const ALL: [Iface; 16] = [
    Iface::Bit,
    Iface::Clk,
    Iface::Word2,
    Iface::Addr2,
    Iface::Op2,
    Iface::Instr,
    Iface::Flags,
    Iface::Ctl,
    Iface::Phases,
    Iface::Byte,
    Iface::Reg3,
    Iface::Op4,
    Iface::Imm6,
    Iface::Instr16,
    Iface::Oh8,
    Iface::Ctrl,
];

/// Пути всех бит типа по порядку: у `Instr` — `op.Op1, op.Op0, k.D1, k.D0`; у простого типа — `[""]`.
pub fn leaf_paths(ty: Iface, prefix: &str) -> Vec<String> {
    if ty.is_simple() {
        return vec![prefix.to_string()];
    }
    ty.fields()
        .iter()
        .flat_map(|f| {
            let p = if prefix.is_empty() { f.name.to_string() } else { format!("{prefix}.{}", f.name) };
            leaf_paths(f.ty, &p)
        })
        .collect()
}

/// Часть типа: какой тип, с какого бита и сколько бит.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TypeSlice {
    pub ty: Iface,
    pub offset: usize,
    pub length: usize,
}

/// Ищет поле по пути (`""` — весь тип, `"op"`, `"k.D1"`); `None`, если такого поля нет.
pub fn slice_of(ty: Iface, path: &str) -> Option<TypeSlice> {
    let mut cur = ty;
    let mut offset = 0;
    if !path.is_empty() {
        for segment in path.split('.') {
            let mut found = false;
            for f in cur.fields() {
                if f.name == segment {
                    cur = f.ty;
                    found = true;
                    break;
                }
                offset += f.ty.width();
            }
            if !found {
                return None;
            }
        }
    }
    Some(TypeSlice { ty: cur, offset, length: cur.width() })
}

/// Непосредственное поле типа — для раскрытия порта на доске.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChildField {
    pub name: &'static str,
    pub path: String,
    pub ty: Iface,
}

/// Непосредственные поля типа по пути.
pub fn child_fields(ty: Iface, path: &str) -> Vec<ChildField> {
    let Some(slice) = slice_of(ty, path) else {
        return Vec::new();
    };
    slice
        .ty
        .fields()
        .iter()
        .map(|f| ChildField {
            name: f.name,
            path: if path.is_empty() { f.name.to_string() } else { format!("{path}.{}", f.name) },
            ty: f.ty,
        })
        .collect()
}

/// Типы совместимы только при совпадении имён.
pub fn can_connect(from: Iface, to: Iface) -> bool {
    from == to
}

/// Значение шины текстом: `10`, `1?` (старший бит слева).
pub fn bus_text(values: &[NodeValue]) -> String {
    values.iter().map(|v| v.map_or('?', |b| if b == 1 { '1' } else { '0' })).collect()
}
