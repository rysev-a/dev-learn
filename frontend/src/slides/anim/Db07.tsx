import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 7 книги «Базы данных»: вложенные запросы. */

const PR = [
  ["Планшет", "Электроника", 12000],
  ["Наушники", "Электроника", 8000],
  ["Клавиатура", "Аксессуары", 3000],
  ["Книга", "Книги", 1500],
  ["Чай", "Продукты", 500],
] as const;
const code = { w: 340, size: 10, lh: 14 };
const PT = (hot: number[] = [], dim: number[] = [], x = 14, y = 60) =>
  tbl("t", x, y, ["title", "category", "price"], PR, [68, 78, 48], { size: 8, hot, dim, cell: 17 });
const res = (head: string[], rows: (string | number)[][], x: number, y = 70, w = 70) =>
  tbl("r", x, y, head, rows, head.map(() => w), { size: 9, hot: rows.map((_, i) => i) });

// 1. Запрос в запросе
export const V01 = scene({
  labels: ["Два шага", "Внутренний первым", "Подстановка"],
  caption: [
    "Какие товары дороже средней цены? Сначала нужна средняя цена",
    "Внутренний запрос (в скобках) выполняется первым и даёт число",
    "Число подставляется во внешний запрос как обычное значение",
  ],
  frames: [
    [Box("a", 90, 70, 130, 40, "1. средняя цена", "b", { size: 10 }), Box("b", 270, 70, 130, 40, "2. сравнить цены", "b", { size: 10 }), arrow("e", 156, 70, 204, 70, "m")],
    [sql("c", 10, 30, ["SELECT AVG(price) FROM products;"], [0], code), ...res(["AVG"], [[5000]], 140, 80, 80)],
    [sql("c", 10, 20, ["SELECT title FROM products", "WHERE price > (SELECT AVG(price)", "              FROM products);"], [1, 2], { ...code, lh: 14 }), Tx("n", 180, 110, "(SELECT …) → 5000", { size: 10, c: "g" })],
  ],
});

// 2. Скалярный подзапрос
export const V02 = scene({
  labels: ["Дороже среднего", "Равно максимуму", "Много строк — ловушка"],
  caption: [
    "Подзапрос с AVG даёт одно значение — сравниваем с ним цену каждой строки",
    "Заказы с максимальной суммой: сравнение с (SELECT MAX(total) …)",
    "Если подзапрос вернул несколько строк, SQLite молча берёт первую — осторожно",
  ],
  frames: [
    [sql("c", 10, 14, ["WHERE price > (SELECT AVG(price) FROM products)"], [0], { ...code, size: 9.5 }), ...PT([0, 1], [2, 3, 4])],
    [sql("c", 10, 14, ["WHERE price = (SELECT MAX(price) FROM products)"], [0], { ...code, size: 9.5 }), ...PT([0], [1, 2, 3, 4])],
    [sql("c", 10, 14, ["WHERE price > (SELECT price FROM products)"], [0], { ...code, bad: [0] }), Box("e", 180, 100, 280, 36, "подзапрос вернул 5 строк:\nвзята только первая", "r", { size: 9.5 })],
  ],
});

// 3. IN с подзапросом
const CU = [
  [1, "Анна"],
  [2, "Борис"],
  [3, "Вера"],
  [4, "Глеб"],
] as const;
export const V03 = scene({
  labels: ["Список номеров", "IN", "Динамический список"],
  caption: [
    "Подзапрос возвращает столбец: номера клиентов, у которых есть заказы",
    "IN оставляет клиентов, чей id входит в этот список",
    "Список строится на лету: появился новый заказ — клиент попал в результат",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust FROM orders;"], [0], code), ...tbl("r", 140, 50, ["cust"], [[1], [1], [2]], [60], { size: 9, hot: [0, 1, 2] })],
    [sql("c", 10, 14, ["SELECT name FROM customers", "WHERE id IN (SELECT cust FROM orders);"], [1], code), ...tbl("c", 90, 56, ["id", "name"], CU, [40, 70], { size: 8.5, hot: [0, 1], dim: [2, 3] })],
    [sql("c", 10, 14, ["… id IN (SELECT cust FROM orders);"], [0], code), ...tbl("c", 90, 56, ["id", "name"], CU, [40, 70], { size: 8.5, hot: [0, 1, 2], dim: [3] }), Tx("n", 300, 100, "новый заказ Веры\n→ Вера в списке", { size: 8.5, c: "g" })],
  ],
});

