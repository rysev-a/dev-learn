//! Разовый перенос упражнений книги «Компьютерные сети» из TypeScript в данные.
//!
//! Выгрузка: `cd frontend && node scripts/net-export.mjs /tmp/nx`. Затем
//! `cargo run --release --bin import -- /tmp/nx ../../backend/app/data/labs/net`
//! (второй аргумент — каталог `labs/net` или его родитель `backend/app/data`): пишет `15-NN.json` на каждую главу.

use netlab::export::{convert_all, Export};
use std::path::{Path, PathBuf};

fn main() {
    if let Err(e) = run() {
        eprintln!("ошибка: {e}");
        std::process::exit(1);
    }
}

fn run() -> Result<(), String> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let (Some(src), Some(dst)) = (args.first(), args.get(1)) else {
        return Err("использование: import <выгрузка (каталог или scenarios.json)> <каталог данных>".into());
    };
    let src = Path::new(src);
    let file: PathBuf = if src.is_dir() { src.join("scenarios.json") } else { src.to_path_buf() };
    let text = std::fs::read_to_string(&file).map_err(|e| format!("{}: {e}", file.display()))?;
    let export: Export = serde_json::from_str(&text).map_err(|e| format!("{}: {e}", file.display()))?;
    let chapters = convert_all(&export)?;
    let mut dir = PathBuf::from(dst);
    if !dir.ends_with("labs/net") {
        dir = dir.join("labs").join("net");
    }
    std::fs::create_dir_all(&dir).map_err(|e| format!("{}: {e}", dir.display()))?;
    let mut tasks = 0;
    for c in &chapters {
        let path = dir.join(c.file_name());
        let json = serde_json::to_string_pretty(c).map_err(|e| e.to_string())?;
        std::fs::write(&path, json + "\n").map_err(|e| format!("{}: {e}", path.display()))?;
        tasks += c.tasks.len();
    }
    println!("глав {}, упражнений {tasks} → {}", chapters.len(), dir.display());
    Ok(())
}
