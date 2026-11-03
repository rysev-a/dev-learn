//! Chapter 24: disaster recovery. A replica of a storage domain in another data center is what survives the loss of a site, but only an Active one:
//! an Up host of the other data center must see it. Five boards: the first replica, a replica in an empty site, two sites replicating to each other,
//! a VM with two disk domains and a copy that sits in the same site as the original.

use std::collections::BTreeMap;

#[allow(unused_imports)]
use super::super::{DomainType, Kind, OpKind, Rel, Role, Scenario, TopoGoal, Topology};
#[allow(unused_imports)]
use super::builder::*;

/// The scenarios of the pack and the reference boards by scenario identifier.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let mut scenarios = vec![];
    let mut solution = BTreeMap::new();
    for (sc, fixed) in [first_replica(), empty_site(), both_ways(), one_of_two(), same_site()] {
        solution.insert(sc.id.clone(), fixed);
        scenarios.push(sc);
    }
    (scenarios, solution)
}

/// One engine and two data centers (`dc1`, `dc2`) with a cluster, the management network and the given hosts each (`h1`, `h2`, … by identifier).
/// There is no storage yet.
fn two_sites(names: (&str, &str), hosts1: &[&str], hosts2: &[&str]) -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, names.0)
        .add("dc2", Kind::DataCenter, names.1)
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "ovirtmgmt-2", Role::Management)
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("dc2", "mgmt2"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt2"),
        ]);
    for (hosts, cl, net) in [(hosts1, "cl1", "mgmt"), (hosts2, "cl2", "mgmt2")] {
        for h in hosts {
            b.host(h, &format!("host-{}", &h[1..]), 32).link(&[(cl, h), (net, h)]);
        }
    }
    b
}

/// A domain attached to a data center and seen by the given hosts.
fn storage(b: &mut B, dc: &str, id: &str, name: &str, hosts: &[&str]) {
    b.domain(id, name, DomainType::Nfs).link(&[(dc, id)]);
    for h in hosts {
        b.link(&[(id, h)]);
    }
}

/// A VM on a host with the disks on the given domains.
fn put_vm(b: &mut B, id: &str, name: &str, host: &str, disks: &[&str]) {
    b.vm(id, name, 4, false).link(&[(host, id)]);
    for d in disks {
        b.link(&[(d, id)]);
    }
}

fn drop_edges(t: &mut Topology, gone: &[(&str, &str)]) {
    t.edges.retain(|e| !gone.iter().any(|(a, b)| e.from == *a && e.to == *b));
}

/// The Recovery data center has a host and no storage at all: nothing to receive a replica.
fn first_replica() -> (Scenario, Topology) {
    let mut b = two_sites(("Default", "Recovery"), &["h1", "h2"], &["h3"]);
    storage(&mut b, "dc1", "nfs", "nfs-prod", &["h1", "h2"]);
    put_vm(&mut b, "vm1", "web-1", "h1", &["nfs"]);
    put_vm(&mut b, "vm2", "db-1", "h2", &["nfs"]);
    let start = b.done();
    storage(&mut b, "dc2", "dr", "nfs-dr", &["h3"]);
    b.replica("nfs", "dr");
    let sc = Scenario {
        id: s("first-replica"),
        title: s("A copy in the other data center"),
        story: s("All production VMs keep their disks on nfs-prod in the Default data center. The Recovery data center has a host and nothing else, and losing the Default site would lose every disk."),
        goal: s("Every VM disk has a replica that is Active in the Recovery data center, and both data centers are Up"),
        hint: s("A replica is a storage domain of its own in the other data center. The hosts there must see it, or it stays Inactive."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 16,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::Link { rel: Rel::Replica, min: 1 },
            TopoGoal::SurviveSiteLoss,
        ],
    };
    (sc, b.done())
}

/// The replica is configured and attached, but its data center has no host: the replica stays Inactive.
fn empty_site() -> (Scenario, Topology) {
    let mut b = two_sites(("Default", "Recovery"), &["h1", "h2"], &[]);
    storage(&mut b, "dc1", "nfs", "nfs-prod", &["h1", "h2"]);
    storage(&mut b, "dc2", "dr", "nfs-dr", &[]);
    b.replica("nfs", "dr");
    put_vm(&mut b, "vm1", "web-1", "h1", &["nfs"]);
    put_vm(&mut b, "vm2", "db-1", "h2", &["nfs"]);
    let start = b.done();
    b.host("h3", "host-3", 32).link(&[("cl2", "h3"), ("mgmt2", "h3"), ("dr", "h3")]);
    let sc = Scenario {
        id: s("empty-site"),
        title: s("A replica nobody can open"),
        story: s("nfs-dr is configured as the replica of nfs-prod and attached to the Recovery data center, but the drill shows it Inactive and the Recovery data center is not Up."),
        goal: s("The replica is Active in an Up Recovery data center, so the production disks survive the loss of the Default site"),
        hint: s("A domain is Active only while an Up host of its data center sees it. Look at what the Recovery data center has."),
        palette: vec![Kind::Host],
        max_nodes: 15,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::HostsUp { min: 3 },
            TopoGoal::SurviveSiteLoss,
        ],
    };
    (sc, b.done())
}