// 4. NOT IN и NULL
export const V04 = scene({
  labels: ["NOT IN", "NULL в списке", "NOT EXISTS"],
  caption: [
    "Без пропусков NOT IN работает как ожидалось: клиенты без заказов",
    "Появился NULL: x <> NULL — неизвестно, и результат пуст",
    "NOT EXISTS не боится пропусков и находит Веру и Глеба",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT name FROM customers", "WHERE id NOT IN (1, 2);"], [1], code), ...tbl("r", 120, 56, ["name"], [["Вера"], ["Глеб"]], [90], { size: 9, hot: [0, 1] })],
    [sql("c", 10, 14, ["SELECT name FROM customers", "WHERE id NOT IN (1, 2, NULL);"], [1], code), Box("e", 180, 100, 220, 40, "0 строк:\nid <> NULL — неизвестно", "r", { size: 10 })],
    [sql("c", 10, 14, ["SELECT name FROM customers c", "WHERE NOT EXISTS (SELECT 1 FROM orders o", "                  WHERE o.cust = c.id);"], [1, 2], { ...code, size: 9.5, lh: 13 }), ...tbl("r", 120, 80, ["name"], [["Вера"], ["Глеб"]], [90], { size: 9, hot: [0, 1] })],
  ],
});

// 5. EXISTS
export const V05 = scene({
  labels: ["Для каждого клиента", "Нашлась строка", "Остановка"],
  caption: [
    "Для каждого клиента база проверяет: есть ли заказ с его номером",
    "Нашлась хотя бы одна строка — EXISTS истинно, клиент проходит",
    "Остальные заказы не проверяются: поиск останавливается на первом",
  ],
  frames: [
    [sql("c", 10, 14, ["WHERE EXISTS (SELECT 1 FROM orders o", "              WHERE o.cust = c.id)"], [0, 1], code), ...tbl("c", 14, 56, ["id", "name"], CU, [26, 56], { size: 8, cell: 17 }), Tx("n", 270, 100, "проверка для\nкаждого клиента", { size: 8.5 })],
    [sql("c", 10, 14, ["WHERE EXISTS (SELECT 1 FROM orders o", "              WHERE o.cust = c.id)"], [0, 1], code), ...tbl("c", 14, 56, ["id", "name"], CU, [26, 56], { size: 8, cell: 17, hot: [0, 1], dim: [2, 3] }), Tx("n", 270, 100, "Анна, Борис:\nзаказ найден", { size: 8.5, c: "g" })],
    [
      ...tbl("o", 20, 40, ["id", "cust"], [[101, 1], [102, 1], [103, 2]], [40, 40], { size: 8.5, hot: [0], dim: [1, 2] }),
      Tx("n", 250, 80, "нашли 101 —\nостальные не нужны", { size: 9, c: "g" }),
    ],
  ],
});

// 6. Коррелированный
const CAT = [
  ["Планшет", "Электроника", 12000, 10000],
  ["Наушники", "Электроника", 8000, 10000],
  ["Клавиатура", "Аксессуары", 3000, 3000],
] as const;
export const V06 = scene({
  labels: ["Нужна строка снаружи", "Среднее по категории", "Результат"],
  caption: [
    "Подзапрос ссылается на p.category — столбец внешней строки",
    "Для каждого товара считается среднее своей категории",
    "Остаются товары выше среднего в своей категории",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT title FROM products p", "WHERE price > (SELECT AVG(price)", "  FROM products", "  WHERE category = p.category);"], [3], { ...code, lh: 13 }), Tx("n", 290, 120, "p.category — из\nвнешней строки", { size: 8.5, c: "y" })],
    [...tbl("t", 10, 40, ["title", "category", "price", "AVG"], CAT, [74, 78, 50, 50], { size: 8.5 }), Tx("n", 180, 140, "среднее считается отдельно для каждой категории", { size: 9 })],
    [...tbl("t", 10, 40, ["title", "category", "price", "AVG"], CAT, [74, 78, 50, 50], { size: 8.5, hot: [0], dim: [1, 2] }), Tx("n", 180, 140, "выше своего среднего: только Планшет", { size: 9, c: "g" })],
  ],
});

