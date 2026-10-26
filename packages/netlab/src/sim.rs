//! Симулятор сети: кадры, ARP, коммутаторы, маршрутизация, TTL, ICMP, TCP-рукопожатие, NAT и фильтр FORWARD.
//! Всё синхронное и детерминированное: одна «проба» (ping, TCP-подключение) даёт список переходов кадров для
//! анимации, журнал событий и итог. Время — в микросекундах.

use crate::attacks::attacks_before;
use crate::capture::record_capture;
use crate::ip::*;
use crate::types::*;
use crate::util::{js_round, to_fixed};
use std::collections::{HashMap, HashSet};

/// Задержка обработки кадра устройством, мкс.
fn proc_us(kind: DeviceKind) -> f64 {
    match kind {
        DeviceKind::Host | DeviceKind::Server => 20.0,
        DeviceKind::Router | DeviceKind::Internet => 50.0,
        DeviceKind::Switch => 5.0,
        DeviceKind::Hub => 1.0,
    }
}

const ARP_SIZE: u32 = 60;

fn ip_frame_size(p: Proto) -> u32 {
    match p {
        Proto::Icmp => 98,
        Proto::Tcp | Proto::Udp => 74,
    }
}

/// Число как в шаблонной строке JavaScript; отсутствующее — «undefined».
fn on(o: Option<i64>) -> String {
    o.map(|v| v.to_string()).unwrap_or_else(|| "undefined".into())
}

/* ---- маршруты ---- */

/// Строка таблицы маршрутов: сеть, префикс, шлюз, интерфейс и признак «подключена напрямую».
#[derive(Clone, Debug, PartialEq)]
pub struct RouteEntry {
    pub net: u32,
    pub prefix: u32,
    pub via: Option<u32>,
    pub dev: String,
    pub connected: bool,
}

/// Таблица маршрутов устройства: подключённые сети и статические маршруты. `no_tun` — без туннельных интерфейсов.
pub fn route_table(d: &Device, no_tun: bool) -> Vec<RouteEntry> {
    let mut out: Vec<RouteEntry> = Vec::new();
    for i in &d.ifaces {
        if i.ip.is_none() || !i.up {
            continue;
        }
        if no_tun && i.tun.is_some() {
            continue;
        }
        let ip = parse_ip_opt(i.ip.as_deref());
        out.push(RouteEntry {
            net: network_of(ip, i.prefix as u32),
            prefix: i.prefix as u32,
            via: None,
            dev: i.name.clone(),
            connected: true,
        });
    }
    for r in &d.routes {
        let Some((net, prefix)) = parse_net(Some(&r.dst)) else { continue };
        let via = match r.via.as_deref() {
            Some(v) if !v.is_empty() => parse_ip(v),
            _ => None,
        };
        let mut dev = r.dev.clone().filter(|s| !s.is_empty());
        if via.is_some() && dev.is_none() {
            dev = out.iter().find(|c| c.connected && in_net(via, Some(c.net), c.prefix)).map(|c| c.dev.clone());
        }
        let Some(dev) = dev else { continue };
        let Some(ifc) = d.iface(&dev) else { continue };
        if !ifc.up || ifc.ip.is_none() || (no_tun && ifc.tun.is_some()) {
            continue;
        }
        out.push(RouteEntry { net, prefix, via, dev, connected: false });
    }
    out
}

/// Лучший маршрут до адреса: самый длинный префикс, при равенстве — подключённая сеть.
pub fn lookup(d: &Device, dst: Option<u32>, no_tun: bool) -> Option<RouteEntry> {
    let mut best: Option<RouteEntry> = None;
    for r in route_table(d, no_tun) {
        if !in_net(dst, Some(r.net), r.prefix) {
            continue;
        }
        let better = match &best {
            None => true,
            Some(b) => r.prefix > b.prefix || (r.prefix == b.prefix && r.connected && !b.connected),
        };
        if better {
            best = Some(r);
        }
    }
    best
}

/// Адреса всех интерфейсов устройства.
pub fn own_ips(d: &Device) -> Vec<u32> {
    d.ifaces.iter().filter(|i| i.ip.is_some()).filter_map(|i| parse_ip_opt(i.ip.as_deref())).collect()
}

/* ---- кортежи соединений (conntrack) ---- */

pub(crate) fn tuple_of(p: &Packet) -> Tuple {
    let (sport, dport) = if p.proto == Proto::Icmp {
        let id = p.icmp.as_ref().map(|i| i.id);
        (id, id)
    } else {
        (p.sport, p.dport)
    };
    Tuple { proto: p.proto, src: p.src, dst: p.dst, sport, dport }
}

fn reverse(t: &Tuple) -> Tuple {
    Tuple { proto: t.proto, src: Some(t.dst), dst: t.src.unwrap_or(0), sport: t.dport, dport: t.sport }
}

fn apply_tuple(p: &mut Packet, t: &Tuple) {
    p.src = t.src;
    p.dst = t.dst;
    if p.proto == Proto::Icmp {
        return;
    }
    p.sport = t.sport;
    p.dport = t.dport;
}

/* ---- описание кадров для подписей и журнала ---- */

pub(crate) fn describe(f: &Frame) -> String {
    match &f.body {
        Payload::Arp(a) => {
            if a.op == ArpOp::Req {
                format!("ARP: у кого {}?", ip_str(a.tip))
            } else {
                format!("ARP: {} — это {}", ip_str(a.sip), a.smac)
            }
        }
        Payload::Ip(p) => {
            let addr = format!("{}→{}", ip_str_opt(p.src), ip_str(p.dst));
            if p.proto == Proto::Icmp {
                let nm = match p.icmp.as_ref().map(|i| i.typ) {
                    Some(IcmpType::EchoReq) => "ICMP echo",
                    Some(IcmpType::EchoRep) => "ICMP ответ",
                    Some(IcmpType::Ttl) => "ICMP TTL истёк",
                    _ => "ICMP недоступно",
                };
                return format!("{nm} {addr}");
            }
            if let Some(t) = &p.tunnel {
                return format!(
                    "VPN-туннель {}→{} (внутри: {}→{} {})",
                    ip_str_opt(p.src),
                    ip_str(p.dst),
                    ip_str_opt(t.inner.src),
                    ip_str(t.inner.dst),
                    t.inner.proto.as_str()
                );
            }
            if p.proto == Proto::Udp {
                if let Some(dns) = &p.dns {
                    return if dns.response {
                        let rc = dns.rcode.map(|r| r.as_str()).unwrap_or("undefined");
                        let rf = dns.referral.as_ref().map(|r| format!(" (реферал {})", r.zone)).unwrap_or_default();
                        format!("DNS ответ {rc}{rf} {}→{}", ip_str_opt(p.src), ip_str(p.dst))
                    } else {
                        format!("DNS {} {}? {}→{}", dns.q.name, dns.q.typ, ip_str_opt(p.src), ip_str(p.dst))
                    };
                }
                return format!("UDP {}:{}→{}:{}", ip_str_opt(p.src), on(p.sport), ip_str(p.dst), on(p.dport));
            }
            let fl = p.flags.map(|f| f.as_str()).unwrap_or("undefined");
            let sq = match p.seq {
                Some(seq) => {
                    let ack = if p.flags.map(|f| f.has_ack()).unwrap_or(false) { format!(" ack={}", on(p.ack)) } else { String::new() };
                    let len = match p.len {
                        Some(l) if l != 0 => format!(" len={l}"),
                        _ => String::new(),
                    };
                    format!(" seq={seq}{ack}{len}")
                }
                None => String::new(),
            };
            format!("TCP {fl}{sq} {}:{}→{}:{}", ip_str_opt(p.src), on(p.sport), ip_str(p.dst), on(p.dport))
        }
    }
}

