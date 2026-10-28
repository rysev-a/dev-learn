//! RV32IM assembler: text → memory image. All errors are collected, not just the first one.
//!
//! Port of the previous TypeScript assembler: the same directives, pseudo-instructions, expressions (`%hi`, `%lo`, `+`/`-`, quoted
//! characters) and the same Russian message texts, including the order and repetition of messages (expressions are evaluated in two
//! passes).

use std::collections::{BTreeMap, HashMap};

use serde::{Deserialize, Serialize};

use crate::isa::{
    enc_b, enc_i, enc_j, enc_r, enc_s, enc_sh, enc_u, op_by_mnemonic, reg_num, Fmt, Op, OpInfo, EBREAK, ECALL,
};
use crate::js;

/// RAM size of the educational "soft processor" — 16 KiB.
pub const RAM_SIZE: usize = 0x4000;
/// Address where instructions start.
pub const TEXT_BASE: u32 = 0x0000;
/// Address where data starts.
pub const DATA_BASE: u32 = 0x1000;
/// The last kilobyte of memory is reserved for the stack.
pub const STACK_RESERVE: usize = 0x400;
/// Initial value of sp — top of memory.
pub const STACK_TOP: u32 = RAM_SIZE as u32;

/// One word of machine code and where it came from.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmLine {
    /// source line number, 1-based
    pub line: u32,
    /// address
    pub addr: u32,
    /// instruction word
    pub word: u32,
    /// source text of the instruction
    pub text: String,
    /// this instruction is part of an expanded pseudo-instruction
    pub pseudo: bool,
}

/// Assembler error.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmError {
    /// source line number, 1-based
    pub line: u32,
    /// message text
    pub message: String,
}

/// Assembly result.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmResult {
    /// RAM image (`RAM_SIZE` bytes): instructions from address 0, data from `DATA_BASE`
    pub image: Vec<u8>,
    /// how many bytes the instructions occupy
    pub text_size: usize,
    /// how many bytes the data occupies
    pub data_size: usize,
    /// listing: machine code words and where they came from
    pub lines: Vec<AsmLine>,
    /// label addresses
    pub symbols: BTreeMap<String, u32>,
    /// address where execution starts: the `_start` label, or 0 if there is none
    pub entry: u32,
    /// errors (empty if everything assembled)
    pub errors: Vec<AsmError>,
}

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Section {
    Text,
    Data,
}

enum Kind {
    Insn {
        text: String,
        mnemonic: String,
        operands: Vec<String>,
    },
    /// ready bytes (the trailing zeros are not stored: the memory image is zeroed anyway)
    Bytes(Vec<u8>),
    /// `.word`, `.half`, `.byte`: expressions are evaluated in the second pass
    Exprs {
        exprs: Vec<String>,
        size: usize,
    },
}

struct Item {
    line: u32,
    section: Section,
    /// offset within its section
    offset: usize,
    kind: Kind,
}

/// Symbol value: for label and constant names.
type AddrOf<'a> = Option<&'a dyn Fn(&str) -> Option<i64>>;

/* ---------- low-level text parsing ---------- */

/// Strip a comment (`#`, `;`, `//`) outside quotes.
fn strip_comment(s: &str) -> String {
    let c: Vec<char> = s.chars().collect();
    let mut quote: Option<char> = None;
    let mut i = 0;
    while i < c.len() {
        let ch = c[i];
        if let Some(q) = quote {
            if ch == '\\' {
                i += 1;
            } else if ch == q {
                quote = None;
            }
            i += 1;
            continue;
        }
        if ch == '"' || ch == '\'' {
            quote = Some(ch);
        } else if ch == '#' || ch == ';' || (ch == '/' && c.get(i + 1) == Some(&'/')) {
            return c[..i].iter().collect();
        }
        i += 1;
    }
    s.to_string()
}

/// Split operands by commas outside parentheses and quotes.
fn split_operands(s: &str) -> Vec<String> {
    let c: Vec<char> = s.chars().collect();
    let mut out: Vec<String> = Vec::new();
    let mut cur = String::new();
    let mut quote: Option<char> = None;
    let mut depth: i32 = 0;
    let mut i = 0;
    while i < c.len() {
        let ch = c[i];
        if let Some(q) = quote {
            cur.push(ch);
            if ch == '\\' {
                i += 1;
                if let Some(n) = c.get(i) {
                    cur.push(*n);
                }
            } else if ch == q {
                quote = None;
            }
            i += 1;
            continue;
        }
        if ch == '"' || ch == '\'' {
            quote = Some(ch);
            cur.push(ch);
        } else if ch == '(' {
            depth += 1;
            cur.push(ch);
        } else if ch == ')' {
            depth -= 1;
            cur.push(ch);
        } else if ch == ',' && depth == 0 {
            out.push(js::trim(&cur).to_string());
            cur.clear();
        } else {
            cur.push(ch);
        }
        i += 1;
    }
    if !js::trim(&cur).is_empty() || !out.is_empty() {
        out.push(js::trim(&cur).to_string());
    }
    out
}

