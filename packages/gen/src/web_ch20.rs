//! Book 11 "Modern Frontend", chapter 20 "CSS: Grid" (section "CSS and layout"):
//! 13 slides, each with a diagram on the shared DSL. `cues` marks computed by the paragraph's character share (≈14 characters per second, no voice-over).

use content::{
    dsl::{arrow, bx, code, text, zone},
    Block, Chapter, Frame, Lang, SceneSpec, Slide, Tone, B, G, M, R, V, Y,
};

/// Step marks (seconds from the paragraph start) for each of the 13 slides.
const CUES: [&[f64]; 13] = [
    &[10.5, 17.9],
    &[13.4, 23.5, 33.2],
    &[10.6, 15.4, 25.1],
    &[9.1, 16.4, 26.2],
    &[12.4, 20.1, 24.7],
    &[12.4, 21.1, 30.4],
    &[4.5, 18.3, 32.4],
    &[14.2, 20.7, 25.2],
    &[4.1, 10.4, 24.7],
    &[12.6, 16.9, 34.7],
    &[13.2, 17.9, 23.5],
    &[10.8, 19.3, 28.1],
    &[14.8, 19.6, 25.2],
];

/// Chapter as data: `cargo run --bin generate` writes it to `backend/data/slides/11-20.json`.
pub fn chapter() -> Chapter {
    let slides: [(&str, &str, &str, fn() -> SceneSpec); 13] = [
        ("Двумерная раскладка", "Контейнер, дорожки, ячейки", "Грид раскладывает по двум осям сразу: display: grid делает детей элементами сетки.", v01),
        ("Колонки и строки", "grid-template-columns, fr, repeat()", "Размеры дорожек — через пробел; fr делит остаток свободного места.", v02),
        ("Промежутки и неявные дорожки", "gap, grid-auto-rows", "gap — только между дорожками; лишние элементы создают неявные строки.", v03),
        ("Границы дорожек", "minmax(), auto, min-content", "minmax(мин, макс) держит дорожку в границах; minmax(0, 1fr) защищает от распирания.", v04),
        ("Адаптивная сетка без медиа-запросов", "auto-fit и auto-fill", "repeat(auto-fit, minmax(200px, 1fr)) — столько колонок, сколько влезает.", v05),
        ("Размещение по линиям", "grid-column, grid-row, span", "Линии нумеруются с 1, отрицательные — с конца; span задаёт длину.", v06),
        ("Именованные области", "grid-template-areas, grid-area", "Раскладка рисуется словами; области — только прямоугольники.", v07),
        ("Выравнивание", "justify-items, place-items, place-content", "items — внутри ячеек, content — сетка внутри контейнера, self — один элемент.", v08),
        ("Автозаполнение", "grid-auto-flow и dense", "dense затыкает дыры, но порядок на экране расходится с порядком в документе.", v09),
        ("Вложенные сетки", "Сетка в ячейке и subgrid", "Вложенная сетка — со своими дорожками; subgrid берёт дорожки родителя.", v10),
        ("Типичные макеты", "Страница, галерея, карточки", "Два-три свойства — и страница, галерея, карточки; без процентов и расчётов.", v11),
        ("Грид и флексбокс", "Что и когда брать", "Flex — ряд и содержимое ведёт; grid — структура и контейнер ведёт; вместе — лучше всего.", v12),
        ("Отладка и чек-лист", "DevTools и хорошая сетка", "Значок grid в DevTools рисует линии и имена; fr, minmax, gap, auto-fit, области по смыслу.", v13),
    ];
    Chapter {
        book: 11,
        chapter: 20,
        rubric: "СОВРЕМЕННЫЙ FRONTEND / CSS И ВЁРСТКА".into(),
        slides: slides.iter().enumerate().map(|(i, (title, sub, main, scene))| slide(title, sub, main, scene, CUES[i])).collect(),
    }
}

/// Slide with a single diagram: `cues` marks — when steps 2, 3, … begin (seconds from the paragraph start).
fn slide(title: &str, sub: &str, main: &str, scene: &fn() -> SceneSpec, cues: &[f64]) -> Slide {
    Slide { title: title.into(), sub: Some(sub.into()), short: None, main: main.into(), body: vec![Block::Scene(scene().cues(cues))] }
}

// --- scene helpers -----------------------------------------------------------------------------

/// Rectangle with a label: (x, y) — centre.
#[allow(clippy::too_many_arguments)]
fn b(id: &str, x: f64, y: f64, w: f64, h: f64, label: &str, tone: Tone, size: f64) -> content::item::Cell {
    bx(id, x, y, w, h, label).tone(tone).size(size)
}

/// Short label.
fn note(id: &str, x: f64, y: f64, label: &str, size: f64) -> content::item::Text {
    text(id, x, y, label).size(size)
}

/// CSS inset; (x, y) — start of the first line (baseline).
fn css(id: &str, x: f64, y: f64, lines: &[&str]) -> content::item::Code {
    code(Lang::Css, id, x, y, lines)
}

fn spec(labels: &[&str], captions: &[&str], frames: Vec<Frame>) -> SceneSpec {
    SceneSpec::new(labels, captions, frames)
}

/// Grid geometry: left edge, column widths, top, row heights and gaps.
struct Grid {
    x: f64,
    cols: Vec<f64>,
    gx: f64,
    y: f64,
    rows: Vec<f64>,
    gy: f64,
}

impl Grid {
    fn new(x: f64, cols: &[f64], gx: f64, y: f64, rows: &[f64], gy: f64) -> Grid {
        Grid { x, cols: cols.to_vec(), gx, y, rows: rows.to_vec(), gy }
    }

    fn left(&self, c: usize) -> f64 {
        self.x + self.cols[..c].iter().sum::<f64>() + self.gx * c as f64
    }

    fn top(&self, r: usize) -> f64 {
        self.y + self.rows[..r].iter().sum::<f64>() + self.gy * r as f64
    }

