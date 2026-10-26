//! Дифференциальные тесты: движок на Rust даёт те же результаты, что прежний TypeScript-движок.
//! «Золотые» данные — `tests/golden.json` (их строит `frontend/scripts/net-export.mjs`): сводка проверки целей на
//! исходной и на решённой сети, итоговая решённая сеть и хеши вывода команд терминала.

use netlab::check::{apply_ops, check_goals, GoalResult};
use netlab::lab::{load_dir, Task};
use netlab::term::exec;
use netlab::types::NetState;
use netlab::util::num_str;
use serde_json::Value;
use std::path::PathBuf;

fn fnv(s: &str, basis: u32) -> String {
    let mut h = basis;
    for b in s.bytes() {
        h ^= b as u32;
        h = h.wrapping_mul(16777619);
    }
    format!("{h:08x}")
}

fn hash(s: &str) -> String {
    format!("{}{}", fnv(s, 0x811c9dc5), fnv(s, 0x01000193))
}

fn kind_str<T: serde::Serialize>(k: &T) -> String {
    serde_json::to_value(k).ok().and_then(|v| v.as_str().map(|s| s.to_string())).unwrap_or_default()
}

fn summarize(rs: &[GoalResult]) -> Vec<Value> {
    rs.iter()
        .map(|r| {
            let ev: Vec<String> =
                r.run.events.iter().map(|e| format!("{}|{}|{}|{}", num_str(e.t), e.dev, kind_str(&e.kind), e.text)).collect();
            let hp: Vec<String> = r
                .run
                .hops
                .iter()
                .map(|h| {
                    format!(
                        "{}|{}|{}|{}|{}|{}|{}|{}",
                        num_str(h.t0),
                        num_str(h.t1),
                        h.from,
                        h.from_port,
                        h.to,
                        h.to_port,
                        kind_str(&h.kind),
                        h.label
                    )
                })
                .collect();
            serde_json::json!({
                "id": r.id,
                "ok": r.ok,
                "detail": r.detail,
                "events": r.run.events.len(),
                "ev_hash": hash(&ev.join("\n")),
                "hops": r.run.hops.len(),
                "hop_hash": hash(&hp.join("\n")),
                "delivered": r.run.delivered.len(),
            })
        })
        .collect()
}

fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/net")
}

fn golden() -> Value {
    let p = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/golden.json");
    serde_json::from_str(&std::fs::read_to_string(p).expect("tests/golden.json")).expect("golden.json")
}

fn tasks() -> Vec<Task> {
    load_dir(&data_dir()).expect("данные упражнений").into_iter().flat_map(|c| c.tasks).collect()
}

fn compare_summary(id: &str, what: &str, got: &[Value], want: &Value, errs: &mut Vec<String>) {
    let want = want.as_array().cloned().unwrap_or_default();
    if got.len() != want.len() {
        errs.push(format!("{id}/{what}: целей {} вместо {}", got.len(), want.len()));
        return;
    }
    for (g, w) in got.iter().zip(&want) {
        for key in ["ok", "detail", "events", "ev_hash", "hops", "hop_hash", "delivered"] {
            if g[key] != w[key] {
                errs.push(format!("{id}/{what}/{}: поле {key}: {} вместо {}", w["id"], g[key], w[key]));
            }
        }
    }
}

#[test]
fn цели_совпадают_с_typescript() {
    let gold = golden();
    let mut errs = Vec::new();
    let all = tasks();
    assert!(all.len() >= 79, "упражнений {}", all.len());
    for t in &all {
        let g = &gold["scenarios"][&t.id];
        assert!(g.is_object(), "нет золотых данных для {}", t.id);
        let start = t.spec.start_state();
        compare_summary(&t.id, "start", &summarize(&check_goals(&start, &t.spec.goals)), &g["start"], &mut errs);
        let solved = t.spec.solved_state().unwrap_or_else(|e| panic!("{}: решение не применилось: {e}", t.id));
        compare_summary(&t.id, "solved", &summarize(&check_goals(&solved, &t.spec.goals)), &g["solved"], &mut errs);
    }
    assert!(errs.is_empty(), "{} расхождений:\n{}", errs.len(), errs.iter().take(40).cloned().collect::<Vec<_>>().join("\n"));
}

