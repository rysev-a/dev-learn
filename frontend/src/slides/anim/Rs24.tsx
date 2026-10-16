import { scene } from "./alg.tsx";
import { Box, rs } from "./rs.tsx";

/* Глава 24 книги «Изучаем Rust»: стандартная библиотека — core, alloc, std и прелюдия. */

const row = (pre: string, items: (string|number)[], c = "g", y = 66, size = 10.5) =>
  items.map((t: string|number, i: number) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Карта", "Идиомы", "Справочник"],
  caption: [
    "Раздел: структура библиотеки, коллекции, текст, ввод-вывод, время, числа, память, трейты",
    "В этой главе: прелюдия, имена методов, комбинаторы Option и Result, mem, cmp, iter",
    "Глава — как оглавление: держите документацию открытой",
  ],
  frames: [
    [...row("a", ["коллекции", "текст", "ввод-вывод", "время"], "b", 66, 9)],
    [...row("a", ["prelude", "Option", "mem", "iter"], "g")],
    [Box("a", 180, 60, 230, 34, "doc.rust-lang.org/std", "y", { size: 11.5 })],
  ],
});

// 2. Слои
export const V02 = scene({
  labels: ["core", "alloc", "std"],
  caption: [
    "core — без ОС и кучи: Option, Result, итераторы, срезы, числа, форматирование",
    "alloc — всё, что требует кучи: Box, Vec, String, Rc, Arc, BTreeMap",
    "std — включает оба и добавляет ОС: файлы, сеть, потоки, время, процессы, HashMap; #![no_std] — только core (и alloc)",
  ],
  frames: [
    [Box("a", 180, 66, 200, 60, "core", "g", { size: 14 })],
    [
      Box("a", 180, 44, 240, 26, "alloc", "b", { size: 12 }),
      Box("b", 180, 100, 200, 60, "core", "g", { size: 14 }),
    ],
    [
      Box("c", 180, 28, 280, 24, "std", "y", { size: 12 }),
      Box("a", 180, 68, 240, 24, "alloc", "b", { size: 12 }),
      Box("b", 180, 108, 200, 40, "core", "g", { size: 14 }),
    ],
  ],
});

