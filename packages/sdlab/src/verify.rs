//! Server-side solution verification: the design submitted by the student really meets the exercise goals and does not violate
//! its constraints (palette, node count, allowed links and parameter values). Previously the client was trusted.

use std::collections::HashSet;

use serde::Serialize;
use serde_json::Value;

use crate::checks::{all_ok, check_goals};
use crate::engine::{can_link, evaluate};
use crate::error::SdError;
use crate::kinds::{param_spec, ParamType};
use crate::ports::reaches;
use crate::types::{EvalOptions, Goal, GoalResult, Kind, ParamValue, Scenario, SdState, Task};

/// Size limit of a submitted solution, bytes.
pub const MAX_SOLUTION_BYTES: usize = 1 << 20;

/// Exercise constraint violation.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Problem {
    /// the design has no "Users" component
    NoClients,
    /// more than one "Users"
    ManyClients { count: usize },
    /// the design has no components at all
    Empty,
    DuplicateNode { id: String },
    /// more components than the exercise allows
    TooManyNodes { count: usize, max: usize },
    /// a link leads to a nonexistent component
    UnknownEdgeEnd { from: String, to: String },
    /// such components are not connected in the model
    BadLink { from: String, to: String },
    DuplicateEdge { from: String, to: String },
    /// the link closes a cycle
    Cycle { from: String, to: String },
    /// component outside the exercise palette
    OutsidePalette { node: String, kind: Kind },
    /// parameter value is invalid (unknown key, not from the list, out of range)
    BadParam { node: String, key: String, reason: String },
    /// the parameter is hidden in this exercise and cannot be changed
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

/// Solution verification outcome.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Verdict {
    /// the solution is accepted: no violations and all goals met
    pub ok: bool,
    /// result per goal, in the exercise's goal order (empty if the design was not evaluated)
    pub goals: Vec<GoalResult>,
    /// exercise constraint violations
    pub problems: Vec<Problem>,
}

impl Verdict {
    /// Message for the client response: the first violation or the first unmet goal.
    pub fn reason(&self) -> Option<String> {
        if let Some(p) = self.problems.first() {
            return Some(p.to_string());
        }
        self.goals.iter().find(|g| !g.ok).map(|g| i18n::trf!("goal not met: {0} ({1})", g.text, g.detail))
    }
}

/// Parses a solution submitted by the client: a JSON string of the design state (as the draft stores it) or an already parsed
/// object; tolerant of `{"state": …}` / `{"solution": …}` wrappers, double serialization, missing names and coordinates.
pub fn parse_solution(raw: &str) -> Result<SdState, SdError> {
    if raw.len() > MAX_SOLUTION_BYTES {
        return Err(SdError::new(i18n::tr("the solution is too large")));
    }
    state_from_value(serde_json::from_str(raw)?)
}

/// The same for already parsed JSON.
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

/// Exercise constraint violations (without evaluation).
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
    // links: in order, as the UI places them (no duplicates or cycles)
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
    // palette: users, monitoring and everything on the starting design are always available
    for n in &s.nodes {
        let free = matches!(n.kind, Kind::Clients | Kind::Monitor) || sc.palette.contains(&n.kind) || sc.start.nodes.iter().any(|x| x.kind == n.kind);
        if !free {
            out.push(Problem::OutsidePalette { node: n.id.clone(), kind: n.kind });
        }
    }
    // parameters: only known ones with valid values; those hidden in this exercise — as on the starting design
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

/// Whether any exercise goal refers to the parameter.
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

/// Verifies an exercise solution: constraint violations and goals. The design is evaluated only if the node count is within the
/// exercise limit (otherwise evaluation is pointless, and the cost of a mistake is server time).
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

/// Verifies a solution submitted as a string (`PUT …/solved`, the `solution` field).
pub fn verify_raw(sc: &Scenario, raw: &str) -> Result<Verdict, SdError> {
    Ok(verify(sc, &parse_solution(raw)?))
}

/// Exercise self-check (port of `sd-selfcheck`): the starting design does not solve it, the reference does, everything within constraints.
#[derive(Debug, Clone, PartialEq)]
pub struct SelfCheck {
    /// how many goals are unmet in the starting design
    pub start_failed: usize,
    /// goals of the starting design
    pub start: Vec<GoalResult>,
    /// goals of the reference solution
    pub solution: Vec<GoalResult>,
    /// reference components outside the palette (and not on the starting design)
    pub outside: Vec<Kind>,
    /// the reference has more nodes than allowed
    pub too_many: bool,
}

impl SelfCheck {
    /// All good: the starting design fails, the reference passes, constraints are met.
    pub fn is_ok(&self) -> bool {
        self.start_failed > 0 && all_ok(&self.solution) && self.outside.is_empty() && !self.too_many
    }
}

/// Self-check of one exercise.
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
