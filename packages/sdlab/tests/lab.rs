//! Exercise data: self-check (port of `sd-selfcheck`), serde round-trip, server-side verification, wasm build.

mod common;

use std::collections::HashSet;

use sdlab::verify::{problems, self_check};
use sdlab::{parse_solution, verify, verify_raw, Kind, LabChapter, ParamValue, Problem, SdEdge, SdNode, SdState};

#[test]
fn data_is_complete() {
    locales::set_locale(i18n::Locale::Ru);
    let chapters = common::chapters();
    assert_eq!(chapters.len(), 24);
    for (i, c) in chapters.iter().enumerate() {
        assert_eq!((c.book, c.chapter, c.lab.as_str()), (18, i as u32 + 1, "sd"));
    }
    assert_eq!(chapters.iter().map(|c| c.tasks.len()).sum::<usize>(), 149);
}

/// The starting design does not solve the exercise, the reference does, reference components are in the palette, ids are unique.
#[test]
fn self_check_all_tasks() {
    locales::set_locale(i18n::Locale::Ru);
    let mut ids = HashSet::new();
    let mut bad = Vec::new();
    for c in common::chapters() {
        for t in &c.tasks {
            assert!(ids.insert(t.id.clone()), "duplicate id: {}", t.id);
            let r = self_check(t);
            if !r.is_ok() {
                bad.push(format!(
                    "{}: starter does not fail ({} of {} goals), reference passes: {}, outside palette: {:?}, too many nodes: {}",
                    t.id,
                    r.start_failed,
                    r.start.len(),
                    r.solution.iter().all(|g| g.ok),
                    r.outside,
                    r.too_many
                ));
            }
        }
    }
    assert!(bad.is_empty(), "problems:\n{}", bad.join("\n"));
}

#[test]
fn serde_round_trip() {
    locales::set_locale(i18n::Locale::Ru);
    for c in common::chapters() {
        // data file → text → the same file
        let pretty = sdlab::pretty::to_string(&c).expect("serialize");
        assert_eq!(LabChapter::parse(&pretty).expect("parse"), c, "chapter {}", c.chapter);
        // plain serde_json (without our formatting)
        let compact = serde_json::to_string(&c).expect("serialize");
        let back: LabChapter = serde_json::from_str(&compact).expect("parse");
        assert_eq!(back, c, "chapter {}", c.chapter);
        // and via the value tree
        let v = serde_json::to_value(&c).expect("value");
        let back: LabChapter = serde_json::from_value(v).expect("parse");
        assert_eq!(back, c);
    }
}

/// The file on disk is exactly what the formatter writes (manual edits do not silently break the format).
#[test]
fn files_are_canonical() {
    locales::set_locale(i18n::Locale::Ru);
    for c in common::chapters() {
        let name = sdlab::data::file_name(c.book, c.chapter);
        let text = std::fs::read_to_string(common::data_dir().join(&name)).expect("parse");
        assert_eq!(text, sdlab::pretty::to_string(&c).expect("serialize"), "{name}: file is not canonical (cargo run --bin import)");
    }
}

