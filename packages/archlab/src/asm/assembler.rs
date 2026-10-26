//! Ассемблер «Мини-8»: текст программы → машинные слова. Все ошибки собираются, а не только первая.
//! Порт `assembler.ts`; сообщения об ошибках совпадают с ним дословно.

use super::isa::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Одна собранная команда: откуда она, по какому адресу, во что превратилась.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmLine {
    /// Номер строки исходника, с 1.
    pub line: usize,
    pub addr: usize,
    pub word: u16,
    /// Исходный текст команды (без метки и комментария).
    pub text: String,
}

/// Ошибка ассемблирования.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmError {
    pub line: usize,
    pub message: String,
}

/// Результат ассемблирования.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct AsmResult {
    pub words: Vec<u16>,
    pub lines: Vec<AsmLine>,
    pub labels: HashMap<String, usize>,
    pub errors: Vec<AsmError>,
}

struct Parsed {
    line: usize,
    mnemonic: String,
    operands: Vec<String>,
    text: String,
}

fn is_ident(s: &str) -> bool {
    let word = |c: char| c.is_ascii_alphanumeric() || c == '_' || ('\u{410}'..='\u{44f}').contains(&c) || c == '\u{401}' || c == '\u{451}';
    let mut it = s.chars();
    match it.next() {
        Some(c) if word(c) && !c.is_ascii_digit() => it.all(word),
        _ => false,
    }
}

/// Убирает комментарий (`;` или `#`), не трогая символы в кавычках.
fn strip_comment(s: &str) -> &str {
    let mut quote = false;
    for (i, c) in s.char_indices() {
        if c == '\'' {
            quote = !quote;
        }
        if !quote && (c == ';' || c == '#') {
            return &s[..i];
        }
    }
    s
}

/// Делит операнды по запятым, не ломая символ `,` в кавычках.
fn split_operands(s: &str) -> Vec<String> {
    let mut parts = Vec::new();
    let mut cur = String::new();
    let mut quote = false;
    for ch in s.chars() {
        if ch == '\'' {
            quote = !quote;
        }
        if ch == ',' && !quote {
            parts.push(cur.trim().to_string());
            cur.clear();
        } else {
            cur.push(ch);
        }
    }
    if !cur.trim().is_empty() || !parts.is_empty() {
        parts.push(cur.trim().to_string());
    }
    parts
}

fn escape(c: char) -> Option<f64> {
    match c {
        'n' => Some(10.0),
        't' => Some(9.0),
        '0' => Some(0.0),
        'r' => Some(13.0),
        '\\' => Some(92.0),
        '\'' => Some(39.0),
        _ => None,
    }
}

/// Число: `42`, `-5`, `0x2A`, `0b101`, `'A'`, `'\n'` или имя из `.equ`. Числа — `f64`, как в JavaScript.
fn parse_number(token: &str, equ: &HashMap<String, f64>) -> Option<f64> {
    let t = token.trim();
    if let Some(v) = equ.get(t) {
        return Some(*v);
    }
    // 'x' или '\x': один символ BMP (в JS регулярка без флага u не берёт суррогатные пары)
    let chars: Vec<char> = t.chars().collect();
    if chars.len() >= 3 && chars[0] == '\'' && chars[chars.len() - 1] == '\'' {
        let body = &chars[1..chars.len() - 1];
        let bmp = |c: char| (c as u32) <= 0xffff;
        let line_term = |c: char| matches!(c, '\n' | '\r' | '\u{2028}' | '\u{2029}');
        match body {
            ['\\', c] if bmp(*c) && !line_term(*c) => return escape(*c),
            [c] if *c != '\\' && *c != '\'' && bmp(*c) => return Some(*c as u32 as f64),
            _ => {}
        }
    }
    let (sign, rest) = match t.chars().next() {
        Some('+') => (1.0, &t[1..]),
        Some('-') => (-1.0, &t[1..]),
        _ => (1.0, t),
    };
    let lower = rest.to_lowercase();
    let (digits, base) = if let Some(h) = lower.strip_prefix("0x") {
        (h, 16)
    } else if let Some(b) = lower.strip_prefix("0b") {
        (b, 2)
    } else {
        (lower.as_str(), 10)
    };
    if digits.is_empty() || !digits.chars().all(|c| c.is_digit(base)) {
        return None;
    }
    // 0b101 — двоичное; но «0b» без бит или с другими цифрами не подходит, как и в регулярке JS
    if base == 10 && !digits.chars().all(|c| c.is_ascii_digit()) {
        return None;
    }
    let n = digits.chars().fold(0.0f64, |acc, c| acc * base as f64 + c.to_digit(base).unwrap_or(0) as f64);
    Some(sign * n)
}

