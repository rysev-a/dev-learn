import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 10 книги «Базы данных»: условная логика CASE WHEN. */

const PR = [
  ["Чай", 420],
  ["Мышь", 1500],
  ["Смартфон", 45000],
  ["Блокнот", 250],
] as const;
const ST = [
  ["paid", 4200],
  ["new", 1500],
  ["shipped", 79500],
  ["cancelled", 3900],
  ["paid", 5200],
] as const;
const code = { w: 340, size: 10, lh: 14 };

// 1. Если… то…
export const V01 = scene({
  labels: ["Значение по условию", "Выражение", "Где можно"],
  caption: [
    "Нужна метка, зависящая от значения: «дёшево», «дорого»",
    "CASE — не команда, а выражение: оно возвращает значение",
    "Поэтому его можно ставить в SELECT, WHERE, ORDER BY, агрегаты и UPDATE",
  ],
  frames: [
    [...tbl("t", 70, 50, ["title", "price"], PR, [90, 80], { size: 8.5 }), Tx("n", 300, 100, "какая\nкатегория?", { size: 9, c: "y" })],
    [sql("c", 10, 30, ["CASE WHEN price < 1000 THEN 'дёшево'", "     ELSE 'дорого' END"], [0, 1], { ...code, size: 10.5, lh: 16 })],
    [
      Box("a", 70, 50, 100, 26, "SELECT", "g", { size: 9.5 }),
      Box("b", 180, 50, 100, 26, "WHERE", "g", { size: 9.5 }),
      Box("c", 290, 50, 100, 26, "ORDER BY", "g", { size: 9.5 }),
      Box("d", 70, 96, 100, 26, "SUM(CASE …)", "g", { size: 9 }),
      Box("e", 180, 96, 100, 26, "UPDATE", "g", { size: 9.5 }),
    ],
  ],
});

// 2. Поисковый CASE
const LAB = (mark: (p: number) => string) => PR.map((r) => [r[0], r[1], mark(r[1])]);
const cheap = (p: number) => (p < 1000 ? "дёшево" : p < 10000 ? "средне" : "дорого");
export const V02 = scene({
  labels: ["Ветки", "Проверка по порядку", "Результат"],
  caption: [
    "CASE WHEN условие THEN значение … ELSE значение END",
    "Условия проверяются по порядку; берётся первая сработавшая ветка",
    "Каждая строка получила метку по своей цене",
  ],
  frames: [
    [sql("c", 10, 14, ["CASE", "  WHEN price < 1000  THEN 'дёшево'", "  WHEN price < 10000 THEN 'средне'", "  ELSE 'дорого'", "END AS label"], [1, 2, 3], { ...code, lh: 13 })],
    [sql("c", 10, 14, ["CASE", "  WHEN price < 1000  THEN 'дёшево'", "  WHEN price < 10000 THEN 'средне'", "  ELSE 'дорого'", "END AS label"], [2], { ...code, lh: 13 }), Tx("n", 290, 110, "1500: первая\nветка — нет,\nвторая — да", { size: 8.5, c: "g" })],
    [...tbl("t", 50, 50, ["title", "price", "label"], LAB(cheap), [80, 60, 80], { size: 8.5, hot: [0, 1, 2, 3] })],
  ],
});

// 3. Простой CASE
const RU = (s: string) => ({ paid: "Оплачен", new: "Новый", shipped: "Отправлен", cancelled: "Отменён" })[s as "paid"] ?? s;
export const V03 = scene({
  labels: ["Сравнение значений", "Названия", "Ограничение"],
  caption: [
    "CASE x WHEN значение THEN … — выражение сравнивается с набором значений",
    "Технические статусы превращаются в понятные названия",
    "Простая форма сравнивает только на равенство — с NULL не работает",
  ],
  frames: [
    [sql("c", 10, 14, ["CASE status", "  WHEN 'paid'      THEN 'Оплачен'", "  WHEN 'new'       THEN 'Новый'", "  WHEN 'shipped'   THEN 'Отправлен'", "  ELSE status END"], [1, 2, 3], { ...code, lh: 13, size: 9.5 })],
    [...tbl("t", 70, 46, ["status", "название"], ST.slice(0, 4).map((r) => [r[0], RU(r[0])]), [80, 90], { size: 8.5, hot: [0, 1, 2, 3] })],
    [sql("c", 10, 20, ["CASE x WHEN NULL THEN 'пусто' END", "-- никогда: NULL = NULL не истина"], undefined, { ...code, bad: [0] }), Box("g", 180, 100, 280, 28, "для пропусков: WHEN x IS NULL", "g", { size: 9.5 })],
  ],
});