fn esc_code(unit: u16) -> Option<u16> {
    match unit {
        0x6e => Some(10), // n
        0x74 => Some(9),  // t
        0x72 => Some(13), // r
        0x30 => Some(0),  // 0
        0x5c => Some(92), // \
        0x22 => Some(34), // "
        0x27 => Some(39), // '
        _ => None,
    }
}

fn unit_is_terminator(u: u16) -> bool {
    matches!(u, 0x0a | 0x0d | 0x2028 | 0x2029)
}

/// Quoted string → bytes. Works on UTF-16 code units, like the previous parser: a character outside the BMP yields two replacement
/// characters (each half of the pair is encoded separately), and the code after a backslash is taken by its low 8 bits.
fn parse_string(token: &str) -> Option<Vec<u8>> {
    let t: Vec<u16> = js::trim(token).encode_utf16().collect();
    if t.len() < 2 || t[0] != 0x22 || t[t.len() - 1] != 0x22 {
        return None;
    }
    let inner = &t[1..t.len() - 1];
    // pattern check: (\\. | [^"\\])*
    let mut i = 0;
    while i < inner.len() {
        let u = inner[i];
        if u == 0x5c {
            match inner.get(i + 1) {
                Some(n) if !unit_is_terminator(*n) => i += 2,
                _ => return None,
            }
        } else if u == 0x22 {
            return None;
        } else {
            i += 1;
        }
    }
    let mut out: Vec<u8> = Vec::new();
    let mut i = 0;
    while i < inner.len() {
        let u = inner[i];
        if u == 0x5c {
            i += 1;
            let ch = inner[i];
            out.push((esc_code(ch).unwrap_or(ch) & 0xff) as u8);
        } else if (0xd800..=0xdfff).contains(&u) {
            out.extend_from_slice("\u{fffd}".as_bytes());
        } else if let Some(c) = char::from_u32(u32::from(u)) {
            let mut buf = [0u8; 4];
            out.extend_from_slice(c.encode_utf8(&mut buf).as_bytes());
        }
        i += 1;
    }
    Some(out)
}

/// Low 32 bits of a number, like `ToInt32` in JavaScript.
fn i32w(v: i64) -> i32 {
    v as i32
}

/// Sign extension of the low `bits` bits.
fn sext(v: i64, bits: u32) -> i64 {
    let m: i32 = 1 << (bits - 1);
    i64::from(((i32w(v) & ((1i32 << bits) - 1)) ^ m).wrapping_sub(m))
}

fn parse_radix(digits: &str, radix: u32) -> i64 {
    i64::from_str_radix(digits, radix).unwrap_or(i64::MAX)
}

/// Whether the text matches `^'(\\.|[^\\'])'$` (by UTF-16 code units) and what the character code is.
fn char_literal(t: &str) -> Option<i64> {
    let u: Vec<u16> = t.encode_utf16().collect();
    if u.len() < 3 || u[0] != 0x27 || u[u.len() - 1] != 0x27 {
        return None;
    }
    let g = &u[1..u.len() - 1];
    match g {
        [0x5c, n] if !unit_is_terminator(*n) => Some(i64::from(esc_code(*n).unwrap_or(*n))),
        [c] if *c != 0x5c && *c != 0x27 => Some(i64::from(*c)),
        _ => None,
    }
}

/// `^(.*)\(\s*([^)]+?)\s*\)$`: offset and register from `offset(register)`.
fn parse_mem_operand(s: &str) -> Option<(String, String)> {
    let c: Vec<char> = s.chars().collect();
    // the greedy ".*" backtracks from the end: try the last opening parenthesis first
    for k in (0..c.len()).rev() {
        if c[k] != '(' {
            continue;
        }
        if c[..k].iter().any(|ch| js::is_line_terminator(*ch)) {
            continue;
        }
        if c.last() != Some(&')') || k + 1 >= c.len() {
            continue;
        }
        let m = &c[k + 1..c.len() - 1];
        if m.is_empty() || m.contains(&')') {
            continue;
        }
        let lead = m.iter().take_while(|ch| js::is_space(**ch)).count();
        let group: String = if lead == m.len() {
            m[m.len() - 1..].iter().collect()
        } else {
            let last = m.iter().rposition(|ch| !js::is_space(*ch)).unwrap_or(lead);
            m[lead..=last].iter().collect()
        };
        return Some((c[..k].iter().collect(), group));
    }
    None
}

/// Label at the start of a line: `name:` and the rest of the line.
fn split_label(text: &str) -> Option<(String, String)> {
    let c: Vec<char> = text.chars().collect();
    if !c.first().is_some_and(|ch| js::is_ident_start(*ch)) {
        return None;
    }
    let mut p = c.iter().take_while(|ch| js::is_ident_char(**ch)).count();
    let name: String = c[..p].iter().collect();
    while c.get(p).is_some_and(|ch| js::is_space(*ch)) {
        p += 1;
    }
    if c.get(p) != Some(&':') {
        return None;
    }
    p += 1;
    while c.get(p).is_some_and(|ch| js::is_space(*ch)) {
        p += 1;
    }
    let rest: String = c[p..].iter().collect();
    if js::has_line_terminator(&rest) {
        return None;
    }
    Some((name, rest))
}

