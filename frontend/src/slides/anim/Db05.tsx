import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 5 книги «Базы данных»: агрегатные функции. */

const ORD = [
  [1, "shipped", 79500],
  [2, "shipped", 5200],
  [3, "paid", 55400],
  [4, "cancelled", 3900],
  [5, "paid", 4200],
] as const;
const OH = ["id", "status", "total"];
const OW = [30, 72, 56];
const code = { w: 340, size: 10, lh: 14 };
const OT = (hot: number[] = [], dim: number[] = [], x = 14) => tbl("t", x, 56, OH, ORD, OW, { size: 8, hot, dim });
const res = (head: string[], row: (string | number)[], x: number, y = 86, w = 70) =>
  tbl("r", x, y, head, [row], head.map(() => w), { size: 9, hot: [0] });

// 1. Много строк — одно число
export const V01 = scene({
  labels: ["Много строк", "Свёртка", "Одна строка"],
  caption: [
    "Обычный запрос возвращает столько строк, сколько нашёл",
    "Агрегатная функция сворачивает все строки в одно значение",
    "Агрегат без группировки всегда возвращает одну строку",
  ],
  frames: [
    [...OT([0, 1, 2, 3, 4]), Tx("n", 280, 90, "5 строк", { size: 11 })],
    [...OT([0, 1, 2, 3, 4]), arrow("a", 200, 90, 244, 90, "g"), Box("f", 300, 90, 90, 40, "COUNT\nSUM · AVG\nMIN · MAX", "g", { size: 8.5 })],
    [Box("f", 90, 90, 120, 40, "SUM(total)", "m", { size: 10 }), arrow("a", 156, 90, 204, 90, "g"), Box("r", 280, 90, 100, 40, "148200", "g", { size: 12 })],
  ],
});

// 2. COUNT(*)
export const V02 = scene({
  labels: ["Все строки", "С условием", "Пустая таблица"],
  caption: [
    "COUNT(*) считает строки целиком, независимо от содержимого столбцов",
    "WHERE выполняется раньше агрегата: считаются только оплаченные",
    "Для пустого набора COUNT вернёт 0, а не пропуск",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT COUNT(*) FROM orders;"], [0], code), ...OT([0, 1, 2, 3, 4], [], 10), ...res(["COUNT(*)"], [5], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT COUNT(*) FROM orders", "WHERE status = 'paid';"], [0, 1], code), ...OT([2, 4], [0, 1, 3], 10), ...res(["COUNT(*)"], [2], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT COUNT(*) FROM orders", "WHERE status = 'lost';"], [0, 1], code), ...res(["COUNT(*)"], [0], 180, 90, 90)],
  ],
});

// 3. SUM и AVG
export const V03 = scene({
  labels: ["SUM", "AVG", "ROUND"],
  caption: [
    "SUM складывает значения столбца: 148 200 на все пять заказов",
    "AVG — сумма, делённая на число значений: 29 640",
    "Среднее обычно дробное: ROUND(x, 2) оставляет два знака",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT SUM(total) FROM orders;"], [0], code), ...OT([0, 1, 2, 3, 4], [], 10), ...res(["SUM"], [148200], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT AVG(total) FROM orders;"], [0], code), ...OT([0, 1, 2, 3, 4], [], 10), ...res(["AVG"], [29640], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT ROUND(AVG(total) / 7, 2) FROM orders;"], [0], code), ...res(["результат"], [4234.29], 180, 90, 100), Tx("n", 180, 130, "29640 / 7 = 4234.2857…", { size: 9 })],
  ],
});

// 4. MIN и MAX
export const V04 = scene({
  labels: ["MIN", "MAX", "Не только числа"],
  caption: [
    "MIN возвращает наименьшее значение: 3900",
    "MAX — наибольшее: 79500; но саму строку агрегат не возвращает",
    "Работают со строками и датами: самая ранняя дата, последнее имя по алфавиту",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT MIN(total) FROM orders;"], [0], code), ...OT([3], [0, 1, 2, 4], 10), ...res(["MIN"], [3900], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT MAX(total) FROM orders;"], [0], code), ...OT([0], [1, 2, 3, 4], 10), ...res(["MAX"], [79500], 290, 90, 70)],
    [
      sql("c", 10, 14, ["SELECT MIN(created), MAX(name)", "FROM orders, customers;"], [0], code),
      ...tbl("r", 90, 74, ["MIN(created)", "MAX(name)"], [["2024-02-01", "Лев"]], [100, 90], { size: 9, hot: [0] }),
    ],
  ],
});

