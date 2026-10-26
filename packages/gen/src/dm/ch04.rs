//! Дискретная математика, глава 4 — «Бином, Паскаль и принцип Дирихле»: сцены.
//! Перенос с `frontend/src/slides/anim/C4*.tsx` (React, `kit.tsx`) на данные: названия шагов, подписи и метки `cues` — как в
//! прежних компонентах; группы `<G o={…}>` заменены присутствием элемента в кадре (отсутствующий гаснет на месте).

use content::{
    dsl::{arrow, bar, bx, cell, circle, disc, dot, intersect, line, path, text, zone},
    item::{Anchor, Cell, Item, Text},
    Frame, SceneSpec, Tone, B, G, M, R, Y,
};

/// Сцены главы: имя прежнего компонента — описание.
pub fn scenes() -> Vec<(&'static str, SceneSpec)> {
    vec![
        ("C4Intro", intro()),
        ("C4Pascal", pascal()),
        ("C4Paths", paths()),
        ("C4Props", props()),
        ("C4Binomial", binomial()),
        ("C4Estimate", estimate()),
        ("C4Incl2", incl2()),
        ("C4Incl3", incl3()),
        ("C4Pigeon", pigeon()),
        ("C4Hash", hash()),
        ("C4Birthday", birthday()),
        ("C4Crypto", crypto()),
        ("C4Recap", recap()),
    ]
}

// --- помощники ---------------------------------------------------------------------------------------------------

const ACCENT: &str = "var(--s-accent)";

fn put(f: &mut Frame, item: impl Into<Item>) {
    f.0.push(item.into());
}

/// Биномиальный коэффициент C(n, k).
fn binom(n: u64, k: u64) -> u64 {
    (1..=k).fold(1, |r, i| r * (n - k + i) / i)
}

/// Центр клетки строки `r`, номера `c` в треугольнике с шагом (dx, dy).
fn tri_pos(r: usize, c: usize, dx: f64, dy: f64, cx: f64, y0: f64) -> (f64, f64) {
    (cx + (c as f64 - r as f64 / 2.0) * dx, y0 + r as f64 * dy)
}

/// Подпись `size` (приглушённая).
fn tx(id: &str, x: f64, y: f64, s: &str, size: f64) -> Text {
    text(id, x, y, s).size(size)
}

/// Моноширинная подпись `size`.
fn mono(id: &str, x: f64, y: f64, s: &str, size: f64) -> Text {
    text(id, x, y, s).mono().size(size)
}

/// Плашка: рамка и лёгкая заливка цвета `tone`, подпись `size`.
fn pill(id: &str, x: f64, y: f64, w: f64, h: f64, label: &str, tone: Tone, size: f64) -> Cell {
    bx(id, x, y, w, h, label).tone(tone).size(size)
}

/// Зелёная плашка с подписью цвета акцента.
fn pill_g(id: &str, x: f64, y: f64, w: f64, h: f64, label: &str, size: f64) -> Cell {
    pill(id, x, y, w, h, label, G, size).text_color(ACCENT)
}

/// Круг-узел треугольника: число внутри.
fn tri_dot(id: String, x: f64, y: f64, r: f64, label: String, tone: Tone, size: f64) -> content::item::Dot {
    dot(id, x, y, label).r(r).size(size).tone(tone)
}

fn sup(n: u64) -> String {
    n.to_string().chars().map(|d| "⁰¹²³⁴⁵⁶⁷⁸⁹".chars().nth(d.to_digit(10).unwrap_or(0) as usize).unwrap_or(d)).collect()
}

// --- 1. Введение ---------------------------------------------------------------------------------------------------

fn intro() -> SceneSpec {
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            if step == 0 {
                put(&mut f, mono("title", 180.0, 84.0, "Бином, Паскаль, Дирихле", 15.0).tone(G));
            }
            if step == 1 || step == 2 {
                // треугольник
                for r in 0..4 {
                    for c in 0..=r {
                        let (x, y) = tri_pos(r, c, 18.0, 17.0, 66.0, 30.0);
                        put(&mut f, tri_dot(format!("t{r}{c}"), x, y, 6.0, String::new(), Y, 8.0));
                    }
                }
                put(&mut f, tx("l-tri", 66.0, 108.0, "треугольник", 9.5));
                // бином
                put(&mut f, mono("bin", 180.0, 68.0, "(a+b)ⁿ", 18.0).tone(G));
                put(&mut f, tx("l-bin", 180.0, 108.0, "формула", 9.5));
                // кролики и клетки
                for i in 0..3 {
                    put(&mut f, zone(format!("cage{i}"), 265.0 + i as f64 * 28.0, 64.0, 22.0, 32.0).tone(B));
                }
                for i in 0..4 {
                    let (x, y) = if i < 3 { (265.0 + i as f64 * 28.0, 64.0) } else { (265.0, 58.0) };
                    put(&mut f, dot(format!("rab{i}"), x, y, "").r(5.0).tone(B));
                }
                put(&mut f, tx("l-rab", 294.0, 108.0, "кролики и клетки", 9.5));
            }
            if step == 2 {
                put(&mut f, mono("q", 180.0, 140.0, "как считать, не перебирая?", 14.0).tone(G));
            }
            if step >= 3 {
                for i in 0..4 {
                    put(&mut f, bx(format!("cell{i}"), 75.0 + i as f64 * 70.0, 96.0, 58.0, 40.0, "").tone(if i == 1 { R } else { M }));
                }
                put(&mut f, dot("k0", 64.0, 96.0, "").r(7.0).tone(G));
                put(&mut f, dot("k1", 126.0, 88.0, "").r(7.0).tone(Y));
                put(&mut f, dot("k2", 138.0, 106.0, "").r(7.0).tone(R));
                put(&mut f, dot("k3", 204.0, 96.0, "").r(7.0).tone(G));
                put(&mut f, dot("k4", 274.0, 96.0, "").r(7.0).tone(G));
                put(&mut f, mono("coll", 180.0, 140.0, "два ключа в одной ячейке — коллизия", 12.0).tone(R));
                put(&mut f, mono("hash", 180.0, 56.0, "hash(key) % 4", 12.0));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Глава", "Три вещи", "Один вопрос", "Коллизии"],
        &[
            "Бином, Паскаль и принцип Дирихле",
            "Треугольник чисел, формула степени суммы и шутка про кроликов и клетки",
            "На деле это три взгляда на один вопрос — как считать, не перебирая",
            "Сегодня увидим, как принцип Дирихле объясняет коллизии в хеш-таблицах",
        ],
        frames,
    )
    .cues(&[4.9, 11.8, 16.2])
    .step_ms(2800)
}

