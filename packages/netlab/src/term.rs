//! Linux mini-terminal for network devices: ip, ping, traceroute, curl, iptables, sysctl etc.
//! Commands change the state the same way the forms in the device card do (they call the same functions),
//! so the reference solution of an exercise is simply a list of commands.

use crate::attacks::background_traffic;
use crate::capture::capture_lines;
use crate::dns::{answer_ip, fmt_dns, fqdn, local_lookup, new_dns, LocalLookup};
use crate::http::{fmt_curl, http_fetch, new_http, FetchOptions, FetchResult};
use crate::ip::*;
use crate::pageload::{fmt_page, pageload};
use crate::sim::{dns1, fmt_ms, lookup, ping1, route_table, tcp1, traceroute, udp1, PingOpts, RouteEntry};
use crate::ssh::{make_key, new_ssh, ssh_connect};
use crate::tls::{add_days, default_pki, default_trust, new_tls, s_client, NOW};
use crate::transfer::{transfer, TransferChart, TransferResult};
use crate::types::*;
use crate::util::{js_num, num_or, num_str, to_int, und, OrdMap};

/// Terminal command result: output, whether the network state changed, probe for animation.
#[derive(Clone, Debug, Default)]
pub struct CmdResult {
    pub out: String,
    /// `Some(false)` means the command failed (error in `out`), `Some(true)` means the state changed, `None` means output only.
    pub changed: Option<bool>,
    pub probe: Option<ProbeRun>,
    pub http: Option<FetchResult>,
    pub clear: bool,
    pub chart: Option<TransferChart>,
    pub xfer: Option<TransferResult>,
}

fn out(s: impl Into<String>) -> CmdResult {
    CmdResult { out: s.into(), ..Default::default() }
}

fn changed(s: impl Into<String>) -> CmdResult {
    CmdResult { out: s.into(), changed: Some(true), ..Default::default() }
}

fn probe(s: impl Into<String>, p: Option<ProbeRun>) -> CmdResult {
    CmdResult { out: s.into(), probe: p, ..Default::default() }
}

/// Action outcome: empty error is success (`changed: true`), otherwise the error text.
fn done(err: Option<String>) -> CmdResult {
    CmdResult { changed: Some(err.is_none()), out: err.unwrap_or_default(), ..Default::default() }
}

fn no(d: &Device) -> Option<String> {
    if d.locked {
        Some(i18n::trf!("Permission denied: \"{0}\" belongs to the provider and cannot be configured", d.name))
    } else {
        None
    }
}

/// Index of the first occurrence (-1 if none), like `Array.prototype.indexOf`.
fn index_of(a: &[&str], x: &str) -> isize {
    a.iter().position(|v| *v == x).map(|i| i as isize).unwrap_or(-1)
}

/// Element after the key: `a[a.indexOf(key) + 1]` (without the key `a[0]`).
fn after<'a>(a: &[&'a str], key: &str) -> Option<&'a str> {
    a.get((index_of(a, key) + 1) as usize).copied()
}

fn splice_at<T>(v: &mut Vec<T>, idx: f64, item: T) {
    let len = v.len() as f64;
    let i = if idx < 0.0 { (len + idx).max(0.0) } else { idx.min(len) } as usize;
    v.insert(i, item);
}

/* ---- settings changes (shared by forms and the terminal) ---- */

/// Assign address "ip/prefix" to an interface. Error is text like `ip addr add` gives.
pub fn set_addr(d: &mut Device, if_name: &str, cidr: &str) -> Option<String> {
    let Some(i) = d.iface_mut(if_name) else { return Some(format!("Cannot find device \"{if_name}\"")) };
    let Some((ip, prefix)) = parse_cidr(cidr) else { return Some(format!("Error: inet prefix is expected rather than \"{cidr}\".")) };
    if i.ip.is_some() {
        return Some(i18n::trf!("RTNETLINK answers: File exists (run ip addr flush dev {0} first)", if_name));
    }
    i.ip = Some(ip_str(ip));
    i.prefix = prefix as u8;
    None
}

/// Remove the interface address; routes via the vanished subnet disappear with it.
pub fn clear_addr(d: &mut Device, if_name: &str) -> Option<String> {
    let Some(i) = d.iface_mut(if_name) else { return Some(format!("Cannot find device \"{if_name}\"")) };
    i.ip = None;
    let ifaces = d.ifaces.clone();
    d.routes.retain(|r| match r.via.as_deref().filter(|v| !v.is_empty()) {
        None => true,
        Some(via) => {
            let v = parse_ip(via);
            ifaces
                .iter()
                .any(|x| x.ip.is_some() && in_net(v, Some(network_of(parse_ip_opt(x.ip.as_deref()), x.prefix as u32)), x.prefix as u32))
        }
    });
    None
}

/// Bring an interface up or down.
pub fn set_up(d: &mut Device, if_name: &str, up: bool) -> Option<String> {
    let Some(i) = d.iface_mut(if_name) else { return Some(format!("Cannot find device \"{if_name}\"")) };
    i.up = up;
    None
}

/// Add a static route.
pub fn add_route(d: &mut Device, dst: Option<&str>, via: Option<&str>, dev: Option<&str>) -> Option<String> {
    let is_default = dst == Some("default") || dst == Some("0.0.0.0/0");
    let n = if is_default { Some((0, 0)) } else { parse_net(dst) };
    let valid = match dst {
        Some(s) => parse_cidr(s).is_some() || parse_ip(s).is_some(),
        None => false,
    };
    let Some((net, prefix)) = n.filter(|_| is_default || valid) else {
        return Some(format!("Error: inet prefix is expected rather than \"{}\".", und(dst)));
    };
    let key = net_str(Some(net), prefix);
    let via = via.filter(|v| !v.is_empty());
    if let Some(via) = via {
        let Some(v) = parse_ip(via) else { return Some(format!("Error: inet address is expected rather than \"{via}\".")) };
        let ok = d.ifaces.iter().any(|x| {
            x.ip.is_some() && x.up && in_net(Some(v), Some(network_of(parse_ip_opt(x.ip.as_deref()), x.prefix as u32)), x.prefix as u32)
        });
        if !ok {
            return Some(i18n::tr("Error: Nexthop has invalid gateway. (the gateway must lie in one of the connected subnets)").into());
        }
    } else if !dev.map(|x| !x.is_empty() && d.iface(x).is_some()).unwrap_or(false) {
        return Some(i18n::tr("Error: specify via <gateway> or dev <interface>").into());
    }
    let dup = d.routes.iter().any(|r| r.dst == key);
    if dup || (prefix != 0 && route_table(d, false).iter().any(|r| r.connected && r.net == net && r.prefix == prefix)) {
        return Some("RTNETLINK answers: File exists".into());
    }
    d.routes.push(Route { dst: key, via: via.map(|s| s.to_string()), dev: dev.map(|s| s.to_string()) });
    None
}

/// Delete a static route.
pub fn del_route(d: &mut Device, dst: Option<&str>) -> Option<String> {
    let is_default = dst == Some("default") || dst == Some("0.0.0.0/0");
    let n = if is_default { Some((0, 0)) } else { parse_net(dst) };
    let Some((net, prefix)) = n else { return Some(format!("Error: inet prefix is expected rather than \"{}\".", und(dst))) };
    let key = net_str(Some(net), prefix);
    let Some(i) = d.routes.iter().position(|r| r.dst == key) else { return Some("RTNETLINK answers: No such process".into()) };
    d.routes.remove(i);
    None
}

/// Default gateway; empty string removes it.
pub fn set_gateway(d: &mut Device, gw: Option<&str>) -> Option<String> {
    let old: Vec<Route> = d.routes.iter().filter(|r| r.dst == "0.0.0.0/0").cloned().collect();
    d.routes.retain(|r| r.dst != "0.0.0.0/0");
    let Some(gw) = gw.filter(|g| !g.is_empty()) else { return None };
    let e = add_route(d, Some("default"), Some(gw), None);
    if e.is_some() {
        d.routes.extend(old);
    }
    e
}

/// Default gateway ("" means none).
pub fn get_gateway(d: &Device) -> String {
    d.routes.iter().find(|r| r.dst == "0.0.0.0/0").and_then(|r| r.via.clone()).unwrap_or_default()
}

/* ---- output ---- */

fn route_line(r: &RouteEntry, d: &Device) -> String {
    let dst = if r.prefix == 0 { "default".to_string() } else { net_str(Some(r.net), r.prefix) };
    if r.connected {
        let ip = d.iface(&r.dev).and_then(|i| i.ip.clone()).unwrap_or_else(|| "null".into());
        return format!("{dst} dev {} proto kernel scope link src {ip}", r.dev);
    }
    match r.via {
        Some(v) => format!("{dst} via {} dev {}", ip_str(v), r.dev),
        None => format!("{dst} dev {} scope link", r.dev),
    }
}

fn show_addr(d: &Device) -> String {
    d.ifaces
        .iter()
        .enumerate()
        .map(|(n, i)| {
            let st = if i.up { "UP" } else { "DOWN" };
            let mut s = format!("{}: {}: <{}> mtu {}\n    link/ether {}", n + 1, i.name, st, i.mtu.unwrap_or(1500), i.mac);
            if let Some(ip) = i.ip.as_deref().filter(|x| !x.is_empty()) {
                s.push_str(&format!("\n    inet {}/{}", ip, i.prefix));
            }
            s
        })
        .collect::<Vec<_>>()
        .join("\n")
}

const HELP: &str = i18n::t!("Available commands:\n  ip addr [add|del|flush ...]    ip link [set <if> up|down]\n  ip route [add|del|get ...]     ip neigh   (or arp -n)\n  ping [-c N] [-t TTL] <ip>      traceroute <ip>\n  curl <ip>[:port]               nc -zv <ip> <port>    nc -l <port>\n  ss -ltn                        sysctl net.ipv4.ip_forward|tcp_rmem|tcp_congestion_control\n  iperf3 <ip> [-n MB]            ip link set <if> txqueuelen N\n  iptables [-t nat] -L|-A|-I|-D|-F|-P ...   hostname   clear");

/* ---- iptables ---- */

/// iptables rule from command-line parameters.
#[derive(Default, Clone)]
struct RuleSpec {
    src: Option<String>,
    dst: Option<String>,
    iif: Option<String>,
    out: Option<String>,
    proto: Option<String>,
    dport: Option<i64>,
    sport: Option<i64>,
    action: Option<String>,
    to: Option<String>,
    state: Option<ConnState>,
    error: Option<String>,
}

fn parse_rule_spec(tokens: &[&str]) -> RuleSpec {
    let mut r = RuleSpec::default();
    let mut i = 0;
    while i < tokens.len() {
        let t = tokens[i];
        let v = tokens.get(i + 1).copied();
        let s = |v: Option<&str>| v.map(|x| x.to_string());
        match t {
            "-s" => {
                r.src = s(v);
                i += 1;
            }
            "-d" => {
                r.dst = s(v);
                i += 1;
            }
            "-i" => {
                r.iif = s(v);
                i += 1;
            }
            "-o" => {
                r.out = s(v);
                i += 1;
            }
            "-p" => {
                r.proto = s(v);
                i += 1;
            }
            "--dport" => {
                r.dport = Some(to_int(v.map(js_num).unwrap_or(f64::NAN)));
                i += 1;
            }
            "--sport" => {
                r.sport = Some(to_int(v.map(js_num).unwrap_or(f64::NAN)));
                i += 1;
            }
            "-j" => {
                r.action = s(v);
                i += 1;
            }
            "--to-destination" => {
                r.to = s(v);
                i += 1;
            }
            "-m" => i += 1,
            "--ctstate" | "--state" => {
                if let Some(v) = v {
                    let parts: Vec<&str> = v.split(',').collect();
                    r.state = if parts.iter().all(|p| *p == "ESTABLISHED" || *p == "RELATED") {
                        Some(ConnState::Established)
                    } else if parts.len() == 1 && parts[0] == "NEW" {
                        Some(ConnState::New)
                    } else {
                        None
                    };
                }
                i += 1;
            }
            _ => {
                r.error = Some(i18n::trf!("iptables: unknown option \"{0}\"", t));
                return r;
            }
        }
        i += 1;
    }
    r
}

