//! Дискретная математика, глава 1 — «Множества: язык математики»: сцены 13 слайдов.
//! Перенос с `frontend/src/slides/dm/ch01.tsx` и `anim/*.tsx` (ручная отрисовка на `kit.tsx`) на данные: названия шагов, подписи
//! и метки `cues` взяты из прежних сцен как есть. Что упрощено — см. примечания у сцен («Венн», «Взрыв», «Контракты»).

use content::{
    dsl::{bx, cell, circle, disc, dot, intersect, line, minus, outside, path, py, rect, text, union, zone},
    item::{Anchor, Cell, Path, Text},
    Frame, SceneSpec, Tone, B, G, M, R, Y,
};

/// Сцены главы: имя прежнего компонента — описание.
pub fn scenes() -> Vec<(&'static str, SceneSpec)> {
    vec![
        ("ShapesIntro", shapes_intro()),
        ("ListVsSet", list_vs_set()),
        ("Equality", equality()),
        ("VennOps", venn_ops()),
        ("Complement", complement()),
        ("DeMorgan", de_morgan()),
        ("Overlap", overlap()),
        ("Subset", subset()),
        ("Powerset", powerset()),
        ("Explosion", explosion()),
        ("SetsInUse", sets_in_use()),
        ("Contracts", contracts()),
        ("Recap", recap()),
    ]
}

// --- помощники ---------------------------------------------------------------------------------

/// Прозрачность по условию: показан или погашен.
fn op(on: bool) -> f64 {
    if on {
        1.0
    } else {
        0.0
    }
}

/// Подпись обычным шрифтом (9,5), приглушённая.
fn cap(id: &str, x: f64, y: f64, t: &str) -> Text {
    text(id, x, y, t).size(9.5)
}

/// Моноширинная подпись (по умолчанию 11).
fn mono(id: &str, x: f64, y: f64, t: &str) -> Text {
    text(id, x, y, t).mono().size(11.0)
}

/// Подпись, прижатая к левой точке.
fn left(id: &str, x: f64, y: f64, t: &str) -> Text {
    cap(id, x, y, t).anchor(Anchor::Start)
}

/// Плашка высотой 20 с моноширинной подписью.
fn pill(id: &str, x: f64, y: f64, w: f64, t: &str, tone: Tone) -> Cell {
    bx(id, x, y, w, 20.0, t).tone(tone).size(10.5)
}

/// Контур со скруглёнными углами (без заливки): `(x, y, w, h)` — левый верхний угол и размеры; пунктир `5 4`.
fn hull(id: &str, (x, y, w, h): (f64, f64, f64, f64), r: f64, tone: Tone, dashed: bool) -> Path {
    let d = format!(
        "M{} {y} H{} A{r} {r} 0 0 1 {} {} V{} A{r} {r} 0 0 1 {} {} H{} A{r} {r} 0 0 1 {x} {} V{} A{r} {r} 0 0 1 {} {y} Z",
        x + r,
        x + w - r,
        x + w,
        y + r,
        y + h - r,
        x + w - r,
        y + h,
        x + r,
        y + h - r,
        y + r,
        x + r
    );
    Path { dash: dashed.then(|| "5 4".to_string()), width: 1.6, ..path(id, d).tone(tone) }
}

fn spec(labels: &[&str], captions: &[&str], frames: Vec<Frame>) -> SceneSpec {
    SceneSpec::new(labels, captions, frames)
}

// --- 1. Фигуры и группы ------------------------------------------------------------------------

/// Фигура: (кружок?, цвет, место в «двух группах», место в «трёх группах»).
type Shape = (bool, Tone, (f64, f64), (f64, f64));

const SHAPES: [Shape; 10] = [
    (true, B, (55.0, 62.0), (40.0, 70.0)),
    (true, R, (95.0, 62.0), (160.0, 70.0)),
    (true, G, (135.0, 62.0), (280.0, 70.0)),
    (true, B, (75.0, 108.0), (80.0, 70.0)),
    (true, R, (115.0, 108.0), (200.0, 70.0)),
    (false, G, (225.0, 62.0), (320.0, 70.0)),
    (false, B, (265.0, 62.0), (40.0, 112.0)),
    (false, R, (305.0, 62.0), (180.0, 112.0)),
    (false, G, (245.0, 108.0), (300.0, 112.0)),
    (false, B, (285.0, 108.0), (80.0, 112.0)),
];
/// Обводка двух групп: (x, y, ширина, высота).
const HULLS_A: [(f64, f64, f64, f64); 2] = [(30.0, 38.0, 130.0, 96.0), (200.0, 38.0, 130.0, 96.0)];
/// Обводка трёх групп: рамка, подпись, цвет.
const HULLS_G: [((f64, f64, f64, f64), &str, Tone); 3] =
    [((18.0, 44.0, 84.0, 92.0), "синие", B), ((138.0, 44.0, 84.0, 92.0), "красные", R), ((258.0, 44.0, 84.0, 92.0), "зелёные", G)];

/// Пять кружков и пять квадратов: две группы по форме, затем цвета и три группы по цвету. Те же фигуры переезжают (один `id`).
fn shapes_intro() -> SceneSpec {
    let frames = (0..4)
        .map(|step| {
            let mut f = Frame::new();
            for (i, &(round, tone, a, g)) in SHAPES.iter().enumerate() {
                let (x, y) = if step >= 3 { g } else { a };
                let tone = if step >= 2 { tone } else { M };
                let id = format!("f{i}");
                f = if round { f.with(dot(id, x, y, "").r(12.0).tone(tone)) } else { f.with(cell(id, x, y, "").w(24.0).h(24.0).tone(tone)) };
            }
            if step == 1 {
                for (i, h) in HULLS_A.iter().enumerate() {
                    f = f.with(hull(&format!("pair{i}"), *h, 14.0, G, true));
                }
                f = f.with(cap("lbl-round", 95.0, 152.0, "кружки")).with(cap("lbl-square", 265.0, 152.0, "квадраты"));
            }
            if step >= 3 {
                for (i, &(h, name, tone)) in HULLS_G.iter().enumerate() {
                    f = f.with(hull(&format!("col{i}"), h, 14.0, tone, true)).with(cap(&format!("lbl-col{i}"), h.0 + h.2 / 2.0, 152.0, name));
                }
            }
            f
        })
        .collect();
    spec(
        &["Фигуры", "Две группы", "Цвета", "Три группы"],
        &[
            "Появляются элементы: пять кружков и пять квадратов",
            "Каждую группу можно обвести — получились два множества",
            "Теперь у фигур есть цвета: синий, красный, зелёный",
            "Обведём по цвету — те же фигуры, но уже три других множества",
        ],
        frames,
    )
    .cues(&[4.9, 14.3, 19.2])
}

// --- 2. Множество и список ---------------------------------------------------------------------