fn parse_reg(token: &str) -> Option<u16> {
    let t = token.trim().to_lowercase();
    if t == "zero" {
        return Some(0);
    }
    let mut it = t.chars();
    match (it.next(), it.next(), it.next()) {
        (Some('r'), Some(d @ '0'..='7'), None) => Some(d as u16 - '0' as u16),
        _ => None,
    }
}

/// Число как в шаблонной строке JavaScript: целые без дробной части и без «-0».
fn show_num(v: f64) -> String {
    if v == 0.0 {
        "0".into()
    } else if v.fract() == 0.0 && v.abs() < 1e21 {
        format!("{}", v as i128)
    } else {
        format!("{v}")
    }
}

fn plural(n: usize) -> &'static str {
    if n == 1 {
        "операнд"
    } else {
        "операнда"
    }
}

/// Ассемблер: текст программы → машинные слова.
pub fn assemble(source: &str) -> AsmResult {
    let mut errors: Vec<AsmError> = Vec::new();
    let mut labels: HashMap<String, usize> = HashMap::new();
    let mut equ: HashMap<String, f64> = HashMap::new();
    let mut parsed: Vec<Parsed> = Vec::new();
    let fail = |errors: &mut Vec<AsmError>, line: usize, message: String| errors.push(AsmError { line, message });

    /* ---------- проход 1: метки, константы, разбор строк ---------- */
    for (i, raw) in source.split('\n').enumerate() {
        let raw = raw.strip_suffix('\r').unwrap_or(raw);
        let line = i + 1;
        let mut text = strip_comment(raw).trim().to_string();
        if text.is_empty() {
            continue;
        }

        // метка в начале строки: `имя:` — непустая серия символов без пробелов, `:` и `,`, затем двоеточие
        let run_end = text.find(|c: char| c.is_whitespace() || c == ':' || c == ',').unwrap_or(text.len());
        if run_end > 0 && text[run_end..].starts_with(':') {
            let name = text[..run_end].to_string();
            let rest = text[run_end + 1..].trim_start().to_string();
            if !is_ident(&name) {
                fail(&mut errors, line, format!("Недопустимое имя метки «{name}»"));
            } else if labels.contains_key(&name) {
                fail(&mut errors, line, format!("Метка «{name}» уже объявлена"));
            } else {
                labels.insert(name, parsed.len());
            }
            text = rest.trim().to_string();
            if text.is_empty() {
                continue;
            }
        }

        let head_end = text.find(char::is_whitespace).unwrap_or(text.len());
        let mnemonic = text[..head_end].to_lowercase();
        let operands = split_operands(text[head_end..].trim_start());

        if mnemonic == ".equ" {
            let name = operands.first().cloned().unwrap_or_default();
            let value = if operands.len() == 2 { parse_number(&operands[1], &equ) } else { None };
            if operands.len() != 2 || !is_ident(&name) {
                fail(&mut errors, line, "Нужно так: .equ ИМЯ, число".into());
            } else if let Some(v) = value {
                equ.insert(name, v);
            } else {
                fail(&mut errors, line, format!("Не понимаю число «{}»", operands[1]));
            }
            continue;
        }

        parsed.push(Parsed { line, mnemonic, operands, text });
    }

    if parsed.len() > PROGRAM_MAX {
        let line = parsed[PROGRAM_MAX].line;
        fail(&mut errors, line, format!("Слишком длинная программа: не больше {PROGRAM_MAX} команд"));
    }

    /* ---------- проход 2: кодирование ---------- */
    let mut words = Vec::new();
    let mut lines = Vec::new();

    for (addr, p) in parsed.iter().enumerate() {
        let line = p.line;
        let mut mnemonic = p.mnemonic.clone();
        let mut ops = p.operands.clone();

        // псевдокоманды
        let need = |errors: &mut Vec<AsmError>, mnemonic: &str, ops: &[String], n: usize, usage: &str| -> bool {
            if ops.len() != n {
                errors.push(AsmError { line, message: format!("«{mnemonic}» принимает {n} {}: {usage}", plural(n)) });
                return false;
            }
            true
        };
        match mnemonic.as_str() {
            "nop" => {
                if !need(&mut errors, &mnemonic, &ops, 0, "nop") {
                    continue;
                }
                mnemonic = "addi".into();
                ops = vec!["r0".into(), "r0".into(), "0".into()];
            }
            "mv" => {
                if !need(&mut errors, &mnemonic, &ops, 2, "mv rd, rs") {
                    continue;
                }
                ops = vec![ops[0].clone(), ops[1].clone(), "0".into()];
                mnemonic = "addi".into();
            }
            "inc" => {
                if !need(&mut errors, &mnemonic, &ops, 1, "inc rd") {
                    continue;
                }
                ops = vec![ops[0].clone(), ops[0].clone(), "1".into()];
                mnemonic = "addi".into();
            }
            "dec" => {
                if !need(&mut errors, &mnemonic, &ops, 1, "dec rd") {
                    continue;
                }
                ops = vec![ops[0].clone(), ops[0].clone(), "-1".into()];
                mnemonic = "addi".into();
            }
            "beqz" | "bnez" => {
                let usage = format!("{mnemonic} r, метка");
                if !need(&mut errors, &mnemonic, &ops, 2, &usage) {
                    continue;
                }
                ops = vec![ops[0].clone(), "r0".into(), ops[1].clone()];
                mnemonic = if mnemonic == "beqz" { "beq" } else { "bne" }.into();
            }
            "bgtu" | "bleu" => {
                let usage = format!("{mnemonic} ra, rb, метка");
                if !need(&mut errors, &mnemonic, &ops, 3, &usage) {
                    continue;
                }
                ops = vec![ops[1].clone(), ops[0].clone(), ops[2].clone()];
                mnemonic = if mnemonic == "bgtu" { "bltu" } else { "bgeu" }.into();
            }
            "j" => {
                if !need(&mut errors, &mnemonic, &ops, 1, "j метка") {
                    continue;
                }
                mnemonic = "jmp".into();
            }
            _ => {}
        }

        let Some(def) = op_by_mnemonic(&mnemonic) else {
            fail(&mut errors, line, format!("Неизвестная команда «{}»", p.mnemonic));
            continue;
        };

        let Some(word) = encode(def, &ops, addr, line, &labels, &equ, &mut errors) else {
            continue;
        };
        words.push(word);
        lines.push(AsmLine { line, addr, word, text: p.text.clone() });
    }

    AsmResult { words, lines, labels, errors }
}

