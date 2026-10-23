//! Файлы данных упражнений: `backend/app/data/labs/sd/<книга>-<глава:02>.json` — по файлу на главу.

use std::collections::HashSet;
use std::path::{Path, PathBuf};

use crate::error::SdError;
use crate::types::{LabChapter, Task};

/// Вид лаборатории в файлах данных.
pub const LAB: &str = "sd";
/// Номер книги «Системный дизайн».
pub const BOOK: u32 = 18;

/// Имя файла главы: `18-05.json`.
pub fn file_name(book: u32, chapter: u32) -> String {
    format!("{book}-{chapter:02}.json")
}

impl LabChapter {
    /// Разбор файла главы с проверкой: вид лаборатории, уникальность id.
    pub fn parse(json: &str) -> Result<LabChapter, SdError> {
        let mut ch: LabChapter = serde_json::from_str(json)?;
        if ch.lab != LAB {
            return Err(SdError::new(format!("глава {}: лаборатория «{}», а ожидается «{LAB}»", ch.chapter, ch.lab)));
        }
        let mut ids = HashSet::new();
        for t in &mut ch.tasks {
            if !ids.insert(t.id.clone()) {
                return Err(SdError::new(format!("глава {}: id упражнения повторяется: {}", ch.chapter, t.id)));
            }
            t.spec.start.normalize();
            t.spec.solution.normalize();
        }
        Ok(ch)
    }

    /// Упражнение по id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }
}

/// Читает один файл главы.
pub fn read_chapter(path: &Path) -> Result<LabChapter, SdError> {
    let text = std::fs::read_to_string(path).map_err(|e| SdError::new(format!("{}: {e}", path.display())))?;
    LabChapter::parse(&text).map_err(|e| SdError::new(format!("{}: {e}", path.display())))
}

/// Читает все главы каталога (`*.json`), по порядку номеров глав.
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
                return Err(SdError::new(format!("id упражнения повторяется между главами: {}", t.id)));
            }
        }
    }
    Ok(chapters)
}
