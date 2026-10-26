//! Дискретная математика, глава 3 («Комбинаторика: перестановки и сочетания»): сцены.
//! Перенос с `frontend/src/slides/anim/C3*.tsx` (ручная отрисовка на `kit.tsx`) в данные: шаги, подписи и метки `cues` прежние.
//! Что упрощено: «столбики» (горизонтальные полосы) — ячейки, у которых ширина растёт между кадрами; ступенчатые задержки
//! появления рядов исчезли (всё в кадре появляется одновременно); двунаправленные стрелки в «Classify» — простые линии.

use content::{
    dsl::{arrow, bx, cell, dot, line, path, py, text},
    item::{Anchor, Cell, Dot, Line, Text},
    Frame, SceneSpec, Tone, B, G, M, R, Y,
};

/// Все сцены главы: имя прежнего компонента — описание.
pub fn scenes() -> Vec<(&'static str, SceneSpec)> {
    vec![
        ("C3Intro", intro()),
        ("C3Sum", sum()),
        ("C3Product", product()),
        ("C3Password", password()),
        ("C3Factorial", factorial()),
        ("C3Perm", perm()),
        ("C3Arrange", arrange()),
        ("C3Combine", combine()),
        ("C3Poker", poker()),
        ("C3Pairs", pairs()),
        ("C3Classify", classify()),
        ("C3Links", links()),
        ("C3Recap", recap()),
    ]
}

// --- помощники -----------------------------------------------------------------------------------

/// Плашка 20 в высоту с подписью (шрифт 10,5): (x, y) — центр.
fn pill(id: &str, x: f64, y: f64, w: f64, label: &str, tone: Tone) -> Cell {
    bx(id, x, y, w, 20.0, label).tone(tone).size(10.5)
}

/// Плашка произвольной высоты и шрифта.
fn pill_hs(id: &str, x: f64, y: f64, w: f64, h: f64, label: &str, tone: Tone, size: f64) -> Cell {
    bx(id, x, y, w, h, label).tone(tone).size(size)
}

/// Пустая рамка (карточка, панель, ячейка сетки): подписи кладутся поверх отдельными элементами.
fn panel(id: &str, x: f64, y: f64, w: f64, h: f64, tone: Tone) -> Cell {
    cell(id, x, y, "").w(w).h(h).tone(tone)
}

/// Приглушённая подпись (шрифт 10 по умолчанию): (x, y) — база строки.
fn cap(id: &str, x: f64, y: f64, label: &str) -> Text {
    text(id, x, y, label)
}

/// Моноширинная подпись обычным цветом текста.
fn mono(id: &str, x: f64, y: f64, size: f64, label: &str) -> Text {
    text(id, x, y, label).mono().size(size)
}

/// Моноширинная подпись цветом оттенка.
fn monoc(id: &str, x: f64, y: f64, size: f64, label: &str, tone: Tone) -> Text {
    mono(id, x, y, size, label).tone(tone)
}

/// Горизонтальная полоса от левого края `x`; не выросшая — нулевой ширины и невидимая (в следующем кадре вырастает).
fn hbar(id: &str, x: f64, y: f64, w: f64, h: f64, tone: Tone, grown: bool) -> Cell {
    if grown {
        panel(id, x + w / 2.0, y, w, h, tone)
    } else {
        panel(id, x, y, 0.0, h, tone).opacity(0.0)
    }
}

/// Кружок-узел без подписи или с номером (радиус 11 — как у прежних точек).
fn node(id: &str, x: f64, y: f64, label: &str, tone: Tone) -> Dot {
    dot(id, x, y, label).r(11.0).tone(tone)
}

/// Линия цвета рамки (прежний `var(--s-border)`).
fn rule(id: &str, x1: f64, y1: f64, x2: f64, y2: f64) -> Line {
    line(id, x1, y1, x2, y2).tone(Tone::Outline).width(1.2)
}

/// Число с пробелами между тройками цифр: 1302540 → «1 302 540».
fn group(n: u64) -> String {
    let s = n.to_string();
    let mut out = String::new();
    for (i, ch) in s.chars().enumerate() {
        if i > 0 && (s.len() - i) % 3 == 0 {
            out.push(' ');
        }
        out.push(ch);
    }
    out
}

fn frames(v: Vec<Frame>) -> Vec<Frame> {
    v
}

/// Точки правильного многоугольника: центр (cx, cy), радиус r, первая точка сверху.
fn ring(n: usize, r: f64, cx: f64, cy: f64) -> Vec<(f64, f64)> {
    (0..n)
        .map(|i| {
            let a = 2.0 * std::f64::consts::PI * i as f64 / n as f64 - std::f64::consts::FRAC_PI_2;
            (cx + r * a.cos(), cy + r * a.sin())
        })
        .collect()
}

/// Все пары вершин i < j.
fn all_pairs(n: usize) -> Vec<(usize, usize)> {
    (0..n).flat_map(|i| (i + 1..n).map(move |j| (i, j))).collect()
}

// --- 1. Введение ---------------------------------------------------------------------------------

fn intro() -> SceneSpec {
    let pin = |frame: Frame| {
        frame
            .with_all((0..4).map(|i| cell(format!("pin{i}"), 115.0 + i as f64 * 46.0, 67.0, "?").w(38.0).h(46.0).tone(G).size(22.0)))
            .with(mono("pin-top", 180.0, 30.0, 11.0, "каждая позиция: 10 цифр"))
            .with(monoc("pin-sum", 180.0, 122.0, 20.0, "10⁴ = 10 000", Y))
            .with(cap("pin-note", 180.0, 144.0, "считаем, а не перечисляем"))
    };
    let choices = |frame: Frame| {
        let mut f = frame;
        for i in 0..3 {
            let x = 70.0 + i as f64 * 110.0;
            f = f
                .with(pill(&format!("yes{i}"), x, 50.0, 64.0, "да", G))
                .with(pill(&format!("no{i}"), x, 84.0, 64.0, "нет", Y))
                .with(monoc(&format!("x2{i}"), x, 112.0, 13.0, "×2", G));
        }
        f.with(monoc("ch-sum", 180.0, 140.0, 14.0, "2 · 2 · 2 = 8 способов", G)).with(cap("ch-top", 180.0, 24.0, "три мелких решения"))
    };
    let tools = |frame: Frame| {
        let mut f = frame;
        for (i, (sym, name)) in [("+", "сумма"), ("×", "произведение")].iter().enumerate() {
            let x = 80.0 + i as f64 * 100.0;
            f = f
                .with(panel(&format!("rule{i}"), x, 53.0, 88.0, 46.0, G))
                .with(monoc(&format!("rule-s{i}"), x, 56.0, 20.0, sym, G))
                .with(cap(&format!("rule-n{i}"), x, 70.0, name));
        }
        f = f.with(cap("rules", 130.0, 22.0, "два правила"));
        for (i, (sym, name)) in [("n!", "перестановки"), ("A", "размещения"), ("C", "сочетания")].iter().enumerate() {
            let x = 75.0 + i as f64 * 100.0;
            f = f
                .with(panel(&format!("cnt{i}"), x, 127.0, 90.0, 46.0, Y))
                .with(monoc(&format!("cnt-s{i}"), x, 128.0, 17.0, sym, Y))
                .with(cap(&format!("cnt-n{i}"), x, 142.0, name));
        }
        f.with(cap("counters", 180.0, 98.0, "три счётчика"))
    };
    SceneSpec::new(
        &["Глава", "Перебор", "Выбор", "Инструменты"],
        &[
            "Комбинаторика: перестановки и сочетания",
            "Оценка «перебор отработает через сто лет» начинается с умения посчитать варианты",
            "Комбинаторика — арифметика выбора: из мелких решений складывается число способов",
            "Два правила и три счётчика — на них держатся почти все инженерные оценки",
        ],
        frames(vec![
            Frame::new().with(monoc("title", 180.0, 92.0, 24.0, "+   ×   n!   C(n, k)", G)),
            pin(Frame::new()),
            choices(Frame::new()),
            tools(Frame::new()),
        ]),
    )
    .cues(&[4.6, 14.4, 20.6])
    .step_ms(2800)
}

