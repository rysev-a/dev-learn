import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 3 книги «Базы данных»: сортировка и ограничение строк. */

const PROD = [
  ["Ноутбук", "Электроника", 78000],
  ["Мышь", "Аксессуары", 1500],
  ["Чай", "Продукты", 420],
  ["Книга SQL", "Книги", 1200],
  ["Кофе", "Продукты", 890],
] as const;
const code = { w: 340, size: 10, lh: 14 };
// товары в заданном порядке индексов; hot — подсвеченные позиции результата
const P = (order: number[], hot: number[] = [], x = 20): ReturnType<typeof tbl> =>
  tbl("t", x, 56, ["title", "category", "price"], order.map((i) => PROD[i]!), [76, 84, 56], { size: 8, hot });
const ALL = [0, 1, 2, 3, 4];

// 1. Порядок не обещан
export const V01 = scene({
  labels: ["Как записали", "Другой запуск", "ORDER BY"],
  caption: [
    "Пока читаем таблицу целиком, строки приходят «как записали» — порядок кажется постоянным",
    "После индекса или условия порядок может измениться — приложение ломается",
    "Если порядок важен, его просят явно: ORDER BY",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT * FROM products;"], undefined, code), ...P(ALL)],
    [sql("c", 10, 14, ["SELECT * FROM products;"], undefined, code), ...P([2, 4, 0, 3, 1]), Tx("n", 300, 100, "другой порядок —\nне ошибка базы", { size: 8.5, c: "y" })],
    [sql("c", 10, 14, ["SELECT * FROM products", "ORDER BY price;"], [1], code), ...P([2, 4, 3, 1, 0], [0, 1, 2, 3, 4])],
  ],
});

// 2. ASC и DESC
export const V02 = scene({
  labels: ["По возрастанию", "По убыванию", "Скрытый ключ"],
  caption: [
    "ASC — по возрастанию, это порядок по умолчанию",
    "DESC — по убыванию: самые большие значения первыми",
    "Столбец сортировки не обязан быть в списке выбора",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT title, price FROM products", "ORDER BY price ASC;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [2, 4, 3, 1, 0].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5, hot: [0] })],
    [sql("c", 10, 14, ["SELECT title, price FROM products", "ORDER BY price DESC;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [0, 1, 3, 4, 2].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5, hot: [0] })],
    [sql("c", 10, 14, ["SELECT title FROM products", "ORDER BY price DESC;"], [1], code), ...tbl("t", 110, 56, ["title"], [0, 1, 3, 4, 2].map((i) => [PROD[i]![0]]), [100], { size: 8.5 }), Tx("n", 300, 100, "цены не видно,\nно порядок по ним", { size: 8, c: "y" })],
  ],
});

// 3. Сортировка текста
const WORDS = ["бег", "Арбуз", "арбуз", "Zebra", "apple"];
const WT = (order: number[]) => tbl("t", 120, 56, ["word"], order.map((i) => [WORDS[i]!]), [100], { size: 9 });
export const V03 = scene({
  labels: ["Побайтово", "Заглавные раньше", "Приведение регистра"],
  caption: [
    "SQLite сравнивает строки по кодам символов, а не «по-человечески»",
    "Заглавные латинские идут перед строчными, кириллица — после латиницы",
    "Нужен словарный порядок — приведите значения к одному регистру",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT word FROM words", "ORDER BY word;"], [1], code), ...WT([3, 4, 1, 2, 0]), Tx("n", 300, 100, "Z < a < А < а < б", { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT word FROM words", "ORDER BY word;"], [1], code), ...WT([3, 4, 1, 2, 0]), Box("n", 300, 70, 90, 34, "заглавные\nраньше строчных", "y", { size: 8 })],
    [sql("c", 10, 14, ["SELECT word FROM words", "ORDER BY LOWER(word);"], [1], code), ...WT([4, 1, 2, 0, 3]), Tx("n", 300, 100, "арбуз и Арбуз\nрядом", { size: 8.5, c: "g" })],
  ],
});

