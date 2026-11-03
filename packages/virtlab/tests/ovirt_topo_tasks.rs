//! Python tasks over the board data (chapters 20 and 21, ids `ovb…`): the student gets the board as JSON (`{nodes, edges}` without the positions) and
//! writes a function. The expected answers of the tests are **computed by the model** (`oracle`), so the Python reference and the Rust model check each
//! other: `sql_tasks_match_the_model` recomputes every test case stored in `backend/data/sql/tasks/17-virt-20.sql` and `17-virt-21.sql`.
//!
//! The test cases are produced by `cargo test --test ovirt_topo_tasks -- --ignored write_cases` (set `OVB_CASES_OUT` to the output file): the authoring
//! script turns them into SQL rows; after that the SQL files are canonical.

use std::collections::BTreeSet;
use std::path::PathBuf;

use serde_json::{json, Map, Value};
use virtlab::ovirt_topo::{
    default_scenarios, default_solution, evaluate, management_path, migration_network, missing_domains,
    missing_networks, rel, unplugged_networks, DcStatus, DomainStatus, Edge, Kind, Node, Rel, Role, Topology,
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

fn ids<'a>(nodes: impl IntoIterator<Item = &'a Node>) -> Vec<String> {
    nodes.into_iter().map(|n| n.id.clone()).collect()
}

fn sorted(mut v: Vec<String>) -> Vec<String> {
    v.sort();
    v
}

fn up_hosts(t: &Topology) -> Vec<String> {
    sorted(
        evaluate(t)
            .hosts
            .iter()
            .filter(|h| h.status == virtlab::ovirt_topo::HostStatus::Up)
            .map(|h| h.id.clone())
            .collect(),
    )
}

fn dc_name(s: DcStatus) -> &'static str {
    s.name()
}

// ---------------------------------------------------------------- the oracle: the answers of the model

/// The expected answer of the task function for the arguments (the first one is the board).
fn oracle(func: &str, args: &[Value]) -> Value {
    let t = board(&args[0]);
    let s = |i: usize| args[i].as_str().expect("a string argument").to_string();
    match func {
        "domains_of" => json!(ids(t.targets(&s(1), Rel::Domain))),
        "master_domain" => t.targets(&s(1), Rel::Domain).next().map(|d| json!(d.id)).unwrap_or(Value::Null),
        "hosts_seeing" => json!(sorted(ids(t.targets(&s(1), Rel::Sees)))),
        "domain_statuses" => {
            let ev = evaluate(&t);
            Value::Object(ev.domains.iter().map(|d| (d.id.clone(), json!(d.status.name()))).collect())
        }
        "dc_statuses" => {
            let ev = evaluate(&t);
            Value::Object(ev.dcs.iter().map(|d| (d.id.clone(), json!(dc_name(d.status)))).collect())
        }
        "spm_hosts" => {
            let ev = evaluate(&t);
            Value::Object(ev.dcs.iter().map(|d| (d.id.clone(), json!(d.spm))).collect())
        }
        "missing_storage" => Value::Object(
            t.of_kind(Kind::Host)
                .filter(|h| t.dc_of_host(&h.id).is_some())
                .map(|h| (h.id.clone(), json!(sorted(ids(missing_domains(&t, &h.id))))))
                .collect(),
        ),
        "relation" => {
            let (Some(a), Some(b)) = (t.node(&s(1)), t.node(&s(2))) else { panic!("unknown objects") };
            rel(a.kind, b.kind).map(|r| serde_json::to_value(r).unwrap()).unwrap_or(Value::Null)
        }
        "required_missing" => Value::Object(
            t.of_kind(Kind::Host)
                .filter(|h| t.cluster_of_host(&h.id).is_some())
                .map(|h| (h.id.clone(), json!(sorted(ids(missing_networks(&t, &h.id))))))
                .collect(),
        ),
        "management_path" => management_path(&t, &s(1)).map(|(e, n)| json!([e, n])).unwrap_or(Value::Null),
        "host_statuses" => {
            Value::Object(evaluate(&t).hosts.iter().map(|h| (h.id.clone(), json!(h.status.name()))).collect())
        }
        "migration_network" => migration_network(&t, &s(1), &s(2)).map(|n| json!(n.id)).unwrap_or(Value::Null),
        "unplugged" => match t.host_of_vm(&s(1)) {
            None => Value::Null,
            Some(_) => json!(sorted(ids(unplugged_networks(&t, &s(1))))),
        },
        other => panic!("no oracle for {other}"),
    }
}

