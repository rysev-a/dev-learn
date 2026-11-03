//! Python tasks over the Linux network board (book 19, chapter 12, ids `nb12-…`).
//!
//! Level 1 and 2: the student gets the board as JSON (`{nodes, edges}` without positions) and writes a function. The expected answers of the tests are
//! **computed by the model** (`oracle`), so the Python reference and the Rust model check each other: `sql_tasks_match_the_model` recomputes every test
//! case stored in `backend/data/sql/tasks/19-ladm-12.sql`. The candidate cases are written by `write_cases` (set `NB_CASES_OUT`); the authoring script
//! picks from them the boards on which the rules of the statement and the model agree, and builds the SQL rows. After that the SQL file is canonical.
//!
//! Level 3: `nb12-wire-network` is a `fix(board)` task; the boards are the scenarios of the task-only pack `virt-fix-net`, and the verdict is `judge`.

use std::collections::{BTreeMap, BTreeSet};
use std::path::PathBuf;

use serde_json::{json, Map, Value};
use virtlab::net_board::{address, evaluate, pack, pack_ids, IfaceStatus, Kind, Param, Rel, Topology, FIX_PACK};

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

fn state_code(s: IfaceStatus) -> &'static str {
    match s {
        IfaceStatus::Ok => "up",
        IfaceStatus::Down => "down",
        IfaceStatus::NoCarrier => "no_carrier",
    }
}

/// The expected answer of the task function for the arguments (the first one is the board).
fn oracle(func: &str, args: &[Value]) -> Value {
    let t = board(&args[0]);
    match func {
        "addresses" => Value::Object(
            t.nodes
                .iter()
                .filter(|n| n.kind.is_iface() || n.kind == Kind::External)
                .filter_map(|n| address(&t, &n.id).map(|a| (n.id.clone(), json!(a))))
                .collect(),
        ),
        "link_states" => Value::Object(evaluate(&t).ifaces.iter().map(|i| (i.id.clone(), json!(state_code(i.status)))).collect()),
        "bridge_vlans" => Value::Object(
            t.of_kind(Kind::Bridge)
                .map(|b| {
                    let mut by_tag: BTreeMap<String, Vec<String>> = BTreeMap::new();
                    let mut ports: Vec<&virtlab::net_board::Node> = t.sources(&b.id, Rel::Port);
                    ports.extend(t.sources(&b.id, Rel::Tap));
                    for p in ports {
                        by_tag.entry(p.param_text("access_vlan")).or_default().push(p.id.clone());
                    }
                    for v in by_tag.values_mut() {
                        v.sort();
                    }
                    (b.id.clone(), json!(by_tag))
                })
                .collect(),
        ),
        other => panic!("no oracle for {other}"),
    }
}

const FUNCS: [&str; 3] = ["addresses", "link_states", "bridge_vlans"];

// ---------------------------------------------------------------- the boards of the cases

fn set(mut t: Topology, id: &str, key: &str, value: Param) -> Topology {
    if let Some(n) = t.nodes.iter_mut().find(|n| n.id == id) {
        n.params.insert(key.into(), value);
    }
    t
}

/// Every starting and reference board of the packs (and of the task-only pack), then variants of the references: an interface taken down, a link
/// taken away, an interface in another network, a port in another VLAN.
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
        let mut ids = pack_ids();
        ids.push(FIX_PACK);
        for id in ids {
            let (scs, sols) = pack(id).unwrap();
            for sc in &scs {
                push(sc.start.clone());
                refs.push(sols[&sc.id].clone());
            }
        }
        for r in refs {
            push(r.clone());
            let ifaces: Vec<String> = r.nodes.iter().filter(|n| n.kind.is_iface()).map(|n| n.id.clone()).collect();
            if let Some(first) = ifaces.first() {
                push(set(r.clone(), first, "up", Param::Bool(false)));
            }
            if let Some(last) = ifaces.last() {
                push(set(r.clone(), last, "up", Param::Bool(false)));
                push(set(r.clone(), last, "net", Param::Str("c".into())));
                push(set(r.clone(), last, "access_vlan", Param::Str("20".into())));
            }
            // a link taken away: the first of every kind of target
            let mut seen = BTreeSet::new();
            for (i, e) in r.edges.iter().enumerate() {
                let key = (r.node(&e.from).map(|n| n.kind), r.node(&e.to).map(|n| n.kind));
                if seen.insert(key) {
                    let mut cut = r.clone();
                    cut.edges.remove(i);
                    push(cut);
                }
            }
        }
    });
    out
}

/// The candidate cases of a function: the arguments (the board first) and the answer of the model.
fn full_cases(func: &str) -> Vec<(Vec<Value>, Value)> {
    candidates()
        .into_iter()
        .filter(|t| func != "bridge_vlans" || t.of_kind(Kind::Bridge).next().is_some())
        .map(|t| {
            let args = vec![arg(&t)];
            let expected = oracle(func, &args);
            (args, expected)
        })
        .collect()
}

