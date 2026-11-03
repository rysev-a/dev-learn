//! Python tasks over the LVM board (book 19, chapter 16, ids `lvb16-…`).
//!
//! Level 1 and 2: the student gets the board as JSON (`{nodes, edges}` without positions) and writes a function. The expected answers of the tests are
//! **computed by the model** (`oracle`), so the Python reference and the Rust model check each other: `sql_tasks_match_the_model` recomputes every test
//! case stored in `backend/data/sql/tasks/19-ladm-16.sql`. The candidate cases are written by `write_cases` (set `LVB_CASES_OUT`); the authoring script
//! picks from them the boards on which the rules of the statement and the model agree, and builds the SQL rows. After that the SQL file is canonical.
//!
//! Level 3: `lvb16-wire-stack` is a `fix(board)` task; the boards are the scenarios of the task-only pack `virt-fix-lvm`, and the verdict is `judge`.

use std::collections::BTreeSet;
use std::path::PathBuf;

use serde_json::{json, Map, Value};
use virtlab::lvm_board::{
    evaluate, pack, pack_ids, Edge, FsStatus, Kind, Param, SnapStatus, Topology, Workload, FIX_PACK,
};

// ---------------------------------------------------------------- the board as task data

/// The board as the task gives it: without positions.
fn arg(t: &Topology) -> Value {
    let mut v = serde_json::to_value(t).unwrap();
    for n in v["nodes"].as_array_mut().unwrap() {
        let n = n.as_object_mut().unwrap();
        n.remove("x");
        n.remove("y");
    }
    v
}

/// The board back from the task data.
fn board(v: &Value) -> Topology {
    let mut v = v.clone();
    for n in v["nodes"].as_array_mut().expect("nodes") {
        let n = n.as_object_mut().unwrap();
        n.insert("x".into(), json!(0.0));
        n.insert("y".into(), json!(0.0));
    }
    serde_json::from_value(v).expect("a board")
}

fn zero_positions(mut t: Topology) -> Topology {
    for n in &mut t.nodes {
        n.x = 0.0;
        n.y = 0.0;
    }
    t
}

// ---------------------------------------------------------------- the oracle: the answers of the model

fn fs_code(s: FsStatus) -> &'static str {
    match s {
        FsStatus::Ok => "ok",
        FsStatus::NotGrown => "not_grown",
        FsStatus::TooBig => "too_big",
        FsStatus::Detached => "detached",
        FsStatus::VolumeDown => "volume_down",
    }
}

fn snap_code(s: SnapStatus) -> &'static str {
    match s {
        SnapStatus::Valid => "valid",
        SnapStatus::Invalid => "invalid",
        SnapStatus::Orphan => "orphan",
        SnapStatus::NoSpace => "no_space",
        SnapStatus::OriginDown => "origin_down",
        SnapStatus::PoolFull => "pool_full",
    }
}

/// The expected answer of the task function for the arguments (the first one is the board).
fn oracle(func: &str, args: &[Value]) -> Value {
    let t = board(&args[0]);
    match func {
        "vg_free" => {
            let ev = evaluate(&t, &Workload::default());
            Value::Object(ev.vgs.iter().map(|g| (g.id.clone(), json!([g.total, g.total - g.used]))).collect())
        }
        "fs_status" => {
            let ev = evaluate(&t, &Workload::default());
            Value::Object(ev.filesystems.iter().map(|f| (f.id.clone(), json!(fs_code(f.status)))).collect())
        }
        "snapshot_status" => {
            let changed = args[1].as_u64().expect("changed GiB");
            let ev = evaluate(&t, &Workload { changed_gib: changed as u32, written_gib: 0 });
            Value::Object(ev.snapshots.iter().map(|s| (s.id.clone(), json!(snap_code(s.status)))).collect())
        }
        other => panic!("no oracle for {other}"),
    }
}

const FUNCS: [&str; 3] = ["vg_free", "fs_status", "snapshot_status"];

// ---------------------------------------------------------------- the boards of the cases

fn set(mut t: Topology, id: &str, key: &str, value: &str) -> Topology {
    if let Some(n) = t.nodes.iter_mut().find(|n| n.id == id) {
        n.params.insert(key.into(), Param::Str(value.into()));
    }
    t
}

