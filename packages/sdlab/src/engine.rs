//! Расчёт схемы под нагрузкой. Запросы трёх классов — статика, чтение, запись — проходят по схеме по
//! «деревьям решений» (кэш: попал/промахнулся, очередь: запись уходит в буфер, CDN: отдаёт статику).
//! Для каждого пути известны вероятность и список узлов. Из путей считаются нагрузка узлов, затем
//! задержка, доля успешных ответов и доступность. Всё — формулы, без случайности.
//!
//! Это точный порт `engine.ts`: те же формулы и порядок операций над `f64`, поэтому результаты совпадают с
//! прежней версией (проверяется дифференциальными тестами на «золотых» результатах TypeScript).
//! Единственное расхождение — схема с циклом: лишняя связь, замыкающая цикл, отбрасывается с предупреждением
//! (в TypeScript такая схема уходила в бесконечную рекурсию; интерфейс циклы не допускает).

use std::collections::{HashMap, HashSet};

use crate::jsfmt;
use crate::reference as r;
use crate::reference::Size;
use crate::types::{DepKind, EvalOptions, EvalResult, FailKind, Kind, Loads, NodeLoad, NodeStatus, SdNode, SdState, Workload};

/// Сервисы-зависимости в порядке обхода.
pub const DEPS: [DepKind; 4] = DepKind::ALL;

/// Допустима ли связь `a → b` в этой модели.
pub fn can_link(a: Kind, b: Kind) -> bool {
    use Kind::*;
    match a {
        Clients => matches!(b, Cdn | Limiter | Gateway | Lb | Ws | App),
        Cdn => matches!(b, Limiter | Gateway | Lb | App | Blob),
        Limiter => matches!(b, Gateway | Lb | App | Ws),
        Gateway => matches!(b, Limiter | Lb | App | Ws),
        Lb => matches!(b, Limiter | Gateway | Lb | App | Ws),
        Ws => matches!(b, App | Queue | Stream),
        App => matches!(b, Cache | Db | Queue | Blob | Search | Stream | Auth | Geo | Ml | Pay),
        Queue => matches!(b, Worker | Notify),
        Stream => matches!(b, Worker | Notify | Analytics),
        Worker => matches!(b, Db | Blob | Search),
        Auth | Geo | Ml | Pay | Notify | Analytics | Cache | Db | Blob | Search | Monitor => false,
    }
}

/// Сколько экземпляров заявлено на схеме.
pub fn base_units(n: &SdNode) -> f64 {
    match n.kind {
        Kind::App | Kind::Lb | Kind::Gateway | Kind::Worker | Kind::Ws | Kind::Auth | Kind::Geo | Kind::Ml | Kind::Pay | Kind::Notify | Kind::Analytics => {
            n.num("instances")
        }
        Kind::Db => n.num("shards"),
        Kind::Search => n.num("replicas"),
        _ => 1.0,
    }
}

/// Сколько экземпляров работает при заданных отказах.
fn working_units(n: &SdNode, opts: &EvalOptions) -> f64 {
    if opts.down.contains(&n.id) {
        return 0.0;
    }
    let base = base_units(n);
    let Some(f) = opts.fail else { return base };
    let zone_aware = matches!(n.kind, Kind::App | Kind::Cache | Kind::Worker | Kind::Db);
    match f {
        FailKind::Zone | FailKind::Region => {
            if !zone_aware {
                return base;
            }
            let z = n.text("zone");
            let spare = match n.kind {
                Kind::Db => n.num("replicas") > 0.0 && n.flag("failover"),
                Kind::Cache => n.num("replicas") > 0.0,
                _ => false,
            };
            if f == FailKind::Zone && z != "single" {
                return if spare { base.max(1.0) } else { (base - (base / 3.0).ceil()).max(0.0) };
            }
            if f == FailKind::Region && z == "regions" {
                return if spare { base.max(1.0) } else { (base - (base / 2.0).ceil()).max(0.0) };
            }
            0.0
        }
        FailKind::Deploy => {
            if n.kind != Kind::App {
                return base;
            }
            match n.text("deploy").as_ref() {
                "all" => 0.0,
                "rolling" => (base - 1.0).max(0.0),
                _ => base,
            }
        }
        FailKind::Component(k) => {
            if k != n.kind {
                return base;
            }
            match n.kind {
                Kind::App
                | Kind::Lb
                | Kind::Gateway
                | Kind::Worker
                | Kind::Ws
                | Kind::Search
                | Kind::Auth
                | Kind::Geo
                | Kind::Ml
                | Kind::Pay
                | Kind::Notify
                | Kind::Analytics => (base - 1.0).max(0.0),
                Kind::Cache => {
                    if n.num("replicas") > 0.0 {
                        1.0
                    } else {
                        0.0
                    }
                }
                Kind::Db => {
                    if n.num("replicas") > 0.0 && n.flag("failover") {
                        base
                    } else {
                        0.0
                    }
                }
                Kind::Queue | Kind::Stream if n.num("partitions") >= 3.0 => 1.0,
                _ => 0.0,
            }
        }
    }
}

/* ---------- кэш и CDN ---------- */

/// Доля попаданий CDN по TTL.
pub fn cdn_hit(n: &SdNode) -> f64 {
    let ttl = n.num("ttl");
    if ttl <= 30.0 {
        0.55
    } else if ttl <= 300.0 {
        0.9
    } else {
        0.98
    }
}

/// Доля попаданий кэша: размер относительно рабочего набора, TTL и доля записей.
pub fn cache_hit(n: &SdNode, wl: &Workload) -> f64 {
    let reads = wl.read_rps;
    if reads <= 0.0 {
        return 0.0;
    }
    let hot_gb = (wl.data_gb * wl.hot_set).max(0.1);
    let coverage = (n.num("size_gb") / hot_gb).min(1.0);
    let ttl = n.num("ttl");
    let ttl_mul = if ttl <= 30.0 {
        0.75
    } else if ttl <= 300.0 {
        0.95
    } else {
        1.0
    };
    let write_frac = wl.write_rps / (wl.read_rps + wl.write_rps).max(1.0);
    let h = 0.95 * coverage.sqrt() * ttl_mul * (1.0 - 0.4 * write_frac);
    jsfmt::round(h * 1000.0) / 1000.0
}

