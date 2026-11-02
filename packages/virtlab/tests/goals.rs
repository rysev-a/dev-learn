//! Goals are reachable: for every exercise there is an action sequence that reaches all goals, and the server accepts it.
//! Plus negative verification cases (`verify`): forged data is rejected.

use serde_json::{json, Value};
use virtlab::labfile::build_chapters;
use virtlab::{hv, migration, numa, qcow2, verify_with, virtq, GoalStatus, Spec, Strictness, Task};

const DEFINITIONS: &str = include_str!("../data/tasks.json");

fn task(id: &str) -> Task {
    build_chapters(DEFINITIONS)
        .expect("chapters build")
        .into_iter()
        .flat_map(|c| c.tasks)
        .find(|t| t.id == id)
        .unwrap_or_else(|| panic!("no task {id}"))
}

fn statuses(t: &Task, submitted: &Value) -> Vec<(String, GoalStatus)> {
    t.verify(submitted).goals.into_iter().map(|g| (g.id, g.status)).collect()
}

fn all_verified(t: &Task, submitted: &Value) {
    let v = t.verify(submitted);
    assert!(v.solved, "{}: {:?}", t.id, v);
    assert!(v.goals.iter().all(|g| g.status == GoalStatus::Verified), "{}: {:?}", t.id, v);
    // and in strict mode
    assert!(verify_with(&t.spec, submitted, Strictness::Strict).solved);
}

fn status_of(t: &Task, submitted: &Value, goal: &str) -> GoalStatus {
    statuses(t, submitted).into_iter().find(|(id, _)| id == goal).map(|(_, s)| s).unwrap()
}

fn is_rejected(s: &GoalStatus) -> bool {
    matches!(s, GoalStatus::Rejected { .. })
}

// ---------------------------------------------------------------- hv

fn programs(t: &Task) -> Vec<hv::Program> {
    match &t.spec {
        Spec::Hv { programs } => programs.clone(),
        _ => panic!("not hv"),
    }
}

#[test]
fn hv_ideal_runs_reach_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-hv");
    let mut submitted = serde_json::Map::new();
    for p in programs(&t) {
        let translate = hv::needs_translation(&p).unwrap();
        let run = hv::ideal_run(&p, translate).unwrap();
        let fin = hv::replay(&p, &run).unwrap();
        assert!(fin.ok && fin.mistakes == 0, "{}", p.id);
        submitted.insert(p.id.clone(), json!({ "translate": translate, "mistakes": 0, "trace": run.steps }));
    }
    // POPF needs translation, the others do not
    assert!(hv::needs_translation(&programs(&t)[2]).unwrap());
    assert!(!hv::needs_translation(&programs(&t)[0]).unwrap());
    all_verified(&t, &Value::Object(submitted));
}

#[test]
fn hv_popf_without_translation_fails_and_silent_is_counted() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-hv");
    let p = programs(&t).into_iter().find(|p| p.id == "popf").unwrap();
    let run = hv::ideal_run(&p, false).unwrap();
    assert!(run.steps.contains(&hv::Step::Silent));
    let fin = hv::replay(&p, &run).unwrap();
    assert!(!fin.ok && fin.state.silent && fin.state.vif == 0);
    // the server rejects such a run even if the client claimed "success"
    let sub = json!({ "popf": { "translate": false, "mistakes": 0, "trace": run.steps } });
    assert!(is_rejected(&status_of(&t, &sub, "popf")));
}

#[test]
fn hv_session_behaves_like_the_react_lab() {
    locales::set_locale(i18n::Locale::Ru);
    let p = programs(&task("virt-sim-hv")).into_iter().find(|p| p.id == "irq").unwrap();
    let mut s = hv::Session::new(&p.code, false).unwrap();
    assert!(!s.started());
    assert!(s.set_translate(true));
    // CLI is a trap: step is blocked, a wrong choice is a mistake, the state does not change
    assert_eq!(s.step(), hv::Stepped::Blocked);
    assert!(matches!(s.choose("vif ← 1"), hv::Choice::Wrong { .. }));
    assert_eq!(s.state().mistakes, 1);
    assert_eq!(s.state().pc, 0);
    assert_eq!(s.choose("nonexistent option"), hv::Choice::Invalid);
    assert_eq!(s.choose("виртуальный флаг vif ← 0"), hv::Choice::Applied);
    assert!(s.started());
    assert!(!s.set_translate(false), "translation cannot change after start");
    // IRQ with vif = 0: only "put in the queue" is correct
    assert!(matches!(s.choose("доставить гостю сейчас"), hv::Choice::Wrong { .. }));
    assert_eq!(s.choose("поставить в очередь"), hv::Choice::Applied);
    assert_eq!(s.choose("поставить в очередь"), hv::Choice::Applied);
    assert_eq!(s.state().queue, vec![1, 2]);
    assert_eq!(s.choose("vif ← 1 и доставить очередь"), hv::Choice::Applied);
    assert_eq!(s.state().delivered, vec![1, 2]);
    let hv::Choice::Finished(f) = s.choose("остановить виртуальный процессор гостя")
    else {
        panic!("expected a halt")
    };
    assert!(f.ok);
    assert_eq!(f.mistakes, 2);
    assert_eq!(s.current(), None);
    assert_eq!(s.state().log.len(), 5);
}

