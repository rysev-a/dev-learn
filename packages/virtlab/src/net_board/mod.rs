//! Linux network board (book 19, chapters 10–12): the student assembles the network of a Linux host — namespaces, physical interfaces, veth pairs,
//! bridges, bonds, VLAN interfaces, VMs, the outside network and NAT rules — and links the objects. The model ([`evaluate`]) derives what follows from
//! the links: which interfaces have a link, which layer-2 segment every address lives in, and ([`trace`]) whether a ping goes through, hop by hop.
//!
//! These are the **rules of the lab**, not a copy of Linux:
//!
//! * three private networks `a`, `b`, `c` (10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24); an interface holds one address of its network (host number by the
//!   order of the board), an enslaved interface (a bridge port, a bond slave) holds none;
//! * a veth end has a link only when its peer exists and is up, a physical interface only when it is up and cabled to the outside, a bond when one of its
//!   slaves has a link (an 802.3ad bond needs all its slaves on one switch), a bridge when one of its ports has, a VLAN interface when its parent has;
//! * ports of a bridge carry the VLAN tag of the port (`access_vlan`, 0 = untagged): ports with different tags are different segments, a veth or a
//!   cable joins the segments of the two ends untagged, a VLAN interface sits on the tagged frames of its parent;
//! * a host reaches a host of its own network and segment directly, any other through the default-route interface and a router: a namespace with
//!   `forward` and one interface in the segment of the gateway and one in the segment of the destination (one router at most);
//! * the outside network does not know the private networks: a ping from a private network to the outside needs a masquerade rule on the router,
//!   and the outside reaches an inner host only through a DNAT rule that forwards to it.
//!
//! The solution of a scenario is the whole [`Topology`]; the server checks it with the same functions ([`Scenario::reached`]).

mod eval;
mod goals;
mod judge;
mod layout;
mod packs;
mod params;
mod rules;
mod trace;

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

pub use eval::{address, evaluate, ping, published, Endpoint, Evaluation, IfaceEval, IfaceStatus, Reach, Why};
pub use goals::{GoalResult, NetGoal, Scenario};
pub use judge::{find as scenario_of, judge, Judgement};
pub use layout::{auto_layout, column, next_pos, NODE_H, NODE_W};
pub(crate) use params::raw_specs;
pub use packs::{pack, pack_chapter, pack_ids, PackDef, FIX_PACK, PACKS};
pub use params::{net_label, param_error, param_specs, param_to_text, ParamOption, ParamSpec, ParamTy};
pub use rules::{add_error, connect_error, problems, prune, rel, Problem, Rel};
pub use trace::{trace, Hop, Op, Trace};

/// The most objects on a board (a bound for the server check).
pub const MAX_NODES: usize = 40;
/// The longest object name.
pub const MAX_NAME: usize = 40;

/// Kind of an object.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Kind {
    /// The outside network (a switch and the host behind it).
    External,
    /// A physical interface (a NIC).
    Eth,
    /// A bond of physical interfaces.
    Bond,
    /// A VLAN interface on a physical interface or a bond.
    Vlan,
    /// A bridge: a software switch.
    Bridge,
    /// One end of a veth pair.
    Veth,
    /// A virtual machine (its tap device is a port of a bridge).
    Vm,
    /// A network namespace (the host itself is one).
    Netns,
    /// A NAT rule of a namespace.
    Nat,
}

impl Kind {
    /// All kinds in the order of the palette.
    pub const ALL: [Kind; 9] =
        [Kind::Netns, Kind::Eth, Kind::Veth, Kind::Bridge, Kind::Bond, Kind::Vlan, Kind::Vm, Kind::External, Kind::Nat];

    /// Name in data files.
    pub fn as_str(self) -> &'static str {
        match self {
            Kind::External => "external",
            Kind::Eth => "eth",
            Kind::Bond => "bond",
            Kind::Vlan => "vlan",
            Kind::Bridge => "bridge",
            Kind::Veth => "veth",
            Kind::Vm => "vm",
            Kind::Netns => "netns",
            Kind::Nat => "nat",
        }
    }

    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Kind::External => i18n::tr("outside network"),
            Kind::Eth => i18n::tr("physical interface"),
            Kind::Bond => i18n::tr("bond"),
            Kind::Vlan => i18n::tr("VLAN interface"),
            Kind::Bridge => i18n::tr("bridge"),
            Kind::Veth => i18n::tr("veth end"),
            Kind::Vm => i18n::tr("VM"),
            Kind::Netns => i18n::tr("namespace"),
            Kind::Nat => i18n::tr("NAT rule"),
        }
    }

    /// An object with an interface of its own: it has a link state, can be a port and can hold an address.
    pub fn is_iface(self) -> bool {
        matches!(self, Kind::Eth | Kind::Bond | Kind::Vlan | Kind::Bridge | Kind::Veth | Kind::Vm)
    }

    /// An object that can be pinged: a namespace, a VM or the outside network.
    pub fn is_host(self) -> bool {
        matches!(self, Kind::Netns | Kind::Vm | Kind::External)
    }
}

/// Parameter of an object.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Param {
    /// Switch.
    Bool(bool),
    /// Choice from a list.
    Str(String),
}

/// Object on the board.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Node {
    /// Identifier, unique on the board.
    pub id: String,
    /// Kind.
    pub kind: Kind,
    /// Name shown on the board.
    pub name: String,
    /// Position of the centre (boards given as task data have none: `auto_layout` places them).
    #[serde(default)]
    pub x: f64,
    /// Position of the centre.
    #[serde(default)]
    pub y: f64,
    /// Parameters (`net` of an interface, `forward` of a namespace, …).
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub params: BTreeMap<String, Param>,
}

