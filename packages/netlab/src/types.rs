//! Domain types of the lab: network state (devices, interfaces, cables, services), frames and packets,
//! simulation events, runtime caches.
//!
//! The network state is plain `serde` data: it can be saved as a string, sent to the server and the check
//! replayed on a clean copy. The canonical form is snake_case with devices as an array; the former TypeScript
//! client form (camelCase, devices as an object keyed by id) is read too: that is what the `alias`es are for.

use crate::util::OrdMap;
use serde::de::{SeqAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::fmt;

/* ---- enums ---- */

/// Device kind.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum DeviceKind {
    Host,
    Server,
    Router,
    Switch,
    Hub,
    /// Provider router: does not route private addresses.
    Internet,
}

/// Transport protocol of a packet or service.
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

/// TCP segment flags (to the extent the simulator distinguishes them).
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
    /// Whether the segment carries an acknowledgement (substring "ACK").
    pub fn has_ack(self) -> bool {
        matches!(self, TcpFlags::SynAck | TcpFlags::Ack | TcpFlags::PshAck | TcpFlags::FinAck)
    }
}

/// ICMP message kind.
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

/// Refinement of "unreachable": port closed or fragmentation needed.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum IcmpCode {
    Port,
    Frag,
}

/// Firewall rule action.
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

/// Chain of the nat table.
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

/// Target of a nat rule.
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

/// Connection state in a firewall rule.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ConnState {
    Established,
    New,
}

/// Load balancer algorithm.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LbAlgo {
    /// Round robin.
    Rr,
    /// Hash by client address.
    Hash,
}

/// HTTP version offered by the server.
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

/// TCP congestion control algorithm.
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

/// Attack kind of the attacker device.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum AttackKind {
    Arpspoof,
    Synflood,
    Scan,
}

/// DNS response code.
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

/// Log event kind.
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

/// Kind of a frame on a cable.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum FrameKind {
    Arp,
    Tcp,
    Udp,
    Icmp,
}

/// Probe outcome.
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
    /// The target could not be resolved to an address (name without a record, no resolver).
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

/* ---- network state ---- */

fn yes() -> bool {
    true
}
fn is_false(b: &bool) -> bool {
    !*b
}
fn prefix24() -> u8 {
    24
}

/// Number in JSON: integer values without ".0" (coordinates, cable lengths).
fn ser_num<S: Serializer>(v: &f64, s: S) -> Result<S::Ok, S::Error> {
    if v.fract() == 0.0 && v.abs() < 1e15 {
        s.serialize_i64(*v as i64)
    } else {
        s.serialize_f64(*v)
    }
}

/// Tunnel (VPN) on an interface: peer's external address, UDP port and shared secret.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Tun {
    pub peer: String,
    pub port: i64,
    pub key: String,
}

/// Network interface of a device (a port on a switch).
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
    /// Interface without an address: `up`, prefix 24.
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
    /// Interface with an address.
    pub fn with_ip(mut self, ip: &str, prefix: u8) -> Iface {
        self.ip = Some(ip.into());
        self.prefix = prefix;
        self
    }
}

/// Route: `dst` is "10.0.0.0/24", `via` is the gateway or `None` (directly), `dev` is the interface.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Route {
    pub dst: String,
    #[serde(default)]
    pub via: Option<String>,
    #[serde(default)]
    pub dev: Option<String>,
}

/// Rule of the nat table.
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

/// FORWARD filter rule.
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

/// FORWARD chain: default policy and rules.
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

/// Listening port.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Service {
    pub proto: Proto,
    pub port: i64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub bind: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
}

/* ---- application services ---- */

/// DNS record.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsRecord {
    pub name: String,
    #[serde(rename = "type")]
    pub typ: String,
    pub value: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub ttl: Option<u32>,
}

/// Zone delegation: name server at address `ns`.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DnsDelegation {
    pub zone: String,
    pub ns: String,
}

/// DNS server settings of a device.
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

/// Web server route.
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

/// Page for load measurement: number of resources and size of each (KB).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct PageSpec {
    pub count: f64,
    pub kb: f64,
}

