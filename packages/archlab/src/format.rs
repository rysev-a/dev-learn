//! Канонический вид файлов данных: JSON с отступами, но короткие массивы чисел и строк — в одну строку
//! (таблицы истинности, списки входов), чтобы файлы читались и не раздувались.

use serde::Serialize;

/// Длина строки, до которой массив сворачивается в одну строку.
const INLINE_MAX: usize = 100;

fn is_scalar_line(line: &str) -> bool {
    let t = line.trim_start();
    t.starts_with('"') || t.starts_with(|c: char| c.is_ascii_digit() || c == '-') || t.starts_with("null") || t.starts_with("true") || t.starts_with("false")
}

fn is_inline_array_line(line: &str) -> bool {
    let t = line.trim_end_matches(',');
    t.trim_start().starts_with('[') && t.ends_with(']')
}

/// Сворачивает массивы, все элементы которых — скаляры или уже свёрнутые массивы, если строка выходит короткой.
pub fn compact(pretty: &str) -> String {
    let mut lines: Vec<String> = pretty.lines().map(str::to_string).collect();
    loop {
        let mut changed = false;
        let mut i = 0;
        while i < lines.len() {
            if lines[i].ends_with('[') {
                let indent = lines[i].len() - lines[i].trim_start().len();
                let close_a = format!("{}]", " ".repeat(indent));
                let close_b = format!("{}],", " ".repeat(indent));
                let mut j = i + 1;
                let mut ok = true;
                while j < lines.len() && lines[j] != close_a && lines[j] != close_b {
                    if !(is_scalar_line(&lines[j]) || is_inline_array_line(&lines[j])) || lines[j].ends_with('{') {
                        ok = false;
                        break;
                    }
                    j += 1;
                }
                if ok && j < lines.len() && j > i + 1 {
                    let items: Vec<String> = lines[i + 1..j].iter().map(|l| l.trim().trim_end_matches(',').to_string()).collect();
                    let tail = if lines[j] == close_b { "]," } else { "]" };
                    let joined = format!("{}{}{}", lines[i], items.join(", "), tail);
                    if joined.chars().count() <= INLINE_MAX {
                        lines.splice(i..=j, [joined]);
                        changed = true;
                    }
                }
            }
            i += 1;
        }
        if !changed {
            break;
        }
    }
    let mut out = lines.join("\n");
    out.push('\n');
    out
}

/// Канонический JSON значения: с отступами, короткие массивы в строку, перевод строки в конце.
pub fn canonical_json<T: Serialize>(v: &T) -> Result<String, serde_json::Error> {
    Ok(compact(&serde_json::to_string_pretty(v)?))
}
