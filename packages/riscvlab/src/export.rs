//! Format of the export from the previous TypeScript implementation (`frontend/scripts/riscv-export.mjs`) and conversion into course data.
//!
//! The export is an intermediate file: fields are named as in TypeScript (`text`, `solution`), checks are already data.
//! [`ExportChapter::into_lab_chapter`] builds the canonical [`LabChapter`] and validates it: the reference program of every
//! task must pass the check, and an empty program must not.

use serde::{Deserialize, Serialize};

use crate::task::{verify, Check, Lab, LabChapter, Profile, Task, TaskSpec, Test, DEFAULT_TASK_STEPS};

/// Export file.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Export {
    /// export format version
    pub version: u32,
    /// chapters
    pub chapters: Vec<ExportChapter>,
}

/// Chapter in the export.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ExportChapter {
    /// book number
    pub book: u32,
    /// chapter number
    pub chapter: u32,
    /// environment the programs run in
    pub profile: Profile,
    /// tasks
    pub tasks: Vec<ExportTask>,
}

/// Task in the export.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ExportTask {
    /// task identifier
    pub id: String,
    /// title
    pub title: String,
    /// statement
    pub text: String,
    /// hint
    pub hint: String,
    /// program starter
    pub starter: String,
    /// reference solution
    pub solution: String,
    /// task data (the `.data` section)
    pub data: String,
    #[serde(default)]
    /// switch positions (8 bits)
    pub switches: u8,
    #[serde(default)]
    /// step limit per test (200000 by default)
    pub max_steps: Option<u64>,
    /// check of the outcome
    pub check: Check,
}

/// What is wrong with the export.
#[derive(Debug, PartialEq, Eq)]
pub struct ExportError(pub String);

impl std::fmt::Display for ExportError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for ExportError {}

impl ExportChapter {
    /// Canonical chapter file with task validation.
    pub fn into_lab_chapter(self) -> Result<LabChapter, ExportError> {
        let mut tasks = Vec::new();
        for t in self.tasks {
            let spec = TaskSpec {
                profile: self.profile,
                starter: t.starter,
                reference: t.solution,
                data: t.data,
                max_steps: t.max_steps.unwrap_or(DEFAULT_TASK_STEPS),
                tests: vec![Test { switches: t.switches, regs: Vec::new(), check: t.check }],
            };
            let v = verify(&spec, &spec.reference);
            if !v.ok {
                return Err(ExportError(i18n::trf!("reference solution of task {0} fails verification: {1}", t.id, v.message)));
            }
            if verify(&spec, "").ok {
                return Err(ExportError(i18n::trf!("the empty program passes task {0}", t.id)));
            }
            tasks.push(Task { id: t.id, title: t.title, statement: t.text, hint: t.hint, spec });
        }
        Ok(LabChapter { book: self.book, chapter: self.chapter, lab: Lab::Riscv, tasks })
    }
}
