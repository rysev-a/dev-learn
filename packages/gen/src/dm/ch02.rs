//! Дискретная математика, глава 2 («Отношения и функции»): сцены.
//! Перенос с `frontend/src/slides/anim/C2*.tsx` (`kit.tsx`, сырой SVG) на данные: те же шаги, подписи, метки `cues`.
//! Объекты, которые «переезжают» между шагами, имеют один и тот же `id`; чего нет в кадре — гаснет на месте.

use content::{
    dsl::{arrow, bx, dot, line, path, text, zone},
    item::{Anchor, Cell, Text},
    Frame, SceneSpec, Tone, B, G, M, R, Y,
};

/// Добавить элементы в кадр: `put!(f; cell(..), text(..))`.
macro_rules! put {
    ($f:ident; $($e:expr),+ $(,)?) => {{ $( $f.0.push(($e).into()); )+ }};
}

/// Плашка высотой 20 с моноширинной подписью (бывший `Pill`).
fn pill(id: impl Into<String>, x: f64, y: f64, w: f64, t: &str, tone: Tone) -> Cell {
    bx(id, x, y, w, 20.0, t).size(10.5).tone(tone)
}

/// Приглушённая подпись (`a-cap`).
fn cap(id: impl Into<String>, x: f64, y: f64, t: &str) -> Text {
    text(id, x, y, t)
}

/// Подпись цветом оттенка.
fn capc(id: impl Into<String>, x: f64, y: f64, t: &str, tone: Tone) -> Text {
    text(id, x, y, t).tone(tone)
}

/// Моноширинная подпись цветом оттенка.
fn mono(id: impl Into<String>, x: f64, y: f64, t: &str, tone: Tone, size: f64) -> Text {
    text(id, x, y, t).mono().tone(tone).size(size)
}

/// Моноширинная подпись обычным цветом текста.
fn plain(id: impl Into<String>, x: f64, y: f64, t: &str, size: f64) -> Text {
    text(id, x, y, t).mono().size(size)
}

fn arr(id: impl Into<String>, x1: f64, y1: f64, x2: f64, y2: f64, tone: Tone) -> content::item::Line {
    arrow(id, x1, y1, x2, y2).tone(tone)
}

/// Штриховка кривой (у `Path` нет своего метода).
fn dashed(p: content::item::Path, pattern: &str) -> content::item::Path {
    content::item::Path { dash: Some(pattern.into()), ..p }
}

/// Кадры по номеру шага.
fn frames(n: usize, f: impl Fn(usize) -> Frame) -> Vec<Frame> {
    (0..n).map(f).collect()
}

/// Таблица-матрица отношения: клетки `rows × cols` с левым верхним углом (x, y); `mark` — цвет клетки или `None`.
fn grid(f: &mut Frame, pfx: &str, (x, y): (f64, f64), rows: usize, cols: usize, size: f64, mark: impl Fn(usize, usize) -> Option<Tone>) {
    for r in 0..rows {
        for c in 0..cols {
            put!(f; bx(format!("{pfx}{r}-{c}"), x + c as f64 * size + size / 2.0, y + r as f64 * size + size / 2.0, size - 3.0, size - 3.0, "").tone(mark(r, c).unwrap_or(M)));
        }
    }
}

pub fn scenes() -> Vec<(&'static str, SceneSpec)> {
    vec![
        ("C2Intro", intro()),
        ("C2Pair", pair()),
        ("C2Product", product()),
        ("C2Relation", relation()),
        ("C2Reflexive", reflexive()),
        ("C2Symmetric", symmetric()),
        ("C2Transitive", transitive()),
        ("C2Equivalence", equivalence()),
        ("C2Partial", partial()),
        ("C2Function", function()),
        ("C2Mapping", mapping()),
        ("C2Pure", pure()),
        ("C2Recap", recap()),
    ]
}

// 1. Отношения в базе, функции в модуле, один словарь
fn intro() -> SceneSpec {
    const ORDERS: [(&str, f64); 3] = [("#1", 36.0), ("#2", 64.0), ("#3", 92.0)];
    const LINKS: [usize; 3] = [0, 0, 1];
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        let rel = step == 1 || step == 3;
        let fun = step == 2 || step == 3;
        let dim = if step == 3 { 0.45 } else { 1.0 };
        if rel {
            put!(f; cap("rel-t", 76.0, 16.0, "заказы → клиенты").opacity(dim));
            for (i, (t, y)) in ORDERS.iter().enumerate() {
                put!(f; pill(format!("o{i}"), 36.0, *y, 40.0, t, Y).opacity(dim));
            }
            for (i, n) in ["Аня", "Борис"].iter().enumerate() {
                put!(f; pill(format!("c{i}"), 120.0, 50.0 + i as f64 * 40.0, 52.0, n, G).opacity(dim));
            }
            for (i, c) in LINKS.iter().enumerate() {
                put!(f; arr(format!("ol{i}"), 58.0, ORDERS[i].1, 92.0, 50.0 + *c as f64 * 40.0, G).opacity(dim));
            }
        }
        if fun {
            put!(f;
                cap("fun-t", 270.0, 18.0, "модуль").opacity(dim),
                pill("fx", 216.0, 70.0, 36.0, "x", M).opacity(dim),
                bx("ff", 269.0, 70.0, 50.0, 44.0, "f").size(18.0).tone(G).opacity(dim),
                pill("fy", 332.0, 70.0, 36.0, "y", M).opacity(dim),
                arr("fa1", 236.0, 70.0, 242.0, 70.0, G).opacity(dim),
                arr("fa2", 296.0, 70.0, 312.0, 70.0, G).opacity(dim),
            );
        }
        if step == 3 {
            for (i, (big, t)) in [("(a, b)", "пары"), ("R ⊆ A×B", "отношения"), ("f : A → B", "функции")].iter().enumerate() {
                let x = 77.0 + i as f64 * 108.0;
                put!(f; bx(format!("g{i}"), x, 147.0, 98.0, 30.0, "").tone(G), mono(format!("gb{i}"), x, 146.0, big, G, 10.5), cap(format!("gt{i}"), x, 157.0, t));
            }
        }
        f
    });
    SceneSpec::new(
        &["Глава", "Отношения", "Функции", "Один словарь"],
        &[
            "Отношения и функции: два слова, которыми вы пользуетесь каждый день",
            "В каждой базе данных живут отношения: заказ связан с клиентом, пост — с автором",
            "В каждом модуле живут функции: на входе значение, на выходе ровно одно",
            "Математика описывает и то и другое одним словарём — пары, отношения, функции",
        ],
        fr,
    )
    .cues(&[4.2, 11.5, 14.8])
    .step_ms(2800)
}