const SET_SLOTS: [(f64, f64); 3] = [(270.0, 62.0), (270.0, 88.0), (270.0, 114.0)];
const GUESTS: [&str; 3] = ["Аня", "Борис", "Вера"];
/// Список гостей: имя и место в списке до и после перестановки (при перестановке плашки едут, а не пересоздаются).
const LIST: [(&str, [usize; 2]); 4] = [("Аня", [0, 1]), ("Борис", [1, 2]), ("Аня", [2, 3]), ("Вера", [3, 0])];

/// Множество гостей (кольцо) и список: вторая «Аня» сливается, порядок списка меняется, а множество то же.
fn list_vs_set() -> SceneSpec {
    let shift = |s: usize| [0, 0, 1, 1, 2][s];
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            for (i, name) in GUESTS.iter().enumerate() {
                let (x, y) = SET_SLOTS[(i + shift(step)) % 3];
                f = f.with(pill(&format!("g{i}"), x, y, 56.0, name, G).opacity(op(step >= 1)));
            }
            // повторная «Аня»: стучится снаружи и сливается с настоящей
            let (dx, dy) = if step >= 2 { SET_SLOTS[shift(step) % 3] } else { (180.0, 40.0) };
            f = f.with(pill("dup", dx, dy, 56.0, "Аня", Y).opacity(if step == 1 { 0.9 } else { 0.0 }));
            f = f.with(cap("dup-ask", 180.0, 22.0, "ещё одна «Аня»?").tone(Y).opacity(op(step == 1)));
            let outsider = (1..=2).contains(&step);
            f = f.with(pill("outsider", 336.0, 22.0, 40.0, "Глеб", M).opacity(if outsider { 0.55 } else { 0.0 }));
            f = f.with(cap("outsider-no", 336.0, 42.0, "∉ гостей").opacity(op(outsider)));
            // список
            f = f.with(hull("list-box", (14.0, 26.0, 118.0, 116.0), 10.0, Y, false).opacity(op(step >= 3)));
            f = f.with(cap("list-title", 73.0, 164.0, "список гостей").opacity(op(step >= 3)));
            for k in 0..4 {
                f = f.with(mono(&format!("num{k}"), 28.0, 55.7 + k as f64 * 25.0, &(k + 1).to_string()).opacity(op(step >= 3)));
            }
            for (i, &(name, pos)) in LIST.iter().enumerate() {
                let k = pos[usize::from(step >= 4)];
                let tone = if name == "Аня" { Y } else { M };
                f = f.with(pill(&format!("l{i}"), 85.0, 52.0 + k as f64 * 25.0, 56.0, name, tone).opacity(op(step >= 3)));
            }
            f
        })
        .collect();
    spec(
        &["Набор", "Состав", "Без повторов", "Список", "Порядок"],
        &[
            "Множество — набор элементов",
            "Известно ровно две вещи: кто внутри и что больше никого нет",
            "Ни порядка, ни повторов: вторая «Аня» в множество не добавляется",
            "В списке один человек может встретиться дважды, в множестве — нет",
            "Порядок в списке изменился — множество гостей то же самое",
        ],
        frames,
    )
    .base(Frame::new().with(circle("set-ring", 270.0, 88.0, 62.0).tone(G)).with(cap("set-title", 270.0, 164.0, "множество гостей")))
    .cues(&[1.8, 8.5, 13.4, 20.4])
}

// --- 3. Равенство и пустое множество -----------------------------------------------------------

/// {1, 2} и {2, 1, 1}: повтор сливается, множества равны; затем появляется ∅.
fn equality() -> SceneSpec {
    let frames = (0..4)
        .map(|step| {
            let dim = if step >= 2 { 0.1 } else { 1.0 };
            let grown = step >= 2;
            Frame::new()
                .with(circle("ring-a", 85.0, 70.0, 46.0).tone(G).opacity(dim))
                .with(cap("name-a", 85.0, 132.0, "{1, 2}").opacity(dim))
                .with(circle("ring-b", 275.0, 70.0, 46.0).tone(B).opacity(dim))
                .with(cap("name-b", 275.0, 132.0, "{2, 1, 1}").opacity(dim))
                .with(dot("a1", 68.0, 70.0, "1").r(11.0).opacity(dim))
                .with(dot("a2", 102.0, 70.0, "2").r(11.0).opacity(dim))
                .with(dot("b2", 252.0, 70.0, "2").r(11.0).opacity(dim))
                .with(dot("b1", 288.0, 55.0, "1").r(11.0).opacity(dim))
                // лишняя «1» сливается с настоящей
                .with(dot("b1-dup", 288.0, if step >= 1 { 55.0 } else { 87.0 }, "1").r(11.0).tone(Y).opacity(op(step < 1)))
                .with(mono("eq", 180.0, 76.0, "=").size(22.0).tone(G).opacity(op(step == 1)))
                .with(circle("empty", 180.0, 72.0, 38.0).tone(Y).dash().opacity(op(grown)).scale(if grown { 1.0 } else { 0.5 }))
                .with(mono("empty-sign", 180.0, 81.0, "∅").size(28.0).tone(Y).opacity(op(grown)).scale(if grown { 1.0 } else { 0.5 }))
                .with(mono("sum", 100.0, 154.0, "Σ ∅ = 0").tone(G).opacity(op(step >= 3)))
                .with(mono("search", 260.0, 154.0, "поиск в ∅ → ничего").tone(G).opacity(op(step >= 3)))
                .with(cap("one", 180.0, 128.0, "пустое множество — одно на всех").opacity(op(step >= 2)))
        })
        .collect();
    spec(
        &["Две записи", "Равны", "Пустое", "Точка отсчёта"],
        &[
            "Две записи, в одной есть повтор: {1, 2} и {2, 1, 1}",
            "Повторы и порядок ничего не меняют — это одно и то же множество",
            "Особый житель — пустое множество: в нём нет ни одного элемента",
            "Оно у всех одно: сумма по пустоте равна нулю, поиск ничего не находит",
        ],
        frames,
    )
    .cues(&[5.9, 11.5, 18.4])
}

// --- 4. Три операции (диаграмма Венна) ---------------------------------------------------------

/// Элемент диаграммы: число, к каким множествам относится, дубль общего элемента, место «врозь» и «вместе».
struct VDot {
    n: u8,
    set: &'static str,
    dup: bool,
    apart: (f64, f64),
    joined: (f64, f64),
}

const VDOTS: [VDot; 8] = [
    VDot { n: 1, set: "a", dup: false, apart: (45.0, 68.0), joined: (112.0, 68.0) },
    VDot { n: 2, set: "a", dup: false, apart: (45.0, 104.0), joined: (112.0, 104.0) },
    VDot { n: 3, set: "ab", dup: false, apart: (100.0, 68.0), joined: (180.0, 68.0) },
    VDot { n: 4, set: "ab", dup: false, apart: (100.0, 104.0), joined: (180.0, 104.0) },
    VDot { n: 3, set: "ab", dup: true, apart: (260.0, 68.0), joined: (180.0, 68.0) },
    VDot { n: 4, set: "ab", dup: true, apart: (260.0, 104.0), joined: (180.0, 104.0) },
    VDot { n: 5, set: "b", dup: false, apart: (320.0, 68.0), joined: (248.0, 68.0) },
    VDot { n: 6, set: "b", dup: false, apart: (320.0, 104.0), joined: (248.0, 104.0) },
];

