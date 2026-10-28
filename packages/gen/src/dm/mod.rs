//! "Discrete mathematics": diagrams of chapters 1–10, rewritten from manual React rendering (`slides/anim/C<n>*.tsx`, `kit.tsx`) to data.
//! Each chapter is a file `chNN.rs` with a `scenes()` function: pairs "former component name — scene description". The rest of the slides
//! (titles, "KEY POINTS", insets) is ported from TypeScript automatically.

use content::SceneSpec;

/// All rewritten scenes.
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
