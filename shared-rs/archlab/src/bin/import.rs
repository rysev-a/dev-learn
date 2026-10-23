//! `cargo run --release --bin import -- <выгрузка.json> <каталог данных>`
//!
//! Читает выгрузку `frontend/scripts/arch-export.mjs` (`{"chapters": [...]}`), проверяет её типами крейта и
//! эталонами (каждое эталонное решение обязано проходить `verify`, а пустое — нет) и пишет канонические файлы
//! `<каталог данных>/labs/arch/<книга>-<глава:02>.json` (`backend/app/data` — каталог данных бэкенда).

use archlab::exercise::{LabChapter, Spec};
use archlab::{verify, ArchLab};
use serde::Deserialize;
use std::path::PathBuf;
use std::process::ExitCode;

#[derive(Deserialize)]
struct Export {
    chapters: Vec<LabChapter>,
}

fn run() -> Result<(), String> {
    let mut args = std::env::args().skip(1);
    let (Some(src), Some(dir)) = (args.next(), args.next()) else {
        return Err("нужно: import <выгрузка.json> <каталог данных>".into());
    };
    let text = std::fs::read_to_string(&src).map_err(|e| format!("{src}: {e}"))?;
    let export: Export = serde_json::from_str(&text).map_err(|e| format!("выгрузка не разобрана: {e}"))?;
    let lab = ArchLab::from_chapters(export.chapters.clone())?;

    // эталоны: решение проходит, пустое — нет
    let lib = lab.reference_library();
    let mut tasks = 0;
    for ch in lab.chapters() {
        for t in &ch.tasks {
            tasks += 1;
            let (reference, empty) = match &t.spec {
                Spec::Circuit(c) => {
                    let Some(sol) = &c.solution else {
                        return Err(format!("{}/{}: нет эталонного решения", ch.chapter, t.id));
                    };
                    let empty = match c.build {
                        archlab::exercise::Build::Gates => r#"{"gates":[],"wires":[]}"#,
                        archlab::exercise::Build::Blocks => r#"{"instances":[],"bus_wires":[]}"#,
                    };
                    (serde_json::to_string(sol).map_err(|e| e.to_string())?, empty.to_string())
                }
                Spec::Asm(a) => (a.solution.clone(), a.starter.clone()),
            };
            let v = verify(t, &reference, &lib);
            if !v.ok {
                return Err(format!("{}/{}: эталон не проходит проверку: {}", ch.chapter, t.id, v.message));
            }
            if verify(t, &empty, &lib).ok {
                return Err(format!("{}/{}: пустое решение проходит проверку", ch.chapter, t.id));
            }
        }
    }

    let out: PathBuf = PathBuf::from(&dir).join("labs").join("arch");
    std::fs::create_dir_all(&out).map_err(|e| format!("{}: {e}", out.display()))?;
    for ch in lab.chapters() {
        let path = out.join(format!("{}-{:02}.json", ch.book, ch.chapter));
        let json = archlab::format::canonical_json(ch).map_err(|e| e.to_string())?;
        std::fs::write(&path, json).map_err(|e| format!("{}: {e}", path.display()))?;
    }
    println!("глав {}, упражнений {tasks} → {}", lab.chapters().count(), out.display());
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("ошибка: {e}");
            ExitCode::FAILURE
        }
    }
}