// --- 2. Правило суммы ----------------------------------------------------------------------------

fn sum() -> SceneSpec {
    let groups = |row: bool| {
        let mut f = Frame::new()
            .with(panel("hull-a", 92.0, 56.0, 132.0, 56.0, Tone::Blue).dash())
            .with(panel("hull-b", 268.0, 56.0, 132.0, 56.0, Y).dash())
            .with(cap("lbl-a", 92.0, 22.0, "A · 3 варианта").tone(B))
            .with(cap("lbl-b", 268.0, 22.0, "B · 4 варианта").tone(Y))
            .with(monoc("plus", 180.0, 62.0, 16.0, "+", G));
        for i in 0..3 {
            let (x, y) = if row { (36.0 + i as f64 * 30.0, 130.0) } else { (56.0 + i as f64 * 36.0, 56.0) };
            f = f.with(node(&format!("a{i}"), x, y, &(i + 1).to_string(), B));
        }
        for i in 0..4 {
            let (x, y) = if row { (126.0 + i as f64 * 30.0, 130.0) } else { (222.0 + i as f64 * 30.0, 56.0) };
            f = f.with(node(&format!("b{i}"), x, y, &(i + 4).to_string(), Y));
        }
        f
    };
    let menu = {
        let mut f = Frame::new().with(cap("soup-t", 90.0, 22.0, "супы · 3").tone(B)).with(cap("salad-t", 270.0, 22.0, "салаты · 4").tone(Y));
        for (i, t) in ["борщ", "щи", "уха"].iter().enumerate() {
            f = f.with(pill(&format!("soup{i}"), 90.0, 46.0 + i as f64 * 28.0, 70.0, t, B));
        }
        for (i, t) in ["цезарь", "греческий", "оливье", "винегрет"].iter().enumerate() {
            f = f.with(pill(&format!("salad{i}"), 270.0, 42.0 + i as f64 * 26.0, 86.0, t, Y));
        }
        f.with(mono("or", 180.0, 70.0, 14.0, "или")).with(monoc("menu-sum", 180.0, 150.0, 14.0, "3 + 4 = 7 первых блюд", G))
    };
    let branches = Frame::new()
        .with(panel("code-bg", 180.0, 79.0, 260.0, 106.0, Tone::Muted))
        .with(py("code", 66.0, 38.0, &["if cond:", "    …  # 3 пути", "else:", "    …  # 4 пути"]).hl([0, 2]).size(11.5).lh(19.0))
        .with(monoc("code-sum", 180.0, 152.0, 13.0, "всего путей: 3 + 4 = 7", G));
    SceneSpec::new(
        &["Правило", "3 + 4", "Меню", "Ветви"],
        &[
            "Правило суммы: выбираем ровно одну вещь, группы не пересекаются",
            "Три варианта в первой группе и четыре во второй — всего семь",
            "Три супа или четыре салата — семь способов выбрать первое блюдо",
            "В коде это ветвление: число путей исполнения складывается по веткам",
        ],
        frames(vec![
            groups(false).with(cap("disjoint", 180.0, 150.0, "A ∩ B = ∅ — общих вариантов нет")),
            groups(true).with(monoc("row-sum", 180.0, 104.0, 13.0, "3 + 4 = 7", G)),
            menu,
            branches,
        ]),
    )
    .cues(&[3.7, 12.7, 17.2])
    .step_ms(2800)
}

// --- 3. Правило произведения ---------------------------------------------------------------------

fn product() -> SceneSpec {
    let tree = {
        let mut f = Frame::new().with(pill("root", 40.0, 80.0, 56.0, "старт", M));
        for (i, t) in ["М", "Ж"].iter().enumerate() {
            let y = 50.0 + i as f64 * 60.0;
            f = f.with(rule(&format!("t1-{i}"), 68.0, 80.0, 110.0, y)).with(pill(&format!("mid{i}"), 130.0, y, 40.0, t, B));
        }
        for i in 0..2 {
            for j in 0..3 {
                let y = 24.0 + i as f64 * 66.0 + j as f64 * 22.0;
                let name = format!("{}{}", i + 1, ["а", "б", "в"][j]);
                f = f.with(rule(&format!("t2-{i}{j}"), 150.0, 50.0 + i as f64 * 60.0, 224.0, y)).with(pill(&format!("leaf{i}{j}"), 246.0, y, 48.0, &name, Y));
            }
        }
        f.with(monoc("tree-sum", 320.0, 84.0, 14.0, "2·3=6", G))
    };
    let pin = {
        let mut f = Frame::new();
        for i in 0..4 {
            let x = 101.0 + i as f64 * 56.0;
            f = f
                .with(panel(&format!("pin{i}"), x, 65.0, 46.0, 54.0, G))
                .with(monoc(&format!("pin-n{i}"), x, 68.0, 20.0, "10", G))
                .with(cap(&format!("pin-c{i}"), x, 84.0, "цифр"));
            if i < 3 {
                f = f.with(monoc(&format!("pin-x{i}"), x + 28.0, 68.0, 15.0, "×", Y));
            }
        }
        f.with(monoc("pin-sum", 180.0, 130.0, 18.0, "10⁴ = 10 000", G))
    };
    let loops = {
        let mut f = Frame::new()
            .with(py("loops", 30.0, 20.0, &["for a in A:", "    for b in B:", "        body(a, b)"]).hl([2]).size(11.0).lh(16.0));
        for r in 0..3 {
            for c in 0..4 {
                f = f.with(panel(&format!("g{r}{c}"), 199.0 + c as f64 * 32.0, 43.0 + r as f64 * 32.0, 26.0, 26.0, G));
            }
        }
        f.with(mono("b-axis", 250.0, 22.0, 10.0, "B →"))
            .with(mono("a-axis", 170.0, 64.0, 10.0, "A ↓"))
            .with(monoc("loops-sum", 180.0, 150.0, 13.0, "итераций: 3 · 4 = 12", G))
    };
    let times = Frame::new().with(monoc("times", 180.0, 86.0, 56.0, "×", G)).with(cap("times-note", 180.0, 126.0, "независимые выборы → умножаем"));
    SceneSpec::new(
        &["Правило", "Выборы", "Пин-код", "Циклы", "Умножайте"],
        &[
            "Правило произведения заметно мощнее правила суммы",
            "Несколько независимых выборов подряд: число вариантов перемножается — 2 · 3 = 6",
            "Пин-код из четырёх цифр: на каждой позиции десять возможностей — 10⁴ = 10 000",
            "Вложенные циклы — прямое воплощение правила: итераций тела столько, сколько длина × длина",
            "Как только видите цепочку независимых выборов — умножайте",
        ],
        frames(vec![Frame::new().with(monoc("title", 180.0, 86.0, 20.0, "правило произведения", G)), tree, pin, loops, times]),
    )
    .cues(&[2.7, 7.6, 15.0, 24.5])
    .step_ms(2800)
}

