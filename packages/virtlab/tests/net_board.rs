//! Network board: the rules of links, the derived link states, reachability, the trace and the scenarios of every pack.

use virtlab::net_board::{
    add_error, address, auto_layout, connect_error, evaluate, judge, pack, pack_chapter, pack_ids, param_error, param_specs, ping,
    problems, prune, published, trace, Edge, IfaceStatus, Kind, Node, NetGoal, Op, Param, Reach, Scenario, Topology, Why,
};
use virtlab::{GoalStatus, Spec, Strictness};

fn en() {
    locales::set_locale(i18n::Locale::En);
}

fn node(kind: Kind, id: &str) -> Node {
    Node::new(id, kind, id, 0.0, 0.0)
}

fn with(mut n: Node, key: &str, value: &str) -> Node {
    let is_switch = matches!(value, "true" | "false");
    n.params.insert(key.into(), if is_switch { Param::Bool(value == "true") } else { Param::Str(value.into()) });
    n
}

fn link(t: &mut Topology, from: &str, to: &str) {
    t.edges.push(Edge::new(from, to));
}

/// The host with a bridge `br0` (address in network `a`) and VMs with the given VLAN tags on it.
fn vm_board(vms: &[(&str, &str)]) -> Topology {
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Netns, "host"));
    t.nodes.push(node(Kind::Bridge, "br0"));
    link(&mut t, "host", "br0");
    for (id, tag) in vms {
        t.nodes.push(with(with(node(Kind::Vm, id), "net", "a"), "access_vlan", tag));
        link(&mut t, id, "br0");
    }
    t
}

/// A host with two NICs cabled to a switch, a bond over them with the address.
fn bond_board(mode: &str) -> Topology {
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Netns, "host"));
    t.nodes.push(node(Kind::External, "sw"));
    t.nodes.push(with(with(node(Kind::Bond, "bond0"), "net", "a"), "mode", mode));
    link(&mut t, "host", "bond0");
    for e in ["eth1", "eth2"] {
        t.nodes.push(node(Kind::Eth, e));
        link(&mut t, "host", e);
        link(&mut t, e, "sw");
        link(&mut t, e, "bond0");
    }
    t
}

/// The container network: host with uplink, a bridge, a veth pair, a container. All the switches on.
fn nat_board() -> Topology {
    let mut t = Topology::default();
    t.nodes.push(with(node(Kind::Netns, "host"), "forward", "true"));
    t.nodes.push(node(Kind::Netns, "ns1"));
    t.nodes.push(node(Kind::External, "net"));
    t.nodes.push(with(node(Kind::Eth, "eth0"), "net", "a"));
    t.nodes.push(with(node(Kind::Bridge, "br0"), "net", "b"));
    t.nodes.push(node(Kind::Veth, "v1h"));
    t.nodes.push(with(with(node(Kind::Veth, "v1c"), "net", "b"), "default_route", "true"));
    t.nodes.push(node(Kind::Nat, "masq"));
    for (a, b) in [("host", "eth0"), ("eth0", "net"), ("host", "br0"), ("host", "v1h"), ("ns1", "v1c"), ("v1h", "v1c"), ("v1h", "br0"), ("masq", "host")] {
        link(&mut t, a, b);
    }
    t
}

fn reach(t: &Topology, from: &str, to: &str) -> Reach {
    ping(t, &evaluate(t), from, to)
}

fn set(t: &mut Topology, id: &str, key: &str, value: &str) {
    let n = t.nodes.iter_mut().find(|n| n.id == id).unwrap();
    n.params.insert(key.into(), if matches!(value, "true" | "false") { Param::Bool(value == "true") } else { Param::Str(value.into()) });
}

// ---------------------------------------------------------------- scenarios

/// Scenarios of every pack with their reference boards.
fn all() -> Vec<(Scenario, Topology)> {
    en();
    let mut out = vec![];
    for id in pack_ids() {
        let (scenarios, mut solution) = pack(id).expect("pack");
        assert_eq!(scenarios.len(), solution.len(), "{id}: a reference board for every scenario");
        for sc in scenarios {
            let reference = solution.remove(&sc.id).unwrap_or_else(|| panic!("{id}/{}: no reference", sc.id));
            out.push((sc, reference));
        }
    }
    out
}