// 3. Прелюдия
export const V03 = scene({
  labels: ["Без use", "Трейты", "Остальное — use"],
  caption: [
    "Option, Result, Vec, String, Box доступны в каждом файле автоматически",
    "В прелюдии и трейты: Clone, Copy, Drop, Iterator, ToString, From, Into, PartialEq, PartialOrd, Default",
    "HashMap, файлы, время, потоки подключают через use; «не найден метод» часто = трейт не подключён",
  ],
  frames: [
    [...row("a", ["Option", "Result", "Vec", "String"], "g")],
    [...row("a", ["Clone", "Iterator", "From", "Default"], "b")],
    [
      rs(
        "c",
        20,
        50,
        [
          "use std::collections::HashMap;",
          "use std::fs;",
          "use std::time::Duration;",
        ],
        undefined,
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 4. Карта модулей
export const V04 = scene({
  labels: ["Данные", "Ввод-вывод", "Системные"],
  caption: [
    "std::collections, std::string, std::vec, std::option, std::result, std::iter",
    "std::io, std::fs, std::path, std::net",
    "std::thread, std::sync, std::time, std::env, std::process, std::mem, std::rc, std::cell",
  ],
  frames: [
    [...row("a", ["collections", "string", "option", "iter"], "b", 66, 8.5)],
    [...row("a", ["io", "fs", "path", "net"], "g")],
    [...row("a", ["thread", "sync", "time", "process"], "y", 66, 9.5)],
  ],
});

// 5. Option
export const V05 = scene({
  labels: ["map и and_then", "unwrap_or…", "ok_or, take"],
  caption: [
    "map применяет функцию к значению внутри; and_then связывает операции, возвращающие Option; filter",
    "unwrap_or, unwrap_or_else (лениво), unwrap_or_default; as_ref и as_mut — Option<&T>",
    "ok_or(err) → Result; take() вынимает значение, оставляя None; copied и cloned — из Option<&T>",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "x.map(|v| v + 1)",
          "x.and_then(|v| v.checked_mul(2))",
          "x.filter(|v| *v > 0)",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "x.unwrap_or(0)",
          "x.unwrap_or_else(|| compute())",
          "x.unwrap_or_default()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          'x.ok_or("нет")        // Result',
          "x.take()               // None остаётся",
          "v.first().copied()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 6. Result
export const V06 = scene({
  labels: ["map_err", "ok() и err()", "? и From"],
  caption: [
    "map_err преобразует ошибку; and_then связывает; or_else подставляет другой Result",
    'ok() делает Option из Result, ok_or — обратно; unwrap_or_default; expect("msg") — только в примерах',
    "Оператор ? возвращает ошибку наверх и применяет From: разные типы ошибок объединяются",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "r.map_err(|e| e.to_string())",
          "r.and_then(next_step)",
          "r.or_else(fallback)",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "r.ok()               // Option<T>",
          "r.unwrap_or_default()",
          'r.expect("файл должен быть")',
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn f() -> Result<i32, MyError> {",
          "    let n: i32 = s.parse()?;   // From<ParseIntError>",
          "    Ok(n)",
          "}",
        ],
        [1],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
  ],
});

// 7. Имена
export const V07 = scene({
  labels: ["as_, to_, into_", "is_, try_", "_mut"],
  caption: [
    "as_ — дешёвая ссылка в ссылку; to_ — новое значение (возможно дорого); into_ — забирает владение",
    "is_ задаёт вопрос (bool); try_ может не получиться и вернёт Result или Option",
    "Суффикс _mut — изменяемая версия: iter_mut, get_mut; цена операции видна по имени",
  ],
  frames: [
    [...row("a", ["as_str", "to_string", "into_iter"], "g", 66, 10)],
    [...row("a", ["is_empty", "try_from", "is_ok"], "b", 66, 10)],
    [
      rs(
        "c",
        20,
        50,
        [
          "v.iter()       // &T",
          "v.iter_mut()   // &mut T",
          "v.into_iter()  // T",
        ],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
  ],
});

// 8. mem
export const V08 = scene({
  labels: ["swap", "replace и take", "size_of, drop"],
  caption: [
    "mem::swap(&mut a, &mut b) меняет местами без копирования",
    "replace(&mut x, new) возвращает старое; take(&mut x) оставляет Default — вынуть из &mut",
    "size_of и align_of — размеры; drop — освободить досрочно; forget — почти никогда",
  ],
  frames: [
    [
      rs("c", 20, 50, ["std::mem::swap(&mut a, &mut b);"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let old = mem::replace(&mut s, new_s);",
          "let items = mem::take(&mut self.items);",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["mem::size_of::<T>()", "drop(x);   // раньше срока"],
        undefined,
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
  ],
});

// 9. cmp
export const V09 = scene({
  labels: ["min, max, clamp", "Ordering и then", "Reverse"],
  caption: [
    "cmp::min(a, b), cmp::max, x.clamp(lo, hi) — для любых упорядоченных значений",
    "Ordering: Less, Equal, Greater; a.cmp(&b).then(c.cmp(&d)) — сравнение по нескольким полям",
    "Reverse переворачивает порядок: сортировка по убыванию и куча-минимум; f64 — total_cmp",
  ],
  frames: [
    [
      rs("c", 20, 50, ["cmp::max(3, 7)", "x.clamp(0, 10)"], undefined, {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["a.age.cmp(&b.age)", "    .then(a.name.cmp(&b.name))"],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "v.sort_by_key(|x| Reverse(*x));",
          "xs.sort_by(|a, b| a.total_cmp(b));",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
  ],
});

// 10. convert
export const V10 = scene({
  labels: ["From и Into", "AsRef", "FromStr"],
  caption: [
    "Реализовали From<A> for B — Into получаете даром: let b: B = a.into();",
    "fn f(p: impl AsRef<str>) и impl Into<String> — принимают любую форму строки",
    'FromStr даёт "…".parse::<T>() для своего типа; Display даёт to_string()',
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["impl From<Celsius> for Kelvin { … }", "let k: Kelvin = c.into();"],
        [1],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "fn open(p: impl AsRef<Path>) { … }",
          "fn name(s: impl Into<String>) { … }",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl FromStr for Point { … }",
          'let p: Point = "1,2".parse().unwrap();',
        ],
        [1],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
  ],
});

// 11. iter
export const V11 = scene({
  labels: [
    "once, repeat, empty",
    "successors, from_fn",
    "Адаптеры и потребители",
  ],
  caption: [
    "iter::once(x), repeat(x), empty() — маленькие кирпичики",
    "successors(Some(1), |&x| Some(x * 2)) — последовательность «следующий из предыдущего»; from_fn вызывает замыкание на каждом шаге",
    "chain, zip, cycle, skip, take, step_by — адаптеры; sum, product, count, last, min, max, fold, collect — потребители",
  ],
  frames: [
    [...row("a", ["once", "repeat", "empty"], "b", 66, 10)],
    [
      rs(
        "c",
        20,
        40,
        [
          "iter::successors(Some(1), |&x| Some(x * 2))",
          "    .take(5)   // 1 2 4 8 16",
        ],
        [0],
        { w: 340, size: 8.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "a.iter().chain(b.iter()).zip(c.iter())",
          "    .skip(1).take(3).sum::<i32>()",
        ],
        undefined,
        { w: 340, size: 9, lh: 26 },
      ),
    ],
  ],
});

// 12. env и process
export const V12 = scene({
  labels: ["env", "process", "Документация"],
  caption: [
    'env::args() — аргументы командной строки, env::var("HOME") — переменные окружения',
    'process::exit(code) завершает программу; Command::new("ls") запускает другие программы',
    "rustup doc открывает документацию локально; на doc.rust-lang.org/std — поиск; примеры в ней запускаются как тесты",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "let args: Vec<String> = env::args().collect();",
          'let home = env::var("HOME");',
        ],
        undefined,
        { w: 340, size: 9, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["process::exit(1);", 'Command::new("ls").arg("-l").status()'],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [Box("a", 180, 60, 240, 34, "$ rustup doc --std", "y", { size: 11.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Инструменты", "Дальше"],
  caption: [
    "core, alloc, std; прелюдия; имена методов подсказывают цену и владение",
    "Option и Result — комбинаторы; mem, cmp, convert, iter — ежедневные модули",
    "Следующая глава — коллекции: Vec, VecDeque, HashMap, BTreeMap, BinaryHeap и выбор между ними",
  ],
  frames: [
    [...row("a", ["core", "alloc", "std", "prelude"], "g")],
    [...row("a", ["Option", "mem", "cmp", "iter"], "b")],
    [
      Box(
        "a",
        180,
        60,
        250,
        34,
        "Vec · VecDeque · HashMap · BTreeMap · BinaryHeap",
        "b",
        { size: 8.5 },
      ),
    ],
  ],
});
