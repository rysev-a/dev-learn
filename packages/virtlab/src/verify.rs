//! Server-side check of a simulator exercise solution.
//!
//! On solving, the client sends JSON `{goal id: data, …}` — achieved goals with data (the former
//! TypeScript client does the same: `onSolved(JSON.stringify(...))`). What the "data" holds and how far it can be re-checked:
//!
//! | simulator | goal data | server check |
//! |---|---|---|
//! | `hv` | `{translate, mistakes}` (+ optional `trace` — recorded actions, [`crate::hv::Step`]) | with `trace` — full replay of the run ([`GoalStatus::Verified`]); without — only shape and sanity: a program with POPF is impossible without translation ([`GoalStatus::Unverified`]) |
//! | `ept` | run settings `{mode, guest, host, workload}` | the model is re-run, the goal is checked against the result — **full re-check** |
//! | `numa` | placement `{machine: {cpu, mem, vnuma}}` | the placement is re-evaluated — **full re-check** |
//! | `migration` | parameters `{dirty, bw, downtimeMs, autoConverge, compress, postcopyAfter}` | rates are checked against the scenario, parameters against allowed bounds, the simulation is re-run — **full re-check** |
//! | `ovirt_dc` | `{trace: [actions]}` | session replay; without a trace — [`GoalStatus::Unverified`] |
//! | `ovirt_fence` | settings `{soft, power, skip_lease, skip_connectivity, threshold, vm_leases}` | the simulation is re-run — **full re-check** |
//! | `ovirt_sched` | policy `{memory, network, affinity, even, free_mem, pack}` | the scheduling is re-run — **full re-check** |
//! | `ovirt_topo` | the whole board `{nodes, edges}` | the rules of the board are checked, the statuses are derived again and the scenario goals checked — **full re-check** |
//! | `lvm_board` | the whole board `{nodes, edges}` | the same, with the write load of the scenario — **full re-check** |
//! | `net_board` | the whole board `{nodes, edges}` | the rules of the board are checked, the links and segments derived again and the pings of the scenario made — **full re-check** |
//! | `virtq`, `qcow2` | `true` (former client) or `{trace: [actions]}` | with `trace` — session replay; without — goal achievement cannot be checked (history is not sent): [`GoalStatus::Unverified`] |
//!
//! Mode [`Strictness::Lenient`] also accepts unverifiable goals (a correct structure with all goals), mode
//! [`Strictness::Strict`] accepts only verified ones: the old client fails it, the new one (sending `trace`) passes.

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::error::SpecError;
use crate::spec::{base_map, Spec};
use crate::{ept, hv, lvm_board, migration, net_board, numa, ovirt_dc, ovirt_fence, ovirt_sched, ovirt_topo, qcow2, virtq};

/// Maximum action trace length: longer traces are rejected (protects the server from overload).
pub const MAX_TRACE: usize = 2000;

/// How strictly to accept a solution.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Strictness {
    /// Also accept goals that cannot be re-checked (a correct structure is enough).
    Lenient,
    /// Accept only goals whose achievement is confirmed by the model.
    Strict,
}

/// Status of one goal in the submitted solution.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "status", rename_all = "snake_case")]
pub enum GoalStatus {
    /// Goal achievement confirmed by recomputation from the submitted data.
    Verified,
    /// Structure is correct, but there is no way to check goal achievement from the submitted data.
    Unverified,
    /// The goal is absent from the solution.
    Missing,
    /// Data is invalid or the goal is not reached with it.
    Rejected {
        /// Reason.
        reason: String,
    },
}

/// Verdict for one goal.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GoalVerdict {
    /// Goal identifier.
    pub id: String,
    /// Status.
    #[serde(flatten)]
    pub status: GoalStatus,
}

/// Verdict for the solution.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Verdict {
    /// The exercise is solved (taking strictness into account).
    pub solved: bool,
    /// Per exercise goal, in goal order.
    pub goals: Vec<GoalVerdict>,
}

