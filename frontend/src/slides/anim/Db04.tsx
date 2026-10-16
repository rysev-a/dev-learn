import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, sql, tbl } from "./db.tsx";

/* Глава 4 книги «Базы данных»: работа с текстом и пропусками (NULL). */

const CUST = [
  ["Анна", "Москва", "anna@mail.ru"],
  ["Борис", "Казань", "boris@gmail.com"],
  ["Вера", "Москва", "NULL"],
  ["Жанна", "NULL", "zhanna@yandex.ru"],
] as const;
const CH = ["name", "city", "email"];
const CWD = [56, 66, 112];
const code = { w: 340, size: 10, lh: 14 };
const CT = (hot: number[] = [], dim: number[] = [], x = 20) => tbl("t", x, 60, CH, CUST, CWD, { size: 8, hot, dim });

// 1. Что такое NULL
export const V01 = scene({
  labels: ["Неполные данные", "Не ноль", "Особое значение"],
  caption: [
    "У клиента не указан город или почта: данные в жизни неполны",
    "NULL — не ноль и не пустая строка: те — известные значения",
    "NULL значит «значения нет или оно неизвестно»; операции над ним дают тоже неизвестное",
  ],
  frames: [
    [...CT(), Box("n", 300, 140, 100, 22, "дыры в данных", "y", { size: 8.5 })],
    [
      Box("a", 70, 60, 100, 36, "0\nчисло ноль", "b", { size: 9.5 }),
      Box("b", 180, 60, 100, 36, "''\nпустая строка", "b", { size: 9.5 }),
      Box("c", 290, 60, 100, 36, "NULL\nнеизвестно", "y", { size: 9.5 }),
    ],
    [Box("c", 180, 50, 120, 36, "NULL", "y", { size: 14 }), Tx("n", 180, 110, "NULL + 1 → NULL     'а' || NULL → NULL", { size: 9.5 })],
  ],
});

// 2. IS NULL
export const V02 = scene({
  labels: ["= NULL", "IS NULL", "IS NOT NULL"],
  caption: [
    "Сравнение «город = NULL» не вернёт ничего, даже если пропуски есть",
    "IS NULL даёт честные истину или ложь: находит клиентов без города",
    "IS NOT NULL оставляет тех, у кого значение известно",
  ],
  frames: [
    [sql("c", 10, 14, ["WHERE city = NULL;"], undefined, { ...code, bad: [0] }), ...CT([], [0, 1, 2, 3]), Box("n", 300, 140, 100, 22, "0 строк", "r", { size: 9 })],
    [sql("c", 10, 14, ["WHERE city IS NULL;"], [0], code), ...CT([3], [0, 1, 2])],
    [sql("c", 10, 14, ["WHERE email IS NOT NULL;"], [0], code), ...CT([0, 1, 3], [2])],
  ],
});

// 3. Три значения
const TRI = [
  ["T AND U", "U"],
  ["F AND U", "F"],
  ["T OR U", "T"],
  ["F OR U", "U"],
] as const;
export const V03 = scene({
  labels: ["Три значения", "Связки", "Фильтр WHERE"],
  caption: [
    "Логика трёхзначная: истина, ложь и неизвестно",
    "Ложь побеждает в AND, истина побеждает в OR; в остальных случаях — неизвестно",
    "WHERE пропускает только TRUE: ложь и неизвестно одинаково отбрасываются",
  ],
  frames: [
    [Box("t", 70, 70, 80, 36, "TRUE", "g", { size: 11 }), Box("f", 180, 70, 80, 36, "FALSE", "r", { size: 11 }), Box("u", 290, 70, 80, 36, "UNKNOWN", "y", { size: 10 })],
    [...tbl("t", 100, 50, ["выражение", "результат"], TRI, [90, 70], { size: 9 })],
    [
      Box("t", 70, 70, 80, 36, "TRUE", "g", { size: 11 }),
      Box("f", 180, 70, 80, 36, "FALSE", "m", { size: 11, o: 0.4 }),
      Box("u", 290, 70, 80, 36, "UNKNOWN", "m", { size: 10, o: 0.4 }),
      Tx("n", 180, 130, "в результат попадает только TRUE", { size: 9.5 }),
    ],
  ],
});