/// The task functions that take the list of Up hosts as the second argument.
const WITH_UP: [&str; 3] = ["domain_statuses", "dc_statuses", "spm_hosts"];

// ---------------------------------------------------------------- the boards of the cases

fn solution(id: &str) -> Topology {
    default_solution().remove(id).expect("reference board")
}

fn start(id: &str) -> Topology {
    i18n::with_locale(i18n::Locale::En, || {
        default_scenarios().into_iter().find(|s| s.id == id).expect("scenario").start
    })
}

fn cut(mut t: Topology, from: &str, to: &str) -> Topology {
    let before = t.edges.len();
    t.edges.retain(|e| !(e.from == from && e.to == to));
    assert_eq!(t.edges.len() + 1, before, "no link {from} → {to}");
    t
}

fn add(mut t: Topology, from: &str, to: &str) -> Topology {
    t.edges.push(Edge::new(from, to));
    t
}

fn node(mut t: Topology, id: &str, kind: Kind, name: &str) -> Topology {
    t.nodes.push(Node::new(id, kind, name, 0.0, 0.0));
    t
}

fn optional(mut t: Topology, id: &str) -> Topology {
    t.nodes
        .iter_mut()
        .find(|n| n.id == id)
        .unwrap()
        .params
        .insert("required".into(), virtlab::ovirt_topo::Param::Bool(false));
    t
}

/// The boards the cases are made of.
fn pool() -> Vec<Topology> {
    let storage = solution("storage");
    let two = solution("two");
    let repair_start = start("repair");
    let repair = solution("repair");
    let migrate = solution("migrate");
    let mut with_migration = migrate.clone();
    with_migration.nodes.push(Node::network("mig", "migration", 0.0, 0.0, Role::Migration, false));
    with_migration.edges.extend([
        Edge::new("dc1", "mig"),
        Edge::new("mig", "cl1"),
        Edge::new("mig", "h1"),
        Edge::new("mig", "h3"),
    ]);
    let second_domain = add(
        add(add(node(storage.clone(), "scratch", Kind::StorageDomain, "scratch"), "dc1", "scratch"), "scratch", "h1"),
        "scratch",
        "h2",
    );
    // only the out-of-band management network reaches host-1: the path goes over it
    let mut oob = cut(storage.clone(), "engine", "mgmt");
    oob.nodes.push(Node::network("oob", "oob", 0.0, 0.0, Role::Management, false));
    oob.edges.extend([
        Edge::new("dc1", "oob"),
        Edge::new("oob", "cl1"),
        Edge::new("engine", "oob"),
        Edge::new("oob", "h1"),
    ]);
    vec![
        solution("build"),                                                   // 0: no storage
        storage.clone(),                                                     // 1: one data center, everything works
        second_domain,          // 2: two attached domains, the master is the first
        two.clone(),            // 3: two data centers
        cut(two, "nfs2", "h3"), // 4: the second data center misses its domain on its only host
        repair_start,           // 5: NonOperational and NonResponsive hosts
        repair,                 // 6: repaired
        start("migrate"),       // 7: two clusters
        with_migration,         // 8: a dedicated migration network
        node(storage.clone(), "spare", Kind::StorageDomain, "spare"), // 9: a domain attached nowhere
        cut(storage.clone(), "engine", "mgmt"), // 10: no management path
        add(node(storage.clone(), "h9", Kind::Host, "host-9"), "nfs", "h9"), // 11: a host outside every cluster
        optional(repair_start_with_gap(), "vmnet"), // 12: the VM network is optional
        cut(storage, "nfs", "h1"), // 13: one host misses the domain
        migrate,
        oob, // 14
    ]
}

fn repair_start_with_gap() -> Topology {
    start("repair")
}

fn host_ids(t: &Topology) -> Vec<String> {
    ids(t.of_kind(Kind::Host))
}

fn dc_ids(t: &Topology) -> Vec<String> {
    ids(t.of_kind(Kind::DataCenter))
}