// 2. Упорядоченная пара
fn pair() -> SceneSpec {
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 1 {
            put!(f; mono("ttl", 180.0, 22.0, if step == 0 { "{ 1, 2 } = { 2, 1 }" } else { "(1, 2) ≠ (2, 1)" }, G, 13.0));
            let (a, b) = (zone("sa", 142.0, 62.0, 64.0, 44.0), zone("sb", 218.0, 62.0, 64.0, 44.0));
            if step == 0 {
                put!(f; a, b);
            } else {
                put!(f; a.dash(), b.dash());
            }
            put!(f; pill("p1", 142.0, 62.0, 40.0, "1", B), pill("p2", 218.0, 62.0, 40.0, "2", Y));
            if step == 1 {
                put!(f;
                    cap("l1", 142.0, 100.0, "1-й"),
                    cap("l2", 218.0, 100.0, "2-й"),
                    zone("qa", 142.0, 135.0, 64.0, 30.0).dash(),
                    zone("qb", 218.0, 135.0, 64.0, 30.0).dash(),
                    pill("q1", 142.0, 135.0, 40.0, "2", Y),
                    pill("q2", 218.0, 135.0, 40.0, "1", B),
                    capc("other", 290.0, 104.0, "другая пара", R),
                );
            }
        }
        if step == 2 {
            put!(f; zone("map", 145.0, 76.0, 170.0, 120.0));
            for i in 1..=3 {
                put!(f;
                    line(format!("mv{i}"), 60.0 + i as f64 * 42.5, 16.0, 60.0 + i as f64 * 42.5, 136.0).dash_pattern("2 4").width(1.0),
                    line(format!("mh{i}"), 60.0, 16.0 + i as f64 * 30.0, 230.0, 16.0 + i as f64 * 30.0).dash_pattern("2 4").width(1.0),
                );
            }
            put!(f;
                dot("pt1", 187.0, 46.0, "").r(7.0).tone(G),
                dot("pt2", 102.0, 106.0, "").r(7.0).tone(R),
                mono("c1", 260.0, 52.0, "(7, 3)", G, 11.0).anchor(Anchor::Start),
                mono("c2", 260.0, 112.0, "(3, 7)", R, 11.0).anchor(Anchor::Start),
                cap("lon", 145.0, 152.0, "долгота →"),
            );
        }
        if step == 3 {
            put!(f;
                bx("code", 180.0, 70.0, 240.0, 80.0, ""),
                mono("k1", 76.0, 56.0, "point = (55.7, 37.6)", G, 12.0).anchor(Anchor::Start),
                plain("k2", 76.0, 78.0, "lat, lon = point", 12.0).anchor(Anchor::Start),
                mono("k3", 76.0, 98.0, "позиция 0 — широта, 1 — долгота", M, 10.5).anchor(Anchor::Start),
            );
        }
        f
    });
    SceneSpec::new(
        &["Множество", "Пара", "Карта", "В коде"],
        &[
            "В множестве порядок не играл никакой роли: {1, 2} = {2, 1}",
            "В паре порядок — суть: первый и второй элемент занимают разные позиции",
            "Точка на карте — пара (широта, долгота); переставили — и получилось другое место",
            "В коде это кортеж или массив из двух элементов, где позиция несёт смысл",
        ],
        fr,
    )
    .cues(&[3.1, 10.4, 16.6])
    .step_ms(3000)
}

