//! Данные упражнений и серверная проверка: самопроверка (порт `net-selfcheck.mjs`), формат файлов, `verify`.

use netlab::check::{check_goals, Step};
use netlab::lab::{check_integrity, load_dir, verify, verify_json, LabChapter, Task};
use netlab::model::state_from_json;
use netlab::types::*;
use serde_json::{json, Value};
use std::path::PathBuf;

fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/net")
}

fn chapters() -> Vec<LabChapter> {
    load_dir(&data_dir()).expect("данные упражнений")
}

fn tasks() -> Vec<Task> {
    chapters().into_iter().flat_map(|c| c.tasks).collect()
}

/// Каноническое состояние → запись прежнего клиента: устройства объектом по id, ключи в camelCase.
fn to_ts(v: &Value) -> Value {
    const R: &[(&str, &str)] = &[
        ("drop_private", "dropPrivate"),
        ("icmp_block", "icmpBlock"),
        ("arp_static", "arpStatic"),
        ("tls_min", "tlsMin"),
        ("ssh_key", "sshKey"),
        ("known_hosts", "knownHosts"),
        ("not_after", "notAfter"),
        ("host_key", "hostKey"),
        ("password_auth", "passwordAuth"),
        ("gateway_ip", "gatewayIp"),
    ];
    match v {
        Value::Object(m) => {
            let mut o = serde_json::Map::new();
            for (k, x) in m {
                let key = R.iter().find(|(a, _)| a == k).map(|(_, b)| b.to_string()).unwrap_or_else(|| k.clone());
                if key == "devices" {
                    let mut by = serde_json::Map::new();
                    for d in x.as_array().cloned().unwrap_or_default() {
                        by.insert(d["id"].as_str().unwrap_or("").to_string(), to_ts(&d));
                    }
                    o.insert(key, Value::Object(by));
                } else {
                    o.insert(key, to_ts(x));
                }
            }
            Value::Object(o)
        }
        Value::Array(a) => Value::Array(a.iter().map(to_ts).collect()),
        other => other.clone(),
    }
}

/// То же, но строкой и с сохранением порядка устройств (объект `Value` ключи сортирует).
fn state_to_ts_string(s: &NetState) -> String {
    let v = serde_json::to_value(s).unwrap();
    let devs: Vec<String> = v["devices"]
        .as_array()
        .unwrap()
        .iter()
        .map(|d| format!("{}:{}", serde_json::to_string(d["id"].as_str().unwrap()).unwrap(), to_ts(d)))
        .collect();
    let mut o = serde_json::Map::new();
    for k in ["links", "pki"] {
        if !v[k].is_null() {
            o.insert(k.into(), to_ts(&v[k]));
        }
    }
    let mut text = Value::Object(o).to_string();
    text.insert_str(1, &format!("\"devices\":{{{}}}{}", devs.join(","), if text.len() > 2 { "," } else { "" }));
    text
}

#[test]
fn данные_полны_и_согласованы() {
    let cs = chapters();
    assert_eq!(cs.len(), 18, "главы с лабораторией: 1–8, 10–13, 15–20");
    let mut ids = std::collections::HashSet::new();
    let mut n = 0;
    for c in &cs {
        assert_eq!(c.book, 15);
        assert!(c.chapter != 9 && c.chapter != 14, "главы 9 и 14 — код на Python");
        assert_eq!(c.lab, "net");
        for t in &c.tasks {
            assert!(ids.insert(t.id.clone()), "повтор id {}", t.id);
            assert!(t.id.starts_with(&format!("n{}-", c.chapter)), "{}: id не по номеру главы", t.id);
            assert!(!t.spec.goals.is_empty() && !t.spec.solution.is_empty(), "{}", t.id);
            n += 1;
        }
    }
    assert_eq!(n, 79);
}

