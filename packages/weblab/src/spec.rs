//! Exercise data and the check result. The format is the `spec` field of a task in `backend/data/labs/web/<book>-<chapter:02>.json`.

use serde::{Deserialize, Serialize};

/// Exercise kind.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Kind {
    /// the student writes HTML, the structure is checked
    Html,
    /// HTML is given, the student writes CSS, computed styles are checked
    Css,
    /// HTML is given, the student writes a single selector: it must select exactly the required elements
    Selector,
}

/// A single condition. The `msg` field replaces the automatically composed wording.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Check {
    // ---- HTML ----
    /// At least `min` (default 1) and at most `max` elements match the selector.
    Exists { sel: String, #[serde(default = "one")] min: usize, #[serde(default)] max: Option<usize>, #[serde(default)] msg: Option<String> },
    /// Exactly `n` elements.
    Count { sel: String, n: usize, #[serde(default)] msg: Option<String> },
    /// Element text (ignoring case and extra whitespace): equals or contains. One matching element is enough.
    Text { sel: String, #[serde(default)] equals: Option<String>, #[serde(default)] contains: Option<String>, #[serde(default)] msg: Option<String> },
    /// Attribute: `present` — whether it is set, `equals`/`contains` — its value. By default one element is enough, `all` — every one.
    Attr {
        sel: String,
        name: String,
        #[serde(default)] present: Option<bool>,
        #[serde(default)] equals: Option<String>,
        #[serde(default)] contains: Option<String>,
        #[serde(default)] all: bool,
        #[serde(default)] msg: Option<String>,
    },
    /// There is a `child` nested inside `parent` (`direct` — immediately).
    Child { parent: String, child: String, #[serde(default)] direct: bool, #[serde(default)] msg: Option<String> },
    /// The first `before` element precedes the first `after` element in the document.
    Order { before: String, after: String, #[serde(default)] msg: Option<String> },
    /// No elements may match the selector.
    Forbid { sel: String, #[serde(default)] msg: Option<String> },
    /// A single `h1`, heading levels have no gaps.
    Headings,
    /// Every input field has a label: `label[for]`, a wrapping `label`, `aria-label` or `aria-labelledby`.
    Labels,
    /// Every `img` has an `alt` attribute.
    ImgAlt,
    /// The document starts with `<!doctype html>`.
    Doctype,
    /// The markup parses without errors (no unclosed or "stray" tags).
    CleanParse,
    // ---- CSS ----
    /// Computed value of a property on the elements matching the selector (all matches, `any` — one is enough).
    Style {
        sel: String,
        prop: String,
        #[serde(default)] equals: Option<String>,
        #[serde(default)] one_of: Vec<String>,
        /// numeric bounds in px (the value is converted to pixels)
        #[serde(default)] min: Option<f64>,
        #[serde(default)] max: Option<f64>,
        #[serde(default)] any: bool,
        /// viewport width for `@media` (defaults to the task's `viewport`)
        #[serde(default)] viewport: Option<f64>,
        /// element state: `hover`, `focus`, `active`… (rules with `:hover` etc. apply only in it)
        #[serde(default)] state: Option<String>,
        /// pseudo-element: `before`, `after`, `marker`… (its own styles are checked)
        #[serde(default)] pseudo: Option<String>,
        /// container width in px for `@container` rules (without it such rules do not apply)
        #[serde(default)] container_width: Option<f64>,
        /// environment features: `{"prefers-color-scheme": "dark"}`, `{"prefers-reduced-motion": "reduce"}`, `hover`, `pointer`, `orientation`
        #[serde(default)] env: std::collections::BTreeMap<String, String>,
        /// substring of the computed value (case-insensitive): for gradients, shadows, font lists etc.
        #[serde(default)] contains: Option<String>,
        #[serde(default)] msg: Option<String>,
    },
    /// The stylesheet declares the property (and, if given, the value) — for requirements like "use flex".
    Uses { prop: String, #[serde(default)] value: Option<String>, #[serde(default)] msg: Option<String> },
    /// The CSS has no `!important`.
    NoImportant,
    /// The CSS selectors have no `#id`.
    NoIds,
    /// The stylesheet parses without errors.
    CssValid,
    /// `@keyframes <name>` is declared; `contains` is a substring that must occur in its body (e.g. `transform`).
    Keyframes { name: String, #[serde(default)] contains: Option<String>, #[serde(default)] msg: Option<String> },
    /// There is a `@container` rule whose condition contains the substring.
    Container { contains: String, #[serde(default)] msg: Option<String> },
    /// There is a `@media` rule whose condition contains the substring (e.g. `max-width`).
    Media { contains: String, #[serde(default)] msg: Option<String> },
}

fn one() -> usize {
    1
}

/// Reference solution: available only to the server, never sent to the client.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Reference {
    #[serde(default)] pub html: String,
    #[serde(default)] pub css: String,
    #[serde(default)] pub selector: String,
}

/// Exercise specification (`spec`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub kind: Kind,
    /// HTML the student does not change (kinds `css` and `selector`); unused for `html`
    #[serde(default)] pub html: String,
    /// editor starter: HTML (kind `html`)
    #[serde(default)] pub starter_html: String,
    /// editor starter: CSS (kind `css`) or a selector (kind `selector`)
    #[serde(default)] pub starter_css: String,
    /// default viewport width for `@media`
    #[serde(default = "default_viewport")] pub viewport: f64,
    #[serde(default)] pub checks: Vec<Check>,
    /// kind `selector`: `id`s of the elements the selector must select
    #[serde(default)] pub want: Vec<String>,
    /// kind `selector`: specificity at most (ids, classes, types)
    #[serde(default)] pub max_specificity: Option<[u32; 3]>,
    #[serde(default)] pub reference: Option<Reference>,
}

fn default_viewport() -> f64 {
    1024.0
}

/// Submitted solution: HTML (kind `html`), CSS or a selector (kinds `css` and `selector`).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Solution {
    #[serde(default)] pub html: String,
    #[serde(default)] pub css: String,
}

/// Report row: the condition and the result.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Item {
    pub text: String,
    pub ok: bool,
    /// what came out (on failure, a hint about what exactly is wrong)
    #[serde(default, skip_serializing_if = "String::is_empty")]
    pub detail: String,
}

/// Check result: solved when all conditions are met.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Report {
    pub items: Vec<Item>,
}

impl Report {
    pub fn ok(&self) -> bool {
        !self.items.is_empty() && self.items.iter().all(|i| i.ok)
    }

    /// The first failed row is the server's rejection reason.
    pub fn reason(&self) -> Option<String> {
        self.items.iter().find(|i| !i.ok).map(|i| if i.detail.is_empty() { i.text.clone() } else { format!("{}: {}", i.text, i.detail) })
    }
}
