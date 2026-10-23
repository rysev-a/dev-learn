//! Дифференциальные тесты: Rust-модели против «золотых» результатов прежних TypeScript-моделей
//! (`tests/golden/virt.json`, выгрузка `cd frontend && node scripts/virt-export.mjs`). Сравнение точное, в том числе дробных чисел.

use std::collections::BTreeMap;

use serde::de::DeserializeOwned;
use serde_json::Value;
use virtlab::{ept, hv, migration, numa, qcow2, virtq};

fn golden() -> Value {
    serde_json::from_str(include_str!("golden/virt.json")).expect("золотой файл читается")
}

fn get<T: DeserializeOwned>(v: &Value, key: &str) -> T {
    serde_json::from_value(v[key].clone()).unwrap_or_else(|e| panic!("поле {key}: {e}"))
}

fn arr<'a>(v: &'a Value, key: &str) -> &'a Vec<Value> {
    v[key].as_array().unwrap_or_else(|| panic!("поле {key} — не массив"))
}

fn instr(s: &str) -> hv::Instr {
    hv::Instr::parse(s).expect("команда разбирается")
}

#[test]
fn hv_matches_ts() {
    let g = golden();
    let g = &g["hv"];
    let defaults = hv::default_programs();
    let progs = arr(g, "programs");
    assert_eq!(progs.len(), defaults.len());
    for (p, d) in progs.iter().zip(&defaults) {
        let prog: hv::Program = serde_json::from_value(serde_json::json!({
            "id": p["id"], "title": p["title"], "code": p["code"], "goal": p["goal"],
        }))
        .unwrap();
        assert_eq!(&prog, d, "программа {}", d.id);
        let code: Vec<hv::Instr> = d.code.iter().map(|c| instr(c)).collect();
        assert_eq!(hv::expected(&code), get::<hv::GuestState>(p, "expected"), "expected {}", d.id);
    }

    let mut steps_checked = 0;
    for w in arr(g, "walks") {
        let translate = w["translate"].as_bool().unwrap();
        for st in arr(w, "steps") {
            let ins = instr(st["ins"].as_str().unwrap());
            let state: hv::GuestState = get(st, "state");
            let want_info: hv::Inspection = get(st, "inspection");
            let info = hv::inspect(&ins, &state, translate);
            assert_eq!(info, want_info, "{} (трансляция {translate})", st["ins"]);
            let next = match info {
                hv::Inspection::Silent { .. } => hv::GuestState { pc: state.pc + 1, silent: true, ..state.clone() },
                _ => hv::apply(&ins, &state),
            };
            assert_eq!(next, get::<hv::GuestState>(st, "after"), "после {}", st["ins"]);
            steps_checked += 1;
        }
    }
    assert!(steps_checked > 30);

    for p in arr(g, "probes") {
        let ins = instr(p["ins"].as_str().unwrap());
        let state: hv::GuestState = get(p, "state");
        let translate = p["translate"].as_bool().unwrap();
        assert_eq!(hv::inspect(&ins, &state, translate), get::<hv::Inspection>(p, "inspection"), "проба {}", p["ins"]);
        assert_eq!(hv::apply(&ins, &state), get::<hv::GuestState>(p, "after"), "применение {}", p["ins"]);
    }
}

#[test]
fn ept_matches_ts() {
    let g = golden();
    let g = &g["ept"];
    let workloads = ept::default_workloads();
    let goals = ept::default_goals();

    for (gw, w) in arr(g, "workloads").iter().zip(&workloads) {
        assert_eq!(gw["id"], w.id.as_str());
        assert_eq!(gw["title"], w.title.as_str());
        assert_eq!(gw["note"], w.note.as_str());
        let t = w.make();
        assert_eq!(gw["len"].as_u64().unwrap(), t.addrs.len() as u64, "{}", w.id);
        assert_eq!(gw["maps"].as_u64().unwrap(), t.maps, "{}", w.id);
        assert_eq!(gw["sum"].as_u64().unwrap(), t.addrs.iter().sum::<u64>(), "сумма адресов {}", w.id);
        let first: Vec<u64> = get(gw, "first");
        let last: Vec<u64> = get(gw, "last");
        assert_eq!(first, t.addrs[..first.len()], "{}", w.id);
        assert_eq!(last, t.addrs[t.addrs.len() - last.len()..], "{}", w.id);
    }
    for (gg, d) in arr(g, "goals").iter().zip(&goals) {
        assert_eq!(gg["id"], d.id.as_str());
        assert_eq!(gg["text"], d.text.as_str());
        assert_eq!(gg["workload"], d.workload.as_str());
    }

    for w in arr(g, "walks") {
        let (mode, guest, host): (ept::Mode, ept::PageSize, ept::PageSize) =
            (get(w, "mode"), get(w, "guest"), get(w, "host"));
        assert_eq!(u64::from(ept::walk_cost(mode, guest, host)), w["walk"].as_u64().unwrap());
    }
    let runs = arr(g, "runs");
    assert_eq!(runs.len(), 2 * 3 * 3 * 4);
    for r in runs {
        let input: ept::SimInput = serde_json::from_value(
            serde_json::json!({ "mode": r["mode"], "guest": r["guest"], "host": r["host"], "workload": r["workload"] }),
        )
        .unwrap();
        let got = ept::simulate(&workloads, &input).unwrap();
        assert_eq!(got, get::<ept::SimRun>(r, "result"), "{input:?}");
        let want_goals: Vec<String> = get(r, "goals");
        assert_eq!(ept::achieved(&workloads, &goals, &input).unwrap(), want_goals, "{input:?}");
    }
}

