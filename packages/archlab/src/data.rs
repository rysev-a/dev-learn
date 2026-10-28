//! Loading lab data and accessing exercises.

use crate::blocks::{BlockDef, BlockLibrary, BlockSource, Solution};
use crate::exercise::*;
use crate::model::GateType;
use crate::registry;
use std::collections::BTreeMap;
use std::path::Path;

/// Where the block library takes the contents of solved exercises from.
pub trait SolutionStore {
    /// Solution of exercise `exercise_id` in section `section`; `None` — not solved (block locked).
    fn load(&self, section: &str, exercise_id: &str) -> Option<Solution>;
}

/// All lab chapters (6–15) loaded from data files.
#[derive(Debug, Clone, Default)]
pub struct ArchLab {
    chapters: BTreeMap<u32, LabChapter>,
}

impl ArchLab {
    /// From ready-made chapters; checks the book, the lab kind and task uniqueness.
    pub fn from_chapters(list: Vec<LabChapter>) -> Result<ArchLab, String> {
        let mut chapters = BTreeMap::new();
        for c in list {
            if c.book != ARCH_BOOK || c.lab != "arch" {
                return Err(i18n::trf!("chapter {0}: expected book {1} and lab = arch", c.chapter, ARCH_BOOK));
            }
            let mut seen = std::collections::HashSet::new();
            for t in &c.tasks {
                if !seen.insert(t.id.as_str()) {
                    return Err(i18n::trf!("chapter {0}: duplicate task “{1}”", c.chapter, t.id));
                }
            }
            if chapters.insert(c.chapter, c).is_some() {
                return Err(i18n::tr("duplicate chapter").into());
            }
        }
        Ok(ArchLab { chapters })
    }

    /// From file contents (one chapter JSON each).
    pub fn from_json<'a>(texts: impl IntoIterator<Item = &'a str>) -> Result<ArchLab, String> {
        let list = texts
            .into_iter()
            .map(|t| serde_json::from_str::<LabChapter>(t).map_err(|e| i18n::trf!("chapter file: {0}", e)))
            .collect::<Result<Vec<_>, _>>()?;
        Self::from_chapters(list)
    }

    /// From the `backend/data/labs/arch` directory: files `14-06.json` … `14-15.json` (foreign chapters — RISC-V — are skipped).
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

    /// Chapter by number.
    pub fn chapter(&self, n: u32) -> Option<&LabChapter> {
        self.chapters.get(&n)
    }

    /// All chapters in order.
    pub fn chapters(&self) -> impl Iterator<Item = &LabChapter> {
        self.chapters.values()
    }

    /// Chapter exercise by id.
    pub fn task(&self, chapter: u32, id: &str) -> Option<&Task> {
        self.chapters.get(&chapter)?.tasks.iter().find(|t| t.id == id)
    }

    /// Circuit exercise by section and id (for blocks: `source`).
    pub fn circuit_task(&self, section: &str, id: &str) -> Option<(&Task, &CircuitSpec)> {
        let chapter = registry::chapter_of_slug(section)?;
        let t = self.task(chapter, id)?;
        match &t.spec {
            Spec::Circuit(c) => Some((t, c)),
            Spec::Asm(_) => None,
        }
    }

    /// Chapter exercises for the client — without reference solutions.
    pub fn tasks_for_client(&self, chapter: u32) -> Vec<Task> {
        self.chapters.get(&chapter).map(|c| c.tasks.iter().map(Task::for_client).collect()).unwrap_or_default()
    }

    /// Block library: definitions — from exercises with `block`, contents — from `store`.
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
                let hint = i18n::trf!("Solve “{0}” (practice “{1}”)", t.title, i18n::tr(info.title));
                lib.insert(def, store.load(info.slug, &t.id), hint);
            }
        }
        lib
    }

    /// Library in which all blocks are unlocked by reference solutions.
    pub fn reference_library(&self) -> BlockLibrary {
        self.library(&ReferenceStore(self))
    }

    /// Hint for a locked composite element: what needs to be built (`gateLockHint`).
    pub fn gate_lock_hint(&self, ty: GateType) -> String {
        let Some((slug, id)) = registry::composite_requirement(ty) else {
            return String::new();
        };
        let section = registry::section_by_slug(slug).map_or(slug, |s| i18n::tr(s.title));
        let title = self.circuit_task(slug, id).map_or(id, |(t, _)| t.title.as_str());
        i18n::trf!("Build “{0}” (practice “{1}”)", title, section)
    }
}

/// Store of reference solutions: all blocks unlocked.
pub struct ReferenceStore<'a>(pub &'a ArchLab);

impl SolutionStore for ReferenceStore<'_> {
    fn load(&self, section: &str, exercise_id: &str) -> Option<Solution> {
        self.0.circuit_task(section, exercise_id)?.1.solution.clone()
    }
}

/// Store of the student's solutions: what is left in the account as "solved" (analog of `hydrateLab`:
/// solved work carries over between chapters, composite blocks are built from it).
#[derive(Debug, Clone, Default)]
pub struct DraftStore {
    drafts: BTreeMap<(String, String), Solution>,
}

impl DraftStore {
    /// Empty store: all blocks locked.
    pub fn new() -> Self {
        Self::default()
    }

    /// Add a solution (JSON as sent by the client) of exercise `exercise_id` in section `section`.
    /// Broken JSON is skipped — as in `hydrate.ts` ("not a circuit — skip").
    pub fn add(&mut self, section: &str, exercise_id: &str, json: &str) -> bool {
        match Solution::from_json(json) {
            Ok(s) => {
                self.drafts.insert((section.to_string(), exercise_id.to_string()), s);
                true
            }
            Err(_) => false,
        }
    }

    /// Build from account records `(chapter, exercise id, solution JSON)`.
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