// 3. Прямое произведение
fn product() -> SceneSpec {
    const SHIRTS: [&str; 3] = ["красная", "синяя", "белая"];
    const PANTS: [&str; 2] = ["чёрные", "серые"];
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            // футболки уезжают влево, освобождая место таблице
            let x = if step == 0 { 90.0 } else { 50.0 };
            put!(f; cap("sh-t", x, 18.0, "футболки A"));
            for (i, t) in SHIRTS.iter().enumerate() {
                put!(f; pill(format!("sh{i}"), x, 50.0 + i as f64 * 34.0, 64.0, t, B));
            }
        }
        if step == 0 {
            put!(f; cap("pa-t", 270.0, 18.0, "брюки B"));
            for (i, t) in PANTS.iter().enumerate() {
                put!(f; pill(format!("pa{i}"), 270.0, 66.0 + i as f64 * 34.0, 64.0, t, Y));
            }
            put!(f; mono("times", 180.0, 96.0, "×", G, 20.0));
        }
        if step == 1 || step == 2 {
            put!(f; plain("tb-h", 226.0, 30.0, "B ↓ · A →", 11.0));
            for (r, t) in PANTS.iter().enumerate() {
                put!(f; cap(format!("tb-r{r}"), 146.0, 70.0 + r as f64 * 38.0, t).anchor(Anchor::End));
            }
            for (c, t) in SHIRTS.iter().enumerate() {
                put!(f; cap(format!("tb-c{c}"), 176.0 + c as f64 * 56.0, 44.0, t));
            }
            for r in 0..2 {
                for c in 0..3 {
                    put!(f; bx(format!("tb{r}{c}"), 176.0 + c as f64 * 56.0, 67.0 + r as f64 * 38.0, 48.0, 30.0, format!("({}, {})", c + 1, r + 1)).size(10.0).tone(G));
                }
            }
        }
        if step == 1 {
            put!(f; mono("res1", 180.0, 150.0, "A × B: 6 пар", G, 13.0));
        }
        if step == 2 {
            put!(f; mono("res2", 180.0, 150.0, "|A × B| = 3 · 2 = 6", G, 15.0));
        }
        if step == 3 {
            put!(f;
                bx("sql", 180.0, 80.0, 260.0, 104.0, ""),
                mono("q1", 66.0, 54.0, "SELECT *", G, 12.0).anchor(Anchor::Start),
                plain("q2", 66.0, 74.0, "FROM shirts CROSS JOIN pants;", 12.0).anchor(Anchor::Start),
                mono("q3", 66.0, 104.0, "3 строки × 2 строки = 6 строк", Y, 11.0).anchor(Anchor::Start),
                cap("q4", 66.0, 121.0, "без условия отбора — все сочетания").anchor(Anchor::Start),
            );
        }
        f
    });
    SceneSpec::new(
        &["Множества", "Наряды", "Правило", "В базе"],
        &[
            "Берём два множества: три футболки и двое брюк",
            "Все возможные пары — прямое произведение: шесть нарядов",
            "Это заготовка под правило произведения: 3 · 2 = 6 — основа комбинаторики",
            "В базах данных этому отвечает перекрёстное соединение таблиц",
        ],
        fr,
    )
    .cues(&[5.1, 10.3, 17.0])
    .step_ms(3000)
}

// 4. Отношение — подмножество A × B
fn relation() -> SceneSpec {
    const ORD: [&str; 4] = ["#1", "#2", "#3", "#4"];
    const CLI: [&str; 3] = ["Аня", "Борис", "Вера"];
    const PPL: [&str; 4] = ["А", "Б", "В", "Г"];
    const FK: [usize; 4] = [0, 0, 1, 2]; // клиент каждого заказа
    const FR: [(usize, usize); 6] = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)];
    const SUB: [(usize, usize); 4] = [(0, 0), (1, 2), (2, 1), (0, 2)];
    let (x0, y0, size) = (146.0, 40.0, 32.0);
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            let cols = if step == 2 { 4 } else { 3 };
            grid(&mut f, "m", (x0, y0), 4, cols, size, |r, c| match step {
                0 => SUB.contains(&(r, c)).then_some(G),
                1 => (FK[r] == c).then_some(G),
                _ => FR.contains(&(r, c)).then_some(Y),
            });
            for r in 0..4 {
                let t = if step == 2 { PPL[r] } else { ORD[r] };
                put!(f; plain(format!("rl{r}"), x0 - 7.0, y0 + r as f64 * size + size / 2.0 + 3.5, t, 10.0).anchor(Anchor::End));
            }
            for c in 0..cols {
                let t = if step == 2 { PPL[c] } else { CLI[c] };
                put!(f; plain(format!("cl{c}"), x0 + c as f64 * size + size / 2.0, y0 - 5.0, t, 10.0));
            }
            let (t, tone) = [("R ⊆ A × B", G), ("внешний ключ", G), ("симметрично", Y)][step];
            put!(f; mono("lab", 60.0, 30.0, t, tone, 10.0));
        } else {
            put!(f;
                bx("tbl", 180.0, 78.0, 180.0, 108.0, ""),
                mono("th1", 110.0, 46.0, "order_id", M, 10.5).anchor(Anchor::Start),
                mono("th2", 190.0, 46.0, "client_id", M, 10.5).anchor(Anchor::Start),
            );
            for (i, c) in FK.iter().enumerate() {
                let y = 68.0 + i as f64 * 20.0;
                put!(f; plain(format!("to{i}"), 120.0, y, &(i + 1).to_string(), 11.0).anchor(Anchor::Start), mono(format!("tc{i}"), 205.0, y, &(c + 1).to_string(), G, 11.0).anchor(Anchor::Start));
            }
            put!(f; mono("tnote", 180.0, 152.0, "строка таблицы = пара отношения", G, 10.0));
        }
        f
    });
    SceneSpec::new(
        &["Подмножество", "Заказ → клиент", "Дружит", "Таблица"],
        &[
            "Отношение — подмножество прямого произведения: часть пар отмечена как связанные",
            "«Заказ принадлежит клиенту» — пары (заказ, клиент); в базе это внешний ключ",
            "«Дружит» — пары людей, симметричные по смыслу: отмечены обе половины",
            "Таблица в базе данных и есть отношение — от этого и слово «реляционная»",
        ],
        fr,
    )
    .cues(&[7.1, 13.5, 17.9])
    .step_ms(3000)
}