/// Круги плывут навстречу, общие элементы 3 и 4 сливаются, затем по очереди заливаются A ∪ B, A ∩ B и A \ B.
/// Шаги: 0 — врозь, 1 — сближение, 2 — слияние, 3–5 — операции (формула и результат — в подписи шага).
/// Упрощено: кнопки шагов — названия шагов (раньше были только три операции), «пульс» слившихся элементов — увеличенные кружки.
fn venn_ops() -> SceneSpec {
    let (da, db) = (disc(140.0, 85.0, 62.0), disc(220.0, 85.0, 62.0));
    let frames = (0..6usize)
        .map(|step| {
            let joined = step >= 1;
            let merged = step >= 2;
            // операция на шаге: 0 — объединение, 1 — пересечение, 2 — разность
            let mode = step.checked_sub(3);
            let mut f = Frame::new()
                .with(circle("ring-a", if joined { 140.0 } else { 70.0 }, 85.0, 62.0).tone(G))
                .with(circle("ring-b", if joined { 220.0 } else { 290.0 }, 85.0, 62.0).tone(B))
                .with(union("fill-union", &[da, db]).tone(G).fill_opacity(0.42).shown(op(mode == Some(0))))
                .with(intersect("fill-inter", da, db).tone(Y).fill_opacity(0.42).shown(op(mode == Some(1))))
                .with(minus("fill-diff", da, &[db]).tone(B).fill_opacity(0.42).shown(op(mode == Some(2))))
                .with(text("label-a", if joined { 92.0 } else { 22.0 }, 30.0, "A").mono().size(15.0).tone(M))
                .with(text("label-b", if joined { 268.0 } else { 338.0 }, 30.0, "B").mono().size(15.0).tone(M));
            for (i, d) in VDOTS.iter().enumerate() {
                let (x, y) = if joined { d.joined } else { d.apart };
                let common = d.set == "ab";
                let hit = match mode {
                    Some(1) => common,
                    Some(2) => d.set == "a",
                    _ => true,
                };
                let (tone, o) = if d.dup && merged {
                    (G, 0.0)
                } else if !hit {
                    (M, 0.28)
                } else if common && !merged {
                    (Y, 1.0)
                } else {
                    (G, 1.0)
                };
                let pulse = if common && !d.dup && step == 2 { 1.25 } else { 1.0 };
                f = f.with(dot(format!("e{i}"), x, y, d.n.to_string()).r(12.0).tone(tone).opacity(o).scale(pulse));
            }
            f
        })
        .collect();
    spec(
        &["Врозь", "Сближение", "Слияние", "A ∪ B", "A ∩ B", "A \\ B"],
        &[
            "A = {1, 2, 3, 4} и B = {3, 4, 5, 6}: общие элементы 3 и 4 есть и там, и там",
            "Множества сближаются…",
            "Общие элементы слились: в множестве каждое значение — один раз",
            "A ∪ B = { 1, 2, 3, 4, 5, 6 } — всё, что есть хотя бы в одном множестве",
            "A ∩ B = { 3, 4 } — только то, что есть в обоих",
            "A \\ B = { 1, 2 } — из A без того, что есть в B",
        ],
        frames,
    )
    .cues(&[4.4, 5.4, 5.9, 11.8, 17.3])
    .step_ms(2600)
}

// --- 5. Универсум и дополнение -----------------------------------------------------------------

/// Пользователи системы, администраторы A и дополнение ¬A; затем универсум меняется на «людей планеты» — дополнение растёт, A прежнее.
/// Рамка универсума при смене меняется не плавным ростом, а перекрёстным появлением двух рамок.
fn complement() -> SceneSpec {
    const ADMIN: [usize; 4] = [0, 1, 4, 5];
    let extra: Vec<(f64, f64)> = [16.0, 30.0, 44.0, 318.0, 332.0, 346.0].iter().flat_map(|&x| (0..6).map(move |k| (x, 28.0 + k as f64 * 20.0))).collect();
    let frames = (0..5)
        .map(|step| {
            let big = step >= 3;
            let mut f = Frame::new()
                .with(hull("u-small", (78.0, 26.0, 204.0, 114.0), 12.0, M, true).opacity(op((1..3).contains(&step))))
                .with(hull("u-big", (6.0, 8.0, 348.0, 138.0), 12.0, M, true).opacity(op(big)))
                .with(left("u-small-name", 88.0, 38.0, "U · все пользователи системы").opacity(op((1..3).contains(&step))))
                .with(left("u-big-name", 16.0, 20.0, "U · люди на планете").opacity(op(big)))
                .with(circle("ring-a", 133.0, 66.0, 38.0).tone(B).opacity(op(step >= 2)))
                .with(cap("name-a", 128.0, 134.0, "A · администраторы").tone(B).opacity(op(step >= 2)));
            for i in 0..12 {
                let tone = if step < 2 {
                    M
                } else if ADMIN.contains(&i) {
                    B
                } else {
                    Y
                };
                f = f.with(dot(format!("u{i}"), 110.0 + (i % 4) as f64 * 46.0, 52.0 + (i / 4) as f64 * 30.0, "").r(9.0).tone(tone));
            }
            for (i, &(x, y)) in extra.iter().enumerate() {
                f = f.with(dot(format!("x{i}"), x, y, "").r(4.5).tone(Y).opacity(op(big)));
            }
            f.with(cap("name-not-a", 242.0, 134.0, "¬A · остальные").tone(Y).opacity(op(step >= 2)))
                .with(bx("code", 180.0, if step >= 4 { 157.0 } else { 163.0 }, 232.0, 18.0, "[u for u in U if u not in A]").size(10.0).opacity(op(step >= 4)))
        })
        .collect();
    spec(
        &["Договор", "Универсум", "Дополнение", "Другой U", "В коде"],
        &[
            "Четвёртая операция — дополнение: сначала нужно договориться, от чего считать",
            "Универсум U — все элементы, которые мы вообще рассматриваем",
            "Дополнение администраторов A — все остальные пользователи",
            "Сменили универсум на людей планеты — дополнение стало другим, а A то же",
            "В коде это «всё, что не попало в фильтр»",
        ],
        frames,
    )
    .cues(&[5.4, 12.0, 17.5, 24.4])
    .step_ms(3000)
}

// --- 6. Законы де Моргана ----------------------------------------------------------------------