fn rule_text(r: &RuleSpecView) -> String {
    let mut parts: Vec<String> = Vec::new();
    let nz = |o: &Option<String>| o.as_deref().filter(|s| !s.is_empty()).map(|s| s.to_string());
    if let Some(x) = nz(r.iif) {
        parts.push(format!("-i {x}"));
    }
    if let Some(x) = nz(r.out) {
        parts.push(format!("-o {x}"));
    }
    if let Some(x) = nz(r.proto) {
        parts.push(format!("-p {x}"));
    }
    if let Some(x) = nz(r.src) {
        parts.push(format!("-s {x}"));
    }
    if let Some(x) = nz(r.dst) {
        parts.push(format!("-d {x}"));
    }
    if let Some(x) = r.sport.filter(|p| *p != 0) {
        parts.push(format!("--sport {x}"));
    }
    if let Some(x) = r.dport.filter(|p| *p != 0) {
        parts.push(format!("--dport {x}"));
    }
    if let Some(s) = r.state {
        parts.push(format!("state {}", if s == ConnState::Established { "ESTABLISHED,RELATED" } else { "NEW" }));
    }
    if let Some(x) = nz(r.to) {
        parts.push(format!("to:{x}"));
    }
    if parts.is_empty() {
        "anywhere".into()
    } else {
        parts.join(" ")
    }
}

/// Rule fields for output (shared by filter and nat).
struct RuleSpecView<'a> {
    iif: &'a Option<String>,
    out: &'a Option<String>,
    proto: &'a Option<String>,
    src: &'a Option<String>,
    dst: &'a Option<String>,
    sport: Option<i64>,
    dport: Option<i64>,
    state: Option<ConnState>,
    to: &'a Option<String>,
}

fn iptables(d: &mut Device, tokens: &[&str]) -> CmdResult {
    let mut table = "filter";
    let mut i = 0;
    if tokens.first() == Some(&"-t") {
        table = tokens.get(1).copied().unwrap_or("undefined");
        i = 2;
    }
    if table != "nat" && table != "filter" {
        return out(i18n::trf!("iptables: table \"{0}\" is not supported", table));
    }
    let op = tokens.get(i).copied();
    let chain = tokens.get(i + 1).copied();
    let rest: &[&str] = if tokens.len() > i + 2 { &tokens[i + 2..] } else { &[] };
    let nat = table == "nat";

    if op == Some("-L") || op == Some("-S") {
        let chains: &[&str] = if nat { &["PREROUTING", "POSTROUTING"] } else { &["FORWARD"] };
        let want: Vec<&str> = match chain {
            Some(c) if !c.is_empty() && !c.starts_with('-') => vec![c],
            _ => chains.to_vec(),
        };
        let mut lines: Vec<String> = Vec::new();
        for c in want {
            if !chains.contains(&c) {
                return out(i18n::trf!("iptables: no chain \"{0}\" in table {1}", c, table));
            }
            if nat {
                lines.push(format!("Chain {c} (policy ACCEPT)"));
                let mut k = 0;
                for n in d.nat.iter().filter(|n| n.chain.as_str() == c) {
                    k += 1;
                    let v = RuleSpecView {
                        iif: &n.iif,
                        out: &n.out,
                        proto: &n.proto,
                        src: &n.src,
                        dst: &n.dst,
                        sport: n.sport,
                        dport: n.dport,
                        state: n.state,
                        to: &n.to,
                    };
                    lines.push(format!("{}  {}  {}", k, n.action.as_str(), rule_text(&v)));
                }
            } else {
                lines.push(format!("Chain {c} (policy {})", d.fw.policy.as_str()));
                for (k, n) in d.fw.rules.iter().enumerate() {
                    let v = RuleSpecView {
                        iif: &n.iif,
                        out: &n.out,
                        proto: &n.proto,
                        src: &n.src,
                        dst: &n.dst,
                        sport: n.sport,
                        dport: n.dport,
                        state: n.state,
                        to: &n.to,
                    };
                    lines.push(format!("{}  {}  {}", k + 1, n.action.as_str(), rule_text(&v)));
                }
            }
        }
        return out(lines.join("\n"));
    }
    if let Some(bad) = no(d) {
        return out(bad);
    }

    if op == Some("-F") {
        if nat {
            d.nat.clear();
        } else {
            d.fw.rules.clear();
        }
        return changed("");
    }
    if op == Some("-P") {
        if nat || chain != Some("FORWARD") {
            return out(i18n::tr("iptables: a policy can only be set for FORWARD"));
        }
        let pol = rest.first().and_then(|p| FwAction::parse(p)).filter(|p| *p != FwAction::Reject);
        let Some(pol) = pol else { return out(i18n::tr("iptables: the policy is ACCEPT or DROP")) };
        d.fw.policy = pol;
        return changed("");
    }
    if op == Some("-A") || op == Some("-I") || op == Some("-D") {
        let op = op.unwrap_or("");
        let mut spec = rest;
        let mut pos = 0.0;
        if op == "-I" {
            if let Some(f) = rest.first().filter(|f| !f.is_empty() && f.bytes().all(|b| b.is_ascii_digit())) {
                pos = js_num(f) - 1.0;
                spec = &rest[1..];
            }
        }
        let r = parse_rule_spec(spec);
        if let Some(e) = r.error {
            return out(e);
        }
        let Some(action) = r.action.clone().filter(|a| !a.is_empty()) else { return out(i18n::tr("iptables: no target specified (-j)")) };
        let chain_s = chain.unwrap_or("undefined");
        if nat {
            let ch = match chain_s {
                "PREROUTING" => NatChain::Prerouting,
                "POSTROUTING" => NatChain::Postrouting,
                _ => return out(i18n::tr("iptables: the nat table models the PREROUTING and POSTROUTING chains")),
            };
            if ch == NatChain::Postrouting && action != "MASQUERADE" {
                return out(i18n::tr("iptables: POSTROUTING supports the MASQUERADE target"));
            }
            if ch == NatChain::Prerouting && (action != "DNAT" || r.to.as_deref().map(|t| t.is_empty()).unwrap_or(true)) {
                return out(i18n::tr("iptables: PREROUTING needs the target DNAT --to-destination address[:port]"));
            }
            if let Some(to) = r.to.as_deref().filter(|t| !t.is_empty()) {
                if parse_ip(to.split(':').next().unwrap_or("")).is_none() {
                    return out(i18n::trf!("iptables: invalid address \"{0}\"", to));
                }
            }
            let act = if action == "MASQUERADE" { NatAction::Masquerade } else { NatAction::Dnat };
            let rule = NatRule {
                chain: ch,
                action: act,
                iif: r.iif.clone(),
                out: r.out.clone(),
                src: r.src.clone(),
                dst: r.dst.clone(),
                proto: r.proto.clone(),
                sport: r.sport,
                dport: r.dport,
                to: r.to.clone(),
                state: r.state,
            };
            if op == "-D" {
                let Some(k) = d.nat.iter().position(|n| *n == rule) else { return out(i18n::tr("iptables: no such rule")) };
                d.nat.remove(k);
            } else if op == "-I" {
                let first = d.nat.iter().position(|n| n.chain == ch);
                match first {
                    None => d.nat.push(rule),
                    Some(f) => splice_at(&mut d.nat, f as f64 + pos, rule),
                }
            } else {
                d.nat.push(rule);
            }
            return changed("");
        }
        if chain_s != "FORWARD" {
            return out(i18n::tr("iptables: this simulator filters only the FORWARD chain"));
        }
        let Some(act) = FwAction::parse(&action) else { return out(i18n::tr("iptables: the target is ACCEPT, DROP or REJECT")) };
        let fw = FwRule {
            action: act,
            src: r.src.clone(),
            dst: r.dst.clone(),
            proto: r.proto.clone(),
            sport: r.sport,
            dport: r.dport,
            iif: r.iif.clone(),
            out: r.out.clone(),
            state: r.state,
            to: r.to.clone(),
        };
        if op == "-D" {
            let Some(k) = d.fw.rules.iter().position(|n| *n == fw) else { return out(i18n::tr("iptables: no such rule")) };
            d.fw.rules.remove(k);
        } else if op == "-I" {
            splice_at(&mut d.fw.rules, pos, fw);
        } else {
            d.fw.rules.push(fw);
        }
        return changed("");
    }
    out(i18n::tr("iptables: unknown operation. Example: iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE"))
}

/* ---- names: hosts → DNS query to the resolver ---- */

/// Resolved name: address, source ("hosts") and DNS probe for animation and log.
#[derive(Clone, Debug)]
pub struct Resolved {
    pub ip: u32,
    pub from: Option<&'static str>,
    pub run: Option<ProbeRun>,
}

/// Resolution error: text and DNS probe (if there was one).
#[derive(Clone, Debug)]
pub struct ResolveErr {
    pub err: String,
    pub run: Option<ProbeRun>,
}

fn rerr(s: impl Into<String>, run: Option<ProbeRun>) -> ResolveErr {
    ResolveErr { err: s.into(), run }
}

/// Name or address -> address (hosts, then a DNS query to the device's resolver).
pub fn to_ip(state: &mut NetState, dev_id: &str, arg: &str) -> Result<Resolved, ResolveErr> {
    let Some(d) = state.devices.get(dev_id) else { return Err(rerr(i18n::trf!("no device \"{0}\"", dev_id), None)) };
    let l = local_lookup(d, arg);
    let ask = match l {
        LocalLookup::Ip(Some(ip), from) => return Ok(Resolved { ip, from, run: None }),
        LocalLookup::Error(e) => return Err(rerr(format!("Temporary failure in name resolution ({e})"), None)),
        LocalLookup::Ip(None, _) | LocalLookup::Ask(None) => {
            return Err(rerr(i18n::tr("Temporary failure in name resolution (no DNS server in /etc/resolv.conf)"), None));
        }
        LocalLookup::Ask(Some(a)) => a,
    };
    let run = dns1(state, dev_id, ask, DnsQuestion { name: fqdn(arg), typ: "A".into() }, true);
    let dns = match (&run.status, &run.dns) {
        (ProbeStatus::Reply, Some(dns)) => dns.clone(),
        _ => return Err(rerr(i18n::tr("Temporary failure in name resolution (the DNS server does not respond)"), Some(run))),
    };
    match answer_ip(Some(&dns)) {
        None => {
            let msg = if dns.rcode == Some(Rcode::NxDomain) {
                "Name or service not known (NXDOMAIN)".to_string()
            } else {
                i18n::trf!("name did not resolve ({0})", dns.rcode.map(|r| r.as_str()).unwrap_or("undefined"))
            };
            Err(rerr(msg, Some(run)))
        }
        Some(ip) => Ok(Resolved { ip, from: None, run: Some(run) }),
    }
}