// 5. COUNT(столбец)
const BR = [
  [1, "Nova"],
  [2, "NULL"],
  [3, "Sonic"],
  [4, "NULL"],
  [5, "Keyra"],
] as const;
export const V05 = scene({
  labels: ["COUNT(*)", "COUNT(brand)", "Разность"],
  caption: [
    "COUNT(*) считает все пять строк",
    "COUNT(brand) считает только непустые значения: три",
    "COUNT(*) − COUNT(brand) показывает число пропусков",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT COUNT(*) FROM products;"], [0], code), ...tbl("t", 20, 56, ["id", "brand"], BR, [30, 70], { size: 8.5, hot: [0, 1, 2, 3, 4] }), ...res(["COUNT(*)"], [5], 280, 90, 70)],
    [sql("c", 10, 14, ["SELECT COUNT(brand) FROM products;"], [0], code), ...tbl("t", 20, 56, ["id", "brand"], BR, [30, 70], { size: 8.5, hot: [0, 2, 4], dim: [1, 3] }), ...res(["COUNT(brand)"], [3], 280, 90, 76)],
    [sql("c", 10, 14, ["SELECT COUNT(*) - COUNT(brand)", "FROM products;"], [0], code), ...tbl("t", 20, 56, ["id", "brand"], BR, [30, 70], { size: 8.5, hot: [1, 3], dim: [0, 2, 4] }), ...res(["без бренда"], [2], 280, 90, 76)],
  ],
});

// 6. NULL и агрегаты
export const V06 = scene({
  labels: ["AVG", "SUM пустого", "COALESCE"],
  caption: [
    "Среднее от 10, NULL, 30 равно 20: пропуск не считается нулём и не входит в делитель",
    "Если подходящих строк нет, SUM возвращает NULL, а COUNT — нуль",
    "COALESCE(SUM(x), 0) превращает NULL в ноль",
  ],
  frames: [
    [
      ...tbl("t", 30, 40, ["x"], [[10], ["NULL"], [30]], [50], { size: 9, hot: [0, 2], dim: [1] }),
      sql("c", 150, 58, ["SELECT AVG(x) FROM t;"], [0], { ...code, w: 200 }),
      ...res(["AVG"], [20], 210, 100, 70),
    ],
    [
      sql("c", 10, 14, ["SELECT SUM(x), COUNT(x)", "FROM t WHERE x > 100;"], [0], code),
      ...tbl("r", 110, 70, ["SUM", "COUNT"], [["NULL", 0]], [70, 70], { size: 10, hot: [0], c: "y" }),
    ],
    [
      sql("c", 10, 14, ["SELECT COALESCE(SUM(x), 0)", "FROM t WHERE x > 100;"], [0], code),
      ...res(["результат"], [0], 180, 90, 90),
    ],
  ],
});

// 7. COUNT(DISTINCT)
const CITY = ["Москва", "Казань", "Москва", "NULL", "Тверь"];
export const V07 = scene({
  labels: ["COUNT(city)", "COUNT(DISTINCT city)", "Не то же, что DISTINCT"],
  caption: [
    "COUNT(city) считает непустые значения: четыре",
    "С DISTINCT повторы убираются: Москва, Казань, Тверь — три",
    "DISTINCT внутри агрегата и после SELECT — разные вещи",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT COUNT(city) FROM customers;"], [0], code), ...tbl("t", 30, 56, ["city"], CITY.map((c) => [c]), [90], { size: 8.5, hot: [0, 1, 2, 4], dim: [3] }), ...res(["COUNT"], [4], 270, 90, 70)],
    [sql("c", 10, 14, ["SELECT COUNT(DISTINCT city) FROM customers;"], [0], code), ...tbl("t", 30, 56, ["city"], CITY.map((c) => [c]), [90], { size: 8.5, hot: [0, 1, 4], dim: [2, 3] }), ...res(["разных"], [3], 270, 90, 70)],
    [
      Box("a", 90, 70, 150, 40, "SELECT DISTINCT city\n→ несколько строк", "b", { size: 9 }),
      Box("b", 270, 70, 150, 40, "COUNT(DISTINCT city)\n→ одно число", "g", { size: 9 }),
    ],
  ],
});