// --- 4. Пространство паролей ---------------------------------------------------------------------

fn password() -> SceneSpec {
    let lens: Vec<(u32, f64)> = [6u32, 8, 10, 12].iter().map(|&n| (n, n as f64 * 95f64.log10())).collect();
    let cells = |frame: Frame| frame.with_all((0..8).map(|i| cell(format!("sym{i}"), 46.0 + i as f64 * 38.0, 56.0, "95").w(32.0).h(44.0).tone(G).size(14.0)));
    // полосы длины: `grown` — выросли (иначе нулевой ширины, чтобы вырасти в следующем кадре)
    let lengths = |grown: bool| {
        let mut f = Frame::new();
        for (i, (n, lg)) in lens.iter().enumerate() {
            let y = 39.0 + i as f64 * 28.0;
            let w = lg * 9.0;
            f = f.with(hbar(&format!("len{i}"), 72.0, y, w, 18.0, G, grown));
            if grown {
                f = f
                    .with(mono(&format!("len-n{i}"), 64.0, y + 3.0, 11.0, &format!("{n} символов")).anchor(Anchor::End))
                    .with(monoc(&format!("len-v{i}"), 78.0 + w, y + 3.0, 10.0, &format!("10^{lg:.0}"), Y).anchor(Anchor::Start));
            }
        }
        if grown {
            f = f.with(cap("len-note", 180.0, 152.0, "длина полосы — порядок числа вариантов").size(9.5));
        }
        f
    };
    let phrase = |grown: bool| {
        let mut f = Frame::new()
            .with(hbar("short", 40.0, 61.0, 95.0, 18.0, Y, grown))
            .with(hbar("words", 40.0, 117.0, 200.0, 18.0, G, grown));
        if grown {
            f = f
                .with(mono("short-t", 40.0, 44.0, 11.0, "6 символов: 95⁶ ≈ 7 · 10¹¹").anchor(Anchor::Start))
                .with(mono("words-t", 40.0, 100.0, 11.0, "4 слова из 2000: 2000⁴ ≈ 1,6 · 10¹³").anchor(Anchor::Start))
                .with(cap("stronger", 250.0, 86.0, "сильнее").tone(G).anchor(Anchor::Start));
        }
        f
    };
    // кадр 1 несёт ещё и невыросшие полосы шага 2, кадр 2 — полосы шага 3
    let with_hidden = |frame: Frame, extra: Frame| frame.with_all(extra.0);
    let hidden_lengths = Frame::new().with_all((0..4).map(|i| hbar(&format!("len{i}"), 72.0, 39.0 + i as f64 * 28.0, lens[i].1 * 9.0, 18.0, G, false)));
    let hidden_phrase = Frame::new().with(hbar("short", 40.0, 61.0, 95.0, 18.0, Y, false)).with(hbar("words", 40.0, 117.0, 200.0, 18.0, G, false));
    SceneSpec::new(
        &["Пароль", "95⁸", "Длина", "Фраза", "Перебор"],
        &[
            "Применим правило произведения к паролям",
            "Восемь символов из девяноста пяти — 95⁸, около 6,6 квадриллиона вариантов",
            "Каждый лишний символ умножает пространство на 95 — рост очень быстрый",
            "Длинный пароль из простых слов обычно сильнее короткого из «умных» символов",
            "Перебор упирается не в талант взломщика, а в размер пространства",
        ],
        frames(vec![
            cells(Frame::new()),
            with_hidden(
                cells(Frame::new())
                    .with(cap("pos-note", 180.0, 26.0, "на каждой позиции — 95 печатных знаков"))
                    .with(monoc("total", 180.0, 116.0, 16.0, "95⁸ ≈ 6,6 · 10¹⁵", Y))
                    .with(cap("total-note", 180.0, 140.0, "около шести с половиной квадриллионов")),
                hidden_lengths,
            ),
            with_hidden(lengths(true), hidden_phrase),
            phrase(true),
            Frame::new()
                .with(mono("rate", 180.0, 38.0, 11.0, "1 млрд проб в секунду"))
                .with(monoc("t8", 180.0, 78.0, 20.0, "95⁸ → ≈ 77 суток", Y))
                .with(monoc("t12", 180.0, 116.0, 20.0, "95¹² → ≈ 17 млн лет", G))
                .with(cap("t-note", 180.0, 148.0, "каждый символ в длине — ×95 ко времени")),
        ]),
    )
    .cues(&[2.7, 11.1, 18.5, 27.4])
    .step_ms(2800)
}

// --- 5. Факториал --------------------------------------------------------------------------------

/// Ломаная «порядок числа» для n = 1…15: по горизонтали n, по вертикали lg f(n).
fn curve(f: impl Fn(f64) -> f64) -> String {
    let pts: Vec<String> = (1..=15).map(|n| format!("{:.1} {:.1}", 40.0 + n as f64 * 19.0, 140.0 - f(n as f64).log10() * 9.0)).collect();
    format!("M{}", pts.join(" L"))
}

