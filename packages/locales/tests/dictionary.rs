//! The dictionary and the code do not diverge: every key from `tr("…")`, `trf!("…")`, `plural(n, "…", "…")` and `tr_dyn` server messages is in the dictionary,
//! the dictionary has no unused entries, and the placeholders and plural forms in a translation agree with its key.

use std::{collections::BTreeSet, fs, path::Path};

/// All entries of the Russian dictionary (English key, translation) in area order — taken from the JSON files themselves, to also catch a key
/// repeated in two areas (after loading into `i18n` such entries would silently merge).
fn entries() -> Vec<(String, String)> {
    let mut out = Vec::new();
    for (area, json) in locales::RU {
        let map: serde_json::Map<String, serde_json::Value> = serde_json::from_str(json).unwrap_or_else(|e| panic!("ru/{area}.json: {e}"));
        // the file is formatted one entry per line: a key repeated inside a file would be swallowed by the JSON parser
        let lines = json.lines().filter(|l| l.starts_with("  \"")).count();
        assert_eq!(lines, map.len(), "ru/{area}.json: повтор ключа внутри файла");
        for (k, v) in map {
            let v = v.as_str().unwrap_or_else(|| panic!("ru/{area}.json: {k:?} не строка")).to_string();
            out.push((k, v));
        }
    }
    out
}

/// All `.rs` files of a directory.
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

/// The string literal that starts right after `from` in `text`: its value, honouring `\"`, `\\` and `\n`.
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

/// Source directories where keys occur (relative to the repository root).
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

/// Template placeholders: `{}`, `{0}`, `{1}` — in order of appearance.
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

/// Keys the code requests from the dictionary.
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
                    // plural(n, "one", "many"): two literals after the first comma
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
    let all = entries();
    let have: BTreeSet<&str> = all.iter().map(|(k, _)| k.as_str()).collect();
    let missing: Vec<_> = used_keys().into_iter().filter(|k| !have.contains(k.as_str())).collect();
    assert!(missing.is_empty(), "нет перевода для ключей: {missing:#?}");
}

/// Server messages (`ApiError`, check errors) arrive in English, and engine tables (`&'static str` in `const`) keep keys
/// as plain literals and translate them when shown: such keys are searched for across all sources.
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
    for (key, value) in entries() {
        let (key, value) = (key.as_str(), value.as_str());
        assert!(seen.insert(key.to_string()), "дубликат ключа {key:?}");
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