// 8. WHERE и агрегаты
export const V08 = scene({
  labels: ["Порядок", "Фильтр, потом сумма", "Условие на агрегат"],
  caption: [
    "Сначала WHERE отбирает строки, потом агрегат сворачивает остаток",
    "Сумма оплаченных заказов: 55 400 + 4 200 = 59 600",
    "Условие на значение агрегата в WHERE невозможно — суммы ещё нет; для этого есть HAVING",
  ],
  frames: [
    [
      Box("a", 60, 80, 90, 34, "FROM", "b", { size: 10 }),
      Box("b", 180, 80, 90, 34, "WHERE", "g", { size: 10 }),
      Box("c", 300, 80, 90, 34, "SUM(...)", "y", { size: 10 }),
      arrow("e1", 108, 80, 132, 80, "m"),
      arrow("e2", 228, 80, 252, 80, "m"),
    ],
    [sql("c", 10, 14, ["SELECT SUM(total) FROM orders", "WHERE status = 'paid';"], [1], code), ...OT([2, 4], [0, 1, 3], 10), ...res(["SUM"], [59600], 290, 90, 70)],
    [sql("c", 10, 14, ["SELECT status FROM orders", "WHERE SUM(total) > 1000;"], undefined, { ...code, bad: [1] }), Box("e", 180, 110, 280, 28, "ошибка: misuse of aggregate", "r", { size: 9.5 })],
  ],
});

// 9. Столбец рядом с агрегатом
export const V09 = scene({
  labels: ["Имя и счёт", "Произвольная строка", "Нужен GROUP BY"],
  caption: [
    "SELECT status, COUNT(*) — одно значение рядом с набором значений",
    "SQLite не ругается, но берёт status случайной строки: результат неверен",
    "Итоги по каждой группе получают через GROUP BY (глава 12)",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT status, COUNT(*)", "FROM orders;"], [0], code), ...OT([0, 1, 2, 3, 4], [], 10)],
    [sql("c", 10, 14, ["SELECT status, COUNT(*)", "FROM orders;"], [0], code), ...OT([], [0, 1, 2, 3, 4], 10), ...tbl("r", 250, 86, ["status", "COUNT"], [["shipped", 5]], [60, 46], { size: 8, c: "r" }), Tx("n", 280, 130, "статус взят\nслучайно", { size: 8.5, c: "r" })],
    [sql("c", 10, 14, ["SELECT status, COUNT(*)", "FROM orders GROUP BY status;"], [1], code), ...tbl("r", 90, 66, ["status", "COUNT"], [["shipped", 2], ["paid", 2], ["cancelled", 1]], [90, 60], { size: 8.5, hot: [0, 1, 2] })],
  ],
});

// 10. Несколько агрегатов
export const V10 = scene({
  labels: ["Набор", "Псевдонимы", "Доли"],
  caption: [
    "Несколько агрегатов в одном SELECT работают над одним набором строк",
    "Каждому — псевдоним: столбцы результата получают понятные имена",
    "Доля = сумма / сумма: приведите одно число к дробному, иначе будет 0",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT COUNT(*), SUM(total),", "       MIN(total), MAX(total)", "FROM orders;"], [0, 1], { ...code, lh: 13 }), ...tbl("r", 40, 90, ["COUNT", "SUM", "MIN", "MAX"], [[5, 148200, 3900, 79500]], [50, 80, 60, 60], { size: 9, hot: [0] })],
    [sql("c", 10, 14, ["SELECT COUNT(*) AS n, SUM(total) AS sum,", "       ROUND(AVG(total)) AS avg", "FROM orders;"], [0, 1], { ...code, lh: 13, size: 9.5 }), ...tbl("r", 90, 90, ["n", "sum", "avg"], [[5, 148200, 29640]], [50, 80, 70], { size: 9, hot: [0] })],
    [sql("c", 10, 14, ["SELECT 59600 / 148200,", "       59600 * 1.0 / 148200;"], [0, 1], code), ...tbl("r", 110, 80, ["целое", "дробное"], [[0, 0.402]], [70, 70], { size: 9.5, hot: [0] })],
  ],
});

