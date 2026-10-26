//! Книга 11, глава 13 (раздел «HTML и разметка»): слайды как данные. Заглушка: глава пишется.

use content::Chapter;

pub fn chapter() -> Chapter {
    Chapter { book: 11, chapter: 13, rubric: "СОВРЕМЕННЫЙ FRONTEND / HTML И РАЗМЕТКА".into(), slides: vec![] }
}
