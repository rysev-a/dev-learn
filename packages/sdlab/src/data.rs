//! Exercise data files: `backend/data/labs/sd/<book>-<chapter:02>.json` — one file per chapter.

use std::collections::HashSet;
use std::path::{Path, PathBuf};

use crate::error::SdError;
use crate::types::{LabChapter, Task};

/// Lab kind in the data files.
pub const LAB: &str = "sd";
/// Number of the "System design" book.
pub const BOOK: u32 = 18;

/// Chapter file name: `18-05.json`.
pub fn file_name(book: u32, chapter: u32) -> String {
    format!("{book}-{chapter:02}.json")
}

impl LabChapter {
    /// Parses a chapter file with validation: lab kind, id uniqueness.
    pub fn parse(json: &str) -> Result<LabChapter, SdError> {
        let mut ch: LabChapter = serde_json::from_str(json)?;
        if ch.lab != LAB {
            return Err(SdError::new(i18n::trf!("chapter {0}: lab “{1}”, but “{2}” is expected", ch.chapter, ch.lab, LAB)));
        }
        let mut ids = HashSet::new();
        for t in &mut ch.tasks {
            if !ids.insert(t.id.clone()) {
                return Err(SdError::new(i18n::trf!("chapter {0}: exercise id is repeated: {1}", ch.chapter, t.id)));
            }
            t.spec.start.normalize();
            t.spec.solution.normalize();
        }
        Ok(ch)
    }

    /// Exercise by id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }
}

/// Reads one chapter file.
pub fn read_chapter(path: &Path) -> Result<LabChapter, SdError> {
    let text = std::fs::read_to_string(path).map_err(|e| SdError::new(format!("{}: {e}", path.display())))?;
    LabChapter::parse(&text).map_err(|e| SdError::new(format!("{}: {e}", path.display())))
}

/// Reads all chapters of a directory (`*.json`), in chapter number order.
pub fn read_dir(dir: &Path) -> Result<Vec<LabChapter>, SdError> {
    let mut paths: Vec<PathBuf> = std::fs::read_dir(dir)
        .map_err(|e| SdError::new(format!("{}: {e}", dir.display())))?
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| p.extension().is_some_and(|x| x == "json"))
        .collect();
    paths.sort();
    let mut chapters = paths.iter().map(|p| read_chapter(p)).collect::<Result<Vec<_>, _>>()?;
    chapters.sort_by_key(|c| (c.book, c.chapter));
    let mut ids = HashSet::new();
    for c in &chapters {
        for t in &c.tasks {
            if !ids.insert(t.id.as_str()) {
                return Err(SdError::new(i18n::trf!("exercise id is repeated across chapters: {0}", t.id)));
            }
        }
    }
    Ok(chapters)
}
