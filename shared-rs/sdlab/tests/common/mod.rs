//! Общие помощники тестов: пути к данным и золотым файлам.
#![allow(dead_code)]

use std::path::PathBuf;

use sdlab::import::GoldenChapter;
use sdlab::LabChapter;

pub fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/sd")
}

pub fn golden_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/golden")
}

pub fn chapters() -> Vec<LabChapter> {
    sdlab::data::read_dir(&data_dir()).expect("файлы данных читаются")
}

pub fn golden() -> Vec<GoldenChapter> {
    let mut paths: Vec<PathBuf> = std::fs::read_dir(golden_dir()).expect("каталог golden").filter_map(|e| e.ok().map(|e| e.path())).collect();
    paths.sort();
    paths
        .iter()
        .map(|p| serde_json::from_str(&std::fs::read_to_string(p).expect("чтение")).unwrap_or_else(|e| panic!("{}: {e}", p.display())))
        .collect()
}

/// Равенство чисел с относительным допуском; нечисловые значения считаются равными друг другу.
pub fn close(a: f64, b: f64, tol: f64) -> bool {
    if !a.is_finite() || !b.is_finite() {
        return !a.is_finite() && !b.is_finite();
    }
    (a - b).abs() <= tol * a.abs().max(b.abs()).max(1e-12)
}