// 5. Рефлексивность
fn reflexive() -> SceneSpec {
    let (x0, y0, size) = (130.0, 34.0, 26.0);
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            grid(&mut f, "m", (x0, y0), 4, 4, size, |r, c| match step {
                0 | 1 => (r == c).then_some(G),
                _ => {
                    if r < c {
                        Some(Y)
                    } else {
                        (r == c).then_some(R)
                    }
                }
            });
            for i in 0..4 {
                let n = (i + 1).to_string();
                put!(f;
                    plain(format!("rl{i}"), x0 - 7.0, y0 + i as f64 * size + size / 2.0 + 3.5, &n, 10.0).anchor(Anchor::End),
                    plain(format!("cl{i}"), x0 + i as f64 * size + size / 2.0, y0 - 5.0, &n, 10.0),
                );
            }
            let (t, tone) = [("a R a", G), ("a = a ✓", G), ("a < a ✗", R)][step];
            put!(f; mono("lab", 60.0, 50.0, t, tone, 10.0));
            if step == 2 {
                put!(f; capc("note", 180.0, 152.0, "диагональ пуста — не рефлексивно", R));
            }
        } else {
            put!(f;
                pill("boss", 180.0, 112.0, 76.0, "директор", G),
                path("loop", "M174 103 C158 79 202 79 186 103").tone(G).width(1.6).arrow(),
                pill("anya", 64.0, 112.0, 56.0, "Аня", M),
                pill("boris", 296.0, 112.0, 56.0, "Борис", M),
                arr("a1", 94.0, 112.0, 140.0, 112.0, M),
                arr("a2", 266.0, 112.0, 220.0, 112.0, M),
                mono("sql", 180.0, 152.0, "manager_id = id — допустимо", G, 10.0),
            );
        }
        f
    });
    SceneSpec::new(
        &["Свойство", "Равно", "Меньше", "В схеме"],
        &[
            "Рефлексивность: каждый элемент связан с самим собой — вся диагональ отмечена",
            "«Равно» рефлексивно: любое число равно самому себе",
            "«Меньше» рефлексивным не будет: число не меньше самого себя",
            "В схеме данных: сотрудник может ссылаться на себя через руководителя",
        ],
        fr,
    )
    .cues(&[5.7, 9.3, 14.1])
    .step_ms(3000)
}

// 6. Симметричность
fn symmetric() -> SceneSpec {
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            put!(f; pill("anya", 60.0, 74.0, 56.0, "Аня", B), pill("boris", 180.0, 34.0, 56.0, "Борис", Y), pill("vera", 300.0, 74.0, 56.0, "Вера", G));
            match step {
                // «туда» сплошной, «обратно» пунктиром
                0 => put!(f; arr("ab", 86.0, 64.0, 150.0, 42.0, G), arr("ba", 150.0, 46.0, 90.0, 68.0, G).dash_pattern("4 3")),
                // обе половины: стрелки с наконечниками в обе стороны
                1 => put!(f;
                    arr("ab", 86.0, 64.0, 150.0, 42.0, G),
                    arr("ba", 150.0, 42.0, 86.0, 64.0, G),
                    arr("bv", 210.0, 42.0, 274.0, 64.0, G),
                    arr("vb", 274.0, 64.0, 210.0, 42.0, G),
                ),
                // подписки в одну сторону, обратных стрелок нет
                _ => put!(f;
                    arr("ab", 86.0, 64.0, 150.0, 42.0, Y),
                    arr("vb", 274.0, 68.0, 210.0, 46.0, Y),
                    arr("ba", 150.0, 46.0, 90.0, 68.0, R).dash_pattern("3 4").opacity(0.6),
                    arr("bv", 210.0, 46.0, 270.0, 66.0, R).dash_pattern("3 4").opacity(0.6),
                ),
            }
            let t = match step {
                0 => cap("t", 180.0, 112.0, "a R b ⇒ b R a"),
                1 => capc("t", 180.0, 112.0, "a ↔ b: обе половины пары", G),
                _ => capc("t", 180.0, 112.0, "обратных стрелок нет", R),
            };
            put!(f; t);
        } else {
            put!(f;
                bx("fr", 99.0, 74.0, 150.0, 104.0, "").tone(G),
                cap("fr-t", 99.0, 40.0, "friends"),
                bx("fo", 261.0, 74.0, 150.0, 104.0, "").tone(Y),
                cap("fo-t", 261.0, 40.0, "follows"),
                capc("fr-n", 99.0, 148.0, "в обе стороны", G),
                capc("fo-n", 261.0, 148.0, "только в одну", Y),
            );
            for (i, t) in ["(Аня, Борис)", "(Борис, Аня)", "(Борис, Вера)", "(Вера, Борис)"].iter().enumerate() {
                put!(f; plain(format!("fr{i}"), 40.0, 62.0 + i as f64 * 16.0, t, 10.0).anchor(Anchor::Start));
            }
            for (i, t) in ["(Аня, Борис)", "(Вера, Борис)"].iter().enumerate() {
                put!(f; plain(format!("fo{i}"), 202.0, 62.0 + i as f64 * 16.0, t, 10.0).anchor(Anchor::Start));
            }
        }
        f
    });
    SceneSpec::new(
        &["Свойство", "Дружба", "Подписка", "В схеме"],
        &[
            "Симметричность: если первый связан со вторым, то и второй связан с первым",
            "Дружба симметрична: подружились оба — связь в обе стороны",
            "Подписка несимметрична: вы подписаны на автора, а автор на вас — нет",
            "В схеме: дружба хранится парой в обе стороны, подписка — только в одну",
        ],
        fr,
    )
    .cues(&[5.5, 8.8, 13.6])
    .step_ms(3000)
}