#[test]
fn start_boards_do_not_reach_the_goals_and_references_do() {
    for (sc, reference) in all() {
        assert!(problems(&sc.start).is_empty(), "{}: the starting board breaks a rule: {:?}", sc.id, problems(&sc.start));
        assert!(!sc.reached(&sc.start), "{}: the starting board must not solve the scenario", sc.id);
        assert!(!sc.reached(&Topology::default()), "{}: an empty board must not solve the scenario", sc.id);
        assert!(problems(&reference).is_empty(), "{}: reference breaks a rule: {:?}", sc.id, problems(&reference).into_iter().map(|p| p.text).collect::<Vec<_>>());
        assert!(sc.invalid(&reference).is_none(), "{}: {:?}", sc.id, sc.invalid(&reference));
        let results = sc.results(&reference);
        assert!(results.iter().all(|r| r.ok), "{}: {:?}", sc.id, results);
    }
}

#[test]
fn every_step_of_every_reference_is_needed() {
    // undoing any single thing the student does (a link, an object, a changed parameter) must break the scenario
    for (sc, reference) in all() {
        let mut weaker: Vec<(String, Topology)> = vec![];
        for e in reference.edges.iter().filter(|e| !sc.start.edges.contains(e)) {
            let mut t = reference.clone();
            t.edges.retain(|x| x != e);
            weaker.push((format!("link {} → {}", e.from, e.to), t));
        }
        for n in &reference.nodes {
            match sc.start.node(&n.id) {
                None => weaker.push((format!("object {}", n.id), reference.without(&n.id))),
                Some(old) if old != n => {
                    let keys: std::collections::BTreeSet<&String> = old.params.keys().chain(n.params.keys()).collect();
                    for key in keys {
                        if old.params.get(key) != n.params.get(key) {
                            let mut t = reference.clone();
                            let node = t.nodes.iter_mut().find(|x| x.id == n.id).unwrap();
                            match old.params.get(key) {
                                Some(v) => {
                                    node.params.insert(key.clone(), v.clone());
                                }
                                None => {
                                    node.params.remove(key);
                                }
                            }
                            weaker.push((format!("parameter {key} of {}", n.id), t));
                        }
                    }
                }
                Some(_) => {}
            }
        }
        assert!(!weaker.is_empty(), "{}: the reference changes nothing", sc.id);
        for (what, mut t) in weaker {
            prune(&mut t);
            assert!(!sc.reached(&t), "{}: {what} is not needed", sc.id);
        }
    }
}

#[test]
fn every_pack_is_a_well_formed_exercise() {
    en();
    let mut seen = std::collections::BTreeSet::new();
    for id in pack_ids() {
        let (scenarios, solution) = pack(id).unwrap();
        assert!((4..=6).contains(&scenarios.len()), "{id}: a pack has 4 to 6 scenarios, not {}", scenarios.len());
        assert!(pack_chapter(id).is_some());
        assert_eq!(solution.len(), scenarios.len(), "{id}");
        for sc in &scenarios {
            assert!(seen.insert(format!("{id}/{}", sc.id)), "{id}: duplicate scenario {}", sc.id);
            assert!(!sc.title.is_empty() && !sc.story.is_empty() && !sc.goal.is_empty() && !sc.hint.is_empty(), "{id}/{}: texts", sc.id);
            assert!(sc.goals.len() >= 2, "{id}/{}: a scenario has at least two goals", sc.id);
            assert!(!sc.palette.is_empty(), "{id}/{}: palette", sc.id);
            // English texts only; the Russian ones live in the dictionary
            assert!(sc.title.chars().all(|c| !('а'..='я').contains(&c.to_ascii_lowercase())), "{id}/{}: Cyrillic in a key", sc.id);
        }
        // the spec validates and survives a round trip
        let spec = virtlab::builtin(id).expect("builtin");
        spec.validate().unwrap();
        let v = serde_json::to_value(&spec).unwrap();
        assert_eq!(v["sim"], "net_board");
        assert_eq!(serde_json::from_value::<Spec>(v).unwrap(), spec);
        assert_eq!(spec.goals().len(), scenarios.len());
    }
    assert_eq!(pack_ids().len(), 3);
    assert_eq!(pack_chapter("virt-sim-net-bridge"), Some(10));
    assert_eq!(pack_chapter("virt-sim-net-bond"), Some(11));
    assert_eq!(pack_chapter("virt-sim-net-nat"), Some(12));
    assert!(pack("virt-sim-net-nope").is_none());
}