fn do_dig(state: &mut NetState, dev_id: &str, a: &[&str], nslookup: bool) -> CmdResult {
    let resolver = state.devices.get(dev_id).and_then(|d| d.resolver.clone());
    let at = a.iter().find(|x| x.starts_with('@')).copied();
    let rest: Vec<&str> = a.iter().copied().filter(|x| !x.starts_with('@')).collect();
    let name = rest.first().copied();
    let mut typ = rest.get(1).copied().unwrap_or("A").to_uppercase();
    let mut server = match at {
        Some(at) => parse_ip(&at[1..]),
        None => match resolver.as_deref().filter(|r| !r.is_empty()) {
            Some(r) => parse_ip(r),
            None => None,
        },
    };
    if nslookup {
        if let Some(r1) = rest.get(1).filter(|r| !r.is_empty()) {
            if let Some(ip) = parse_ip(r1) {
                server = Some(ip);
                typ = "A".into();
            }
        }
    }
    let Some(name) = name.filter(|n| !n.is_empty()) else {
        return out(i18n::tr("dig: specify a name: dig www.example.org [A|CNAME|NS] [@server]"));
    };
    let Some(server) = server else {
        return out(i18n::tr("dig: no DNS server: add \"nameserver …\" to /etc/resolv.conf or specify @server"));
    };
    let run = dns1(state, dev_id, server, DnsQuestion { name: fqdn(name), typ: typ.clone() }, true);
    let dns = match (&run.status, &run.dns) {
        (ProbeStatus::Reply, Some(dns)) => dns.clone(),
        _ => return probe(i18n::trf!(";; connection failed: DNS server {0} is not responding (timed out)", ip_str(server)), Some(run)),
    };
    let text =
        [i18n::trf!(";; query to {0}, question \"{1} {2}\", time {3}", ip_str(server), fqdn(name), typ, fmt_ms(run.rtt_us)), fmt_dns(&dns)].join("\n");
    probe(text, Some(run))
}

fn dns_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub == Some("show") || sub.is_none() {
        let Some(dns) = &d.dns else { return out(i18n::tr("The DNS server is not enabled on this device (dns enable)")) };
        let mut l = vec![i18n::trf!("mode: {0}", if dns.recursive { i18n::tr("recursive resolver") } else { i18n::tr("authoritative server") })];
        if !dns.zones.is_empty() {
            l.push(i18n::trf!("zones: {0}", dns.zones.join(", ")));
        }
        if !dns.roots.is_empty() {
            l.push(i18n::trf!("root servers: {0}", dns.roots.join(", ")));
        }
        for r in &dns.records {
            l.push(format!("{}.  {}  IN  {}  {}", r.name, r.ttl.unwrap_or(300), r.typ, r.value));
        }
        for x in &dns.delegations {
            l.push(i18n::trf!("delegation: {0} → NS {1}", x.zone, x.ns));
        }
        return out(l.join("\n"));
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.dns.is_none() {
            d.dns = Some(new_dns());
        }
        return changed(i18n::tr("DNS server enabled (listening on udp/53)"));
    }
    let Some(dns) = d.dns.as_mut() else { return out(i18n::tr("enable the DNS server first: dns enable")) };
    match sub {
        "recursive" => {
            dns.recursive = g(1) != Some("off");
            changed(i18n::trf!("recursion: {0}", if dns.recursive { i18n::tr("enabled") } else { i18n::tr("disabled") }))
        }
        "root" => {
            if parse_ip(g(1).unwrap_or("")).is_none() {
                return out(i18n::tr("dns root <root server ip>"));
            }
            dns.roots = vec![g(1).unwrap_or("").to_string()];
            changed(i18n::tr("root server set"))
        }
        "zone" => {
            let z = fqdn(g(1).unwrap_or(""));
            if z.is_empty() {
                return out(i18n::tr("dns zone <zone>"));
            }
            if !dns.zones.contains(&z) {
                dns.zones.push(z.clone());
            }
            changed(i18n::trf!("zone {0} is served by this server", z))
        }
        "add" => {
            let name = g(1);
            let typ = g(2).unwrap_or("").to_uppercase();
            let v: Vec<&str> = if a.len() > 3 { a[3..].to_vec() } else { vec![] };
            let value = v.first().copied();
            let (Some(name), Some(value)) = (name.filter(|n| !n.is_empty()), value.filter(|v| !v.is_empty())) else {
                return out(i18n::tr("dns add <name> <A|CNAME|MX|TXT> <value> [ttl]"));
            };
            if !["A", "CNAME", "NS", "MX", "TXT"].contains(&typ.as_str()) {
                return out(i18n::tr("dns add <name> <A|CNAME|MX|TXT> <value> [ttl]"));
            }
            if typ == "A" && parse_ip(value).is_none() {
                return out(i18n::trf!("invalid IPv4 address \"{0}\"", value));
            }
            let ttl = num_or(v.get(1).copied(), 300.0);
            dns.records.push(DnsRecord {
                name: fqdn(name),
                typ: typ.clone(),
                value: if typ == "CNAME" { fqdn(value) } else { value.to_string() },
                ttl: Some(ttl.clamp(0.0, u32::MAX as f64) as u32),
            });
            changed(i18n::tr("record added"))
        }
        "del" => {
            let name = fqdn(g(1).unwrap_or(""));
            let t = g(2).filter(|x| !x.is_empty()).map(|x| x.to_uppercase());
            let n = dns.records.len();
            dns.records.retain(|r| !(fqdn(&r.name) == name && t.as_ref().map(|t| *t == r.typ).unwrap_or(true)));
            if dns.records.len() < n {
                changed(i18n::tr("record removed"))
            } else {
                out(i18n::tr("no such record"))
            }
        }
        "delegate" => {
            if g(1).map(|x| x.is_empty()).unwrap_or(true) || parse_ip(g(2).unwrap_or("")).is_none() {
                return out(i18n::tr("dns delegate <zone> <name server ip>"));
            }
            let z = fqdn(g(1).unwrap_or(""));
            dns.delegations.retain(|x| fqdn(&x.zone) != z);
            dns.delegations.push(DnsDelegation { zone: z.clone(), ns: g(2).unwrap_or("").to_string() });
            changed(i18n::trf!("zone {0} delegated to {1}", z, g(2).unwrap_or("")))
        }
        "undelegate" => {
            let z = fqdn(g(1).unwrap_or(""));
            dns.delegations.retain(|x| fqdn(&x.zone) != z);
            changed(i18n::tr("delegation removed"))
        }
        _ => out(i18n::tr("dns show | enable | recursive on|off | root <ip> | zone <z> | add … | del … | delegate <zone> <ip> | undelegate <zone>")),
    }
}

/// `echo ... > /etc/resolv.conf` and `echo ... >> /etc/hosts`; `None` means the line is not about these files.
fn file_write(d: &mut Device, line: &str) -> Option<CmdResult> {
    let t = line.trim();
    let after_echo = t.strip_prefix("echo")?;
    if !after_echo.starts_with(char::is_whitespace) {
        return None;
    }
    let (path, rest) = if let Some(r) = after_echo.strip_suffix("/etc/resolv.conf") {
        ("resolv", r)
    } else if let Some(r) = after_echo.strip_suffix("/etc/hosts") {
        ("hosts", r)
    } else {
        return None;
    };
    let rest = rest.trim_end();
    let (op, body) = if let Some(b) = rest.strip_suffix(">>") {
        (">>", b)
    } else if let Some(b) = rest.strip_suffix('>') {
        (">", b)
    } else {
        return None;
    };
    let body = body.trim();
    if let Some(bad) = no(d) {
        return Some(out(bad));
    }
    let mut b = body.to_string();
    if b.starts_with('"') || b.starts_with('\'') {
        b.remove(0);
    }
    if b.ends_with('"') || b.ends_with('\'') {
        b.pop();
    }
    let body = b.trim().to_string();
    if path == "resolv" {
        let ip = body
            .strip_prefix("nameserver")
            .filter(|r| r.starts_with(char::is_whitespace))
            .map(|r| r.trim_start())
            .filter(|r| !r.is_empty() && !r.contains(char::is_whitespace));
        let Some(ip) = ip.filter(|ip| parse_ip(ip).is_some()) else {
            return Some(out(i18n::tr("resolv.conf needs a line like: nameserver 10.0.0.53")));
        };
        d.resolver = Some(ip.to_string());
        return Some(changed(""));
    }
    let toks: Vec<&str> = body.split_whitespace().collect();
    if toks.len() != 2 || parse_ip(toks[0]).is_none() {
        return Some(out(i18n::tr("hosts needs a line like: 10.0.0.5 name")));
    }
    if op == ">" {
        d.hosts = OrdMap::new();
    }
    d.hosts.insert(fqdn(toks[1]), toks[0].to_string());
    Some(changed(""))
}

fn do_curl(state: &mut NetState, dev_id: &str, a: &[&str]) -> CmdResult {
    let mut method = "GET".to_string();
    let mut proxy: Option<String> = None;
    let mut headers: OrdMap<String> = OrdMap::new();
    let mut flags: Vec<char> = Vec::new();
    let mut url: Option<String> = None;
    let unq = |s: &str| {
        let mut x = s.to_string();
        if x.starts_with('"') || x.starts_with('\'') {
            x.remove(0);
        }
        if x.ends_with('"') || x.ends_with('\'') {
            x.pop();
        }
        x
    };
    let mut i = 0;
    while i < a.len() {
        let x = a[i];
        if x == "-x" {
            i += 1;
            proxy = a.get(i).map(|s| s.to_string());
        } else if x == "-X" {
            i += 1;
            method = a.get(i).copied().unwrap_or("GET").to_uppercase();
        } else if x == "-H" {
            i += 1;
            let h = unq(a.get(i).copied().unwrap_or(""));
            let mut parts = h.split(':');
            let k = parts.next().unwrap_or("").trim().to_lowercase();
            let v: Vec<&str> = parts.collect();
            headers.insert(k, v.join(":").trim().to_string());
        } else if x.starts_with('-') {
            flags.extend(x.chars().skip(1));
        } else {
            url = Some(unq(x));
        }
        i += 1;
    }
    let Some(mut url) = url.filter(|u| !u.is_empty()) else {
        return out(i18n::tr("curl: specify a URL, for example curl -v http://www.example.org/"));
    };
    let lower = url.to_lowercase();
    if !(lower.starts_with("http://") || lower.starts_with("https://")) {
        url = format!("http://{url}");
    }
    let head = flags.contains(&'I');
    if head {
        method = "HEAD".into();
    }
    let r = http_fetch(state, dev_id, &FetchOptions { url, method: method.clone(), follow: flags.contains(&'L'), headers, proxy });
    let text = fmt_curl(&r, flags.contains(&'v'), head, &method);
    CmdResult { out: text, probe: r.run.clone(), http: Some(r), ..Default::default() }
}

