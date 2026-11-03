//! Chapter data file: `backend/data/labs/virt/<book>-<chapter:02>.json` (book 17 "Virtualization", book 19 "Linux Administration").

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::error::SpecError;
use crate::spec::Spec;
use crate::verify::{verify_with, Strictness, Verdict};

/// Simulator exercise.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Task {
    /// Exercise identifier (`virt-sim-hv`…).
    pub id: String,
    /// Title.
    pub title: String,
    /// Statement.
    pub statement: String,
    /// Hint.
    pub hint: String,
    /// Simulator description: module, scenarios, goals.
    pub spec: Spec,
}

impl Task {
    /// Check a submitted solution (JSON `{goal id: data, …}`), see [`mod@crate::verify`].
    pub fn verify(&self, submitted: &Value) -> Verdict {
        verify_with(&self.spec, submitted, Strictness::Lenient)
    }
}

/// Chapter file: simulator exercises of one chapter of one book.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    /// Book number (17, or 19 for the LVM board).
    pub book: u32,
    /// Chapter number.
    pub chapter: u32,
    /// Lab kind (`"virt"`).
    pub lab: String,
    /// Chapter exercises in order.
    pub tasks: Vec<Task>,
}

impl LabChapter {
    /// Parse a chapter file.
    pub fn from_json(text: &str) -> Result<LabChapter, SpecError> {
        serde_json::from_str(text).map_err(|e| SpecError::new(i18n::trf!("parsing the chapter file: {0}", e)))
    }

    /// Canonical JSON of the file: 2-space indent, field order as in the structs, trailing newline.
    pub fn to_canonical_json(&self) -> Result<String, SpecError> {
        let mut s =
            serde_json::to_string_pretty(self).map_err(|e| SpecError::new(i18n::trf!("writing the chapter file: {0}", e)))?;
        s.push('\n');
        Ok(s)
    }

    /// File name: `17-02.json`.
    pub fn file_name(&self) -> String {
        format!("{}-{:02}.json", self.book, self.chapter)
    }

    /// Validation: book and lab kind are correct, exercises are unique, descriptions are intact.
    pub fn validate(&self) -> Result<(), SpecError> {
        if self.lab != "virt" {
            return Err(SpecError::new(i18n::trf!("lab kind “{0}”, expected “virt”", self.lab)));
        }
        if self.tasks.is_empty() {
            return Err(SpecError::new(i18n::tr("the chapter has no exercises")));
        }
        let mut seen = std::collections::BTreeSet::new();
        for t in &self.tasks {
            if !seen.insert(t.id.clone()) {
                return Err(SpecError::new(i18n::trf!("duplicate exercise “{0}”", t.id)));
            }
            t.spec.validate().map_err(|e| SpecError::new(format!("{}: {e}", t.id)))?;
        }
        Ok(())
    }
}

/// Exercise definition from `labs.py` (`data/tasks.json` is a snapshot of the former implementation's definitions, a test fixture).
#[derive(Clone, Debug, Deserialize)]
struct Definition {
    /// Book the exercise belongs to (17 when the definition does not say).
    #[serde(default = "default_book")]
    book: u32,
    chapter: u32,
    id: String,
    title: String,
    statement: String,
    hint: String,
}

/// Book the exercises belong to unless a definition says otherwise.
pub const BOOK: u32 = 17;

fn default_book() -> u32 {
    BOOK
}

/// Build chapter files: definitions (id, title, statement, hint, chapter) from the `labs.py` export plus the default
/// simulator description ([`crate::builtin`]). Chapter files in ascending order of the book and then of the chapter.
pub fn build_chapters(definitions_json: &str) -> Result<Vec<LabChapter>, SpecError> {
    let defs: Vec<Definition> =
        serde_json::from_str(definitions_json).map_err(|e| SpecError::new(i18n::trf!("parsing definitions: {0}", e)))?;
    let mut by_chapter: std::collections::BTreeMap<(u32, u32), Vec<Task>> = Default::default();
    for d in defs {
        let spec =
            crate::builtin(&d.id).ok_or_else(|| SpecError::new(i18n::trf!("no description for simulator “{0}”", d.id)))?;
        by_chapter.entry((d.book, d.chapter)).or_default().push(Task {
            id: d.id,
            title: d.title,
            statement: d.statement,
            hint: d.hint,
            spec,
        });
    }
    let chapters: Vec<LabChapter> = by_chapter
        .into_iter()
        .map(|((book, chapter), tasks)| LabChapter { book, chapter, lab: "virt".into(), tasks })
        .collect();
    for c in &chapters {
        c.validate()?;
    }
    Ok(chapters)
}