fn factorial() -> SceneSpec {
    let fact = |n: f64| (1..=n as u64).map(|v| v as f64).product::<f64>();
    let run = ["4", "12", "24", "24"];
    let chain = {
        let mut f = Frame::new();
        for (i, v) in [4, 3, 2, 1].iter().enumerate() {
            let x = 56.0 + i as f64 * 76.0;
            f = f.with(pill_hs(&format!("v{i}"), x, 50.0, 44.0, 20.0, &v.to_string(), B, 14.0)).with(monoc(&format!("run{i}"), x, 92.0, 13.0, run[i], G));
            if i < 3 {
                f = f.with(monoc(&format!("x{i}"), 94.0 + i as f64 * 76.0, 54.0, 14.0, "×", Y));
            }
        }
        f.with(monoc("res", 180.0, 126.0, 16.0, "4! = 24", G))
    };
    // (n, подпись, порядок числа / 12 шириной)
    let bars: [(u32, &str, f64); 4] = [(5, "120", 2.08), (10, "3,6 · 10⁶", 6.56), (15, "1,3 · 10¹²", 12.12), (20, "2,4 · 10¹⁸", 18.39)];
    let growth = |grown: bool| {
        let mut f = Frame::new();
        for (i, (n, t, lg)) in bars.iter().enumerate() {
            let y = 43.0 + i as f64 * 30.0;
            let w = lg * 12.0 + 6.0;
            f = f.with(hbar(&format!("fb{i}"), 48.0, y, w, 18.0, Y, grown));
            if grown {
                f = f.with(mono(&format!("fb-n{i}"), 40.0, y + 3.0, 11.0, &format!("{n}!")).anchor(Anchor::End)).with(mono(&format!("fb-v{i}"), 48.0 + w + 6.0, y + 3.0, 10.0, t).anchor(Anchor::Start));
            }
        }
        f
    };
    let hidden_bars = growth(false);
    let axes = |draw: f64, o: f64| {
        Frame::new()
            .with(path("c-2n", curve(|n| 2f64.powf(n))).tone(B).width(2.2).draw(draw).opacity(o))
            .with(path("c-fact", curve(fact)).tone(Y).width(2.2).draw(draw).opacity(o))
    };
    let growth_frame = Frame::new().with_all(growth(true).0).with_all(axes(0.0, 0.0).0);
    let compare = Frame::new()
        .with(rule("ax-x", 40.0, 140.0, 332.0, 140.0).width(1.6))
        .with(rule("ax-y", 40.0, 20.0, 40.0, 140.0).width(1.6))
        .with_all(axes(1.0, 1.0).0)
        .with(monoc("l-fact", 300.0, 48.0, 11.0, "n!", Y).anchor(Anchor::End))
        .with(monoc("l-2n", 300.0, 104.0, 11.0, "2ⁿ", B).anchor(Anchor::End))
        .with(cap("axis-note", 186.0, 156.0, "n = 1 … 15, по вертикали порядок числа (логарифм)").size(9.0));
    SceneSpec::new(
        &["Определение", "4!", "Рост", "Против 2ⁿ"],
        &[
            "Для подсчёта порядков нужна своя единица — факториал",
            "n! — произведение всех чисел от 1 до n: 4! = 4 · 3 · 2 · 1 = 24",
            "Растёт пугающе: 10! — больше трёх с половиной миллионов, 20! — за квинтиллион",
            "n! догоняет и обгоняет экспоненту уже на скромных числах — и железо не спасёт",
        ],
        frames(vec![
            Frame::new().with(monoc("def", 180.0, 86.0, 22.0, "n! = 1 · 2 · … · n", G)),
            chain.with_all(hidden_bars.0),
            growth_frame,
            compare,
        ]),
    )
    .cues(&[4.4, 10.1, 17.5])
    .step_ms(3000)
}

// --- 6. Перестановки -----------------------------------------------------------------------------

fn perm() -> SceneSpec {
    let orders = ["abc", "acb", "bac", "bca", "cab", "cba"];
    let tone_of = |ch: char| [B, Y, G][(ch as u8 - b'a') as usize];
    let six = {
        let mut f = Frame::new();
        for (i, o) in orders.iter().enumerate() {
            for (j, ch) in o.chars().enumerate() {
                f = f.with(pill(&format!("o{i}{j}"), 64.0 + (i % 3) as f64 * 112.0 + j as f64 * 30.0, 36.0 + (i / 3) as f64 * 40.0, 26.0, &ch.to_string(), tone_of(ch)));
            }
        }
        f.with(monoc("six", 180.0, 140.0, 15.0, "3! = 3 · 2 · 1 = 6", G))
    };
    let talks = Frame::new()
        .with_all((0..10).map(|i| pill_hs(&format!("talk{i}"), 36.0 + i as f64 * 32.0, 52.0, 28.0, 20.0, &format!("Д{}", i + 1), B, 9.0)))
        .with(cap("talk-top", 180.0, 30.0, "10 слотов в расписании"))
        .with(monoc("talk-sum", 180.0, 112.0, 16.0, "10! = 3 628 800", Y))
        .with(cap("talk-note", 180.0, 138.0, "расписаний"));
    let city: [(f64, f64); 6] = [(60.0, 50.0), (140.0, 30.0), (250.0, 54.0), (300.0, 108.0), (190.0, 124.0), (86.0, 112.0)];
    let mut tour = Frame::new();
    for (i, &(x, y)) in city.iter().enumerate() {
        let (nx, ny) = city[(i + 1) % 6];
        tour = tour.with(line(format!("road{i}"), x, y, nx, ny).tone(G).width(1.8).dash_pattern("5 3"));
    }
    for (i, &(x, y)) in city.iter().enumerate() {
        tour = tour.with(node(&format!("city{i}"), x, y, &(i + 1).to_string(), Y));
    }
    let tour = tour.with(monoc("tour-note", 180.0, 154.0, 12.0, "n городов → порядка n! маршрутов", G));
    let fifty = Frame::new()
        .with(monoc("fifty", 180.0, 58.0, 26.0, "50! ≈ 3 · 10⁶⁴", R))
        .with(cap("fifty-note", 180.0, 92.0, "маршрутов — за разумное время не перебрать"))
        .with(pill_hs("exit", 180.0, 124.0, 230.0, 26.0, "выход: приближённые алгоритмы", G, 11.0));
    SceneSpec::new(
        &["n!", "Доклады", "Коммивояжёр", "50 городов"],
        &[
            "Перестановка — способ расставить n предметов по местам; способов ровно n!",
            "Десять докладов на конференции — 10! вариантов расписания, больше 3,5 миллионов",
            "Коммивояжёр: обойти все города по самому короткому маршруту — вариантов столько же, сколько перестановок",
            "При 50 городах полный перебор не закончится никогда — отсюда приближённые алгоритмы",
        ],
        frames(vec![six, talks, tour, fifty]),
    )
    .cues(&[5.9, 13.7, 23.9])
    .step_ms(3000)
}

// --- 7. Размещения -------------------------------------------------------------------------------

