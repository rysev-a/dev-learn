//! Topology board of oVirt: the rules of links, derived statuses, paths of operations and the scenarios.

use serde_json::{json, Value};
use virtlab::ovirt_topo::{
    add_error, connect_error, default_scenarios, default_solution, evaluate, problems, prune, trace, DcStatus,
    DomainStatus, Edge, HostStatus, Kind, Node, Op, Param, Role, Scenario, TopoGoal, Topology, VmStatus, Why,
};
use virtlab::{GoalStatus, Spec, Strictness};

fn en() {
    locales::set_locale(i18n::Locale::En);
}

fn scenario(id: &str) -> Scenario {
    en();
    default_scenarios().into_iter().find(|s| s.id == id).expect("scenario")
}

fn solution(id: &str) -> Topology {
    default_solution().remove(id).expect("reference board")
}

fn node(t: &Topology, id: &str) -> Node {
    t.node(id).cloned().unwrap_or_else(|| panic!("no {id}"))
}

// ---------------------------------------------------------------- scenarios

/// Scenarios of every pack with their reference boards.
fn all() -> Vec<(Scenario, Topology)> {
    en();
    let mut out = vec![];
    for id in virtlab::ovirt_topo::pack_ids() {
        let (scenarios, mut solution) = virtlab::ovirt_topo::pack(id).expect("pack");
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
        assert!(problems(&sc.start).is_empty(), "{}: the starting board breaks a rule", sc.id);
        assert!(!sc.reached(&sc.start), "{}: the starting board must not solve the scenario", sc.id);
        assert!(!sc.reached(&Topology::default()), "{}: an empty board must not solve the scenario", sc.id);
        assert!(problems(&reference).is_empty(), "{}: reference breaks a rule", sc.id);
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
                    let mut t = reference.clone();
                    *t.nodes.iter_mut().find(|x| x.id == n.id).unwrap() = old.clone();
                    weaker.push((format!("parameters of {}", n.id), t));
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

// ---------------------------------------------------------------- rules of links

fn base() -> Topology {
    solution("storage")
}

#[test]
fn links_follow_the_table_and_explain_refusals() {
    en();
    let t = base();
    // allowed
    assert_eq!(connect_error(&t, "dc1", "cl1"), Some("these objects are already linked".to_string()));
    // wrong pair of kinds
    assert!(connect_error(&t, "h1", "dc1").unwrap().contains("not linked directly"));
    assert!(connect_error(&t, "h1", "h1").unwrap().contains("itself"));
    assert!(connect_error(&t, "nope", "h1").unwrap().contains("unknown"));
}

#[test]
fn single_parent_relations() {
    en();
    let mut t = base();
    t.nodes.push(Node::new("cl9", Kind::Cluster, "other", 0.0, 0.0));
    t.nodes.push(Node::new("dc9", Kind::DataCenter, "other", 0.0, 0.0));
    t.nodes.push(Node::new("e9", Kind::Engine, "other", 0.0, 0.0));
    // a host belongs to one cluster, a cluster to one data center, a data center to one engine
    assert_eq!(connect_error(&t, "cl9", "h1").unwrap(), "a host belongs to one cluster");
    t.edges.push(Edge::new("dc1", "cl9"));
    assert_eq!(connect_error(&t, "dc9", "cl9").unwrap(), "a cluster belongs to one data center");
    assert_eq!(connect_error(&t, "e9", "dc1").unwrap(), "a data center is managed by one engine");
    // a network and a storage domain belong to one data center
    assert_eq!(connect_error(&t, "dc9", "mgmt").unwrap(), "a logical network belongs to one data center");
    assert_eq!(connect_error(&t, "dc9", "nfs").unwrap(), "a storage domain is attached to one data center only");
    // a single engine
    assert!(add_error(&t, Kind::Engine, 24).unwrap().contains("single engine"));
    assert!(add_error(&t, Kind::Host, 24).is_none());
    assert!(add_error(&t, Kind::Host, t.nodes.len()).unwrap().contains("at most"));
}

#[test]
fn networks_and_domains_do_not_cross_data_centers() {
    en();
    let mut t = base();
    for (id, kind) in [("dc2", Kind::DataCenter), ("cl2", Kind::Cluster), ("h3", Kind::Host)] {
        t.nodes.push(Node::new(id, kind, id, 0.0, 0.0));
    }
    t.edges.extend([Edge::new("dc2", "cl2"), Edge::new("cl2", "h3")]);
    // the network of the first data center cannot be attached to the cluster of the second
    assert_eq!(connect_error(&t, "mgmt", "cl2").unwrap(), "the network is defined in another data center");
    // a host cannot see the domain of another data center
    assert_eq!(connect_error(&t, "nfs", "h3").unwrap(), "the host is in another data center");
    // and cannot take a network that is not attached to its cluster
    assert_eq!(connect_error(&t, "mgmt", "h3").unwrap(), "attach the network to the cluster of the host first");
}

#[test]
fn context_rules_do_not_depend_on_the_order_of_links() {
    en();
    // a link to an unplaced network or cluster is explained
    let mut t = Topology::default();
    for (id, kind) in [
        ("dc", Kind::DataCenter),
        ("cl", Kind::Cluster),
        ("n", Kind::Network),
        ("h", Kind::Host),
        ("d", Kind::StorageDomain),
    ] {
        t.nodes.push(Node::new(id, kind, id, 0.0, 0.0));
    }
    assert_eq!(connect_error(&t, "n", "cl").unwrap(), "define the network in a data center first");
    t.edges.push(Edge::new("dc", "n"));
    assert_eq!(connect_error(&t, "n", "cl").unwrap(), "put the cluster into a data center first");
    assert_eq!(connect_error(&t, "n", "h").unwrap(), "add the host to a cluster first");
    assert_eq!(connect_error(&t, "d", "h").unwrap(), "attach the storage domain to a data center first");
    t.edges.push(Edge::new("dc", "cl"));
    t.edges.push(Edge::new("cl", "h"));
    assert!(connect_error(&t, "n", "cl").is_none());
    t.edges.push(Edge::new("n", "cl"));
    assert!(connect_error(&t, "n", "h").is_none());
    assert!(problems(&t).is_empty());
}

#[test]
fn removing_an_object_drops_what_depends_on_it() {
    en();
    let mut t = base();
    // detaching the network from the cluster leaves the assignments to hosts without a base: they go too
    t.edges.retain(|e| !(e.from == "mgmt" && e.to == "cl1"));
    assert!(!problems(&t).is_empty());
    let dropped = prune(&mut t);
    assert_eq!(dropped, 2, "the assignments to both hosts");
    assert!(problems(&t).is_empty());
    // removing the cluster node itself: the dangling links are dropped
    let mut t = base();
    t.nodes.retain(|n| n.id != "cl1");
    prune(&mut t);
    assert!(t.edges.iter().all(|e| e.from != "cl1" && e.to != "cl1"));
    assert!(problems(&t).is_empty());
}

#[test]
fn problems_catch_a_hand_made_board() {
    en();
    let mut t = base();
    t.edges.push(Edge::new("dc1", "cl1"));
    t.edges.push(Edge::new("h1", "dc1"));
    t.edges.push(Edge::new("ghost", "dc1"));
    let texts: Vec<String> = problems(&t).into_iter().map(|p| p.text).collect();
    assert!(texts.contains(&"these objects are already linked".to_string()), "{texts:?}");
    assert!(texts.contains(&"in oVirt these objects are not linked directly".to_string()));
    assert!(texts.contains(&"a link leads to an unknown object".to_string()));
    let mut dup = base();
    dup.nodes.push(Node::new("h1", Kind::Host, "again", 0.0, 0.0));
    assert!(problems(&dup).iter().any(|p| p.text.contains("unique")));
    let mut many = Topology::default();
    for i in 0..61 {
        many.nodes.push(Node::new(&format!("n{i}"), Kind::Host, "h", 0.0, 0.0));
    }
    assert!(problems(&many).iter().any(|p| p.text.contains("at most 60")));
    let mut bad_pos = base();
    bad_pos.nodes[0].x = f64::INFINITY;
    assert!(!problems(&bad_pos).is_empty());
}

// ---------------------------------------------------------------- statuses

#[test]
fn statuses_follow_the_links() {
    en();
    let t = base();
    let ev = evaluate(&t);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::Up));
    assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::Up);
    assert_eq!(ev.dc("dc1").unwrap().spm.as_deref(), Some("h1"), "the first Up host is the SPM");
    assert_eq!(ev.domain("nfs").unwrap().status, DomainStatus::Active);
    assert!(ev.domain("nfs").unwrap().master);

    // no management network: NonResponsive, the data center loses its host
    let mut broken = t.clone();
    broken.edges.retain(|e| !(e.from == "engine" && e.to == "mgmt"));
    let ev = evaluate(&broken);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::NonResponsive));
    assert_eq!(ev.hosts[0].why, [Why::NoManagementPath]);
    assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::NonResponsive);
    assert_eq!(ev.domain("nfs").unwrap().status, DomainStatus::Inactive);

    // the role matters: the same network as a VM network is no path for the engine
    let mut vm_net = t.clone();
    vm_net
        .nodes
        .iter_mut()
        .find(|n| n.id == "mgmt")
        .unwrap()
        .params
        .insert("role".into(), virtlab::ovirt_topo::Param::Str("vm".into()));
    assert_eq!(node(&vm_net, "mgmt").role(), Role::Vm);
    assert!(evaluate(&vm_net).hosts.iter().all(|h| h.status == HostStatus::NonResponsive));
}

#[test]
fn a_domain_nobody_sees_breaks_the_hosts() {
    en();
    let mut t = base();
    t.edges.retain(|e| !(e.from == "nfs" && e.to == "h2"));
    let ev = evaluate(&t);
    assert_eq!(ev.host("h1").unwrap().status, HostStatus::Up);
    let h2 = ev.host("h2").unwrap();
    assert_eq!(h2.status, HostStatus::NonOperational);
    assert_eq!(h2.why, [Why::MissingStorage("nfs-data".into())]);
    assert_eq!(h2.why[0].text(), "the host does not see the storage domain “nfs-data”");
    // the data center is still Up through the other host
    assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::Up);
    // an attached domain without any connected host leaves the data center Uninitialized
    let mut none = base();
    none.edges.retain(|e| !(e.from == "nfs"));
    none.edges.push(Edge::new("dc1", "nfs"));
    let ev = evaluate(&none);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::NonOperational));
    assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::NonResponsive);
}