fn web_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        let Some(http) = &d.http else { return out(i18n::tr("the web server is not enabled (web enable)")) };
        let rows: Vec<String> = http
            .routes
            .iter()
            .map(|r| {
                let loc = r.location.as_deref().filter(|l| !l.is_empty()).map(|l| format!(" → {l}")).unwrap_or_default();
                let hs = if r.headers.is_empty() {
                    String::new()
                } else {
                    format!("  {}", r.headers.iter().map(|(k, v)| format!("{k}: {v}")).collect::<Vec<_>>().join("; "))
                };
                format!("{}  {}{}{}", r.path, r.status.unwrap_or(200), loc, hs)
            })
            .collect();
        return out(if rows.is_empty() { i18n::tr("(no routes)").to_string() } else { rows.join("\n") });
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.http.is_none() {
            d.http = Some(new_http());
        }
        if !d.services.iter().any(|s| s.proto == Proto::Tcp && s.port == 80) {
            d.services.push(Service { proto: Proto::Tcp, port: 80, bind: None, name: None });
        }
        return changed(i18n::tr("web server enabled on tcp/80"));
    }
    let Some(http) = d.http.as_mut() else { return out(i18n::tr("first: web enable")) };
    let path = g(1);
    match sub {
        "route" => {
            let status = js_num(g(2).unwrap_or("200"));
            let ok_path = path.map(|p| p.starts_with('/')).unwrap_or(false);
            if !ok_path || !(status >= 100.0 && status < 600.0) {
                return out(i18n::tr("web route /path <code> [response text]"));
            }
            let path = path.unwrap_or("");
            http.routes.retain(|r| r.path != path);
            let body = if a.len() > 3 { a[3..].join(" ") } else { String::new() };
            http.routes.push(HttpRoute { path: path.into(), status: Some(status as u32), body: if body.is_empty() { None } else { Some(body) }, ..Default::default() });
            changed(i18n::trf!("route {0} → {1}", path, num_str(status)))
        }
        "redirect" => {
            let status = js_num(g(2).unwrap_or("301"));
            if path.map(|p| p.is_empty()).unwrap_or(true) || g(3).map(|x| x.is_empty()).unwrap_or(true) || ![301.0, 302.0, 307.0, 308.0].contains(&status) {
                return out(i18n::tr("web redirect /old <301|302|307|308> /new"));
            }
            let path = path.unwrap_or("");
            http.routes.retain(|r| r.path != path);
            http.routes.push(HttpRoute { path: path.into(), status: Some(status as u32), location: g(3).map(|s| s.to_string()), ..Default::default() });
            changed(format!("{path} → {} → {}", num_str(status), g(3).unwrap_or("")))
        }
        "header" => {
            let Some(r) = http.routes.iter_mut().find(|x| Some(x.path.as_str()) == path) else { return out(i18n::trf!("no route {0}", und(path))) };
            let Some(name) = g(2).filter(|x| !x.is_empty()) else { return out(i18n::tr("web header /path Name value")) };
            r.headers.insert(name.to_lowercase(), if a.len() > 3 { a[3..].join(" ") } else { String::new() });
            changed(i18n::tr("header added"))
        }
        "protocol" => {
            let proto = match g(1) {
                Some("h1") => HttpProto::H1,
                Some("h2") => HttpProto::H2,
                Some("h3") => HttpProto::H3,
                _ => return out("web protocol h1|h2|h3"),
            };
            http.protocol = Some(proto);
            let tail = if proto == HttpProto::H3 { i18n::tr(" (needs open UDP/443)") } else { "" };
            changed(i18n::trf!("the server offers {0}{1}", proto.name(), tail))
        }
        "etag" => {
            let r = http.routes.iter_mut().find(|x| Some(x.path.as_str()) == path);
            let (Some(r), Some(e)) = (r, g(2).filter(|x| !x.is_empty())) else { return out(i18n::tr("web etag /path value")) };
            r.etag = Some(e.to_string());
            changed(i18n::tr("ETag set"))
        }
        "del" => {
            http.routes.retain(|r| Some(r.path.as_str()) != path);
            changed(i18n::tr("route removed"))
        }
        _ => out(i18n::tr("web show | enable | protocol h1|h2|h3 | route /p code [text] | redirect /p code /to | header /p Name val | etag /p val | del /p")),
    }
}

fn tls_admin(pki: &Pki, d: &mut Device, a: &[&str]) -> CmdResult {
    let cas = &pki.cas;
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        let Some(tls) = &d.tls else { return out(i18n::tr("TLS is not enabled on this device (tls enable)")) };
        let c = &tls.cert;
        let chain = if tls.chain.is_empty() { i18n::tr("(its own certificate only)").to_string() } else { tls.chain.join(" → ") };
        return out([
            i18n::trf!("certificate: CN={0}", c.cn),
            format!("  SAN: {}", c.san.join(", ")),
            i18n::trf!("  issuer: {0}", c.issuer),
            i18n::trf!("  valid until: {0} (today {1})", c.not_after, NOW),
            i18n::trf!("chain the server sends: {0}", chain),
            i18n::trf!("TLS versions: {0}", tls.versions.join(", ")),
        ]
        .join("\n"));
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.tls.is_none() {
            d.tls = Some(new_tls());
        }
        if !d.services.iter().any(|s| s.proto == Proto::Tcp && s.port == 443) {
            d.services.push(Service { proto: Proto::Tcp, port: 443, bind: None, name: None });
        }
        return changed(i18n::tr("TLS enabled on tcp/443"));
    }
    let Some(tls) = d.tls.as_mut() else { return out(i18n::tr("first: tls enable")) };
    if sub == "cert" && g(1) == Some("new") {
        let rest: Vec<&str> = if a.len() > 2 { a[2..].to_vec() } else { vec![] };
        let iss = index_of(&rest, "--issuer");
        let days = index_of(&rest, "--days");
        let issuer = if iss >= 0 { rest.get((iss + 1) as usize).copied() } else { None };
        let n = if days >= 0 { js_num(rest.get((days + 1) as usize).copied().unwrap_or("undefined")) } else { 90.0 };
        let names: Vec<&str> = rest
            .iter()
            .enumerate()
            .filter(|(i, x)| !x.starts_with("--") && (iss < 0 || *i as isize != iss + 1) && (days < 0 || *i as isize != days + 1))
            .map(|(_, x)| *x)
            .collect();
        let issuer = issuer.filter(|i| !i.is_empty());
        let (Some(issuer), false) = (issuer, names.is_empty()) else {
            return out(i18n::tr("tls cert new <name> [extra names…] --issuer <CA> --days <N>"));
        };
        if !(n >= 1.0) {
            return out(i18n::tr("tls cert new <name> [extra names…] --issuer <CA> --days <N>"));
        }
        if !cas.contains_key(issuer) {
            let list: Vec<&str> = cas.keys().map(|k| k.as_str()).collect();
            return out(i18n::trf!("unknown issuer \"{0}\" (available: {1})", issuer, list.join(", ")));
        }
        tls.cert = TlsCert {
            cn: names[0].to_string(),
            san: names.iter().map(|s| s.to_string()).collect(),
            issuer: issuer.to_string(),
            not_after: add_days(n),
        };
        return changed(i18n::trf!("issued certificate CN={0} SAN={1} issuer {2} until {3}", names[0], names.join(","), issuer, tls.cert.not_after));
    }
    if sub == "chain" {
        if g(1) == Some("clear") {
            tls.chain.clear();
            return changed(i18n::tr("chain cleared: the server sends only its own certificate"));
        }
        if g(1) == Some("add") {
            let ca = g(2).unwrap_or("undefined");
            if !cas.contains_key(ca) {
                return out(i18n::trf!("unknown CA \"{0}\"", g(2).unwrap_or("")));
            }
            if !tls.chain.iter().any(|x| x == ca) {
                tls.chain.push(ca.to_string());
            }
            return changed(i18n::trf!("{0} added to the chain", ca));
        }
    }
    if sub == "versions" {
        let v: Vec<String> = g(1).unwrap_or("").split(',').filter(|x| !x.is_empty()).map(|x| x.to_string()).collect();
        if v.is_empty() || v.iter().any(|x| !["1.0", "1.1", "1.2", "1.3"].contains(&x.as_str())) {
            return out("tls versions 1.2,1.3");
        }
        tls.versions = v.clone();
        return changed(i18n::trf!("versions: {0}", v.join(", ")));
    }
    out(i18n::tr("tls show | enable | cert new <name> [names…] --issuer <CA> --days N | chain add <CA> | chain clear | versions 1.2,1.3"))
}

fn trust_admin(pki: &Pki, d: &mut Device, a: &[&str]) -> CmdResult {
    let cas = &pki.cas;
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        let t = d.trust.clone().unwrap_or_else(default_trust);
        return out(i18n::trf!("trusted root CAs: {0}", t.join(", ")));
    }
    if let Some(bad) = no(d) {
        return out(bad);
    }
    match sub.unwrap_or("") {
        "add" => {
            let ca = g(1).unwrap_or("undefined");
            if !cas.contains_key(ca) {
                let list: Vec<&str> = cas.keys().map(|k| k.as_str()).collect();
                return out(i18n::trf!("unknown CA \"{0}\" (available: {1})", g(1).unwrap_or(""), list.join(", ")));
            }
            let mut t = d.trust.clone().unwrap_or_else(default_trust);
            if !t.iter().any(|x| x == ca) {
                t.push(ca.to_string());
            }
            d.trust = Some(t);
            changed(i18n::trf!("root CA {0} added to the trust store", ca))
        }
        "del" => {
            let t: Vec<String> = d.trust.clone().unwrap_or_else(default_trust).into_iter().filter(|x| Some(x.as_str()) != g(1)).collect();
            d.trust = Some(t);
            changed(i18n::tr("removed from the store"))
        }
        _ => out("trust show | add <CA> | del <CA>"),
    }
}

fn proxy_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        return out(match &d.proxy {
            Some(p) => i18n::trf!("proxy on tcp/{0}; denied: {1}", p.port.unwrap_or(3128), if p.deny.is_empty() { i18n::tr("(none)").to_string() } else { p.deny.join(", ") }),
            None => i18n::tr("the proxy is not enabled (proxy enable)").to_string(),
        });
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.proxy.is_none() {
            d.proxy = Some(ProxyConfig { port: Some(3128), deny: vec![] });
        }
        let port = d.proxy.as_ref().and_then(|p| p.port).unwrap_or(3128);
        if !d.services.iter().any(|s| s.proto == Proto::Tcp && s.port == port) {
            d.services.push(Service { proto: Proto::Tcp, port, bind: None, name: None });
        }
        return changed(i18n::trf!("HTTP proxy enabled on tcp/{0}", port));
    }
    let Some(p) = d.proxy.as_mut() else { return out(i18n::tr("first: proxy enable")) };
    if let Some(h) = g(1).filter(|x| !x.is_empty()) {
        if sub == "deny" {
            if !p.deny.iter().any(|x| x == h) {
                p.deny.push(h.to_string());
            }
            return changed(i18n::trf!("{0} denied", h));
        }
        if sub == "allow" {
            p.deny.retain(|x| x != h);
            return changed(i18n::trf!("{0} allowed", h));
        }
    }
    out(i18n::tr("proxy show | enable | deny <host> | allow <host>"))
}

fn lb_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        let Some(lb) = &d.lb else { return out(i18n::tr("there is no load balancer on this node")) };
        let mut l = vec![
            i18n::trf!("virtual address {0}:{1}", lb.vip, lb.port),
            i18n::trf!("algorithm: {0}", if lb.algo == Some(LbAlgo::Hash) {
                    i18n::tr("hash by client address (sticky)")
                } else {
                    i18n::tr("round robin")
                }),
            i18n::trf!("health check: {0}", if lb.health { i18n::tr("enabled") } else { i18n::tr("disabled") }),
        ];
        l.extend(lb.backends.iter().map(|b| i18n::trf!("  server {0}:{1}", b.ip, b.port)));
        return out(l.join("\n"));
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let Some(lb) = d.lb.as_mut() else { return out(i18n::tr("there is no load balancer on this node")) };
    match sub.unwrap_or("") {
        "add" => {
            let spec = g(1).unwrap_or("");
            let mut parts = spec.split(':');
            let ip = parts.next().unwrap_or("");
            let port = parts.next();
            if parse_ip(ip).is_none() {
                return out(i18n::tr("lb add <ip>:<port>"));
            }
            let p = match port {
                Some(p) => to_int(js_num(p)),
                None => lb.port,
            };
            if lb.backends.iter().any(|b| b.ip == ip && b.port == p) {
                return out(i18n::tr("this server is already in the pool"));
            }
            lb.backends.push(LbBackend { ip: ip.to_string(), port: p });
            changed(i18n::trf!("server {0}:{1} added to the pool", ip, port.map(|s| s.to_string()).unwrap_or_else(|| lb.port.to_string())))
        }
        "del" => {
            let n = lb.backends.len();
            let ip = g(1).unwrap_or("").split(':').next().unwrap_or("").to_string();
            lb.backends.retain(|b| b.ip != ip);
            if lb.backends.len() < n {
                changed(i18n::tr("removed from the pool"))
            } else {
                out(i18n::tr("no such server"))
            }
        }
        "algo" => match g(1) {
            Some("rr") => {
                lb.algo = Some(LbAlgo::Rr);
                changed(i18n::tr("algorithm: rr"))
            }
            Some("hash") => {
                lb.algo = Some(LbAlgo::Hash);
                changed(i18n::tr("algorithm: hash"))
            }
            _ => out(i18n::tr("lb algo rr (round robin) | hash (sticky by client address)")),
        },
        "health" => {
            lb.health = g(1) != Some("off");
            changed(i18n::trf!("health check {0}", if lb.health { i18n::tr("enabled") } else { i18n::tr("disabled") }))
        }
        _ => out(i18n::tr("lb show | add ip:port | del ip | algo rr|hash | health on|off")),
    }
}