/// Append ready bytes to a section (`len` may exceed `bytes.len()`: the remainder is zeros).
fn emit(items: &mut Vec<Item>, size: &mut [usize; 2], section: Section, line: u32, len: usize, bytes: Vec<u8>) {
    items.push(Item { line, section, offset: size[section as usize], kind: Kind::Bytes(bytes) });
    size[section as usize] = size[section as usize].saturating_add(len);
}

/* ---------- expression evaluation ---------- */

struct Ctx {
    errors: Vec<AsmError>,
    equ: HashMap<String, i64>,
}

impl Ctx {
    fn fail(&mut self, line: u32, message: impl Into<String>) {
        self.errors.push(AsmError { line, message: message.into() });
    }

    /// Value of an expression; `addr_of` — whether labels are available (after the first pass).
    fn eval(&mut self, expr: &str, line: u32, addr_of: AddrOf) -> Option<i64> {
        let e = js::trim(expr);
        if e.is_empty() {
            self.fail(line, i18n::tr("Empty expression"));
            return None;
        }
        // %hi(...) and %lo(...)
        for (prefix, hi) in [("%hi(", true), ("%lo(", false)] {
            if e.len() >= 5 && e.starts_with(prefix) && e.ends_with(')') {
                let inner = &e[4..e.len() - 1];
                if !js::has_line_terminator(inner) {
                    let v = self.eval(inner, line, addr_of)?;
                    return Some(if hi {
                        i64::from((i32w(v.wrapping_add(0x800)) >> 12) & 0xfffff)
                    } else {
                        sext(v, 12)
                    });
                }
            }
        }
        // sum and difference of terms
        let units: Vec<u16> = e.encode_utf16().collect();
        let parts = scan_terms(&units);
        let strip = |u: &[u16]| -> Vec<u16> { u.iter().copied().filter(|x| !js::is_space_unit(*x)).collect() };
        let joined: Vec<u16> = parts.iter().flat_map(|p| p.iter().copied()).collect();
        if parts.is_empty() || strip(&joined) != strip(&units) {
            self.fail(line, i18n::trf!("Cannot understand the expression “{0}”", e));
            return None;
        }
        let mut total: i64 = 0;
        for raw in &parts {
            let raw_s = String::from_utf16_lossy(raw);
            let raw_t = js::trim(&raw_s);
            let sign: i64 = if raw_t.starts_with('-') { -1 } else { 1 };
            let t = js::trim_start_sign(raw_t);
            let v: Option<i64> = if let Some(c) = char_literal(t) {
                Some(c)
            } else if let Some(h) = t
                .strip_prefix("0x")
                .or_else(|| t.strip_prefix("0X"))
                .filter(|h| !h.is_empty() && h.bytes().all(|b| b.is_ascii_hexdigit()))
            {
                Some(parse_radix(h, 16))
            } else if let Some(b) = t
                .strip_prefix("0b")
                .or_else(|| t.strip_prefix("0B"))
                .filter(|b| !b.is_empty() && b.bytes().all(|x| x == b'0' || x == b'1'))
            {
                Some(parse_radix(b, 2))
            } else if !t.is_empty() && t.bytes().all(|b| b.is_ascii_digit()) {
                Some(parse_radix(t, 10))
            } else if let Some(v) = self.equ.get(t) {
                Some(*v)
            } else if js::is_ident(t) {
                let v = addr_of.and_then(|f| f(t));
                if v.is_none() {
                    if addr_of.is_some() {
                        self.fail(line, i18n::trf!("No label “{0}”", t));
                    } else {
                        self.fail(line, i18n::trf!("Labels cannot be used here (a number is needed): “{0}”", t));
                    }
                    return None;
                }
                v
            } else {
                self.fail(line, i18n::trf!("Cannot understand “{0}”", t));
                return None;
            };
            total = total.wrapping_add(sign.wrapping_mul(v?));
        }
        Some(total)
    }
}

