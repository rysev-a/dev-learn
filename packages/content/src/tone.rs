//! Colors of diagram elements. Only the theme variables `--s-*` (both app themes), no custom colors.

use serde::{Deserialize, Serialize};

/// Element color: muted, green (accent), yellow, red, blue, violet are "hues"; the rest are special fills.
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
    /// "black" tree node
    Ink,
    /// "red" tree node (solid fill)
    SolidRed,
    /// light fill
    Light,
    /// outline only
    Outline,
}

// Short names for scene authors: `cell("a", 10.0, 20.0, "x").tone(G)`.
pub const M: Tone = Tone::Muted;
pub const G: Tone = Tone::Green;
pub const Y: Tone = Tone::Yellow;
pub const R: Tone = Tone::Red;
pub const B: Tone = Tone::Blue;
pub const V: Tone = Tone::Violet;

/// Fill, stroke and label color of an element.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Look {
    pub fill: &'static str,
    pub fill_opacity: f64,
    pub stroke: &'static str,
    pub text: &'static str,
}

impl Tone {
    /// Hue color (`None` for special fills).
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

    /// Id of the arrowhead in the scene's `<defs>` (muted for special fills).
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

/// Hues that have an arrowhead in `<defs>`: (marker name, color).
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