fn kind_of(f: &Frame) -> FrameKind {
    match &f.body {
        Payload::Arp(_) => FrameKind::Arp,
        Payload::Ip(p) => match p.proto {
            Proto::Tcp => FrameKind::Tcp,
            Proto::Udp => FrameKind::Udp,
            Proto::Icmp => FrameKind::Icmp,
        },
    }
}

/// Слушает ли служба на адрес `dst` (учёт привязки `bind`).
pub(crate) fn bind_ok(svc: &Service, dst: Option<u32>) -> bool {
    match svc.bind.as_deref() {
        None | Some("") | Some("0.0.0.0") => true,
        Some(b) => parse_ip(b) == dst || (b == "127.0.0.1" && (dst.unwrap_or(0) >> 24) == 127),
    }
}

/// Текущая проба симулятора: кто её послал и чем она закончилась.
#[derive(Clone, Debug)]
pub struct Probe {
    pub origin: String,
    pub id: i64,
    pub sport: Option<i64>,
    pub result: Option<ProbeResult>,
    pub dst: Option<u32>,
    pub session: bool,
}

#[derive(Clone, Debug)]
pub struct ProbeResult {
    pub status: ProbeStatus,
    pub from: Option<u32>,
    pub at: f64,
    pub ttl: Option<i64>,
    pub code: Option<IcmpCode>,
    pub mtu: Option<u32>,
    pub dns: Option<DnsMessage>,
}

impl ProbeResult {
    fn new(status: ProbeStatus, from: Option<u32>, at: f64) -> ProbeResult {
        ProbeResult { status, from, at, ttl: None, code: None, mtu: None, dns: None }
    }
}

/// Симулятор одной пробы над состоянием сети. Устройства и кабели только читаются, меняются кэши (`rt`).
pub struct Sim<'a> {
    pub(crate) devices: &'a Devices,
    pub(crate) links: &'a [Link],
    pub(crate) rt: &'a mut Runtime,
    pub(crate) id: i64,
    pub events: Vec<NetEvent>,
    pub hops: Vec<Hop>,
    pub delivered: Vec<Delivered>,
    pub probe: Option<Probe>,
    resolving: HashSet<String>,
    seen: HashSet<String>,
    pub(crate) dns_pend: HashMap<String, crate::dns::DnsPending>,
    pub(crate) dns_seq: i64,
    uid_seq: u64,
}

impl<'a> Sim<'a> {
    pub fn new(state: &'a mut NetState) -> Sim<'a> {
        let NetState { devices, links, rt, .. } = state;
        rt.sim_seq += 1;
        Sim {
            devices: &*devices,
            links: &links[..],
            id: rt.sim_seq,
            rt,
            events: Vec::new(),
            hops: Vec::new(),
            delivered: Vec::new(),
            probe: None,
            resolving: HashSet::new(),
            seen: HashSet::new(),
            dns_pend: HashMap::new(),
            dns_seq: 0,
            uid_seq: 0,
        }
    }

    pub fn dev(&self, id: &str) -> Option<&'a Device> {
        let devices: &'a Devices = self.devices;
        devices.get(id)
    }

    pub fn log(&mut self, t: f64, dev: &str, kind: EventKind, text: impl Into<String>) {
        self.events.push(NetEvent { t, dev: dev.to_string(), kind, text: text.into() });
    }

    fn peer(&self, dev: &str, port: &str) -> Option<(String, String, &'a Link)> {
        let links: &'a [Link] = self.links;
        let key = port_ref(dev, port);
        let l = links.iter().find(|l| l.a == key || l.b == key)?;
        let other = if l.a == key { &l.b } else { &l.a };
        let (d, p) = crate::model::split_ref(other);
        // обе стороны кабеля должны существовать
        self.dev(d)?.iface(p)?;
        Some((d.to_string(), p.to_string(), l))
    }

    /* --- уровень 2 --- */

    pub(crate) fn xmit(&mut self, dev_id: &str, port: &str, frame: Frame, at: f64) {
        let Some(d) = self.dev(dev_id) else { return };
        let Some(ifc) = d.iface(port) else { return };
        let Some((peer_dev, peer_port, link)) = self.peer(dev_id, port) else {
            self.log(at, dev_id, EventKind::Drop, format!("порт {port}: кабель не подключён"));
            return;
        };
        if !ifc.up {
            self.log(at, dev_id, EventKind::Drop, format!("порт {port} выключен"));
            return;
        }
        if let Payload::Ip(p) = &frame.body {
            if let Some(size) = p.size.filter(|s| *s != 0) {
                let mtu = ifc.mtu.unwrap_or(1500).min(link.mtu.unwrap_or(1500)) as i64;
                if size > mtu {
                    let origin = self.probe.as_ref().map(|x| x.origin == dev_id).unwrap_or(false) && !p.fwd;
                    if origin {
                        self.log(
                            at,
                            dev_id,
                            EventKind::Drop,
                            format!("пакет {size} Б больше MTU {mtu} интерфейса {port}: message too long"),
                        );
                        if let Some(pr) = self.probe.as_mut() {
                            if pr.result.is_none() {
                                let mut r = ProbeResult::new(ProbeStatus::Toolong, None, at);
                                r.mtu = Some(mtu as u32);
                                pr.result = Some(r);
                            }
                        }
                        return;
                    }
                    if p.df {
                        let tail = if d.icmp_block {
                            " — ICMP «frag needed» тоже заблокирован: отправитель ничего не узнает"
                        } else {
                            " — шлю ICMP «frag needed»"
                        };
                        self.log(
                            at,
                            dev_id,
                            EventKind::Drop,
                            format!("пакет {size} Б не лезет в MTU {mtu}, а запрещена фрагментация (DF){tail}"),
                        );
                        if !d.icmp_block {
                            self.icmp_error(d, ifc.ip.as_deref(), p, IcmpType::Unreach, at, Some(IcmpCode::Frag), Some(mtu as u32));
                        }
                        return;
                    }
                    self.log(at, dev_id, EventKind::Info, format!("пакет {size} Б больше MTU {mtu}: фрагментирую"));
                }
            }
        }
        let mbps = if link.mbps == 0.0 { 1000.0 } else { link.mbps };
        let dt = js_round((frame.size as f64 * 8.0) / mbps) + js_round(link.km * 5.0);
        let t1 = at + dt.max(1.0);
        self.hops.push(Hop {
            from: dev_id.to_string(),
            from_port: port.to_string(),
            to: peer_dev.clone(),
            to_port: peer_port.clone(),
            t0: at,
            t1,
            kind: kind_of(&frame),
            label: describe(&frame),
            frame: frame.clone(),
        });
        self.recv(&peer_dev, &peer_port, frame, t1);
    }