struct Enc<'a> {
    def: &'a OpDef,
    ops: &'a [String],
    addr: usize,
    line: usize,
    labels: &'a HashMap<String, usize>,
    equ: &'a HashMap<String, f64>,
}

impl Enc<'_> {
    fn err(&self, errors: &mut Vec<AsmError>, message: String) {
        errors.push(AsmError { line: self.line, message });
    }

    fn reg(&self, errors: &mut Vec<AsmError>, token: Option<&str>) -> Option<u16> {
        let r = token.and_then(parse_reg);
        if r.is_none() {
            self.err(errors, format!("Ожидался регистр r0…r7, а здесь «{}»", token.unwrap_or("")));
        }
        r
    }

    fn num(&self, errors: &mut Vec<AsmError>, token: Option<&str>, min: i32, max: i32, what: &str) -> Option<i32> {
        let Some(v) = token.and_then(|t| parse_number(t, self.equ)) else {
            self.err(errors, format!("Ожидалось число, а здесь «{}»", token.unwrap_or("")));
            return None;
        };
        if v < min as f64 || v > max as f64 {
            self.err(errors, format!("{what}: {} не помещается — допустимо от {min} до {max}", show_num(v)));
            return None;
        }
        Some(v as i32)
    }

    fn count(&self, errors: &mut Vec<AsmError>, n: usize, usage: &str) -> bool {
        if self.ops.len() == n {
            return true;
        }
        self.err(errors, format!("«{}» принимает {n} {}: {usage}", self.def.mnemonic, plural(n)));
        false
    }

    /// Смещение до метки (или числом) — в командах от самой этой команды.
    fn target(&self, errors: &mut Vec<AsmError>, token: &str, bits: u32) -> Option<i32> {
        let off: f64 = if let Some(l) = self.labels.get(token) {
            *l as f64 - self.addr as f64
        } else {
            match parse_number(token, self.equ) {
                Some(n) => n,
                None => {
                    let msg = if is_ident(token) { format!("Нет метки «{token}»") } else { format!("Ожидалась метка, а здесь «{token}»") };
                    self.err(errors, msg);
                    return None;
                }
            }
        };
        let lim = 1i32 << (bits - 1);
        if off < -(lim as f64) || off >= lim as f64 {
            self.err(errors, format!("Метка «{token}» слишком далеко ({} команд); можно от {} до {}", show_num(off), -lim, lim - 1));
            return None;
        }
        Some(off as i32)
    }
}