// 4. Несколько ключей
export const V04 = scene({
  labels: ["Один ключ", "Второй ключ", "Уникальный ключ"],
  caption: [
    "По одной категории товары одной категории идут в произвольном порядке",
    "Через запятую второй ключ: внутри категории — по цене убыванием",
    "Последним ключом ставят номер: порядок становится однозначным",
  ],
  frames: [
    [sql("c", 10, 14, ["ORDER BY category;"], [0], code), ...P([1, 3, 0, 4, 2], [])],
    [sql("c", 10, 14, ["ORDER BY category, price DESC;"], [0], code), ...P([1, 3, 0, 4, 2], [0, 1, 2, 3, 4])],
    [sql("c", 10, 14, ["ORDER BY category, price DESC, id;"], [0], code), ...P([1, 3, 0, 4, 2], [0, 1, 2, 3, 4]), Tx("n", 300, 100, "порядок строк\nопределён полностью", { size: 8.5, c: "g" })],
  ],
});

// 5. Что можно сортировать
export const V05 = scene({
  labels: ["Выражение", "Псевдоним", "Номер столбца"],
  caption: [
    "Ключом может быть выражение: длина названия",
    "ORDER BY выполняется после SELECT, поэтому псевдоним ему виден",
    "Можно указать номер столбца, но при правке запроса он «уедет»",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT title FROM products", "ORDER BY LENGTH(title);"], [1], code), ...tbl("t", 100, 56, ["title", "len"], [2, 1, 4, 3, 0].map((i) => [PROD[i]![0], PROD[i]![0].length]), [90, 40], { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT price * 2 AS dbl FROM products", "ORDER BY dbl;"], [1], code), ...tbl("t", 130, 56, ["dbl"], [840, 1780, 2400, 3000, 156000].map((v) => [v]), [60], { size: 8.5 }), Tx("n", 300, 100, "псевдоним виден", { size: 8.5, c: "g" })],
    [sql("c", 10, 14, ["SELECT title, price FROM products", "ORDER BY 2 DESC;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [0, 1, 3, 4, 2].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5, hot: [0, 1, 2, 3, 4] }), Tx("n", 300, 100, "2 — второй\nстолбец списка", { size: 8.5, c: "y" })],
  ],
});

// 6. NULL при сортировке
export const V06 = scene({
  labels: ["ASC", "DESC", "NULLS LAST"],
  caption: [
    "В SQLite NULL меньше любого значения, поэтому при ASC он идёт первым",
    "При DESC пустые значения оказываются в конце",
    "NULLS FIRST и NULLS LAST задают положение явно, не полагаясь на умолчание",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT brand FROM products", "ORDER BY brand ASC;"], [1], code), ...tbl("t", 120, 56, ["brand"], [[ "NULL"], ["NULL"], ["Keyra"], ["Nova"], ["Sonic"]], [100], { size: 9, hot: [0, 1] })],
    [sql("c", 10, 14, ["SELECT brand FROM products", "ORDER BY brand DESC;"], [1], code), ...tbl("t", 120, 56, ["brand"], [["Sonic"], ["Nova"], ["Keyra"], ["NULL"], ["NULL"]], [100], { size: 9, hot: [3, 4] })],
    [sql("c", 10, 14, ["SELECT brand FROM products", "ORDER BY brand ASC NULLS LAST;"], [1], code), ...tbl("t", 120, 56, ["brand"], [["Keyra"], ["Nova"], ["Sonic"], ["NULL"], ["NULL"]], [100], { size: 9, hot: [3, 4] })],
  ],
});