    fn recv(&mut self, dev_id: &str, port: &str, frame: Frame, at: f64) {
        let Some(d) = self.dev(dev_id) else { return };
        if d.kind == DeviceKind::Switch {
            return self.switch_in(d, port, frame, at);
        }
        if d.kind == DeviceKind::Hub {
            return self.hub_in(d, port, frame, at);
        }
        let Some(ifc) = d.iface(port) else { return };
        if !ifc.up {
            return self.log(at, dev_id, EventKind::Drop, format!("порт {port} выключен"));
        }
        if frame.dst != ifc.mac && frame.dst != BCAST_MAC {
            return; // чужой кадр
        }
        let t = at + proc_us(d.kind);
        match frame.body {
            Payload::Arp(a) => self.arp_in(d, ifc, &a, t),
            Payload::Ip(p) => self.ip_in(d, Some(ifc), p, t),
        }
    }

    /// Кадр уже проходил через это устройство — значит, в сети петля.
    fn loop_seen(&mut self, d: &Device, frame: &mut Frame, at: f64) -> bool {
        if frame.uid.is_none() {
            self.uid_seq += 1;
            frame.uid = Some(self.uid_seq);
        }
        let key = format!("{}|{}", d.id, frame.uid.unwrap_or(0));
        if self.seen.contains(&key) {
            self.log(at, &d.id, EventKind::Loop, "этот кадр уже проходил здесь — в сети петля, кадры будут ходить по кругу");
            return true;
        }
        self.seen.insert(key);
        false
    }

    fn hub_in(&mut self, d: &'a Device, port: &str, mut frame: Frame, at: f64) {
        if self.loop_seen(d, &mut frame, at) {
            return;
        }
        let t = at + proc_us(DeviceKind::Hub);
        self.log(t, &d.id, EventKind::Learn, "хаб повторяет кадр на все остальные порты");
        for i in &d.ifaces {
            if i.name != port {
                self.xmit(&d.id, &i.name, frame.clone(), t);
            }
        }
    }

    fn switch_in(&mut self, d: &'a Device, port: &str, mut frame: Frame, at: f64) {
        if self.loop_seen(d, &mut frame, at) {
            return;
        }
        let Some(pin) = d.iface(port) else { return };
        if !pin.up {
            return self.log(at, &d.id, EventKind::Drop, format!("порт {port} выключен"));
        }
        let vlan = if pin.trunk { frame.vlan.unwrap_or(1) } else { pin.vlan.unwrap_or(1) };
        let key = |m: &str| if vlan == 1 { m.to_string() } else { format!("{m}@vlan{vlan}") };
        let learned = {
            let mt = self.rt.mac.entry(d.id.clone()).or_default();
            if frame.src != BCAST_MAC && mt.get(&key(&frame.src)).map(|p| p.as_str()) != Some(port) {
                mt.insert(key(&frame.src), port.to_string());
                true
            } else {
                false
            }
        };
        if learned {
            let tail = if vlan == 1 { String::new() } else { format!(" (VLAN {vlan})") };
            self.log(at, &d.id, EventKind::Learn, format!("запомнил: {} за портом {port}{tail}", frame.src));
        }
        let t = at + proc_us(DeviceKind::Switch);
        let known: Option<String> =
            if frame.dst != BCAST_MAC { self.rt.mac.get(&d.id).and_then(|m| m.get(&key(&frame.dst))).cloned() } else { None };
        if let Some(known) = known.filter(|k| !k.is_empty()) {
            if known == port {
                return;
            }
            return self.switch_out(d, &known, &frame, vlan, t);
        }
        let text = if frame.dst == BCAST_MAC {
            "широковещательный кадр — рассылаю во все порты этого VLAN".to_string()
        } else {
            format!("адрес {} неизвестен — рассылаю во все порты этого VLAN", frame.dst)
        };
        self.log(t, &d.id, EventKind::Learn, text);
        for i in &d.ifaces {
            if i.name != port {
                self.switch_out(d, &i.name, &frame, vlan, t);
            }
        }
    }

    fn switch_out(&mut self, d: &'a Device, name: &str, frame: &Frame, vlan: u32, t: f64) {
        let Some(e) = d.iface(name) else { return };
        if e.trunk {
            let mut f = frame.clone();
            f.vlan = Some(vlan);
            return self.xmit(&d.id, name, f, t);
        }
        if e.vlan.unwrap_or(1) != vlan {
            return;
        }
        let mut f = frame.clone();
        f.vlan = None;
        self.xmit(&d.id, name, f, t);
    }

    /* --- ARP --- */

    fn arp_in(&mut self, d: &'a Device, ifc: &'a Iface, a: &ArpInfo, at: f64) {
        let Some(ip) = ifc.ip.as_deref() else { return };
        if Some(a.tip) != parse_ip(ip) {
            return;
        }
        let sim_id = self.id;
        let prev = self.rt.arp.entry(d.id.clone()).or_default().get(&a.sip).cloned();
        if let Some(p) = &prev {
            if p.sim == sim_id && p.mac != a.smac {
                self.log(
                    at,
                    &d.id,
                    EventKind::Conflict,
                    format!("конфликт адресов: {} отвечают сразу два устройства ({} и {})", ip_str(a.sip), p.mac, a.smac),
                );
            }
        }
        self.rt.arp.entry(d.id.clone()).or_default().insert(a.sip, ArpEntry { mac: a.smac.clone(), at, sim: sim_id });
        if a.op == ArpOp::Req {
            self.log(at, &d.id, EventKind::Arp, format!("{} — это я, отвечаю {}", ip, ifc.mac));
            let rep = Frame {
                size: ARP_SIZE,
                src: ifc.mac.clone(),
                dst: a.smac.clone(),
                vlan: None,
                uid: None,
                body: Payload::Arp(ArpInfo { op: ArpOp::Rep, sip: a.tip, smac: ifc.mac.clone(), tip: a.sip, tmac: Some(a.smac.clone()) }),
            };
            self.xmit(&d.id, &ifc.name, rep, at);
        }
    }

    fn resolve(&mut self, d: &'a Device, ifc: &'a Iface, next_hop: u32, at: f64) -> Option<(String, f64)> {
        if let Some(st) = d.arp_static.get(&ip_str(next_hop)) {
            if !st.is_empty() {
                return Some((st.clone(), at));
            }
        }
        let sim_id = self.id;
        let known = |e: &ArpEntry| (e.mac.clone(), if e.sim == sim_id { at.max(e.at) } else { at });
        if let Some(e) = self.rt.arp.get(&d.id).and_then(|c| c.get(&next_hop)) {
            return Some(known(e));
        }
        let key = format!("{}:{}", d.id, next_hop);
        if self.resolving.contains(&key) {
            return None;
        }
        self.resolving.insert(key.clone());
        self.log(at, &d.id, EventKind::Arp, format!("нужен MAC для {} — спрашиваю ARP-запросом", ip_str(next_hop)));
        let req = Frame {
            size: ARP_SIZE,
            src: ifc.mac.clone(),
            dst: BCAST_MAC.to_string(),
            vlan: None,
            uid: None,
            body: Payload::Arp(ArpInfo {
                op: ArpOp::Req,
                sip: parse_ip_opt(ifc.ip.as_deref()).unwrap_or(0),
                smac: ifc.mac.clone(),
                tip: next_hop,
                tmac: None,
            }),
        };
        self.xmit(&d.id, &ifc.name, req, at);
        self.resolving.remove(&key);
        self.rt.arp.get(&d.id).and_then(|c| c.get(&next_hop)).map(known)
    }

