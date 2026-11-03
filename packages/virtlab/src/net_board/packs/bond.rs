//! Chapter 11: bonds, the loss of a NIC, LACP, VLANs on a bond.

use std::collections::BTreeMap;

use super::super::{Kind, NetGoal, Scenario, Topology};
use super::builder::*;

fn ping(from: &str, to: &str) -> NetGoal {
    NetGoal::Ping { from: s(from), to: s(to) }
}

fn survive(node: &str, from: &str, to: &str) -> NetGoal {
    NetGoal::SurviveLoss { node: s(node), from: s(from), to: s(to) }
}

/// Scenarios of the pack "bond" (chapter 11) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    // two NICs cabled to a switch
    let mut nics = B::default();
    nics.ns("host", "host", false).ext("sw", "switch", "a", 0);
    nics.eth("eth1", "eth1", "host", "none", "sw").eth("eth2", "eth2", "host", "none", "sw");
    let build_bond = Scenario {
        id: s("build-bond"),
        title: s("A bond of two NICs"),
        story: s("The server has two NICs, both cabled to the same switch, but each is a single point of failure. Make a bond of them, give the address to the bond, and the server must keep talking to the switch when either NIC is lost."),
        goal: s("The host pings the switch, and survives the loss of either NIC"),
        hint: s("A bond is an object of the host. The NICs become its slaves and give up their own addresses: the address belongs to the bond."),
        palette: vec![Kind::Bond],
        max_nodes: 8,
        start: nics.done(),
        goals: vec![ping("host", "sw"), survive("eth1", "host", "sw"), survive("eth2", "host", "sw"), NetGoal::Has { node: Kind::Bond, min: 1 }],
    };
    let mut build_ref = nics.clone();
    build_ref.bond("bond0", "bond0", "host", "active-backup", "a").link(&[("eth1", "bond0"), ("eth2", "bond0")]);

    // a bond with one slave
    let mut one = B::default();
    one.ns("host", "host", false).ext("sw", "switch", "a", 0);
    one.eth("eth1", "eth1", "host", "none", "sw").eth("eth2", "eth2", "host", "none", "sw");
    one.bond("bond0", "bond0", "host", "active-backup", "a").link(&[("eth1", "bond0")]);
    let one_slave = Scenario {
        id: s("one-slave"),
        title: s("A bond that survives nothing"),
        story: s("The bond works, but only eth1 is its slave: eth2 is cabled and idle. When eth1 dies, the server is cut off. A bond is a protection only with at least two slaves."),
        goal: s("The host survives the loss of eth1 and the loss of eth2"),
        hint: s("Make eth2 a slave of the bond as well."),
        palette: vec![Kind::Eth],
        max_nodes: 8,
        start: one.done(),
        goals: vec![ping("host", "sw"), survive("eth1", "host", "sw"), survive("eth2", "host", "sw")],
    };
    let mut one_ref = one.clone();
    one_ref.link(&[("eth2", "bond0")]);

    // a VLAN on the bond
    let mut trunk = B::default();
    trunk.ns("host", "host", false).ext("sw", "switch VLAN 20", "b", 20);
    trunk.eth("eth1", "eth1", "host", "none", "sw").eth("eth2", "eth2", "host", "none", "sw");
    trunk.bond("bond0", "bond0", "host", "active-backup", "none").link(&[("eth1", "bond0"), ("eth2", "bond0")]);
    let vlan_on_bond = Scenario {
        id: s("vlan-on-bond"),
        title: s("A VLAN on top of the bond"),
        story: s("The switch ports are trunk ports: the management network 10.0.2.0/24 travels tagged with VLAN 20, nothing travels untagged. The bond is up, but the host has no address in the management network. Add a VLAN interface on the bond."),
        goal: s("The host pings the switch through a VLAN interface of VLAN 20 on the bond"),
        hint: s("A VLAN interface is an object of the host with the bond as its parent. Choose the VLAN id of the switch, and give the interface the address."),
        palette: vec![Kind::Vlan],
        max_nodes: 8,
        start: trunk.done(),
        goals: vec![ping("host", "sw"), NetGoal::Has { node: Kind::Vlan, min: 1 }, NetGoal::Healthy],
    };
    let mut trunk_ref = trunk.clone();
    trunk_ref.vlan("bond0-20", "bond0.20", "host", "bond0", 20, "b");

    // a slave that is down
    let mut sick = B::default();
    sick.ns("host", "host", false).ext("sw", "switch", "a", 0);
    sick.eth("eth1", "eth1", "host", "none", "sw").eth("eth2", "eth2", "host", "none", "sw");
    sick.bond("bond0", "bond0", "host", "active-backup", "a").link(&[("eth1", "bond0"), ("eth2", "bond0")]);
    sick.param("eth1", "up", "false");
    let down_slave = Scenario {
        id: s("down-slave"),
        title: s("A slave that nobody noticed"),
        story: s("The server talks to the switch, so nobody looked at the bond. But eth1 is down since the last maintenance, and the bond runs on eth2 alone: the loss of eth2 would cut the server off."),
        goal: s("Both slaves are up, and the host survives the loss of either NIC"),
        hint: s("Check the state of every interface, not only of the bond."),
        palette: vec![Kind::Eth],
        max_nodes: 8,
        start: sick.done(),
        goals: vec![ping("host", "sw"), survive("eth1", "host", "sw"), survive("eth2", "host", "sw"), NetGoal::Healthy],
    };
    let mut sick_ref = sick.clone();
    sick_ref.param("eth1", "up", "true");

    // LACP and two switches
    let mut lacp = B::default();
    lacp.ns("host", "host", false).ext("sw1", "switch 1", "a", 0).ext("sw2", "switch 2", "a", 0);
    lacp.eth("eth1", "eth1", "host", "none", "sw1").eth("eth2", "eth2", "host", "none", "sw2");
    lacp.bond("bond0", "bond0", "host", "802.3ad", "a").link(&[("eth1", "bond0"), ("eth2", "bond0")]);
    let lacp_switch = Scenario {
        id: s("lacp-switch"),
        title: s("LACP and two switches"),
        story: s("The bond works in the 802.3ad mode, but the two NICs were cabled to two different switches, and the partner of an LACP aggregate is a single device. The bond has no link at all. Move one cable (or choose a mode that does not need one switch)."),
        goal: s("The host pings switch 1 and survives the loss of either NIC"),
        hint: s("Both slaves of an 802.3ad bond must be cabled to the same switch. One NIC has one cable: remove the old one before you add the new one."),
        palette: vec![Kind::External],
        max_nodes: 8,
        start: lacp.done(),
        goals: vec![ping("host", "sw1"), survive("eth1", "host", "sw1"), survive("eth2", "host", "sw1"), NetGoal::Healthy],
    };
    let mut lacp_ref = lacp.clone();
    lacp_ref.unlink("eth2", "sw2").link(&[("eth2", "sw1")]);

    // a bond under a bridge
    let mut under = B::default();
    under.ns("host", "host", false).ext("sw", "switch", "a", 0);
    under.eth("eth1", "eth1", "host", "none", "sw").eth("eth2", "eth2", "host", "none", "sw");
    under.bond("bond0", "bond0", "host", "active-backup", "none").link(&[("eth1", "bond0"), ("eth2", "bond0")]);
    under.bridge("br0", "br0", "host", "none").vm("vm1", "vm1", "br0", "a", 0);
    under.param("br0", "up", "false");
    let bond_bridge = Scenario {
        id: s("bond-bridge"),
        title: s("A bridge on a bond for the VMs"),
        story: s("The VMs get their network from the bridge br0, and the bridge should reach the switch through the bond: this is how a hypervisor host usually does it. Today vm1 is cut off: the bridge is down and the bond is not one of its ports."),
        goal: s("vm1 pings the switch through br0 and the bond, and survives the loss of either NIC"),
        hint: s("The bond is a port of the bridge. Bring the bridge up too: a VM whose bridge is down has no link."),
        palette: vec![Kind::Vm],
        max_nodes: 10,
        start: under.done(),
        goals: vec![ping("vm1", "sw"), survive("eth1", "vm1", "sw"), survive("eth2", "vm1", "sw"), NetGoal::Healthy],
    };
    let mut under_ref = under.clone();
    under_ref.param("br0", "up", "true").link(&[("bond0", "br0")]);

    let mut solution = BTreeMap::new();
    solution.insert(s("build-bond"), build_ref.done());
    solution.insert(s("one-slave"), one_ref.done());
    solution.insert(s("vlan-on-bond"), trunk_ref.done());
    solution.insert(s("down-slave"), sick_ref.done());
    solution.insert(s("lacp-switch"), lacp_ref.done());
    solution.insert(s("bond-bridge"), under_ref.done());
    (vec![build_bond, one_slave, vlan_on_bond, down_slave, lacp_switch, bond_bridge], solution)
}