#[test]
fn hv_verify_rejects_forged_data() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-hv");
    let ps = programs(&t);
    let base = ps.iter().find(|p| p.id == "base").unwrap();
    let run = hv::ideal_run(base, false).unwrap();
    // the number of mistakes does not match the trace
    let sub = json!({ "base": { "translate": false, "mistakes": 3, "trace": run.steps } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // incomplete trace: the guest is not halted
    let short: Vec<_> = run.steps[..run.steps.len() - 1].to_vec();
    let sub = json!({ "base": { "translate": false, "mistakes": 0, "trace": short } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // an action impossible on this instruction (the first instruction is ADD, not a trap)
    let sub = json!({ "base": { "translate": false, "mistakes": 0, "trace": [{"step": "silent"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // invalid shape
    let sub = json!({ "base": { "translate": "yes" } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // former client: POPF without translation is rejected; the rest is accepted without re-checking
    let legacy = json!({
        "base": { "translate": false, "mistakes": 0 },
        "irq": { "translate": false, "mistakes": 1 },
        "popf": { "translate": false, "mistakes": 0 },
    });
    assert_eq!(status_of(&t, &legacy, "base"), GoalStatus::Unverified);
    assert!(is_rejected(&status_of(&t, &legacy, "popf")));
    assert!(!t.verify(&legacy).solved);
    let legacy_ok = json!({
        "base": { "translate": false, "mistakes": 0 },
        "irq": { "translate": false, "mistakes": 1 },
        "popf": { "translate": true, "mistakes": 0 },
    });
    assert!(t.verify(&legacy_ok).solved, "legacy client is accepted by structure");
    assert!(!verify_with(&t.spec, &legacy_ok, Strictness::Strict).solved);
}

// ---------------------------------------------------------------- ept

#[test]
fn ept_solutions_reach_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-ept");
    let sub = json!({
        "walk": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "one" },
        "scan": { "mode": "shadow", "guest": "4K", "host": "4K", "workload": "scan" },
        "random": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "random" },
        "fork": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "fork" },
    });
    all_verified(&t, &sub);
}

#[test]
fn ept_verify_rejects_wrong_configs() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-ept");
    // 4K/4K in EPT is 24 accesses per miss: the "at most 15" goal is not met
    let sub = json!({ "walk": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "one" } });
    assert!(is_rejected(&status_of(&t, &sub, "walk")));
    // "shadow" mode does not count toward the nested tables goal
    let sub = json!({ "walk": { "mode": "shadow", "guest": "1G", "host": "1G", "workload": "one" } });
    assert!(is_rejected(&status_of(&t, &sub, "walk")));
    // is scanning in EPT more expensive than 15 000?  4K/4K: 2048 × (24 + 1) = 51 200
    let sub = json!({ "scan": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "scan" } });
    assert!(is_rejected(&status_of(&t, &sub, "scan")));
    // a run on a different workload does not count
    let sub = json!({ "fork": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "random" } });
    assert!(is_rejected(&status_of(&t, &sub, "fork")));
    // shadow tables on "fork": 500 exits at 1000 each
    let sub = json!({ "fork": { "mode": "shadow", "guest": "1G", "host": "1G", "workload": "fork" } });
    assert!(is_rejected(&status_of(&t, &sub, "fork")));
    // garbage and an unknown workload
    assert!(is_rejected(&status_of(&t, &json!({ "fork": { "mode": "x" } }), "fork")));
    assert!(is_rejected(&status_of(
        &t,
        &json!({ "fork": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "nope" } }),
        "fork"
    )));
    // no goals — no solution
    let v = t.verify(&json!({}));
    assert!(!v.solved && v.goals.iter().all(|g| g.status == GoalStatus::Missing));
    assert!(!t.verify(&json!(null)).solved);
    assert!(!t.verify(&json!([1, 2])).solved);
}

// ---------------------------------------------------------------- virtq

fn virtq_actions() -> Vec<virtq::Action> {
    use virtq::Action::*;
    vec![
        // batch: two batches of 3 without suppression — 6 buffers, 2 notifications
        Post { n: 3 },
        Post { n: 3 },
        // overflow: 2 free, but posting 3
        Post { n: 3 },
        // suppress: reset the queue, enabled suppression, 10 buffers with a single notification
        Reset,
        Suppress { on: true },
        Post { n: 3 },
        Post { n: 3 },
        Device,
        Device,
        Reap,
        Post { n: 3 },
        Device,
        Reap,
        Post { n: 1 },
    ]
}

#[test]
fn virtq_trace_reaches_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-virtqueue");
    let Spec::Virtq { size, goals } = &t.spec else { panic!() };
    let mut s = virtq::Session::new(*size, goals);
    for a in virtq_actions() {
        s.act(&a);
    }
    assert!(s.solved(), "{:?}", s.done());
    assert_eq!(s.done(), ["batch", "overflow", "suppress"]);
    let sub = json!({ "batch": { "trace": virtq_actions() }, "overflow": { "trace": virtq_actions() }, "suppress": { "trace": virtq_actions() } });
    all_verified(&t, &sub);
}

