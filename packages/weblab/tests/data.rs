//! Data files `backend/data/labs/web`: conditions parse, the reference solution passes, the starter does not, ids are unique.

use std::{collections::BTreeSet, path::PathBuf};

use serde_json::Value;
use weblab::{verify::self_check, Task};

fn dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/web")
}

#[test]
fn every_task_has_a_working_reference() {
    locales::set_locale(i18n::Locale::Ru);
    let mut files: Vec<PathBuf> = std::fs::read_dir(dir()).expect("labs/web dir").filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")).collect();
    files.sort();
    assert!(!files.is_empty(), "no data files");
    let mut seen = BTreeSet::new();
    let mut bad = Vec::new();
    let mut n = 0;
    for f in files {
        let doc: Value = serde_json::from_slice(&std::fs::read(&f).unwrap()).unwrap();
        assert_eq!(doc["lab"], "web", "{}", f.display());
        for t in doc["tasks"].as_array().expect("tasks") {
            let id = t["id"].as_str().unwrap().to_string();
            assert!(seen.insert(format!("{}:{id}", doc["chapter"])), "duplicate id {id}");
            for key in ["title", "statement", "hint"] {
                assert!(!t[key].as_str().unwrap_or("").is_empty(), "{id}: empty field {key}");
            }
            n += 1;
            match serde_json::from_value::<Task>(t["spec"].clone()) {
                Err(e) => bad.push(format!("{id}: spec failed to parse: {e}")),
                Ok(task) => {
                    if let Err(e) = self_check(&task) {
                        bad.push(format!("{id}: {e}"));
                    }
                }
            }
        }
    }
    assert!(bad.is_empty(), "of {n} tasks failed the self-check:\n{}", bad.join("\n"));
}
