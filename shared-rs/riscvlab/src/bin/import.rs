//! Перенос упражнений глав 16–17 из выгрузки прежней реализации в файлы данных курса.
//!
//! `cargo run --release --bin import -- <выгрузка.json> <каталог данных>`
//! (выгрузка: `cd frontend && node scripts/riscv-export.mjs <выгрузка.json>`; каталог данных:
//! `backend/app/data/labs/arch`). Пишет только `14-16.json` и `14-17.json`.

use std::path::PathBuf;
use std::process::ExitCode;

use riscvlab::export::Export;
use riscvlab::task::chapter_file_name;

/// Главы, которыми владеет этот крейт.
const CHAPTERS: [(u32, u32); 2] = [(14, 16), (14, 17)];

fn run() -> Result<(), String> {
    let mut args = std::env::args().skip(1);
    let (Some(src), Some(dir)) = (args.next(), args.next()) else {
        return Err("нужно: import <выгрузка.json> <каталог данных>".to_string());
    };
    let text = std::fs::read_to_string(&src).map_err(|e| format!("не прочитать {src}: {e}"))?;
    let export: Export = serde_json::from_str(&text).map_err(|e| format!("выгрузка {src}: {e}"))?;
    let dir = PathBuf::from(dir);
    std::fs::create_dir_all(&dir).map_err(|e| format!("не создать {}: {e}", dir.display()))?;
    for ch in export.chapters {
        let key = (ch.book, ch.chapter);
        if !CHAPTERS.contains(&key) {
            return Err(format!("глава {}-{} не принадлежит этому крейту (только 14-16 и 14-17)", key.0, key.1));
        }
        let chapter = ch.into_lab_chapter().map_err(|e| e.to_string())?;
        let json = chapter.to_canonical_json().map_err(|e| e.to_string())?;
        let path = dir.join(chapter_file_name(chapter.book, chapter.chapter));
        std::fs::write(&path, json).map_err(|e| format!("не записать {}: {e}", path.display()))?;
        println!("{}: задач {}", path.display(), chapter.tasks.len());
    }
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