// --- 2. Треугольник Паскаля ----------------------------------------------------------------------------------------

fn pascal() -> SceneSpec {
    const ROWS: usize = 7;
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            for r in 0..ROWS {
                for c in 0..=r {
                    let edge = c == 0 || c == r;
                    if !(r == 0 || (step >= 1 && edge) || step >= 2) {
                        continue;
                    }
                    let hl = step == 2 && r == 4 && c == 2;
                    let src = step == 2 && r == 3 && (c == 1 || c == 2);
                    let tone = if hl {
                        G
                    } else if src || edge {
                        Y
                    } else {
                        M
                    };
                    let (x, y) = tri_pos(r, c, 38.0, 20.0, 150.0, 18.0);
                    put(&mut f, tri_dot(format!("p{r}{c}"), x, y, 10.0, binom(r as u64, c as u64).to_string(), tone, 9.5));
                }
            }
            if step == 2 {
                put(&mut f, mono("sum", 262.0, 100.0, "3 + 3 = 6", 10.5).tone(G).anchor(Anchor::Start));
                put(&mut f, tx("sum-note", 262.0, 84.0, "сумма двух над ним", 9.5).anchor(Anchor::Start));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Вершина", "Края", "Сумма", "Таблица"],
        &[
            "Начнём с треугольника Паскаля: он строится без единой формулы — на вершине единица",
            "Вдоль обоих краёв тоже стоят единицы",
            "Каждое число внутри равно сумме двух чисел над ним: 1, 2, 1; 1, 3, 3, 1 …",
            "Ни умножения, ни деления — а в итоге таблица всей комбинаторики выбора",
        ],
        frames,
    )
    .cues(&[4.4, 10.7, 16.8])
    .step_ms(2800)
}

// --- 3. Маршруты и сетка -------------------------------------------------------------------------------------------

fn paths() -> SceneSpec {
    const PATH: [(usize, usize); 5] = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 2)];
    const ROUTES: [&str; 6] = ["ЛЛПП", "ЛПЛП", "ЛППЛ", "ПЛЛП", "ПЛПЛ", "ППЛЛ"];
    const GRID: [[&str; 3]; 3] = [["1", "1", "1"], ["1", "▨", "1"], ["1", "1", "2"]];
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 1 {
                for r in 0..5usize {
                    for c in 0..=r {
                        let (x, y) = tri_pos(r, c, 40.0, 28.0, 130.0, 22.0);
                        let on = step == 1 && PATH.contains(&(r, c));
                        put(&mut f, tri_dot(format!("t{r}{c}"), x, y, 12.0, binom(r as u64, c as u64).to_string(), if on { G } else { M }, 10.0));
                    }
                }
            }
            match step {
                0 => {
                    put(&mut f, mono("s0a", 300.0, 40.0, "строка 4:", 11.0));
                    put(&mut f, mono("s0b", 300.0, 56.0, "C(4,0)…C(4,4)", 10.0));
                }
                1 => {
                    put(&mut f, mono("s1a", 300.0, 46.0, "6 маршрутов", 11.0).tone(G));
                    put(&mut f, tx("s1b", 300.0, 62.0, "до центральной", 9.5));
                }
                2 => {
                    for (i, route) in ROUTES.iter().enumerate() {
                        for (j, ch) in route.chars().enumerate() {
                            let (x, y) = (44.0 + (i % 3) as f64 * 112.0 + j as f64 * 24.0, 40.0 + (i / 3) as f64 * 38.0);
                            put(&mut f, bx(format!("r{i}{j}"), x, y, 20.0, 20.0, ch.to_string()).tone(if ch == 'Л' { G } else { M }).size(10.0));
                        }
                    }
                    put(&mut f, mono("c2", 180.0, 130.0, "выбрать 2 из 4 шагов: C(4, 2) = 6", 13.0).tone(G));
                }
                _ => {
                    for i in 0..3 {
                        let lbl = (i + 1).to_string();
                        put(&mut f, mono(&format!("gc{i}"), 96.0 + i as f64 * 34.0 + 17.0, 21.0, &lbl, 10.0));
                        put(&mut f, mono(&format!("gr{i}"), 89.0, 26.0 + i as f64 * 34.0 + 21.0, &lbl, 10.0).anchor(Anchor::End));
                    }
                    for (r, row) in GRID.iter().enumerate() {
                        for (c, v) in row.iter().enumerate() {
                            let tone = if (r, c) == (1, 1) {
                                R
                            } else if (r, c) == (2, 2) {
                                G
                            } else {
                                M
                            };
                            put(&mut f, cell(format!("g{r}{c}"), 96.0 + c as f64 * 34.0 + 17.0, 26.0 + r as f64 * 34.0 + 17.0, *v).w(31.0).h(31.0).size(12.0).tone(tone));
                        }
                    }
                    put(&mut f, tx("g-note", 282.0, 60.0, "▨ — препятствие", 9.5));
                    put(&mut f, mono("g-cnt", 282.0, 84.0, "путей: 2", 11.0).tone(G));
                    put(&mut f, tx("g-rule", 180.0, 152.0, "каждая клетка = сумма клетки слева и клетки сверху — как в треугольнике", 9.5));
                }
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Строка = C(n, k)", "Маршруты", "Шаги влево", "Сетка"],
        &[
            "Строка с номером n — все сочетания C(n, k), выписанные по порядку",
            "Спускаясь от вершины, вы делаете n шагов влево или вправо: число в клетке считает маршруты до неё",
            "Маршрут — это выбор, в каких именно шагах свернуть влево: сочетание",
            "Сетка с препятствиями: число путей из угла в угол вправо и вниз — тот же C(n, k)",
        ],
        frames,
    )
    .cues(&[6.8, 17.6, 23.0])
    .step_ms(3000)
}

