//! Генераторы содержимого. Результат — файлы данных `backend/data/slides/<книга>-<глава>.json` (канонический JSON
//! структуры [`content::Chapter`]); бэкенд читает их при сиде и кладёт в базу.

use std::path::Path;

use content::{Chapter, SceneSpec};

pub mod dm;
pub mod py_ch00;
pub mod web_ch13;
pub mod web_ch14;
pub mod web_ch15;

/// Главы, которые пишут генераторы на Rust (источник — этот код, а не перенос из TypeScript).
pub fn generated() -> Vec<Chapter> {
    // главы без слайдов — заготовки (их ещё пишут), в данные не попадают
    vec![py_ch00::chapter(), web_ch13::chapter(), web_ch14::chapter(), web_ch15::chapter()].into_iter().filter(|c| !c.slides.is_empty()).collect()
}

/// Имя файла главы: `13-05.json`.
pub fn file_name(book: i64, chapter: i64) -> String {
    format!("{book:02}-{chapter:02}.json")
}

/// Записывает главу как данные (проверяет её перед записью).
pub fn write_chapter(dir: &Path, ch: &Chapter) -> anyhow::Result<()> {
    ch.check().map_err(|e| anyhow::anyhow!("{e}"))?;
    std::fs::create_dir_all(dir)?;
    std::fs::write(dir.join(file_name(ch.book, ch.chapter)), serde_json::to_string(ch)?)?;
    Ok(())
}

/// Сцены, переписанные из ручной отрисовки React (`kit.tsx`) в данные: по имени прежнего компонента.
pub fn kit_scene(name: &str) -> Option<SceneSpec> {
    dm::scenes().into_iter().find(|(n, _)| *n == name).map(|(_, spec)| spec)
}