#[test]
fn the_server_check_accepts_references_and_refuses_the_rest() {
    en();
    for id in pack_ids() {
        let spec = virtlab::builtin(id).unwrap();
        let Spec::NetBoard { scenarios, solution } = &spec else { panic!("not a board") };
        let mut submitted = serde_json::Map::new();
        for sc in scenarios {
            submitted.insert(sc.id.clone(), serde_json::to_value(&solution[&sc.id]).unwrap());
        }
        let v = virtlab::verify_with(&spec, &serde_json::Value::Object(submitted), Strictness::Strict);
        assert!(v.solved, "{id}: {:?}", v.goals);
        // the starting boards are refused
        let mut starts = serde_json::Map::new();
        for sc in scenarios {
            starts.insert(sc.id.clone(), serde_json::to_value(&sc.start).unwrap());
        }
        let v = virtlab::verify_with(&spec, &serde_json::Value::Object(starts), Strictness::Strict);
        assert!(!v.solved);
        assert!(v.goals.iter().all(|g| matches!(g.status, GoalStatus::Rejected { .. })), "{id}");
    }
}

#[test]
fn the_judge_gives_the_verdict_of_the_scenario_and_keeps_the_objects() {
    en();
    let (scenarios, solution) = pack("virt-sim-net-nat").unwrap();
    let sc = &scenarios[2];
    let reference = serde_json::to_string(&solution[&sc.id]).unwrap();
    let j = judge("virt-sim-net-nat", &sc.id, &reference).unwrap();
    assert!(j.reached && j.invalid.is_none() && j.goals.iter().all(|g| g.ok));
    let start = serde_json::to_string(&sc.start).unwrap();
    let j = judge("virt-sim-net-nat", &sc.id, &start).unwrap();
    assert!(!j.reached && j.invalid.is_none() && j.goals.iter().any(|g| !g.ok));
    // positionless boards are accepted, other objects are not
    let mut bare = sc.start.clone();
    for n in &mut bare.nodes {
        n.x = 0.0;
        n.y = 0.0;
    }
    assert!(judge("virt-sim-net-nat", &sc.id, &serde_json::to_string(&bare).unwrap()).is_ok());
    let mut more = sc.start.clone();
    more.nodes.push(node(Kind::Veth, "extra"));
    let j = judge("virt-sim-net-nat", &sc.id, &serde_json::to_string(&more).unwrap()).unwrap();
    assert!(!j.reached && j.invalid.is_some());
    assert!(judge("virt-sim-net-nat", "nope", "{}").is_err());
    assert!(judge("virt-sim-net-nat", &sc.id, "[]").is_err());
}

// ---------------------------------------------------------------- rules of links

#[test]
fn links_follow_the_table_and_explain_refusals() {
    en();
    let mut t = Topology::default();
    for (kind, id) in [(Kind::Netns, "h"), (Kind::Netns, "n2"), (Kind::Veth, "a"), (Kind::Veth, "b"), (Kind::Veth, "c"), (Kind::Bridge, "br"), (Kind::Bridge, "br2")] {
        t.nodes.push(node(kind, id));
    }
    t.nodes.push(node(Kind::Eth, "e"));
    t.nodes.push(node(Kind::External, "x"));
    assert!(connect_error(&t, "a", "h").unwrap().contains("not linked directly"));
    assert!(connect_error(&t, "a", "a").unwrap().contains("itself"));
    assert!(connect_error(&t, "nope", "a").unwrap().contains("unknown"));
    assert!(connect_error(&t, "e", "br").is_none());
    // an interface lives in one namespace
    link(&mut t, "h", "a");
    assert_eq!(connect_error(&t, "n2", "a").unwrap(), "an interface lives in one namespace");
    // a veth end has one peer, and the pair is stored once
    link(&mut t, "a", "b");
    assert_eq!(connect_error(&t, "b", "a").unwrap(), "these objects are already linked");
    assert_eq!(connect_error(&t, "a", "c").unwrap(), "a veth end has one peer");
    assert_eq!(connect_error(&t, "c", "b").unwrap(), "a veth end has one peer");
    // one master: a bridge or a bond
    link(&mut t, "a", "br");
    assert_eq!(connect_error(&t, "a", "br2").unwrap(), "an interface is a port of one bridge or a slave of one bond");
    // one cable
    link(&mut t, "e", "x");
    t.nodes.push(node(Kind::External, "y"));
    assert_eq!(connect_error(&t, "e", "y").unwrap(), "a physical interface has one cable");
    // the same namespace for a port and its bridge
    link(&mut t, "h", "br");
    t.nodes.push(node(Kind::Veth, "d"));
    link(&mut t, "n2", "d");
    assert_eq!(connect_error(&t, "d", "br").unwrap(), "a port and its bridge or bond must be in the same namespace");
    // …and for a namespace link added afterwards
    let mut u = Topology::default();
    for (kind, id) in [(Kind::Netns, "h"), (Kind::Netns, "n2"), (Kind::Veth, "a"), (Kind::Bridge, "br")] {
        u.nodes.push(node(kind, id));
    }
    link(&mut u, "h", "br");
    link(&mut u, "a", "br");
    assert!(connect_error(&u, "n2", "a").unwrap().contains("same namespace"));
    assert!(connect_error(&u, "h", "a").is_none());
}

