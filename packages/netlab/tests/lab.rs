//! Exercise data and server-side check: self-check (port of `net-selfcheck.mjs`), file format, `verify`.

use netlab::check::{check_goals, Step};
use netlab::lab::{check_integrity, load_dir, verify, verify_json, LabChapter, Task};
use netlab::model::state_from_json;
use netlab::types::*;
use serde_json::{json, Value};
use std::path::PathBuf;

fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/net")
}

fn chapters() -> Vec<LabChapter> {
    load_dir(&data_dir()).expect("exercise data")
}

fn tasks() -> Vec<Task> {
    chapters().into_iter().flat_map(|c| c.tasks).collect()
}

/// Canonical state -> former client form: devices as an object by id, keys in camelCase.
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

/// Same, but as a string and preserving device order (a `Value` object sorts keys).
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
fn data_is_complete_and_consistent() {
    locales::set_locale(i18n::Locale::Ru);
    let cs = chapters();
    assert_eq!(cs.len(), 18, "chapters with a lab: 1-8, 10-13, 15-20");
    let mut ids = std::collections::HashSet::new();
    let mut n = 0;
    for c in &cs {
        assert_eq!(c.book, 15);
        assert!(c.chapter != 9 && c.chapter != 14, "chapters 9 and 14 are Python code");
        assert_eq!(c.lab, "net");
        for t in &c.tasks {
            assert!(ids.insert(t.id.clone()), "duplicate id {}", t.id);
            assert!(t.id.starts_with(&format!("n{}-", c.chapter)), "{}: id does not match the chapter number", t.id);
            assert!(!t.spec.goals.is_empty() && !t.spec.solution.is_empty(), "{}", t.id);
            n += 1;
        }
    }
    assert_eq!(n, 79);
}

/// Self-check: in the initial network at least one goal is not met, the reference solution passes.
#[test]
fn self_check_starter_fails_reference_passes() {
    locales::set_locale(i18n::Locale::Ru);
    for t in tasks() {
        let start = check_goals(&t.spec.start_state(), &t.spec.goals);
        assert!(!start.iter().all(|r| r.ok), "{}: already solved in the starter", t.id);
        let solved = t.spec.solved_state().unwrap_or_else(|e| panic!("{}: the solution failed: {e}", t.id));
        let res = check_goals(&solved, &t.spec.goals);
        for r in &res {
            assert!(r.ok, "{}: the reference does not meet the goal '{}': {}", t.id, r.text, r.detail);
        }
    }
}

#[test]
fn data_files_are_canonical_and_lossless() {
    locales::set_locale(i18n::Locale::Ru);
    for c in chapters() {
        let path = data_dir().join(c.file_name());
        let text = std::fs::read_to_string(&path).expect("file");
        // file = serialization of the parsed data: nothing extra in it and nothing lost while parsing
        let again = serde_json::to_string_pretty(&c).expect("serialization") + "\n";
        assert_eq!(text, again, "{} is not in canonical form (cargo run --release --bin import)", path.display());
        let v1: Value = serde_json::from_str(&text).expect("json");
        let c2 = LabChapter::from_json(&text).expect("parse");
        assert_eq!(v1, serde_json::to_value(&c2).expect("value"));
    }
}

#[test]
fn state_round_trip() {
    locales::set_locale(i18n::Locale::Ru);
    for t in tasks() {
        let s = t.spec.start_state();
        let j = serde_json::to_string(&s).unwrap();
        let back: NetState = serde_json::from_str(&j).unwrap();
        assert_eq!(j, serde_json::to_string(&back).unwrap(), "{}", t.id);
        assert_eq!(back.devices.len(), s.devices.len());
        // device and key order is preserved
        let ids: Vec<&str> = s.devices.iter().map(|d| d.id.as_str()).collect();
        let ids2: Vec<&str> = back.devices.iter().map(|d| d.id.as_str()).collect();
        assert_eq!(ids, ids2);
        // the former client form (camelCase, devices as an object) is read the same way
        let from_ts = state_from_json(&state_to_ts_string(&s)).unwrap_or_else(|e| panic!("{}: {e}", t.id));
        assert_eq!(serde_json::to_value(&from_ts).unwrap(), serde_json::to_value(&s).unwrap(), "{}", t.id);
    }
}