/// Разбор `смещение(регистр)` как регулярка `^(.*)\(\s*([^)]+?)\s*\)$`: последняя `(`, после которой до
/// конца нет других `)`; в скобках должен быть хотя бы один символ.
fn split_mem(text: &str) -> Option<(String, String)> {
    let chars: Vec<char> = text.chars().collect();
    if chars.last() != Some(&')') {
        return None;
    }
    let end = chars.len() - 1;
    for idx in (0..end).rev().filter(|i| chars[*i] == '(') {
        let inner: String = chars[idx + 1..end].iter().collect();
        if inner.is_empty() || inner.contains(')') {
            continue;
        }
        let trimmed = inner.trim();
        let core = if trimmed.is_empty() { inner.chars().last().map(String::from).unwrap_or_default() } else { trimmed.to_string() };
        return Some((chars[..idx].iter().collect(), core));
    }
    None
}

fn encode(
    def: &OpDef,
    ops: &[String],
    addr: usize,
    line: usize,
    labels: &HashMap<String, usize>,
    equ: &HashMap<String, f64>,
    errors: &mut Vec<AsmError>,
) -> Option<u16> {
    let e = Enc { def, ops, addr, line, labels, equ };
    let op = |i: usize| ops.get(i).map(String::as_str);
    match def.format {
        Format::None => e.count(errors, 0, def.mnemonic).then(|| pack(def.opcode, 0, 0, 0)),
        Format::Li => {
            if !e.count(errors, 2, "li rd, число") {
                return None;
            }
            let rd = e.reg(errors, op(0));
            let v = e.num(errors, op(1), -128, 255, "Число");
            Some((def.opcode << 12) | (rd? << 9) | (v? & 0xff) as u16)
        }
        Format::R => {
            if !e.count(errors, 3, &format!("{} rd, rs, rt", def.mnemonic)) {
                return None;
            }
            let (rd, rs, rt) = (e.reg(errors, op(0)), e.reg(errors, op(1)), e.reg(errors, op(2)));
            Some(pack(def.opcode, rd?, rs?, rt? as i32))
        }
        Format::I => {
            if !e.count(errors, 3, &format!("{} rd, rs, число", def.mnemonic)) {
                return None;
            }
            let (rd, rs) = (e.reg(errors, op(0)), e.reg(errors, op(1)));
            let v = e.num(errors, op(2), -32, 31, "Число");
            Some(pack(def.opcode, rd?, rs?, v?))
        }
        Format::Mem => {
            if !e.count(errors, 2, &format!("{} rd, смещение(rs)", def.mnemonic)) {
                return None;
            }
            let rd = e.reg(errors, op(0));
            let Some((off_text, reg_text)) = split_mem(&ops[1]) else {
                e.err(errors, format!("Адрес пишется как смещение(регистр), например 0(r2), а здесь «{}»", ops[1]));
                return None;
            };
            let rs = e.reg(errors, Some(&reg_text));
            let off = if off_text.trim().is_empty() { Some(0) } else { e.num(errors, Some(&off_text), -32, 31, "Смещение") };
            Some(pack(def.opcode, rd?, rs?, off?))
        }
        Format::Branch => {
            if !e.count(errors, 3, &format!("{} ra, rb, метка", def.mnemonic)) {
                return None;
            }
            let (ra, rb) = (e.reg(errors, op(0)), e.reg(errors, op(1)));
            let off = e.target(errors, &ops[2], 6);
            Some(pack(def.opcode, ra?, rb?, off?))
        }
        Format::Jump => {
            if !e.count(errors, 1, "jmp метка") {
                return None;
            }
            let off = e.target(errors, &ops[0], 12)?;
            Some((def.opcode << 12) | (off & 0xfff) as u16)
        }
    }
}