/* ---------- ёмкость и цена ---------- */

fn node_size(n: &SdNode) -> Size {
    Size::parse(&n.text("size"))
}

/// Цена компонента, $ в месяц.
fn node_cost(n: &SdNode, wl: &Workload) -> f64 {
    match n.kind {
        Kind::App => {
            r::APP_COST.get(node_size(n)) * n.num("instances") * r::price_factor(&n.text("pricing")) * if n.text("deploy") == "bluegreen" { 2.0 } else { 1.0 }
        }
        Kind::Lb => r::LB.cost * n.num("instances"),
        Kind::Gateway => r::GATEWAY.cost * n.num("instances"),
        Kind::Limiter => r::LIMITER.cost,
        Kind::Cdn => r::CDN.cost,
        Kind::Cache => r::CACHE_COST_PER_GB * n.num("size_gb") * (1.0 + n.num("replicas")),
        Kind::Db => r::DB_COST.get(node_size(n)) * n.num("shards") * (1.0 + n.num("replicas")),
        Kind::Queue => r::QUEUE_COST + r::QUEUE_COST_PER_PARTITION * n.num("partitions"),
        Kind::Worker => r::WORKER_COST.get(node_size(n)) * n.num("instances") * r::price_factor(&n.text("pricing")),
        Kind::Blob => {
            let tier = r::blob_tier(&n.text("tier")).map_or(23.0, |t| t.price);
            r::BLOB.cost + wl.media_tb.unwrap_or(0.0) * tier
        }
        Kind::Auth => r::AUTH.cost * n.num("instances"),
        Kind::Geo => r::GEO.cost * n.num("instances"),
        Kind::Ml => r::ML.cost * n.num("instances"),
        Kind::Pay => r::PAY.cost * n.num("instances"),
        Kind::Notify => r::NOTIFY.cost * n.num("instances"),
        Kind::Analytics => r::ANALYTICS.cost * n.num("instances"),
        Kind::Stream => r::STREAM_COST + r::STREAM_COST_PER_PARTITION * n.num("partitions"),
        Kind::Search => r::SEARCH_COST * n.num("shards") * n.num("replicas"),
        Kind::Ws => r::WS.cost * n.num("instances"),
        Kind::Monitor => r::MONITOR_COST,
        Kind::Clients => 0.0,
    }
}

/// Доступность узла: n экземпляров дают `1 − (1 − a)ⁿ`.
fn tier_avail(n: &SdNode) -> f64 {
    let redundant = |a: f64, k: f64| 1.0 - (1.0 - a).powf(k.max(1.0));
    match n.kind {
        Kind::App => redundant(if n.text("pricing") == "spot" { 0.95 } else { r::APP_AVAIL }, n.num("instances")),
        Kind::Lb => redundant(r::LB.avail, n.num("instances")),
        Kind::Gateway => redundant(r::GATEWAY.avail, n.num("instances")),
        Kind::Ws => redundant(r::WS.avail, n.num("instances")),
        Kind::Limiter => r::LIMITER.avail,
        Kind::Db => {
            if n.flag("failover") && n.num("replicas") > 0.0 {
                redundant(r::DB_AVAIL, 1.0 + n.num("replicas"))
            } else {
                r::DB_AVAIL
            }
        }
        Kind::Queue => {
            if n.num("partitions") >= 3.0 {
                0.99999
            } else {
                r::QUEUE_AVAIL
            }
        }
        Kind::Blob => r::BLOB.avail,
        Kind::Auth => redundant(r::AUTH.avail, n.num("instances")),
        Kind::Geo => redundant(r::GEO.avail, n.num("instances")),
        Kind::Ml => redundant(r::ML.avail, n.num("instances")),
        Kind::Pay => redundant(r::PAY.avail, n.num("instances")),
        Kind::Stream => {
            if n.num("partitions") >= 3.0 {
                0.99999
            } else {
                r::STREAM_AVAIL
            }
        }
        Kind::Search => redundant(r::SEARCH_AVAIL, n.num("replicas")),
        _ => 1.0,
    }
}

/* ---------- расчёт ---------- */

#[derive(Clone, Copy, PartialEq, Eq)]
enum Cls {
    Static,
    Read,
    Write,
}

struct Path {
    p: f64,
    cls: Cls,
    nodes: Vec<usize>,
    ok: bool,
    /// отброшено ограничителем: для доступности схема исправна
    rej: bool,
}

#[derive(Clone, Default)]
#[allow(dead_code)]
struct Acc {
    rps: f64,
    heavy: f64,
    writes: f64,
    conn: f64,
    msgs: f64,
    /// запросы, обработанные приложением как статика
    static_self: f64,
    /// то, что пришло в очередь
    queued: f64,
    /// асинхронная запись в БД из обработчиков
    async_writes: f64,
    reads: f64,
    /// дополнительные чтения из-за ленты pull/гибрид
    extra: f64,
}

struct RunState {
    acc: Vec<Acc>,
    paths: Vec<Path>,
}

/// Параметры одного прохода: пропуск ограничителей, скорость разбора очереди, повторы к базе.
struct RunIn<'a> {
    pass_limiter: &'a HashMap<usize, f64>,
    drain: f64,
    retry_mul: &'a HashMap<usize, f64>,
}

const WEB: [Kind; 4] = [Kind::Limiter, Kind::Gateway, Kind::Lb, Kind::App];

