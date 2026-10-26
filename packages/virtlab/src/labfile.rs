//! Файл данных главы: `backend/data/labs/virt/<книга>-<глава:02>.json`.

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::error::SpecError;
use crate::spec::Spec;
use crate::verify::{verify_with, Strictness, Verdict};

/// Упражнение-симулятор.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Task {
    /// Идентификатор упражнения (`virt-sim-hv`…).
    pub id: String,
    /// Название.
    pub title: String,
    /// Условие.
    pub statement: String,
    /// Подсказка.
    pub hint: String,
    /// Описание симулятора: модуль, сценарии, цели.
    pub spec: Spec,
}

impl Task {
    /// Проверить присланное решение (JSON `{идентификатор цели: данные, …}`), см. [`mod@crate::verify`].
    pub fn verify(&self, submitted: &Value) -> Verdict {
        verify_with(&self.spec, submitted, Strictness::Lenient)
    }
}

/// Файл главы: упражнения-симуляторы одной главы одной книги.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    /// Номер книги (17).
    pub book: u32,
    /// Номер главы.
    pub chapter: u32,
    /// Вид лаборатории (`"virt"`).
    pub lab: String,
    /// Упражнения главы по порядку.
    pub tasks: Vec<Task>,
}

impl LabChapter {
    /// Разобрать файл главы.
    pub fn from_json(text: &str) -> Result<LabChapter, SpecError> {
        serde_json::from_str(text).map_err(|e| SpecError::new(format!("разбор файла главы: {e}")))
    }

    /// Канонический JSON файла: отступ 2 пробела, порядок полей как в структурах, перевод строки в конце.
    pub fn to_canonical_json(&self) -> Result<String, SpecError> {
        let mut s =
            serde_json::to_string_pretty(self).map_err(|e| SpecError::new(format!("запись файла главы: {e}")))?;
        s.push('\n');
        Ok(s)
    }

    /// Имя файла: `17-02.json`.
    pub fn file_name(&self) -> String {
        format!("{}-{:02}.json", self.book, self.chapter)
    }

    /// Проверка: книга и вид лаборатории верны, упражнения уникальны, описания целы.
    pub fn validate(&self) -> Result<(), SpecError> {
        if self.lab != "virt" {
            return Err(SpecError::new(format!("вид лаборатории «{}», ожидается «virt»", self.lab)));
        }
        if self.tasks.is_empty() {
            return Err(SpecError::new("в главе нет упражнений"));
        }
        let mut seen = std::collections::BTreeSet::new();
        for t in &self.tasks {
            if !seen.insert(t.id.clone()) {
                return Err(SpecError::new(format!("повтор упражнения «{}»", t.id)));
            }
            t.spec.validate().map_err(|e| SpecError::new(format!("{}: {e}", t.id)))?;
        }
        Ok(())
    }
}

/// Определение упражнения из `labs.py` (`data/tasks.json` — снимок определений прежней реализации, фикстура тестов).
#[derive(Clone, Debug, Deserialize)]
struct Definition {
    chapter: u32,
    id: String,
    title: String,
    statement: String,
    hint: String,
}

/// Книга, к которой относятся упражнения.
pub const BOOK: u32 = 17;

/// Собрать файлы глав: определения (id, название, условие, подсказка, глава) из выгрузки `labs.py` плюс описание
/// симулятора по умолчанию ([`crate::builtin`]). Главы по возрастанию номера.
pub fn build_chapters(definitions_json: &str) -> Result<Vec<LabChapter>, SpecError> {
    let defs: Vec<Definition> =
        serde_json::from_str(definitions_json).map_err(|e| SpecError::new(format!("разбор определений: {e}")))?;
    let mut by_chapter: std::collections::BTreeMap<u32, Vec<Task>> = Default::default();
    for d in defs {
        let spec =
            crate::builtin(&d.id).ok_or_else(|| SpecError::new(format!("нет описания симулятора «{}»", d.id)))?;
        by_chapter.entry(d.chapter).or_default().push(Task {
            id: d.id,
            title: d.title,
            statement: d.statement,
            hint: d.hint,
            spec,
        });
    }
    let chapters: Vec<LabChapter> = by_chapter
        .into_iter()
        .map(|(chapter, tasks)| LabChapter { book: BOOK, chapter, lab: "virt".into(), tasks })
        .collect();
    for c in &chapters {
        c.validate()?;
    }
    Ok(chapters)
}
