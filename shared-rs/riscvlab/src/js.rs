//! Мелкие помощники, повторяющие поведение JavaScript там, где от него зависит результат
//! (какие символы считаются пробелами, как печатается строка в JSON, имена в ассемблере).

/// Пробел в смысле JavaScript (`\s`, `String.prototype.trim`).
pub fn is_space(c: char) -> bool {
    matches!(
        c,
        '\u{9}' | '\u{a}' | '\u{b}' | '\u{c}' | '\u{d}' | ' ' | '\u{a0}' | '\u{1680}' | '\u{2000}'
            ..='\u{200a}' | '\u{2028}' | '\u{2029}' | '\u{202f}' | '\u{205f}' | '\u{3000}' | '\u{feff}'
    )
}

/// То же для кода UTF-16 (суррогаты пробелами не бывают).
pub fn is_space_unit(u: u16) -> bool {
    char::from_u32(u32::from(u)).is_some_and(is_space)
}

/// `str.trim()` из JavaScript.
pub fn trim(s: &str) -> &str {
    s.trim_matches(is_space)
}

/// Конец строки в смысле JavaScript: символ, которого не принимает `.` в регулярных выражениях.
pub fn is_line_terminator(c: char) -> bool {
    matches!(c, '\n' | '\r' | '\u{2028}' | '\u{2029}')
}

/// Есть ли в тексте символы конца строки.
pub fn has_line_terminator(s: &str) -> bool {
    s.chars().any(is_line_terminator)
}

/// Начало имени метки или константы: латиница, кириллица, `_ . $`.
pub fn is_ident_start(c: char) -> bool {
    c.is_ascii_alphabetic() || is_cyr(c) || matches!(c, '_' | '.' | '$')
}

/// Продолжение имени: то же плюс цифры.
pub fn is_ident_char(c: char) -> bool {
    is_ident_start(c) || c.is_ascii_digit()
}

fn is_cyr(c: char) -> bool {
    matches!(c, '\u{410}'..='\u{44f}' | '\u{401}' | '\u{451}')
}

/// Подходит ли весь текст под имя.
pub fn is_ident(s: &str) -> bool {
    let mut it = s.chars();
    it.next().is_some_and(is_ident_start) && it.all(is_ident_char)
}

/// `JSON.stringify(строка)`.
pub fn json_quote(s: &str) -> String {
    serde_json::to_string(s).unwrap_or_else(|_| format!("\"{s}\""))
}

/// Шестнадцатеричная запись слова: `0x` и восемь цифр.
pub fn hex32(n: u32) -> String {
    format!("0x{n:08x}")
}

/// `str.replace(/^[+-]\s*/, '')`: убрать один знак в начале и пробелы за ним.
pub fn trim_start_sign(s: &str) -> &str {
    match s.strip_prefix(['+', '-']) {
        Some(rest) => rest.trim_start_matches(is_space),
        None => s,
    }
}