#[test]
fn virtq_model_rules() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-virtqueue");
    let Spec::Virtq { size, goals } = &t.spec else { panic!() };
    let mut s = virtq::Session::new(*size, goals);
    assert_eq!(s.device(), virtq::Note::DeviceIdle);
    assert_eq!(s.post(3), virtq::Note::Notified { n: 3 });
    assert_eq!(s.post(1), virtq::Note::Notified { n: 1 }, "without suppression every post notifies");
    s.set_suppress(true);
    assert_eq!(s.post(1), virtq::Note::Quiet { n: 1 }, "device is busy — no notification needed");
    assert_eq!(s.post(4), virtq::Note::Overflow { need: 4, free: 3 });
    assert!(s.state().overflow);
    assert_eq!(s.post(3), virtq::Note::Quiet { n: 3 });
    assert!(!s.state().overflow);
    assert_eq!(virtq::free(*size, s.state()), 0);
    for _ in 0..8 {
        assert_eq!(s.device(), virtq::Note::Processed);
    }
    assert!(!s.state().busy, "avail ring is empty — device went to sleep");
    assert_eq!(s.device(), virtq::Note::DeviceIdle);
    s.reap();
    assert_eq!(s.state().used, 0);
    // with suppression, but with the device asleep — a kick is sent
    assert_eq!(s.post(1), virtq::Note::Notified { n: 1 });
}

#[test]
fn virtq_verify_traces_and_legacy() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-virtqueue");
    // a trace in which the "suppress" goal is not reached
    let sub = json!({ "suppress": { "trace": [{"op": "post", "n": 3}] } });
    assert!(is_rejected(&status_of(&t, &sub, "suppress")));
    // unknown action
    let sub = json!({ "batch": { "trace": [{"op": "explode"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "batch")));
    // trace too long
    let long: Vec<_> = (0..virtlab::verify::MAX_TRACE + 1).map(|_| json!({"op": "device"})).collect();
    assert!(is_rejected(&status_of(&t, &json!({ "batch": { "trace": long } }), "batch")));
    // the former client sends true: accepted by structure, but not verified
    let legacy = json!({ "batch": true, "overflow": true, "suppress": true });
    let v = t.verify(&legacy);
    assert!(v.solved);
    assert!(v.goals.iter().all(|g| g.status == GoalStatus::Unverified));
    assert!(!verify_with(&t.spec, &legacy, Strictness::Strict).solved);
    // false means "no goal", as in JavaScript
    assert_eq!(status_of(&t, &json!({ "batch": false }), "batch"), GoalStatus::Missing);
}

// ---------------------------------------------------------------- qcow2

fn qcow2_actions() -> Vec<qcow2::Action> {
    use qcow2::Action::*;
    vec![
        // deep: a chain of 4 layers, cluster 0 is in the base — 4 lookups
        Snapshot,
        Snapshot,
        Snapshot,
        Read { cluster: 0 },
        // squash: two merges — 4 layers become 2
        Commit,
        Commit,
        // rollback: write to the top layer, roll back, read — the data is the old one
        Snapshot,
        Write { cluster: 0, data: "E".into() },
        Revert,
        Read { cluster: 0 },
    ]
}

#[test]
fn qcow2_trace_reaches_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-qcow2");
    let Spec::Qcow2 { base, goals, .. } = &t.spec else { panic!() };
    let mut s = qcow2::Session::new(&virtlab::spec::base_map(base), goals);
    for a in qcow2_actions() {
        s.act(&a);
    }
    assert!(s.solved(), "{:?}", s.done());
    assert_eq!(s.done(), ["deep", "squash", "rollback"]);
    assert_eq!(s.chain().len(), 2);
    let tr = json!({ "trace": qcow2_actions() });
    all_verified(&t, &json!({ "deep": tr, "squash": tr, "rollback": tr }));
}

