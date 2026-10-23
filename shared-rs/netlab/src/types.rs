//! Доменные типы лаборатории: состояние сети (устройства, интерфейсы, кабели, службы), кадры и пакеты,
//! события симуляции, служебные кэши.
//!
//! Состояние сети — обычные данные с `serde`: его можно сохранить строкой, отправить на сервер и повторить
//! проверку на чистой копии. Каноническая запись — snake_case, устройства — массивом; читается и прежняя запись
//! клиента на TypeScript (camelCase, устройства — объектом по id): за это отвечают `alias`.

use crate::util::OrdMap;
use serde::de::{SeqAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::fmt;

/* ---- перечисления ---- */

/// Вид устройства.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum DeviceKind {
    Host,
    Server,
    Router,
    Switch,
    Hub,
    /// Маршрутизатор провайдера: не маршрутизирует частные адреса.
    Internet,
}

/// Транспортный протокол пакета или службы.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Proto {
    Tcp,
    Udp,
    Icmp,
}

impl Proto {
    pub fn as_str(self) -> &'static str {
        match self {
            Proto::Tcp => "tcp",
            Proto::Udp => "udp",
            Proto::Icmp => "icmp",
        }
    }
}

/// Флаги TCP-сегмента (в той степени, в какой их различает симулятор).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum TcpFlags {
    #[serde(rename = "SYN")]
    Syn,
    #[serde(rename = "SYN-ACK")]
    SynAck,
    #[serde(rename = "ACK")]
    Ack,
    #[serde(rename = "PSH-ACK")]
    PshAck,
    #[serde(rename = "FIN-ACK")]
    FinAck,
    #[serde(rename = "RST")]
    Rst,
}

impl TcpFlags {
    pub fn as_str(self) -> &'static str {
        match self {
            TcpFlags::Syn => "SYN",
            TcpFlags::SynAck => "SYN-ACK",
            TcpFlags::Ack => "ACK",
            TcpFlags::PshAck => "PSH-ACK",
            TcpFlags::FinAck => "FIN-ACK",
            TcpFlags::Rst => "RST",
        }
    }
    /// Есть ли в сегменте подтверждение (подстрока «ACK»).
    pub fn has_ack(self) -> bool {
        matches!(self, TcpFlags::SynAck | TcpFlags::Ack | TcpFlags::PshAck | TcpFlags::FinAck)
    }
}

/// Вид ICMP-сообщения.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum IcmpType {
    #[serde(rename = "echo-req")]
    EchoReq,
    #[serde(rename = "echo-rep")]
    EchoRep,
    #[serde(rename = "ttl")]
    Ttl,
    #[serde(rename = "unreach")]
    Unreach,
}

/// Уточнение «недоступно»: порт закрыт или нужна фрагментация.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum IcmpCode {
    Port,
    Frag,
}

/// Действие правила файрвола.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum FwAction {
    #[serde(rename = "ACCEPT")]
    Accept,
    #[serde(rename = "DROP")]
    Drop,
    #[serde(rename = "REJECT")]
    Reject,
}

impl FwAction {
    pub fn as_str(self) -> &'static str {
        match self {
            FwAction::Accept => "ACCEPT",
            FwAction::Drop => "DROP",
            FwAction::Reject => "REJECT",
        }
    }
    pub fn parse(s: &str) -> Option<FwAction> {
        match s {
            "ACCEPT" => Some(FwAction::Accept),
            "DROP" => Some(FwAction::Drop),
            "REJECT" => Some(FwAction::Reject),
            _ => None,
        }
    }
}

/// Цепочка таблицы nat.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum NatChain {
    #[serde(rename = "PREROUTING")]
    Prerouting,
    #[serde(rename = "POSTROUTING")]
    Postrouting,
}

impl NatChain {
    pub fn as_str(self) -> &'static str {
        match self {
            NatChain::Prerouting => "PREROUTING",
            NatChain::Postrouting => "POSTROUTING",
        }
    }
}