/// All matches of `(?:^|[+-])\s*(?:'(?:\\.|[^\\'])'|[^+\-\s]+)` in the text (like `String.match` with the g flag).
fn scan_terms(c: &[u16]) -> Vec<Vec<u16>> {
    let n = c.len();
    let is_sp = |i: usize| c.get(i).is_some_and(|u| js::is_space_unit(*u));
    // term from position q (after whitespace): first a quoted character, then a "word"
    let term = |q: usize| -> Option<usize> {
        if c.get(q) == Some(&0x27) {
            match (c.get(q + 1), c.get(q + 2), c.get(q + 3)) {
                (Some(0x5c), Some(x), Some(0x27)) if !unit_is_terminator(*x) => return Some(q + 4),
                (Some(x), Some(0x27), _) if *x != 0x5c && *x != 0x27 => return Some(q + 3),
                _ => {}
            }
        }
        let mut e = q;
        while e < n && c[e] != 0x2b && c[e] != 0x2d && !is_sp(e) {
            e += 1;
        }
        (e > q).then_some(e)
    };
    let after_ws = |mut q: usize| -> Option<usize> {
        while is_sp(q) {
            q += 1;
        }
        term(q)
    };
    let mut out = Vec::new();
    let mut p = 0;
    while p < n {
        let mut end = None;
        if p == 0 {
            end = after_ws(0);
        }
        if end.is_none() && (c[p] == 0x2b || c[p] == 0x2d) {
            end = after_ws(p + 1);
        }
        match end {
            Some(e) => {
                out.push(c[p..e].to_vec());
                p = e;
            }
            None => p += 1,
        }
    }
    out
}

/* ---------- assembler ---------- */

