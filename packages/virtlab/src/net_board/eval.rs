//! What follows from the links: the link state of every interface, the layer-2 segment every address lives in, and whether one host reaches another.
//!
//! The rules are the ones listed in the module documentation of [`net_board`](super): a veth end has a link only when its peer is up, a bond when a
//! slave has one, a bridge when a port has one; ports of a bridge carry a VLAN tag; a host reaches a host of its own network and segment directly and any
//! other through a gateway that forwards; the outside network needs a masquerade rule to answer a private address, and a DNAT rule to be let in.

use std::collections::{BTreeMap, BTreeSet};

use super::{Kind, Node, Rel, Topology};

/// Link state of an interface.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum IfaceStatus {
    /// The interface works.
    Ok,
    /// The interface is down by the administrator.
    Down,
    /// The interface is up but has no link.
    NoCarrier,
}

impl IfaceStatus {
    /// Name for the student.
    pub fn name(self) -> &'static str {
        match self {
            IfaceStatus::Ok => i18n::tr("up"),
            IfaceStatus::Down => i18n::tr("down"),
            IfaceStatus::NoCarrier => i18n::tr("no carrier"),
        }
    }
}

/// Why an interface has no link.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Why {
    /// The interface lives in no namespace.
    NoNamespace,
    /// The interface is down.
    AdminDown,
    /// A physical interface without a cable.
    NoCable,
    /// A veth end without a peer.
    NoPeer,
    /// The peer of a veth end is down or lives in no namespace.
    PeerDown,
    /// A bond without a slave that has a link.
    NoSlave,
    /// An 802.3ad bond whose slaves are cabled to different switches.
    LacpMismatch,
    /// A VLAN interface without a parent.
    NoParent,
    /// The parent of a VLAN interface has no link.
    ParentDown,
    /// A bridge without a port that has a link.
    NoPort,
    /// A VM whose tap is on no bridge.
    NoBridge,
    /// The bridge of a VM is down.
    BridgeDown,
}

impl Why {
    /// The explanation for the student.
    pub fn text(self) -> String {
        match self {
            Why::NoNamespace => i18n::tr("the interface lives in no namespace").to_string(),
            Why::AdminDown => i18n::tr("the interface is down").to_string(),
            Why::NoCable => i18n::tr("no cable: the interface is not connected to the outside network").to_string(),
            Why::NoPeer => i18n::tr("the veth end has no peer").to_string(),
            Why::PeerDown => i18n::tr("the other end of the veth pair is down or in no namespace, so this end has no link either").to_string(),
            Why::NoSlave => i18n::tr("no slave of the bond has a link").to_string(),
            Why::LacpMismatch => i18n::tr("an 802.3ad bond needs all its slaves on one switch").to_string(),
            Why::NoParent => i18n::tr("the VLAN interface has no parent").to_string(),
            Why::ParentDown => i18n::tr("the parent of the VLAN interface has no link").to_string(),
            Why::NoPort => i18n::tr("no port of the bridge has a link").to_string(),
            Why::NoBridge => i18n::tr("the tap of the VM is not on a bridge").to_string(),
            Why::BridgeDown => i18n::tr("the bridge of the VM is down").to_string(),
        }
    }
}

/// An interface after evaluation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct IfaceEval {
    /// Object identifier.
    pub id: String,
    /// Link state.
    pub status: IfaceStatus,
    /// Why there is no link.
    pub why: Option<Why>,
    /// The address, when the interface holds one that works (`10.0.1.2`).
    pub addr: Option<String>,
    /// The interface is a port of a bridge or a slave of a bond: it holds no address of its own.
    pub enslaved: bool,
    /// The layer-2 segment of the address (1, 2, …; the same number is the same segment), 0 when the interface has none.
    pub segment: u32,
}

/// An address that works: an interface that holds one, or the outside network.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Endpoint {
    /// The interface (or the outside network) that holds the address.
    pub iface: String,
    /// The host it belongs to: the namespace of the interface, the VM itself, or the outside network.
    pub host: String,
    /// Kind of the host.
    pub host_kind: Kind,
    /// The network, `a`, `b` or `c`.
    pub net: String,
    /// The layer-2 segment (an opaque identifier; equal identifiers are the same segment).
    pub domain: String,
    /// The segment if VLAN tags were ignored (tells a wrong VLAN from a missing cable).
    pub loose: String,
    /// The default route of the host goes out here.
    pub default_route: bool,
}