impl Verdict {
    /// Identifiers of goals with the given status.
    pub fn ids(&self, f: impl Fn(&GoalStatus) -> bool) -> Vec<&str> {
        self.goals.iter().filter(|g| f(&g.status)).map(|g| g.id.as_str()).collect()
    }

    /// First rejection reason, if any.
    pub fn first_rejection(&self) -> Option<String> {
        self.goals.iter().find_map(|g| match &g.status {
            GoalStatus::Rejected { reason } => Some(format!("{}: {reason}", g.id)),
            GoalStatus::Missing => Some(i18n::trf!("{0}: goal not reached", g.id)),
            _ => None,
        })
    }
}

/// Check a solution in [`Strictness::Lenient`] mode.
pub fn verify(spec: &Spec, submitted: &Value) -> Verdict {
    verify_with(spec, submitted, Strictness::Lenient)
}

/// Check a solution: for each exercise goal take the submitted data and re-check it with the model as far as possible.
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

// As in JavaScript: false, null, 0 and the empty string mean "no goal".
fn truthy(v: &Value) -> bool {
    match v {
        Value::Null | Value::Bool(false) => false,
        Value::Number(n) => n.as_f64().is_none_or(|x| x != 0.0),
        Value::String(s) => !s.is_empty(),
        _ => true,
    }
}

fn parse<T: serde::de::DeserializeOwned>(info: &Value) -> Result<T, SpecError> {
    serde_json::from_value(info.clone()).map_err(|e| SpecError::new(i18n::trf!("invalid data shape: {0}", e)))
}

fn rejected(reason: impl Into<String>) -> Result<GoalStatus, SpecError> {
    Ok(GoalStatus::Rejected { reason: reason.into() })
}

