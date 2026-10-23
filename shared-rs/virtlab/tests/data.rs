//! Файлы данных (`backend/app/data/labs/virt`) и serde-круг: данные читаются, пишутся обратно без потерь и совпадают
//! с тем, что строит `import` из `labs.py` и описаний симуляторов.

use std::path::PathBuf;

use serde::{de::DeserializeOwned, Serialize};
use serde_json::{json, Value};
use virtlab::labfile::build_chapters;
use virtlab::{ept, hv, migration, numa, qcow2, virtq, Goal, GoalStatus, LabChapter, Spec, Verdict};

fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/virt")
}

fn round_trip<T: Serialize + DeserializeOwned + PartialEq + std::fmt::Debug>(x: &T) {
    let v = serde_json::to_value(x).unwrap();
    let back: T = serde_json::from_value(v.clone()).unwrap();
    assert_eq!(&back, x);
    let text = serde_json::to_string(x).unwrap();
    let back: T = serde_json::from_str(&text).unwrap();
    assert_eq!(&back, x);
    assert_eq!(serde_json::to_value(&back).unwrap(), v);
}

#[test]
fn data_files_are_canonical_and_up_to_date() {
    let built = build_chapters(include_str!("../data/tasks.json")).unwrap();
    assert_eq!(built.iter().map(|c| c.chapter).collect::<Vec<_>>(), [2, 4, 6, 9, 10, 11]);
    let mut files: Vec<_> =
        std::fs::read_dir(data_dir()).expect("каталог данных есть").map(|e| e.unwrap().file_name()).collect();
    files.sort();
    let want: Vec<_> = built.iter().map(|c| std::ffi::OsString::from(c.file_name())).collect();
    assert_eq!(files, want, "набор файлов: запустите import");
    for c in &built {
        let text = std::fs::read_to_string(data_dir().join(c.file_name())).unwrap();
        let parsed = LabChapter::from_json(&text).unwrap();
        parsed.validate().unwrap();
        assert_eq!(&parsed, c, "{}: файл отстал от определений, запустите import", c.file_name());
        assert_eq!(parsed.to_canonical_json().unwrap(), text, "{}: файл не канонический", c.file_name());
        assert_eq!((parsed.book, parsed.lab.as_str()), (17, "virt"));
        // порядок глав и id совпадают с labs.py
        assert!(parsed.tasks.iter().all(|t| t.id.starts_with("virt-sim-")));
    }
}

#[test]
fn spec_files_serialize_with_sim_tag() {
    for c in build_chapters(include_str!("../data/tasks.json")).unwrap() {
        for t in &c.tasks {
            let v = serde_json::to_value(&t.spec).unwrap();
            assert_eq!(v["sim"], t.spec.sim());
            round_trip(&t.spec);
            round_trip(t);
        }
        round_trip(&c);
    }
}

#[test]
fn model_types_round_trip() {
    for id in virtlab::LAB_IDS {
        round_trip(&virtlab::builtin(id).unwrap());
    }
    round_trip(&hv::initial());
    round_trip(&hv::Run {
        translate: true,
        steps: vec![hv::Step::Direct, hv::Step::Silent, hv::Step::Trap { label: "x".into() }],
    });
    round_trip(&hv::Inspection::Silent { why: "w".into() });
    round_trip(&hv::Inspection::Trap {
        title: "t".into(),
        options: vec![hv::TrapOption { label: "l".into(), ok: true, why: None }],
    });
    round_trip(&virtq::initial());
    for a in [
        virtq::Action::Post { n: 2 },
        virtq::Action::Device,
        virtq::Action::Reap,
        virtq::Action::Reset,
        virtq::Action::Suppress { on: true },
    ] {
        round_trip(&a);
    }
    for a in [
        qcow2::Action::Snapshot,
        qcow2::Action::Write { cluster: 3, data: "Q".into() },
        qcow2::Action::Read { cluster: 1 },
        qcow2::Action::Commit,
        qcow2::Action::Revert,
    ] {
        round_trip(&a);
    }
    round_trip(&qcow2::initial_chain(&qcow2::default_base()));
    let sim = migration::simulate(&migration::default_scenarios()[1].input(100.0, true, false, None));
    round_trip(&sim);
    let r = ept::simulate(
        &ept::default_workloads(),
        &ept::SimInput {
            mode: ept::Mode::Ept,
            guest: ept::PageSize::M2,
            host: ept::PageSize::K4,
            workload: "scan".into(),
        },
    )
    .unwrap();
    round_trip(&r);
    round_trip(&numa::default_plan(&numa::default_scenarios()[0].vms));
    round_trip(&Goal::new("a", "b"));
    round_trip(&Verdict {
        solved: false,
        goals: vec![
            virtlab::GoalVerdict { id: "a".into(), status: GoalStatus::Verified },
            virtlab::GoalVerdict { id: "b".into(), status: GoalStatus::Rejected { reason: "r".into() } },
        ],
    });
}