    /* --- уровень 3: отправка --- */

    pub(crate) fn ip_out(&mut self, d: &'a Device, mut pkt: Packet, at: f64) {
        if own_ips(d).contains(&pkt.dst) {
            if pkt.src.is_none() {
                pkt.src = Some(pkt.dst);
            }
            return self.ip_in(d, None, pkt, at); // сам себе
        }
        let Some(r) = lookup(d, Some(pkt.dst), pkt.no_tun) else {
            return self.log(at, &d.id, EventKind::Drop, format!("нет маршрута до {} (Network is unreachable)", ip_str(pkt.dst)));
        };
        let Some(ifc) = d.iface(&r.dev) else { return };
        if pkt.src.is_none() {
            pkt.src = parse_ip_opt(ifc.ip.as_deref());
        }
        if let Some(tun) = &ifc.tun {
            return self.tun_send(d, ifc, tun, pkt, at);
        }
        let hop = r.via.unwrap_or(pkt.dst);
        let Some((mac, at2)) = self.resolve(d, ifc, hop, at) else {
            return self.log(at + 1000.0, &d.id, EventKind::Drop, format!("{} не ответил на ARP (Host unreachable)", ip_str(hop)));
        };
        let size = ip_frame_size(pkt.proto);
        self.xmit(&d.id, &ifc.name, Frame { size, src: ifc.mac.clone(), dst: mac, vlan: None, uid: None, body: Payload::Ip(pkt) }, at2);
    }

    /// Туннель (VPN): внутренний пакет упаковывается в UDP до пира.
    fn tun_send(&mut self, d: &'a Device, ifc: &'a Iface, tun: &Tun, pkt: Packet, at: f64) {
        let peer = parse_ip(&tun.peer).unwrap_or(0);
        self.log(
            at,
            &d.id,
            EventKind::Tun,
            format!("туннель {}: {}→{} упакован в UDP до {}", ifc.name, ip_str_opt(pkt.src), ip_str(pkt.dst), tun.peer),
        );
        let dport = self.rt.tun_peer.get(&format!("{}:{}", d.id, ifc.name)).and_then(|e| e.port).unwrap_or(tun.port);
        let mut outer = Packet::new(Proto::Udp, peer);
        outer.sport = Some(tun.port);
        outer.dport = Some(dport);
        outer.size = Some(pkt.size.unwrap_or(84).saturating_add(60));
        outer.no_tun = true;
        outer.tunnel = Some(Box::new(Wrapped { inner: pkt, key: tun.key.clone(), name: ifc.name.clone() }));
        self.ip_out(d, outer, at + 15.0);
    }

    fn tun_in(&mut self, d: &'a Device, pkt: &Packet, at: f64) -> bool {
        let tif = d.ifaces.iter().find(|i| {
            i.tun.as_ref().map(|t| Some(t.port) == pkt.dport && parse_ip(&t.peer) == pkt.src && pkt.src.is_some()).unwrap_or(false)
        });
        let (Some(tif), Some(wrapped)) = (tif, pkt.tunnel.as_ref()) else {
            self.log(
                at,
                &d.id,
                EventKind::Drop,
                format!("UDP/{} от {}: туннеля с таким пиром нет — пакет отброшен", on(pkt.dport), ip_str_opt(pkt.src)),
            );
            return true;
        };
        let Some(tun) = tif.tun.as_ref() else { return true };
        if tun.key != wrapped.key {
            self.log(
                at,
                &d.id,
                EventKind::Drop,
                format!("туннель {}: ключ не совпал — пакет от {} отброшен (тишина, как у WireGuard)", tif.name, ip_str_opt(pkt.src)),
            );
            return true;
        }
        self.rt.tun_peer.insert(format!("{}:{}", d.id, tif.name), TunPeer { ip: pkt.src, port: pkt.sport });
        let inner = wrapped.inner.clone();
        self.log(at, &d.id, EventKind::Tun, format!("туннель {}: распаковал {}→{}", tif.name, ip_str_opt(inner.src), ip_str(inner.dst)));
        self.ip_in(d, Some(tif), inner, at + 15.0);
        true
    }

    pub(crate) fn icmp_error(
        &mut self,
        d: &'a Device,
        ifc_ip: Option<&str>,
        pkt: &Packet,
        typ: IcmpType,
        at: f64,
        code: Option<IcmpCode>,
        mtu: Option<u32>,
    ) {
        if d.icmp_block {
            return;
        }
        if pkt.proto == Proto::Icmp {
            let t = pkt.icmp.as_ref().map(|i| i.typ);
            if t != Some(IcmpType::EchoReq) && t != Some(IcmpType::EchoRep) {
                return;
            }
        }
        let orig = tuple_of(pkt);
        let mut err = Packet::new(Proto::Icmp, pkt.src.unwrap_or(0));
        err.src = match ifc_ip {
            Some(ip) if !ip.is_empty() => parse_ip(ip),
            _ => None,
        };
        err.icmp = Some(IcmpInfo { typ, id: 0, orig: Some(orig), code, mtu });
        self.ip_out(d, err, at);
    }

    /* --- уровень 3: приём и пересылка --- */

