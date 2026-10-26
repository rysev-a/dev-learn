//! DNS в симуляторе: авторитативные серверы (записи, делегирования), рекурсивный резолвер (итеративный обход
//! от корня, CNAME, кэш) и клиентские настройки (resolv.conf, hosts). Запросы и ответы — настоящие
//! UDP-датаграммы на порт 53, поэтому видны в журнале и в анимации.

use crate::ip::*;
use crate::sim::Sim;
use crate::types::*;
use crate::util::utf16_len;

/// Имя в нижнем регистре без пробелов и без завершающей точки.
pub fn fqdn(s: &str) -> String {
    let t = s.trim().to_lowercase();
    match t.strip_suffix('.') {
        Some(x) => x.to_string(),
        None => t,
    }
}

fn in_zone(name: &str, zone: &str) -> bool {
    zone.is_empty() || name == zone || name.ends_with(&format!(".{zone}"))
}

/// Пустая конфигурация DNS-сервера.
pub fn new_dns() -> DnsConfig {
    DnsConfig::default()
}

/// Ответ авторитативного сервера: код, записи и реферал.
#[derive(Clone, Debug, PartialEq)]
pub struct DnsAnswer {
    pub rcode: Rcode,
    pub answers: Vec<DnsRecord>,
    pub referral: Option<Referral>,
}

fn rr(r: &DnsRecord) -> DnsRecord {
    DnsRecord { name: fqdn(&r.name), typ: r.typ.clone(), value: r.value.clone(), ttl: Some(r.ttl.unwrap_or(300)) }
}

/// Самый длинный элемент (при равенстве — первый).
fn longest<T>(items: Vec<T>, len: impl Fn(&T) -> usize) -> Option<T> {
    let mut best: Option<(usize, T)> = None;
    for it in items {
        let l = len(&it);
        if best.as_ref().map(|(b, _)| l > *b).unwrap_or(true) {
            best = Some((l, it));
        }
    }
    best.map(|(_, t)| t)
}

/// Ответ авторитативного сервера на вопрос `q`.
pub fn auth_answer(dns: &DnsConfig, q: &DnsQuestion) -> DnsAnswer {
    let name = fqdn(&q.name);
    let here: Vec<&DnsRecord> = dns.records.iter().filter(|r| fqdn(&r.name) == name).collect();
    let exact: Vec<&DnsRecord> = here.iter().copied().filter(|r| r.typ == q.typ).collect();
    if !exact.is_empty() {
        return DnsAnswer { rcode: Rcode::NoError, answers: exact.into_iter().map(rr).collect(), referral: None };
    }
    if let Some(cn) = here.iter().find(|r| r.typ == "CNAME") {
        if q.typ != "CNAME" {
            return DnsAnswer { rcode: Rcode::NoError, answers: vec![rr(cn)], referral: None };
        }
    }
    // делегирование: самая длинная подходящая зона (но своя зона важнее более короткой чужой)
    let del = longest(dns.delegations.iter().filter(|d| in_zone(&name, &fqdn(&d.zone))).collect(), |d| utf16_len(&fqdn(&d.zone)));
    // как в исходной реализации, пустая строка (корневая зона) в проверке «есть своя зона» считается «нет»
    let own = longest(dns.zones.iter().filter(|z| in_zone(&name, &fqdn(z))).collect(), |z| utf16_len(&fqdn(z))).filter(|z| !z.is_empty());
    if let Some(del) = del {
        if own.map(|o| utf16_len(&fqdn(&del.zone)) > utf16_len(&fqdn(o))).unwrap_or(true) {
            return DnsAnswer {
                rcode: Rcode::NoError,
                answers: vec![],
                referral: Some(Referral { zone: fqdn(&del.zone), ns: del.ns.clone() }),
            };
        }
    }
    if own.is_some() {
        return DnsAnswer { rcode: if here.is_empty() { Rcode::NxDomain } else { Rcode::NoError }, answers: vec![], referral: None };
    }
    DnsAnswer { rcode: Rcode::Refused, answers: vec![], referral: None }
}

/// Клиент, которому резолвер должен ответить.
#[derive(Clone, Debug)]
pub struct DnsClient {
    pub id: i64,
    pub dport: Option<i64>,
    pub src_ip: u32,
    pub dst_ip: u32,
}

/// Состояние рекурсивного резолвера: клиент и ход обхода.
#[derive(Clone, Debug)]
pub struct DnsPending {
    pub client: DnsClient,
    pub q: DnsQuestion,
    pub cur: DnsQuestion,
    pub chain: Vec<DnsRecord>,
    pub hops: u32,
}

fn dns_msg(id: i64, q: DnsQuestion) -> DnsMessage {
    DnsMessage { id, q, response: true, rd: None, ra: None, rcode: Some(Rcode::NoError), answers: None, referral: None }
}

