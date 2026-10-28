//! Color themes of the interface and code editor (as in VS Code). The colors themselves are `styles/themes.css` (a `data-palette="<id>"` block on `<html>`):
//! they override the variables of the app, slides and code highlighting. Here is the theme list for settings.

use crate::settings::Theme;

/// Theme: identifier (the `data-palette` value), name and mode (light or dark).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Palette {
    pub id: &'static str,
    pub name: &'static str,
    pub mode: Theme,
}

/// Default theme: the palette from `app.css`, the `data-palette` attribute is not set on `<html>`.
pub const DEFAULT: &str = "default";

pub const PALETTES: &[Palette] = &[
    Palette { id: DEFAULT, name: i18n::t!("Dark"), mode: Theme::Dark },
    Palette { id: "dracula", name: "Dracula", mode: Theme::Dark },
    Palette { id: "one-dark", name: "One Dark", mode: Theme::Dark },
    Palette { id: "nord", name: "Nord", mode: Theme::Dark },
    Palette { id: "tokyo-night", name: "Tokyo Night", mode: Theme::Dark },
    Palette { id: "solarized-dark", name: "Solarized Dark", mode: Theme::Dark },
    Palette { id: "monokai", name: "Monokai", mode: Theme::Dark },
    Palette { id: DEFAULT, name: i18n::t!("Light"), mode: Theme::Light },
    Palette { id: "github-light", name: "GitHub Light", mode: Theme::Light },
    Palette { id: "solarized-light", name: "Solarized Light", mode: Theme::Light },
    Palette { id: "one-light", name: "One Light", mode: Theme::Light },
    Palette { id: "gruvbox-light", name: "Gruvbox Light", mode: Theme::Light },
];

/// Themes of one mode in display order.
pub fn of_mode(mode: Theme) -> impl Iterator<Item = &'static Palette> {
    PALETTES.iter().filter(move |p| p.mode == mode)
}

/// Whether the theme is known for this mode (protection against an outdated value in `localStorage`).
pub fn is_known(mode: Theme, id: &str) -> bool {
    PALETTES.iter().any(|p| p.mode == mode && p.id == id)
}

/// Identifier for the preview card: default themes have their own blocks `default-dark` and `default-light` in `themes.css`.
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
            assert!(CSS.contains(&format!(".palette-card[data-palette=\"{id}\"]")), "no card for theme {id}");
            if p.id != DEFAULT {
                assert!(CSS.contains(&format!(":root[data-palette=\"{id}\"]")), "no block for theme {id}");
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
            assert_eq!(sorted.len(), ids.len(), "repeated identifier in mode {mode:?}");
            assert_eq!(ids.first(), Some(&DEFAULT), "the default theme goes first");
            assert!(ids.len() >= 4, "too few themes in mode {mode:?}");
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