// 4. ELSE и NULL
export const V04 = scene({
  labels: ["Есть ELSE", "Нет ELSE", "Явный ELSE"],
  caption: [
    "ELSE даёт значение для всех неподошедших строк",
    "Без ELSE результатом будет NULL — пропуски, которые ломают подсчёты",
    "Привычка: всегда писать ELSE, даже если там NULL — читателю ясно, что вы подумали",
  ],
  frames: [
    [sql("c", 10, 14, ["CASE WHEN price > 10000", "     THEN 'дорого' ELSE 'обычно' END"], [1], code), ...tbl("t", 80, 62, ["title", "метка"], [["Чай", "обычно"], ["Смартфон", "дорого"]], [80, 80], { size: 8.5, hot: [0, 1] })],
    [sql("c", 10, 14, ["CASE WHEN price > 10000", "     THEN 'дорого' END"], [1], code), ...tbl("t", 80, 62, ["title", "метка"], [["Чай", "NULL"], ["Смартфон", "дорого"]], [80, 80], { size: 8.5, hot: [0], c: "b" }), Tx("n", 290, 100, "пропуск у Чая", { size: 8.5, c: "y" })],
    [sql("c", 10, 20, ["CASE WHEN price > 10000", "     THEN 'дорого' ELSE NULL END"], [1], code), Tx("n", 180, 100, "ясно: пропуск — намеренно", { size: 10, c: "g" })],
  ],
});

// 5. Порядок веток
export const V05 = scene({
  labels: ["Неверный порядок", "Первая побеждает", "Верный порядок"],
  caption: [
    "Широкое условие стоит раньше узкого: price < 10000, потом price < 1000",
    "Цена 420 уже подошла под первую ветку — вторая недостижима",
    "От узкого к широкому: сначала < 1000, затем < 10000",
  ],
  frames: [
    [sql("c", 10, 14, ["CASE", "  WHEN price < 10000 THEN 'средне'", "  WHEN price < 1000  THEN 'дёшево'", "END"], [1, 2], { ...code, lh: 14 })],
    [sql("c", 10, 14, ["CASE", "  WHEN price < 10000 THEN 'средне'", "  WHEN price < 1000  THEN 'дёшево'", "END"], [1], { ...code, lh: 14, bad: [2] }), Box("e", 180, 112, 260, 28, "420 → «средне»: вторая ветка не нужна", "r", { size: 9.5 })],
    [sql("c", 10, 14, ["CASE", "  WHEN price < 1000  THEN 'дёшево'", "  WHEN price < 10000 THEN 'средне'", "END"], [1, 2], { ...code, lh: 14 }), Box("g", 180, 112, 260, 28, "420 → «дёшево»", "g", { size: 10 })],
  ],
});

// 6. Категоризация
const AMT = [1200, 5200, 79500, 3900, 55400];
const sz = (v: number) => (v < 5000 ? "малый" : v < 50000 ? "средний" : "крупный");
export const V06 = scene({
  labels: ["Суммы", "Размер", "Группировка"],
  caption: [
    "Суммы заказов — просто числа",
    "CASE превращает их в категории: малый, средний, крупный",
    "По категориям можно группировать: сколько заказов каждого размера",
  ],
  frames: [
    [...tbl("t", 120, 50, ["total"], AMT.map((v) => [v]), [90], { size: 9 })],
    [...tbl("t", 80, 50, ["total", "размер"], AMT.map((v) => [v, sz(v)]), [80, 90], { size: 9, hot: [0, 1, 2, 3, 4] })],
    [...tbl("t", 100, 60, ["размер", "заказов"], [["малый", 2], ["средний", 2], ["крупный", 1]], [90, 70], { size: 9, hot: [0, 1, 2] }), Tx("n", 180, 150, "GROUP BY CASE …", { size: 9.5 })],
  ],
});