    /// Rectangle from column `c0` to `c1` (exclusive) and from row `r0` to `r1`: centre and size.
    fn rect(&self, c0: usize, c1: usize, r0: usize, r1: usize) -> (f64, f64, f64, f64) {
        let (x0, x1) = (self.left(c0), self.left(c1 - 1) + self.cols[c1 - 1]);
        let (y0, y1) = (self.top(r0), self.top(r1 - 1) + self.rows[r1 - 1]);
        ((x0 + x1) / 2.0, (y0 + y1) / 2.0, x1 - x0, y1 - y0)
    }

    /// Vertical line `i` (zero-based): track edge or the middle of a gap.
    fn line_x(&self, i: usize) -> f64 {
        if i == 0 {
            self.x
        } else if i == self.cols.len() {
            self.left(i - 1) + self.cols[i - 1]
        } else {
            self.left(i) - self.gx / 2.0
        }
    }

    /// Horizontal line `i` (zero-based).
    fn line_y(&self, i: usize) -> f64 {
        if i == 0 {
            self.y
        } else if i == self.rows.len() {
            self.top(i - 1) + self.rows[i - 1]
        } else {
            self.top(i) - self.gy / 2.0
        }
    }

    /// Grid item.
    #[allow(clippy::too_many_arguments)]
    fn put(&self, id: &str, c0: usize, c1: usize, r0: usize, r1: usize, label: &str, tone: Tone, size: f64) -> content::item::Cell {
        let (x, y, w, h) = self.rect(c0, c1, r0, r1);
        b(id, x, y, w, h, label, tone, size)
    }

    /// Dashed cell placeholder.
    fn slot(&self, id: &str, c0: usize, c1: usize, r0: usize, r1: usize) -> content::item::Zone {
        let (x, y, w, h) = self.rect(c0, c1, r0, r1);
        zone(id, x, y, w, h).tone(M).dash()
    }
}

// 1. Two-dimensional layout
fn v01() -> SceneSpec {
    let g = Grid::new(69.0, &[70.0, 70.0, 70.0], 6.0, 50.0, &[38.0, 38.0], 6.0);
    let cells = |f: Frame, tones: [Tone; 6]| {
        let mut f = f;
        for i in 0..6 {
            f = f.with(g.put(&format!("g{i}"), i % 3, i % 3 + 1, i / 3, i / 3 + 1, &format!("{}", i + 1), tones[i], 9.5));
        }
        f
    };
    let nums = |f: Frame, hl: Option<(usize, usize)>| {
        let mut f = f;
        for i in 0..4 {
            let t = note(&format!("lx{i}"), g.line_x(i), 44.0, &format!("{}", i + 1), 9.0);
            f = f.with(if hl.is_some() { t.tone(Y) } else { t });
        }
        for i in 0..3 {
            f = f.with(note(&format!("ly{i}"), 56.0, g.line_y(i) + 3.0, &format!("{}", i + 1), 9.0).tone(Y));
        }
        f
    };
    spec(
        &["Одна ось и две", "Контейнер", "Линии и дорожки"],
        &[
            "Флексбокс идёт вдоль одной оси, грид — по двум сразу: по строкам и по колонкам",
            "Контейнеру достаточно display: grid — и его прямые дети становятся элементами сетки",
            "Линии нумеруются с единицы; между соседними линиями — дорожка, на пересечении строки и колонки — ячейка",
        ],
        vec![
            Frame::new()
                .with(b("g0", 31.0, 52.0, 34.0, 30.0, "1", G, 9.0))
                .with(b("g1", 71.0, 52.0, 34.0, 30.0, "2", G, 9.0))
                .with(b("g2", 111.0, 52.0, 34.0, 30.0, "3", G, 9.0))
                .with(b("g3", 151.0, 52.0, 34.0, 30.0, "4", G, 9.0))
                .with(arrow("fa", 14.0, 96.0, 168.0, 96.0).tone(G))
                .with(note("fn", 90.0, 120.0, "flex: одна ось", 10.0).tone(G))
                .with(b("h0", 235.0, 40.0, 40.0, 28.0, "1", B, 9.0))
                .with(b("h1", 281.0, 40.0, 40.0, 28.0, "2", B, 9.0))
                .with(b("h2", 235.0, 74.0, 40.0, 28.0, "3", B, 9.0))
                .with(b("h3", 281.0, 74.0, 40.0, 28.0, "4", B, 9.0))
                .with(arrow("ax", 215.0, 114.0, 301.0, 114.0).tone(B))
                .with(arrow("ay", 330.0, 26.0, 330.0, 90.0).tone(B))
                .with(note("gn", 258.0, 136.0, "grid: две оси", 10.0).tone(B)),
            cells(Frame::new(), [B; 6])
                .with(zone("z", 180.0, 96.0, 262.0, 106.0).tone(G).dash().label("display: grid"))
                .with(note("n", 180.0, 164.0, "прямые дети контейнера — элементы сетки", 10.0)),
            nums(cells(Frame::new(), [B, B, B, B, Y, B]), Some((0, 0)))
                .with(zone("z", 180.0, 96.0, 262.0, 106.0).tone(G).dash())
                .with(note("n", 180.0, 164.0, "линии 1…4 · дорожки между ними · ячейка", 10.0)),
        ],
    )
}