#[test]
fn virtq_matches_ts() {
    let g = golden();
    let g = &g["virtq"];
    assert_eq!(g["size"].as_u64().unwrap(), u64::from(virtq::SIZE));
    let goals = virtq::default_goals();
    for (gg, d) in arr(g, "goals").iter().zip(&goals) {
        assert_eq!(gg["id"], d.id.as_str());
        assert_eq!(gg["text"], d.text.as_str());
    }
    let mut done_any = false;
    for seq in arr(g, "sequences") {
        let mut s = virtq::Session::new(virtq::SIZE, &goals);
        for (i, st) in seq.as_array().unwrap().iter().enumerate() {
            let a: virtq::Action = get(st, "action");
            s.act(&a);
            assert_eq!(s.state(), &get::<virtq::QueueState>(st, "state"), "шаг {i} {a:?}");
            assert_eq!(u64::from(virtq::free(virtq::SIZE, s.state())), st["free"].as_u64().unwrap());
            assert_eq!(s.suppress(), st["suppress"].as_bool().unwrap(), "шаг {i}");
            assert_eq!(s.done(), get::<Vec<String>>(st, "done"), "цели, шаг {i}");
            done_any |= !s.done().is_empty();
        }
    }
    assert!(done_any, "в наборе должны встречаться достигнутые цели");
}

#[test]
fn numa_matches_ts() {
    let g = golden();
    let g = &g["numa"];
    let nodes: Vec<numa::Node> = get(g, "nodes");
    assert_eq!(nodes, numa::default_nodes());
    let defaults = numa::default_scenarios();
    for (gs, d) in arr(g, "scenarios").iter().zip(&defaults) {
        let sc: numa::Scenario = serde_json::from_value(serde_json::json!({
            "id": gs["id"], "title": gs["title"], "vms": gs["vms"], "goal": gs["goal"], "max": gs["max"],
        }))
        .unwrap();
        assert_eq!(&sc, d);
        for (i, c) in arr(gs, "cases").iter().enumerate() {
            let plan: numa::Plan = get(c, "plan");
            let ev = numa::evaluate(&nodes, &sc.vms, &plan).unwrap();
            assert_eq!(ev.load, get::<Vec<numa::Load>>(c, "load"), "{} #{i}", sc.id);
            assert_eq!(ev.over, c["over"].as_bool().unwrap(), "{} #{i}", sc.id);
            assert_eq!(ev.avg, c["avg"].as_f64().unwrap(), "{} #{i}", sc.id);
            let per: BTreeMap<String, f64> = get(c, "per");
            let got: BTreeMap<String, f64> = ev.per.iter().cloned().collect();
            assert_eq!(got, per, "{} #{i}", sc.id);
            let acc = matches!(numa::accept(&nodes, &sc, &plan).unwrap(), numa::Accept::Ok { .. });
            assert_eq!(acc, c["accepted"].as_bool().unwrap(), "{} #{i}", sc.id);
        }
    }
    for r in arr(g, "remote") {
        let (cpu, mem, vnuma): (numa::Place, numa::Place, bool) = (get(r, "cpu"), get(r, "mem"), get(r, "vnuma"));
        assert_eq!(numa::remote(cpu, mem, vnuma), r["remote"].as_f64().unwrap());
    }
}

