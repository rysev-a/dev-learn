//! Общее для тестов: данные из `backend/app/data/labs/arch` и «золото» из TypeScript.
#![allow(dead_code)]

use archlab::ArchLab;
use serde_json::Value;
use std::path::PathBuf;

/// Каталог данных лаборатории (через `CARGO_MANIFEST_DIR`).
pub fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/arch")
}

/// Все главы 6–15.
pub fn lab() -> ArchLab {
    let lab = ArchLab::load_dir(&data_dir()).expect("данные лаборатории загружаются");
    assert_eq!(lab.chapters().count(), 10, "главы 6–15");
    lab
}

/// Золотые результаты TypeScript-движка (`frontend/scripts/arch-export.mjs`).
pub fn golden() -> Value {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/golden.json");
    let text = std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("{}: {e}", path.display()));
    serde_json::from_str(&text).expect("golden.json разбирается")
}

/// Сравнение JSON как данных: числа — по значению (150 и 150.0 равны), `null` и отсутствие поля равны.
pub fn json_eq(a: &Value, b: &Value) -> bool {
    match (a, b) {
        (Value::Number(x), Value::Number(y)) => x.as_f64() == y.as_f64(),
        (Value::Array(x), Value::Array(y)) => x.len() == y.len() && x.iter().zip(y).all(|(p, q)| json_eq(p, q)),
        (Value::Object(x), Value::Object(y)) => {
            let keys: std::collections::BTreeSet<&String> = x.keys().chain(y.keys()).collect();
            keys.into_iter().all(|k| {
                let (p, q) = (x.get(k).unwrap_or(&Value::Null), y.get(k).unwrap_or(&Value::Null));
                json_eq(p, q)
            })
        }
        _ => a == b,
    }
}

/// Отпечаток плоской схемы (как `fingerprint` в экспортёре): число вентилей, проводов, памяти и FNV-1a строки.
pub fn fingerprint(c: &archlab::model::Circuit) -> (usize, usize, usize, u32) {
    let opt = |s: &Option<String>| s.clone().unwrap_or_default();
    let list = |v: &[Option<String>]| v.iter().map(opt).collect::<Vec<_>>().join(",");
    let gates = c.gates.iter().map(|g| format!("{}:{}", g.id, g.ty.name())).collect::<Vec<_>>().join("|");
    let wires = c
        .wires
        .iter()
        .map(|w| format!("{}>{}:{}", w.from.node, w.to.node, serde_json::to_value(w.to.pin).ok().and_then(|v| v.as_str().map(String::from)).unwrap_or_default()))
        .collect::<Vec<_>>()
        .join("|");
    let natives = c
        .natives
        .iter()
        .map(|n| {
            let kind = if n.kind == archlab::model::NativeKind::Rom { "rom" } else { "ram" };
            let din = n.din.as_deref().map(list).unwrap_or_default();
            [n.id.clone(), kind.to_string(), list(&n.addr), din, opt(&n.we), opt(&n.clk), n.dout.join(",")].join("/")
        })
        .collect::<Vec<_>>()
        .join("|");
    let s = format!("{gates}#{wires}#{natives}");
    let mut h: u32 = 2166136261;
    for u in s.encode_utf16() {
        h ^= u as u32;
        h = h.wrapping_mul(16777619);
    }
    (c.gates.len(), c.wires.len(), c.natives.len(), h)
}