/// RV32IM assembler: text → memory image. All errors are collected, not just the first one.
pub fn assemble(source: &str) -> AsmResult {
    let mut cx = Ctx { errors: Vec::new(), equ: HashMap::new() };
    // label → section and offset (the address becomes known after the first pass)
    let mut labels: HashMap<String, (Section, usize)> = HashMap::new();
    let mut label_order: Vec<String> = Vec::new();
    let mut items: Vec<Item> = Vec::new();
    // space used per section: [instructions, data]
    let mut size: [usize; 2] = [0, 0];
    let mut section = Section::Text;

    let pieces: Vec<&str> = source.split('\n').collect();
    let last = pieces.len().saturating_sub(1);
    for (i, raw0) in pieces.iter().enumerate() {
        let raw = if i < last { raw0.strip_suffix('\r').unwrap_or(raw0) } else { raw0 };
        let line = (i + 1) as u32;
        let mut text = js::trim(&strip_comment(raw)).to_string();
        if text.is_empty() {
            continue;
        }

        // labels at the start of the line (there may be several)
        while let Some((name, rest)) = split_label(&text) {
            if labels.contains_key(&name) {
                cx.fail(line, i18n::trf!("Label “{0}” is already defined", name));
            } else {
                let off = size[section as usize];
                labels.insert(name.clone(), (section, off));
                label_order.push(name);
            }
            text = js::trim(&rest).to_string();
        }
        if text.is_empty() {
            continue;
        }

        // head: the "word" up to the first space, and the rest
        let (head, rest) = match text.find(js::is_space) {
            Some(p) => {
                let (h, r) = text.split_at(p);
                (h.to_string(), r.trim_start_matches(js::is_space).to_string())
            }
            None => (text.clone(), String::new()),
        };
        let mn = head.to_lowercase();
        let ops = split_operands(&rest);

        if mn.starts_with('.') {
            match mn.as_str() {
                ".text" => section = Section::Text,
                ".data" | ".rodata" | ".bss" => section = Section::Data,
                ".section" => {
                    let name = js::trim(ops.first().map_or("", |s| s.as_str()));
                    section = if name.starts_with(".text") { Section::Text } else { Section::Data };
                }
                ".globl" | ".global" | ".type" | ".size" | ".option" | ".attribute" | ".file" => {}
                ".equ" | ".set" => {
                    let v = if ops.len() == 2 { cx.eval(&ops[1], line, None) } else { None };
                    if ops.len() != 2 || !js::is_ident(&ops[0]) {
                        cx.fail(line, i18n::tr("Usage: .equ NAME, number"));
                    } else if let Some(v) = v {
                        cx.equ.insert(ops[0].clone(), v);
                    }
                }
                ".word" | ".half" | ".short" | ".byte" => {
                    let sz = if mn == ".word" {
                        4
                    } else if mn == ".byte" {
                        1
                    } else {
                        2
                    };
                    items.push(Item {
                        line,
                        section,
                        offset: size[section as usize],
                        kind: Kind::Exprs { exprs: ops.clone(), size: sz },
                    });
                    size[section as usize] = size[section as usize].saturating_add(sz * ops.len());
                }
                ".ascii" | ".asciz" | ".string" => {
                    let mut bytes: Vec<u8> = Vec::new();
                    for o in &ops {
                        match parse_string(o) {
                            None => {
                                cx.fail(line, i18n::trf!("Expected a quoted string, but found “{0}”", o));
                                continue;
                            }
                            Some(s) => {
                                bytes.extend(s);
                                if mn != ".ascii" {
                                    bytes.push(0);
                                }
                            }
                        }
                    }
                    let len = bytes.len();
                    emit(&mut items, &mut size, section, line, len, bytes);
                }
                ".space" | ".zero" | ".skip" => {
                    let n = if !ops.is_empty() { cx.eval(&ops[0], line, None) } else { None };
                    match n {
                        Some(n) if n >= 0 => emit(
                            &mut items,
                            &mut size,
                            section,
                            line,
                            usize::try_from(n).unwrap_or(usize::MAX),
                            Vec::new(),
                        ),
                        _ => cx.fail(line, i18n::tr("Usage: .space number_of_bytes")),
                    }
                }
                ".align" | ".balign" => {
                    let n = if !ops.is_empty() { cx.eval(&ops[0], line, None) } else { None };
                    match n {
                        Some(n) if n >= 0 => {
                            let a: i64 =
                                if mn == ".align" { i64::from(1i32.wrapping_shl((i32w(n) as u32) & 31)) } else { n };
                            let (cur, a) = (size[section as usize] as i128, i128::from(a));
                            if a != 0 {
                                let pad = (a - (cur % a)) % a;
                                if pad > 0 {
                                    emit(
                                        &mut items,
                                        &mut size,
                                        section,
                                        line,
                                        usize::try_from(pad).unwrap_or(usize::MAX),
                                        Vec::new(),
                                    );
                                }
                            }
                        }
                        _ => cx.fail(line, i18n::trf!("Usage: {0} number", mn)),
                    }
                }
                _ => cx.fail(line, i18n::trf!("Unknown directive “{0}”", mn)),
            }
            continue;
        }

        if section != Section::Text {
            cx.fail(line, i18n::tr("Instructions can only be written in the .text section (.data is currently active)"));
            continue;
        }
        let words = insn_words(&mut cx, &mn, &ops, line);
        items.push(Item {
            line,
            section,
            offset: size[0],
            kind: Kind::Insn { text: text.clone(), mnemonic: mn.clone(), operands: ops },
        });
        size[0] += 4 * words;
    }

    let (size_text, size_data) = (size[0], size[1]);
    if size_text > DATA_BASE as usize {
        cx.fail(
            1,
            i18n::trf!("The program is too long: the instructions ({0} bytes) do not fit before the data address 0x{1}", size_text, format!("{:x}", DATA_BASE)),
        );
    }
    if (DATA_BASE as usize).saturating_add(size_data) > RAM_SIZE - STACK_RESERVE {
        cx.fail(1, i18n::trf!("Too much data: {0} bytes; {1} bytes must be left for the stack", size_data, STACK_RESERVE));
    }

    // label addresses
    let mut symbols: BTreeMap<String, u32> = BTreeMap::new();
    for name in &label_order {
        if let Some((sec, off)) = labels.get(name) {
            let base = if *sec == Section::Text { TEXT_BASE } else { DATA_BASE };
            symbols.insert(name.clone(), base.wrapping_add(*off as u32));
        }
    }
    let sym_lookup = |name: &str| -> Option<i64> { symbols.get(name).map(|v| i64::from(*v)) };

    // pass 2: encoding
    let mut image = vec![0u8; RAM_SIZE];
    let mut lines: Vec<AsmLine> = Vec::new();
    for it in &items {
        let base =
            ((if it.section == Section::Text { TEXT_BASE } else { DATA_BASE }) as usize).saturating_add(it.offset);
        match &it.kind {
            Kind::Bytes(bytes) => {
                for (k, b) in bytes.iter().enumerate() {
                    if let Some(slot) = image.get_mut(base.saturating_add(k)) {
                        *slot = *b;
                    }
                }
            }
            Kind::Exprs { exprs, size } => {
                let mut a = base;
                for expr in exprs {
                    if let Some(v) = cx.eval(expr, it.line, Some(&sym_lookup)) {
                        for k in 0..*size {
                            if let Some(slot) = image.get_mut(a.saturating_add(k)) {
                                *slot = ((i32w(v) as u32) >> (8 * k)) as u8;
                            }
                        }
                    }
                    a = a.saturating_add(*size);
                }
            }
            Kind::Insn { text, mnemonic, operands } => {
                let words = encode_insn(&mut cx, it.line, mnemonic, operands, base as i64, &sym_lookup);
                let Some(words) = words else { continue };
                let multi = words.len() > 1;
                for (k, w) in words.iter().enumerate() {
                    let addr = base.saturating_add(4 * k);
                    for j in 0..4 {
                        if let Some(slot) = image.get_mut(addr.saturating_add(j)) {
                            *slot = (*w >> (8 * j)) as u8;
                        }
                    }
                    lines.push(AsmLine {
                        line: it.line,
                        addr: addr as u32,
                        word: *w,
                        text: text.clone(),
                        pseudo: multi || is_pseudo(mnemonic),
                    });
                }
            }
        }
    }

    let entry = symbols.get("_start").copied().unwrap_or(TEXT_BASE);
    AsmResult { image, text_size: size_text, data_size: size_data, lines, symbols, entry, errors: cx.errors }
}

/// How many words an instruction or pseudo-instruction will take.
fn insn_words(cx: &mut Ctx, mn: &str, ops: &[String], line: u32) -> usize {
    match mn {
        "la" | "call" | "tail" => 2,
        "li" => {
            if ops.len() != 2 {
                return 1; // the error will be caught by the second pass
            }
            let Some(raw) = cx.eval(&ops[1], line, None) else { return 1 };
            let v = i32w(raw); // 0xFFFFFFFF and −1 are the same 32-bit word
            if (-2048..=2047).contains(&v) || v & 0xfff == 0 {
                1
            } else {
                2
            }
        }
        _ => 1,
    }
}

