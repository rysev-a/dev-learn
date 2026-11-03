//! Chapter 12: a container network by hand: a namespace, a veth pair, a bridge, forwarding, masquerade, a published port.

use std::collections::BTreeMap;

use super::super::{Kind, NetGoal, Scenario, Topology};
use super::builder::*;

fn ping(from: &str, to: &str) -> NetGoal {
    NetGoal::Ping { from: s(from), to: s(to) }
}

/// The host with its uplink and the container namespace, nothing between them yet.
fn uplink() -> B {
    let mut b = B::default();
    b.ns("host", "host", false).ns("ns1", "ns1", false).ext("net", "internet", "a", 0);
    b.eth("eth0", "eth0", "host", "a", "net");
    b
}

/// The whole container network except what the scenario leaves out.
fn complete(forward: bool, default_route: bool, masquerade: bool) -> B {
    let mut b = uplink();
    b.bridge("br0", "br0", "host", "b");
    b.veth("v1h", "veth1-host", "host", "none").veth("v1c", "veth1-ns1", "ns1", "b").link(&[("v1h", "v1c"), ("v1h", "br0")]);
    b.param("host", "forward", if forward { "true" } else { "false" });
    b.param("v1c", "default_route", if default_route { "true" } else { "false" });
    if masquerade {
        b.nat("masq", "masquerade", "host", "masquerade");
    }
    b
}

/// Scenarios of the pack "nat" (chapter 12) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let start = uplink();
    let build = Scenario {
        id: s("build"),
        title: s("A container network from nothing"),
        story: s("The host has an uplink eth0 to the internet. The namespace ns1 is empty. Build what Docker builds for a container: a veth pair, a bridge with the address 10.0.2.x of the container network, the address and the default route in the container, forwarding in the host and a masquerade rule."),
        goal: s("ns1 pings the host and the internet, and every interface has a link"),
        hint: s("Work from the container outwards: the container end gets an address of the container network and the default route, the host end becomes a port of the bridge, the bridge holds the gateway address. Then the host must forward packets and replace the source address."),
        palette: vec![Kind::Veth, Kind::Bridge, Kind::Nat],
        max_nodes: 14,
        start: start.done(),
        goals: vec![ping("ns1", "host"), ping("ns1", "net"), NetGoal::Healthy],
    };
    let build_ref = complete(true, true, true);

    let no_masq = complete(true, true, false);
    let no_nat = Scenario {
        id: s("no-masquerade"),
        title: s("The packets leave but nothing comes back"),
        story: s("The container reaches the host, forwarding is on, the default route is there, but the ping to the internet gets no answer. The outside network knows nothing about the private network 10.0.2.0/24 and cannot send the reply back."),
        goal: s("ns1 pings the internet"),
        hint: s("The router must replace the private source address with its own. That is a rule of the host."),
        palette: vec![Kind::Nat],
        max_nodes: 14,
        start: no_masq.done(),
        goals: vec![ping("ns1", "host"), ping("ns1", "net"), NetGoal::Healthy],
    };
    let mut no_masq_ref = no_masq.clone();
    no_masq_ref.nat("masq", "masquerade", "host", "masquerade");

    let no_forward = complete(false, true, true);
    let forward_off = Scenario {
        id: s("forward-off"),
        title: s("The host does not forward"),
        story: s("The container reaches the host and the rule of masquerade is in place, but nothing goes further. The host answers its own packets and drops the packets that are not for it: forwarding between its interfaces is off."),
        goal: s("ns1 pings the internet"),
        hint: s("The setting is a parameter of the namespace of the host (net.ipv4.ip_forward)."),
        palette: vec![Kind::Nat],
        max_nodes: 14,
        start: no_forward.done(),
        goals: vec![ping("ns1", "host"), ping("ns1", "net"), NetGoal::Healthy],
    };
    let mut no_forward_ref = no_forward.clone();
    no_forward_ref.param("host", "forward", "true");

    let no_route = complete(true, false, true);
    let no_default = Scenario {
        id: s("no-default-route"),
        title: s("The container does not know the way out"),
        story: s("The container reaches the host by its address in the container network, but a ping to the internet fails at once: the container has no default route, so it does not know where to send packets for other networks."),
        goal: s("ns1 pings the internet"),
        hint: s("The default route of the container goes out of its only interface."),
        palette: vec![Kind::Nat],
        max_nodes: 14,
        start: no_route.done(),
        goals: vec![ping("ns1", "host"), ping("ns1", "net"), NetGoal::Healthy],
    };
    let mut no_route_ref = no_route.clone();
    no_route_ref.param("v1c", "default_route", "true");

    let working = complete(true, true, true);
    let publish = Scenario {
        id: s("publish"),
        title: s("Publish a port"),
        story: s("The container reaches the internet, but a web server in the container must be reachable from the internet through the address of the host (what docker run -p does). Add a DNAT rule to the host that forwards the connection to the container."),
        goal: s("The internet reaches the published port of the container, and the container still reaches the internet"),
        hint: s("A DNAT rule belongs to the namespace of the host and forwards to the container end of the veth pair. Choose the kind of the rule: the masquerade rule that is already there does not publish anything."),
        palette: vec![Kind::Nat],
        max_nodes: 14,
        start: working.done(),
        goals: vec![ping("ns1", "net"), NetGoal::Published { external: s("net"), target: s("v1c") }, NetGoal::Healthy],
    };
    let mut publish_ref = working.clone();
    publish_ref.nat("dnat", "DNAT port 80", "host", "dnat").link(&[("dnat", "v1c")]);

    let mut solution = BTreeMap::new();
    solution.insert(s("build"), build_ref.done());
    solution.insert(s("no-masquerade"), no_masq_ref.done());
    solution.insert(s("forward-off"), no_forward_ref.done());
    solution.insert(s("no-default-route"), no_route_ref.done());
    solution.insert(s("publish"), publish_ref.done());
    (vec![build, no_nat, forward_off, no_default, publish], solution)
}
