//! Типы лаборатории: схема сервиса, нагрузка, результат расчёта, цели и упражнения.
//!
//! Имена полей в данных — `snake_case`. При чтении принимаются и прежние имена из TypeScript-версии
//! (`dataGB`, `maxNodes`, `cdnHit` …) — через `alias`, чтобы разбирать старые черновики и выгрузки.

use std::collections::BTreeMap;
use std::fmt;
use std::str::FromStr;

use serde::de::{self, MapAccess, Visitor};
use serde::ser::SerializeMap;
use serde::{Deserialize, Deserializer, Serialize, Serializer};

use crate::kinds;

/* ---------- виды компонентов ---------- */

/// Вид компонента схемы.
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
    /// Все виды в порядке объявления.
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

    /// Строковое имя, как в данных (`"cdn"`, `"app"` …).
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

    /// Порядковый номер вида (индекс в [`Kind::ALL`]).
    pub const fn index(self) -> usize {
        self as usize
    }

    /// Русское название компонента.
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
        Kind::ALL.iter().copied().find(|k| k.as_str() == s).ok_or_else(|| format!("неизвестный вид компонента «{s}»"))
    }
}

/// Сервисы, которые приложение вызывает на части запросов (`Workload::calls`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum DepKind {
    Auth,
    Geo,
    Ml,
    Pay,
}

impl DepKind {
    /// Все зависимости в порядке обхода движком.
    pub const ALL: [DepKind; 4] = [DepKind::Auth, DepKind::Geo, DepKind::Ml, DepKind::Pay];

    /// Вид компонента, который отвечает за зависимость.
    pub const fn kind(self) -> Kind {
        match self {
            DepKind::Auth => Kind::Auth,
            DepKind::Geo => Kind::Geo,
            DepKind::Ml => Kind::Ml,
            DepKind::Pay => Kind::Pay,
        }
    }
}

/// Что ломаем при проверке отказа: вид компонента (по одному экземпляру) или зона, регион, выкладка.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum FailKind {
    /// отказ зоны доступности
    Zone,
    /// отказ региона
    Region,
    /// выкладка новой версии
    Deploy,
    /// отказ одного экземпляра компонента этого вида
    Component(Kind),
}

impl FailKind {
    /// Строка для данных: `"zone"`, `"region"`, `"deploy"` или вид компонента.
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
            other => Kind::from_str(other).map(FailKind::Component).map_err(|_| format!("неизвестный отказ «{other}»")),
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

/* ---------- параметры и схема ---------- */

/// Значение параметра компонента: число, строка (из списка) или флаг.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum ParamValue {
    Bool(bool),
    Num(f64),
    Str(String),
}

impl PartialEq for ParamValue {
    /// Строгое равенство, как `===` в JavaScript: число не равно строке.
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
    /// Число: как `Number(v) || 0` в JavaScript (флаг — 0/1, нечисловая строка — 0).
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

    /// Число для сравнений: как `Number(v)` в JavaScript (нечисловая строка — `NaN`, при котором сравнения ложны).
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

    /// Строка: как `String(v)` в JavaScript.
    pub fn as_text(&self) -> std::borrow::Cow<'_, str> {
        match self {
            ParamValue::Str(s) => std::borrow::Cow::Borrowed(s),
            ParamValue::Num(x) => std::borrow::Cow::Owned(crate::jsfmt::num(*x)),
            ParamValue::Bool(b) => std::borrow::Cow::Borrowed(if *b { "true" } else { "false" }),
        }
    }

    /// Флаг включён (только настоящий `true`).
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

/// Компонент на схеме.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SdNode {
    pub id: String,
    pub kind: Kind,
    /// Название на схеме; пустое при чтении заменяется названием вида ([`SdState::normalize`]).
    #[serde(default)]
    pub name: String,
    /// Положение на поле; отрицательное — «не размещён», его расставляет [`crate::layout::place`].
    #[serde(default = "unplaced")]
    pub x: f64,
    #[serde(default = "unplaced")]
    pub y: f64,
    #[serde(default, deserialize_with = "de_params")]
    pub params: BTreeMap<String, ParamValue>,
}

