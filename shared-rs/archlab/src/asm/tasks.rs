//! Сверка диска с ожидаемым после остановки: итог и разбор расхождения понятным языком
//! (`compare` и `show` из `tasks.ts`).

use super::isa::MEM_SIZE;
use serde::{Deserialize, Serialize};

/// Итог проверки.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CheckResult {
    pub ok: bool,
    pub message: String,
}

/// `0x0A`: два знака, заглавные.
pub fn hex(n: u8) -> String {
    format!("0x{n:02X}")
}

fn show(b: u8) -> String {
    if (32..127).contains(&b) {
        format!("{} «{}»", hex(b), b as char)
    } else {
        hex(b)
    }
}

/// Сравнение памяти с ожидаемой: первое расхождение понятным языком.
pub fn compare(mem: &[u8], expected: &[u8]) -> CheckResult {
    let at = |s: &[u8], i: usize| s.get(i).copied().unwrap_or(0);
    let diffs: Vec<usize> = (0..MEM_SIZE).filter(|i| mem.get(*i) != expected.get(*i)).collect();
    let Some(&first) = diffs.first() else {
        return CheckResult { ok: true, message: "Диск совпал с ожидаемым — задание выполнено!".into() };
    };
    let more = if diffs.len() > 1 {
        format!(" (и ещё {} {})", diffs.len() - 1, if diffs.len() == 2 { "байт" } else { "байт(а)" })
    } else {
        String::new()
    };
    CheckResult {
        ok: false,
        message: format!("Адрес {}: ожидалось {}, а лежит {}{more}", hex(first as u8), show(at(expected, first)), show(at(mem, first))),
    }
}
