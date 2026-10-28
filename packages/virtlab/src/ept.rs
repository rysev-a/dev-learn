//! Guest address translation model (chapter 4, "Guest memory").
//!
//! Cost is measured in memory accesses. Shadow page tables: a TLB miss costs one table walk (as many levels as
//! the smallest page has), but every mapping change is an exit ([`EXIT_COST`]). Nested EPT/NPT: a miss
//! costs `(g+1)*(h+1)-1` accesses, and the hypervisor does not see guest changes. A TLB entry describes a page of the smaller of the two
//! sizes: a large guest page on a small host page gets "split".
//!
//! Workloads and goals are data ([`Workload`], [`EptGoal`]); a goal is bound to a workload and checked against the run result
//! and settings.

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Page size.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PageSize {
    /// 4 KiB.
    #[serde(rename = "4K")]
    K4,
    /// 2 MiB.
    #[serde(rename = "2M")]
    M2,
    /// 1 GiB.
    #[serde(rename = "1G")]
    G1,
}

impl PageSize {
    /// All sizes from smallest to largest.
    pub const ALL: [PageSize; 3] = [PageSize::K4, PageSize::M2, PageSize::G1];

    /// Page size in bytes.
    pub fn bytes(self) -> u64 {
        match self {
            PageSize::K4 => 4096,
            PageSize::M2 => 2 * 1024 * 1024,
            PageSize::G1 => 1024 * 1024 * 1024,
        }
    }

    /// Number of table levels walked to reach a page of this size.
    pub fn levels(self) -> u32 {
        match self {
            PageSize::K4 => 4,
            PageSize::M2 => 3,
            PageSize::G1 => 2,
        }
    }
}

/// Translation mode.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Mode {
    /// Shadow page tables.
    Shadow,
    /// Nested EPT/NPT tables.
    Ept,
}

/// Number of TLB entries.
pub const TLB_ENTRIES: usize = 64;
/// Cost of an exit to the hypervisor (in memory accesses).
pub const EXIT_COST: u64 = 1000;

fn smaller(a: PageSize, b: PageSize) -> PageSize {
    if a.bytes() <= b.bytes() {
        a
    } else {
        b
    }
}

/// Cost of one TLB miss in memory accesses (table walk; excluding the data access itself).
pub fn walk_cost(mode: Mode, guest: PageSize, host: PageSize) -> u32 {
    match mode {
        Mode::Shadow => smaller(guest, host).levels(),
        Mode::Ept => (guest.levels() + 1) * (host.levels() + 1) - 1,
    }
}

const MIB: u64 = 1024 * 1024;

/// Linear congruential generator (same as in TypeScript: `Math.imul(x, 1664525) + 1013904223 >>> 0`).
fn lcg(seed: u32) -> impl FnMut() -> u32 {
    let mut x = seed;
    move || {
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        x
    }
}

fn random_addrs(n: usize, span: u64, seed: u32) -> Vec<u64> {
    let mut r = lcg(seed);
    (0..n).map(|_| (u64::from(r()) % (span / 8)) * 8).collect()
}

/// How the workload's access addresses are built.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Access {
    /// One access at an address.
    Single {
        /// Address.
        addr: u64,
    },
    /// `count` consecutive accesses with a `step`-byte stride.
    Stride {
        /// Number of accesses.
        count: usize,
        /// Stride in bytes.
        step: u64,
    },
    /// `count` random accesses (8 bytes each) within `span_mib` MiB; generator seeded with `seed`.
    Random {
        /// Number of accesses.
        count: usize,
        /// Address span, MiB.
        span_mib: u64,
        /// Generator seed.
        seed: u32,
    },
}

/// Workload: guest memory accesses and the number of mapping changes by the guest.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Workload {
    /// Identifier.
    pub id: String,
    /// Title.
    pub title: String,
    /// Note under the workload selector.
    pub note: String,
    /// Access addresses.
    pub access: Access,
    /// How many times the guest changes the mapping (in shadow mode each one is an exit).
    pub maps: u64,
}

/// Expanded workload.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Trace {
    /// Access addresses in order.
    pub addrs: Vec<u64>,
    /// Number of mapping changes.
    pub maps: u64,
}

impl Workload {
    /// Expand the workload into a list of addresses.
    pub fn make(&self) -> Trace {
        let addrs = match self.access {
            Access::Single { addr } => vec![addr],
            Access::Stride { count, step } => (0..count as u64).map(|i| i * step).collect(),
            Access::Random { count, span_mib, seed } => random_addrs(count, span_mib * MIB, seed),
        };
        Trace { addrs, maps: self.maps }
    }
}

/// Run settings.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimInput {
    /// Translation mode.
    pub mode: Mode,
    /// Guest page size.
    pub guest: PageSize,
    /// Host page size.
    pub host: PageSize,
    /// Workload identifier.
    pub workload: String,
}

/// Result of running a workload.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimRun {
    /// Cost of one miss.
    pub walk: u32,
    /// Number of guest accesses.
    pub accesses: u64,
    /// TLB misses.
    pub misses: u64,
    /// TLB hits.
    pub hits: u64,
    /// Exits to the hypervisor due to table edits.
    pub exits: u64,
    /// Total memory accesses.
    pub cost: u64,
    /// Size of the page described by a TLB entry.
    pub eff_page: PageSize,
}