struct Model<'a> {
    nodes: &'a [SdNode],
    wl: &'a Workload,
    /// исходящие связи по индексу узла (только допустимые и не замыкающие цикл)
    out: Vec<Vec<usize>>,
    units: Vec<f64>,
    entries: Vec<usize>,
    clients: Option<usize>,
}

fn with(seq: &[usize], n: usize) -> Vec<usize> {
    let mut v = Vec::with_capacity(seq.len() + 1);
    v.extend_from_slice(seq);
    v.push(n);
    v
}

impl Model<'_> {
    fn kind(&self, i: usize) -> Kind {
        self.nodes[i].kind
    }

    fn kids(&self, i: usize, kinds: &[Kind]) -> Vec<usize> {
        self.out[i].iter().copied().filter(|&k| kinds.contains(&self.kind(k))).collect()
    }

    fn has_cache(&self, app: usize) -> Option<usize> {
        self.kids(app, &[Kind::Cache]).into_iter().find(|&c| self.units[c] > 0.0)
    }

    /// Деление потока между узлами: живые поровну (или по весу приложений).
    fn split(&self, list: &[usize]) -> Vec<(usize, f64)> {
        let live: Vec<usize> = list.iter().copied().filter(|&i| self.units[i] > 0.0 || self.kind(i) == Kind::Limiter).collect();
        let pool: &[usize] = if live.is_empty() { list } else { &live };
        let w = |i: usize| if self.kind(i) == Kind::App { self.nodes[i].num("weight").max(1.0) } else { self.units[i].max(1.0) };
        let mut total = 0.0;
        for &i in pool {
            total += w(i);
        }
        if total == 0.0 || total.is_nan() {
            total = 1.0;
        }
        pool.iter().map(|&i| (i, w(i) / total)).collect()
    }

    fn feed_read(&self, app: usize) -> f64 {
        let fo = self.wl.fanout.unwrap_or(0.0);
        match self.nodes[app].text("feed").as_ref() {
            "pull" => 1.0 + fo / 20.0,
            "hybrid" => 1.0 + fo / 100.0,
            _ => 1.0,
        }
    }

    fn feed_write(&self, app: usize) -> f64 {
        let fo = self.wl.fanout.unwrap_or(0.0);
        if fo <= 0.0 {
            return 1.0;
        }
        match self.nodes[app].text("feed").as_ref() {
            "push" => fo,
            "hybrid" => 1.0 + fo / 100.0,
            _ => 1.0,
        }
    }

    /// Нагрузка потребителям очереди или потока: уведомления и аналитика получают копию.
    fn fan_consumers(&self, st: &mut RunState, queue: usize, rate: f64) {
        for k in [Kind::Notify, Kind::Analytics] {
            for (c, share) in self.split(&self.kids(queue, &[k])) {
                st.acc[c].rps += rate * share;
            }
        }
    }

    fn is_write_back(&self, seq: &[usize]) -> bool {
        seq.iter().any(|&i| self.kind(i) == Kind::Cache && self.nodes[i].text("policy") == "back")
    }

    #[allow(clippy::too_many_arguments)]
    fn forward(&self, st: &mut RunState, inp: &RunIn, list: &[usize], cls: Cls, prob: f64, rate: f64, seq: &[usize]) {
        if list.is_empty() {
            st.paths.push(Path { p: prob, cls, nodes: seq.to_vec(), ok: false, rej: false });
            return;
        }
        for (n, share) in self.split(list) {
            self.walk(st, inp, n, cls, prob * share, rate, seq);
        }
    }

    /// Продолжение пути от узла для класса `cls`; `seq` — уже пройденные узлы.
    #[allow(clippy::too_many_arguments)]
    fn walk(&self, st: &mut RunState, inp: &RunIn, n: usize, cls: Cls, prob: f64, rate: f64, seq: &[usize]) {
        if prob <= 1e-9 {
            return;
        }
        let here = with(seq, n);
        let rr = prob * rate;
        let node = &self.nodes[n];
        match node.kind {
            Kind::Cdn => {
                st.acc[n].rps += rr;
                if cls == Cls::Static {
                    let h = if self.units[n] > 0.0 { cdn_hit(node) } else { 0.0 };
                    st.paths.push(Path { p: prob * h, cls, nodes: here.clone(), ok: true, rej: false });
                    let miss = prob * (1.0 - h);
                    let blobs = self.kids(n, &[Kind::Blob]);
                    let webs = self.kids(n, &WEB);
                    if let Some(&b) = blobs.first() {
                        self.walk(st, inp, b, cls, miss, rate, &here);
                    } else {
                        self.forward(st, inp, &webs, cls, miss, rate, &here);
                    }
                } else {
                    self.forward(st, inp, &self.kids(n, &WEB), cls, prob, rate, &here);
                }
            }
            Kind::Limiter => {
                st.acc[n].rps += rr;
                let pass = inp.pass_limiter.get(&n).copied().unwrap_or(1.0);
                st.paths.push(Path { p: prob * (1.0 - pass), cls, nodes: here.clone(), ok: false, rej: true });
                self.forward(st, inp, &self.kids(n, &[Kind::Gateway, Kind::Lb, Kind::App, Kind::Limiter]), cls, prob * pass, rate, &here);
            }
            Kind::Gateway | Kind::Lb => {
                st.acc[n].rps += rr;
                self.forward(st, inp, &self.kids(n, &[Kind::Limiter, Kind::Gateway, Kind::Lb, Kind::App]), cls, prob, rate, &here);
            }
            Kind::App => self.walk_app(st, inp, n, cls, prob, rate, &here),
            Kind::Db => {
                st.acc[n].rps += rr;
                let mul = inp.retry_mul.get(&n).copied().unwrap_or(1.0);
                if cls == Cls::Write {
                    st.acc[n].writes += rr * mul * if self.is_write_back(seq) { r::WRITE_BACK } else { 1.0 };
                } else {
                    st.acc[n].reads += rr * mul;
                }
                st.paths.push(Path { p: prob, cls, nodes: here, ok: true, rej: false });
            }
            Kind::Search | Kind::Blob => {
                st.acc[n].rps += rr;
                st.paths.push(Path { p: prob, cls, nodes: here, ok: true, rej: false });
            }
            _ => st.paths.push(Path { p: prob, cls, nodes: here, ok: false, rej: false }),
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn walk_app(&self, st: &mut RunState, inp: &RunIn, n: usize, cls: Cls, prob: f64, rate: f64, here: &[usize]) {
        let rr = prob * rate;
        let wl = self.wl;
        if cls == Cls::Static {
            let blobs = self.kids(n, &[Kind::Blob]);
            if let Some(&b) = blobs.first() {
                self.walk(st, inp, b, cls, prob, rate, here);
            } else {
                st.acc[n].rps += rr * r::STATIC_WEIGHT;
                st.acc[n].static_self += rr;
                st.paths.push(Path { p: prob, cls, nodes: here.to_vec(), ok: true, rej: false });
            }
            return;
        }
        st.acc[n].rps += rr;
        for k in DEPS {
            let f = wl.calls_of(k).clamp(0.0, 1.0);
            if f > 0.0 {
                for (d, share) in self.split(&self.kids(n, &[k.kind()])) {
                    st.acc[d].rps += rr * f * share;
                }
            }
        }
        let db = self.kids(n, &[Kind::Db]).first().copied();
        if cls == Cls::Read {
            st.acc[n].reads += rr;
            let s = wl.search_share.unwrap_or(0.0).clamp(0.0, 1.0);
            let searches = self.kids(n, &[Kind::Search]);
            if s > 0.0 {
                if let Some(&sr) = searches.first() {
                    self.walk(st, inp, sr, Cls::Read, prob * s, rate, here);
                } else if let Some(d) = db {
                    st.acc[d].heavy += rr * s;
                    self.walk(st, inp, d, Cls::Read, prob * s, rate, here);
                } else {
                    st.paths.push(Path { p: prob * s, cls, nodes: here.to_vec(), ok: false, rej: false });
                }
            }
            let plain = prob * (1.0 - s);
            if let Some(cache) = self.has_cache(n) {
                let h = cache_hit(&self.nodes[cache], wl);
                st.acc[cache].rps += plain * rate;
                st.acc[cache].reads += plain * rate;
                let via = with(here, cache);
                st.paths.push(Path { p: plain * h, cls, nodes: via.clone(), ok: true, rej: false });
                if let Some(d) = db {
                    st.acc[d].extra += plain * (1.0 - h) * rate * (self.feed_read(n) - 1.0);
                    self.walk(st, inp, d, Cls::Read, plain * (1.0 - h), rate, &via);
                } else {
                    st.paths.push(Path { p: plain * (1.0 - h), cls, nodes: via, ok: false, rej: false });
                }
            } else if let Some(d) = db {
                st.acc[d].extra += plain * rate * (self.feed_read(n) - 1.0);
                self.walk(st, inp, d, Cls::Read, plain, rate, here);
            } else {
                st.paths.push(Path { p: plain, cls, nodes: here.to_vec(), ok: false, rej: false });
            }
            return;
        }
        // запись
        let queue = self.kids(n, &[Kind::Queue]).first().copied();
        let stream = self.kids(n, &[Kind::Stream]).first().copied();
        let cache = self.has_cache(n);
        if let Some(c) = cache {
            st.acc[c].rps += rr * 0.5;
            st.acc[c].writes += rr;
        }
        // поток событий — побочная копия записи: потребители получают событие, путь запроса не меняется
        if let Some(sm) = stream {
            st.acc[sm].queued += rr;
            st.acc[sm].rps += rr;
            self.fan_consumers(st, sm, rr);
        }
        if let Some(q) = queue {
            st.acc[q].queued += rr;
            st.acc[q].rps += rr;
            st.paths.push(Path { p: prob, cls, nodes: with(here, q), ok: true, rej: false });
            // асинхронное продолжение: обработчики → БД (по схеме, только нагрузка)
            self.fan_consumers(st, q, rr);
            let workers = self.kids(q, &[Kind::Worker]);
            let amp = self.feed_write(n);
            for (w, share) in self.split(&workers) {
                st.acc[w].async_writes += rr * share * amp;
                for d in self.kids(w, &[Kind::Db]) {
                    st.acc[d].writes += rr * share * inp.drain * amp;
                    st.acc[d].async_writes += rr * share * inp.drain * amp;
                }
            }
        } else if let Some(d) = db {
            st.acc[d].writes += rr * (self.feed_write(n) - 1.0);
            let seq = match cache {
                Some(c) => with(here, c),
                None => here.to_vec(),
            };
            self.walk(st, inp, d, Cls::Write, prob, rate, &seq);
        } else if let Some(sm) = stream {
            st.paths.push(Path { p: prob, cls, nodes: with(here, sm), ok: true, rej: false });
        } else {
            st.paths.push(Path { p: prob, cls, nodes: here.to_vec(), ok: false, rej: false });
        }
    }

    fn run(&self, inp: &RunIn) -> RunState {
        let mut st = RunState { acc: vec![Acc::default(); self.nodes.len()], paths: Vec::new() };
        let wl = self.wl;
        let cdns: Vec<usize> = self.entries.iter().copied().filter(|&i| self.kind(i) == Kind::Cdn).collect();
        let entry_web: Vec<usize> = self.entries.iter().copied().filter(|&i| WEB.contains(&self.kind(i))).collect();
        let root: Vec<usize> = self.clients.into_iter().collect();
        for (cls, rate) in [(Cls::Static, wl.static_rps), (Cls::Read, wl.read_rps), (Cls::Write, wl.write_rps)] {
            if rate <= 0.0 {
                continue;
            }
            if !cdns.is_empty() && cls == Cls::Static {
                self.forward(&mut st, inp, &cdns, cls, 1.0, rate, &root);
            } else if !entry_web.is_empty() {
                self.forward(&mut st, inp, &entry_web, cls, 1.0, rate, &root);
            } else if !cdns.is_empty() {
                self.forward(&mut st, inp, &cdns, cls, 1.0, rate, &root);
            } else {
                st.paths.push(Path { p: 1.0, cls, nodes: root.clone(), ok: false, rej: false });
            }
        }

        // соединения WebSocket и сообщения
        let ws_entries: Vec<usize> = self.entries.iter().copied().filter(|&i| self.kind(i) == Kind::Ws).collect();
        let mut ws_all = ws_entries;
        for &e in &self.entries {
            if matches!(self.kind(e), Kind::Lb | Kind::Gateway | Kind::Limiter) {
                for w in self.kids(e, &[Kind::Ws]) {
                    if !ws_all.contains(&w) {
                        ws_all.push(w);
                    }
                }
            }
        }
        let conns = wl.connections.unwrap_or(0.0);
        if conns > 0.0 && !ws_all.is_empty() {
            for (w, share) in self.split(&ws_all) {
                st.acc[w].conn += conns * share;
                let msgs = conns * wl.msg_per_conn.unwrap_or(0.0) * share;
                st.acc[w].msgs += msgs;
                let targets = self.kids(w, &[Kind::App]);
                for (app, s2) in self.split(&targets) {
                    st.acc[app].rps += msgs * s2;
                    let queue = self.kids(app, &[Kind::Queue, Kind::Stream]).first().copied();
                    let db = self.kids(app, &[Kind::Db]).first().copied();
                    if let Some(q) = queue {
                        st.acc[q].queued += msgs * s2;
                        self.fan_consumers(&mut st, q, msgs * s2);
                    } else if let Some(d) = db {
                        st.acc[d].writes += msgs * s2;
                        st.acc[d].rps += msgs * s2;
                    }
                }
            }
        }
        // обновления геопозиций идут прямо в сервисы геопоиска, подключённые к приложению
        let geo_updates = wl.geo_updates.unwrap_or(0.0);
        if geo_updates > 0.0 {
            let geos: Vec<usize> = (0..self.nodes.len())
                .filter(|&g| self.kind(g) == Kind::Geo && (0..self.nodes.len()).any(|a| self.kind(a) == Kind::App && self.out[a].contains(&g)))
                .collect();
            for (g, share) in self.split(&geos) {
                st.acc[g].rps += geo_updates * share;
            }
        }
        st
    }
}

/// Строит исходящие связи: только допустимые по видам и не замыкающие цикл.
fn build_links(state: &SdState, warnings: &mut Vec<String>) -> Vec<Vec<usize>> {
    let mut idx: HashMap<&str, usize> = HashMap::new();
    for (i, n) in state.nodes.iter().enumerate() {
        idx.insert(n.id.as_str(), i);
    }
    let mut out: Vec<Vec<usize>> = vec![Vec::new(); state.nodes.len()];
    for e in &state.edges {
        let (Some(&a), Some(&b)) = (idx.get(e.from.as_str()), idx.get(e.to.as_str())) else { continue };
        let (na, nb) = (&state.nodes[a], &state.nodes[b]);
        if !can_link(na.kind, nb.kind) {
            warnings.push(format!("связь «{} → {}» не работает: такие компоненты не соединяются", na.name, nb.name));
            continue;
        }
        if reaches(&out, b, a) {
            warnings.push(format!("связь «{} → {}» замыкает цикл и не учитывается", na.name, nb.name));
            continue;
        }
        out[a].push(b);
    }
    out
}

fn reaches(out: &[Vec<usize>], from: usize, to: usize) -> bool {
    let mut seen = vec![false; out.len()];
    let mut stack = vec![from];
    while let Some(cur) = stack.pop() {
        if cur == to {
            return true;
        }
        if std::mem::replace(&mut seen[cur], true) {
            continue;
        }
        stack.extend(out[cur].iter().copied());
    }
    false
}

/// Расчёт схемы под нагрузкой: загрузка узлов, задержки p50/p99, доля успешных запросов, доступность, стоимость.
pub fn evaluate(state: &SdState, wl: &Workload, opts: &EvalOptions) -> EvalResult {
    let nodes = &state.nodes;
    let mut warnings: Vec<String> = Vec::new();
    let out = build_links(state, &mut warnings);
    let units: Vec<f64> = nodes.iter().map(|n| working_units(n, opts)).collect();
    let clients = nodes.iter().position(|n| n.kind == Kind::Clients);
    let entries = clients.map(|c| out[c].clone()).unwrap_or_default();
    let m = Model { nodes, wl, out, units, entries, clients };
    let size_of = |i: usize| node_size(&nodes[i]);

    /* --- первая итерация: ёмкость узлов, пропуск ограничителей и скорость разбора очереди --- */
    let mut pass_limiter: HashMap<usize, f64> = HashMap::new();
    let mut drain = 1.0;
    let mut retry_mul: HashMap<usize, f64> = HashMap::new();
    let mut r1 = m.run(&RunIn { pass_limiter: &pass_limiter, drain, retry_mul: &retry_mul });
    for (i, l) in nodes.iter().enumerate() {
        if l.kind != Kind::Limiter {
            continue;
        }
        let total = r1.acc[i].rps;
        let lim = l.num("limit");
        pass_limiter.insert(i, if total > 0.0 { (lim / total).min(1.0) } else { 1.0 });
    }
    let worker_cap = |i: usize| m.units[i] * r::WORKER_CAP.get(size_of(i));
    let mut async_total = 0.0;
    let mut drain_cap = 0.0;
    for (i, n) in nodes.iter().enumerate() {
        if n.kind == Kind::Worker {
            async_total += r1.acc[i].async_writes;
            drain_cap += worker_cap(i);
        }
    }
    if async_total > 0.0 {
        drain = (drain_cap / async_total).min(1.0);
    }
    r1 = m.run(&RunIn { pass_limiter: &pass_limiter, drain, retry_mul: &retry_mul });

    /* повторы: если база перегружена, каждая неудача возвращается ещё r раз — нагрузка растёт (если нет автомата разрыва) */
    let dbs: Vec<usize> = (0..nodes.len()).filter(|&i| nodes[i].kind == Kind::Db).collect();
    let apps: Vec<usize> = (0..nodes.len()).filter(|&i| nodes[i].kind == Kind::App).collect();
    let retry_util = |db: usize, acc: &[Acc]| -> f64 {
        let a = &acc[db];
        let n = &nodes[db];
        let u = m.units[db];
        let shards = n.num("shards").max(1.0);
        let eng = if n.text("engine") == "nosql" { r::DB_NOSQL } else { 1.0 };
        let reps = n.num("replicas");
        let read_base = r::DB_READ.get(size_of(db)) * eng;
        let write_base = r::DB_WRITE.get(size_of(db)) * eng;
        let hot = wl.hot_key.unwrap_or(0.0).clamp(0.0, 1.0);
        let share = if shards > 1.0 { hot + (1.0 - hot) / shards } else { 1.0 };
        let rl = (a.reads + a.extra + a.heavy * (r::HEAVY_SEARCH - 1.0)) * share;
        let wlo = a.writes * share;
        if u == 0.0 {
            if rl + wlo > 0.0 {
                9.0
            } else {
                0.0
            }
        } else if reps > 0.0 {
            (rl / (read_base * reps.max(1.0))).max(wlo / write_base)
        } else {
            rl / read_base + wlo / write_base
        }
    };
    let mut retry_factor = 1.0f64;
    for &db in &dbs {
        let ut = retry_util(db, &r1.acc);
        if ut <= 1.0 {
            continue;
        }
        let f = (1.0 - 1.0 / ut).min(0.95);
        for &app in &apps {
            if !m.kids(app, &[Kind::Db]).contains(&db) {
                continue;
            }
            let retries = nodes[app].num("retries");
            if retries <= 0.0 || nodes[app].flag("breaker") {
                continue;
            }
            let mut mm = 0.0;
            let mut i = 0.0;
            while i <= retries {
                mm += f.powf(i);
                i += 1.0;
            }
            retry_factor = retry_factor.max(mm);
        }
    }
    if retry_factor > 1.0 {
        for &db in &dbs {
            retry_mul.insert(db, retry_factor);
        }
        r1 = m.run(&RunIn { pass_limiter: &pass_limiter, drain, retry_mul: &retry_mul });
    }
    let RunState { acc, paths } = r1;

    /* --- загрузка узлов --- */
    let mut loads = Loads::default();
    let mut util: Vec<f64> = vec![0.0; nodes.len()];
    let mut max_shard_share: Option<f64> = None;
    let mut replica_lag_ms: Option<f64> = None;
    let mut hit_ratio: Option<f64> = None;
    let mut cdn_hit_ratio: Option<f64> = None;

    for (i, n) in nodes.iter().enumerate() {
        let a = &acc[i];
        let u = m.units[i];
        let mut load = a.rps;
        let cap: f64;
        let mut ut: f64;
        let mut nt = String::new();
        let by_cap = |load: f64, cap: f64| if cap > 0.0 { load / cap } else if load > 0.0 { 9.0 } else { 0.0 };
        match n.kind {
            Kind::Clients => continue,
            Kind::Cdn => {
                cap = r::CDN.cap;
                ut = load / cap;
                let h = if u > 0.0 { cdn_hit(n) } else { 0.0 };
                cdn_hit_ratio = Some(h);
                nt = format!("попаданий {}%", jsfmt::pct0(h));
            }
            Kind::Limiter => {
                cap = n.num("limit");
                ut = load / cap;
                nt = if ut > 1.0 { format!("отбрасывает {}%", jsfmt::pct0(1.0 - 1.0 / ut)) } else { String::new() };
            }
            Kind::Gateway => {
                cap = r::GATEWAY.cap * u;
                ut = by_cap(load, cap);
            }
            Kind::Lb => {
                cap = r::LB.cap * u;
                ut = by_cap(load, cap);
            }
            Kind::Ws => {
                load = a.conn;
                cap = r::WS.cap * u;
                ut = by_cap(load, cap);
            }
            Kind::App => {
                cap = r::APP_CAP.get(size_of(i)) * u;
                ut = by_cap(load, cap);
                if n.num("instances") > 1.0 && n.text("sessions") == "local" {
                    nt = "сессии в памяти: при балансировке пользователи «теряют» вход".into();
                }
            }
            Kind::Cache => {
                load = a.rps;
                cap = if u > 0.0 { r::CACHE_CAP } else { 0.0 };
                ut = if cap > 0.0 { load / cap } else { 0.0 };
                let h = if u > 0.0 { cache_hit(n, wl) } else { 0.0 };
                hit_ratio = Some(h);
                nt = format!("попаданий {}%", jsfmt::pct0(h));
            }
            Kind::Queue => {
                load = a.queued;
                cap = r::QUEUE_CAP_PER_PARTITION * n.num("partitions") * if u > 0.0 { 1.0 } else { 0.0 };
                ut = by_cap(load, cap);
            }
            Kind::Auth | Kind::Geo | Kind::Ml | Kind::Pay | Kind::Notify | Kind::Analytics => {
                let b = match n.kind {
                    Kind::Auth => r::AUTH,
                    Kind::Geo => r::GEO,
                    Kind::Ml => r::ML,
                    Kind::Pay => r::PAY,
                    Kind::Notify => r::NOTIFY,
                    _ => r::ANALYTICS,
                };
                cap = b.cap * u;
                ut = by_cap(load, cap);
            }
            Kind::Stream => {
                load = a.queued;
                cap = r::STREAM_CAP_PER_PARTITION * n.num("partitions") * if u > 0.0 { 1.0 } else { 0.0 };
                ut = by_cap(load, cap);
            }
            Kind::Worker => {
                load = a.async_writes;
                cap = worker_cap(i);
                ut = by_cap(load, cap);
            }
            Kind::Blob => {
                cap = r::BLOB.cap;
                ut = load / cap;
            }
            Kind::Search => {
                let shards = n.num("shards");
                cap = r::SEARCH_CAP * u;
                ut = by_cap(load, cap);
                let per_shard = wl.data_gb / shards.max(1.0);
                if per_shard > r::SEARCH_MAX_GB_PER_SHARD {
                    ut = ut.max(per_shard / r::SEARCH_MAX_GB_PER_SHARD);
                    nt = format!("индекс {} ГБ на шард — слишком много", jsfmt::num(jsfmt::round(per_shard)));
                }
            }
            Kind::Db => {
                let shards = n.num("shards").max(1.0);
                let reps = n.num("replicas");
                let eng = if n.text("engine") == "nosql" { r::DB_NOSQL } else { 1.0 };
                let hot = wl.hot_key.unwrap_or(0.0).clamp(0.0, 1.0);
                let share = if shards > 1.0 { hot + (1.0 - hot) / shards } else { 1.0 };
                max_shard_share = Some(share);
                let read_load = a.reads + a.extra + a.heavy * (r::HEAVY_SEARCH - 1.0);
                let write_load = a.writes;
                let read_base = r::DB_READ.get(size_of(i)) * eng;
                let write_base = r::DB_WRITE.get(size_of(i)) * eng;
                let working_reps = if u > 0.0 {
                    match opts.fail {
                        Some(FailKind::Component(Kind::Db)) => (reps - 1.0).max(0.0),
                        Some(FailKind::Zone) => (reps - (reps / 3.0).ceil()).max(0.0),
                        _ => reps,
                    }
                } else {
                    0.0
                };
                let wshare = if n.text("shard_key") == "range" && wl.monotonic == Some(true) { 1.0 } else { share };
                if shards > 1.0 {
                    max_shard_share = Some(share.max(wshare));
                }
                let rl = read_load * share;
                let wlo = write_load * wshare;
                if u == 0.0 {
                    ut = if read_load + write_load > 0.0 { 9.0 } else { 0.0 };
                } else if reps > 0.0 {
                    let read_cap = read_base * working_reps.max(1.0);
                    ut = (rl / read_cap).max(wlo / write_base);
                    replica_lag_ms = Some(if n.text("sync") == "sync" { 0.0 } else { jsfmt::round(15.0 + 120.0 * (wlo / write_base).min(1.0)) });
                } else {
                    ut = rl / read_base + wlo / write_base;
                }
                load = read_load + write_load;
                cap = if ut > 0.0 { load / ut } else { read_base + write_base };
                if shards > 1.0 && hot > 0.1 {
                    nt = format!("горячий ключ: {}% нагрузки на один шард", jsfmt::pct0(share));
                }
            }
            Kind::Monitor => {
                load = 0.0;
                cap = 0.0;
                ut = 0.0;
            }
        }
        let down = u == 0.0 && !matches!(n.kind, Kind::Monitor | Kind::Cdn | Kind::Cache);
        let status = if down {
            NodeStatus::Down
        } else if load <= 0.0 && n.kind != Kind::Monitor {
            NodeStatus::Idle
        } else if ut > 1.0 {
            NodeStatus::Over
        } else if ut > 0.8 {
            NodeStatus::Hot
        } else if ut > 0.6 {
            NodeStatus::Warm
        } else {
            NodeStatus::Ok
        };
        util[i] = ut;
        loads.push(n.id.clone(), NodeLoad { load, cap, util: ut, units: u, status, note: if nt.is_empty() { None } else { Some(nt) } });
    }

    /* очередь: отставание */
    let mut lag_sec: Option<f64> = None;
    let queue = nodes.iter().position(|n| n.kind == Kind::Queue).or_else(|| nodes.iter().position(|n| n.kind == Kind::Stream));
    if let Some(q) = queue {
        let arrive = acc[q].queued;
        let has_worker = nodes.iter().any(|n| n.kind == Kind::Worker);
        lag_sec = Some(if !has_worker || drain_cap <= 0.0 {
            if arrive > 0.0 {
                999.0
            } else {
                0.0
            }
        } else if arrive <= drain_cap {
            0.0
        } else {
            match wl.spike_sec {
                Some(sp) if sp != 0.0 => jsfmt::round(((arrive - drain_cap) * sp) / drain_cap),
                _ => 999.0,
            }
        });
    }

    /* --- метрики по путям --- */
    let own_lat = |i: usize, cls: Cls| -> f64 {
        let n = &nodes[i];
        let base = match n.kind {
            Kind::Cdn => r::lat::CDN,
            Kind::Limiter => r::lat::LIMITER,
            Kind::Gateway => r::lat::GATEWAY,
            Kind::Lb => {
                if n.text("layer") == "L7" {
                    r::lat::LB_L7
                } else {
                    r::lat::LB_L4
                }
            }
            Kind::Ws => r::lat::WS,
            Kind::App => {
                if cls == Cls::Static {
                    r::lat::APP_STATIC
                } else {
                    r::lat::APP
                }
            }
            Kind::Cache => r::lat::CACHE,
            Kind::Queue => r::lat::QUEUE,
            Kind::Blob => r::blob_tier(&n.text("tier")).map_or(r::lat::BLOB, |t| t.lat),
            Kind::Auth => r::lat::AUTH,
            Kind::Geo => r::lat::GEO,
            Kind::Ml => r::lat::ML,
            Kind::Pay => r::lat::PAY,
            Kind::Search => r::lat::SEARCH,
            Kind::Db => {
                let k = if n.text("engine") == "nosql" { 0.7 } else { 1.0 };
                let a = &acc[i];
                let heavy_share = if a.reads > 0.0 { (a.heavy / a.reads).min(1.0) } else { 0.0 };
                let op = if cls == Cls::Write {
                    r::lat::DB_WRITE + if n.text("sync") == "sync" && n.num("replicas") > 0.0 { 8.0 } else { 0.0 }
                } else {
                    r::lat::DB_READ
                };
                op * k * (1.0 + 4.0 * heavy_share)
            }
            _ => 0.0,
        };
        let u = util[i];
        let q = if matches!(n.kind, Kind::Cdn | Kind::Blob) || u < 0.5 {
            1.0
        } else if u >= 1.0 {
            40.0
        } else {
            (1.0 / (1.0 - u)).min(40.0)
        };
        base * q
    };

    let rate = |c: Cls| match c {
        Cls::Static => wl.static_rps,
        Cls::Read => wl.read_rps,
        Cls::Write => wl.write_rps,
    };
    let total_rate = (wl.static_rps + wl.read_rps + wl.write_rps).max(1.0);
    let mut lat = 0.0;
    let mut succ = 0.0;
    let mut avail = 0.0;
    let mut wsum = 0.0;
    let mut touched: Vec<usize> = Vec::new();
    let mut touched_set: HashSet<usize> = HashSet::new();
    let mut touch = |i: usize, touched: &mut Vec<usize>| {
        if touched_set.insert(i) {
            touched.push(i);
        }
    };
    for p in &paths {
        let w = (p.p * rate(p.cls)) / total_rate;
        if w <= 0.0 {
            continue;
        }
        wsum += w;
        let mut l = 0.0;
        let mut s = if p.ok { 1.0 } else { 0.0 };
        let mut av = if p.ok || p.rej { 1.0 } else { 0.0 };
        let mut seen: HashSet<usize> = HashSet::new();
        for &id in &p.nodes {
            let n = &nodes[id];
            if n.kind == Kind::Clients {
                continue;
            }
            touch(id, &mut touched);
            l += own_lat(id, p.cls);
            if n.kind == Kind::App && p.cls != Cls::Static {
                // вызовы сервисов: на долю f запросов добавляются задержка, потери и риск сервиса; нет связи — эти запросы не выполняются
                for k in DEPS {
                    let f = wl.calls_of(k).clamp(0.0, 1.0);
                    if f <= 0.0 {
                        continue;
                    }
                    let group = m.kids(id, &[k.kind()]);
                    if group.is_empty() {
                        s *= 1.0 - f;
                        av *= 1.0 - f;
                        continue;
                    }
                    let mut gl = 0.0;
                    let mut gs = 0.0;
                    let mut ga = 0.0;
                    for &d in &group {
                        touch(d, &mut touched);
                        let du = util[d];
                        gl += own_lat(d, p.cls);
                        gs += if m.units[d] > 0.0 {
                            if du > 1.0 {
                                1.0 / du
                            } else {
                                1.0
                            }
                        } else {
                            0.0
                        };
                        ga += tier_avail(&nodes[d]);
                    }
                    let len = group.len() as f64;
                    l += (f * gl) / len;
                    s *= 1.0 - f + (f * gs) / len;
                    av *= 1.0 - f + (f * ga) / len;
                }
            }
            let ut = util[id];
            let served = if ut > 1.0 { 1.0 / ut } else { 1.0 };
            if n.kind == Kind::Limiter {
                // пропуск уже учтён отдельными путями
            } else {
                s *= if m.units[id] > 0.0 || matches!(n.kind, Kind::Cache | Kind::Cdn | Kind::Monitor) { served } else { 0.0 };
            }
            if !seen.contains(&id) && !matches!(n.kind, Kind::Cache | Kind::Cdn) {
                av *= tier_avail(n);
            }
            seen.insert(id);
        }
        lat += w * l;
        succ += w * s;
        avail += w * av;
    }
    if wsum > 0.0 {
        lat /= wsum;
        succ /= wsum;
        avail /= wsum;
    }
    let mut tail = 0.0;
    for &id in &touched {
        tail += 200.0 * (util[id] - 0.7).max(0.0);
    }
    let p50 = jsfmt::round(lat);
    let p99 = jsfmt::round(lat * 1.8 + tail.min(4000.0));

    let entry = !paths.is_empty() && paths.iter().any(|p| p.ok);
    let mut cost = 0.0;
    for n in nodes {
        cost += node_cost(n, wl);
    }

    {
        let mut idx: HashMap<&str, usize> = HashMap::new();
        for (i, n) in nodes.iter().enumerate() {
            idx.insert(n.id.as_str(), i);
        }
        for n in nodes {
            if n.kind == Kind::Clients {
                continue;
            }
            let incoming = state.edges.iter().any(|e| e.to == n.id && idx.get(e.from.as_str()).is_some_and(|&f| can_link(nodes[f].kind, n.kind)));
            if !incoming && n.kind != Kind::Monitor {
                warnings.push(format!("«{}» ни к чему не подключён — к нему не приходит нагрузка", n.name));
            }
        }
    }
    let mut uniq: Vec<String> = Vec::with_capacity(warnings.len());
    for w in warnings {
        if !uniq.contains(&w) {
            uniq.push(w);
        }
    }

    EvalResult {
        loads,
        p50,
        p99,
        success: jsfmt::round(succ * 10000.0) / 10000.0,
        availability: avail,
        cost,
        hit: hit_ratio,
        cdn_hit: cdn_hit_ratio,
        lag_sec,
        replica_lag_ms,
        max_shard_share,
        entry,
        warnings: uniq,
    }
}