// 7. CASE в ORDER BY
export const V07 = scene({
  labels: ["По алфавиту", "Свой порядок", "VIP вперёд"],
  caption: [
    "ORDER BY status даёт алфавит: cancelled, new, paid, shipped — не по жизненному циклу",
    "CASE присваивает каждому статусу число, и сортировка идёт по нему",
    "Тот же приём ставит вперёд нужные строки: VIP-клиентов",
  ],
  frames: [
    [sql("c", 10, 14, ["ORDER BY status;"], [0], code), ...tbl("t", 120, 46, ["status"], [["cancelled"], ["new"], ["paid"], ["shipped"]], [100], { size: 9 })],
    [sql("c", 10, 14, ["ORDER BY CASE status", "  WHEN 'new' THEN 1 WHEN 'paid' THEN 2", "  WHEN 'shipped' THEN 3 ELSE 4 END;"], [1, 2], { ...code, lh: 13, size: 9.5 }), ...tbl("t", 120, 66, ["status"], [["new"], ["paid"], ["shipped"], ["cancelled"]], [100], { size: 9, hot: [0, 1, 2, 3] })],
    [sql("c", 10, 14, ["ORDER BY CASE WHEN vip = 1", "         THEN 0 ELSE 1 END, name;"], [0, 1], code), ...tbl("t", 100, 56, ["name", "vip"], [["Анна", 1], ["Лев", 1], ["Борис", 0], ["Вера", 0]], [80, 50], { size: 9, hot: [0, 1] })],
  ],
});

// 8. Условный подсчёт
export const V08 = scene({
  labels: ["Единицы и нули", "SUM по условию", "Суммы по условию"],
  caption: [
    "CASE возвращает 1 для оплаченных заказов и 0 для остальных",
    "SUM складывает единицы — получаем число оплаченных за один проход",
    "Так же считают выручку: значение или нуль в двух соседних столбцах",
  ],
  frames: [
    [...tbl("t", 70, 40, ["status", "total", "paid?"], ST, [80, 60, 50], { size: 8.5, hot: [0, 4] }), Tx("n", 290, 100, "1 для paid,\n0 для остальных", { size: 8.5 })],
    [sql("c", 10, 14, ["SELECT SUM(CASE WHEN status = 'paid'", "              THEN 1 ELSE 0 END)", "FROM orders;"], [0, 1], { ...code, lh: 13 }), ...tbl("r", 140, 72, ["paid"], [[2]], [80], { size: 11, hot: [0] })],
    [sql("c", 10, 14, ["SELECT SUM(CASE WHEN status = 'paid'", "              THEN total ELSE 0 END) AS paid,", "       SUM(CASE WHEN status = 'cancelled'", "              THEN total ELSE 0 END) AS lost"], [0, 2], { ...code, lh: 13, size: 9.5 }), ...tbl("r", 100, 104, ["paid", "lost"], [[9400, 3900]], [70, 70], { size: 9, hot: [0] })],
  ],
});

// 9. Сводная таблица
export const V09 = scene({
  labels: ["Категории и статусы", "Столбец на значение", "Пересечения"],
  caption: [
    "Нужна таблица: категории в строках, статусы в столбцах",
    "Отдельной команды поворота нет: для каждого статуса — свой условный агрегат",
    "На пересечении — число заказов; значения должны быть известны заранее",
  ],
  frames: [
    [Box("a", 90, 70, 130, 36, "строки:\nкатегории", "b", { size: 10 }), Box("b", 270, 70, 130, 36, "столбцы:\nстатусы", "b", { size: 10 })],
    [sql("c", 10, 14, ["SELECT category,", "  SUM(status = 'paid') AS paid,", "  SUM(status = 'new')  AS new", "FROM orders GROUP BY category;"], [1, 2], { ...code, lh: 13 })],
    [...tbl("t", 80, 50, ["category", "paid", "new"], [["Книги", 3, 1], ["Еда", 5, 2], ["Техника", 1, 4]], [80, 50, 50], { size: 9, hot: [0, 1, 2] })],
  ],
});

