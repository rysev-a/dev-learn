//! Data files (`backend/data/labs/virt`) and the serde round trip: data is read, written back losslessly and matches
//! what `import` builds from `labs.py` and the simulator descriptions.

use std::path::PathBuf;

use serde::{de::DeserializeOwned, Serialize};
use serde_json::{json, Value};
use virtlab::labfile::build_chapters;
use virtlab::{ept, hv, migration, numa, qcow2, virtq, Goal, GoalStatus, LabChapter, Spec, Verdict};

fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/virt")
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
    // the scenario text inside `spec` is English; only title/statement/hint are Russian
    let built = i18n::with_locale(i18n::Locale::En, || build_chapters(include_str!("../data/tasks.json")).unwrap());
    let chapters: Vec<(u32, u32)> = built.iter().map(|c| (c.book, c.chapter)).collect();
    assert!(chapters.windows(2).all(|w| w[0] < w[1]), "chapters ascend: {chapters:?}");
    let book17 = [2, 4, 6, 9, 10, 11, 17, 18, 19, 20, 21, 22, 24, 25].map(|c| (17, c));
    assert_eq!(chapters, [&book17[..], &[(19, 10), (19, 11), (19, 12), (19, 16), (19, 20)]].concat());
    let mut files: Vec<_> =
        std::fs::read_dir(data_dir()).expect("data dir exists").map(|e| e.unwrap().file_name()).collect();
    files.sort();
    let want: Vec<_> = built.iter().map(|c| std::ffi::OsString::from(c.file_name())).collect();
    assert_eq!(files, want, "file set: run import");
    for c in &built {
        let text = std::fs::read_to_string(data_dir().join(c.file_name())).unwrap();
        let parsed = LabChapter::from_json(&text).unwrap();
        parsed.validate().unwrap();
        assert_eq!(&parsed, c, "{}: file is stale relative to definitions, run import", c.file_name());
        assert_eq!(parsed.to_canonical_json().unwrap(), text, "{}: file is not canonical", c.file_name());
        assert!(matches!(parsed.book, 17 | 19) && parsed.lab == "virt", "{}", c.file_name());
        // chapter order and ids match labs.py
        assert!(parsed.tasks.iter().all(|t| t.id.starts_with("virt-sim-")));
    }
}

#[test]
fn spec_files_serialize_with_sim_tag() {
    locales::set_locale(i18n::Locale::Ru);
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
    locales::set_locale(i18n::Locale::Ru);
    for id in virtlab::lab_ids() {
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
    locales::set_locale(i18n::Locale::Ru);
    // this is how the former client sends migration parameters and translation settings
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
    // back again — the same field names
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
    locales::set_locale(i18n::Locale::Ru);
    let mut spec = virtlab::builtin("virt-sim-ept").unwrap();
    if let Spec::Ept { goals, .. } = &mut spec {
        goals[0].workload = "no such".into();
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
    assert!(v.as_array().unwrap().len() >= 12);
}

/// Writes the chapter files of `backend/data/labs/virt` from the definitions (`data/tasks.json`) and the built-in simulator descriptions:
/// `cargo test --test data -- --ignored write_data_files`. Run it after changing a scenario or a definition.
#[test]
#[ignore]
fn write_data_files() {
    let built = i18n::with_locale(i18n::Locale::En, || build_chapters(include_str!("../data/tasks.json")).unwrap());
    for c in &built {
        std::fs::write(data_dir().join(c.file_name()), c.to_canonical_json().unwrap()).unwrap();
    }
}