#[test]
fn legacy_names_are_accepted() {
    locales::set_locale(i18n::Locale::Ru);
    // names from the TypeScript version: dataGB, searchShare, camelCase parameters
    let json = r#"{"static":1,"read":2,"write":3,"dataGB":4,"hotSet":0.5,"searchShare":0.1,"mediaTB":2,"calls":{"auth":1}}"#;
    let w: sdlab::Workload = serde_json::from_str(json).expect("parse");
    assert_eq!((w.static_rps, w.read_rps, w.write_rps, w.data_gb), (1.0, 2.0, 3.0, 4.0));
    assert_eq!((w.search_share, w.media_tb), (Some(0.1), Some(2.0)));
    let n: SdNode = serde_json::from_str(r#"{"id":"c","kind":"cache","params":{"sizeGB":8}}"#).expect("parse");
    assert_eq!(n.num("size_gb"), 8.0);
    assert_eq!(n.name, "");
}

fn task(id: &str) -> sdlab::Task {
    common::chapters().into_iter().flat_map(|c| c.tasks).find(|t| t.id == id).expect("task exists")
}

#[test]
fn verify_accepts_solutions_and_rejects_start() {
    locales::set_locale(i18n::Locale::Ru);
    let mut accepted = 0;
    for c in common::chapters() {
        for t in &c.tasks {
            let v = verify(&t.spec, &t.spec.solution);
            assert!(v.ok, "{}: reference rejected: {:?} {:?}", t.id, v.problems, v.reason());
            assert_eq!(v.goals.len(), t.spec.goals.len());
            let v = verify(&t.spec, &t.spec.start);
            assert!(!v.ok, "{}: starter diagram accepted", t.id);
            // the solution arrives as a string — as the client sends it
            let raw = serde_json::to_string(&t.spec.solution).expect("serialize");
            assert!(verify_raw(&t.spec, &raw).expect("parse").ok, "{}", t.id);
            accepted += 1;
        }
    }
    assert_eq!(accepted, 149);
}

#[test]
fn parse_solution_is_tolerant() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("sd01-wire");
    let s = &t.spec.solution;
    let plain = serde_json::to_string(s).expect("serialize");
    // wrappers and double serialization
    let wrapped = format!(r#"{{"state": {plain}}}"#);
    let double = serde_json::to_string(&plain).expect("serialize");
    for raw in [plain.clone(), wrapped, double] {
        assert_eq!(&parse_solution(&raw).expect("parse"), s);
    }
    // without names and coordinates (old drafts)
    let bare = r#"{"nodes":[{"id":"users","kind":"clients"},{"id":"app","kind":"app"},{"id":"db","kind":"db"}],
                  "edges":[{"from":"users","to":"app"},{"from":"app","to":"db"}]}"#;
    let parsed = parse_solution(bare).expect("parse");
    assert_eq!(parsed.nodes[0].name, "Пользователи");
    assert!(verify(&t.spec, &parsed).ok);
    // garbage is an error, not a panic
    for junk in ["", "null", "[]", "{}", r#"{"nodes": 5}"#, r#"{"nodes":[{"id":1}]}"#, r#""x""#, r#"{"nodes":[{"id":"a","kind":"nope"}]}"#] {
        assert!(parse_solution(junk).is_err(), "accepted: {junk}");
    }
    assert!(parse_solution(&"x".repeat(2 << 20)).is_err());
}

