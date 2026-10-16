import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 6 книги «Базы данных»: объединение таблиц JOIN. */

const CU = [
  [1, "Анна"],
  [2, "Борис"],
  [3, "Вера"],
  [4, "Глеб"],
] as const;
const OR = [
  [101, 1, 79500],
  [102, 1, 5200],
  [103, 2, 55400],
] as const;
const code = { w: 340, size: 10, lh: 14 };
const CUT = (hot: number[] = [], dim: number[] = [], x = 14) => tbl("c", x, 56, ["id", "name"], CU, [26, 56], { size: 8, hot, dim });
const ORT = (hot: number[] = [], dim: number[] = [], x = 150) => tbl("o", x, 56, ["id", "cust", "total"], OR, [30, 36, 50], { size: 8, hot, dim });

// 1. Данные в разных таблицах
export const V01 = scene({
  labels: ["Две таблицы", "Связь", "Склейка"],
  caption: [
    "Клиенты и заказы лежат в разных таблицах",
    "customer_id в заказе указывает на id клиента",
    "JOIN склеивает связанные строки в одну: клиент рядом со своим заказом",
  ],
  frames: [
    [...CUT(), ...ORT()],
    [...CUT([0, 1], [2, 3]), ...ORT([0, 1, 2]), Tx("n", 180, 150, "o.cust = c.id", { size: 9.5, c: "g" })],
    [
      ...tbl("r", 40, 56, ["name", "order", "total"], [["Анна", 101, 79500], ["Анна", 102, 5200], ["Борис", 103, 55400]], [70, 70, 90], { size: 8.5, hot: [0, 1, 2] }),
      Tx("n", 180, 140, "строки склеены", { size: 9.5 }),
    ],
  ],
});

// 2. Каждая с каждой
const L = ["Анна", "Борис"];
const R = ["S", "M", "L"];
export const V02 = scene({
  labels: ["Две таблицы", "Все пары", "Условие нужно"],
  caption: [
    "Две таблицы: два клиента и три размера",
    "Без условия получаем каждую пару: 2 × 3 = 6 строк",
    "С клиентами и заказами: 4 × 3 = 12 строк, осмысленных только 3",
  ],
  frames: [
    [
      ...L.map((n, i) => Box(`l${i}`, 80, 56 + i * 34, 70, 26, n, "b", { size: 9.5 })),
      ...R.map((n, i) => Box(`r${i}`, 280, 40 + i * 34, 50, 26, n, "b", { size: 9.5 })),
    ],
    [
      ...L.flatMap((a, i) => R.map((b, j) => Box(`p${i}${j}`, 70 + j * 100, 60 + i * 44, 86, 30, `${a} × ${b}`, "g", { size: 9.5 }))),
      Tx("n", 180, 150, "6 пар", { size: 10 }),
    ],
    [
      Box("a", 70, 70, 100, 36, "customers\n4 строки", "b", { size: 9.5 }),
      Tx("x", 130, 70, "×", { size: 16 }),
      Box("b", 190, 70, 100, 36, "orders\n3 строки", "b", { size: 9.5 }),
      Tx("e", 245, 70, "=", { size: 16 }),
      Box("c", 315, 70, 76, 36, "12 пар", "r", { size: 11 }),
      Tx("n", 180, 130, "осмысленных — только 3", { size: 9.5 }),
    ],
  ],
});

