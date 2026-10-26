//! Настройки интерфейса в `localStorage` (ключи с префиксом `say-`) и тема.

use leptos::prelude::{RwSignal, Set};
use wasm_bindgen::JsCast;

pub const THEME: &str = "say-theme";
/// Выбранная цветовая тема для тёмного и светлого режима (`default` — не хранится).
pub const PALETTE_DARK: &str = "say-palette-dark";
pub const PALETTE_LIGHT: &str = "say-palette-light";
pub const ASIDE: &str = "say-aside-collapsed";
pub const ANIM: &str = "say-anim-auto";
pub const VOICE_H: &str = "say-voice-h";
pub const TOKEN: &str = "say-token";
pub const AUTO_NEXT: &str = "say-auto-next";
pub const AUTOWIRE_LAB: &str = "say-autowire-lab";
pub const AUTOWIRE_SD: &str = "say-autowire-sd";

fn storage() -> Option<web_sys::Storage> {
    web_sys::window()?.local_storage().ok()?
}

pub fn read(key: &str) -> Option<String> {
    storage()?.get_item(key).ok()?
}

/// Записывает значение; `None` — удаляет ключ. Недоступное хранилище молча игнорируется (настройка не сохранится).
pub fn write(key: &str, value: Option<&str>) {
    if let Some(s) = storage() {
        let _ = match value {
            Some(v) => s.set_item(key, v),
            None => s.remove_item(key),
        };
    }
}

/// Булева настройка: ключ в `localStorage` и значение по умолчанию. В хранилище лежит только отклонение от умолчания
/// (выключенное по умолчанию включённое — «1», включённое по умолчанию выключенное — «0»), как у React-фронтенда.
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

    /// Значение настройки по сохранённой строке.
    pub fn parse(self, raw: Option<&str>) -> bool {
        if self.default_on {
            raw != Some("0")
        } else {
            raw == Some("1")
        }
    }

    /// Что записать в хранилище: значение по умолчанию — ничего (ключ удаляется).
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

/// Левое меню разделов свёрнуто в колонку иконок.
pub const ASIDE_FLAG: Flag = Flag::off_by_default(ASIDE);
/// Схемы на слайдах сами проходят шаги по таймеру.
pub const ANIM_FLAG: Flag = Flag::on_by_default(ANIM);
/// После успешной проверки кода открывается следующее упражнение.
pub const AUTO_NEXT_FLAG: Flag = Flag::off_by_default(AUTO_NEXT);
/// Автосвязывание на досках книг 14 и 18 (в этом фронтенде досок ещё нет — настройка общая с React).
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

/// Ключ хранилища для цветовой темы режима.
fn palette_key(mode: Theme) -> &'static str {
    match mode {
        Theme::Dark => PALETTE_DARK,
        Theme::Light => PALETTE_LIGHT,
    }
}

/// Сохранённая цветовая тема режима (неизвестное или устаревшее значение — тема по умолчанию).
pub fn read_palette(mode: Theme) -> String {
    match read(palette_key(mode)) {
        Some(id) if crate::themes::is_known(mode, &id) => id,
        _ => crate::themes::DEFAULT.to_string(),
    }
}

/// Меняет тему: сигнал, документ и сохранённая настройка.
pub fn switch_theme(theme: RwSignal<Theme>, to: Theme) {
    theme.set(to);
    apply_theme(to);
}

/// Выбирает цветовую тему и включает её режим (как в VS Code: выбор темы переключает светлый и тёмный режим).
pub fn choose_palette(theme: RwSignal<Theme>, mode: Theme, id: &str) {
    write(palette_key(mode), (id != crate::themes::DEFAULT).then_some(id));
    theme.set(mode);
    apply_theme(mode);
}

/// Режим и цветовая тема документа и запись режима в настройки.
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

/// Сцены без движения: настройка «автопроигрывание выключено» или системное «уменьшить движение».
pub fn motion_off() -> bool {
    let system = web_sys::window().and_then(|w| w.match_media("(prefers-reduced-motion: reduce)").ok().flatten()).is_some_and(|m| m.matches());
    system || !ANIM_FLAG.read()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn flags_default_to_their_default_and_store_only_the_deviation() {
        assert!(ANIM_FLAG.parse(None), "анимации включены по умолчанию");
        assert!(!ANIM_FLAG.parse(Some("0")));
        assert!(!AUTO_NEXT_FLAG.parse(None), "автопереход выключен по умолчанию");
        assert!(AUTO_NEXT_FLAG.parse(Some("1")));
        assert!(!ASIDE_FLAG.parse(Some("0")), "«0» у свёрнутого меню — старое явное «выключено»");
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
        assert_eq!((AUTOWIRE_LAB, AUTOWIRE_SD), ("say-autowire-lab", "say-autowire-sd"));
        assert!(AUTOWIRE_LAB_FLAG.parse(None), "автосвязывание включено по умолчанию, выключенное хранится как «0»");
        assert!(!AUTOWIRE_SD_FLAG.parse(Some("0")));
    }
}