#[test]
fn qcow2_model_rules() {
    locales::set_locale(i18n::Locale::Ru);
    let base = qcow2::default_base();
    let chain = qcow2::initial_chain(&base);
    let c = qcow2::snapshot(&chain, 1);
    let (c, copy_up) = qcow2::write(&c, 0, "Z");
    assert!(copy_up, "cluster 0 was in the base — copy on write");
    let (c, copy_up) = qcow2::write(&c, 7, "Y");
    assert!(!copy_up);
    let r = qcow2::read(&c, 0);
    assert_eq!((r.value.as_deref(), r.depth, r.lookups, r.layer.as_deref()), (Some("Z"), Some(0), 1, Some("слой 1")));
    let r = qcow2::read(&c, 1);
    assert_eq!((r.value.as_deref(), r.depth, r.lookups, r.layer.as_deref()), (Some("B"), Some(1), 2, Some("база")));
    let r = qcow2::read(&c, 5);
    assert_eq!((r.value, r.depth, r.lookups), (None, None, 2));
    let merged = qcow2::commit(&c).unwrap();
    assert_eq!(merged.len(), 1);
    assert_eq!(merged[0].name, "база");
    assert_eq!(merged[0].data[&0], "Z");
    assert!(qcow2::commit(&merged).is_none());
    assert!(qcow2::revert(&merged).is_none());
    assert_eq!(qcow2::revert(&c).unwrap(), chain);
}

#[test]
fn qcow2_verify_traces_and_legacy() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-qcow2");
    // reading from the base with a 2-layer chain — "deep" is not reached
    let sub = json!({ "deep": { "trace": [{"op": "snapshot"}, {"op": "read", "cluster": 0}] } });
    assert!(is_rejected(&status_of(&t, &sub, "deep")));
    // a rollback without a read does not confirm "rollback"
    let sub = json!({ "rollback": { "trace": [{"op": "snapshot"}, {"op": "write", "cluster": 0, "data": "E"}, {"op": "revert"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "rollback")));
    let legacy = json!({ "deep": true, "squash": true, "rollback": true });
    assert!(t.verify(&legacy).solved);
    assert!(!verify_with(&t.spec, &legacy, Strictness::Strict).solved);
}

// ---------------------------------------------------------------- numa

#[test]
fn numa_plans_reach_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-numa");
    let sub = json!({
        "small": {
            "A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
            "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false},
        },
        "wide": {
            "E": {"cpu": "wide", "mem": "wide", "vnuma": true},
            "F": {"cpu": "0", "mem": "0", "vnuma": true}, "G": {"cpu": "1", "mem": "1", "vnuma": true},
        },
    });
    all_verified(&t, &sub);
}

