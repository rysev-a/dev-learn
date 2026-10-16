import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow, rs, slot } from "./rs.jsx";

/* Глава 14 книги «Изучаем Rust»: словари Python, HashMap, множества. */

const pair = (a, b, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];

// 1. Введение
export const V01 = scene({
  labels: ["dict → HashMap", "Что сравним", "Дальше"],
  caption: [
    "Словарь Python — HashMap в Rust; рядом упорядоченная карта BTreeMap и два вида множеств",
    "Создание, чтение, обновление, подсчёт, перебор, множества",
    "Последняя глава раздела «Rust после Python»; дальше — владение и заимствование",
  ],
  frames: [
    [...pair("dict", "HashMap<K, V>", "m", "g")],
    [
      ...["создать", "читать", "entry", "перебор", "set"].map((t, i) =>
        Box(`a${i}`, 36 + i * 72, 66, 64, 28, t, "b", { size: 9.5 }),
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "владение и заимствование →", "y", {
        size: 11,
      }),
    ],
  ],
});

// 2. Создание
export const V02 = scene({
  labels: ["new и insert", "from и collect", "Ключи"],
  caption: [
    "Литерала нет: HashMap::new() и insert(ключ, значение)",
    "HashMap::from([(k, v), …]) или collect() из итератора пар",
    "Ключ: Hash + Eq — числа, строки, char, кортежи; f64 — нельзя",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut m = HashMap::new();",
          'm.insert("a", 1);',
          'm.insert("b", 2);',
        ],
        [1, 2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          'let m = HashMap::from([("a", 1), ("b", 2)]);',
          "let n: HashMap<_, _> = pairs.into_iter().collect();",
        ],
        undefined,
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
    [...pair("i32, String, char\n(i32, i32)", "f64\nVec<…>?", "g", "r")],
  ],
});