// 7. LIMIT
export const V07 = scene({
  labels: ["Первые три", "Строк меньше", "Нуль"],
  caption: [
    "LIMIT 3 оставляет три первые строки; какие они — зависит от сортировки",
    "Если строк меньше, вернётся сколько есть — без ошибки",
    "LIMIT 0 возвращает пустой результат",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT title FROM products", "LIMIT 3;"], [1], code), ...tbl("t", 110, 56, ["title"], PROD.map((r) => [r[0]]), [100], { size: 8.5, hot: [0, 1, 2], dim: [3, 4] })],
    [sql("c", 10, 14, ["SELECT title FROM products", "LIMIT 10;"], [1], code), ...tbl("t", 110, 56, ["title"], PROD.map((r) => [r[0]]), [100], { size: 8.5, hot: [0, 1, 2, 3, 4] }), Tx("n", 300, 100, "10 > 5:\nвернулось 5", { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT title FROM products", "LIMIT 0;"], [1], code), Box("n", 180, 100, 160, 30, "0 строк", "m", { size: 10 })],
  ],
});

// 8. Топ-N
export const V08 = scene({
  labels: ["Сортируем", "Отрезаем", "Без сортировки"],
  caption: [
    "Сначала ORDER BY расставляет все строки по цене убыванием",
    "Потом LIMIT 3 оставляет первые три — топ дорогих товаров",
    "Без ORDER BY те же три строки были бы случайными",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT title, price FROM products", "ORDER BY price DESC LIMIT 3;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [0, 1, 3, 4, 2].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT title, price FROM products", "ORDER BY price DESC LIMIT 3;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [0, 1, 3, 4, 2].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5, hot: [0, 1, 2], dim: [3, 4] })],
    [sql("c", 10, 14, ["SELECT title, price FROM products", "LIMIT 3;"], [1], code), ...tbl("t", 80, 56, ["title", "price"], [2, 4, 0, 3, 1].map((i) => [PROD[i]![0], PROD[i]![2]]), [90, 60], { size: 8.5, hot: [0, 1, 2], dim: [3, 4], c: "r" }), Tx("n", 300, 100, "случайные три", { size: 8.5, c: "r" })],
  ],
});

// 9. OFFSET
const NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const PG = (hot: number[]) => NUMS.map((n, i) => Box(`n${n}`, 30 + i * 33, 120, 28, 24, n, hot.includes(i) ? "g" : "m", { size: 10 }));
export const V09 = scene({
  labels: ["Страница 1", "Страница 2", "Страница 3"],
  caption: [
    "LIMIT 3 OFFSET 0 — первые три строки",
    "LIMIT 3 OFFSET 3 — три строки после пропуска трёх",
    "LIMIT 3 OFFSET 6 — смещение = (страница − 1) × размер",
  ],
  frames: [
    [sql("c", 10, 20, ["SELECT id FROM t ORDER BY id", "LIMIT 3 OFFSET 0;"], [1], code), ...PG([0, 1, 2])],
    [sql("c", 10, 20, ["SELECT id FROM t ORDER BY id", "LIMIT 3 OFFSET 3;"], [1], code), ...PG([3, 4, 5])],
    [sql("c", 10, 20, ["SELECT id FROM t ORDER BY id", "LIMIT 3 OFFSET 6;"], [1], code), ...PG([6, 7, 8])],
  ],
});

// 10. Ловушки пагинации
export const V10 = scene({
  labels: ["Читаем и отбрасываем", "Сдвиг страниц", "По ключу"],
  caption: [
    "OFFSET 20000 заставляет базу найти и выбросить 20000 строк — поздние страницы медленнее",
    "Если между запросами добавилась запись, страницы сдвигаются: строка появится дважды",
    "Листание по ключу: «id > последний увиденный» работает одинаково быстро всегда",
  ],
  frames: [
    [
      ...NUMS.map((n, i) => Box(`n${n}`, 30 + i * 33, 70, 28, 24, n, i < 7 ? "r" : "g", { size: 10 })),
      Tx("a", 130, 110, "прочитано и выброшено", { size: 9, c: "r" }),
      Tx("b", 300, 110, "страница", { size: 9, c: "g" }),
    ],
    [
      Box("p1", 70, 50, 110, 28, "страница 1: 4 5 6", "b", { size: 9 }),
      Box("new", 180, 90, 100, 24, "вставлена строка", "y", { size: 9 }),
      Box("p2", 290, 50, 110, 28, "страница 2: 6 7 8", "r", { size: 9 }),
      Tx("n", 180, 130, "6 показана дважды", { size: 9, c: "r" }),
    ],
    [
      sql("c", 10, 20, ["SELECT * FROM t", "WHERE id > :last", "ORDER BY id LIMIT 3;"], [1], code),
      Tx("n", 300, 70, "last — id\nпоследней\nстроки", { size: 8.5 }),
    ],
  ],
});

