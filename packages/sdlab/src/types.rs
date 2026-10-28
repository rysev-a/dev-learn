//! Lab types: service design, workload, evaluation result, goals and exercises.
//!
//! Field names in the data are `snake_case`. On reading, the former names from the TypeScript version are also accepted
//! (`dataGB`, `maxNodes`, `cdnHit` …) — via `alias`, to parse old drafts and exports.

use std::collections::BTreeMap;
use std::fmt;
use std::str::FromStr;

use serde::de::{self, MapAccess, Visitor};
use serde::ser::SerializeMap;
use serde::{Deserialize, Deserializer, Serialize, Serializer};

use crate::kinds;

/* ---------- component kinds ---------- */

/// Design component kind.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Kind {
    Clients,
    Cdn,
    Lb,
    Gateway,
    Limiter,
    App,
    Cache,
    Db,
    Queue,
    Worker,
    Blob,
    Search,
    Ws,
    Monitor,
    Auth,
    Geo,
    Ml,
    Pay,
    Stream,
    Notify,
    Analytics,
}

impl Kind {
    /// All kinds in declaration order.
    pub const ALL: [Kind; 21] = [
        Kind::Clients,
        Kind::Cdn,
        Kind::Lb,
        Kind::Gateway,
        Kind::Limiter,
        Kind::App,
        Kind::Cache,
        Kind::Db,
        Kind::Queue,
        Kind::Worker,
        Kind::Blob,
        Kind::Search,
        Kind::Ws,
        Kind::Monitor,
        Kind::Auth,
        Kind::Geo,
        Kind::Ml,
        Kind::Pay,
        Kind::Stream,
        Kind::Notify,
        Kind::Analytics,
    ];

    /// String name as in the data (`"cdn"`, `"app"` …).
    pub const fn as_str(self) -> &'static str {
        match self {
            Kind::Clients => "clients",
            Kind::Cdn => "cdn",
            Kind::Lb => "lb",
            Kind::Gateway => "gateway",
            Kind::Limiter => "limiter",
            Kind::App => "app",
            Kind::Cache => "cache",
            Kind::Db => "db",
            Kind::Queue => "queue",
            Kind::Worker => "worker",
            Kind::Blob => "blob",
            Kind::Search => "search",
            Kind::Ws => "ws",
            Kind::Monitor => "monitor",
            Kind::Auth => "auth",
            Kind::Geo => "geo",
            Kind::Ml => "ml",
            Kind::Pay => "pay",
            Kind::Stream => "stream",
            Kind::Notify => "notify",
            Kind::Analytics => "analytics",
        }
    }

    /// Ordinal of the kind (index in [`Kind::ALL`]).
    pub const fn index(self) -> usize {
        self as usize
    }

    /// Russian name of the component.
    pub fn label(self) -> &'static str {
        kinds::spec(self).label
    }
}

impl fmt::Display for Kind {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

impl FromStr for Kind {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Kind::ALL.iter().copied().find(|k| k.as_str() == s).ok_or_else(|| i18n::trf!("unknown component kind “{0}”", s))
    }
}

/// Services the application calls on a share of requests (`Workload::calls`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum DepKind {
    Auth,
    Geo,
    Ml,
    Pay,
}

impl DepKind {
    /// All dependencies in the engine's traversal order.
    pub const ALL: [DepKind; 4] = [DepKind::Auth, DepKind::Geo, DepKind::Ml, DepKind::Pay];

    /// Component kind responsible for the dependency.
    pub const fn kind(self) -> Kind {
        match self {
            DepKind::Auth => Kind::Auth,
            DepKind::Geo => Kind::Geo,
            DepKind::Ml => Kind::Ml,
            DepKind::Pay => Kind::Pay,
        }
    }
}

/// What to break in a failure check: a component kind (one instance) or a zone, region, deploy.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum FailKind {
    /// availability zone failure
    Zone,
    /// region failure
    Region,
    /// deploy of a new version
    Deploy,
    /// failure of one instance of a component of this kind
    Component(Kind),
}

impl FailKind {
    /// String for the data: `"zone"`, `"region"`, `"deploy"` or a component kind.
    pub const fn as_str(self) -> &'static str {
        match self {
            FailKind::Zone => "zone",
            FailKind::Region => "region",
            FailKind::Deploy => "deploy",
            FailKind::Component(k) => k.as_str(),
        }
    }
}

impl FromStr for FailKind {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "zone" => Ok(FailKind::Zone),
            "region" => Ok(FailKind::Region),
            "deploy" => Ok(FailKind::Deploy),
            other => Kind::from_str(other).map(FailKind::Component).map_err(|_| i18n::trf!("unknown failure “{0}”", other)),
        }
    }
}

