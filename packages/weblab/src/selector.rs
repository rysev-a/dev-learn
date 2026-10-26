//! Специфичность селекторов и упражнения «напишите селектор».

use std::collections::BTreeSet;

use crate::html::{selector, Doc};
use crate::spec::{Item, Task};

/// Специфичность (идентификаторы, классы/атрибуты/псевдоклассы, типы/псевдоэлементы). Для списка через запятую — наибольшая.
pub fn specificity(sel: &str) -> [u32; 3] {
    split_top(sel, ',').iter().map(|s| one(s)).max().unwrap_or([0, 0, 0])
}

fn add(a: &mut [u32; 3], b: [u32; 3]) {
    for i in 0..3 {
        a[i] += b[i];
    }
}

/// Делит по символу вне скобок и кавычек.
fn split_top(s: &str, sep: char) -> Vec<String> {
    let (mut out, mut cur, mut depth, mut quote) = (Vec::new(), String::new(), 0i32, None::<char>);
    for c in s.chars() {
        match quote {
            Some(q) => {
                cur.push(c);
                if c == q {
                    quote = None;
                }
            }
            None => match c {
                '"' | '\'' => {
                    quote = Some(c);
                    cur.push(c);
                }
                '(' | '[' => {
                    depth += 1;
                    cur.push(c);
                }
                ')' | ']' => {
                    depth -= 1;
                    cur.push(c);
                }
                c if c == sep && depth == 0 => out.push(std::mem::take(&mut cur)),
                _ => cur.push(c),
            },
        }
    }
    out.push(cur);
    out.into_iter().filter(|s| !s.trim().is_empty()).collect()
}

fn ident_end(chars: &[char], mut i: usize) -> usize {
    while i < chars.len() && (chars[i].is_alphanumeric() || chars[i] == '-' || chars[i] == '_' || chars[i] == '\\') {
        i += 1;
    }
    i
}

/// Специфичность одного сложного селектора.
fn one(sel: &str) -> [u32; 3] {
    let chars: Vec<char> = sel.trim().chars().collect();
    let mut sp = [0u32; 3];
    let mut i = 0;
    while i < chars.len() {
        match chars[i] {
            '#' => {
                sp[0] += 1;
                i = ident_end(&chars, i + 1);
            }
            '.' => {
                sp[1] += 1;
                i = ident_end(&chars, i + 1);
            }
            '[' => {
                sp[1] += 1;
                let mut q = None::<char>;
                while i < chars.len() {
                    let c = chars[i];
                    match q {
                        Some(x) if c == x => q = None,
                        Some(_) => {}
                        None if c == '"' || c == '\'' => q = Some(c),
                        None if c == ']' => break,
                        None => {}
                    }
                    i += 1;
                }
                i += 1;
            }
            ':' => {
                let double = chars.get(i + 1) == Some(&':');
                let start = i + if double { 2 } else { 1 };
                let end = ident_end(&chars, start);
                let name: String = chars[start..end].iter().collect::<String>().to_lowercase();
                i = end;
                let mut arg = None;
                if chars.get(i) == Some(&'(') {
                    let mut depth = 0;
                    let a = i + 1;
                    while i < chars.len() {
                        match chars[i] {
                            '(' => depth += 1,
                            ')' => {
                                depth -= 1;
                                if depth == 0 {
                                    break;
                                }
                            }
                            _ => {}
                        }
                        i += 1;
                    }
                    arg = Some(chars[a..i.min(chars.len())].iter().collect::<String>());
                    i += 1;
                }
                if double || matches!(name.as_str(), "before" | "after" | "first-line" | "first-letter") {
                    sp[2] += 1;
                } else {
                    match (name.as_str(), arg) {
                        ("where", _) => {}
                        ("not" | "is" | "has" | "matches" | "-webkit-any" | "-moz-any", Some(a)) => add(&mut sp, specificity(&a)),
                        ("nth-child" | "nth-last-child", Some(a)) => {
                            sp[1] += 1;
                            if let Some(pos) = a.find(" of ") {
                                add(&mut sp, specificity(&a[pos + 4..]));
                            }
                        }
                        _ => sp[1] += 1,
                    }
                }
            }
            '*' => i += 1,
            '|' => i += 1,
            c if c.is_alphabetic() => {
                sp[2] += 1;
                i = ident_end(&chars, i);
            }
            _ => i += 1,
        }
    }
    sp
}

