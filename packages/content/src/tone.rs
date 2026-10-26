//! Цвета элементов схем. Только переменные темы `--s-*` (обе темы приложения), своих цветов нет.

use serde::{Deserialize, Serialize};

/// Цвет элемента: приглушённый, зелёный (акцент), жёлтый, красный, синий, фиолетовый — «оттенки»; остальные — особые заливки.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Tone {
    #[default]
    Muted,
    Green,
    Yellow,
    Red,
    Blue,
    Violet,
    /// «чёрный» узел дерева
    Ink,
    /// «красный» узел дерева (сплошная заливка)
    SolidRed,
    /// светлая заливка
    Light,
    /// только рамка
    Outline,
}

// Короткие имена для авторов сцен: `cell("a", 10.0, 20.0, "x").tone(G)`.
pub const M: Tone = Tone::Muted;
pub const G: Tone = Tone::Green;
pub const Y: Tone = Tone::Yellow;
pub const R: Tone = Tone::Red;
pub const B: Tone = Tone::Blue;
pub const V: Tone = Tone::Violet;

/// Заливка, рамка и цвет подписи элемента.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Look {
    pub fill: &'static str,
    pub fill_opacity: f64,
    pub stroke: &'static str,
    pub text: &'static str,
}

impl Tone {
    /// Цвет оттенка (`None` у особых заливок).
    pub fn hue(self) -> Option<&'static str> {
        Some(match self {
            Tone::Muted => "var(--s-muted)",
            Tone::Green => "var(--s-accent)",
            Tone::Yellow => "var(--s-amber)",
            Tone::Red => "var(--s-red)",
            Tone::Blue => "var(--s-blue)",
            Tone::Violet => "var(--s-violet)",
            _ => return None,
        })
    }

    pub fn look(self) -> Look {
        match self {
            Tone::Ink => Look { fill: "var(--s-ink)", fill_opacity: 1.0, stroke: "var(--s-text)", text: "var(--s-onink)" },
            Tone::SolidRed => Look { fill: "var(--s-red)", fill_opacity: 0.92, stroke: "var(--s-red)", text: "var(--s-bg)" },
            Tone::Muted => Look { fill: "var(--s-panel2)", fill_opacity: 1.0, stroke: "var(--s-border)", text: "var(--s-text)" },
            Tone::Light => Look { fill: "var(--s-border)", fill_opacity: 1.0, stroke: "var(--s-border)", text: "var(--s-text)" },
            Tone::Outline => Look { fill: "none", fill_opacity: 0.0, stroke: "var(--s-border)", text: "var(--s-text)" },
            hue => {
                let c = hue.hue().unwrap_or("var(--s-muted)");
                Look { fill: c, fill_opacity: 0.28, stroke: c, text: "var(--s-text)" }
            }
        }
    }

    /// Идентификатор наконечника стрелки в `<defs>` сцены (для особых заливок — приглушённый).
    pub fn marker(self) -> &'static str {
        match self {
            Tone::Green => "a-hd-g",
            Tone::Yellow => "a-hd-y",
            Tone::Red => "a-hd-r",
            Tone::Blue => "a-hd-b",
            _ => "a-hd-m",
        }
    }
}

/// Оттенки, для которых в `<defs>` есть наконечник стрелки: (имя маркера, цвет).
pub const ARROW_HEADS: [(&str, &str); 5] = [
    ("a-hd-m", "var(--s-muted)"),
    ("a-hd-g", "var(--s-accent)"),
    ("a-hd-y", "var(--s-amber)"),
    ("a-hd-r", "var(--s-red)"),
    ("a-hd-b", "var(--s-blue)"),
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tones_are_written_by_name() {
        assert_eq!(serde_json::to_string(&Tone::SolidRed).unwrap(), "\"solid_red\"");
        assert_eq!(serde_json::from_str::<Tone>("\"green\"").unwrap(), G);
    }
}