// --- 4. Свойства треугольника --------------------------------------------------------------------------------------

fn props() -> SceneSpec {
    const ROWS: usize = 7;
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            for r in 0..ROWS {
                for c in 0..=r {
                    let tone = match step {
                        1 if r == 4 => G,
                        2 if r == 5 && (c == 2 || c == 3) => Y,
                        3 if (r == 5 && c == 2) || (r == 4 && (c == 1 || c == 2)) => B,
                        _ => M,
                    };
                    let (x, y) = tri_pos(r, c, 38.0, 20.0, 150.0, 18.0);
                    put(&mut f, tri_dot(format!("p{r}{c}"), x, y, 10.0, binom(r as u64, c as u64).to_string(), tone, 9.5));
                }
            }
            match step {
                1 => {
                    put(&mut f, mono("a1", 296.0, 62.0, "1+4+6+4+1", 11.0));
                    put(&mut f, mono("a2", 296.0, 82.0, "= 16 = 2⁴", 15.0).tone(G));
                }
                2 => {
                    put(&mut f, line("mirror", 150.0, 12.0, 150.0, 158.0).tone(Y).dash_pattern("4 4").opacity(0.8));
                    put(&mut f, mono("b1", 296.0, 62.0, "C(5,2) = 10", 11.0));
                    put(&mut f, mono("b2", 296.0, 80.0, "C(5,3) = 10", 11.0));
                    put(&mut f, tx("b3", 296.0, 100.0, "зеркало", 9.5).tone(Y));
                }
                3 => {
                    put(&mut f, mono("c1", 296.0, 62.0, "C(5,2) =", 11.0));
                    put(&mut f, mono("c2", 296.0, 80.0, "C(4,1) + C(4,2)", 11.0));
                    put(&mut f, mono("c3", 296.0, 100.0, "10 = 4 + 6", 12.0).tone(B));
                }
                4 => {
                    put(&mut f, tx("d1", 296.0, 74.0, "всё видно", 10.0));
                    put(&mut f, tx("d2", 296.0, 90.0, "на таблице", 10.0));
                }
                _ => {}
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Свойства", "Сумма 2ⁿ", "Симметрия", "Правило", "Справочник"],
        &[
            "Из треугольника мгновенно читаются свойства, которые мы встречали в главе про множества",
            "Сумма чисел строки n равна 2ⁿ: строка — все подмножества, сгруппированные по размеру",
            "Строка симметрична: C(n, k) = C(n, n − k) — выбрать, кого взять, то же, что выбрать, кого оставить",
            "Правило Паскаля: C(n, k) = C(n−1, k−1) + C(n−1, k) — взять конкретный элемент или не взять",
            "Треугольник — наглядный справочник: равенства видны, а не заучиваются",
        ],
        frames,
    )
    .cues(&[5.1, 13.8, 21.5, 29.0])
    .step_ms(3000)
}

// --- 5. Бином Ньютона ----------------------------------------------------------------------------------------------

/// Члены разложения (a + b)ⁿ: коэффициент и одночлен.
fn terms(n: u64) -> Vec<(u64, String)> {
    (0..=n)
        .map(|k| {
            let a = match n - k {
                0 => String::new(),
                1 => "a".to_string(),
                e => format!("a{}", sup(e)),
            };
            let b = match k {
                0 => String::new(),
                1 => "b".to_string(),
                e => format!("b{}", sup(e)),
            };
            (binom(n, k), format!("{a}{b}"))
        })
        .collect()
}

fn binomial() -> SceneSpec {
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            match step {
                0 => put(&mut f, mono("big", 180.0, 86.0, "(a + b)ⁿ", 30.0).tone(G)),
                1 => {
                    put(&mut f, mono("ttl", 180.0, 22.0, "(a + b)(a + b)", 12.0));
                    for (i, t) in ["aa", "ab", "ba", "bb"].iter().enumerate() {
                        let tone = if *t == "ab" || *t == "ba" { Y } else { B };
                        put(&mut f, pill(&format!("w{i}"), 60.0 + i as f64 * 80.0, 64.0, 48.0, 22.0, t, tone, 10.5));
                    }
                    put(&mut f, mono("res", 180.0, 112.0, "a² + 2ab + b²", 13.0).tone(G));
                    put(&mut f, tx("note", 180.0, 134.0, "ab и ba — одно слагаемое, поэтому коэффициент 2", 9.5));
                }
                _ => {
                    // один и тот же ряд плашек: из трёх коэффициентов куба получаются пять коэффициентов четвёртой степени
                    let n: u64 = if step == 2 { 3 } else { 4 };
                    put(&mut f, mono("ttl", 180.0, 22.0, &format!("(a + b){}", sup(n)), 12.0));
                    for (i, (c, t)) in terms(n).iter().enumerate() {
                        let (x, y1, y2, w1, w2, s1, s2) = if n == 3 { (48.0 + i as f64 * 88.0, 64.0, 102.0, 32.0, 46.0, 13.0, 10.5) } else { (40.0 + i as f64 * 70.0, 60.0, 98.0, 34.0, 50.0, 14.0, 9.5) };
                        put(&mut f, pill_g(&format!("c{i}"), x, y1, w1, 24.0, &c.to_string(), s1));
                        put(&mut f, pill(&format!("m{i}"), x, y2, w2, 22.0, t, B, s2));
                    }
                    if n == 3 {
                        put(&mut f, mono("res", 180.0, 140.0, "коэффициент при aⁿ⁻ᵏbᵏ — C(n, k)", 11.0));
                    } else {
                        put(&mut f, mono("res", 180.0, 140.0, "строка Паскаля: 1 · 4 · 6 · 4 · 1", 12.0).tone(G));
                    }
                }
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Бином", "(a+b)²", "Коэффициент", "(a+b)⁴"],
        &[
            "Теперь бином Ньютона: степень суммы двух слагаемых",
            "В каждой скобке берём a или b — перебираем все способы и складываем: aa + ab + ba + bb",
            "Член с n − k множителями a и k множителями b встречается ровно C(n, k) раз",
            "Коэффициенты раскрытия — строка Паскаля целиком: 1, 4, 6, 4, 1",
        ],
        frames,
    )
    .cues(&[4.0, 13.4, 22.7])
    .step_ms(3000)
}

