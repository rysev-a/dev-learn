import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 8 книги «Базы данных»: добавление, обновление и удаление данных (DML). */

type Row = readonly (string | number)[];
const CU: Row[] = [
  [1, "Анна", "Москва"],
  [2, "Борис", "Казань"],
  [3, "Вера", "Москва"],
];
const code = { w: 340, size: 10, lh: 14 };
const CT = (rows: Row[], hot: number[] = [], dim: number[] = [], x = 70, y = 70, c = "b") =>
  tbl("t", x, y, ["id", "name", "city"], rows, [30, 70, 80], { size: 8.5, hot, dim, c });

// 1. Меняем данные
export const V01 = scene({
  labels: ["Четыре действия", "INSERT, UPDATE, DELETE", "Цена ошибки"],
  caption: [
    "До сих пор мы только читали — SELECT",
    "Данные попадают в базу и меняются тремя командами",
    "Неудачный SELECT просто вернёт не то, неудачный UPDATE испортит данные",
  ],
  frames: [
    [Box("s", 180, 70, 120, 40, "SELECT\nчитать", "b", { size: 11 })],
    [
      Box("s", 50, 70, 80, 40, "SELECT\nчитать", "b", { size: 9.5 }),
      Box("i", 140, 70, 80, 40, "INSERT\nдобавить", "g", { size: 9.5 }),
      Box("u", 230, 70, 80, 40, "UPDATE\nизменить", "y", { size: 9.5 }),
      Box("d", 320, 70, 80, 40, "DELETE\nудалить", "r", { size: 9.5 }),
    ],
    [Box("a", 90, 70, 150, 40, "ошибка в SELECT:\nне то показали", "g", { size: 9.5 }), Box("b", 270, 70, 150, 40, "ошибка в UPDATE:\nиспорчены данные", "r", { size: 9.5 })],
  ],
});

// 2. INSERT
export const V02 = scene({
  labels: ["Команда", "Новая строка", "Явные столбцы"],
  caption: [
    "INSERT INTO таблица (столбцы) VALUES (значения в том же порядке)",
    "В таблице появляется строка; непереданные столбцы получают значения по умолчанию или NULL",
    "Всегда перечисляйте столбцы: порядок в таблице может измениться",
  ],
  frames: [
    [sql("c", 10, 14, ["INSERT INTO customers (id, name, city)", "VALUES (4, 'Глеб', 'Тверь');"], [0, 1], code), ...CT(CU, [], [], 70, 76)],
    [sql("c", 10, 14, ["INSERT INTO customers (id, name, city)", "VALUES (4, 'Глеб', 'Тверь');"], [0, 1], code), ...CT([...CU, [4, "Глеб", "Тверь"]], [3], [], 70, 76)],
    [sql("c", 10, 14, ["INSERT INTO customers VALUES (4, 'Глеб');", "-- ошибка: 2 значения вместо 3"], undefined, { ...code, bad: [0] }), Box("g", 180, 110, 260, 28, "список столбцов защищает от этого", "g", { size: 9.5 })],
  ],
});

// 3. Много строк
export const V03 = scene({
  labels: ["Одна за другой", "Один VALUES", "Всё или ничего"],
  caption: [
    "Три отдельных INSERT — три разбора команды",
    "Один VALUES с несколькими наборами через запятую — короче и быстрее",
    "Ошибка в любой строке — не добавится ни одна: команда выполняется целиком",
  ],
  frames: [
    [sql("c", 10, 14, ["INSERT INTO t (a) VALUES (1);", "INSERT INTO t (a) VALUES (2);", "INSERT INTO t (a) VALUES (3);"], [0, 1, 2], { ...code, lh: 13 }), Tx("n", 280, 90, "3 команды", { size: 9 })],
    [sql("c", 10, 14, ["INSERT INTO t (a) VALUES", "  (1), (2), (3);"], [1], code), ...[1, 2, 3].map((n, i) => Box(`n${n}`, 100 + i * 70, 100, 50, 28, n, "g", { size: 11 }))],
    [sql("c", 10, 14, ["INSERT INTO t (a) VALUES", "  (1), (2), (NULL);  -- NOT NULL"], undefined, { ...code, bad: [1] }), Box("e", 180, 100, 230, 28, "ни одна строка не добавлена", "r", { size: 9.5 })],
  ],
});

