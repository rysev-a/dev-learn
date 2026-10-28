//! Exercise check: the scenario goals are run on a clean copy of the network (without ARP and MAC caches) so the result
//! does not depend on what the student managed to "feel out" with pings. Goals and reference solution steps are data.

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

/* ---- goals ---- */

/// Expectation of a probe: it succeeds or it must be blocked.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Expect {
    Ok,
    Fail,
}

/// Probe goal: ping, TCP or UDP from device `from` to `to` (address, "@device" or name).
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
    /// Expected address, "NXDOMAIN" or "error".
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
    /// "key" or "password".
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub auth: Option<String>,
    /// "fail" means login must be denied.
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

/// Expectation of a response header: it exists (`true`) or contains a substring.
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

/// Goal kind: exactly one check.
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

/// Exercise goal.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Goal {
    pub id: String,
    pub text: String,
    #[serde(flatten)]
    pub kind: GoalKind,
}

/// What the result panel shows: frame hops, events and (for file transfer) a chart.
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

/// Result of checking one goal.
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

/// "10.0.0.5" | "@srv" | "@r1.eth1" -> address.
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

/// Probe target: address, "@device" or name (via hosts and the DNS resolver of the source device).
pub fn resolve_from(state: &mut NetState, spec: &str, from_id: &str) -> Result<crate::term::Resolved, crate::term::ResolveErr> {
    if spec.starts_with('@') {
        return match resolve_target(state, spec) {
            None => Err(crate::term::ResolveErr { err: i18n::tr("the goal has no address").into(), run: None }),
            Some(ip) => Ok(crate::term::Resolved { ip, from: None, run: None }),
        };
    }
    if let Some(ip) = parse_ip(spec) {
        return Ok(crate::term::Resolved { ip, from: None, run: None });
    }
    to_ip(state, from_id, spec)
}

/// Outcome of a goal probe: status and what the result panel needs.
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