// 7. Транзитивность
fn transitive() -> SceneSpec {
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            let names = [["a", "b", "c"], ["бабушка", "мама", "я"], ["Аня", "Борис", "Вера"]][step];
            for (i, n) in names.iter().enumerate() {
                put!(f; pill(format!("p{i}"), 70.0 + i as f64 * 110.0, 96.0, 78.0, n, if i == 1 { M } else { B }));
            }
            let col = if step == 2 { Y } else { G };
            put!(f; arr("e0", 110.0, 96.0, 142.0, 96.0, col), arr("e1", 220.0, 96.0, 252.0, 96.0, col));
            // вывод: дуга a → c
            if step >= 1 {
                put!(f; dashed(path("arc", "M70 82 C100 28 250 28 290 82").tone(if step == 2 { R } else { G }).width(1.8).arrow(), "6 4"));
            }
            let t = match step {
                0 => plain("t", 180.0, 36.0, "a R b, b R c ⇒ a R c", 10.0),
                1 => mono("t", 180.0, 36.0, "предок ✓ автоматически", G, 10.0),
                _ => mono("t", 180.0, 36.0, "знакомы? — не следует", R, 10.0),
            };
            put!(f; t);
            if step == 2 {
                put!(f; cap("n", 180.0, 140.0, "соцсеть показывает его как рекомендацию"));
            }
        } else {
            // те же плашки и стрелки превращаются в цепочку пакетов
            for (i, n) in ["app", "lib-a", "lib-b", "lib-c"].iter().enumerate() {
                put!(f; pill(format!("p{i}"), 46.0 + i as f64 * 90.0, 90.0, 62.0, n, if i == 0 { G } else { M }));
            }
            for i in 0..3 {
                put!(f; arr(format!("e{i}"), 78.0 + i as f64 * 90.0, 90.0, 104.0 + i as f64 * 90.0, 90.0, G));
            }
            put!(f;
                dashed(path("arc", "M46 76 C80 30 230 30 316 76").tone(Y).width(1.6).arrow(), "5 4"),
                mono("t", 180.0, 30.0, "app зависит и от lib-c (транзитивно)", Y, 11.0),
                cap("n", 180.0, 130.0, "прямые зависимости — сплошные, транзитивные — пунктир"),
            );
        }
        f
    });
    SceneSpec::new(
        &["Свойство", "Предки", "Знаком с", "Зависимости"],
        &[
            "Транзитивность: первый связан со вторым, второй с третьим — значит, первый с третьим",
            "«Является предком» транзитивно: предок предка — тоже предок",
            "«Знаком с» не транзитивно: друг вашего друга — не обязательно друг; соцсеть лишь рекомендует",
            "В пакетных менеджерах: зависимость зависимости — ваша зависимость",
        ],
        fr,
    )
    .cues(&[6.4, 10.7, 20.1])
    .step_ms(3000)
}

// 8. Отношение эквивалентности
fn equivalence() -> SceneSpec {
    const COL: [Tone; 3] = [B, Y, G];
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step == 0 {
            for (i, (formula, name)) in [("a ~ a", "рефлексивность"), ("a ~ b ⇒ b ~ a", "симметричность"), ("a ~ b, b ~ c ⇒ a ~ c", "транзитивность")].iter().enumerate() {
                let y = 45.0 + i as f64 * 38.0;
                put!(f;
                    bx(format!("pr{i}"), 180.0, y, 300.0, 30.0, "").tone(G),
                    mono(format!("pf{i}"), 44.0, y + 4.0, formula, G, 11.0).anchor(Anchor::Start),
                    cap(format!("pn{i}"), 316.0, y + 4.0, name).anchor(Anchor::End),
                );
            }
        }
        if step >= 1 {
            // числа: ряд → классы по остатку
            for i in 0..9usize {
                let (x, y) = if step >= 2 { (66.0 + (i % 3) as f64 * 124.0 + ((i / 3) as f64 - 1.0) * 30.0, 62.0) } else { (24.0 + i as f64 * 38.0, 70.0) };
                put!(f; dot(format!("n{i}"), x, y, (i + 1).to_string()).r(13.0).size(11.0).tone(COL[i % 3]));
            }
        }
        if step >= 2 {
            for (k, tone) in COL.iter().enumerate() {
                let x = 66.0 + k as f64 * 124.0;
                put!(f; zone(format!("cls{k}"), x, 62.0, 104.0, 68.0).tone(*tone).dash(), cap(format!("clt{k}"), x, 112.0, &format!("остаток {}", (k + 1) % 3)));
            }
        }
        if step == 1 {
            put!(f; plain("rule", 180.0, 152.0, "n ~ m ⇔ n % 3 = m % 3", 10.5));
        }
        if step == 3 {
            put!(f; bx("grp", 180.0, 143.0, 268.0, 34.0, ""), mono("grp-t", 60.0, 147.0, "GROUP BY n % 3  →  3 класса по 3 элемента", G, 11.0).anchor(Anchor::Start));
        }
        f
    });
    SceneSpec::new(
        &["Три свойства", "Примеры", "Классы", "Группировка"],
        &[
            "Рефлексивность + симметричность + транзитивность — отношение эквивалентности",
            "«Одинаковый остаток при делении на 3» — эквивалентность; цвет показывает остаток",
            "Эквивалентность режет множество на непересекающиеся классы",
            "Группировка по ключу — разбиение на классы; результат GROUP BY — готовые классы",
        ],
        fr,
    )
    .cues(&[7.8, 15.2, 22.8])
    .step_ms(3000)
}