/// Writes the candidate cases for the authoring script: `NB_CASES_OUT=/path/cases.json cargo test --test net_board_tasks -- --ignored write_cases`.
#[test]
#[ignore]
fn write_cases() {
    let out = std::env::var("NB_CASES_OUT").expect("NB_CASES_OUT");
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
fn the_candidates_hold_every_state_the_tasks_are_about() {
    let states: BTreeSet<String> = full_cases("link_states")
        .iter()
        .flat_map(|(_, e)| e.as_object().unwrap().values().map(|v| v.as_str().unwrap().to_string()).collect::<Vec<_>>())
        .collect();
    for want in ["up", "down", "no_carrier"] {
        assert!(states.contains(want), "no candidate board with an interface that is {want}: {states:?}");
    }
    let tags: BTreeSet<String> = full_cases("bridge_vlans")
        .iter()
        .flat_map(|(_, e)| e.as_object().unwrap().values().flat_map(|b| b.as_object().unwrap().keys().cloned().collect::<Vec<_>>()).collect::<Vec<_>>())
        .collect();
    for want in ["0", "10", "20"] {
        assert!(tags.contains(want), "no candidate bridge with a port in VLAN {want}: {tags:?}");
    }
}

// ---------------------------------------------------------------- the stored tasks

fn sql_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/sql/tasks/19-ladm-12.sql")
}

/// `(task id, spec)` of the `nb12-…` rows with a `{"func"` spec (the answer is plain data) or a `{"driver"` spec (the code returns a board).
fn stored(kind: &str) -> Vec<(String, Value)> {
    let text = std::fs::read_to_string(sql_path()).expect("sql file");
    text.split("\nINSERT INTO tasks")
        .filter_map(|stmt| {
            let id = stmt.split_once("VALUES (19, 12, '")?.1.split('\'').next()?.to_string();
            if !id.starts_with("nb12-") {
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
    assert!(tasks.len() >= 3, "the board data tasks of the chapter 12 are missing");
    for (id, spec) in tasks {
        let func = spec["func"].as_str().unwrap().to_string();
        assert!(FUNCS.contains(&func.as_str()), "{id}: unknown function {func}");
        assert_eq!(spec["board_view"], json!(true), "{id}: the board is shown beside the results");
        assert_eq!(spec["board_kind"], json!("net_board"), "{id}");
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
            let verdict = virtlab::net_board::judge(FIX_PACK, &sc.id, &line).unwrap();
            assert!(!verdict.reached, "{}: the unrepaired board must not pass", sc.id);
            let line = serde_json::to_string(&arg(&sols[&sc.id])).unwrap();
            assert!(virtlab::net_board::judge(FIX_PACK, &sc.id, &line).unwrap().reached, "{}: the reference", sc.id);
            // only links are missing: the same objects, the same parameters
            assert_eq!(sc.start.nodes, sols[&sc.id].nodes, "{}", sc.id);
            assert!(sc.start.edges.len() < sols[&sc.id].edges.len());
            // every missing link is needed: put back all but one and the board still fails
            for e in sols[&sc.id].edges.iter().filter(|e| !sc.start.edges.contains(e)) {
                let mut b = sols[&sc.id].clone();
                b.edges.retain(|x| x != e);
                let line = serde_json::to_string(&arg(&b)).unwrap();
                assert!(!virtlab::net_board::judge(FIX_PACK, &sc.id, &line).unwrap().reached, "{}: the link {}>{} is needed", sc.id, e.from, e.to);
            }
        }
    });
}

#[test]
fn fix_tasks_use_the_boards_of_their_scenarios() {
    i18n::with_locale(i18n::Locale::En, || {
        let tasks = stored("driver");
        assert_eq!(tasks.len(), 1, "one fix task in the chapter 12");
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
        t.nodes.push(virtlab::net_board::Node::new("extra", Kind::Eth, "extra", 0.0, 0.0));
        let verdict = virtlab::net_board::judge(FIX_PACK, &sc.id, &serde_json::to_string(&t).unwrap()).unwrap();
        assert!(!verdict.reached && verdict.invalid.is_some());
        assert!(virtlab::net_board::judge(FIX_PACK, "nope", "{}").is_err());
    });
}

/// Judges the boards printed by a reference run: `PRINTED=/path/printed.json TASK=<task id> cargo test --test net_board_tasks -- --ignored judge_printed`
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
            let verdict = virtlab::net_board::judge(pack, s.as_str().unwrap(), line.as_str().unwrap()).unwrap();
            assert!(verdict.reached, "{task}/{s}: {:?} {:?}", verdict.invalid, verdict.goals);
        }
    });
}