#[test]
fn the_first_attached_domain_is_the_master() {
    en();
    let mut t = base();
    t.nodes.push(Node::new("nfs2", Kind::StorageDomain, "second", 0.0, 0.0));
    t.edges.extend([Edge::new("dc1", "nfs2"), Edge::new("nfs2", "h1"), Edge::new("nfs2", "h2")]);
    let ev = evaluate(&t);
    assert!(ev.domain("nfs").unwrap().master);
    assert!(!ev.domain("nfs2").unwrap().master);
    // without storage the data center is Uninitialized
    let ev = evaluate(&solution("build"));
    assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::Uninitialized);
    assert!(ev.dc("dc1").unwrap().spm.is_none());
}

#[test]
fn a_required_network_must_be_on_every_host() {
    en();
    let ev = evaluate(&solution("repair"));
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::Up), "the repaired board is healthy");
    let mut t;
    t = scenario("repair").start;
    let ev = evaluate(&t);
    assert_eq!(ev.host("h2").unwrap().why, [Why::MissingNetwork("vm-net".into())]);
    assert_eq!(ev.host("h3").unwrap().status, HostStatus::NonResponsive);
    t.nodes
        .iter_mut()
        .find(|n| n.id == "vmnet")
        .unwrap()
        .params
        .insert("required".into(), virtlab::ovirt_topo::Param::Bool(false));
    assert_eq!(
        evaluate(&t).host("h2").unwrap().status,
        HostStatus::Up,
        "an optional network is not required on the host"
    );
    // but the VM that has a virtual NIC in it still cannot start there
    let vm = evaluate(&t).vm("vm1").unwrap().clone();
    assert_eq!(vm.status, VmStatus::Down);
}

#[test]
fn a_vm_needs_its_host_networks_and_disk() {
    en();
    let t = solution("repair");
    let ev = evaluate(&t);
    assert_eq!(ev.vm("vm1").unwrap().status, VmStatus::Running);
    // a disk in a domain of another data center
    let mut other = t.clone();
    other.nodes.push(Node::new("dc2", Kind::DataCenter, "other", 0.0, 0.0));
    other.nodes.push(Node::new("far", Kind::StorageDomain, "far", 0.0, 0.0));
    other.edges.extend([Edge::new("dc2", "far"), Edge::new("far", "vm1")]);
    let vm = evaluate(&other).vm("vm1").unwrap().clone();
    assert_eq!(vm.status, VmStatus::Down);
    assert!(vm.why[0].text().contains("far"));
    // no host at all
    let mut unplaced = t.clone();
    unplaced.edges.retain(|e| e.to != "vm1" || e.from != "h2");
    assert_eq!(evaluate(&unplaced).vm("vm1").unwrap().why[0].text(), "the VM is not placed on a host");
}

// ---------------------------------------------------------------- paths of operations

#[test]
fn the_path_of_a_command_goes_over_the_management_network() {
    en();
    let t = solution("repair");
    let ev = evaluate(&t);
    let tr = trace(&t, &ev, &Op::StartVm { vm: "vm1".into() });
    assert!(tr.ok, "{:?}", tr.hops);
    // engine -> host over the management network, then the NIC and the disk
    assert_eq!(tr.hops.len(), 3);
    assert_eq!(tr.hops[0].links, [("engine".to_string(), "mgmt".to_string()), ("mgmt".to_string(), "h2".to_string())]);
    assert!(tr.hops[0].text.contains("ovirtmgmt"));
    // break the host: the path stops at the first hop
    let start = scenario("repair").start;
    let ev = evaluate(&start);
    let tr = trace(&start, &ev, &Op::EngineToHost { host: "h3".into() });
    assert!(!tr.ok);
    assert!(tr.hops[0].text.contains("no management network"));
    let tr = trace(&start, &ev, &Op::StartVm { vm: "vm1".into() });
    assert!(!tr.ok, "the VM sits on a NonOperational host");
}

#[test]
fn a_vm_migrates_only_inside_its_cluster() {
    en();
    let sc = scenario("migrate");
    let ev = evaluate(&sc.start);
    let tr = trace(&sc.start, &ev, &Op::Migrate { vm: "vm1".into() });
    assert!(!tr.ok);
    assert!(tr.hops[0].text.contains("never leaves its cluster"));
    let fixed = solution("migrate");
    let ev = evaluate(&fixed);
    let tr = trace(&fixed, &ev, &Op::Migrate { vm: "vm1".into() });
    assert!(tr.ok, "{:?}", tr.hops);
    // the memory goes over the management network when there is no migration one
    assert!(tr.hops.iter().any(|h| h.links.len() == 2 && h.text.contains("memory of the VM")));
    // a dedicated migration network is preferred
    let mut with_migration = fixed.clone();
    with_migration.nodes.push(Node::network("mig", "migration", 0.0, 0.0, Role::Migration, false));
    with_migration.edges.extend([
        Edge::new("dc1", "mig"),
        Edge::new("mig", "cl1"),
        Edge::new("mig", "h1"),
        Edge::new("mig", "h3"),
    ]);
    assert!(problems(&with_migration).is_empty());
    let ev = evaluate(&with_migration);
    let tr = trace(&with_migration, &ev, &Op::Migrate { vm: "vm1".into() });
    assert!(tr.ok);
    assert!(tr.hops.iter().any(|h| h.text.contains("“migration”")));
    // a VM without a host and an unknown VM cannot migrate
    let mut unplaced = fixed.clone();
    unplaced.edges.retain(|e| e.to != "vm1" || e.from != "h1");
    let ev = evaluate(&unplaced);
    assert!(!trace(&unplaced, &ev, &Op::Migrate { vm: "vm1".into() }).ok);
    assert!(!trace(&unplaced, &ev, &Op::Migrate { vm: "nobody".into() }).ok);
}

// ---------------------------------------------------------------- goals

#[test]
fn goals_are_described_and_checked() {
    en();
    let t = solution("two");
    let ev = evaluate(&t);
    assert!(TopoGoal::DcUp { min: 2 }.check(&t, &ev));
    assert!(!TopoGoal::DcUp { min: 3 }.check(&t, &ev));
    assert!(TopoGoal::EachDcHasUpHosts { min: 1 }.check(&t, &ev));
    assert!(!TopoGoal::EachDcHasUpHosts { min: 2 }.check(&t, &ev));
    assert!(TopoGoal::Spm { min: 2 }.check(&t, &ev));
    assert!(TopoGoal::Has { node: Kind::Host, min: 3 }.check(&t, &ev));
    assert!(TopoGoal::Lacks { node: Kind::Vm }.check(&t, &ev));
    assert!(!TopoGoal::Healthy.check(&Topology::default(), &evaluate(&Topology::default())));
    assert_eq!(TopoGoal::HostsUp { min: 2 }.describe(), "at least 2 host(s) are Up");
    assert_eq!(
        TopoGoal::OpOk { op: virtlab::ovirt_topo::OpKind::Migrate }.describe(),
        "every VM can be live-migrated within its cluster"
    );
    assert!(
        TopoGoal::Link { rel: virtlab::ovirt_topo::rel(Kind::Engine, Kind::Network).unwrap(), min: 2 }.check(&t, &ev)
    );
}

// ---------------------------------------------------------------- server check

fn spec() -> Spec {
    en();
    virtlab::builtin("virt-sim-ovirt-topo").expect("topology exercise")
}

fn verdict(spec: &Spec, goal: &str, board: Value) -> GoalStatus {
    let mut m = serde_json::Map::new();
    m.insert(goal.into(), board);
    virtlab::verify(spec, &Value::Object(m)).goals.into_iter().find(|g| g.id == goal).expect("goal").status
}

#[test]
fn the_server_checks_the_board() {
    let spec = spec();
    spec.validate().unwrap();
    for sc in default_scenarios() {
        let board = serde_json::to_value(solution(&sc.id)).unwrap();
        assert_eq!(verdict(&spec, &sc.id, board), GoalStatus::Verified, "{}", sc.id);
        let start = serde_json::to_value(&sc.start).unwrap();
        if sc.id != "build" {
            assert!(matches!(verdict(&spec, &sc.id, start), GoalStatus::Rejected { .. }), "{}", sc.id);
        }
    }
    // a kind outside the palette
    let mut cheat = solution("migrate");
    cheat.nodes.push(Node::new("x", Kind::Vm, "vm", 0.0, 0.0));
    let GoalStatus::Rejected { reason } = verdict(&spec, "migrate", serde_json::to_value(&cheat).unwrap()) else {
        panic!("accepted")
    };
    assert!(reason.contains("not available"), "{reason}");
    // a broken rule
    let mut broken = solution("storage");
    broken.edges.push(Edge::new("dc1", "cl1"));
    assert!(matches!(verdict(&spec, "storage", serde_json::to_value(&broken).unwrap()), GoalStatus::Rejected { .. }));
    // garbage
    assert!(matches!(verdict(&spec, "storage", json!({"nodes": 3})), GoalStatus::Rejected { .. }));
    // a whole solution map is solved only when every scenario is
    let mut all = serde_json::Map::new();
    for sc in default_scenarios() {
        all.insert(sc.id.clone(), serde_json::to_value(solution(&sc.id)).unwrap());
    }
    assert!(virtlab::verify_with(&spec, &Value::Object(all.clone()), Strictness::Strict).solved);
    all.remove("two");
    assert!(!virtlab::verify_with(&spec, &Value::Object(all), Strictness::Strict).solved);
}

#[test]
fn the_reference_is_in_the_spec_but_not_needed_to_parse_it() {
    let spec = spec();
    let mut v = serde_json::to_value(&spec).unwrap();
    assert!(v["solution"].is_object());
    v.as_object_mut().unwrap().remove("solution");
    let parsed: Spec = serde_json::from_value(v).unwrap();
    parsed.validate().unwrap();
    let Spec::OvirtTopo { solution, .. } = parsed else { panic!("variant") };
    assert!(solution.is_empty());
}

#[test]
fn texts_are_in_russian() {
    let _ru = locales::guard(i18n::Locale::Ru);
    let t = scenario("repair").start;
    let ev = evaluate(&t);
    let why = ev.host("h2").unwrap().why[0].text();
    assert_eq!(why, "обязательная сеть «vm-net» не назначена на хост");
    assert_eq!(
        ev.host("h3").unwrap().why[0].text(),
        "менеджер не может связаться с хостом: между ними нет сети управления"
    );
    assert_eq!(connect_error(&t, "dc1", "cl1").unwrap(), "эти объекты уже соединены");
}

// ---------------------------------------------------------------- storage and networks (chapters 20 and 21)

fn find(id: &str) -> (Scenario, Topology) {
    all().into_iter().find(|(sc, _)| sc.id == id).unwrap_or_else(|| panic!("scenario {id}"))
}