// --- 6. Быстрые прикидки -------------------------------------------------------------------------------------------

/// Десятичное число с запятой, три знака.
fn dec3(v: f64) -> String {
    format!("{v:.3}").replace('.', ",")
}

fn estimate() -> SceneSpec {
    let terms: Vec<f64> = (0..6u64).map(|k| binom(100, k) as f64 * 0.01f64.powi(k as i32)).collect();
    let total: f64 = terms.iter().sum();
    let names = ["1", "100·x", "C₂·x²", "C₃·x³", "C₄·x⁴", "C₅·x⁵"];
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            if step == 0 {
                put(&mut f, mono("big", 180.0, 86.0, "(1 + x)ⁿ ≈ 1 + n·x", 22.0).tone(G));
            }
            if step == 1 || step >= 3 {
                put(&mut f, mono("head", 180.0, 18.0, "(1 + 0,01)¹⁰⁰ = 1 + 1 + 0,495 + 0,162 + …", 11.0));
                for (k, v) in terms.iter().enumerate() {
                    let y = 44.0 + k as f64 * 17.0;
                    let w = v * 90.0 + 2.0;
                    let dim = if step >= 3 && k >= 3 { 0.3 } else { 1.0 };
                    put(&mut f, mono(&format!("n{k}"), 40.0, y, names[k], 9.5).anchor(Anchor::End));
                    put(&mut f, cell(format!("b{k}"), 48.0 + w / 2.0, y - 4.0, "").w(w).h(12.0).tone(if k < 2 { G } else { M }).opacity(if dim < 1.0 { 0.3 } else { 1.0 }));
                    put(&mut f, mono(&format!("v{k}"), 48.0 + w + 8.0, y, &dec3(*v), 9.0).anchor(Anchor::Start).opacity(dim));
                }
                put(&mut f, mono("sum", 180.0, 150.0, &format!("сумма ≈ {} — первые два члена дают 2,00", format!("{total:.2}").replace('.', ",")), 12.0).tone(Y));
            }
            if step == 2 {
                let rows = [("сложный процент", "1,05¹⁰ ≈ 1 + 10·0,05 + …"), ("нагрузка", "+1 % в день: за месяц ≈ ×1,35"), ("анализ алгоритмов", "(n + 1)² = n² + 2n + 1 → n²")];
                for (i, (t, formula)) in rows.iter().enumerate() {
                    put(&mut f, pill(&format!("w{i}"), 80.0, 36.0 + i as f64 * 40.0, 128.0, 24.0, t, G, 9.5));
                    put(&mut f, mono(&format!("f{i}"), 160.0, 40.0 + i as f64 * 40.0, formula, 10.5).anchor(Anchor::Start));
                }
            }
            if step >= 4 {
                put(&mut f, tx("gist", 180.0, 165.0, "суть остаётся, шум уходит", 9.5).tone(G));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Прикидка", "(1,01)¹⁰⁰", "Где нужно", "Навык", "Суть"],
        &[
            "Практическая сила бинома — быстрые прикидки без калькулятора",
            "(1 + 0,01)¹⁰⁰ — главную роль играет член, где малое число в первой степени",
            "Так оценивают сложный процент, рост нагрузки при небольшом ежедневном ухудшении, анализ алгоритмов",
            "Общий навык: разложить по биному, увидеть доминирующие члены, отбросить хвост",
            "Честные упрощения оставляют суть и убирают шум",
        ],
        frames,
    )
    .cues(&[3.9, 13.0, 20.1, 26.2])
    .step_ms(3000)
}

// --- 7. Включения и исключения: два множества ----------------------------------------------------------------------

fn incl2() -> SceneSpec {
    let (a, b) = (disc(150.0, 70.0, 46.0), disc(210.0, 70.0, 46.0));
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 2 {
                put(&mut f, circle("ca", 150.0, 70.0, 46.0).tone(B));
                put(&mut f, circle("cb", 210.0, 70.0, 46.0).tone(G));
                // общая часть: бледная на первом шаге, потом ярче
                put(&mut f, intersect("both", a, b).tone(Y).fill_opacity(0.4).shown(if step >= 1 { 1.0 } else { 0.375 }));
                put(&mut f, mono("na", 124.0, 74.0, "30", 13.0));
                put(&mut f, mono("nab", 180.0, 74.0, "10", 13.0).tone(Y));
                put(&mut f, mono("nb", 236.0, 74.0, "20", 13.0));
                put(&mut f, tx("la", 110.0, 22.0, "аудиокурс · 40", 9.5).tone(B));
                put(&mut f, tx("lb", 250.0, 22.0, "вебинар · 30", 9.5).tone(G));
                if step == 1 {
                    put(&mut f, mono("f1", 180.0, 144.0, "|A ∪ B| = |A| + |B| − |A ∩ B|", 12.0).tone(G));
                }
                if step == 2 {
                    put(&mut f, mono("f2", 180.0, 144.0, "40 + 30 − 10 = 60", 14.0).tone(G));
                }
            } else {
                put(&mut f, mono("A", 90.0, 22.0, "A", 10.0));
                put(&mut f, mono("B", 270.0, 22.0, "B", 10.0));
                for (i, v) in ["1", "2"].iter().enumerate() {
                    put(&mut f, pill(&format!("a{i}"), 90.0, 42.0 + i as f64 * 28.0, 44.0, 22.0, v, B, 10.5));
                }
                for (i, v) in ["2", "3"].iter().enumerate() {
                    put(&mut f, pill(&format!("b{i}"), 270.0, 42.0 + i as f64 * 28.0, 44.0, 22.0, v, G, 10.5));
                }
                put(&mut f, mono("union", 180.0, 78.0, "UNION", 11.0));
                for (i, v) in ["1", "2", "3"].iter().enumerate() {
                    put(&mut f, pill(&format!("u{i}"), 120.0 + i as f64 * 60.0, 120.0, 44.0, 22.0, v, Y, 10.5));
                }
                put(&mut f, tx("once", 180.0, 152.0, "2 встречается в обоих, но в результате — один раз", 9.5));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Перекрытие", "Формула", "40 + 30 − 10", "UNION"],
        &[
            "Переходим к включениям и исключениям — честному счёту по перекрывающимся группам",
            "|A ∪ B| = |A| + |B| − |A ∩ B|: общая часть посчитана дважды, вычитаем один раз",
            "Аудиокурс начали 40 человек, вебинар смотрели 30, оба — 10: охвачено 60, а не 70",
            "Объединение в базе данных не возвращает дубликаты — оно молча делает то же за вас",
        ],
        frames,
    )
    .cues(&[5.2, 11.8, 22.8])
    .step_ms(3000)
}

