//! Формат выгрузки из прежней реализации на TypeScript (`frontend/scripts/riscv-export.mjs`) и перевод в данные курса.
//!
//! Выгрузка — промежуточный файл: поля названы, как в TypeScript (`text`, `solution`), проверки уже в виде данных.
//! [`ExportChapter::into_lab_chapter`] строит канонический [`LabChapter`] и проверяет его: эталонная программа каждой
//! задачи обязана проходить проверку, а пустая программа — нет.

use serde::{Deserialize, Serialize};

use crate::task::{verify, Check, Lab, LabChapter, Profile, Task, TaskSpec, Test, DEFAULT_TASK_STEPS};

/// Файл выгрузки.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Export {
    /// версия формата выгрузки
    pub version: u32,
    /// главы
    pub chapters: Vec<ExportChapter>,
}

/// Глава в выгрузке.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ExportChapter {
    /// номер книги
    pub book: u32,
    /// номер главы
    pub chapter: u32,
    /// окружение, в котором работают программы
    pub profile: Profile,
    /// задачи
    pub tasks: Vec<ExportTask>,
}

/// Задача в выгрузке.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ExportTask {
    /// идентификатор задачи
    pub id: String,
    /// название
    pub title: String,
    /// условие
    pub text: String,
    /// подсказка
    pub hint: String,
    /// заготовка программы
    pub starter: String,
    /// эталонное решение
    pub solution: String,
    /// данные задания (секция `.data`)
    pub data: String,
    #[serde(default)]
    /// положение переключателей (8 бит)
    pub switches: u8,
    #[serde(default)]
    /// лимит шагов на тест (по умолчанию 200000)
    pub max_steps: Option<u64>,
    /// проверка итога
    pub check: Check,
}

/// Что не так с выгрузкой.
#[derive(Debug, PartialEq, Eq)]
pub struct ExportError(pub String);

impl std::fmt::Display for ExportError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for ExportError {}

impl ExportChapter {
    /// Канонический файл главы с проверкой задач.
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
                return Err(ExportError(format!("эталон задачи {} не проходит проверку: {}", t.id, v.message)));
            }
            if verify(&spec, "").ok {
                return Err(ExportError(format!("пустая программа проходит задачу {}", t.id)));
            }
            tasks.push(Task { id: t.id, title: t.title, statement: t.text, hint: t.hint, spec });
        }
        Ok(LabChapter { book: self.book, chapter: self.chapter, lab: Lab::Riscv, tasks })
    }
}