#[test]
fn an_iscsi_domain_needs_a_storage_network_on_the_host() {
    en();
    let (sc, reference) = find("iscsi");
    let ev = evaluate(&reference);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::Up));
    // without the storage network both hosts are NonOperational and say why
    let mut no_net = reference.clone();
    no_net.edges.retain(|e| e.from != "stor");
    prune(&mut no_net);
    let ev = evaluate(&no_net);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::NonOperational));
    assert_eq!(ev.hosts[0].why, [Why::NoStorageNetwork("iscsi-lun".into())]);
    assert_eq!(
        ev.hosts[0].why[0].text(),
        "the domain “iscsi-lun” is iSCSI: the host needs a network with the storage role"
    );
    // an NFS domain does not need it, and the role matters: a VM network does not help
    let mut nfs = reference.clone();
    nfs.nodes.iter_mut().find(|n| n.id == "iscsi").unwrap().params.clear();
    nfs.edges.retain(|e| e.from != "stor");
    prune(&mut nfs);
    assert!(evaluate(&nfs).hosts.iter().all(|h| h.status == HostStatus::Up));
    let mut wrong_role = reference.clone();
    wrong_role
        .nodes
        .iter_mut()
        .find(|n| n.id == "stor")
        .unwrap()
        .params
        .insert("role".into(), virtlab::ovirt_topo::Param::Str("vm".into()));
    assert!(evaluate(&wrong_role).hosts.iter().all(|h| h.status == HostStatus::NonOperational));
    assert!(!sc.reached(&wrong_role));
}

#[test]
fn losing_one_object_is_survived_only_with_a_spare() {
    en();
    let ev_goal = |t: &Topology, kind: Kind| TopoGoal::SurviveLoss { node: kind }.check(t, &evaluate(t));
    let one = find("spm").0.start;
    assert!(!ev_goal(&one, Kind::Host), "a single host is a single point of failure");
    let (_, two_hosts) = find("spm");
    assert!(ev_goal(&two_hosts, Kind::Host));
    assert!(!ev_goal(&two_hosts, Kind::Vm), "no VM at all: nothing to lose");
    // the master domain: the next attached one takes over
    let (_, with_spare) = find("master");
    assert!(ev_goal(&with_spare, Kind::StorageDomain));
    assert_eq!(evaluate(&with_spare.without("nfs")).domain("nfs2").map(|d| d.master), Some(true));
    // a second domain that one host does not see breaks that host: the data center survives, but the exercise wants both hosts Up
    let mut unseen = with_spare.clone();
    unseen.edges.retain(|e| !(e.from == "nfs2" && e.to == "h2"));
    assert!(ev_goal(&unseen, Kind::StorageDomain));
    assert!(!TopoGoal::HostsUp { min: 2 }.check(&unseen, &evaluate(&unseen)));
}

#[test]
fn migration_goes_over_the_network_of_the_wanted_role() {
    en();
    let (sc, reference) = find("migration-net");
    let goal = TopoGoal::MigrateOverRole { role: Role::Migration };
    assert!(goal.check(&reference, &evaluate(&reference)));
    assert_eq!(goal.describe(), "the memory of a migration goes over a migration network");
    let start = &sc.start;
    assert!(!goal.check(start, &evaluate(start)), "the management network carries it without a dedicated one");
    assert!(TopoGoal::MigrateOverRole { role: Role::Management }.check(start, &evaluate(start)));
    // a migration network that only one host has is not a path
    let mut one_side = reference.clone();
    one_side.edges.retain(|e| !(e.from == "migr" && e.to == "h2"));
    assert!(!goal.check(&one_side, &evaluate(&one_side)));
}

#[test]
fn parameter_goals_read_the_defaults() {
    en();
    let (_, optional) = find("optional");
    let optional_goal = TopoGoal::Param { node: Kind::Network, key: "required".into(), value: "false".into() };
    assert!(optional_goal.check(&optional, &evaluate(&optional)));
    assert_eq!(optional_goal.describe(), "a network with required = false");
    let start = find("optional").0.start;
    assert!(!optional_goal.check(&start, &evaluate(&start)), "networks are required unless told otherwise");
    let nfs = TopoGoal::Param { node: Kind::StorageDomain, key: "type".into(), value: "nfs".into() };
    assert!(nfs.check(&start, &evaluate(&start)), "a domain is NFS unless told otherwise");
    assert_eq!(node(&start, "nfs").domain_type(), virtlab::ovirt_topo::DomainType::Nfs);
}

#[test]
fn a_vm_with_an_optional_network_runs_only_where_it_is() {
    en();
    let (sc, reference) = find("vm-optional");
    let ev = evaluate(&sc.start);
    assert!(ev.hosts.iter().all(|h| h.status == HostStatus::Up), "the optional network is not needed for Up");
    let tr = trace(&sc.start, &ev, &Op::Migrate { vm: "vm1".into() });
    assert!(!tr.ok);
    assert!(tr.hops.iter().any(|h| !h.ok && h.text.contains("vm-net")), "{:?}", tr.hops);
    let ev = evaluate(&reference);
    assert!(trace(&reference, &ev, &Op::Migrate { vm: "vm1".into() }).ok);
    // making it required while one host misses it breaks that host
    let mut required = sc.start.clone();
    required
        .nodes
        .iter_mut()
        .find(|n| n.id == "vmnet")
        .unwrap()
        .params
        .insert("required".into(), virtlab::ovirt_topo::Param::Bool(true));
    assert_eq!(evaluate(&required).host("h2").unwrap().status, HostStatus::NonOperational);
}

#[test]
fn every_pack_is_a_well_formed_exercise() {
    en();
    let mut seen = std::collections::BTreeSet::new();
    for id in virtlab::ovirt_topo::pack_ids() {
        let (scenarios, solution) = virtlab::ovirt_topo::pack(id).unwrap();
        assert!((4..=6).contains(&scenarios.len()), "{id}: a pack has 4 to 6 scenarios, not {}", scenarios.len());
        assert!(virtlab::ovirt_topo::pack_chapter(id).is_some());
        assert_eq!(solution.len(), scenarios.len(), "{id}");
        for sc in &scenarios {
            assert!(seen.insert(format!("{id}/{}", sc.id)), "{id}: duplicate scenario {}", sc.id);
            assert!(
                !sc.title.is_empty() && !sc.story.is_empty() && !sc.goal.is_empty() && !sc.hint.is_empty(),
                "{id}/{}: texts",
                sc.id
            );
            assert!(sc.goals.len() >= 2, "{id}/{}: a scenario has at least two goals", sc.id);
            assert!(!sc.palette.is_empty(), "{id}/{}: palette", sc.id);
            // English texts only; the Russian ones live in the dictionary
            assert!(
                sc.title.is_ascii() || sc.title.chars().all(|c| !('а'..='я').contains(&c.to_ascii_lowercase())),
                "{id}/{}: Cyrillic in a key",
                sc.id
            );
        }
        // the identifiers of scenarios are unique within the whole exercise and the spec validates
        let spec = virtlab::builtin(id).expect("builtin");
        spec.validate().unwrap_or_else(|e| panic!("{id}: {}", e.0));
    }
    assert!(seen.len() >= 13);
}

// ---------------------------------------------------------------- the mechanics of chapters 18, 19, 22 and 24
//
// Small hand-made boards: one data center with a cluster and hosts, the management network and an NFS domain every host sees.

mod mechanics {
    use super::*;
    use virtlab::ovirt_topo::{
        affinity_breaks, ancestors, evacuation_possible, fence_agent, fence_proxy, ha_restart_ok, host_load, param_specs,
        restorable_after_domain_loss, survives_site_loss, user_can, Action, BackupType, OpKind, ParamTy, PermRole, Rel, VmWhy,
    };

    fn put(t: &mut Topology, id: &str, kind: Kind) {
        t.nodes.push(Node::new(id, kind, id, 0.0, 0.0));
    }

    fn put_with(t: &mut Topology, id: &str, kind: Kind, params: &[(&str, Param)]) {
        let mut n = Node::new(id, kind, id, 0.0, 0.0);
        for (k, v) in params {
            n.params.insert((*k).into(), v.clone());
        }
        t.nodes.push(n);
    }

    fn link(t: &mut Topology, pairs: &[(&str, &str)]) {
        t.edges.extend(pairs.iter().map(|(a, b)| Edge::new(a, b)));
    }

    fn mem(gb: u32) -> Param {
        Param::Str(gb.to_string())
    }

    /// The engine, `dc1` with `cl1`, the management network, the NFS domain `nfs` and the given hosts (name, GB), all Up.
    fn lab(hosts: &[(&str, u32)]) -> Topology {
        let mut t = Topology::default();
        put(&mut t, "engine", Kind::Engine);
        put(&mut t, "dc1", Kind::DataCenter);
        put(&mut t, "cl1", Kind::Cluster);
        put_with(&mut t, "mgmt", Kind::Network, &[("role", Param::Str("management".into()))]);
        put(&mut t, "nfs", Kind::StorageDomain);
        link(&mut t, &[("engine", "dc1"), ("dc1", "cl1"), ("dc1", "mgmt"), ("mgmt", "cl1"), ("engine", "mgmt"), ("dc1", "nfs")]);
        for (h, gb) in hosts {
            put_with(&mut t, h, Kind::Host, &[("mem", mem(*gb))]);
            link(&mut t, &[("cl1", h), ("mgmt", h), ("nfs", h)]);
        }
        t
    }

    /// A VM with a disk on `nfs`, placed on `host`.
    fn vm(t: &mut Topology, id: &str, host: Option<&str>, gb: u32, ha: bool) {
        put_with(t, id, Kind::Vm, &[("mem", mem(gb)), ("ha", Param::Bool(ha))]);
        link(t, &[("nfs", id)]);
        if let Some(h) = host {
            link(t, &[(h, id)]);
        }
    }

    fn fence(t: &mut Topology, agent: &str, host: &str) {
        put(t, agent, Kind::FenceAgent);
        link(t, &[(agent, host)]);
    }

    fn running(t: &Topology, vm: &str) -> bool {
        evaluate(t).vm(vm).unwrap().status == VmStatus::Running
    }

    fn check(goal: TopoGoal, t: &Topology) -> bool {
        en();
        goal.check(t, &evaluate(t))
    }

    // ---- parameters