#[test]
fn nat_rules_and_vlan_interfaces_follow_their_rules() {
    en();
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Netns, "h"));
    t.nodes.push(node(Kind::Nat, "m"));
    t.nodes.push(with(node(Kind::Nat, "d"), "kind", "dnat"));
    t.nodes.push(node(Kind::Veth, "v"));
    t.nodes.push(node(Kind::Eth, "e1"));
    t.nodes.push(node(Kind::Eth, "e2"));
    t.nodes.push(node(Kind::Vlan, "v10"));
    assert_eq!(connect_error(&t, "m", "v").unwrap(), "only a DNAT rule forwards to a host");
    assert!(connect_error(&t, "d", "v").is_none());
    link(&mut t, "d", "v");
    t.nodes.push(node(Kind::Vm, "vm"));
    assert_eq!(connect_error(&t, "d", "vm").unwrap(), "a DNAT rule forwards to one host");
    link(&mut t, "m", "h");
    t.nodes.push(node(Kind::Netns, "h2"));
    assert_eq!(connect_error(&t, "m", "h2").unwrap(), "a NAT rule belongs to one namespace");
    link(&mut t, "e1", "v10");
    assert_eq!(connect_error(&t, "e2", "v10").unwrap(), "a VLAN interface has one parent");
    assert!(connect_error(&t, "v10", "e1").unwrap().contains("not linked directly"));
}

#[test]
fn removing_an_object_drops_what_depends_on_it() {
    en();
    let mut t = vm_board(&[("vm1", "0")]);
    t.nodes.retain(|n| n.id != "br0");
    assert!(!problems(&t).is_empty(), "the links to the removed bridge dangle");
    let dropped = prune(&mut t);
    assert_eq!(dropped, 2, "the namespace link and the tap of the VM");
    assert!(problems(&t).is_empty());
}

#[test]
fn problems_catch_a_hand_made_board() {
    en();
    let mut t = vm_board(&[("vm1", "0")]);
    t.nodes.push(node(Kind::Netns, "host"));
    assert!(problems(&t).iter().any(|p| p.edge.is_none() && p.text.contains("unique")));
    let mut t = vm_board(&[("vm1", "0")]);
    t.nodes.push(Node::new("long", Kind::Eth, &"x".repeat(60), 0.0, 0.0));
    assert!(problems(&t).iter().any(|p| p.text.contains("invalid name")));
    let mut t = vm_board(&[("vm1", "0")]);
    t.edges.push(Edge::new("vm1", "ghost"));
    assert!(problems(&t).iter().any(|p| p.edge.is_some() && p.text.contains("unknown")));
    let mut t = vm_board(&[("vm1", "0")]);
    for i in 0..45 {
        t.nodes.push(node(Kind::Vm, &format!("x{i}")));
    }
    assert!(problems(&t).iter().any(|p| p.text.contains("at most")));
    assert!(add_error(&t, Kind::Vm, 24).is_some());
    assert!(add_error(&Topology::default(), Kind::Vm, 24).is_none());
}

#[test]
fn parameters_are_checked_against_the_table() {
    en();
    let mut n = node(Kind::Bond, "b");
    assert!(param_error(&n).is_none());
    n.params.insert("mode".into(), Param::Str("802.3ad".into()));
    assert!(param_error(&n).is_none());
    n.params.insert("mode".into(), Param::Str("round-robin".into()));
    assert!(param_error(&n).unwrap().contains("not a valid value"));
    let mut v = node(Kind::Vlan, "v");
    v.params.insert("id".into(), Param::Str("40".into()));
    assert!(param_error(&v).is_some());
    let mut x = node(Kind::External, "x");
    x.params.insert("forward".into(), Param::Bool(true));
    assert!(param_error(&x).unwrap().contains("not a parameter"));
    // the table and the raw table agree: every default is one of the options
    for kind in Kind::ALL {
        for spec in param_specs(kind) {
            assert!(spec.accepts(&spec.default), "{kind:?}/{}", spec.key);
            let probe = node(kind, "p");
            assert_eq!(probe.param_text(spec.key), spec.default_text(), "{kind:?}/{}", spec.key);
        }
    }
    assert_eq!(node(Kind::Eth, "e").param_text("up"), "true");
    assert_eq!(node(Kind::Netns, "n").param_text("forward"), "false");
    assert_eq!(node(Kind::Veth, "e").access_vlan(), 0);
}