/// Цель правила nat.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum NatAction {
    #[serde(rename = "DNAT")]
    Dnat,
    #[serde(rename = "MASQUERADE")]
    Masquerade,
}

impl NatAction {
    pub fn as_str(self) -> &'static str {
        match self {
            NatAction::Dnat => "DNAT",
            NatAction::Masquerade => "MASQUERADE",
        }
    }
}

/// Состояние соединения в правиле файрвола.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ConnState {
    Established,
    New,
}

/// Алгоритм балансировщика.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LbAlgo {
    /// По кругу.
    Rr,
    /// Хеш по адресу клиента.
    Hash,
}

/// Версия HTTP, которую предлагает сервер.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum HttpProto {
    H1,
    H2,
    H3,
}

impl HttpProto {
    pub fn name(self) -> &'static str {
        match self {
            HttpProto::H1 => "HTTP/1.1",
            HttpProto::H2 => "HTTP/2",
            HttpProto::H3 => "HTTP/3",
        }
    }
    pub fn id(self) -> &'static str {
        match self {
            HttpProto::H1 => "h1",
            HttpProto::H2 => "h2",
            HttpProto::H3 => "h3",
        }
    }
}

/// Алгоритм управления перегрузкой TCP.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Cc {
    Reno,
    Cubic,
    Bbr,
}

impl Cc {
    pub fn as_str(self) -> &'static str {
        match self {
            Cc::Reno => "reno",
            Cc::Cubic => "cubic",
            Cc::Bbr => "bbr",
        }
    }
}

/// Вид атаки у устройства-нарушителя.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum AttackKind {
    Arpspoof,
    Synflood,
    Scan,
}

/// Код ответа DNS.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum Rcode {
    #[serde(rename = "NOERROR")]
    NoError,
    #[serde(rename = "NXDOMAIN")]
    NxDomain,
    #[serde(rename = "REFUSED")]
    Refused,
    #[serde(rename = "SERVFAIL")]
    ServFail,
}

impl Rcode {
    pub fn as_str(self) -> &'static str {
        match self {
            Rcode::NoError => "NOERROR",
            Rcode::NxDomain => "NXDOMAIN",
            Rcode::Refused => "REFUSED",
            Rcode::ServFail => "SERVFAIL",
        }
    }
}

/// Вид события журнала.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum EventKind {
    Icmp,
    Tcp,
    Udp,
    Arp,
    Learn,
    Drop,
    Loop,
    Conflict,
    Nat,
    Fw,
    Tun,
    Dns,
    Http,
    Tls,
    Info,
}

/// Вид кадра на кабеле.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum FrameKind {
    Arp,
    Tcp,
    Udp,
    Icmp,
}

/// Итог пробы.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ProbeStatus {
    Reply,
    Connected,
    Refused,
    Timeout,
    Ttl,
    Unreach,
    Toolong,
    /// Цель не удалось разрешить в адрес (имя без записи, нет резолвера).
    Noaddr,
}

impl ProbeStatus {
    pub fn as_str(self) -> &'static str {
        match self {
            ProbeStatus::Reply => "reply",
            ProbeStatus::Connected => "connected",
            ProbeStatus::Refused => "refused",
            ProbeStatus::Timeout => "timeout",
            ProbeStatus::Ttl => "ttl",
            ProbeStatus::Unreach => "unreach",
            ProbeStatus::Toolong => "toolong",
            ProbeStatus::Noaddr => "noaddr",
        }
    }
}

/* ---- состояние сети ---- */

fn yes() -> bool {
    true
}
fn is_false(b: &bool) -> bool {
    !*b
}
fn prefix24() -> u8 {
    24
}

/// Число в JSON: целые значения без «.0» (координаты, длины кабелей).
fn ser_num<S: Serializer>(v: &f64, s: S) -> Result<S::Ok, S::Error> {
    if v.fract() == 0.0 && v.abs() < 1e15 {
        s.serialize_i64(*v as i64)
    } else {
        s.serialize_f64(*v)
    }
}