// 2. Columns and rows
fn v02() -> SceneSpec {
    // scale: 200px ≈ 90 canvas units; container 320 units, gap 4
    let g = |w: [f64; 3]| Grid::new(20.0, &w, 4.0, 60.0, &[44.0], 0.0);
    let fixed = [90.0, 45.0, 68.0];
    let fr = [90.0, 74.0, 148.0];
    let eq = [104.0, 104.0, 104.0];
    let boxes = |gr: Grid, labels: [&str; 3], tones: [Tone; 3]| {
        let mut f = Frame::new();
        for i in 0..3 {
            f = f.with(gr.put(&format!("c{i}"), i, i + 1, 0, 1, labels[i], tones[i], 9.5));
        }
        f
    };
    let lines = |l: &[&str]| css("k", 14.0, 20.0, l).size(9.5).lh(13.0).w(250.0);
    spec(
        &["Размеры в px", "Свободное место", "Доли fr", "repeat()"],
        &[
            "Колонки и строки задаются списком размеров через пробел: пиксели, проценты и особая единица fr",
            "Фиксированные размеры и промежутки вычитаются, остаётся свободное место",
            "Остаток делится по долям: 1fr и 2fr — получается вторая колонка вдвое шире первой",
            "Одинаковые дорожки записывают функцией repeat: repeat(3, 1fr) — три равные колонки",
        ],
        vec![
            boxes(g(fixed), ["200px", "100px", "150px"], [B, B, B]).with(lines(&["grid-template-columns:", "  200px 100px 150px;"]).hl([1])).with(note("n", 180.0, 150.0, "фиксированные дорожки: ширина не меняется", 10.0))
                .with(zone("zc", 180.0, 82.0, 328.0, 56.0).tone(M).dash()),
            Frame::new()
                .with(Grid::new(20.0, &[90.0, 222.0], 4.0, 60.0, &[44.0], 0.0).put("c0", 0, 1, 0, 1, "200px", B, 9.5))
                .with(Grid::new(20.0, &[90.0, 222.0], 4.0, 60.0, &[44.0], 0.0).put("c1", 1, 2, 0, 1, "свободное место", M, 9.5).dash())
                .with(lines(&["grid-template-columns:", "  200px 1fr 2fr;"]).hl([1]))
                .with(note("n", 180.0, 150.0, "ширина контейнера − 200px − промежутки = остаток", 10.0))
                .with(zone("zc", 180.0, 82.0, 328.0, 56.0).tone(M).dash()),
            boxes(g(fr), ["200px", "1fr", "2fr"], [B, G, G])
                .with(lines(&["grid-template-columns:", "  200px 1fr 2fr;"]).hl([1]))
                .with(note("n", 180.0, 150.0, "остаток делится 1 : 2", 10.0))
                .with(zone("zc", 180.0, 82.0, 328.0, 56.0).tone(M).dash()),
            boxes(g(eq), ["1fr", "1fr", "1fr"], [G, G, G])
                .with(lines(&["grid-template-columns:", "  repeat(3, 1fr);"]).hl([1]))
                .with(note("n", 180.0, 150.0, "три равные колонки", 10.0))
                .with(zone("zc", 180.0, 82.0, 328.0, 56.0).tone(M).dash()),
        ],
    )
}

// 3. Gaps and implicit tracks
fn v03() -> SceneSpec {
    let cells = |g: &Grid, tones: [Tone; 6], dash_second: bool| {
        let mut f = Frame::new();
        for i in 0..6 {
            let mut c = g.put(&format!("a{i}"), i % 3, i % 3 + 1, i / 3, i / 3 + 1, &format!("{}", i + 1), tones[i], 9.5);
            if dash_second && i >= 3 {
                c = c.dash();
            }
            f = f.with(c);
        }
        f
    };
    let g1 = Grid::new(36.0, &[80.0; 3], 24.0, 34.0, &[30.0, 30.0], 8.0);
    let g3 = Grid::new(46.0, &[80.0; 3], 14.0, 34.0, &[30.0, 22.0], 14.0);
    let g4 = Grid::new(46.0, &[80.0; 3], 14.0, 34.0, &[30.0, 46.0], 14.0);
    spec(
        &["Два промежутка", "Только между", "Неявные строки", "grid-auto-rows"],
        &[
            "gap: одно значение на всё или два — сначала между строками, потом между колонками",
            "Полей по краям gap не добавляет — только промежутки между соседями",
            "Элементов больше, чем ячеек в явной сетке: браузер достраивает неявные строки, их высота — по содержимому",
            "grid-auto-rows задаёт размер неявных строк — например, каждая новая 46px",
        ],
        vec![
            cells(&g1, [B; 6], false)
                .with(arrow("ga", 116.0, 49.0, 140.0, 49.0).tone(Y))
                .with(arrow("gb", 76.0, 64.0, 76.0, 72.0).tone(Y))
                .with(note("n", 180.0, 128.0, "gap: 8px 24px — между строками 8, между колонками 24", 10.0)),
            cells(&g1, [B; 6], false)
                .with(zone("zc", 180.0, 68.0, 292.0, 72.0).tone(G).dash())
                .with(note("n", 180.0, 128.0, "рамка вокруг сетки: по краям промежутков нет", 10.0)),
            cells(&g3, [B, B, B, Y, Y, Y], true)
                .with(note("n1", 180.0, 120.0, "явная строка: grid-template-rows: 30px", 10.0).tone(B))
                .with(note("n2", 180.0, 138.0, "неявная строка: высота по содержимому", 10.0).tone(Y)),
            cells(&g4, [B, B, B, Y, Y, Y], true)
                .with(note("n1", 180.0, 136.0, "grid-auto-rows: 46px", 10.0).tone(Y))
                .with(note("n2", 180.0, 154.0, "сетка растёт вместе с данными", 10.0)),
        ],
    )
}

