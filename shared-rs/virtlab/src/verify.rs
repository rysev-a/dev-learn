//! Серверная проверка решения упражнения-симулятора.
//!
//! Клиент при решении присылает JSON `{идентификатор цели: данные, …}` — достигнутые цели с данными (так делает и прежний
//! TypeScript-клиент: `onSolved(JSON.stringify(...))`). Что лежит в «данных» и насколько их можно перепроверить:
//!
//! | симулятор | данные цели | проверка на сервере |
//! |---|---|---|
//! | `hv` | `{translate, mistakes}` (+ необязательно `trace` — записанные действия, [`crate::hv::Step`]) | с `trace` — полное воспроизведение прогона ([`GoalStatus::Verified`]); без — только форма и здравый смысл: программа с POPF невозможна без трансляции ([`GoalStatus::Unverified`]) |
//! | `ept` | настройки запуска `{mode, guest, host, workload}` | модель запускается заново, цель проверяется по результату — **полная перепроверка** |
//! | `numa` | размещение `{машина: {cpu, mem, vnuma}}` | оценка размещения заново — **полная перепроверка** |
//! | `migration` | параметры `{dirty, bw, downtimeMs, autoConverge, compress, postcopyAfter}` | скорости сверяются со сценарием, параметры — с допустимыми границами, симуляция заново — **полная перепроверка** |
//! | `virtq`, `qcow2` | `true` (прежний клиент) или `{trace: [действия]}` | с `trace` — воспроизведение сессии; без — достижение цели не проверить (история не присылается): [`GoalStatus::Unverified`] |
//!
//! Режим [`Strictness::Lenient`] принимает и непроверяемые цели (корректная структура со всеми целями), режим
//! [`Strictness::Strict`] — только проверенные: старый клиент в нём не пройдёт, новый (присылающий `trace`) пройдёт.

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::error::SpecError;
use crate::spec::{base_map, Spec};
use crate::{ept, hv, migration, numa, qcow2, virtq};

/// Наибольшая длина записи действий: больше — отклоняется (защита от перегрузки сервера).
pub const MAX_TRACE: usize = 2000;

/// Насколько строго принимать решение.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Strictness {
    /// Принимать и цели, которые перепроверить нечем (достаточно корректной структуры).
    Lenient,
    /// Принимать только цели, достижение которых подтверждено моделью.
    Strict,
}

/// Состояние одной цели в присланном решении.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "status", rename_all = "snake_case")]
pub enum GoalStatus {
    /// Достижение цели подтверждено повторным расчётом по присланным данным.
    Verified,
    /// Структура верна, но достижение цели по присланным данным проверить нечем.
    Unverified,
    /// Цели в решении нет.
    Missing,
    /// Данные неверны или цель по ним не достигается.
    Rejected {
        /// Причина.
        reason: String,
    },
}

/// Вердикт по одной цели.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GoalVerdict {
    /// Идентификатор цели.
    pub id: String,
    /// Состояние.
    #[serde(flatten)]
    pub status: GoalStatus,
}

/// Вердикт по решению.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Verdict {
    /// Упражнение решено (с учётом строгости).
    pub solved: bool,
    /// По каждой цели упражнения, в порядке целей.
    pub goals: Vec<GoalVerdict>,
}

impl Verdict {
    /// Идентификаторы целей с данным состоянием.
    pub fn ids(&self, f: impl Fn(&GoalStatus) -> bool) -> Vec<&str> {
        self.goals.iter().filter(|g| f(&g.status)).map(|g| g.id.as_str()).collect()
    }

    /// Первая причина отказа, если есть.
    pub fn first_rejection(&self) -> Option<String> {
        self.goals.iter().find_map(|g| match &g.status {
            GoalStatus::Rejected { reason } => Some(format!("{}: {reason}", g.id)),
            GoalStatus::Missing => Some(format!("{}: цель не достигнута", g.id)),
            _ => None,
        })
    }
}

/// Проверить решение в режиме [`Strictness::Lenient`].
pub fn verify(spec: &Spec, submitted: &Value) -> Verdict {
    verify_with(spec, submitted, Strictness::Lenient)
}

/// Проверить решение: для каждой цели упражнения взять присланные данные и перепроверить моделью, насколько это возможно.
pub fn verify_with(spec: &Spec, submitted: &Value, strict: Strictness) -> Verdict {
    let mut goals = vec![];
    for g in spec.goals() {
        let info = submitted.get(&g.id).filter(|v| truthy(v));
        let status = match info {
            None => GoalStatus::Missing,
            Some(info) => check_goal(spec, &g.id, info).unwrap_or_else(|e| GoalStatus::Rejected { reason: e.0 }),
        };
        goals.push(GoalVerdict { id: g.id, status });
    }
    let solved = goals.iter().all(|g| match g.status {
        GoalStatus::Verified => true,
        GoalStatus::Unverified => strict == Strictness::Lenient,
        _ => false,
    });
    Verdict { solved, goals }
}

