import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 15 книги «Базы данных»: оконные функции. */

type Row = readonly (string | number)[];
const code = { w: 340, size: 10, lh: 14 };
const MON: Row[] = [
  ["янв", 100],
  ["фев", 150],
  ["мар", 120],
  ["апр", 180],
];
const T = (head: string[], rows: Row[], x: number, y: number, widths: number[], hot: number[] = [], dim: number[] = []) =>
  tbl("t", x, y, head, rows, widths, { size: 8.5, hot, dim });

// 1. Агрегат без схлопывания
export const V01 = scene({
  labels: ["Группировка схлопывает", "Нужно рядом", "Окно"],
  caption: [
    "GROUP BY превращает строки группы в одну — детали потеряны",
    "Хочется видеть каждую строку и рядом итог группы",
    "Оконная функция считает по окну, но возвращает результат для каждой строки",
  ],
  frames: [
    [...T(["m", "total"], MON, 30, 50, [50, 60], [0, 1, 2, 3]), arrow("a", 150, 90, 190, 90, "g"), Box("r", 280, 90, 130, 34, "один итог: 550", "y", { size: 10 })],
    [...T(["m", "total", "итого"], MON.map((r) => [r[0]!, r[1]!, "?"]), 80, 50, [50, 60, 60], [0, 1, 2, 3])],
    [...T(["m", "total", "итого"], MON.map((r) => [r[0]!, r[1]!, 550]), 80, 50, [50, 60, 60], [0, 1, 2, 3]), Tx("n", 300, 100, "строки\nна месте", { size: 8.5, c: "g" })],
  ],
});

// 2. OVER
export const V02 = scene({
  labels: ["Пустое OVER", "Доля", "Формула окна"],
  caption: [
    "SUM(total) OVER () — сумма по всем строкам, повторённая в каждой",
    "Доля строки: total / SUM(total) OVER ()",
    "В скобках OVER: PARTITION BY, ORDER BY и рамка",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT m, total, SUM(total) OVER () AS s", "FROM sales;"], [0], code), ...T(["m", "total", "s"], MON.map((r) => [r[0]!, r[1]!, 550]), 80, 58, [50, 60, 60], [0, 1, 2, 3])],
    [sql("c", 10, 14, ["SELECT m, ROUND(100.0 * total / SUM(total) OVER ())", "FROM sales;"], [0], { ...code, size: 9.5 }), ...T(["m", "доля %"], [["янв", 18.2], ["фев", 27.3], ["мар", 21.8], ["апр", 32.7]], 100, 58, [50, 70], [0, 1, 2, 3])],
    [sql("c", 10, 20, ["функция(…) OVER (", "  PARTITION BY …", "  ORDER BY …", "  ROWS …)"], [0, 1, 2, 3], { ...code, lh: 14 })],
  ],
});

// 3. PARTITION BY
const OC: Row[] = [
  [1, 79500],
  [1, 5200],
  [2, 55400],
  [2, 3900],
  [3, 4200],
];
export const V03 = scene({
  labels: ["Окна по клиентам", "Итог в каждой строке", "Доля от клиента"],
  caption: [
    "PARTITION BY cust делит строки на окна; окна не видят друг друга",
    "SUM(total) OVER (PARTITION BY cust) — итог клиента рядом с каждым заказом",
    "Доля заказа от суммы клиента: total / итог клиента",
  ],
  frames: [
    [...tbl("t", 100, 40, ["cust", "total"], OC, [50, 70], { size: 8.5, hot: [0, 1], dim: [2, 3, 4], cell: 17 }), Tx("n", 290, 70, "окно клиента 1", { size: 8.5, c: "g" })],
    [sql("c", 10, 14, ["SUM(total) OVER (PARTITION BY cust)"], [0], code), ...tbl("t", 60, 50, ["cust", "total", "итог"], OC.map((r, i) => [r[0]!, r[1]!, [84700, 84700, 59300, 59300, 4200][i]!]), [50, 70, 70], { size: 8.5, hot: [0, 1, 2, 3, 4], cell: 17 })],
    [sql("c", 10, 14, ["total * 100.0 / SUM(total) OVER (PARTITION BY cust)"], [0], { ...code, size: 9 }), ...tbl("t", 80, 50, ["cust", "total", "%"], OC.map((r, i) => [r[0]!, r[1]!, [94, 6, 93, 7, 100][i]!]), [50, 70, 50], { size: 8.5, hot: [0, 1, 2, 3, 4], cell: 17 })],
  ],
});

