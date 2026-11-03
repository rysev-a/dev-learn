//! Shared building blocks of the scenario packs: a board builder.

use super::super::{next_pos, raw_specs, Edge, Kind, Node, Param, Topology};

pub(crate) fn s(text: &str) -> String {
    text.to_string()
}

/// Board builder: objects get places by their kind, links are added by identifiers. Parameters that equal the default of the kind stay unset
/// (the data files and the drafts stay small, and a start board and a reference board do not differ by a parameter that merely repeats its default).
#[derive(Clone, Default)]
pub(crate) struct B {
    pub(crate) t: Topology,
}

fn store(n: &mut Node, key: &str, value: &str) {
    n.params.remove(key);
    if n.param_text(key) != value {
        let is_switch = raw_specs(n.kind).iter().find(|r| r.key == key).is_some_and(|r| r.options.is_empty());
        n.params.insert(key.into(), if is_switch { Param::Bool(value == "true") } else { Param::Str(value.into()) });
    }
}

impl B {
    fn put(&mut self, id: &str, kind: Kind, name: &str, params: &[(&str, &str)]) -> &mut Self {
        let (x, y) = next_pos(&self.t, kind);
        let mut n = Node::new(id, kind, name, x, y);
        for (key, value) in params {
            store(&mut n, key, value);
        }
        self.t.nodes.push(n);
        self
    }

    /// A network namespace (`forward`: ip_forward on).
    pub(crate) fn ns(&mut self, id: &str, name: &str, forward: bool) -> &mut Self {
        self.put(id, Kind::Netns, name, &[("forward", if forward { "true" } else { "false" })])
    }

    /// The outside network of the network `net` (a, b or c), speaking the VLAN `tagged` (0: untagged).
    pub(crate) fn ext(&mut self, id: &str, name: &str, net: &str, tagged: u32) -> &mut Self {
        self.put(id, Kind::External, name, &[("net", net), ("tagged", &tagged.to_string())])
    }

    /// A physical interface in a namespace, cabled to an outside network (`ext` empty: no cable).
    pub(crate) fn eth(&mut self, id: &str, name: &str, ns: &str, net: &str, ext: &str) -> &mut Self {
        self.put(id, Kind::Eth, name, &[("net", net)]).link(&[(ns, id)]);
        if !ext.is_empty() {
            self.link(&[(id, ext)]);
        }
        self
    }

    /// One end of a veth pair in a namespace.
    pub(crate) fn veth(&mut self, id: &str, name: &str, ns: &str, net: &str) -> &mut Self {
        self.put(id, Kind::Veth, name, &[("net", net)]).link(&[(ns, id)])
    }

    /// A bridge in a namespace.
    pub(crate) fn bridge(&mut self, id: &str, name: &str, ns: &str, net: &str) -> &mut Self {
        self.put(id, Kind::Bridge, name, &[("net", net)]).link(&[(ns, id)])
    }

    /// A bond in a namespace.
    pub(crate) fn bond(&mut self, id: &str, name: &str, ns: &str, mode: &str, net: &str) -> &mut Self {
        self.put(id, Kind::Bond, name, &[("mode", mode), ("net", net)]).link(&[(ns, id)])
    }

    /// A VLAN interface of a parent in a namespace.
    pub(crate) fn vlan(&mut self, id: &str, name: &str, ns: &str, parent: &str, vlan: u32, net: &str) -> &mut Self {
        self.put(id, Kind::Vlan, name, &[("id", &vlan.to_string()), ("net", net)]).link(&[(ns, id), (parent, id)])
    }

    /// A VM whose tap is a port of a bridge (`vlan`: the tag of the port).
    pub(crate) fn vm(&mut self, id: &str, name: &str, bridge: &str, net: &str, vlan: u32) -> &mut Self {
        self.put(id, Kind::Vm, name, &[("net", net), ("access_vlan", &vlan.to_string())]).link(&[(id, bridge)])
    }

    /// A NAT rule (`kind`: masquerade or dnat) on a namespace.
    pub(crate) fn nat(&mut self, id: &str, name: &str, ns: &str, kind: &str) -> &mut Self {
        self.put(id, Kind::Nat, name, &[("kind", kind)]).link(&[(id, ns)])
    }

    /// Change a parameter of an object (to the default too: the parameter is then removed). Switches take `true` / `false`.
    pub(crate) fn param(&mut self, id: &str, key: &str, value: &str) -> &mut Self {
        let n = self.t.nodes.iter_mut().find(|n| n.id == id).expect("object");
        store(n, key, value);
        self
    }

    pub(crate) fn link(&mut self, pairs: &[(&str, &str)]) -> &mut Self {
        for (a, b) in pairs {
            self.t.edges.push(Edge::new(a, b));
        }
        self
    }

    /// Drop a link.
    pub(crate) fn unlink(&mut self, a: &str, b: &str) -> &mut Self {
        self.t.edges.retain(|e| !(e.from == a && e.to == b));
        self
    }

    pub(crate) fn done(&self) -> Topology {
        self.t.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::super::super::{evaluate, problems, IfaceStatus};
    use super::*;

    #[test]
    fn the_helpers_build_valid_boards_and_leave_defaults_unset() {
        let mut b = B::default();
        b.ns("host", "host", false).ext("net", "internet", "a", 0).eth("eth0", "eth0", "host", "a", "net");
        let t = b.done();
        assert!(problems(&t).is_empty(), "{:?}", problems(&t).into_iter().map(|p| p.text).collect::<Vec<_>>());
        assert_eq!(t.node("host").map(|n| n.params.len()), Some(0), "forwarding is off by default");
        assert_eq!(t.node("net").map(|n| n.params.len()), Some(0), "net a untagged is the default of the outside network");
        assert_eq!(t.node("eth0").map(|n| n.params.len()), Some(1));
        assert_eq!(evaluate(&t).iface("eth0").map(|i| i.status), Some(IfaceStatus::Ok));
        for (i, a) in t.nodes.iter().enumerate() {
            for n in &t.nodes[i + 1..] {
                assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
            }
        }
    }
}