/// Active-active: both sites run VMs and each site holds a spare domain for the other one's copy; the pairing has to cross the border.
fn both_ways() -> (Scenario, Topology) {
    let mut b = two_sites(("East", "West"), &["h1"], &["h2"]);
    storage(&mut b, "dc1", "east", "east-data", &["h1"]);
    storage(&mut b, "dc2", "west", "west-data", &["h2"]);
    storage(&mut b, "dc1", "west-copy", "west-copy", &["h1"]);
    storage(&mut b, "dc2", "east-copy", "east-copy", &["h2"]);
    put_vm(&mut b, "vm1", "web-1", "h1", &["east"]);
    put_vm(&mut b, "vm2", "web-2", "h1", &["east"]);
    put_vm(&mut b, "vm3", "erp-1", "h2", &["west"]);
    let start = b.done();
    b.replica("east", "east-copy").replica("west", "west-copy");
    let sc = Scenario {
        id: s("both-ways"),
        title: s("Two sites, each other's backup"),
        story: s("East and West both run production VMs, and each site has a spare domain waiting for the copy of the other site's data. Nothing is replicated yet."),
        goal: s("Losing either site loses no VM disk: each production domain is replicated into the other data center"),
        hint: s("A copy in the same data center does not survive the loss of that data center. Pair every production domain with the spare of the other site."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 18,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::Link { rel: Rel::Replica, min: 2 },
            TopoGoal::SurviveSiteLoss,
        ],
    };
    (sc, b.done())
}

/// db-1 has disks on two domains; the second copy hangs on the wrong primary.
fn one_of_two() -> (Scenario, Topology) {
    let mut b = two_sites(("Default", "Recovery"), &["h1", "h2"], &["h3"]);
    storage(&mut b, "dc1", "os", "nfs-os", &["h1", "h2"]);
    storage(&mut b, "dc1", "data", "nfs-data", &["h1", "h2"]);
    storage(&mut b, "dc2", "dr1", "dr-1", &["h3"]);
    storage(&mut b, "dc2", "dr2", "dr-2", &["h3"]);
    put_vm(&mut b, "vm1", "db-1", "h1", &["os", "data"]);
    put_vm(&mut b, "vm2", "web-1", "h2", &["os"]);
    b.replica("os", "dr1").replica("os", "dr2");
    let start = b.done();
    let mut fixed = start.clone();
    drop_edges(&mut fixed, &[("os", "dr2")]);
    fixed.edges.push(super::super::Edge::new("data", "dr2"));
    let sc = Scenario {
        id: s("one-of-two"),
        title: s("One disk of two"),
        story: s("db-1 has disks on nfs-os and nfs-data. After the drill the Recovery site brought back its system disk but not the data disk."),
        goal: s("Every disk domain of every VM has its own replica in the Recovery data center"),
        hint: s("Check each disk domain of db-1 for a copy in the other site. A copy belongs to one primary only."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 18,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::Link { rel: Rel::Replica, min: 2 },
            TopoGoal::SurviveSiteLoss,
        ],
    };
    (sc, fixed)
}

/// The copy of nfs-prod is attached to the same data center as the original and is lost with it; the Recovery site has storage of its own.
fn same_site() -> (Scenario, Topology) {
    let mut b = two_sites(("Default", "Recovery"), &["h1", "h2"], &["h3"]);
    storage(&mut b, "dc1", "nfs", "nfs-prod", &["h1", "h2"]);
    storage(&mut b, "dc1", "copy", "nfs-copy", &["h1", "h2"]);
    storage(&mut b, "dc2", "local", "nfs-local", &["h3"]);
    b.replica("nfs", "copy");
    put_vm(&mut b, "vm1", "web-1", "h1", &["nfs"]);
    put_vm(&mut b, "vm2", "db-1", "h2", &["nfs"]);
    let start = b.done();
    let mut fixed = start.clone();
    drop_edges(&mut fixed, &[("dc1", "copy"), ("copy", "h1"), ("copy", "h2")]);
    fixed.edges.push(super::super::Edge::new("dc2", "copy"));
    fixed.edges.push(super::super::Edge::new("copy", "h3"));
    let sc = Scenario {
        id: s("same-site"),
        title: s("The copy sits next to the original"),
        story: s("nfs-copy is the replica of nfs-prod, but both domains are attached to the Default data center. The Recovery data center runs on its own nfs-local and has no copy of production."),
        goal: s("The replica of nfs-prod is Active in the Recovery data center and both data centers are Up"),
        hint: s("A domain is attached to one data center. A copy in the same site disappears together with the original, so it has to be moved."),
        palette: vec![Kind::StorageDomain],
        max_nodes: 17,
        start,
        goals: vec![
            TopoGoal::Healthy,
            TopoGoal::DcUp { min: 2 },
            TopoGoal::Link { rel: Rel::Replica, min: 1 },
            TopoGoal::SurviveSiteLoss,
        ],
    };
    (sc, fixed)
}
