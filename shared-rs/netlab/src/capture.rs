//! Перехват пакетов (tcpdump): каждый кадр, прошедший через интерфейс при пробах, попадает в кольцо
//! устройства; команда tcpdump показывает кольцо с фильтром. Время в кольце — монотонные «московские» часы.

use crate::ip::*;
use crate::sim::Sim;
use crate::types::*;
use crate::util::{js_num, js_round};

const LIMIT: usize = 300;

/// Записать переходы кадров пробы в кольца перехвата.
pub(crate) fn record_capture(sim: &mut Sim) {
    let base = sim.rt.clock;
    let mut last: f64 = 0.0;
    for h in &sim.hops {
        for (dev, port, t, inbound) in [(&h.from, &h.from_port, base + h.t0, false), (&h.to, &h.to_port, base + h.t1, true)] {
            let ring = sim.rt.cap.entry(format!("{dev}:{port}")).or_default();
            ring.push(CapRow { t, inbound, frame: h.frame.clone() });
            if ring.len() > LIMIT {
                ring.remove(0);
            }
        }
        last = last.max(h.t1);
    }
    sim.rt.clock = base + last + 500_000.0;
}

fn clock(us: f64) -> String {
    let sec = (us / 1e6).floor();
    let f = format!("{}", js_round(us % 1e6) as i64);
    let hh = 12 + (sec / 3600.0).floor() as i64;
    format!("{:02}:{:02}:{:02}.{:0>6}", hh, ((sec / 60.0).floor() as i64) % 60, (sec as i64) % 60, f)
}

fn flag_text(f: TcpFlags) -> &'static str {
    match f {
        TcpFlags::Syn => "S",
        TcpFlags::SynAck => "S.",
        TcpFlags::Ack => ".",
        TcpFlags::PshAck => "P.",
        TcpFlags::FinAck => "F.",
        TcpFlags::Rst => "R.",
    }
}

fn or_undef(o: Option<i64>) -> String {
    o.map(|v| v.to_string()).unwrap_or_else(|| "undefined".into())
}

/// Строка перехвата в стиле tcpdump.
pub fn line_of(frame: &Frame) -> String {
    match &frame.body {
        Payload::Arp(a) => {
            if a.op == ArpOp::Req {
                format!("ARP, Request who-has {} tell {}, length 28", ip_str(a.tip), ip_str(a.sip))
            } else {
                format!("ARP, Reply {} is-at {}, length 28", ip_str(a.sip), a.smac)
            }
        }
        Payload::Ip(p) => {
            let len = p.size.unwrap_or(84) - 20;
            let (src, dst) = (ip_str_opt(p.src), ip_str(p.dst));
            match p.proto {
                Proto::Icmp => {
                    let (typ, id, code, mtu) = match &p.icmp {
                        Some(ic) => (Some(ic.typ), ic.id, ic.code, ic.mtu),
                        None => (None, 0, None, None),
                    };
                    let what = match typ {
                        Some(IcmpType::EchoReq) => format!("echo request, id {id}, length {len}"),
                        Some(IcmpType::EchoRep) => format!("echo reply, id {id}, length {len}"),
                        Some(IcmpType::Ttl) => "time exceeded in-transit, length 56".to_string(),
                        _ => match code {
                            Some(IcmpCode::Port) => "destination unreachable (port), length 56".to_string(),
                            Some(IcmpCode::Frag) => format!(
                                "destination unreachable (need to frag, mtu {}), length 56",
                                mtu.map(|m| m.to_string()).unwrap_or_else(|| "undefined".into())
                            ),
                            None => "destination unreachable (net), length 56".to_string(),
                        },
                    };
                    format!("IP {src} > {dst}: ICMP {what} [ttl {}]", p.ttl)
                }
                Proto::Udp => {
                    if let Some(dns) = &p.dns {
                        let what = if dns.response {
                            format!("ответ {}", dns.rcode.map(|r| r.as_str()).unwrap_or("undefined"))
                        } else {
                            format!("{} {}?", dns.q.name, dns.q.typ)
                        };
                        return format!("IP {src}.{} > {dst}.{}: UDP, DNS {what}", or_undef(p.sport), or_undef(p.dport));
                    }
                    format!("IP {src}.{} > {dst}.{}: UDP, length {}", or_undef(p.sport), or_undef(p.dport), p.len.unwrap_or(56))
                }
                Proto::Tcp => {
                    let fl = p.flags;
                    let ack = if fl.map(|f| f.has_ack()).unwrap_or(false) { format!(", ack {}", or_undef(p.ack)) } else { String::new() };
                    format!(
                        "IP {src}.{} > {dst}.{}: Flags [{}], seq {}{ack}, length {}",
                        or_undef(p.sport),
                        or_undef(p.dport),
                        fl.map(flag_text).unwrap_or(""),
                        p.seq.unwrap_or(0),
                        p.len.unwrap_or(0)
                    )
                }
            }
        }
    }
}