// 4. Накопительный итог
export const V04 = scene({
  labels: ["Порядок", "Нарастающий итог", "Все строки"],
  caption: [
    "ORDER BY в окне: каждая строка видит предыдущие и себя",
    "SUM(total) OVER (ORDER BY m): 100, 250, 370, 550",
    "Без ORDER BY окно — вся таблица, и итог одинаков в каждой строке",
  ],
  frames: [
    [...T(["m", "total"], MON, 110, 50, [50, 70], [0], []), Tx("n", 290, 70, "строка видит\nсебя и прошлые", { size: 8.5, c: "g" })],
    [sql("c", 10, 14, ["SELECT m, total, SUM(total) OVER (ORDER BY m) AS run", "FROM sales;"], [0], { ...code, size: 9.5 }), ...T(["m", "total", "run"], [["янв", 100, 100], ["фев", 150, 250], ["мар", 120, 370], ["апр", 180, 550]], 80, 58, [50, 60, 60], [0, 1, 2, 3])],
    [sql("c", 10, 14, ["SELECT m, total, SUM(total) OVER () AS s", "FROM sales;"], [0], code), ...T(["m", "total", "s"], MON.map((r) => [r[0]!, r[1]!, 550]), 80, 58, [50, 60, 60], [0, 1, 2, 3])],
  ],
});

// 5. ROW_NUMBER
const SC: Row[] = [
  ["Анна", 90],
  ["Борис", 85],
  ["Вера", 85],
  ["Глеб", 70],
];
export const V05 = scene({
  labels: ["Нумерация", "Уникальный ключ", "В группах"],
  caption: [
    "ROW_NUMBER() OVER (ORDER BY …) присваивает 1, 2, 3, … без повторов",
    "Среди равных значений порядок произвольный — добавляйте уникальный ключ",
    "С PARTITION BY нумерация начинается заново в каждой группе",
  ],
  frames: [
    [sql("c", 10, 14, ["ROW_NUMBER() OVER (ORDER BY score DESC)"], [0], code), ...tbl("t", 60, 50, ["name", "score", "n"], SC.map((r, i) => [r[0]!, r[1]!, i + 1]), [70, 60, 40], { size: 8.5, hot: [0, 1, 2, 3] })],
    [sql("c", 10, 14, ["ROW_NUMBER() OVER (ORDER BY score DESC, name)"], [0], code), ...tbl("t", 60, 50, ["name", "score", "n"], SC.map((r, i) => [r[0]!, r[1]!, i + 1]), [70, 60, 40], { size: 8.5, hot: [1, 2] })],
    [sql("c", 10, 14, ["ROW_NUMBER() OVER (PARTITION BY cust ORDER BY created)"], [0], { ...code, size: 9 }), ...tbl("t", 80, 50, ["cust", "created", "n"], [[1, "02-01", 1], [1, "03-15", 2], [2, "03-02", 1], [2, "04-10", 2]], [50, 70, 40], { size: 8.5, hot: [0, 2] })],
  ],
});

// 6. RANK и DENSE_RANK
export const V06 = scene({
  labels: ["ROW_NUMBER", "RANK", "DENSE_RANK"],
  caption: [
    "ROW_NUMBER: 1, 2, 3, 4 — у всех разные номера",
    "RANK: ничья делит место, следующее пропускается — 1, 2, 2, 4",
    "DENSE_RANK: без пропусков — 1, 2, 2, 3",
  ],
  frames: [
    [...tbl("t", 70, 50, ["name", "score", "номер"], SC.map((r, i) => [r[0]!, r[1]!, i + 1]), [70, 60, 50], { size: 9, hot: [0, 1, 2, 3] })],
    [...tbl("t", 70, 50, ["name", "score", "RANK"], SC.map((r, i) => [r[0]!, r[1]!, [1, 2, 2, 4][i]!]), [70, 60, 50], { size: 9, hot: [1, 2] }), Tx("n", 300, 100, "места 3 нет", { size: 8.5, c: "y" })],
    [...tbl("t", 70, 50, ["name", "score", "DENSE"], SC.map((r, i) => [r[0]!, r[1]!, [1, 2, 2, 3][i]!]), [70, 60, 50], { size: 9, hot: [1, 2] }), Tx("n", 300, 100, "без пропусков", { size: 8.5, c: "g" })],
  ],
});