/// Категория точки: a — только A, b — только B, ab — оба, n — ни там ни там.
const MORGAN_DOTS: [(&str, &str, f64, f64); 8] = [
    ("a1", "a", 126.0, 56.0),
    ("a2", "a", 124.0, 92.0),
    ("c1", "ab", 180.0, 72.0),
    ("b1", "b", 234.0, 56.0),
    ("b2", "b", 236.0, 92.0),
    ("n1", "n", 64.0, 36.0),
    ("n2", "n", 298.0, 112.0),
    ("n3", "n", 66.0, 112.0),
];

/// Подписи кругов по шагам: (номер набора, левый, правый).
const CIRCLE_NAMES: [(usize, &str, &str); 4] = [(0, "A", "B"), (4, "дешёвый", "старый"), (5, "тесты ✓", "ревью ✓"), (6, "админ", "редактор")];

/// Подпись внизу: (шаг, текст, цвет, кегль).
const MORGAN_LINES: [(usize, &str, Tone, f64); 7] = [
    (1, "¬(A ∪ B) = ¬A ∩ ¬B", G, 12.0),
    (2, "¬(A ∩ B) = ¬A ∪ ¬B", Y, 12.0),
    (3, "x ∈ ¬A ∩ ¬B ⇒ x ∈ ¬(A ∪ B)", G, 11.0),
    (4, "не (дешёвый или старый) = не дешёвый и не старый", G, 10.5),
    (5, "не (тесты и ревью) = красные тесты или нет ревью", Y, 10.5),
    (6, "¬A ∪ ¬B: все, кроме тех, кто и админ, и редактор", R, 10.5),
    (7, "не админ И не редактор = не (админ или редактор)", G, 10.5),
];

/// Какой набор подписей кругов показан на шаге.
fn name_set(step: usize) -> usize {
    match step {
        6 | 7 => 6,
        5 => 5,
        4 => 4,
        _ => 0,
    }
}

/// Цвет подсвеченной точки на шаге.
fn morgan_mark(step: usize, cat: &str) -> Option<Tone> {
    match step {
        4 | 7 if cat == "n" => Some(G),
        5 if cat != "ab" => Some(Y),
        6 if cat != "ab" => Some(R),
        _ => None,
    }
}

/// Заливка на диаграмме Венна показывает ¬(A ∪ B) и ¬(A ∩ B); затем доказательство на одном элементе, примеры, частая ошибка и SQL.
/// ¬(A ∩ B) — прямоугольник с «дыркой» в линзе пересечения (контур с противоположным обходом), два контура: жёлтый и красный.
fn de_morgan() -> SceneSpec {
    let (da, db) = (disc(150.0, 72.0, 46.0), disc(210.0, 72.0, 46.0));
    // линза A ∩ B: дуги кругов через точки (180, 72 ± √(46² − 30²))
    let (top, bottom) = (72.0 - 34.871, 72.0 + 34.871);
    let not_lens = format!(
        "M50 10 H310 A10 10 0 0 1 320 20 V124 A10 10 0 0 1 310 134 H50 A10 10 0 0 1 40 124 V20 A10 10 0 0 1 50 10 Z M180 {top} A46 46 0 0 0 180 {bottom} A46 46 0 0 0 180 {top} Z"
    );
    let lens = |id: &str, hue: &str, o: f64| Path { fill: Some(hue.to_string()), fill_opacity: Some(0.35), width: 0.0, ..path(id, not_lens.clone()).opacity(o) };
    let frames = (0..10)
        .map(|step| {
            // диаграмма гаснет, когда на экране код и итог
            let venn = if step <= 7 { 1.0 } else { 0.06 };
            let out_o = match step {
                1 => 1.0,
                4 | 7 => 0.3 / 0.35,
                _ => 0.0,
            };
            let lens_y = match step {
                2 => 1.0,
                5 => 0.3 / 0.35,
                _ => 0.0,
            };
            let lens_r = if step == 6 { 0.3 / 0.35 } else { 0.0 };
            let mut f = Frame::new()
                .with(zone("universe", 180.0, 72.0, 280.0, 124.0).opacity(venn))
                .with(outside("not-union", rect(40.0, 10.0, 280.0, 124.0), &[da, db]).tone(G).fill_opacity(0.35).shown(out_o))
                .with(lens("not-inter-y", "var(--s-amber)", lens_y))
                .with(lens("not-inter-r", "var(--s-red)", lens_r))
                .with(circle("ring-a", 150.0, 72.0, 46.0).tone(G).opacity(venn))
                .with(circle("ring-b", 210.0, 72.0, 46.0).tone(B).opacity(venn));
            for &(k, a, b) in &CIRCLE_NAMES {
                let o = op(k == name_set(step)) * venn;
                f = f.with(mono(&format!("na{k}"), 124.0, 40.0, a).size(9.5).opacity(o)).with(mono(&format!("nb{k}"), 236.0, 40.0, b).size(9.5).opacity(o));
            }
            f = f.with(cap("u-name", 52.0, 24.0, "U").anchor(Anchor::Start).opacity(venn));
            for &(id, cat, x, y) in &MORGAN_DOTS {
                let solo = step == 3 && id == "n1";
                let shown = (4..=7).contains(&step) || solo;
                let tone = morgan_mark(step, cat).unwrap_or(if solo { G } else { M });
                f = f.with(dot(id, x, y, "").r(if solo { 10.0 } else { 8.0 }).tone(tone).opacity(op(shown)));
            }
            if step == 3 {
                f = f.with(mono("solo", 64.0, 62.0, "x ∉ A, x ∉ B").size(10.0).tone(G));
            }
            for &(s, t, tone, size) in &MORGAN_LINES {
                if s == step {
                    f = f.with(mono(&format!("rule{s}"), 180.0, 154.0, t).size(size).tone(tone));
                }
            }
            if step == 8 {
                f = f
                    .with(mono("code1", 180.0, 42.0, "!(a || b) === !a && !b"))
                    .with(mono("code2", 180.0, 62.0, "!(a && b) === !a || !b"))
                    .with(mono("sql1", 180.0, 96.0, "WHERE NOT (a OR b)").tone(G))
                    .with(mono("sql2", 180.0, 112.0, "= WHERE NOT a AND NOT b").tone(G));
            }
            if step >= 9 {
                f = f.with(mono("flip", 180.0, 86.0, "«или» ↔ «и»").size(20.0).tone(G));
            }
            f
        })
        .collect();
    spec(
        &["Законы", "Первый", "Второй", "Почему", "Товары", "Задание", "Ошибка", "Верно", "База", "Итог"],
        &[
            "Операции подчиняются законам; самые знаменитые — законы де Моргана",
            "Первый: дополнение объединения — всё вне обоих кругов, то есть ¬A ∩ ¬B",
            "Второй: дополнение пересечения — всё, кроме общей части, то есть ¬A ∪ ¬B",
            "Почему так: элемент вне объединения не входит ни в A, ни в B — значит, он в обоих дополнениях",
            "Магазин: «не дешёвые и не старые» — то же, что «не (дешёвый или старый)»",
            "Задание принято, если тесты зелёные и ревью пройдено; не принято — если нарушено хотя бы одно",
            "Частая ошибка: «не админ или не редактор» пропускает почти всех",
            "Верно: «не админ и не редактор» — или «не» от скобки с «или»",
            "В коде и в базе данных — то же самое: отрицание переворачивает «или» и «и»",
            "Отрицание переворачивает «или» в «и» и обратно",
        ],
        frames,
    )
    .cues(&[5.0, 8.5, 12.2, 25.4, 38.9, 51.7, 64.9, 69.7, 76.8])
    .step_ms(3000)
}

