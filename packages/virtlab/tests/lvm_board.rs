//! LVM board: the rules of links, the derived statuses, the loss of a disk and the scenarios of every pack.

use virtlab::lvm_board::{
    add_error, auto_layout, connect_error, evacuable, evaluate, judge, lost_by_disk, pack, pack_chapter, pack_ids, param_error,
    param_specs, problems, prune, survives_disk_loss, Edge, FsStatus, Kind, LvmGoal, Node, Param, PoolStatus, PvStatus, Scenario,
    SnapStatus, Topology, VgStatus, VmStatus, VolStatus, Why, Workload,
};
use virtlab::{GoalStatus, Spec, Strictness};

fn en() {
    locales::set_locale(i18n::Locale::En);
}

fn none() -> Workload {
    Workload::default()
}

fn node(kind: Kind, id: &str) -> Node {
    Node::new(id, kind, id, 0.0, 0.0)
}

fn sized(kind: Kind, id: &str, size: &str) -> Node {
    node(kind, id).with_param("size", Param::Str(size.into()))
}

/// A disk of `gib` GiB as a physical volume `pv` in the group `vg` (extent size 4 MiB unless the group is given).
fn board(disks: &[(&str, &str)]) -> Topology {
    let mut t = Topology::default();
    t.nodes.push(node(Kind::Vg, "vg"));
    for (d, gib) in disks {
        let pv = format!("pv-{d}");
        t.nodes.push(sized(Kind::Disk, d, gib));
        t.nodes.push(node(Kind::Pv, &pv));
        t.edges.push(Edge::new(d, &pv));
        t.edges.push(Edge::new(&pv, "vg"));
    }
    t
}

fn lv(t: &mut Topology, id: &str, size: &str, mirror: &str) {
    t.nodes.push(sized(Kind::Lv, id, size).with_param("mirror", Param::Str(mirror.into())));
    t.edges.push(Edge::new("vg", id));
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
            assert!(
                !sc.title.is_empty() && !sc.story.is_empty() && !sc.goal.is_empty() && !sc.hint.is_empty(),
                "{id}/{}: texts",
                sc.id
            );
            assert!(sc.goals.len() >= 2, "{id}/{}: a scenario has at least two goals", sc.id);
            assert!(!sc.palette.is_empty(), "{id}/{}: palette", sc.id);
            // English texts only; the Russian ones live in the dictionary
            assert!(
                sc.title.chars().all(|c| !('а'..='я').contains(&c.to_ascii_lowercase())),
                "{id}/{}: Cyrillic in a key",
                sc.id
            );
        }
        // the spec validates and survives a round trip
        let spec = virtlab::builtin(id).expect("builtin");
        spec.validate().unwrap();
        let v = serde_json::to_value(&spec).unwrap();
        assert_eq!(v["sim"], "lvm_board");
        assert_eq!(serde_json::from_value::<Spec>(v).unwrap(), spec);
        assert_eq!(spec.goals().len(), scenarios.len());
    }
    assert_eq!(pack_ids().len(), 3);
    assert_eq!(pack_chapter("virt-sim-lvm-snapshots"), Some(20));
    assert!(pack("virt-sim-lvm-nope").is_none());
}