impl Serialize for FailKind {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        s.serialize_str(self.as_str())
    }
}

impl<'de> Deserialize<'de> for FailKind {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        let s = String::deserialize(d)?;
        s.parse().map_err(de::Error::custom)
    }
}

/* ---------- parameters and design ---------- */

/// Component parameter value: number, string (from a list) or flag.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum ParamValue {
    Bool(bool),
    Num(f64),
    Str(String),
}

impl PartialEq for ParamValue {
    /// Strict equality, like `===` in JavaScript: a number is not equal to a string.
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (ParamValue::Bool(a), ParamValue::Bool(b)) => a == b,
            (ParamValue::Num(a), ParamValue::Num(b)) => a == b,
            (ParamValue::Str(a), ParamValue::Str(b)) => a == b,
            _ => false,
        }
    }
}

impl From<f64> for ParamValue {
    fn from(v: f64) -> Self {
        ParamValue::Num(v)
    }
}
impl From<i32> for ParamValue {
    fn from(v: i32) -> Self {
        ParamValue::Num(f64::from(v))
    }
}
impl From<bool> for ParamValue {
    fn from(v: bool) -> Self {
        ParamValue::Bool(v)
    }
}
impl From<&str> for ParamValue {
    fn from(v: &str) -> Self {
        ParamValue::Str(v.to_owned())
    }
}

impl ParamValue {
    /// Number: like `Number(v) || 0` in JavaScript (flag — 0/1, non-numeric string — 0).
    pub fn as_num(&self) -> f64 {
        match self {
            ParamValue::Num(x) => *x,
            ParamValue::Bool(b) => f64::from(u8::from(*b)),
            ParamValue::Str(s) => {
                let t = s.trim();
                if t.is_empty() {
                    0.0
                } else {
                    t.parse::<f64>().ok().filter(|x| !x.is_nan()).unwrap_or(0.0)
                }
            }
        }
    }

    /// Number for comparisons: like `Number(v)` in JavaScript (non-numeric string — `NaN`, for which comparisons are false).
    pub fn to_number(&self) -> f64 {
        match self {
            ParamValue::Str(s) => {
                let t = s.trim();
                if t.is_empty() {
                    0.0
                } else {
                    t.parse::<f64>().unwrap_or(f64::NAN)
                }
            }
            other => other.as_num(),
        }
    }

    /// String: like `String(v)` in JavaScript.
    pub fn as_text(&self) -> std::borrow::Cow<'_, str> {
        match self {
            ParamValue::Str(s) => std::borrow::Cow::Borrowed(s),
            ParamValue::Num(x) => std::borrow::Cow::Owned(crate::jsfmt::num(*x)),
            ParamValue::Bool(b) => std::borrow::Cow::Borrowed(if *b { "true" } else { "false" }),
        }
    }

    /// Flag is on (only a real `true`).
    pub fn is_true(&self) -> bool {
        matches!(self, ParamValue::Bool(true))
    }
}

fn de_params<'de, D: Deserializer<'de>>(d: D) -> Result<BTreeMap<String, ParamValue>, D::Error> {
    let raw = BTreeMap::<String, ParamValue>::deserialize(d)?;
    Ok(raw.into_iter().map(|(k, v)| (kinds::canonical_param_key(&k).to_owned(), v)).collect())
}

fn unplaced() -> f64 {
    -1.0
}

/// Component on the design.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SdNode {
    pub id: String,
    pub kind: Kind,
    /// Name on the design; empty on reading is replaced by the kind name ([`SdState::normalize`]).
    #[serde(default)]
    pub name: String,
    /// Position on the board; negative — "not placed", laid out by [`crate::layout::place`].
    #[serde(default = "unplaced")]
    pub x: f64,
    #[serde(default = "unplaced")]
    pub y: f64,
    #[serde(default, deserialize_with = "de_params")]
    pub params: BTreeMap<String, ParamValue>,
}

impl SdNode {
    /// New component with defaults overridden by `params`; the name is the kind name.
    pub fn new(id: &str, kind: Kind, params: &[(&str, ParamValue)]) -> SdNode {
        let mut p = kinds::default_params(kind);
        for (k, v) in params {
            p.insert((*k).to_owned(), v.clone());
        }
        SdNode { id: id.to_owned(), kind, name: kind.label().to_owned(), x: -1.0, y: -1.0, params: p }
    }

    /// Parameter value: the set one, else the kind default, else 0.
    pub fn param(&self, key: &str) -> &ParamValue {
        static ZERO: ParamValue = ParamValue::Num(0.0);
        match self.params.get(key) {
            Some(v) => v,
            None => kinds::default_param(self.kind, key).unwrap_or(&ZERO),
        }
    }

