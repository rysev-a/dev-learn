//! Chapter 18: users, roles and permissions. A permission is a role on one object and applies to that object and everything under it.

use std::collections::BTreeMap;

use super::super::{DomainType, Kind, Role, Scenario, TopoGoal, Topology};
use super::builder::*;

fn can(user: &str, action: Action, object: &str) -> TopoGoal {
    TopoGoal::UserCan { user: s(user), action, object: s(object) }
}

fn cannot(user: &str, action: Action, object: &str) -> TopoGoal {
    TopoGoal::UserCannot { user: s(user), action, object: s(object) }
}

/// A VM with a disk on the NFS domain, placed on a host.
fn vm_on(b: &mut B, id: &str, name: &str, host: &str) {
    b.vm(id, name, 4, false).link(&[(host, id), ("nfs", id)]);
}

/// One cluster of two hosts, two VMs on host-1 and the user anna, who has no permissions yet.
fn run_only_start() -> B {
    let mut b = with_storage();
    vm_on(&mut b, "vm1", "web-1", "h1");
    vm_on(&mut b, "vm2", "db-1", "h1");
    b.add("anna", Kind::User, "anna");
    b
}

/// Two clusters in one data center, hosts 1 and 2 in cluster-a and host-3 in cluster-b, a VM on host-1 and a VM on host-3; the user boris has no permissions.
fn two_clusters_start() -> B {
    let mut b = with_storage();
    b.add("cl2", Kind::Cluster, "cluster-b").host("h3", "host-3", 32).link(&[
        ("dc1", "cl2"),
        ("cl2", "h3"),
        ("mgmt", "cl2"),
        ("mgmt", "h3"),
        ("nfs", "h3"),
    ]);
    vm_on(&mut b, "vm1", "web-1", "h1");
    vm_on(&mut b, "vm2", "db-1", "h3");
    b.add("boris", Kind::User, "boris");
    b
}

/// One cluster, two hosts with a VM each, and two users with different needs and no permissions.
fn least_start() -> B {
    let mut b = with_storage();
    vm_on(&mut b, "vm1", "web-1", "h1");
    vm_on(&mut b, "vm2", "db-1", "h2");
    b.add("dana", Kind::User, "dana").add("erin", Kind::User, "erin");
    b
}