/// Goal data of simulators with an action trace: `true` (former client) or `{trace: [...]}`.
fn trace_of<A: serde::de::DeserializeOwned>(info: &Value) -> Result<Option<Vec<A>>, SpecError> {
    let Some(t) = info.get("trace") else {
        return Ok(None);
    };
    let v: Vec<A> = parse(t)?;
    if v.len() > MAX_TRACE {
        return Err(SpecError::new(i18n::trf!("action trace longer than {0}", MAX_TRACE)));
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
            let program = programs.iter().find(|p| p.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such program")))?;
            let i: Info = parse(info)?;
            match i.trace {
                Some(steps) => {
                    if steps.len() > MAX_TRACE {
                        return rejected(i18n::trf!("action trace longer than {0}", MAX_TRACE));
                    }
                    let fin = hv::replay(program, &hv::Run { translate: i.translate, steps })?;
                    if !fin.ok {
                        return rejected(i18n::tr("the run ended with an incorrect guest state"));
                    }
                    if fin.mistakes != i.mistakes {
                        return rejected(i18n::tr("the number of mistakes does not match the action trace"));
                    }
                    Ok(GoalStatus::Verified)
                }
                None => {
                    if hv::needs_translation(program)? && !i.translate {
                        return rejected(i18n::tr("the program contains POPF: without binary translation it cannot be completed correctly"));
                    }
                    Ok(GoalStatus::Unverified)
                }
            }
        }
        Spec::Ept { workloads, goals } => {
            let goal = goals.iter().find(|g| g.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such goal")))?;
            let cfg: ept::SimInput = parse(info)?;
            if cfg.workload != goal.workload {
                return rejected(i18n::tr("the run was made on a different workload"));
            }
            if ept::achieved(workloads, goals, &cfg)?.iter().any(|g| g == id) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the goal is not reached with these settings"))
            }
        }
        Spec::Virtq { size, goals } => match trace_of::<virtq::Action>(info)? {
            Some(actions) => {
                if virtq::replay(*size, goals, &actions).iter().any(|g| g == id) {
                    Ok(GoalStatus::Verified)
                } else {
                    rejected(i18n::tr("the goal is not reached according to the action trace"))
                }
            }
            None => Ok(GoalStatus::Unverified),
        },
        Spec::Qcow2 { base, goals, .. } => match trace_of::<qcow2::Action>(info)? {
            Some(actions) => {
                if qcow2::replay(&base_map(base), goals, &actions).iter().any(|g| g == id) {
                    Ok(GoalStatus::Verified)
                } else {
                    rejected(i18n::tr("the goal is not reached according to the action trace"))
                }
            }
            None => Ok(GoalStatus::Unverified),
        },
        Spec::Numa { nodes, scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let plan: numa::Plan = parse(info)?;
            match numa::accept(nodes, sc, &plan)? {
                numa::Accept::Ok { .. } => Ok(GoalStatus::Verified),
                numa::Accept::Over => rejected(i18n::tr("the placement does not fit into the nodes")),
                numa::Accept::TooRemote { .. } => rejected(i18n::tr("too many remote accesses")),
            }
        }
        Spec::Migration { scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let p: migration::MigrationInput = parse(info)?;
            if p.dirty != sc.dirty || p.bw != sc.bw {
                return rejected(i18n::tr("guest and network rates do not match the scenario"));
            }
            if !p.downtime_ms.is_finite() || !(20.0..=1000.0).contains(&p.downtime_ms) {
                return rejected(i18n::tr("the allowed downtime is outside the range of 20–1000 ms"));
            }
            if p.postcopy_after.is_some_and(|n| !(1..=6).contains(&n)) {
                return rejected(i18n::tr("switching to post-copy is possible after 1–6 rounds"));
            }
            if p.mem.is_some_and(|m| m != migration::MEM_MIB) {
                return rejected(i18n::tr("guest memory does not match the scenario"));
            }
            if sc.reached(&p) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goal is not reached with these parameters"))
            }
        }
        Spec::OvirtDc { goals } => match trace_of::<ovirt_dc::Action>(info)? {
            Some(actions) => {
                if ovirt_dc::replay(goals, &actions).iter().any(|g| g == id) {
                    Ok(GoalStatus::Verified)
                } else {
                    rejected(i18n::tr("the goal is not reached according to the action trace"))
                }
            }
            None => Ok(GoalStatus::Unverified),
        },
        Spec::OvirtFence { scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let cfg: ovirt_fence::FenceConfig = parse(info)?;
            if !ovirt_fence::valid(&cfg) {
                return rejected(i18n::tr("the threshold must be from 1 to 100 percent"));
            }
            if sc.reached(&cfg) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goal is not reached with these settings"))
            }
        }
        Spec::OvirtSched { scenarios } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let policy: ovirt_sched::Policy = parse(info)?;
            if !ovirt_sched::valid(&policy) {
                return rejected(i18n::trf!("weight factors must be from 0 to {0}", ovirt_sched::MAX_FACTOR));
            }
            if sc.reached(&policy) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goal is not reached with this policy"))
            }
        }
        Spec::OvirtTopo { scenarios, .. } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let board: ovirt_topo::Topology = parse(info)?;
            if let Some(reason) = sc.invalid(&board) {
                return rejected(reason);
            }
            if sc.reached(&board) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goals are not reached on this board"))
            }
        }
        Spec::LvmBoard { scenarios, .. } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let board: lvm_board::Topology = parse(info)?;
            if let Some(reason) = sc.invalid(&board) {
                return rejected(reason);
            }
            if sc.reached(&board) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goals are not reached on this board"))
            }
        }
        Spec::NetBoard { scenarios, .. } => {
            let sc = scenarios.iter().find(|s| s.id == id).ok_or_else(|| SpecError::new(i18n::tr("no such scenario")))?;
            let board: net_board::Topology = parse(info)?;
            if let Some(reason) = sc.invalid(&board) {
                return rejected(reason);
            }
            if sc.reached(&board) {
                Ok(GoalStatus::Verified)
            } else {
                rejected(i18n::tr("the scenario goals are not reached on this board"))
            }
        }
    }
}
