//! «Дискретная математика»: схемы глав 1–10, переписанные с ручной отрисовки React (`slides/anim/C<n>*.tsx`, `kit.tsx`) на данные.
//! Каждая глава — файл `chNN.rs` с функцией `scenes()`: пары «имя прежнего компонента — описание сцены». Остальное в слайдах
//! (заголовки, «ГЛАВНОЕ», врезки) переносится из TypeScript автоматически.

use content::SceneSpec;

/// Все переписанные сцены.
pub fn scenes() -> Vec<(&'static str, SceneSpec)> {
    let mut all = Vec::new();
    all.extend(ch01::scenes());
    all.extend(ch02::scenes());
    all.extend(ch03::scenes());
    all.extend(ch04::scenes());
    all.extend(ch05::scenes());
    all.extend(ch06::scenes());
    all.extend(ch07::scenes());
    all.extend(ch08::scenes());
    all.extend(ch09::scenes());
    all.extend(ch10::scenes());
    all
}

mod ch01;
mod ch02;
mod ch03;
mod ch04;
mod ch05;
mod ch06;
mod ch07;
mod ch08;
mod ch09;
mod ch10;