fn arrange() -> SceneSpec {
    let question = Frame::new()
        .with(pill_hs("order", 110.0, 70.0, 150.0, 46.0, "порядок важен?", G, 12.0))
        .with(arrow("ar-yes", 190.0, 62.0, 242.0, 38.0).tone(Y))
        .with(arrow("ar-no", 190.0, 78.0, 242.0, 102.0).tone(G))
        .with(pill_hs("yes", 296.0, 38.0, 90.0, 20.0, "да: размещение", Y, 9.5))
        .with(pill_hs("no", 296.0, 102.0, 90.0, 20.0, "нет: сочетание", G, 9.5));
    let podium = {
        let mut f = Frame::new();
        // (подпись места, название, число вариантов, высота ступени над общим основанием)
        for (i, (m, t, n, up)) in [("🥇", "золото", "20", 38.0), ("🥈", "серебро", "19", 24.0), ("🥉", "бронза", "18", 12.0)].iter().enumerate() {
            let x = 98.0 + i as f64 * 88.0;
            let h = 44.0 + up;
            f = f
                .with(panel(&format!("step{i}"), x, 134.0 - h / 2.0, 76.0, h, Y))
                .with(text(format!("medal{i}"), x, 70.0 - up, *m).size(22.0))
                .with(monoc(&format!("num{i}"), x, 120.0, 15.0, n, G))
                .with(cap(&format!("place{i}"), x, 134.0, t));
        }
        f.with(monoc("podium-sum", 180.0, 154.0, 13.0, "20 · 19 · 18 = 6 840", G))
    };
    let formula = {
        let mut f = Frame::new().with(mono("formula", 180.0, 26.0, 13.0, "n! / (n − k)!   при n = 20, k = 3"));
        for i in 0..20u32 {
            let x = 21.0 + i as f64 * 16.4;
            f = f.with(cell(format!("n{i}"), x, 55.0, (20 - i).to_string()).w(14.0).h(22.0).size(7.0).tone(if i < 3 { G } else { M }));
        }
        f.with(line("cut", 62.0, 72.0, 62.0, 40.0).tone(R).dash())
            .with(cap("need", 36.0, 86.0, "нужны").tone(G))
            .with(cap("tail", 200.0, 86.0, "хвост (17!) сокращается").tone(M))
            .with(monoc("formula-sum", 180.0, 130.0, 15.0, "20!/17! = 20 · 19 · 18", G))
    };
    let pin = {
        let mut f = Frame::new();
        for (i, v) in [10, 9, 8, 7].iter().enumerate() {
            let x = 97.0 + i as f64 * 56.0;
            f = f.with(panel(&format!("d{i}"), x, 67.0, 46.0, 54.0, G)).with(monoc(&format!("d-n{i}"), x, 73.0, 20.0, &v.to_string(), G));
        }
        f.with(cap("pin-top", 180.0, 30.0, "цифры не повторяются: выбор сужается")).with(monoc("pin-sum", 180.0, 130.0, 16.0, "10!/6! = 5 040", G))
    };
    let swap = Frame::new()
        .with(pill("p1", 90.0, 50.0, 100.0, "(Аня, Борис)", B))
        .with(pill("p2", 90.0, 96.0, 100.0, "(Борис, Аня)", Y))
        .with(monoc("neq", 180.0, 78.0, 20.0, "≠", R))
        .with(cap("other", 270.0, 76.0, "другая комбинация"))
        .with(cap("means", 270.0, 94.0, "значит — размещение").tone(G));
    SceneSpec::new(
        &["Порядок", "Подиум", "Формула", "Пин-код", "Проверка"],
        &[
            "Теперь выбираем не всё, а часть, — и смотрим, важен ли порядок",
            "Золото, серебро, бронза из двадцати: три разные награды, 20 · 19 · 18 = 6 840 способов",
            "Формула словами: n! делим на (n − k)! — отрезаем хвост тех, кто остался без места",
            "Пин-код без повторяющихся цифр: 10 · 9 · 8 · 7 = 10!/6! = 5 040 вариантов",
            "Если поменять двоих выбранных местами и получится другая комбинация — считаем размещение",
        ],
        frames(vec![question, podium, formula, pin, swap]),
    )
    .cues(&[4.0, 13.8, 22.6, 30.4])
    .step_ms(3000)
}

// --- 8. Сочетания --------------------------------------------------------------------------------

fn combine() -> SceneSpec {
    let ord = ["abc", "acb", "bac", "bca", "cab", "cba"];
    // порядки сливаются в одну точку (128, 56) и гаснут
    let orders = |merged: bool| {
        Frame::new().with_all(ord.iter().enumerate().map(|(i, o)| {
            let (x, y) = if merged { (128.0, 56.0) } else { (70.0 + (i % 3) as f64 * 56.0, 40.0 + (i / 3) as f64 * 34.0) };
            pill(&format!("ord{i}"), x, y, 48.0, o, M).opacity(if merged { 0.0 } else { 1.0 })
        }))
    };
    let free = orders(false)
        .with(pill("set", 270.0, 56.0, 90.0, "{a, b, c}", G))
        .with(monoc("to", 226.0, 60.0, 16.0, "→", G))
        .with(monoc("free-sum", 180.0, 130.0, 13.0, "6 порядков = 1 сочетание", G));
    let ratio = Frame::new()
        .with_all(orders(true).0)
        .with(mono("ratio", 180.0, 28.0, 13.0, "C(n, k) = A(n, k) / k!"))
        .with(pill_hs("r-a", 70.0, 76.0, 80.0, 20.0, "A = 60", Y, 14.0))
        .with(monoc("div", 130.0, 80.0, 16.0, "÷", G))
        .with(pill_hs("r-f", 190.0, 76.0, 80.0, 20.0, "3! = 6", B, 14.0))
        .with(monoc("eq", 248.0, 80.0, 16.0, "=", G))
        .with(pill_hs("r-c", 310.0, 76.0, 80.0, 20.0, "C = 10", G, 14.0))
        .with(cap("ratio-note", 180.0, 130.0, "C(5, 3): выбрать трёх из пяти"));
    let deck = {
        let picked = [3usize, 14, 22, 38, 47];
        Frame::new()
            .with_all((0..52).map(|i| panel(&format!("card{i}"), 24.0 + (i % 13) as f64 * 25.0, 37.0 + (i / 13) as f64 * 24.0, 20.0, 18.0, if picked.contains(&i) { G } else { M })))
            .with(monoc("deck-sum", 180.0, 140.0, 16.0, "C(52, 5) = 2 598 960", G))
    };
    let reviewers = {
        let name = |i: usize| "ABCDEF".chars().nth(i).map_or(String::new(), |c| c.to_string());
        Frame::new()
            .with_all((0..6).map(|i| node(&format!("dev{i}"), 40.0 + i as f64 * 50.0, 34.0, &name(i), B)))
            .with_all(all_pairs(6).iter().enumerate().map(|(i, &(a, b))| pill_hs(&format!("pair{i}"), 34.0 + (i % 5) as f64 * 66.0, 74.0 + (i / 5) as f64 * 24.0, 56.0, 20.0, &format!("{}{}", name(a), name(b)), G, 9.5)))
            .with(monoc("rev-sum", 180.0, 160.0, 12.0, "C(6, 2) = 15", G))
    };
    let link = Frame::new()
        .with(panel("c-box", 62.0, 58.0, 64.0, 40.0, G))
        .with(monoc("c-sym", 62.0, 62.0, 14.0, "C", G))
        .with(monoc("times-k", 118.0, 62.0, 16.0, "· k!", Y))
        .with(mono("link-eq", 160.0, 62.0, 16.0, "="))
        .with(panel("a-box", 260.0, 58.0, 140.0, 40.0, Y))
        .with(monoc("a-sym", 260.0, 62.0, 14.0, "A  (с порядком)", Y))
        .with(mono("link-sum", 180.0, 118.0, 13.0, "A(5,3) = C(5,3) · 3! = 10 · 6 = 60"));
    SceneSpec::new(
        &["Без порядка", "A / k!", "Колода", "Ревьюеры", "Связь"],
        &[
            "Если порядок не важен — считаем сочетания: шесть порядков одной тройки неотличимы",
            "Сочетание — размещение, делённое на k!: делим на все перестановки внутри группы",
            "Пять карт из пятидесяти двух — C(52, 5), около 2,6 миллиона рук",
            "Двое ревьюеров из шести — C(6, 2) = 15 вариантов",
            "Выборка с порядком и без отличается ровно в k! раз",
        ],
        frames(vec![free, ratio, deck, reviewers, link]),
    )
    .cues(&[6.2, 17.1, 22.7, 27.1])
    .step_ms(3000)
}

