//! Серверная проверка решения: схема, присланная учеником, действительно выполняет цели упражнения и не нарушает
//! его ограничений (палитра, число узлов, допустимые связи и значения параметров). Раньше решению доверял клиент.

use std::collections::HashSet;

use serde::Serialize;
use serde_json::Value;

use crate::checks::{all_ok, check_goals};
use crate::engine::{can_link, evaluate};
use crate::error::SdError;
use crate::kinds::{param_spec, ParamType};
use crate::ports::reaches;
use crate::types::{EvalOptions, Goal, GoalResult, Kind, ParamValue, Scenario, SdState, Task};

/// Предел размера присланного решения, байт.
pub const MAX_SOLUTION_BYTES: usize = 1 << 20;

/// Нарушение ограничений упражнения.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Problem {
    /// на схеме нет компонента «Пользователи»
    NoClients,
    /// «Пользователей» больше одного
    ManyClients { count: usize },
    /// на схеме нет ни одного компонента
    Empty,
    DuplicateNode { id: String },
    /// компонентов больше, чем разрешено упражнением
    TooManyNodes { count: usize, max: usize },
    /// связь ведёт к несуществующему компоненту
    UnknownEdgeEnd { from: String, to: String },
    /// такие компоненты в модели не соединяются
    BadLink { from: String, to: String },
    DuplicateEdge { from: String, to: String },
    /// связь замыкает цикл
    Cycle { from: String, to: String },
    /// компонент вне палитры упражнения
    OutsidePalette { node: String, kind: Kind },
    /// значение параметра недопустимо (неизвестный ключ, не из списка, вне диапазона)
    BadParam { node: String, key: String, reason: String },
    /// параметр скрыт в этом упражнении, менять его нельзя
    HiddenParam { node: String, key: String },
}

impl std::fmt::Display for Problem {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Problem::NoClients => f.write_str(i18n::tr("the diagram has no “Users” component")),
            Problem::ManyClients { count } => write!(f, "{}", i18n::trf!("there must be exactly one “Users” component, but there are {0}", count)),
            Problem::Empty => f.write_str(i18n::tr("the diagram is empty")),
            Problem::DuplicateNode { id } => write!(f, "{}", i18n::trf!("component id is repeated: {0}", id)),
            Problem::TooManyNodes { count, max } => write!(f, "{}", i18n::trf!("the diagram has {0} components, but at most {1} are allowed", count, max)),
            Problem::UnknownEdgeEnd { from, to } => write!(f, "{}", i18n::trf!("link {0} → {1} points to a nonexistent component", from, to)),
            Problem::BadLink { from, to } => write!(f, "{}", i18n::trf!("link {0} → {1}: these components cannot be linked", from, to)),
            Problem::DuplicateEdge { from, to } => write!(f, "{}", i18n::trf!("link {0} → {1} is repeated", from, to)),
            Problem::Cycle { from, to } => write!(f, "{}", i18n::trf!("link {0} → {1} closes a cycle", from, to)),
            Problem::OutsidePalette { node, kind } => write!(f, "{}", i18n::trf!("component {0} ({1}) is not available in this exercise", node, kind)),
            Problem::BadParam { node, key, reason } => write!(f, "{}", i18n::trf!("component {0}: parameter {1}: {2}", node, key, reason)),
            Problem::HiddenParam { node, key } => write!(f, "{}", i18n::trf!("component {0}: parameter {1} cannot be changed in this exercise", node, key)),
        }
    }
}

/// Итог проверки решения.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Verdict {
    /// решение засчитывается: нет нарушений и выполнены все цели
    pub ok: bool,
    /// результат по каждой цели, в порядке целей упражнения (пусто, если схему считать не стали)
    pub goals: Vec<GoalResult>,
    /// нарушения ограничений упражнения
    pub problems: Vec<Problem>,
}

impl Verdict {
    /// Сообщение для ответа клиенту: первое нарушение или первая невыполненная цель.
    pub fn reason(&self) -> Option<String> {
        if let Some(p) = self.problems.first() {
            return Some(p.to_string());
        }
        self.goals.iter().find(|g| !g.ok).map(|g| i18n::trf!("goal not met: {0} ({1})", g.text, g.detail))
    }
}