/// A cluster of three hosts; frank's cluster administrator permission sits on host-1 instead of the cluster.
fn wrong_object_start() -> B {
    let mut b = with_storage();
    b.host("h3", "host-3", 32).link(&[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
    vm_on(&mut b, "vm1", "web-1", "h3");
    b.grant("frank", "perm-1", PermRole::ClusterAdmin, "h1");
    b
}

/// Two data centers under one engine, each with a cluster, a host, a management network and a domain; the user kira has no permissions.
fn two_sites_start() -> B {
    let mut b = B::default();
    b.add("engine", Kind::Engine, "engine")
        .add("dc1", Kind::DataCenter, "Default")
        .add("dc2", Kind::DataCenter, "Remote")
        .add("cl1", Kind::Cluster, "cluster-a")
        .add("cl2", Kind::Cluster, "cluster-b")
        .add("h1", Kind::Host, "host-1")
        .add("h2", Kind::Host, "host-2")
        .net("mgmt", "ovirtmgmt", Role::Management)
        .net("mgmt2", "remote-mgmt", Role::Management)
        .domain("nfs", "nfs-data", DomainType::Nfs)
        .domain("nfs2", "nfs-remote", DomainType::Nfs)
        .link(&[
            ("engine", "dc1"),
            ("engine", "dc2"),
            ("dc1", "cl1"),
            ("dc2", "cl2"),
            ("cl1", "h1"),
            ("cl2", "h2"),
            ("dc1", "mgmt"),
            ("mgmt", "cl1"),
            ("engine", "mgmt"),
            ("mgmt", "h1"),
            ("dc2", "mgmt2"),
            ("mgmt2", "cl2"),
            ("engine", "mgmt2"),
            ("mgmt2", "h2"),
            ("dc1", "nfs"),
            ("nfs", "h1"),
            ("dc2", "nfs2"),
            ("nfs2", "h2"),
        ]);
    b.add("kira", Kind::User, "kira");
    b
}

/// Scenarios of chapter 18 (users and permissions) and the reference boards.
pub fn build() -> (Vec<Scenario>, BTreeMap<String, Topology>) {
    let run_only = Scenario {
        id: s("run-only"),
        title: s("An operator who only starts machines"),
        story: s("Anna works on the support desk. She has to start and stop web-1 when customers call, but she has no business changing its configuration, and db-1 is not hers at all. Both VMs run on the same host."),
        goal: s("Anna can run web-1, cannot edit it and cannot touch db-1"),
        hint: s("A permission applies to the object it is set on and to everything under it. Anna needs the weakest role that can still run a VM, set on the smallest object that holds only web-1."),
        palette: vec![Kind::Permission],
        max_nodes: 12,
        start: run_only_start().done(),
        goals: vec![can("anna", Action::RunVm, "vm1"), cannot("anna", Action::EditVm, "vm1"), cannot("anna", Action::RunVm, "vm2")],
    };
    let mut run_only_ref = run_only_start();
    run_only_ref.grant("anna", "perm-1", PermRole::UserRole, "vm1");

    let cluster = Scenario {
        id: s("cluster-admin"),
        title: s("The administrator of one cluster"),
        story: s("Boris looks after cluster-a: its hosts and the VMs on them. Cluster-b in the same data center belongs to another team, and Boris has no access to anything there yet."),
        goal: s("Boris manages cluster-a, its hosts and VMs, and cannot touch host-3 or db-1 in cluster-b"),
        hint: s("A permission set on a cluster reaches its hosts and the VMs placed on them, but not the next cluster. Pick the role that may manage a cluster, and the cluster as the object."),
        palette: vec![Kind::Permission],
        max_nodes: 14,
        start: two_clusters_start().done(),
        goals: vec![
            can("boris", Action::ManageCluster, "cl1"),
            can("boris", Action::ManageHost, "h2"),
            can("boris", Action::EditVm, "vm1"),
            cannot("boris", Action::ManageHost, "h3"),
            cannot("boris", Action::EditVm, "vm2"),
        ],
    };
    let mut cluster_ref = two_clusters_start();
    cluster_ref.grant("boris", "perm-1", PermRole::ClusterAdmin, "cl1");

    let least = Scenario {
        id: s("least-privilege"),
        title: s("Two users, two different needs"),
        story: s("Dana, a junior operator, starts and stops VMs in cluster-a and nothing more. Erin patches host-1 and edits the VMs on it, but must not manage host-2 or the cluster."),
        goal: s("Dana can only run the VMs, and Erin can manage host-1 and its VM but not the rest"),
        hint: s("Give each user the weakest role that does the job, on the smallest object that covers it. The roles differ in what they allow: a user role only runs VMs, a host administrator also edits them and manages the host."),
        palette: vec![Kind::Permission],
        max_nodes: 15,
        start: least_start().done(),
        goals: vec![
            can("dana", Action::RunVm, "vm1"),
            can("dana", Action::RunVm, "vm2"),
            cannot("dana", Action::EditVm, "vm1"),
            cannot("dana", Action::EditVm, "vm2"),
            can("erin", Action::ManageHost, "h1"),
            can("erin", Action::EditVm, "vm1"),
            cannot("erin", Action::ManageHost, "h2"),
            cannot("erin", Action::ManageCluster, "cl1"),
        ],
    };
    let mut least_ref = least_start();
    least_ref.grant("dana", "perm-1", PermRole::UserRole, "cl1").grant("erin", "perm-2", PermRole::HostAdmin, "h1");

    let wrong = Scenario {
        id: s("wrong-object"),
        title: s("A permission on the wrong object"),
        story: s("Frank was made a cluster administrator of cluster-a, yet he can only work with host-1: the portal refuses everything on host-2 and host-3 and on the cluster itself. He must not see the networks of the data center either."),
        goal: s("Frank manages cluster-a and its hosts and VMs, and still cannot see the data center networks"),
        hint: s("A permission applies down the hierarchy, never up or sideways, so a role set on a host stays on that host. Move the permission to the object that holds all three hosts and nothing above it."),
        palette: vec![Kind::Permission],
        max_nodes: 14,
        start: wrong_object_start().done(),
        goals: vec![
            can("frank", Action::ManageCluster, "cl1"),
            can("frank", Action::ManageHost, "h3"),
            can("frank", Action::EditVm, "vm1"),
            cannot("frank", Action::View, "mgmt"),
        ],
    };
    let mut wrong_ref = wrong_object_start().done();
    wrong_ref.edges.retain(|e| !(e.from == "perm-1" && e.to == "h1"));
    let mut wrong_ref_b = wrong_object_start();
    wrong_ref_b.t = wrong_ref;
    wrong_ref_b.link(&[("perm-1", "cl1")]);

    let site = Scenario {
        id: s("data-center-border"),
        title: s("Networks and storage of one site"),
        story: s("Kira runs the networks and the storage of the Default data center. The Remote data center belongs to another team: Kira may not manage its network or its storage domain, even though both data centers share one engine."),
        goal: s("Kira manages the networks, the storage and the hosts of Default and cannot manage anything in Remote"),
        hint: s("Networks and storage domains hang directly under the data center, not under a cluster. The role must allow managing them, and a role set on a data center stops at its border, whatever its name."),
        palette: vec![Kind::Permission],
        max_nodes: 15,
        start: two_sites_start().done(),
        goals: vec![
            can("kira", Action::ManageNetwork, "mgmt"),
            can("kira", Action::ManageStorage, "nfs"),
            can("kira", Action::ManageHost, "h1"),
            cannot("kira", Action::ManageNetwork, "mgmt2"),
            cannot("kira", Action::ManageStorage, "nfs2"),
        ],
    };
    let mut site_ref = two_sites_start();
    site_ref.grant("kira", "perm-1", PermRole::DataCenterAdmin, "dc1");

    let mut solution = BTreeMap::new();
    solution.insert(s("run-only"), run_only_ref.done());
    solution.insert(s("cluster-admin"), cluster_ref.done());
    solution.insert(s("least-privilege"), least_ref.done());
    solution.insert(s("wrong-object"), wrong_ref_b.done());
    solution.insert(s("data-center-border"), site_ref.done());
    (vec![run_only, cluster, least, wrong, site], solution)
}