#[test]
fn verify_accepts_reference_and_rejects_starter() {
    locales::set_locale(i18n::Locale::Ru);
    for t in tasks() {
        let solved = t.spec.solved_state().expect("solution");
        let v = verify(&t.spec, &solved);
        assert!(v.ok, "{}: reference rejected: {:?}", t.id, v);
        assert_eq!(v.goals.len(), t.spec.goals.len());
        // what the client sends: a JSON string without caches (in the former form too)
        let canon = serde_json::to_string(&solved.stripped()).unwrap();
        assert!(verify_json(&t.spec, &canon).ok, "{}", t.id);
        let ts = state_to_ts_string(&solved);
        let v = verify_json(&t.spec, &ts);
        assert!(v.ok, "{}: previous client format: {v:?}", t.id);
        let bad = verify(&t.spec, &t.spec.start_state());
        assert!(!bad.ok && bad.error.is_none() && bad.goals.iter().any(|g| !g.ok), "{}: starter accepted", t.id);
    }
}

#[test]
fn verify_rejects_forgeries() {
    locales::set_locale(i18n::Locale::Ru);
    let all = tasks();
    // locked device
    let t = all.iter().find(|t| t.spec.start.devices.iter().any(|d| d.locked)).expect("exercise with a locked device");
    let mut s = t.spec.solved_state().unwrap();
    let id = t.spec.start.devices.iter().find(|d| d.locked).unwrap().id.clone();
    s.devices.get_mut(&id).unwrap().forward = !s.devices.get(&id).unwrap().forward;
    let v = verify(&t.spec, &s);
    assert!(!v.ok && v.error.is_some(), "a locked device was changed: {v:?}");

    // extra and missing device
    let t = &all[0];
    let mut s = t.spec.solved_state().unwrap();
    s.devices.insert(Device::new("evil", DeviceKind::Host, "Stranger", 0.0, 0.0));
    assert!(verify(&t.spec, &s).error.is_some());
    let mut s = t.spec.solved_state().unwrap();
    let first = s.devices.iter().next().unwrap().id.clone();
    let mut kept = NetState { pki: s.pki.clone(), links: vec![], ..Default::default() };
    for d in s.devices.iter().filter(|d| d.id != first) {
        kept.devices.insert(d.clone());
    }
    s = kept;
    assert!(verify(&t.spec, &s).error.is_some());

    // cable to a nonexistent port and two cables into one port
    let mut s = t.spec.solved_state().unwrap();
    s.links.push(Link::new("pc1:nope", "pc2:nope"));
    assert!(verify(&t.spec, &s).error.is_some());
    let mut s = t.spec.solved_state().unwrap();
    let l = s.links[0].clone();
    s.links.push(l);
    assert!(verify(&t.spec, &s).error.is_some());

    // cables cannot be changed if the tool is locked
    let t = all.iter().find(|t| !t.spec.tools.cable && !t.spec.start.links.is_empty()).expect("without cables");
    let mut s = t.spec.solved_state().unwrap();
    s.links.remove(0);
    let v = verify(&t.spec, &s);
    assert!(v.error.is_some(), "{v:?}");

    // cable with "superluminal" properties
    let t = all.iter().find(|t| t.spec.tools.cable).expect("with a cable");
    let mut s = t.spec.solved_state().unwrap();
    for l in s.links.iter_mut() {
        l.km = 0.0;
        l.mbps = 1e9;
    }
    assert!(check_integrity(&t.spec, &s).is_err());

    // garbage instead of a state
    assert!(verify_json(&t.spec, "{").error.is_some());
    assert!(verify_json(&t.spec, "[]").error.is_some());
    assert!(verify_json(&t.spec, r#"{"devices":{},"links":[]}"#).error.is_some());
}

#[test]
fn solution_steps_in_data_are_readable() {
    locales::set_locale(i18n::Locale::Ru);
    let all = tasks();
    let cmds = all.iter().flat_map(|t| t.spec.solution.iter()).filter(|s| matches!(s, Step::Cmd { .. })).count();
    let cables = all.iter().flat_map(|t| t.spec.solution.iter()).filter(|s| matches!(s, Step::Cable { .. })).count();
    assert!(cmds > 100 && cables >= 9);
    let j = serde_json::to_value(Step::Cable { a: "a".into(), b: "b".into(), extra: None }).unwrap();
    assert_eq!(j, json!({"op": "cable", "a": "a", "b": "b"}));
    let j = serde_json::to_value(Step::Cmd { dev: "pc".into(), line: "ip link".into() }).unwrap();
    assert_eq!(j, json!({"op": "cmd", "dev": "pc", "line": "ip link"}));
}