impl SdNode {
    /// Новый компонент с параметрами по умолчанию, перекрытыми `params`; название — название вида.
    pub fn new(id: &str, kind: Kind, params: &[(&str, ParamValue)]) -> SdNode {
        let mut p = kinds::default_params(kind);
        for (k, v) in params {
            p.insert((*k).to_owned(), v.clone());
        }
        SdNode { id: id.to_owned(), kind, name: kind.label().to_owned(), x: -1.0, y: -1.0, params: p }
    }

    /// Значение параметра: заданное, иначе по умолчанию для вида, иначе 0.
    pub fn param(&self, key: &str) -> &ParamValue {
        static ZERO: ParamValue = ParamValue::Num(0.0);
        match self.params.get(key) {
            Some(v) => v,
            None => kinds::default_param(self.kind, key).unwrap_or(&ZERO),
        }
    }

    /// Числовое значение параметра.
    pub fn num(&self, key: &str) -> f64 {
        self.param(key).as_num()
    }

    /// Строковое значение параметра.
    pub fn text(&self, key: &str) -> std::borrow::Cow<'_, str> {
        self.param(key).as_text()
    }

    /// Флаг-параметр включён.
    pub fn flag(&self, key: &str) -> bool {
        self.param(key).is_true()
    }
}

/// Связь «от выхода к входу».
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

/// Схема: компоненты и связи. Это же — решение ученика (черновик в кабинете, `solution` на сервере).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct SdState {
    #[serde(default)]
    pub nodes: Vec<SdNode>,
    #[serde(default)]
    pub edges: Vec<SdEdge>,
}

impl SdState {
    /// Подставляет название вида компонентам без названия.
    pub fn normalize(&mut self) {
        for n in &mut self.nodes {
            if n.name.is_empty() {
                n.name = n.kind.label().to_owned();
            }
        }
    }

    /// Компонент по id (первый).
    pub fn node(&self, id: &str) -> Option<&SdNode> {
        self.nodes.iter().find(|n| n.id == id)
    }

    /// Компоненты данного вида.
    pub fn of_kind(&self, kind: Kind) -> impl Iterator<Item = &SdNode> {
        self.nodes.iter().filter(move |n| n.kind == kind)
    }
}

/* ---------- нагрузка ---------- */

/// Доля запросов приложения, которая обращается к сервису-зависимости (0..1).
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
    /// Доля обращений к сервису (0, если не задана).
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

/// Нагрузка на сервис: запросы в секунду по классам и данные.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct Workload {
    /// статика (картинки, скрипты), запр/с: CDN или blob; иначе её отдаёт приложение
    #[serde(alias = "static")]
    pub static_rps: f64,
    /// динамические чтения, запр/с
    #[serde(alias = "read")]
    pub read_rps: f64,
    /// записи, запр/с
    #[serde(alias = "write")]
    pub write_rps: f64,
    /// доля чтений, которые на самом деле поиск (идут в search; без него — тяжёлый запрос в БД)
    #[serde(default, alias = "searchShare", skip_serializing_if = "Option::is_none")]
    pub search_share: Option<f64>,
    /// объём данных, ГБ
    #[serde(alias = "dataGB")]
    pub data_gb: f64,
    /// доля данных, которую читают часто (рабочий набор), 0..1
    #[serde(alias = "hotSet")]
    pub hot_set: f64,
    /// доля запросов на самый «горячий» ключ (0..1): перекос шардов
    #[serde(default, alias = "hotKey", skip_serializing_if = "Option::is_none")]
    pub hot_key: Option<f64>,
    /// одновременных соединений WebSocket
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub connections: Option<f64>,
    /// сообщений в секунду на соединение
    #[serde(default, alias = "msgPerConn", skip_serializing_if = "Option::is_none")]
    pub msg_per_conn: Option<f64>,
    /// длительность пика для расчёта отставания очереди, секунд
    #[serde(default, alias = "spikeSec", skip_serializing_if = "Option::is_none")]
    pub spike_sec: Option<f64>,
    /// ключи шардирования растут монотонно: при range-шардировании все записи уходят в один шард
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub monotonic: Option<bool>,
    /// среднее число подписчиков автора (лента)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fanout: Option<f64>,
    /// доли запросов приложения к сервисам-зависимостям; без связи с сервисом такие запросы не выполняются
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub calls: Option<Calls>,
    /// обновления геопозиций в секунду (такси, курьеры)
    #[serde(default, alias = "geoUpdates", skip_serializing_if = "Option::is_none")]
    pub geo_updates: Option<f64>,
    /// объём файлов в объектном хранилище, ТБ
    #[serde(default, alias = "mediaTB", skip_serializing_if = "Option::is_none")]
    pub media_tb: Option<f64>,
}