// 4. Track boundaries
fn v04() -> SceneSpec {
    spec(
        &["minmax", "Не меньше минимума", "Ключевые слова", "Ловушка 1fr"],
        &[
            "minmax(мин, макс): колонка растёт от минимума до максимума, когда есть место",
            "Контейнер уже минимума — колонка остаётся шириной в минимум и выходит за край",
            "auto, min-content и max-content: по содержимому, самое узкое и самое широкое",
            "1fr не бывает меньше содержимого: длинное слово распирает колонку; minmax(0, 1fr) держит колонки равными",
        ],
        vec![
            Frame::new()
                .with(zone("z", 180.0, 70.0, 324.0, 56.0).tone(B).dash())
                .with(b("t1", 180.0, 70.0, 308.0, 36.0, "minmax(200px, 1fr)", G, 9.5))
                .with(note("n", 180.0, 124.0, "места много: колонка растёт до 1fr", 10.0)),
            Frame::new()
                .with(zone("z", 180.0, 70.0, 140.0, 56.0).tone(B).dash())
                .with(b("t1", 180.0, 70.0, 170.0, 36.0, "min 200px", R, 9.5))
                .with(note("n", 180.0, 124.0, "дальше минимума не сжимается — выйдет за рамку", 10.0)),
            Frame::new()
                .with(b("k0", 64.0, 60.0, 100.0, 30.0, "auto", B, 9.5).under("растягивается"))
                .with(b("k1", 160.0, 60.0, 76.0, 30.0, "min-content", G, 9.0).under("самое узкое"))
                .with(b("k2", 280.0, 60.0, 130.0, 30.0, "max-content", Y, 9.5).under("самое широкое"))
                .with(note("n", 180.0, 128.0, "размер дорожки по содержимому", 10.0)),
            Frame::new()
                .with(b("t1", 118.0, 40.0, 196.0, 28.0, "длинное_слово_внутри", R, 9.0))
                .with(b("t2", 281.0, 40.0, 100.0, 28.0, "1fr", R, 9.0))
                .with(note("n1", 180.0, 70.0, "1fr: слово распёрло колонку — доли не равны", 10.0).tone(R))
                .with(b("u1", 98.0, 108.0, 156.0, 28.0, "minmax(0, 1fr)", G, 9.0))
                .with(b("u2", 262.0, 108.0, 156.0, 28.0, "minmax(0, 1fr)", G, 9.0))
                .with(note("n2", 180.0, 138.0, "колонки равны, слово можно перенести или обрезать", 10.0).tone(G)),
        ],
    )
}

// 5. Responsive grid without media queries
fn v05() -> SceneSpec {
    let lines = || css("k", 14.0, 18.0, &["grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));"]).size(8.5).w(332.0);
    let items = |g: &Grid, n: usize| {
        let mut f = Frame::new();
        let per = g.cols.len();
        for i in 0..n {
            f = f.with(g.put(&format!("b{i}"), i % per, i % per + 1, i / per, i / per + 1, &format!("{}", i + 1), B, 9.0));
        }
        f
    };
    let wide = Grid::new(15.0, &[62.8; 5], 4.0, 46.0, &[26.0], 4.0);
    let mid = Grid::new(75.0, &[67.3; 3], 4.0, 46.0, &[26.0, 26.0], 4.0);
    let narrow = Grid::new(126.0, &[108.0], 4.0, 46.0, &[18.0; 5], 4.0);
    let fill = Grid::new(15.0, &[62.8; 5], 4.0, 50.0, &[22.0], 0.0);
    let fit = Grid::new(15.0, &[106.0; 3], 6.0, 112.0, &[22.0], 0.0);
    spec(
        &["Широкое окно", "Среднее", "Узкое", "fill и fit"],
        &[
            "repeat(auto-fit, minmax(200px, 1fr)): широкое окно — все пять колонок в одной строке",
            "Браузер сам считает, сколько колонок по минимуму помещается, и растягивает их на всю ширину",
            "На телефоне остаётся одна колонка — и ни одного медиа-запроса",
            "auto-fill сохраняет пустые дорожки, auto-fit схлопывает их и растягивает остальные",
        ],
        vec![
            items(&wide, 5).with(lines()).with(zone("z", 180.0, 59.0, 340.0, 36.0).tone(M).dash()).with(note("n", 180.0, 34.0, "1100px → 5 колонок", 10.0)),
            items(&mid, 5).with(lines()).with(zone("z", 180.0, 74.0, 218.0, 66.0).tone(M).dash()).with(note("n", 180.0, 34.0, "700px → 3 колонки", 10.0)),
            items(&narrow, 5).with(lines()).with(zone("z", 180.0, 99.0, 116.0, 114.0).tone(M).dash()).with(note("n", 180.0, 34.0, "360px → 1 колонка", 10.0)),
            Frame::new()
                .with(lines())
                .with(fill.put("b0", 0, 1, 0, 1, "1", G, 9.0))
                .with(fill.put("b1", 1, 2, 0, 1, "2", G, 9.0))
                .with(fill.put("b2", 2, 3, 0, 1, "3", G, 9.0))
                .with(fill.put("b3", 3, 4, 0, 1, "", M, 9.0).dash())
                .with(fill.put("b4", 4, 5, 0, 1, "", M, 9.0).dash())
                .with(note("n", 180.0, 42.0, "auto-fill: пустые дорожки остаются", 10.0))
                .with(fit.put("f0", 0, 1, 0, 1, "1", G, 9.0))
                .with(fit.put("f1", 1, 2, 0, 1, "2", G, 9.0))
                .with(fit.put("f2", 2, 3, 0, 1, "3", G, 9.0))
                .with(note("n2", 180.0, 104.0, "auto-fit: пустые схлопнуты, остальные шире", 10.0)),
        ],
    )
}