/// Есть ли в тексте селекторов `#id` (вне строк и скобок атрибутов).
pub fn has_id(sel: &str) -> bool {
    let (mut quote, mut attr) = (None::<char>, false);
    for c in sel.chars() {
        match quote {
            Some(q) => {
                if c == q {
                    quote = None;
                }
            }
            None => match c {
                '"' | '\'' => quote = Some(c),
                '[' => attr = true,
                ']' => attr = false,
                '#' if !attr => return true,
                _ => {}
            },
        }
    }
    false
}

fn label(el: &scraper::ElementRef) -> String {
    match el.value().attr("id") {
        Some(id) => format!("#{id}"),
        None => format!("<{}>", el.value().name()),
    }
}

/// Упражнение «селектор»: должен выбрать ровно элементы с `id` из `want` (и ничего больше).
pub fn check_selector(task: &Task, answer: &str) -> Vec<Item> {
    let mut items = Vec::new();
    let answer = answer.trim();
    let parsed = if answer.is_empty() { Err("селектор не написан".to_string()) } else { selector(answer) };
    items.push(Item { text: "Селектор записан верно".into(), ok: parsed.is_ok(), detail: parsed.as_ref().err().cloned().unwrap_or_default() });
    let Ok(sel) = parsed else { return items };
    let doc = Doc::parse(&task.html);
    let got: Vec<scraper::ElementRef> = doc.html.select(&sel).collect();
    let got_ids: BTreeSet<String> = got.iter().map(label).collect();
    let want: BTreeSet<String> = task.want.iter().map(|w| format!("#{w}")).collect();
    let missing: Vec<&String> = want.difference(&got_ids).collect();
    let extra: Vec<&String> = got_ids.difference(&want).collect();
    let detail = [
        (!missing.is_empty()).then(|| format!("не выбраны: {}", missing.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", "))),
        (!extra.is_empty()).then(|| format!("лишние: {}", extra.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", "))),
    ]
    .into_iter()
    .flatten()
    .collect::<Vec<_>>()
    .join("; ");
    items.push(Item { text: format!("Выбирает ровно {}", want.iter().cloned().collect::<Vec<_>>().join(", ")), ok: missing.is_empty() && extra.is_empty(), detail });
    if let Some(max) = task.max_specificity {
        let sp = specificity(answer);
        items.push(Item {
            text: format!("Специфичность не выше ({}, {}, {})", max[0], max[1], max[2]),
            ok: sp <= max,
            detail: format!("у вашего селектора ({}, {}, {})", sp[0], sp[1], sp[2]),
        });
    }
    items
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn specificity_of_common_selectors() {
        assert_eq!(specificity("p"), [0, 0, 1]);
        assert_eq!(specificity(".a.b"), [0, 2, 0]);
        assert_eq!(specificity("#nav a:hover"), [1, 1, 1]);
        assert_eq!(specificity("ul li::before"), [0, 0, 3]);
        assert_eq!(specificity("a[href^='http'] .x"), [0, 2, 1]);
        assert_eq!(specificity(":not(#a, .b)"), [1, 0, 0]);
        assert_eq!(specificity(":where(#a) p"), [0, 0, 1]);
        assert_eq!(specificity("li:nth-child(2n+1)"), [0, 1, 1]);
        assert_eq!(specificity("*"), [0, 0, 0]);
        assert_eq!(specificity(".a, #b"), [1, 0, 0]);
        assert_eq!(specificity("form > input:focus + label"), [0, 1, 3]);
    }

    #[test]
    fn ids_are_found_outside_attributes() {
        assert!(has_id("#a .b"));
        assert!(!has_id("[href='#top']"));
        assert!(!has_id(".a > .b"));
    }
}