    /// Numeric parameter value.
    pub fn num(&self, key: &str) -> f64 {
        self.param(key).as_num()
    }

    /// String parameter value.
    pub fn text(&self, key: &str) -> std::borrow::Cow<'_, str> {
        self.param(key).as_text()
    }

    /// Flag parameter is on.
    pub fn flag(&self, key: &str) -> bool {
        self.param(key).is_true()
    }
}

/// Link "from output to input".
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SdEdge {
    pub from: String,
    pub to: String,
}

impl SdEdge {
    pub fn new(from: &str, to: &str) -> SdEdge {
        SdEdge { from: from.to_owned(), to: to.to_owned() }
    }
}

/// Design: components and links. This is also the student's solution (draft in the account, `solution` on the server).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct SdState {
    #[serde(default)]
    pub nodes: Vec<SdNode>,
    #[serde(default)]
    pub edges: Vec<SdEdge>,
}

impl SdState {
    /// Fills in the kind name for components without a name.
    pub fn normalize(&mut self) {
        for n in &mut self.nodes {
            if n.name.is_empty() {
                n.name = n.kind.label().to_owned();
            }
        }
    }

    /// Component by id (first).
    pub fn node(&self, id: &str) -> Option<&SdNode> {
        self.nodes.iter().find(|n| n.id == id)
    }

    /// Components of the given kind.
    pub fn of_kind(&self, kind: Kind) -> impl Iterator<Item = &SdNode> {
        self.nodes.iter().filter(move |n| n.kind == kind)
    }
}

/* ---------- workload ---------- */

/// Share of application requests that call a dependency service (0..1).
#[derive(Debug, Clone, Copy, Default, PartialEq, Serialize, Deserialize)]
pub struct Calls {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub auth: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub geo: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ml: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub pay: Option<f64>,
}

impl Calls {
    /// Share of calls to the service (0 if not set).
    pub fn get(&self, k: DepKind) -> f64 {
        match k {
            DepKind::Auth => self.auth,
            DepKind::Geo => self.geo,
            DepKind::Ml => self.ml,
            DepKind::Pay => self.pay,
        }
        .unwrap_or(0.0)
    }
}

/// Service workload: requests per second by class and data.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Workload {
    /// static content (images, scripts), req/s: CDN or blob; otherwise served by the application
    #[serde(alias = "static")]
    pub static_rps: f64,
    /// dynamic reads, req/s
    #[serde(alias = "read")]
    pub read_rps: f64,
    /// writes, req/s
    #[serde(alias = "write")]
    pub write_rps: f64,
    /// share of reads that are actually search (go to search; without it — a heavy DB query)
    #[serde(default, alias = "searchShare", skip_serializing_if = "Option::is_none")]
    pub search_share: Option<f64>,
    /// data volume, GB
    #[serde(alias = "dataGB")]
    pub data_gb: f64,
    /// share of data read frequently (working set), 0..1
    #[serde(alias = "hotSet")]
    pub hot_set: f64,
    /// share of requests to the single "hottest" key (0..1): shard skew
    #[serde(default, alias = "hotKey", skip_serializing_if = "Option::is_none")]
    pub hot_key: Option<f64>,
    /// concurrent WebSocket connections
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub connections: Option<f64>,
    /// messages per second per connection
    #[serde(default, alias = "msgPerConn", skip_serializing_if = "Option::is_none")]
    pub msg_per_conn: Option<f64>,
    /// spike duration for computing queue lag, seconds
    #[serde(default, alias = "spikeSec", skip_serializing_if = "Option::is_none")]
    pub spike_sec: Option<f64>,
    /// shard keys grow monotonically: with range sharding all writes go to one shard
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub monotonic: Option<bool>,
    /// average number of an author's followers (feed)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fanout: Option<f64>,
    /// shares of application requests to dependency services; without a link to the service such requests fail
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub calls: Option<Calls>,
    /// geo-position updates per second (taxi, couriers)
    #[serde(default, alias = "geoUpdates", skip_serializing_if = "Option::is_none")]
    pub geo_updates: Option<f64>,
    /// volume of files in object storage, TB
    #[serde(default, alias = "mediaTB", skip_serializing_if = "Option::is_none")]
    pub media_tb: Option<f64>,
}

impl Workload {
    /// Workload from the three main numbers; the rest is default (data 10 GB, working set 20%).
    pub fn new(static_rps: f64, read_rps: f64, write_rps: f64) -> Workload {
        Workload { static_rps, read_rps, write_rps, data_gb: 10.0, hot_set: 0.2, ..Workload::default() }
    }

