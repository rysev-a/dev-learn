//! Component catalog: Russian names, configurable parameters, defaults, palette.
//! Capacity, price and latency numbers are in [`crate::reference`].

use std::collections::BTreeMap;
use std::sync::LazyLock;

use serde::Serialize;

use crate::types::{Kind, ParamValue};

/// Field type of a parameter in the component panel.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum ParamType {
    Int,
    Select,
    Bool,
}

/// Choice option.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ParamOption {
    pub value: ParamValue,
    pub label: &'static str,
}

/// Description of a component parameter.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ParamSpec {
    pub key: &'static str,
    pub label: &'static str,
    #[serde(rename = "type")]
    pub ty: ParamType,
    pub min: Option<f64>,
    pub max: Option<f64>,
    pub options: Vec<ParamOption>,
    pub default: ParamValue,
    /// hint under the field
    pub help: Option<&'static str>,
    /// `false` — shown only in exercises where the parameter is listed in `show`
    pub basic: bool,
    /// the engine does not read the parameter: it exists only for `param` goals (a "how it works" marker, not an evaluation lever)
    pub inert: bool,
}

impl ParamSpec {
    fn int(key: &'static str, label: &'static str, min: i32, max: i32, default: i32) -> ParamSpec {
        ParamSpec {
            key,
            label,
            ty: ParamType::Int,
            min: Some(f64::from(min)),
            max: Some(f64::from(max)),
            options: Vec::new(),
            default: default.into(),
            help: None,
            basic: true,
            inert: false,
        }
    }

