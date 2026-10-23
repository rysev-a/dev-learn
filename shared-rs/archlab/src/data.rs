//! Загрузка данных лаборатории и доступ к упражнениям.

use crate::blocks::{BlockDef, BlockLibrary, BlockSource, Solution};
use crate::exercise::*;
use crate::model::GateType;
use crate::registry;
use std::collections::BTreeMap;
use std::path::Path;

/// Откуда библиотека блоков берёт содержимое решённых упражнений.
pub trait SolutionStore {
    /// Решение упражнения `exercise_id` раздела `section`; `None` — не решено (блок закрыт).
    fn load(&self, section: &str, exercise_id: &str) -> Option<Solution>;
}

/// Все главы лаборатории (6–15), загруженные из файлов данных.
#[derive(Debug, Clone, Default)]
pub struct ArchLab {
    chapters: BTreeMap<u32, LabChapter>,
}

impl ArchLab {
    /// Из готовых глав; проверяет книгу, вид лаборатории и уникальность задач.
    pub fn from_chapters(list: Vec<LabChapter>) -> Result<ArchLab, String> {
        let mut chapters = BTreeMap::new();
        for c in list {
            if c.book != ARCH_BOOK || c.lab != "arch" {
                return Err(format!("глава {}: ожидалась книга {ARCH_BOOK} и lab = arch", c.chapter));
            }
            let mut seen = std::collections::HashSet::new();
            for t in &c.tasks {
                if !seen.insert(t.id.as_str()) {
                    return Err(format!("глава {}: повтор задачи «{}»", c.chapter, t.id));
                }
            }
            if chapters.insert(c.chapter, c).is_some() {
                return Err("повтор главы".into());
            }
        }
        Ok(ArchLab { chapters })
    }

    /// Из текстов файлов (JSON одной главы каждый).
    pub fn from_json<'a>(texts: impl IntoIterator<Item = &'a str>) -> Result<ArchLab, String> {
        let list = texts
            .into_iter()
            .map(|t| serde_json::from_str::<LabChapter>(t).map_err(|e| format!("файл главы: {e}")))
            .collect::<Result<Vec<_>, _>>()?;
        Self::from_chapters(list)
    }

    /// Из каталога `backend/app/data/labs/arch`: файлы `14-06.json` … `14-15.json` (чужие главы — RISC-V — пропускаются).
    pub fn load_dir(dir: &Path) -> Result<ArchLab, String> {
        let mut texts = Vec::new();
        for n in registry::chapters() {
            let path = dir.join(format!("{ARCH_BOOK}-{n:02}.json"));
            if path.exists() {
                texts.push(std::fs::read_to_string(&path).map_err(|e| format!("{}: {e}", path.display()))?);
            }
        }
        Self::from_json(texts.iter().map(String::as_str))
    }

    /// Глава по номеру.
    pub fn chapter(&self, n: u32) -> Option<&LabChapter> {
        self.chapters.get(&n)
    }

    /// Все главы по порядку.
    pub fn chapters(&self) -> impl Iterator<Item = &LabChapter> {
        self.chapters.values()
    }

    /// Упражнение главы по id.
    pub fn task(&self, chapter: u32, id: &str) -> Option<&Task> {
        self.chapters.get(&chapter)?.tasks.iter().find(|t| t.id == id)
    }

    /// Упражнение со схемой по разделу и id (для блоков: `source`).
    pub fn circuit_task(&self, section: &str, id: &str) -> Option<(&Task, &CircuitSpec)> {
        let chapter = registry::chapter_of_slug(section)?;
        let t = self.task(chapter, id)?;
        match &t.spec {
            Spec::Circuit(c) => Some((t, c)),
            Spec::Asm(_) => None,
        }
    }

    /// Упражнения главы для клиента — без эталонов.
    pub fn tasks_for_client(&self, chapter: u32) -> Vec<Task> {
        self.chapters.get(&chapter).map(|c| c.tasks.iter().map(Task::for_client).collect()).unwrap_or_default()
    }

    /// Библиотека блоков: определения — из упражнений с `block`, содержимое — из `store`.
    pub fn library(&self, store: &dyn SolutionStore) -> BlockLibrary {
        let mut lib = BlockLibrary::builtin();
        for info in registry::SECTIONS {
            let Some(ch) = self.chapters.get(&info.chapter) else { continue };
            for t in &ch.tasks {
                let Spec::Circuit(c) = &t.spec else { continue };
                let Some(meta) = &c.block else { continue };
                let def = BlockDef {
                    id: meta.id.clone(),
                    title: meta.title.clone(),
                    iface: c.interface(),
                    source: Some(BlockSource { section_slug: info.slug.to_string(), exercise_id: t.id.clone() }),
                };
                let hint = format!("Решите «{}» (практика «{}»)", t.title, info.title);
                lib.insert(def, store.load(info.slug, &t.id), hint);
            }
        }
        lib
    }

    /// Библиотека, в которой все блоки открыты эталонными решениями.
    pub fn reference_library(&self) -> BlockLibrary {
        self.library(&ReferenceStore(self))
    }

    /// Подсказка для закрытого составного элемента: что нужно собрать (`gateLockHint`).
    pub fn gate_lock_hint(&self, ty: GateType) -> String {
        let Some((slug, id)) = registry::composite_requirement(ty) else {
            return String::new();
        };
        let section = registry::section_by_slug(slug).map_or(slug, |s| s.title);
        let title = self.circuit_task(slug, id).map_or(id, |(t, _)| t.title.as_str());
        format!("Соберите «{title}» (практика «{section}»)")
    }
}

/// Хранилище эталонных решений: все блоки открыты.
pub struct ReferenceStore<'a>(pub &'a ArchLab);

impl SolutionStore for ReferenceStore<'_> {
    fn load(&self, section: &str, exercise_id: &str) -> Option<Solution> {
        self.0.circuit_task(section, exercise_id)?.1.solution.clone()
    }
}

/// Хранилище решений ученика: то, что осталось в кабинете как «решено» (аналог `hydrateLab`:
/// решённое переносится между главами, из него собираются составные блоки).
#[derive(Debug, Clone, Default)]
pub struct DraftStore {
    drafts: BTreeMap<(String, String), Solution>,
}

impl DraftStore {
    /// Пустое хранилище: все блоки закрыты.
    pub fn new() -> Self {
        Self::default()
    }

    /// Добавить решение (JSON, как его присылает клиент) упражнения `exercise_id` раздела `section`.
    /// Нерабочий JSON пропускается — как в `hydrate.ts` («не схема — пропускаем»).
    pub fn add(&mut self, section: &str, exercise_id: &str, json: &str) -> bool {
        match Solution::from_json(json) {
            Ok(s) => {
                self.drafts.insert((section.to_string(), exercise_id.to_string()), s);
                true
            }
            Err(_) => false,
        }
    }

    /// Собрать из записей кабинета `(глава, id упражнения, JSON решения)`.
    pub fn from_drafts<'a>(lab: &ArchLab, drafts: impl IntoIterator<Item = (u32, &'a str, &'a str)>) -> Self {
        let mut s = DraftStore::new();
        for (chapter, id, json) in drafts {
            if let Some(info) = registry::section_of_chapter(chapter) {
                if lab.task(chapter, id).is_some() {
                    s.add(info.slug, id, json);
                }
            }
        }
        s
    }
}

impl SolutionStore for DraftStore {
    fn load(&self, section: &str, exercise_id: &str) -> Option<Solution> {
        self.drafts.get(&(section.to_string(), exercise_id.to_string())).cloned()
    }
}
