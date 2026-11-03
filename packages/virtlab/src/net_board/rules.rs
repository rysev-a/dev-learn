//! Which objects may be linked and what a link means; the checks of the board state.

use std::collections::{BTreeMap, BTreeSet};

use super::{param_error, Edge, Kind, Topology, MAX_NAME, MAX_NODES};

/// Relation a link stands for. The direction follows the table in [`rel`].
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Rel {
    /// An interface lives in a network namespace.
    Lives,
    /// Two veth ends are a pair (stored once, in either direction).
    Peer,
    /// An interface is a port of a bridge.
    Port,
    /// The tap device of a VM is a port of a bridge.
    Tap,
    /// A physical interface is a slave of a bond.
    Slave,
    /// A VLAN interface sits on a parent interface.
    Parent,
    /// A physical interface is cabled to the outside network.
    Cable,
    /// A NAT rule belongs to a namespace.
    On,
    /// A DNAT rule forwards the published port to a host inside.
    Forwards,
}

impl Rel {
    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Rel::Lives => i18n::tr("lives in the namespace"),
            Rel::Peer => i18n::tr("the other end of the veth pair"),
            Rel::Port => i18n::tr("port of the bridge"),
            Rel::Tap => i18n::tr("tap port of the bridge"),
            Rel::Slave => i18n::tr("slave of the bond"),
            Rel::Parent => i18n::tr("parent of the VLAN interface"),
            Rel::Cable => i18n::tr("cabled to the outside network"),
            Rel::On => i18n::tr("rule of the namespace"),
            Rel::Forwards => i18n::tr("forwards to"),
        }
    }
}

/// Relation of a link from an object of one kind to an object of another (`None`: the objects are not linked directly).
pub fn rel(from: Kind, to: Kind) -> Option<Rel> {
    Some(match (from, to) {
        (Kind::Netns, Kind::Eth | Kind::Veth | Kind::Bridge | Kind::Bond | Kind::Vlan) => Rel::Lives,
        (Kind::Veth, Kind::Veth) => Rel::Peer,
        (Kind::Eth | Kind::Veth | Kind::Bond | Kind::Vlan, Kind::Bridge) => Rel::Port,
        (Kind::Vm, Kind::Bridge) => Rel::Tap,
        (Kind::Eth, Kind::Bond) => Rel::Slave,
        (Kind::Eth | Kind::Bond, Kind::Vlan) => Rel::Parent,
        (Kind::Eth, Kind::External) => Rel::Cable,
        (Kind::Nat, Kind::Netns) => Rel::On,
        (Kind::Nat, Kind::Vm | Kind::Veth) => Rel::Forwards,
        _ => return None,
    })
}

/// Relations where an object of the target kind has exactly one source.
fn single_parent(r: Rel) -> bool {
    matches!(r, Rel::Lives | Rel::Parent)
}

/// Relations where an object of the source kind has exactly one target.
fn single_target(r: Rel) -> bool {
    matches!(r, Rel::Cable | Rel::On | Rel::Forwards)
}

/// A violated rule: the link it is about (index in `edges`) or the board as a whole, and the explanation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Problem {
    /// Index of the link, if the problem is about one.
    pub edge: Option<usize>,
    /// What is wrong, for the student.
    pub text: String,
}

fn about(edge: usize, text: &str) -> Problem {
    Problem { edge: Some(edge), text: text.to_string() }
}

fn single_parent_text(r: Rel) -> &'static str {
    match r {
        Rel::Lives => i18n::tr("an interface lives in one namespace"),
        _ => i18n::tr("a VLAN interface has one parent"),
    }
}

fn single_target_text(r: Rel) -> &'static str {
    match r {
        Rel::Cable => i18n::tr("a physical interface has one cable"),
        Rel::On => i18n::tr("a NAT rule belongs to one namespace"),
        _ => i18n::tr("a DNAT rule forwards to one host"),
    }
}

/// Interfaces that must share a namespace with `iface`: its bridge or bond, its ports and slaves, its parent and its VLAN interfaces.
fn bound(t: &Topology, iface: &str) -> Vec<String> {
    let mut v: Vec<String> = vec![];
    v.extend(t.bridge_of(iface).map(|n| n.id.clone()));
    v.extend(t.bond_of(iface).map(|n| n.id.clone()));
    v.extend(t.parent_of(iface).map(|n| n.id.clone()));
    for n in &t.nodes {
        let to_me = t.linked(&n.id, iface) && matches!(rel(n.kind, t.node(iface).map_or(Kind::Nat, |x| x.kind)), Some(Rel::Port | Rel::Slave | Rel::Parent));
        let from_me = t.linked(iface, &n.id) && rel(t.node(iface).map_or(Kind::Nat, |x| x.kind), n.kind) == Some(Rel::Parent);
        if to_me || from_me {
            v.push(n.id.clone());
        }
    }
    v
}

/// Putting `iface` into the namespace `ns` would split it from an interface it is bound to.
fn ns_conflict(t: &Topology, iface: &str, ns: &str) -> bool {
    bound(t, iface).iter().any(|b| t.netns_of(b).is_some_and(|x| x.id != ns))
}