// --- 8. Включения и исключения: три множества ----------------------------------------------------------------------

fn incl3() -> SceneSpec {
    const CIRCLES: [(f64, f64, Tone); 3] = [(140.0, 70.0, B), (200.0, 70.0, Y), (170.0, 112.0, G)];
    const REGIONS: [(f64, f64, &str); 7] = [(118.0, 58.0, "30"), (222.0, 58.0, "24"), (170.0, 138.0, "10"), (170.0, 52.0, "13"), (146.0, 100.0, "7"), (194.0, 100.0, "3"), (170.0, 84.0, "5")];
    const RUN: [(&str, &str); 7] = [("55", "55"), ("+45", "100"), ("+25", "125"), ("−18", "107"), ("−12", "95"), ("−8", "87"), ("+5", "92")];
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            if step == 0 {
                put(&mut f, mono("plus", 180.0, 50.0, "+  −  +  −  …", 13.0).tone(G));
            }
            if step == 1 {
                put(&mut f, mono("e1", 180.0, 56.0, "|A∪B∪C| = |A|+|B|+|C|", 11.0));
                put(&mut f, mono("e2", 180.0, 76.0, "− |A∩B| − |A∩C| − |B∩C|", 11.0).tone(R));
                put(&mut f, mono("e3", 180.0, 96.0, "+ |A∩B∩C|", 11.0).tone(G));
            }
            if step >= 2 {
                put(&mut f, zone("frame", 180.0, 85.0, 220.0, 146.0));
                for (i, (x, y, tone)) in CIRCLES.iter().enumerate() {
                    put(&mut f, circle(format!("c{i}"), *x, *y, 42.0).tone(*tone));
                }
                for (i, (x, y, t)) in REGIONS.iter().enumerate() {
                    let n = mono(&format!("r{i}"), *x, *y + 3.6, t, 11.5);
                    put(&mut f, if i == 6 { n.tone(G) } else { n });
                }
                put(&mut f, tx("l-en", 100.0, 38.0, "EN 55", 10.0).tone(B));
                put(&mut f, tx("l-de", 260.0, 38.0, "DE 45", 10.0).tone(Y));
                put(&mut f, tx("l-fr", 260.0, 148.0, "FR 25", 10.0).tone(G));
            }
            if step == 3 {
                for (i, (t, v)) in RUN.iter().enumerate() {
                    let y = 26.0 + i as f64 * 20.0;
                    let t_text = mono(&format!("rt{i}"), 308.0, y, t, 10.0).anchor(Anchor::Start);
                    put(&mut f, if t.starts_with('−') { t_text.tone(R) } else { t_text.tone(G) });
                    put(&mut f, mono(&format!("rv{i}"), 348.0, y, v, 10.0).anchor(Anchor::End));
                }
            }
            if step >= 4 {
                put(&mut f, mono("l-none", 92.0, 150.0, "8", 10.0).tone(R));
                put(&mut f, mono("d1", 320.0, 70.0, "100 − 92", 11.0));
                put(&mut f, mono("d2", 320.0, 92.0, "= 8", 20.0).tone(R));
                put(&mut f, tx("d3", 320.0, 110.0, "ни одного языка", 9.5));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["+ − +", "Формула", "Данные", "Счёт", "Ответ"],
        &[
            "С тремя множествами начинается пульсация: прибавить, отнять, прибавить",
            "Сумма мощностей, минус попарные пересечения, плюс пересечение всех трёх",
            "Из ста человек: английский — 55, немецкий — 45, французский — 25; пары 18, 12, 8; все три — 5",
            "55 + 45 + 25 − 18 − 12 − 8 + 5 = 92",
            "Значит, восемь человек не знают ни одного языка — без единого перебора",
        ],
        frames,
    )
    .cues(&[5.0, 11.8, 26.1, 34.8])
    .step_ms(3000)
}

// --- 9. Принцип Дирихле --------------------------------------------------------------------------------------------