// ---------------------------------------------------------------- link states and addresses

#[test]
fn a_veth_end_has_a_link_only_when_the_pair_is_complete_and_up() {
    en();
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Netns, "h"));
    t.nodes.push(node(Kind::Netns, "n"));
    t.nodes.push(node(Kind::Veth, "a"));
    t.nodes.push(node(Kind::Veth, "b"));
    link(&mut t, "h", "a");
    let ev = evaluate(&t);
    assert_eq!(ev.iface("a").unwrap().why, Some(Why::NoPeer));
    link(&mut t, "a", "b");
    let ev = evaluate(&t);
    assert_eq!(ev.iface("a").unwrap().why, Some(Why::PeerDown), "the peer lives in no namespace");
    link(&mut t, "n", "b");
    assert_eq!(evaluate(&t).iface("a").unwrap().status, IfaceStatus::Ok);
    assert_eq!(evaluate(&t).iface("b").unwrap().status, IfaceStatus::Ok);
    set(&mut t, "b", "up", "false");
    let ev = evaluate(&t);
    assert_eq!(ev.iface("b").unwrap().status, IfaceStatus::Down);
    assert_eq!(ev.iface("a").unwrap().status, IfaceStatus::NoCarrier);
    assert!(Why::PeerDown.text().contains("veth"));
}

#[test]
fn interfaces_without_a_cable_a_namespace_or_a_parent_have_no_link() {
    en();
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Netns, "h"));
    t.nodes.push(node(Kind::Eth, "e"));
    t.nodes.push(node(Kind::External, "x"));
    t.nodes.push(node(Kind::Vlan, "v"));
    t.nodes.push(node(Kind::Bridge, "br"));
    t.nodes.push(node(Kind::Vm, "vm"));
    assert_eq!(evaluate(&t).iface("e").unwrap().why, Some(Why::NoNamespace));
    link(&mut t, "h", "e");
    assert_eq!(evaluate(&t).iface("e").unwrap().why, Some(Why::NoCable));
    link(&mut t, "e", "x");
    assert_eq!(evaluate(&t).iface("e").unwrap().status, IfaceStatus::Ok);
    link(&mut t, "h", "v");
    assert_eq!(evaluate(&t).iface("v").unwrap().why, Some(Why::NoParent));
    link(&mut t, "e", "v");
    assert_eq!(evaluate(&t).iface("v").unwrap().status, IfaceStatus::Ok);
    set(&mut t, "e", "up", "false");
    assert_eq!(evaluate(&t).iface("v").unwrap().why, Some(Why::ParentDown));
    link(&mut t, "h", "br");
    assert_eq!(evaluate(&t).iface("br").unwrap().why, Some(Why::NoPort));
    assert_eq!(evaluate(&t).iface("vm").unwrap().why, Some(Why::NoBridge));
    link(&mut t, "vm", "br");
    assert_eq!(evaluate(&t).iface("vm").unwrap().status, IfaceStatus::Ok);
    assert_eq!(evaluate(&t).iface("br").unwrap().status, IfaceStatus::Ok, "the tap of a VM is a port with a link");
    set(&mut t, "br", "up", "false");
    assert_eq!(evaluate(&t).iface("vm").unwrap().why, Some(Why::BridgeDown));
}

#[test]
fn addresses_are_numbered_by_the_order_of_the_board_and_enslaved_interfaces_have_none() {
    en();
    let mut t = bond_board("active-backup");
    assert_eq!(address(&t, "bond0").as_deref(), Some("10.0.1.1"));
    assert_eq!(address(&t, "sw").as_deref(), Some("10.0.1.254"));
    assert_eq!(address(&t, "eth1"), None, "net none");
    // an address on a slave does not work, the bond holds the address
    set(&mut t, "eth1", "net", "a");
    let ev = evaluate(&t);
    assert!(ev.iface("eth1").unwrap().enslaved);
    assert_eq!(ev.iface("eth1").unwrap().addr, None);
    assert_eq!(ev.iface("bond0").unwrap().addr.as_deref(), Some("10.0.1.1"), "the bond comes first in the order of the board");
    assert_eq!(address(&t, "eth1").as_deref(), Some("10.0.1.2"), "a slave still counts in the numbering, so the addresses do not move when it is enslaved");
    assert_eq!(address(&t, "host"), None);
}

// ---------------------------------------------------------------- reachability