    pub(crate) fn ip_in(&mut self, d: &'a Device, ifc: Option<&'a Iface>, mut pkt: Packet, at: f64) {
        let tup = tuple_of(&pkt);
        let mut est = false;
        let (rep_i, fwd_i) = {
            let ct = self.rt.ct.entry(d.id.clone()).or_default();
            let rep_i = ct.iter().position(|e| reverse(&e.tr) == tup);
            let fwd_i = if rep_i.is_some() { None } else { ct.iter().position(|e| e.orig == tup) };
            (rep_i, fwd_i)
        };
        let mut found_rep = false;
        let mut found_fwd = false;
        if let Some(i) = rep_i {
            found_rep = true;
            est = true;
            let (tr, orig) = {
                let ct = self.rt.ct.entry(d.id.clone()).or_default();
                ct[i].replied = true;
                (ct[i].tr.clone(), ct[i].orig.clone())
            };
            if tr != orig {
                self.log(
                    at,
                    &d.id,
                    EventKind::Nat,
                    format!("NAT: ответ {}→{} возвращаю клиенту {}", ip_str_opt(pkt.src), ip_str(pkt.dst), ip_str_opt(orig.src)),
                );
            }
            apply_tuple(&mut pkt, &reverse(&orig));
        } else if let Some(i) = fwd_i {
            found_fwd = true;
            let (replied, tr) = {
                let ct = self.rt.ct.entry(d.id.clone()).or_default();
                (ct[i].replied, ct[i].tr.clone())
            };
            est = replied;
            apply_tuple(&mut pkt, &tr);
        } else if pkt.proto == Proto::Icmp && pkt.icmp.as_ref().and_then(|i| i.orig.as_ref()).is_some() {
            // ошибка ICMP про уже трансформированный пакет
            let inner = pkt.icmp.as_ref().and_then(|i| i.orig.clone());
            if let Some(inner) = inner {
                let e = self.rt.ct.entry(d.id.clone()).or_default().iter().find(|x| x.tr == inner).cloned();
                if let Some(e) = e {
                    pkt.dst = e.orig.src.unwrap_or(0);
                    if let Some(ic) = pkt.icmp.as_mut() {
                        ic.orig = Some(e.orig.clone());
                    }
                }
            }
        } else if let Some(ifc) = ifc {
            let rule = d.nat.iter().find(|n| {
                n.chain == NatChain::Prerouting
                    && n.action == NatAction::Dnat
                    && n.iif.as_deref().map(|x| x.is_empty() || x == ifc.name).unwrap_or(true)
                    && n.dst.as_deref().map(|x| x.is_empty() || in_net_str(Some(pkt.dst), Some(x))).unwrap_or(true)
                    && n.proto.as_deref().map(|x| x.is_empty() || x == pkt.proto.as_str()).unwrap_or(true)
                    && n.dport.map(|x| x == 0 || Some(x) == pkt.dport).unwrap_or(true)
            });
            if let Some(rule) = rule {
                let to = rule.to.clone().unwrap_or_default();
                let mut parts = to.split(':');
                let h = parts.next().unwrap_or("");
                let p = parts.next();
                if let Some(nd) = parse_ip(h) {
                    let ptxt = match p {
                        Some(p) if !p.is_empty() => format!(":{p}"),
                        _ => String::new(),
                    };
                    self.log(at, &d.id, EventKind::Nat, format!("DNAT: {}:{} → {h}{ptxt}", ip_str(pkt.dst), on(pkt.dport)));
                    pkt.dst = nd;
                    if let Some(p) = p.filter(|p| !p.is_empty()) {
                        pkt.dport = Some(crate::util::to_int(crate::util::js_num(p)));
                    }
                }
            }
        }

        if !found_rep && !found_fwd {
            if let Some(lb) = &d.lb {
                if pkt.proto == Proto::Tcp && pkt.dport == Some(lb.port) && parse_ip(&lb.vip) == Some(pkt.dst) {
                    return self.lb_in(d, pkt, at, tup);
                }
            }
        }
        if own_ips(d).contains(&pkt.dst) {
            return self.local_in(d, pkt, at);
        }
        if !d.forward {
            return self.log(
                at,
                &d.id,
                EventKind::Drop,
                format!("пакет для {} — не мне, а пересылка выключена (ip_forward=0)", ip_str(pkt.dst)),
            );
        }
        self.forward(d, ifc, pkt, at, est, tup);
    }

    /* --- балансировщик (L4): виртуальный адрес → один из бэкендов; источник подменяется на адрес балансировщика --- */