/// Every rule the board state breaks. A state built with [`connect_error`] and [`prune`] has no problems; the server rejects a hand-made one.
pub fn problems(t: &Topology) -> Vec<Problem> {
    let mut out = vec![];
    let mut ids = BTreeSet::new();
    for n in &t.nodes {
        if n.id.is_empty() || !ids.insert(n.id.as_str()) {
            out.push(Problem { edge: None, text: i18n::tr("object identifiers must be unique and not empty").to_string() });
        }
        if n.name.chars().count() > MAX_NAME || !n.x.is_finite() || !n.y.is_finite() {
            out.push(Problem { edge: None, text: i18n::tr("an object has an invalid name or position").to_string() });
        }
        if let Some(text) = param_error(n) {
            out.push(Problem { edge: None, text });
        }
    }
    if t.nodes.len() > MAX_NODES {
        out.push(Problem { edge: None, text: i18n::trf!("at most {0} objects are allowed", MAX_NODES) });
    }
    if t.edges.len() > MAX_NODES * 3 {
        out.push(Problem { edge: None, text: i18n::tr("too many links").to_string() });
        return out;
    }
    let mut seen: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut seen_from: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut pairs = BTreeSet::new();
    let mut masters: BTreeSet<&str> = BTreeSet::new();
    let mut peered: BTreeSet<&str> = BTreeSet::new();
    for (i, Edge { from, to }) in t.edges.iter().enumerate() {
        let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
            out.push(about(i, i18n::tr("a link leads to an unknown object")));
            continue;
        };
        if from == to {
            out.push(about(i, i18n::tr("an object cannot be linked to itself")));
            continue;
        }
        let Some(r) = rel(a.kind, b.kind) else {
            out.push(about(i, i18n::tr("in Linux networking these objects are not linked directly")));
            continue;
        };
        let (lo, hi) = if r == Rel::Peer && to < from { (to.as_str(), from.as_str()) } else { (from.as_str(), to.as_str()) };
        if !pairs.insert((lo, hi)) {
            out.push(about(i, i18n::tr("these objects are already linked")));
            continue;
        }
        if single_parent(r) && seen.insert((r, to.as_str()), i).is_some() {
            out.push(about(i, single_parent_text(r)));
            continue;
        }
        if single_target(r) && seen_from.insert((r, from.as_str()), i).is_some() {
            out.push(about(i, single_target_text(r)));
            continue;
        }
        match r {
            Rel::Peer => {
                if !peered.insert(from.as_str()) || !peered.insert(to.as_str()) {
                    out.push(about(i, i18n::tr("a veth end has one peer")));
                }
            }
            Rel::Port | Rel::Tap | Rel::Slave => {
                if !masters.insert(from.as_str()) {
                    out.push(about(i, i18n::tr("an interface is a port of one bridge or a slave of one bond")));
                } else if r != Rel::Tap {
                    let (ns_a, ns_b) = (t.netns_of(from), t.netns_of(to));
                    if let (Some(x), Some(y)) = (ns_a, ns_b) {
                        if x.id != y.id {
                            out.push(about(i, i18n::tr("a port and its bridge or bond must be in the same namespace")));
                        }
                    }
                }
            }
            Rel::Parent => {
                if let (Some(x), Some(y)) = (t.netns_of(from), t.netns_of(to)) {
                    if x.id != y.id {
                        out.push(about(i, i18n::tr("a VLAN interface must be in the namespace of its parent")));
                    }
                }
            }
            Rel::Forwards => {
                if a.param_text("kind") != "dnat" {
                    out.push(about(i, i18n::tr("only a DNAT rule forwards to a host")));
                }
            }
            Rel::Lives if ns_conflict(t, to, from) => {
                out.push(about(i, i18n::tr("a port and its bridge or bond must be in the same namespace")));
            }
            _ => {}
        }
    }
    out
}

/// Why the link `from → to` cannot be added to the board (`None`: it can). The direction is the one of [`rel`]; a veth pair may be linked either way.
pub fn connect_error(t: &Topology, from: &str, to: &str) -> Option<String> {
    if from == to {
        return Some(i18n::tr("an object cannot be linked to itself").to_string());
    }
    let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
        return Some(i18n::tr("a link leads to an unknown object").to_string());
    };
    if rel(a.kind, b.kind).is_none() {
        return Some(i18n::tr("in Linux networking these objects are not linked directly").to_string());
    }
    let mut next = t.clone();
    next.edges.push(Edge::new(from, to));
    let index = next.edges.len() - 1;
    problems(&next).into_iter().find(|p| p.edge == Some(index)).map(|p| p.text)
}

/// Why an object of this kind cannot be added to the board (`None`: it can).
pub fn add_error(t: &Topology, _kind: Kind, max_nodes: usize) -> Option<String> {
    if t.nodes.len() >= max_nodes.min(MAX_NODES) {
        return Some(i18n::trf!("at most {0} objects are allowed", max_nodes.min(MAX_NODES)));
    }
    None
}

/// Drop the links that no longer make sense (after an object or a link was removed). Returns how many were dropped.
pub fn prune(t: &mut Topology) -> usize {
    let mut dropped = 0;
    loop {
        let bad = problems(t).into_iter().find_map(|p| p.edge);
        match bad {
            Some(i) => {
                t.edges.remove(i);
                dropped += 1;
            }
            None => return dropped,
        }
    }
}