fn kind_ids(t: &Topology, k: Kind) -> Vec<String> {
    ids(t.of_kind(k))
}

fn pairs(v: &[String]) -> Vec<(String, String)> {
    v.iter().flat_map(|a| v.iter().filter(move |b| *b != a).map(move |b| (a.clone(), b.clone()))).collect()
}

/// The test cases of a task function: the arguments (the board first). Every board of the pool gives at most a few cases, so that the answers vary.
fn cases(func: &str) -> Vec<Vec<Value>> {
    let pool = pool();
    let mut out: Vec<Vec<Value>> = vec![];
    // `extras`: the arguments after the board; at most `k` of them per board
    let mut take = |t: &Topology, extras: Vec<Vec<Value>>, k: usize| {
        for e in extras.into_iter().take(k) {
            let mut args = vec![arg(t)];
            args.extend(e);
            if !out.contains(&args) {
                out.push(args);
            }
        }
    };
    let ids_of =
        |t: &Topology, f: fn(&Topology) -> Vec<String>| f(t).into_iter().map(|id| vec![json!(id)]).collect::<Vec<_>>();
    match func {
        "domains_of" | "master_domain" => {
            for i in [0, 1, 2, 3, 9] {
                take(&pool[i], ids_of(&pool[i], dc_ids), 2);
            }
        }
        "hosts_seeing" => {
            for i in [1, 2, 3, 13] {
                take(&pool[i], ids_of(&pool[i], |t| kind_ids(t, Kind::StorageDomain)), 2);
            }
        }
        "domain_statuses" | "dc_statuses" | "spm_hosts" => {
            for i in [0, 1, 2, 3, 4, 9, 10, 13] {
                take(&pool[i], vec![vec![json!(up_hosts(&pool[i]))]], 1);
            }
        }
        "missing_storage" => {
            for i in [1, 2, 3, 4, 5, 11, 13] {
                take(&pool[i], vec![vec![]], 1);
            }
        }
        "relation" => {
            let t = &pool[14];
            // every pair of kinds once: a representative pair of objects
            let mut seen = BTreeSet::new();
            let mut extras = vec![];
            for (a, b) in pairs(&t.nodes.iter().map(|n| n.id.clone()).collect::<Vec<_>>()) {
                let (ka, kb) = (t.node(&a).unwrap().kind, t.node(&b).unwrap().kind);
                if seen.insert((ka, kb)) {
                    extras.push(vec![json!(a), json!(b)]);
                }
            }
            take(t, extras, 16);
        }
        "required_missing" | "host_statuses" => {
            let boards: &[usize] =
                if func == "host_statuses" { &[0, 1, 3, 4, 5, 6, 10, 11, 12, 13] } else { &[1, 3, 5, 6, 11, 12, 14] };
            for &i in boards {
                take(&pool[i], vec![vec![]], 1);
            }
        }
        "management_path" => {
            for i in [1, 5, 10, 11, 15] {
                take(&pool[i], ids_of(&pool[i], host_ids), 3);
            }
        }
        "migration_network" => {
            for i in [5, 6, 8, 10] {
                let extras = pairs(&host_ids(&pool[i])).into_iter().map(|(a, b)| vec![json!(a), json!(b)]).collect();
                take(&pool[i], extras, 2);
            }
        }
        "unplugged" => {
            for i in [5, 6, 7, 12] {
                take(&pool[i], ids_of(&pool[i], |t| kind_ids(t, Kind::Vm)), 1);
            }
            // a VM that is not placed on a host
            let mut lost = pool[6].clone();
            lost.edges.retain(|e| e.to != "vm1" || e.from != "h2");
            take(&lost, vec![vec![json!("vm1")]], 1);
        }
        other => panic!("no cases for {other}"),
    }
    out
}

/// The cases of a function with the answers of the model.
fn full_cases(func: &str) -> Vec<(Vec<Value>, Value)> {
    cases(func)
        .into_iter()
        .map(|args| {
            let expected = oracle(func, &args);
            (args, expected)
        })
        .collect()
}

const FUNCS: [&str; 13] = [
    "domains_of",
    "master_domain",
    "hosts_seeing",
    "domain_statuses",
    "dc_statuses",
    "spm_hosts",
    "missing_storage",
    "relation",
    "required_missing",
    "management_path",
    "host_statuses",
    "migration_network",
    "unplugged",
];

