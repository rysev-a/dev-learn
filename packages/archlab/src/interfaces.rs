//! Block interface types. A block port is not a single bit but a named set of bits with fields: this is how the outputs
//! of one block connect to the inputs of another with a single wire. Types are compatible by NAME only:
//! `Addr2` and `Word2` are both two bits, but they are different things — an explicit adapter is needed between them.
//! Port of `interfaces.ts`.

use crate::model::NodeValue;
use serde::{Deserialize, Serialize};

/// Port interface type (a finite set).
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
    // the "Mini-8" processor
    Byte,
    Reg3,
    Op4,
    Imm6,
    Instr16,
    Oh8,
    Ctrl,
}

/// Field of a composite type: name and type.
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
    /// Type name.
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

    /// Short explanation for hints on the board.
    pub fn title(self) -> &'static str {
        match self {
            Iface::Bit => i18n::tr("single bit"),
            Iface::Clk => i18n::tr("clock"),
            Iface::Word2 => i18n::tr("two-bit word"),
            Iface::Addr2 => i18n::tr("two-bit address"),
            Iface::Op2 => i18n::tr("opcode"),
            Iface::Instr => i18n::tr("instruction: opcode and operand"),
            Iface::Flags => i18n::tr("result flags"),
            Iface::Ctl => i18n::tr("control signals"),
            Iface::Phases => i18n::tr("clock phases"),
            Iface::Byte => i18n::tr("byte (8 bits)"),
            Iface::Reg3 => i18n::tr("register number (3 bits)"),
            Iface::Op4 => i18n::tr("opcode (4 bits)"),
            Iface::Imm6 => i18n::tr("immediate from instruction (6 bits)"),
            Iface::Instr16 => i18n::tr("instruction (16 bits)"),
            Iface::Oh8 => i18n::tr("one of eight"),
            Iface::Ctrl => i18n::tr("processor control signals"),
        }
    }

    /// Fields in order: most significant first. Simple types (`Bit`, `Clk`) have no fields — they are a single bit.
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

    /// Simple type — a single bit.
    pub fn is_simple(self) -> bool {
        self.fields().is_empty()
    }

    /// How many bits the type has.
    pub fn width(self) -> usize {
        if self.is_simple() {
            1
        } else {
            self.fields().iter().map(|f| f.ty.width()).sum()
        }
    }

    /// Parse a type name.
    pub fn parse(name: &str) -> Option<Iface> {
        ALL.iter().copied().find(|t| t.name() == name)
    }
}

/// All interface types.
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

/// Paths of all bits of a type in order: for `Instr` — `op.Op1, op.Op0, k.D1, k.D0`; for a simple type — `[""]`.
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

/// Part of a type: which type, from which bit and how many bits.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TypeSlice {
    pub ty: Iface,
    pub offset: usize,
    pub length: usize,
}

/// Looks up a field by path (`""` — the whole type, `"op"`, `"k.D1"`); `None` if there is no such field.
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

/// Immediate field of a type — for expanding a port on the board.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChildField {
    pub name: &'static str,
    pub path: String,
    pub ty: Iface,
}

/// Immediate fields of a type by path.
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

/// Types are compatible only when their names match.
pub fn can_connect(from: Iface, to: Iface) -> bool {
    from == to
}

/// Bus value as text: `10`, `1?` (most significant bit on the left).
pub fn bus_text(values: &[NodeValue]) -> String {
    values.iter().map(|v| v.map_or('?', |b| if b == 1 { '1' } else { '0' })).collect()
}
