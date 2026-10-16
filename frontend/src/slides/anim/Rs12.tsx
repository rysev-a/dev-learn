import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 12 книги «Изучаем Rust»: списки Python, массивы и векторы Rust. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const cells = (
  pre: string,
  vals: (string | number)[],
  c = "b",
  y = 66,
  x0 = 40,
  step = 56,
  w = 48,
  size = 12,
) =>
  vals.map((v, i: number) =>
    Box(`${pre}${i}`, x0 + i * step, y, w, 32, String(v), c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["list", "Операции", "Ловушки"],
  caption: [
    "Список — главная структура Python; в Rust ему соответствуют Vec, массив и срез",
    "Добавление, удаление, срезы, копирование, сортировка, включения, очереди",
    "Ловушки: изменение при обходе, общие ссылки, «список списков» — в Rust исчезают или ловятся при сборке",
  ],
  frames: [
    [...pair("list", "Vec / [T; N] / &[T]", "m", "g")],
    [
      ...["push", "срезы", "копии", "sort", "очередь"].map((t, i) =>
        Box(`a${i}`, 36 + i * 72, 66, 64, 28, t, "b", { size: 9.5 }),
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "ошибки — при сборке, а не при запуске", "g", {
        size: 10.5,
      }),
    ],
  ],
});