// --- 7. Мощность и двойной счёт ----------------------------------------------------------------

/// Два множества по 20 точек (EN и DE); 5 общих точек при сближении кругов сливаются: 20 + 20 = 40 превращается в честные 35.
fn overlap() -> SceneSpec {
    const ROWS: [f64; 5] = [-28.0, -14.0, 0.0, 14.0, 28.0];
    const OWN: [f64; 3] = [-34.0, -18.0, -2.0];
    let frames = (0..5)
        .map(|step| {
            let xa = [180.0, 90.0, 145.0, 145.0, 145.0][step];
            let xb = if step == 1 { 270.0 } else { 215.0 };
            let both = if step >= 4 { R } else { Y };
            let de_on = op(step >= 1);
            let mut f = Frame::new().with(circle("ring-en", xa, 84.0, 50.0).tone(G));
            // EN: свои точки слева, общие — справа
            for (xi, &x) in OWN.iter().enumerate() {
                for (yi, &y) in ROWS.iter().enumerate() {
                    f = f.with(dot(format!("en{xi}{yi}"), xa + x, 84.0 + y, "").r(3.4).tone(M));
                }
            }
            for (yi, &y) in ROWS.iter().enumerate() {
                f = f.with(dot(format!("enb{yi}"), xa + 35.0, 84.0 + y, "").r(3.4).tone(both));
            }
            f = f.with(cap("name-en", xa - 34.0, 26.0, "EN"));
            // DE: свои точки справа, общие — слева; при слиянии общие точки DE исчезают (остаются точки EN)
            f = f.with(circle("ring-de", xb, 84.0, 50.0).tone(B).opacity(de_on));
            for (xi, &x) in OWN.iter().enumerate() {
                for (yi, &y) in ROWS.iter().enumerate() {
                    f = f.with(dot(format!("de{xi}{yi}"), xb - x, 84.0 + y, "").r(3.4).tone(M).opacity(de_on));
                }
            }
            for (yi, &y) in ROWS.iter().enumerate() {
                f = f.with(dot(format!("deb{yi}"), xb - 35.0, 84.0 + y, "").r(3.4).tone(both).opacity(op(step >= 1 && step < 2)));
            }
            f = f.with(cap("name-de", xb + 34.0, 26.0, "DE").opacity(de_on));
            let top: [(&str, Tone, f64); 5] =
                [("|EN| = 20", G, 13.0), ("20 + 20 = 40 ?", G, 13.0), ("|EN ∪ DE| = 35", G, 13.0), ("|A ∪ B| = |A| + |B| − |A ∩ B|", G, 10.5), ("5 человек посчитаны дважды", R, 12.0)];
            let (t, tone, size) = top[step];
            f = f.with(mono("top", 180.0, 16.0, t).size(size).tone(tone));
            if step == 3 {
                f = f.with(mono("calc", 180.0, 162.0, "= 20 + 20 − 5 = 35"));
            }
            f
        })
        .collect();
    spec(
        &["Мощность", "20 + 20", "Перекрытие", "Формула", "Двойной счёт"],
        &[
            "Мощность |A| — число элементов: как размер массива или число записей запроса",
            "Знают английский 20 человек и немецкий 20: наивно сложим и получим 40",
            "Но знающие оба языка попали в оба списка — при объединении их считают один раз",
            "Честный счёт — формулой включений и исключений: ей посвящена отдельная глава",
            "Наивное сложение — классическая ошибка двойного счёта",
        ],
        frames,
    )
    .cues(&[6.9, 14.7, 23.5, 28.5])
    .step_ms(3000)
}

// --- 8. Подмножества ---------------------------------------------------------------------------

/// Внутри большого множества B живёт меньшее A; подписи меняются с абстрактных на числа и права ролей; в конце — проверка A ∩ B = A.
fn subset() -> SceneSpec {
    const INSIDE: [(f64, f64); 4] = [(122.0, 76.0), (158.0, 76.0), (122.0, 108.0), (158.0, 108.0)];
    const OUTSIDE: [(f64, f64); 4] = [(205.0, 52.0), (236.0, 72.0), (236.0, 104.0), (205.0, 124.0)];
    // наборы подписей: внутри A, снаружи A (но в B), название B, название A
    const WORDS: [([&str; 4], [&str; 4], &str, &str); 3] = [
        (["a", "b", "c", "d"], ["e", "f", "g", "h"], "B", "A"),
        (["2", "4", "6", "8"], ["1", "3", "5", "7"], "ℤ · целые", "чётные"),
        (["чт", "зап", "удл", "пуб"], ["нст", "рол", "клч", "бэк"], "администратор", "редактор"),
    ];
    let (da, db) = (disc(140.0, 90.0, 44.0), disc(180.0, 88.0, 70.0));
    let frames = (0..4)
        .map(|step| {
            let v = step.min(2);
            let mut f = Frame::new()
                .with(circle("ring-b", db.x, db.y, db.r).tone(G))
                .with(union("fill-a", &[da]).tone(Y).fill_opacity(0.28).shown(op(step >= 3)))
                .with(circle("ring-a", da.x, da.y, da.r).tone(Y));
            for (vi, (inn, out, big, small)) in WORDS.iter().enumerate() {
                let on = op(v == vi);
                let size = if vi == 2 { 8.5 } else { 11.0 };
                for i in 0..4 {
                    f = f.with(dot(format!("w{vi}in{i}"), INSIDE[i].0, INSIDE[i].1, inn[i]).r(13.0).tone(Y).size(size).opacity(on));
                    f = f.with(dot(format!("w{vi}out{i}"), OUTSIDE[i].0, OUTSIDE[i].1, out[i]).r(13.0).tone(M).size(size).opacity(on));
                }
                f = f.with(left(&format!("w{vi}b"), 6.0, 22.0, &format!("B: {big}")).tone(G).opacity(on));
                f = f.with(left(&format!("w{vi}a"), 6.0, 38.0, &format!("A: {small}")).tone(Y).opacity(on));
            }
            f.with(mono("rel", 300.0, 40.0, "A ⊆ B").size(13.0).tone(G).opacity(op(step < 3)))
                .with(mono("rel-inter", 300.0, 40.0, "A ∩ B = A").size(13.0).tone(Y).opacity(op(step >= 3)))
                .with(mono("rel-then", 300.0, 60.0, "⇒ A ⊆ B").size(13.0).tone(G).opacity(op(step >= 3)))
        })
        .collect();
    spec(
        &["Вложение", "Числа", "Права", "Проверка"],
        &[
            "Если каждый элемент A есть и в B, то A — подмножество B: A ⊆ B",
            "Чётные числа — подмножество целых: каждое чётное является целым",
            "Права редактора — подмножество прав администратора: без настройки системы",
            "Проверка: пересечение с большим множеством совпало с меньшим — оно вложено",
        ],
        frames,
    )
    .cues(&[7.3, 11.0, 17.9])
    .step_ms(3000)
}

