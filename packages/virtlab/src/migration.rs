//! Live migration model (chapter 10).
//!
//! Units: memory — MiB, time — seconds, downtime — milliseconds. A pre-copy round transfers the remainder; meanwhile the guest
//! dirties `dirty * time` MiB (at most all memory) — that is the next remainder. The migration converges when the remainder
//! fits into the allowed downtime.
//!
//! A scenario ([`Scenario`]) sets the guest dirtying rate, the network rate and the goal (condition [`MigrationGoal`]); the rest is chosen by
//! the student ([`MigrationInput`]). The scenario goal is checked against the run result.

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Guest memory, MiB (16 GiB).
pub const MEM_MIB: f64 = 16384.0;
/// Transfer of CPU and device state at stop, ms.
pub const STATE_MS: f64 = 20.0;
/// Pre-copy round limit.
pub const MAX_ROUNDS: u32 = 12;
/// Nominal channel gain from compression (zero pages and deltas).
pub const COMPRESS_FACTOR: f64 = 1.5;

/// Migration parameters (field format as in the former TypeScript client: `downtimeMs`, `autoConverge`, `postcopyAfter`).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct MigrationInput {
    /// Guest dirtying rate, MiB/s.
    pub dirty: f64,
    /// Network bandwidth, MiB/s.
    pub bw: f64,
    /// Allowed downtime, ms.
    pub downtime_ms: f64,
    /// Throttle vCPUs (start at 20%, +10% per round, at most 99%).
    #[serde(default)]
    pub auto_converge: bool,
    /// Page compression.
    #[serde(default)]
    pub compress: bool,
    /// `None` — pre-copy only, otherwise the number of pre-copy rounds before switching to post-copy.
    #[serde(default)]
    pub postcopy_after: Option<u32>,
    /// Guest memory, MiB (default [`MEM_MIB`]).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mem: Option<f64>,
}

/// How the migration ended.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    /// The remainder fit into the downtime: ordinary pre-copy.
    Precopy,
    /// Switched to post-copy.
    Postcopy,
    /// Ran out of rounds, stopped with a large remainder.
    Failed,
}

/// One pre-copy round.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Round {
    /// Round number (from 1).
    pub k: u32,
    /// Sent in this round, MiB.
    pub sent: f64,
    /// Round duration, s.
    pub secs: f64,
    /// vCPU throttling, %.
    pub throttle: f64,
    /// Remainder after the round, MiB.
    pub next: f64,
}

/// Simulation result.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Simulation {
    /// Outcome.
    pub outcome: Outcome,
    /// Pre-copy rounds.
    pub rounds: Vec<Round>,
    /// Remainder at the moment of stop/switch, MiB.
    pub remaining: f64,
    /// Downtime, ms (rounded).
    pub downtime: u64,
    /// Total migration time, s (rounded to tenths).
    pub total: f64,
    /// Nominal number of page faults during post-copy.
    pub faults: u64,
    /// Stop threshold: how many MiB can be sent within the allowed downtime.
    pub limit: f64,
}

/// Simulate the migration.
pub fn simulate(input: &MigrationInput) -> Simulation {
    let mem = input.mem.unwrap_or(MEM_MIB);
    let eff = input.bw * if input.compress { COMPRESS_FACTOR } else { 1.0 };
    let limit = (eff * input.downtime_ms) / 1000.0; // how many MiB can be sent within the allowed downtime
    let mut rounds: Vec<Round> = vec![];
    let mut remaining = mem;
    let mut elapsed = 0.0;
    let mut throttle = 0.0;
    let mut switched = false;

    for k in 1..=MAX_ROUNDS {
        if remaining <= limit {
            break;
        }
        if let Some(after) = input.postcopy_after {
            if k > after {
                switched = true;
                break;
            }
        }
        let secs = remaining / eff;
        if input.auto_converge && k >= 2 {
            throttle = f64::min(99.0, 20.0 + 10.0 * f64::from(k - 2));
        }
        let rate = input.dirty * (1.0 - throttle / 100.0);
        let next = f64::min(mem, rate * secs);
        rounds.push(Round { k, sent: remaining, secs, throttle, next });
        elapsed += secs;
        remaining = next;
    }

    let fit = remaining <= limit;
    let (outcome, downtime, total, faults);
    if fit {
        outcome = Outcome::Precopy;
        downtime = (remaining / eff) * 1000.0 + STATE_MS;
        total = elapsed + downtime / 1000.0;
        faults = 0.0;
    } else if switched {
        // the guest is already on the destination, pages are pulled on demand and in the background
        outcome = Outcome::Postcopy;
        downtime = STATE_MS;
        total = elapsed + remaining / eff;
        faults = (remaining / 64.0).round(); // nominally: one fault per 64 MiB of remainder
    } else {
        // round limit exhausted: the machine still has to be stopped with a large remainder
        outcome = Outcome::Failed;
        downtime = (remaining / eff) * 1000.0 + STATE_MS;
        total = elapsed + downtime / 1000.0;
        faults = 0.0;
    }
    Simulation {
        outcome,
        rounds,
        remaining,
        downtime: downtime.round() as u64,
        total: (total * 10.0).round() / 10.0,
        faults: faults as u64,
        limit,
    }
}