// 7. Топ-N в группе
const PRD: Row[] = [
  ["Планшет", "Эл.", 12000, 1],
  ["Наушники", "Эл.", 8000, 2],
  ["Колонка", "Эл.", 3000, 3],
  ["Книга", "Кн.", 1500, 1],
  ["Блокнот", "Кн.", 300, 2],
];
export const V07 = scene({
  labels: ["Нумеруем", "Фильтруем снаружи", "Почему не LIMIT"],
  caption: [
    "Внутри категории нумеруем товары по цене: ROW_NUMBER … PARTITION BY category",
    "Оконную функцию в WHERE нельзя: берём номера не больше двух во внешнем запросе",
    "LIMIT ограничил бы весь результат, а не каждую категорию",
  ],
  frames: [
    [sql("c", 10, 14, ["WITH r AS (SELECT *, ROW_NUMBER() OVER (", "  PARTITION BY category ORDER BY price DESC) AS rn", "  FROM products)"], [0, 1], { ...code, size: 9.5, lh: 13 }), ...tbl("t", 50, 70, ["title", "cat", "price", "rn"], PRD, [76, 40, 56, 40], { size: 8, hot: [0, 1, 2, 3, 4], cell: 16 })],
    [sql("c", 10, 14, ["SELECT * FROM r WHERE rn <= 2;"], [0], code), ...tbl("t", 50, 50, ["title", "cat", "price", "rn"], PRD, [76, 40, 56, 40], { size: 8, hot: [0, 1, 3, 4], dim: [2], cell: 16 })],
    [Box("a", 90, 70, 150, 40, "LIMIT 2:\nвсего две строки", "r", { size: 9.5 }), Box("b", 270, 70, 150, 40, "rn <= 2:\nпо две в категории", "g", { size: 9.5 })],
  ],
});

// 8. LAG и LEAD
export const V08 = scene({
  labels: ["LAG", "Изменение", "LEAD"],
  caption: [
    "LAG(total) — значение предыдущей строки; у первой — NULL",
    "total − LAG(total): рост к предыдущему месяцу",
    "LEAD(total) — значение следующей строки",
  ],
  frames: [
    [sql("c", 10, 14, ["LAG(total) OVER (ORDER BY m)"], [0], code), ...T(["m", "total", "LAG"], [["янв", 100, "NULL"], ["фев", 150, 100], ["мар", 120, 150], ["апр", 180, 120]], 80, 50, [50, 60, 60], [1, 2, 3])],
    [sql("c", 10, 14, ["total - LAG(total) OVER (ORDER BY m)"], [0], code), ...T(["m", "total", "рост"], [["янв", 100, "NULL"], ["фев", 150, 50], ["мар", 120, -30], ["апр", 180, 60]], 80, 50, [50, 60, 60], [1, 2, 3])],
    [sql("c", 10, 14, ["LEAD(total) OVER (ORDER BY m)"], [0], code), ...T(["m", "total", "LEAD"], [["янв", 100, 150], ["фев", 150, 120], ["мар", 120, 180], ["апр", 180, "NULL"]], 80, 50, [50, 60, 60], [0, 1, 2])],
  ],
});

// 9. FIRST_VALUE и LAST_VALUE
export const V09 = scene({
  labels: ["FIRST_VALUE", "LAST_VALUE по умолчанию", "Расширенная рамка"],
  caption: [
    "FIRST_VALUE(total) — значение первой строки окна: 100 в каждой строке",
    "LAST_VALUE без указаний даёт значение текущей строки: рамка кончается на ней",
    "Расширьте рамку до конца окна — получите настоящую последнюю",
  ],
  frames: [
    [sql("c", 10, 14, ["FIRST_VALUE(total) OVER (ORDER BY m)"], [0], code), ...T(["m", "total", "first"], MON.map((r) => [r[0]!, r[1]!, 100]), 80, 50, [50, 60, 60], [0, 1, 2, 3])],
    [sql("c", 10, 14, ["LAST_VALUE(total) OVER (ORDER BY m)"], [0], code), ...T(["m", "total", "last"], MON.map((r) => [r[0]!, r[1]!, r[1]!]), 80, 50, [50, 60, 60], [0, 1, 2, 3]), Tx("n", 300, 100, "это сама\nстрока!", { size: 8.5, c: "r" })],
    [sql("c", 10, 14, ["LAST_VALUE(total) OVER (ORDER BY m", "  ROWS BETWEEN UNBOUNDED PRECEDING", "  AND UNBOUNDED FOLLOWING)"], [1, 2], { ...code, lh: 13, size: 9.5 }), ...T(["m", "total", "last"], MON.map((r) => [r[0]!, r[1]!, 180]), 80, 70, [50, 60, 60], [0, 1, 2, 3])],
  ],
});

// 10. Рамка окна
export const V10 = scene({
  labels: ["Три строки", "Скользящее среднее", "Рамки"],
  caption: [
    "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW — текущая и две предыдущие",
    "AVG по такой рамке — скользящее среднее за три месяца",
    "Рамка по умолчанию с ORDER BY: от начала окна до текущей — это накопительный итог",
  ],
  frames: [
    [...MON.map((r, i) => Box(`m${i}`, 60 + i * 80, 80, 66, 30, `${r[0]}: ${r[1]}`, i >= 1 && i <= 3 ? "g" : "m", { size: 9 })), Tx("n", 180, 130, "рамка апреля: фев, мар, апр", { size: 9.5 })],
    [sql("c", 10, 14, ["AVG(total) OVER (ORDER BY m", "  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)"], [0, 1], { ...code, lh: 13 }), ...T(["m", "total", "avg"], [["янв", 100, 100], ["фев", 150, 125], ["мар", 120, 123], ["апр", 180, 150]], 80, 62, [50, 60, 60], [0, 1, 2, 3])],
    [Box("a", 90, 70, 150, 40, "UNBOUNDED PRECEDING\n→ CURRENT ROW", "b", { size: 8.5 }), Box("b", 270, 70, 150, 40, "накопительный\nитог", "g", { size: 10 })],
  ],
});