// 3. INNER JOIN
export const V03 = scene({
  labels: ["Запрос", "Совпавшие пары", "Результат"],
  caption: [
    "INNER JOIN … ON: условие связывает внешний ключ с первичным",
    "Пары находятся там, где o.customer_id = c.id; у Веры и Глеба пары нет",
    "В результат попадают только совпавшие пары",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT c.name, o.total", "FROM customers c", "JOIN orders o ON o.cust = c.id;"], [2], { ...code, lh: 13 }), ...CUT([], [], 14).map((e) => ({ ...e, y: (e.y ?? 0) + 6 })), ...ORT([], [], 150).map((e) => ({ ...e, y: (e.y ?? 0) + 6 }))],
    [sql("c", 10, 14, ["SELECT c.name, o.total", "FROM customers c", "JOIN orders o ON o.cust = c.id;"], [2], { ...code, lh: 13 }), ...CUT([0, 1], [2, 3], 14).map((e) => ({ ...e, y: (e.y ?? 0) + 6 })), ...ORT([0, 1, 2], [], 150).map((e) => ({ ...e, y: (e.y ?? 0) + 6 }))],
    [sql("c", 10, 14, ["SELECT c.name, o.total", "FROM customers c", "JOIN orders o ON o.cust = c.id;"], [2], { ...code, lh: 13 }), ...tbl("r", 90, 76, ["name", "total"], [["Анна", 79500], ["Анна", 5200], ["Борис", 55400]], [80, 80], { size: 8.5, hot: [0, 1, 2] })],
  ],
});

// 4. Имена и псевдонимы
export const V04 = scene({
  labels: ["Неоднозначно", "Таблица.столбец", "Псевдонимы"],
  caption: [
    "id есть и в customers, и в orders — база не знает, какой имеется в виду",
    "Перед столбцом ставят имя таблицы и точку",
    "Короткие псевдонимы c и o после имён таблиц делают запрос компактным",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT id, name", "FROM customers JOIN orders", "  ON cust = id;"], undefined, { ...code, bad: [0, 2] }), Box("e", 180, 110, 300, 28, "ошибка: ambiguous column name: id", "r", { size: 9.5 })],
    [sql("c", 10, 14, ["SELECT customers.id, name", "FROM customers JOIN orders", "  ON orders.cust = customers.id;"], [0, 2], { ...code, size: 9.5 }), Tx("n", 180, 120, "длинно, но однозначно", { size: 9.5, c: "y" })],
    [sql("c", 10, 14, ["SELECT c.id, c.name", "FROM customers c JOIN orders o", "  ON o.cust = c.id;"], [0, 1, 2], code), Tx("n", 180, 120, "c и o — псевдонимы таблиц", { size: 9.5, c: "g" })],
  ],
});

// 5. ON и WHERE
export const V05 = scene({
  labels: ["Соединили", "Отфильтровали", "То же в ON"],
  caption: [
    "Сначала получаем все пары клиент–заказ",
    "WHERE оставляет заказы дороже 10 000",
    "Для INNER JOIN условие можно перенести в ON — результат тот же",
  ],
  frames: [
    [
      sql("c", 10, 14, ["FROM customers c JOIN orders o ON o.cust = c.id"], [0], { ...code, size: 9 }),
      ...tbl("r", 90, 50, ["name", "total"], [["Анна", 79500], ["Анна", 5200], ["Борис", 55400]], [80, 80], { size: 8.5 }),
    ],
    [
      sql("c", 10, 14, ["FROM customers c JOIN orders o ON o.cust = c.id", "WHERE o.total > 10000"], [1], { ...code, size: 9 }),
      ...tbl("r", 90, 60, ["name", "total"], [["Анна", 79500], ["Анна", 5200], ["Борис", 55400]], [80, 80], { size: 8.5, hot: [0, 2], dim: [1] }),
    ],
    [
      sql("c", 10, 14, ["FROM customers c JOIN orders o", "  ON o.cust = c.id AND o.total > 10000"], [1], { ...code, size: 9 }),
      ...tbl("r", 90, 60, ["name", "total"], [["Анна", 79500], ["Борис", 55400]], [80, 80], { size: 8.5, hot: [0, 1] }),
      Tx("n", 300, 100, "результат\nтот же", { size: 8.5, c: "g" }),
    ],
  ],
});