#[test]
fn the_server_check_accepts_references_and_refuses_the_rest() {
    en();
    for id in pack_ids() {
        let spec = virtlab::builtin(id).unwrap();
        let Spec::LvmBoard { scenarios, solution } = &spec else { panic!("not a board") };
        let mut submitted = serde_json::Map::new();
        for sc in scenarios {
            submitted.insert(sc.id.clone(), serde_json::to_value(&solution[&sc.id]).unwrap());
        }
        let v = virtlab::verify_with(&spec, &serde_json::Value::Object(submitted.clone()), Strictness::Strict);
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
    let (scenarios, solution) = pack("virt-sim-lvm-grow").unwrap();
    let sc = &scenarios[1];
    let reference = serde_json::to_string(&solution[&sc.id]).unwrap();
    let j = judge("virt-sim-lvm-grow", &sc.id, &reference).unwrap();
    assert!(j.reached && j.invalid.is_none() && j.goals.iter().all(|g| g.ok));
    let start = serde_json::to_string(&sc.start).unwrap();
    let j = judge("virt-sim-lvm-grow", &sc.id, &start).unwrap();
    assert!(!j.reached && j.invalid.is_none() && j.goals.iter().any(|g| !g.ok));
    // positionless boards are accepted, other objects are not
    let mut bare = sc.start.clone();
    for n in &mut bare.nodes {
        n.x = 0.0;
        n.y = 0.0;
    }
    assert!(judge("virt-sim-lvm-grow", &sc.id, &serde_json::to_string(&bare).unwrap()).is_ok());
    let mut more = sc.start.clone();
    more.nodes.push(node(Kind::Lv, "extra"));
    let j = judge("virt-sim-lvm-grow", &sc.id, &serde_json::to_string(&more).unwrap()).unwrap();
    assert!(!j.reached && j.invalid.is_some());
    assert!(judge("virt-sim-lvm-grow", "nope", "{}").is_err());
    assert!(judge("virt-sim-lvm-grow", &sc.id, "[]").is_err());
}

// ---------------------------------------------------------------- rules of links

#[test]
fn links_follow_the_table_and_explain_refusals() {
    en();
    let mut t = board(&[("d1", "50")]);
    lv(&mut t, "a", "10", "1");
    t.nodes.push(node(Kind::Fs, "fs"));
    t.nodes.push(node(Kind::Snapshot, "s"));
    t.nodes.push(node(Kind::Vm, "vm"));
    assert_eq!(connect_error(&t, "vg", "a"), Some("these objects are already linked".to_string()));
    assert!(connect_error(&t, "a", "vg").unwrap().contains("not linked directly"));
    assert!(connect_error(&t, "d1", "vg").unwrap().contains("not linked directly"));
    assert!(connect_error(&t, "a", "a").unwrap().contains("itself"));
    assert!(connect_error(&t, "nope", "a").unwrap().contains("unknown"));
    // a volume holds one filesystem and belongs to one VM; a filesystem sits on one volume
    assert!(connect_error(&t, "a", "fs").is_none());
    t.edges.push(Edge::new("a", "fs"));
    lv(&mut t, "b", "10", "1");
    assert_eq!(connect_error(&t, "b", "fs").unwrap(), "a filesystem sits on one volume");
    t.nodes.push(node(Kind::Fs, "fs2"));
    assert_eq!(connect_error(&t, "a", "fs2").unwrap(), "a volume holds one filesystem");
    assert!(connect_error(&t, "a", "vm").is_none());
    t.edges.push(Edge::new("a", "vm"));
    t.nodes.push(node(Kind::Vm, "vm2"));
    assert_eq!(connect_error(&t, "a", "vm2").unwrap(), "a volume is the disk of one VM");
    // a VM may have several disks, a snapshot has one origin
    assert!(connect_error(&t, "b", "vm").is_none());
    t.edges.push(Edge::new("a", "s"));
    assert_eq!(connect_error(&t, "b", "s").unwrap(), "a snapshot has one origin");
}

#[test]
fn physical_volumes_and_groups_follow_the_single_parent_rules() {
    en();
    let mut t = board(&[("d1", "50")]);
    t.nodes.push(node(Kind::Vg, "vg2"));
    t.nodes.push(node(Kind::Pv, "pv2"));
    t.nodes.push(node(Kind::Disk, "d2"));
    assert_eq!(connect_error(&t, "pv-d1", "vg2").unwrap(), "a physical volume belongs to one volume group");
    assert_eq!(connect_error(&t, "d1", "pv2").unwrap(), "a disk is used as one physical volume");
    t.edges.push(Edge::new("d2", "pv2"));
    t.nodes.push(node(Kind::Pv, "pv3"));
    assert_eq!(connect_error(&t, "d2", "pv3").unwrap(), "a disk is used as one physical volume");
    // a physical volume is made of one disk
    assert_eq!(connect_error(&t, "d1", "pv2").unwrap(), "a physical volume is made of one disk");
    // thin volumes: one pool; logical volumes and pools: one group
    t.nodes.push(node(Kind::ThinPool, "p1"));
    t.nodes.push(node(Kind::ThinPool, "p2"));
    t.nodes.push(node(Kind::ThinLv, "t"));
    t.edges.push(Edge::new("p1", "t"));
    assert_eq!(connect_error(&t, "p2", "t").unwrap(), "a thin volume belongs to one thin pool");
    t.edges.push(Edge::new("vg", "p1"));
    assert_eq!(connect_error(&t, "vg2", "p1").unwrap(), "a thin pool belongs to one volume group");
    // limits
    assert!(add_error(&t, Kind::Lv, 24).is_none());
    assert!(add_error(&t, Kind::Lv, t.nodes.len()).unwrap().contains("at most"));
}

#[test]
fn removing_an_object_drops_what_depends_on_it() {
    en();
    let mut t = board(&[("d1", "50")]);
    lv(&mut t, "a", "10", "1");
    t.nodes.retain(|n| n.id != "vg");
    assert!(!problems(&t).is_empty(), "the links to the removed group dangle");
    let dropped = prune(&mut t);
    assert_eq!(dropped, 2, "the membership of the physical volume and the volume of the group");
    assert!(problems(&t).is_empty());
}

#[test]
fn problems_catch_a_hand_made_board() {
    en();
    let mut t = board(&[("d1", "50")]);
    t.edges.push(Edge::new("d1", "pv-d1"));
    t.edges.push(Edge::new("vg", "d1"));
    t.edges.push(Edge::new("ghost", "vg"));
    let texts: Vec<String> = problems(&t).into_iter().map(|p| p.text).collect();
    assert!(texts.contains(&"these objects are already linked".to_string()), "{texts:?}");
    assert!(texts.contains(&"in LVM these objects are not linked directly".to_string()));
    assert!(texts.contains(&"a link leads to an unknown object".to_string()));
    let mut dup = board(&[("d1", "50")]);
    dup.nodes.push(node(Kind::Disk, "d1"));
    assert!(problems(&dup).iter().any(|p| p.text.contains("unique")));
    let mut many = Topology::default();
    for i in 0..41 {
        many.nodes.push(node(Kind::Disk, &format!("d{i}")));
    }
    assert!(problems(&many).iter().any(|p| p.text.contains("at most 40")));
    let mut bad_pos = board(&[("d1", "50")]);
    bad_pos.nodes[0].x = f64::INFINITY;
    assert!(!problems(&bad_pos).is_empty());
}

#[test]
fn parameters_are_checked_against_the_table() {
    en();
    let mut n = node(Kind::Lv, "a");
    assert_eq!(n.param_text("size"), "10");
    assert_eq!(n.param_text("mirror"), "1");
    assert!(param_error(&n).is_none());
    n.params.insert("size".into(), Param::Str("7".into()));
    assert!(param_error(&n).unwrap().contains("not a valid value"));
    n.params.insert("size".into(), Param::Str("20".into()));
    n.params.insert("colour".into(), Param::Str("red".into()));
    assert!(param_error(&n).unwrap().contains("not a parameter"));
    // a value that is not allowed reads as the default
    let mut bad = node(Kind::Disk, "d");
    bad.params.insert("size".into(), Param::Str("7".into()));
    assert_eq!(bad.size_gib(), 100);
    assert!(node(Kind::Pv, "p").params.is_empty() && param_specs(Kind::Pv).is_empty());
    // the typed table and the allocation-free one agree
    for kind in Kind::ALL {
        for spec in param_specs(kind) {
            let n = node(kind, "x");
            assert_eq!(n.param_text(spec.key), spec.default_text(), "{kind:?}.{}", spec.key);
            for o in spec.options() {
                let ok = node(kind, "x").with_param(spec.key, Param::Str(o.value.into()));
                assert!(param_error(&ok).is_none(), "{kind:?}.{}={}", spec.key, o.value);
            }
        }
    }
}

// ---------------------------------------------------------------- statuses

#[test]
fn extents_follow_the_formula_of_chapter_16() {
    en();
    // a physical volume of S MiB has (S - 1) // pe usable extents
    for (gib, pe, extents) in [(50, "4", 12799), (10, "4", 2559), (100, "32", 3199), (200, "128", 1599)] {
        let mut t = board(&[("d1", &gib.to_string())]);
        t.nodes.iter_mut().find(|n| n.id == "vg").unwrap().params.insert("pe".into(), Param::Str(pe.into()));
        let ev = evaluate(&t, &none());
        assert_eq!(ev.pv("pv-d1").unwrap().extents, extents, "{gib} GiB at {pe} MiB");
        assert_eq!(ev.vg("vg").unwrap().total, extents);
    }
    // a physical volume in no group counts in extents of 4 MiB
    let mut t = board(&[("d1", "50")]);
    t.edges.retain(|e| e.to != "vg");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.pv("pv-d1").unwrap().extents, 12799);
    assert_eq!(ev.pv("pv-d1").unwrap().status, PvStatus::NoGroup);
    assert_eq!(ev.vg("vg").unwrap().status, VgStatus::Empty);
    // without a disk a physical volume has nothing
    let mut t = board(&[("d1", "50")]);
    t.edges.retain(|e| e.from != "d1");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.pv("pv-d1").unwrap().status, PvStatus::NoDisk);
    assert_eq!(ev.pv("pv-d1").unwrap().why, Some(Why::PvNoDisk));
    assert_eq!(ev.vg("vg").unwrap().total, 0);
}