/// The board after evaluation.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Evaluation {
    /// Every interface of the board, in board order.
    pub ifaces: Vec<IfaceEval>,
    /// Every address that works.
    pub endpoints: Vec<Endpoint>,
}

impl Evaluation {
    /// An interface by identifier.
    pub fn iface(&self, id: &str) -> Option<&IfaceEval> {
        self.ifaces.iter().find(|i| i.id == id)
    }

    /// The addresses of a host (a namespace, a VM or the outside network).
    pub fn endpoints_of(&self, host: &str) -> Vec<&Endpoint> {
        self.endpoints.iter().filter(|e| e.host == host).collect()
    }
}

// ------------------------------------------------------------------------------------------------------------------------------ link state

/// Ports of a bridge (a VM's tap included), in board order.
fn ports<'a>(t: &'a Topology, bridge: &str) -> Vec<&'a Node> {
    let mut v = t.sources(bridge, Rel::Port);
    v.extend(t.sources(bridge, Rel::Tap));
    v
}

/// The link state of an interface: `Ok` when it has a link.
fn carrier(t: &Topology, id: &str) -> Result<(), Why> {
    let Some(n) = t.node(id) else { return Err(Why::NoNamespace) };
    if n.kind != Kind::Vm && t.netns_of(id).is_none() {
        return Err(Why::NoNamespace);
    }
    if !n.up() {
        return Err(Why::AdminDown);
    }
    match n.kind {
        Kind::Eth => t.cable_of(id).map(|_| ()).ok_or(Why::NoCable),
        Kind::Veth => {
            let peer = t.peer_of(id).ok_or(Why::NoPeer)?;
            if peer.up() && t.netns_of(&peer.id).is_some() {
                Ok(())
            } else {
                Err(Why::PeerDown)
            }
        }
        Kind::Bond => {
            let live: Vec<&Node> = t.sources(id, Rel::Slave).into_iter().filter(|s| carrier(t, &s.id).is_ok()).collect();
            if live.is_empty() {
                return Err(Why::NoSlave);
            }
            if n.param_text("mode") == "802.3ad" {
                let switches: BTreeSet<&str> = live.iter().filter_map(|s| t.cable_of(&s.id)).map(|x| x.id.as_str()).collect();
                if switches.len() > 1 {
                    return Err(Why::LacpMismatch);
                }
            }
            Ok(())
        }
        Kind::Vlan => {
            let parent = t.parent_of(id).ok_or(Why::NoParent)?;
            carrier(t, &parent.id).map_err(|_| Why::ParentDown)
        }
        Kind::Bridge => {
            if ports(t, id).iter().any(|p| p.up() && carrier(t, &p.id).is_ok()) {
                Ok(())
            } else {
                Err(Why::NoPort)
            }
        }
        Kind::Vm => {
            let bridge = t.bridge_of(id).ok_or(Why::NoBridge)?;
            if bridge.up() {
                Ok(())
            } else {
                Err(Why::BridgeDown)
            }
        }
        _ => Ok(()),
    }
}

/// A port of a bridge or a slave of a bond holds no address of its own.
fn enslaved(t: &Topology, n: &Node) -> bool {
    n.kind != Kind::Vm && (t.bridge_of(&n.id).is_some() || t.bond_of(&n.id).is_some())
}

/// The address of an interface: the network and the host number by the order of the board (`10.0.1.1`, `10.0.1.2`, …); the outside network is `.254`.
pub fn address(t: &Topology, id: &str) -> Option<String> {
    let n = t.node(id)?;
    let net = n.net();
    let third = match net.as_str() {
        "a" => 1,
        "b" => 2,
        "c" => 3,
        _ => return None,
    };
    if n.kind == Kind::External {
        return Some(format!("10.0.{third}.254"));
    }
    let number = t.nodes.iter().filter(|x| x.kind.is_iface() && x.net() == net).position(|x| x.id == id)? + 1;
    Some(format!("10.0.{third}.{number}"))
}

