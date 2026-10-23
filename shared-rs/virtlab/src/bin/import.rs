//! Запись файлов данных лаборатории книги 17: `<каталог данных>/labs/virt/17-NN.json`.
//!
//! Запуск: `cargo run --release --bin import -- <каталог данных>` (например `../../backend/app/data`);
//! `--check` ничего не пишет и завершается кодом 1, если файлы отстали от определений.
//! Определения упражнений — `data/tasks.json` (выгрузка из `backend/app/exercises/virt_tasks/labs.py`:
//! `python3 -I data/export_labs.py`), описания симуляторов (сценарии, цели) — из крейта.

use std::path::PathBuf;
use std::process::ExitCode;

use virtlab::labfile::build_chapters;

const DEFINITIONS: &str = include_str!("../../data/tasks.json");

fn main() -> ExitCode {
    let mut check = false;
    let mut dir: Option<PathBuf> = None;
    for a in std::env::args().skip(1) {
        if a == "--check" {
            check = true;
        } else {
            dir = Some(PathBuf::from(a));
        }
    }
    let Some(dir) = dir else {
        eprintln!("запуск: import [--check] <каталог данных>");
        return ExitCode::from(2);
    };
    match run(&dir.join("labs").join("virt"), check) {
        Ok(true) => ExitCode::SUCCESS,
        Ok(false) => ExitCode::from(1),
        Err(e) => {
            eprintln!("ошибка: {e}");
            ExitCode::from(2)
        }
    }
}

fn run(out: &std::path::Path, check: bool) -> Result<bool, Box<dyn std::error::Error>> {
    let chapters = build_chapters(DEFINITIONS)?;
    if !check {
        std::fs::create_dir_all(out)?;
    }
    let mut stale = 0;
    for c in &chapters {
        let path = out.join(c.file_name());
        let text = c.to_canonical_json()?;
        if check {
            if std::fs::read_to_string(&path).ok().as_deref() != Some(text.as_str()) {
                eprintln!("отстал: {}", path.display());
                stale += 1;
            }
        } else {
            std::fs::write(&path, text)?;
            println!("{} — упражнений {}", path.display(), c.tasks.len());
        }
    }
    Ok(stale == 0)
}
