//! Multi-language interface without any texts inside: the translation key is the English text (`tr("Sign in")`), the application
//! loads its dictionaries itself at startup ([`load_json`] / [`extend`]) from its own JSON files. An unknown key is shown as is (the English
//! text), so a gap in the dictionary never breaks the screen.
//!
//! The language is chosen once at startup ([`set_locale`]) and usually changes with a page reload, so `tr` reads it without
//! subscribing to a signal; on the server the request language is enabled for the duration of a call ([`with_locale`]). The crate is project-agnostic:
//! it can be used in any service together with that service's own set of JSON dictionaries.
//!
//! Dictionary format — a flat JSON object: `{"Sign in": "Войти", "row|rows": "строка|строки|строк"}`. A key with `|` holds plural forms
//! ([`plural`]): two forms — the English rule (1 / the rest), three — the Russian rule (1 / 2–4 / 5+, with the 11–14 exception).

use std::{
    collections::HashMap,
    fmt::{Display, Write},
    sync::{
        atomic::{AtomicU8, Ordering},
        RwLock,
    },
};

/// Interface language. The base language is English: its texts are the keys, so it needs no dictionary.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Locale {
    En,
    Ru,
}

impl Locale {
    pub const ALL: [Locale; 2] = [Locale::En, Locale::Ru];

    /// Code for `localStorage`, `<html lang>` and the `Accept-Language` header.
    pub fn code(self) -> &'static str {
        match self {
            Locale::En => "en",
            Locale::Ru => "ru",
        }
    }

    /// Name in the language itself (for the language picker).
    pub fn native_name(self) -> &'static str {
        match self {
            Locale::En => "English",
            Locale::Ru => "Русский",
        }
    }

    /// `ru`, `ru-RU`, `en_US` → language; an unknown tag — `None`.
    pub fn parse(tag: &str) -> Option<Locale> {
        let primary = tag.trim().split(['-', '_']).next()?.to_ascii_lowercase();
        Locale::ALL.into_iter().find(|l| l.code() == primary)
    }

    /// Choice at startup: the stored language wins over the browser language; otherwise English.
    pub fn detect(stored: Option<&str>, browser: Option<&str>) -> Locale {
        stored
            .and_then(Locale::parse)
            .or_else(|| browser.and_then(Locale::parse))
            .unwrap_or(Locale::En)
    }

    fn index(self) -> usize {
        self as usize
    }
}

static CURRENT: AtomicU8 = AtomicU8::new(0);

thread_local! {
    /// Language for the duration of a [`with_locale`] call: the server checks solutions in the request language, while the process language is shared by everyone.
    static OVERRIDE: std::cell::Cell<Option<Locale>> = const { std::cell::Cell::new(None) };
}

/// Current language (English until [`set_locale`]; inside [`with_locale`] — the one set there).
pub fn locale() -> Locale {
    if let Some(l) = OVERRIDE.with(std::cell::Cell::get) {
        return l;
    }
    match CURRENT.load(Ordering::Relaxed) {
        1 => Locale::Ru,
        _ => Locale::En,
    }
}

/// Language guard: while it lives, the given language is active in the current thread (tests that compare Russian texts).
pub struct LocaleGuard(Option<Locale>);

impl Drop for LocaleGuard {
    fn drop(&mut self) {
        OVERRIDE.with(|o| o.set(self.0));
    }
}

/// Enables the language until the end of the guard's scope.
#[must_use]
pub fn guard(locale: Locale) -> LocaleGuard {
    LocaleGuard(OVERRIDE.with(|o| o.replace(Some(locale))))
}

/// Runs `f` with another language in the current thread: lab engines on the server report rejection reasons in the request language.
pub fn with_locale<T>(locale: Locale, f: impl FnOnce() -> T) -> T {
    let before = OVERRIDE.with(|o| o.replace(Some(locale)));
    let out = f();
    OVERRIDE.with(|o| o.set(before));
    out
}

pub fn set_locale(locale: Locale) {
    CURRENT.store(locale.index() as u8, Ordering::Relaxed);
}

// --- dictionaries ----------------------------------------------------------------------------

