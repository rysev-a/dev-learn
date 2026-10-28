//! Slides and chapters: the slide frame (headings, "KEY POINT") and the body, a sequence of blocks.
//!
//! Blocks are the whole vocabulary of the former slides: scene diagram, code callout, "ON SCREEN", cards, topic grid, table, labels
//! and callouts. A slide is stored in the database as a document; the client renders the blocks with a single shared component.

use highlight::Lang;
use serde::{Deserialize, Serialize};

use crate::scene::{Scene, SceneError, SceneSpec};

/// Node card: a title and an explanation.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Card {
    pub title: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    /// border color: `green`, `amber`, `red`, `blue` …
    #[serde(default, skip_serializing_if = "String::is_empty")]
    pub kind: String,
    /// title in a monospace font (names, code)
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub mono: bool,
}

/// An item of a card row.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Cell {
    Card(Card),
    /// a "→" arrow between cards
    Arrow,
}

/// A topic in the grid: a large symbol, a title, an explanation.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Topic {
    pub big: String,
    pub title: String,
    pub sub: String,
}

/// A block of the slide body.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", rename_all = "snake_case")]
pub enum Block {
    /// animated diagram; `cues` in the spec are the step cues of this slide
    Scene(SceneSpec),
    /// code callout with syntax highlighting
    Code { lang: Lang, text: String },
    /// "ON SCREEN": program output or a command
    Cmd { text: String },
    /// label above a block (`ON SCREEN`, `RESULT`)
    Label { text: String },
    /// explanatory callout; `` `code` `` in the text are monospace inserts
    Note { text: String },
    /// hint line below the diagram
    Hint { text: String },
    /// 2×2 topic grid
    Topics { items: Vec<Topic> },
    /// row of cards (with arrows between them)
    Cols { cells: Vec<Cell> },
    /// 2×2 card grid
    Grid { cards: Vec<Card> },
    /// "expression — explanation" table
    Table { rows: Vec<(String, String)> },
}

/// Slide: one lesson paragraph = one slide.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Slide {
    pub title: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sub: Option<String>,
    /// short name for the slide list in fullscreen mode
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub short: Option<String>,
    /// the "KEY POINT" block
    pub main: String,
    pub body: Vec<Block>,
}

impl Slide {
    /// The slide's scene (the first one in the body), if any.
    pub fn scene_spec(&self) -> Option<&SceneSpec> {
        self.body.iter().find_map(|b| if let Block::Scene(s) = b { Some(s) } else { None })
    }
}

/// Chapter: the rubric above the slide title and one slide per lesson paragraph.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Chapter {
    pub book: i64,
    pub chapter: i64,
    /// "BOOK / SECTION / CHAPTER N"
    pub rubric: String,
    pub slides: Vec<Slide>,
}

impl Chapter {
    /// Chapter data check: all scenes compile, slides have titles and a "KEY POINT".
    pub fn check(&self) -> Result<(), SceneError> {
        if self.slides.is_empty() {
            return Err(SceneError(format!("chapter {}:{}: no slides", self.book, self.chapter)));
        }
        for (i, s) in self.slides.iter().enumerate() {
            let at = |m: &str| SceneError(format!("chapter {}:{}, slide {}: {m}", self.book, self.chapter, i + 1));
            if s.title.trim().is_empty() || s.main.trim().is_empty() {
                return Err(at("empty title or \"ГЛАВНОЕ\" (key point)"));
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
        let ch = Chapter { book: 1, chapter: 1, rubric: "R".into(), slides: vec![] };
        assert!(ch.check().is_err());
    }
}
