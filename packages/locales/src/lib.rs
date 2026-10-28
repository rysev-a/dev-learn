//! Dictionaries of the "cs-core" project for the shared `i18n` crate: Russian translations live in `ru/<area>.json` (key — the English text,
//! value — the translation; a key with `|` holds plural forms). The files are embedded into the binary at build time; the application calls [`install`] once at startup
//! (the frontend — before the first text, the backend — on launch, lab crate tests — before checking Russian messages).
//!
//! A new area is one more file in `ru/` and a line in [`RU`]; the test `tests/dictionary.rs` makes sure every key used in the code is in the dictionary and
//! the dictionary has no unused entries.

use std::sync::Once;

/// Russian dictionaries by area: (area name, JSON).
pub const RU: &[(&str, &str)] = &[
    ("ui", include_str!("../ru/ui.json")),
    ("labs_ui", include_str!("../ru/labs_ui.json")),
    ("server", include_str!("../ru/server.json")),
    ("archlab", include_str!("../ru/archlab.json")),
    ("riscvlab", include_str!("../ru/riscvlab.json")),
    ("netlab", include_str!("../ru/netlab.json")),
    ("sdlab", include_str!("../ru/sdlab.json")),
    ("virtlab", include_str!("../ru/virtlab.json")),
    ("weblab", include_str!("../ru/weblab.json")),
];

/// Loads all dictionaries into `i18n` (repeated calls do nothing). Broken JSON is a data build error, not a surprise on
/// the screen, hence a panic with the area name.
pub fn install() {
    static ONCE: Once = Once::new();
    ONCE.call_once(|| {
        for (area, json) in RU {
            if let Err(e) = i18n::load_json(i18n::Locale::Ru, json) {
                panic!("словарь ru/{area}.json: {e}");
            }
        }
    });
}

/// Like [`i18n::guard`], but loads the dictionaries first: for tests that compare Russian texts.
#[must_use]
pub fn guard(locale: i18n::Locale) -> i18n::LocaleGuard {
    install();
    i18n::guard(locale)
}

/// Like [`i18n::set_locale`], but loads the dictionaries first.
pub fn set_locale(locale: i18n::Locale) {
    install();
    i18n::set_locale(locale);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn dictionaries_load_and_translate() {
        install();
        install();
        let _ru = i18n::guard(i18n::Locale::Ru);
        assert_eq!(i18n::tr("Loading…"), "Загрузка…");
        assert_eq!(i18n::plural(5, "row", "rows"), "строк");
        assert!(i18n::entries(i18n::Locale::Ru).len() > 1900);
    }
}