/// Разбор решения, присланного клиентом: JSON-строка состояния схемы (как её хранит черновик) либо уже разобранный
/// объект; терпимо к обёрткам `{"state": …}` / `{"solution": …}`, двойной сериализации, пропущенным названиям и координатам.
pub fn parse_solution(raw: &str) -> Result<SdState, SdError> {
    if raw.len() > MAX_SOLUTION_BYTES {
        return Err(SdError::new(i18n::tr("the solution is too large")));
    }
    state_from_value(serde_json::from_str(raw)?)
}

/// То же для уже разобранного JSON.
pub fn state_from_value(v: Value) -> Result<SdState, SdError> {
    let mut v = v;
    for _ in 0..4 {
        match v {
            Value::String(ref s) => v = serde_json::from_str(s)?,
            Value::Object(ref m) if !m.contains_key("nodes") => {
                let inner = m.get("state").or_else(|| m.get("solution")).cloned();
                match inner {
                    Some(i) => v = i,
                    None => return Err(SdError::new(i18n::tr("the solution has no nodes field"))),
                }
            }
            Value::Object(_) => {
                let mut s: SdState = serde_json::from_value(v).map_err(|e| SdError::new(i18n::trf!("the diagram could not be parsed: {0}", e)))?;
                s.normalize();
                return Ok(s);
            }
            _ => return Err(SdError::new(i18n::tr("the solution must be an object with nodes and edges lists"))),
        }
    }
    Err(SdError::new(i18n::tr("the solution is nested too deeply")))
}

/// Нарушения ограничений упражнения (без расчёта).
pub fn problems(sc: &Scenario, s: &SdState) -> Vec<Problem> {
    let mut out = Vec::new();
    if s.nodes.is_empty() {
        out.push(Problem::Empty);
    }
    match s.of_kind(Kind::Clients).count() {
        0 => out.push(Problem::NoClients),
        1 => {}
        count => out.push(Problem::ManyClients { count }),
    }
    let max = sc.max_nodes();
    if s.nodes.len() > max {
        out.push(Problem::TooManyNodes { count: s.nodes.len(), max });
    }
    let mut ids: HashSet<&str> = HashSet::new();
    for n in &s.nodes {
        if !ids.insert(n.id.as_str()) {
            out.push(Problem::DuplicateNode { id: n.id.clone() });
        }
    }
    // связи: по порядку, как их ставит интерфейс (без повторов и циклов)
    let mut accepted: Vec<crate::types::SdEdge> = Vec::new();
    for e in &s.edges {
        let (Some(a), Some(b)) = (s.node(&e.from), s.node(&e.to)) else {
            out.push(Problem::UnknownEdgeEnd { from: e.from.clone(), to: e.to.clone() });
            continue;
        };
        if !can_link(a.kind, b.kind) {
            out.push(Problem::BadLink { from: e.from.clone(), to: e.to.clone() });
        } else if accepted.iter().any(|x| x == e) {
            out.push(Problem::DuplicateEdge { from: e.from.clone(), to: e.to.clone() });
        } else if e.from == e.to || reaches(&accepted, &e.to, &e.from) {
            out.push(Problem::Cycle { from: e.from.clone(), to: e.to.clone() });
        } else {
            accepted.push(e.clone());
        }
    }
    // палитра: пользователи, мониторинг и всё, что стояло на исходной схеме, доступны всегда
    for n in &s.nodes {
        let free = matches!(n.kind, Kind::Clients | Kind::Monitor) || sc.palette.contains(&n.kind) || sc.start.nodes.iter().any(|x| x.kind == n.kind);
        if !free {
            out.push(Problem::OutsidePalette { node: n.id.clone(), kind: n.kind });
        }
    }
    // параметры: только известные, допустимых значений; скрытые в этом упражнении — как на исходной схеме
    for n in &s.nodes {
        for (key, value) in &n.params {
            if let Some(reason) = param_problem(n.kind, key, value) {
                out.push(Problem::BadParam { node: n.id.clone(), key: key.clone(), reason });
            }
        }
        for p in &crate::kinds::spec(n.kind).params {
            if sc.param_visible(n.kind, p) || (p.inert && !references(sc, n.kind, p.key)) {
                continue;
            }
            let original = sc.start.node(&n.id).filter(|o| o.kind == n.kind).map_or(&p.default, |o| o.param(p.key));
            if n.param(p.key) != original {
                out.push(Problem::HiddenParam { node: n.id.clone(), key: p.key.to_owned() });
            }
        }
    }
    out
}