#[test]
fn a_volume_that_fills_the_disk_does_not_fit_it() {
    en();
    // 50 GiB = 12800 extents, a 50 GiB disk gives 12799: the first MiB is metadata
    let mut t = board(&[("d1", "50")]);
    lv(&mut t, "a", "50", "1");
    let ev = evaluate(&t, &none());
    let a = ev.volume("a").unwrap();
    assert_eq!(a.status, VolStatus::NoSpace);
    assert_eq!(a.why, Some(Why::NoSpace { need: 12800, free: 12799 }));
    assert_eq!(a.why.as_ref().unwrap().text(), "it needs 12800 extents and the group has 12799 free");
    // a second disk is enough, the volume spans both
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "a", "50", "1");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.volume("a").unwrap().status, VolStatus::Ok);
    let pieces = &ev.placement["a"];
    assert_eq!(pieces.iter().map(|p| (p.pv.as_str(), p.extents)).collect::<Vec<_>>(), [("pv-d1", 12799), ("pv-d2", 1)]);
    assert_eq!(ev.vg("vg").unwrap().used, 12800);
    assert_eq!(ev.vg("vg").unwrap().free(), 12798);
    // the extent size rounds a size up: 1 GiB at 128 MiB is 8 extents exactly
    let mut t = board(&[("d1", "10")]);
    t.nodes.iter_mut().find(|n| n.id == "vg").unwrap().params.insert("pe".into(), Param::Str("128".into()));
    lv(&mut t, "a", "1", "1");
    assert_eq!(evaluate(&t, &none()).volume("a").unwrap().extents, 8);
    assert_eq!(evaluate(&t, &none()).vg("vg").unwrap().used, 8);
}