/// Туннель (VPN) на интерфейсе: внешний адрес пира, UDP-порт и общий секрет.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Tun {
    pub peer: String,
    pub port: i64,
    pub key: String,
}

/// Сетевой интерфейс устройства (у коммутатора — порт).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Iface {
    pub name: String,
    pub mac: String,
    #[serde(default)]
    pub ip: Option<String>,
    #[serde(default = "prefix24")]
    pub prefix: u8,
    #[serde(default = "yes")]
    pub up: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mtu: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub vlan: Option<u32>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub trunk: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tun: Option<Tun>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub txqueuelen: Option<u32>,
}

impl Iface {
    /// Интерфейс без адреса: `up`, префикс 24.
    pub fn new(name: &str, mac: &str) -> Iface {
        Iface {
            name: name.into(),
            mac: mac.into(),
            ip: None,
            prefix: 24,
            up: true,
            mtu: None,
            vlan: None,
            trunk: false,
            tun: None,
            txqueuelen: None,
        }
    }
    /// Интерфейс с адресом.
    pub fn with_ip(mut self, ip: &str, prefix: u8) -> Iface {
        self.ip = Some(ip.into());
        self.prefix = prefix;
        self
    }
}

/// Маршрут: `dst` — «10.0.0.0/24», `via` — шлюз или `None` (напрямую), `dev` — интерфейс.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Route {
    pub dst: String,
    #[serde(default)]
    pub via: Option<String>,
    #[serde(default)]
    pub dev: Option<String>,
}

/// Правило таблицы nat.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct NatRule {
    pub chain: NatChain,
    pub action: NatAction,
    #[serde(rename = "in", default, skip_serializing_if = "Option::is_none")]
    pub iif: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub out: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub src: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dst: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proto: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sport: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dport: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub to: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub state: Option<ConnState>,
}

/// Правило фильтра FORWARD.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct FwRule {
    pub action: FwAction,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub src: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dst: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proto: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sport: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dport: Option<i64>,
    #[serde(rename = "in", default, skip_serializing_if = "Option::is_none")]
    pub iif: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub out: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub state: Option<ConnState>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub to: Option<String>,
}

/// Цепочка FORWARD: политика по умолчанию и правила.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Firewall {
    pub policy: FwAction,
    #[serde(default)]
    pub rules: Vec<FwRule>,
}

impl Default for Firewall {
    fn default() -> Self {
        Firewall { policy: FwAction::Accept, rules: Vec::new() }
    }
}

/// Слушающий порт.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Service {
    pub proto: Proto,
    pub port: i64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub bind: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
}

/* ---- прикладные службы ---- */

/// Запись DNS.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsRecord {
    pub name: String,
    #[serde(rename = "type")]
    pub typ: String,
    pub value: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ttl: Option<u32>,
}

/// Делегирование зоны: сервер имён по адресу `ns`.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsDelegation {
    pub zone: String,
    pub ns: String,
}

/// Настройки DNS-сервера устройства.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct DnsConfig {
    #[serde(default)]
    pub records: Vec<DnsRecord>,
    #[serde(default)]
    pub delegations: Vec<DnsDelegation>,
    #[serde(default)]
    pub zones: Vec<String>,
    #[serde(default)]
    pub recursive: bool,
    #[serde(default)]
    pub roots: Vec<String>,
}

/// Маршрут веб-сервера.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct HttpRoute {
    pub path: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub status: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub body: Option<String>,
    #[serde(rename = "type", default, skip_serializing_if = "Option::is_none")]
    pub typ: Option<String>,
    #[serde(default, skip_serializing_if = "OrdMap::is_empty")]
    pub headers: OrdMap<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub location: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub etag: Option<String>,
}

/// Страница для измерения загрузки: число ресурсов и размер каждого (КБ).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PageSpec {
    pub count: f64,
    pub kb: f64,
}