/// Every starting and reference board of the packs, then variants of the references: other extent sizes, bigger disks, a filesystem or a link taken away.
fn candidates() -> Vec<Topology> {
    let mut out: Vec<Topology> = Vec::new();
    let mut push = |t: Topology| {
        let t = zero_positions(t);
        if !out.contains(&t) {
            out.push(t);
        }
    };
    i18n::with_locale(i18n::Locale::En, || {
        let mut refs = Vec::new();
        for id in pack_ids() {
            let (scs, sols) = pack(id).unwrap();
            for sc in &scs {
                push(sc.start.clone());
                refs.push(sols[&sc.id].clone());
            }
        }
        for r in refs {
            push(r.clone());
            for pe in ["32", "128"] {
                let vgs: Vec<String> = r.of_kind(Kind::Vg).map(|n| n.id.clone()).collect();
                push(vgs.iter().fold(r.clone(), |t, v| set(t, v, "pe", pe)));
            }
            let disks: Vec<String> = r.of_kind(Kind::Disk).map(|n| n.id.clone()).collect();
            push(disks.iter().fold(r.clone(), |t, d| set(t, d, "size", "200")));
            // a filesystem that does not follow its volume: the volume grew, or the filesystem is larger than the volume
            for (i, e) in r.edges.iter().enumerate().filter(|(_, e)| r.node(&e.to).is_some_and(|n| n.kind == Kind::Fs)).take(1) {
                push(set(r.clone(), &e.from, "size", "100"));
                push(set(r.clone(), &e.to, "size", "200"));
                push(set(r.clone(), &e.from, "size", "2"));
                let _ = i;
            }
            if let Some(i) = r.edges.iter().position(|e| r.node(&e.to).is_some_and(|n| n.kind == Kind::Fs)) {
                let mut cut = r.clone();
                cut.edges.remove(i);
                push(cut);
            }
            // a second, small snapshot of the same classic origin
            if let Some(e) = r.edges.iter().find(|e| r.node(&e.to).is_some_and(|n| n.kind == Kind::Snapshot) && r.node(&e.from).is_some_and(|n| n.kind == Kind::Lv)) {
                let mut more = r.clone();
                more.nodes.push(virtlab::lvm_board::Node::new("snap2", Kind::Snapshot, "second-snap", 0.0, 0.0));
                more.edges.push(Edge::new(&e.from, "snap2"));
                push(set(more.clone(), "snap2", "size", "2"));
                push(set(set(more, "snap2", "size", "20"), &e.to, "size", "1"));
            }
            if let Some(i) = r.edges.iter().position(|e| r.node(&e.to).is_some_and(|n| n.kind == Kind::Snapshot)) {
                let mut cut = r.clone();
                cut.edges.remove(i);
                push(cut);
            }
        }
    });
    out
}

/// The candidate cases of a function: the arguments (the board first) and the answer of the model.
fn full_cases(func: &str) -> Vec<(Vec<Value>, Value)> {
    let mut out = vec![];
    for t in candidates() {
        let ev = evaluate(&t, &Workload::default());
        let extras: Vec<Vec<Value>> = match func {
            "vg_free" if !ev.vgs.is_empty() => vec![vec![]],
            "fs_status" if !ev.filesystems.is_empty() => vec![vec![]],
            "snapshot_status" if !ev.snapshots.is_empty() => [0, 8, 40, 90].into_iter().map(|c| vec![json!(c)]).collect(),
            _ => vec![],
        };
        for e in extras {
            let mut args = vec![arg(&t)];
            args.extend(e);
            let expected = oracle(func, &args);
            out.push((args, expected));
        }
    }
    out
}

/// Writes the candidate cases for the authoring script: `LVB_CASES_OUT=/path/cases.json cargo test --test lvm_board_tasks -- --ignored write_cases`.
#[test]
#[ignore]
fn write_cases() {
    let out = std::env::var("LVB_CASES_OUT").expect("LVB_CASES_OUT");
    let mut all = Map::new();
    for f in FUNCS {
        let tests: Vec<Value> =
            full_cases(f).into_iter().map(|(args, expected)| json!({ "args": args, "expected": expected })).collect();
        assert!(tests.len() >= 8, "{f}: too few candidate cases");
        all.insert(f.to_string(), Value::Array(tests));
    }
    std::fs::write(out, serde_json::to_string_pretty(&Value::Object(all)).unwrap()).unwrap();
}