const PSEUDO_NAMES: &[&str] = &[
    "nop", "li", "la", "mv", "not", "neg", "seqz", "snez", "j", "jr", "ret", "call", "tail", "beqz", "bnez", "blez",
    "bgez", "bltz", "bgtz", "bgt", "ble", "bgtu", "bleu",
];

fn is_pseudo(mn: &str) -> bool {
    PSEUDO_NAMES.contains(&mn)
}

/// State of encoding one instruction: errors accumulate here and operands are evaluated.
struct Enc<'a> {
    cx: &'a mut Ctx,
    line: u32,
    mn: &'a str,
    ops: &'a [String],
    pc: i64,
    addr_of: &'a dyn Fn(&str) -> Option<i64>,
}

impl<'a> Enc<'a> {
    fn fail(&mut self, msg: impl Into<String>) {
        self.cx.fail(self.line, msg);
    }

    fn need(&mut self, n: usize, usage: &str) -> bool {
        if self.ops.len() == n {
            return true;
        }
        let word = if n == 1 {
            i18n::tr("operand")
        } else if n < 5 {
            i18n::tr("operands")
        } else {
            i18n::tr("operands (in total)")
        };
        let mn = self.mn;
        self.fail(i18n::trf!("“{0}” takes {1} {2}: {3}", mn, n, word, usage));
        false
    }

    fn reg(&mut self, t: Option<&str>) -> Option<u8> {
        let r = t.and_then(reg_num);
        if r.is_none() {
            self.fail(i18n::trf!("Expected a register (x0…x31 or zero, ra, sp, a0…), but found “{0}”", t.unwrap_or("")));
        }
        r
    }

    fn op(&self, i: usize) -> Option<&'a str> {
        let ops: &'a [String] = self.ops;
        ops.get(i).map(|s| s.as_str())
    }

    fn eval(&mut self, t: &str) -> Option<i64> {
        let f = self.addr_of;
        self.cx.eval(t, self.line, Some(f))
    }

    fn num(&mut self, t: &str, min: i64, max: i64, what: &str) -> Option<i64> {
        let v = self.eval(t)?;
        if v < min || v > max {
            self.fail(i18n::trf!("{0}: {1} does not fit — allowed range is {2} to {3}", what, v, min, max));
            return None;
        }
        Some(v)
    }

    /// Offset to a label (or an explicit number).
    fn target(&mut self, t: &str, bits: u32) -> Option<i64> {
        let tt = js::trim(t);
        let off = if js::is_ident(tt) && (self.addr_of)(tt).is_some() {
            (self.addr_of)(tt).map(|a| a - self.pc)
        } else {
            self.eval(t)
        }?;
        let lim: i64 = 1 << (bits - 1);
        if off % 2 != 0 {
            self.fail(i18n::trf!("Offset {0} must be even", off));
            return None;
        }
        if off < -lim || off >= lim {
            self.fail(i18n::trf!("Label “{0}” is too far away: {1} bytes (allowed from {2} to {3})", t, off, -lim, lim - 2));
            return None;
        }
        Some(off)
    }
}

fn opi(op: Op) -> &'static OpInfo {
    op.info()
}

/// Encoding of an instruction or pseudo-instruction into words; `None` — there were errors.
fn encode_insn(
    cx: &mut Ctx,
    line: u32,
    mn: &str,
    ops: &[String],
    pc: i64,
    addr_of: &dyn Fn(&str) -> Option<i64>,
) -> Option<Vec<u32>> {
    let mut e = Enc { cx, line, mn, ops, pc, addr_of };
    if let Some(r) = pseudo(&mut e) {
        return r;
    }
    real(&mut e)
}

/// Two registers `rd, rs`; `None` — errors already recorded.
fn two_regs(e: &mut Enc, usage: &str) -> Option<(u8, u8)> {
    if !e.need(2, usage) {
        return None;
    }
    let (rd, rs) = (e.reg(e.op(0)), e.reg(e.op(1)));
    rd.zip(rs)
}

