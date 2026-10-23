//! Разовый перенос: `cargo run --release --bin import_ts_slides -- <выгрузка TS> <каталог данных>`.
//! Читает JSON-файлы выгрузки (`frontend/scripts/slides-export.mjs`), собирает главы, проверяет их и пишет файлы данных.
//! Главы с ручной отрисовкой сцен пропускаются (их заменяют генераторы).

use std::path::PathBuf;

fn main() -> anyhow::Result<()> {
    let mut args = std::env::args().skip(1);
    let (src, dst) = (PathBuf::from(args.next().expect("каталог выгрузки")), PathBuf::from(args.next().expect("каталог данных")));
    let (mut done, mut skipped, mut slides) = (0, Vec::new(), 0);
    let mut files: Vec<_> = std::fs::read_dir(&src)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")).collect();
    files.sort();
    for p in files {
        let name = p.file_stem().and_then(|s| s.to_str()).unwrap_or("");
        let (book, num) = name.split_once('-').expect("имя BB-CC");
        let key = format!("{}:{}", book.parse::<i64>()?, num.parse::<i64>()?);
        let doc: serde_json::Value = serde_json::from_slice(&std::fs::read(&p)?)?;
        match gen::ts_import::chapter(&key, &doc, &gen::kit_scene) {
            Ok(ch) => match gen::write_chapter(&dst, &ch) {
                Ok(()) => {
                    slides += ch.slides.len();
                    done += 1;
                }
                Err(e) => skipped.push(format!("{key}: {e:#}")),
            },
            Err(e) => skipped.push(format!("{key}: {e:#}")),
        }
    }
    println!("глав {done}, слайдов {slides}; пропущено {}", skipped.len());
    for s in skipped.iter().take(40) {
        println!("  {}", s.chars().take(240).collect::<String>());
    }
    Ok(())
}