// 9. Частичный порядок
fn partial() -> SceneSpec {
    // пакеты: имя, (x, y) в графе, x в линии сборки
    const PK: [(&str, f64, f64, f64); 4] = [("core", 180.0, 120.0, 40.0), ("utils", 100.0, 70.0, 130.0), ("net", 260.0, 70.0, 220.0), ("app", 180.0, 24.0, 310.0)];
    const EDGES: [(usize, usize); 4] = [(0, 1), (0, 2), (1, 3), (2, 3)];
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 1 {
            for (id, x, y, t) in [("d1", 180.0, 120.0, "1"), ("d2", 110.0, 72.0, "2"), ("d3", 250.0, 72.0, "3"), ("d6", 180.0, 24.0, "6")] {
                let bad = step == 1 && (t == "2" || t == "3");
                put!(f; pill(id, x, y, 34.0, t, if bad { R } else { G }));
            }
            put!(f;
                arr("h1", 160.0, 110.0, 128.0, 86.0, G),
                arr("h2", 200.0, 110.0, 232.0, 86.0, G),
                arr("h3", 128.0, 58.0, 160.0, 34.0, G),
                arr("h4", 232.0, 58.0, 200.0, 34.0, G),
            );
            if step == 0 {
                put!(f; mono("n1", 180.0, 156.0, "a ≼ b: «a делит b»", G, 10.0));
            } else {
                put!(f;
                    mono("q", 180.0, 72.0, "?", R, 14.0),
                    arr("x1", 130.0, 72.0, 228.0, 72.0, R).dash_pattern("3 4").opacity(0.7),
                    arr("x2", 228.0, 72.0, 130.0, 72.0, R).dash_pattern("3 4").opacity(0.7),
                    mono("n1", 180.0, 156.0, "2 и 3 несравнимы", R, 10.0),
                );
            }
        } else {
            let line_mode = step == 3;
            if step == 2 {
                for (i, (a, b)) in EDGES.iter().enumerate() {
                    put!(f; arr(format!("e{i}"), PK[*a].1, PK[*a].2 - 12.0, PK[*b].1, PK[*b].2 + 12.0, M));
                }
            }
            for (i, (t, x, y, lx)) in PK.iter().enumerate() {
                let bad = step == 2 && (*t == "utils" || *t == "net");
                let (px, py) = if line_mode { (*lx, 90.0) } else { (*x, *y) };
                put!(f; pill(format!("k{i}"), px, py, 58.0, t, if bad { R } else { G }));
            }
            if line_mode {
                for (i, (_, _, _, lx)) in PK.iter().enumerate() {
                    put!(f; mono(format!("no{i}"), *lx, 118.0, &(i + 1).to_string(), G, 10.0));
                }
                for i in 0..3 {
                    put!(f; arr(format!("s{i}"), PK[i].3 + 30.0, 90.0, PK[i + 1].3 - 30.0, 90.0, G));
                }
                put!(f; capc("n2", 180.0, 156.0, "порядок сборки: core → utils → net → app", G));
            } else {
                put!(f; capc("n2", 180.0, 156.0, "utils и net не упорядочены между собой", R));
            }
        }
        f
    });
    SceneSpec::new(
        &["Порядок", "Несравнимы", "Зависимости", "Сортировка"],
        &[
            "Рефлексивность + антисимметричность + транзитивность — частичный порядок, как «≤»",
            "«Частичный»: бывают элементы, которые никак не сравнить — 2 и 3 не делятся друг на друга",
            "В дереве зависимостей пакеты из разных ветвей не упорядочены между собой",
            "Топологическая сортировка вытягивает частичный порядок в линию сборки",
        ],
        fr,
    )
    .cues(&[9.4, 14.7, 21.0])
    .step_ms(3000)
}

// 10. Функция — отношение с контрактом
fn function() -> SceneSpec {
    let (lx, rx) = (90.0, 270.0);
    let ys = [36.0, 80.0, 124.0];
    let fr = frames(5, |step| {
        let mut f = Frame::new();
        if step <= 2 {
            put!(f; cap("dom", lx, 14.0, "область определения"), cap("cod", rx, 14.0, "область значений"));
            for (i, y) in ys.iter().enumerate() {
                put!(f; dot(format!("l{i}"), lx, *y, ["a", "b", "c"][i]).tone(B), dot(format!("r{i}"), rx, *y, (i + 1).to_string()).tone(Y));
            }
            let (x1, x2) = (lx + 14.0, rx - 14.0);
            // a → 2 и b → 3 есть всегда; c → 1 — только у функции; у нарушения a → 2 краснеет, a → 1 добавляется
            put!(f; arr("f1", x1, ys[0], x2, ys[1], if step == 2 { R } else { G }), arr("f2", x1, ys[1], x2, ys[2], G));
            if step <= 1 {
                put!(f; arr("f3", x1, ys[2], x2, ys[0], G));
            } else {
                put!(f; arr("f4", x1, ys[0], x2, ys[0], R), mono("q", 52.0, 128.0, "?", R, 13.0));
            }
            if step == 1 {
                put!(f; capc("n", 180.0, 152.0, "ровно одна стрелка из каждого входа", G));
            } else if step == 2 {
                put!(f; capc("n", 180.0, 152.0, "у a — два ответа, у c — ни одного", R));
            }
        } else if step == 3 {
            put!(f;
                pill("sg-in", 70.0, 80.0, 82.0, "str", B),
                bx("sg-f", 180.0, 80.0, 104.0, 48.0, "len(s)").size(12.0).tone(G),
                pill("sg-out", 290.0, 80.0, 82.0, "int", Y),
                arr("sg-a1", 114.0, 80.0, 126.0, 80.0, G),
                arr("sg-a2", 234.0, 80.0, 246.0, 80.0, G),
                mono("sg-t", 180.0, 130.0, "def f(s: str) -> int", G, 10.0),
            );
        } else {
            for i in 0..3 {
                let y = 36.0 + i as f64 * 38.0;
                put!(f; pill(format!("w-in{i}"), 110.0, y, 64.0, "f(2)", B), arr(format!("w-a{i}"), 144.0, y, 208.0, y, G), pill(format!("w-out{i}"), 240.0, y, 50.0, "4", G));
            }
            put!(f; capc("w-t", 180.0, 150.0, "один вход — всегда один и тот же выход, и без исключений", G));
        }
        f
    });
    SceneSpec::new(
        &["Функции", "Контракт", "Нарушения", "Сигнатура", "Без сюрпризов"],
        &[
            "Теперь функции: отношение, у которого есть дополнительный контракт",
            "У каждого элемента области определения — ровно один образ в области значений",
            "Два ответа для одного входа или вход без ответа — это уже не функция",
            "Сигнатура в языке — тот же контракт, записанный типами: на входе строка, на выходе число",
            "Математическая функция не падает и на одинаковый вход даёт одинаковый выход",
        ],
        fr,
    )
    .cues(&[1.4, 11.1, 15.4, 22.4])
    .step_ms(3000)
}