    fn select(key: &'static str, label: &'static str, options: &[(ParamValue, &'static str)], default: ParamValue) -> ParamSpec {
        ParamSpec {
            key,
            label,
            ty: ParamType::Select,
            min: None,
            max: None,
            options: options.iter().map(|(v, l)| ParamOption { value: v.clone(), label: l }).collect(),
            default,
            help: None,
            basic: true,
            inert: false,
        }
    }

    fn flag(key: &'static str, label: &'static str) -> ParamSpec {
        ParamSpec { key, label, ty: ParamType::Bool, min: None, max: None, options: Vec::new(), default: false.into(), help: None, basic: true, inert: false }
    }

    fn help(mut self, h: &'static str) -> ParamSpec {
        self.help = Some(h);
        self
    }

    /// A parameter the engine does not read (see [`ParamSpec::inert`]).
    fn inert(mut self) -> ParamSpec {
        self.inert = true;
        self
    }

    /// Extra parameter: visible only in exercises that list it in `show`.
    fn advanced(mut self) -> ParamSpec {
        self.basic = false;
        self
    }
}

/// Description of a component kind.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct KindSpec {
    pub kind: Kind,
    pub label: &'static str,
    /// one line: what the component does
    pub about: &'static str,
    pub params: Vec<ParamSpec>,
    /// layout column, left to right
    pub col: usize,
}

fn s(v: &'static str) -> ParamValue {
    ParamValue::Str(v.to_owned())
}

fn n(v: i32) -> ParamValue {
    ParamValue::Num(f64::from(v))
}

fn size() -> ParamSpec {
    ParamSpec::select("size", i18n::tr("Size"), &[(s("S"), i18n::tr("S — small")), (s("M"), i18n::tr("M — medium")), (s("L"), i18n::tr("L — large"))], s("S"))
}

fn zone() -> ParamSpec {
    ParamSpec::select(
        "zone",
        i18n::tr("Placement"),
        &[(s("single"), i18n::tr("single zone")), (s("multi"), i18n::tr("three zones of a region")), (s("regions"), i18n::tr("two regions"))],
        s("single"),
    )
    .help(i18n::tr("zone failure: “single zone” loses everything, the others lose a third; region failure: two regions lose half"))
}

fn ttl() -> ParamSpec {
    ParamSpec::select("ttl", i18n::tr("TTL, s"), &[(n(30), "30"), (n(300), "300"), (n(3600), "3600")], n(300))
}

fn pricing(spot: &'static str) -> ParamSpec {
    ParamSpec::select(
        "pricing",
        i18n::tr("Pricing"),
        &[(s("ondemand"), i18n::tr("on demand")), (s("reserved"), i18n::tr("reserved (−40%)")), (s("spot"), spot)],
        s("ondemand"),
    )
    .advanced()
}

fn instances(max: i32) -> ParamSpec {
    ParamSpec::int("instances", i18n::tr("Instances"), 1, max, 1)
}

fn mk(kind: Kind, label: &'static str, about: &'static str, col: usize, params: Vec<ParamSpec>) -> KindSpec {
    KindSpec { kind, label, about, params, col }
}

fn build() -> Vec<KindSpec> {
    // order — as in `Kind::ALL`
    let mut v = vec![
        mk(Kind::Clients, i18n::tr("Users"), i18n::tr("source of the load"), 0, vec![]),
        mk(Kind::Cdn, "CDN", i18n::tr("serves static content from the nearest servers"), 1, vec![ttl().help(i18n::tr("the larger the TTL, the higher the hit ratio"))]),
        mk(Kind::Lb, i18n::tr("Load balancer"), i18n::tr("splits requests between servers"), 3, vec![
            ParamSpec::int("instances", i18n::tr("Instances"), 1, 3, 1),
            ParamSpec::select("layer", i18n::tr("Layer"), &[(s("L4"), "L4 (TCP)"), (s("L7"), "L7 (HTTP)")], s("L4")),
        ]),
        mk(Kind::Gateway, i18n::tr("API gateway"), i18n::tr("entry point: authorization, routing, limits"), 2, vec![ParamSpec::int("instances", i18n::tr("Instances"), 1, 4, 1)]),
        mk(Kind::Limiter, i18n::tr("Rate limiter"), i18n::tr("lets through at most N requests per second"), 2, vec![ParamSpec::int("limit", i18n::tr("Limit, req/s"), 100, 50000, 2000)]),
        mk(Kind::App, i18n::tr("App server"), i18n::tr("stateless business logic"), 4, vec![
            // the upper limit is 40, not 30 as in the TypeScript version: reference solutions of the final exercises (chapters 22–24) need 33–35 servers
            instances(40),
            size(),
            ParamSpec::select("sessions", i18n::tr("Sessions"), &[(s("local"), i18n::tr("in server memory")), (s("external"), i18n::tr("in external storage"))], s("local")),
            zone(),
            ParamSpec::int("weight", i18n::tr("Traffic share"), 1, 10, 1).advanced().help(i18n::tr("service weight when traffic is split between services")),
            ParamSpec::flag("idempotency", i18n::tr("Idempotency keys")).advanced().inert(),
            ParamSpec::int("retries", i18n::tr("DB retries"), 0, 3, 0).advanced().help(i18n::tr("retries without a pause make overload worse")),
            ParamSpec::flag("breaker", i18n::tr("Circuit breaker")).advanced().help(i18n::tr("stops retries when the database is overloaded")),
            ParamSpec::select(
                "feed",
                i18n::tr("Feed"),
                &[(s("pull"), i18n::tr("pull — build on read")), (s("push"), i18n::tr("push — fan out on write")), (s("hybrid"), i18n::tr("hybrid"))],
                s("pull"),
            )
            .advanced(),
            ParamSpec::select(
                "deploy",
                i18n::tr("Deployment"),
                &[(s("all"), i18n::tr("all at once")), (s("rolling"), i18n::tr("one at a time (rolling)")), (s("bluegreen"), "blue/green")],
                s("all"),
            )
            .advanced()
            .help(i18n::tr("blue/green keeps a second copy — cost ×2")),
            pricing(i18n::tr("spot (−70%, can be interrupted)")),
        ]),
        mk(Kind::Cache, i18n::tr("Cache"), i18n::tr("fast memory for hot data"), 5, vec![
            ParamSpec::int("size_gb", i18n::tr("Memory, GB"), 1, 128, 4),
            ttl(),
            ParamSpec::select(
                "policy",
                i18n::tr("Write policy"),
                &[(s("aside"), "cache-aside"), (s("through"), "write-through"), (s("back"), "write-back")],
                s("aside"),
            )
            .help(i18n::tr("write-back takes write load off the DB, but data may be lost"))
            .advanced(),
            ParamSpec::int("replicas", i18n::tr("Replicas"), 0, 2, 0),
            zone(),
        ]),
        mk(Kind::Db, i18n::tr("Database"), i18n::tr("persistent storage"), 7, vec![
            size(),
            ParamSpec::int("replicas", i18n::tr("Replicas per shard"), 0, 5, 0),
            ParamSpec::int("shards", i18n::tr("Shards"), 1, 16, 1),
            ParamSpec::flag("failover", i18n::tr("Automatic failover")).help(i18n::tr("when the leader fails, a replica takes its place")),
            ParamSpec::select("engine", i18n::tr("Type"), &[(s("sql"), "SQL"), (s("nosql"), "NoSQL")], s("sql")),
            ParamSpec::select("sync", i18n::tr("Replication"), &[(s("async"), i18n::tr("asynchronous")), (s("sync"), i18n::tr("synchronous"))], s("async"))
                .advanced()
                .help(i18n::tr("synchronous: replicas never lag, but writes are slower")),
            ParamSpec::select("shard_key", i18n::tr("Shard key"), &[(s("hash"), i18n::tr("hash")), (s("range"), i18n::tr("range"))], s("hash")).advanced(),
            zone(),
        ]),
        mk(Kind::Queue, i18n::tr("Queue"), i18n::tr("buffer between producers and workers"), 5, vec![
            ParamSpec::int("partitions", i18n::tr("Partitions"), 1, 16, 1),
            ParamSpec::flag("dlq", i18n::tr("Dead-letter queue")).advanced().inert(),
        ]),
        mk(Kind::Worker, i18n::tr("Worker"), i18n::tr("consumes the queue"), 6, vec![
            instances(30),
            ParamSpec::select("size", i18n::tr("Size"), &[(s("S"), i18n::tr("S — small")), (s("M"), i18n::tr("M — medium"))], s("S")),
            zone(),
            ParamSpec::flag("idempotent", i18n::tr("Idempotent processing")).advanced().inert().help(i18n::tr("redelivery does not corrupt data")),
            pricing(i18n::tr("spot (−70%)")),
        ]),
        mk(Kind::Blob, i18n::tr("Object storage"), i18n::tr("files and media"), 7, vec![ParamSpec::select(
            "tier",
            i18n::tr("Storage class"),
            &[(s("hot"), i18n::tr("hot ($23/TB)")), (s("mix"), i18n::tr("hot + cold ($10/TB)")), (s("cold"), i18n::tr("cold ($4/TB)"))],
            s("hot"),
        )
        .advanced()
        .help(i18n::tr("cold is cheaper, but object access is slower"))]),
        mk(Kind::Search, i18n::tr("Search"), i18n::tr("full-text index"), 7, vec![
            ParamSpec::int("shards", i18n::tr("Shards"), 1, 16, 1),
            ParamSpec::int("replicas", i18n::tr("Replicas"), 1, 6, 1),
        ]),
        mk(Kind::Ws, i18n::tr("WebSocket gateway"), i18n::tr("holds persistent connections"), 3, vec![instances(40)]),
        mk(Kind::Monitor, i18n::tr("Monitoring"), i18n::tr("metrics, logs, alerts"), 6, vec![]),
        mk(Kind::Auth, i18n::tr("Auth service"), i18n::tr("authentication and permissions: token and session checks"), 5, vec![instances(20)]),
        mk(Kind::Geo, i18n::tr("Geo service"), i18n::tr("in-memory geosearch and locations: nearest drivers, couriers, restaurants"), 5, vec![instances(30)]),
        mk(Kind::Ml, i18n::tr("Ranking service"), i18n::tr("recommendation and scoring model: expensive computation per request"), 5, vec![instances(20)]),
        mk(Kind::Pay, i18n::tr("Payment gateway"), i18n::tr("external payment provider: a slow and expensive call"), 5, vec![ParamSpec::int("instances", i18n::tr("Provider channels"), 1, 4, 1)]),
        mk(Kind::Stream, i18n::tr("Event stream"), i18n::tr("partitioned event log: each consumer gets its own copy"), 5, vec![ParamSpec::int("partitions", i18n::tr("Partitions"), 1, 32, 1)]),
        mk(Kind::Notify, i18n::tr("Notifications"), i18n::tr("sends pushes and emails from a queue or stream"), 6, vec![instances(20)]),
        mk(Kind::Analytics, i18n::tr("Analytics"), i18n::tr("event store for reports and product metrics"), 6, vec![instances(10)]),
    ];
    // bring into Kind::ALL order
    v.sort_by_key(|k| k.kind.index());
    v
}

static SPECS: LazyLock<Vec<KindSpec>> = LazyLock::new(build);

/// Description of a component kind.
pub fn spec(kind: Kind) -> &'static KindSpec {
    // the order in SPECS matches Kind::ALL (build sorts by kind index)
    &SPECS[kind.index()]
}