// 6. Placement by lines
fn v06() -> SceneSpec {
    let g = Grid::new(54.0, &[80.0; 3], 6.0, 44.0, &[44.0, 44.0], 6.0);
    let frame = |item: (usize, usize, usize, usize), label: &str, top: &[usize], left: &[usize], neg: bool, neg_hl: &[usize], caption: &str| {
        let mut f = Frame::new();
        for i in 0..6 {
            f = f.with(g.slot(&format!("s{i}"), i % 3, i % 3 + 1, i / 3, i / 3 + 1));
        }
        f = f.with(g.put("it", item.0, item.1, item.2, item.3, label, G, 10.0));
        for i in 0..4 {
            let t = note(&format!("lx{i}"), g.line_x(i), 36.0, &format!("{}", i + 1), 9.0);
            f = f.with(if top.contains(&i) { t.tone(Y) } else { t });
        }
        for i in 0..3 {
            let t = note(&format!("ly{i}"), 40.0, g.line_y(i) + 3.0, &format!("{}", i + 1), 9.0);
            f = f.with(if left.contains(&i) { t.tone(Y) } else { t });
        }
        if neg {
            for i in 0..4 {
                let t = note(&format!("nx{i}"), g.line_x(i), 152.0, &format!("{}", i as i32 - 4), 9.0);
                f = f.with(if neg_hl.contains(&i) { t.tone(Y) } else { t });
            }
        }
        f.with(note("cap", 180.0, 166.0, caption, 10.0))
    };
    spec(
        &["От линии до линии", "span", "Минус первая", "Строки"],
        &[
            "grid-column: 1 / 3 — от первой линии до третьей, то есть две колонки",
            "Вместо конечной линии — span: 2 / span 2 начинается на второй линии и занимает две колонки",
            "Отрицательные номера идут с конца: 1 / -1 — на всю строку, сколько бы ни было колонок",
            "Для строк то же самое делает grid-row: span 2 — элемент в две строки высотой",
        ],
        vec![
            frame((0, 2, 0, 1), "A", &[0, 2], &[], false, &[], "grid-column: 1 / 3"),
            frame((1, 3, 0, 1), "A", &[1, 3], &[], false, &[], "grid-column: 2 / span 2"),
            frame((0, 3, 1, 2), "A", &[0], &[], true, &[3], "grid-column: 1 / -1"),
            frame((2, 3, 0, 2), "A", &[], &[0, 2], true, &[], "grid-row: span 2"),
        ],
    )
}

// 7. Named areas
fn v07() -> SceneSpec {
    let g = Grid::new(150.0, &[60.0, 134.0], 4.0, 26.0, &[26.0, 70.0, 22.0], 4.0);
    let page = |hl_header: bool| {
        let o = |on: bool| if on { 1.0 } else { 0.35 };
        Frame::new()
            .with(g.put("hd", 0, 2, 0, 1, "header", B, 9.5))
            .with(g.put("nv", 0, 1, 1, 2, "nav", G, 9.5).opacity(o(!hl_header)))
            .with(g.put("mn", 1, 2, 1, 2, "main", Y, 9.5).opacity(o(!hl_header)))
            .with(g.put("ft", 0, 2, 2, 3, "footer", V, 9.5).opacity(o(!hl_header)))
    };
    let areas = || css("c", 8.0, 30.0, &["grid-template-areas:", "  \"header header\"", "  \"nav    main\"", "  \"footer footer\";"]).size(8.5).lh(13.0).w(130.0);
    let l2 = Grid::new(180.0, &[70.0, 70.0], 4.0, 40.0, &[40.0, 40.0], 4.0);
    spec(
        &["Имена областей", "Одинаковые имена", "grid-area", "Только прямоугольники"],
        &[
            "grid-template-areas рисует сетку словами: каждая строка в кавычках, имя — на ячейку",
            "Одинаковые имена подряд склеиваются в одну область — шапка занимает обе колонки",
            "Элементу достаточно назвать область: grid-area: header",
            "Область должна быть прямоугольником — Г-образная запись недействительна",
        ],
        vec![
            page(false).with(areas()).with(note("n", 180.0, 164.0, "раскладка читается как набросок на бумаге", 10.0)),
            page(true).with(areas().hl([1])).with(note("n", 180.0, 164.0, "две «header» подряд — одна область на две колонки", 10.0)),
            page(false)
                .with(css("c", 8.0, 44.0, &[".top {", "  grid-area: header;", "}"]).size(9.0).lh(14.0).w(130.0))
                .with(arrow("a", 128.0, 56.0, 148.0, 40.0).tone(B))
                .with(note("n", 180.0, 164.0, "каждый элемент называет свою область", 10.0)),
            Frame::new()
                .with(css("c", 8.0, 44.0, &["grid-template-areas:", "  \"a a\"", "  \"a b\";"]).size(9.0).lh(14.0).w(130.0))
                .with(l2.put("e0", 0, 1, 0, 1, "a", R, 9.5))
                .with(l2.put("e1", 1, 2, 0, 1, "a", R, 9.5))
                .with(l2.put("e2", 0, 1, 1, 2, "a", R, 9.5))
                .with(l2.put("e3", 1, 2, 1, 2, "b", G, 9.5))
                .with(note("n", 180.0, 164.0, "Г-образная область: правило отбрасывается", 10.0).tone(R)),
        ],
    )
}