// --- 9. Числа покера -----------------------------------------------------------------------------

fn poker() -> SceneSpec {
    const CAT: [(&str, u64); 10] = [
        ("старшая карта", 1_302_540),
        ("пара", 1_098_240),
        ("две пары", 123_552),
        ("тройка", 54_912),
        ("стрит", 10_200),
        ("флеш", 5_108),
        ("фулл-хаус", 3_744),
        ("каре", 624),
        ("стрит-флеш", 36),
        ("флеш-рояль", 4),
    ];
    let tone_of = |i: usize| if i > 6 { R } else { Y };
    let bar_w = |v: u64| (v as f64).log10() * 32.0;
    let hidden_bars = Frame::new().with_all(CAT.iter().enumerate().map(|(i, &(_, v))| hbar(&format!("hb{i}"), 104.0, 20.0 + i as f64 * 14.0, bar_w(v), 10.0, tone_of(i), false)));
    // колода: на первом шаге — крупная плашка, на втором — сжимается к левому краю
    let all = Frame::new().with(cell("deck", 180.0, 69.0, "2 598 960 рук").w(220.0).h(70.0).size(20.0).tone(G)).with(cap("deck-note", 180.0, 132.0, "C(52, 5) — все возможные руки"));
    let cats = Frame::new()
        .with(cell("deck", 65.0, 74.0, "2 598 960").w(90.0).h(100.0).size(11.0).tone(G))
        .with_all(CAT.iter().enumerate().map(|(i, &(n, _))| pill_hs(&format!("cat{i}"), 200.0 + (i % 2) as f64 * 90.0, 34.0 + (i / 2) as f64 * 22.0, 84.0, 18.0, n, Y, 8.5)))
        .with(monoc("cats-sum", 180.0, 152.0, 12.0, "10 категорий", G))
        .with_all(hidden_bars.0);
    let rarity = {
        let mut f = Frame::new();
        for (i, &(n, v)) in CAT.iter().enumerate() {
            let y = 20.0 + i as f64 * 14.0;
            let w = bar_w(v);
            f = f
                .with(cap(&format!("pk-n{i}"), 100.0, y + 4.0, n).size(8.5).anchor(Anchor::End))
                .with(hbar(&format!("hb{i}"), 104.0, y, w, 10.0, tone_of(i), true))
                .with(mono(&format!("pk-v{i}"), 104.0 + w + 5.0, y + 4.0, 8.0, &group(v)).anchor(Anchor::Start));
        }
        f
    };
    let method = {
        let mut f = Frame::new();
        for (i, (n, t)) in [("1", "все исходы"), ("2", "группировка\nпо свойству"), ("3", "размер группы")].iter().enumerate() {
            let x = 72.0 + i as f64 * 114.0;
            f = f.with(panel(&format!("st{i}"), x, 76.0, 104.0, 56.0, G)).with(monoc(&format!("st-n{i}"), x, 68.0, 16.0, n, G)).with(cap(&format!("st-t{i}"), x, 82.0, t));
            if i < 2 {
                f = f.with(monoc(&format!("st-a{i}"), 130.0 + i as f64 * 114.0, 80.0, 14.0, "→", Y));
            }
        }
        f
    };
    let share = Frame::new()
        .with(mono("pr", 180.0, 46.0, 13.0, "P(каре) = 624 / 2 598 960"))
        .with(monoc("pr-v", 180.0, 86.0, 22.0, "≈ 0,024 %", G))
        .with(panel("track", 180.0, 115.0, 260.0, 10.0, M))
        .with(panel("mark", 51.0, 115.0, 2.0, 10.0, Tone::SolidRed))
        .with(cap("pr-note", 180.0, 140.0, "доля группы в целом — это и есть вероятность"));
    SceneSpec::new(
        &["Пространство", "Категории", "Редкость", "Приём", "Вероятность"],
        &[
            "Числа покера показывают, как комбинации сжимают пространство исходов",
            "Рук — две с половиной миллиона, а старшинств всего десяток категорий",
            "Миллионы рук раскладываются по категориям очень неравномерно — редкость делает категорию старше",
            "Общий приём: посчитать все исходы, сгруппировать по свойству, посчитать группу",
            "Отношение размера группы к целому — вероятность: каре — около 0,024 %",
        ],
        frames(vec![all, cats, rarity, method, share]),
    )
    .cues(&[5.9, 11.5, 18.1, 26.3])
    .step_ms(3000)
}

// --- 10. Число пар -------------------------------------------------------------------------------