/// Настройки веб-сервера.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct HttpConfig {
    #[serde(default)]
    pub routes: Vec<HttpRoute>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub protocol: Option<HttpProto>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub page: Option<PageSpec>,
}

/// Правило обратного прокси.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct RProxyRule {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub host: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub path: Option<String>,
    pub backend: String,
    #[serde(default, skip_serializing_if = "is_false")]
    pub cache: bool,
}

#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct RProxyConfig {
    #[serde(default)]
    pub rules: Vec<RProxyRule>,
}

/// Прямой HTTP-прокси.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct ProxyConfig {
    #[serde(default)]
    pub deny: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub port: Option<i64>,
}

/// Сертификат сервера.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct TlsCert {
    pub cn: String,
    #[serde(default)]
    pub san: Vec<String>,
    pub issuer: String,
    #[serde(rename = "not_after", alias = "notAfter")]
    pub not_after: String,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct TlsConfig {
    pub cert: TlsCert,
    #[serde(default)]
    pub chain: Vec<String>,
    #[serde(default)]
    pub versions: Vec<String>,
}

/// Центр сертификации: издатель (`None` — корневой).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Ca {
    #[serde(default)]
    pub issuer: Option<String>,
}

/// Инфраструктура открытых ключей сети.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct Pki {
    #[serde(default)]
    pub cas: OrdMap<Ca>,
}

#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct SshUser {
    #[serde(default)]
    pub keys: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub password: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct SshConfig {
    #[serde(rename = "host_key", alias = "hostKey")]
    pub host_key: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rot: Option<u32>,
    #[serde(rename = "password_auth", alias = "passwordAuth", default = "yes")]
    pub password_auth: bool,
    #[serde(default)]
    pub users: OrdMap<SshUser>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct LbBackend {
    pub ip: String,
    pub port: i64,
}

/// Балансировщик L4: виртуальный адрес и пул серверов.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct LbConfig {
    pub vip: String,
    pub port: i64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub algo: Option<LbAlgo>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub health: bool,
    #[serde(default)]
    pub backends: Vec<LbBackend>,
}

/// Поведение нарушителя (атака на фоне).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct AttackConfig {
    #[serde(rename = "type")]
    pub typ: AttackKind,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub victim: Option<String>,
    #[serde(rename = "gateway_ip", alias = "gatewayIp", default, skip_serializing_if = "Option::is_none")]
    pub gateway_ip: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub target: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub port: Option<i64>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub ports: Vec<i64>,
}

/// Устройство: расширения (`dns`, `http`, `tls`, …) есть только у тех, кто запускает соответствующую службу.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Device {
    pub id: String,
    pub kind: DeviceKind,
    pub name: String,
    #[serde(default, serialize_with = "ser_num")]
    pub x: f64,
    #[serde(default, serialize_with = "ser_num")]
    pub y: f64,
    #[serde(default)]
    pub ifaces: Vec<Iface>,
    #[serde(default)]
    pub routes: Vec<Route>,
    #[serde(default)]
    pub forward: bool,
    #[serde(default)]
    pub nat: Vec<NatRule>,
    #[serde(default)]
    pub fw: Firewall,
    #[serde(default)]
    pub services: Vec<Service>,
    #[serde(default)]
    pub locked: bool,
    #[serde(rename = "drop_private", alias = "dropPrivate", default)]
    pub drop_private: bool,
    #[serde(rename = "icmp_block", alias = "icmpBlock", default, skip_serializing_if = "is_false")]
    pub icmp_block: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub syncookies: bool,
    #[serde(rename = "arp_static", alias = "arpStatic", default, skip_serializing_if = "OrdMap::is_empty")]
    pub arp_static: OrdMap<String>,
    #[serde(default, skip_serializing_if = "OrdMap::is_empty")]
    pub hosts: OrdMap<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub resolver: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub trust: Option<Vec<String>>,
    #[serde(rename = "tls_min", alias = "tlsMin", default, skip_serializing_if = "Option::is_none")]
    pub tls_min: Option<String>,
    #[serde(rename = "ssh_key", alias = "sshKey", default, skip_serializing_if = "Option::is_none")]
    pub ssh_key: Option<String>,
    #[serde(rename = "known_hosts", alias = "knownHosts", default, skip_serializing_if = "OrdMap::is_empty")]
    pub known_hosts: OrdMap<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rwnd: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cc: Option<Cc>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dns: Option<DnsConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub http: Option<HttpConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rproxy: Option<RProxyConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proxy: Option<ProxyConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tls: Option<TlsConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ssh: Option<SshConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub lb: Option<LbConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub attack: Option<AttackConfig>,
}