// 4. INSERT SELECT
export const V04 = scene({
  labels: ["Источник", "Копирование", "По порядку столбцов"],
  caption: [
    "В orders есть отменённые заказы — их нужно перенести в архив",
    "INSERT … SELECT добавляет в archive строки, которые вернул запрос",
    "Столбцы сопоставляются по порядку, а не по именам — следите за ним",
  ],
  frames: [
    [...tbl("o", 20, 40, ["id", "status"], [[1, "shipped"], [2, "cancelled"], [3, "cancelled"]], [30, 80], { size: 8.5, hot: [1, 2], dim: [0] }), Box("a", 270, 70, 90, 30, "archive\n(пусто)", "m", { size: 9 })],
    [
      sql("c", 10, 14, ["INSERT INTO archive (id, status)", "SELECT id, status FROM orders", "WHERE status = 'cancelled';"], [1, 2], { ...code, lh: 13 }),
      ...tbl("a", 100, 70, ["id", "status"], [[2, "cancelled"], [3, "cancelled"]], [30, 80], { size: 8.5, hot: [0, 1] }),
    ],
    [Box("a", 90, 70, 150, 40, "SELECT id, status", "b", { size: 9.5 }), arrow("e", 168, 70, 192, 70, "g"), Box("b", 280, 70, 150, 40, "INSERT (status, id)\n→ перепутаны!", "r", { size: 9 })],
  ],
});

// 5. UPDATE
export const V05 = scene({
  labels: ["Команда", "Условие отбирает строки", "Выражение"],
  caption: [
    "UPDATE … SET столбец = значение … WHERE условие",
    "Меняются только строки, подходящие под WHERE: Москва → Мск",
    "В правой части можно считать: цена × 1,1 — по старым значениям",
  ],
  frames: [
    [sql("c", 10, 14, ["UPDATE customers", "SET city = 'Мск'", "WHERE city = 'Москва';"], [1, 2], { ...code, lh: 13 }), ...CT(CU, [], [], 70, 76)],
    [sql("c", 10, 14, ["UPDATE customers", "SET city = 'Мск'", "WHERE city = 'Москва';"], [1, 2], { ...code, lh: 13 }), ...CT([[1, "Анна", "Мск"], [2, "Борис", "Казань"], [3, "Вера", "Мск"]], [0, 2], [1], 70, 76)],
    [sql("c", 10, 14, ["UPDATE products", "SET price = price * 1.1", "WHERE category = 'Книги';"], [1, 2], { ...code, lh: 13 }), ...tbl("p", 100, 76, ["title", "price"], [["Книга SQL", 1200], ["Книга Python", 1350]], [100, 60], { size: 8.5 }), Tx("n", 290, 110, "→ 1320, 1485", { size: 9, c: "g" })],
  ],
});

// 6. Без WHERE
export const V06 = scene({
  labels: ["С условием", "Без условия", "Привычка"],
  caption: [
    "С WHERE изменяется одна строка — как и задумано",
    "Без WHERE апдейт затрагивает все строки таблицы",
    "Сначала пишите WHERE, потом остальное; изменения — в транзакции",
  ],
  frames: [
    [sql("c", 10, 14, ["UPDATE customers SET city = 'Омск'", "WHERE id = 2;"], [1], code), ...CT([[1, "Анна", "Москва"], [2, "Борис", "Омск"], [3, "Вера", "Москва"]], [1], [0, 2], 70, 76)],
    [sql("c", 10, 14, ["UPDATE customers SET city = 'Омск';"], undefined, { ...code, bad: [0] }), ...CT([[1, "Анна", "Омск"], [2, "Борис", "Омск"], [3, "Вера", "Омск"]], [], [], 70, 76, "r")],
    [Box("a", 70, 60, 110, 30, "1. WHERE", "g", { size: 10 }), Box("b", 190, 60, 110, 30, "2. SELECT-проверка", "g", { size: 9 }), Box("c", 310, 60, 100, 30, "3. транзакция", "g", { size: 9.5 })],
  ],
});