#[test]
fn the_candidates_hold_every_status_the_tasks_are_about() {
    let fs: BTreeSet<String> = full_cases("fs_status").iter().flat_map(|(_, e)| e.as_object().unwrap().values().map(|v| v.as_str().unwrap().to_string()).collect::<Vec<_>>()).collect();
    for want in ["ok", "not_grown", "detached"] {
        assert!(fs.contains(want), "no candidate board with a filesystem that is {want}: {fs:?}");
    }
    let snap: BTreeSet<String> = full_cases("snapshot_status").iter().flat_map(|(_, e)| e.as_object().unwrap().values().map(|v| v.as_str().unwrap().to_string()).collect::<Vec<_>>()).collect();
    for want in ["valid", "invalid", "orphan"] {
        assert!(snap.contains(want), "no candidate board with a snapshot that is {want}: {snap:?}");
    }
}

// ---------------------------------------------------------------- the stored tasks

fn sql_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/sql/tasks/19-ladm-16.sql")
}

/// `(task id, spec)` of the `lvb16-…` rows with a `{"func"` spec (the answer is plain data) or a `{"driver"` spec (the code returns a board).
fn stored(kind: &str) -> Vec<(String, Value)> {
    let text = std::fs::read_to_string(sql_path()).expect("sql file");
    text.split("\nINSERT INTO tasks")
        .filter_map(|stmt| {
            let id = stmt.split_once("VALUES (19, 16, '")?.1.split('\'').next()?.to_string();
            if !id.starts_with("lvb16-") {
                return None;
            }
            let open = stmt.rfind(&format!("'{{\"{kind}\""))?;
            let close = stmt.rfind('\'')?;
            let spec = stmt[open + 1..close].replace("''", "'");
            let value = serde_json::from_str::<Value>(&spec).unwrap_or_else(|e| panic!("{id}: spec is not JSON: {e}"));
            Some((id, value))
        })
        .collect()
}

#[test]
fn sql_tasks_match_the_model() {
    let tasks = stored("func");
    let mut seen = BTreeSet::new();
    assert!(tasks.len() >= 3, "the board data tasks of the chapter 16 are missing");
    for (id, spec) in tasks {
        let func = spec["func"].as_str().unwrap().to_string();
        assert!(FUNCS.contains(&func.as_str()), "{id}: unknown function {func}");
        assert_eq!(spec["board_view"], json!(true), "{id}: the board is shown beside the results");
        assert_eq!(spec["board_kind"], json!("lvm_board"), "{id}");
        let tests = spec["tests"].as_array().unwrap();
        assert!(tests.len() >= 6, "{id}: too few tests");
        for (i, t) in tests.iter().enumerate() {
            let args = t["args"].as_array().unwrap();
            assert_eq!(&oracle(&func, args), &t["expected"], "{id} test {i}: the stored answer differs from the model");
            assert!(board(&args[0]).edges.len() < 80);
        }
        // the tests must not all give the same answer: a constant function would pass
        let distinct: BTreeSet<String> = tests.iter().map(|t| t["expected"].to_string()).collect();
        assert!(distinct.len() >= 4, "{id}: the answers are too uniform ({} distinct)", distinct.len());
        seen.insert(func);
    }
    assert_eq!(seen.len(), FUNCS.len(), "every function has a stored task: {seen:?}");
}

// ---------------------------------------------------------------- level 3: `fix(board)` judged by the model