/// Writes the cases for the authoring script: `OVB_CASES_OUT=/path/cases.json cargo test --test ovirt_topo_tasks -- --ignored write_cases`.
#[test]
#[ignore]
fn write_cases() {
    let out = std::env::var("OVB_CASES_OUT").expect("OVB_CASES_OUT");
    let mut all = Map::new();
    for f in FUNCS {
        let tests: Vec<Value> =
            full_cases(f).into_iter().map(|(args, expected)| json!({ "args": args, "expected": expected })).collect();
        assert!(tests.len() >= 3, "{f}: too few cases");
        all.insert(f.to_string(), Value::Array(tests));
    }
    std::fs::write(out, serde_json::to_string_pretty(&Value::Object(all)).unwrap()).unwrap();
}

// ---------------------------------------------------------------- the stored tasks

fn sql_path(chapter: u32) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(format!("../../backend/data/sql/tasks/17-virt-{chapter}.sql"))
}

/// `(task id, spec)` of the `ovb…` rows of a SQL file.
fn stored_tasks(chapter: u32) -> Vec<(String, Value)> {
    let text = std::fs::read_to_string(sql_path(chapter)).expect("sql file");
    text.split("\nINSERT INTO tasks")
        .filter_map(|stmt| {
            let id = stmt.split_once(&format!("VALUES (17, {chapter}, '"))?.1.split('\'').next()?.to_string();
            if !id.starts_with("ovb") {
                return None;
            }
            let open = stmt.rfind("'{\"func\"")?;
            let close = stmt.rfind('\'')?;
            let spec = stmt[open + 1..close].replace("''", "'");
            let value = serde_json::from_str::<Value>(&spec).unwrap_or_else(|e| panic!("{id}: spec is not JSON: {e}"));
            Some((id, value))
        })
        .collect()
}

#[test]
fn sql_tasks_match_the_model() {
    let mut seen = BTreeSet::new();
    for chapter in [20, 21] {
        let tasks = stored_tasks(chapter);
        assert!(tasks.len() >= 5, "chapter {chapter}: the board tasks are missing");
        for (id, spec) in tasks {
            let func = spec["func"].as_str().unwrap().to_string();
            assert!(FUNCS.contains(&func.as_str()), "{id}: unknown function {func}");
            let tests = spec["tests"].as_array().unwrap();
            assert!(tests.len() >= 5, "{id}: too few tests");
            for (i, t) in tests.iter().enumerate() {
                let args = t["args"].as_array().unwrap();
                let got = oracle(&func, args);
                assert_eq!(&got, &t["expected"], "{id} test {i}: the stored answer differs from the model");
                if WITH_UP.contains(&func.as_str()) {
                    assert_eq!(
                        args[1],
                        json!(up_hosts(&board(&args[0]))),
                        "{id} test {i}: the list of Up hosts is not the one of the model"
                    );
                }
                assert!(board(&args[0]).edges.len() < 80);
            }
            // the tests must not all give the same answer: a constant function would pass
            let distinct: BTreeSet<String> = tests.iter().map(|t| t["expected"].to_string()).collect();
            assert!(distinct.len() >= 3, "{id}: the answers are too uniform ({} distinct)", distinct.len());
            seen.insert(func);
        }
    }
    assert_eq!(seen.len(), FUNCS.len(), "every function has a stored task: {seen:?}");
}

#[test]
fn the_generator_produces_enough_varied_cases() {
    for f in FUNCS {
        let cases = full_cases(f);
        assert!(cases.len() >= 5, "{f}: {} cases", cases.len());
        let distinct: BTreeSet<String> = cases.iter().map(|(_, e)| e.to_string()).collect();
        assert!(distinct.len() >= 3, "{f}: only {} distinct answers", distinct.len());
    }
    // the pool itself holds the statuses the tasks are about
    let statuses: BTreeSet<&str> = pool()
        .iter()
        .flat_map(|t| evaluate(t).domains.iter().map(|d| d.status).collect::<Vec<_>>())
        .map(|s| match s {
            DomainStatus::Unattached => "unattached",
            DomainStatus::Inactive => "inactive",
            DomainStatus::Active => "active",
        })
        .collect();
    assert_eq!(statuses.len(), 3, "{statuses:?}");
}