    #[test]
    fn parameters_come_from_a_table_and_are_validated_against_it() {
        en();
        let keys = |k: Kind| param_specs(k).iter().map(|s| s.key).collect::<Vec<_>>();
        assert_eq!(keys(Kind::Network), ["role", "required"], "the e2e relies on the role being first");
        assert_eq!(keys(Kind::StorageDomain), ["type"]);
        assert_eq!(keys(Kind::Host), ["mem", "maintenance"]);
        assert_eq!(keys(Kind::Vm), ["ha", "mem"]);
        assert_eq!(keys(Kind::AffinityGroup), ["polarity", "hard"]);
        assert_eq!(keys(Kind::Backup), ["type"]);
        assert_eq!(keys(Kind::Permission), ["role"]);
        for k in [Kind::Engine, Kind::DataCenter, Kind::Cluster, Kind::FenceAgent, Kind::User] {
            assert!(keys(k).is_empty(), "{k:?}");
        }
        // every default is a value the parameter accepts, and a select lists it
        for k in Kind::ALL {
            for s in param_specs(k) {
                assert!(s.accepts(&s.default), "{k:?}.{}", s.key);
                if let ParamTy::Select(options) = &s.ty {
                    assert!(options.iter().any(|o| Param::Str(o.value.into()) == s.default));
                }
            }
        }
        // defaults
        let n = |k: Kind| Node::new("x", k, "x", 0.0, 0.0);
        assert_eq!(n(Kind::Vm).param_text("mem"), "4");
        assert_eq!(n(Kind::Vm).param_text("ha"), "false");
        assert_eq!(n(Kind::Host).param_text("mem"), "32");
        assert_eq!(n(Kind::Host).param_text("maintenance"), "false");
        assert_eq!(n(Kind::AffinityGroup).param_text("polarity"), "negative");
        assert_eq!(n(Kind::AffinityGroup).param_text("hard"), "true");
        assert_eq!(n(Kind::Backup).backup_type(), BackupType::Snapshot);
        assert_eq!(n(Kind::Permission).perm_role(), PermRole::UserRole);
        assert_eq!(n(Kind::Network).param_text("role"), "vm");
        assert_eq!(n(Kind::StorageDomain).param_text("type"), "nfs");
        assert_eq!(n(Kind::Host).mem_gb(), 32);
        // the network role and the permission role share a key but not a meaning
        assert_eq!(Node::network("n", "n", 0.0, 0.0, Role::Storage, true).param_text("role"), "storage");
        assert_eq!(n(Kind::Permission).with_param("role", Param::Str("HostAdmin".into())).param_text("role"), "HostAdmin");
    }

    #[test]
    fn unknown_keys_and_values_are_rejected_with_a_rule() {
        en();
        let mut t = lab(&[("h1", 16)]);
        assert!(problems(&t).is_empty());
        fn host(t: &mut Topology) -> &mut Node {
            t.nodes.iter_mut().find(|n| n.id == "h1").unwrap()
        }
        host(&mut t).params.insert("color".into(), Param::Bool(true));
        let texts: Vec<String> = problems(&t).into_iter().map(|p| p.text).collect();
        assert_eq!(texts, ["“color” is not a parameter of a host"]);
        let mut t = lab(&[("h1", 16)]);
        host(&mut t).params.insert("mem".into(), Param::Str("48".into()));
        assert_eq!(problems(&t)[0].text, "“48” is not a valid value of the parameter “mem”");
        // the wrong type counts as a wrong value
        let mut t = lab(&[("h1", 16)]);
        host(&mut t).params.insert("maintenance".into(), Param::Str("yes".into()));
        assert!(!problems(&t).is_empty());
        let mut t = lab(&[("h1", 16)]);
        host(&mut t).params.insert("mem".into(), Param::Bool(true));
        assert!(!problems(&t).is_empty());
        // the invalid value reads as the default, so nothing downstream sees garbage
        assert_eq!(host(&mut t).param_text("mem"), "32");
        // the server refuses it
        let sc = scenario("build");
        assert!(sc.invalid(&t).is_some());
    }

    // ---- maintenance, memory, affinity