// Как в JavaScript: false, null, 0 и пустая строка — «цели нет».
fn truthy(v: &Value) -> bool {
    match v {
        Value::Null | Value::Bool(false) => false,
        Value::Number(n) => n.as_f64().is_none_or(|x| x != 0.0),
        Value::String(s) => !s.is_empty(),
        _ => true,
    }
}

fn parse<T: serde::de::DeserializeOwned>(info: &Value) -> Result<T, SpecError> {
    serde_json::from_value(info.clone()).map_err(|e| SpecError::new(format!("неверная форма данных: {e}")))
}

fn rejected(reason: impl Into<String>) -> Result<GoalStatus, SpecError> {
    Ok(GoalStatus::Rejected { reason: reason.into() })
}

/// Данные цели симуляторов с записью действий: `true` (прежний клиент) или `{trace: [...]}`.
fn trace_of<A: serde::de::DeserializeOwned>(info: &Value) -> Result<Option<Vec<A>>, SpecError> {
    let Some(t) = info.get("trace") else {
        return Ok(None);
    };
    let v: Vec<A> = parse(t)?;
    if v.len() > MAX_TRACE {
        return Err(SpecError::new(format!("запись действий длиннее {MAX_TRACE}")));
    }
    Ok(Some(v))
}

fn check_goal(spec: &Spec, id: &str, info: &Value) -> Result<GoalStatus, SpecError> {
    match spec {
        Spec::Hv { programs } => {
            #[derive(Deserialize)]
            struct Info {
                translate: bool,
                mistakes: u32,
                #[serde(default)]
                trace: Option<Vec<hv::Step>>,
            }
            let program = programs.iter().find(|p| p.id == id).ok_or_else(|| SpecError::new("нет такой программы"))?;
            let i: Info = parse(info)?;
            match i.trace {
                Some(steps) => {
                    if steps.len() > MAX_TRACE {
                        return rejected(format!("запись действий длиннее {MAX_TRACE}"));
                    }
                    let fin = hv::replay(program, &hv::Run { translate: i.translate, steps })?;
                    if !fin.ok {
                        return rejected("прогон закончился неверным состоянием гостя");
                    }
                    if fin.mistakes != i.mistakes {
                        return rejected("число ошибок не совпадает с записью действий");
                    }
                    Ok(GoalStatus::Verified)
                }
                None => {
                    if hv::needs_translation(program)? && !i.translate {
                        return rejected("в программе есть POPF: без двоичной трансляции она не проходится верно");
                    }
                    Ok(GoalStatus::Unverified)
                }
            }
        }
        Spec::Ept { workloads, goals } => {
            let goal = goals.iter().find(|g| g.id == id).ok_or_else(|| SpecError::new("нет такой цели"))?;
            let cfg: ept::SimInput = parse(info)?;
            if cfg.workload != goal.workload {
                return rejected("запуск выполнен на другой нагрузке");
            }
            if ept::achieved(workloads, goals, &cfg)?.iter().any(|g| g == id) {
                Ok(GoalStatus::Verified)
            } else {
                rejected("при этих настройках цель не достигается")
            }
        }
        Spec::Virtq { size, goals } => match trace_of::<virtq::Action>(info)? {
            Some(actions) => {
                if virtq::replay(*size, goals, &actions).iter().any(|g| g == id) {
                    Ok(GoalStatus::Verified)
                } else {
                    rejected("по записи действий цель не достигается")
                }
            }
            None => Ok(GoalStatus::Unverified),
        },
        Spec::Qcow2 { base, goals, .. } => match trace_of::<qcow2::Action>(info)? {
            Some(actions) => {
                if qcow2::replay(&base_map(base), goals, &actions).iter().any(|g| g == id) {
                    Ok(GoalStatus::Verified)
                } else {
                    rejected("по записи действий цель не достигается")
                }
            }
            None => Ok(GoalStatus::Unverified),
        },
        Spec::Numa { nodes, scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new("нет такого сценария"))?;
            let plan: numa::Plan = parse(info)?;
            match numa::accept(nodes, sc, &plan)? {
                numa::Accept::Ok { .. } => Ok(GoalStatus::Verified),
                numa::Accept::Over => rejected("размещение не помещается в узлы"),
                numa::Accept::TooRemote { .. } => rejected("слишком много удалённых обращений"),
            }
        }
        Spec::Migration { scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new("нет такого сценария"))?;
            let p: migration::MigrationInput = parse(info)?;
            if p.dirty != sc.dirty || p.bw != sc.bw {
                return rejected("скорости гостя и сети не совпадают со сценарием");
            }
            if !p.downtime_ms.is_finite() || !(20.0..=1000.0).contains(&p.downtime_ms) {
                return rejected("допустимый простой вне диапазона 20–1000 мс");
            }
            if p.postcopy_after.is_some_and(|n| !(1..=6).contains(&n)) {
                return rejected("переход на post-copy возможен после 1–6 кругов");
            }
            if p.mem.is_some_and(|m| m != migration::MEM_MIB) {
                return rejected("память гостя не совпадает со сценарием");
            }
            if sc.reached(&p) {
                Ok(GoalStatus::Verified)
            } else {
                rejected("при этих параметрах цель сценария не достигается")
            }
        }
    }
}