    pub(crate) fn calls_of(&self, k: DepKind) -> f64 {
        self.calls.map_or(0.0, |c| c.get(k))
    }
}

/* ---------- evaluation result ---------- */

/// Evaluation options: what to break.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct EvalOptions {
    /// break one instance of each component of this kind (or a whole zone, region, deploy)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fail: Option<FailKind>,
    /// manually disabled nodes (click on a node in the UI)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub down: Vec<String>,
}

impl EvalOptions {
    /// Failure only.
    pub fn fail(f: FailKind) -> EvalOptions {
        EvalOptions { fail: Some(f), down: Vec::new() }
    }
}

/// Node state by utilization.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum NodeStatus {
    Idle,
    Ok,
    Warm,
    Hot,
    Over,
    Down,
}

/// Accepts `null` instead of a non-numeric value (JSON has no NaN or infinity).
fn lenient_f64<'de, D: Deserializer<'de>>(d: D) -> Result<f64, D::Error> {
    Ok(Option::<f64>::deserialize(d)?.unwrap_or(f64::NAN))
}

/// Node load.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NodeLoad {
    /// incoming load, conventional requests per second
    #[serde(deserialize_with = "lenient_f64")]
    pub load: f64,
    /// capacity (what the node can handle), conventional requests per second
    #[serde(deserialize_with = "lenient_f64")]
    pub cap: f64,
    #[serde(deserialize_with = "lenient_f64")]
    pub util: f64,
    #[serde(deserialize_with = "lenient_f64")]
    pub units: f64,
    pub status: NodeStatus,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub note: Option<String>,
}

/// Node loads in the order of design nodes (without users); in JSON — an object `{id: load}`.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct Loads(Vec<(String, NodeLoad)>);

impl Loads {
    pub fn get(&self, id: &str) -> Option<&NodeLoad> {
        self.0.iter().find(|(k, _)| k == id).map(|(_, v)| v)
    }
    pub fn iter(&self) -> impl Iterator<Item = (&str, &NodeLoad)> {
        self.0.iter().map(|(k, v)| (k.as_str(), v))
    }
    pub fn len(&self) -> usize {
        self.0.len()
    }
    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }
    pub(crate) fn push(&mut self, id: String, load: NodeLoad) {
        self.0.push((id, load));
    }
}

impl Serialize for Loads {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        let mut m = s.serialize_map(Some(self.0.len()))?;
        for (k, v) in &self.0 {
            m.serialize_entry(k, v)?;
        }
        m.end()
    }
}

impl<'de> Deserialize<'de> for Loads {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct V;
        impl<'de> Visitor<'de> for V {
            type Value = Loads;
            fn expecting(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                f.write_str(i18n::tr("an object “node id → workload”"))
            }
            fn visit_map<A: MapAccess<'de>>(self, mut m: A) -> Result<Loads, A::Error> {
                let mut out = Vec::new();
                while let Some((k, v)) = m.next_entry::<String, NodeLoad>()? {
                    out.push((k, v));
                }
                Ok(Loads(out))
            }
        }
        d.deserialize_map(V)
    }
}

/// Result of evaluating a design under a workload (`Result` in TypeScript).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EvalResult {
    pub loads: Loads,
    /// average and "tail" latency of a user request, ms
    #[serde(deserialize_with = "lenient_f64")]
    pub p50: f64,
    #[serde(deserialize_with = "lenient_f64")]
    pub p99: f64,
    /// success rate, 0..1 (accounting for overloads)
    #[serde(deserialize_with = "lenient_f64")]
    pub success: f64,
    /// design availability by components, 0..1
    #[serde(deserialize_with = "lenient_f64")]
    pub availability: f64,
    /// cost, $ per month
    #[serde(deserialize_with = "lenient_f64")]
    pub cost: f64,
    /// share of reads from cache (`None` — no cache)
    pub hit: Option<f64>,
    #[serde(alias = "cdnHit")]
    pub cdn_hit: Option<f64>,
    /// queue lag after a spike, seconds (`None` — no queue; 999 — not draining)
    #[serde(alias = "lagSec")]
    pub lag_sec: Option<f64>,
    /// replica lag, ms
    #[serde(alias = "replicaLagMs")]
    pub replica_lag_ms: Option<f64>,
    /// maximum share of data on one shard, 0..1
    #[serde(alias = "maxShardShare")]
    pub max_shard_share: Option<f64>,
    /// whether there is a path from users to request processing
    pub entry: bool,
    /// warnings: extra links, unconnected components…
    pub warnings: Vec<String>,
}