// 2. Однородность
export const V02 = scene({
  labels: ["list", "Vec и массив", "enum"],
  caption: [
    'Python list: [1, "а", [2]] — любые типы подряд',
    "Vec<T> и [T; N]: все элементы одного типа; кортеж — разные типы, но фиксированной длины",
    "Разные типы в векторе — через enum: каждый вариант хранит своё",
  ],
  frames: [
    [...cells("a", ["1", '"а"', "[2]"], "m", 66, 90, 72, 62, 10)],
    [
      ...cells("a", [1, 2, 3], "g", 50, 90),
      Box("t", 180, 106, 160, 28, '(1, "а", 2.5) — кортеж', "b", { size: 9.5 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["enum Val { Int(i32), Text(String) }", "let v: Vec<Val> = vec![…];"],
        [0],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
  ],
});

// 3. Методы
export const V03 = scene({
  labels: ["append → push", "pop → Option", "remove и in"],
  caption: [
    "append → push; extend → extend; insert → insert; len → len; clear → clear",
    "pop() → pop() возвращает Option: у пустого вектора нет последнего; pop(i) → remove(i)",
    "x in l → contains(&x); l.remove(x) по значению → retain или position + remove",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "l.append(x)   →   v.push(x)",
          "l.extend(m)   →   v.extend(m)",
          "l.insert(i, x) →  v.insert(i, x)",
        ],
        undefined,
        { w: 340, size: 10, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["l.pop()    →   v.pop()      // Option", "l.pop(i)   →   v.remove(i)"],
        [0],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "x in l       →   v.contains(&x)",
          "l.remove(x)  →   v.retain(|&e| e != x)",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
  ],
});

// 4. Индексы и срезы
export const V04 = scene({
  labels: ["l[-1]", "Срез — ссылка", "Шаг и окна"],
  caption: [
    "Отрицательных индексов нет: v.last() или v[v.len() - 1]",
    "Срез Python — копия; &v[a..b] в Rust — ссылка на часть, без копирования",
    "l[::2] → v.iter().step_by(2); chunks(n) режет на куски, windows(n) даёт скользящие окна",
  ],
  frames: [
    [...pair("l[-1]", "v.last()", "m", "g")],
    [...pair("l[1:3] — копия", "&v[1..3] — ссылка", "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "v.iter().step_by(2)",
          "v.chunks(3)      // [1,2,3] [4,5,6]",
          "v.windows(2)     // [1,2] [2,3] [3,4]",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 5. Копирование
export const V05 = scene({
  labels: ["Python: алиас", "Rust: перемещение", "clone и to_vec"],
  caption: [
    "l2 = l — одно значение под двумя именами; копия — copy(), вложенная — deepcopy()",
    "let b = a; перемещает вектор: старая переменная недоступна — случайно получить общий нельзя",
    "a.clone() — глубокая копия; s.to_vec() — вектор из среза",
  ],
  frames: [
    [
      slot("a", 60, 70, "l", "→", "m", { w: 50, h: 36 }),
      slot("b", 60, 118, "l2", "→", "m", { w: 50, h: 36 }),
      arrow("e1", 86, 70, 220, 90, "m"),
      arrow("e2", 86, 118, 220, 100, "m"),
      Box("o", 270, 94, 100, 40, "[1, 2]", "m", { size: 12 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let a = vec![1, 2];",
          "let b = a;     // перемещено",
          "// a недоступна",
        ],
        [1],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let b = a.clone();      // глубокая копия",
          "let c = a[1..].to_vec();",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 6. Изменение при обходе
export const V06 = scene({
  labels: ["Python", "Rust: ошибка сборки", "retain и drain"],
  caption: [
    "Python: удаление из списка в цикле по нему же пропускает элементы — ошибка только на части данных",
    "Rust: цикл держит ссылку на вектор — изменить его одновременно нельзя; ошибка при сборке",
    "Правильно: retain (по условию за один проход), drain (вынуть диапазон), filter + collect",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["for x in l:", "    if x < 0: l.remove(x)   # пропускает"],
        [1],
        { w: 340, size: 10.5, lh: 26, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["for x in &v {", "    v.remove(0);   // ✕ cannot borrow", "}"],
        [1],
        { w: 340, size: 10.5, lh: 24, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "v.retain(|&x| x >= 0);",
          "let d: Vec<i32> = v.drain(1..3).collect();",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
  ],
});

// 7. Сортировка
export const V07 = scene({
  labels: ["sort", "key", "bisect"],
  caption: [
    "sorted(l) → копия + sort(); l.sort() → v.sort() на месте; для f64 — sort_by и partial_cmp",
    "key=… → sort_by_key; reverse=True → sort_by с обратным сравнением",
    "max, min — Option; sum — число; bisect → binary_search: Ok(позиция) или Err(место вставки)",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["v.sort();", "w.sort_by(|a, b| a.partial_cmp(b).unwrap());"],
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
          "v.sort_by_key(|s| s.len());",
          "v.sort_by(|a, b| b.cmp(a));   // убывание",
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
          "v.binary_search(&5)   // Ok(2) или Err(2)",
          "v.iter().max()       // Option",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
  ],
});

// 8. Включения
export const V08 = scene({
  labels: ["Включение", "zip и enumerate", "Ленивость"],
  caption: [
    "[f(x) for x in l if c(x)] → v.iter().filter(c).map(f).collect()",
    "zip склеивает последовательности, enumerate добавляет индексы, windows сравнивает соседей",
    "Пока нет collect, sum или for — ничего не вычисляется; fold собирает любой результат",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "v.iter()",
          "    .filter(|x| **x > 0)",
          "    .map(|x| x * 2)",
          "    .collect::<Vec<_>>()",
        ],
        [1, 2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "a.iter().zip(b.iter())",
          "v.iter().enumerate()",
          "v.windows(2).all(|w| w[0] <= w[1])",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let s = v.iter().fold(0, |acc, x| acc + x);",
          "let it = v.iter().map(|x| x + 1);  // ничего не считает",
        ],
        [1],
        { w: 340, size: 8.5, lh: 26 },
      ),
    ],
  ],
});

// 9. Ёмкость
export const V09 = scene({
  labels: ["len и capacity", "Рост ×2", "with_capacity"],
  caption: [
    "len — сколько элементов, capacity — сколько поместится без нового выделения памяти",
    "Когда ёмкость кончается, вектор выделяет вдвое больше и копирует старые данные — как список Python",
    "Vec::with_capacity(1000) и reserve(n) выделяют память один раз; shrink_to_fit возвращает лишнее",
  ],
  frames: [
    [
      ...cells("a", [1, 2, 3], "g", 56, 50),
      ...cells("b", ["", ""], "m", 56, 218, 56, 48),
      Tx("n", 180, 110, "len = 3, capacity = 5", { size: 10.5 }),
    ],
    [
      Box("a", 100, 60, 120, 34, "cap 4 → полно", "y", { size: 10.5 }),
      arrow("e", 168, 60, 212, 60, "g"),
      Box("b", 270, 60, 110, 34, "cap 8 + копия", "g", { size: 10.5 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let mut v = Vec::with_capacity(1000);", "v.reserve(500);"],
        [0],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 10. Разнородные данные
export const V10 = scene({
  labels: ["enum", "Box<dyn Trait>", "Выбор"],
  caption: [
    "Вектор перечислений: все варианты известны, match обрабатывает каждый",
    "Вектор Box<dyn Trait>: любая структура с нужным трейтом — для расширяемых систем",
    "Фиксированный набор — enum; открытый набор — трейт-объекты (разберём в главе про трейты)",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["let v = vec![Shape::Circle(1.0), Shape::Rect(2.0, 3.0)];"],
        undefined,
        { w: 340, size: 8, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let v: Vec<Box<dyn Plugin>> = vec![",
          "    Box::new(A), Box::new(B),",
          "];",
        ],
        undefined,
        { w: 340, size: 10, lh: 22 },
      ),
    ],
    [...pair("enum\nзакрытый набор", "dyn Trait\nоткрытый набор", "b", "g")],
  ],
});

// 11. Очередь и стек
export const V11 = scene({
  labels: ["Стек", "VecDeque", "BinaryHeap"],
  caption: [
    "Vec — стек: push и pop в конце за константное время",
    "Очередь: Python deque → VecDeque; вставка и удаление в начале Vec — линейные, не подходит",
    "heapq → BinaryHeap: быстрый максимум; все — в стандартной библиотеке",
  ],
  frames: [
    [
      ...cells("a", [1, 2, 3], "b", 66, 90),
      Box("p", 290, 66, 50, 32, "push/pop", "g", { size: 8.5 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "push_back\npop_front", "b", { size: 10 }),
      Box("b", 270, 60, 130, 34, "VecDeque", "g", { size: 12 }),
    ],
    [...pair("heapq", "BinaryHeap", "m", "g")],
  ],
});

// 12. Двумерные
export const V12 = scene({
  labels: ["Ловушка Python", "vec![vec![…]]", "Плоский вектор"],
  caption: [
    "[[0] * n] * m — все строки один список: изменение одной меняет все",
    "vec![vec![0; n]; m] клонирует внутренний вектор для каждой строки: строки независимы",
    "Для скорости — один плоский Vec и индекс row * width + col",
  ],
  frames: [
    [
      ...[0, 1, 2].map((i) =>
        Box(`r${i}`, 60, 40 + i * 28, 70, 22, "→", "m", { size: 10 }),
      ),
      Box("o", 270, 66, 100, 40, "[0, 0, 0]", "m", { size: 11 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut g = vec![vec![0; 3]; 2];",
          "g[0][1] = 5;   // только первая строка",
        ],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let w = 3;", "let mut a = vec![0; w * 2];", "a[row * w + col] = 5;"],
        [2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "Vec однороден, срезы — ссылки, копирование явное, изменение при обходе — retain и drain",
    "Разнотипность — enum или dyn Trait; очередь — VecDeque; куча — BinaryHeap; сетка — vec![vec![…]]",
    "Следующая глава — классы, трейты и перегрузка операторов",
  ],
  frames: [
    [
      ...["Vec", "&[T]", "clone", "retain"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 10.5 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let mut v = vec![3, 1, 2];", "v.sort(); v.retain(|&x| x > 1);"],
        undefined,
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "class ↔ struct + impl + trait", "b", {
        size: 11,
      }),
    ],
  ],
});