/// Run a probe goal (ping, TCP or UDP) on state `state` (the state caches change in the process).
/// For goals of other kinds returns `Noaddr` with an explanation.
pub fn run_probe(state: &mut NetState, goal: &Goal) -> ProbeOutcome {
    let (p, which) = match &goal.kind {
        GoalKind::Ping(p) => (p, 0),
        GoalKind::Udp(p) => (p, 1),
        GoalKind::Tcp(p) => (p, 2),
        _ => {
            return ProbeOutcome {
                status: ProbeStatus::Noaddr,
                err: Some(i18n::tr("this is not a probe").into()),
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
        once(state); // "warm-up": ARP and switch tables are already learned
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
        ProbeStatus::Reply => i18n::tr("reply received"),
        ProbeStatus::Connected => i18n::tr("connection established"),
        ProbeStatus::Refused => i18n::tr("port closed (RST)"),
        ProbeStatus::Timeout => i18n::tr("no response"),
        ProbeStatus::Ttl => i18n::tr("TTL expired along the way"),
        ProbeStatus::Unreach => i18n::tr("received “unreachable”"),
        ProbeStatus::Noaddr => i18n::tr("target name or address could not be resolved"),
        ProbeStatus::Toolong => i18n::tr("packet is larger than the interface MTU"),
    }
}

/// The packet really passed through the device: it sent it or it was addressed to its interface.
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

/// Check all goals on a clean copy of the network.
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
                    let got = if e.err.contains("NXDOMAIN") { "NXDOMAIN".to_string() } else { i18n::tr("error").to_string() };
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
                        i18n::trf!("{0} → {1}, expected {2}", x.name, got, x.expect)
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
                let lo = x.min.map(|v| i18n::trf!("at least {0}", v)).unwrap_or_default();
                let hi = x.max.map(|v| i18n::trf!(" at most {0}", v)).unwrap_or_default();
                i18n::trf!("MTU {0} = {1}, need {2}{3}", i.map(|i| i.name.as_str()).unwrap_or("?"), m, lo, hi)
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
                bad.push(i18n::trf!("successful connections: {0} of {1}", ok_n, x.n));
            }
            let used: Vec<&String> = hits.keys().collect();
            if let Some(d) = x.distinct.filter(|d| *d != 0) {
                if (used.len() as u32) < d {
                    bad.push(i18n::trf!("servers used: {0}, need {1}", used.len(), d));
                }
            }
            for a in &x.avoid {
                if hits.get(a).copied().unwrap_or(0) != 0 {
                    bad.push(i18n::trf!("requests reached the failed “{0}”", dev_name(&s, a)));
                }
            }
            if x.sticky && used.len() > 1 {
                bad.push(i18n::tr("one client reaches different servers").into());
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
                i18n::trf!("logged in ({0}){1}", if r.auth == Some(Auth::Key) { i18n::tr("by key") } else { i18n::tr("by password") }, if want_fail { i18n::tr(" — but it should be closed") } else { "" })
            } else {
                let last = r.error.clone().unwrap_or_default();
                let last = last.split('\n').next_back().unwrap_or("").to_string();
                format!("{last}{}", if want_fail { i18n::tr(" — as intended") } else { "" })
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
                        i18n::trf!("{0} s over {1}{2}", to_fixed(sec, 2), proto_name(used), if note.is_empty() { "" } else { i18n::tr(" (fell back from HTTP/3)") });
                    if !ok {
                        detail.push_str(&i18n::trf!(", need at most {0} s", num_str(x.max_s)));
                    }
                    res(g, ok, detail, GoalRun::default())
                }
            }
        }
        GoalKind::Http(x) => check_http(state, g, x),
        GoalKind::Xfer(x) => {
            let mut s = state.stripped();
            let Some(dst) = resolve_target(&s, &x.to) else { return fail(g, i18n::tr("the target has no address"), GoalRun::default()) };
            let r = transfer(&mut s, &x.from, dst, x.mb.unwrap_or(50.0) * 1e6);
            if !r.ok {
                return fail(g, r.text, GoalRun::default());
            }
            let mut bad: Vec<String> = Vec::new();
            if let Some(m) = x.min_mbps {
                if r.mbps < m {
                    bad.push(i18n::trf!("speed {0} Mbit/s — need at least {1}", to_fixed(r.mbps, 1), num_str(m)));
                }
            }
            if let Some(m) = x.max_loaded_rtt_ms {
                if r.loaded_rtt_ms > m {
                    bad.push(i18n::trf!("RTT under load {0} ms — need at most {1}", to_fixed(r.loaded_rtt_ms, 0), num_str(m)));
                }
            }
            let detail = if bad.is_empty() {
                i18n::trf!("{0} Mbit/s, RTT under load up to {1} ms", to_fixed(r.mbps, 1), to_fixed(r.loaded_rtt_ms, 0))
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
            Some(e) => res(g, true, i18n::trf!("{0} — as intended", e), run),
            None => res(g, false, i18n::tr("the request went through, but it should be blocked"), run),
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
        None => bad.push(i18n::tr("no response").into()),
        Some(resp) => {
            let rtt = resp.rtt_us.unwrap_or(0.0) / 1000.0;
            if let Some(st) = x.status {
                if resp.status != st {
                    bad.push(i18n::trf!("status {0} {1}, expected {2}", resp.status, resp.reason, st));
                }
            }
            for (k, v) in x.header.iter() {
                match resp.headers.get(&k.to_lowercase()) {
                    None => bad.push(i18n::trf!("missing header {0}", k)),
                    Some(got) => {
                        if let HeaderWant::Contains(want) = v {
                            if !got.to_lowercase().contains(&want.to_lowercase()) {
                                bad.push(i18n::trf!("{0}: “{1}”, expected to contain “{2}”", k, got, want));
                            }
                        }
                    }
                }
            }
            for k in &x.no_header {
                if resp.headers.get(&k.to_lowercase()).is_some() {
                    bad.push(i18n::trf!("header {0} must not be present", k));
                }
            }
            if let Some(b) = x.body_includes.as_deref().filter(|b| !b.is_empty()) {
                if !resp.body.contains(b) {
                    bad.push(i18n::trf!("body does not contain “{0}”", b));
                }
            }
            if let Some(m) = x.max_rtt_ms {
                if rtt > m {
                    bad.push(i18n::trf!("response in {0} ms, must be faster than {1}", to_fixed(rtt, 0), num_str(m)));
                }
            }
            if let Some(h) = x.hops {
                if r.responses.len() != h {
                    bad.push(i18n::trf!("requests: {0}, expected {1}", r.responses.len(), h));
                }
            }
            if let Some(f) = x.final_url.as_deref().filter(|f| !f.is_empty()) {
                if !resp.url.as_deref().unwrap_or("").ends_with(f) {
                    bad.push(i18n::trf!("final address {0}", resp.url.as_deref().unwrap_or("undefined")));
                }
            }
        }
    }
    let detail = if !bad.is_empty() {
        bad.join("; ")
    } else if let Some(resp) = resp {
        let more = if r.responses.len() > 1 { i18n::trf!(", requests: {0}", r.responses.len()) } else { String::new() };
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
        i18n::tr("port unreachable (ICMP)").to_string()
    } else if o.status == ProbeStatus::Unreach && o.code == Some(IcmpCode::Frag) {
        i18n::trf!("fragmentation needed but DF forbids it (MTU {0})", mtu_s)
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
        return fail(g, i18n::tr("there is a loop in the network: frames go round in circles"), run);
    }
    if let Some(n) = p.not_seen_by.as_deref().filter(|n| !n.is_empty()) {
        if o.hops.iter().any(|h| h.to == n && matches!(h.frame.body, Payload::Ip(_))) {
            return fail(g, i18n::trf!("another host's frame reached “{0}” — it can be eavesdropped", dev_name(&s, n)), run);
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
            detail = i18n::trf!("reply arrived in {0}, must be faster than {1} ms", fmt_ms(Some(rtt)), num_str(m));
        } else if let Some(v) = p.via.as_deref().filter(|v| !v.is_empty()).filter(|v| !touches(&run, &s, v)) {
            ok = false;
            detail = i18n::trf!("the packet arrived, but not via “{0}”", dev_name(&s, v));
        } else if let Some(a) = p.avoid.as_deref().filter(|a| !a.is_empty()).filter(|a| touches(&run, &s, a)) {
            ok = false;
            detail = i18n::trf!("the packet arrived, but passed through “{0}”", dev_name(&s, a));
        } else if let Some(ss) = p.seen_src.as_deref().filter(|v| !v.is_empty()) {
            let want = resolve_target(&s, ss);
            let to_dev = p.to.strip_prefix('@').unwrap_or(&p.to).split('.').next().unwrap_or("").to_string();
            let hit = o.delivered.iter().find(|x| x.dev == to_dev);
            match hit {
                Some(h) if h.src == want => detail = i18n::trf!("the receiver sees the sender as {0}", ip_str_opt(h.src)),
                other => {
                    ok = false;
                    detail = match other {
                        Some(h) => i18n::trf!("the receiver sees the sender as {0}, but should see {1}", ip_str_opt(h.src), ip_str_opt(want)),
                        None => i18n::tr("the receiver does not see the request").to_string(),
                    };
                }
            }
        } else if let Some(rtt) = rtt_us {
            detail.push_str(&i18n::trf!(" in {0}", fmt_ms(Some(rtt))));
        }
    } else if !ok && want_ok {
        detail = i18n::trf!("{0} — it should succeed", detail);
    } else if !ok && !want_ok {
        detail = i18n::trf!("{0} — but it should be blocked", detail);
    } else if ok && !want_ok {
        detail = i18n::trf!("{0} — as intended", detail);
    }
    res(g, ok, detail, run)
}

/* ---- reference solution steps ---- */

/// Solution step: a cable action or a terminal command.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Step {
    /// Remove the cable between two devices.
    Unlink { a: String, b: String },
    /// Remove all cables of a device.
    Drop { dev: String },
    /// Lay a cable between the first free ports.
    Cable {
        a: String,
        b: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        extra: Option<LinkExtra>,
    },
    /// Execute a terminal command on a device.
    Cmd { dev: String, line: String },
}

/// Apply the reference solution steps. Error means a step failed (no cable, no ports, command rejected).
pub fn apply_ops(state: &mut NetState, ops: &[Step]) -> Result<(), String> {
    for op in ops {
        match op {
            Step::Unlink { a, b } => {
                let i = state.links.iter().position(|l| {
                    let x = split_ref(&l.a).0;
                    let y = split_ref(&l.b).0;
                    (x == a && y == b) || (x == b && y == a)
                });
                let Some(i) = i else { return Err(i18n::trf!("no cable {0}–{1}", a, b)) };
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