fn pigeon() -> SceneSpec {
    let cage = |c: usize| 48.0 + c as f64 * 76.0;
    let frames = (0..4)
        .map(|step| {
            // рассадка кроликов: на шаге 2 — другая, остальные — первая
            let arr: [usize; 5] = if step == 2 { [3, 3, 0, 2, 3] } else { [0, 1, 1, 2, 3] };
            let placed = step >= 1;
            let cnt = |c: usize| arr.iter().filter(|&&a| a == c).count();
            let mut f = Frame::new();
            for c in 0..4 {
                let full = placed && cnt(c) >= 2;
                let z = zone(format!("cage{c}"), cage(c), 82.0, 60.0, 64.0).tone(if full { Y } else { Tone::Outline });
                put(&mut f, if placed { z } else { z.dash() });
                if placed {
                    put(&mut f, mono(&format!("cnt{c}"), cage(c), 130.0, &cnt(c).to_string(), 11.0).tone(if full { Y } else { M }));
                }
            }
            for i in 0..5 {
                let c = arr[i];
                let k = arr[..i].iter().filter(|&&a| a == c).count();
                let (x, y) = if placed { (cage(c) - 14.0 + (k % 2) as f64 * 28.0, 72.0 + (k / 2) as f64 * 26.0) } else { (40.0 + i as f64 * 70.0, 20.0) };
                put(&mut f, dot(format!("rab{i}"), x, y, "🐇").r(10.0).size(12.0).tone(B));
            }
            if step == 1 || step == 2 {
                put(&mut f, mono("law", 180.0, 154.0, "5 кроликов > 4 клеток ⇒ где-то ≥ 2", 13.0).tone(Y));
            }
            if step >= 3 {
                for c in 0..4 {
                    put(&mut f, mono(&format!("q{c}"), cage(c), 46.0, "?", 15.0).tone(R));
                }
                put(&mut f, tx("noaddr", 180.0, 154.0, "существование есть — адреса нет", 11.0));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Принцип", "5 > 4", "Любая рассадка", "Без адреса"],
        &[
            "Принцип Дирихле — самый незамысловатый и самый хитрый инструмент курса",
            "Кроликов больше, чем клеток: хотя бы в одной клетке сидят минимум двое",
            "Как бы кролики ни рассаживались — вывод гарантирован самим количеством",
            "Принцип доказывает существование, но не говорит, в какой именно клетке искать",
        ],
        frames,
    )
    .cues(&[5.1, 10.7, 16.6])
    .step_ms(3000)
}

// --- 10. Принцип Дирихле в хеш-таблицах ----------------------------------------------------------------------------

fn hash() -> SceneSpec {
    const KEYS: [usize; 6] = [0, 1, 1, 2, 3, 1]; // ячейка каждого из шести ключей
    let cell_x = |c: usize| 76.0 + c as f64 * 64.0;
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 1 {
                for c in 0..4 {
                    put(&mut f, bx(format!("slot{c}"), cell_x(c), 114.0, 56.0, 44.0, "").tone(if step == 1 && c == 1 { R } else { M }));
                    put(&mut f, tx(&format!("idx{c}"), cell_x(c), 148.0, &c.to_string(), 9.5));
                }
                let placed = step >= 1;
                for (i, &c) in KEYS.iter().enumerate() {
                    let k = KEYS[..i].iter().filter(|&&a| a == c).count();
                    let (x, y) = if placed { (cell_x(c) - 12.0 + (k % 2) as f64 * 24.0, 106.0 + (k / 2) as f64 * 18.0) } else { (40.0 + i as f64 * 56.0, 30.0) };
                    put(&mut f, dot(format!("key{i}"), x, y, (i + 1).to_string()).r(8.0).size(8.0).tone(if c == 1 && placed { R } else { G }));
                }
                if step == 1 {
                    put(&mut f, mono("law", 180.0, 70.0, "6 ключей > 4 ячеек ⇒ коллизия", 12.0).tone(R));
                } else {
                    put(&mut f, mono("fn", 180.0, 70.0, "hash(key) % 4", 12.0));
                }
            }
            if step == 2 {
                for (t, x) in [("цепочки", 60.0), ("открытая адресация", 180.0), ("расширение", 300.0)] {
                    put(&mut f, zone(format!("box-{x}"), x, 71.0, 108.0, 94.0));
                    put(&mut f, tx(&format!("cap-{x}"), x, 136.0, t, 9.5));
                }
                // цепочка
                put(&mut f, bx("ch0", 60.0, 54.0, 52.0, 24.0, ""));
                put(&mut f, dot("ch-d1", 46.0, 54.0, "1").r(7.0).size(8.0).tone(G));
                put(&mut f, arrow("ch-ar", 54.0, 54.0, 64.0, 54.0).tone(G));
                put(&mut f, dot("ch-d2", 74.0, 54.0, "2").r(7.0).size(8.0).tone(G));
                put(&mut f, bx("ch1", 60.0, 90.0, 52.0, 24.0, ""));
                // открытая адресация
                for i in 0..3 {
                    put(&mut f, cell(format!("oa{i}"), 152.0 + i as f64 * 26.0, 72.0, "").w(24.0).h(32.0));
                }
                put(&mut f, dot("oa-d1", 152.0, 72.0, "1").r(7.0).size(8.0).tone(G));
                put(&mut f, dot("oa-d2", 178.0, 72.0, "2").r(7.0).size(8.0).tone(Y));
                put(&mut f, path("oa-hop", "M152 56 C160 36 172 36 178 54").tone(Y).width(1.4).arrow());
                // расширение
                for i in 0..2 {
                    put(&mut f, cell(format!("ex-a{i}"), 270.0 + i as f64 * 18.0, 50.0, "").w(16.0).h(24.0));
                }
                put(&mut f, mono("ex-t", 300.0, 82.0, "2 → 4 → 8", 10.0).tone(G));
                for i in 0..4 {
                    put(&mut f, cell(format!("ex-b{i}"), 270.0 + i as f64 * 18.0, 100.0, "").w(16.0).h(16.0).tone(G));
                }
            }
            // гистограммы: на шаге 2 столбики лежат невидимыми, на шаге 3 вырастают
            if step == 2 || step == 3 {
                for (j, (title, tone, hs)) in [("хорошо: ровно", G, [30.0, 28.0, 32.0, 30.0]), ("плохо: кучно", R, [74.0, 20.0, 18.0, 8.0])].into_iter().enumerate() {
                    if step == 3 {
                        put(&mut f, tx(&format!("h-t{j}"), 90.0 + j as f64 * 180.0, 22.0, title, 9.5).tone(tone));
                    }
                    for (c, h) in hs.iter().enumerate() {
                        let b = bar(format!("h{j}{c}"), 46.0 + j as f64 * 180.0 + c as f64 * 24.0 + 9.0, 130.0, if step == 3 { *h } else { 0.0 }).w(18.0).tone(tone);
                        put(&mut f, if step == 3 { b } else { b.opacity(0.0) });
                    }
                }
                if step == 3 {
                    put(&mut f, tx("h-note", 180.0, 152.0, "коллизии остаются — но редкие и нерегулярные", 9.5));
                }
            }
            if step >= 4 {
                put(&mut f, pill("no", 110.0, 64.0, 150.0, 34.0, "убрать коллизии", R, 10.0));
                put(&mut f, mono("no-x", 110.0, 104.0, "✗", 16.0).tone(R));
                put(&mut f, pill_g("yes", 270.0, 64.0, 150.0, 34.0, "сделать дешёвыми", 10.0));
                put(&mut f, mono("yes-v", 270.0, 104.0, "✓", 16.0).tone(G));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Таблица", "Коллизия", "Механика", "Хеш-функция", "Дизайн"],
        &[
            "Для программиста принцип — приговор и утешение одновременно",
            "В таблице четыре ячейки, ключей — сколько угодно: коллизия не «возможна», а гарантирована",
            "Отсюда вся механика: цепочки в ячейках, открытая адресация, расширение с перехешированием",
            "Хеш-функция не убирает коллизии — она лишь делает их редкими и нерегулярными",
            "Воевать с самой возможностью бессмысленно; делать коллизии дешёвыми — осмысленно",
        ],
        frames,
    )
    .cues(&[4.3, 14.3, 21.6, 26.6])
    .step_ms(3000)
}

// --- 11. Дни рождения и волосы -------------------------------------------------------------------------------------

fn birthday() -> SceneSpec {
    const N: usize = 23;
    let pts: Vec<(f64, f64)> = (0..N)
        .map(|i| {
            let a = 2.0 * std::f64::consts::PI * i as f64 / N as f64 - std::f64::consts::FRAC_PI_2;
            (180.0 + 58.0 * a.cos(), 82.0 + 58.0 * a.sin())
        })
        .collect();
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 1 {
                if step == 1 {
                    for i in 0..N {
                        for j in i + 1..N {
                            put(&mut f, line(format!("e{i}-{j}"), pts[i].0, pts[i].1, pts[j].0, pts[j].1).tone(G).width(0.8).opacity(0.35));
                        }
                    }
                }
                for (i, (x, y)) in pts.iter().enumerate() {
                    put(&mut f, dot(format!("man{i}"), *x, *y, "").r(4.5).tone(B));
                }
                if step == 0 {
                    put(&mut f, mono("n0", 62.0, 70.0, "23 человека", 12.0));
                    put(&mut f, tx("n0b", 62.0, 88.0, "366 дней", 9.5));
                } else {
                    put(&mut f, mono("n1", 62.0, 70.0, "253", 20.0).tone(G));
                    put(&mut f, tx("n1b", 62.0, 88.0, "пары-кандидаты", 9.5));
                    put(&mut f, mono("n1c", 300.0, 76.0, "C(23, 2)", 10.0));
                }
            } else {
                put(&mut f, zone("city", 100.0, 69.0, 120.0, 86.0).tone(B));
                put(&mut f, mono("c1", 100.0, 70.0, "1 000 000", 14.0).tone(B));
                put(&mut f, tx("c2", 100.0, 88.0, "человек в городе", 9.5));
                put(&mut f, mono("gt", 180.0, 72.0, ">", 18.0).tone(G));
                put(&mut f, zone("hairs", 260.0, 69.0, 120.0, 54.0).tone(Y));
                put(&mut f, mono("h1", 260.0, 68.0, "< 400 000", 13.0).tone(Y));
                put(&mut f, tx("h2", 260.0, 84.0, "вариантов числа волос", 9.5));
                if step == 2 {
                    put(&mut f, mono("fin0", 180.0, 140.0, "кроликов больше, чем клеток", 12.0));
                } else {
                    put(&mut f, mono("fin1", 180.0, 140.0, "двое с одинаковым числом волос есть", 12.0).tone(G));
                }
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Сюрприз", "Пары", "Волосы", "Итог"],
        &[
            "Тот же принцип даёт сюрприз: в группе из 23 человек двое с одним днём рождения — скорее да, чем нет, хотя дней 366",
            "Интуиция считает людей, а надо считать пары-кандидаты: их почти 250, и каждой достаточно совпасть",
            "Классическое доказательство существования: в городе-миллионнике двое с одинаковым числом волос",
            "Искать этих людей не нужно — Дирихле уже всё сказал",
        ],
        frames,
    )
    .cues(&[10.4, 19.1, 30.3])
    .step_ms(3000)
}

// --- 12. Криптографические хеши ------------------------------------------------------------------------------------

fn crypto() -> SceneSpec {
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 1 {
                for (i, t) in ["файл 1", "файл 2", "файл 3", "…"].iter().enumerate() {
                    put(&mut f, pill(&format!("file{i}"), 52.0, 30.0 + i as f64 * 32.0, 64.0, 22.0, t, B, 9.5));
                }
                put(&mut f, pill_g("H", 194.0, 83.0, 48.0, 90.0, "H", 14.0));
                for i in 0..3 {
                    put(&mut f, arrow(&format!("in{i}"), 86.0, 30.0 + i as f64 * 32.0, 166.0, 64.0 + i as f64 * 14.0).opacity(0.8));
                }
                let out = zone("out", 301.0, 83.0, 70.0, 54.0).tone(Y);
                put(&mut f, if step == 0 { out } else { out.dash() });
                put(&mut f, tx("out-l", 301.0, 48.0, "2ᵏ выходов", 9.5));
                for i in 0..4 {
                    put(&mut f, dot(format!("o{i}"), 282.0 + (i % 2) as f64 * 24.0, 74.0 + (i / 2) as f64 * 22.0, "").r(6.0).tone(Y));
                }
                if step == 1 {
                    put(&mut f, arrow("to-out", 222.0, 78.0, 262.0, 78.0).tone(Y));
                    put(&mut f, mono("law", 180.0, 152.0, "файлов больше, чем выходов ⇒ коллизия", 11.0).tone(R));
                }
            }
            if step == 2 {
                put(&mut f, mono("sha", 180.0, 30.0, "SHA-256: 2²⁵⁶ ≈ 1,2 · 10⁷⁷ значений", 12.0));
                put(&mut f, cell("space", 180.0, 55.0, "").w(280.0).h(14.0));
                put(&mut f, cell("dot", 41.5, 55.0, "").w(3.0).h(14.0).tone(R));
                put(&mut f, tx("tiny", 180.0, 86.0, "все когда-либо созданные файлы — крошечная точка слева", 9.5));
                put(&mut f, mono("hard", 180.0, 118.0, "поиск пары — практически нереален", 13.0).tone(G));
                put(&mut f, tx("uses", 180.0, 144.0, "цифровые подписи · контроль целостности", 9.5));
            }
            if step >= 3 {
                put(&mut f, pill_g("idea", 180.0, 70.0, 260.0, 44.0, "конечность — это структура", 13.0));
                put(&mut f, tx("idea-n", 180.0, 116.0, "принцип Дирихле напомнит о себе", 10.0));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Хеш", "Коллизия", "Масштаб", "Мысль"],
        &[
            "Даже криптография живёт под этим законом, просто с огромными числами",
            "У любого хеша конечное пространство выходов: при достаточном числе файлов коллизия обязана случиться",
            "Хорошая хеш-функция делает пространство практически необозримым — на этом держатся подписи и контроль целостности",
            "Конечность — это структура, а не мелочь: принцип Дирихле рано или поздно напомнит о себе",
        ],
        frames,
    )
    .cues(&[4.6, 16.0, 23.5])
    .step_ms(3000)
}

// --- 13. Итог главы ------------------------------------------------------------------------------------------------

fn recap() -> SceneSpec {
    // (крупная подпись, название, шаг, на котором карточка в фокусе)
    const CARDS: [(&str, &str, usize); 4] = [("Δ", "Паскаль", 1), ("(a+b)ⁿ", "бином", 2), ("∪ −", "включения", 3), ("5 > 4", "Дирихле", 3)];
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            for (i, (big, name, at)) in CARDS.iter().enumerate() {
                let on = step == *at;
                let s = if on { 1.1 } else { 1.0 };
                let x = 50.0 + i as f64 * 86.0;
                put(&mut f, cell(format!("card{i}"), x, 62.0, "").w(72.0).h(80.0).tone(if step >= *at { G } else { M }).scale(s));
                put(&mut f, mono(&format!("big{i}"), x, 62.0 + 4.0 * s, big, 15.0).tone(G).scale(s));
                put(&mut f, tx(&format!("name{i}"), x, 62.0 + 26.0 * s, name, 9.5).scale(s));
            }
            if step >= 4 {
                put(&mut f, pill_g("next", 180.0, 140.0, 260.0, 26.0, "Глава 5 · логика высказываний →", 11.0));
            }
            f
        })
        .collect();
    SceneSpec::new(
        &["Итог", "Паскаль", "Бином", "Включения · Дирихле", "Дальше"],
        &[
            "Подведём итог главы",
            "Треугольник Паскаля — таблица сочетаний, построенная одним сложением; строки суммируются в 2ⁿ",
            "Бином Ньютона раскладывает степень суммы по строке Паскаля и даёт быстрые прикидки",
            "Включения и исключения чинят двойной счёт, а принцип Дирихле гарантирует коллизии",
            "Дальше — логика высказываний: формально разберём условия из оператора «если»",
        ],
        frames,
    )
    .cues(&[1.4, 9.6, 14.7, 25.5])
    .step_ms(2600)
}