// 4. Отрицание и пропуски
export const V04 = scene({
  labels: ["<> теряет NULL", "Явное условие", "IS NOT"],
  caption: [
    "«Город не Москва» не вернёт Жанну: NULL <> 'Москва' — неизвестно",
    "Добавим OR city IS NULL, чтобы включить и клиентов без города",
    "IS NOT сравнивает, считая NULL значением, и не возвращает неизвестное",
  ],
  frames: [
    [sql("c", 10, 14, ["WHERE city <> 'Москва';"], [0], code), ...CT([1], [0, 2, 3]), Tx("n", 300, 140, "Жанна потеряна", { size: 8.5, c: "r" })],
    [sql("c", 10, 14, ["WHERE city <> 'Москва'", "   OR city IS NULL;"], [0, 1], code), ...CT([1, 3], [0, 2])],
    [sql("c", 10, 14, ["WHERE city IS NOT 'Москва';"], [0], code), ...CT([1, 3], [0, 2]), Tx("n", 300, 140, "короткая форма", { size: 8.5, c: "g" })],
  ],
});

// 5. Арифметика с NULL
export const V05 = scene({
  labels: ["Сумма", "Склейка", "Потери"],
  caption: [
    "10 + NULL даёт NULL: не зная слагаемого, не знаем суммы",
    "Имя, запятая и пустой город — вся подпись превращается в NULL",
    "Каждое «потенциально пустое» значение — потенциальная дыра в результате",
  ],
  frames: [
    [sql("c", 10, 20, ["SELECT 10 + NULL;"], [0], code), ...tbl("t", 140, 70, ["10 + NULL"], [["NULL"]], [80], { size: 9, hot: [0], c: "y" })],
    [
      sql("c", 10, 14, ["SELECT name || ', ' || city FROM customers;"], [0], code),
      ...tbl("t", 100, 56, ["label"], [["Анна, Москва"], ["Борис, Казань"], ["Вера, Москва"], ["NULL"]], [140], { size: 8.5, hot: [3], c: "b" }),
    ],
    [Box("a", 180, 60, 280, 30, "любой NULL в выражении → весь результат NULL", "y", { size: 9.5 }), Tx("n", 180, 110, "нужна подстановка запасного значения", { size: 9.5 })],
  ],
});

