//! Точечная смена цвета у отдельных фигур поверх оттенка ([`content::Tone`]) — для сцен со своей отрисовкой.

use content::tone::Look;

// Цвета-переменные темы для подписей и точечных переопределений.
pub const ACC: &str = "var(--s-accent)";
pub const AMB: &str = "var(--s-amber)";
pub const RED: &str = "var(--s-red)";
pub const BLU: &str = "var(--s-blue)";
pub const MUTED: &str = "var(--s-muted)";
pub const PANEL: &str = "var(--s-panel2)";

/// Точечное переопределение краски поверх [`Tone`]: `None` — взять из оттенка (как необязательные `stroke`/`fill` у плашек старых сцен).
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Paint {
    pub stroke: Option<&'static str>,
    pub fill: Option<&'static str>,
    pub fill_opacity: Option<f64>,
    pub text: Option<&'static str>,
}

impl Paint {
    /// Рамка и заливка одним цветом с прозрачностью заливки `fill_opacity` (как «подсвеченный» элемент).
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