#[test]
fn numa_verify_rejects_bad_plans() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-numa");
    // everything on node 0 does not fit (16 cores on 8)
    let all0: Value = json!({"A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "0", "mem": "0", "vnuma": false}, "D": {"cpu": "0", "mem": "0", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": all0 }), "small")));
    // fits, but memory and CPUs are on different nodes: 25% remote with a threshold of 0
    let remote = json!({"A": {"cpu": "0", "mem": "1", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": remote }), "small")));
    // a large machine without a virtual topology: 0.5 × 12 / 16 = 37.5% > 20%
    let novnuma = json!({"E": {"cpu": "wide", "mem": "wide", "vnuma": false},
        "F": {"cpu": "0", "mem": "0", "vnuma": false}, "G": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "wide": novnuma }), "wide")));
    // a machine missing from the plan, a nonexistent node
    assert!(is_rejected(&status_of(&t, &json!({ "small": {"A": {"cpu": "0", "mem": "0", "vnuma": false}} }), "small")));
    let ghost = json!({"A": {"cpu": "5", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": ghost }), "small")));
    // a placement that fails the second goal does not count the whole exercise
    let ok_small = json!({
        "A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false},
    });
    let v = t.verify(&json!({ "small": ok_small }));
    assert!(!v.solved);
    assert_eq!(v.goals[0].status, GoalStatus::Verified);
    assert_eq!(v.goals[1].status, GoalStatus::Missing);
}

#[test]
fn numa_threshold_boundary() {
    locales::set_locale(i18n::Locale::Ru);
    // boundary: an average share of exactly 0.1875 (vnuma) passes the 0.2 threshold, 0.375 does not
    let nodes = numa::default_nodes();
    let sc = numa::default_scenarios().remove(1);
    let mut plan = numa::default_plan(&sc.vms);
    plan.insert("E".into(), numa::Placement { cpu: numa::Place::Wide, mem: numa::Place::Wide, vnuma: true });
    plan.insert("G".into(), numa::Placement { cpu: numa::Place::Node(1), mem: numa::Place::Node(1), vnuma: false });
    let ev = numa::evaluate(&nodes, &sc.vms, &plan).unwrap();
    assert!(!ev.over);
    assert_eq!(ev.avg, 0.1875);
    assert!(matches!(numa::accept(&nodes, &sc, &plan).unwrap(), numa::Accept::Ok { .. }));
}

// ---------------------------------------------------------------- migration

fn migration_sub() -> Value {
    json!({
        "calm": { "dirty": 300, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": null },
        "busy": { "dirty": 2000, "bw": 1250, "downtimeMs": 50, "autoConverge": true, "compress": true, "postcopyAfter": null },
        "wild": { "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 1 },
    })
}

#[test]
fn migration_params_reach_every_goal() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-migration");
    all_verified(&t, &migration_sub());
    // and the simulations themselves yield the required outcomes
    let scs = migration::default_scenarios();
    let r = migration::simulate(&scs[0].input(100.0, false, false, None));
    assert_eq!(r.outcome, migration::Outcome::Precopy);
    assert!(r.downtime <= 100);
    let r = migration::simulate(&scs[2].input(100.0, false, false, Some(1)));
    assert_eq!((r.outcome, r.downtime), (migration::Outcome::Postcopy, 20));
}

#[test]
fn migration_verify_rejects_cheating() {
    locales::set_locale(i18n::Locale::Ru);
    let t = task("virt-sim-migration");
    let mut sub = migration_sub();
    // "active guest" without throttling does not converge
    sub["busy"] = json!({ "dirty": 2000, "bw": 1250, "downtimeMs": 600, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "busy")));
    // tampered scenario rates: the guest barely writes
    sub["busy"] = json!({ "dirty": 1, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "busy")));
    // allowed downtime outside the slider: a huge threshold "solves" any goal
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 1.0e9, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 5, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    // post-copy after 0 or 99 rounds
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 0 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 99 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    // less memory — easier to migrate
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "postcopyAfter": 1, "mem": 1024 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    // optional fields of the former client may be omitted
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 100 });
    assert_eq!(status_of(&t, &sub, "calm"), GoalStatus::Verified);
    // negative and non-numeric values
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": -100 });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    sub["calm"] = json!({ "dirty": "300" });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
}

// ---------------------------------------------------------------- common

#[test]
fn every_spec_has_goals_and_is_valid() {
    locales::set_locale(i18n::Locale::Ru);
    for c in build_chapters(DEFINITIONS).unwrap() {
        for t in &c.tasks {
            t.spec.validate().unwrap();
            let goals = t.spec.goals();
            assert!(goals.len() >= 2, "{}", t.id);
            assert!(goals.iter().all(|g| !g.text.is_empty()));
            // an empty solution is unsolved, no goal counts
            let v = t.verify(&json!({}));
            assert!(!v.solved);
            assert_eq!(v.goals.len(), goals.len());
        }
    }
    assert_eq!(virtlab::LAB_IDS.len(), 9);
    for id in virtlab::LAB_IDS {
        assert!(virtlab::builtin(id).is_some(), "{id}");
    }
    assert!(virtlab::builtin("virt-sim-nope").is_none());
}