// ---------------------------------------------------------------- level 3: `fix(board)` tasks judged by the model

/// `(task id, spec)` of the stored `ovb…` rows whose spec has a `board_check` (the code returns the repaired board).
fn stored_fix_tasks(chapter: u32) -> Vec<(String, Value)> {
    let text = std::fs::read_to_string(sql_path(chapter)).expect("sql file");
    text.split("\nINSERT INTO tasks")
        .filter_map(|stmt| {
            let id = stmt.split_once(&format!("VALUES (17, {chapter}, '"))?.1.split('\'').next()?.to_string();
            let open = stmt.rfind("'{\"driver\"")?;
            let close = stmt.rfind('\'')?;
            let spec = stmt[open + 1..close].replace("''", "'");
            let value = serde_json::from_str::<Value>(&spec).unwrap_or_else(|e| panic!("{id}: spec is not JSON: {e}"));
            value.get("board_check").is_some().then_some((id, value))
        })
        .collect()
}

#[test]
fn fix_tasks_use_the_boards_of_their_scenarios_and_the_starting_boards_do_not_pass() {
    let mut count = 0;
    for chapter in [20, 21, 25] {
        for (id, spec) in stored_fix_tasks(chapter) {
            count += 1;
            let checks = spec["board_check"].as_array().unwrap();
            assert!(checks.len() >= 3, "{id}: a fix task is judged on several boards, or a hard-coded answer passes");
            // the boards the driver hands to fix() are the starting boards of the scenarios, without positions
            let driver = spec["driver"].as_str().unwrap();
            let literal = driver.split_once("_json.loads(r\"\"\"").unwrap().1.split_once("\"\"\")").unwrap().0;
            let given: Vec<Value> = serde_json::from_str(literal).unwrap_or_else(|e| panic!("{id}: boards in the driver: {e}"));
            assert_eq!(given.len(), checks.len(), "{id}");
            for (c, g) in checks.iter().zip(&given) {
                let (pack, scenario) = (c["pack"].as_str().unwrap(), c["scenario"].as_str().unwrap());
                let sc = virtlab::ovirt_topo::pack(pack).unwrap().0.into_iter().find(|s| s.id == scenario).unwrap_or_else(|| panic!("{id}: no {pack}/{scenario}"));
                assert_eq!(board(g), { let mut b = sc.start.clone(); for n in &mut b.nodes { n.x = 0.0; n.y = 0.0; } b }, "{id}: the driver's board is not the start of {scenario}");
                let line = serde_json::to_string(&arg(&sc.start)).unwrap();
                let verdict = virtlab::ovirt_topo::judge(pack, scenario, &line).unwrap();
                assert!(!verdict.reached, "{id}: the unrepaired {scenario} must not pass");
            }
            // the correct boards of the scenarios pass
            for c in checks {
                let (pack, scenario) = (c["pack"].as_str().unwrap(), c["scenario"].as_str().unwrap());
                let (_, solutions) = virtlab::ovirt_topo::pack(pack).unwrap();
                let line = serde_json::to_string(&arg(&solutions[scenario])).unwrap();
                assert!(virtlab::ovirt_topo::judge(pack, scenario, &line).unwrap().reached, "{id}: the reference of {scenario}");
            }
        }
    }
    assert_eq!(count, 3, "one fix task in each of the chapters 20, 21 and 25");
}

#[test]
fn judging_refuses_a_board_with_other_objects() {
    let (scs, _) = virtlab::ovirt_topo::pack("virt-sim-ovirt-storage-2").unwrap();
    let sc = scs.iter().find(|s| s.id == "no-connection").unwrap();
    let mut t = sc.start.clone();
    t.nodes.push(Node::new("extra", Kind::Host, "extra", 0.0, 0.0));
    let verdict = virtlab::ovirt_topo::judge("virt-sim-ovirt-storage-2", "no-connection", &serde_json::to_string(&t).unwrap()).unwrap();
    assert!(!verdict.reached && verdict.invalid.is_some());
    assert!(virtlab::ovirt_topo::judge("virt-sim-ovirt-storage-2", "nope", "{}").is_err());
}