#[test]
fn volumes_take_space_in_the_order_of_the_board() {
    en();
    // 10 GiB disk: 2559 extents of 4 MiB; 5 GiB = 1280 extents. The first two fit, the third does not, a later small one still does
    let mut t = board(&[("d1", "10")]);
    lv(&mut t, "a", "5", "1");
    lv(&mut t, "b", "2", "1");
    lv(&mut t, "c", "5", "1");
    lv(&mut t, "d", "1", "1");
    let ev = evaluate(&t, &none());
    let s = |id: &str| ev.volume(id).unwrap().status;
    assert_eq!((s("a"), s("b"), s("c"), s("d")), (VolStatus::Ok, VolStatus::Ok, VolStatus::NoSpace, VolStatus::Ok));
    assert_eq!(ev.vg("vg").unwrap().free(), 2559 - 1280 - 512 - 256);
    // the order decides who gets the room: 5 GiB and 5 GiB do not both fit 9.99 GiB, the one that comes first does
    let mut u = board(&[("d1", "10")]);
    lv(&mut u, "c", "5", "1");
    lv(&mut u, "a", "5", "1");
    let ev = evaluate(&u, &none());
    assert_eq!((ev.volume("c").unwrap().status, ev.volume("a").unwrap().status), (VolStatus::Ok, VolStatus::NoSpace));
    assert_eq!(ev.volume("a").unwrap().why, Some(Why::NoSpace { need: 1280, free: 1279 }));
}

#[test]
fn a_mirror_needs_two_physical_volumes() {
    en();
    let mut t = board(&[("d1", "50")]);
    lv(&mut t, "a", "10", "2");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.volume("a").unwrap().status, VolStatus::NeedsTwoPvs);
    // two physical volumes: a copy on each
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "a", "10", "2");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.volume("a").unwrap().status, VolStatus::Ok);
    let legs: Vec<_> = ev.placement["a"].iter().map(|p| (p.pv.as_str(), p.leg, p.extents)).collect();
    assert_eq!(legs, [("pv-d1", 0, 2560), ("pv-d2", 1, 2560)]);
    assert_eq!(ev.vg("vg").unwrap().used, 5120);
    // no room for a copy on a second physical volume
    let mut t = board(&[("d1", "50"), ("d2", "10")]);
    lv(&mut t, "a", "20", "2");
    let ev = evaluate(&t, &none());
    assert_eq!(ev.volume("a").unwrap().status, VolStatus::NoSpace);
}

#[test]
fn the_loss_of_a_disk_takes_what_has_no_copy_left() {
    en();
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "lin", "10", "1");
    lv(&mut t, "mir", "5", "2");
    let ev = evaluate(&t, &none());
    // lin sits on pv-d1; mir has a copy on each
    assert_eq!(lost_by_disk(&t, &ev, "d1"), ["lin"]);
    assert_eq!(lost_by_disk(&t, &ev, "d2"), Vec::<String>::new());
    assert!(!survives_disk_loss(&t, &ev));
    // a linear volume that spans both disks is lost with either
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "big", "50", "1");
    let ev = evaluate(&t, &none());
    assert_eq!(lost_by_disk(&t, &ev, "d1"), ["big"]);
    assert_eq!(lost_by_disk(&t, &ev, "d2"), ["big"]);
    // all mirrored: nothing is lost
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "m1", "10", "2");
    lv(&mut t, "m2", "5", "2");
    let ev = evaluate(&t, &none());
    assert!(survives_disk_loss(&t, &ev));
    // a disk with no physical volume holds nothing; no volumes at all is not a survival
    let mut t = board(&[("d1", "50")]);
    t.nodes.push(node(Kind::Disk, "spare"));
    let ev = evaluate(&t, &none());
    assert!(lost_by_disk(&t, &ev, "spare").is_empty());
    assert!(!survives_disk_loss(&t, &ev));
    // thin volumes and snapshots go down with their pool or origin
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    t.nodes.push(sized(Kind::ThinPool, "pool", "10"));
    t.nodes.push(sized(Kind::ThinLv, "t", "20"));
    t.nodes.push(node(Kind::Snapshot, "ts"));
    t.edges.extend([Edge::new("vg", "pool"), Edge::new("pool", "t"), Edge::new("t", "ts")]);
    let ev = evaluate(&t, &none());
    assert_eq!(lost_by_disk(&t, &ev, "d1"), ["pool", "t", "ts"]);
}