// 6. LEFT JOIN
const LJ = [
  ["Анна", 101],
  ["Анна", 102],
  ["Борис", 103],
  ["Вера", "NULL"],
  ["Глеб", "NULL"],
] as const;
export const V06 = scene({
  labels: ["INNER", "LEFT", "Пустые справа"],
  caption: [
    "INNER JOIN теряет клиентов без заказов — Веры и Глеба нет",
    "LEFT JOIN сохраняет всех клиентов из левой таблицы",
    "Где пары нет, столбцы правой таблицы заполняются NULL",
  ],
  frames: [
    [sql("c", 10, 14, ["FROM customers c JOIN orders o ON …"], [0], code), ...tbl("r", 90, 44, ["name", "order"], LJ.slice(0, 3), [80, 70], { size: 8.5, hot: [0, 1, 2] }), Tx("n", 300, 120, "Веры и Глеба\nнет", { size: 8.5, c: "r" })],
    [sql("c", 10, 14, ["FROM customers c LEFT JOIN orders o ON …"], [0], code), ...tbl("r", 90, 44, ["name", "order"], LJ, [80, 70], { size: 8.5, hot: [0, 1, 2, 3, 4] })],
    [sql("c", 10, 14, ["FROM customers c LEFT JOIN orders o ON …"], [0], code), ...tbl("r", 90, 44, ["name", "order"], LJ, [80, 70], { size: 8.5, hot: [3, 4], dim: [0, 1, 2], c: "y" }), Tx("n", 300, 120, "NULL — пары\nнет", { size: 8.5, c: "y" })],
  ],
});

// 7. Кто без пары
export const V07 = scene({
  labels: ["LEFT JOIN", "IS NULL", "NOT EXISTS"],
  caption: [
    "Делаем LEFT JOIN: у клиентов без заказов правая часть пуста",
    "WHERE o.id IS NULL оставляет только их: Вера и Глеб",
    "NOT EXISTS даёт тот же результат: нет заказа этого клиента",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT c.name FROM customers c", "LEFT JOIN orders o ON o.cust = c.id;"], [1], code), ...tbl("r", 90, 54, ["name", "o.id"], LJ, [80, 60], { size: 8, hot: [], dim: [] })],
    [sql("c", 10, 14, ["SELECT c.name FROM customers c", "LEFT JOIN orders o ON o.cust = c.id", "WHERE o.id IS NULL;"], [2], { ...code, lh: 13 }), ...tbl("r", 90, 64, ["name", "o.id"], LJ, [80, 60], { size: 8, cell: 16, hot: [3, 4], dim: [0, 1, 2], c: "y" })],
    [sql("c", 10, 14, ["SELECT name FROM customers c", "WHERE NOT EXISTS (SELECT 1 FROM orders o", "                  WHERE o.cust = c.id);"], [1, 2], { ...code, lh: 13, size: 9.5 }), ...tbl("r", 120, 80, ["name"], [["Вера"], ["Глеб"]], [100], { size: 9, hot: [0, 1] })],
  ],
});

// 8. Ловушка
export const V08 = scene({
  labels: ["Условие в WHERE", "Потеряли клиентов", "Условие в ON"],
  caption: [
    "LEFT JOIN, а статус заказа проверяем в WHERE",
    "У Веры и Глеба status = NULL — условие не проходит, строки исчезли",
    "Перенесли условие в ON: клиенты сохранены, а чужие заказы отброшены",
  ],
  frames: [
    [sql("c", 10, 14, ["FROM customers c LEFT JOIN orders o", "  ON o.cust = c.id", "WHERE o.status = 'paid'"], [2], { ...code, lh: 13 }), ...tbl("r", 90, 66, ["name", "status"], [["Анна", "shipped"], ["Борис", "paid"], ["Вера", "NULL"], ["Глеб", "NULL"]], [80, 80], { size: 8.5 })],
    [sql("c", 10, 14, ["FROM customers c LEFT JOIN orders o", "  ON o.cust = c.id", "WHERE o.status = 'paid'"], [2], { ...code, lh: 13 }), ...tbl("r", 90, 66, ["name", "status"], [["Анна", "shipped"], ["Борис", "paid"], ["Вера", "NULL"], ["Глеб", "NULL"]], [80, 80], { size: 8.5, hot: [1], dim: [0, 2, 3], c: "r" }), Tx("n", 300, 120, "осталась 1 строка", { size: 8.5, c: "r" })],
    [sql("c", 10, 14, ["FROM customers c LEFT JOIN orders o", "  ON o.cust = c.id AND o.status = 'paid'"], [1], { ...code, lh: 13, size: 9.5 }), ...tbl("r", 90, 52, ["name", "status"], [["Анна", "NULL"], ["Борис", "paid"], ["Вера", "NULL"], ["Глеб", "NULL"]], [80, 80], { size: 8.5, hot: [1] }), Tx("n", 300, 120, "все 4 клиента", { size: 8.5, c: "g" })],
  ],
});

