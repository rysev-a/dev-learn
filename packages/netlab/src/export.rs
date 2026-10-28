//! Migration of exercises from the former TypeScript code: parsing the dump of `frontend/scripts/net-export.mjs`
//! (`scenarios.json`) and turning it into chapter files ([`LabChapter`]). Also the "nothing is lost" check:
//! state and goals after parsing match the original JSON (up to key renaming).

use crate::check::{Goal, Step};
use crate::lab::{LabChapter, NetSpec, Task, Tools, NET_BOOK};
use crate::model::LinkExtra;
use crate::types::NetState;
use serde::Deserialize;
use serde_json::value::RawValue;
use serde_json::Value;
use std::collections::BTreeMap;

/// Solution step in TypeScript form: `{unlink:[a,b]}`, `{drop:id}`, `{cable:[a,b]}`, `{cmd:[device, string]}`.
#[derive(Clone, Debug, Deserialize)]
#[serde(untagged)]
pub enum TsOp {
    Unlink {
        unlink: [String; 2],
    },
    Drop {
        drop: String,
    },
    Cable {
        cable: [String; 2],
        #[serde(default)]
        extra: Option<LinkExtra>,
    },
    Cmd {
        cmd: [String; 2],
    },
}

impl From<TsOp> for Step {
    fn from(o: TsOp) -> Step {
        match o {
            TsOp::Unlink { unlink: [a, b] } => Step::Unlink { a, b },
            TsOp::Drop { drop } => Step::Drop { dev: drop },
            TsOp::Cable { cable: [a, b], extra } => Step::Cable { a, b, extra },
            TsOp::Cmd { cmd: [dev, line] } => Step::Cmd { dev, line },
        }
    }
}

/// Exercise in dump form.
#[derive(Clone, Debug, Deserialize)]
pub struct TsScenario {
    pub chapter: u32,
    pub id: String,
    pub title: String,
    pub statement: String,
    pub hint: String,
    #[serde(default)]
    pub tools: BTreeMap<String, Option<bool>>,
    /// Initial network as JSON (raw text: key order in `hosts`, headers etc. matters).
    pub start: Box<RawValue>,
    pub goals: Vec<Box<RawValue>>,
    pub solution: Vec<TsOp>,
}

/// Dump file.
#[derive(Clone, Debug, Deserialize)]
pub struct Export {
    pub scenarios: Vec<TsScenario>,
}

/// Former key names (camelCase) -> canonical ones.
const RENAMES: &[(&str, &str)] = &[
    ("dropPrivate", "drop_private"),
    ("icmpBlock", "icmp_block"),
    ("arpStatic", "arp_static"),
    ("tlsMin", "tls_min"),
    ("sshKey", "ssh_key"),
    ("knownHosts", "known_hosts"),
    ("notAfter", "not_after"),
    ("hostKey", "host_key"),
    ("passwordAuth", "password_auth"),
    ("gatewayIp", "gateway_ip"),
    ("maxRttMs", "max_rtt_ms"),
    ("sizeFromMtu", "size_from_mtu"),
    ("noLoop", "no_loop"),
    ("notSeenBy", "not_seen_by"),
    ("seenSrc", "seen_src"),
    ("noHeader", "no_header"),
    ("bodyIncludes", "body_includes"),
    ("finalUrl", "final_url"),
    ("minMbps", "min_mbps"),
    ("maxLoadedRttMs", "max_loaded_rtt_ms"),
    ("maxS", "max_s"),
];

/// Normalize JSON for comparison: canonical keys, devices as an array, numbers as f64, without `null`, `false`
/// and empty objects/arrays (their absence is equivalent to the default value).
pub fn normalize(v: &Value, in_devices: bool) -> Value {
    match v {
        Value::Object(m) => {
            if in_devices {
                // "id -> device" becomes an array of devices (by id: key order in `Value` is lost)
                let mut v: Vec<Value> = m.values().map(|d| normalize(d, false)).collect();
                v.sort_by_key(|d| d["id"].as_str().unwrap_or("").to_string());
                return Value::Array(v);
            }
            let mut out = serde_json::Map::new();
            for (k, x) in m {
                let key = RENAMES.iter().find(|(a, _)| a == k).map(|(_, b)| b.to_string()).unwrap_or_else(|| k.clone());
                let mut nv = normalize(x, key == "devices" && x.is_object());
                if key == "devices" {
                    if let Value::Array(a) = &mut nv {
                        a.sort_by_key(|d| d["id"].as_str().unwrap_or("").to_string());
                    }
                }
                let empty = match &nv {
                    Value::Null | Value::Bool(false) => true,
                    Value::Object(o) => o.is_empty(),
                    Value::Array(a) => a.is_empty(),
                    _ => false,
                };
                if !empty {
                    out.insert(key, nv);
                }
            }
            Value::Object(out)
        }
        Value::Array(a) => Value::Array(a.iter().map(|x| normalize(x, false)).collect()),
        Value::Number(n) => n.as_f64().and_then(serde_json::Number::from_f64).map(Value::Number).unwrap_or_else(|| v.clone()),
        other => other.clone(),
    }
}

/// Turn a dump exercise into a task. Error means something was lost while parsing.
pub fn convert(s: &TsScenario) -> Result<Task, String> {
    let ctx = |e: String| format!("{}: {e}", s.id);
    let start: NetState = serde_json::from_str(s.start.get()).map_err(|e| ctx(i18n::trf!("start network: {0}", e)))?;
    start.validate().map_err(|e| ctx(i18n::trf!("start network: {0}", e)))?;
    let start_value: Value = serde_json::from_str(s.start.get()).map_err(|e| ctx(e.to_string()))?;
    let a = normalize(&start_value, false);
    let b = normalize(&serde_json::to_value(&start).map_err(|e| ctx(e.to_string()))?, false);
    if a != b {
        return Err(ctx(i18n::trf!("start network changed during parsing:\n  was    {0}\n  became {1}", a, b)));
    }
    let mut goals: Vec<Goal> = Vec::new();
    for g in &s.goals {
        let goal: Goal = serde_json::from_str(g.get()).map_err(|e| ctx(i18n::trf!("goal: {0}", e)))?;
        let gv: Value = serde_json::from_str(g.get()).map_err(|e| ctx(e.to_string()))?;
        let a = normalize(&gv, false);
        let b = normalize(&serde_json::to_value(&goal).map_err(|e| ctx(e.to_string()))?, false);
        if a != b {
            return Err(ctx(i18n::trf!("goal changed during parsing:\n  was    {0}\n  became {1}", a, b)));
        }
        goals.push(goal);
    }
    let mut tools = Tools::default();
    for (k, v) in &s.tools {
        if !tools.set(k, v.unwrap_or(false)) {
            return Err(ctx(i18n::trf!("unknown tool \"{0}\"", k)));
        }
    }
    Ok(Task {
        id: s.id.clone(),
        title: s.title.clone(),
        statement: s.statement.clone(),
        hint: s.hint.clone(),
        spec: NetSpec { tools, start, goals, solution: s.solution.iter().cloned().map(Step::from).collect() },
    })
}

/// Parse the whole dump into chapter files (in ascending chapter order).
pub fn convert_all(e: &Export) -> Result<Vec<LabChapter>, String> {
    let mut by: BTreeMap<u32, Vec<Task>> = BTreeMap::new();
    for s in &e.scenarios {
        by.entry(s.chapter).or_default().push(convert(s)?);
    }
    Ok(by.into_iter().map(|(chapter, tasks)| LabChapter { book: NET_BOOK, chapter, lab: "net".into(), tasks }).collect())
}