#[test]
fn evacuating_counts_the_free_space_of_the_others() {
    en();
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "a", "20", "1");
    lv(&mut t, "b", "50", "1");
    // another disk makes room
    let before = evaluate(&t, &none());
    assert!(!evacuable(&t, &before, "pv-d1"));
    t.nodes.push(sized(Kind::Disk, "d3", "50"));
    t.nodes.push(node(Kind::Pv, "pv-d3"));
    t.edges.extend([Edge::new("d3", "pv-d3"), Edge::new("pv-d3", "vg")]);
    let after = evaluate(&t, &none());
    assert!(evacuable(&t, &after, "pv-d1"));
    // a physical volume in no group, a missing one, the only one
    assert!(!evacuable(&t, &after, "nope"));
    let single = board(&[("d1", "50")]);
    assert!(!evacuable(&single, &evaluate(&single, &none()), "pv-d1"), "there is nowhere to move to");
    // a copy of a mirror cannot move to the physical volume that holds the other copy
    let mut m = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut m, "m", "10", "2");
    assert!(!evacuable(&m, &evaluate(&m, &none()), "pv-d1"));
    m.nodes.push(sized(Kind::Disk, "d3", "50"));
    m.nodes.push(node(Kind::Pv, "pv-d3"));
    m.edges.extend([Edge::new("d3", "pv-d3"), Edge::new("pv-d3", "vg")]);
    assert!(evacuable(&m, &evaluate(&m, &none()), "pv-d1"));
}

#[test]
fn filesystems_follow_their_volume() {
    en();
    let mut t = board(&[("d1", "100")]);
    lv(&mut t, "a", "20", "1");
    t.nodes.push(sized(Kind::Fs, "fs", "20"));
    t.edges.push(Edge::new("a", "fs"));
    let status = |t: &Topology| evaluate(t, &none()).fs("fs").unwrap().status;
    assert_eq!(status(&t), FsStatus::Ok);
    t.nodes.iter_mut().find(|n| n.id == "fs").unwrap().params.insert("size".into(), Param::Str("10".into()));
    assert_eq!(status(&t), FsStatus::NotGrown);
    assert_eq!(
        evaluate(&t, &none()).fs("fs").unwrap().why.as_ref().unwrap().text(),
        "the filesystem is 10 GiB and the volume 20 GiB: grow the filesystem (lvextend -r does both)"
    );
    t.nodes.iter_mut().find(|n| n.id == "fs").unwrap().params.insert("size".into(), Param::Str("50".into()));
    assert_eq!(status(&t), FsStatus::TooBig);
    // a volume that does not exist (no room) takes its filesystem down
    t.nodes.iter_mut().find(|n| n.id == "a").unwrap().params.insert("size".into(), Param::Str("200".into()));
    t.nodes.iter_mut().find(|n| n.id == "fs").unwrap().params.insert("size".into(), Param::Str("200".into()));
    assert_eq!(status(&t), FsStatus::VolumeDown);
    // a filesystem on no volume
    t.edges.retain(|e| e.to != "fs");
    assert_eq!(status(&t), FsStatus::Detached);
}