    #[test]
    fn a_host_in_maintenance_is_not_up_and_runs_nothing() {
        en();
        let mut t = lab(&[("h1", 16), ("h2", 16)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        assert!(TopoGoal::Healthy.check(&t, &evaluate(&t)));
        t.nodes.iter_mut().find(|n| n.id == "h1").unwrap().params.insert("maintenance".into(), Param::Bool(true));
        let ev = evaluate(&t);
        assert_eq!(ev.host("h1").unwrap().status, HostStatus::Maintenance);
        assert_eq!(HostStatus::Maintenance.name(), "Maintenance");
        assert_eq!(ev.host("h1").unwrap().why[0].text(), "the host is in maintenance mode: it runs no VMs");
        assert_eq!(ev.vm("vm1").unwrap().status, VmStatus::Down);
        assert_eq!(ev.vm("vm1").unwrap().why, [VmWhy::HostMaintenance("h1".into())]);
        assert_eq!(ev.vm("vm1").unwrap().why[0].text(), "the host “h1” is in maintenance mode");
        // the data center lives on the other host; the VM that needs the maintenance host keeps the board from being healthy
        assert_eq!(ev.dc("dc1").unwrap().status, DcStatus::Up);
        assert_eq!(ev.dc("dc1").unwrap().spm.as_deref(), Some("h2"));
        assert!(!TopoGoal::Healthy.check(&t, &ev));
        assert!(!TopoGoal::HostsUp { min: 2 }.check(&t, &ev));
        // an empty host in maintenance is allowed
        t.edges.retain(|e| e.from != "h1" || e.to != "vm1");
        assert!(!TopoGoal::Healthy.check(&t, &evaluate(&t)), "the unplaced VM does not run");
        t.edges.push(Edge::new("h2", "vm1"));
        assert!(TopoGoal::Healthy.check(&t, &evaluate(&t)));
        // a host outside a cluster is not "in maintenance"
        let mut loose = Topology::default();
        put_with(&mut loose, "h", Kind::Host, &[("maintenance", Param::Bool(true))]);
        assert_eq!(evaluate(&loose).host("h").unwrap().status, HostStatus::NoCluster);
    }

    #[test]
    fn vms_that_need_more_memory_than_the_host_has_do_not_run() {
        en();
        let mut t = lab(&[("h1", 16)]);
        vm(&mut t, "vm1", Some("h1"), 8, false);
        vm(&mut t, "vm2", Some("h1"), 8, false);
        let load = host_load(&t, "h1");
        assert_eq!((load.used, load.capacity, load.over()), (16, 16, false), "exactly full is fine");
        assert!(running(&t, "vm1") && running(&t, "vm2"));
        vm(&mut t, "vm3", Some("h1"), 2, false);
        let load = host_load(&t, "h1");
        assert_eq!((load.used, load.over()), (18, true));
        let ev = evaluate(&t);
        for v in ["vm1", "vm2", "vm3"] {
            assert_eq!(ev.vm(v).unwrap().status, VmStatus::Down, "{v}");
            assert_eq!(ev.vm(v).unwrap().why, [VmWhy::NoMemory("h1".into())]);
        }
        assert_eq!(ev.vm("vm1").unwrap().why[0].text(), "the VMs placed on the host “h1” need more memory than it has");
        // the host itself stays Up
        assert_eq!(ev.host("h1").unwrap().status, HostStatus::Up);
        // an unplaced VM and the VMs of other hosts do not count
        assert_eq!(host_load(&t, "nope").capacity, 0);
    }

    fn group(t: &mut Topology, id: &str, polarity: &str, hard: bool, vms: &[&str]) {
        put_with(t, id, Kind::AffinityGroup, &[("polarity", Param::Str(polarity.into())), ("hard", Param::Bool(hard))]);
        for v in vms {
            link(t, &[(id, v)]);
        }
    }

    #[test]
    fn a_negative_group_keeps_the_vms_on_different_hosts() {
        en();
        let mut t = lab(&[("h1", 32), ("h2", 32)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        vm(&mut t, "vm2", Some("h1"), 4, false);
        vm(&mut t, "vm3", Some("h2"), 4, false);
        group(&mut t, "anti", "negative", true, &["vm1", "vm2", "vm3"]);
        assert_eq!(affinity_breaks(&t, "anti"), ["vm2"], "the later member on a taken host");
        let ev = evaluate(&t);
        assert_eq!(ev.vm("vm1").unwrap().status, VmStatus::Running, "the first member is fine");
        assert_eq!(ev.vm("vm2").unwrap().why, [VmWhy::AffinityViolated("anti".into())]);
        assert_eq!(ev.vm("vm2").unwrap().why[0].text(), "the VM breaks the hard affinity group “anti”");
        assert_eq!(ev.vm("vm3").unwrap().status, VmStatus::Running);
        // the order of the links decides who is "later"
        let mut t2 = t.clone();
        t2.edges.retain(|e| !(e.from == "anti"));
        link(&mut t2, &[("anti", "vm2"), ("anti", "vm1"), ("anti", "vm3")]);
        assert_eq!(affinity_breaks(&t2, "anti"), ["vm1"]);
        // moving the VM apart fixes it
        t.edges.retain(|e| !(e.from == "h1" && e.to == "vm2"));
        link(&mut t, &[("h2", "vm2")]);
                assert_eq!(affinity_breaks(&t, "anti"), ["vm3"]);
        // an unplaced member cannot break anything
        t.edges.retain(|e| !(e.from == "h2"));
        assert!(affinity_breaks(&t, "anti").is_empty());
    }

    #[test]
    fn a_positive_group_keeps_the_vms_on_one_host() {
        en();
        let mut t = lab(&[("h1", 32), ("h2", 32)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        vm(&mut t, "vm2", Some("h2"), 4, false);
        vm(&mut t, "vm3", Some("h1"), 4, false);
        group(&mut t, "together", "positive", true, &["vm1", "vm2", "vm3"]);
        assert_eq!(affinity_breaks(&t, "together"), ["vm2"], "those not on the host of the first member");
        assert_eq!(evaluate(&t).vm("vm2").unwrap().status, VmStatus::Down);
        assert!(running(&t, "vm1") && running(&t, "vm3"));
        // all together: fine
        t.edges.retain(|e| !(e.from == "h2" && e.to == "vm2"));
        link(&mut t, &[("h1", "vm2")]);
        assert!(affinity_breaks(&t, "together").is_empty());
        assert!(running(&t, "vm2"));
    }

    #[test]
    fn a_soft_group_never_changes_a_status() {
        en();
        let mut t = lab(&[("h1", 32)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        vm(&mut t, "vm2", Some("h1"), 4, false);
        group(&mut t, "soft", "negative", false, &["vm1", "vm2"]);
        assert_eq!(affinity_breaks(&t, "soft"), ["vm2"], "it is a violation, only not an enforced one");
        assert!(running(&t, "vm1") && running(&t, "vm2"));
        // a VM may be in several groups: the hard one decides
        group(&mut t, "hard", "negative", true, &["vm2"]);
        assert!(running(&t, "vm2"), "alone in the hard group");
        group(&mut t, "hard2", "negative", true, &["vm1", "vm2"]);
        assert_eq!(evaluate(&t).vm("vm2").unwrap().why, [VmWhy::AffinityViolated("hard2".into())]);
    }

    // ---- fencing and HA

    #[test]
    fn the_fence_path_goes_engine_proxy_agent_host() {
        en();
        let mut t = lab(&[("h1", 16), ("h2", 16)]);
        let ev = evaluate(&t);
        let op = Op::Fence { host: "h1".into() };
        // no agent: the engine reaches the proxy, then the path breaks
        let tr = trace(&t, &ev, &op);
        assert!(!tr.ok);
        assert_eq!(tr.hops.len(), 2);
        assert!(tr.hops[0].ok && tr.hops[0].to == "h2" && tr.hops[0].text.contains("fence proxy"));
        assert!(tr.hops[0].links.contains(&("mgmt".into(), "h2".into())));
        assert!(!tr.hops[1].ok && tr.hops[1].text.contains("has no fence agent"), "{:?}", tr.hops[1]);
        fence(&mut t, "fence1", "h1");
        let tr = trace(&t, &evaluate(&t), &op);
        assert!(tr.ok);
        assert_eq!(tr.hops.iter().map(|h| (h.from.as_str(), h.to.as_str())).collect::<Vec<_>>(), [("engine", "h2"), ("h2", "fence1"), ("fence1", "h1")]);
        assert_eq!(tr.hops[2].links, [("fence1".to_string(), "h1".to_string())]);
        assert_eq!(fence_agent(&t, "h1").map(|a| a.id.as_str()), Some("fence1"));
        assert_eq!(fence_proxy(&t, &evaluate(&t), "h1").map(|h| h.id.as_str()), Some("h2"));
        assert!(!TopoGoal::OpOk { op: OpKind::Fence }.check(&t, &evaluate(&t)), "h2 has no agent");
        fence(&mut t, "fence2", "h2");
        assert!(TopoGoal::OpOk { op: OpKind::Fence }.check(&t, &evaluate(&t)));
        assert_eq!(TopoGoal::OpOk { op: OpKind::Fence }.describe(), "every host can be fenced");
        // no other Up host: nobody can carry the command out
        let mut alone = lab(&[("h1", 16), ("h2", 16)]);
        fence(&mut alone, "fence1", "h1");
        alone.edges.retain(|e| !(e.from == "nfs" && e.to == "h2"));
        let tr = trace(&alone, &evaluate(&alone), &op);
        assert!(!tr.ok);
        assert!(tr.hops[0].text.contains("no other Up host"), "{:?}", tr.hops);
    }

    #[test]
    fn ha_restart_needs_an_agent_a_proxy_and_room() {
        en();
        let mut t = lab(&[("h1", 16), ("h2", 16)]);
        vm(&mut t, "vm1", Some("h1"), 4, true);
        assert!(!check(TopoGoal::HaRestart, &t), "no fence agent");
        fence(&mut t, "fence1", "h1");
        // h2 is the proxy and the target; h2 itself runs nothing the goal cares about
        assert!(check(TopoGoal::HaRestart, &t));
        // without the agent link
        let mut no_agent = t.clone();
        no_agent.edges.retain(|e| e.from != "fence1");
        assert!(!check(TopoGoal::HaRestart, &no_agent));
        // the flag matters: a VM that is not HA is not restarted
        let mut plain = t.clone();
        plain.nodes.iter_mut().find(|n| n.id == "vm1").unwrap().params.insert("ha".into(), Param::Bool(false));
        assert!(!check(TopoGoal::HaRestart, &plain), "there is no HA VM at all");
        // no room: h2 is full
        let mut full = t.clone();
        vm(&mut full, "big", Some("h2"), 16, false);
        assert!(!check(TopoGoal::HaRestart, &full));
        // no proxy: the other host is not Up
        let mut no_proxy = t.clone();
        no_proxy.edges.retain(|e| !(e.from == "nfs" && e.to == "h2"));
        assert!(!check(TopoGoal::HaRestart, &no_proxy));
        // a third host takes over when the second is full (the first host where the VM would run)
        let mut three = full.clone();
        put_with(&mut three, "h3", Kind::Host, &[("mem", mem(16))]);
        link(&mut three, &[("cl1", "h3"), ("mgmt", "h3"), ("nfs", "h3")]);
        assert!(check(TopoGoal::HaRestart, &three));
        // the hard anti-affinity group closes h3 as well when its other member is there
        vm(&mut three, "mate", Some("h3"), 2, false);
        group(&mut three, "apart", "negative", true, &["mate", "vm1"]);
        assert!(!check(TopoGoal::HaRestart, &three), "h2 is full, h3 holds the mate");
        // the restarted VMs share the memory of the target, one after the other
        let mut two = lab(&[("h1", 32), ("h2", 16)]);
        vm(&mut two, "a", Some("h1"), 8, true);
        vm(&mut two, "b", Some("h1"), 16, true);
        fence(&mut two, "fence1", "h1");
        assert!(!check(TopoGoal::HaRestart, &two), "8 + 16 do not fit into 16 GB together");
        two.nodes.iter_mut().find(|n| n.id == "b").unwrap().params.insert("mem".into(), mem(8));
        assert!(check(TopoGoal::HaRestart, &two));
        // every host that runs an HA VM needs its own agent
        let mut both = t.clone();
        vm(&mut both, "vm2", Some("h2"), 4, true);
        assert!(!check(TopoGoal::HaRestart, &both));
        fence(&mut both, "fence2", "h2");
        assert!(check(TopoGoal::HaRestart, &both));
        assert!(TopoGoal::HaRestart.describe().contains("HA VMs restart"));
        // the goal never touches the board it is given
        let before = t.clone();
        let _ = check(TopoGoal::HaRestart, &t);
        assert_eq!(before, t);
        assert!(ha_restart_ok(&t));
    }

    // ---- evacuation

    #[test]
    fn evacuation_needs_another_host_with_room() {
        en();
        let mut t = lab(&[("h1", 16), ("h2", 16)]);
        assert!(!check(TopoGoal::EvacuationPossible, &t), "no host runs a VM");
        vm(&mut t, "vm1", Some("h1"), 4, false);
        assert!(check(TopoGoal::EvacuationPossible, &t));
        // the other host is full
        let mut full = t.clone();
        vm(&mut full, "big", Some("h2"), 16, false);
        assert!(!check(TopoGoal::EvacuationPossible, &full));
        // every host that runs VMs is evacuated in turn; the VMs of one host must fit next to the VMs of the other
        let mut both = t.clone();
        vm(&mut both, "vm2", Some("h2"), 8, false);
        vm(&mut both, "vm3", Some("h1"), 8, false);
        assert!(!check(TopoGoal::EvacuationPossible, &both), "4 + 8 + 8 = 20 GB do not fit into one 16 GB host");
        both.nodes.iter_mut().find(|n| n.id == "vm2").unwrap().params.insert("mem".into(), mem(2));
        assert!(check(TopoGoal::EvacuationPossible, &both), "2 + 4 + 8 = 14 GB fit, each side is moved alone");
        // a single host has nowhere to go
        let mut one = lab(&[("h1", 16)]);
        vm(&mut one, "vm1", Some("h1"), 4, false);
        assert!(!check(TopoGoal::EvacuationPossible, &one));
        // the target must be Up
        let mut down = t.clone();
        down.edges.retain(|e| !(e.from == "nfs" && e.to == "h2"));
        assert!(!check(TopoGoal::EvacuationPossible, &down));
        // memory is shared by the VMs moved one after the other
        let mut shared = lab(&[("h1", 32), ("h2", 16)]);
        vm(&mut shared, "a", Some("h1"), 8, false);
        vm(&mut shared, "b", Some("h1"), 16, false);
        assert!(!check(TopoGoal::EvacuationPossible, &shared));
        // an affinity group can close the way
        let mut apart = t.clone();
        vm(&mut apart, "vm2", Some("h2"), 2, false);
        group(&mut apart, "apart", "negative", true, &["vm1", "vm2"]);
        assert!(!check(TopoGoal::EvacuationPossible, &apart));
        assert!(!evacuation_possible(&apart), "vm1 can only go to h2, where its group mate is");
        // the board itself is untouched
        assert!(running(&t, "vm1"));
        assert_eq!(t.node("h1").unwrap().param_text("maintenance"), "false");
    }

    // ---- backups and domain loss

    #[test]
    fn only_incremental_and_full_backups_count() {
        en();
        let mut t = lab(&[("h1", 32)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        vm(&mut t, "vm2", Some("h1"), 4, false);
        assert!(!check(TopoGoal::AllVmsBackedUp, &t));
        assert!(!check(TopoGoal::RestorableAfterDomainLoss, &t));
        // a snapshot of both VMs: it lives on the disk domain
        put_with(&mut t, "snap", Kind::Backup, &[("type", Param::Str("snapshot".into()))]);
        link(&mut t, &[("vm1", "snap"), ("vm2", "snap")]);
        assert!(!check(TopoGoal::AllVmsBackedUp, &t));
        assert!(!check(TopoGoal::RestorableAfterDomainLoss, &t));
        // an incremental backup of one VM
        put_with(&mut t, "inc", Kind::Backup, &[("type", Param::Str("incremental".into()))]);
        link(&mut t, &[("vm1", "inc")]);
        assert!(!check(TopoGoal::AllVmsBackedUp, &t));
        // a full backup shared by both VMs (a backup holds several VMs, a VM has several backups)
        put_with(&mut t, "full", Kind::Backup, &[("type", Param::Str("full".into()))]);
        link(&mut t, &[("vm1", "full"), ("vm2", "full")]);
        assert!(check(TopoGoal::AllVmsBackedUp, &t));
        assert!(check(TopoGoal::RestorableAfterDomainLoss, &t));
        assert!(restorable_after_domain_loss(&t));
        // without the VMs there is nothing to say
        assert!(!check(TopoGoal::AllVmsBackedUp, &lab(&[("h1", 32)])));
        // a VM on a second domain without a good backup breaks it
        put(&mut t, "nfs2", Kind::StorageDomain);
        link(&mut t, &[("dc1", "nfs2"), ("nfs2", "h1")]);
        vm(&mut t, "vm3", Some("h1"), 2, false);
        t.edges.retain(|e| !(e.from == "nfs" && e.to == "vm3"));
        link(&mut t, &[("nfs2", "vm3")]);
        assert!(!check(TopoGoal::RestorableAfterDomainLoss, &t));
        assert!(!check(TopoGoal::AllVmsBackedUp, &t));
        link(&mut t, &[("vm3", "inc")]);
        assert!(check(TopoGoal::RestorableAfterDomainLoss, &t));
        assert!(check(TopoGoal::AllVmsBackedUp, &t));
        assert_eq!(BackupType::parse("full"), Some(BackupType::Full));
        assert!(BackupType::Full.off_site() && BackupType::Incremental.off_site() && !BackupType::Snapshot.off_site());
        assert!(TopoGoal::AllVmsBackedUp.describe().contains("incremental or a full"));
    }

    // ---- replicas and the loss of a site

    /// Two data centers, each with a host and a domain; `vm1` runs in the first with its disk on `nfs1`.
    fn two_sites() -> Topology {
        let mut t = Topology::default();
        put(&mut t, "engine", Kind::Engine);
        link(&mut t, &[]);
        for n in ["1", "2"] {
            let (dc, cl, h, m, d) = (format!("dc{n}"), format!("cl{n}"), format!("h{n}"), format!("mgmt{n}"), format!("nfs{n}"));
            put(&mut t, &dc, Kind::DataCenter);
            put(&mut t, &cl, Kind::Cluster);
            put(&mut t, &h, Kind::Host);
            put_with(&mut t, &m, Kind::Network, &[("role", Param::Str("management".into()))]);
            put(&mut t, &d, Kind::StorageDomain);
            let edges = [("engine", &dc), (&dc, &cl), (&cl, &h), (&dc, &m), (&m, &cl), ("engine", &m), (&m, &h), (&dc, &d), (&d, &h)];
            for (a, b) in edges {
                t.edges.push(Edge::new(a, b));
            }
        }
        vm(&mut t, "vm1", Some("h1"), 4, false);
        t.edges.retain(|e| !(e.from == "nfs" && e.to == "vm1")); // vm() links a domain called "nfs"; here it is "nfs1"
        link(&mut t, &[("nfs1", "vm1")]);
        t
    }

    #[test]
    fn the_loss_of_a_site_leaves_what_has_a_replica_elsewhere() {
        en();
        let mut t = two_sites();
        assert!(problems(&t).is_empty(), "{:?}", problems(&t).iter().map(|p| p.text.clone()).collect::<Vec<_>>());
        assert!(evaluate(&t).vms.iter().all(|v| v.status == VmStatus::Running));
        assert!(!check(TopoGoal::SurviveSiteLoss, &t), "no replica");
        // the loss of dc1 takes its cluster, host, network, domain and the VM's host link with it
        let after = t.without_dc("dc1");
        assert!(["dc1", "cl1", "h1", "mgmt1", "nfs1"].iter().all(|id| after.node(id).is_none()));
        assert!(after.node("vm1").is_some() && after.host_of_vm("vm1").is_none());
        assert!(after.node("dc2").is_some() && after.linked("dc2", "cl2"));
        assert!(evaluate(&after).dc("dc2").unwrap().status == DcStatus::Up);
        // the replica of the domain in the other data center
        link(&mut t, &[("nfs1", "nfs2")]);
        assert!(problems(&t).is_empty());
        assert!(check(TopoGoal::SurviveSiteLoss, &t));
        assert!(survives_site_loss(&t));
        // one data center is no site loss at all
        let mut single = t.without_dc("dc2");
        single.edges.retain(|e| e.to != "nfs2");
        assert!(!check(TopoGoal::SurviveSiteLoss, &single));
        // the replica must be seen by a host of an Up data center
        let mut unseen = t.clone();
        put(&mut unseen, "repl", Kind::StorageDomain);
        unseen.edges.retain(|e| !(e.from == "nfs1" && e.to == "nfs2"));
        link(&mut unseen, &[("dc2", "repl"), ("nfs1", "repl")]);
        assert!(!check(TopoGoal::SurviveSiteLoss, &unseen), "an Inactive replica domain is not a copy anyone can use");
        link(&mut unseen, &[("repl", "h2")]);
        assert!(check(TopoGoal::SurviveSiteLoss, &unseen));
        // the other data center must be Up: without its host it is not
        let mut down = t.clone();
        down.edges.retain(|e| !(e.from == "nfs2" && e.to == "h2"));
        assert!(!check(TopoGoal::SurviveSiteLoss, &down));
        // every data center that hosts VMs is lost in turn: a VM in dc2 without a replica breaks the goal
        let mut both = t.clone();
        vm(&mut both, "vm2", Some("h2"), 4, false);
        both.edges.retain(|e| !(e.from == "nfs" && e.to == "vm2")); // vm() links a domain called "nfs"; here it is "nfs2"
        link(&mut both, &[("nfs2", "vm2")]);
        assert!(problems(&both).is_empty(), "{:?}", problems(&both).iter().map(|p| p.text.clone()).collect::<Vec<_>>());
        assert!(!check(TopoGoal::SurviveSiteLoss, &both));
        put(&mut both, "nfs3", Kind::StorageDomain);
        link(&mut both, &[("dc1", "nfs3"), ("nfs3", "h1")]);
        // a replica of a replica is refused, so nfs2 cannot be the primary while it is a replica
        assert_eq!(connect_error(&both, "nfs2", "nfs3").unwrap(), "a replica is a copy: it cannot be replicated further");
        // a replica of dc2's own domain, in dc1: a second domain of dc2 carries it the other way round
        let mut swapped = two_sites();
        vm(&mut swapped, "vm2", Some("h2"), 4, false);
        swapped.edges.retain(|e| !(e.from == "nfs" && e.to == "vm2"));
        link(&mut swapped, &[("nfs2", "vm2")]);
        put(&mut swapped, "dr1", Kind::StorageDomain);
        put(&mut swapped, "dr2", Kind::StorageDomain);
        link(&mut swapped, &[("dc1", "dr1"), ("dr1", "h1"), ("dc2", "dr2"), ("dr2", "h2"), ("nfs1", "dr2"), ("nfs2", "dr1")]);
        assert!(problems(&swapped).is_empty());
        assert!(check(TopoGoal::SurviveSiteLoss, &swapped), "each site has the copy of the other one");
        swapped.edges.retain(|e| !(e.from == "nfs2" && e.to == "dr1"));
        assert!(!check(TopoGoal::SurviveSiteLoss, &swapped), "dc2 has no copy in dc1 any more");
        // a VM without a disk is not recoverable
        let mut diskless = t.clone();
        diskless.edges.retain(|e| e.to != "vm1" || e.from.starts_with('h'));
        assert!(!check(TopoGoal::SurviveSiteLoss, &diskless));
        // a VM whose disk is on a domain that survives needs no replica
        let mut elsewhere = t.clone();
        elsewhere.edges.retain(|e| e.to != "vm1" || e.from.starts_with('h'));
        link(&mut elsewhere, &[("nfs2", "vm1")]);
        elsewhere.edges.retain(|e| !(e.from == "nfs1" && e.to == "nfs2"));
        // vm1 runs on h1 (dc1) with the disk in dc2: the losing of dc1 leaves the disk
        assert!(evaluate(&elsewhere).vm("vm1").unwrap().status == VmStatus::Down, "the disk is in another data center than the host");
        assert!(check(TopoGoal::SurviveSiteLoss, &elsewhere));
    }

    // ---- the rules of the new links

    #[test]
    fn the_new_links_follow_their_cardinality_rules() {
        en();
        let mut t = lab(&[("h1", 16), ("h2", 16)]);
        vm(&mut t, "vm1", Some("h1"), 4, false);
        for (id, kind) in [
            ("fa1", Kind::FenceAgent),
            ("fa2", Kind::FenceAgent),
            ("g1", Kind::AffinityGroup),
            ("g2", Kind::AffinityGroup),
            ("b1", Kind::Backup),
            ("b2", Kind::Backup),
            ("u1", Kind::User),
            ("u2", Kind::User),
            ("p1", Kind::Permission),
            ("nfs2", Kind::StorageDomain),
            ("nfs3", Kind::StorageDomain),
        ] {
            put(&mut t, id, kind);
        }
        // directions
        assert_eq!(virtlab::ovirt_topo::rel(Kind::FenceAgent, Kind::Host), Some(Rel::Fence));
        assert_eq!(virtlab::ovirt_topo::rel(Kind::AffinityGroup, Kind::Vm), Some(Rel::Affine));
        assert_eq!(virtlab::ovirt_topo::rel(Kind::Vm, Kind::Backup), Some(Rel::BackupOf));
        assert_eq!(virtlab::ovirt_topo::rel(Kind::User, Kind::Permission), Some(Rel::Grants));
        assert_eq!(virtlab::ovirt_topo::rel(Kind::StorageDomain, Kind::StorageDomain), Some(Rel::Replica));
        for k in [Kind::DataCenter, Kind::Cluster, Kind::Host, Kind::Vm, Kind::StorageDomain, Kind::Network] {
            assert_eq!(virtlab::ovirt_topo::rel(Kind::Permission, k), Some(Rel::OnObject), "{k:?}");
        }
        for k in [Kind::Engine, Kind::User, Kind::Backup, Kind::FenceAgent, Kind::AffinityGroup, Kind::Permission] {
            assert_eq!(virtlab::ovirt_topo::rel(Kind::Permission, k), None, "{k:?}");
        }
        assert_eq!(virtlab::ovirt_topo::rel(Kind::Host, Kind::FenceAgent), None, "the direction is fixed");
        // a host has one agent; an agent may serve several hosts
        link(&mut t, &[("fa1", "h1")]);
        assert_eq!(connect_error(&t, "fa2", "h1").unwrap(), "a host has one fence agent");
        assert!(connect_error(&t, "fa1", "h2").is_none());
        // a VM in several groups, a group of several VMs, a backup of several VMs, a VM with several backups
        link(&mut t, &[("g1", "vm1")]);
        assert!(connect_error(&t, "g2", "vm1").is_none());
        assert!(connect_error(&t, "vm1", "b1").is_none());
        link(&mut t, &[("vm1", "b1")]);
        assert!(connect_error(&t, "vm1", "b2").is_none());
        assert_eq!(connect_error(&t, "vm1", "b1").unwrap(), "these objects are already linked");
        // a permission belongs to one user and applies to one object
        link(&mut t, &[("u1", "p1")]);
        assert_eq!(connect_error(&t, "u2", "p1").unwrap(), "a permission belongs to one user");
        assert!(connect_error(&t, "p1", "cl1").is_none());
        link(&mut t, &[("p1", "cl1")]);
        assert_eq!(connect_error(&t, "p1", "h1").unwrap(), "a permission applies to one object");
        // replicas: a different domain, one primary, no chains
        assert_eq!(connect_error(&t, "nfs", "nfs").unwrap(), "an object cannot be linked to itself");
        assert!(connect_error(&t, "nfs", "nfs2").is_none());
        link(&mut t, &[("nfs", "nfs2")]);
        assert_eq!(connect_error(&t, "nfs3", "nfs2").unwrap(), "a domain is the replica of one primary domain only");
        assert!(connect_error(&t, "nfs", "nfs3").is_none(), "a primary may have several replicas");
        assert_eq!(connect_error(&t, "nfs2", "nfs3").unwrap(), "a replica is a copy: it cannot be replicated further");
        assert_eq!(connect_error(&t, "nfs3", "nfs").unwrap(), "a replica is a copy: it cannot be replicated further");
        assert_eq!(connect_error(&t, "nfs2", "nfs").unwrap(), "a replica is a copy: it cannot be replicated further");
        assert!(problems(&t).is_empty());
        // a hand-made board with such links is refused and pruned back
        let mut bad = t.clone();
        link(&mut bad, &[("fa2", "h1"), ("u2", "p1"), ("p1", "h1"), ("nfs2", "nfs2")]);
        let texts: Vec<String> = problems(&bad).into_iter().map(|p| p.text).collect();
        assert_eq!(texts.len(), 4, "{texts:?}");
        assert_eq!(prune(&mut bad), 4);
        assert_eq!(bad, t);
        // a chain of replicas is refused on both of its links; pruning drops the first one and the rest is fine
        let mut chain = t.clone();
        link(&mut chain, &[("nfs2", "nfs3")]);
        assert_eq!(problems(&chain).len(), 2);
        assert_eq!(prune(&mut chain), 1);
        assert!(problems(&chain).is_empty() && chain.linked("nfs2", "nfs3"));
        // removing an object takes its links with it
        let mut gone = t.clone();
        gone.nodes.retain(|n| n.id != "p1");
        assert!(!problems(&gone).is_empty(), "dangling links");
        prune(&mut gone);
        assert!(problems(&gone).is_empty());
        assert!(gone.edges.iter().all(|e| e.from != "p1" && e.to != "p1"));
        // the board can hold the new kinds
        assert!(add_error(&t, Kind::User, 60).is_none());
    }

    // ---- permissions

    /// `dc1 ⊃ cl1 ⊃ h1 ⊃ vm1`, a network and a domain in `dc1`, and the same in `dc2` (`cl2`, `h2`, `vm2`, `net2`, `dom2`).
    fn estate() -> Topology {
        let mut t = Topology::default();
        for n in ["1", "2"] {
            for (p, k) in [("dc", Kind::DataCenter), ("cl", Kind::Cluster), ("h", Kind::Host), ("vm", Kind::Vm), ("net", Kind::Network), ("dom", Kind::StorageDomain)] {
                put(&mut t, &format!("{p}{n}"), k);
            }
            let id = |p: &str| format!("{p}{n}");
            for (a, b) in [("dc", "cl"), ("cl", "h"), ("h", "vm"), ("dc", "net"), ("dc", "dom")] {
                t.edges.push(Edge::new(&id(a), &id(b)));
            }
        }
        t
    }

    fn grant(t: &mut Topology, user: &str, perm: &str, role: PermRole, on: &str) {
        if t.node(user).is_none() {
            put(t, user, Kind::User);
        }
        put_with(t, perm, Kind::Permission, &[("role", Param::Str(role.as_str().into()))]);
        link(t, &[(user, perm), (perm, on)]);
    }

    #[test]
    fn the_role_table() {
        en();
        // View, RunVm, EditVm, ManageHost, ManageCluster, ManageDataCenter, ManageStorage, ManageNetwork
        let table = [
            (PermRole::SuperUser, "11111111"),
            (PermRole::DataCenterAdmin, "11111111"),
            (PermRole::ClusterAdmin, "11111000"),
            (PermRole::HostAdmin, "11110000"),
            (PermRole::UserRole, "11000000"),
        ];
        assert_eq!(
            Action::ALL.map(|a| a.label()),
            ["view", "run VMs", "edit VMs", "manage hosts", "manage clusters", "manage data centers", "manage storage", "manage networks"]
        );
        for (role, row) in table {
            let bits: String = Action::ALL.iter().map(|a| if role.allows(*a) { '1' } else { '0' }).collect();
            assert_eq!(bits, row, "{role:?}");
        }
        // the table holds on the whole subtree of the object, and nowhere else
        let cases = [
            ("dc1", vec!["dc1", "cl1", "h1", "vm1", "net1", "dom1"], vec!["dc2", "cl2", "h2", "vm2", "net2", "dom2"]),
            ("cl1", vec!["cl1", "h1", "vm1"], vec!["dc1", "net1", "dom1", "h2", "vm2", "cl2"]),
            ("h1", vec!["h1", "vm1"], vec!["cl1", "dc1", "net1", "dom1", "h2", "vm2"]),
            ("vm1", vec!["vm1"], vec!["h1", "cl1", "dc1", "vm2", "net1", "dom1"]),
            ("net1", vec!["net1"], vec!["dc1", "cl1", "h1", "vm1", "dom1", "net2"]),
            ("dom1", vec!["dom1"], vec!["dc1", "cl1", "h1", "vm1", "net1", "dom2"]),
        ];
        for (on, inside, outside) in cases {
            for (role, _) in table {
                let mut t = estate();
                grant(&mut t, "u", "p", role, on);
                for a in Action::ALL {
                    for o in &inside {
                        assert_eq!(user_can(&t, "u", a, o), role.allows(a), "{role:?} on {on}: {a:?} {o}");
                    }
                    for o in &outside {
                        assert!(!user_can(&t, "u", a, o), "{role:?} on {on}: {a:?} outside, {o}");
                    }
                }
            }
        }
    }

    #[test]
    fn permissions_are_inherited_down_the_hierarchy_by_placement() {
        en();
        let mut t = estate();
        grant(&mut t, "alice", "p1", PermRole::HostAdmin, "h1");
        grant(&mut t, "bob", "p2", PermRole::ClusterAdmin, "cl1");
        grant(&mut t, "carol", "p3", PermRole::UserRole, "vm1");
        grant(&mut t, "dave", "p4", PermRole::DataCenterAdmin, "dc2");
        assert!(user_can(&t, "alice", Action::EditVm, "vm1"), "the VM is placed on the host");
        assert!(!user_can(&t, "alice", Action::ManageCluster, "cl1"));
        assert!(user_can(&t, "bob", Action::ManageHost, "h1"));
        assert!(!user_can(&t, "bob", Action::ManageStorage, "dom1"), "storage hangs from the data center, not from the cluster");
        assert!(user_can(&t, "carol", Action::RunVm, "vm1") && !user_can(&t, "carol", Action::EditVm, "vm1"));
        assert!(!user_can(&t, "carol", Action::View, "h1"), "a permission never reaches up");
        assert!(user_can(&t, "dave", Action::ManageNetwork, "net2") && !user_can(&t, "dave", Action::View, "net1"));
        assert_eq!(ancestors(&t, "vm1"), ["vm1", "h1", "cl1", "dc1"]);
        assert_eq!(ancestors(&t, "net2"), ["net2", "dc2"]);
        assert_eq!(ancestors(&t, "dom1"), ["dom1", "dc1"]);
        assert!(ancestors(&t, "nobody").is_empty());
        // moving the VM to another host moves who is its administrator
        t.edges.retain(|e| !(e.from == "h1" && e.to == "vm1"));
        link(&mut t, &[("h2", "vm1")]);
        assert!(!user_can(&t, "alice", Action::EditVm, "vm1"));
        assert!(!user_can(&t, "bob", Action::RunVm, "vm1"));
        assert!(user_can(&t, "dave", Action::EditVm, "vm1"), "dc2 now holds it");
        assert!(user_can(&t, "carol", Action::RunVm, "vm1"), "her permission is on the VM itself");
        // several permissions add up, and a permission without an object grants nothing
        grant(&mut t, "alice", "p5", PermRole::UserRole, "dc1");
        assert!(user_can(&t, "alice", Action::View, "dom1"));
        assert!(!user_can(&t, "alice", Action::ManageStorage, "dom1"));
        put_with(&mut t, "loose", Kind::Permission, &[("role", Param::Str("SuperUser".into()))]);
        link(&mut t, &[("erin", "loose")].map(|(_, b)| ("alice", b)));
        assert!(!user_can(&t, "alice", Action::ManageStorage, "dom1"));
        // unknown users and objects
        assert!(!user_can(&t, "nobody", Action::View, "vm1"));
        assert!(!user_can(&t, "alice", Action::View, "nothing"));
        assert!(!user_can(&t, "vm1", Action::View, "vm1"), "only a user has permissions");
    }

    #[test]
    fn user_goals_check_both_ways() {
        en();
        let mut t = estate();
        grant(&mut t, "alice", "p1", PermRole::HostAdmin, "h1");
        let can = |u: &str, a: Action, o: &str| TopoGoal::UserCan { user: u.into(), action: a, object: o.into() };
        let cannot = |u: &str, a: Action, o: &str| TopoGoal::UserCannot { user: u.into(), action: a, object: o.into() };
        assert!(check(can("alice", Action::EditVm, "vm1"), &t));
        assert!(!check(cannot("alice", Action::EditVm, "vm1"), &t));
        assert!(check(cannot("alice", Action::ManageCluster, "cl1"), &t));
        assert!(!check(can("alice", Action::ManageCluster, "cl1"), &t));
        // a goal about something that is not there is neither true nor false
        assert!(!check(cannot("nobody", Action::View, "vm1"), &t), "UserCannot needs the user to exist");
        assert!(!check(cannot("alice", Action::View, "ghost"), &t), "and the object");
        assert!(!check(cannot("vm1", Action::View, "vm1"), &t), "and the user to be a user");
        assert!(!check(can("nobody", Action::View, "vm1"), &t));
        // the sentences use the names on the board
        t.nodes.iter_mut().find(|n| n.id == "alice").unwrap().name = "Alice".into();
        t.nodes.iter_mut().find(|n| n.id == "vm1").unwrap().name = "web-1".into();
        assert_eq!(can("alice", Action::RunVm, "vm1").describe_for(&t), "“Alice” can run VMs on “web-1”");
        assert_eq!(cannot("alice", Action::ManageHost, "vm1").describe_for(&t), "“Alice” cannot manage hosts on “web-1”");
        assert_eq!(can("alice", Action::View, "vm1").describe(), "“alice” can view on “vm1”", "without a board the identifiers are shown");
    }

    // ---- precise goals and the shape of the goals in data files

    #[test]
    fn precise_goals_name_the_object() {
        en();
        let mut t = lab(&[("h1", 16)]);
        vm(&mut t, "vm1", Some("h1"), 8, true);
        let param = |id: &str, key: &str, v: &str| TopoGoal::ParamOf { id: id.into(), key: key.into(), value: v.into() };
        assert!(check(param("vm1", "ha", "true"), &t));
        assert!(check(param("vm1", "mem", "8"), &t));
        assert!(check(param("h1", "maintenance", "false"), &t), "the default counts");
        assert!(!check(param("h1", "mem", "32"), &t));
        assert!(!check(param("nobody", "mem", "8"), &t));
        assert!(check(TopoGoal::Param { node: Kind::Vm, key: "ha".into(), value: "true".into() }, &t), "the old goal is an any-object check");
        assert_eq!(param("vm1", "ha", "true").describe_for(&t), "“vm1” has ha = true");
        let linked = TopoGoal::Linked { from: "cl1".into(), to: "h1".into() };
        assert!(check(linked.clone(), &t));
        assert!(!check(TopoGoal::Linked { from: "h1".into(), to: "cl1".into() }, &t), "the direction is the model's");
        assert_eq!(linked.describe_for(&t), "“cl1” → “h1” are linked");
        assert!(check(TopoGoal::HostInCluster { host: "h1".into(), cluster: "cl1".into() }, &t));
        assert!(!check(TopoGoal::HostInCluster { host: "h1".into(), cluster: "dc1".into() }, &t));
        assert!(!check(TopoGoal::HostInCluster { host: "h2".into(), cluster: "cl1".into() }, &t));
        t.nodes.iter_mut().find(|n| n.id == "h1").unwrap().name = "host-1".into();
        assert_eq!(
            TopoGoal::HostInCluster { host: "h1".into(), cluster: "cl1".into() }.describe_for(&t),
            "the host “host-1” is a member of the cluster “cl1”"
        );
    }

    #[test]
    fn goals_have_the_documented_json_shape() {
        let shape = |g: TopoGoal| serde_json::to_value(g).unwrap();
        assert_eq!(shape(TopoGoal::HaRestart), json!({"kind": "ha_restart"}));
        assert_eq!(shape(TopoGoal::EvacuationPossible), json!({"kind": "evacuation_possible"}));
        assert_eq!(shape(TopoGoal::AllVmsBackedUp), json!({"kind": "all_vms_backed_up"}));
        assert_eq!(shape(TopoGoal::RestorableAfterDomainLoss), json!({"kind": "restorable_after_domain_loss"}));
        assert_eq!(shape(TopoGoal::SurviveSiteLoss), json!({"kind": "survive_site_loss"}));
        assert_eq!(
            shape(TopoGoal::UserCan { user: "u1".into(), action: Action::RunVm, object: "vm1".into() }),
            json!({"kind": "user_can", "user": "u1", "action": "run_vm", "object": "vm1"})
        );
        assert_eq!(
            shape(TopoGoal::UserCannot { user: "u1".into(), action: Action::ManageDataCenter, object: "dc1".into() }),
            json!({"kind": "user_cannot", "user": "u1", "action": "manage_data_center", "object": "dc1"})
        );
        assert_eq!(
            shape(TopoGoal::ParamOf { id: "vm1".into(), key: "ha".into(), value: "true".into() }),
            json!({"kind": "param_of", "id": "vm1", "key": "ha", "value": "true"})
        );
        assert_eq!(shape(TopoGoal::Linked { from: "a".into(), to: "b".into() }), json!({"kind": "linked", "from": "a", "to": "b"}));
        assert_eq!(
            shape(TopoGoal::HostInCluster { host: "h1".into(), cluster: "cl1".into() }),
            json!({"kind": "host_in_cluster", "host": "h1", "cluster": "cl1"})
        );
        assert_eq!(shape(TopoGoal::OpOk { op: OpKind::Fence }), json!({"kind": "op_ok", "op": "fence"}));
        assert_eq!(serde_json::to_value(Op::Fence { host: "h1".into() }).unwrap(), json!({"op": "fence", "host": "h1"}));
        // and they read back
        let back: TopoGoal = serde_json::from_value(json!({"kind": "user_can", "user": "u", "action": "manage_storage", "object": "d"})).unwrap();
        assert_eq!(back, TopoGoal::UserCan { user: "u".into(), action: Action::ManageStorage, object: "d".into() });
        // kinds and relations in data files
        let kinds: Vec<String> = Kind::ALL.iter().map(|k| k.as_str().to_string()).collect();
        for k in ["fence_agent", "affinity_group", "backup", "user", "permission"] {
            assert!(kinds.contains(&k.to_string()), "{k}");
            let parsed: Kind = serde_json::from_value(json!(k)).unwrap();
            assert_eq!(parsed.as_str(), k);
        }
        assert_eq!(serde_json::to_value(Rel::BackupOf).unwrap(), json!("backup_of"));
        assert_eq!(serde_json::to_value(Rel::OnObject).unwrap(), json!("on_object"));
    }

    #[test]
    fn a_scenario_with_the_new_kinds_goes_through_the_server_check() {
        en();
        // a one-off scenario on a hand-made board: the mechanics work inside Scenario, not only as functions
        let mut start = lab(&[("h1", 16), ("h2", 16)]);
        vm(&mut start, "vm1", Some("h1"), 4, false);
        let sc = Scenario {
            id: "ha".into(),
            title: "t".into(),
            story: "s".into(),
            goal: "g".into(),
            hint: "h".into(),
            palette: vec![Kind::FenceAgent],
            max_nodes: 24,
            start: start.clone(),
            goals: vec![TopoGoal::HaRestart, TopoGoal::Healthy],
        };
        assert!(!sc.reached(&start));
        let mut done = start.clone();
        done.nodes.iter_mut().find(|n| n.id == "vm1").unwrap().params.insert("ha".into(), Param::Bool(true));
        fence(&mut done, "fence1", "h1");
        assert!(sc.reached(&done));
        // the student may add only the kinds of the palette
        let mut cheat = done.clone();
        put(&mut cheat, "u", Kind::User);
        assert!(sc.invalid(&cheat).unwrap().contains("not available"));
    }
}

// ---------------------------------------------------------------- layout

#[test]
fn new_objects_take_free_places_in_their_columns() {
    use virtlab::ovirt_topo::{column, next_pos, NODE_H, NODE_W};
    en();
    let overlap = |a: &Node, b: &Node| (a.x - b.x).abs() < NODE_W && (a.y - b.y).abs() < NODE_H;
    // six networks and three domains in turn, plus one object of every other kind and a few more of the busy ones
    let mut t = Topology::default();
    let order = [
        Kind::Network, Kind::Network, Kind::Network, Kind::Network, Kind::StorageDomain, Kind::Network, Kind::Network,
        Kind::StorageDomain, Kind::StorageDomain, Kind::Engine, Kind::DataCenter, Kind::DataCenter, Kind::DataCenter,
        Kind::DataCenter, Kind::DataCenter, Kind::User, Kind::User, Kind::Permission, Kind::Permission, Kind::Cluster,
        Kind::Host, Kind::Host, Kind::Host, Kind::Host, Kind::Host, Kind::Host, Kind::FenceAgent, Kind::FenceAgent,
        Kind::AffinityGroup, Kind::AffinityGroup, Kind::Vm, Kind::Vm, Kind::Backup, Kind::Backup,
    ];
    for (i, k) in order.into_iter().enumerate() {
        let (x, y) = next_pos(&t, k);
        assert_eq!(x, column(k).0, "{k:?} stays in its column");
        t.nodes.push(Node::new(&format!("n{i}"), k, "n", x, y));
    }
    for (i, a) in t.nodes.iter().enumerate() {
        for b in &t.nodes[i + 1..] {
            assert!(!overlap(a, b), "{:?} at ({}, {}) overlaps {:?} at ({}, {})", a.kind, a.x, a.y, b.kind, b.x, b.y);
        }
    }
    // the columns of different kinds are far enough apart that their objects never touch sideways
    let xs: std::collections::BTreeSet<i64> = Kind::ALL.iter().map(|k| column(*k).0 as i64).collect();
    let xs: Vec<i64> = xs.into_iter().collect();
    assert!(xs.windows(2).all(|w| w[1] - w[0] >= NODE_W as i64), "{xs:?}");
}

#[test]
fn no_scenario_of_any_pack_has_objects_on_top_of_each_other() {
    use virtlab::ovirt_topo::{NODE_H, NODE_W};
    for (sc, reference) in all() {
        for (what, t) in [("start", &sc.start), ("reference", &reference)] {
            for (i, a) in t.nodes.iter().enumerate() {
                for b in &t.nodes[i + 1..] {
                    assert!(
                        (a.x - b.x).abs() >= NODE_W || (a.y - b.y).abs() >= NODE_H,
                        "{}/{what}: {} and {} overlap",
                        sc.id,
                        a.id,
                        b.id
                    );
                }
            }
        }
    }
}

#[test]
fn the_raw_parameter_table_agrees_with_the_specs_the_ui_draws() {
    use virtlab::ovirt_topo::{param_specs, ParamTy};
    en();
    // the model reads defaults from an allocation-free table; the specs add the captions: they must describe the same parameters
    for k in Kind::ALL {
        let n = Node::new("x", k, "x", 0.0, 0.0);
        for s in param_specs(k) {
            assert_eq!(n.param_text(s.key), s.default_text(), "{k:?}.{}", s.key);
            match &s.ty {
                ParamTy::Select(options) => {
                    for o in options {
                        let set = n.clone().with_param(s.key, Param::Str(o.value.into()));
                        assert_eq!(set.param_text(s.key), o.value, "{k:?}.{} accepts {}", s.key, o.value);
                        assert!(virtlab::ovirt_topo::param_error(&set).is_none());
                    }
                    let bad = n.clone().with_param(s.key, Param::Str("nonsense".into()));
                    assert!(virtlab::ovirt_topo::param_error(&bad).is_some());
                    assert_eq!(bad.param_text(s.key), s.default_text());
                    assert!(virtlab::ovirt_topo::param_error(&n.clone().with_param(s.key, Param::Bool(true))).is_some());
                }
                ParamTy::Bool => {
                    for b in [true, false] {
                        let set = n.clone().with_param(s.key, Param::Bool(b));
                        assert_eq!(set.param_text(s.key), b.to_string());
                        assert!(virtlab::ovirt_topo::param_error(&set).is_none());
                    }
                    assert!(virtlab::ovirt_topo::param_error(&n.clone().with_param(s.key, Param::Str("true".into()))).is_some());
                }
            }
        }
        // and nothing else is accepted
        let stray = n.clone().with_param("nonsense", Param::Bool(true));
        assert!(virtlab::ovirt_topo::param_error(&stray).is_some(), "{k:?}");
    }
}