// 8. Alignment
fn v08() -> SceneSpec {
    let g = Grid::new(30.0, &[96.0; 3], 8.0, 34.0, &[84.0], 0.0);
    let slots = |f: Frame| {
        let mut f = f;
        for i in 0..3 {
            f = f.with(g.slot(&format!("sl{i}"), i, i + 1, 0, 1));
        }
        f
    };
    // position of a 28×18 box in a cell: start / center / end
    let pos = |i: usize, kind: usize| {
        let (x, y, w, h) = g.rect(i, i + 1, 0, 1);
        match kind {
            0 => (x - w / 2.0 + 17.0, y - h / 2.0 + 12.0),
            1 => (x, y),
            _ => (x + w / 2.0 - 17.0, y + h / 2.0 - 12.0),
        }
    };
    let item = |i: usize, kind: usize, tone: Tone| {
        let (x, y) = pos(i, kind);
        b(&format!("it{i}"), x, y, 28.0, 18.0, "", tone, 9.0)
    };
    let contain = |xs: [f64; 3]| {
        let mut f = Frame::new().with(zone("ct", 180.0, 80.0, 330.0, 100.0).tone(B).dash());
        for (i, x) in xs.iter().enumerate() {
            f = f.with(b(&format!("it{i}"), *x, 80.0, 60.0, 84.0, &format!("{}", i + 1), G, 9.5));
        }
        f
    };
    spec(
        &["Внутри ячейки", "place-items", "Один элемент", "Сетка в контейнере"],
        &[
            "justify-items — по горизонтали внутри ячейки, align-items — по вертикали: start, center, end",
            "place-items: center — оба выравнивания сразу, элемент точно в середине ячейки",
            "Одному элементу — align-self и justify-self: только он уходит в угол",
            "Если дорожки заняли не всё место, сетку двигают justify-content, align-content и place-content",
        ],
        vec![
            slots(Frame::new())
                .with(item(0, 0, G))
                .with(item(1, 1, G))
                .with(item(2, 2, G))
                .with(note("t0", g.rect(0, 1, 0, 1).0, 134.0, "start", 10.0))
                .with(note("t1", g.rect(1, 2, 0, 1).0, 134.0, "center", 10.0))
                .with(note("t2", g.rect(2, 3, 0, 1).0, 134.0, "end", 10.0))
                .with(note("n", 180.0, 158.0, "justify-items: по горизонтали · align-items: по вертикали", 10.0)),
            slots(Frame::new()).with(item(0, 1, G)).with(item(1, 1, G)).with(item(2, 1, G)).with(note("n", 180.0, 140.0, "place-items: center", 11.0)),
            slots(Frame::new()).with(item(0, 1, G)).with(item(1, 2, Y)).with(item(2, 1, G)).with(note("n", 180.0, 140.0, "align-self: end + justify-self: end — только у среднего", 10.0)),
            contain([54.0, 120.0, 186.0]).with(note("n", 180.0, 148.0, "justify-content: start — дорожки уже контейнера", 10.0)),
        ],
    )
}

// 9. Auto-fill
fn v09() -> SceneSpec {
    let g = Grid::new(69.0, &[70.0; 3], 6.0, 28.0, &[30.0; 3], 6.0);
    let hole = || zone("hole", g.rect(2, 3, 0, 1).0, g.rect(2, 3, 0, 1).1, 70.0, 30.0).tone(R).dash();
    let (a, bb, c, d) = ("A", "B", "C", "D");
    spec(
        &["По умолчанию", "Колонками", "dense", "Порядок"],
        &[
            "По умолчанию строка за строкой: широкий B не влез и ушёл вниз — в первой строке дыра",
            "grid-auto-flow: column — сначала заполняется колонка сверху вниз",
            "dense — плотная упаковка: C берёт дыру, а D идёт следом",
            "Порядок на экране A C B D, в документе A B C D: клавиатура идёт по документу",
        ],
        vec![
            Frame::new()
                .with(g.put("a", 0, 2, 0, 1, a, B, 10.0))
                .with(g.put("b", 0, 2, 1, 2, bb, G, 10.0))
                .with(g.put("c", 2, 3, 1, 2, c, Y, 10.0))
                .with(g.put("d", 0, 1, 2, 3, d, V, 10.0))
                .with(hole())
                .with(note("n", 180.0, 156.0, "в первой строке осталась дыра", 10.0).tone(R)),
            Frame::new()
                .with(g.put("a", 0, 1, 0, 1, a, B, 10.0))
                .with(g.put("b", 0, 1, 1, 2, bb, G, 10.0))
                .with(g.put("c", 1, 2, 0, 1, c, Y, 10.0))
                .with(g.put("d", 1, 2, 1, 2, d, V, 10.0))
                .with(note("n", 180.0, 156.0, "grid-auto-flow: column", 10.0)),
            Frame::new()
                .with(g.put("a", 0, 2, 0, 1, a, B, 10.0))
                .with(g.put("b", 0, 2, 1, 2, bb, G, 10.0))
                .with(g.put("c", 2, 3, 0, 1, c, Y, 10.0))
                .with(g.put("d", 2, 3, 1, 2, d, V, 10.0))
                .with(note("n", 180.0, 156.0, "grid-auto-flow: row dense — дыра заполнена", 10.0).tone(G)),
            Frame::new()
                .with(g.put("a", 0, 2, 0, 1, a, B, 10.0))
                .with(g.put("b", 0, 2, 1, 2, bb, G, 10.0))
                .with(g.put("c", 2, 3, 0, 1, c, R, 10.0))
                .with(g.put("d", 2, 3, 1, 2, d, V, 10.0))
                .with(note("n", 180.0, 148.0, "в документе: A → B → C → D", 10.0))
                .with(note("n2", 180.0, 164.0, "на экране: A → C → B → D", 10.0).tone(R)),
        ],
    )
}

