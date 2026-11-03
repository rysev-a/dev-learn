//! Chapter 10: a bridge, veth pairs, VLAN tags on the ports.

use std::collections::BTreeMap;

use super::super::{Kind, NetGoal, Scenario, Topology};
use super::builder::*;

fn ping(from: &str, to: &str) -> NetGoal {
    NetGoal::Ping { from: s(from), to: s(to) }
}

fn no_ping(from: &str, to: &str) -> NetGoal {
    NetGoal::NoPing { from: s(from), to: s(to) }
}

/// Scenarios of the pack "bridge" (chapter 10) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    // two containers on veth pairs: the host ends wait for a bridge
    let mut pairs = B::default();
    pairs.ns("host", "host", false).ns("ns1", "ns1", false).ns("ns2", "ns2", false);
    pairs.veth("v1h", "veth1-host", "host", "none").veth("v1c", "veth1-ns1", "ns1", "a").link(&[("v1h", "v1c")]);
    pairs.veth("v2h", "veth2-host", "host", "none").veth("v2c", "veth2-ns2", "ns2", "a").link(&[("v2h", "v2c")]);
    let two_ns = Scenario {
        id: s("two-namespaces"),
        title: s("A bridge for two namespaces"),
        story: s("Two containers, ns1 and ns2, are connected to the host with veth pairs and have addresses in the same network. The host ends of the pairs lead nowhere: the containers cannot see each other. Put a bridge in the host and make the host ends its ports."),
        goal: s("ns1 and ns2 ping each other through a bridge in the host"),
        hint: s("A bridge is an object of the namespace it works in: link the host to it, then link both host ends of the veth pairs to the bridge as ports."),
        palette: vec![Kind::Bridge],
        max_nodes: 12,
        start: pairs.done(),
        goals: vec![ping("ns1", "ns2"), NetGoal::Has { node: Kind::Bridge, min: 1 }, NetGoal::Healthy],
    };
    let mut two_ns_ref = pairs.clone();
    two_ns_ref.bridge("br0", "br0", "host", "none").link(&[("v1h", "br0"), ("v2h", "br0")]);

    // four VMs on one bridge, two groups
    let mut four = B::default();
    four.ns("host", "host", false).bridge("br0", "br0", "host", "none");
    four.vm("vm1", "vm1", "br0", "a", 0).vm("vm2", "vm2", "br0", "a", 0).vm("vm3", "vm3", "br0", "a", 0).vm("vm4", "vm4", "br0", "a", 0);
    let vlans = Scenario {
        id: s("two-groups"),
        title: s("Two groups on one bridge"),
        story: s("Four VMs are plugged into one bridge. vm1 and vm2 belong to the shop, vm3 and vm4 to the office: the two groups must not see each other. The bridge is VLAN-aware: every port puts its own VLAN tag on the frames."),
        goal: s("vm1 and vm2 see each other, vm3 and vm4 see each other, the groups are isolated"),
        hint: s("Give the ports of the shop one VLAN tag and the ports of the office another one. Ports with different tags are different segments."),
        palette: vec![Kind::Vm],
        max_nodes: 10,
        start: four.done(),
        goals: vec![ping("vm1", "vm2"), ping("vm3", "vm4"), no_ping("vm1", "vm3"), no_ping("vm2", "vm4"), NetGoal::Healthy],
    };
    let mut vlans_ref = four.clone();
    vlans_ref.param("vm1", "access_vlan", "10").param("vm2", "access_vlan", "10").param("vm3", "access_vlan", "20").param("vm4", "access_vlan", "20");

    // one port in the wrong VLAN
    let mut odd = B::default();
    odd.ns("host", "host", false).bridge("br0", "br0", "host", "none");
    odd.vm("vm1", "vm1", "br0", "a", 10).vm("vm2", "vm2", "br0", "a", 10).vm("vm3", "vm3", "br0", "a", 20).vm("vm4", "vm4", "br0", "a", 20);
    let wrong_vlan = Scenario {
        id: s("wrong-vlan"),
        title: s("A port in the wrong VLAN"),
        story: s("The shop is vm1, vm2 and vm3 (VLAN 10), the office is vm4 (VLAN 20). vm3 cannot reach the rest of the shop: its port was given the tag of the office."),
        goal: s("vm3 joins the shop, and the office stays isolated"),
        hint: s("Look at the VLAN tag of the port of vm3. Do not simply remove the tags: vm4 must stay isolated."),
        palette: vec![Kind::Vm],
        max_nodes: 10,
        start: odd.done(),
        goals: vec![ping("vm1", "vm2"), ping("vm1", "vm3"), no_ping("vm1", "vm4"), NetGoal::Healthy],
    };
    let mut odd_ref = odd.clone();
    odd_ref.param("vm3", "access_vlan", "10");

    // a VM on the wrong bridge
    let mut two_br = B::default();
    two_br.ns("host", "host", false).bridge("br0", "br0", "host", "none").bridge("br1", "br1", "host", "none");
    two_br.vm("vm1", "vm1", "br0", "a", 0).vm("vm2", "vm2", "br0", "a", 0).vm("vm3", "vm3", "br1", "a", 0).vm("vm4", "vm4", "br1", "a", 0);
    let wrong_bridge = Scenario {
        id: s("wrong-bridge"),
        title: s("The tap on the wrong bridge"),
        story: s("The host has two bridges, br0 for the production VMs and br1 for the test VMs. vm3 is a production machine, but its tap was plugged into the test bridge, so vm1 and vm2 cannot see it."),
        goal: s("vm3 is on the production bridge with vm1 and vm2, and the test bridge stays separate"),
        hint: s("A tap is a port of exactly one bridge: remove the link to br1 and link the VM to br0."),
        palette: vec![Kind::Vm],
        max_nodes: 12,
        start: two_br.done(),
        goals: vec![ping("vm1", "vm3"), ping("vm3", "vm2"), no_ping("vm1", "vm4"), NetGoal::Healthy],
    };
    let mut two_br_ref = two_br.clone();
    two_br_ref.unlink("vm3", "br1").link(&[("vm3", "br0")]);

    // a veth end that is down
    let mut down = B::default();
    down.ns("host", "host", false).ns("ns1", "ns1", false).bridge("br0", "br0", "host", "a");
    down.veth("v1h", "veth1-host", "host", "none").veth("v1c", "veth1-ns1", "ns1", "a").link(&[("v1h", "v1c"), ("v1h", "br0")]);
    down.param("v1c", "up", "false");
    let link_down = Scenario {
        id: s("link-down"),
        title: s("The container has no link"),
        story: s("The container ns1 should reach the host through the address of the bridge br0, but the ping fails and the bridge has no carrier. A veth end has a link only when both ends of the pair are up."),
        goal: s("ns1 pings the host, and every interface has a link"),
        hint: s("Look at the state of every interface on the board: the container end of the pair is down, and that takes the host end and the bridge down with it."),
        palette: vec![Kind::Veth],
        max_nodes: 8,
        start: down.done(),
        goals: vec![ping("ns1", "host"), NetGoal::Healthy],
    };
    let mut down_ref = down.clone();
    down_ref.param("v1c", "up", "true");

    let mut solution = BTreeMap::new();
    solution.insert(s("two-namespaces"), two_ns_ref.done());
    solution.insert(s("two-groups"), vlans_ref.done());
    solution.insert(s("wrong-vlan"), odd_ref.done());
    solution.insert(s("wrong-bridge"), two_br_ref.done());
    solution.insert(s("link-down"), down_ref.done());
    (vec![two_ns, vlans, wrong_vlan, wrong_bridge, link_down], solution)
}