// 7. DELETE
export const V07 = scene({
  labels: ["Условие", "Строка исчезла", "Внешний ключ"],
  caption: [
    "DELETE FROM таблица WHERE условие — удаляет подходящие строки",
    "Структура таблицы остаётся, исчезают только записи",
    "Нельзя удалить клиента, на которого ссылаются заказы — база напомнит ошибкой",
  ],
  frames: [
    [sql("c", 10, 14, ["DELETE FROM customers", "WHERE id = 2;"], [1], code), ...CT(CU, [1], [0, 2], 70, 76, "b")],
    [sql("c", 10, 14, ["DELETE FROM customers", "WHERE id = 2;"], [1], code), ...CT([CU[0]!, CU[2]!], [], [], 70, 76)],
    [sql("c", 10, 14, ["DELETE FROM customers WHERE id = 1;"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 280, 36, "FOREIGN KEY constraint failed:\nесть заказы клиента", "r", { size: 9.5 })],
  ],
});

// 8. Сначала SELECT
export const V08 = scene({
  labels: ["Тот же WHERE", "Считаем строки", "Теперь UPDATE"],
  caption: [
    "Возьмите условие будущего UPDATE и подставьте в SELECT",
    "Ожидали три строки, а получили тысячу — условие неверно",
    "Выборка устроила — меняем SELECT на UPDATE с тем же WHERE",
  ],
  frames: [
    [sql("c", 10, 20, ["SELECT * FROM products", "WHERE category = 'Книги';"], [1], code), ...tbl("r", 130, 70, ["id", "title"], [[10, "Книга SQL"], [11, "Книга Python"]], [40, 90], { size: 8.5, hot: [0, 1] })],
    [Box("a", 90, 70, 150, 40, "ожидали: 2 строки", "b", { size: 10 }), Box("b", 270, 70, 150, 40, "получили: 2 ✓", "g", { size: 10 })],
    [sql("c", 10, 20, ["UPDATE products SET price = price * 1.1", "WHERE category = 'Книги';"], [1], code), Tx("n", 180, 100, "проверенное условие", { size: 9.5, c: "g" })],
  ],
});

// 9. Транзакции
export const V09 = scene({
  labels: ["BEGIN", "COMMIT", "ROLLBACK"],
  caption: [
    "BEGIN начинает транзакцию: изменения пока видны только вам",
    "COMMIT фиксирует все изменения разом",
    "ROLLBACK возвращает данные к состоянию до BEGIN",
  ],
  frames: [
    [sql("c", 10, 20, ["BEGIN;", "UPDATE acc SET sum = sum - 100 WHERE id = 1;", "UPDATE acc SET sum = sum + 100 WHERE id = 2;"], [0], { ...code, size: 9.5 }), Tx("n", 180, 110, "изменения ещё не зафиксированы", { size: 9.5, c: "y" })],
    [sql("c", 10, 20, ["BEGIN;", "UPDATE acc SET sum = sum - 100 WHERE id = 1;", "UPDATE acc SET sum = sum + 100 WHERE id = 2;", "COMMIT;"], [3], { ...code, size: 9.5, lh: 13 }), Box("g", 180, 120, 200, 28, "оба изменения сохранены", "g", { size: 9.5 })],
    [sql("c", 10, 20, ["BEGIN;", "UPDATE acc SET sum = sum - 100 WHERE id = 1;", "-- сбой!", "ROLLBACK;"], [3], { ...code, size: 9.5, lh: 13 }), Box("g", 180, 120, 220, 28, "данные как до BEGIN", "y", { size: 9.5 })],
  ],
});

// 10. Ограничения
export const V10 = scene({
  labels: ["NOT NULL", "UNIQUE и ключ", "FOREIGN KEY"],
  caption: [
    "Пропустили обязательный столбец — команда не выполнится",
    "Повторное значение в уникальном столбце или ключе — ошибка",
    "Заказ несуществующего клиента вставить нельзя; PRAGMA foreign_keys = ON",
  ],
  frames: [
    [sql("c", 10, 20, ["INSERT INTO customers (id) VALUES (9);"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 280, 28, "NOT NULL constraint failed: customers.name", "r", { size: 9 })],
    [sql("c", 10, 20, ["INSERT INTO customers (id, name) VALUES (1, 'Я');"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 260, 28, "UNIQUE constraint failed: customers.id", "r", { size: 9.5 })],
    [sql("c", 10, 14, ["PRAGMA foreign_keys = ON;", "INSERT INTO orders (cust) VALUES (999);"], [0], { ...code, bad: [1] }), Box("e", 180, 100, 280, 28, "FOREIGN KEY constraint failed", "r", { size: 9.5 })],
  ],
});

// 11. UPSERT
export const V11 = scene({
  labels: ["Конфликт", "DO UPDATE", "Грубые способы"],
  caption: [
    "Строка с таким ключом уже есть — обычный INSERT выдаст ошибку",
    "ON CONFLICT … DO UPDATE обновляет её; excluded — те значения, что вставляли",
    "OR REPLACE удаляет и вставляет заново (теряет остальные столбцы), OR IGNORE молча пропускает",
  ],
  frames: [
    [sql("c", 10, 14, ["INSERT INTO stock (id, qty) VALUES (7, 5);"], undefined, { ...code, bad: [0] }), ...tbl("t", 120, 60, ["id", "qty"], [[7, 150]], [50, 60], { size: 9 }), Tx("n", 180, 110, "id = 7 уже есть", { size: 9.5, c: "r" })],
    [sql("c", 10, 14, ["INSERT INTO stock (id, qty) VALUES (7, 5)", "ON CONFLICT (id)", "DO UPDATE SET qty = qty + excluded.qty;"], [1, 2], { ...code, lh: 13 }), ...tbl("t", 130, 76, ["id", "qty"], [[7, 155]], [50, 60], { size: 9, hot: [0] })],
    [Box("a", 90, 70, 150, 40, "INSERT OR REPLACE\nудалил и вставил", "y", { size: 9.5 }), Box("b", 270, 70, 150, 40, "INSERT OR IGNORE\nмолча пропустил", "y", { size: 9.5 })],
  ],
});

// 12. RETURNING
export const V12 = scene({
  labels: ["INSERT", "UPDATE", "DELETE"],
  caption: [
    "INSERT … RETURNING id сразу возвращает номер новой строки",
    "UPDATE … RETURNING показывает новые значения затронутых строк",
    "DELETE … RETURNING отдаёт то, что было удалено — простой журнал",
  ],
  frames: [
    [sql("c", 10, 14, ["INSERT INTO customers (name) VALUES ('Глеб')", "RETURNING id;"], [1], code), ...tbl("r", 140, 70, ["id"], [[4]], [60], { size: 10, hot: [0] })],
    [sql("c", 10, 14, ["UPDATE products SET price = price * 1.1", "WHERE category = 'Книги' RETURNING title, price;"], [1], { ...code, size: 9 }), ...tbl("r", 90, 70, ["title", "price"], [["Книга SQL", 1320], ["Книга Python", 1485]], [100, 60], { size: 8.5, hot: [0, 1] })],
    [sql("c", 10, 14, ["DELETE FROM orders WHERE status = 'cancelled'", "RETURNING id;"], [1], code), ...tbl("r", 140, 70, ["id"], [[4], [15]], [60], { size: 10, hot: [0, 1] })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Правила", "Защита", "Дальше"],
  caption: [
    "Явные столбцы, WHERE у каждого UPDATE и DELETE, проверка SELECT-ом",
    "Транзакция, ограничения, UPSERT и RETURNING — страховка и удобство",
    "Следующая тема — структура таблиц: CREATE, ALTER, DROP",
  ],
  frames: [
    [Box("a", 65, 60, 110, 40, "явные\nстолбцы", "b", { size: 10 }), Box("b", 180, 60, 110, 40, "WHERE\nвсегда", "b", { size: 10 }), Box("c", 295, 60, 110, 40, "SELECT\nсначала", "b", { size: 10 })],
    [Box("a", 65, 60, 110, 40, "транзакция", "g", { size: 10 }), Box("b", 180, 60, 110, 40, "ограничения", "g", { size: 10 }), Box("c", 295, 60, 110, 40, "UPSERT\nRETURNING", "g", { size: 9.5 })],
    [sql("c", 20, 40, ["CREATE TABLE t (…);", "ALTER TABLE t …;", "DROP TABLE t;"], [0, 1, 2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