impl Device {
    /// Новое устройство без интерфейсов; пересылка включена у маршрутизаторов, частные адреса режет «интернет».
    pub fn new(id: &str, kind: DeviceKind, name: &str, x: f64, y: f64) -> Device {
        Device {
            id: id.into(),
            kind,
            name: name.into(),
            x,
            y,
            ifaces: Vec::new(),
            routes: Vec::new(),
            forward: matches!(kind, DeviceKind::Router | DeviceKind::Internet),
            nat: Vec::new(),
            fw: Firewall::default(),
            services: Vec::new(),
            locked: false,
            drop_private: kind == DeviceKind::Internet,
            icmp_block: false,
            syncookies: false,
            arp_static: OrdMap::new(),
            hosts: OrdMap::new(),
            resolver: None,
            trust: None,
            tls_min: None,
            ssh_key: None,
            known_hosts: OrdMap::new(),
            rwnd: None,
            cc: None,
            dns: None,
            http: None,
            rproxy: None,
            proxy: None,
            tls: None,
            ssh: None,
            lb: None,
            attack: None,
        }
    }

    pub fn iface(&self, name: &str) -> Option<&Iface> {
        self.ifaces.iter().find(|i| i.name == name)
    }

    pub fn iface_mut(&mut self, name: &str) -> Option<&mut Iface> {
        self.ifaces.iter_mut().find(|i| i.name == name)
    }
}

/// Кабель между «устройство:порт» и «устройство:порт».
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Link {
    pub a: String,
    pub b: String,
    #[serde(default = "default_km", serialize_with = "ser_num")]
    pub km: f64,
    #[serde(default = "default_mbps", serialize_with = "ser_num")]
    pub mbps: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mtu: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub loss: Option<f64>,
}

fn default_km() -> f64 {
    0.01
}
fn default_mbps() -> f64 {
    1000.0
}

impl Link {
    /// Кабель по умолчанию: 10 м, 1 Гбит/с.
    pub fn new(a: &str, b: &str) -> Link {
        Link { a: a.into(), b: b.into(), km: 0.01, mbps: 1000.0, mtu: None, loss: None }
    }
}

/// Устройства сети в порядке добавления. В JSON — массив; читается и объект «id → устройство».
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Devices {
    list: Vec<Device>,
}

impl Devices {
    pub fn new() -> Devices {
        Devices::default()
    }
    pub fn get(&self, id: &str) -> Option<&Device> {
        self.list.iter().find(|d| d.id == id)
    }
    pub fn get_mut(&mut self, id: &str) -> Option<&mut Device> {
        self.list.iter_mut().find(|d| d.id == id)
    }
    pub fn iter(&self) -> impl Iterator<Item = &Device> {
        self.list.iter()
    }
    pub fn iter_mut(&mut self) -> impl Iterator<Item = &mut Device> {
        self.list.iter_mut()
    }
    pub fn len(&self) -> usize {
        self.list.len()
    }
    pub fn is_empty(&self) -> bool {
        self.list.is_empty()
    }
    /// Добавить устройство (с тем же id — заменить).
    pub fn insert(&mut self, d: Device) {
        match self.list.iter().position(|x| x.id == d.id) {
            Some(i) => self.list[i] = d,
            None => self.list.push(d),
        }
    }
}