#[test]
fn snapshots_overflow_when_more_changes_than_they_hold() {
    en();
    let mut t = board(&[("d1", "100")]);
    lv(&mut t, "a", "50", "1");
    t.nodes.push(sized(Kind::Snapshot, "s", "10"));
    t.edges.push(Edge::new("a", "s"));
    let eval = |changed: u32| evaluate(&t, &Workload { changed_gib: changed, written_gib: 0 }).snapshot("s").unwrap().clone();
    assert_eq!(eval(0).status, SnapStatus::Valid);
    assert_eq!(eval(8).status, SnapStatus::Valid);
    assert_eq!(eval(8).pct, 80);
    assert_eq!(eval(10).status, SnapStatus::Valid, "a snapshot that is exactly full still holds");
    assert_eq!(eval(11).status, SnapStatus::Invalid);
    assert_eq!(eval(11).why, Some(Why::Overflow { changed_gib: 11, holds_gib: 10 }));
    // a snapshot never needs more than the origin
    let mut u = board(&[("d1", "100")]);
    lv(&mut u, "a", "5", "1");
    u.nodes.push(sized(Kind::Snapshot, "s", "5"));
    u.edges.push(Edge::new("a", "s"));
    let ev = evaluate(&u, &Workload { changed_gib: 500, written_gib: 0 });
    assert_eq!(ev.snapshot("s").unwrap().status, SnapStatus::Valid);
    assert_eq!(ev.snapshot("s").unwrap().changed_gib, 5);
    // a snapshot takes room from the group; without room it does not exist
    let mut full = board(&[("d1", "10")]);
    lv(&mut full, "a", "5", "1");
    full.nodes.push(sized(Kind::Snapshot, "s", "10"));
    full.edges.push(Edge::new("a", "s"));
    let ev = evaluate(&full, &none());
    assert_eq!(ev.snapshot("s").unwrap().status, SnapStatus::NoSpace);
    // without an origin
    let mut orphan = board(&[("d1", "10")]);
    orphan.nodes.push(node(Kind::Snapshot, "s"));
    assert_eq!(evaluate(&orphan, &none()).snapshot("s").unwrap().status, SnapStatus::Orphan);
}

fn pool_board(pool_gib: &str, meta: &str, virtuals: &[&str]) -> Topology {
    let mut t = board(&[("d1", "500")]);
    t.nodes.push(sized(Kind::ThinPool, "pool", pool_gib).with_param("meta", Param::Str(meta.into())));
    t.edges.push(Edge::new("vg", "pool"));
    for (i, v) in virtuals.iter().enumerate() {
        let id = format!("t{i}");
        t.nodes.push(sized(Kind::ThinLv, &id, v));
        t.edges.push(Edge::new("pool", &id));
    }
    t
}

#[test]
fn a_thin_pool_fills_with_what_is_written() {
    en();
    let t = pool_board("50", "128", &["50", "50", "50"]);
    let at = |written: u32| evaluate(&t, &Workload { changed_gib: 0, written_gib: written }).pool("pool").unwrap().clone();
    assert_eq!((at(0).status, at(0).data_pct, at(0).meta_pct), (PoolStatus::Ok, 0, 0));
    assert_eq!(at(0).virtual_gib, 150);
    assert_eq!(at(0).overprovision_pct(), 300);
    let p = at(30);
    assert_eq!((p.data_pct, p.meta_pct, p.status), (60, 24, PoolStatus::Ok));
    assert_eq!(at(39).status, PoolStatus::Ok);
    assert_eq!(at(40).status, PoolStatus::Warn, "80% is the warning line");
    assert_eq!(at(49).status, PoolStatus::Warn);
    assert_eq!(at(50).status, PoolStatus::Full);
    assert_eq!(at(50).why, Some(Why::PoolFull { meta: false }));
    // writes beyond the virtual sizes do not exist
    assert_eq!(at(500).used_gib, 150);
    // the thin volumes follow the pool
    let ev = evaluate(&t, &Workload { changed_gib: 0, written_gib: 50 });
    assert_eq!(ev.volume("t0").unwrap().status, VolStatus::PoolFull);
    let ev = evaluate(&t, &Workload { changed_gib: 0, written_gib: 10 });
    assert_eq!(ev.volume("t0").unwrap().status, VolStatus::Ok);
    // the pool takes its data and metadata from the group: 50 GiB = 12800 extents, 128 MiB = 32
    assert_eq!(ev.vg("vg").unwrap().used, 12832);
}

#[test]
fn the_metadata_of_a_pool_can_run_out_first() {
    en();
    let t = pool_board("200", "64", &["500"]);
    let ev = evaluate(&t, &Workload { changed_gib: 0, written_gib: 70 });
    let p = ev.pool("pool").unwrap();
    assert_eq!((p.data_pct, p.meta_pct), (35, 110));
    assert_eq!(p.status, PoolStatus::Full);
    assert_eq!(p.why, Some(Why::PoolFull { meta: true }));
    assert_eq!(p.why.as_ref().unwrap().text(), "the metadata of the pool are full: writes fail");
    let ok = pool_board("200", "128", &["500"]);
    assert_eq!(evaluate(&ok, &Workload { changed_gib: 0, written_gib: 70 }).pool("pool").unwrap().status, PoolStatus::Ok);
}