// --- 9. Булеан ---------------------------------------------------------------------------------

const TREE_X: [f64; 4] = [36.0, 106.0, 176.0, 246.0];

fn leaf_y(i: usize) -> f64 {
    24.0 + i as f64 * 17.5
}

/// Высота узла уровня `l` с номером `j`: посередине между листьями его поддерева.
fn node_y(l: usize, j: usize) -> f64 {
    let span = 1usize << (3 - l);
    (leaf_y(j * span) + leaf_y(j * span + span - 1)) / 2.0
}

/// Подмножество с номером `i` (старший бит — элемент a): `∅`, `{c}`, `{b}`, `{b, c}`, …
fn subset_name(i: usize) -> String {
    if i == 0 {
        return "∅".into();
    }
    let items: Vec<&str> = ["a", "b", "c"].iter().enumerate().filter(|(k, _)| (i >> (2 - k)) & 1 == 1).map(|(_, n)| *n).collect();
    format!("{{{}}}", items.join(", "))
}

/// Дерево решений «взять / не взять» для трёх элементов: 8 листьев — 8 подмножеств; затем подписи листьев становятся битовыми масками.
fn powerset() -> SceneSpec {
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            if step <= 1 {
                for (i, n) in ["a", "b", "c"].iter().enumerate() {
                    f = f.with(dot(format!("src{i}"), 130.0 + i as f64 * 50.0, 70.0, *n).r(17.0).tone(G).size(14.0));
                }
                f = f.with(mono("src-name", 180.0, 38.0, "{a, b, c}").size(13.0).tone(G));
            }
            if step == 1 {
                f = f.with(mono("count", 180.0, 124.0, "n = 3 → 2ⁿ = 2·2·2 = 8").size(14.0).tone(Y));
            }
            if (2..=4).contains(&step) {
                let tree = match step {
                    3 => 0.2,
                    _ => 1.0,
                };
                for l in 0..3 {
                    for j in 0..(1usize << l) {
                        for c in 0..2 {
                            let yes = c == 1;
                            let e = line(format!("e{l}{j}{c}"), TREE_X[l], node_y(l, j), TREE_X[l + 1], node_y(l + 1, j * 2 + c)).width(1.4).tone(if yes { G } else { M }).opacity(tree);
                            f = f.with(if yes { e } else { e.dash() });
                        }
                    }
                }
                for (l, n) in ["a?", "b?", "c?"].iter().enumerate() {
                    f = f.with(mono(&format!("q{l}"), (TREE_X[l] + TREE_X[l + 1]) / 2.0, 12.0, n).size(10.5).opacity(tree));
                }
                for i in 0..8 {
                    let y = leaf_y(i);
                    f = f.with(dot(format!("leaf{i}"), TREE_X[3], y, "").r(3.0).tone(G).opacity(tree));
                    f = f.with(mono(&format!("set{i}"), TREE_X[3] + 9.0, y + 3.5, &subset_name(i)).size(9.5).anchor(Anchor::Start).opacity(if step == 4 { 0.0 } else { tree }));
                    f = f.with(mono(&format!("mask{i}"), TREE_X[3] + 9.0, y + 3.5, &format!("{i:03b} = {}", subset_name(i))).size(9.5).tone(Y).anchor(Anchor::Start).opacity(op(step == 4)));
                }
                f = f.with(cap("legend", 180.0, 166.0, "— — не брать · ——— взять").opacity(op(step != 3)));
            }
            if step == 3 {
                f = f.with(mono("n3", 180.0, 70.0, "n = 3 → 8").size(16.0).tone(G)).with(mono("n10", 180.0, 100.0, "n = 10 → 1 024").size(16.0).tone(Y));
            }
            f
        })
        .collect();
    spec(
        &["Булеан", "2ⁿ", "Выбор", "3 → 10", "Биты"],
        &[
            "Булеан — множество всех подмножеств исходного множества",
            "Если в множестве n элементов, то в булеане 2ⁿ подмножеств",
            "Для каждого элемента — два выбора: взять или нет, всего 2 · 2 · 2 решений",
            "Три элемента — восемь подмножеств, десять — уже тысяча двадцать четыре",
            "Битовая маска: один бит на элемент, каждое число — готовое подмножество",
        ],
        frames,
    )
    .cues(&[5.7, 11.2, 18.5, 23.1])
    .step_ms(3000)
}

// --- 10. Цена перебора -------------------------------------------------------------------------

/// Кривая 2ⁿ: почти плоская до самого конца, потом взлетает; метка n = 30 и «бюджет времени».
/// Упрощено: прежняя кривая рисовалась по таймеру целиком в первом шаге; теперь на шаге «Рост» она доходит до n = 28,
/// а взлёт к n = 30 дорисовывается на шаге «n = 30» — рисование идёт вместе со словами.
fn explosion() -> SceneSpec {
    let pts: Vec<(f64, f64)> = (0..=30).map(|n| (30.0 + n as f64 * 10.0, 140.0 - 118.0 * 2f64.powi(n - 30))).collect();
    let d = format!("M{}", pts.iter().map(|(x, y)| format!("{x:.1} {y:.1}")).collect::<Vec<_>>().join(" L"));
    // доля длины кривой до точки n
    let len = |upto: usize| pts[..=upto].windows(2).map(|w| (w[1].0 - w[0].0).hypot(w[1].1 - w[0].1)).sum::<f64>();
    let share28 = len(28) / len(30);
    let mut base = Frame::new().with(line("axis", 30.0, 140.0, 336.0, 140.0).tone(Tone::Outline).width(1.2));
    for n in [10, 20, 30] {
        let x = 30.0 + n as f64 * 10.0;
        base = base.with(line(format!("tick{n}"), x, 140.0, x, 145.0).width(1.0)).with(cap(&format!("tick-name{n}"), x, 156.0, &format!("n = {n}")));
    }
    let frames = (0..4)
        .map(|step| {
            let curve = Path { width: 2.4, ..path("curve", d.clone()).tone(Y).draw(if step == 0 { share28 } else { 1.0 }) };
            let mut f = Frame::new()
                .with(curve)
                .with(mono("v10", 130.0, 130.0, "1 024"))
                .with(mono("v20", 230.0, 130.0, "≈ 10⁶"))
                .with(mono("v30", 306.0, 28.0, "> 10⁹").tone(Y).opacity(op(step >= 1)))
                .with(circle("mark", 330.0, 22.0, 7.0).tone(R).opacity(op(step >= 1)));
            if step == 1 {
                f = f.with(cap("m30", 180.0, 46.0, "n = 30: больше миллиарда вариантов").size(11.0).tone(R));
            }
            if step == 2 {
                f = f
                    .with(line("formula-line", 30.0, 124.0, 330.0, 124.0).tone(G).dash_pattern("6 4"))
                    .with(cap("formula", 180.0, 112.0, "формула: считаем, а не перебираем — мгновенно").size(11.0).tone(G));
            }
            if step == 3 {
                f = f
                    .with(mono("b0", 150.0, 56.0, "1 мкс на вариант:"))
                    .with(mono("b30", 150.0, 76.0, "n = 30 → около 18 минут").size(12.0).tone(Y))
                    .with(mono("b40", 150.0, 96.0, "n = 40 → около 13 суток").size(12.0).tone(R));
            }
            f
        })
        .collect();
    spec(
        &["Рост", "n = 30", "Формула", "Бюджет"],
        &[
            "Перебор всех подмножеств растёт экспоненциально — это самая дорогая операция курса",
            "Уже при тридцати элементах вариантов больше миллиарда",
            "Поэтому дискретная математика дорожит каждой возможностью не перебирать, а считать формулой",
            "Два в степени n — бюджет вашего времени: увидели её в решении — остановитесь",
        ],
        frames,
    )
    .base(base)
    .cues(&[8.3, 18.4, 23.6])
    .step_ms(3000)
}