// -------------------------------------------------------------------------------------------------------------------------- segments

/// Union-find over text keys.
#[derive(Default)]
struct Uf(BTreeMap<String, String>);

impl Uf {
    fn find(&mut self, k: &str) -> String {
        let mut root = k.to_string();
        while let Some(p) = self.0.get(&root) {
            if *p == root {
                break;
            }
            root = p.clone();
        }
        self.0.entry(root.clone()).or_insert_with(|| root.clone());
        root
    }

    fn union(&mut self, a: &str, b: &str) {
        let (ra, rb) = (self.find(a), self.find(b));
        if ra != rb {
            self.0.insert(ra, rb);
        }
    }
}

/// The segment of every interface and of the outside networks; with `ignore_tags` VLAN tags are ignored.
fn segments(t: &Topology, ignore_tags: bool) -> BTreeMap<String, String> {
    // 1. the wires: veth pairs, cables, bonds
    let mut wires = Uf::default();
    for n in &t.nodes {
        match n.kind {
            Kind::Veth => {
                if let Some(peer) = t.peer_of(&n.id) {
                    if carrier(t, &n.id).is_ok() && carrier(t, &peer.id).is_ok() {
                        wires.union(&format!("W:{}", n.id), &format!("W:{}", peer.id));
                    }
                }
            }
            Kind::Eth => {
                if let Some(ext) = t.cable_of(&n.id) {
                    if carrier(t, &n.id).is_ok() {
                        wires.union(&format!("W:{}", n.id), &format!("X:{}", ext.id));
                    }
                }
            }
            Kind::Bond => {
                for s in t.sources(&n.id, Rel::Slave) {
                    if carrier(t, &s.id).is_ok() {
                        wires.union(&format!("W:{}", n.id), &format!("W:{}", s.id));
                    }
                }
            }
            _ => {}
        }
    }
    // 2. the segments: untagged and tagged frames of a wire, the VLANs of a bridge
    let untagged = |w: &mut Uf, key: &str| format!("U:{}", w.find(key));
    let tagged = |w: &mut Uf, key: &str, id: &str| {
        if ignore_tags {
            format!("U:{}", w.find(key))
        } else {
            format!("T:{}:{id}", w.find(key))
        }
    };
    let bridge_domain = |m: &str, tag: u32| if ignore_tags { format!("B:{m}") } else { format!("B:{m}:{tag}") };
    let outer = |w: &mut Uf, n: &Node| -> Option<String> {
        match n.kind {
            Kind::Eth | Kind::Veth | Kind::Bond => Some(untagged(w, &format!("W:{}", n.id))),
            Kind::Vlan => {
                let parent = t.parent_of(&n.id)?;
                Some(tagged(w, &format!("W:{}", parent.id), &n.param_text("id")))
            }
            _ => None,
        }
    };
    let mut seg = Uf::default();
    for m in t.of_kind(Kind::Bridge) {
        if carrier(t, &m.id).is_err() {
            continue;
        }
        for p in ports(t, &m.id) {
            if !p.up() || carrier(t, &p.id).is_err() {
                continue;
            }
            if let Some(o) = outer(&mut wires, p) {
                seg.union(&o, &bridge_domain(&m.id, p.access_vlan()));
            }
        }
    }
    // 3. where every address sits
    let mut at = BTreeMap::new();
    for n in &t.nodes {
        let key = match n.kind {
            Kind::Eth | Kind::Veth | Kind::Bond | Kind::Vlan => outer(&mut wires, n),
            Kind::Bridge => Some(bridge_domain(&n.id, n.access_vlan())),
            Kind::Vm => t.bridge_of(&n.id).map(|b| bridge_domain(&b.id, n.access_vlan())),
            Kind::External => {
                let tag = n.param_text("tagged");
                Some(if tag == "0" { untagged(&mut wires, &format!("X:{}", n.id)) } else { tagged(&mut wires, &format!("X:{}", n.id), &tag) })
            }
            _ => None,
        };
        if let Some(k) = key {
            at.insert(n.id.clone(), seg.find(&k));
        }
    }
    at
}