/// Descriptions of all kinds in [`Kind::ALL`] order.
pub fn all_specs() -> &'static [KindSpec] {
    &SPECS
}

/// Parameter description of a kind by key.
pub fn param_spec(kind: Kind, key: &str) -> Option<&'static ParamSpec> {
    spec(kind).params.iter().find(|p| p.key == key)
}

/// Default parameter value.
pub fn default_param(kind: Kind, key: &str) -> Option<&'static ParamValue> {
    param_spec(kind, key).map(|p| &p.default)
}

/// Parameters of a new component: all defaults.
pub fn default_params(kind: Kind) -> BTreeMap<String, ParamValue> {
    spec(kind).params.iter().map(|p| (p.key.to_owned(), p.default.clone())).collect()
}

/// Component order in the palette.
pub const KIND_ORDER: [Kind; 20] = [
    Kind::Cdn,
    Kind::Limiter,
    Kind::Gateway,
    Kind::Lb,
    Kind::Ws,
    Kind::App,
    Kind::Cache,
    Kind::Queue,
    Kind::Worker,
    Kind::Db,
    Kind::Blob,
    Kind::Search,
    Kind::Auth,
    Kind::Geo,
    Kind::Ml,
    Kind::Pay,
    Kind::Stream,
    Kind::Notify,
    Kind::Analytics,
    Kind::Monitor,
];

/// Parameter key in the modern spelling: the former `sizeGB` and `shardKey` from the TypeScript version become `size_gb` and `shard_key`.
pub fn canonical_param_key(key: &str) -> &str {
    match key {
        "sizeGB" => "size_gb",
        "shardKey" => "shard_key",
        other => other,
    }
}

/// Entry of the `show` list (`"db.shardKey"`) in the modern spelling (`"db.shard_key"`).
pub fn canonical_show_key(entry: &str) -> String {
    match entry.split_once('.') {
        Some((kind, key)) => format!("{kind}.{}", canonical_param_key(key)),
        None => entry.to_owned(),
    }
}
