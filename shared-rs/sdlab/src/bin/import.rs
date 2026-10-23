//! Импорт выгрузки TypeScript-сценариев в данные.
//!
//! `cargo run --release --bin import -- <каталог выгрузки> <каталог данных> [каталог золотых файлов]`
//!
//! Читает `<выгрузка>/18-NN.json` (их делает `frontend/scripts/sd-export.mjs`), пишет канонические файлы глав
//! `<данные>/18-NN.json` (обычно `backend/app/data/labs/sd`) и золотые результаты TypeScript-движка в
//! `<золотые>/18-NN.json` (по умолчанию `shared-rs/sdlab/tests/golden`).

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use sdlab::data::file_name;
use sdlab::LabChapter;
use sdlab::{import, pretty};

fn run(export: &Path, data: &Path, golden: &Path) -> Result<(), Box<dyn std::error::Error>> {
    std::fs::create_dir_all(data)?;
    std::fs::create_dir_all(golden)?;
    let mut files: Vec<PathBuf> = std::fs::read_dir(export)?.filter_map(|e| e.ok().map(|e| e.path())).filter(|p| p.extension().is_some_and(|x| x == "json")).collect();
    files.sort();
    let (mut chapters, mut tasks, mut cases) = (0, 0, 0);
    for f in files {
        let (chapter, g) = import::convert(&std::fs::read_to_string(&f)?)?;
        let name = file_name(chapter.book, chapter.chapter);
        let text = pretty::to_string(&chapter)?;
        // файл должен читаться обратно без потерь
        let back = LabChapter::parse(&text)?;
        if back != chapter {
            return Err(format!("{name}: данные изменились при записи и чтении").into());
        }
        std::fs::write(data.join(&name), text)?;
        std::fs::write(golden.join(&name), serde_json::to_string(&g)?)?;
        chapters += 1;
        tasks += chapter.tasks.len();
        cases += g.tasks.iter().map(|t| t.cases.len()).sum::<usize>();
    }
    println!("глав {chapters}, упражнений {tasks}, золотых случаев {cases}");
    Ok(())
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 2 {
        eprintln!("использование: import <каталог выгрузки> <каталог данных> [каталог золотых файлов]");
        return ExitCode::from(2);
    }
    let golden = args.get(2).map_or_else(|| Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/golden"), PathBuf::from);
    match run(Path::new(&args[0]), Path::new(&args[1]), &golden) {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("ошибка: {e}");
            ExitCode::FAILURE
        }
    }
}
