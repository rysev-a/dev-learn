//! Interface settings in `localStorage` (keys with the `cs-core-` prefix) and theme.

use leptos::prelude::{RwSignal, Set};
use wasm_bindgen::JsCast;

pub const THEME: &str = "cs-core-theme";
/// Selected color theme for dark and light mode (`default` is not stored).
pub const PALETTE_DARK: &str = "cs-core-palette-dark";
pub const PALETTE_LIGHT: &str = "cs-core-palette-light";
pub const ASIDE: &str = "cs-core-aside-collapsed";
pub const ANIM: &str = "cs-core-anim-auto";
pub const VOICE_H: &str = "cs-core-voice-h";
pub const TOKEN: &str = "cs-core-token";
/// Interface language (`en` or `ru`); with no value - the browser language.
pub const LANG: &str = "cs-core-lang";
pub const AUTO_NEXT: &str = "cs-core-auto-next";
pub const AUTOWIRE_LAB: &str = "cs-core-autowire-lab";
pub const AUTOWIRE_SD: &str = "cs-core-autowire-sd";

/// Chooses the interface language at start (saved, otherwise the browser language, otherwise English) and sets it in `<html lang>`.
/// Called before the first displayed text: the language changes only by reloading the page.
pub fn init_locale() -> i18n::Locale {
    locales::install();
    let browser = web_sys::window().and_then(|w| w.navigator().language());
    let locale = i18n::Locale::detect(read(LANG).as_deref(), browser.as_deref());
    i18n::set_locale(locale);
    if let Some(root) = web_sys::window().and_then(|w| w.document()).and_then(|d| d.document_element()) {
        let _ = root.set_attribute("lang", locale.code());
    }
    locale
}

/// Remembers the language and reloads the page: texts are taken once when the interface is built.
pub fn switch_locale(locale: i18n::Locale) {
    write(LANG, Some(locale.code()));
    if let Some(w) = web_sys::window() {
        let _ = w.location().reload();
    }
}

fn storage() -> Option<web_sys::Storage> {
    web_sys::window()?.local_storage().ok()?
}

pub fn read(key: &str) -> Option<String> {
    storage()?.get_item(key).ok()?
}

/// Writes a value; `None` removes the key. Unavailable storage is silently ignored (the setting is not saved).
pub fn write(key: &str, value: Option<&str>) {
    if let Some(s) = storage() {
        let _ = match value {
            Some(v) => s.set_item(key, v),
            None => s.remove_item(key),
        };
    }
}

/// Boolean setting: a `localStorage` key and a default value. Storage holds only a deviation from the default
/// (default-off turned on is "1", default-on turned off is "0"), as in the React frontend.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Flag {
    key: &'static str,
    default_on: bool,
}

impl Flag {
    pub const fn on_by_default(key: &'static str) -> Self {
        Self { key, default_on: true }
    }

    pub const fn off_by_default(key: &'static str) -> Self {
        Self { key, default_on: false }
    }

    /// Setting value from the saved string.
    pub fn parse(self, raw: Option<&str>) -> bool {
        if self.default_on {
            raw != Some("0")
        } else {
            raw == Some("1")
        }
    }

    /// What to write to storage: the default value - nothing (the key is removed).
    pub fn encode(self, on: bool) -> Option<&'static str> {
        match (on == self.default_on, on) {
            (true, _) => None,
            (false, true) => Some("1"),
            (false, false) => Some("0"),
        }
    }

    pub fn read(self) -> bool {
        self.parse(read(self.key).as_deref())
    }

    pub fn write(self, on: bool) {
        write(self.key, self.encode(on));
    }
}

/// Left section menu collapsed into an icon column.
pub const ASIDE_FLAG: Flag = Flag::off_by_default(ASIDE);
/// Diagrams on slides step through by a timer on their own.
pub const ANIM_FLAG: Flag = Flag::on_by_default(ANIM);
/// After a successful code check the next exercise opens.
pub const AUTO_NEXT_FLAG: Flag = Flag::off_by_default(AUTO_NEXT);
/// Auto-wiring on the boards of books 14 and 18 (this frontend has no boards yet - the setting is shared with React).
pub const AUTOWIRE_LAB_FLAG: Flag = Flag::on_by_default(AUTOWIRE_LAB);
pub const AUTOWIRE_SD_FLAG: Flag = Flag::on_by_default(AUTOWIRE_SD);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Theme {
    Dark,
    Light,
}