#[test]
fn wire_formats_match_the_old_ts_client() {
    // так прежний клиент присылает параметры миграции и настройки трансляции
    let m: migration::MigrationInput = serde_json::from_str(
        r#"{"dirty":300,"bw":1250,"downtimeMs":300,"autoConverge":false,"compress":false,"postcopyAfter":null}"#,
    )
    .unwrap();
    assert_eq!((m.dirty, m.downtime_ms, m.postcopy_after), (300.0, 300.0, None));
    let m: migration::MigrationInput = serde_json::from_str(
        r#"{"dirty":6000,"bw":1250,"downtimeMs":100,"autoConverge":true,"compress":true,"postcopyAfter":2}"#,
    )
    .unwrap();
    assert_eq!(m.postcopy_after, Some(2));
    // обратно — те же имена полей
    let v = serde_json::to_value(&m).unwrap();
    assert_eq!(v["downtimeMs"], 100.0);
    assert_eq!(v["postcopyAfter"], 2);
    let e: ept::SimInput =
        serde_json::from_value(json!({"mode": "shadow", "guest": "2M", "host": "1G", "workload": "fork"})).unwrap();
    assert_eq!((e.mode, e.guest, e.host), (ept::Mode::Shadow, ept::PageSize::M2, ept::PageSize::G1));
    assert_eq!(serde_json::to_value(ept::PageSize::K4).unwrap(), "4K");
    let plan: numa::Plan = serde_json::from_value(json!({"A": {"cpu": "wide", "mem": "1", "vnuma": true}})).unwrap();
    assert_eq!(plan["A"].cpu, numa::Place::Wide);
    assert_eq!(plan["A"].mem, numa::Place::Node(1));
    assert!(serde_json::from_value::<numa::Place>(json!("left")).is_err());
}

#[test]
fn validation_catches_broken_data() {
    let mut spec = virtlab::builtin("virt-sim-ept").unwrap();
    if let Spec::Ept { goals, .. } = &mut spec {
        goals[0].workload = "нет такой".into();
    }
    assert!(spec.validate().is_err());
    let mut spec = virtlab::builtin("virt-sim-hv").unwrap();
    if let Spec::Hv { programs } = &mut spec {
        programs[0].code.push("ADD".into());
    }
    assert!(spec.validate().is_err());
    let mut spec = virtlab::builtin("virt-sim-numa").unwrap();
    if let Spec::Numa { scenarios, .. } = &mut spec {
        scenarios[1].id = scenarios[0].id.clone();
    }
    assert!(spec.validate().is_err());
    assert!(build_chapters(r#"[{"chapter":2,"id":"virt-sim-nope","title":"","statement":"","hint":""}]"#).is_err());
    let v: Value = serde_json::from_str(include_str!("../data/tasks.json")).unwrap();
    assert_eq!(v.as_array().unwrap().len(), 6);
}
