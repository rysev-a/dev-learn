//! Проверка раскладки всех сцен в файлах данных: `cargo run --release --bin lint_slides -- <каталог данных> [глава…]`.
//! Печатает замечания (текст шире ячейки, элемент за холстом) и итог; код возврата 1, если замечания есть.

use std::path::PathBuf;

use content::{Block, Chapter, Scene};

fn main() -> anyhow::Result<()> {
    let mut args = std::env::args().skip(1);
    let dir = PathBuf::from(args.next().expect("каталог данных"));
    let only: Vec<String> = args.collect();
    let mut files: Vec<_> = std::fs::read_dir(&dir)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")).collect();
    files.sort();
    let (mut scenes, mut warnings) = (0, 0);
    for f in files {
        let name = f.file_stem().and_then(|s| s.to_str()).unwrap_or("").to_string();
        if !only.is_empty() && !only.iter().any(|o| *o == name) {
            continue;
        }
        let ch: Chapter = serde_json::from_slice(&std::fs::read(&f)?)?;
        for (i, s) in ch.slides.iter().enumerate() {
            for b in &s.body {
                if let Block::Scene(spec) = b {
                    scenes += 1;
                    for w in Scene::compile(spec).map_err(|e| anyhow::anyhow!("{name}: {e}"))?.lint() {
                        warnings += 1;
                        println!("{name} слайд {}: {w}", i + 1);
                    }
                }
            }
        }
    }
    println!("сцен {scenes}, замечаний {warnings}");
    std::process::exit(i32::from(warnings > 0));
}
