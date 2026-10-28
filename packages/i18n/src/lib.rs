//! Интерфейс на двух языках (английский и русский). Ключ перевода — английский текст: в коде везде `tr("Sign in")`, русская
//! версия лежит в словаре [`RU`]. Незнакомый ключ показывается как есть (английский текст), поэтому пропуск в словаре не ломает экран.
//!
//! Язык выбирается один раз при старте (`cs-core-lang` в `localStorage`, иначе язык браузера) и меняется перезагрузкой страницы,
//! поэтому `tr` читает его без подписок на сигнал. Переводятся только неизменные тексты интерфейса: содержимое курса приходит
//! с сервера уже на нужном языке (заголовок `Accept-Language`).

mod ru;

use std::{
    collections::HashMap,
    fmt::{Display, Write},
    sync::{
        atomic::{AtomicU8, Ordering},
        OnceLock,
    },
};

pub use ru::entries;

/// Язык интерфейса.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Locale {
    En,
    Ru,
}

impl Locale {
    pub const ALL: [Locale; 2] = [Locale::En, Locale::Ru];

    /// Код для `localStorage`, `<html lang>` и заголовка `Accept-Language`.
    pub fn code(self) -> &'static str {
        match self {
            Locale::En => "en",
            Locale::Ru => "ru",
        }
    }

    /// Название на самом языке (в списке выбора).
    pub fn native_name(self) -> &'static str {
        match self {
            Locale::En => "English",
            Locale::Ru => "Русский",
        }
    }

    /// `ru`, `ru-RU`, `en_US` → язык; неизвестный тег — `None`.
    pub fn parse(tag: &str) -> Option<Locale> {
        let primary = tag.trim().split(['-', '_']).next()?.to_ascii_lowercase();
        Locale::ALL.into_iter().find(|l| l.code() == primary)
    }

    /// Выбор при старте: сохранённый язык важнее языка браузера; иначе английский.
    pub fn detect(stored: Option<&str>, browser: Option<&str>) -> Locale {
        stored.and_then(Locale::parse).or_else(|| browser.and_then(Locale::parse)).unwrap_or(Locale::En)
    }
}

static CURRENT: AtomicU8 = AtomicU8::new(0);

thread_local! {
    /// Язык на время вызова [`with_locale`]: сервер проверяет решения на языке запроса, а язык процесса у него один на всех.
    static OVERRIDE: std::cell::Cell<Option<Locale>> = const { std::cell::Cell::new(None) };
}

/// Текущий язык (до [`set_locale`] — английский; внутри [`with_locale`] — заданный там).
pub fn locale() -> Locale {
    if let Some(l) = OVERRIDE.with(std::cell::Cell::get) {
        return l;
    }
    if CURRENT.load(Ordering::Relaxed) == 1 {
        Locale::Ru
    } else {
        Locale::En
    }
}

/// Охранник языка: пока он жив, в текущем потоке действует заданный язык (тесты, которые сверяют русские тексты).
pub struct LocaleGuard(Option<Locale>);

impl Drop for LocaleGuard {
    fn drop(&mut self) {
        OVERRIDE.with(|o| o.set(self.0));
    }
}

/// Включает язык до конца области видимости охранника.
#[must_use]
pub fn guard(locale: Locale) -> LocaleGuard {
    LocaleGuard(OVERRIDE.with(|o| o.replace(Some(locale))))
}

/// Выполняет `f` с другим языком в текущем потоке: движки лабораторий на сервере сообщают причины отказа на языке запроса.
pub fn with_locale<T>(locale: Locale, f: impl FnOnce() -> T) -> T {
    let before = OVERRIDE.with(|o| o.replace(Some(locale)));
    let out = f();
    OVERRIDE.with(|o| o.set(before));
    out
}

pub fn set_locale(locale: Locale) {
    CURRENT.store(u8::from(locale == Locale::Ru), Ordering::Relaxed);
}

fn index() -> &'static HashMap<&'static str, &'static str> {
    static INDEX: OnceLock<HashMap<&'static str, &'static str>> = OnceLock::new();
    INDEX.get_or_init(|| entries().collect())
}

