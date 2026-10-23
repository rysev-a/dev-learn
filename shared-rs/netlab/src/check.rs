//! Проверка упражнения: цели сценария прогоняются на чистой копии сети (без кэшей ARP и MAC), чтобы результат
//! не зависел от того, что ученик успел «нащупать» пингами. Цели и шаги эталонного решения — данные.

use crate::http::{http_fetch, FetchOptions, FetchResult};
use crate::ip::*;
use crate::model::{split_ref, LinkExtra};
use crate::pageload::{pageload, PageloadResult};
use crate::sim::{fmt_ms, ping1, tcp1, udp1, PingOpts};
use crate::ssh::{ssh_connect, Auth};
use crate::term::{exec, to_ip};
use crate::transfer::{transfer, TransferChart};
use crate::types::*;
use crate::util::{num_str, to_fixed, OrdMap};
use serde::{Deserialize, Serialize};

/* ---- цели ---- */

/// Ожидание от пробы: получится или должно быть запрещено.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Expect {
    Ok,
    Fail,
}

/// Цель-проба: ping, TCP или UDP от устройства `from` к `to` (адрес, «@устройство» или имя).
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct ProbeGoal {
    pub from: String,
    pub to: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub port: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub expect: Option<Expect>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub size: Option<i64>,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub df: bool,
    #[serde(rename = "size_from_mtu", alias = "sizeFromMtu", default, skip_serializing_if = "std::ops::Not::not")]
    pub size_from_mtu: bool,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub warm: bool,
    #[serde(rename = "max_rtt_ms", alias = "maxRttMs", default, skip_serializing_if = "Option::is_none")]
    pub max_rtt_ms: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub via: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub avoid: Option<String>,
    #[serde(rename = "no_loop", alias = "noLoop", default, skip_serializing_if = "std::ops::Not::not")]
    pub no_loop: bool,
    #[serde(rename = "not_seen_by", alias = "notSeenBy", default, skip_serializing_if = "Option::is_none")]
    pub not_seen_by: Option<String>,
    #[serde(rename = "seen_src", alias = "seenSrc", default, skip_serializing_if = "Option::is_none")]
    pub seen_src: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsGoal {
    pub from: String,
    pub name: String,
    /// Ожидаемый адрес, «NXDOMAIN» или «ошибка».
    pub expect: String,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct MtuGoal {
    pub dev: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub iface: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub min: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max: Option<u32>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct LbSpreadGoal {
    pub from: String,
    pub to: String,
    pub port: i64,
    pub n: u32,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub distinct: Option<u32>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub avoid: Vec<String>,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub sticky: bool,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct SshGoal {
    pub from: String,
    pub to: String,
    pub user: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub via: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub pass: Option<String>,
    /// «key» или «password».
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub auth: Option<String>,
    /// «fail» — вход должен быть закрыт.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub expect: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PageGoal {
    pub from: String,
    pub to: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub https: Option<bool>,
    #[serde(rename = "max_s", alias = "maxS")]
    pub max_s: f64,
}

/// Ожидание от заголовка ответа: он есть (`true`) или содержит подстроку.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum HeaderWant {
    Present(bool),
    Contains(String),
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct HttpGoal {
    pub from: String,
    pub url: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub method: Option<String>,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub follow: bool,
    #[serde(default, skip_serializing_if = "OrdMap::is_empty")]
    pub headers: OrdMap<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proxy: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub repeat: Option<u32>,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub fail: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub nth: Option<usize>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub status: Option<u32>,
    #[serde(default, skip_serializing_if = "OrdMap::is_empty")]
    pub header: OrdMap<HeaderWant>,
    #[serde(rename = "no_header", alias = "noHeader", default, skip_serializing_if = "Vec::is_empty")]
    pub no_header: Vec<String>,
    #[serde(rename = "body_includes", alias = "bodyIncludes", default, skip_serializing_if = "Option::is_none")]
    pub body_includes: Option<String>,
    #[serde(rename = "max_rtt_ms", alias = "maxRttMs", default, skip_serializing_if = "Option::is_none")]
    pub max_rtt_ms: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub hops: Option<usize>,
    #[serde(rename = "final_url", alias = "finalUrl", default, skip_serializing_if = "Option::is_none")]
    pub final_url: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct XferGoal {
    pub from: String,
    pub to: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mb: Option<f64>,
    #[serde(rename = "min_mbps", alias = "minMbps", default, skip_serializing_if = "Option::is_none")]
    pub min_mbps: Option<f64>,
    #[serde(rename = "max_loaded_rtt_ms", alias = "maxLoadedRttMs", default, skip_serializing_if = "Option::is_none")]
    pub max_loaded_rtt_ms: Option<f64>,
}

/// Вид цели: ровно одна проверка.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum GoalKind {
    Ping(ProbeGoal),
    Tcp(ProbeGoal),
    Udp(ProbeGoal),
    Dns(DnsGoal),
    Mtu(MtuGoal),
    Lbspread(LbSpreadGoal),
    Ssh(SshGoal),
    Page(PageGoal),
    Http(HttpGoal),
    Xfer(XferGoal),
}

/// Цель упражнения.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Goal {
    pub id: String,
    pub text: String,
    #[serde(flatten)]
    pub kind: GoalKind,
}

/// Что показывает панель результата: переходы кадров, события и (для передачи файла) график.
#[derive(Clone, Debug, Default, Serialize)]
pub struct GoalRun {
    pub hops: Vec<Hop>,
    pub events: Vec<NetEvent>,
    pub delivered: Vec<Delivered>,
    pub chart: Option<TransferChart>,
    pub status: Option<ProbeStatus>,
    pub err: Option<String>,
}

impl From<&ProbeRun> for GoalRun {
    fn from(r: &ProbeRun) -> GoalRun {
        GoalRun { hops: r.hops.clone(), events: r.events.clone(), delivered: r.delivered.clone(), chart: None, status: None, err: None }
    }
}

/// Результат проверки одной цели.
#[derive(Clone, Debug, Serialize)]
pub struct GoalResult {
    pub id: String,
    pub text: String,
    pub ok: bool,
    pub detail: String,
    pub run: GoalRun,
}

fn from_run(r: Option<&ProbeRun>) -> GoalRun {
    r.map(GoalRun::from).unwrap_or_default()
}

/// «10.0.0.5» | «@srv» | «@r1.eth1» → адрес.
pub fn resolve_target(state: &NetState, spec: &str) -> Option<u32> {
    if let Some(rest) = spec.strip_prefix('@') {
        let mut parts = rest.split('.');
        let id = parts.next().unwrap_or("");
        let ifn = parts.next();
        let d = state.devices.get(id)?;
        let i = match ifn.filter(|x| !x.is_empty()) {
            Some(n) => d.ifaces.iter().find(|x| x.name == n),
            None => d.ifaces.iter().find(|x| x.ip.as_deref().map(|s| !s.is_empty()).unwrap_or(false)),
        };
        return i.and_then(|i| i.ip.as_deref().filter(|s| !s.is_empty())).and_then(parse_ip);
    }
    parse_ip(spec)
}

/// Цель пробы: адрес, «@устройство» или имя (через hosts и DNS-резолвер устройства-источника).
pub fn resolve_from(state: &mut NetState, spec: &str, from_id: &str) -> Result<crate::term::Resolved, crate::term::ResolveErr> {
    if spec.starts_with('@') {
        return match resolve_target(state, spec) {
            None => Err(crate::term::ResolveErr { err: "у цели нет адреса".into(), run: None }),
            Some(ip) => Ok(crate::term::Resolved { ip, from: None, run: None }),
        };
    }
    if let Some(ip) = parse_ip(spec) {
        return Ok(crate::term::Resolved { ip, from: None, run: None });
    }
    to_ip(state, from_id, spec)
}

/// Итог пробы цели: статус и то, что нужно панели результата.
#[derive(Clone, Debug)]
pub struct ProbeOutcome {
    pub status: ProbeStatus,
    pub err: Option<String>,
    pub code: Option<IcmpCode>,
    pub mtu: Option<u32>,
    pub rtt_us: Option<f64>,
    pub events: Vec<NetEvent>,
    pub hops: Vec<Hop>,
    pub delivered: Vec<Delivered>,
}

impl ProbeOutcome {
    fn run(&self) -> GoalRun {
        GoalRun {
            hops: self.hops.clone(),
            events: self.events.clone(),
            delivered: self.delivered.clone(),
            chart: None,
            status: Some(self.status),
            err: self.err.clone(),
        }
    }
}

/// Прогнать цель-пробу (ping, TCP или UDP) на состоянии `state` (кэши состояния при этом меняются).
/// Для целей других видов вернёт `Noaddr` с пояснением.
pub fn run_probe(state: &mut NetState, goal: &Goal) -> ProbeOutcome {
    let (p, which) = match &goal.kind {
        GoalKind::Ping(p) => (p, 0),
        GoalKind::Udp(p) => (p, 1),
        GoalKind::Tcp(p) => (p, 2),
        _ => {
            return ProbeOutcome {
                status: ProbeStatus::Noaddr,
                err: Some("это не проба".into()),
                code: None,
                mtu: None,
                rtt_us: None,
                events: vec![],
                hops: vec![],
                delivered: vec![],
            };
        }
    };
    let res = match resolve_from(state, &p.to, &p.from) {
        Ok(r) => r,
        Err(e) => {
            let (events, hops) = e.run.map(|r| (r.events, r.hops)).unwrap_or_default();
            return ProbeOutcome {
                status: ProbeStatus::Noaddr,
                err: Some(e.err),
                code: None,
                mtu: None,
                rtt_us: None,
                events,
                hops,
                delivered: vec![],
            };
        }
    };
    let dst = res.ip;
    let mut popts = PingOpts::default();
    if which == 0 && p.size_from_mtu {
        let mtu = state
            .devices
            .get(&p.from)
            .and_then(|d| d.ifaces.iter().find(|x| x.ip.is_some()).or(d.ifaces.first()))
            .and_then(|i| i.mtu)
            .unwrap_or(1500);
        popts.size = Some(mtu as i64 - 28);
        popts.df = true;
    } else if which == 0 {
        if let Some(s) = p.size {
            popts.size = Some(s);
            popts.df = p.df;
        }
    }
    let port = p.port.unwrap_or(0);
    let once = |state: &mut NetState| -> ProbeRun {
        match which {
            0 => ping1(state, &p.from, dst, &popts),
            1 => udp1(state, &p.from, dst, port, 50001),
            _ => tcp1(state, &p.from, dst, port, 50000, false),
        }
    };
    if p.warm {
        once(state); // «прогрев»: ARP и таблицы коммутаторов уже выучены
    }
    let r = once(state);
    ProbeOutcome {
        status: r.status,
        err: None,
        code: r.code,
        mtu: r.mtu,
        rtt_us: r.rtt_us,
        events: r.events,
        hops: r.hops,
        delivered: r.delivered,
    }
}

fn status_text(s: ProbeStatus) -> &'static str {
    match s {
        ProbeStatus::Reply => "ответ получен",
        ProbeStatus::Connected => "соединение установлено",
        ProbeStatus::Refused => "порт закрыт (RST)",
        ProbeStatus::Timeout => "ответа нет",
        ProbeStatus::Ttl => "TTL истёк по дороге",
        ProbeStatus::Unreach => "получено «недоступно»",
        ProbeStatus::Noaddr => "имя или адрес цели не определились",
        ProbeStatus::Toolong => "пакет больше MTU интерфейса",
    }
}

/// Пакет действительно прошёл через устройство: оно его отправляло или он был адресован его интерфейсу.
fn touches(run: &GoalRun, state: &NetState, id: &str) -> bool {
    run.hops.iter().any(|h| {
        let Payload::Ip(_) = &h.frame.body else { return false };
        if h.from == id {
            return true;
        }
        if h.to != id {
            return false;
        }
        match state.devices.get(id) {
            Some(d) if matches!(d.kind, DeviceKind::Switch | DeviceKind::Hub) => true,
            Some(d) => d.ifaces.iter().any(|i| i.name == h.to_port && i.mac == h.frame.dst),
            None => false,
        }
    })
}

fn dev_name(state: &NetState, id: &str) -> String {
    state.devices.get(id).map(|d| d.name.clone()).unwrap_or_else(|| id.to_string())
}

fn fail(g: &Goal, detail: impl Into<String>, run: GoalRun) -> GoalResult {
    GoalResult { id: g.id.clone(), text: g.text.clone(), ok: false, detail: detail.into(), run }
}

fn res(g: &Goal, ok: bool, detail: impl Into<String>, run: GoalRun) -> GoalResult {
    GoalResult { id: g.id.clone(), text: g.text.clone(), ok, detail: detail.into(), run }
}

fn proto_name(p: HttpProto) -> &'static str {
    p.name()
}

/// Проверить все цели на чистой копии сети.
pub fn check_goals(state: &NetState, goals: &[Goal]) -> Vec<GoalResult> {
    goals.iter().map(|g| check_goal(state, g)).collect()
}

fn check_goal(state: &NetState, g: &Goal) -> GoalResult {
    match &g.kind {
        GoalKind::Dns(x) => {
            let mut s = state.stripped();
            let r = to_ip(&mut s, &x.from, &x.name);
            let (got, ok, detail, run) = match r {
                Err(e) => {
                    let got = if e.err.contains("NXDOMAIN") { "NXDOMAIN".to_string() } else { "ошибка".to_string() };
                    let ok = got == x.expect;
                    let detail = if ok { format!("{} → {got}", x.name) } else { format!("{}: {}", x.name, e.err) };
                    (got, ok, detail, from_run(e.run.as_ref()))
                }
                Ok(o) => {
                    let got = ip_str(o.ip);
                    let ok = got == x.expect;
                    let detail = if ok {
                        format!("{} → {got}", x.name)
                    } else {
                        format!("{} → {got}, а ожидалось {}", x.name, x.expect)
                    };
                    (got, ok, detail, from_run(o.run.as_ref()))
                }
            };
            let _ = got;
            res(g, ok, detail, run)
        }
        GoalKind::Mtu(x) => {
            let i = state.devices.get(&x.dev).and_then(|d| d.ifaces.iter().find(|k| k.name == x.iface.as_deref().unwrap_or("eth0")));
            let m = i.and_then(|i| i.mtu).unwrap_or(1500);
            let ok = x.min.map(|v| m >= v).unwrap_or(true) && x.max.map(|v| m <= v).unwrap_or(true);
            let detail = if ok {
                format!("MTU {} = {m}", i.map(|i| i.name.as_str()).unwrap_or("undefined"))
            } else {
                let lo = x.min.map(|v| format!("не меньше {v}")).unwrap_or_default();
                let hi = x.max.map(|v| format!(" не больше {v}")).unwrap_or_default();
                format!("MTU {} = {m}, нужно {lo}{hi}", i.map(|i| i.name.as_str()).unwrap_or("?"))
            };
            res(g, ok, detail, GoalRun::default())
        }
        GoalKind::Lbspread(x) => {
            let mut s = state.stripped();
            let r = match resolve_from(&mut s, &x.to, &x.from) {
                Ok(r) => r,
                Err(e) => return fail(g, e.err, GoalRun::default()),
            };
            let mut hits: OrdMap<u32> = OrdMap::new();
            let mut ok_n = 0u32;
            let mut last: Option<ProbeRun> = None;
            for i in 0..x.n {
                let l = tcp1(&mut s, &x.from, r.ip, x.port, 50000 + i as i64, false);
                if l.status == ProbeStatus::Connected {
                    ok_n += 1;
                    if let Some(dev) = l.delivered.iter().rev().find(|e| e.dev != x.from).map(|e| e.dev.clone()) {
                        let n = hits.get(&dev).copied().unwrap_or(0) + 1;
                        hits.insert(dev, n);
                    }
                }
                last = Some(l);
            }
            let mut bad: Vec<String> = Vec::new();
            if ok_n < x.n {
                bad.push(format!("успешных соединений {ok_n} из {}", x.n));
            }
            let used: Vec<&String> = hits.keys().collect();
            if let Some(d) = x.distinct.filter(|d| *d != 0) {
                if (used.len() as u32) < d {
                    bad.push(format!("задействовано серверов {}, а нужно {d}", used.len()));
                }
            }
            for a in &x.avoid {
                if hits.get(a).copied().unwrap_or(0) != 0 {
                    bad.push(format!("запросы попали на неисправный «{}»", dev_name(&s, a)));
                }
            }
            if x.sticky && used.len() > 1 {
                bad.push("один клиент попадает на разные серверы".into());
            }
            let spread: Vec<String> = hits.iter().map(|(k, v)| format!("{}: {v}", dev_name(&s, k))).collect();
            res(g, bad.is_empty(), if bad.is_empty() { spread.join(", ") } else { bad.join("; ") }, from_run(last.as_ref()))
        }
        GoalKind::Ssh(x) => {
            let mut s = state.stripped();
            let dst = match resolve_from(&mut s, &x.to, &x.from) {
                Ok(r) => r,
                Err(e) => return fail(g, e.err, GoalRun::default()),
            };
            let mut jump: Option<u32> = None;
            if let Some(v) = x.via.as_deref().filter(|v| !v.is_empty()) {
                match resolve_from(&mut s, v, &x.from) {
                    Ok(j) => jump = Some(j.ip),
                    Err(e) => return fail(g, e.err, GoalRun::default()),
                }
            }
            let r = ssh_connect(&mut s, &x.from, &x.user, dst.ip, jump, x.pass.as_deref(), x.auth.as_deref() == Some("password"));
            let want_fail = x.expect.as_deref() == Some("fail");
            let auth_ok = match x.auth.as_deref().filter(|a| !a.is_empty()) {
                None => true,
                Some(a) => r.auth.map(Auth::as_str) == Some(a),
            };
            let ok = if want_fail { !r.ok } else { r.ok && auth_ok };
            let detail = if r.ok {
                format!(
                    "вход выполнен ({}){}",
                    if r.auth == Some(Auth::Key) { "по ключу" } else { "по паролю" },
                    if want_fail { " — а должен быть закрыт" } else { "" }
                )
            } else {
                let last = r.error.clone().unwrap_or_default();
                let last = last.split('\n').next_back().unwrap_or("").to_string();
                format!("{last}{}", if want_fail { " — так и задумано" } else { "" })
            };
            res(g, ok, detail, from_run(r.run.as_ref()))
        }
        GoalKind::Page(x) => {
            let mut s = state.stripped();
            let r = match resolve_from(&mut s, &x.to, &x.from) {
                Ok(r) => r,
                Err(e) => return fail(g, e.err, GoalRun::default()),
            };
            match pageload(&mut s, &x.from, r.ip, x.https.unwrap_or(true)) {
                PageloadResult::Failed(e) => fail(g, e, GoalRun::default()),
                PageloadResult::Ok { used, note, chosen, .. } => {
                    let sec = chosen.total / 1e6;
                    let ok = sec <= x.max_s;
                    let mut detail =
                        format!("{} с по {}{}", to_fixed(sec, 2), proto_name(used), if note.is_empty() { "" } else { " (откат с HTTP/3)" });
                    if !ok {
                        detail.push_str(&format!(", нужно не больше {} с", num_str(x.max_s)));
                    }
                    res(g, ok, detail, GoalRun::default())
                }
            }
        }
        GoalKind::Http(x) => check_http(state, g, x),
        GoalKind::Xfer(x) => {
            let mut s = state.stripped();
            let Some(dst) = resolve_target(&s, &x.to) else { return fail(g, "у цели нет адреса", GoalRun::default()) };
            let r = transfer(&mut s, &x.from, dst, x.mb.unwrap_or(50.0) * 1e6);
            if !r.ok {
                return fail(g, r.text, GoalRun::default());
            }
            let mut bad: Vec<String> = Vec::new();
            if let Some(m) = x.min_mbps {
                if r.mbps < m {
                    bad.push(format!("скорость {} Мбит/с — нужно не меньше {}", to_fixed(r.mbps, 1), num_str(m)));
                }
            }
            if let Some(m) = x.max_loaded_rtt_ms {
                if r.loaded_rtt_ms > m {
                    bad.push(format!("RTT под нагрузкой {} мс — нужно не больше {}", to_fixed(r.loaded_rtt_ms, 0), num_str(m)));
                }
            }
            let detail = if bad.is_empty() {
                format!("{} Мбит/с, RTT под нагрузкой до {} мс", to_fixed(r.mbps, 1), to_fixed(r.loaded_rtt_ms, 0))
            } else {
                bad.join("; ")
            };
            res(g, bad.is_empty(), detail, GoalRun { chart: r.chart.clone(), ..Default::default() })
        }
        GoalKind::Ping(p) | GoalKind::Tcp(p) | GoalKind::Udp(p) => check_probe(state, g, p),
    }
}

fn check_http(state: &NetState, g: &Goal, x: &HttpGoal) -> GoalResult {
    let mut s = state.stripped();
    let mut r = FetchResult::default();
    for _ in 0..x.repeat.unwrap_or(1) {
        r = http_fetch(
            &mut s,
            &x.from,
            &FetchOptions {
                url: x.url.clone(),
                method: x.method.clone().unwrap_or_else(|| "GET".into()),
                follow: x.follow,
                headers: x.headers.clone(),
                proxy: x.proxy.clone(),
            },
        );
    }
    let run = from_run(r.run.as_ref());
    if x.fail {
        return match &r.error {
            Some(e) => res(g, true, format!("{e} — так и задумано"), run),
            None => res(g, false, "запрос прошёл, а должен быть запрещён", run),
        };
    }
    if let Some(e) = &r.error {
        return fail(g, e.clone(), run);
    }
    let resp = match x.nth {
        Some(n) => r.responses.get(n),
        None => r.responses.last(),
    };
    let mut bad: Vec<String> = Vec::new();
    match resp {
        None => bad.push("ответа нет".into()),
        Some(resp) => {
            let rtt = resp.rtt_us.unwrap_or(0.0) / 1000.0;
            if let Some(st) = x.status {
                if resp.status != st {
                    bad.push(format!("код {} {}, а нужен {st}", resp.status, resp.reason));
                }
            }
            for (k, v) in x.header.iter() {
                match resp.headers.get(&k.to_lowercase()) {
                    None => bad.push(format!("нет заголовка {k}")),
                    Some(got) => {
                        if let HeaderWant::Contains(want) = v {
                            if !got.to_lowercase().contains(&want.to_lowercase()) {
                                bad.push(format!("{k}: «{got}», нужно содержащее «{want}»"));
                            }
                        }
                    }
                }
            }
            for k in &x.no_header {
                if resp.headers.get(&k.to_lowercase()).is_some() {
                    bad.push(format!("заголовок {k} не нужен"));
                }
            }
            if let Some(b) = x.body_includes.as_deref().filter(|b| !b.is_empty()) {
                if !resp.body.contains(b) {
                    bad.push(format!("в теле нет «{b}»"));
                }
            }
            if let Some(m) = x.max_rtt_ms {
                if rtt > m {
                    bad.push(format!("ответ за {} мс, нужно быстрее {}", to_fixed(rtt, 0), num_str(m)));
                }
            }
            if let Some(h) = x.hops {
                if r.responses.len() != h {
                    bad.push(format!("запросов {}, а нужно {h}", r.responses.len()));
                }
            }
            if let Some(f) = x.final_url.as_deref().filter(|f| !f.is_empty()) {
                if !resp.url.as_deref().unwrap_or("").ends_with(f) {
                    bad.push(format!("итоговый адрес {}", resp.url.as_deref().unwrap_or("undefined")));
                }
            }
        }
    }
    let detail = if !bad.is_empty() {
        bad.join("; ")
    } else if let Some(resp) = resp {
        let more = if r.responses.len() > 1 { format!(", запросов: {}", r.responses.len()) } else { String::new() };
        format!("{} {}{}", resp.status, resp.reason, more)
    } else {
        String::new()
    };
    res(g, bad.is_empty(), detail, run)
}

fn check_probe(state: &NetState, g: &Goal, p: &ProbeGoal) -> GoalResult {
    let mut s = state.stripped();
    let o = run_probe(&mut s, g);
    let run = o.run();
    let want_ok = p.expect.unwrap_or(Expect::Ok) == Expect::Ok;
    let got_ok = o.status == ProbeStatus::Reply || o.status == ProbeStatus::Connected;
    let mut ok = want_ok == got_ok;
    let mtu_s = o.mtu.map(|m| m.to_string()).unwrap_or_else(|| "undefined".into());
    let mut detail = if o.status == ProbeStatus::Unreach && o.code == Some(IcmpCode::Port) {
        "порт недоступен (ICMP)".to_string()
    } else if o.status == ProbeStatus::Unreach && o.code == Some(IcmpCode::Frag) {
        format!("нужна фрагментация, а DF запрещает (MTU {mtu_s})")
    } else if o.status == ProbeStatus::Toolong {
        format!("{} (MTU {mtu_s})", status_text(ProbeStatus::Toolong))
    } else {
        status_text(o.status).to_string()
    };
    if let Some(clash) = o.events.iter().find(|e| e.kind == EventKind::Conflict) {
        if want_ok {
            return fail(g, clash.text.clone(), run);
        }
    }
    if p.no_loop && o.events.iter().any(|e| e.kind == EventKind::Loop) {
        return fail(g, "в сети петля: кадры ходят по кругу", run);
    }
    if let Some(n) = p.not_seen_by.as_deref().filter(|n| !n.is_empty()) {
        if o.hops.iter().any(|h| h.to == n && matches!(h.frame.body, Payload::Ip(_))) {
            return fail(g, format!("чужой кадр дошёл до «{}» — его можно подслушать", dev_name(&s, n)), run);
        }
    }
    let rtt_us = o.rtt_us;
    if ok && want_ok {
        let slow = match (p.max_rtt_ms, rtt_us) {
            (Some(m), Some(rtt)) if rtt / 1000.0 > m => Some((m, rtt)),
            _ => None,
        };
        if let Some((m, rtt)) = slow {
            ok = false;
            detail = format!("ответ пришёл за {}, а нужно быстрее {} мс", fmt_ms(Some(rtt)), num_str(m));
        } else if let Some(v) = p.via.as_deref().filter(|v| !v.is_empty()).filter(|v| !touches(&run, &s, v)) {
            ok = false;
            detail = format!("пакет дошёл, но не через «{}»", dev_name(&s, v));
        } else if let Some(a) = p.avoid.as_deref().filter(|a| !a.is_empty()).filter(|a| touches(&run, &s, a)) {
            ok = false;
            detail = format!("пакет дошёл, но прошёл через «{}»", dev_name(&s, a));
        } else if let Some(ss) = p.seen_src.as_deref().filter(|v| !v.is_empty()) {
            let want = resolve_target(&s, ss);
            let to_dev = p.to.strip_prefix('@').unwrap_or(&p.to).split('.').next().unwrap_or("").to_string();
            let hit = o.delivered.iter().find(|x| x.dev == to_dev);
            match hit {
                Some(h) if h.src == want => detail = format!("получатель видит отправителя {}", ip_str_opt(h.src)),
                other => {
                    ok = false;
                    detail = match other {
                        Some(h) => format!("получатель видит отправителя {}, а должен видеть {}", ip_str_opt(h.src), ip_str_opt(want)),
                        None => "получатель не видит запрос".to_string(),
                    };
                }
            }
        } else if let Some(rtt) = rtt_us {
            detail.push_str(&format!(" за {}", fmt_ms(Some(rtt))));
        }
    } else if !ok && want_ok {
        detail = format!("{detail} — должно получиться");
    } else if !ok && !want_ok {
        detail = format!("{detail} — а должно быть запрещено");
    } else if ok && !want_ok {
        detail = format!("{detail} — так и задумано");
    }
    res(g, ok, detail, run)
}

/* ---- шаги эталонного решения ---- */

/// Шаг решения: действие над кабелями или команда терминала.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Step {
    /// Убрать кабель между двумя устройствами.
    Unlink { a: String, b: String },
    /// Убрать все кабели устройства.
    Drop { dev: String },
    /// Проложить кабель между первыми свободными портами.
    Cable {
        a: String,
        b: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        extra: Option<LinkExtra>,
    },
    /// Выполнить команду терминала на устройстве.
    Cmd { dev: String, line: String },
}

/// Применить шаги эталонного решения. Ошибка — шаг не удался (нет кабеля, нет портов, команда отвергнута).
pub fn apply_ops(state: &mut NetState, ops: &[Step]) -> Result<(), String> {
    for op in ops {
        match op {
            Step::Unlink { a, b } => {
                let i = state.links.iter().position(|l| {
                    let x = split_ref(&l.a).0;
                    let y = split_ref(&l.b).0;
                    (x == a && y == b) || (x == b && y == a)
                });
                let Some(i) = i else { return Err(format!("нет кабеля {a}–{b}")) };
                state.links.remove(i);
            }
            Step::Drop { dev } => state.links.retain(|l| split_ref(&l.a).0 != dev && split_ref(&l.b).0 != dev),
            Step::Cable { a, b, extra } => state.connect(a, b, extra.as_ref())?,
            Step::Cmd { dev, line } => {
                let r = exec(state, dev, line);
                if r.changed == Some(false) && ["Error", "Permission", "RTNETLINK", "не "].iter().any(|k| r.out.contains(k)) {
                    return Err(format!("{dev}: {line} → {}", r.out));
                }
            }
        }
    }
    Ok(())
}