impl Serialize for Devices {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        self.list.serialize(s)
    }
}

impl<'de> Deserialize<'de> for Devices {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct Vis;
        impl<'de> Visitor<'de> for Vis {
            type Value = Devices;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                f.write_str("массив устройств или объект «id → устройство»")
            }
            fn visit_seq<A: SeqAccess<'de>>(self, mut a: A) -> Result<Devices, A::Error> {
                let mut out = Devices::new();
                while let Some(x) = a.next_element::<Device>()? {
                    out.insert(x);
                }
                Ok(out)
            }
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut a: A) -> Result<Devices, A::Error> {
                let mut out = Devices::new();
                while let Some((_, x)) = a.next_entry::<String, Device>()? {
                    out.insert(x);
                }
                Ok(out)
            }
        }
        d.deserialize_any(Vis)
    }
}

/* ---- кадры и пакеты ---- */

/// Кортеж соединения (для conntrack и ICMP-ошибок). Для ICMP «порты» — идентификатор запроса.
#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Tuple {
    pub proto: Proto,
    pub src: Option<u32>,
    pub dst: u32,
    pub sport: Option<i64>,
    pub dport: Option<i64>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct IcmpInfo {
    #[serde(rename = "type")]
    pub typ: IcmpType,
    pub id: i64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub orig: Option<Tuple>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub code: Option<IcmpCode>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mtu: Option<u32>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsQuestion {
    pub name: String,
    #[serde(rename = "type")]
    pub typ: String,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Referral {
    pub zone: String,
    pub ns: String,
}

/// DNS-сообщение внутри UDP-датаграммы.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsMessage {
    pub id: i64,
    pub q: DnsQuestion,
    pub response: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rd: Option<bool>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ra: Option<bool>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rcode: Option<Rcode>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub answers: Option<Vec<DnsRecord>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub referral: Option<Referral>,
}

/// Туннельная упаковка: внутренний пакет, общий ключ и имя интерфейса.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Wrapped {
    pub inner: Packet,
    pub key: String,
    pub name: String,
}

/// IP-пакет. Адреса — числа, `src == None` — «ещё не выбран исходящий интерфейс».
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Packet {
    pub src: Option<u32>,
    pub dst: u32,
    pub ttl: i64,
    pub proto: Proto,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub sport: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dport: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub size: Option<i64>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub no_tun: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tunnel: Option<Box<Wrapped>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub icmp: Option<IcmpInfo>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub df: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub flags: Option<TcpFlags>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub seq: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ack: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub len: Option<i64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub dns: Option<DnsMessage>,
    #[serde(default, skip_serializing_if = "is_false")]
    pub fwd: bool,
}

impl Packet {
    /// Пакет без заполненных полей: отправитель не выбран, TTL 64.
    pub fn new(proto: Proto, dst: u32) -> Packet {
        Packet {
            src: None,
            dst,
            ttl: 64,
            proto,
            sport: None,
            dport: None,
            size: None,
            no_tun: false,
            tunnel: None,
            icmp: None,
            df: false,
            flags: None,
            seq: None,
            ack: None,
            len: None,
            dns: None,
            fwd: false,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ArpOp {
    Req,
    Rep,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ArpInfo {
    pub op: ArpOp,
    pub sip: u32,
    pub smac: String,
    pub tip: u32,
    pub tmac: Option<String>,
}

/// Содержимое кадра: ARP или IP-пакет.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Payload {
    Arp(ArpInfo),
    Ip(Packet),
}

/// Кадр Ethernet на кабеле.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Frame {
    pub size: u32,
    pub src: String,
    pub dst: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub vlan: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub uid: Option<u64>,
    pub body: Payload,
}

/// Событие журнала симуляции: время в микросекундах, устройство, вид и текст.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct NetEvent {
    pub t: f64,
    pub dev: String,
    pub kind: EventKind,
    pub text: String,
}

/// Переход кадра по кабелю (для анимации и перехвата).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Hop {
    pub from: String,
    pub from_port: String,
    pub to: String,
    pub to_port: String,
    pub t0: f64,
    pub t1: f64,
    pub kind: FrameKind,
    pub label: String,
    pub frame: Frame,
}