// 10. CASE в UPDATE
export const V10 = scene({
  labels: ["Разные правила", "Одна команда", "Осторожно с ELSE"],
  caption: [
    "Электроника дорожает на 5%, книги — на 10%, остальное не меняется",
    "Одна команда и одна транзакция вместо трёх отдельных UPDATE",
    "Без ELSE price остальные строки получат NULL — оставляйте текущее значение",
  ],
  frames: [
    [Box("a", 70, 70, 110, 36, "Электроника\n+5%", "b", { size: 9.5 }), Box("b", 180, 70, 100, 36, "Книги\n+10%", "b", { size: 9.5 }), Box("c", 290, 70, 110, 36, "Остальное\n0%", "b", { size: 9.5 })],
    [sql("c", 10, 14, ["UPDATE products SET price = CASE category", "  WHEN 'Электроника' THEN price * 1.05", "  WHEN 'Книги'       THEN price * 1.10", "  ELSE price END;"], [1, 2, 3], { ...code, lh: 13, size: 9.5 })],
    [sql("c", 10, 20, ["UPDATE products SET price = CASE category", "  WHEN 'Книги' THEN price * 1.10 END;"], undefined, { ...code, bad: [1], size: 9.5 }), Box("e", 180, 112, 270, 28, "остальные цены стали NULL", "r", { size: 9.5 })],
  ],
});

// 11. IIF и родственники
export const V11 = scene({
  labels: ["IIF", "COALESCE и NULLIF", "Скалярные MIN и MAX"],
  caption: [
    "IIF(условие, если_да, если_нет) — CASE с одной веткой",
    "COALESCE — первое непустое, NULLIF — NULL при равенстве: частные случаи CASE",
    "MIN и MAX с несколькими аргументами выбирают из значений одной строки",
  ],
  frames: [
    [sql("c", 10, 20, ["SELECT IIF(price > 1000, 'дорого', 'дёшево')", "FROM products;"], [0], code)],
    [Box("a", 90, 70, 150, 40, "COALESCE(a, b)\n= CASE WHEN a IS NOT NULL …", "b", { size: 8 }), Box("b", 270, 70, 150, 40, "NULLIF(a, b)\n= CASE WHEN a = b THEN NULL …", "b", { size: 8 })],
    [sql("c", 10, 20, ["SELECT MAX(1, 5, 3), MIN(1, 5, 3);"], [0], code), ...tbl("r", 130, 70, ["MAX", "MIN"], [[5, 1]], [60, 60], { size: 10, hot: [0] })],
  ],
});

// 12. Типы и ловушки
export const V12 = scene({
  labels: ["Один тип", "NULL в условии", "Вынести логику"],
  caption: [
    "Ветки должны возвращать значения одного смысла: число и слово не смешивают",
    "Условие, которое стало NULL, не считается истинным — для пропусков нужна ветка IS NULL",
    "Один и тот же длинный CASE в нескольких местах — повод для представления или CTE",
  ],
  frames: [
    [Box("a", 90, 70, 150, 36, "THEN 1 … ELSE 'нет'\nсмешение типов", "r", { size: 9 }), Box("b", 270, 70, 150, 36, "THEN 1 … ELSE 0\nодин тип", "g", { size: 9 })],
    [sql("c", 10, 14, ["CASE WHEN city = 'Москва' THEN 'M'", "     WHEN city IS NULL   THEN '?'", "     ELSE 'др.' END"], [1], { ...code, lh: 13 }), Tx("n", 290, 100, "NULL = 'Москва'\nне истина", { size: 8.5, c: "y" })],
    [Box("a", 90, 70, 150, 36, "CASE в 5 запросах", "y", { size: 10 }), arrow("e", 168, 70, 192, 70, "m"), Box("b", 280, 70, 150, 36, "VIEW или CTE\nс одним CASE", "g", { size: 9.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Формы", "Применения", "Дальше"],
  caption: [
    "Поисковый и простой CASE, ELSE, порядок веток, IIF",
    "Категории, сортировка, условные агрегаты, сводные таблицы, UPDATE",
    "Следующая тема — встроенные функции: строки, числа и даты",
  ],
  frames: [
    [Box("a", 65, 60, 110, 30, "поисковый", "b", { size: 10 }), Box("b", 180, 60, 110, 30, "простой", "b", { size: 10 }), Box("c", 295, 60, 110, 30, "IIF", "b", { size: 10 })],
    [Box("a", 65, 50, 110, 26, "категории", "g", { size: 9.5 }), Box("b", 180, 50, 110, 26, "ORDER BY", "g", { size: 9.5 }), Box("c", 295, 50, 110, 26, "SUM(CASE)", "g", { size: 9.5 }), Box("d", 122, 96, 110, 26, "сводные", "g", { size: 9.5 }), Box("e", 238, 96, 110, 26, "UPDATE", "g", { size: 9.5 })],
    [sql("c", 20, 40, ["ROUND(x, 2)", "DATE('now')", "SUBSTR(s, 1, 3)"], [0, 1, 2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