#[test]
fn решённая_сеть_совпадает_с_typescript() {
    let gold = golden();
    let mut errs = Vec::new();
    for t in &tasks() {
        let g = &gold["scenarios"][&t.id];
        let solved = t.spec.solved_state().expect("решение");
        let changed: Vec<NetState> = Vec::new();
        let _ = changed;
        // устройства: изменившиеся берём из золотых данных, остальные — как в исходной сети
        let ch = g["solved_changed"].as_array().cloned().unwrap_or_default();
        for d in solved.devices.iter() {
            let want: Value = match ch.iter().find(|x| x["id"] == d.id.as_str()) {
                Some(x) => x.clone(),
                None => serde_json::to_value(t.spec.start.devices.get(&d.id).expect("устройство")).unwrap(),
            };
            let want = netlab::export::normalize(&want, false);
            let got = netlab::export::normalize(&serde_json::to_value(d).unwrap(), false);
            if got != want {
                errs.push(format!("{}: устройство {} после решения отличается:\n  rust {got}\n  ts   {want}", t.id, d.id));
            }
        }
        let want_links = netlab::export::normalize(&g["solved_links"], false);
        let got_links = netlab::export::normalize(&serde_json::to_value(&solved.links).unwrap(), false);
        if want_links != got_links {
            errs.push(format!("{}: кабели после решения отличаются:\n  rust {got_links}\n  ts   {want_links}", t.id));
        }
    }
    assert!(errs.is_empty(), "{} расхождений:\n{}", errs.len(), errs.iter().take(10).cloned().collect::<Vec<_>>().join("\n"));
}

fn run_cmds(id: &str, label: &str, state: &NetState, cmds: &Value, errs: &mut Vec<String>) -> usize {
    let mut s = state.stripped();
    let mut n = 0;
    for c in cmds.as_array().cloned().unwrap_or_default() {
        let (dev, line, want) = (c[0].as_str().unwrap_or(""), c[1].as_str().unwrap_or(""), c[2].as_str().unwrap_or(""));
        let r = exec(&mut s, dev, line);
        let tag = match r.changed {
            None => "u",
            Some(true) => "t",
            Some(false) => "f",
        };
        let got = hash(&format!("{tag}|{}", r.out));
        n += 1;
        if got != want {
            errs.push(format!(
                "{id}/{label}: `{dev}$ {line}` — вывод отличается от TypeScript (rust: {:?})",
                r.out.chars().take(300).collect::<String>()
            ));
        }
    }
    n
}

#[test]
fn команды_терминала_совпадают_с_typescript() {
    let gold = golden();
    let mut errs = Vec::new();
    let mut total = 0;
    for t in &tasks() {
        let g = &gold["scenarios"][&t.id];
        total += run_cmds(&t.id, "start", &t.spec.start_state(), &g["cmds_start"], &mut errs);
        total += run_cmds(&t.id, "solved", &t.spec.solved_state().expect("решение"), &g["cmds_solved"], &mut errs);
    }
    assert!(total > 2000, "команд проверено {total}");
    assert!(errs.is_empty(), "{} расхождений из {total}:\n{}", errs.len(), errs.iter().take(25).cloned().collect::<Vec<_>>().join("\n"));
}

#[test]
fn решение_применяется_без_ошибок() {
    for t in &tasks() {
        let mut s = t.spec.start_state();
        apply_ops(&mut s, &t.spec.solution).unwrap_or_else(|e| panic!("{}: {e}", t.id));
    }
}

