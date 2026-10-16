import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 12 книги «Базы данных»: группировка GROUP BY и HAVING. */

type Row = readonly (string | number)[];
const ORD: Row[] = [
  [1, "shipped", 79500],
  [1, "shipped", 5200],
  [2, "paid", 55400],
  [2, "cancelled", 3900],
  [3, "paid", 4200],
];
const code = { w: 340, size: 10, lh: 14 };
const OT = (hot: number[] = [], dim: number[] = [], x = 14, y = 56, c = "b") =>
  tbl("o", x, y, ["cust", "status", "total"], ORD, [36, 66, 56], { size: 8, hot, dim, c, cell: 17 });
const GR = (head: string[], rows: Row[], x: number, y: number, widths: number[], hot: number[] = [0, 1, 2]) =>
  tbl("g", x, y, head, rows, widths, { size: 8.5, hot });

// 1. Итог по группе
export const V01 = scene({
  labels: ["Итог на всё", "Итог на каждого", "По группам"],
  caption: [
    "Агрегат без группировки — одно число на всю таблицу",
    "Нужны итоги по группам: по клиентам, месяцам, категориям",
    "GROUP BY делит строки на группы и считает агрегат в каждой",
  ],
  frames: [
    [...OT([0, 1, 2, 3, 4], [], 14, 40), Box("r", 290, 90, 100, 36, "SUM = 148 200", "g", { size: 9.5 })],
    [Box("a", 90, 60, 130, 30, "клиент 1: ?", "y", { size: 10 }), Box("b", 90, 100, 130, 30, "клиент 2: ?", "y", { size: 10 }), Box("c", 270, 80, 130, 30, "клиент 3: ?", "y", { size: 10 })],
    [Box("a", 90, 60, 130, 30, "клиент 1: 84 700", "g", { size: 10 }), Box("b", 90, 100, 130, 30, "клиент 2: 59 300", "g", { size: 10 }), Box("c", 270, 80, 130, 30, "клиент 3: 4 200", "g", { size: 10 })],
  ],
});