fn rproxy_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        return out(match &d.rproxy {
            Some(rp) => {
                let rows: Vec<String> = rp
                    .rules
                    .iter()
                    .map(|r| {
                        format!(
                            "{}{} → {}{}",
                            r.host.as_deref().unwrap_or("*"),
                            r.path.as_deref().unwrap_or("/"),
                            r.backend,
                            if r.cache { i18n::tr("  [cache]") } else { "" }
                        )
                    })
                    .collect();
                if rows.is_empty() {
                    i18n::tr("(no rules)").to_string()
                } else {
                    rows.join("\n")
                }
            }
            None => i18n::tr("the reverse proxy is not enabled (rproxy enable)").to_string(),
        });
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.rproxy.is_none() {
            d.rproxy = Some(RProxyConfig::default());
        }
        if !d.services.iter().any(|s| s.proto == Proto::Tcp && s.port == 80) {
            d.services.push(Service { proto: Proto::Tcp, port: 80, bind: None, name: None });
        }
        return changed(i18n::tr("reverse proxy enabled on tcp/80"));
    }
    let Some(rp) = d.rproxy.as_mut() else { return out(i18n::tr("first: rproxy enable")) };
    match sub {
        "add" => {
            let (host, path, backend) = (g(1), g(2), g(3));
            let ok = path.map(|p| p.starts_with('/')).unwrap_or(false)
                && backend.map(|b| !b.is_empty() && parse_ip(b.split(':').next().unwrap_or("")).is_some()).unwrap_or(false);
            if !ok {
                return out(i18n::tr("rproxy add <host|*> </path> <ip:port>"));
            }
            let (path, backend) = (path.unwrap_or(""), backend.unwrap_or(""));
            rp.rules.retain(|r| !(r.host.as_deref().unwrap_or("*") == host.unwrap_or("undefined") && r.path.as_deref() == Some(path)));
            rp.rules.push(RProxyRule {
                host: if host == Some("*") { None } else { host.map(|s| s.to_string()) },
                path: Some(path.to_string()),
                backend: backend.to_string(),
                cache: false,
            });
            changed(i18n::trf!("rule: {0}{1} → {2}", und(host), path, backend))
        }
        "del" => {
            rp.rules.retain(|r| r.path.as_deref() != g(1));
            changed(i18n::tr("rule removed"))
        }
        "cache" => {
            let Some(r) = rp.rules.iter_mut().find(|x| x.path.as_deref() == g(1)) else {
                return out(i18n::trf!("no rule for {0}", g(1).unwrap_or("")));
            };
            r.cache = g(2) != Some("off");
            let on = r.cache;
            changed(i18n::trf!("cache for {0}: {1}", g(1).unwrap_or("undefined"), if on { i18n::tr("on") } else { i18n::tr("off") }))
        }
        _ => out(i18n::tr("rproxy show | enable | add <host|*> /path ip:port | del /path | cache /path on|off")),
    }
}

fn ssh_client(state: &mut NetState, dev_id: &str, cmd: &str, a: &[&str]) -> CmdResult {
    if cmd == "ssh-keygen" {
        let Some(d) = state.devices.get_mut(dev_id) else { return out("") };
        if a.first() == Some(&"-R") {
            if let Some(h) = a.get(1) {
                d.known_hosts.remove(h);
            } else {
                d.known_hosts.remove("undefined");
            }
            return changed(i18n::trf!("address {0} removed from known_hosts", a.get(1).copied().unwrap_or("")));
        }
        if a.first() == Some(&"-l") {
            return out(match &d.ssh_key {
                Some(k) if !k.is_empty() => format!("256 {k} (ED25519)"),
                _ => i18n::tr("no key: ssh-keygen").to_string(),
            });
        }
        if let Some(bad) = no(d) {
            return out(bad);
        }
        let k = make_key(d);
        d.ssh_key = Some(k.clone());
        return changed(i18n::trf!("ED25519 key pair created. Fingerprint: {0}", k));
    }
    let mut pass: Option<String> = None;
    let mut jump: Option<String> = None;
    let mut no_key = false;
    let mut rest: Vec<&str> = Vec::new();
    let mut i = 0;
    while i < a.len() {
        if a[i] == "-P" || a[i] == "-p" {
            i += 1;
            pass = a.get(i).map(|s| s.to_string());
        } else if a[i] == "-J" {
            i += 1;
            jump = a.get(i).map(|s| s.to_string());
        } else if a[i] == "-o" && a.get(i + 1) == Some(&"PubkeyAuthentication=no") {
            no_key = true;
            i += 1;
        } else {
            rest.push(a[i]);
        }
        i += 1;
    }
    let target = rest.last().copied().unwrap_or("");
    let (user, host): (Option<&str>, &str) = if target.contains('@') {
        let mut p = target.split('@');
        (p.next(), p.next().unwrap_or(""))
    } else {
        (None, target)
    };
    let (Some(user), false) = (user.filter(|u| !u.is_empty()), host.is_empty()) else {
        return out(i18n::trf!("{0}: specify a user and a host: {0} alice@10.0.0.5", cmd));
    };
    let res = match to_ip(state, dev_id, host) {
        Ok(r) => r,
        Err(e) => return out(format!("ssh: {host}: {}", e.err)),
    };
    let mut jump_ip: Option<u32> = None;
    if let Some(j) = jump.as_deref().filter(|j| !j.is_empty()) {
        let jh = if j.contains('@') { j.split('@').nth(1).unwrap_or("") } else { j };
        match to_ip(state, dev_id, jh) {
            Ok(r) => jump_ip = Some(r.ip),
            Err(e) => return out(i18n::trf!("ssh: bastion {0}: {1}", jh, e.err)),
        }
    }
    if cmd == "ssh-copy-id" {
        let key = state.devices.get(dev_id).and_then(|d| d.ssh_key.clone()).filter(|k| !k.is_empty());
        let Some(key) = key else { return out(i18n::tr("ssh-copy-id: you have no key — run ssh-keygen")) };
        let r = ssh_connect(state, dev_id, user, res.ip, jump_ip, pass.as_deref(), true);
        let Some(srv) = r.srv.clone().filter(|_| r.ok) else { return probe(r.error.clone().unwrap_or_default(), r.run.clone()) };
        if let Some(sd) = state.devices.get_mut(&srv.id) {
            if let Some(u) = sd.ssh.as_mut().and_then(|s| s.users.get_mut(user)) {
                if !u.keys.contains(&key) {
                    u.keys.push(key.clone());
                }
            }
        }
        return CmdResult {
            out: i18n::trf!("Key {0} added to {1} for user {2}", key, srv.name, user),
            changed: Some(true),
            probe: r.run,
            ..Default::default()
        };
    }
    let r = ssh_connect(state, dev_id, user, res.ip, jump_ip, pass.as_deref(), no_key);
    let Some(srv) = r.srv.clone().filter(|_| r.ok) else { return probe(r.error.clone().unwrap_or_default(), r.run.clone()) };
    let mut lines = r.lines.clone();
    lines.push(i18n::trf!("{0}@{1}:~$ (session established; exit to leave)", user, srv.name));
    probe(lines.join("\n"), r.run)
}

fn sshd_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    let g = |i: usize| a.get(i).copied();
    if sub.is_none() || sub == Some("show") {
        let Some(ssh) = &d.ssh else { return out(i18n::tr("The SSH server is not enabled (sshd enable)")) };
        let mut l = vec![
            i18n::trf!("host key: {0}", ssh.host_key),
            i18n::trf!("password login: {0}", if ssh.password_auth { i18n::tr("allowed") } else { i18n::tr("off") }),
        ];
        for (u, v) in ssh.users.iter() {
            let keys = if v.keys.is_empty() { String::new() } else { format!(" ({})", v.keys.join(", ")) };
            l.push(i18n::trf!("user {0}: {1} key(s){2}", u, v.keys.len(), keys));
        }
        return out(l.join("\n"));
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    let sub = sub.unwrap_or("");
    if sub == "enable" {
        if d.ssh.is_none() {
            d.ssh = Some(new_ssh());
        }
        if !d.services.iter().any(|s| s.proto == Proto::Tcp && s.port == 22) {
            d.services.push(Service { proto: Proto::Tcp, port: 22, bind: None, name: None });
        }
        return changed(i18n::tr("SSH server enabled on tcp/22"));
    }
    let id = d.id.clone();
    let Some(ssh) = d.ssh.as_mut() else { return out(i18n::tr("first: sshd enable")) };
    match sub {
        "user" => {
            let Some(name) = g(1).filter(|x| !x.is_empty()) else { return out(i18n::tr("sshd user <name> [password]")) };
            let old = ssh.users.get(name).cloned();
            let keys = old.as_ref().map(|u| u.keys.clone()).unwrap_or_default();
            let password = g(2).map(|s| s.to_string()).or_else(|| old.and_then(|u| u.password));
            ssh.users.insert(name, SshUser { keys, password });
            changed(i18n::trf!("user {0} created", name))
        }
        "authorize" => {
            let (Some(u), Some(k)) = (ssh.users.get_mut(g(1).unwrap_or("undefined")), g(2).filter(|x| !x.is_empty())) else {
                return out(i18n::tr("sshd authorize <user> <key fingerprint>"));
            };
            if !u.keys.iter().any(|x| x == k) {
                u.keys.push(k.to_string());
            }
            changed(i18n::trf!("key {0} authorized for {1}", k, g(1).unwrap_or("")))
        }
        "password" => match g(1) {
            Some("on") | Some("off") => {
                ssh.password_auth = g(1) == Some("on");
                changed(i18n::trf!("password login {0}", if ssh.password_auth { i18n::tr("allowed") } else { i18n::tr("off") }))
            }
            _ => out("sshd password on|off"),
        },
        "hostkey" => {
            let rot = ssh.rot.unwrap_or(0) + 1;
            ssh.rot = Some(rot);
            let sum: u64 = id.chars().map(|c| c as u64).sum();
            ssh.host_key = format!("SHA256:hostKey{}", sum * 31 + rot as u64);
            changed(i18n::trf!("host key replaced: {0}", ssh.host_key))
        }
        _ => out(i18n::tr("sshd show | enable | user <name> [password] | authorize <user> <fingerprint> | password on|off | hostkey")),
    }
}