// 6. COALESCE
export const V06 = scene({
  labels: ["Первое непустое", "Склейка без потерь", "IFNULL"],
  caption: [
    "COALESCE берёт первый аргумент, который не NULL",
    "Оборачиваем пустое значение в COALESCE — подпись не пропадает",
    "IFNULL(a, b) — короткая форма для двух аргументов",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT COALESCE(NULL, NULL, 'нет', 'x');"], [0], code),
      ...tbl("t", 130, 70, ["результат"], [["нет"]], [100], { size: 10, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT name || ', ' || COALESCE(city, '—')", "FROM customers;"], [0], code),
      ...tbl("t", 100, 60, ["label"], [["Анна, Москва"], ["Борис, Казань"], ["Вера, Москва"], ["Жанна, —"]], [140], { size: 8.5, hot: [3] }),
    ],
    [
      sql("c", 10, 20, ["SELECT IFNULL(city, 'не указан')", "FROM customers;"], [0], code),
      ...tbl("t", 110, 70, ["city"], [["Москва"], ["Казань"], ["Москва"], ["не указан"]], [110], { size: 8.5, hot: [3] }),
    ],
  ],
});

// 7. NULLIF
export const V07 = scene({
  labels: ["Равны — NULL", "Деление на ноль", "Пустая строка"],
  caption: [
    "NULLIF(a, b) возвращает NULL, если a равно b, иначе — a",
    "Знаменатель в NULLIF(x, 0): при нуле получим NULL, а не ошибку",
    "NULLIF(email, '') превращает пустую строку в настоящий NULL",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT NULLIF(5, 5), NULLIF(5, 3);"], [0], code),
      ...tbl("t", 100, 66, ["NULLIF(5,5)", "NULLIF(5,3)"], [["NULL", 5]], [80, 80], { size: 9, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT total / NULLIF(cnt, 0)", "FROM stats;"], [0], code),
      ...tbl("t", 80, 66, ["total", "cnt", "результат"], [[100, 4, 25], [50, 0, "NULL"]], [60, 60, 70], { size: 9, hot: [1] }),
    ],
    [
      sql("c", 10, 14, ["SELECT NULLIF(email, '') FROM users;"], [0], code),
      ...tbl("t", 100, 66, ["email", "NULLIF"], [["a@x.ru", "a@x.ru"], ["", "NULL"]], [90, 80], { size: 9, hot: [1] }),
    ],
  ],
});

// 8. NULL = NULL
export const V08 = scene({
  labels: ["NULL = NULL", "IS", "DISTINCT"],
  caption: [
    "Оператор = для двух NULL возвращает неизвестно — условие не проходит",
    "IS и IS NOT считают пропуски одинаковыми и дают только 0 или 1",
    "DISTINCT и GROUP BY считают все NULL одним значением",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT NULL = NULL,", "       NULL <> NULL;"], [0, 1], code),
      ...tbl("t", 100, 66, ["NULL = NULL", "NULL <> NULL"], [["NULL", "NULL"]], [90, 90], { size: 9, c: "y", hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT NULL IS NULL,", "       1 IS NOT NULL;"], [0, 1], code),
      ...tbl("t", 100, 66, ["NULL IS NULL", "1 IS NOT NULL"], [[1, 1]], [90, 90], { size: 9, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT DISTINCT city FROM customers;"], [0], code),
      ...tbl("t", 120, 50, ["city"], [["Москва"], ["Казань"], ["NULL"]], [100], { size: 9, hot: [2] }),
      Tx("n", 300, 100, "пустые города\nслились в один", { size: 8.5, c: "y" }),
    ],
  ],
});

// 9. Регистр
export const V09 = scene({
  labels: ["UPPER / LOWER", "LENGTH", "TRIM"],
  caption: [
    "UPPER и LOWER меняют регистр; для кириллицы по умолчанию не работают",
    "LENGTH возвращает число символов строки",
    "TRIM убирает пробелы по краям — важно при сравнении введённых значений",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT UPPER('nova'), LOWER('SONIC'),", "       UPPER('книга');"], [0, 1], code),
      ...tbl("t", 70, 66, ["UPPER", "LOWER", "UPPER(рус)"], [["NOVA", "sonic", "книга"]], [70, 70, 80], { size: 9, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT LENGTH('SQL'), LENGTH('кот'),", "       LENGTH('');"], [0, 1], code),
      ...tbl("t", 110, 66, ["3 буквы", "кот", "пусто"], [[3, 3, 0]], [60, 50, 50], { size: 9, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT '[' || TRIM('  hi  ') || ']',", "       '[' || '  hi  ' || ']';"], [0, 1], code),
      ...tbl("t", 100, 66, ["с TRIM", "без TRIM"], [["[hi]", "[  hi  ]"]], [80, 90], { size: 9, hot: [0] }),
    ],
  ],
});

// 10. Срезы
export const V10 = scene({
  labels: ["SUBSTR", "INSTR", "REPLACE"],
  caption: [
    "SUBSTR(строка, с_какой, сколько): позиции считаются с единицы",
    "INSTR возвращает позицию первого вхождения или 0",
    "REPLACE заменяет все вхождения подстроки на новую",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT SUBSTR('Москва', 1, 3);"], [0], code),
      ...[..."Москва"].map((ch, i) => Box(`l${i}`, 70 + i * 36, 90, 32, 28, ch, i < 3 ? "g" : "m", { size: 12 })),
      Tx("n", 180, 136, "результат: Мос", { size: 10 }),
    ],
    [
      sql("c", 10, 14, ["SELECT INSTR('anna@mail.ru', '@');"], [0], code),
      ...[..."anna@mail.ru"].map((ch, i) => Box(`l${i}`, 40 + i * 25.5, 90, 23, 26, ch, ch === "@" ? "y" : "m", { size: 10 })),
      Tx("n", 180, 136, "позиция 5", { size: 10 }),
    ],
    [
      sql("c", 10, 14, ["SELECT REPLACE('a-b-c', '-', '+');"], [0], code),
      ...tbl("t", 130, 66, ["результат"], [["a+b+c"]], [90], { size: 10, hot: [0] }),
    ],
  ],
});

// 11. Домен почты
export const V11 = scene({
  labels: ["Позиция @", "Подстрока после", "Домены"],
  caption: [
    "Находим позицию знака @ с помощью INSTR",
    "Берём всё после неё: SUBSTR(email, INSTR(email, '@') + 1)",
    "Результат — домены; пустая почта даёт NULL",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT INSTR(email, '@')", "FROM customers;"], [0], code),
      ...tbl("t", 50, 60, ["email", "pos"], [["anna@mail.ru", 5], ["boris@gmail.com", 6], ["NULL", "NULL"]], [120, 50], { size: 8.5, hot: [0, 1] }),
    ],
    [
      sql("c", 10, 14, ["SELECT SUBSTR(email, INSTR(email, '@') + 1)", "FROM customers;"], [0], { ...code, size: 9.5 }),
      ...tbl("t", 50, 60, ["email", "domain"], [["anna@mail.ru", "mail.ru"], ["boris@gmail.com", "gmail.com"], ["NULL", "NULL"]], [120, 80], { size: 8.5, hot: [0, 1] }),
    ],
    [
      sql("c", 10, 14, ["… GROUP BY домен"], undefined, code),
      Box("a", 70, 70, 100, 28, "mail.ru ×2", "g", { size: 9.5 }),
      Box("b", 180, 70, 100, 28, "gmail.com ×1", "g", { size: 9.5 }),
      Box("c", 290, 70, 100, 28, "NULL ×1", "y", { size: 9.5 }),
    ],
  ],
});

// 12. GLOB
export const V12 = scene({
  labels: ["LIKE", "GLOB", "Набор символов"],
  caption: [
    "LIKE не различает регистр латиницы; кириллицу — различает",
    "GLOB различает регистр: * — любые символы, ? — один символ",
    "[а-я] — любой символ из набора: имена на строчную русскую букву",
  ],
  frames: [
    [sql("c", 10, 20, ["name LIKE 'a%'  -- Anna, anna"], [0], code), Box("n", 180, 100, 200, 28, "LIKE: регистр латиницы не важен", "b", { size: 9 })],
    [sql("c", 10, 20, ["name GLOB 'A*'  -- только Anna", "name GLOB 'A?na'"], [0, 1], code), Box("n", 180, 110, 200, 28, "GLOB: регистр важен", "g", { size: 9 })],
    [sql("c", 10, 20, ["name GLOB '[а-я]*'"], [0], code), Tx("n", 180, 100, "первая буква — строчная русская", { size: 9.5 })],
  ],
});

// 13. CAST
export const V13 = scene({
  labels: ["Число в текст", "Текст в число", "Итоги"],
  caption: [
    "CAST(price AS TEXT) превращает число в строку",
    "CAST('12abc' AS INTEGER) читает число с начала строки; мусор в начале даёт 0",
    "NULL, IS NULL, COALESCE, NULLIF и функции текста — набор первой части курса",
  ],
  frames: [
    [
      sql("c", 10, 14, ["SELECT CAST(1500 AS TEXT) || ' руб';"], [0], code),
      ...tbl("t", 110, 66, ["результат"], [["1500 руб"]], [120], { size: 10, hot: [0] }),
    ],
    [
      sql("c", 10, 14, ["SELECT CAST('12abc' AS INTEGER),", "       CAST('abc' AS INTEGER);"], [0, 1], code),
      ...tbl("t", 130, 66, ["12abc", "abc"], [[12, 0]], [70, 70], { size: 10, hot: [0] }),
    ],
    [
      Box("a", 65, 60, 110, 30, "IS NULL", "b", { size: 9.5 }),
      Box("b", 180, 60, 110, 30, "COALESCE", "b", { size: 9.5 }),
      Box("c", 295, 60, 110, 30, "NULLIF", "b", { size: 9.5 }),
      Box("d", 65, 104, 110, 30, "UPPER LOWER TRIM", "g", { size: 8.5 }),
      Box("e", 180, 104, 110, 30, "SUBSTR INSTR", "g", { size: 9 }),
      Box("f", 295, 104, 110, 30, "LIKE GLOB", "g", { size: 9.5 }),
    ],
  ],
});