/// Condition for reaching the scenario goal by the simulation result (unspecified ones are not checked).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct MigrationGoal {
    /// Required outcome.
    pub outcome: Outcome,
    /// Downtime at most, ms.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_downtime: Option<u64>,
    /// Total time at most, s.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_total: Option<f64>,
}

impl MigrationGoal {
    /// Whether the goal is reached on result `r`.
    pub fn check(&self, r: &Simulation) -> bool {
        r.outcome == self.outcome
            && self.max_downtime.is_none_or(|d| r.downtime <= d)
            && self.max_total.is_none_or(|t| r.total <= t)
    }
}

/// Scenario: guest and network rates are given, the rest is chosen by the student.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (also the goal identifier).
    pub id: String,
    /// Tab title.
    pub title: String,
    /// Guest dirtying rate, MiB/s.
    pub dirty: f64,
    /// Network bandwidth, MiB/s.
    pub bw: f64,
    /// Goal text.
    pub goal: String,
    /// Scenario hint.
    pub hint: String,
    /// Goal condition.
    pub check: MigrationGoal,
}

impl Scenario {
    /// Exercise goal for this scenario.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Run parameters: scenario rates and the student's settings.
    pub fn input(
        &self,
        downtime_ms: f64,
        auto_converge: bool,
        compress: bool,
        postcopy_after: Option<u32>,
    ) -> MigrationInput {
        MigrationInput {
            dirty: self.dirty,
            bw: self.bw,
            downtime_ms,
            auto_converge,
            compress,
            postcopy_after,
            mem: None,
        }
    }

    /// Whether the scenario goal is reached by a run with settings `input` (rates are taken from the scenario, not from `input`).
    pub fn reached(&self, input: &MigrationInput) -> bool {
        let p = MigrationInput { dirty: self.dirty, bw: self.bw, ..input.clone() };
        self.check.check(&simulate(&p))
    }
}

/// Default scenarios (chapter 10 exercise).
pub fn default_scenarios() -> Vec<Scenario> {
    vec![
        Scenario {
            id: "calm".into(),
            title: i18n::tr("A calm guest").into(),
            dirty: 300.0,
            bw: 1250.0,
            goal: i18n::tr("Pre-copy converged, downtime at most 100 ms").into(),
            hint: i18n::tr("The allowed downtime is the stop threshold: the smaller it is, the more rounds, but the shorter the pause.")
                .into(),
            check: MigrationGoal { outcome: Outcome::Precopy, max_downtime: Some(100), max_total: None },
        },
        Scenario {
            id: "busy".into(),
            title: i18n::tr("An active guest").into(),
            dirty: 2000.0,
            bw: 1250.0,
            goal: i18n::tr("No post-copy: migration converged, downtime at most 600 ms").into(),
            hint: i18n::tr("The guest writes faster than the network can carry — the remainder does not shrink. You need to throttle the vCPU.").into(),
            check: MigrationGoal { outcome: Outcome::Precopy, max_downtime: Some(600), max_total: None },
        },
        Scenario {
            id: "wild".into(),
            title: i18n::tr("A very active guest").into(),
            dirty: 6000.0,
            bw: 1250.0,
            goal: i18n::tr("Hybrid: downtime at most 100 ms, total time at most 60 s").into(),
            hint: i18n::tr("Switch to post-copy earlier: each pre-copy round here costs about 13 seconds.").into(),
            check: MigrationGoal { outcome: Outcome::Postcopy, max_downtime: Some(100), max_total: Some(60.0) },
        },
    ]
}