/// Пакет, доставленный устройству (локально).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Delivered {
    pub dev: String,
    pub src: Option<u32>,
    pub dst: Option<u32>,
    pub proto: Proto,
    pub dport: Option<i64>,
    pub sport: Option<i64>,
}

/// Итог пробы (ping, TCP, UDP, DNS).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ProbeRun {
    pub status: ProbeStatus,
    pub from: Option<u32>,
    pub code: Option<IcmpCode>,
    pub mtu: Option<u32>,
    pub dns: Option<DnsMessage>,
    pub rtt_us: Option<f64>,
    pub events: Vec<NetEvent>,
    pub hops: Vec<Hop>,
    pub delivered: Vec<Delivered>,
}

impl ProbeRun {
    /// Пустая проба (нет связи, имя не разрешилось).
    pub fn empty(status: ProbeStatus) -> ProbeRun {
        ProbeRun { status, from: None, code: None, mtu: None, dns: None, rtt_us: None, events: vec![], hops: vec![], delivered: vec![] }
    }
}

/* ---- служебные кэши ---- */

/// Запись ARP-кэша: MAC, время и номер симуляции, которая её выучила (−1 — подмена).
#[derive(Clone, Debug, PartialEq)]
pub struct ArpEntry {
    pub mac: String,
    pub at: f64,
    pub sim: i64,
}

/// Запись conntrack.
#[derive(Clone, Debug, PartialEq)]
pub struct ConnEntry {
    pub orig: Tuple,
    pub tr: Tuple,
    pub replied: bool,
}

/// Строка перехвата пакетов.
#[derive(Clone, Debug, PartialEq)]
pub struct CapRow {
    pub t: f64,
    /// `true` — кадр вошёл («In»), `false` — вышел («Out»).
    pub inbound: bool,
    pub frame: Frame,
}

/// Ответ HTTP.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct HttpResponse {
    pub status: u32,
    pub reason: String,
    pub headers: OrdMap<String>,
    pub body: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rtt_us: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ip: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub via: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub url: Option<String>,
}

/// Адрес партнёра по туннелю, выученный из последнего пакета.
#[derive(Clone, Debug, PartialEq)]
pub struct TunPeer {
    pub ip: Option<u32>,
    pub port: Option<i64>,
}

/// Служебные кэши симулятора: ARP, таблицы MAC, conntrack, кэш DNS, перехват пакетов. В JSON не сохраняются.
#[derive(Clone, Debug, Default)]
pub struct Runtime {
    pub arp: HashMap<String, BTreeMap<u32, ArpEntry>>,
    pub mac: HashMap<String, OrdMap<String>>,
    pub ct: HashMap<String, Vec<ConnEntry>>,
    pub dns_cache: HashMap<String, HashMap<String, Vec<DnsRecord>>>,
    pub tun_peer: HashMap<String, TunPeer>,
    pub lb: HashMap<String, usize>,
    pub synflood: HashSet<String>,
    pub cap: HashMap<String, Vec<CapRow>>,
    pub clock: f64,
    pub rpcache: HashMap<String, HashMap<String, HttpResponse>>,
    pub sim_seq: i64,
}

/// Состояние сети: устройства и кабели (+ PKI, если в сети есть TLS). Кэши симулятора — в `rt`.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct NetState {
    #[serde(default)]
    pub devices: Devices,
    #[serde(default)]
    pub links: Vec<Link>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub pki: Option<Pki>,
    #[serde(skip)]
    pub rt: Runtime,
    #[serde(skip)]
    pub busy: bool,
}

/// Текст-ссылка на порт «устройство:порт».
pub fn port_ref(dev: &str, port: &str) -> String {
    format!("{dev}:{port}")
}