// 10. Nested grids
fn v10() -> SceneSpec {
    let outer = Grid::new(24.0, &[90.0, 150.0, 70.0], 6.0, 36.0, &[100.0], 0.0);
    let inner = Grid::new(132.0, &[60.0, 60.0], 6.0, 50.0, &[34.0, 34.0], 6.0);
    let card_x = [76.0, 180.0, 284.0];
    let text_h = [44.0, 26.0, 14.0];
    let cards = |aligned: bool| {
        let mut f = Frame::new();
        for i in 0..3 {
            f = f.with(zone(&format!("k{i}"), card_x[i], 82.0, 96.0, 108.0).tone(B));
            f = f.with(b(&format!("ti{i}"), card_x[i], 43.0, 84.0, 18.0, "заголовок", G, 8.5));
            let th = if aligned { 44.0 } else { text_h[i] };
            f = f.with(b(&format!("tx{i}"), card_x[i], 56.0 + th / 2.0, 84.0, th, "текст", M, 8.5));
            let by = if aligned { 114.0 } else { 56.0 + text_h[i] + 14.0 };
            f = f.with(b(&format!("bt{i}"), card_x[i], by, 60.0, 18.0, "кнопка", if aligned { G } else { R }, 8.5));
        }
        f
    };
    spec(
        &["Сетка в ячейке", "Не по общим линиям", "subgrid", "Код"],
        &[
            "Элемент сетки сам может быть сеткой — со своими дорожками внутри своей ячейки",
            "У каждой карточки своя раскладка: тексты разной длины, и кнопки оказались на разной высоте",
            "subgrid: карточки берут строки родителя — заголовки, тексты и кнопки лежат на общих линиях",
            "Карточка занимает три строки родителя и берёт их себе: grid-template-rows: subgrid",
        ],
        vec![
            Frame::new()
                .with(outer.put("o0", 0, 1, 0, 1, "1", G, 9.5))
                .with(zone("o1", 195.0, 86.0, 150.0, 100.0).tone(B).label("ячейка"))
                .with(inner.put("m0", 0, 1, 0, 1, "", V, 9.0))
                .with(inner.put("m1", 1, 2, 0, 1, "", V, 9.0))
                .with(inner.put("m2", 0, 1, 1, 2, "", V, 9.0))
                .with(inner.put("m3", 1, 2, 1, 2, "", V, 9.0))
                .with(outer.put("o2", 2, 3, 0, 1, "3", G, 9.5))
                .with(note("n", 180.0, 24.0, "внешняя сетка: три колонки", 10.0))
                .with(note("n2", 180.0, 158.0, "внутри ячейки — своя сетка 2×2", 10.0)),
            cards(false).with(note("n", 180.0, 156.0, "кнопки на разной высоте", 10.0).tone(R)),
            cards(true).with(note("n", 180.0, 156.0, "subgrid: общие строки, кнопки на одной линии", 10.0).tone(G)),
            Frame::new()
                .with(css("c", 100.0, 46.0, &[".card {", "  display: grid;", "  grid-row: span 3;", "  grid-template-rows: subgrid;", "}"]).size(10.5).lh(18.0).w(220.0).hl([3]))
                .with(note("n", 180.0, 156.0, "родитель задаёт строки — карточка берёт их себе", 10.0)),
        ],
    )
}

// 11. Typical layouts
fn v11() -> SceneSpec {
    let page = Grid::new(20.0, &[70.0, 246.0], 4.0, 22.0, &[24.0, 78.0, 20.0], 4.0);
    let gal = Grid::new(20.0, &[74.0; 4], 6.0, 34.0, &[34.0, 34.0], 6.0);
    let cards = Grid::new(20.0, &[100.0; 3], 10.0, 126.0, &[34.0], 0.0);
    spec(
        &["Страница", "Узкий экран", "Галерея и карточки", "Код"],
        &[
            "Страница: меню фиксированной ширины, резиновое содержимое, шапка и подвал на обе колонки",
            "На узком экране внутри медиа-запроса колонки превращаются в одну",
            "Галерея и карточки — адаптивная сетка; плитка может занять несколько ячеек",
            "Страница — одна декларация сетки: ни процентов, ни расчётов",
        ],
        vec![
            Frame::new()
                .with(page.put("hd", 0, 2, 0, 1, "header", B, 9.5))
                .with(page.put("nv", 0, 1, 1, 2, "nav", G, 9.5))
                .with(page.put("mn", 1, 2, 1, 2, "main", Y, 9.5))
                .with(page.put("ft", 0, 2, 2, 3, "footer", V, 9.5))
                .with(note("n", 180.0, 166.0, "колонки: 200px 1fr · строки: auto 1fr auto", 10.0)),
            Frame::new()
                .with(zone("ph", 180.0, 86.0, 132.0, 138.0).tone(M).dash())
                .with(b("hd", 180.0, 34.0, 118.0, 22.0, "header", B, 9.5))
                .with(b("nv", 180.0, 58.0, 118.0, 20.0, "nav", G, 9.5))
                .with(b("mn", 180.0, 100.0, 118.0, 56.0, "main", Y, 9.5))
                .with(b("ft", 180.0, 142.0, 118.0, 20.0, "footer", V, 9.5))
                .with(note("n", 180.0, 166.0, "@media: одна колонка, элементы друг под другом", 10.0)),
            Frame::new()
                .with(gal.put("hd", 0, 2, 0, 2, "плитка 2×2", B, 9.5))
                .with(gal.put("nv", 2, 3, 0, 1, "2", G, 9.5))
                .with(gal.put("mn", 3, 4, 0, 1, "3", Y, 9.5))
                .with(gal.put("ft", 2, 4, 1, 2, "широкая", V, 9.5))
                .with(cards.put("c0", 0, 1, 0, 1, "карточка", G, 9.0))
                .with(cards.put("c1", 1, 2, 0, 1, "карточка", B, 9.0))
                .with(cards.put("c2", 2, 3, 0, 1, "карточка", Y, 9.0))
                .with(note("n", 180.0, 119.0, "галерея и ряд карточек — repeat(auto-fit, minmax(…, 1fr))", 9.0)),
            Frame::new()
                .with(css("c", 40.0, 50.0, &[".page {", "  display: grid;", "  grid-template-columns: 200px 1fr;", "  gap: 16px;", "}"]).size(11.0).lh(18.0).w(280.0))
                .with(note("n", 180.0, 156.0, "дорожки описаны — раскладку считает браузер", 10.0)),
        ],
    )
}