impl Theme {
    pub fn name(self) -> &'static str {
        match self {
            Theme::Dark => "dark",
            Theme::Light => "light",
        }
    }
    pub fn toggled(self) -> Theme {
        match self {
            Theme::Dark => Theme::Light,
            Theme::Light => Theme::Dark,
        }
    }
}

pub fn read_theme() -> Theme {
    if read(THEME).as_deref() == Some("light") {
        Theme::Light
    } else {
        Theme::Dark
    }
}

/// Storage key for a mode's color theme.
fn palette_key(mode: Theme) -> &'static str {
    match mode {
        Theme::Dark => PALETTE_DARK,
        Theme::Light => PALETTE_LIGHT,
    }
}

/// Saved color theme of a mode (an unknown or outdated value gives the default theme).
pub fn read_palette(mode: Theme) -> String {
    match read(palette_key(mode)) {
        Some(id) if crate::themes::is_known(mode, &id) => id,
        _ => crate::themes::DEFAULT.to_string(),
    }
}

/// Changes the theme: signal, document and saved setting.
pub fn switch_theme(theme: RwSignal<Theme>, to: Theme) {
    theme.set(to);
    apply_theme(to);
}

/// Chooses a color theme and enables its mode (as in VS Code: choosing a theme switches light and dark mode).
pub fn choose_palette(theme: RwSignal<Theme>, mode: Theme, id: &str) {
    write(palette_key(mode), (id != crate::themes::DEFAULT).then_some(id));
    theme.set(mode);
    apply_theme(mode);
}

/// Mode and color theme of the document and writing the mode into settings.
pub fn apply_theme(theme: Theme) {
    if let Some(root) = web_sys::window().and_then(|w| w.document()).and_then(|d| d.document_element()) {
        let palette = read_palette(theme);
        if let Ok(html) = root.dyn_into::<web_sys::HtmlElement>() {
            let data = html.dataset();
            let _ = data.set("theme", theme.name());
            if palette == crate::themes::DEFAULT {
                let _ = data.delete("palette");
            } else {
                let _ = data.set("palette", &palette);
            }
        }
    }
    write(THEME, Some(theme.name()));
}

/// Scenes without motion: the "autoplay off" setting or the system "reduce motion".
pub fn motion_off() -> bool {
    let system = web_sys::window().and_then(|w| w.match_media("(prefers-reduced-motion: reduce)").ok().flatten()).is_some_and(|m| m.matches());
    system || !ANIM_FLAG.read()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn flags_default_to_their_default_and_store_only_the_deviation() {
        assert!(ANIM_FLAG.parse(None), "animations are on by default");
        assert!(!ANIM_FLAG.parse(Some("0")));
        assert!(!AUTO_NEXT_FLAG.parse(None), "auto-advance is off by default");
        assert!(AUTO_NEXT_FLAG.parse(Some("1")));
        assert!(!ASIDE_FLAG.parse(Some("0")), "\"0\" for the collapsed menu is the old explicit \"off\"");
        assert_eq!(ANIM_FLAG.encode(true), None);
        assert_eq!(ANIM_FLAG.encode(false), Some("0"));
        assert_eq!(AUTO_NEXT_FLAG.encode(false), None);
        assert_eq!(AUTO_NEXT_FLAG.encode(true), Some("1"));
    }

    #[test]
    fn what_is_written_reads_back_the_same() {
        for flag in [ASIDE_FLAG, ANIM_FLAG, AUTO_NEXT_FLAG, AUTOWIRE_LAB_FLAG, AUTOWIRE_SD_FLAG] {
            for on in [false, true] {
                assert_eq!(flag.parse(flag.encode(on)), on);
            }
        }
    }

    #[test]
    fn autowire_flags_use_the_react_keys() {
        assert_eq!((AUTOWIRE_LAB, AUTOWIRE_SD), ("cs-core-autowire-lab", "cs-core-autowire-sd"));
        assert!(AUTOWIRE_LAB_FLAG.parse(None), "auto-wiring is on by default, off is stored as \"0\"");
        assert!(!AUTOWIRE_SD_FLAG.parse(Some("0")));
    }
}