// 7. Подзапрос во FROM
export const V07 = scene({
  labels: ["Итоги по клиентам", "Как таблица", "Фильтр по итогу"],
  caption: [
    "Внутренний запрос считает сумму заказов каждого клиента",
    "Его результат ведёт себя как временная таблица t — нужен псевдоним",
    "Внешний запрос фильтрует по итогу: суммы выше 50 000",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, SUM(total) AS s", "FROM orders GROUP BY cust"], [0, 1], code), ...tbl("r", 110, 60, ["cust", "s"], [[1, 84700], [2, 55400], [4, 3900]], [50, 70], { size: 9, hot: [0, 1, 2] })],
    [sql("c", 10, 14, ["SELECT * FROM (", "  SELECT cust, SUM(total) AS s FROM orders", "  GROUP BY cust) AS t;"], [0, 2], { ...code, size: 9, lh: 13 }), ...tbl("r", 110, 66, ["cust", "s"], [[1, 84700], [2, 55400], [4, 3900]], [50, 70], { size: 9 })],
    [sql("c", 10, 14, ["SELECT * FROM (…) AS t", "WHERE s > 50000;"], [1], code), ...tbl("r", 110, 66, ["cust", "s"], [[1, 84700], [2, 55400], [4, 3900]], [50, 70], { size: 9, hot: [0, 1], dim: [2] })],
  ],
});

// 8. Подзапрос в SELECT
export const V08 = scene({
  labels: ["Показатель на строку", "Счёт заказов", "Много подзапросов"],
  caption: [
    "Подзапрос в списке столбцов вычисляется для каждой строки результата",
    "Рядом с каждым клиентом — число его заказов",
    "Много таких подзапросов — много подсчётов; лучше JOIN с группировкой",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT name,", "  (SELECT COUNT(*) FROM orders o", "   WHERE o.cust = c.id) AS n", "FROM customers c;"], [1, 2], { ...code, lh: 13 }), Tx("n", 290, 100, "для каждой\nстроки", { size: 8.5 })],
    [...tbl("r", 110, 40, ["name", "n"], [["Анна", 2], ["Борис", 1], ["Вера", 0], ["Глеб", 0]], [80, 50], { size: 9, hot: [0, 1, 2, 3] })],
    [
      Box("a", 90, 70, 150, 36, "подзапрос на строку:\n4 строки → 4 подсчёта", "y", { size: 9 }),
      Box("b", 280, 70, 120, 36, "JOIN + GROUP BY:\nодин проход", "g", { size: 9 }),
    ],
  ],
});

// 9. ANY и ALL
export const V09 = scene({
  labels: ["Больше всех", "Больше какого-то", "Пустой набор"],
  caption: [
    "x > ALL (…) в SQLite записывают как x > (SELECT MAX(…) …)",
    "x > ANY (…) — это x > (SELECT MIN(…) …)",
    "На пустом наборе MAX даёт NULL, а по стандарту ALL — истину: различие",
  ],
  frames: [
    [sql("c", 10, 14, ["price > ALL (SELECT price …)   -- стандарт", "price > (SELECT MAX(price) …)   -- SQLite"], [1], { ...code, size: 9.5 })],
    [sql("c", 10, 14, ["price > ANY (SELECT price …)   -- стандарт", "price > (SELECT MIN(price) …)   -- SQLite"], [1], { ...code, size: 9.5 })],
    [Box("a", 90, 70, 150, 40, "ALL от пустого:\nистина", "b", { size: 9.5 }), Box("b", 270, 70, 150, 40, "MAX пустого: NULL\nсравнение неизвестно", "y", { size: 9 })],
  ],
});