fn vpn_admin(d: &mut Device, a: &[&str]) -> CmdResult {
    let bad = no(d);
    let sub = a.first().copied();
    if sub.is_none() || sub == Some("show") {
        let t: Vec<&Iface> = d.ifaces.iter().filter(|i| i.tun.is_some()).collect();
        return out(if t.is_empty() {
            i18n::tr("no tunnels").to_string()
        } else {
            t.iter()
                .map(|i| {
                    let tun = i.tun.as_ref();
                    i18n::trf!("{0}: {1}/{2} ↔ {3}:{4}  key {5}  {6}", i.name, i.ip.as_deref().unwrap_or("null"), i.prefix, tun.map(|t| t.peer.as_str()).unwrap_or("undefined"), tun.map(|t| t.port.to_string()).unwrap_or_else(|| "undefined".into()), if tun.map(|t| !t.key.is_empty()).unwrap_or(false) { i18n::tr("defined") } else { i18n::tr("no") }, if i.up { "up" } else { "down" })
                })
                .collect::<Vec<_>>()
                .join("\n")
        });
    }
    if let Some(bad) = bad {
        return out(bad);
    }
    match sub.unwrap_or("") {
        "add" => {
            let name = a.get(1).copied();
            let peer = after(a, "--peer");
            let addr = after(a, "--address");
            let key = after(a, "--key");
            let c = parse_cidr(addr.unwrap_or(""));
            let (Some(name), true, Some((cip, cpre)), Some(key)) =
                (name.filter(|n| !n.is_empty()), parse_ip(peer.unwrap_or("")).is_some(), c, key.filter(|k| !k.is_empty()))
            else {
                return out(i18n::tr("vpn add wg0 --peer <peer public IP> --address 10.9.0.1/30 --key <shared secret>"));
            };
            if d.iface(name).is_some() {
                return out(i18n::trf!("interface {0} already exists", name));
            }
            let peer = peer.unwrap_or("");
            d.ifaces.push(Iface {
                name: name.to_string(),
                mac: "00:00:00:00:00:00".into(),
                ip: Some(ip_str(cip)),
                prefix: cpre as u8,
                up: true,
                mtu: None,
                vlan: None,
                trunk: false,
                tun: Some(Tun { peer: peer.to_string(), port: 51820, key: key.to_string() }),
                txqueuelen: None,
            });
            changed(i18n::trf!("tunnel {0} created: peer {1}, UDP/51820. Now add routes to the remote networks: ip route add <network> dev {0}", name, peer))
        }
        "del" => {
            let name = a.get(1).copied();
            d.ifaces.retain(|i| !(i.tun.is_some() && Some(i.name.as_str()) == name));
            d.routes.retain(|r| r.dev.as_deref() != name);
            changed(i18n::tr("tunnel removed"))
        }
        _ => out(i18n::tr("vpn show | add <name> --peer <ip> --address <ip/mask> --key <secret> | del <name>")),
    }
}

/* ---- ping / traceroute / curl ---- */

fn do_ping(state: &mut NetState, dev_id: &str, args: &[&str]) -> CmdResult {
    let mut count = 3.0_f64;
    let mut ttl = 64.0_f64;
    let mut size: Option<f64> = None;
    let mut df = false;
    let mut rest: Vec<String> = Vec::new();
    let mut i = 0;
    while i < args.len() {
        match args[i] {
            "-c" => {
                i += 1;
                count = num_or(args.get(i).copied(), 3.0).min(10.0);
            }
            "-t" => {
                i += 1;
                ttl = num_or(args.get(i).copied(), 64.0);
            }
            "-s" => {
                i += 1;
                size = Some(num_or(args.get(i).copied(), 56.0).max(0.0));
            }
            "-M" => {
                i += 1;
                df = args.get(i) == Some(&"do");
            }
            other => rest.push(other.to_string()),
        }
        i += 1;
    }
    let Some(name) = rest.first().cloned().filter(|n| !n.is_empty()) else { return out(i18n::tr("ping: specify an address or a name")) };
    let res = match to_ip(state, dev_id, &name) {
        Ok(r) => r,
        Err(e) => return probe(format!("ping: {name}: {}", e.err), e.run),
    };
    let dst = res.ip;
    let Some(d) = state.devices.get(dev_id).cloned() else { return out("") };
    if lookup(&d, Some(dst), false).is_none() && !d.ifaces.iter().any(|i| i.ip.as_deref() == Some(ip_str(dst).as_str())) {
        return out("ping: connect: Network is unreachable");
    }
    let dst_s = ip_str(dst);
    let shown = size.map(num_str).unwrap_or_else(|| "56".into());
    let mut lines = vec![format!(
        "PING {name}{}: {shown} data bytes{}",
        if name != dst_s { format!(" ({dst_s})") } else { String::new() },
        if df { ", DF" } else { "" }
    )];
    let mut got = 0.0;
    let mut last: Option<ProbeRun> = None;
    let mut s = 1.0;
    while s <= count {
        let r = ping1(state, dev_id, dst, &PingOpts { ttl: ttl as i64, id: s as i64, size: size.map(|x| x as i64), df });
        let from = ip_str_opt(r.from);
        let mtu = r.mtu.map(|m| m.to_string()).unwrap_or_else(|| "undefined".into());
        let sq = num_str(s);
        match (r.status, r.code) {
            (ProbeStatus::Toolong, _) => lines.push(format!("ping: local error: message too long, mtu={mtu}")),
            (ProbeStatus::Unreach, Some(IcmpCode::Frag)) => {
                lines.push(format!("From {from} icmp_seq={sq} Frag needed and DF set (mtu = {mtu})"))
            }
            (ProbeStatus::Reply, _) => {
                got += 1.0;
                lines.push(format!("{} bytes from {from}: icmp_seq={sq} time={}", num_str(size.unwrap_or(56.0) + 8.0), fmt_ms(r.rtt_us)));
            }
            (ProbeStatus::Ttl, _) => lines.push(format!("From {from} icmp_seq={sq} Time to live exceeded")),
            (ProbeStatus::Unreach, _) => lines.push(format!("From {from} icmp_seq={sq} Destination Host Unreachable")),
            _ => lines.push(format!("Request timeout for icmp_seq={sq}")),
        }
        last = Some(r);
        s += 1.0;
    }
    lines.push(format!("--- {dst_s} ping statistics ---"));
    lines.push(format!(
        "{} packets transmitted, {} received, {}% packet loss",
        num_str(count),
        num_str(got),
        num_str(crate::util::js_round(((count - got) / count) * 100.0))
    ));
    probe(lines.join("\n"), last)
}

fn do_traceroute(state: &mut NetState, dev_id: &str, args: &[&str]) -> CmdResult {
    let target = args.first().copied().unwrap_or("");
    let res = match to_ip(state, dev_id, target) {
        Ok(r) => r,
        Err(e) => return out(format!("traceroute: {target}: {}", e.err)),
    };
    let dst = res.ip;
    let Some(d) = state.devices.get(dev_id).cloned() else { return out("") };
    if lookup(&d, Some(dst), false).is_none() {
        return out("traceroute: connect: Network is unreachable");
    }
    let hops = traceroute(state, dev_id, dst, 12);
    let mut lines = vec![format!("traceroute to {}, 12 hops max", und(args.first().copied()))];
    for (ttl, h) in &hops {
        lines.push(if h.status == ProbeStatus::Timeout {
            format!(" {ttl}  * * *")
        } else {
            format!(" {ttl}  {}  {}", ip_str_opt(h.from), fmt_ms(h.rtt_us))
        });
    }
    probe(lines.join("\n"), hops.into_iter().last().map(|(_, r)| r))
}

fn do_connect(state: &mut NetState, dev_id: &str, host: &str, port: f64, mode: &str, session: bool) -> CmdResult {
    let res = match to_ip(state, dev_id, host) {
        Ok(r) => r,
        Err(e) => return probe(format!("{mode}: {host}: {}", e.err), e.run),
    };
    let dst = res.ip;
    let Some(d) = state.devices.get(dev_id).cloned() else { return out("") };
    if lookup(&d, Some(dst), false).is_none() {
        return out(format!("{mode}: Network is unreachable"));
    }
    let r = tcp1(state, dev_id, dst, to_int(port), 50000, session);
    let p = num_str(port);
    let text = match r.status {
        ProbeStatus::Connected => i18n::trf!("connection to {0}:{1} established (SYN → SYN-ACK → ACK) in {2}{3}", host, p, fmt_ms(r.rtt_us), if session {
                i18n::tr("; request 100 B, response 1000 B, closed (FIN). Details are in the log below")
            } else {
                ""
            }),
        ProbeStatus::Refused => i18n::trf!("{0}: Connection refused — nothing is listening on port {1}", mode, p),
        ProbeStatus::Timeout => i18n::trf!("{0}: Connection timed out — no reply (the packet was lost or filtered)", mode),
        ProbeStatus::Unreach => i18n::trf!("{0}: Destination unreachable from {1}", mode, r.from.map(ip_str).unwrap_or_else(|| "?".into())),
        ProbeStatus::Ttl => i18n::trf!("{0}: TTL expired", mode),
        other => other.as_str().to_string(),
    };
    probe(text, Some(r))
}

fn do_udp(state: &mut NetState, dev_id: &str, host: &str, port: f64) -> CmdResult {
    let Some(dst) = parse_ip(host) else { return out(i18n::tr("nc -u: usage is nc -u <ip> <port>")) };
    if port.is_nan() || port == 0.0 {
        return out(i18n::tr("nc -u: usage is nc -u <ip> <port>"));
    }
    let Some(d) = state.devices.get(dev_id).cloned() else { return out("") };
    if lookup(&d, Some(dst), false).is_none() {
        return out("nc: Network is unreachable");
    }
    let r = udp1(state, dev_id, dst, to_int(port), 50001);
    let from = r.from.map(ip_str).unwrap_or_else(|| "?".into());
    let msg = match r.status {
        ProbeStatus::Reply => i18n::trf!("reply datagram from {0}:{1} in {2}", host, num_str(port), fmt_ms(r.rtt_us)),
        ProbeStatus::Unreach => i18n::trf!("ICMP: {0} (from {1}) — \"Connection refused\"", if r.code == Some(IcmpCode::Port) { i18n::tr("port unreachable") } else { i18n::tr("host unreachable") }, from),
        _ => i18n::tr("silence: no reply (the datagram was lost, filtered or the server is silent) — UDP will not report this by itself").to_string(),
    };
    probe(msg, Some(r))
}

/* ---- line parsing ---- */

/// Show the ARP cache.
fn arp(state: &NetState, dev_id: &str) -> CmdResult {
    let Some(d) = state.devices.get(dev_id) else { return out("") };
    let mut rows: Vec<String> = d.arp_static.iter().map(|(ip, mac)| i18n::trf!("{0}  {1}  (static)", ip, mac)).collect();
    if let Some(c) = state.rt.arp.get(dev_id) {
        for (ip, e) in c {
            if d.arp_static.get(&ip_str(*ip)).map(|m| !m.is_empty()).unwrap_or(false) {
                continue;
            }
            rows.push(format!("{}  {}", ip_str(*ip), e.mac));
        }
    }
    out(if rows.is_empty() {
        i18n::tr("(ARP cache is empty — nobody has been contacted yet)").to_string()
    } else {
        rows.join("\n")
    })
}