/// Run workload `w` with settings `mode`, `guest`, `host`.
pub fn simulate_workload(w: &Workload, mode: Mode, guest: PageSize, host: PageSize) -> SimRun {
    let trace = w.make();
    let eff = smaller(guest, host).bytes();
    let walk = walk_cost(mode, guest, host);
    let mut tlb: Vec<u64> = Vec::with_capacity(TLB_ENTRIES + 1);
    let mut misses = 0u64;
    let mut cost = 0u64;
    for &a in &trace.addrs {
        let p = a / eff;
        if let Some(i) = tlb.iter().position(|&x| x == p) {
            tlb.remove(i);
            cost += 1;
        } else {
            misses += 1;
            cost += u64::from(walk) + 1;
            if tlb.len() >= TLB_ENTRIES {
                tlb.remove(0);
            }
        }
        tlb.push(p);
    }
    let exits = if mode == Mode::Shadow { trace.maps } else { 0 };
    cost += exits * EXIT_COST;
    let accesses = trace.addrs.len() as u64;
    SimRun { walk, accesses, misses, hits: accesses - misses, exits, cost, eff_page: smaller(guest, host) }
}

/// Run a workload from the list by identifier.
pub fn simulate(workloads: &[Workload], input: &SimInput) -> Result<SimRun, SpecError> {
    let w = workloads
        .iter()
        .find(|w| w.id == input.workload)
        .ok_or_else(|| SpecError::new(i18n::trf!("no workload “{0}”", input.workload)))?;
    Ok(simulate_workload(w, input.mode, input.guest, input.host))
}

/// Goal: on its workload all specified conditions hold (unspecified ones are not checked).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct EptGoal {
    /// Goal identifier.
    pub id: String,
    /// Goal text.
    pub text: String,
    /// Workload the goal is checked on.
    pub workload: String,
    /// Required mode.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mode: Option<Mode>,
    /// Required guest page size.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub guest: Option<PageSize>,
    /// Required host page size.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub host: Option<PageSize>,
    /// Miss cost at most.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_walk: Option<u32>,
    /// Total cost at most.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max_cost: Option<u64>,
}

impl EptGoal {
    /// Whether the goal is reached by run `r` with settings `cfg` (the workload is not checked — see [`achieved`]).
    pub fn check(&self, r: &SimRun, cfg: &SimInput) -> bool {
        self.mode.is_none_or(|m| m == cfg.mode)
            && self.guest.is_none_or(|g| g == cfg.guest)
            && self.host.is_none_or(|h| h == cfg.host)
            && self.max_walk.is_none_or(|w| r.walk <= w)
            && self.max_cost.is_none_or(|c| r.cost <= c)
    }

    /// Goal for display.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Goals reached by running `input` (what the "Run workload" button does).
pub fn achieved(workloads: &[Workload], goals: &[EptGoal], input: &SimInput) -> Result<Vec<String>, SpecError> {
    let r = simulate(workloads, input)?;
    Ok(goals.iter().filter(|g| g.workload == input.workload && g.check(&r, input)).map(|g| g.id.clone()).collect())
}

/// Default workloads (chapter 4 exercise).
pub fn default_workloads() -> Vec<Workload> {
    let w = |id: &str, title: &str, note: &str, access: Access, maps: u64| Workload {
        id: id.into(),
        title: title.into(),
        note: note.into(),
        access,
        maps,
    };
    vec![
        w("one", i18n::tr("A single TLB miss"), i18n::tr("one memory access: look at the cost of the walk"), Access::Single { addr: 0 }, 0),
        w(
            "scan",
            i18n::tr("Scanning 8 MiB"),
            i18n::tr("2048 consecutive accesses with a 4 KiB stride"),
            Access::Stride { count: 2048, step: 4096 },
            0,
        ),
        w(
            "random",
            i18n::tr("Random accesses over 64 MiB"),
            i18n::tr("4000 random accesses; TLB of 64 entries"),
            Access::Random { count: 4000, span_mib: 64, seed: 7 },
            0,
        ),
        w(
            "fork",
            i18n::tr("Frequent page table changes"),
            i18n::tr("500 mapping changes by the guest and 2000 random accesses over 1 GiB"),
            Access::Random { count: 2000, span_mib: 1024, seed: 11 },
            500,
        ),
    ]
}

/// Default goals (chapter 4 exercise).
pub fn default_goals() -> Vec<EptGoal> {
    let g = |id: &str, text: &str, workload: &str| EptGoal {
        id: id.into(),
        text: text.into(),
        workload: workload.into(),
        mode: None,
        guest: None,
        host: None,
        max_walk: None,
        max_cost: None,
    };
    vec![
        EptGoal {
            mode: Some(Mode::Ept),
            max_walk: Some(15),
            ..g("walk", i18n::tr("A single miss costs at most 15 accesses (nested tables)"), "one")
        },
        EptGoal {
            mode: Some(Mode::Shadow),
            guest: Some(PageSize::K4),
            host: Some(PageSize::K4),
            max_cost: Some(15000),
            ..g("scan", i18n::tr("Scanning 8 MiB with 4 KiB pages is cheaper than with EPT: at most 15,000"), "scan")
        },
        EptGoal {
            max_cost: Some(10000),
            ..g("random", i18n::tr("Random accesses over 64 MiB fit within 10,000 accesses"), "random")
        },
        EptGoal {
            max_cost: Some(35000), ..g("fork", i18n::tr("Frequent page table changes: at most 35,000 accesses"), "fork")
        },
    ]
}