type Dict = HashMap<&'static str, &'static str>;

/// Dictionaries per language. The strings live until the program ends (a dictionary is loaded once), so `tr` returns `&'static str`.
fn dicts() -> &'static RwLock<Vec<Dict>> {
    static DICTS: std::sync::OnceLock<RwLock<Vec<Dict>>> = std::sync::OnceLock::new();
    DICTS.get_or_init(|| RwLock::new(Locale::ALL.iter().map(|_| Dict::new()).collect()))
}

fn leak(s: &str) -> &'static str {
    Box::leak(s.to_owned().into_boxed_str())
}

/// Adds entries to a language's dictionary (a repeated key replaces the previous one). Returns the number of entries added.
pub fn extend<'a>(locale: Locale, pairs: impl IntoIterator<Item = (&'a str, &'a str)>) -> usize {
    let mut all = dicts().write().unwrap_or_else(|e| e.into_inner());
    let dict = &mut all[locale.index()];
    let mut n = 0;
    for (k, v) in pairs {
        dict.insert(leak(k), leak(v));
        n += 1;
    }
    n
}

/// Loads a dictionary from a JSON object `{"key": "translation"}`; may be called several times (one file per area), entries merge.
pub fn load_json(locale: Locale, text: &str) -> Result<usize, String> {
    let value: serde_json::Value =
        serde_json::from_str(text).map_err(|e| format!("dictionary is not valid JSON: {e}"))?;
    let obj = value
        .as_object()
        .ok_or_else(|| "dictionary must be a JSON object".to_string())?;
    let mut pairs = Vec::with_capacity(obj.len());
    for (k, v) in obj {
        let v = v
            .as_str()
            .ok_or_else(|| format!("translation of {k:?} must be a string"))?;
        pairs.push((k.as_str(), v));
    }
    Ok(extend(locale, pairs))
}

/// All entries of a language's dictionary (for completeness checks).
pub fn entries(locale: Locale) -> Vec<(&'static str, &'static str)> {
    let all = dicts().read().unwrap_or_else(|e| e.into_inner());
    all[locale.index()].iter().map(|(k, v)| (*k, *v)).collect()
}

fn lookup(locale: Locale, key: &str) -> Option<&'static str> {
    if locale == Locale::En {
        return None;
    }
    let all = dicts().read().unwrap_or_else(|e| e.into_inner());
    all[locale.index()].get(key).copied()
}