#[test]
fn vlan_tags_on_the_ports_isolate_the_groups() {
    en();
    let t = vm_board(&[("vm1", "0"), ("vm2", "0"), ("vm3", "0")]);
    assert_eq!(reach(&t, "vm1", "vm3"), Reach::Ok);
    let t = vm_board(&[("vm1", "10"), ("vm2", "10"), ("vm3", "20")]);
    assert_eq!(reach(&t, "vm1", "vm2"), Reach::Ok);
    assert_eq!(reach(&t, "vm1", "vm3"), Reach::VlanMismatch);
    assert_eq!(reach(&t, "vm3", "vm1"), Reach::VlanMismatch);
    // an untagged port and a tagged one are different segments too
    let t = vm_board(&[("vm1", "0"), ("vm2", "10")]);
    assert_eq!(reach(&t, "vm1", "vm2"), Reach::VlanMismatch);
    // other networks are not neighbours at all
    let mut t = vm_board(&[("vm1", "0"), ("vm2", "0")]);
    set(&mut t, "vm2", "net", "b");
    assert_eq!(reach(&t, "vm1", "vm2"), Reach::NoRoute);
}

#[test]
fn different_bridges_are_not_connected() {
    en();
    let mut t = vm_board(&[("vm1", "0"), ("vm2", "0")]);
    t.nodes.push(node(Kind::Bridge, "br1"));
    link(&mut t, "host", "br1");
    t.edges.retain(|e| !(e.from == "vm2" && e.to == "br0"));
    link(&mut t, "vm2", "br1");
    assert_eq!(reach(&t, "vm1", "vm2"), Reach::NotConnected);
    // two bridges joined by a veth pair are one segment (the tag of an access port is local to the bridge)
    t.nodes.push(node(Kind::Veth, "p0"));
    t.nodes.push(node(Kind::Veth, "p1"));
    for (ns, v) in [("host", "p0"), ("host", "p1")] {
        link(&mut t, ns, v);
    }
    link(&mut t, "p0", "p1");
    link(&mut t, "p0", "br0");
    link(&mut t, "p1", "br1");
    assert_eq!(reach(&t, "vm1", "vm2"), Reach::Ok);
}

#[test]
fn a_bond_survives_the_loss_of_a_slave_and_a_vlan_needs_the_tag_of_the_switch() {
    en();
    let t = bond_board("active-backup");
    assert_eq!(reach(&t, "host", "sw"), Reach::Ok);
    for lost in ["eth1", "eth2"] {
        let after = t.without(lost);
        assert_eq!(reach(&after, "host", "sw"), Reach::Ok, "{lost} lost");
    }
    let alone = t.without("eth1").without("eth2");
    assert_eq!(reach(&alone, "host", "sw"), Reach::LinkDown, "the bond has an address but no slave with a link");
    assert!(NetGoal::SurviveLoss { node: "eth1".into(), from: "host".into(), to: "sw".into() }.check(&t, &evaluate(&t)));
    // a VLAN interface on the bond talks to a switch that speaks that VLAN only
    let mut v = bond_board("active-backup");
    set(&mut v, "bond0", "net", "none");
    set(&mut v, "sw", "net", "b");
    set(&mut v, "sw", "tagged", "20");
    v.nodes.push(with(with(node(Kind::Vlan, "v20"), "id", "20"), "net", "b"));
    link(&mut v, "host", "v20");
    link(&mut v, "bond0", "v20");
    assert_eq!(reach(&v, "host", "sw"), Reach::Ok);
    set(&mut v, "v20", "id", "10");
    assert_eq!(reach(&v, "host", "sw"), Reach::VlanMismatch);
    // and the untagged interface cannot talk to a tagged switch
    let mut u = bond_board("active-backup");
    set(&mut u, "sw", "tagged", "20");
    assert_eq!(reach(&u, "host", "sw"), Reach::VlanMismatch);
}

#[test]
fn an_lacp_bond_needs_one_switch() {
    en();
    let mut t = bond_board("802.3ad");
    assert_eq!(reach(&t, "host", "sw"), Reach::Ok);
    t.nodes.push(node(Kind::External, "sw2"));
    t.edges.retain(|e| !(e.from == "eth2" && e.to == "sw"));
    link(&mut t, "eth2", "sw2");
    let ev = evaluate(&t);
    assert_eq!(ev.iface("bond0").unwrap().why, Some(Why::LacpMismatch));
    assert_eq!(reach(&t, "host", "sw"), Reach::LinkDown);
    set(&mut t, "bond0", "mode", "active-backup");
    assert_eq!(reach(&t, "host", "sw"), Reach::Ok, "active-backup does not need one switch");
}