impl Node {
    /// A node without parameters.
    pub fn new(id: &str, kind: Kind, name: &str, x: f64, y: f64) -> Node {
        Node { id: id.into(), kind, name: name.into(), x, y, params: BTreeMap::new() }
    }

    /// The value of a parameter as text, with the default when it is unset or not allowed (`true` / `false` for a switch). A key the kind
    /// does not have reads as the stored value, or as an empty text.
    pub fn param_text(&self, key: &str) -> String {
        let stored = self.params.get(key);
        match raw_specs(self.kind).iter().find(|s| s.key == key) {
            Some(spec) => match stored {
                Some(p) if spec.accepts(p) => param_to_text(p),
                _ => spec.default.to_string(),
            },
            None => stored.map(param_to_text).unwrap_or_default(),
        }
    }

    /// A switch parameter (the default of the kind when unset).
    pub fn flag(&self, key: &str) -> bool {
        self.param_text(key) == "true"
    }

    /// Set a parameter (builder style).
    pub fn with_param(mut self, key: &str, value: Param) -> Node {
        self.params.insert(key.into(), value);
        self
    }

    /// The network of the interface or of the outside network: `a`, `b`, `c`, or `none`.
    pub fn net(&self) -> String {
        self.param_text("net")
    }

    /// The interface is administratively up.
    pub fn up(&self) -> bool {
        self.flag("up")
    }

    /// The VLAN tag the port puts on the frames of its wire inside a bridge (0: none).
    pub fn access_vlan(&self) -> u32 {
        self.param_text("access_vlan").parse().unwrap_or(0)
    }
}

/// Link between two objects; the direction is fixed by the kinds (see [`rel`]).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Edge {
    /// Identifier of the source object.
    pub from: String,
    /// Identifier of the target object.
    pub to: String,
}

impl Edge {
    /// A link.
    pub fn new(from: &str, to: &str) -> Edge {
        Edge { from: from.into(), to: to.into() }
    }
}

/// What the student builds: objects and links. It is also the draft and the solution.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct Topology {
    /// Objects.
    pub nodes: Vec<Node>,
    /// Links.
    pub edges: Vec<Edge>,
}

impl Topology {
    /// Object by identifier.
    pub fn node(&self, id: &str) -> Option<&Node> {
        self.nodes.iter().find(|n| n.id == id)
    }

    /// Objects of a kind, in board order.
    pub fn of_kind(&self, kind: Kind) -> impl Iterator<Item = &Node> {
        self.nodes.iter().filter(move |n| n.kind == kind)
    }

    /// The link exists.
    pub fn linked(&self, from: &str, to: &str) -> bool {
        self.edges.iter().any(|e| e.from == from && e.to == to)
    }

    /// The two objects are linked in either direction (a veth pair is stored once).
    pub fn linked_either(&self, a: &str, b: &str) -> bool {
        self.linked(a, b) || self.linked(b, a)
    }

    /// Targets of the links of a relation that start at `from`, in board order.
    pub fn targets(&self, from: &str, r: Rel) -> Vec<&Node> {
        let Some(from_kind) = self.node(from).map(|n| n.kind) else { return vec![] };
        self.nodes.iter().filter(|n| self.linked(from, &n.id) && rel(from_kind, n.kind) == Some(r)).collect()
    }

    /// Sources of the links of a relation that end at `to`, in board order.
    pub fn sources(&self, to: &str, r: Rel) -> Vec<&Node> {
        let Some(to_kind) = self.node(to).map(|n| n.kind) else { return vec![] };
        self.nodes.iter().filter(|n| self.linked(&n.id, to) && rel(n.kind, to_kind) == Some(r)).collect()
    }

    /// The other end of a veth pair.
    pub fn peer_of(&self, veth: &str) -> Option<&Node> {
        self.nodes.iter().find(|n| n.id != veth && n.kind == Kind::Veth && self.linked_either(veth, &n.id))
    }

    /// Namespace an interface lives in.
    pub fn netns_of(&self, iface: &str) -> Option<&Node> {
        self.sources(iface, Rel::Lives).into_iter().next()
    }

    /// The bridge an interface is a port of (a VM's tap included).
    pub fn bridge_of(&self, iface: &str) -> Option<&Node> {
        let ports = self.targets(iface, Rel::Port);
        ports.into_iter().next().or_else(|| self.targets(iface, Rel::Tap).into_iter().next())
    }

    /// The bond an interface is a slave of.
    pub fn bond_of(&self, iface: &str) -> Option<&Node> {
        self.targets(iface, Rel::Slave).into_iter().next()
    }

    /// The parent of a VLAN interface.
    pub fn parent_of(&self, vlan: &str) -> Option<&Node> {
        self.sources(vlan, Rel::Parent).into_iter().next()
    }

    /// The outside network a physical interface is cabled to.
    pub fn cable_of(&self, eth: &str) -> Option<&Node> {
        self.targets(eth, Rel::Cable).into_iter().next()
    }

    /// The board without an object and the links of it (the object is gone: a NIC that failed).
    pub fn without(&self, id: &str) -> Topology {
        Topology {
            nodes: self.nodes.iter().filter(|n| n.id != id).cloned().collect(),
            edges: self.edges.iter().filter(|e| e.from != id && e.to != id).cloned().collect(),
        }
    }
}
