//! Словарь и код не расходятся: каждый ключ из `tr("…")`, `trf!("…")`, `plural(n, "…", "…")` и `tr_dyn`-сообщений сервера есть в словаре,
//! в словаре нет лишних записей, а подстановки и формы числа в переводе согласованы с ключом.

use std::{collections::BTreeSet, fs, path::Path};


/// Все `.rs`-файлы каталога.
fn sources(dir: &Path, out: &mut Vec<String>) {
    for entry in fs::read_dir(dir).unwrap().flatten() {
        let path = entry.path();
        if path.is_dir() {
            if path.file_name().is_some_and(|n| n != "target") {
                sources(&path, out);
            }
        } else if path.extension().is_some_and(|e| e == "rs") {
            out.push(fs::read_to_string(&path).unwrap());
        }
    }
}

/// Строковый литерал, начинающийся сразу после `from` в `text`: значение с учётом `\"`, `\\` и `\n`.
fn literal_after(text: &str) -> Option<(String, &str)> {
    let rest = text.trim_start().strip_prefix('"')?;
    let mut value = String::new();
    let mut chars = rest.char_indices();
    while let Some((i, c)) = chars.next() {
        match c {
            '"' => return Some((value, &rest[i + 1..])),
            '\\' => match chars.next()?.1 {
                'n' => value.push('\n'),
                't' => value.push('\t'),
                other => value.push(other),
            },
            _ => value.push(c),
        }
    }
    None
}

/// Каталоги исходников, где встречаются ключи (от корня репозитория).
const SOURCES: [&str; 12] = [
    "backend/src",
    "frontend/app/src",
    "frontend/crates/api/src",
    "frontend/crates/scene/src",
    "packages/archlab/src",
    "packages/riscvlab/src",
    "packages/netlab/src",
    "packages/sdlab/src",
    "packages/virtlab/src",
    "packages/weblab/src",
    "packages/content/src",
    "packages/highlight/src",
];

/// Подстановки шаблона: `{}`, `{0}`, `{1}` — по порядку появления.
fn placeholders(text: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut rest = text;
    while let Some(at) = rest.find('{') {
        if rest[at..].starts_with("{{") {
            rest = &rest[at + 2..];
            continue;
        }
        let Some(end) = rest[at..].find('}') else { break };
        let name = &rest[at + 1..at + end];
        if name.chars().all(|c| c.is_ascii_digit()) {
            out.push(name.to_string());
        }
        rest = &rest[at + end + 1..];
    }
    out.sort();
    out
}

/// Ключи, которые код запрашивает у словаря.
fn used_keys() -> BTreeSet<String> {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("..").join("..");
    let mut files = Vec::new();
    for dir in SOURCES {
        sources(&root.join(dir), &mut files);
    }
    let mut keys = BTreeSet::new();
    for text in &files {
        for marker in ["i18n::tr(", "i18n::trf!(", "i18n::plural(", "i18n::t!("] {
            let mut rest = text.as_str();
            while let Some(at) = rest.find(marker) {
                rest = &rest[at + marker.len()..];
                if marker == "i18n::plural(" {
                    // plural(n, "one", "many"): два литерала после первого запятой
                    let Some(comma) = rest.find(',') else { continue };
                    if let Some((one, after)) = literal_after(&rest[comma + 1..]) {
                        if let Some((many, _)) = literal_after(after.trim_start().strip_prefix(',').unwrap_or("")) {
                            keys.insert(format!("{one}|{many}"));
                        }
                    }
                } else if let Some((key, _)) = literal_after(rest) {
                    keys.insert(key);
                }
            }
        }
    }
    keys
}

#[test]
fn every_used_key_is_translated() {
    let have: BTreeSet<&str> = i18n::entries().map(|(k, _)| k).collect();
    let missing: Vec<_> = used_keys().into_iter().filter(|k| !have.contains(k.as_str())).collect();
    assert!(missing.is_empty(), "нет перевода для ключей: {missing:#?}");
}

/// Сообщения сервера (`ApiError`, ошибки проверки) приходят на английском, а таблицы движков (`&'static str` в `const`) хранят ключи
/// просто литералами и переводят их при показе: такие ключи ищем среди всех исходников.
fn backend_source() -> String {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("..").join("..");
    let mut files = Vec::new();
    sources(&root.join("backend/src"), &mut files);
    for dir in SOURCES {
        sources(&root.join(dir), &mut files);
    }
    files.join("\n")
}

#[test]
fn dictionary_has_no_unused_or_broken_entries() {
    let used = used_keys();
    let backend = backend_source();
    let mut seen = BTreeSet::new();
    for (key, value) in i18n::entries() {
        assert!(seen.insert(key), "дубликат ключа {key:?}");
        assert!(!key.chars().any(|c| ('\u{0400}'..='\u{04FF}').contains(&c)), "ключ должен быть английским: {key:?}");
        assert!(!value.is_empty(), "пустой перевод у {key:?}");
        assert!(used.contains(key) || backend.contains(&format!("{key:?}")), "ключ {key:?} не используется в коде");
        if key.contains('|') && !key.contains(' ') {
            assert_eq!(value.split('|').count(), 3, "у {key:?} должно быть три русские формы");
        } else {
            assert_eq!(placeholders(key), placeholders(value), "подстановки в {key:?} и его переводе не совпадают");
        }
    }
}