fn matches(frame: &Frame, filters: &[&str]) -> bool {
    let proto = match &frame.body {
        Payload::Arp(_) => "arp",
        Payload::Ip(p) => p.proto.as_str(),
    };
    let mut i = 0;
    while i < filters.len() {
        let w = filters[i];
        if ["icmp", "tcp", "udp", "arp"].contains(&w) {
            if proto != w {
                return false;
            }
        } else if w == "host" {
            i += 1;
            let h = filters.get(i).copied();
            match &frame.body {
                Payload::Arp(a) => {
                    if !(Some(ip_str(a.sip).as_str()) == h || Some(ip_str(a.tip).as_str()) == h) {
                        return false;
                    }
                }
                Payload::Ip(p) => {
                    if Some(ip_str_opt(p.src).as_str()) != h && Some(ip_str(p.dst).as_str()) != h {
                        return false;
                    }
                }
            }
        } else if w == "port" {
            i += 1;
            let n = filters.get(i).map(|s| js_num(s)).unwrap_or(f64::NAN);
            match &frame.body {
                Payload::Arp(_) => return false,
                Payload::Ip(p) => {
                    if p.sport.map(|v| v as f64) != Some(n) && p.dport.map(|v| v as f64) != Some(n) {
                        return false;
                    }
                }
            }
        }
        i += 1;
    }
    true
}

/// Строки перехвата для устройства: интерфейс или «any».
pub fn capture_lines(state: &NetState, dev: &str, iface: &str, filters: &[&str], count: i64) -> Vec<String> {
    let keys: Vec<String> = if iface == "any" {
        state.devices.get(dev).map(|d| d.ifaces.iter().map(|i| format!("{dev}:{}", i.name)).collect()).unwrap_or_default()
    } else {
        vec![format!("{dev}:{iface}")]
    };
    let mut rows: Vec<(&String, &CapRow)> = Vec::new();
    for k in &keys {
        if let Some(v) = state.rt.cap.get(k) {
            rows.extend(v.iter().map(|r| (k, r)));
        }
    }
    rows.sort_by(|a, b| a.1.t.partial_cmp(&b.1.t).unwrap_or(std::cmp::Ordering::Equal));
    let sel: Vec<_> = rows.into_iter().filter(|(_, r)| matches(&r.frame, filters)).collect();
    let skip = if count >= 0 { sel.len().saturating_sub(count as usize) } else { (-count as usize).min(sel.len()) };
    sel.into_iter()
        .skip(skip)
        .map(|(k, r)| {
            let name = if iface == "any" { format!("{} ", k.split(':').nth(1).unwrap_or("")) } else { String::new() };
            format!("{} {}{:<3} {}", clock(r.t), name, if r.inbound { "In" } else { "Out" }, line_of(&r.frame))
        })
        .collect()
}