/// Evaluates the board.
pub fn evaluate(t: &Topology) -> Evaluation {
    let strict = segments(t, false);
    let loose = segments(t, true);
    let mut ev = Evaluation::default();
    let mut numbers: BTreeMap<String, u32> = BTreeMap::new();
    for n in t.nodes.iter().filter(|n| n.kind.is_iface()) {
        let state = carrier(t, &n.id);
        let status = match state {
            Ok(()) => IfaceStatus::Ok,
            Err(Why::AdminDown) => IfaceStatus::Down,
            Err(_) => IfaceStatus::NoCarrier,
        };
        let slave = enslaved(t, n);
        let works = state.is_ok() && !slave && n.net() != "none";
        let mut segment = 0;
        if works {
            if let Some(d) = strict.get(&n.id) {
                let next = numbers.len() as u32 + 1;
                segment = *numbers.entry(d.clone()).or_insert(next);
            }
            let host = if n.kind == Kind::Vm { Some(n.id.clone()) } else { t.netns_of(&n.id).map(|x| x.id.clone()) };
            if let (Some(host), Some(domain), Some(lo)) = (host, strict.get(&n.id), loose.get(&n.id)) {
                ev.endpoints.push(Endpoint {
                    iface: n.id.clone(),
                    host,
                    host_kind: if n.kind == Kind::Vm { Kind::Vm } else { Kind::Netns },
                    net: n.net(),
                    domain: domain.clone(),
                    loose: lo.clone(),
                    default_route: n.flag("default_route"),
                });
            }
        }
        ev.ifaces.push(IfaceEval {
            id: n.id.clone(),
            status,
            why: state.err(),
            addr: if works { address(t, &n.id) } else { None },
            enslaved: slave,
            segment,
        });
    }
    for n in t.of_kind(Kind::External) {
        if let (Some(domain), Some(lo)) = (strict.get(&n.id), loose.get(&n.id)) {
            ev.endpoints.push(Endpoint {
                iface: n.id.clone(),
                host: n.id.clone(),
                host_kind: Kind::External,
                net: n.net(),
                domain: domain.clone(),
                loose: lo.clone(),
                default_route: false,
            });
        }
    }
    ev
}

// -------------------------------------------------------------------------------------------------------------------------- reachability

/// The answer to «does a ping go through».
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Reach {
    /// The ping goes through and the reply comes back.
    Ok,
    /// A side has no address.
    NoAddress,
    /// A side has an address on an interface that has no link.
    LinkDown,
    /// The two are in the same network but not on the same wire.
    NotConnected,
    /// The two are in the same network but in different VLANs.
    VlanMismatch,
    /// There is no route: no default gateway, or the gateway has no leg into the destination.
    NoRoute,
    /// The gateway does not forward packets.
    ForwardOff,
    /// The outside network cannot answer a private address (no masquerade), or no DNAT rule lets the outside in.
    NoNat,
}

impl Reach {
    /// The ping goes through.
    pub fn ok(self) -> bool {
        self == Reach::Ok
    }

    /// The explanation for the student.
    pub fn text(self) -> String {
        match self {
            Reach::Ok => i18n::tr("the ping goes through and the reply comes back").to_string(),
            Reach::NoAddress => i18n::tr("a side has no address").to_string(),
            Reach::LinkDown => i18n::tr("the interface with the address has no link").to_string(),
            Reach::NotConnected => i18n::tr("same network, but the two are not on one wire").to_string(),
            Reach::VlanMismatch => i18n::tr("same network, but the ports are in different VLANs").to_string(),
            Reach::NoRoute => i18n::tr("no route: no gateway on the segment or no way into the destination network").to_string(),
            Reach::ForwardOff => i18n::tr("the gateway does not forward packets (ip_forward is off)").to_string(),
            Reach::NoNat => i18n::tr("the outside network does not know the private address: no masquerade or DNAT rule").to_string(),
        }
    }

