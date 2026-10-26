//! Генераторы содержимого: `cargo run --release --bin generate -- <каталог данных>` (обычно `backend/data/slides`).
//! Пишут главы, у которых источник — код на Rust; перекрывают одноимённые файлы из переноса TypeScript.

use std::path::PathBuf;

fn main() -> anyhow::Result<()> {
    let dir = PathBuf::from(std::env::args().nth(1).expect("каталог данных: backend/data/slides"));
    let chapters = gen::generated();
    for ch in &chapters {
        gen::write_chapter(&dir, ch)?;
        println!("{}:{} — {} слайдов → {}", ch.book, ch.chapter, ch.slides.len(), gen::file_name(ch.book, ch.chapter));
    }
    Ok(())
}