// 3. Чтение
export const V03 = scene({
  labels: ["d[k] → панику", "get → Option", "remove и in"],
  caption: [
    "d[k] при отсутствии ключа — KeyError в Python; m[&k] в Rust — паника: пользуйтесь редко",
    "m.get(&k) → Option<&V>; запасное значение — get(&k).copied().unwrap_or(0); get_mut меняет на месте",
    "k in d → contains_key(&k); d.pop(k) → remove(&k) возвращает Option",
  ],
  frames: [
    [...pair('d["x"]\nKeyError', 'm[&"x"]\npanic', "r", "r")],
    [
      rs(
        "c",
        20,
        40,
        [
          'm.get("a")                 // Some(&1)',
          'm.get("z").copied().unwrap_or(0)',
          'if let Some(v) = m.get_mut("a") { *v += 1; }',
        ],
        undefined,
        { w: 340, size: 8.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['m.contains_key("a")', 'm.remove("a")   // Option<i32>'],
        undefined,
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
  ],
});

// 4. entry
export const V04 = scene({
  labels: ["insert", "entry().or_insert", "Подсчёт слов"],
  caption: [
    "d[k] = v → insert(k, v): при существующем ключе заменяет и возвращает старое значение",
    "entry(k).or_insert(v) вставляет, только если ключа нет, и возвращает &mut V",
    "Counter и defaultdict(int) → *m.entry(w).or_insert(0) += 1 — одна строка, один поиск по ключу",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ['m.insert("a", 1);   // None', 'm.insert("a", 5);   // Some(1)'],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['let e = m.entry("k");', "let v: &mut i32 = e.or_insert(0);"],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "for w in text.split_whitespace() {",
          "    *counts.entry(w).or_insert(0) += 1;",
          "}",
        ],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 5. entry — больше
export const V05 = scene({
  labels: ["or_default", "and_modify", "Группировка"],
  caption: [
    "or_default() вставляет значение по умолчанию: 0, пустой вектор, пустую строку",
    "and_modify(…) меняет, если ключ есть; or_insert_with(…) вычисляет значение лениво",
    "defaultdict(list) → m.entry(k).or_default().push(v) — группировка за один поиск",
  ],
  frames: [
    [
      rs("c", 20, 50, ['m.entry(k).or_default();   // 0, [], ""'], [0], {
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
        ["m.entry(k)", "    .and_modify(|v| *v += 1)", "    .or_insert(1);"],
        [1, 2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut g: HashMap<usize, Vec<&str>> = HashMap::new();",
          "for w in words {",
          "    g.entry(w.len()).or_default().push(w);",
          "}",
        ],
        [2],
        { w: 340, size: 8.5, lh: 22 },
      ),
    ],
  ],
});

// 6. Перебор
export const V06 = scene({
  labels: ["items → iter", "Порядок", "BTreeMap, IndexMap"],
  caption: [
    "items(), keys(), values() → iter(), keys(), values(); iter_mut и values_mut меняют значения",
    "Python помнит порядок вставки; HashMap — произвольный, и он меняется от запуска к запуску",
    "Нужен порядок: отсортируйте ключи, возьмите BTreeMap или пакет indexmap",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "for (k, v) in &m { … }",
          "for k in m.keys() { … }",
          "for v in m.values_mut() { *v += 1; }",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [...pair("порядок вставки\nPython", "случайный\nHashMap", "m", "y")],
    [
      rs(
        "c",
        20,
        40,
        ["let mut keys: Vec<_> = m.keys().collect();", "keys.sort();"],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 7. Хеширование
export const V07 = scene({
  labels: ["Hash и Eq", "SipHash", "derive"],
  caption: [
    "Изменяемых ключей Python (list, dict) нет; в Rust ключ нельзя менять, пока он лежит в карте",
    "Стандартная хеш-функция SipHash со случайной солью защищена от атак; для скорости — FxHash из пакетов",
    "Ключ-структура: #[derive(Hash, PartialEq, Eq)]",
  ],
  frames: [
    [...pair("list как ключ ✕", "&mut ключа ✕\nпока в карте", "r", "r")],
    [...pair("SipHash\nнадёжнее", "FxHash\nбыстрее", "g", "y")],
    [
      rs(
        "c",
        20,
        50,
        ["#[derive(Hash, PartialEq, Eq)]", "struct Pos { x: i32, y: i32 }"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 8. Владение
export const V08 = scene({
  labels: ["insert забирает", "get по &str", "clone"],
  caption: [
    "insert перемещает ключ и значение в карту: после этого строка принадлежит ей",
    'm: HashMap<String, V> ищется и по &str: m.get("ключ") — без создания String',
    "Нужен ключ и снаружи — clone(); значение достают через remove или клонируют",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          'let k = String::from("a");',
          "m.insert(k, 1);",
          "// k больше недоступна",
        ],
        [1, 2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let m: HashMap<String, i32> = …;", 'm.get("a")   // &str подходит'],
        [1],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["m.insert(k.clone(), 1);", 'let owned = m.remove("a");'],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 9. BTreeMap
export const V09 = scene({
  labels: ["Отсортированная", "Диапазоны", "Когда"],
  caption: [
    "BTreeMap хранит пары в дереве: перебор по возрастанию ключа, операции за логарифм",
    "first_key_value, last_key_value, range(a..b) — запросы по диапазонам (в Python — sortedcontainers)",
    "Малые данные и запросы по порядку — BTreeMap; миллионы записей и точный поиск — HashMap",
  ],
  frames: [
    [
      ...[1, 2, 3, 4].map((v, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, String(v), "g", { size: 12 }),
      ),
      Tx("n", 180, 118, "ключи по возрастанию", { size: 10 }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "m.first_key_value()   // Some((&1, …))",
          "m.range(2..4)            // ключи 2 и 3",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      ...pair(
        "BTreeMap\nпорядок, диапазоны",
        "HashMap\nточный поиск",
        "g",
        "b",
      ),
    ],
  ],
});

// 10. Множества
export const V10 = scene({
  labels: ["HashSet и BTreeSet", "Операции", "frozenset"],
  caption: [
    "set → HashSet, упорядоченное → BTreeSet; insert возвращает bool: добавлен ли элемент",
    "union, intersection, difference, symmetric_difference — итераторы, их собирают в новое множество",
    "frozenset не нужен: неизменяемость — это просто let без mut",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "let mut s = HashSet::new();",
          "s.insert(3);   // true",
          "s.insert(3);   // false",
        ],
        [1, 2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "a.union(&b)",
          "a.intersection(&b)",
          "a.difference(&b)",
          "a.symmetric_difference(&b)",
        ],
        undefined,
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [...pair("frozenset", "let s (без mut)", "m", "g")],
  ],
});

// 11. Включения
export const V11 = scene({
  labels: ["Включение", "update → extend", "В вектор"],
  caption: [
    "{w: len(w) for w in words} → words.iter().map(|w| (*w, w.len())).collect::<HashMap<_, _>>()",
    "a | b и a.update(b) → a.extend(b): совпавшие ключи заменяются; копия — clone()",
    "Сортировка по значению: собрать пары в Vec и sort_by(|a, b| b.1.cmp(&a.1))",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "words.iter()",
          "    .map(|w| (*w, w.len()))",
          "    .collect::<HashMap<_, _>>()",
        ],
        [1, 2],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["a.extend(b);   // b пополняет a", "let c = a.clone();"],
        [0],
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut v: Vec<_> = m.into_iter().collect();",
          "v.sort_by(|a, b| b.1.cmp(&a.1));",
        ],
        [1],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
  ],
});

// 12. Производительность
export const V12 = scene({
  labels: ["O(1) в среднем", "with_capacity", "Малые наборы"],
  caption: [
    "Вставка, поиск, удаление — в среднем за константное время; без объектных обёрток быстрее Python",
    "Карта растёт и перехеширует, как dict; HashMap::with_capacity(n) выделяет память заранее",
    "До десятка элементов вектор пар с линейным поиском часто быстрее: нет хеширования, всё рядом — профилируйте",
  ],
  frames: [
    [
      Box("a", 180, 60, 240, 40, "insert · get · remove ≈ O(1)", "g", {
        size: 12,
      }),
    ],
    [
      rs("c", 20, 50, ["let mut m = HashMap::with_capacity(10_000);"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
    [...pair("≤ 10 элементов\nVec<(K, V)>", "много\nHashMap", "y", "g")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "HashMap: get вместо [], entry для счётчиков и групп, порядок произволен; BTreeMap — отсортирована",
    "HashSet и BTreeSet: union, intersection, difference; включения → collect; слияние → extend",
    "Теперь — главная тема языка: владение и заимствование",
  ],
  frames: [
    [
      ...["get", "entry", "BTreeMap", "HashSet"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 10.5 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "*m.entry(k).or_insert(0) += 1;",
          "let u: HashSet<_> = a.union(&b).collect();",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      Box(
        "a",
        180,
        60,
        250,
        34,
        "владение · заимствование · время жизни",
        "b",
        { size: 10.5 },
      ),
    ],
  ],
});
