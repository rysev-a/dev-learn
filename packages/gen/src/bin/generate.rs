//! Content generators: `cargo run --release --bin generate -- <data directory>` (usually `backend/data/slides`).
//! Write the chapters whose source is Rust code; they override the same-named files from the TypeScript port.

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