// 2. GROUP BY
export const V02 = scene({
  labels: ["Запрос", "Группы", "По строке на группу"],
  caption: [
    "GROUP BY status: строки с одинаковым статусом попадают в одну группу",
    "Три группы: shipped, paid, cancelled",
    "Результат — по одной строке на группу с агрегатами",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT status, COUNT(*), SUM(total)", "FROM orders GROUP BY status;"], [1], code), ...OT([], [], 14, 56)],
    [sql("c", 10, 14, ["SELECT status, COUNT(*), SUM(total)", "FROM orders GROUP BY status;"], [1], code), ...OT([0, 1], [2, 3, 4], 14, 56, "g"), Tx("n", 290, 110, "shipped:\nстроки 1–2", { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT status, COUNT(*), SUM(total)", "FROM orders GROUP BY status;"], [1], code), ...GR(["status", "COUNT", "SUM"], [["shipped", 2, 84700], ["paid", 2, 59600], ["cancelled", 1, 3900]], 70, 60, [80, 56, 70])],
  ],
});

// 3. Что можно в SELECT
export const V03 = scene({
  labels: ["Ключ и агрегат", "Лишний столбец", "MIN и MAX"],
  caption: [
    "В SELECT — ключи группы и агрегаты: у них одно значение на группу",
    "Прочие столбцы значения для группы не имеют: SQLite берёт произвольное — это ошибка логики",
    "Исключение SQLite: с MIN/MAX остальные столбцы берутся из той же строки",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, COUNT(*)", "FROM orders GROUP BY cust;"], [0], code), ...GR(["cust", "COUNT"], [[1, 2], [2, 2], [3, 1]], 110, 60, [60, 60])],
    [sql("c", 10, 14, ["SELECT cust, status, COUNT(*)", "FROM orders GROUP BY cust;"], [0], { ...code, bad: [0] }), ...GR(["cust", "status", "COUNT"], [[1, "shipped", 2], [2, "paid", 2], [3, "paid", 1]], 90, 62, [50, 70, 50]), Tx("n", 180, 140, "status взят случайно", { size: 9, c: "r" })],
    [sql("c", 10, 14, ["SELECT cust, status, MAX(total)", "FROM orders GROUP BY cust;"], [0], code), ...GR(["cust", "status", "MAX"], [[1, "shipped", 79500], [2, "paid", 55400], [3, "paid", 4200]], 90, 62, [50, 70, 60]), Tx("n", 180, 140, "status — из строки с максимумом", { size: 9, c: "g" })],
  ],
});

// 4. Несколько ключей
export const V04 = scene({
  labels: ["Пара ключей", "Комбинации", "Детализация"],
  caption: [
    "GROUP BY cust, status — группа это пара значений",
    "Групп столько, сколько различных пар встретилось в данных",
    "Каждый клиент в разрезе статусов — основа сводных таблиц",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, status, COUNT(*)", "FROM orders GROUP BY cust, status;"], [1], code), ...OT([], [], 14, 56)],
    [sql("c", 10, 14, ["… GROUP BY cust, status;"], [0], code), ...GR(["cust", "status", "COUNT"], [[1, "shipped", 2], [2, "paid", 1], [2, "cancelled", 1], [3, "paid", 1]], 90, 50, [50, 80, 56])],
    [Box("a", 70, 60, 100, 30, "клиент 1", "b", { size: 10 }), Box("b", 70, 100, 100, 30, "клиент 2", "b", { size: 10 }), Box("c", 250, 50, 130, 24, "shipped: 2", "g", { size: 9 }), Box("d", 250, 80, 130, 24, "paid: 1", "g", { size: 9 }), Box("e", 250, 110, 130, 24, "cancelled: 1", "g", { size: 9 })],
  ],
});

// 5. Группировка по выражению
export const V05 = scene({
  labels: ["По месяцу", "По размеру", "По чётности"],
  caption: [
    "Ключ — выражение: STRFTIME('%Y-%m', created) группирует по месяцам",
    "CASE превращает сумму в размер, и группируем по размеру",
    "id % 2 разбивает на чётные и нечётные",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT STRFTIME('%Y-%m', created) AS m, SUM(total)", "FROM orders GROUP BY m;"], [0, 1], { ...code, size: 9 }), ...GR(["m", "SUM"], [["2024-04", 4200], ["2024-05", 84700]], 110, 66, [70, 70], [0, 1])],
    [sql("c", 10, 14, ["SELECT CASE WHEN total < 5000 THEN 'мал' ELSE 'кр' END AS sz,", "       COUNT(*) FROM orders GROUP BY sz;"], [0, 1], { ...code, size: 9 }), ...GR(["sz", "COUNT"], [["мал", 2], ["кр", 3]], 110, 66, [70, 70], [0, 1])],
    [sql("c", 10, 14, ["SELECT id % 2 AS p, COUNT(*)", "FROM orders GROUP BY p;"], [0, 1], code), ...GR(["p", "COUNT"], [[0, 2], [1, 3]], 120, 66, [60, 60], [0, 1])],
  ],
});

// 6. NULL — тоже группа
export const V06 = scene({
  labels: ["Пропуски в ключе", "Отдельная группа", "Подстановка имени"],
  caption: [
    "У части клиентов город не указан — NULL в ключе",
    "Все NULL образуют одну отдельную группу",
    "COALESCE даёт группе понятное имя «не указан»",
  ],
  frames: [
    [...tbl("t", 100, 50, ["name", "city"], [["Анна", "Москва"], ["Борис", "Казань"], ["Вера", "NULL"], ["Глеб", "NULL"]], [70, 80], { size: 9, hot: [2, 3] })],
    [sql("c", 10, 14, ["SELECT city, COUNT(*) FROM customers", "GROUP BY city;"], [1], code), ...GR(["city", "COUNT"], [["Москва", 1], ["Казань", 1], ["NULL", 2]], 100, 62, [90, 60], [2])],
    [sql("c", 10, 14, ["SELECT COALESCE(city, 'не указан') AS c, COUNT(*)", "FROM customers GROUP BY c;"], [0], { ...code, size: 9.5 }), ...GR(["c", "COUNT"], [["Москва", 1], ["Казань", 1], ["не указан", 2]], 100, 66, [90, 60], [2])],
  ],
});

// 7. HAVING
export const V07 = scene({
  labels: ["Итоги групп", "HAVING", "Результат"],
  caption: [
    "Сначала считаем сумму для каждого клиента",
    "HAVING SUM(total) > 50000 оставляет только группы с большой суммой",
    "Остались клиенты 1 и 2; клиент 3 отсеян после группировки",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, SUM(total) AS s", "FROM orders GROUP BY cust;"], [1], code), ...GR(["cust", "s"], [[1, 84700], [2, 59300], [3, 4200]], 110, 62, [50, 80], [])],
    [sql("c", 10, 14, ["SELECT cust, SUM(total) AS s FROM orders", "GROUP BY cust HAVING SUM(total) > 50000;"], [1], code), ...tbl("g", 110, 62, ["cust", "s"], [[1, 84700], [2, 59300], [3, 4200]], [50, 80], { size: 8.5, hot: [0, 1], dim: [2] })],
    [sql("c", 10, 14, ["… HAVING SUM(total) > 50000;"], [0], code), ...GR(["cust", "s"], [[1, 84700], [2, 59300]], 110, 66, [50, 80], [0, 1])],
  ],
});

// 8. WHERE или HAVING
export const V08 = scene({
  labels: ["WHERE — строки", "HAVING — группы", "Вместе"],
  caption: [
    "Условие по строке (status <> 'cancelled') — в WHERE: отбрасывается до группировки",
    "Условие по итогу группы (SUM > 50000) — в HAVING",
    "Вместе: сначала WHERE, потом группировка, потом HAVING",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, SUM(total) FROM orders", "WHERE status <> 'cancelled'", "GROUP BY cust;"], [1], { ...code, lh: 13 }), Box("n", 290, 120, 110, 28, "отменённый\nотброшен сразу", "g", { size: 8 })],
    [sql("c", 10, 14, ["SELECT cust, SUM(total) FROM orders", "GROUP BY cust", "HAVING SUM(total) > 50000;"], [2], { ...code, lh: 13 }), Box("n", 290, 120, 110, 28, "условие\nна итог", "g", { size: 8 })],
    [sql("c", 10, 14, ["SELECT cust, SUM(total) FROM orders", "WHERE status <> 'cancelled'", "GROUP BY cust HAVING SUM(total) > 50000;"], [1, 2], { ...code, lh: 13, size: 9.5 }), ...GR(["cust", "SUM"], [[1, 84700], [2, 55400]], 110, 80, [50, 80], [0, 1])],
  ],
});

// 9. Порядок выполнения
export const V09 = scene({
  labels: ["Первые шаги", "Группировка", "Вывод"],
  caption: [
    "FROM собирает таблицы, WHERE отбирает строки",
    "GROUP BY делит на группы, HAVING отбирает группы",
    "SELECT считает выражения, ORDER BY сортирует, LIMIT ограничивает",
  ],
  frames: [
    [Box("a", 80, 80, 100, 34, "FROM", "g", { size: 11 }), arrow("e", 130, 80, 150, 80, "m"), Box("b", 220, 80, 100, 34, "WHERE", "g", { size: 11 }), Tx("n", 180, 130, "таблицы → строки", { size: 9.5 })],
    [Box("a", 80, 80, 100, 34, "GROUP BY", "g", { size: 10 }), arrow("e", 130, 80, 150, 80, "m"), Box("b", 220, 80, 100, 34, "HAVING", "g", { size: 11 }), Tx("n", 180, 130, "строки → группы", { size: 9.5 })],
    [Box("a", 50, 80, 76, 34, "SELECT", "y", { size: 9.5 }), Box("b", 140, 80, 76, 34, "ORDER BY", "y", { size: 9 }), Box("c", 230, 80, 76, 34, "LIMIT", "y", { size: 9.5 }), arrow("e1", 90, 80, 100, 80, "m"), arrow("e2", 180, 80, 190, 80, "m")],
  ],
});

// 10. Топ групп
export const V10 = scene({
  labels: ["Сортировка по агрегату", "Топ-2", "Ничья"],
  caption: [
    "ORDER BY по агрегату или его псевдониму: рейтинг клиентов по сумме",
    "LIMIT 2 оставляет двух лидеров",
    "При равных итогах добавляйте второй ключ — иначе граница топа случайна",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT cust, SUM(total) AS s FROM orders", "GROUP BY cust ORDER BY s DESC;"], [1], code), ...GR(["cust", "s"], [[1, 84700], [2, 59300], [3, 4200]], 110, 62, [50, 80], [0, 1, 2])],
    [sql("c", 10, 14, ["… ORDER BY s DESC LIMIT 2;"], [0], code), ...tbl("g", 110, 62, ["cust", "s"], [[1, 84700], [2, 59300], [3, 4200]], [50, 80], { size: 8.5, hot: [0, 1], dim: [2] })],
    [sql("c", 10, 14, ["… ORDER BY s DESC, cust LIMIT 2;"], [0], code), ...GR(["cust", "s"], [[1, 5000], [2, 5000], [3, 5000]], 110, 62, [50, 80], [0, 1]), Tx("n", 290, 110, "ничья: cust\nразрешит", { size: 8.5 })],
  ],
});

// 11. Группы и соединения
export const V11 = scene({
  labels: ["Имена клиентов", "Группируем по id", "LEFT JOIN"],
  caption: [
    "JOIN подтягивает имя клиента, GROUP BY считает суммы его заказов",
    "Группируем по c.id, а не по имени: одинаковые имена не слипнутся",
    "LEFT JOIN сохраняет клиентов без заказов; COUNT(o.id) даёт 0, COUNT(*) дал бы 1",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT c.name, SUM(o.total)", "FROM customers c JOIN orders o ON o.cust = c.id", "GROUP BY c.id;"], [2], { ...code, lh: 13, size: 9.5 }), ...GR(["name", "SUM"], [["Анна", 84700], ["Борис", 59300]], 110, 70, [70, 80], [0, 1])],
    [Box("a", 90, 60, 150, 36, "два «Ивана»\nGROUP BY name → 1 группа", "r", { size: 8.5 }), Box("b", 270, 60, 150, 36, "GROUP BY c.id →\n2 группы", "g", { size: 9 })],
    [sql("c", 10, 14, ["SELECT c.name, COUNT(o.id)", "FROM customers c LEFT JOIN orders o ON …", "GROUP BY c.id;"], [1], { ...code, lh: 13, size: 9.5 }), ...GR(["name", "COUNT(o.id)"], [["Анна", 2], ["Вера", 0]], 100, 70, [70, 90], [1])],
  ],
});

// 12. Типичные ошибки
export const V12 = scene({
  labels: ["Лишний столбец", "HAVING вместо WHERE", "Размножение"],
  caption: [
    "Столбец не из ключа и не агрегат — результат неверен",
    "Условие на обычный столбец в HAVING работает, но медленнее WHERE",
    "После JOIN сумма заказа повторяется по каждой позиции",
  ],
  frames: [
    [Box("a", 180, 70, 280, 36, "SELECT city, name, COUNT(*) … GROUP BY city\nname — какой из группы?", "r", { size: 9 })],
    [Box("a", 90, 70, 150, 36, "HAVING status = 'paid'\nпосле группировки", "y", { size: 9 }), Box("b", 270, 70, 150, 36, "WHERE status = 'paid'\nдо группировки", "g", { size: 9 })],
    [Box("a", 90, 70, 150, 36, "SUM(o.total) после\nJOIN с позициями ×3", "r", { size: 9 }), Box("b", 270, 70, 150, 36, "сначала итог по\nзаказам, потом JOIN", "g", { size: 9 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Группировка", "Фильтры и порядок", "Дальше"],
  caption: [
    "GROUP BY — ключи и агрегаты; ключ может быть выражением; NULL — одна группа",
    "WHERE — до, HAVING — после; ORDER BY по агрегату и LIMIT — топ групп",
    "Следующая тема — индексы и планы запросов: как сделать запрос быстрее",
  ],
  frames: [
    [Box("a", 65, 60, 110, 30, "GROUP BY", "g", { size: 10 }), Box("b", 180, 60, 110, 30, "агрегаты", "g", { size: 10 }), Box("c", 295, 60, 110, 30, "NULL — группа", "g", { size: 9.5 })],
    [Box("a", 65, 60, 110, 30, "WHERE → до", "b", { size: 10 }), Box("b", 180, 60, 110, 30, "HAVING → после", "b", { size: 9.5 }), Box("c", 295, 60, 110, 30, "ORDER + LIMIT", "b", { size: 9.5 })],
    [sql("c", 20, 40, ["CREATE INDEX idx", "  ON orders (cust);", "EXPLAIN QUERY PLAN …;"], [0, 1, 2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