#[test]
fn the_wiring_scenarios_start_unsolved_and_the_references_solve_them() {
    i18n::with_locale(i18n::Locale::En, || {
        let (scs, sols) = pack(FIX_PACK).expect("the task-only pack");
        assert!(scs.len() >= 3, "a fix task is judged on several boards, or a hard-coded answer passes");
        assert!(!pack_ids().contains(&FIX_PACK), "the task-only pack is not an exercise");
        for sc in &scs {
            let line = serde_json::to_string(&arg(&sc.start)).unwrap();
            let verdict = virtlab::lvm_board::judge(FIX_PACK, &sc.id, &line).unwrap();
            assert!(!verdict.reached, "{}: the unrepaired board must not pass", sc.id);
            let line = serde_json::to_string(&arg(&sols[&sc.id])).unwrap();
            assert!(virtlab::lvm_board::judge(FIX_PACK, &sc.id, &line).unwrap().reached, "{}: the reference", sc.id);
            // only links are missing: the same objects, the same parameters
            assert_eq!(sc.start.nodes, sols[&sc.id].nodes, "{}", sc.id);
            assert!(sc.start.edges.len() < sols[&sc.id].edges.len());
            // every missing link is needed: put back all but one and the board still fails
            for e in sols[&sc.id].edges.iter().filter(|e| !sc.start.edges.contains(e)) {
                let mut b = sols[&sc.id].clone();
                b.edges.retain(|x| x != e);
                let line = serde_json::to_string(&arg(&b)).unwrap();
                assert!(!virtlab::lvm_board::judge(FIX_PACK, &sc.id, &line).unwrap().reached, "{}: the link {}>{} is needed", sc.id, e.from, e.to);
            }
        }
    });
}

#[test]
fn fix_tasks_use_the_boards_of_their_scenarios() {
    i18n::with_locale(i18n::Locale::En, || {
        let tasks = stored("driver");
        assert_eq!(tasks.len(), 1, "one fix task in the chapter 16");
        for (id, spec) in tasks {
            let checks = spec["board_check"].as_array().unwrap();
            assert!(checks.len() >= 3, "{id}");
            let driver = spec["driver"].as_str().unwrap();
            let literal = driver.split_once("_json.loads(r\"\"\"").unwrap().1.split_once("\"\"\")").unwrap().0;
            let given: Vec<Value> = serde_json::from_str(literal).unwrap_or_else(|e| panic!("{id}: boards in the driver: {e}"));
            assert_eq!(given.len(), checks.len(), "{id}");
            for (c, g) in checks.iter().zip(&given) {
                let (p, s) = (c["pack"].as_str().unwrap(), c["scenario"].as_str().unwrap());
                let sc = pack(p).unwrap().0.into_iter().find(|x| x.id == s).unwrap_or_else(|| panic!("{id}: no {p}/{s}"));
                assert_eq!(board(g), zero_positions(sc.start.clone()), "{id}: the driver's board is not the start of {s}");
            }
        }
    });
}

#[test]
fn judging_refuses_a_board_with_other_objects() {
    i18n::with_locale(i18n::Locale::En, || {
        let (scs, _) = pack(FIX_PACK).unwrap();
        let sc = &scs[0];
        let mut t = sc.start.clone();
        t.nodes.push(virtlab::lvm_board::Node::new("extra", Kind::Disk, "extra", 0.0, 0.0));
        let verdict = virtlab::lvm_board::judge(FIX_PACK, &sc.id, &serde_json::to_string(&t).unwrap()).unwrap();
        assert!(!verdict.reached && verdict.invalid.is_some());
        assert!(virtlab::lvm_board::judge(FIX_PACK, "nope", "{}").is_err());
        let _ = Edge::new("a", "b");
    });
}

/// Judges the boards printed by a reference run: `PRINTED=/path/printed.json TASK=<task id> cargo test --test lvm_board_tasks -- --ignored judge_printed`
/// (the file is `{task: {pack, scenarios, lines}}`, written by the authoring script).
#[test]
#[ignore]
fn judge_printed() {
    let path = std::env::var("PRINTED").expect("PRINTED");
    let task = std::env::var("TASK").expect("TASK");
    let all: Value = serde_json::from_str(&std::fs::read_to_string(path).unwrap()).unwrap();
    let t = &all[&task];
    let pack = t["pack"].as_str().unwrap();
    i18n::with_locale(i18n::Locale::En, || {
        for (s, line) in t["scenarios"].as_array().unwrap().iter().zip(t["lines"].as_array().unwrap()) {
            let verdict = virtlab::lvm_board::judge(pack, s.as_str().unwrap(), line.as_str().unwrap()).unwrap();
            assert!(verdict.reached, "{task}/{s}: {:?} {:?}", verdict.invalid, verdict.goals);
        }
    });
}