    pub(crate) fn backend_dev(&self, ip: &str) -> Option<&'a Device> {
        let n = parse_ip(ip);
        let devices: &'a Devices = self.devices;
        devices.iter().find(|x| x.ifaces.iter().any(|i| i.ip.is_some() && parse_ip_opt(i.ip.as_deref()) == n))
    }

    fn backend_up(&self, b: &LbBackend) -> bool {
        let Some(dev) = self.backend_dev(&b.ip) else { return false };
        let n = parse_ip(&b.ip);
        let ifc = dev.ifaces.iter().find(|i| i.ip.is_some() && parse_ip_opt(i.ip.as_deref()) == n);
        ifc.map(|i| i.up).unwrap_or(false) && dev.services.iter().any(|s| s.proto == Proto::Tcp && s.port == b.port && bind_ok(s, n))
    }

    fn lb_in(&mut self, d: &'a Device, mut pkt: Packet, at: f64, tup: Tuple) {
        let Some(lb) = &d.lb else { return };
        let live: Vec<&LbBackend> =
            if lb.health { lb.backends.iter().filter(|b| self.backend_up(b)).collect() } else { lb.backends.iter().collect() };
        if live.is_empty() {
            return self.log(at, &d.id, EventKind::Drop, "балансировщик: нет живых серверов в пуле — 503");
        }
        let hash = lb.algo == Some(LbAlgo::Hash);
        let b = if hash {
            live[(pkt.src.unwrap_or(0) as usize) % live.len()]
        } else {
            let n = self.rt.lb.entry(d.id.clone()).or_insert(0);
            let i = *n % live.len();
            *n += 1;
            live[i]
        };
        let Some(r) = lookup(d, parse_ip(&b.ip), false) else {
            return self.log(at, &d.id, EventKind::Drop, format!("балансировщик: нет маршрута до {}", b.ip));
        };
        let Some(out) = d.iface(&r.dev) else { return };
        let how = if hash { "хеш по адресу клиента" } else { "по кругу" };
        self.log(at, &d.id, EventKind::Nat, format!("балансировщик ({how}): {} → сервер {}:{}", ip_str_opt(pkt.src), b.ip, b.port));
        pkt.dst = parse_ip(&b.ip).unwrap_or(0);
        pkt.dport = Some(b.port);
        pkt.src = parse_ip_opt(out.ip.as_deref());
        let used: HashSet<Option<i64>> = self.rt.ct.entry(d.id.clone()).or_default().iter().map(|e| e.tr.sport).collect();
        let mut sp = 41000;
        while used.contains(&Some(sp)) {
            sp += 1;
        }
        pkt.sport = Some(sp);
        pkt.ttl = pkt.ttl.saturating_sub(1).max(1);
        self.rt.ct.entry(d.id.clone()).or_default().push(ConnEntry { orig: tup, tr: tuple_of(&pkt), replied: false });
        pkt.fwd = true;
        self.ip_out(d, pkt, at + 5.0);
    }

    fn forward(&mut self, d: &'a Device, ifc: Option<&'a Iface>, mut pkt: Packet, at: f64, est: bool, orig_tuple: Tuple) {
        if d.drop_private && (is_private(pkt.src) || is_private(Some(pkt.dst))) {
            let shown = if is_private(pkt.src) { pkt.src } else { Some(pkt.dst) };
            return self.log(at, &d.id, EventKind::Drop, format!("интернет не маршрутизирует частные адреса: {}", ip_str_opt(shown)));
        }
        let ifc_ip = ifc.and_then(|i| i.ip.as_deref());
        if pkt.ttl <= 1 {
            self.log(at, &d.id, EventKind::Drop, "TTL истёк — отправителю уходит ICMP «time exceeded»");
            return self.icmp_error(d, ifc_ip, &pkt, IcmpType::Ttl, at, None, None);
        }
        pkt.ttl -= 1;
        let Some(r) = lookup(d, Some(pkt.dst), false) else {
            self.log(at, &d.id, EventKind::Drop, format!("нет маршрута до {} — шлю ICMP «unreachable»", ip_str(pkt.dst)));
            return self.icmp_error(d, ifc_ip, &pkt, IcmpType::Unreach, at, None, None);
        };
        let Some(out) = d.iface(&r.dev) else { return };
        let verdict =
            self.filter(d, &pkt, ifc.map(|i| i.name.as_str()), &out.name, if est { ConnState::Established } else { ConnState::New });
        if verdict != FwAction::Accept {
            self.log(at, &d.id, EventKind::Fw, format!("файрвол: {} {}→{}", verdict.as_str(), ip_str_opt(pkt.src), ip_str(pkt.dst)));
            if verdict == FwAction::Reject {
                self.icmp_error(d, ifc_ip, &pkt, IcmpType::Unreach, at, None, None);
            }
            return;
        }
        if !est {
            let exists = self.rt.ct.entry(d.id.clone()).or_default().iter().any(|e| e.orig == orig_tuple);
            if !exists {
                let rule = d.nat.iter().any(|n| {
                    n.chain == NatChain::Postrouting
                        && n.action == NatAction::Masquerade
                        && n.out.as_deref().map(|x| x.is_empty() || x == out.name).unwrap_or(true)
                        && n.src.as_deref().map(|x| x.is_empty() || in_net_str(pkt.src, Some(x))).unwrap_or(true)
                        && n.dst.as_deref().map(|x| x.is_empty() || in_net_str(Some(pkt.dst), Some(x))).unwrap_or(true)
                });
                if rule && out.ip.is_some() {
                    let before = ip_str_opt(pkt.src);
                    pkt.src = parse_ip_opt(out.ip.as_deref());
                    if pkt.proto != Proto::Icmp {
                        let used: HashSet<Option<i64>> = self.rt.ct.entry(d.id.clone()).or_default().iter().map(|e| e.tr.sport).collect();
                        let mut sp = 40000;
                        while used.contains(&Some(sp)) {
                            sp += 1;
                        }
                        pkt.sport = Some(sp);
                    }
                    let port = if pkt.proto == Proto::Icmp { String::new() } else { format!(":{}", on(pkt.sport)) };
                    self.log(at, &d.id, EventKind::Nat, format!("MASQUERADE: {before} → {}{port}", out.ip.as_deref().unwrap_or("")));
                }
                let ct = self.rt.ct.entry(d.id.clone()).or_default();
                ct.push(ConnEntry { orig: orig_tuple, tr: tuple_of(&pkt), replied: false });
                if ct.len() > 200 {
                    ct.remove(0);
                }
            }
        }
        pkt.fwd = true;
        self.ip_out(d, pkt, at + 5.0);
    }

    fn filter(&self, d: &Device, pkt: &Packet, in_name: Option<&str>, out_name: &str, state: ConnState) -> FwAction {
        let some = |o: &Option<String>| o.as_deref().filter(|s| !s.is_empty()).map(|s| s.to_string());
        for r in &d.fw.rules {
            if let Some(s) = some(&r.src) {
                if !in_net_str(pkt.src, Some(&s)) {
                    continue;
                }
            }
            if let Some(s) = some(&r.dst) {
                if !in_net_str(Some(pkt.dst), Some(&s)) {
                    continue;
                }
            }
            if let Some(p) = some(&r.proto) {
                if p != pkt.proto.as_str() {
                    continue;
                }
            }
            if let Some(p) = r.dport.filter(|p| *p != 0) {
                if Some(p) != pkt.dport {
                    continue;
                }
            }
            if let Some(p) = r.sport.filter(|p| *p != 0) {
                if Some(p) != pkt.sport {
                    continue;
                }
            }
            if let Some(i) = some(&r.iif) {
                if Some(i.as_str()) != in_name {
                    continue;
                }
            }
            if let Some(o) = some(&r.out) {
                if o != out_name {
                    continue;
                }
            }
            if let Some(s) = r.state {
                if s != state {
                    continue;
                }
            }
            return r.action;
        }
        d.fw.policy
    }

    /* --- уровень 4: локальная доставка --- */

    /// Ответ на пакет `pkt` от устройства `d`: адреса меняются местами, TTL 64.
    pub(crate) fn reply(&mut self, d: &'a Device, pkt: &Packet, at: f64, mut extra: Packet) {
        extra.src = Some(pkt.dst);
        extra.dst = pkt.src.unwrap_or(0);
        extra.ttl = 64;
        self.ip_out(d, extra, at + 5.0);
    }

    fn local_in(&mut self, d: &'a Device, pkt: Packet, at: f64) {
        self.delivered.push(Delivered {
            dev: d.id.clone(),
            src: pkt.src,
            dst: Some(pkt.dst),
            proto: pkt.proto,
            dport: pkt.dport,
            sport: pkt.sport,
        });
        match pkt.proto {
            Proto::Icmp => {
                let t = pkt.icmp.as_ref().map(|i| i.typ);
                if t == Some(IcmpType::EchoReq) {
                    self.log(at, &d.id, EventKind::Icmp, format!("echo-запрос от {}, отвечаю", ip_str_opt(pkt.src)));
                    let mut r = Packet::new(Proto::Icmp, 0);
                    r.icmp = Some(IcmpInfo {
                        typ: IcmpType::EchoRep,
                        id: pkt.icmp.as_ref().map(|i| i.id).unwrap_or(0),
                        orig: None,
                        code: None,
                        mtu: None,
                    });
                    return self.reply(d, &pkt, at, r);
                }
                self.probe_reply(d, &pkt, at);
            }
            Proto::Udp => {
                if pkt.tunnel.is_some() && self.tun_in(d, &pkt, at) {
                    return;
                }
                if pkt.dns.is_some() && self.dns_in(d, &pkt, at) {
                    return;
                }
                let svc = d.services.iter().any(|x| x.proto == Proto::Udp && Some(x.port) == pkt.dport && bind_ok(x, Some(pkt.dst)));
                if svc {
                    self.log(at, &d.id, EventKind::Udp, format!("порт {}/udp слушает — отвечаю датаграммой", on(pkt.dport)));
                    let mut r = Packet::new(Proto::Udp, 0);
                    r.sport = pkt.dport;
                    r.dport = pkt.sport;
                    return self.reply(d, &pkt, at, r);
                }
                if self.probe.as_ref().map(|p| p.origin == d.id).unwrap_or(false) {
                    return self.probe_reply(d, &pkt, at);
                }
                self.log(at, &d.id, EventKind::Udp, format!("порт {}/udp никто не слушает — шлю ICMP «порт недоступен»", on(pkt.dport)));
                self.icmp_error(d, None, &pkt, IcmpType::Unreach, at, Some(IcmpCode::Port), None);
            }
            Proto::Tcp => self.tcp_local(d, pkt, at),
        }
    }

    fn tcp_local(&mut self, d: &'a Device, pkt: Packet, at: f64) {
        let sess = self.probe.as_ref().map(|p| p.session).unwrap_or(false);
        let seq0 = pkt.seq.unwrap_or(0);
        let ack0 = pkt.ack.unwrap_or(0);
        let len0 = pkt.len.unwrap_or(0);
        let mk = |flags: TcpFlags, seq: i64, ack: i64, len: i64| {
            let mut r = Packet::new(Proto::Tcp, 0);
            r.sport = pkt.dport;
            r.dport = pkt.sport;
            r.flags = Some(flags);
            r.seq = Some(seq);
            r.ack = Some(ack);
            r.len = Some(len);
            r
        };
        if pkt.flags == Some(TcpFlags::Syn) && self.rt.synflood.contains(&format!("{}:{}", d.id, on(pkt.dport))) && !d.syncookies {
            return self.log(at, &d.id, EventKind::Drop, "очередь полуоткрытых соединений переполнена (SYN-флуд) — новый SYN отброшен");
        }
        if pkt.flags == Some(TcpFlags::Syn) {
            let svc = d.services.iter().any(|s| s.proto == Proto::Tcp && Some(s.port) == pkt.dport && bind_ok(s, Some(pkt.dst)));
            if svc {
                self.log(at, &d.id, EventKind::Tcp, format!("порт {} слушает — отвечаю SYN-ACK", on(pkt.dport)));
                return self.reply(d, &pkt, at, mk(TcpFlags::SynAck, 5000, seq0 + 1, 0));
            }
            self.log(at, &d.id, EventKind::Tcp, format!("порт {} никто не слушает — отвечаю RST", on(pkt.dport)));
            return self.reply(d, &pkt, at, mk(TcpFlags::Rst, 0, seq0 + 1, 0));
        }
        let is_server = self.probe.as_ref().map(|p| d.id != p.origin).unwrap_or(false);
        if sess && is_server {
            // сервер: данные, закрытие
            if pkt.flags == Some(TcpFlags::PshAck) {
                self.log(
                    at,
                    &d.id,
                    EventKind::Tcp,
                    format!("получен запрос ({} Б) — отправляю ответ 1000 Б и закрываю соединение", on(pkt.len)),
                );
                let ack = seq0 + len0;
                self.reply(d, &pkt, at, mk(TcpFlags::PshAck, ack0, ack, 1000));
                return self.reply(d, &pkt, at, mk(TcpFlags::FinAck, ack0 + 1000, ack, 0));
            }
            if pkt.flags == Some(TcpFlags::FinAck) {
                self.log(at, &d.id, EventKind::Tcp, "клиент тоже закрыл — подтверждаю последним ACK, соединение закрыто");
                return self.reply(d, &pkt, at, mk(TcpFlags::Ack, ack0, seq0 + 1, 0));
            }
            return;
        }
        self.probe_reply(d, &pkt, at);
    }

    fn probe_reply(&mut self, d: &'a Device, pkt: &Packet, at: f64) {
        let Some(p) = self.probe.clone() else { return };
        if d.id != p.origin {
            return;
        }
        if p.result.is_some() && !(p.session && pkt.proto == Proto::Tcp) {
            return;
        }
        let who = ip_str_opt(pkt.src);
        let is_reply = (pkt.proto == Proto::Icmp && pkt.icmp.as_ref().map(|i| i.typ) == Some(IcmpType::EchoRep))
            || pkt.proto == Proto::Tcp
            || pkt.proto == Proto::Udp;
        if is_reply {
            if let Some(pd) = p.dst {
                if pkt.src != Some(pd) {
                    return self.log(at, &d.id, EventKind::Drop, format!("ответ пришёл с адреса {who}, а запрос уходил на {} — отбрасываю (так делает любой узел без NAT-обратного преобразования)", ip_str(pd)));
                }
            }
        }
        if pkt.proto == Proto::Icmp {
            let Some(ic) = pkt.icmp.as_ref() else { return };
            let t = ic.typ;
            if t == IcmpType::EchoRep && ic.id == p.id {
                let mut r = ProbeResult::new(ProbeStatus::Reply, pkt.src, at);
                r.ttl = Some(pkt.ttl);
                self.set_result(r);
                self.log(at, &d.id, EventKind::Icmp, format!("получен ответ от {who}"));
            } else if t == IcmpType::Ttl || t == IcmpType::Unreach {
                if let Some(o) = &ic.orig {
                    if o.sport == Some(p.sport.unwrap_or(p.id)) {
                        let mut r = ProbeResult::new(if t == IcmpType::Ttl { ProbeStatus::Ttl } else { ProbeStatus::Unreach }, pkt.src, at);
                        r.code = ic.code;
                        r.mtu = ic.mtu;
                        self.set_result(r);
                        let text = if t == IcmpType::Ttl {
                            format!("{who}: TTL истёк по дороге")
                        } else if ic.code == Some(IcmpCode::Frag) {
                            format!(
                                "{who}: нужна фрагментация, а DF запрещает (MTU {})",
                                ic.mtu.map(|m| m.to_string()).unwrap_or_else(|| "undefined".into())
                            )
                        } else if ic.code == Some(IcmpCode::Port) {
                            format!("{who}: порт недоступен (ICMP port unreachable)")
                        } else {
                            format!("{who}: сеть или узел недоступны")
                        };
                        self.log(at, &d.id, EventKind::Icmp, text);
                    }
                }
            }
        } else if pkt.proto == Proto::Udp && pkt.dport == p.sport {
            let mut r = ProbeResult::new(ProbeStatus::Reply, pkt.src, at);
            r.dns = pkt.dns.clone();
            self.set_result(r);
            self.log(at, &d.id, EventKind::Udp, format!("получена датаграмма-ответ от {who}"));
        } else if pkt.proto == Proto::Tcp && pkt.dport == p.sport {
            let rst = pkt.flags == Some(TcpFlags::Rst);
            let seq0 = pkt.seq.unwrap_or(0);
            let ack0 = pkt.ack.unwrap_or(0);
            let len0 = pkt.len.unwrap_or(0);
            let mk = |flags: TcpFlags, seq: i64, ack: i64, len: i64| {
                let mut r = Packet::new(Proto::Tcp, 0);
                r.sport = p.sport;
                r.dport = pkt.sport;
                r.flags = Some(flags);
                r.seq = Some(seq);
                r.ack = Some(ack);
                r.len = Some(len);
                r
            };
            if pkt.flags == Some(TcpFlags::SynAck) || rst {
                self.set_result(ProbeResult::new(if rst { ProbeStatus::Refused } else { ProbeStatus::Connected }, pkt.src, at));
                self.log(
                    at,
                    &d.id,
                    EventKind::Tcp,
                    if rst {
                        "получен RST — порт закрыт"
                    } else {
                        "получен SYN-ACK — соединение установлено"
                    },
                );
                if p.session && !rst {
                    self.send_from(d, pkt, mk(TcpFlags::Ack, ack0, seq0 + 1, 0), at + 5.0);
                    self.send_from(d, pkt, mk(TcpFlags::PshAck, ack0, seq0 + 1, 100), at + 10.0);
                }
            } else if p.session {
                match pkt.flags {
                    Some(TcpFlags::PshAck) => {
                        self.log(at, &d.id, EventKind::Tcp, format!("получен ответ ({} Б), подтверждаю", on(pkt.len)));
                        self.send_from(d, pkt, mk(TcpFlags::Ack, ack0, seq0 + len0, 0), at + 5.0);
                    }
                    Some(TcpFlags::FinAck) => {
                        self.log(at, &d.id, EventKind::Tcp, "сервер закрыл соединение (FIN) — закрываю свою сторону");
                        self.send_from(d, pkt, mk(TcpFlags::FinAck, ack0, seq0 + 1, 0), at + 5.0);
                    }
                    Some(TcpFlags::Ack) => self.log(at, &d.id, EventKind::Tcp, "последний ACK получен — соединение закрыто"),
                    _ => {}
                }
            }
        }
    }

    fn set_result(&mut self, r: ProbeResult) {
        if let Some(p) = self.probe.as_mut() {
            p.result = Some(r);
        }
    }

    fn send_from(&mut self, d: &'a Device, pkt: &Packet, mut extra: Packet, t: f64) {
        extra.src = Some(pkt.dst);
        extra.dst = pkt.src.unwrap_or(0);
        extra.ttl = 64;
        self.ip_out(d, extra, t);
    }

    /// Завершить пробу: записать перехват, упорядочить события и переходы, собрать итог.
    fn finish(mut self, t0: f64) -> ProbeRun {
        record_capture(&mut self);
        self.events.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap_or(std::cmp::Ordering::Equal));
        self.hops.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap_or(std::cmp::Ordering::Equal));
        let r = self.probe.as_ref().and_then(|p| p.result.clone());
        ProbeRun {
            status: r.as_ref().map(|r| r.status).unwrap_or(ProbeStatus::Timeout),
            from: r.as_ref().and_then(|r| r.from),
            code: r.as_ref().and_then(|r| r.code),
            mtu: r.as_ref().and_then(|r| r.mtu),
            dns: r.as_ref().and_then(|r| r.dns.clone()),
            rtt_us: r.as_ref().map(|r| r.at - t0),
            events: self.events,
            hops: self.hops,
            delivered: self.delivered,
        }
    }
}

