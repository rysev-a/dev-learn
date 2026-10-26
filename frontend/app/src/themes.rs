//! Цветовые темы интерфейса и редактора кода (как в VS Code). Сами цвета — `styles/themes.css` (блок `data-palette="<id>"` на `<html>`):
//! они переопределяют переменные приложения, слайдов и подсветки кода. Здесь — список тем для настроек.

use crate::settings::Theme;

/// Тема: идентификатор (значение `data-palette`), название и режим (светлая или тёмная).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Palette {
    pub id: &'static str,
    pub name: &'static str,
    pub mode: Theme,
}

/// Тема по умолчанию: палитра из `app.css`, атрибут `data-palette` на `<html>` не ставится.
pub const DEFAULT: &str = "default";

pub const PALETTES: &[Palette] = &[
    Palette { id: DEFAULT, name: "Тёмная", mode: Theme::Dark },
    Palette { id: "dracula", name: "Dracula", mode: Theme::Dark },
    Palette { id: "one-dark", name: "One Dark", mode: Theme::Dark },
    Palette { id: "nord", name: "Nord", mode: Theme::Dark },
    Palette { id: "tokyo-night", name: "Tokyo Night", mode: Theme::Dark },
    Palette { id: "solarized-dark", name: "Solarized Dark", mode: Theme::Dark },
    Palette { id: "monokai", name: "Monokai", mode: Theme::Dark },
    Palette { id: DEFAULT, name: "Светлая", mode: Theme::Light },
    Palette { id: "github-light", name: "GitHub Light", mode: Theme::Light },
    Palette { id: "solarized-light", name: "Solarized Light", mode: Theme::Light },
    Palette { id: "one-light", name: "One Light", mode: Theme::Light },
    Palette { id: "gruvbox-light", name: "Gruvbox Light", mode: Theme::Light },
];

/// Темы одного режима в порядке показа.
pub fn of_mode(mode: Theme) -> impl Iterator<Item = &'static Palette> {
    PALETTES.iter().filter(move |p| p.mode == mode)
}

/// Известна ли тема этого режима (защита от устаревшего значения в `localStorage`).
pub fn is_known(mode: Theme, id: &str) -> bool {
    PALETTES.iter().any(|p| p.mode == mode && p.id == id)
}

/// Идентификатор для карточки предпросмотра: у тем по умолчанию в `themes.css` свои блоки `default-dark` и `default-light`.
pub fn card_id(p: &Palette) -> String {
    match (p.id, p.mode) {
        (DEFAULT, Theme::Dark) => "default-dark".to_string(),
        (DEFAULT, Theme::Light) => "default-light".to_string(),
        (id, _) => id.to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CSS: &str = include_str!("../styles/themes.css");

    #[test]
    fn every_palette_has_a_css_block_for_the_page_and_for_its_card() {
        for p in PALETTES {
            let id = card_id(p);
            assert!(CSS.contains(&format!(".palette-card[data-palette=\"{id}\"]")), "нет карточки темы {id}");
            if p.id != DEFAULT {
                assert!(CSS.contains(&format!(":root[data-palette=\"{id}\"]")), "нет блока темы {id}");
            }
        }
    }

    #[test]
    fn ids_are_unique_within_a_mode_and_each_mode_has_a_default() {
        for mode in [Theme::Dark, Theme::Light] {
            let ids: Vec<&str> = of_mode(mode).map(|p| p.id).collect();
            let mut sorted = ids.clone();
            sorted.sort_unstable();
            sorted.dedup();
            assert_eq!(sorted.len(), ids.len(), "повтор идентификатора в режиме {mode:?}");
            assert_eq!(ids.first(), Some(&DEFAULT), "первой идёт тема по умолчанию");
            assert!(ids.len() >= 4, "мало тем в режиме {mode:?}");
        }
    }

    #[test]
    fn unknown_ids_are_rejected_and_themes_do_not_cross_modes() {
        assert!(is_known(Theme::Dark, "dracula"));
        assert!(!is_known(Theme::Light, "dracula"));
        assert!(!is_known(Theme::Dark, "no-such-theme"));
        assert!(is_known(Theme::Light, DEFAULT));
    }
}