    /// How far the packet got: a more advanced failure is the better diagnosis.
    fn rank(self) -> u8 {
        match self {
            Reach::Ok | Reach::NoAddress | Reach::LinkDown => 0,
            Reach::NoRoute => 1,
            Reach::NotConnected => 2,
            Reach::VlanMismatch => 3,
            Reach::ForwardOff => 4,
            Reach::NoNat => 5,
        }
    }
}

/// How a ping was resolved.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Resolution {
    pub(crate) reach: Reach,
    /// Layer-2 legs `(address on one side, address on the other)`: one when the hosts are neighbours, two through a gateway.
    pub(crate) legs: Vec<(String, String)>,
    /// The gateway, when the packet goes through one (also set when the failure is at the gateway).
    pub(crate) router: Option<String>,
    /// The masquerade rule that was used.
    pub(crate) nat: Option<String>,
}

fn fail(reach: Reach) -> Resolution {
    Resolution { reach, legs: vec![], router: None, nat: None }
}

/// Whether a host has an interface with an address that is configured but has no link (as opposed to no address at all).
fn dead_address(t: &Topology, ev: &Evaluation, host: &str) -> bool {
    t.nodes.iter().any(|n| {
        n.kind.is_iface()
            && n.net() != "none"
            && ev.iface(&n.id).is_some_and(|i| i.addr.is_none() && !i.enslaved)
            && (if n.kind == Kind::Vm { n.id == host } else { t.netns_of(&n.id).is_some_and(|x| x.id == host) })
    })
}

/// A masquerade rule on a namespace.
fn masquerade<'a>(t: &'a Topology, ns: &str) -> Option<&'a Node> {
    t.of_kind(Kind::Nat).find(|n| n.param_text("kind") == "masquerade" && t.linked(&n.id, ns))
}

/// Resolves a ping from one host to another. With `need_nat` false the masquerade rule is not demanded (the check of a DNAT rule uses that).
pub(crate) fn resolve(t: &Topology, ev: &Evaluation, from: &str, to: &str, need_nat: bool) -> Resolution {
    let (ea, eb) = (ev.endpoints_of(from), ev.endpoints_of(to));
    for (side, e) in [(from, &ea), (to, &eb)] {
        if e.is_empty() {
            return fail(if dead_address(t, ev, side) { Reach::LinkDown } else { Reach::NoAddress });
        }
    }
    if from == to {
        return Resolution { reach: Reach::Ok, legs: vec![], router: None, nat: None };
    }
    // neighbours: one network, one segment
    for a in &ea {
        for b in &eb {
            if a.net == b.net && a.domain == b.domain {
                return Resolution { reach: Reach::Ok, legs: vec![(a.iface.clone(), b.iface.clone())], router: None, nat: None };
            }
        }
    }
    let mut worst = Reach::NoRoute;
    let mut worst_router: Option<String> = None;
    let note = |reach: Reach, router: Option<&str>, worst: &mut Reach, worst_router: &mut Option<String>| {
        if reach.rank() > worst.rank() {
            *worst = reach;
            *worst_router = router.map(str::to_string);
        }
    };
    // the same network but another wire: a missing cable or a wrong VLAN
    for a in &ea {
        for b in &eb {
            if a.net == b.net {
                let reason = if a.loose == b.loose { Reach::VlanMismatch } else { Reach::NotConnected };
                note(reason, None, &mut worst, &mut worst_router);
            }
        }
    }
    // through a gateway: only a namespace or a VM has a default route, the outside network cannot route inwards
    if ea.first().is_some_and(|e| e.host_kind == Kind::External) {
        return fail(worst);
    }
    for a in ea.iter().filter(|e| e.default_route) {
        let gateways: Vec<&Endpoint> = ev
            .endpoints
            .iter()
            .filter(|g| g.host_kind == Kind::Netns && g.host != from && g.net == a.net && g.domain == a.domain && g.iface != a.iface)
            .collect();
        if gateways.is_empty() {
            let near = ev.endpoints.iter().any(|g| g.host_kind == Kind::Netns && g.host != from && g.net == a.net && g.loose == a.loose);
            note(if near { Reach::VlanMismatch } else { Reach::NoRoute }, None, &mut worst, &mut worst_router);
            continue;
        }
        for g in gateways {
            let Some(ns) = t.node(&g.host) else { continue };
            if !ns.flag("forward") {
                note(Reach::ForwardOff, Some(&g.host), &mut worst, &mut worst_router);
                continue;
            }
            let mut found = false;
            for b in &eb {
                for out in ev.endpoints_of(&g.host).into_iter().filter(|o| o.iface != g.iface && o.net == b.net && o.domain == b.domain) {
                    found = true;
                    if b.host_kind == Kind::External {
                        let rule = masquerade(t, &g.host);
                        if need_nat && rule.is_none() {
                            note(Reach::NoNat, Some(&g.host), &mut worst, &mut worst_router);
                            continue;
                        }
                        return Resolution {
                            reach: Reach::Ok,
                            legs: vec![(a.iface.clone(), g.iface.clone()), (out.iface.clone(), b.iface.clone())],
                            router: Some(g.host.clone()),
                            nat: rule.map(|r| r.id.clone()),
                        };
                    }
                    // the destination must be able to answer: its default route leads back to the gateway
                    let back = eb.iter().any(|e| e.host == b.host && e.default_route && e.net == out.net && e.domain == out.domain);
                    if !back {
                        note(Reach::NoRoute, Some(&g.host), &mut worst, &mut worst_router);
                        continue;
                    }
                    return Resolution {
                        reach: Reach::Ok,
                        legs: vec![(a.iface.clone(), g.iface.clone()), (out.iface.clone(), b.iface.clone())],
                        router: Some(g.host.clone()),
                        nat: None,
                    };
                }
            }
            if !found {
                let near = eb.iter().any(|b| ev.endpoints_of(&g.host).iter().any(|o| o.iface != g.iface && o.net == b.net && o.loose == b.loose));
                note(if near { Reach::VlanMismatch } else { Reach::NoRoute }, Some(&g.host), &mut worst, &mut worst_router);
            }
        }
    }
    Resolution { reach: worst, legs: vec![], router: worst_router, nat: None }
}