// 11. Порядок выполнения
export const V11 = scene({
  labels: ["Пять шагов", "Город без повторов", "Топ в категории"],
  caption: [
    "FROM → WHERE → SELECT (DISTINCT) → ORDER BY → LIMIT",
    "DISTINCT убирает повторы, ORDER BY упорядочивает уже уникальное",
    "Условие отбирает категорию, сортировка ставит дорогие первыми, лимит берёт три",
  ],
  frames: [
    [
      Box("a", 40, 80, 62, 30, "FROM", "b", { size: 9 }),
      Box("b", 110, 80, 62, 30, "WHERE", "g", { size: 9 }),
      Box("c", 180, 80, 62, 30, "SELECT\nDISTINCT", "y", { size: 8 }),
      Box("d", 250, 80, 62, 30, "ORDER BY", "b", { size: 8.5 }),
      Box("e", 320, 80, 62, 30, "LIMIT", "g", { size: 9 }),
    ],
    [sql("c", 10, 14, ["SELECT DISTINCT city FROM customers", "ORDER BY city;"], [0, 1], code), ...tbl("t", 120, 56, ["city"], [["Казань"], ["Москва"], ["Тверь"]], [100], { size: 9, hot: [0, 1, 2] })],
    [sql("c", 10, 14, ["SELECT title, price FROM products", "WHERE category = 'Продукты'", "ORDER BY price DESC LIMIT 3;"], [1, 2], { ...code, lh: 13 }), ...tbl("t", 80, 76, ["title", "price"], [[ "Кофе", 890], ["Чай", 420]], [90, 60], { size: 8.5, hot: [0, 1] })],
  ],
});

// 12. Второй по цене
const PR = [78000, 78000, 45000, 5200];
export const V12 = scene({
  labels: ["Окно", "Повторы цены", "DISTINCT"],
  caption: [
    "Второй по стоимости: сортируем по убыванию, пропускаем одну строку, берём одну",
    "Если две первые цены одинаковы, запрос вернёт вторую по порядку, а не по значению",
    "Второе различное значение: сначала DISTINCT, потом сортировка и пропуск",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT price FROM products", "ORDER BY price DESC", "LIMIT 1 OFFSET 1;"], [2], { ...code, lh: 13 }),
      ...tbl("t", 130, 66, ["price"], [[78000], [45000], [5200]], [70], { size: 8.5, hot: [1], dim: [0, 2] }),
    ],
    [
      sql("c", 10, 14, ["SELECT price FROM products", "ORDER BY price DESC", "LIMIT 1 OFFSET 1;"], [2], { ...code, lh: 13 }),
      ...tbl("t", 130, 66, ["price"], PR.map((v) => [v]), [70], { size: 8.5, hot: [1], c: "r" }),
      Tx("n", 290, 110, "снова 78000", { size: 8.5, c: "r" }),
    ],
    [
      sql("c", 10, 14, ["SELECT DISTINCT price FROM products", "ORDER BY price DESC", "LIMIT 1 OFFSET 1;"], [0], { ...code, lh: 13 }),
      ...tbl("t", 130, 66, ["price"], [[78000], [45000], [5200]], [70], { size: 8.5, hot: [1], dim: [0, 2] }),
      Tx("n", 290, 110, "45000", { size: 9, c: "g" }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Инструменты", "Окно", "Дальше"],
  caption: [
    "ORDER BY: ключи, направление, выражения, псевдонимы и положение пустых значений",
    "LIMIT и OFFSET вырезают окно из упорядоченного результата",
    "Следующая тема — пустые значения NULL и работа с текстом",
  ],
  frames: [
    [
      Box("a", 65, 60, 110, 30, "ORDER BY", "b", { size: 9.5 }),
      Box("b", 180, 60, 110, 30, "ASC / DESC", "b", { size: 9.5 }),
      Box("c", 295, 60, 110, 30, "NULLS LAST", "b", { size: 9.5 }),
    ],
    [
      Box("a", 90, 60, 130, 30, "LIMIT n", "g", { size: 10 }),
      Box("b", 270, 60, 130, 30, "OFFSET m", "g", { size: 10 }),
      Tx("n", 180, 110, "топ-N и страницы", { size: 10 }),
    ],
    [sql("c", 20, 50, ["SELECT * FROM customers", "WHERE city IS NULL;"], [1], { ...code, size: 11, lh: 17 }), arrow("e", 180, 120, 180, 132, "g")],
  ],
});