/// Execute a terminal line on a device. Changes the network state (and simulator caches).
pub fn exec(state: &mut NetState, dev_id: &str, line: &str) -> CmdResult {
    let Some(d0) = state.devices.get(dev_id) else { return out(i18n::trf!("no device \"{0}\"", dev_id)) };
    let (kind, dname) = (d0.kind, d0.name.clone());
    let tokens: Vec<&str> = line.split_whitespace().collect();
    if tokens.is_empty() {
        return out("");
    }
    if line.trim().starts_with("echo") {
        if let Some(d) = state.devices.get_mut(dev_id) {
            if let Some(r) = file_write(d, line.trim()) {
                return r;
            }
        }
    }
    let cmd = tokens[0];
    let a: &[&str] = &tokens[1..];
    let g = |i: usize| a.get(i).copied();

    macro_rules! dev {
        () => {
            match state.devices.get_mut(dev_id) {
                Some(d) => d,
                None => return out(""),
            }
        };
    }

    if cmd == "clear" {
        return CmdResult { clear: true, ..Default::default() };
    }
    if cmd == "help" || cmd == "?" {
        return out(i18n::tr(HELP));
    }
    if cmd == "hostname" {
        return out(dname);
    }

    if kind == DeviceKind::Hub {
        return out(
            i18n::tr("A hub is a repeater: it has no settings and no address table. Whatever arrives on a port, it repeats on all the others."),
        );
    }

    if kind == DeviceKind::Switch {
        if cmd == "show" && (g(0) == Some("mac") || g(0) == Some("mac-table")) {
            let rows: Vec<String> =
                state.rt.mac.get(dev_id).map(|m| m.iter().map(|(m, p)| format!("{m}  {p}")).collect()).unwrap_or_default();
            return out(if rows.is_empty() {
                i18n::tr("The MAC table is empty — the switch has not seen anything yet").to_string()
            } else {
                i18n::trf!("MAC address        port\n{0}", rows.join("\n"))
            });
        }
        if cmd == "show" && g(0) == Some("ports") {
            let d = dev!();
            return out(d
                .ifaces
                .iter()
                .map(|i| {
                    format!(
                        "{}  {}  {}",
                        i.name,
                        if i.up { "up" } else { "down" },
                        if i.trunk { "trunk".to_string() } else { format!("access vlan {}", i.vlan.unwrap_or(1)) }
                    )
                })
                .collect::<Vec<_>>()
                .join("\n"));
        }
        if cmd == "port" && (g(1) == Some("vlan") || g(1) == Some("trunk") || g(1) == Some("access")) {
            let d = dev!();
            if let Some(bad) = no(d) {
                return out(bad);
            }
            let Some(i) = d.iface_mut(g(0).unwrap_or("undefined")) else {
                return out(i18n::trf!("no port \"{0}\"", g(0).unwrap_or("")));
            };
            if g(1) == Some("trunk") {
                i.trunk = true;
            } else {
                let v = if g(1) == Some("vlan") { js_num(g(2).unwrap_or("undefined")) } else { 1.0 };
                if !(v >= 1.0 && v <= 4094.0) {
                    return out(i18n::tr("VLAN is a number from 1 to 4094"));
                }
                i.trunk = false;
                i.vlan = Some(v as u32);
            }
            return changed("");
        }
        if cmd == "port" && a.len() == 2 && (g(1) == Some("up") || g(1) == Some("down")) {
            let d = dev!();
            if let Some(bad) = no(d) {
                return out(bad);
            }
            return done(set_up(d, g(0).unwrap_or("undefined"), g(1) == Some("up")));
        }
        return out(i18n::tr("Switch: show mac — MAC address table, show ports — port status, port <port> up|down, port <port> vlan <number>, port <port> trunk. It has no IP addresses."));
    }

    if cmd == "ip" {
        let obj = g(0);
        let verb = g(1);
        let r: Vec<&str> = if a.len() > 2 { a[2..].to_vec() } else { vec![] };
        let dev_arg = || r.get((index_of(&r, "dev") + 1) as usize).copied();
        if matches!(obj, Some("addr") | Some("address") | Some("a")) {
            if verb.is_none() || verb == Some("show") {
                return out(show_addr(dev!()));
            }
            if let Some(bad) = no(dev!()) {
                return out(bad);
            }
            let devname = dev_arg();
            if verb == Some("add") {
                return done(set_addr(dev!(), devname.unwrap_or("undefined"), r.first().copied().unwrap_or("undefined")));
            }
            if verb == Some("flush") {
                return done(clear_addr(dev!(), devname.or(r.first().copied()).unwrap_or("undefined")));
            }
            if verb == Some("del") {
                return done(clear_addr(dev!(), devname.unwrap_or("undefined")));
            }
        }
        if matches!(obj, Some("link") | Some("l")) {
            if verb.is_none() || verb == Some("show") {
                return out(show_addr(dev!()));
            }
            if let Some(bad) = no(dev!()) {
                return out(bad);
            }
            if verb == Some("set") {
                let mt = index_of(&r, "mtu");
                if mt >= 0 {
                    let d = dev!();
                    let v = js_num(r.get((mt + 1) as usize).copied().unwrap_or("undefined"));
                    let ok = v >= 68.0 && v <= 9000.0;
                    match (d.iface_mut(r.first().copied().unwrap_or("undefined")), ok) {
                        (Some(i), true) => {
                            i.mtu = Some(v as u32);
                            return changed("");
                        }
                        _ => return out("Error: ip link set <if> mtu <68..9000>"),
                    }
                }
                let k = index_of(&r, "txqueuelen");
                if k >= 0 {
                    let d = dev!();
                    let v = js_num(r.get((k + 1) as usize).copied().unwrap_or("undefined"));
                    let ok = v >= 1.0 && v <= 10000.0;
                    match (d.iface_mut(r.first().copied().unwrap_or("undefined")), ok) {
                        (Some(i), true) => {
                            i.txqueuelen = Some(v as u32);
                            return changed("");
                        }
                        _ => return out("Error: ip link set <if> txqueuelen <1..10000>"),
                    }
                }
                return done(set_up(dev!(), r.first().copied().unwrap_or("undefined"), r.get(1) == Some(&"up")));
            }
        }
        if matches!(obj, Some("route") | Some("r")) {
            if verb.is_none() || verb == Some("show") {
                let d = dev!().clone();
                let rows: Vec<String> = route_table(&d, false).iter().map(|x| route_line(x, &d)).collect();
                return out(if rows.is_empty() { i18n::tr("(the routing table is empty)").to_string() } else { rows.join("\n") });
            }
            if verb == Some("get") {
                let Some(dst) = parse_ip(r.first().copied().unwrap_or("")) else { return out(i18n::tr("Error: invalid address")) };
                let d = dev!().clone();
                let Some(rt) = lookup(&d, Some(dst), false) else { return out("RTNETLINK answers: Network is unreachable") };
                let src = d.iface(&rt.dev).and_then(|i| i.ip.clone()).unwrap_or_else(|| "null".into());
                let via = rt.via.map(|v| format!("via {} ", ip_str(v))).unwrap_or_default();
                return out(format!("{} {}dev {} src {}", r.first().copied().unwrap_or(""), via, rt.dev, src));
            }
            if let Some(bad) = no(dev!()) {
                return out(bad);
            }
            if verb == Some("add") {
                let dst = r.first().copied();
                let via = if r.contains(&"via") { after(&r, "via") } else { None };
                let devn = if r.contains(&"dev") { after(&r, "dev") } else { None };
                return done(add_route(dev!(), dst, via, devn));
            }
            if verb == Some("del") {
                return done(del_route(dev!(), r.first().copied()));
            }
        }
        if matches!(obj, Some("neigh") | Some("n")) {
            return arp(state, dev_id);
        }
        return out(i18n::tr("ip: unknown command. Type \"help\"."));
    }
    if cmd == "dig" {
        return do_dig(state, dev_id, a, false);
    }
    if cmd == "nslookup" || cmd == "host" {
        return do_dig(state, dev_id, a, true);
    }
    if cmd == "dns" {
        return dns_admin(dev!(), a);
    }
    if cmd == "web" {
        return web_admin(dev!(), a);
    }
    if cmd == "ssh" || cmd == "ssh-keygen" || cmd == "ssh-copy-id" {
        return ssh_client(state, dev_id, cmd, a);
    }
    if cmd == "sshd" {
        return sshd_admin(dev!(), a);
    }
    if cmd == "vpn" {
        return vpn_admin(dev!(), a);
    }
    if cmd == "lb" {
        return lb_admin(dev!(), a);
    }
    if cmd == "rproxy" {
        return rproxy_admin(dev!(), a);
    }
    if cmd == "proxy" {
        return proxy_admin(dev!(), a);
    }
    if cmd == "close" {
        let d = dev!();
        if let Some(bad) = no(d) {
            return out(bad);
        }
        let n = d.services.len();
        let port = js_num(g(1).unwrap_or("undefined"));
        d.services.retain(|x| !(Some(x.proto.as_str()) == g(0) && x.port as f64 == port));
        return if d.services.len() < n {
            changed(i18n::trf!("{0}/{1} closed", g(0).unwrap_or("undefined"), g(1).unwrap_or("undefined")))
        } else {
            out(i18n::tr("close <tcp|udp> <port>: there is no such listening port"))
        };
    }
    if cmd == "tcpdump" {
        background_traffic(state);
        let d = dev!().clone();
        let i = index_of(a, "-i");
        let iface: String = if i >= 0 {
            a.get((i + 1) as usize).copied().unwrap_or("undefined").to_string()
        } else {
            d.ifaces.first().map(|x| x.name.clone()).unwrap_or_default()
        };
        if iface != "any" && d.iface(&iface).is_none() {
            let names: Vec<&str> = d.ifaces.iter().map(|x| x.name.as_str()).collect();
            return out(i18n::trf!("tcpdump: no interface \"{0}\" (available: {1}, any)", iface, names.join(", ")));
        }
        let c = index_of(a, "-c");
        let count = if c >= 0 { num_or(a.get((c + 1) as usize).copied(), 20.0) } else { 20.0 };
        let filters: Vec<&str> = a
            .iter()
            .enumerate()
            .filter(|(k, x)| {
                **x != "-i" && **x != "-c" && *k as isize != i + 1 && *k as isize != c + 1 && !x.starts_with('-') && **x != "and"
            })
            .map(|(_, x)| *x)
            .collect();
        let lines = capture_lines(state, dev_id, &iface, &filters, count as i64);
        return out(if lines.is_empty() {
            i18n::trf!("tcpdump: listening on {0}\n(no packets captured — generate some traffic first: ping, curl)", iface)
        } else {
            format!("tcpdump: listening on {iface}\n{}\n{} packets captured", lines.join("\n"), lines.len())
        });
    }
    if cmd == "listen" {
        let d = dev!();
        if let Some(bad) = no(d) {
            return out(bad);
        }
        let (proto, port, addr) = (g(0), g(1), g(2));
        let pn = js_num(port.unwrap_or("undefined"));
        let Some(s) = d.services.iter_mut().find(|x| Some(x.proto.as_str()) == proto && x.port as f64 == pn) else {
            return out(i18n::trf!("listen <tcp|udp> <port> <address>: nothing is listening on {0}/{1}", und(proto), und(port)));
        };
        if addr != Some("0.0.0.0") && addr != Some("127.0.0.1") && parse_ip(addr.unwrap_or("")).is_none() {
            return out(i18n::tr("address: 0.0.0.0 (everywhere), 127.0.0.1 (local only) or an interface address"));
        }
        let addr = addr.unwrap_or("undefined");
        s.bind = Some(addr.to_string());
        return changed(i18n::trf!("{0}/{1} is now listening on {2}", und(proto), und(port), addr));
    }
    if cmd == "tls" {
        let pki = state.pki.clone().unwrap_or_else(default_pki);
        return tls_admin(&pki, dev!(), a);
    }
    if cmd == "trust" {
        let pki = state.pki.clone().unwrap_or_else(default_pki);
        return trust_admin(&pki, dev!(), a);
    }
    if cmd == "openssl" {
        let k = index_of(a, "-connect");
        let target = a.get((k + 1) as usize).copied().unwrap_or("");
        let mut parts = target.split(':');
        let host = parts.next().unwrap_or("");
        let port = parts.next();
        if g(0) != Some("s_client") || k < 0 || host.is_empty() {
            return out(i18n::tr("openssl s_client -connect www.example.org:443 [-servername name]"));
        }
        let sn = index_of(a, "-servername");
        let res = match to_ip(state, dev_id, host) {
            Ok(r) => r,
            Err(e) => return out(format!("openssl: {host}: {}", e.err)),
        };
        let name = if sn >= 0 { a.get((sn + 1) as usize).copied().unwrap_or("undefined") } else { host };
        let p = match port {
            Some(p) => to_int(js_num(p)),
            None => 443,
        };
        let (text, run) = s_client(state, dev_id, name, res.ip, p);
        return probe(text, Some(run));
    }
    if cmd == "pageload" {
        let arg = g(0).unwrap_or("");
        let lower = arg.to_lowercase();
        let scheme_len = if lower.starts_with("https://") {
            8
        } else if lower.starts_with("http://") {
            7
        } else {
            0
        };
        let host: String = if scheme_len > 0 {
            arg[scheme_len..].chars().take_while(|c| c.is_ascii_alphanumeric() || *c == '_' || *c == '.' || *c == '-').collect()
        } else {
            String::new()
        };
        if scheme_len == 0 || host.is_empty() {
            return out(i18n::tr("pageload https://www.example.org/ — measure page load"));
        }
        let res = match to_ip(state, dev_id, &host) {
            Ok(r) => r,
            Err(e) => return out(format!("pageload: {host}: {}", e.err)),
        };
        return out(fmt_page(&pageload(state, dev_id, res.ip, lower.starts_with("https"))));
    }
    if cmd == "cat" {
        let d = dev!();
        if g(0) == Some("/etc/resolv.conf") {
            return out(match d.resolver.as_deref().filter(|r| !r.is_empty()) {
                Some(r) => format!("nameserver {r}"),
                None => i18n::tr("(the file is empty — no DNS server set)").to_string(),
            });
        }
        if g(0) == Some("/etc/hosts") {
            let mut l = vec!["127.0.0.1 localhost".to_string()];
            l.extend(d.hosts.iter().map(|(n, ip)| format!("{ip} {n}")));
            return out(l.join("\n"));
        }
        return out(i18n::trf!("cat: {0}: no such file (available: /etc/resolv.conf and /etc/hosts)", g(0).unwrap_or("")));
    }
    if cmd == "arp" {
        if g(0) == Some("-s") {
            let d = dev!();
            if let Some(bad) = no(d) {
                return out(bad);
            }
            if parse_ip(g(1).unwrap_or("")).is_none() || !is_mac(g(2).unwrap_or("")) {
                return out(i18n::tr("arp -s <ip> <mac like 28:28:00:00:00:01>"));
            }
            let (ip_s, mac) = (g(1).unwrap_or(""), g(2).unwrap_or("").to_lowercase());
            d.arp_static.insert(ip_s, mac);
            if let Some(key) = parse_ip(ip_s) {
                if let Some(c) = state.rt.arp.get_mut(dev_id) {
                    c.remove(&key);
                }
            }
            return changed(i18n::trf!("static ARP entry: {0} = {1}", g(1).unwrap_or(""), g(2).unwrap_or("")));
        }
        if g(0) == Some("-d") {
            let d = dev!();
            d.arp_static.remove(g(1).unwrap_or("undefined"));
            return changed(i18n::tr("static entry removed"));
        }
        return arp(state, dev_id);
    }
    if cmd == "ping" {
        return do_ping(state, dev_id, a);
    }
    if cmd == "traceroute" || cmd == "tracepath" {
        return do_traceroute(state, dev_id, a);
    }
    if cmd == "curl" {
        return do_curl(state, dev_id, a);
    }
    if cmd == "nc" {
        let udp = a.contains(&"-u");
        let flags: Vec<&str> = a.iter().copied().filter(|x| x.starts_with('-')).collect();
        let rest: Vec<&str> = a.iter().copied().filter(|x| !x.starts_with('-')).collect();
        if flags.iter().any(|f| f.chars().skip(1).any(|c| c == 'l') && *f != "-u") {
            let d = dev!();
            if let Some(bad) = no(d) {
                return out(bad);
            }
            let port = js_num(rest.first().copied().unwrap_or("undefined"));
            if port.is_nan() || port == 0.0 {
                return out(i18n::tr("nc: specify a port: nc -l 8080 (or nc -u -l 5000 for UDP)"));
            }
            let proto = if udp { Proto::Udp } else { Proto::Tcp };
            let pn = to_int(port);
            if !d.services.iter().any(|s| s.port == pn && s.proto == proto) {
                d.services.push(Service { proto, port: pn, bind: None, name: None });
            }
            return changed(i18n::trf!("listening on {0} port {1}", proto.as_str(), num_str(port)));
        }
        let host = rest.first().copied().unwrap_or("");
        let port = js_num(rest.get(1).copied().unwrap_or("undefined"));
        if udp {
            return do_udp(state, dev_id, host, port);
        }
        return do_connect(state, dev_id, host, port, "nc", false);
    }
    if cmd == "iperf3" || cmd == "iperf" {
        let Some(ip) = a.iter().find(|x| parse_ip(x).is_some()).copied() else {
            return out(i18n::tr("iperf3: specify the server address: iperf3 10.0.0.5 [-n MB]"));
        };
        let k = index_of(a, "-n");
        let mb = if k >= 0 { num_or(a.get((k + 1) as usize).copied(), 50.0) } else { 50.0 };
        let dst = parse_ip(ip);
        let d = dev!().clone();
        let Some(dst) = dst.filter(|x| lookup(&d, Some(*x), false).is_some()) else { return out("iperf3: Network is unreachable") };
        let r = transfer(state, dev_id, dst, mb * 1e6);
        return CmdResult {
            out: if r.ok { r.text.clone() } else { format!("iperf3: {}", r.text) },
            chart: r.chart.clone(),
            xfer: Some(r),
            ..Default::default()
        };
    }
    if cmd == "ss" || cmd == "netstat" {
        let d = dev!();
        return out(if d.services.is_empty() {
            i18n::tr("(no listening ports)").to_string()
        } else {
            d.services
                .iter()
                .map(|s| format!("{}  LISTEN  {}:{}", s.proto.as_str(), s.bind.as_deref().unwrap_or("0.0.0.0"), s.port))
                .collect::<Vec<_>>()
                .join("\n")
        });
    }
    if cmd == "sysctl" || cmd == "echo" {
        return sysctl(dev!(), cmd, &a.join(" "));
    }
    if cmd == "iptables" || cmd == "sudo" {
        if cmd == "sudo" && g(0) != Some("iptables") {
            return exec(state, dev_id, &a.join(" "));
        }
        let t: &[&str] = if cmd == "sudo" { &a[1..] } else { a };
        return iptables(dev!(), t);
    }
    out(i18n::trf!("{0}: command not found. Type \"help\".", cmd))
}

