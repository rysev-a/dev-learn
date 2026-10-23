//! Слайды и главы: рамка слайда (заголовки, «ГЛАВНОЕ») и тело — последовательность блоков.
//!
//! Блоки — весь словарь прежних слайдов: схема-сцена, врезка кода, «НА ЭКРАНЕ», карточки, сетка тем, таблица, подписи
//! и врезки. Слайд хранится в базе документом; клиент рисует блоки одним общим компонентом.

use highlight::Lang;
use serde::{Deserialize, Serialize};

use crate::scene::{Scene, SceneError, SceneSpec};

/// Карточка-узел: заголовок и пояснение.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Card {
    pub title: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    /// цвет рамки: `green`, `amber`, `red`, `blue` …
    #[serde(default, skip_serializing_if = "String::is_empty")]
    pub kind: String,
    /// заголовок моноширинным шрифтом (имена, код)
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub mono: bool,
}

/// Элемент ряда карточек.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Cell {
    Card(Card),
    /// стрелка «→» между карточками
    Arrow,
}

/// Тема в сетке: крупный символ, заголовок, пояснение.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Topic {
    pub big: String,
    pub title: String,
    pub sub: String,
}

/// Блок тела слайда.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Block {
    /// анимированная схема; `cues` в описании — метки шагов этого слайда
    Scene(SceneSpec),
    /// врезка кода с подсветкой
    Code { lang: Lang, text: String },
    /// «НА ЭКРАНЕ»: вывод программы или команда
    Cmd { text: String },
    /// подпись над блоком (`НА ЭКРАНЕ`, `РЕЗУЛЬТАТ`)
    Label { text: String },
    /// врезка с пояснением; `` `код` `` в тексте — моноширинные вставки
    Note { text: String },
    /// строка-подсказка под схемой
    Hint { text: String },
    /// сетка тем 2×2
    Topics { items: Vec<Topic> },
    /// ряд карточек (со стрелками между ними)
    Cols { cells: Vec<Cell> },
    /// сетка карточек 2×2
    Grid { cards: Vec<Card> },
    /// таблица «выражение — пояснение»
    Table { rows: Vec<(String, String)> },
}

/// Слайд: один абзац урока = один слайд.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Slide {
    pub title: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    /// короткое название для списка слайдов в полном экране
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub short: Option<String>,
    /// блок «ГЛАВНОЕ»
    pub main: String,
    pub body: Vec<Block>,
}

impl Slide {
    /// Сцена слайда (первая в теле), если есть.
    pub fn scene_spec(&self) -> Option<&SceneSpec> {
        self.body.iter().find_map(|b| if let Block::Scene(s) = b { Some(s) } else { None })
    }
}

/// Глава: рубрика над заголовком слайда и слайды по числу абзацев урока.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Chapter {
    pub book: i64,
    pub chapter: i64,
    /// «КНИГА / РАЗДЕЛ / ГЛАВА N»
    pub rubric: String,
    pub slides: Vec<Slide>,
}

impl Chapter {
    /// Проверка данных главы: все сцены компилируются, у слайдов есть заголовки и «ГЛАВНОЕ».
    pub fn check(&self) -> Result<(), SceneError> {
        if self.slides.is_empty() {
            return Err(SceneError(format!("глава {}:{}: нет слайдов", self.book, self.chapter)));
        }
        for (i, s) in self.slides.iter().enumerate() {
            let at = |m: &str| SceneError(format!("глава {}:{}, слайд {}: {m}", self.book, self.chapter, i + 1));
            if s.title.trim().is_empty() || s.main.trim().is_empty() {
                return Err(at("пустой заголовок или «ГЛАВНОЕ»"));
            }
            for b in &s.body {
                if let Block::Scene(spec) = b {
                    Scene::compile(spec).map_err(|e| at(&e.0))?;
                }
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn blocks_are_tagged_by_kind() {
        let b: Block = serde_json::from_str(r#"{"t":"code","lang":"python","text":"print(1)"}"#).unwrap();
        assert_eq!(b, Block::Code { lang: Lang::Python, text: "print(1)".into() });
        let cols: Block = serde_json::from_str(r#"{"t":"cols","cells":[{"t":"card","title":"A","kind":"green"},{"t":"arrow"}]}"#).unwrap();
        assert!(matches!(cols, Block::Cols { cells } if cells.len() == 2));
    }

    #[test]
    fn empty_chapter_is_an_error() {
        let ch = Chapter { book: 1, chapter: 1, rubric: "К".into(), slides: vec![] };
        assert!(ch.check().is_err());
    }
}