// --- 11. Множества в работе --------------------------------------------------------------------

/// Список → хеш-сет (дедупликация), операции SQL, теги и сегменты, цикл с флагом против одной операции.
fn sets_in_use() -> SceneSpec {
    const VALS: [u8; 5] = [3, 1, 3, 2, 1];
    let bucket = |v: u8| match v {
        3 => 130.0,
        1 => 180.0,
        _ => 230.0,
    };
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new();
            // список → хеш-сет; к шагу 2 всё гаснет
            if step <= 1 {
                for b in 0..3 {
                    f = f.with(hull(&format!("bucket{b}"), (110.0 + b as f64 * 50.0, 102.0, 40.0, 36.0), 8.0, G, true).opacity(op(step >= 1)));
                }
                let mut seen: Vec<u8> = Vec::new();
                for (k, &v) in VALS.iter().enumerate() {
                    let dup = seen.contains(&v);
                    seen.push(v);
                    let to = step >= 1;
                    let (x, y) = if to { (bucket(v), 120.0) } else { (70.0 + k as f64 * 55.0, 44.0) };
                    f = f.with(dot(format!("v{k}"), x, y, v.to_string()).r(11.0).tone(if dup && to { Y } else { M }).opacity(op(!(dup && to))));
                }
                f = f.with(mono("set-eq", 180.0, 80.0, "set([3, 1, 3, 2, 1]) = {3, 1, 2}").tone(G).opacity(op(step == 1)));
                f = f.with(cap("list-name", 180.0, 18.0, "список значений").opacity(op(step == 0)));
            }
            // SQL
            if step == 2 {
                for (i, (code, name)) in [("A UNION B", "объединение"), ("A INTERSECT B", "пересечение"), ("A EXCEPT B", "разность")].iter().enumerate() {
                    let y = 44.0 + i as f64 * 34.0;
                    f = f
                        .with(mono(&format!("sql{i}"), 40.0, y, code).size(12.0).anchor(Anchor::Start))
                        .with(mono(&format!("arr{i}"), 170.0, y, "→").size(12.0).tone(G).anchor(Anchor::Start))
                        .with(cap(&format!("op{i}"), 196.0, y, name).size(12.0).anchor(Anchor::Start));
                }
                f = f.with(cap("rows", 180.0, 150.0, "миллионы строк за один запрос").tone(Y));
            }
            // теги и сегменты
            if step == 3 {
                f = f
                    .with(pill("tag0", 70.0, 50.0, 78.0, "python", B))
                    .with(pill("tag1", 180.0, 50.0, 78.0, "базы", Y))
                    .with(pill("tag2", 290.0, 50.0, 78.0, "алгоритмы", G))
                    .with(mono("and0", 125.0, 54.0, "∩").size(16.0).tone(G))
                    .with(mono("and1", 235.0, 54.0, "∩").size(16.0).tone(G))
                    .with(mono("down", 180.0, 92.0, "↓").size(14.0).tone(G))
                    .with(pill("articles", 180.0, 116.0, 210.0, "статьи со всеми тремя тегами", G));
            }
            // цикл с флагом против одной операции
            if step >= 4 {
                f = f
                    .with(py("loop", 40.0, 40.0, &["found = False", "for x in a:", "    if x in b: found = True"]).w(214.0).size(11.0).lh(16.0).opacity(0.45))
                    .with(line("strike", 36.0, 60.0, 250.0, 38.0).tone(R))
                    .with(bx("inter", 180.0, 116.0, 110.0, 34.0, "a & b").tone(G).size(18.0).text_color("var(--s-accent)"))
                    .with(cap("one-op", 180.0, 152.0, "одна операция вместо цикла"));
            }
            f
        })
        .collect();
    spec(
        &["Список", "Хеш-сет", "SQL", "Продукт", "Код"],
        &[
            "Посмотрим, где это живёт в повседневной работе: вот список значений с повторами",
            "Проверка принадлежности в хеш-сете стоит константу: дедупликация — просто перевод списка в множество",
            "В SQL те же операции — UNION, INTERSECT, EXCEPT — и база выполняет их на миллионах строк",
            "Фильтры аналитики, сегменты пользователей, теги статей — под капотом множества и пересечения",
            "Когда вы думаете множествами, вместо цикла с флагом — одна операция пересечения",
        ],
        frames,
    )
    .cues(&[3.3, 10.1, 16.9, 23.3])
    .step_ms(3000)
}

// --- 12. Список или множество ------------------------------------------------------------------