/// Pseudo-instructions. `None` — not a pseudo-instruction, continue as a real one.
fn pseudo(e: &mut Enc) -> Option<Option<Vec<u32>>> {
    let mn = e.mn;
    let ops = e.ops;
    match mn {
        "nop" => {
            if !e.need(0, "nop") {
                return Some(None);
            }
            Some(Some(vec![enc_i(opi(Op::Addi), 0, 0, 0)]))
        }
        "ret" => {
            if !e.need(0, "ret") {
                return Some(None);
            }
            Some(Some(vec![enc_i(opi(Op::Jalr), 0, 1, 0)]))
        }
        "mv" => Some(two_regs(e, "mv rd, rs").map(|(rd, rs)| vec![enc_i(opi(Op::Addi), rd, rs, 0)])),
        "not" => Some(two_regs(e, "not rd, rs").map(|(rd, rs)| vec![enc_i(opi(Op::Xori), rd, rs, -1)])),
        "neg" => Some(two_regs(e, "neg rd, rs").map(|(rd, rs)| vec![enc_r(opi(Op::Sub), rd, 0, rs)])),
        "seqz" => Some(two_regs(e, "seqz rd, rs").map(|(rd, rs)| vec![enc_i(opi(Op::Sltiu), rd, rs, 1)])),
        "snez" => Some(two_regs(e, "snez rd, rs").map(|(rd, rs)| vec![enc_r(opi(Op::Sltu), rd, 0, rs)])),
        "li" => {
            if !e.need(2, i18n::tr("li rd, number")) {
                return Some(None);
            }
            let rd = e.reg(e.op(0));
            let raw = e.cx.eval(&ops[1], e.line, None);
            let (Some(rd), Some(raw)) = (rd, raw) else { return Some(None) };
            if !(-0x8000_0000..=0xffff_ffff).contains(&raw) {
                e.fail(i18n::trf!("Number {0} does not fit in 32 bits", raw));
                return Some(None);
            }
            let v = i32w(raw); // 0xFFFFFFFF and −1 are the same 32-bit word
            if (-2048..=2047).contains(&v) {
                return Some(Some(vec![enc_i(opi(Op::Addi), rd, 0, v)]));
            }
            let lo = sext(i64::from(v), 12);
            let hi = ((i64::from(v) - lo) as u32 >> 12) & 0xfffff;
            let mut words = vec![enc_u(opi(Op::Lui), rd, hi as i32)];
            if lo != 0 {
                words.push(enc_i(opi(Op::Addi), rd, rd, lo as i32));
            }
            Some(Some(words))
        }
        "la" | "call" | "tail" => {
            let is_la = mn == "la";
            let usage = if is_la { i18n::tr("la rd, label").to_string() } else { i18n::trf!("{0} label", mn) };
            if !e.need(if is_la { 2 } else { 1 }, &usage) {
                return Some(None);
            }
            let rd = if is_la {
                e.reg(e.op(0))
            } else if mn == "call" {
                Some(1)
            } else {
                Some(6)
            };
            let sym = if is_la { &ops[1] } else { &ops[0] };
            let dest = e.eval(sym);
            let (Some(rd), Some(dest)) = (rd, dest) else { return Some(None) };
            let off = dest.wrapping_sub(e.pc);
            let lo = sext(off, 12);
            let hi = (i32w(off.wrapping_sub(lo)) >> 12) & 0xfffff;
            let second = if is_la {
                enc_i(opi(Op::Addi), rd, rd, lo as i32)
            } else {
                enc_i(opi(Op::Jalr), if mn == "call" { 1 } else { 0 }, rd, lo as i32)
            };
            Some(Some(vec![enc_u(opi(Op::Auipc), rd, hi), second]))
        }
        "j" | "jal" => {
            if mn == "j" || ops.len() == 1 {
                if !e.need(1, &i18n::trf!("{0} label", mn)) {
                    return Some(None);
                }
                let off = e.target(&ops[0], 21);
                return Some(off.map(|o| vec![enc_j(opi(Op::Jal), if mn == "j" { 0 } else { 1 }, o as i32)]));
            }
            None
        }
        "jr" => {
            if !e.need(1, "jr rs") {
                return Some(None);
            }
            let rs = e.reg(e.op(0));
            Some(rs.map(|rs| vec![enc_i(opi(Op::Jalr), 0, rs, 0)]))
        }
        "beqz" | "bnez" | "blez" | "bgez" | "bltz" | "bgtz" => {
            if !e.need(2, &i18n::trf!("{0} rs, label", mn)) {
                return Some(None);
            }
            let rs = e.reg(e.op(0));
            let off = e.target(&ops[1], 13);
            let (Some(rs), Some(off)) = (rs, off) else { return Some(None) };
            let (m, swap) = match mn {
                "beqz" => (Op::Beq, false),
                "bnez" => (Op::Bne, false),
                "blez" => (Op::Bge, true), // bge zero, rs
                "bgez" => (Op::Bge, false),
                "bltz" => (Op::Blt, false),
                _ => (Op::Blt, true), // bgtz: blt zero, rs
            };
            Some(Some(vec![enc_b(opi(m), if swap { 0 } else { rs }, if swap { rs } else { 0 }, off as i32)]))
        }
        "bgt" | "ble" | "bgtu" | "bleu" => {
            if !e.need(3, &i18n::trf!("{0} rs1, rs2, label", mn)) {
                return Some(None);
            }
            let (a, b) = (e.reg(e.op(0)), e.reg(e.op(1)));
            let off = e.target(&ops[2], 13);
            let (Some(a), Some(b), Some(off)) = (a, b, off) else { return Some(None) };
            let m = match mn {
                "bgt" => Op::Blt,
                "ble" => Op::Bge,
                "bgtu" => Op::Bltu,
                _ => Op::Bgeu,
            };
            Some(Some(vec![enc_b(opi(m), b, a, off as i32)]))
        }
        _ => None,
    }
}