// 11. NTILE и доли
export const V11 = scene({
  labels: ["NTILE(2)", "NTILE(4)", "Доля"],
  caption: [
    "NTILE(2) делит упорядоченные строки на две равные части",
    "NTILE(4) — квартили: верхняя четверть клиентов по сумме",
    "Доля строки в итоге: значение / SUM(значение) OVER ()",
  ],
  frames: [
    [...tbl("t", 80, 50, ["name", "s", "grp"], [["Анна", 90, 1], ["Борис", 80, 1], ["Вера", 60, 2], ["Глеб", 40, 2]], [60, 50, 50], { size: 9, hot: [0, 1] })],
    [
      ...[90, 80, 70, 60, 50, 40, 30, 20].map((v, i) => Box(`s${i}`, 30 + i * 43, 60, 38, 26, v, "b", { size: 10 })),
      ...[1, 1, 2, 2, 3, 3, 4, 4].map((q, i) => Box(`q${i}`, 30 + i * 43, 100, 38, 26, q, i < 2 ? "g" : "m", { size: 10 })),
      Tx("l1", 180, 40, "значение", { size: 8.5 }),
      Tx("l2", 180, 140, "квартиль (1 — верхняя четверть)", { size: 8.5 }),
    ],
    [sql("c", 10, 14, ["ROUND(100.0 * s / SUM(s) OVER ())"], [0], code), ...tbl("t", 90, 56, ["name", "s", "%"], [["Анна", 90, 36], ["Борис", 80, 32], ["Вера", 80, 32]], [60, 50, 50], { size: 9, hot: [0, 1, 2] })],
  ],
});

// 12. Порядок выполнения
export const V12 = scene({
  labels: ["Место окон", "WHERE влияет", "Условие на окно"],
  caption: [
    "FROM → WHERE → GROUP BY → HAVING → окна → SELECT → ORDER BY → LIMIT",
    "Окно видит только строки, прошедшие WHERE — фильтр меняет его результат",
    "Условие на значение оконной функции — только во внешнем запросе",
  ],
  frames: [
    [Box("a", 44, 80, 62, 30, "WHERE", "b", { size: 9.5 }), Box("b", 114, 80, 62, 30, "GROUP BY", "b", { size: 8.5 }), Box("c", 184, 80, 62, 30, "HAVING", "b", { size: 9.5 }), Box("d", 254, 80, 62, 30, "ОКНА", "g", { size: 10 }), Box("e", 324, 80, 62, 30, "ORDER BY", "b", { size: 8.5 })],
    [sql("c", 10, 20, ["SELECT SUM(total) OVER () FROM orders", "WHERE status = 'paid';"], [1], code), Tx("n", 180, 110, "в сумме — только оплаченные", { size: 10, c: "g" })],
    [sql("c", 10, 20, ["SELECT * FROM t WHERE ROW_NUMBER() OVER (…) = 1;"], undefined, { ...code, bad: [0], size: 9.5 }), Box("g", 180, 110, 260, 28, "оберните в CTE и фильтруйте снаружи", "g", { size: 9.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Формула окна", "Семейства функций", "Дальше"],
  caption: [
    "OVER (PARTITION BY … ORDER BY … ROWS …): разбиение, порядок, рамка",
    "Агрегаты, нумерация, ранги, LAG/LEAD, FIRST/LAST_VALUE, NTILE",
    "Последняя тема части — представления: именованные запросы",
  ],
  frames: [
    [Box("a", 65, 60, 110, 30, "PARTITION BY", "b", { size: 9.5 }), Box("b", 180, 60, 110, 30, "ORDER BY", "b", { size: 10 }), Box("c", 295, 60, 110, 30, "ROWS …", "b", { size: 10 })],
    [Box("a", 65, 50, 110, 26, "SUM AVG COUNT", "g", { size: 9 }), Box("b", 180, 50, 110, 26, "ROW_NUMBER RANK", "g", { size: 8 }), Box("c", 295, 50, 110, 26, "LAG LEAD", "g", { size: 9.5 }), Box("d", 122, 96, 110, 26, "FIRST/LAST_VALUE", "g", { size: 8 }), Box("e", 238, 96, 110, 26, "NTILE", "g", { size: 9.5 })],
    [sql("c", 20, 40, ["CREATE VIEW v AS", "  SELECT …;"], [0, 1], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