/// Translation by the English text key. For English and for keys without a translation returns the key itself.
pub fn tr(key: &'static str) -> &'static str {
    lookup(locale(), key).unwrap_or(key)
}

/// [`tr`] for text that is not a literal in the code (server messages): without a translation returns it as is.
pub fn tr_dyn(key: &str) -> String {
    lookup(locale(), key).map_or_else(|| key.to_string(), str::to_string)
}

/// Substitutes values into a template: `{}` — in order, `{0}`, `{1}` — by number (word order differs between languages).
pub fn format_dyn(template: &str, args: &[&dyn Display]) -> String {
    let mut out = String::with_capacity(template.len() + 8);
    let mut next = 0;
    let mut chars = template.chars();
    while let Some(c) = chars.next() {
        if c == '}' {
            // `}}` — a literal brace
            if chars.clone().next() == Some('}') {
                chars.next();
            }
            out.push('}');
            continue;
        }
        if c != '{' {
            out.push(c);
            continue;
        }
        if chars.clone().next() == Some('{') {
            chars.next();
            out.push('{');
            continue;
        }
        let mut name = String::new();
        for d in chars.by_ref() {
            if d == '}' {
                break;
            }
            name.push(d);
        }
        let n = if name.is_empty() {
            next += 1;
            next - 1
        } else {
            name.parse().unwrap_or(usize::MAX)
        };
        if let Some(arg) = args.get(n) {
            let _ = write!(out, "{arg}");
        }
    }
    out
}

/// Marks a translation key where [`tr`] cannot be called (constants and static tables): yields the literal itself, and it must be
/// shown through `tr(…)`. The dictionary and the completeness test count such keys as used.
#[macro_export]
macro_rules! t {
    ($key:literal) => {
        $key
    };
}

/// `trf!("Solved {} of {}", done, total)` — translates the template and substitutes the values.
#[macro_export]
macro_rules! trf {
    ($key:literal $(, $arg:expr)* $(,)?) => {
        $crate::format_dyn($crate::tr($key), &[$(&$arg as &dyn ::core::fmt::Display),*])
    };
}

/// A word in the right plural form. The key is `"one|many"` in English; the dictionary gives forms separated by `|`: two — the English rule
/// (1 / the rest), three — the Russian rule (1, 2–4, 5+; 11–14 — the third form). Without a dictionary entry — the English rule on the key.
pub fn plural(n: u64, one: &'static str, many: &'static str) -> &'static str {
    let english = if n == 1 { one } else { many };
    let Some(forms) = lookup(locale(), &format!("{one}|{many}")) else {
        return english;
    };
    let forms: Vec<&'static str> = forms.split('|').collect();
    match forms.len() {
        2 => forms[usize::from(n != 1)],
        3 => {
            let (n10, n100) = (n % 10, n % 100);
            let pick = if n10 == 1 && n100 != 11 {
                0
            } else if (2..=4).contains(&n10) && !(12..=14).contains(&n100) {
                1
            } else {
                2
            };
            forms[pick]
        }
        _ => english,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn detects_locale() {
        assert_eq!(Locale::detect(Some("ru"), Some("en-US")), Locale::Ru);
        assert_eq!(Locale::detect(None, Some("ru-RU")), Locale::Ru);
        assert_eq!(Locale::detect(Some("de"), Some("en-GB")), Locale::En);
        assert_eq!(Locale::detect(None, Some("de")), Locale::En);
        assert_eq!(Locale::detect(None, None), Locale::En);
    }

    #[test]
    fn dictionary_is_loaded_from_json_and_used_for_plurals() {
        assert_eq!(
            load_json(
                Locale::Ru,
                r#"{"Loading…": "Загрузка…", "{} of {}": "{} из {}", "row|rows": "строка|строки|строк"}"#
            ),
            Ok(3)
        );
        assert!(load_json(Locale::Ru, "[1]").is_err());
        assert!(load_json(Locale::Ru, r#"{"a": 1}"#).is_err());
        // one guard for all checks: the process language is shared, the guard is per thread
        let _ru = guard(Locale::Ru);
        assert_eq!(tr("Loading…"), "Загрузка…");
        assert_eq!(
            tr("Unknown key"),
            "Unknown key",
            "without a translation the key is returned as is"
        );
        assert_eq!(tr_dyn("Loading…"), "Загрузка…");
        assert_eq!(trf!("{} of {}", 1, 2), "1 из 2");
        let forms: Vec<_> = [1, 2, 4, 5, 11, 12, 21, 22, 25, 111]
            .into_iter()
            .map(|n| plural(n, "row", "rows"))
            .collect();
        assert_eq!(
            forms,
            [
                "строка",
                "строки",
                "строки",
                "строк",
                "строк",
                "строк",
                "строка",
                "строки",
                "строк",
                "строк"
            ]
        );
        assert_eq!(
            plural(2, "cat", "cats"),
            "cats",
            "no entry: the English rule applies"
        );
        assert!(entries(Locale::Ru).len() >= 3);
    }

    #[test]
    fn english_is_the_base_language() {
        let _en = guard(Locale::En);
        assert_eq!(
            (
                plural(1, "row", "rows"),
                plural(0, "row", "rows"),
                plural(5, "row", "rows")
            ),
            ("row", "rows", "rows")
        );
        assert_eq!(tr("Loading…"), "Loading…");
    }

    #[test]
    fn formats_placeholders() {
        assert_eq!(format_dyn("{} of {}", &[&3, &"ten"]), "3 of ten");
        assert_eq!(format_dyn("{1} / {0}", &[&1, &2]), "2 / 1");
        assert_eq!(format_dyn("no placeholders", &[]), "no placeholders");
        assert_eq!(format_dyn("{{\"a\": {0}}}", &[&1]), "{\"a\": 1}");
    }
}