#[test]
fn autoextend_grows_a_pool_while_the_group_has_room() {
    en();
    let mut t = pool_board("50", "128", &["50", "50", "50"]);
    t.nodes.iter_mut().find(|n| n.id == "pool").unwrap().params.insert("autoextend".into(), Param::Bool(true));
    let w = Workload { changed_gib: 0, written_gib: 45 };
    let p = evaluate(&t, &w).pool("pool").unwrap().clone();
    assert_eq!(p.status, PoolStatus::Ok, "90% grows by 20% to 60 GiB, which is 75%");
    assert_eq!((p.data_gib, p.data_pct), (60, 75));
    assert!(p.extended > 0);
    // without room in the group the pool stays as it is
    let mut tight = board(&[("d1", "50")]);
    tight.nodes.push(sized(Kind::ThinPool, "pool", "20").with_param("autoextend", Param::Bool(true)));
    tight.nodes.push(sized(Kind::ThinLv, "t", "50"));
    tight.edges.extend([Edge::new("vg", "pool"), Edge::new("pool", "t")]);
    let p = evaluate(&tight, &Workload { changed_gib: 0, written_gib: 19 }).pool("pool").unwrap().clone();
    assert!(p.data_gib > 20 && p.data_gib <= 50, "{}", p.data_gib);
    let p = evaluate(&tight, &Workload { changed_gib: 0, written_gib: 50 }).pool("pool").unwrap().clone();
    assert_eq!(p.status, PoolStatus::Full, "even the whole group is not enough");
    // a pool with no room at all for its first allocation does not exist
    let mut none_room = board(&[("d1", "10")]);
    none_room.nodes.push(sized(Kind::ThinPool, "pool", "50"));
    none_room.edges.push(Edge::new("vg", "pool"));
    assert_eq!(evaluate(&none_room, &none()).pool("pool").unwrap().status, PoolStatus::NoSpace);
}

#[test]
fn a_snapshot_of_a_thin_volume_shares_the_pool() {
    en();
    let mut t = pool_board("20", "128", &["50"]);
    t.nodes.push(node(Kind::Snapshot, "s"));
    t.edges.push(Edge::new("t0", "s"));
    let w = Workload { changed_gib: 10, written_gib: 15 };
    let ev = evaluate(&t, &w);
    let p = ev.pool("pool").unwrap();
    assert_eq!(p.used_gib, 25, "15 written and 10 changed under the snapshot");
    assert_eq!(p.status, PoolStatus::Full);
    assert_eq!(ev.snapshot("s").unwrap().status, SnapStatus::PoolFull);
    assert!(ev.snapshot("s").unwrap().thin);
    let mut roomy = t.clone();
    roomy.nodes.iter_mut().find(|n| n.id == "pool").unwrap().params.insert("size".into(), Param::Str("50".into()));
    let ev = evaluate(&roomy, &w);
    assert_eq!(ev.snapshot("s").unwrap().status, SnapStatus::Valid);
    assert_eq!(ev.pool("pool").unwrap().status, PoolStatus::Ok);
    // a snapshot of a thin volume takes nothing from the group
    assert_eq!(ev.vg("vg").unwrap().used, evaluate(&pool_board("50", "128", &["50"]), &w).vg("vg").unwrap().used);
}

#[test]
fn vms_need_working_volumes() {
    en();
    let mut t = board(&[("d1", "50")]);
    lv(&mut t, "a", "10", "1");
    t.nodes.push(node(Kind::Vm, "vm"));
    assert_eq!(evaluate(&t, &none()).vm("vm").unwrap().status, VmStatus::NoDisk);
    t.edges.push(Edge::new("a", "vm"));
    assert_eq!(evaluate(&t, &none()).vm("vm").unwrap().status, VmStatus::Ok);
    lv(&mut t, "huge", "200", "1");
    t.edges.push(Edge::new("huge", "vm"));
    assert_eq!(evaluate(&t, &none()).vm("vm").unwrap().status, VmStatus::Down);
}

// ---------------------------------------------------------------- goals