/// Real instructions.
fn real(e: &mut Enc) -> Option<Vec<u32>> {
    let mn = e.mn;
    let ops = e.ops;
    let Some(def) = op_by_mnemonic(mn) else {
        // the message uses the mnemonic as written (it is already lowercase, as in the previous version)
        e.fail(i18n::trf!("Unknown instruction “{0}”", mn));
        return None;
    };
    match def.fmt {
        Fmt::SYS => {
            if !e.need(0, def.mnemonic) {
                return None;
            }
            Some(vec![if def.op == Op::Ecall { ECALL } else { EBREAK }])
        }
        Fmt::R => {
            if !e.need(3, &format!("{mn} rd, rs1, rs2")) {
                return None;
            }
            let (rd, a, b) = (e.reg(e.op(0)), e.reg(e.op(1)), e.reg(e.op(2)));
            Some(vec![enc_r(def, rd?, a?, b?)])
        }
        Fmt::I => {
            if !e.need(3, &i18n::trf!("{0} rd, rs1, number", mn)) {
                return None;
            }
            let (rd, rs) = (e.reg(e.op(0)), e.reg(e.op(1)));
            let v = e.num(&ops[2], -2048, 2047, i18n::tr("Number"));
            Some(vec![enc_i(def, rd?, rs?, v? as i32)])
        }
        Fmt::SH => {
            if !e.need(3, &i18n::trf!("{0} rd, rs1, number 0…31", mn)) {
                return None;
            }
            let (rd, rs) = (e.reg(e.op(0)), e.reg(e.op(1)));
            let v = e.num(&ops[2], 0, 31, i18n::tr("Shift amount"));
            Some(vec![enc_sh(def, rd?, rs?, v? as i32)])
        }
        Fmt::L | Fmt::S => {
            if !e.need(2, &i18n::trf!("{0} register, offset(register)", mn)) {
                return None;
            }
            let r = e.reg(e.op(0));
            let Some((off_t, base_t)) = parse_mem_operand(&ops[1]) else {
                e.fail(i18n::trf!("An address is written as offset(register), for example 4(sp), but found “{0}”", ops[1]));
                return None;
            };
            let base = e.reg(Some(&base_t));
            let off =
                if js::trim(&off_t).is_empty() { Some(0) } else { e.num(&off_t, -2048, 2047, i18n::tr("Offset")) };
            let (r, base, off) = (r?, base?, off? as i32);
            Some(vec![if def.fmt == Fmt::L { enc_i(def, r, base, off) } else { enc_s(def, r, base, off) }])
        }
        Fmt::B => {
            if !e.need(3, &i18n::trf!("{0} rs1, rs2, label", mn)) {
                return None;
            }
            let (a, b) = (e.reg(e.op(0)), e.reg(e.op(1)));
            let off = e.target(&ops[2], 13);
            Some(vec![enc_b(def, a?, b?, off? as i32)])
        }
        Fmt::U => {
            if !e.need(2, &i18n::trf!("{0} rd, number", mn)) {
                return None;
            }
            let rd = e.reg(e.op(0));
            let v = e.num(&ops[1], -0x80000, 0xfffff, i18n::tr("Number"));
            Some(vec![enc_u(def, rd?, v? as i32)])
        }
        Fmt::J => {
            if !e.need(2, i18n::tr("jal rd, label")) {
                return None;
            }
            let rd = e.reg(e.op(0));
            let off = e.target(&ops[1], 21);
            Some(vec![enc_j(def, rd?, off? as i32)])
        }
        Fmt::JR => {
            // jalr rd, offset(rs)  |  jalr rd, rs, offset  |  jalr rs
            if ops.len() == 1 {
                let rs = e.reg(e.op(0));
                return Some(vec![enc_i(def, 1, rs?, 0)]);
            }
            if ops.len() == 2 {
                let Some((off_t, rs_t)) = parse_mem_operand(&ops[1]) else {
                    e.fail(i18n::trf!("Expected: jalr rd, offset(rs), but found “{0}”", ops[1]));
                    return None;
                };
                let (rd, rs) = (e.reg(e.op(0)), e.reg(Some(&rs_t)));
                let off =
                    if js::trim(&off_t).is_empty() { Some(0) } else { e.num(&off_t, -2048, 2047, i18n::tr("Offset")) };
                return Some(vec![enc_i(def, rd?, rs?, off? as i32)]);
            }
            if !e.need(3, i18n::tr("jalr rd, rs, offset")) {
                return None;
            }
            let (rd, rs) = (e.reg(e.op(0)), e.reg(e.op(1)));
            let off = e.num(&ops[2], -2048, 2047, i18n::tr("Offset"));
            Some(vec![enc_i(def, rd?, rs?, off? as i32)])
        }
    }
}