impl Workload {
    /// Нагрузка из трёх основных чисел; остальное — по умолчанию (данные 10 ГБ, рабочий набор 20%).
    pub fn new(static_rps: f64, read_rps: f64, write_rps: f64) -> Workload {
        Workload { static_rps, read_rps, write_rps, data_gb: 10.0, hot_set: 0.2, ..Workload::default() }
    }

    pub(crate) fn calls_of(&self, k: DepKind) -> f64 {
        self.calls.map_or(0.0, |c| c.get(k))
    }
}

/* ---------- результат расчёта ---------- */

/// Опции расчёта: что сломать.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct EvalOptions {
    /// сломать по одному экземпляру каждого компонента этого вида (или всю зону, регион, выкладку)
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fail: Option<FailKind>,
    /// отключённые вручную узлы (клик по узлу в интерфейсе)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub down: Vec<String>,
}

impl EvalOptions {
    /// Только отказ.
    pub fn fail(f: FailKind) -> EvalOptions {
        EvalOptions { fail: Some(f), down: Vec::new() }
    }
}

/// Состояние узла по загрузке.
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

/// Допускает `null` вместо нечислового значения (JSON не умеет NaN и бесконечность).
fn lenient_f64<'de, D: Deserializer<'de>>(d: D) -> Result<f64, D::Error> {
    Ok(Option::<f64>::deserialize(d)?.unwrap_or(f64::NAN))
}

/// Нагрузка на узел.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NodeLoad {
    /// входящая нагрузка, усл. запросов в секунду
    #[serde(deserialize_with = "lenient_f64")]
    pub load: f64,
    /// ёмкость (то, что узел вытягивает), усл. запросов в секунду
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

/// Нагрузки узлов в порядке узлов схемы (без пользователей); в JSON — объект `{id: нагрузка}`.
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
                f.write_str("объект «id узла → нагрузка»")
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

/// Результат расчёта схемы под нагрузкой (в TypeScript — `Result`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EvalResult {
    pub loads: Loads,
    /// средняя и «хвостовая» задержка пользовательского запроса, мс
    #[serde(deserialize_with = "lenient_f64")]
    pub p50: f64,
    #[serde(deserialize_with = "lenient_f64")]
    pub p99: f64,
    /// доля успешных запросов, 0..1 (с учётом перегрузок)
    #[serde(deserialize_with = "lenient_f64")]
    pub success: f64,
    /// доступность схемы по компонентам, 0..1
    #[serde(deserialize_with = "lenient_f64")]
    pub availability: f64,
    /// стоимость, $ в месяц
    #[serde(deserialize_with = "lenient_f64")]
    pub cost: f64,
    /// доля чтений из кэша (`None` — кэша нет)
    pub hit: Option<f64>,
    #[serde(alias = "cdnHit")]
    pub cdn_hit: Option<f64>,
    /// отставание очереди после пика, секунд (`None` — очереди нет; 999 — не разбирается)
    #[serde(alias = "lagSec")]
    pub lag_sec: Option<f64>,
    /// отставание реплик, мс
    #[serde(alias = "replicaLagMs")]
    pub replica_lag_ms: Option<f64>,
    /// максимальная доля данных на одном шарде, 0..1
    #[serde(alias = "maxShardShare")]
    pub max_shard_share: Option<f64>,
    /// есть ли путь от пользователей до обработки запросов
    pub entry: bool,
    /// предупреждения: лишние связи, неподключённые компоненты…
    pub warnings: Vec<String>,
}

