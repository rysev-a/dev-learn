import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs } from "./rs.tsx";

/* Глава 25 книги «Изучаем Rust»: коллекции std. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre: string, items: (string|number)[], c = "g", y = 66, size = 10.5) =>
  items.map((t: string|number, i: number) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );
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
  labels: ["Восемь коллекций", "Правило выбора", "Измеряйте"],
  caption: [
    "Vec, VecDeque, LinkedList, HashMap, HashSet, BTreeMap, BTreeSet, BinaryHeap",
    "Начинайте с Vec; другую берите, когда логика или замеры потребовали",
    "В большинстве программ хватает Vec и HashMap",
  ],
  frames: [
    [
      ...row("a", ["Vec", "VecDeque", "HashMap", "BTreeMap"], "b", 50, 9),
      ...row("b", ["HashSet", "BTreeSet", "Heap", "List"], "g", 96, 9),
    ],
    [Box("a", 180, 60, 230, 34, "Vec — по умолчанию", "g", { size: 12 })],
    [...pair("Vec + HashMap", "остальное\nпо нужде", "g", "y")],
  ],
});

// 2. Vec
export const V02 = scene({
  labels: ["ptr, len, cap", "O(1) и O(n)", "swap_remove, retain"],
  caption: [
    "В стеке три слова: указатель, длина, ёмкость; элементы лежат в куче подряд",
    "push — амортизированно O(1); insert и remove в середине сдвигают хвост — O(n)",
    "swap_remove — O(1), если порядок не важен; truncate, drain, split_off, extend, retain, dedup",
  ],
  frames: [
    [
      Box("p", 80, 40, 110, 24, "ptr", "b", { size: 10 }),
      Box("l", 80, 70, 110, 24, "len", "b", { size: 10 }),
      Box("c", 80, 100, 110, 24, "cap", "b", { size: 10 }),
      ...cells("v", [1, 2, 3, 4], "g", 70, 170, 46, 40, 11),
    ],
    [...pair("push\nамортиз. O(1)", "insert, remove\nO(n)", "g", "y")],
    [
      rs(
        "c",
        20,
        40,
        [
          "v.swap_remove(i);   // O(1)",
          "v.retain(|&x| x > 0);",
          "v.drain(1..3);",
        ],
        [0],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 3. Срезы
export const V03 = scene({
  labels: ["Окна и пачки", "Поиск и склейка", "Сортировка"],
  caption: [
    "windows(n), chunks(n), split(|x| …), split_first(), first(), last()",
    "contains, starts_with, concat, join, rotate_left, fill, copy_from_slice, swap",
    "sort — устойчива, sort_unstable — быстрее; sort_by_key; binary_search на отсортированном",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "v.windows(2)",
          "v.chunks(3)",
          "v.split_first()   // Option<(&T, &[T])>",
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
          "v.concat()   v.join(&0)",
          "v.rotate_left(2)",
          "v.fill(0)   v.copy_from_slice(&w)",
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
          "v.sort();           // устойчивая",
          "v.sort_unstable();  // быстрее",
          "v.binary_search(&x)",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 4. VecDeque
export const V04 = scene({
  labels: ["Кольцо", "Оба конца", "as_slices"],
  caption: [
    "VecDeque — кольцевой буфер: начало может быть в любом месте области памяти",
    "push_front, push_back, pop_front, pop_back — O(1); индексация как у Vec",
    "Элементы не обязательно подряд: as_slices возвращает два среза, make_contiguous собирает в один",
  ],
  frames: [
    [...cells("a", ["", "", "1", "2", "3", ""], "m", 66, 45, 54, 46, 12)],
    [
      rs(
        "c",
        20,
        40,
        ["q.push_back(x);", "let x = q.pop_front();", "q.push_front(y);"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let (a, b) = q.as_slices();", "q.make_contiguous();"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 5. HashMap
export const V05 = scene({
  labels: ["Swiss table", "Рост", "Методы"],
  caption: [
    "Таблица hashbrown: метки хеша хранятся отдельно; сравнение по 16 меток SIMD-инструкциями",
    "Вставка и поиск O(1) в среднем; при заполнении — рост вдвое и перехеширование; with_capacity и reserve",
    "retain, drain, extend, entry; порядок обхода зависит от хеша и случайной соли",
  ],
  frames: [
    [
      ...cells("h", ["a", "b", "c", "d"], "m", 46, 60, 66, 54, 11),
      ...cells("v", ["·", "·", "·", "·"], "g", 100, 60, 66, 54, 11),
      Tx("n", 180, 140, "метки хеша — отдельно", { size: 9 }),
    ],
    [...pair("cap 8\n→ 16 + rehash", "reserve(n)\nзаранее", "y", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "m.retain(|_, v| *v > 0);",
          "m.extend(other);",
          "for (k, v) in m.drain() { … }",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 6. HashSet
export const V06 = scene({
  labels: ["Ключи без значений", "Предикаты", "Когда"],
  caption: [
    "HashSet<T> — HashMap<T, ()>: поиск, вставка, удаление — O(1) в среднем",
    "is_subset, is_superset, is_disjoint; union, intersection, difference — итераторы; take и retain",
    "Только членство: дубликаты, посещённые вершины, уникальные слова; упорядоченный вариант — BTreeSet",
  ],
  frames: [
    [
      ...cells("a", [1, 2, 3], "g", 66, 90, 66, 54, 12),
      Tx("n", 180, 110, "без значений", { size: 10 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["a.is_subset(&b)", "a.is_disjoint(&b)", "a.intersection(&b)"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [...pair("членство", "BTreeSet\nпорядок", "g", "b")],
  ],
});

// 7. BTreeMap
export const V07 = scene({
  labels: ["B-дерево", "Крайние и диапазоны", "Когда"],
  caption: [
    "Узел хранит до 11 ключей и помещается в несколько строк кэша; операции O(log n)",
    "first_key_value, last_key_value, pop_first, pop_last, range(a..b), split_off — порядок возрастания ключа",
    "Нужны порядок, диапазоны, предсказуемый вывод — BTreeMap; иначе HashMap",
  ],
  frames: [
    [
      Box("r", 180, 36, 120, 28, "5 · 10", "b", { size: 11 }),
      Box("a", 100, 100, 100, 28, "1 · 2 · 3", "g", { size: 10 }),
      Box("b", 180, 100, 80, 28, "6 · 8", "g", { size: 10 }),
      Box("c", 266, 100, 100, 28, "12 · 15", "g", { size: 10 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["m.first_key_value()", "m.pop_last()", "m.range(10..20)"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [...pair("порядок\nBTreeMap", "скорость\nHashMap", "b", "g")],
  ],
});

// 8. BinaryHeap
export const V08 = scene({
  labels: ["Куча-максимум", "push, pop, peek", "Reverse"],
  caption: [
    "Вектор, где родитель не меньше детей: наибольший всегда первый",
    "push и pop — O(log n), peek — O(1); BinaryHeap::from(vec) — O(n); into_sorted_vec",
    "Куча-минимум: BinaryHeap<Reverse<T>>; основа Дейкстры, планировщиков, top-k",
  ],
  frames: [
    [
      Box("r", 180, 36, 50, 28, "9", "g", { size: 12 }),
      Box("a", 130, 86, 50, 28, "7", "b", { size: 12 }),
      Box("b", 230, 86, 50, 28, "5", "b", { size: 12 }),
      Box("c", 100, 134, 40, 24, "3", "m", { size: 10 }),
      Box("d", 160, 134, 40, 24, "6", "m", { size: 10 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "h.push(x);",
          "h.peek()    // Option<&T>",
          "h.pop()     // наибольший",
        ],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let mut h = BinaryHeap::new();",
          "h.push(Reverse(5));   // минимум первым",
        ],
        [1],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 9. LinkedList
export const V09 = scene({
  labels: ["Разбросанные узлы", "Что даёт", "Рекомендация"],
  caption: [
    "LinkedList: узлы в куче в случайных местах — обход с промахами кэша",
    "Единственные плюсы: split_off и append за O(1), без перераспределения",
    "Документация сама рекомендует Vec и VecDeque вместо списка",
  ],
  frames: [
    [
      Box("a", 70, 66, 60, 30, "1", "m", { size: 12 }),
      arrow("e1", 100, 66, 130, 90, "m"),
      Box("b", 150, 100, 60, 30, "2", "m", { size: 12 }),
      arrow("e2", 180, 100, 230, 50, "m"),
      Box("c", 260, 40, 60, 30, "3", "m", { size: 12 }),
    ],
    [...pair("split_off\nappend: O(1)", "обход\nмедленный", "g", "r")],
    [
      Box("a", 180, 60, 240, 34, "Vec и VecDeque — почти всегда", "g", {
        size: 11.5,
      }),
    ],
  ],
});

// 10. Общий интерфейс
export const V10 = scene({
  labels: ["iter, iter_mut, into_iter", "FromIterator", "extend, drain"],
  caption: [
    "Каждая коллекция: iter (читать), iter_mut (менять), into_iter (забрать)",
    "collect собирает не только Vec: HashMap, String, Result<Vec<_>, _>, Option<Vec<_>>",
    "extend принимает любой итератор; drain(диапазон) вынимает элементы",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "for x in &c { }",
          "for x in &mut c { }",
          "for x in c { }   // забирает",
        ],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let m: HashMap<_, _> = it.collect();",
          "let r: Result<Vec<i32>, _> = it.collect();",
        ],
        undefined,
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["c.extend(other_iter);", "let part: Vec<_> = c.drain(..2).collect();"],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 11. Сложности
export const V11 = scene({
  labels: ["Таблица", "Кэш решает", "Замеряйте"],
  caption: [
    "Vec: индекс O(1), push O(1)*, вставка O(n); Deque: концы O(1); Hash: O(1)*; BTree и Heap: O(log n)",
    "Константа константе рознь: при малых n Vec обгоняет всех из-за кэша процессора",
    "Выбирайте по логике задачи, замеряйте на реальных данных (criterion, cargo bench)",
  ],
  frames: [
    [
      ...row(
        "a",
        ["Vec O(1)", "Deque O(1)", "Hash O(1)", "BTree log n"],
        "b",
        66,
        9,
      ),
    ],
    [...pair("малые n\nVec", "большие n\nHash, BTree", "g", "b")],
    [
      Box("a", 180, 60, 230, 34, "cargo bench · criterion", "y", {
        size: 11.5,
      }),
    ],
  ],
});

// 12. Внешние пакеты
export const V12 = scene({
  labels: ["indexmap, smallvec", "arrayvec, slab", "dashmap"],
  caption: [
    "indexmap — порядок вставки; smallvec — несколько элементов на стеке, потом куча",
    "arrayvec — фиксированная ёмкость на стеке; slab и slotmap — числовые идентификаторы объектов; bitvec",
    "dashmap — параллельная HashMap; подключаются через cargo, начинайте со стандартной библиотеки",
  ],
  frames: [
    [...pair("indexmap", "smallvec", "b", "g")],
    [...pair("arrayvec", "slab, slotmap", "b", "g")],
    [Box("a", 180, 60, 230, 34, "DashMap<K, V>", "y", { size: 12 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Выбор", "Правила", "Дальше"],
  caption: [
    "Vec; VecDeque — очередь; HashMap и HashSet — поиск; BTree — порядок; BinaryHeap — приоритеты",
    "Сложности подсказывают, кэш решает; общий интерфейс итераторов; внешние пакеты — по необходимости",
    "Следующая глава — текст и форматирование: char, str, fmt и разбор",
  ],
  frames: [
    [...row("a", ["Vec", "Deque", "Hash", "Heap"], "g")],
    [
      rs(
        "c",
        20,
        40,
        ["let m: HashMap<_, _> = it.collect();", "v.sort_unstable();"],
        undefined,
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [Box("a", 180, 60, 230, 34, "char · str · fmt · parse", "b", { size: 12 })],
  ],
});
