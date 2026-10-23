//! Перевод выгрузки из TypeScript (`frontend/scripts/sd-export.mjs`) в канонические файлы данных и «золотые» файлы
//! для дифференциальных тестов. Нужен один раз (и при изменении исходных сценариев): рабочие данные дальше правят в JSON.

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::data::LAB;
use crate::error::SdError;
use crate::types::{EvalOptions, EvalResult, Goal, GoalResult, Kind, LabChapter, Scenario, SdEdge, SdState, Task, Workload};

/// Сценарий в выгрузке: поля прежнего `SdScenario` (названия — как в TypeScript).
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

/// Состояние в золотом случае: ссылка на схему упражнения (`"start"`, `"solution"`) или схема целиком.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum CaseState {
    Ref(String),
    Inline(SdState),
}

/// Золотой случай: результат TypeScript-движка на схеме при нагрузке и отказах.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Case {
    pub label: String,
    pub state: CaseState,
    /// нагрузка (если не задана — нагрузка упражнения)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub workload: Option<Workload>,
    #[serde(default)]
    pub opts: EvalOptions,
    pub result: EvalResult,
    /// результаты `checkGoals` по целям упражнения (если выгружены)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub goals: Option<Vec<GoalResult>>,
}

/// Автосвязи: какие связи подставило поле TypeScript для узла эталона, у которого убрали все связи.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SuggestCase {
    pub node: String,
    pub edges: Vec<SdEdge>,
}

/// Золотые результаты одного упражнения.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Golden {
    pub cases: Vec<Case>,
    #[serde(default)]
    pub suggest: Vec<SuggestCase>,
}

/// Золотой файл главы (`tests/golden/18-NN.json`).
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

/// Цель из выгрузки: поле `k` называется теперь `type`.
fn goal(mut v: Value) -> Result<Goal, SdError> {
    if let Some(m) = v.as_object_mut() {
        if let Some(k) = m.remove("k") {
            m.insert("type".into(), k);
        }
    }
    Ok(serde_json::from_value(v)?)
}

/// Разбирает файл выгрузки одной главы: канонические данные и золотые случаи.
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