impl<'a> Sim<'a> {
    /// Обработка DNS-пакета на устройстве `d`; `true` — пакет обработан.
    pub(crate) fn dns_in(&mut self, d: &'a Device, pkt: &Packet, at: f64) -> bool {
        let Some(m) = pkt.dns.as_ref() else { return false };
        if m.response {
            let Some(st) = self.dns_pend.remove(&format!("{}:{}", d.id, m.id)) else {
                return false; // ответ клиенту-источнику пробы
            };
            self.resolver_step(d, st, m, at);
            return true;
        }
        let Some(cfg) = d.dns.as_ref() else { return false };
        let q = m.q.clone();
        let name = fqdn(&q.name);
        let who = if cfg.recursive && m.rd == Some(true) { "резолвер" } else { "сервер" };
        self.log(at, &d.id, EventKind::Dns, format!("{who}: вопрос «{name} {}»", q.typ));
        let reply_msg = |extra: DnsMessage| {
            let mut r = Packet::new(Proto::Udp, 0);
            r.sport = Some(53);
            r.dport = pkt.sport;
            r.dns = Some(extra);
            r
        };
        if cfg.recursive && m.rd == Some(true) {
            let key = format!("{name}|{}", q.typ);
            let hit = self.rt.dns_cache.get(&d.id).and_then(|c| c.get(&key)).cloned();
            if let Some(hit) = hit {
                let vals: Vec<&str> = hit.iter().map(|a| a.value.as_str()).collect();
                self.log(at, &d.id, EventKind::Dns, format!("ответ из кэша: {}", vals.join(", ")));
                let mut msg = dns_msg(m.id, q);
                msg.answers = Some(hit);
                msg.ra = Some(true);
                self.reply(d, pkt, at, reply_msg(msg));
                return true;
            }
            let own = auth_answer(cfg, &q);
            if !own.answers.is_empty() {
                let vals: Vec<&str> = own.answers.iter().map(|a| a.value.as_str()).collect();
                self.log(at, &d.id, EventKind::Dns, format!("отвечаю из своей зоны: {}", vals.join(", ")));
                let mut msg = dns_msg(m.id, q);
                msg.answers = Some(own.answers);
                msg.ra = Some(true);
                self.reply(d, pkt, at, reply_msg(msg));
                return true;
            }
            let st = DnsPending {
                client: DnsClient { id: m.id, dport: pkt.sport, src_ip: pkt.dst, dst_ip: pkt.src.unwrap_or(0) },
                q: q.clone(),
                cur: DnsQuestion { name, typ: q.typ.clone() },
                chain: vec![],
                hops: 0,
            };
            match cfg.roots.first() {
                None => self.dns_finish(d, st, Rcode::ServFail, at, Some("корневые серверы не заданы")),
                Some(root) => self.dns_send(d, st, root, at),
            }
            return true;
        }
        let a = auth_answer(cfg, &q);
        let text = if let Some(r) = &a.referral {
            format!("не знаю, но зона {} у {} — отправляю реферал", r.zone, r.ns)
        } else if !a.answers.is_empty() {
            let v: Vec<String> = a.answers.iter().map(|x| format!("{} {}", x.typ, x.value)).collect();
            format!("отвечаю: {}", v.join(", "))
        } else {
            format!("ответ: {}", a.rcode.as_str())
        };
        self.log(at, &d.id, EventKind::Dns, text);
        let mut msg = dns_msg(m.id, q);
        msg.rcode = Some(a.rcode);
        msg.answers = Some(a.answers);
        msg.referral = a.referral;
        self.reply(d, pkt, at, reply_msg(msg));
        true
    }

    fn dns_send(&mut self, d: &'a Device, mut st: DnsPending, server: &str, at: f64) {
        st.hops += 1;
        if st.hops > 12 {
            return self.dns_finish(d, st, Rcode::ServFail, at, Some("слишком много шагов"));
        }
        self.dns_seq += 1;
        let id = self.dns_seq;
        let key = format!("{}:{}", d.id, id);
        let ip = parse_ip(server).unwrap_or(0);
        self.log(at, &d.id, EventKind::Dns, format!("спрашиваю {server}: «{} {}»", st.cur.name, st.cur.typ));
        let cur = st.cur.clone();
        self.dns_pend.insert(key.clone(), st);
        let mut p = Packet::new(Proto::Udp, ip);
        p.sport = Some(33000 + (id % 1000));
        p.dport = Some(53);
        p.dns = Some(DnsMessage { id, q: cur, response: false, rd: Some(false), ra: None, rcode: None, answers: None, referral: None });
        self.ip_out(d, p, at + 5.0);
        if let Some(st) = self.dns_pend.remove(&key) {
            // ответа не будет: резолвер ждёт таймаут и отвечает SERVFAIL
            self.log(at + 1_000_000.0, &d.id, EventKind::Dns, format!("{server} не отвечает — SERVFAIL клиенту"));
            self.dns_finish(d, st, Rcode::ServFail, at + 1_000_000.0, None);
        }
    }