#[test]
fn qcow2_matches_ts() {
    let g = golden();
    let g = &g["qcow2"];
    let base: BTreeMap<u32, String> = get(g, "base");
    assert_eq!(base, qcow2::default_base());
    assert_eq!(g["clusters"].as_u64().unwrap(), u64::from(qcow2::CLUSTERS));
    let goals = qcow2::default_goals();
    for (gg, d) in arr(g, "goals").iter().zip(&goals) {
        assert_eq!(gg["id"], d.id.as_str());
        assert_eq!(gg["text"], d.text.as_str());
    }
    let mut seen = [false; 3];
    for seq in arr(g, "sequences") {
        let mut s = qcow2::Session::new(&base, &goals);
        for (i, st) in seq.as_array().unwrap().iter().enumerate() {
            let a: qcow2::Action = get(st, "action");
            let note = s.act(&a);
            let out = &st["out"];
            match (&a, &note) {
                (qcow2::Action::Write { .. }, qcow2::Note::Write { copy_up }) => {
                    assert_eq!(*copy_up, out["copy_up"].as_bool().unwrap(), "шаг {i}");
                }
                (qcow2::Action::Read { .. }, qcow2::Note::Read(r)) => {
                    assert_eq!(r.value, get::<Option<String>>(out, "value"), "шаг {i}");
                    assert_eq!(r.depth, get::<Option<usize>>(out, "depth"), "шаг {i}");
                    assert_eq!(r.lookups, out["lookups"].as_u64().unwrap() as usize, "шаг {i}");
                    assert_eq!(r.layer, get::<Option<String>>(out, "layer"), "шаг {i}");
                }
                (qcow2::Action::Commit, n) => {
                    assert_eq!(*n != qcow2::Note::CommitImpossible, out["ok"].as_bool().unwrap(), "шаг {i}");
                }
                (qcow2::Action::Revert, n) => {
                    assert_eq!(*n != qcow2::Note::RevertImpossible, out["ok"].as_bool().unwrap(), "шаг {i}");
                }
                (qcow2::Action::Snapshot, qcow2::Note::Snapshot) => {}
                other => panic!("шаг {i}: неожиданная пара {other:?}"),
            }
            assert_eq!(s.chain(), get::<Vec<qcow2::Layer>>(st, "chain"), "цепочка, шаг {i}");
            assert_eq!(s.max_len(), st["max_len"].as_u64().unwrap() as usize, "шаг {i}");
            assert_eq!(s.done(), get::<Vec<String>>(st, "done"), "цели, шаг {i}");
        }
        for (k, g) in goals.iter().enumerate() {
            seen[k] |= s.done().contains(&g.id);
        }
    }
    assert!(seen.iter().any(|x| *x), "в наборе должны встречаться достигнутые цели");
}

#[test]
fn migration_matches_ts() {
    let g = golden();
    let g = &g["migration"];
    assert_eq!(g["mem_mib"].as_f64().unwrap(), migration::MEM_MIB);
    let scenarios = migration::default_scenarios();
    for (gs, d) in arr(g, "scenarios").iter().zip(&scenarios) {
        assert_eq!(gs["id"], d.id.as_str());
        assert_eq!(gs["title"], d.title.as_str());
        assert_eq!(gs["dirty"].as_f64().unwrap(), d.dirty);
        assert_eq!(gs["bw"].as_f64().unwrap(), d.bw);
        assert_eq!(gs["goal"], d.goal.as_str());
        assert_eq!(gs["hint"], d.hint.as_str());
    }
    let cases = arr(g, "cases");
    assert!(cases.len() > 400);
    let mut outcomes = [0; 3];
    for c in cases {
        let input: migration::MigrationInput = get(c, "input");
        let got = migration::simulate(&input);
        assert_eq!(got, get::<migration::Simulation>(c, "result"), "{input:?}");
        let sc = scenarios.iter().find(|s| c["scenario"] == s.id.as_str()).unwrap();
        assert_eq!(sc.check.check(&got), c["ok"].as_bool().unwrap(), "цель {} при {input:?}", sc.id);
        assert_eq!(sc.reached(&input), c["ok"].as_bool().unwrap());
        outcomes[got.outcome as usize] += 1;
    }
    assert!(outcomes.iter().all(|n| *n > 0), "должны встречаться все исходы: {outcomes:?}");
    for r in arr(g, "rows") {
        let input: migration::MigrationInput = get(r, "input");
        assert_eq!(migration::simulate(&input), get::<migration::Simulation>(r, "result"), "{input:?}");
    }
}