fn pairs() -> SceneSpec {
    let p10 = ring(10, 56.0, 180.0, 84.0);
    let p7 = ring(7, 54.0, 180.0, 84.0);
    let handshakes = {
        let mut f = Frame::new();
        for (a, b) in all_pairs(10) {
            f = f.with(line(format!("h{a}-{b}"), p10[a].0, p10[a].1, p10[b].0, p10[b].1).tone(G).width(1.0).opacity(0.5));
        }
        for (i, &(x, y)) in p10.iter().enumerate() {
            f = f.with(dot(format!("hp{i}"), x, y, "").r(6.0).tone(B));
        }
        f.with(monoc("h-sum", 72.0, 90.0, 20.0, "45", G)).with(cap("h-note", 72.0, 106.0, "рукопожатий")).with(mono("h-calc", 288.0, 90.0, 11.0, "10 · 9 / 2"))
    };
    let triangle = {
        let n = ["0", "1", "2", "3", "4", "5", "6"];
        let mut f = Frame::new();
        for (c, l) in n.iter().enumerate() {
            f = f.with(mono(&format!("mc{c}"), 210.0 + c as f64 * 20.0, 25.0, 10.0, l));
        }
        for (r, l) in n.iter().enumerate() {
            f = f.with(mono(&format!("mr{r}"), 193.0, 43.5 + r as f64 * 20.0, 10.0, l).anchor(Anchor::End));
            for c in 0..7 {
                f = f.with(panel(&format!("m{r}{c}"), 210.0 + c as f64 * 20.0, 40.0 + r as f64 * 20.0, 17.0, 17.0, if c > r { G } else { M }));
            }
        }
        f.with(py("pair-loops", 24.0, 36.0, &["for i in range(n):", "    for j in range(i+1, n):", "        pair(i, j)"]).hl([2]).size(10.0).lh(18.0))
            .with(monoc("tri-note", 110.0, 150.0, 11.0, "j > i: ровно C(n, 2) клеток", G))
    };
    let servers = {
        let mut f = Frame::new();
        for (a, b) in all_pairs(7) {
            f = f.with(line(format!("s{a}-{b}"), p7[a].0, p7[a].1, p7[b].0, p7[b].1).tone(Y).width(1.0).opacity(0.5));
        }
        for (i, &(x, y)) in p7.iter().enumerate() {
            f = f.with(cell(format!("sv{i}"), x, y, "").w(12.0).h(12.0).tone(Y));
        }
        f.with(mono("s-n", 62.0, 86.0, 11.0, "100 серверов")).with(monoc("s-sum", 298.0, 84.0, 18.0, "4 950", Y)).with(cap("s-note", 298.0, 102.0, "каналов"))
    };
    SceneSpec::new(
        &["C(n, 2)", "Рукопожатия", "Цикл", "Серверы"],
        &[
            "Частный случай сочетаний — число пар: C(n, 2) = n(n − 1) / 2",
            "Десять человек пожмут руки C(10, 2) = 45 раз",
            "В коде: второй индекс всегда больше первого — все пары без повторов и зеркальных дублей",
            "Это же число рёбер полного графа: для 100 серверов нужно 4 950 каналов",
        ],
        frames(vec![Frame::new().with(monoc("formula", 180.0, 78.0, 20.0, "C(n, 2) = n(n − 1) / 2", G)), handshakes, triangle, servers]),
    )
    .cues(&[6.6, 11.5, 18.8])
    .step_ms(3000)
}

// --- 11. Двойной счёт и классификация ------------------------------------------------------------

fn classify() -> SceneSpec {
    let dup = {
        let mut f = Frame::new();
        for (i, t) in ["АБ", "БА", "АВ", "ВА", "БВ", "ВБ"].iter().enumerate() {
            f = f.with(pill(&format!("d{i}"), 50.0 + (i % 2) as f64 * 70.0, 34.0 + (i / 2) as f64 * 32.0, 56.0, t, if i % 2 == 1 { R } else { G }));
        }
        f.with(monoc("six", 236.0, 60.0, 14.0, "6 пар?", R))
            .with(monoc("three", 236.0, 80.0, 14.0, "на деле 3", G))
            .with(cap("dup-note", 180.0, 150.0, "«АБ» и «БА» — один и тот же выбор"))
    };
    let friends: [(f64, f64, &str); 3] = [(180.0, 36.0, "А"), (110.0, 112.0, "Б"), (250.0, 112.0, "В")];
    let trio = |checked: bool| {
        let mut f = Frame::new().with_all(friends.iter().enumerate().map(|(i, &(x, y, t))| dot(format!("fr{i}"), x, y, t).r(14.0).tone(B)));
        if checked {
            f = f
                .with(line("pair-ab", 172.0, 46.0, 118.0, 102.0).tone(G).width(2.0))
                .with(line("pair-av", 188.0, 46.0, 242.0, 102.0).tone(G).width(2.0))
                .with(line("pair-bv", 126.0, 112.0, 234.0, 112.0).tone(G).width(2.0))
                .with(monoc("by-hand", 60.0, 70.0, 13.0, "руками: 3", G))
                .with(monoc("by-formula", 300.0, 70.0, 13.0, "C(3,2) = 3 ✓", G));
        }
        f
    };
    let decide = Frame::new()
        .with(pill_hs("what", 180.0, 22.0, 220.0, 22.0, "что считаем?", G, 10.5))
        .with(arrow("to-sum", 180.0, 34.0, 60.0, 62.0).tone(Y))
        .with(arrow("to-prod", 180.0, 34.0, 180.0, 62.0).tone(G))
        .with(arrow("to-pick", 180.0, 34.0, 300.0, 62.0).tone(B))
        .with(pill_hs("k-sum", 60.0, 76.0, 96.0, 30.0, "сумма", Y, 10.0))
        .with(pill_hs("k-prod", 180.0, 76.0, 96.0, 30.0, "произведение", G, 10.0))
        .with(pill_hs("k-pick", 300.0, 76.0, 96.0, 30.0, "выбор k из n", B, 10.0))
        .with(arrow("to-order", 300.0, 92.0, 256.0, 122.0).tone(B))
        .with(arrow("to-free", 300.0, 92.0, 344.0, 122.0).tone(B))
        .with(pill_hs("k-order", 250.0, 134.0, 96.0, 24.0, "порядок → A, n!", Y, 9.0))
        .with(pill_hs("k-free", 344.0, 134.0, 30.0, 24.0, "C", G, 11.0));
    SceneSpec::new(
        &["Ошибка", "Пример", "Проверка", "Классификация"],
        &[
            "Главная ошибка новичка — двойной счёт: порядок учтён там, где его нет",
            "Лекарство: возьмите крошечный пример — три друга, выбрать двоих",
            "Руками получается три пары, и C(3, 2) = 3 — формулы сходятся",
            "Перед расчётом классифицируйте задачу — половина решения уже готова",
        ],
        frames(vec![dup, trio(false), trio(true), decide]),
    )
    .cues(&[6.6, 10.4, 19.0])
    .step_ms(3000)
}

// --- 12. Сцепки глав -----------------------------------------------------------------------------