// 11. Инъекция, сюръекция, биекция
fn mapping() -> SceneSpec {
    let (lx, rx) = (100.0, 260.0);
    let slot = [28.0, 64.0, 100.0, 136.0];
    // (число входов, число выходов, пары вход → выход, цвет стрелок) для видов 1–3
    let kinds: [(usize, usize, &[(usize, usize)], Tone); 3] = [
        (3, 4, &[(0, 0), (1, 1), (2, 3)], G),
        (4, 3, &[(0, 0), (1, 0), (2, 1), (3, 2)], Y),
        (3, 3, &[(0, 1), (1, 2), (2, 0)], B),
    ];
    let fr = frames(5, |step| {
        let mut f = Frame::new();
        // шаг 0 показывает раскладку биекции, шаг 4 — её же, развёрнутую
        let k = if step == 0 || step == 4 { 3 } else { step };
        let (nl, nr, pairs, tone) = kinds[k - 1];
        for i in 0..nl {
            put!(f; dot(format!("l{i}"), lx, slot[i], ["a", "b", "c", "d"][i]).tone(B));
        }
        for i in 0..nr {
            put!(f; dot(format!("r{i}"), rx, slot[i], (i + 1).to_string()).tone(Y));
        }
        for (i, (a, b)) in pairs.iter().enumerate() {
            if step == 4 {
                put!(f; arr(format!("k{k}-{i}"), rx - 14.0, slot[*b], lx + 14.0, slot[*a], G));
            } else {
                put!(f; arr(format!("k{k}-{i}"), lx + 14.0, slot[*a], rx - 14.0, slot[*b], tone));
            }
        }
        let note = match step {
            1 => Some(("число 3 никому не достаётся, но склеек нет", G)),
            2 => Some(("все числа заняты, но a и b склеились", Y)),
            3 => Some(("один к одному", B)),
            4 => Some(("f⁻¹: стрелки в обратную сторону", G)),
            _ => None,
        };
        if let Some((t, tone)) = note {
            put!(f; mono("n", 180.0, 162.0, t, tone, 11.0));
        }
        f
    });
    SceneSpec::new(
        &["Виды", "Инъекция", "Сюръекция", "Биекция", "Обратная"],
        &[
            "Функции различают по тому, как они заполняют выход",
            "Инъекция: разные входы дают разные выходы — ничего не склеивается, но места могут остаться",
            "Сюръекция: каждый элемент выхода кем-то занят — пустых мест нет, но входы могут склеиваться",
            "Биекция — и то и другое: один к одному, и функцию можно развернуть",
            "Обратная функция: кодирование и декодирование живут на биекциях",
        ],
        fr,
    )
    .cues(&[3.4, 9.9, 17.1, 22.9])
    .step_ms(3200)
}