// 12. Grid and flexbox
fn v12() -> SceneSpec {
    let g = Grid::new(76.0, &[100.0, 100.0], 8.0, 36.0, &[32.0, 32.0], 8.0);
    let labels = ["Главная", "Каталог", "О компании", "Вход"];
    spec(
        &["Flex: ряд", "Grid: сетка", "Вместе", "Выбор"],
        &[
            "Флексбокс: ось одна, ширину элементов определяет содержимое — меню, кнопки, панели",
            "Грид: колонки и строки общие для всех элементов, их размеры задаёт контейнер",
            "Грид строит каркас страницы, флексбокс выстраивает ряд внутри шапки",
            "Выбирайте тот способ, который проще читается: часто подходят оба",
        ],
        vec![
            Frame::new()
                .with(b("m0", 74.0, 70.0, 60.0, 30.0, labels[0], G, 9.0))
                .with(b("m1", 142.0, 70.0, 60.0, 30.0, labels[1], G, 9.0))
                .with(b("m2", 222.0, 70.0, 84.0, 30.0, labels[2], G, 9.0))
                .with(b("m3", 294.0, 70.0, 44.0, 30.0, labels[3], G, 9.0))
                .with(arrow("ax", 44.0, 108.0, 316.0, 108.0).tone(G))
                .with(note("n", 180.0, 130.0, "flex: ширину определяет содержимое, ось одна", 10.0)),
            Frame::new()
                .with(g.put("m0", 0, 1, 0, 1, labels[0], B, 9.0))
                .with(g.put("m1", 1, 2, 0, 1, labels[1], B, 9.0))
                .with(g.put("m2", 0, 1, 1, 2, labels[2], B, 9.0))
                .with(g.put("m3", 1, 2, 1, 2, labels[3], B, 9.0))
                .with(note("n", 180.0, 130.0, "grid: колонки и строки общие для всех", 10.0)),
            Frame::new()
                .with(zone("hz", 180.0, 40.0, 320.0, 40.0).tone(B).dash())
                .with(b("m0", 80.0, 40.0, 56.0, 20.0, labels[0], V, 8.5))
                .with(b("m1", 146.0, 40.0, 56.0, 20.0, labels[1], V, 8.5))
                .with(b("m2", 218.0, 40.0, 76.0, 20.0, labels[2], V, 8.5))
                .with(b("m3", 282.0, 40.0, 44.0, 20.0, labels[3], V, 8.5))
                .with(b("sd", 55.0, 104.0, 70.0, 72.0, "aside", G, 9.5))
                .with(b("mn", 219.0, 104.0, 242.0, 72.0, "main", Y, 9.5))
                .with(note("n", 180.0, 156.0, "каркас — grid, ряд в шапке — flex", 10.0)),
            Frame::new()
                .with(b("fx", 95.0, 58.0, 150.0, 40.0, "flexbox", G, 11.0))
                .with(note("f1", 95.0, 104.0, "одна ось", 10.0))
                .with(note("f2", 95.0, 120.0, "содержимое ведёт", 10.0))
                .with(note("f3", 95.0, 136.0, "меню, кнопки, панели", 10.0).tone(G))
                .with(b("gd", 265.0, 58.0, 150.0, 40.0, "grid", B, 11.0))
                .with(note("g1", 265.0, 104.0, "две оси", 10.0))
                .with(note("g2", 265.0, 120.0, "контейнер ведёт", 10.0))
                .with(note("g3", 265.0, 136.0, "страница, галерея, форма", 10.0).tone(B)),
        ],
    )
}

// 13. Debugging and checklist
fn v13() -> SceneSpec {
    let ov = Grid::new(196.0, &[50.0, 100.0], 4.0, 34.0, &[20.0, 60.0, 20.0], 4.0);
    let overlay = || {
        let mut f = Frame::new()
            .with(ov.put("ov_h", 0, 2, 0, 1, "header", V, 8.5).dash())
            .with(ov.put("ov_n", 0, 1, 1, 2, "nav", V, 8.5).dash())
            .with(ov.put("ov_m", 1, 2, 1, 2, "main", V, 8.5).dash())
            .with(ov.put("ov_f", 0, 2, 2, 3, "footer", V, 8.5).dash());
        for i in 0..3 {
            f = f.with(note(&format!("lx{i}"), ov.line_x(i), 28.0, &format!("{}", i + 1), 8.5).tone(Y));
        }
        for i in 0..4 {
            f = f.with(note(&format!("ly{i}"), 186.0, ov.line_y(i) + 3.0, &format!("{}", i + 1), 8.5).tone(Y));
        }
        f
    };
    spec(
        &["Значок в DevTools", "Панель раскладки", "Первый пункт", "Остальное"],
        &[
            "Значок grid рядом с элементом: поверх страницы линии, их номера и имена областей",
            "В панели раскладки включаются номера линий, имена областей и размеры дорожек",
            "Дорожки заданы долями и minmax, промежутки — через gap",
            "Адаптивность — auto-fit, области названы по смыслу, порядок в документе совпадает с экраном",
        ],
        vec![
            overlay().with(code(Lang::Html, "tree", 10.0, 40.0, &["<div class=\"page\"> grid", "  <header>", "  <nav>", "  <main>", "  <footer>"]).size(9.0).lh(14.0).w(150.0).hl([0])),
            overlay()
                .with(b("cb0", 90.0, 56.0, 150.0, 22.0, "номера линий", G, 9.0))
                .with(b("cb1", 90.0, 84.0, 150.0, 22.0, "имена областей", G, 9.0))
                .with(b("cb2", 90.0, 112.0, 150.0, 22.0, "размеры дорожек", G, 9.0))
                .with(note("n", 90.0, 40.0, "панель раскладки", 10.0)),
            Frame::new()
                .with(b("cb0", 180.0, 60.0, 300.0, 28.0, "дорожки: fr и minmax", G, 10.0))
                .with(b("cb1", 180.0, 100.0, 300.0, 28.0, "промежутки: gap", G, 10.0)),
            Frame::new()
                .with(b("cb0", 180.0, 28.0, 300.0, 22.0, "дорожки: fr и minmax", G, 9.5))
                .with(b("cb1", 180.0, 58.0, 300.0, 22.0, "промежутки: gap", G, 9.5))
                .with(b("ck2", 180.0, 88.0, 300.0, 22.0, "адаптивность: auto-fit", B, 9.5))
                .with(b("ck3", 180.0, 118.0, 300.0, 22.0, "области названы по смыслу", B, 9.5))
                .with(b("ck4", 180.0, 148.0, 300.0, 22.0, "порядок в документе = порядок на экране", B, 9.5)),
        ],
    )
}
