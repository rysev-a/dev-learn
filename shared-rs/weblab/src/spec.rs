//! Данные упражнения и результат проверки. Формат — поле `spec` задания в `backend/data/labs/web/<книга>-<глава:02>.json`.

use serde::{Deserialize, Serialize};

/// Вид упражнения.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Kind {
    /// ученик пишет HTML, проверяется структура
    Html,
    /// HTML задан, ученик пишет CSS, проверяются вычисленные стили
    Css,
    /// HTML задан, ученик пишет один селектор: он должен выбрать ровно нужные элементы
    Selector,
}

/// Одно условие. Поле `msg` заменяет автоматически составленную формулировку.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Check {
    // ---- HTML ----
    /// Элементов по селектору не меньше `min` (по умолчанию 1) и не больше `max`.
    Exists { sel: String, #[serde(default = "one")] min: usize, #[serde(default)] max: Option<usize>, #[serde(default)] msg: Option<String> },
    /// Ровно `n` элементов.
    Count { sel: String, n: usize, #[serde(default)] msg: Option<String> },
    /// Текст элемента (без учёта регистра и лишних пробелов): совпадает или содержит. Достаточно одного подходящего элемента.
    Text { sel: String, #[serde(default)] equals: Option<String>, #[serde(default)] contains: Option<String>, #[serde(default)] msg: Option<String> },
    /// Атрибут: `present` — задан ли, `equals`/`contains` — значение. По умолчанию достаточно одного элемента, `all` — у каждого.
    Attr {
        sel: String,
        name: String,
        #[serde(default)] present: Option<bool>,
        #[serde(default)] equals: Option<String>,
        #[serde(default)] contains: Option<String>,
        #[serde(default)] all: bool,
        #[serde(default)] msg: Option<String>,
    },
    /// Есть `child`, вложенный в `parent` (`direct` — непосредственно).
    Child { parent: String, child: String, #[serde(default)] direct: bool, #[serde(default)] msg: Option<String> },
    /// Первый элемент `before` стоит в документе раньше первого элемента `after`.
    Order { before: String, after: String, #[serde(default)] msg: Option<String> },
    /// Элементов по селектору быть не должно.
    Forbid { sel: String, #[serde(default)] msg: Option<String> },
    /// Один `h1`, уровни заголовков идут без пропусков.
    Headings,
    /// У каждого поля ввода есть подпись: `label[for]`, обёртка `label`, `aria-label` или `aria-labelledby`.
    Labels,
    /// У каждого `img` есть атрибут `alt`.
    ImgAlt,
    /// Разметка разобрана без ошибок (нет незакрытых и «потерянных» тегов).
    CleanParse,
    // ---- CSS ----
    /// Вычисленное значение свойства у элементов по селектору (все совпавшие, `any` — достаточно одного).
    Style {
        sel: String,
        prop: String,
        #[serde(default)] equals: Option<String>,
        #[serde(default)] one_of: Vec<String>,
        /// числовые границы в px (значение приводится к пикселям)
        #[serde(default)] min: Option<f64>,
        #[serde(default)] max: Option<f64>,
        #[serde(default)] any: bool,
        /// ширина окна для `@media` (по умолчанию — `viewport` задания)
        #[serde(default)] viewport: Option<f64>,
        #[serde(default)] msg: Option<String>,
    },
    /// В таблице стилей объявлено свойство (и, если задано, значение) — для требований вида «используйте flex».
    Uses { prop: String, #[serde(default)] value: Option<String>, #[serde(default)] msg: Option<String> },
    /// В CSS нет `!important`.
    NoImportant,
    /// В селекторах CSS нет `#id`.
    NoIds,
    /// Таблица стилей разобрана без ошибок.
    CssValid,
    /// Есть правило `@media` с условием, содержащим подстроку (например `max-width`).
    Media { contains: String, #[serde(default)] msg: Option<String> },
}

fn one() -> usize {
    1
}

/// Эталон: отдаётся только серверу, клиенту не уходит.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Reference {
    #[serde(default)] pub html: String,
    #[serde(default)] pub css: String,
    #[serde(default)] pub selector: String,
}

/// Спецификация упражнения (`spec`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub kind: Kind,
    /// HTML, который не меняет ученик (виды `css` и `selector`); для `html` — не используется
    #[serde(default)] pub html: String,
    /// заготовка редактора: HTML (вид `html`)
    #[serde(default)] pub starter_html: String,
    /// заготовка редактора: CSS (вид `css`) или селектор (вид `selector`)
    #[serde(default)] pub starter_css: String,
    /// ширина окна по умолчанию для `@media`
    #[serde(default = "default_viewport")] pub viewport: f64,
    #[serde(default)] pub checks: Vec<Check>,
    /// вид `selector`: `id` элементов, которые обязан выбрать селектор
    #[serde(default)] pub want: Vec<String>,
    /// вид `selector`: специфичность не больше (идентификаторы, классы, типы)
    #[serde(default)] pub max_specificity: Option<[u32; 3]>,
    #[serde(default)] pub reference: Option<Reference>,
}

fn default_viewport() -> f64 {
    1024.0
}

/// Присланное решение: HTML (вид `html`), CSS или селектор (виды `css` и `selector`).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Solution {
    #[serde(default)] pub html: String,
    #[serde(default)] pub css: String,
}

/// Строка отчёта: условие и результат.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Item {
    pub text: String,
    pub ok: bool,
    /// что получилось (при провале — подсказка, что именно не так)
    #[serde(default, skip_serializing_if = "String::is_empty")]
    pub detail: String,
}

/// Результат проверки: решено, когда выполнены все условия.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Report {
    pub items: Vec<Item>,
}

impl Report {
    pub fn ok(&self) -> bool {
        !self.items.is_empty() && self.items.iter().all(|i| i.ok)
    }

    /// Первая невыполненная строка — причина отказа сервера.
    pub fn reason(&self) -> Option<String> {
        self.items.iter().find(|i| !i.ok).map(|i| if i.detail.is_empty() { i.text.clone() } else { format!("{}: {}", i.text, i.detail) })
    }
}
