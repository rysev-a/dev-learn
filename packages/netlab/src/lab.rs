//! Exercise data of the "Computer Networks" book and server-side check of a submitted solution.
//!
//! The chapter data file is `labs/net/<book>-<chapter:02>.json` ([`LabChapter`]): each exercise has a statement, a hint and
//! `spec`: the initial network, goals, reference solution steps and allowed tools. `spec.solution` is not sent
//! to the client; the server checks the submitted network state with [`verify`].

use crate::check::{apply_ops, check_goals, Goal, GoalResult, Step};
use crate::types::*;
use serde::{Deserialize, Serialize};
use std::path::Path;

/// Number of the "Computer Networks" book.
pub const NET_BOOK: u32 = 15;

fn is_false(b: &bool) -> bool {
    !*b
}

/// Tools opened in the exercise (forms in the device card and the "Cable" panel).
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct Tools {
    #[serde(default, skip_serializing_if = "is_false")]
    pub cable: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub nat: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub fw: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub dns: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub http: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub tls: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub tcp: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub queue: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub proxy: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub lb: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub rproxy: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub ssh: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub vpn: bool,
}

impl Tools {
    /// Enable a tool by name; `false` means there is no such tool.
    pub fn set(&mut self, name: &str, on: bool) -> bool {
        let slot = match name {
            "cable" => &mut self.cable,
            "nat" => &mut self.nat,
            "fw" => &mut self.fw,
            "dns" => &mut self.dns,
            "http" => &mut self.http,
            "tls" => &mut self.tls,
            "tcp" => &mut self.tcp,
            "queue" => &mut self.queue,
            "proxy" => &mut self.proxy,
            "lb" => &mut self.lb,
            "rproxy" => &mut self.rproxy,
            "ssh" => &mut self.ssh,
            "vpn" => &mut self.vpn,
            _ => return false,
        };
        *slot = on;
        true
    }
}

/// Exercise contents: initial network, goals and reference solution.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct NetSpec {
    #[serde(default)]
    pub tools: Tools,
    pub start: NetState,
    pub goals: Vec<Goal>,
    /// Reference steps; the server does not send them to the client, so the field is optional.
    #[serde(default)]
    pub solution: Vec<Step>,
}

/// Chapter exercise.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub statement: String,
    pub hint: String,
    pub spec: NetSpec,
}

/// Chapter data file.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// Lab kind: "net".
    pub lab: String,
    pub tasks: Vec<Task>,
}

impl LabChapter {
    /// Parse a data file.
    pub fn from_json(s: &str) -> Result<LabChapter, String> {
        let c: LabChapter = serde_json::from_str(s).map_err(|e| i18n::trf!("chapter file: {0}", e))?;
        if c.lab != "net" {
            return Err(i18n::trf!("chapter file: expected the “net” lab, not “{0}”", c.lab));
        }
        Ok(c)
    }

    /// Read a data file from disk.
    pub fn load(path: &Path) -> Result<LabChapter, String> {
        let s = std::fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
        Self::from_json(&s).map_err(|e| format!("{}: {e}", path.display()))
    }

    /// Chapter file name: `15-03.json`.
    pub fn file_name(&self) -> String {
        format!("{}-{:02}.json", self.book, self.chapter)
    }

    /// Exercise by id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }
}

/// Read all chapters of a data directory (`*.json`), in chapter order.
pub fn load_dir(dir: &Path) -> Result<Vec<LabChapter>, String> {
    let mut files: Vec<_> = std::fs::read_dir(dir)
        .map_err(|e| format!("{}: {e}", dir.display()))?
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| p.extension().map(|x| x == "json").unwrap_or(false))
        .collect();
    files.sort();
    let mut out = Vec::new();
    for f in files {
        out.push(LabChapter::load(&f)?);
    }
    out.sort_by_key(|c| (c.book, c.chapter));
    Ok(out)
}

impl NetSpec {
    /// Initial network of the exercise (clean copy without caches).
    pub fn start_state(&self) -> NetState {
        self.start.stripped()
    }

    /// Network after the reference solution steps.
    pub fn solved_state(&self) -> Result<NetState, String> {
        let mut s = self.start_state();
        apply_ops(&mut s, &self.solution)?;
        Ok(s)
    }
}

/// Check outcome for one goal.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct GoalVerdict {
    pub id: String,
    pub text: String,
    pub ok: bool,
    pub detail: String,
}

/// Solution check outcome: whether all goals are met and what happened to each.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Verdict {
    pub ok: bool,
    /// The submitted solution is unusable at all (foreign devices, broken JSON): the reason text.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
    pub goals: Vec<GoalVerdict>,
}

impl Verdict {
    fn rejected(e: impl Into<String>) -> Verdict {
        Verdict { ok: false, error: Some(e.into()), goals: vec![] }
    }

    fn from_results(rs: Vec<GoalResult>) -> Verdict {
        let ok = !rs.is_empty() && rs.iter().all(|r| r.ok);
        Verdict {
            ok,
            error: None,
            goals: rs.into_iter().map(|r| GoalVerdict { id: r.id, text: r.text, ok: r.ok, detail: r.detail }).collect(),
        }
    }
}

fn default_cable(l: &Link) -> bool {
    l.km == 0.01 && l.mbps == 1000.0 && l.mtu.is_none() && l.loss.is_none()
}

/// The submitted state is the same exercise: same devices, locked devices untouched, cables change
/// only with the "Cable" tool open (and only as ordinary cables).
pub fn check_integrity(spec: &NetSpec, sub: &NetState) -> Result<(), String> {
    sub.validate()?;
    let start = &spec.start;
    if sub.devices.len() != start.devices.len() {
        return Err(i18n::tr("the set of devices does not match the exercise").into());
    }
    for d0 in start.devices.iter() {
        let Some(d) = sub.devices.get(&d0.id) else { return Err(i18n::trf!("no device “{0}”", d0.id)) };
        if d.kind != d0.kind || d.name != d0.name {
            return Err(i18n::trf!("device “{0}” was tampered with", d0.id));
        }
        if d0.locked {
            let mut same = d.clone();
            same.x = d0.x;
            same.y = d0.y;
            // the host's knowledge of SSH keys is client state, not configuration
            same.known_hosts = d0.known_hosts.clone();
            if same != *d0 {
                return Err(i18n::trf!("device “{0}” is locked for configuration, but it was changed", d0.name));
            }
        }
    }
    if sub.pki != start.pki {
        return Err(i18n::tr("the key infrastructure was changed").into());
    }
    let same_links = sub.links.len() == start.links.len() && start.links.iter().all(|l| sub.links.contains(l));
    if !same_links {
        if !spec.tools.cable {
            return Err(i18n::tr("cables cannot be changed in this exercise").into());
        }
        for l in &sub.links {
            if !start.links.contains(l) && !default_cable(l) {
                return Err(i18n::tr("a cable with unusual properties").into());
            }
        }
    }
    Ok(())
}

/// Check a submitted solution: integrity and goals on a clean copy of the network.
pub fn verify(spec: &NetSpec, submitted: &NetState) -> Verdict {
    if let Err(e) = check_integrity(spec, submitted) {
        return Verdict::rejected(e);
    }
    Verdict::from_results(check_goals(submitted, &spec.goals))
}

/// Same for a JSON string (what the client sends to `PUT /api/exercises/15/<chapter>/<id>/solved`).
pub fn verify_json(spec: &NetSpec, solution: &str) -> Verdict {
    match crate::model::state_from_json(solution) {
        Ok(s) => verify(spec, &s),
        Err(e) => Verdict::rejected(e),
    }
}