// 10. Подзапрос или JOIN
export const V10 = scene({
  labels: ["Есть ли", "Нужны столбцы обеих", "Показатель на строку"],
  caption: [
    "Вопрос «есть ли» — IN или EXISTS: запрос читается как фраза",
    "Нужны столбцы обеих таблиц — JOIN",
    "Один показатель на строку — подзапрос в SELECT",
  ],
  frames: [
    [Box("a", 180, 40, 280, 26, "клиенты, у которых есть заказы", "b", { size: 9.5 }), sql("c", 20, 74, ["WHERE EXISTS (SELECT 1 FROM orders …)"], [0], code)],
    [Box("a", 180, 40, 280, 26, "клиент и сумма его заказа", "b", { size: 9.5 }), sql("c", 20, 74, ["FROM customers c JOIN orders o ON …"], [0], code)],
    [Box("a", 180, 40, 280, 26, "клиент и число его заказов", "b", { size: 9.5 }), sql("c", 20, 74, ["SELECT name, (SELECT COUNT(*) …)"], [0], code)],
  ],
});

// 11. Подзапросы в изменениях
export const V11 = scene({
  labels: ["UPDATE", "DELETE", "Сначала SELECT"],
  caption: [
    "В UPDATE значение берут подзапросом: пересчёт суммы заказа по позициям",
    "В DELETE условие использует подзапрос: клиенты без заказов",
    "Сначала выполните тот же подзапрос как SELECT и посмотрите, что затронется",
  ],
  frames: [
    [sql("c", 10, 14, ["UPDATE orders SET total =", "  (SELECT SUM(qty * price)", "   FROM order_items", "   WHERE order_id = orders.id);"], [1, 2, 3], { ...code, lh: 13 })],
    [sql("c", 10, 20, ["DELETE FROM customers", "WHERE id NOT IN (SELECT cust FROM orders", "                WHERE cust IS NOT NULL);"], [1, 2], { ...code, size: 9.5 })],
    [sql("c", 10, 20, ["-- проверка", "SELECT * FROM customers", "WHERE id NOT IN (SELECT cust FROM orders …);"], [1, 2], { ...code, size: 9.5 }), Tx("n", 180, 110, "убедитесь, что строки те, что нужно", { size: 9.5, c: "g" })],
  ],
});

// 12. Ошибки
export const V12 = scene({
  labels: ["Много строк", "Много столбцов", "Нет псевдонима"],
  caption: [
    "Скалярный подзапрос вернул несколько строк: SQLite берёт первую, другие базы — ошибка",
    "Подзапрос в IN должен возвращать один столбец",
    "Подзапрос во FROM без псевдонима — ошибка во многих базах",
  ],
  frames: [
    [Box("a", 180, 60, 280, 36, "= (SELECT price FROM products)\n→ 5 строк, взята первая", "y", { size: 9.5 }), Tx("n", 180, 110, "проверьте число строк", { size: 9.5 })],
    [sql("c", 10, 20, ["WHERE id IN (SELECT id, name FROM t)"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 280, 28, "sub-select returns 2 columns", "r", { size: 9.5 })],
    [sql("c", 10, 20, ["SELECT * FROM (SELECT 1 AS x);"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 220, 28, "нужен псевдоним: … ) AS t", "y", { size: 9.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Виды", "Выбор", "Дальше"],
  caption: [
    "Скалярный, список для IN, EXISTS, коррелированный, производная таблица",
    "NOT IN опасен из-за NULL — лучше NOT EXISTS",
    "Следующая тема — изменение данных: INSERT, UPDATE, DELETE",
  ],
  frames: [
    [
      Box("a", 65, 60, 110, 28, "скалярный", "b", { size: 9.5 }),
      Box("b", 180, 60, 110, 28, "IN (список)", "b", { size: 9.5 }),
      Box("c", 295, 60, 110, 28, "EXISTS", "b", { size: 9.5 }),
      Box("d", 100, 104, 140, 28, "коррелированный", "g", { size: 9.5 }),
      Box("e", 260, 104, 140, 28, "во FROM (таблица)", "g", { size: 9.5 }),
    ],
    [Box("a", 90, 70, 150, 36, "NOT IN + NULL\n→ пусто", "r", { size: 10 }), Box("b", 270, 70, 150, 36, "NOT EXISTS\n→ надёжно", "g", { size: 10 })],
    [sql("c", 20, 40, ["INSERT INTO t …;", "UPDATE t SET …;", "DELETE FROM t …;"], [0, 1, 2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