/* ---------- goals and exercises ---------- */

/// Parameter value comparison.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Op {
    #[serde(rename = ">=")]
    Ge,
    #[serde(rename = "<=")]
    Le,
    #[serde(rename = "==")]
    Eq,
    #[serde(rename = "!=")]
    Ne,
}

impl Op {
    /// Operator spelling, as in the goal text.
    pub const fn as_str(self) -> &'static str {
        match self {
            Op::Ge => ">=",
            Op::Le => "<=",
            Op::Eq => "==",
            Op::Ne => "!=",
        }
    }
}

/// Exercise goal. In the data — an object with a `type` field (`{"type": "p99", "max": 150}`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Goal {
    /// no component is utilized above `max` (0..1)
    Capacity { max: f64 },
    /// a component of this kind is utilized at most `max`
    Util { kind: Kind, max: f64 },
    P99 { max: f64 },
    P50 { max: f64 },
    Success { min: f64 },
    Availability { min: f64 },
    Cost { max: f64 },
    /// the design has a component (at least `min` of them, default 1)
    Has {
        kind: Kind,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        min: Option<f64>,
    },
    Lacks { kind: Kind },
    /// there is a link from a component of kind `from` to a component of kind `to`
    Link { from: Kind, to: Kind },
    Hit { min: f64 },
    #[serde(alias = "cdnHit")]
    CdnHit { min: f64 },
    /// after the failure at least 99% of requests succeed
    Survive { fail: FailKind },
    /// the parameter of all components of the kind satisfies the condition
    Param {
        kind: Kind,
        #[serde(deserialize_with = "de_param_key")]
        key: String,
        op: Op,
        value: ParamValue,
    },
    Lag { max: f64 },
    #[serde(alias = "replicaLag")]
    ReplicaLag { max: f64 },
    #[serde(alias = "shardShare")]
    ShardShare { max: f64 },
    /// no single point of failure among components of these kinds
    #[serde(alias = "noSpof")]
    NoSpof { kinds: Vec<Kind> },
}

fn de_param_key<'de, D: Deserializer<'de>>(d: D) -> Result<String, D::Error> {
    let s = String::deserialize(d)?;
    Ok(kinds::canonical_param_key(&s).to_owned())
}

/// Result of checking one goal.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GoalResult {
    pub ok: bool,
    /// condition in words
    pub text: String,
    /// "now …" — what came out
    pub detail: String,
}

fn default_max_nodes() -> usize {
    14
}

fn no_show(v: &[String]) -> bool {
    v.is_empty()
}

fn de_show<'de, D: Deserializer<'de>>(d: D) -> Result<Vec<String>, D::Error> {
    let raw = Vec::<String>::deserialize(d)?;
    Ok(raw.into_iter().map(|s| kinds::canonical_show_key(&s)).collect())
}

/// Exercise content without text: workload, palette, starting design, goals and reference solution.
/// The backend does not send `solution` to the client.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    pub workload: Workload,
    /// which components can be added from the panel
    pub palette: Vec<Kind>,
    /// starting design
    pub start: SdState,
    pub goals: Vec<Goal>,
    /// reference design (checked by the self-check and tests)
    pub solution: SdState,
    /// how many nodes the design may hold (default 14)
    #[serde(default, alias = "maxNodes", skip_serializing_if = "Option::is_none")]
    pub max_nodes: Option<usize>,
    /// which extra parameters to show: `"app.retries"` etc.
    #[serde(default, deserialize_with = "de_show", skip_serializing_if = "no_show")]
    pub show: Vec<String>,
}

impl Scenario {
    /// Limit on the number of nodes in the design.
    pub fn max_nodes(&self) -> usize {
        self.max_nodes.unwrap_or_else(default_max_nodes)
    }

    /// Whether to show a parameter in the component panel: basic ones — always, extra ones — if listed in `show`.
    pub fn param_visible(&self, kind: Kind, p: &kinds::ParamSpec) -> bool {
        p.basic || self.show.iter().any(|s| s.split_once('.').is_some_and(|(k, key)| k == kind.as_str() && key == p.key))
    }

    /// Copy for the client: without the reference solution.
    pub fn without_solution(&self) -> Scenario {
        Scenario { solution: SdState::default(), ..self.clone() }
    }
}

/// Exercise: text and content.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    /// statement (a paragraph)
    pub statement: String,
    pub hint: String,
    pub spec: Scenario,
}

/// Chapter data file: `backend/data/labs/sd/<book>-<chapter:02>.json`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// lab kind (`"sd"`)
    pub lab: String,
    pub tasks: Vec<Task>,
}