/* ---- пробы ---- */

/// Устройство, принявшее пакет для адреса `ip` в ходе пробы.
pub fn delivered_to(state: &NetState, run: &ProbeRun, ip: Option<u32>) -> Option<Device> {
    let id = &run.delivered.iter().find(|x| x.dst == ip)?.dev;
    state.devices.get(id).cloned()
}

fn run_probe(state: &mut NetState, dev_id: &str, probe: Probe, kind: EventKind, text: String, mut pkt: Packet) -> ProbeRun {
    let mut sim = Sim::new(state);
    let Some(d) = sim.dev(dev_id) else { return ProbeRun::empty(ProbeStatus::Timeout) };
    sim.probe = Some(probe);
    let t0 = 0.0;
    sim.log(t0, dev_id, kind, text);
    pkt.src = None;
    sim.ip_out(d, pkt, t0 + proc_us(d.kind));
    sim.finish(t0)
}

/// Параметры одной ICMP-пробы.
#[derive(Clone, Debug)]
pub struct PingOpts {
    pub ttl: i64,
    pub id: i64,
    /// Полезная нагрузка, байт; `None` — обычный пакет.
    pub size: Option<i64>,
    pub df: bool,
}

impl Default for PingOpts {
    fn default() -> Self {
        PingOpts { ttl: 64, id: 1, size: None, df: false }
    }
}