// 9. RIGHT и FULL
export const V09 = scene({
  labels: ["LEFT и RIGHT", "FULL", "CROSS"],
  caption: [
    "RIGHT — зеркальный LEFT: сохраняются строки правой таблицы",
    "FULL сохраняет строки обеих таблиц, недостающее — NULL с обеих сторон",
    "CROSS — все пары без условия",
  ],
  frames: [
    [
      Box("a", 70, 60, 110, 34, "LEFT\nвсе слева", "g", { size: 9.5 }),
      Box("b", 290, 60, 110, 34, "RIGHT\nвсе справа", "g", { size: 9.5 }),
      Tx("n", 180, 110, "RIGHT = LEFT с обменом таблиц", { size: 9.5 }),
    ],
    [
      Box("a", 70, 60, 110, 34, "слева есть,\nсправа нет", "y", { size: 9 }),
      Box("b", 180, 60, 90, 34, "обе\nстороны", "g", { size: 9 }),
      Box("c", 290, 60, 110, 34, "справа есть,\nслева нет", "y", { size: 9 }),
      Tx("n", 180, 110, "FULL JOIN: все три группы (SQLite ≥ 3.39)", { size: 9.5 }),
    ],
    [Box("a", 70, 60, 110, 34, "n строк", "b", { size: 10 }), Tx("x", 140, 60, "×", { size: 16 }), Box("b", 210, 60, 110, 34, "m строк", "b", { size: 10 }), Tx("n", 180, 110, "результат: n × m", { size: 10, c: "r" })],
  ],
});

// 10. Цепочка таблиц
export const V10 = scene({
  labels: ["Четыре таблицы", "Цепочка JOIN", "Результат"],
  caption: [
    "Чтобы узнать, кто что купил, нужны клиенты, заказы, позиции и товары",
    "Подключаем по одной: каждая новая таблица — своя связь в ON",
    "Каждая строка результата — клиент, заказ и купленный товар",
  ],
  frames: [
    [
      Box("c", 50, 60, 76, 30, "customers", "b", { size: 8.5 }),
      Box("o", 140, 60, 70, 30, "orders", "b", { size: 8.5 }),
      Box("i", 230, 60, 86, 30, "order_items", "b", { size: 8.5 }),
      Box("p", 320, 60, 70, 30, "products", "b", { size: 8.5 }),
    ],
    [
      Box("c", 50, 60, 76, 30, "customers", "g", { size: 8.5 }),
      Box("o", 140, 60, 70, 30, "orders", "g", { size: 8.5 }),
      Box("i", 230, 60, 86, 30, "order_items", "g", { size: 8.5 }),
      Box("p", 320, 60, 70, 30, "products", "g", { size: 8.5 }),
      arrow("a1", 90, 60, 105, 60, "g"),
      arrow("a2", 175, 60, 185, 60, "g"),
      arrow("a3", 273, 60, 285, 60, "g"),
      Tx("n", 180, 110, "JOIN … ON … JOIN … ON … JOIN … ON …", { size: 9 }),
    ],
    [...tbl("r", 20, 50, ["name", "order", "title"], [["Анна", 101, "Ноутбук"], ["Анна", 101, "Мышь"], ["Борис", 103, "Смартфон"]], [80, 70, 110], { size: 8.5, hot: [0, 1, 2] })],
  ],
});