// 12. Чистая функция
fn pure() -> SceneSpec {
    let fr = frames(4, |step| {
        let mut f = Frame::new();
        if step <= 1 {
            put!(f;
                pill("x", 60.0, 74.0, 50.0, "x", B),
                bx("f", 180.0, 74.0, 80.0, 56.0, "f").size(20.0).tone(G),
                pill("y", 300.0, 74.0, 50.0, "y", Y),
                arr("a1", 88.0, 74.0, 138.0, 74.0, G),
                arr("a2", 222.0, 74.0, 272.0, 74.0, G),
            );
            if step == 0 {
                put!(f; capc("n", 180.0, 152.0, "результат зависит только от аргументов", G));
            } else {
                // побочные каналы, которых у чистой функции нет
                for (i, t) in ["время", "global", "база"].iter().enumerate() {
                    let x = 100.0 + i as f64 * 80.0;
                    let off = [20.0, 0.0, -20.0][i];
                    put!(f;
                        pill(format!("s{i}"), x, 20.0, 62.0, t, R),
                        arr(format!("sa{i}"), x + off, 32.0, 150.0 + i as f64 * 30.0, 48.0, R).dash_pattern("3 3").opacity(0.8),
                        mono(format!("sx{i}"), x, 128.0, "✗", R, 18.0),
                    );
                }
                put!(f; capc("n", 180.0, 152.0, "никаких скрытых входов и побочных эффектов", R));
            }
        } else if step == 2 {
            put!(f; bx("tests", 180.0, 70.0, 220.0, 92.0, ""));
            for (i, t) in ["assert f(2) == 4", "assert f(3) == 9", "assert f(0) == 0"].iter().enumerate() {
                let y = 50.0 + i as f64 * 22.0;
                put!(f; plain(format!("as{i}"), 88.0, y, t, 11.5).anchor(Anchor::Start), mono(format!("ok{i}"), 268.0, y, "✓", G, 13.0).anchor(Anchor::End));
            }
            put!(f; capc("tn", 180.0, 140.0, "без моков и настройки окружения", G));
        } else {
            put!(f; mono("ct", 180.0, 26.0, "cache = { }", G, 11.0));
            for (i, (a, b)) in [("2", "4"), ("3", "9"), ("4", "16")].iter().enumerate() {
                let y = 56.0 + i as f64 * 32.0;
                put!(f; pill(format!("ca{i}"), 130.0, y, 52.0, a, B), arr(format!("cr{i}"), 160.0, y, 198.0, y, G), pill(format!("cb{i}"), 230.0, y, 52.0, b, Y));
            }
            put!(f; mono("cn", 180.0, 158.0, "таблица пар — это отношение", G, 10.0));
        }
        f
    });
    SceneSpec::new(
        &["Чистая", "Без сюрпризов", "Тесты", "Мемоизация"],
        &[
            "Чистая функция в программировании — это математическая функция по построению",
            "Не смотрит на время, не читает глобальные переменные, не пишет в базу",
            "За это её любят тесты: один вход — один ожидаемый выход, без моков",
            "Мемоизация сохраняет пары вход–выход: таблица соответствия — это отношение",
        ],
        fr,
    )
    .cues(&[8.7, 18.3, 24.0])
    .step_ms(3000)
}

// 13. Итог главы
fn recap() -> SceneSpec {
    // (крупная подпись, название, шаг, на котором карточка загорается)
    const CARDS: [(&str, &str, usize); 5] = [("(a, b)", "пары", 1), ("A × B", "произв.", 1), ("R", "отношение", 1), ("≡  ≼", "свойства", 2), ("f", "функции", 3)];
    let fr = frames(6, |step| {
        let mut f = Frame::new();
        for (i, (big, name, at)) in CARDS.iter().enumerate() {
            let on = step == *at;
            let lit = step >= *at;
            let s = if on { 1.1 } else { 1.0 };
            let x = 40.0 + i as f64 * 70.0;
            put!(f;
                bx(format!("k{i}"), x, 52.0, 62.0, 68.0, "").tone(if lit { G } else { M }).scale(s),
                mono(format!("kb{i}"), x, 52.0 + 6.0 * s, big, G, 15.0).scale(s),
                cap(format!("kn{i}"), x, 52.0 + 24.0 * s, name).scale(s),
            );
        }
        if step >= 4 {
            for (i, t) in ["внешний ключ", "GROUP BY", "toposort", "чистая f"].iter().enumerate() {
                put!(f; pill(format!("u{i}"), 50.0 + i as f64 * 87.0, 116.0, 80.0, t, Y).size(9.5));
            }
        }
        if step >= 5 {
            put!(f; bx("next", 180.0, 152.0, 300.0, 24.0, "Глава 3 · комбинаторика: сколько всего бывает →").size(9.5).tone(G).text_color("var(--s-accent)"));
        }
        f
    });
    SceneSpec::new(
        &["Итог", "Пары → отношение", "Свойства", "Функции", "Словарь", "Дальше"],
        &[
            "Подведём итог главы",
            "Пары собираются в прямое произведение; подмножество произведения — отношение",
            "Рефлексивность, симметричность и транзитивность делят отношения на эквивалентности и порядки",
            "Функция — отношение с контрактом «ровно один выход»; её виды — инъекция, сюръекция, биекция",
            "Внешние ключи, группировки, топологическая сортировка, чистые функции — один словарь",
            "Дальше — калькулятор: комбинаторика научит считать, сколько всего бывает",
        ],
        fr,
    )
    // в React меток было четыре на шесть шагов (шаг «Дальше» достижим только кнопкой); пятая — по доле символов
    .cues(&[1.5, 10.8, 19.5, 25.7, 31.5])
    .step_ms(2600)
}

#[cfg(test)]
mod tests {
    use super::*;
    use content::Scene;

    #[test]
    fn names_match_the_old_components() {
        let names: Vec<&str> = scenes().iter().map(|(n, _)| *n).collect();
        assert_eq!(names.len(), 13);
    }

    #[test]
    fn every_scene_compiles_and_is_laid_out() {
        for (name, spec) in scenes() {
            let n = spec.frames.len();
            assert!(n >= 4, "{name}: кадров {n}");
            assert_eq!((spec.labels.len(), spec.captions.len()), (n, n), "{name}: названия, подписи и кадры не сходятся");
            let cues = spec.cues.clone().unwrap_or_default();
            assert_eq!(cues.len() + 1, n, "{name}: меток {} при кадрах {n}", cues.len());
            assert!(cues.windows(2).all(|w| w[0] < w[1]), "{name}: метки не возрастают");
            let scene = Scene::compile(&spec).unwrap_or_else(|e| panic!("{name}: {e}"));
            assert_eq!(scene.lint(), Vec::<String>::new(), "{name}");
        }
    }

    #[test]
    fn scenes_survive_json() {
        for (name, spec) in scenes() {
            let json = serde_json::to_string(&spec).unwrap();
            assert_eq!(serde_json::from_str::<SceneSpec>(&json).unwrap(), spec, "{name}");
        }
    }
}