    fn resolver_step(&mut self, d: &'a Device, mut st: DnsPending, m: &DnsMessage, at: f64) {
        let answers = m.answers.clone().unwrap_or_default();
        if !answers.is_empty() {
            st.chain.extend(answers.iter().cloned());
            let want = st.cur.typ.clone();
            let final_ = answers.iter().any(|a| a.typ == want);
            if final_ || st.cur.typ == "CNAME" {
                return self.dns_finish(d, st, Rcode::NoError, at, None);
            }
            if let Some(cname) = answers.iter().find(|a| a.typ == "CNAME") {
                self.log(at, &d.id, EventKind::Dns, format!("{} — псевдоним для {}, ищу дальше", cname.name, cname.value));
                st.cur = DnsQuestion { name: fqdn(&cname.value), typ: want };
                let root = d.dns.as_ref().and_then(|x| x.roots.first().cloned()).unwrap_or_default();
                return self.dns_send(d, st, &root, at);
            }
            return self.dns_finish(d, st, Rcode::NoError, at, None);
        }
        if let Some(r) = &m.referral {
            self.log(at, &d.id, EventKind::Dns, format!("реферал: зона {} → {}", r.zone, r.ns));
            return self.dns_send(d, st, &r.ns, at);
        }
        self.dns_finish(d, st, m.rcode.unwrap_or(Rcode::ServFail), at, None);
    }

    fn dns_finish(&mut self, d: &'a Device, st: DnsPending, rcode: Rcode, at: f64, why: Option<&str>) {
        if let Some(w) = why {
            self.log(at, &d.id, EventKind::Dns, w);
        }
        let answers = st.chain.clone();
        if rcode == Rcode::NoError && !answers.is_empty() {
            let key = format!("{}|{}", fqdn(&st.q.name), st.q.typ);
            self.rt.dns_cache.entry(d.id.clone()).or_default().insert(key, answers.clone());
        }
        let mut p = Packet::new(Proto::Udp, st.client.dst_ip);
        p.src = Some(st.client.src_ip);
        p.sport = Some(53);
        p.dport = st.client.dport;
        p.dns = Some(DnsMessage {
            id: st.client.id,
            q: st.q.clone(),
            response: true,
            rd: None,
            ra: Some(true),
            rcode: Some(rcode),
            answers: Some(answers),
            referral: None,
        });
        self.ip_out(d, p, at + 5.0);
    }
}

/// Результат локального разрешения имени на клиенте.
#[derive(Clone, Debug, PartialEq)]
pub enum LocalLookup {
    /// Адрес известен без запроса (литерал или hosts); `from` — «hosts».
    Ip(Option<u32>, Option<&'static str>),
    /// Разрешить нельзя (нет резолвера).
    Error(String),
    /// Нужно спросить DNS-сервер по этому адресу.
    Ask(Option<u32>),
}

/// Разрешение на клиенте: литерал адреса → hosts → вопрос серверу из resolv.conf.
pub fn local_lookup(d: &Device, name: &str) -> LocalLookup {
    let n = fqdn(name);
    if let Some(ip) = parse_ip(&n) {
        return LocalLookup::Ip(Some(ip), None);
    }
    if let Some(h) = d.hosts.get(&n).filter(|h| !h.is_empty()) {
        return LocalLookup::Ip(parse_ip(h), Some("hosts"));
    }
    match d.resolver.as_deref() {
        Some(r) if !r.is_empty() => LocalLookup::Ask(parse_ip(r)),
        _ => LocalLookup::Error("в /etc/resolv.conf нет DNS-сервера".into()),
    }
}

/// Первый адрес A из ответа.
pub fn answer_ip(dns: Option<&DnsMessage>) -> Option<u32> {
    let a = dns?.answers.as_ref()?.iter().find(|x| x.typ == "A")?;
    parse_ip(&a.value)
}

/// Ответ в виде вывода `dig`.
pub fn fmt_dns(dns: &DnsMessage) -> String {
    let mut lines = vec![format!(";; status: {}", dns.rcode.map(|r| r.as_str()).unwrap_or("undefined"))];
    for a in dns.answers.iter().flatten() {
        lines.push(format!(
            "{}.\t{}\tIN\t{}\t{}",
            a.name,
            a.ttl.map(|t| t.to_string()).unwrap_or_else(|| "undefined".into()),
            a.typ,
            a.value
        ));
    }
    lines.join("\n")
}