#[test]
fn goals_read_the_board() {
    en();
    let mut t = board(&[("d1", "100")]);
    lv(&mut t, "a", "20", "1");
    let ev = evaluate(&t, &none());
    let holds = |g: LvmGoal| g.check(&t, &ev);
    assert!(holds(LvmGoal::Healthy));
    assert!(holds(LvmGoal::VgFree { vg: None, min_gib: 70 }));
    assert!(!holds(LvmGoal::VgFree { vg: Some("vg".into()), min_gib: 80 }));
    assert!(!holds(LvmGoal::VgFree { vg: Some("nope".into()), min_gib: 1 }));
    assert!(holds(LvmGoal::LvSize { lv: Some("a".into()), min_gib: 20, count: 1 }));
    assert!(!holds(LvmGoal::LvSize { lv: Some("a".into()), min_gib: 50, count: 1 }));
    assert!(holds(LvmGoal::LvSize { lv: None, min_gib: 10, count: 1 }));
    assert!(!holds(LvmGoal::LvSize { lv: None, min_gib: 10, count: 2 }));
    assert!(!holds(LvmGoal::FsFits), "there is no filesystem");
    assert!(!holds(LvmGoal::SnapshotValid) && !holds(LvmGoal::PoolFits) && !holds(LvmGoal::SurviveDiskLoss));
    assert!(holds(LvmGoal::Has { node: Kind::Disk, min: 1 }) && !holds(LvmGoal::Has { node: Kind::Disk, min: 2 }));
    assert!(holds(LvmGoal::AtMost { node: Kind::Disk, max: 1 }) && !holds(LvmGoal::AtMost { node: Kind::Lv, max: 0 }));
    assert!(holds(LvmGoal::Lacks { node: Kind::Vm }));
    assert!(holds(LvmGoal::ParamOf { id: "a".into(), key: "size".into(), value: "20".into() }));
    assert!(holds(LvmGoal::ParamOf { id: "a".into(), key: "mirror".into(), value: "1".into() }), "the default counts");
    assert!(holds(LvmGoal::Linked { from: "vg".into(), to: "a".into() }));
    // a physical volume in no group is not healthy, a board without volumes is not healthy
    let mut orphan = t.clone();
    orphan.edges.retain(|e| e.to != "vg");
    assert!(!LvmGoal::Healthy.check(&orphan, &evaluate(&orphan, &none())));
    assert!(!LvmGoal::Healthy.check(&Topology::default(), &evaluate(&Topology::default(), &none())));
}

#[test]
fn goal_texts_name_the_objects() {
    en();
    let mut t = board(&[("d1", "100")]);
    lv(&mut t, "a", "20", "1");
    t.nodes.iter_mut().find(|n| n.id == "a").unwrap().name = "data".into();
    assert_eq!(
        LvmGoal::LvSize { lv: Some("a".into()), min_gib: 50, count: 1 }.describe_for(&t),
        "“data” is a working volume of at least 50 GiB"
    );
    assert_eq!(LvmGoal::LvSize { lv: None, min_gib: 50, count: 3 }.describe(), "at least 3 working volumes of 50 GiB or more");
    assert_eq!(LvmGoal::VgFree { vg: None, min_gib: 5 }.describe(), "a volume group has at least 5 GiB free");
    assert_eq!(LvmGoal::Has { node: Kind::Pv, min: 2 }.describe(), "at least 2 × physical volume");
    assert_eq!(LvmGoal::AtMost { node: Kind::Disk, max: 1 }.describe(), "at most 1 × disk");
    for g in [
        LvmGoal::FsFits,
        LvmGoal::SnapshotValid,
        LvmGoal::PoolFits,
        LvmGoal::SurviveDiskLoss,
        LvmGoal::Healthy,
        LvmGoal::Evacuable { pv: "pv-d1".into() },
        LvmGoal::Lacks { node: Kind::Vm },
    ] {
        assert!(!g.describe_for(&t).is_empty());
    }
}

#[test]
fn a_scenario_refuses_what_is_not_in_the_palette() {
    en();
    let (scenarios, solution) = pack("virt-sim-lvm-grow").unwrap();
    let sc = &scenarios[1];
    let mut t = solution[&sc.id].clone();
    assert!(sc.invalid(&t).is_none());
    t.nodes.push(node(Kind::Vm, "vm"));
    assert!(sc.invalid(&t).unwrap().contains("not available"));
    let mut many = solution[&sc.id].clone();
    for i in 0..30 {
        many.nodes.push(node(Kind::Lv, &format!("x{i}")));
    }
    assert!(sc.invalid(&many).unwrap().contains("at most"));
}

#[test]
fn boards_without_positions_are_laid_out_in_columns() {
    en();
    let mut t = board(&[("d1", "50"), ("d2", "50")]);
    lv(&mut t, "a", "10", "1");
    lv(&mut t, "b", "10", "1");
    t.nodes.push(sized(Kind::ThinPool, "pool", "10"));
    t.nodes.push(sized(Kind::ThinLv, "t", "10"));
    auto_layout(&mut t);
    for (i, a) in t.nodes.iter().enumerate() {
        for n in &t.nodes[i + 1..] {
            assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
        }
    }
    let x = |id: &str| t.node(id).unwrap().x;
    assert!(x("d1") < x("pv-d1") && x("pv-d1") < x("vg") && x("vg") < x("a"));
}

#[test]
fn boards_round_trip_through_json_with_defaults_omitted() {
    en();
    for (sc, reference) in all() {
        let text = serde_json::to_string(&reference).unwrap();
        let back: Topology = serde_json::from_str(&text).unwrap();
        assert_eq!(back, reference, "{}", sc.id);
        // the workload and the goals survive too
        let s = serde_json::to_string(&sc).unwrap();
        assert_eq!(serde_json::from_str::<Scenario>(&s).unwrap(), sc);
    }
    let wl: Workload = serde_json::from_str("{}").unwrap();
    assert_eq!(wl, Workload::default());
}