#[test]
fn ид_и_заголовки_совпадают_с_манифестом_задач() {
    let p = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/exercises/net_tasks/lab_manifest.json");
    let m: Value = serde_json::from_str(&std::fs::read_to_string(p).expect("lab_manifest.json")).expect("json");
    for c in chapters() {
        let want = m[c.chapter.to_string()].as_array().cloned().unwrap_or_default();
        assert_eq!(want.len(), c.tasks.len(), "глава {}", c.chapter);
        for (w, t) in want.iter().zip(&c.tasks) {
            assert_eq!(w["id"], t.id.as_str());
            assert_eq!(w["title"], t.title.as_str());
            assert_eq!(w["statement"], t.statement.as_str());
            assert_eq!(w["hint"], t.hint.as_str());
        }
    }
}

/// Порт `frontend/scripts/net-selfcheck.mjs`: в исходной сети хотя бы одна цель не выполнена, эталон проходит.
#[test]
fn самопроверка_заготовка_не_проходит_эталон_проходит() {
    for t in tasks() {
        let start = check_goals(&t.spec.start_state(), &t.spec.goals);
        assert!(!start.iter().all(|r| r.ok), "{}: уже решено в заготовке", t.id);
        let solved = t.spec.solved_state().unwrap_or_else(|e| panic!("{}: решение упало: {e}", t.id));
        let res = check_goals(&solved, &t.spec.goals);
        for r in &res {
            assert!(r.ok, "{}: эталон не проходит цель «{}»: {}", t.id, r.text, r.detail);
        }
    }
}

#[test]
fn файлы_данных_канонические_и_без_потерь() {
    for c in chapters() {
        let path = data_dir().join(c.file_name());
        let text = std::fs::read_to_string(&path).expect("файл");
        // файл = сериализация разобранного: в нём нет лишнего и ничего не теряется при разборе
        let again = serde_json::to_string_pretty(&c).expect("сериализация") + "\n";
        assert_eq!(text, again, "{} не в каноническом виде (cargo run --release --bin import)", path.display());
        let v1: Value = serde_json::from_str(&text).expect("json");
        let c2 = LabChapter::from_json(&text).expect("разбор");
        assert_eq!(v1, serde_json::to_value(&c2).expect("значение"));
    }
}

#[test]
fn состояние_туда_и_обратно() {
    for t in tasks() {
        let s = t.spec.start_state();
        let j = serde_json::to_string(&s).unwrap();
        let back: NetState = serde_json::from_str(&j).unwrap();
        assert_eq!(j, serde_json::to_string(&back).unwrap(), "{}", t.id);
        assert_eq!(back.devices.len(), s.devices.len());
        // порядок устройств и ключей сохраняется
        let ids: Vec<&str> = s.devices.iter().map(|d| d.id.as_str()).collect();
        let ids2: Vec<&str> = back.devices.iter().map(|d| d.id.as_str()).collect();
        assert_eq!(ids, ids2);
        // прежняя запись клиента (camelCase, устройства объектом) читается так же
        let from_ts = state_from_json(&state_to_ts_string(&s)).unwrap_or_else(|e| panic!("{}: {e}", t.id));
        assert_eq!(serde_json::to_value(&from_ts).unwrap(), serde_json::to_value(&s).unwrap(), "{}", t.id);
    }
}

#[test]
fn verify_принимает_эталон_и_отклоняет_заготовку() {
    for t in tasks() {
        let solved = t.spec.solved_state().expect("решение");
        let v = verify(&t.spec, &solved);
        assert!(v.ok, "{}: эталон отклонён: {:?}", t.id, v);
        assert_eq!(v.goals.len(), t.spec.goals.len());
        // то, что присылает клиент: строка JSON без кэшей (и в прежней записи тоже)
        let canon = serde_json::to_string(&solved.stripped()).unwrap();
        assert!(verify_json(&t.spec, &canon).ok, "{}", t.id);
        let ts = state_to_ts_string(&solved);
        let v = verify_json(&t.spec, &ts);
        assert!(v.ok, "{}: прежняя запись клиента: {v:?}", t.id);
        let bad = verify(&t.spec, &t.spec.start_state());
        assert!(!bad.ok && bad.error.is_none() && bad.goals.iter().any(|g| !g.ok), "{}: заготовка принята", t.id);
    }
}