/// Перевод по английскому тексту-ключу. Для английского и для ключей без перевода возвращает сам ключ.
pub fn tr(key: &'static str) -> &'static str {
    match locale() {
        Locale::En => key,
        Locale::Ru => index().get(key).copied().unwrap_or(key),
    }
}

/// [`tr`] для текста, которого нет в коде как литерала (сообщения сервера): без перевода возвращает его как есть.
pub fn tr_dyn(key: &str) -> String {
    match locale() {
        Locale::En => key.to_string(),
        Locale::Ru => index().get(key).copied().unwrap_or(key).to_string(),
    }
}

/// Подставляет значения в шаблон: `{}` — по порядку, `{0}`, `{1}` — по номеру (порядок слов в языках разный).
pub fn format_dyn(template: &str, args: &[&dyn Display]) -> String {
    let mut out = String::with_capacity(template.len() + 8);
    let mut next = 0;
    let mut chars = template.chars();
    while let Some(c) = chars.next() {
        if c == '}' {
            // `}}` — литеральная скобка
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

/// Помечает ключ перевода там, где вызвать [`tr`] нельзя (константы и статические таблицы): сам даёт литерал, а показывать его
/// нужно через `tr(…)`. Словарь и тест полноты считают такие ключи используемыми.
#[macro_export]
macro_rules! t {
    ($key:literal) => {
        $key
    };
}

/// `trf!("Solved {} of {}", done, total)` — перевод шаблона и подстановка значений.
#[macro_export]
macro_rules! trf {
    ($key:literal $(, $arg:expr)* $(,)?) => {
        $crate::format_dyn($crate::tr($key), &[$(&$arg as &dyn ::core::fmt::Display),*])
    };
}

/// Слово в нужной форме числа. Ключ — `"one|many"` по-английски; русский словарь даёт три формы `"одна|две|пять"`
/// (1, 2–4, 5+; 11–14 — третья форма).
pub fn plural(n: u64, one: &'static str, many: &'static str) -> &'static str {
    match locale() {
        Locale::En => {
            if n == 1 {
                one
            } else {
                many
            }
        }
        Locale::Ru => {
            let (n10, n100) = (n % 10, n % 100);
            let pick = if n10 == 1 && n100 != 11 {
                0
            } else if (2..=4).contains(&n10) && !(12..=14).contains(&n100) {
                1
            } else {
                2
            };
            ru_forms(one, many).map_or(many, |f| f[pick])
        }
    }
}

/// Три русские формы слова из словаря (ключ `"one|many"`, значение `"форма1|форма2|форма3"`).
fn ru_forms(one: &'static str, many: &'static str) -> Option<[&'static str; 3]> {
    static FORMS: OnceLock<HashMap<String, [&'static str; 3]>> = OnceLock::new();
    let forms = FORMS.get_or_init(|| {
        entries()
            .filter(|(k, _)| k.contains('|'))
            .filter_map(|(k, v)| {
                let mut it = v.split('|');
                Some((k.to_string(), [it.next()?, it.next()?, it.next()?]))
            })
            .collect()
    });
    forms.get(&format!("{one}|{many}")).copied()
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
    fn plurals_in_both_languages() {
        // одна проверка на оба языка: язык — глобальное состояние, параллельные тесты мешали бы друг другу
        set_locale(Locale::En);
        assert_eq!((plural(1, "row", "rows"), plural(0, "row", "rows"), plural(5, "row", "rows")), ("row", "rows", "rows"));
        set_locale(Locale::Ru);
        let forms: Vec<_> = [1, 2, 4, 5, 11, 12, 21, 22, 25, 111].into_iter().map(|n| plural(n, "row", "rows")).collect();
        assert_eq!(forms, ["строка", "строки", "строки", "строк", "строк", "строк", "строка", "строки", "строк", "строк"]);
        assert_eq!(tr("Loading…"), "Загрузка…");
        assert_eq!(trf!("{} of {}", 1, 2), "1 из 2");
        set_locale(Locale::En);
    }

    #[test]
    fn formats_placeholders() {
        assert_eq!(format_dyn("{} of {}", &[&3, &"ten"]), "3 of ten");
        assert_eq!(format_dyn("{1} / {0}", &[&1, &2]), "2 / 1");
        assert_eq!(format_dyn("no placeholders", &[]), "no placeholders");
        assert_eq!(format_dyn("{{\"a\": {0}}}", &[&1]), "{\"a\": 1}");
    }
}