#[test]
fn a_gateway_needs_forwarding_a_route_and_masquerade() {
    en();
    let t = nat_board();
    assert_eq!(reach(&t, "ns1", "host"), Reach::Ok);
    assert_eq!(reach(&t, "ns1", "net"), Reach::Ok);
    assert_eq!(reach(&t, "host", "net"), Reach::Ok, "the uplink is in the network of the outside");
    // forwarding off
    let mut f = t.clone();
    set(&mut f, "host", "forward", "false");
    assert_eq!(reach(&f, "ns1", "net"), Reach::ForwardOff);
    assert_eq!(reach(&f, "ns1", "host"), Reach::Ok, "the host answers for its own addresses");
    // no masquerade
    let m = t.without("masq");
    assert_eq!(reach(&m, "ns1", "net"), Reach::NoNat);
    // no default route
    let mut d = t.clone();
    set(&mut d, "v1c", "default_route", "false");
    assert_eq!(reach(&d, "ns1", "net"), Reach::NoRoute);
    // the veth peer missing
    let p = t.without("v1h");
    assert_eq!(reach(&p, "ns1", "host"), Reach::LinkDown);
    // the container end without an address
    let mut a = t.clone();
    set(&mut a, "v1c", "net", "none");
    assert_eq!(reach(&a, "ns1", "host"), Reach::NoAddress);
    // the outside cannot route inwards
    assert_eq!(reach(&t, "net", "ns1"), Reach::NoRoute);
    // forwarding on, but the gateway has no leg into the destination network
    let mut e = t.clone();
    set(&mut e, "eth0", "net", "c");
    assert_eq!(reach(&e, "ns1", "net"), Reach::NoRoute);
}

#[test]
fn a_dnat_rule_publishes_a_host_inside() {
    en();
    let mut t = nat_board();
    let ev = evaluate(&t);
    assert_eq!(published(&t, &ev, "net", "v1c"), Reach::NoNat, "no DNAT rule yet");
    t.nodes.push(with(node(Kind::Nat, "dnat"), "kind", "dnat"));
    link(&mut t, "dnat", "host");
    link(&mut t, "dnat", "v1c");
    let ev = evaluate(&t);
    assert_eq!(published(&t, &ev, "net", "v1c"), Reach::Ok);
    assert!(NetGoal::Published { external: "net".into(), target: "v1c".into() }.check(&t, &ev));
    // forwarding off: the connection stops at the router
    set(&mut t, "host", "forward", "false");
    assert_eq!(published(&t, &evaluate(&t), "net", "v1c"), Reach::ForwardOff);
    // the target cannot answer: no default route in the container
    set(&mut t, "host", "forward", "true");
    set(&mut t, "v1c", "default_route", "false");
    assert_eq!(published(&t, &evaluate(&t), "net", "v1c"), Reach::NoRoute);
}

// ---------------------------------------------------------------- trace

#[test]
fn the_trace_follows_the_packet_and_stops_where_it_breaks() {
    en();
    let t = nat_board();
    let ev = evaluate(&t);
    let tr = trace(&t, &ev, &Op::Ping { from: "ns1".into(), to: "net".into() });
    assert!(tr.ok);
    assert_eq!(tr.hops.len(), 3);
    assert!(tr.hops[0].text.contains("default gateway"));
    assert!(tr.hops[1].text.contains("masq"), "{}", tr.hops[1].text);
    assert!(tr.hops[0].links.iter().any(|(a, b)| a == "v1h" && b == "v1c" || a == "v1c" && b == "v1h" || a == "v1h" && b == "br0"));
    // direct
    let tr = trace(&t, &ev, &Op::Ping { from: "ns1".into(), to: "host".into() });
    assert!(tr.ok && tr.hops.len() == 1 && tr.hops[0].text.contains("straight"));
    // forwarding off: the first step works, the second breaks
    let mut f = t.clone();
    set(&mut f, "host", "forward", "false");
    let tr = trace(&f, &evaluate(&f), &Op::Ping { from: "ns1".into(), to: "net".into() });
    assert!(!tr.ok);
    assert_eq!(tr.hops.iter().map(|h| h.ok).collect::<Vec<_>>(), [true, false]);
    assert!(tr.hops[1].text.contains("ip_forward"));
    // no route: one failing step
    let mut d = t.clone();
    set(&mut d, "v1c", "default_route", "false");
    let tr = trace(&d, &evaluate(&d), &Op::Ping { from: "ns1".into(), to: "net".into() });
    assert!(!tr.ok && tr.hops.len() == 1 && !tr.hops[0].ok);
    // publishing
    let mut p = t.clone();
    p.nodes.push(with(node(Kind::Nat, "dnat"), "kind", "dnat"));
    link(&mut p, "dnat", "host");
    link(&mut p, "dnat", "v1c");
    let tr = trace(&p, &evaluate(&p), &Op::Publish { external: "net".into(), target: "v1c".into() });
    assert!(tr.ok && tr.hops.len() == 3);
    let tr = trace(&t, &ev, &Op::Publish { external: "net".into(), target: "v1c".into() });
    assert!(!tr.ok && tr.hops.len() == 1);
}