#[test]
fn verify_отклоняет_подделки() {
    let all = tasks();
    // закрытое устройство
    let t = all.iter().find(|t| t.spec.start.devices.iter().any(|d| d.locked)).expect("упражнение с закрытым устройством");
    let mut s = t.spec.solved_state().unwrap();
    let id = t.spec.start.devices.iter().find(|d| d.locked).unwrap().id.clone();
    s.devices.get_mut(&id).unwrap().forward = !s.devices.get(&id).unwrap().forward;
    let v = verify(&t.spec, &s);
    assert!(!v.ok && v.error.is_some(), "закрытое устройство изменили: {v:?}");

    // лишнее и пропавшее устройство
    let t = &all[0];
    let mut s = t.spec.solved_state().unwrap();
    s.devices.insert(Device::new("evil", DeviceKind::Host, "Чужой", 0.0, 0.0));
    assert!(verify(&t.spec, &s).error.is_some());
    let mut s = t.spec.solved_state().unwrap();
    let first = s.devices.iter().next().unwrap().id.clone();
    let mut kept = NetState { pki: s.pki.clone(), links: vec![], ..Default::default() };
    for d in s.devices.iter().filter(|d| d.id != first) {
        kept.devices.insert(d.clone());
    }
    s = kept;
    assert!(verify(&t.spec, &s).error.is_some());

    // кабель к несуществующему порту и два кабеля в один порт
    let mut s = t.spec.solved_state().unwrap();
    s.links.push(Link::new("pc1:nope", "pc2:nope"));
    assert!(verify(&t.spec, &s).error.is_some());
    let mut s = t.spec.solved_state().unwrap();
    let l = s.links[0].clone();
    s.links.push(l);
    assert!(verify(&t.spec, &s).error.is_some());

    // кабели менять нельзя, если инструмент закрыт
    let t = all.iter().find(|t| !t.spec.tools.cable && !t.spec.start.links.is_empty()).expect("без кабелей");
    let mut s = t.spec.solved_state().unwrap();
    s.links.remove(0);
    let v = verify(&t.spec, &s);
    assert!(v.error.is_some(), "{v:?}");

    // кабель со «сверхсветовыми» свойствами
    let t = all.iter().find(|t| t.spec.tools.cable).expect("с кабелем");
    let mut s = t.spec.solved_state().unwrap();
    for l in s.links.iter_mut() {
        l.km = 0.0;
        l.mbps = 1e9;
    }
    assert!(check_integrity(&t.spec, &s).is_err());

    // мусор вместо состояния
    assert!(verify_json(&t.spec, "{").error.is_some());
    assert!(verify_json(&t.spec, "[]").error.is_some());
    assert!(verify_json(&t.spec, r#"{"devices":{},"links":[]}"#).error.is_some());
}

#[test]
fn шаги_решения_в_данных_читаемы() {
    let all = tasks();
    let cmds = all.iter().flat_map(|t| t.spec.solution.iter()).filter(|s| matches!(s, Step::Cmd { .. })).count();
    let cables = all.iter().flat_map(|t| t.spec.solution.iter()).filter(|s| matches!(s, Step::Cable { .. })).count();
    assert!(cmds > 100 && cables >= 9);
    let j = serde_json::to_value(Step::Cable { a: "a".into(), b: "b".into(), extra: None }).unwrap();
    assert_eq!(j, json!({"op": "cable", "a": "a", "b": "b"}));
    let j = serde_json::to_value(Step::Cmd { dev: "pc".into(), line: "ip link".into() }).unwrap();
    assert_eq!(j, json!({"op": "cmd", "dev": "pc", "line": "ip link"}));
}