/// Find `=` followed (after spaces) by a character from `ok`; return that character.
fn after_eq(text: &str, ok: impl Fn(char) -> bool) -> Option<char> {
    let b: Vec<char> = text.chars().collect();
    for (i, c) in b.iter().enumerate() {
        if *c == '=' {
            let mut j = i + 1;
            while j < b.len() && b[j].is_whitespace() {
                j += 1;
            }
            if j < b.len() && ok(b[j]) {
                return Some(b[j]);
            }
        }
    }
    None
}

/// Word after `=` (after spaces): `\w+`.
fn word_after_eq(text: &str) -> Option<String> {
    let b: Vec<char> = text.chars().collect();
    for (i, c) in b.iter().enumerate() {
        if *c == '=' {
            let mut j = i + 1;
            while j < b.len() && b[j].is_whitespace() {
                j += 1;
            }
            let w: String = b[j..].iter().take_while(|c| c.is_ascii_alphanumeric() || **c == '_').collect();
            if !w.is_empty() {
                return Some(w);
            }
        }
    }
    None
}

/// Numbers after `tcp_rmem`: `tcp_rmem\s*=?\s*"?([\d\s,]+)"?`; `None` means the pattern did not match.
fn rmem_numbers(text: &str) -> Option<Vec<f64>> {
    let mut from = 0;
    while let Some(off) = text[from..].find("tcp_rmem") {
        let start = from + off + "tcp_rmem".len();
        let chars: Vec<char> = text[start..].chars().collect();
        let mut j = 0;
        let mut ws = false;
        while j < chars.len() && chars[j].is_whitespace() {
            j += 1;
            ws = true;
        }
        if j < chars.len() && chars[j] == '=' {
            j += 1;
        }
        while j < chars.len() && chars[j].is_whitespace() {
            j += 1;
            ws = true;
        }
        if j < chars.len() && chars[j] == '"' {
            j += 1;
        }
        let cap: String = chars[j..].iter().take_while(|c| c.is_ascii_digit() || c.is_whitespace() || **c == ',').collect();
        if !cap.is_empty() {
            return Some(cap.split(|c: char| c.is_whitespace() || c == ',').filter(|x| !x.is_empty()).map(js_num).collect());
        }
        if ws {
            return Some(vec![]);
        }
        from = start;
    }
    None
}

fn sysctl(d: &mut Device, cmd: &str, text: &str) -> CmdResult {
    if let Some(nums) = rmem_numbers(text) {
        let rwnd = d.rwnd.unwrap_or(64) as f64;
        if !text.contains('=') {
            return out(format!("net.ipv4.tcp_rmem = 4096 {} {}", num_str(rwnd * 1024.0), num_str(rwnd * 1024.0)));
        }
        if let Some(bad) = no(d) {
            return out(bad);
        }
        let max_b = nums.last().copied();
        if !max_b.map(|m| m >= 4096.0).unwrap_or(false) {
            return out(i18n::tr("sysctl: the maximum buffer size must be at least 4096 bytes"));
        }
        let max_b = max_b.unwrap_or(0.0);
        let r = crate::util::js_round(max_b / 1024.0);
        d.rwnd = Some(r as u32);
        let mid = if nums.len() > 2 { num_str(nums[1]) } else { num_str(max_b) };
        return changed(i18n::trf!("net.ipv4.tcp_rmem = 4096 {0} {1}  (receive window up to {2} KB)", mid, num_str(max_b), num_str(r)));
    }
    if text.contains("tcp_syncookies") {
        let Some(m) = after_eq(text, |c| c == '0' || c == '1') else {
            return out(format!("net.ipv4.tcp_syncookies = {}", if d.syncookies { 1 } else { 0 }));
        };
        if let Some(bad) = no(d) {
            return out(bad);
        }
        d.syncookies = m == '1';
        return changed(format!("net.ipv4.tcp_syncookies = {m}"));
    }
    if text.contains("tcp_congestion_control") {
        let Some(m) = word_after_eq(text) else {
            return out(format!("net.ipv4.tcp_congestion_control = {}", d.cc.unwrap_or(Cc::Cubic).as_str()));
        };
        if let Some(bad) = no(d) {
            return out(bad);
        }
        let cc = match m.as_str() {
            "reno" => Cc::Reno,
            "cubic" => Cc::Cubic,
            "bbr" => Cc::Bbr,
            _ => return out(i18n::tr("sysctl: available: reno, cubic, bbr")),
        };
        d.cc = Some(cc);
        return changed(format!("net.ipv4.tcp_congestion_control = {m}"));
    }
    if !text.contains("ip_forward") {
        if cmd == "echo" {
            return out(text);
        }
        return out(i18n::tr("sysctl: supported: net.ipv4.ip_forward, net.ipv4.tcp_rmem, net.ipv4.tcp_congestion_control"));
    }
    let val = after_eq(text, |c| c == '0' || c == '1').or_else(|| {
        let mut ch = text.chars();
        let first = ch.next().filter(|c| *c == '0' || *c == '1')?;
        let _ = first;
        let rest: &str = &text[1..];
        if rest.trim_start().starts_with('>') {
            Some(first)
        } else {
            None
        }
    });
    let Some(val) = val else { return out(format!("net.ipv4.ip_forward = {}", if d.forward { 1 } else { 0 })) };
    if let Some(bad) = no(d) {
        return out(bad);
    }
    d.forward = val == '1';
    changed(format!("net.ipv4.ip_forward = {val}"))
}
