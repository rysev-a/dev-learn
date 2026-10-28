//! Content generators. The result — data files `backend/data/slides/<book>-<chapter>.json` (canonical JSON
//! of the [`content::Chapter`] structure); the backend reads them at seed time and stores them in the database.

use std::path::Path;

use content::{Chapter, SceneSpec};

pub mod dm;
pub mod py_ch00;
pub mod web_ch13;
pub mod web_ch14;
pub mod web_ch15;
pub mod web_ch16;
pub mod web_ch17;
pub mod web_ch18;
pub mod web_ch19;
pub mod web_ch20;
pub mod web_ch21;

/// Chapters written by Rust generators (the source is this code, not the port from TypeScript).
pub fn generated() -> Vec<Chapter> {
    // chapters without slides — stubs (still being written), not included in the data
    vec![py_ch00::chapter(), web_ch13::chapter(), web_ch14::chapter(), web_ch15::chapter(), web_ch16::chapter(), web_ch17::chapter(), web_ch18::chapter(), web_ch19::chapter(), web_ch20::chapter(), web_ch21::chapter()].into_iter().filter(|c| !c.slides.is_empty()).collect()
}

/// Chapter file name: `13-05.json`.
pub fn file_name(book: i64, chapter: i64) -> String {
    format!("{book:02}-{chapter:02}.json")
}

/// Writes a chapter as data (checks it before writing).
pub fn write_chapter(dir: &Path, ch: &Chapter) -> anyhow::Result<()> {
    ch.check().map_err(|e| anyhow::anyhow!("{e}"))?;
    std::fs::create_dir_all(dir)?;
    std::fs::write(dir.join(file_name(ch.book, ch.chapter)), serde_json::to_string(ch)?)?;
    Ok(())
}

/// Scenes rewritten from manual React rendering (`kit.tsx`) to data: by former component name.
pub fn kit_scene(name: &str) -> Option<SceneSpec> {
    dm::scenes().into_iter().find(|(n, _)| *n == name).map(|(_, spec)| spec)
}