/* ---------- цели и упражнения ---------- */

/// Сравнение значения параметра.
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
    /// Запись оператора, как в тексте цели.
    pub const fn as_str(self) -> &'static str {
        match self {
            Op::Ge => ">=",
            Op::Le => "<=",
            Op::Eq => "==",
            Op::Ne => "!=",
        }
    }
}

/// Цель упражнения. В данных — объект с полем `type` (`{"type": "p99", "max": 150}`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Goal {
    /// ни один компонент не загружен больше чем на `max` (0..1)
    Capacity { max: f64 },
    /// компонент этого вида загружен не больше чем на `max`
    Util { kind: Kind, max: f64 },
    P99 { max: f64 },
    P50 { max: f64 },
    Success { min: f64 },
    Availability { min: f64 },
    Cost { max: f64 },
    /// в схеме есть компонент (не меньше `min` штук, по умолчанию 1)
    Has {
        kind: Kind,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        min: Option<f64>,
    },
    Lacks { kind: Kind },
    /// есть связь от компонента вида `from` к компоненту вида `to`
    Link { from: Kind, to: Kind },
    Hit { min: f64 },
    #[serde(alias = "cdnHit")]
    CdnHit { min: f64 },
    /// после отказа успешно не меньше 99% запросов
    Survive { fail: FailKind },
    /// параметр всех компонентов вида соответствует условию
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
    /// нет единой точки отказа среди компонентов этих видов
    #[serde(alias = "noSpof")]
    NoSpof { kinds: Vec<Kind> },
}

fn de_param_key<'de, D: Deserializer<'de>>(d: D) -> Result<String, D::Error> {
    let s = String::deserialize(d)?;
    Ok(kinds::canonical_param_key(&s).to_owned())
}

/// Результат проверки одной цели.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GoalResult {
    pub ok: bool,
    /// условие словами
    pub text: String,
    /// «сейчас …» — что получилось
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

/// Содержимое упражнения без текста: нагрузка, палитра, исходная схема, цели и эталон.
/// `solution` бэкенд не отдаёт клиенту.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    pub workload: Workload,
    /// какие компоненты можно добавлять с панели
    pub palette: Vec<Kind>,
    /// исходная схема
    pub start: SdState,
    pub goals: Vec<Goal>,
    /// эталонная схема (проверяется самопроверкой и тестами)
    pub solution: SdState,
    /// сколько узлов можно держать на схеме (по умолчанию 14)
    #[serde(default, alias = "maxNodes", skip_serializing_if = "Option::is_none")]
    pub max_nodes: Option<usize>,
    /// какие дополнительные параметры показывать: `"app.retries"` и т. п.
    #[serde(default, deserialize_with = "de_show", skip_serializing_if = "no_show")]
    pub show: Vec<String>,
}

impl Scenario {
    /// Предел числа узлов на схеме.
    pub fn max_nodes(&self) -> usize {
        self.max_nodes.unwrap_or_else(default_max_nodes)
    }

    /// Показывать ли параметр в панели компонента: основные — всегда, дополнительные — если перечислены в `show`.
    pub fn param_visible(&self, kind: Kind, p: &kinds::ParamSpec) -> bool {
        p.basic || self.show.iter().any(|s| s.split_once('.').is_some_and(|(k, key)| k == kind.as_str() && key == p.key))
    }

    /// Копия для клиента: без эталонного решения.
    pub fn without_solution(&self) -> Scenario {
        Scenario { solution: SdState::default(), ..self.clone() }
    }
}

/// Упражнение: текст и содержимое.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    /// условие (абзац)
    pub statement: String,
    pub hint: String,
    pub spec: Scenario,
}

/// Файл данных главы: `backend/data/labs/sd/<книга>-<глава:02>.json`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// вид лаборатории (`"sd"`)
    pub lab: String,
    pub tasks: Vec<Task>,
}
