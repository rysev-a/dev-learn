//! Converts the TypeScript export (`frontend/scripts/sd-export.mjs`) into canonical data files and "golden" files
//! for differential tests. Needed once (and when the source scenarios change): working data is edited in JSON afterwards.

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::data::LAB;
use crate::error::SdError;
use crate::types::{EvalOptions, EvalResult, Goal, GoalResult, Kind, LabChapter, Scenario, SdEdge, SdState, Task, Workload};

/// Scenario in the export: fields of the former `SdScenario` (names as in TypeScript).
#[derive(Debug, Deserialize)]
struct RawTask {
    id: String,
    title: String,
    statement: String,
    hint: String,
    workload: Workload,
    palette: Vec<Kind>,
    start: SdState,
    goals: Vec<Value>,
    solution: SdState,
    #[serde(default, rename = "maxNodes")]
    max_nodes: Option<usize>,
    #[serde(default)]
    show: Vec<String>,
    golden: Golden,
}

#[derive(Debug, Deserialize)]
struct RawChapter {
    book: u32,
    chapter: u32,
    tasks: Vec<RawTask>,
}

/// State in a golden case: a reference to the exercise design (`"start"`, `"solution"`) or the whole design.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum CaseState {
    Ref(String),
    Inline(SdState),
}

/// Golden case: the TypeScript engine's result on a design under a workload and failures.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Case {
    pub label: String,
    pub state: CaseState,
    /// workload (if not set — the exercise workload)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub workload: Option<Workload>,
    #[serde(default)]
    pub opts: EvalOptions,
    pub result: EvalResult,
    /// `checkGoals` results for the exercise goals (if exported)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub goals: Option<Vec<GoalResult>>,
}

/// Auto-links: which links the TypeScript board suggested for a reference-solution node with all links removed.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SuggestCase {
    pub node: String,
    pub edges: Vec<SdEdge>,
}

/// Golden results of one exercise.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Golden {
    pub cases: Vec<Case>,
    #[serde(default)]
    pub suggest: Vec<SuggestCase>,
}

/// Golden file of a chapter (`tests/golden/18-NN.json`).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GoldenChapter {
    pub book: u32,
    pub chapter: u32,
    pub tasks: Vec<GoldenTask>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GoldenTask {
    pub id: String,
    pub cases: Vec<Case>,
    #[serde(default)]
    pub suggest: Vec<SuggestCase>,
}

/// Goal from the export: the `k` field is now called `type`.
fn goal(mut v: Value) -> Result<Goal, SdError> {
    if let Some(m) = v.as_object_mut() {
        if let Some(k) = m.remove("k") {
            m.insert("type".into(), k);
        }
    }
    Ok(serde_json::from_value(v)?)
}

/// Parses one chapter's export file: canonical data and golden cases.
pub fn convert(json: &str) -> Result<(LabChapter, GoldenChapter), SdError> {
    let raw: RawChapter = serde_json::from_str(json)?;
    let mut tasks = Vec::new();
    let mut golden = Vec::new();
    for t in raw.tasks {
        golden.push(GoldenTask { id: t.id.clone(), cases: t.golden.cases, suggest: t.golden.suggest });
        let max_nodes = t.max_nodes;
        let show = t.show.iter().map(|s| crate::kinds::canonical_show_key(s)).collect();
        let goals = t.goals.into_iter().map(goal).collect::<Result<Vec<_>, _>>()?;
        let spec = Scenario { workload: t.workload, palette: t.palette, start: t.start, goals, solution: t.solution, max_nodes, show };
        tasks.push(Task { id: t.id, title: t.title, statement: t.statement, hint: t.hint, spec });
    }
    Ok((LabChapter { book: raw.book, chapter: raw.chapter, lab: LAB.to_owned(), tasks }, GoldenChapter { book: raw.book, chapter: raw.chapter, tasks: golden }))
}