// 11. Размножение строк
export const V11 = scene({
  labels: ["Заказ и позиции", "JOIN размножил", "Сумма втрое больше"],
  caption: [
    "Заказ на 100 рублей с тремя позициями",
    "После JOIN строк три, и total повторяется в каждой",
    "SUM(o.total) = 300 вместо 100; считайте до соединения или по уникальным заказам",
  ],
  frames: [
    [Box("o", 70, 70, 100, 40, "заказ 1\ntotal = 100", "b", { size: 10 }), ...[0, 1, 2].map((i) => Box(`i${i}`, 280, 40 + i * 32, 90, 24, `позиция ${i + 1}`, "b", { size: 9 }))],
    [...tbl("r", 90, 50, ["order", "total", "item"], [[1, 100, "A"], [1, 100, "B"], [1, 100, "C"]], [50, 50, 50], { size: 9, hot: [0, 1, 2] }), Tx("n", 180, 140, "заказ 1 повторился 3 раза", { size: 9 })],
    [...tbl("r", 90, 40, ["order", "total", "item"], [[1, 100, "A"], [1, 100, "B"], [1, 100, "C"]], [50, 50, 50], { size: 8.5 }), Box("s", 180, 130, 200, 28, "SUM(total) = 300  (верно 100)", "r", { size: 9.5 })],
  ],
});

// 12. Самосоединение
const EMP = [
  [1, "Ольга", "NULL"],
  [2, "Пётр", 1],
  [3, "Рита", 1],
  [4, "Сергей", 2],
] as const;
export const V12 = scene({
  labels: ["Одна таблица", "Две копии", "Пары"],
  caption: [
    "В сотрудниках у каждого есть boss_id — номер начальника из той же таблицы",
    "Берём таблицу дважды под псевдонимами e и b",
    "Каждый сотрудник рядом с начальником; у Ольги начальника нет — нужен LEFT JOIN",
  ],
  frames: [
    [...tbl("t", 80, 40, ["id", "name", "boss_id"], EMP, [30, 70, 60], { size: 8.5 })],
    [sql("c", 10, 14, ["FROM employees e", "JOIN employees b ON e.boss_id = b.id"], [0, 1], code), ...tbl("t", 80, 62, ["id", "name", "boss_id"], EMP, [30, 70, 60], { size: 8, hot: [1, 2, 3], dim: [0] })],
    [sql("c", 10, 14, ["FROM employees e", "LEFT JOIN employees b ON e.boss_id = b.id"], [1], code), ...tbl("r", 90, 54, ["сотрудник", "начальник"], [["Ольга", "NULL"], ["Пётр", "Ольга"], ["Рита", "Ольга"], ["Сергей", "Пётр"]], [80, 80], { size: 8.5, hot: [1, 2, 3] })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Виды", "Правила", "Дальше"],
  caption: [
    "INNER, LEFT, RIGHT, FULL, CROSS — виды соединений",
    "Связь — в ON; фильтр правой таблицы при LEFT — в ON; следите за размножением",
    "Следующая тема — вложенные запросы",
  ],
  frames: [
    [
      Box("a", 65, 60, 110, 28, "INNER", "g", { size: 10 }),
      Box("b", 180, 60, 110, 28, "LEFT", "g", { size: 10 }),
      Box("c", 295, 60, 110, 28, "RIGHT / FULL", "b", { size: 9.5 }),
      Box("d", 180, 104, 110, 28, "CROSS", "m", { size: 10 }),
    ],
    [
      Box("a", 65, 60, 110, 44, "ON — связь", "b", { size: 10 }),
      Box("b", 180, 60, 110, 44, "правая при LEFT\n— в ON", "y", { size: 9 }),
      Box("c", 295, 60, 110, 44, "следим за\nразмножением", "r", { size: 9.5 }),
    ],
    [sql("c", 20, 40, ["SELECT …", "FROM t", "WHERE x > (SELECT …);"], [2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