#[test]
fn verify_rejects_cheating() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("sd01-fleet");
    let sol = t.spec.solution.clone();
    let reject = |s: &SdState, what: &str| {
        let v = verify(&t.spec, s);
        assert!(!v.ok, "accepted: {what}");
        v
    };

    // too many nodes (and evaluation does not run)
    let mut s = sol.clone();
    for i in 0..20 {
        s.nodes.push(SdNode::new(&format!("x{i}"), Kind::App, &[]));
    }
    let v = reject(&s, "too many nodes");
    assert!(v.problems.iter().any(|p| matches!(p, Problem::TooManyNodes { .. })));
    assert!(v.goals.is_empty());

    // component outside the palette
    let mut s = sol.clone();
    s.nodes.push(SdNode::new("c", Kind::Cache, &[]));
    assert!(reject(&s, "outside palette").problems.iter().any(|p| matches!(p, Problem::OutsidePalette { kind: Kind::Cache, .. })));

    // value out of range: a hundred thousand servers would solve any workload
    let mut s = sol.clone();
    s.nodes.iter_mut().find(|n| n.id == "app").expect("node").params.insert("instances".into(), ParamValue::Num(100000.0));
    assert!(reject(&s, "out of range").problems.iter().any(|p| matches!(p, Problem::BadParam { .. })));

    // fractional and unknown parameter
    let mut s = sol.clone();
    let app = s.nodes.iter_mut().find(|n| n.id == "app").expect("node");
    app.params.insert("instances".into(), ParamValue::Num(2.5));
    app.params.insert("magic".into(), ParamValue::Bool(true));
    let v = reject(&s, "fractional and unknown");
    assert_eq!(v.problems.iter().filter(|p| matches!(p, Problem::BadParam { .. })).count(), 2);

    // hidden parameter (DB retries are not configurable in this exercise)
    let mut s = sol.clone();
    s.nodes.iter_mut().find(|n| n.id == "app").expect("node").params.insert("weight".into(), ParamValue::Num(10.0));
    assert!(reject(&s, "hidden param").problems.iter().any(|p| matches!(p, Problem::HiddenParam { .. })));

    // cycle, duplicate, link to a nonexistent component and an invalid link
    let mut s = sol.clone();
    s.edges.push(SdEdge::new("lb", "lb"));
    s.edges.push(SdEdge::new("users", "lb"));
    s.edges.push(SdEdge::new("app", "ghost"));
    s.edges.push(SdEdge::new("db", "app"));
    let ps = problems(&t.spec, &s);
    assert!(ps.iter().any(|p| matches!(p, Problem::Cycle { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::DuplicateEdge { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::UnknownEdgeEnd { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::BadLink { .. })));

    // no users, two users, duplicate id, empty design
    let mut s = sol.clone();
    s.nodes.retain(|n| n.kind != Kind::Clients);
    s.edges.retain(|e| e.from != "users");
    assert!(reject(&s, "no users").problems.contains(&Problem::NoClients));
    let mut s = sol.clone();
    s.nodes.push(SdNode::new("users2", Kind::Clients, &[]));
    assert!(reject(&s, "two clients").problems.iter().any(|p| matches!(p, Problem::ManyClients { .. })));
    let mut s = sol.clone();
    s.nodes.push(s.nodes[1].clone());
    assert!(reject(&s, "duplicate id").problems.iter().any(|p| matches!(p, Problem::DuplicateNode { .. })));
    assert!(reject(&SdState::default(), "empty").problems.contains(&Problem::Empty));
    assert!(sol.nodes.len() <= t.spec.max_nodes());
}

/// A design with a cycle does not cause infinite recursion: the extra link is dropped with a warning.
#[test]
fn evaluate_survives_cycles() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("sd01-fleet");
    let mut s = t.spec.solution.clone();
    s.edges.push(SdEdge::new("lb", "lb"));
    s.edges.push(SdEdge::new("app", "lb"));
    let r = sdlab::evaluate(&s, &t.spec.workload, &Default::default());
    assert!(r.warnings.iter().any(|w| w.contains("цикл")), "{:?}", r.warnings);
    let base = sdlab::evaluate(&t.spec.solution, &t.spec.workload, &Default::default());
    assert_eq!(r.p50, base.p50);
    assert_eq!(r.success, base.success);
}

#[test]
fn client_copy_has_no_solution() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("sd01-wire");
    let c = t.spec.without_solution();
    assert!(c.solution.nodes.is_empty());
    assert_eq!(c.goals, t.spec.goals);
}

/// The crate builds for wasm32 (if the target is installed in the toolchain).
#[test]
fn builds_for_wasm() {
    locales::set_locale(i18n::Locale::Ru);
    let sysroot = std::process::Command::new("rustc").args(["--print", "sysroot"]).output().expect("rustc");
    let sysroot = String::from_utf8_lossy(&sysroot.stdout).trim().to_owned();
    if !std::path::Path::new(&sysroot).join("lib/rustlib/wasm32-unknown-unknown").exists() {
        eprintln!("target wasm32-unknown-unknown is not installed — skipping");
        return;
    }
    let target_dir = std::env::temp_dir().join("sdlab-wasm-check");
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| "cargo".into());
    let out = std::process::Command::new(cargo)
        .args(["check", "--lib", "--target", "wasm32-unknown-unknown", "--manifest-path"])
        .arg(concat!(env!("CARGO_MANIFEST_DIR"), "/Cargo.toml"))
        .env("CARGO_TARGET_DIR", target_dir)
        .output()
        .expect("run cargo");
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
}