#[test]
fn краевые_команды_совпадают_с_typescript() {
    let gold = golden();
    let template: Vec<String> =
        gold["edge_template"].as_array().expect("шаблон").iter().map(|v| v.as_str().unwrap_or("").to_string()).collect();
    let mut errs = Vec::new();
    let mut total = 0;
    for t in &tasks() {
        let runs = gold["scenarios"][&t.id]["edge"].as_array().cloned().unwrap_or_default();
        let mut s = t.spec.start_state();
        for run in runs {
            let dev = run["dev"].as_str().unwrap_or("");
            let hashes = run["hashes"].as_str().unwrap_or("");
            let var = |k: &str| run["vars"][k].as_str().unwrap_or("").to_string();
            for (i, tmpl) in template.iter().enumerate() {
                let line =
                    tmpl.replace("{if}", &var("if")).replace("{ip}", &var("ip")).replace("{own}", &var("own")).replace("{gw}", &var("gw"));
                let r = exec(&mut s, dev, &line);
                let tag = match r.changed {
                    None => "u",
                    Some(true) => "t",
                    Some(false) => "f",
                };
                let got = fnv(&format!("{tag}|{}", r.out), 0x811c9dc5);
                total += 1;
                if hashes.get(i * 8..i * 8 + 8) != Some(got.as_str()) {
                    errs.push(format!("{}: `{dev}$ {line}` (rust: {:?})", t.id, r.out.chars().take(200).collect::<String>()));
                }
            }
        }
    }
    assert!(total > 20000, "команд проверено {total}");
    assert!(errs.is_empty(), "{} расхождений из {total}:\n{}", errs.len(), errs.iter().take(40).cloned().collect::<Vec<_>>().join("\n"));
}

#[test]
fn цели_на_промежуточных_и_испорченных_сетях_совпадают_с_typescript() {
    let gold = golden();
    let template: Vec<String> =
        gold["edge_template"].as_array().expect("шаблон").iter().map(|v| v.as_str().unwrap_or("").to_string()).collect();
    let mut errs = Vec::new();
    let mut partials = 0;
    for t in &tasks() {
        let g = &gold["scenarios"][&t.id];
        // промежуточные состояния: после каждого шага решения, кроме последнего
        let mut s = t.spec.start_state();
        let want = g["partial"].as_array().cloned().unwrap_or_default();
        assert_eq!(want.len(), t.spec.solution.len().saturating_sub(1), "{}", t.id);
        for (k, w) in want.iter().enumerate() {
            apply_ops(&mut s, &t.spec.solution[k..k + 1]).expect("шаг");
            compare_summary(&t.id, &format!("partial{k}"), &summarize(&check_goals(&s, &t.spec.goals)), w, &mut errs);
            partials += 1;
        }
        // сеть после краевых команд
        let mut e = t.spec.start_state();
        for run in g["edge"].as_array().cloned().unwrap_or_default() {
            let dev = run["dev"].as_str().unwrap_or("");
            let var = |k: &str| run["vars"][k].as_str().unwrap_or("").to_string();
            for tmpl in &template {
                let line =
                    tmpl.replace("{if}", &var("if")).replace("{ip}", &var("ip")).replace("{own}", &var("own")).replace("{gw}", &var("gw"));
                exec(&mut e, dev, &line);
            }
        }
        compare_summary(&t.id, "edge_goals", &summarize(&check_goals(&e, &t.spec.goals)), &g["edge_goals"], &mut errs);
    }
    assert!(partials > 50, "промежуточных состояний {partials}");
    assert!(errs.is_empty(), "{} расхождений:\n{}", errs.len(), errs.iter().take(30).cloned().collect::<Vec<_>>().join("\n"));
}

#[test]
fn синтетические_цели_совпадают_с_typescript() {
    let gold = golden();
    let mut errs = Vec::new();
    let mut n = 0;
    for t in &tasks() {
        let sy = &gold["scenarios"][&t.id]["synth"];
        let goals: Vec<netlab::check::Goal> = serde_json::from_value(sy["goals"].clone()).unwrap_or_else(|e| panic!("{}: цели: {e}", t.id));
        n += goals.len();
        compare_summary(&t.id, "synth/start", &summarize(&check_goals(&t.spec.start_state(), &goals)), &sy["start"], &mut errs);
        compare_summary(&t.id, "synth/solved", &summarize(&check_goals(&t.spec.solved_state().expect("решение"), &goals)), &sy["solved"], &mut errs);
    }
    assert!(n > 1000, "синтетических целей {n}");
    assert!(errs.is_empty(), "{} расхождений из {n}:\n{}", errs.len(), errs.iter().take(30).cloned().collect::<Vec<_>>().join("\n"));
}