/// Список помнит порядок и повторы, множество мгновенно отвечает «есть ли такой»; поиск в цикле по списку — множество в маске списка.
/// Упрощено: прежняя «бегущая подсветка» клеток при переборе заменена вспышкой всего ряда на шаге «Поиск».
fn contracts() -> SceneSpec {
    let frames = (0..5)
        .map(|step| {
            let mut f = Frame::new()
                .with(mono("lt", 90.0, 16.0, "Список").size(12.0).tone(Y))
                .with(mono("st", 270.0, 16.0, "Множество").size(12.0).tone(G))
                .with(cap("lsub", 90.0, 30.0, "порядок и повторы").opacity(op(step == 0)))
                .with(cap("ssub", 270.0, 30.0, "только принадлежность").opacity(op(step == 0)));
            // список
            for (i, v) in ["A", "B", "A", "C"].iter().enumerate() {
                let x = 30.0 + i as f64 * 40.0;
                f = f.with(pill(&format!("li{i}"), x, 56.0, 34.0, v, Y).opacity(op(step >= 1)));
                f = f.with(cap(&format!("ix{i}"), x, 80.0, &i.to_string()).opacity(op(step >= 1)));
            }
            f = f.with(cap("lnote", 90.0, 98.0, "очередь · история · страницы").opacity(op(step == 1)));
            for i in 0..7 {
                f = f.with(cell(format!("scan{i}"), 31.5 + i as f64 * 22.0, 123.0, "").w(19.0).h(22.0).tone(Y).opacity(match step {
                    3 => 1.0,
                    4 => 0.45,
                    _ => 0.0,
                }));
            }
            f = f.with(cap("lscan", 90.0, 150.0, "в цикле: смотрим всех подряд").tone(Y).opacity(op(step == 3)));
            f = f.with(hull("mask", (14.0, 104.0, 152.0, 38.0), 10.0, G, true).opacity(op(step >= 4)));
            f = f.with(cap("lmask", 90.0, 158.0, "это множество в маске списка").tone(G).opacity(op(step >= 4)));
            // множество
            f = f.with(circle("ring", 270.0, 66.0, 38.0).tone(G).opacity(op(step >= 2)));
            for &(x, y, v) in &[(252.0, 56.0, 3), (286.0, 56.0, 1), (252.0, 82.0, 4), (286.0, 82.0, 7)] {
                f = f.with(dot(format!("s{v}"), x, y, v.to_string()).r(10.0).tone(if v == 7 { G } else { M }).opacity(op(step >= 2)));
            }
            f.with(pill("ask", 270.0, 126.0, 64.0, "есть 7?", G).opacity(op(step >= 2)))
                .with(cap("yes", 270.0, 150.0, "✓ да — сразу").tone(G).opacity(op(step >= 2)))
        })
        .collect();
    spec(
        &["Контракты", "Список", "Множество", "Поиск", "Выбор"],
        &[
            "Список и множество — разные контракты под похожим синтаксисом",
            "Список хранит порядок и допускает повторы: очередь задач, история, постраничная выдача",
            "Множество хранит факт принадлежности и мгновенно отвечает «есть ли здесь такой»",
            "Поиск внутри списка в цикле — перебор всех элементов подряд",
            "Если вы ищете в списке — это почти всегда множество, замаскированное под список",
        ],
        frames,
    )
    .base(Frame::new().with(line("divider", 180.0, 8.0, 180.0, 164.0).tone(Tone::Outline).dash_pattern("3 4").width(1.0)))
    .cues(&[4.7, 12.0, 18.1, 25.4])
    .step_ms(3000)
}

// --- 13. Итог ----------------------------------------------------------------------------------

/// Карточки тем по очереди загораются, затем — где это применялось и что дальше.
fn recap() -> SceneSpec {
    const CARDS: [(&str, &str); 5] = [("∈", "элементы"), ("∪ ∩", "операции"), ("¬", "де Морган"), ("|A|", "мощность"), ("2ⁿ", "булеан")];
    let frames = (0..8)
        .map(|step| {
            let mut f = Frame::new();
            for (i, &(big, name)) in CARDS.iter().enumerate() {
                let (cx, cy) = (38.0 + i as f64 * 71.0, 52.0);
                let current = step == i + 1;
                let lit = step >= i + 1;
                let k = if current { 1.1 } else { 1.0 };
                f = f
                    .with(bx(format!("card{i}"), cx, cy, 62.0, 68.0, "").tone(if lit { G } else { M }).scale(k))
                    .with(mono(&format!("big{i}"), cx, cy + 6.0 * k, big).size(17.0).tone(G).scale(k))
                    .with(cap(&format!("name{i}"), cx, cy + 24.0 * k, name).scale(k));
            }
            for (i, t) in ["set()", "UNION", "INTERSECT", "EXCEPT"].iter().enumerate() {
                f = f.with(pill(&format!("use{i}"), 64.0 + i as f64 * 77.0, 116.0, 66.0, t, Y).opacity(op(step >= 6)));
            }
            f.with(bx("next", 180.0, 150.0, 250.0, 24.0, "Глава 2 · отношения и функции →").tone(G).size(11.0).text_color("var(--s-accent)").opacity(op(step >= 7)))
        })
        .collect();
    spec(
        &["Итог", "∈", "∪ ∩", "¬", "|A|", "2ⁿ", "Применяли", "Дальше"],
        &[
            "Подведём итог главы",
            "Множество — элементы без порядка и повторов",
            "Операции: объединение, пересечение, разность и дополнение",
            "Законы де Моргана связывают отрицание с этими операциями",
            "Мощность считает элементы",
            "Булеан содержит 2ⁿ подмножеств",
            "Всё это вы уже применяли в сетах и запросах к базам — теперь у инструментов есть точный язык",
            "Дальше — отношения и функции: внешние ключи, связи таблиц, чистые функции",
        ],
        frames,
    )
    .cues(&[1.4, 4.2, 7.8, 11.1, 13.2, 15.3, 21.1])
    .step_ms(2400)
}

#[cfg(test)]
mod tests {
    use super::*;
    use content::Scene;

    /// Компоненты из импортов `slides/dm/ch01.tsx`.
    const IMPORTS: [&str; 13] = [
        "ShapesIntro",
        "ListVsSet",
        "Equality",
        "VennOps",
        "Complement",
        "DeMorgan",
        "Overlap",
        "Subset",
        "Powerset",
        "Explosion",
        "SetsInUse",
        "Contracts",
        "Recap",
    ];

    #[test]
    fn scene_names_match_the_imports() {
        let mut names: Vec<&str> = scenes().iter().map(|(n, _)| *n).collect();
        let mut want = IMPORTS.to_vec();
        names.sort_unstable();
        want.sort_unstable();
        assert_eq!(names, want);
    }

    #[test]
    fn every_scene_compiles_and_fits_the_canvas() {
        for (name, spec) in scenes() {
            let scene = Scene::compile(&spec).unwrap_or_else(|e| panic!("{name}: {e}"));
            assert!(scene.lint().is_empty(), "{name}: {:?}", scene.lint());
        }
    }

    #[test]
    fn steps_captions_and_cues_agree() {
        for (name, spec) in scenes() {
            let n = spec.frames.len();
            assert_eq!(spec.labels.len(), n, "{name}: названий шагов");
            assert_eq!(spec.captions.len(), n, "{name}: подписей");
            let cues = spec.cues.as_ref().unwrap_or_else(|| panic!("{name}: нет меток шагов"));
            assert_eq!(cues.len(), n - 1, "{name}: меток должно быть на одну меньше кадров");
            assert!(cues.windows(2).all(|w| w[0] < w[1]), "{name}: метки не возрастают");
            assert!(spec.height <= 170.0, "{name}: холст выше 170");
        }
    }

    #[test]
    fn powerset_has_eight_distinct_subsets() {
        let names: std::collections::BTreeSet<String> = (0..8).map(subset_name).collect();
        assert_eq!(names.len(), 8);
        assert_eq!(subset_name(5), "{a, c}");
    }
}