#[cfg(test)]
mod tests {
    use super::*;
    use content::Scene;

    /// Имена компонентов в порядке импортов `slides/dm/ch04.tsx`.
    const NAMES: [&str; 13] = ["C4Intro", "C4Pascal", "C4Paths", "C4Props", "C4Binomial", "C4Estimate", "C4Incl2", "C4Incl3", "C4Pigeon", "C4Hash", "C4Birthday", "C4Crypto", "C4Recap"];

    #[test]
    fn names_match_the_imports_of_the_slide_file() {
        let got: Vec<&str> = scenes().iter().map(|(n, _)| *n).collect();
        assert_eq!(got, NAMES);
    }

    #[test]
    fn every_scene_compiles_and_has_a_clean_layout() {
        for (name, spec) in scenes() {
            let scene = Scene::compile(&spec).unwrap_or_else(|e| panic!("{name}: {e}"));
            let lint = scene.lint();
            assert!(lint.is_empty(), "{name}: {lint:?}");
        }
    }

    #[test]
    fn steps_labels_captions_and_cues_agree() {
        for (name, spec) in scenes() {
            let n = spec.frames.len();
            assert_eq!(spec.labels.len(), n, "{name}: названий шагов");
            assert_eq!(spec.captions.len(), n, "{name}: подписей");
            let cues = spec.cues.as_ref().unwrap_or_else(|| panic!("{name}: нет cues"));
            assert_eq!(cues.len(), n - 1, "{name}: меток шагов");
            assert!(cues.windows(2).all(|w| w[0] < w[1]) && cues[0] > 0.0, "{name}: метки не по возрастанию");
        }
    }

    #[test]
    fn binomials_and_triangle_positions() {
        assert_eq!((0..=6).map(|k| binom(6, k)).collect::<Vec<_>>(), [1, 6, 15, 20, 15, 6, 1]);
        assert_eq!(binom(100, 2), 4950);
        assert_eq!(tri_pos(0, 0, 38.0, 20.0, 150.0, 18.0), (150.0, 18.0));
        assert_eq!(tri_pos(2, 0, 10.0, 5.0, 100.0, 0.0), (90.0, 10.0));
        assert_eq!(sup(14), "¹⁴");
    }
}