// ---------------------------------------------------------------- goals, palette, layout

#[test]
fn goals_read_the_board() {
    en();
    let t = vm_board(&[("vm1", "10"), ("vm2", "20")]);
    let ev = evaluate(&t);
    let g = |g: NetGoal| g.check(&t, &ev);
    assert!(g(NetGoal::NoPing { from: "vm1".into(), to: "vm2".into() }));
    assert!(!g(NetGoal::Ping { from: "vm1".into(), to: "vm2".into() }));
    assert!(g(NetGoal::Healthy));
    assert!(g(NetGoal::Has { node: Kind::Vm, min: 2 }) && !g(NetGoal::Has { node: Kind::Vm, min: 3 }));
    assert!(g(NetGoal::AtMost { node: Kind::Vm, max: 2 }) && !g(NetGoal::AtMost { node: Kind::Vm, max: 1 }));
    assert!(g(NetGoal::Lacks { node: Kind::Bond }));
    assert!(g(NetGoal::ParamOf { id: "vm1".into(), key: "access_vlan".into(), value: "10".into() }));
    assert!(g(NetGoal::ParamOf { id: "vm1".into(), key: "up".into(), value: "true".into() }), "the default counts");
    assert!(g(NetGoal::Linked { from: "vm1".into(), to: "br0".into() }));
    let mut sick = t.clone();
    set(&mut sick, "vm1", "up", "false");
    assert!(!NetGoal::Healthy.check(&sick, &evaluate(&sick)));
    assert!(!NetGoal::Healthy.check(&Topology::default(), &evaluate(&Topology::default())));
}

#[test]
fn goal_texts_name_the_objects() {
    en();
    let mut t = Topology::default();
    t.nodes.push(Node::new("vm1", Kind::Vm, "web server", 0.0, 0.0));
    t.nodes.push(Node::new("sw", Kind::External, "switch", 0.0, 0.0));
    let text = NetGoal::Ping { from: "vm1".into(), to: "sw".into() }.describe_for(&t);
    assert_eq!(text, "“web server” can ping “switch”");
    assert!(NetGoal::SurviveLoss { node: "eth1".into(), from: "vm1".into(), to: "sw".into() }.describe_for(&t).contains("eth1"));
    assert!(NetGoal::Healthy.describe().contains("link"));
}

#[test]
fn a_scenario_refuses_what_is_not_in_the_palette() {
    en();
    let (scenarios, solution) = pack("virt-sim-net-bridge").unwrap();
    let sc = &scenarios[0];
    let mut t = solution[&sc.id].clone();
    assert!(sc.invalid(&t).is_none());
    t.nodes.push(node(Kind::Bond, "bond"));
    assert!(sc.invalid(&t).unwrap().contains("not available"));
    let mut many = solution[&sc.id].clone();
    for i in 0..30 {
        many.nodes.push(node(Kind::Bridge, &format!("x{i}")));
    }
    assert!(sc.invalid(&many).unwrap().contains("at most"));
}

#[test]
fn boards_without_positions_are_laid_out_in_columns() {
    en();
    let mut t = nat_board();
    auto_layout(&mut t);
    for (i, a) in t.nodes.iter().enumerate() {
        for n in &t.nodes[i + 1..] {
            assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
        }
    }
    let x = |id: &str| t.node(id).unwrap().x;
    assert!(x("net") < x("eth0") && x("eth0") < x("br0") && x("br0") < x("v1h") && x("v1h") < x("host") && x("host") < x("masq"));
}

#[test]
fn boards_round_trip_through_json_with_defaults_omitted() {
    en();
    for (sc, reference) in all() {
        let text = serde_json::to_string(&reference).unwrap();
        let back: Topology = serde_json::from_str(&text).unwrap();
        assert_eq!(back, reference, "{}", sc.id);
        let s = serde_json::to_string(&sc).unwrap();
        assert_eq!(serde_json::from_str::<Scenario>(&s).unwrap(), sc);
    }
}