/// Whether a ping from `from` to `to` goes through (hosts: namespaces, VMs, outside networks).
pub fn ping(t: &Topology, ev: &Evaluation, from: &str, to: &str) -> Reach {
    resolve(t, ev, from, to, true).reach
}

/// The host a target of a DNAT rule belongs to: the VM itself, or the namespace of a veth end.
pub(crate) fn host_of(t: &Topology, target: &str) -> Option<String> {
    let n = t.node(target)?;
    match n.kind {
        Kind::Vm | Kind::Netns | Kind::External => Some(n.id.clone()),
        _ => t.netns_of(target).map(|x| x.id.clone()),
    }
}

/// Whether the outside network reaches a host inside through a DNAT rule on its router: a rule forwarding to the target, the router forwards,
/// has a leg in the segment of the outside network and one in the segment of the target, and the target can answer through it.
pub fn published(t: &Topology, ev: &Evaluation, external: &str, target: &str) -> Reach {
    let Some(host) = host_of(t, target) else { return Reach::NoAddress };
    let rules: Vec<&Node> = t.of_kind(Kind::Nat).filter(|n| n.param_text("kind") == "dnat" && t.linked(&n.id, target)).collect();
    if rules.is_empty() {
        return Reach::NoNat;
    }
    let (ee, eh) = (ev.endpoints_of(external), ev.endpoints_of(&host));
    if ee.is_empty() || eh.is_empty() {
        return Reach::NoAddress;
    }
    let mut worst = Reach::NoRoute;
    for rule in rules {
        let Some(router) = t.targets(&rule.id, Rel::On).into_iter().next() else { continue };
        if !router.flag("forward") {
            if Reach::ForwardOff.rank() > worst.rank() {
                worst = Reach::ForwardOff;
            }
            continue;
        }
        let legs = ev.endpoints_of(&router.id);
        let outside = legs.iter().any(|l| ee.iter().any(|e| e.net == l.net && e.domain == l.domain));
        let inside = legs.iter().any(|l| eh.iter().any(|e| e.net == l.net && e.domain == l.domain));
        if outside && inside && resolve(t, ev, &host, external, false).reach.ok() {
            return Reach::Ok;
        }
    }
    worst
}