/// Одна ICMP-проба: TTL можно задать (для traceroute).
pub fn ping1(state: &mut NetState, dev_id: &str, dst: u32, o: &PingOpts) -> ProbeRun {
    attacks_before(state);
    let mut pkt = Packet::new(Proto::Icmp, dst);
    pkt.ttl = o.ttl;
    pkt.icmp = Some(IcmpInfo { typ: IcmpType::EchoReq, id: o.id, orig: None, code: None, mtu: None });
    if let Some(s) = o.size {
        pkt.size = Some(s.saturating_add(28));
        pkt.df = o.df;
    }
    let probe = Probe { origin: dev_id.to_string(), id: o.id, sport: None, result: None, dst: Some(dst), session: false };
    run_probe(state, dev_id, probe, EventKind::Icmp, format!("ping {}", ip_str(dst)), pkt)
}

/// TCP-подключение к порту: SYN → SYN-ACK / RST / тишина. `session` — полный сеанс с данными и закрытием.
pub fn tcp1(state: &mut NetState, dev_id: &str, dst: u32, port: i64, sport: i64, session: bool) -> ProbeRun {
    attacks_before(state);
    let mut pkt = Packet::new(Proto::Tcp, dst);
    pkt.sport = Some(sport);
    pkt.dport = Some(port);
    pkt.flags = Some(TcpFlags::Syn);
    pkt.seq = Some(1000);
    pkt.ack = Some(0);
    pkt.len = Some(0);
    let probe = Probe { origin: dev_id.to_string(), id: 0, sport: Some(sport), result: None, dst: Some(dst), session };
    run_probe(state, dev_id, probe, EventKind::Tcp, format!("подключаюсь к {}:{}", ip_str(dst), port), pkt)
}

/// Одна UDP-датаграмма на порт: ответ, ICMP «порт недоступен» или тишина.
pub fn udp1(state: &mut NetState, dev_id: &str, dst: u32, port: i64, sport: i64) -> ProbeRun {
    let mut pkt = Packet::new(Proto::Udp, dst);
    pkt.sport = Some(sport);
    pkt.dport = Some(port);
    let probe = Probe { origin: dev_id.to_string(), id: 0, sport: Some(sport), result: None, dst: Some(dst), session: false };
    run_probe(state, dev_id, probe, EventKind::Udp, format!("отправляю датаграмму на {}:{}/udp", ip_str(dst), port), pkt)
}

/// DNS-запрос с устройства: вопрос `q` к серверу `server`.
pub fn dns1(state: &mut NetState, dev_id: &str, server: u32, q: DnsQuestion, rd: bool) -> ProbeRun {
    let sport = 50002;
    let mut pkt = Packet::new(Proto::Udp, server);
    pkt.sport = Some(sport);
    pkt.dport = Some(53);
    let text = format!("спрашиваю {}: «{} {}»", ip_str(server), q.name, q.typ);
    pkt.dns = Some(DnsMessage { id: 1, q, response: false, rd: Some(rd), ra: None, rcode: None, answers: None, referral: None });
    let probe = Probe { origin: dev_id.to_string(), id: 0, sport: Some(sport), result: None, dst: Some(server), session: false };
    run_probe(state, dev_id, probe, EventKind::Dns, text, pkt)
}

/// Проба ICMP с растущим TTL до ответа, «недоступно» или трёх тишин подряд.
pub fn traceroute(state: &mut NetState, dev_id: &str, dst: u32, max_hops: i64) -> Vec<(i64, ProbeRun)> {
    let mut hops = Vec::new();
    let mut misses = 0;
    for ttl in 1..=max_hops {
        let r = ping1(state, dev_id, dst, &PingOpts { ttl, id: 100 + ttl, size: None, df: false });
        let status = r.status;
        hops.push((ttl, r));
        if status == ProbeStatus::Reply || status == ProbeStatus::Unreach {
            break;
        }
        if status == ProbeStatus::Timeout {
            misses += 1;
            if misses >= 3 {
                break;
            }
        }
    }
    hops
}

/// «3.141 мс» / «12.3 мс»; `None` — «—».
pub fn fmt_ms(us: Option<f64>) -> String {
    match us {
        None => "—".into(),
        Some(us) => format!("{} мс", to_fixed(us / 1000.0, if us < 10000.0 { 3 } else { 1 })),
    }
}
