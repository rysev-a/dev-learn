//! Per-shape color override on top of the tone ([`content::Tone`]) — for scenes with custom rendering.

use content::tone::Look;

// Theme color variables for labels and per-shape overrides.
pub const ACC: &str = "var(--s-accent)";
pub const AMB: &str = "var(--s-amber)";
pub const RED: &str = "var(--s-red)";
pub const BLU: &str = "var(--s-blue)";
pub const MUTED: &str = "var(--s-muted)";
pub const PANEL: &str = "var(--s-panel2)";

/// Per-shape paint override on top of [`Tone`]: `None` means take it from the tone (like the optional `stroke`/`fill` of old scenes' plates).
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Paint {
    pub stroke: Option<&'static str>,
    pub fill: Option<&'static str>,
    pub fill_opacity: Option<f64>,
    pub text: Option<&'static str>,
}

impl Paint {
    /// Stroke and fill in one color with fill opacity `fill_opacity` (like a "highlighted" element).
    pub fn tint(color: &'static str, fill_opacity: f64) -> Self {
        Self { stroke: Some(color), fill: Some(color), fill_opacity: Some(fill_opacity), text: None }
    }

    pub fn stroke(color: &'static str) -> Self {
        Self { stroke: Some(color), ..Self::default() }
    }

    pub fn apply(self, base: Look) -> Look {
        Look {
            fill: self.fill.unwrap_or(base.fill),
            fill_opacity: self.fill_opacity.unwrap_or(base.fill_opacity),
            stroke: self.stroke.unwrap_or(base.stroke),
            text: self.text.unwrap_or(base.text),
        }
    }
}