fn links() -> SceneSpec {
    let subs = ["ab", "ac", "ad", "bc", "bd", "cd"];
    let subsets = {
        let mut f = Frame::new().with(pill("all", 180.0, 28.0, 120.0, "{a, b, c, d}", G));
        for (i, t) in subs.iter().enumerate() {
            let x = 52.0 + i as f64 * 51.2;
            let mut ch = t.chars();
            let label = format!("{{{},{}}}", ch.next().unwrap_or(' '), ch.next().unwrap_or(' '));
            f = f.with(arrow(&format!("sub-ar{i}"), 180.0, 40.0, x, 72.0).opacity(0.5)).with(pill_hs(&format!("sub{i}"), x, 84.0, 44.0, 20.0, &label, B, 9.5));
        }
        f.with(monoc("sub-sum", 180.0, 132.0, 13.0, "C(4, 2) = 6 подмножеств размера 2", G))
    };
    let product = {
        let mut f = Frame::new();
        for r in 0..3 {
            for c in 0..2 {
                f = f.with(panel(&format!("ab{r}{c}"), 144.0 + c as f64 * 56.0, 44.0 + r as f64 * 30.0, 48.0, 24.0, G));
            }
        }
        f.with(cap("ab-top", 180.0, 22.0, "A × B (глава 2)").size(9.5)).with(monoc("ab-sum", 180.0, 140.0, 13.0, "|A × B| = |A| · |B| = 3 · 2 = 6", G))
    };
    let pascal = {
        let mut f = Frame::new();
        for (r, n) in [1usize, 2, 3, 4, 5].iter().enumerate() {
            let row = pascal_row(n - 1);
            for (c, v) in row.iter().enumerate() {
                let x = 180.0 + (c as f64 - (*n as f64 - 1.0) / 2.0) * 38.0;
                f = f.with(dot(format!("pa{r}{c}"), x, 26.0 + r as f64 * 28.0, v.to_string()).r(12.0).tone(Y));
            }
        }
        f.with(cap("pa-note", 320.0, 86.0, "C(n, k)").size(9.5).anchor(Anchor::End))
    };
    let chain = {
        let mut f = Frame::new();
        for (i, t) in ["множества", "отношения", "комбинаторика", "Паскаль"].iter().enumerate() {
            f = f.with(pill_hs(&format!("ch{i}"), 52.0 + i as f64 * 86.0, 84.0, 78.0, 20.0, t, if i < 3 { G } else { Y }, 9.0));
            if i < 3 {
                f = f.with(arrow(&format!("ch-ar{i}"), 92.0 + i as f64 * 86.0, 84.0, 98.0 + i as f64 * 86.0, 84.0).tone(G));
            }
        }
        f.with(cap("ch-note", 180.0, 130.0, "каждый шаг опирается на предыдущие"))
    };
    SceneSpec::new(
        &["Сцепки", "Подмножества", "Произведение", "Паскаль", "Цепочка"],
        &[
            "Заметьте, как главы сцепляются",
            "Сочетание — подмножество размера k из множества размера n: комбинаторика выросла из множеств",
            "Правило произведения — прямое произведение из второй главы, посчитанное по числу элементов",
            "Перестановки и сочетания встретятся в следующей главе: из них сложится треугольник Паскаля",
            "Каждый новый инструмент переиспользует старые — в этом ценность дискретной математики",
        ],
        frames(vec![Frame::new().with(monoc("title", 180.0, 86.0, 20.0, "главы сцепляются", G)), subsets, product, pascal, chain]),
    )
    .cues(&[2.4, 9.9, 15.8, 22.7])
    .step_ms(3000)
}

/// Строка треугольника Паскаля с номером `n` (с нуля).
fn pascal_row(n: usize) -> Vec<u64> {
    let mut row = vec![1u64];
    for k in 0..n {
        let next = row[k] * (n - k) as u64 / (k as u64 + 1);
        row.push(next);
    }
    row
}

// --- 13. Итог ------------------------------------------------------------------------------------

fn recap() -> SceneSpec {
    // (символ, название, шаг, на котором карточка выступает)
    let cards: [(&str, &str, usize); 5] = [("+  ×", "правила", 1), ("n!", "перестановки", 2), ("A", "размещения", 2), ("C", "сочетания", 2), ("C(n,2)", "пары", 2)];
    let at = |step: usize| {
        let mut f = Frame::new();
        for (i, &(sym, name, when)) in cards.iter().enumerate() {
            let (on, done) = (step == when, step > when);
            let x = 40.0 + i as f64 * 70.0;
            let s = if on { 1.1 } else { 1.0 };
            f = f
                .with(panel(&format!("card{i}"), x, 52.0, 62.0, 68.0, if on || done { G } else { M }).scale(s))
                .with(monoc(&format!("card-s{i}"), x, 58.0, 14.0, sym, G).scale(s))
                .with(cap(&format!("card-n{i}"), x, 76.0, name).size(9.0).scale(s));
        }
        if step >= 3 {
            for (i, t) in ["пароли", "пин-коды", "покер", "рукопожатия"].iter().enumerate() {
                f = f.with(pill_hs(&format!("use{i}"), 50.0 + i as f64 * 87.0, 116.0, 80.0, 20.0, t, Y, 9.5));
            }
        }
        if step >= 4 {
            f = f.with(pill_hs("next", 180.0, 152.0, 280.0, 24.0, "Глава 4 · Паскаль, бином Ньютона, Дирихле →", G, 10.0));
        }
        f
    };
    SceneSpec::new(
        &["Итог", "Правила", "Счётчики", "Применение", "Дальше"],
        &[
            "Подведём итог главы",
            "Два правила — сумма для взаимоисключающих групп и произведение для независимых выборов",
            "Счётчики: n! для перестановок, размещения с порядком, C(n, k) без порядка, C(n, 2) для пар",
            "Применяйте к паролям, пин-кодам, рукам в покере и рукопожатиям — оценивайте перебор до запуска",
            "Дальше — треугольник Паскаля, бином Ньютона и принцип Дирихле",
        ],
        frames((0..5).map(at).collect()),
    )
    .cues(&[1.5, 8.1, 18.3, 24.7])
    .step_ms(2600)
}

// --- проверки ------------------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use content::Scene;

    /// Компоненты из импортов `slides/dm/ch03.tsx` по порядку.
    const COMPONENTS: [&str; 13] =
        ["C3Intro", "C3Sum", "C3Product", "C3Password", "C3Factorial", "C3Perm", "C3Arrange", "C3Combine", "C3Poker", "C3Pairs", "C3Classify", "C3Links", "C3Recap"];

    #[test]
    fn names_match_the_old_components_in_order() {
        let names: Vec<_> = scenes().iter().map(|(n, _)| *n).collect();
        assert_eq!(names, COMPONENTS);
    }

    #[test]
    fn every_scene_compiles_and_fits() {
        for (name, spec) in scenes() {
            let scene = Scene::compile(&spec).unwrap_or_else(|e| panic!("{name}: {e}"));
            let lint = scene.lint();
            assert!(lint.is_empty(), "{name}: {lint:#?}");
        }
    }

    #[test]
    fn steps_labels_captions_and_cues_agree() {
        for (name, spec) in scenes() {
            let n = spec.frames.len();
            assert_eq!(spec.labels.len(), n, "{name}: названия шагов");
            assert_eq!(spec.captions.len(), n, "{name}: подписи");
            let cues = spec.cues.as_ref().unwrap_or_else(|| panic!("{name}: нет cues"));
            assert_eq!(cues.len(), n - 1, "{name}: меток шагов");
            assert!(cues.windows(2).all(|w| w[0] < w[1]) && cues[0] > 0.0, "{name}: метки не возрастают");
        }
    }

    #[test]
    fn helpers_are_right() {
        assert_eq!(group(1_302_540), "1 302 540");
        assert_eq!(group(624), "624");
        assert_eq!(group(4), "4");
        assert_eq!(pascal_row(4), vec![1, 4, 6, 4, 1]);
        assert_eq!(all_pairs(5).len(), 10);
    }
}