// 11. Выражения внутри
const IT = [
  [1, 78000, 1],
  [1, 1500, 1],
  [2, 5200, 2],
] as const;
export const V11 = scene({
  labels: ["Выручка", "Условный счёт", "AVG и SUM/COUNT"],
  caption: [
    "SUM(qty * price) — выручка позиций заказа",
    "SUM(status = 'paid') — число оплаченных: сравнение даёт 1 или 0",
    "Без пропусков AVG(x) = SUM(x) / COUNT(*), при пропусках — нет",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT SUM(qty * price)", "FROM order_items;"], [0], code), ...tbl("t", 20, 56, ["order", "price", "qty"], IT, [40, 56, 40], { size: 8.5, hot: [0, 1, 2] }), ...res(["выручка"], [89900], 270, 90, 76)],
    [sql("c", 10, 14, ["SELECT SUM(status = 'paid')", "FROM orders;"], [0], code), ...OT([2, 4], [0, 1, 3], 10), ...res(["оплаченных"], [2], 280, 90, 80)],
    [
      ...tbl("t", 30, 30, ["x"], [[10], ["NULL"], [30]], [50], { size: 9 }),
      Box("a", 230, 50, 160, 28, "AVG(x) = 20", "g", { size: 10 }),
      Box("b", 230, 90, 160, 28, "SUM(x) / COUNT(*) = 13.3", "y", { size: 9.5 }),
      Tx("n", 230, 130, "делители разные", { size: 9 }),
    ],
  ],
});

// 12. GROUP_CONCAT
export const V12 = scene({
  labels: ["Склейка значений", "Разделитель", "Порядок"],
  caption: [
    "GROUP_CONCAT склеивает значения столбца в одну строку",
    "Разделитель — второй аргумент; по умолчанию запятая",
    "Порядок внутри строки не гарантирован; в других базах функция зовётся string_agg",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT GROUP_CONCAT(city)", "FROM customers;"], [0], code), ...tbl("r", 60, 80, ["результат"], [["Москва,Казань,Москва,Тверь"]], [240], { size: 9, hot: [0] })],
    [sql("c", 10, 14, ["SELECT GROUP_CONCAT(name, '; ')", "FROM customers;"], [0], code), ...tbl("r", 60, 80, ["результат"], [["Анна; Борис; Вера; Глеб"]], [240], { size: 9, hot: [0] })],
    [Box("a", 90, 70, 150, 36, "SQLite:\nGROUP_CONCAT", "b", { size: 9.5 }), Box("b", 270, 70, 150, 36, "Postgres:\nstring_agg", "b", { size: 9.5 }), Tx("n", 180, 120, "порядок задавайте явно", { size: 9.5 })],
  ],
});

// 13. Ловушки и итоги
export const V13 = scene({
  labels: ["Пять ловушек", "Итоги", "Дальше"],
  caption: [
    "COUNT(*) и COUNT(col), SUM пустого, игнор NULL, целое деление, столбец рядом с агрегатом",
    "COUNT · SUM · AVG · MIN · MAX · GROUP_CONCAT — свёртка набора строк",
    "Следующая тема — соединения: JOIN связывает таблицы по ключам",
  ],
  frames: [
    [
      Box("a", 70, 40, 120, 24, "COUNT(*) ≠ COUNT(col)", "y", { size: 8 }),
      Box("b", 70, 70, 120, 24, "SUM пустого → NULL", "y", { size: 8.5 }),
      Box("c", 70, 100, 120, 24, "NULL игнорируется", "y", { size: 8.5 }),
      Box("d", 70, 130, 120, 24, "7 / 2 = 3", "y", { size: 9 }),
      Box("e", 250, 85, 130, 40, "столбец рядом\nс агрегатом", "y", { size: 9 }),
    ],
    [
      Box("a", 65, 60, 110, 28, "COUNT", "g", { size: 10 }),
      Box("b", 180, 60, 110, 28, "SUM  AVG", "g", { size: 10 }),
      Box("c", 295, 60, 110, 28, "MIN  MAX", "g", { size: 10 }),
      Box("d", 180, 104, 140, 28, "GROUP_CONCAT", "g", { size: 10 }),
    ],
    [Box("a", 90, 80, 100, 34, "customers", "b", { size: 10 }), Box("b", 270, 80, 100, 34, "orders", "b", { size: 10 }), arrow("e", 142, 80, 218, 80, "g"), Tx("n", 180, 120, "JOIN", { size: 11, c: "g" })],
  ],
});