/// Web server settings.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct HttpConfig {
    #[serde(default)]
    pub routes: Vec<HttpRoute>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub protocol: Option<HttpProto>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub page: Option<PageSpec>,
}

/// Reverse proxy rule.
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

/// Forward HTTP proxy.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct ProxyConfig {
    #[serde(default)]
    pub deny: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub port: Option<i64>,
}

/// Server certificate.
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

/// Certificate authority: issuer (`None` for a root).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Ca {
    #[serde(default)]
    pub issuer: Option<String>,
}

/// Public key infrastructure of the network.
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

/// L4 load balancer: virtual address and server pool.
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

/// Attacker behaviour (background attack).
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

/// Device: extensions (`dns`, `http`, `tls`, ...) exist only on those that run the corresponding service.
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
    /// New device without interfaces; forwarding is on for routers, private addresses are dropped by "internet".
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

/// Cable between "device:port" and "device:port".
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
    /// Default cable: 10 m, 1 Gbit/s.
    pub fn new(a: &str, b: &str) -> Link {
        Link { a: a.into(), b: b.into(), km: 0.01, mbps: 1000.0, mtu: None, loss: None }
    }
}

/// Network devices in insertion order. In JSON an array; an "id -> device" object is read too.
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
    /// Add a device (replace one with the same id).
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
                f.write_str(i18n::tr("an array of devices or an object \"id → device\""))
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

/* ---- frames and packets ---- */

/// Connection tuple (for conntrack and ICMP errors). For ICMP the "ports" are the request identifier.
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

/// DNS message inside a UDP datagram.
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

/// Tunnel encapsulation: inner packet, shared key and interface name.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Wrapped {
    pub inner: Packet,
    pub key: String,
    pub name: String,
}

/// IP packet. Addresses are numbers, `src == None` means "outgoing interface not chosen yet".
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
    /// Packet with unfilled fields: no sender chosen, TTL 64.
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

/// Frame payload: ARP or IP packet.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Payload {
    Arp(ArpInfo),
    Ip(Packet),
}

/// Ethernet frame on a cable.
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

/// Simulation log event: time in microseconds, device, kind and text.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct NetEvent {
    pub t: f64,
    pub dev: String,
    pub kind: EventKind,
    pub text: String,
}

/// Frame hop over a cable (for animation and capture).
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

/// Packet delivered to a device (locally).
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Delivered {
    pub dev: String,
    pub src: Option<u32>,
    pub dst: Option<u32>,
    pub proto: Proto,
    pub dport: Option<i64>,
    pub sport: Option<i64>,
}

/// Probe outcome (ping, TCP, UDP, DNS).
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
    /// Empty probe (no connectivity, name not resolved).
    pub fn empty(status: ProbeStatus) -> ProbeRun {
        ProbeRun { status, from: None, code: None, mtu: None, dns: None, rtt_us: None, events: vec![], hops: vec![], delivered: vec![] }
    }
}

/* ---- internal caches ---- */

/// ARP cache entry: MAC, time and number of the simulation that learned it (-1 means spoofed).
#[derive(Clone, Debug, PartialEq)]
pub struct ArpEntry {
    pub mac: String,
    pub at: f64,
    pub sim: i64,
}

/// Conntrack entry.
#[derive(Clone, Debug, PartialEq)]
pub struct ConnEntry {
    pub orig: Tuple,
    pub tr: Tuple,
    pub replied: bool,
}

/// Packet capture line.
#[derive(Clone, Debug, PartialEq)]
pub struct CapRow {
    pub t: f64,
    /// `true` means the frame came in ("In"), `false` means it went out ("Out").
    pub inbound: bool,
    pub frame: Frame,
}

/// HTTP response.
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

/// Tunnel peer address learned from the last packet.
#[derive(Clone, Debug, PartialEq)]
pub struct TunPeer {
    pub ip: Option<u32>,
    pub port: Option<i64>,
}

/// Runtime caches of the simulator: ARP, MAC tables, conntrack, DNS cache, packet capture. Not saved in JSON.
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

/// Network state: devices and cables (+ PKI if the network has TLS). Simulator caches are in `rt`.
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

/// Port reference text "device:port".
pub fn port_ref(dev: &str, port: &str) -> String {
    format!("{dev}:{port}")
}