/// Ссылается ли на параметр какая-нибудь цель упражнения.
fn references(sc: &Scenario, kind: Kind, key: &str) -> bool {
    sc.goals.iter().any(|g| matches!(g, Goal::Param { kind: k, key: kk, .. } if *k == kind && kk == key))
}

fn param_problem(kind: Kind, key: &str, value: &ParamValue) -> Option<String> {
    let Some(spec) = param_spec(kind, key) else {
        return Some(i18n::tr("unknown parameter").into());
    };
    match (spec.ty, value) {
        (ParamType::Bool, ParamValue::Bool(_)) => None,
        (ParamType::Bool, _) => Some(i18n::tr("yes/no expected").into()),
        (ParamType::Int, ParamValue::Num(x)) => {
            let (lo, hi) = (spec.min.unwrap_or(f64::MIN), spec.max.unwrap_or(f64::MAX));
            if !x.is_finite() || x.fract() != 0.0 {
                Some(i18n::tr("an integer expected").into())
            } else if *x < lo || *x > hi {
                Some(i18n::trf!("value out of range {0}–{1}", lo, hi))
            } else {
                None
            }
        }
        (ParamType::Int, _) => Some(i18n::tr("a number expected").into()),
        (ParamType::Select, v) => (!spec.options.iter().any(|o| &o.value == v)).then(|| i18n::tr("value is not in the list").to_owned()),
    }
}

/// Проверка решения упражнения: нарушения ограничений и цели. Схему считают, только если число узлов в пределах
/// упражнения (иначе расчёт не нужен, а цена ошибки — время сервера).
pub fn verify(sc: &Scenario, submitted: &SdState) -> Verdict {
    let mut s = submitted.clone();
    s.normalize();
    let problems = problems(sc, &s);
    let goals = if s.nodes.len() <= sc.max_nodes() {
        let base = evaluate(&s, &sc.workload, &EvalOptions::default());
        check_goals(&s, &sc.workload, &sc.goals, Some(&base))
    } else {
        Vec::new()
    };
    let ok = problems.is_empty() && !s.nodes.is_empty() && !goals.is_empty() && all_ok(&goals);
    Verdict { ok, goals, problems }
}

/// Проверка решения, присланного строкой (`PUT …/solved`, поле `solution`).
pub fn verify_raw(sc: &Scenario, raw: &str) -> Result<Verdict, SdError> {
    Ok(verify(sc, &parse_solution(raw)?))
}

/// Самопроверка упражнения (порт `sd-selfcheck`): исходная схема не решает его, эталон решает, всё в рамках ограничений.
#[derive(Debug, Clone, PartialEq)]
pub struct SelfCheck {
    /// сколько целей не выполнено в исходной схеме
    pub start_failed: usize,
    /// цели исходной схемы
    pub start: Vec<GoalResult>,
    /// цели эталона
    pub solution: Vec<GoalResult>,
    /// компоненты эталона вне палитры (и не стоявшие на исходной схеме)
    pub outside: Vec<Kind>,
    /// в эталоне больше узлов, чем разрешено
    pub too_many: bool,
}

impl SelfCheck {
    /// Всё в порядке: исходная схема не проходит, эталон проходит, ограничения соблюдены.
    pub fn is_ok(&self) -> bool {
        self.start_failed > 0 && all_ok(&self.solution) && self.outside.is_empty() && !self.too_many
    }
}

/// Самопроверка одного упражнения.
pub fn self_check(task: &Task) -> SelfCheck {
    let sc = &task.spec;
    let start = check_goals(&sc.start, &sc.workload, &sc.goals, None);
    let solution = check_goals(&sc.solution, &sc.workload, &sc.goals, None);
    let mut outside: Vec<Kind> = Vec::new();
    for n in &sc.solution.nodes {
        let k = n.kind;
        if k != Kind::Clients && k != Kind::Monitor && !sc.palette.contains(&k) && !sc.start.nodes.iter().any(|x| x.kind == k) && !outside.contains(&k) {
            outside.push(k);
        }
    }
    SelfCheck {
        start_failed: start.iter().filter(|r| !r.ok).count(),
        start,
        solution,
        outside,
        too_many: sc.solution.nodes.len() > sc.max_nodes(),
    }
}
