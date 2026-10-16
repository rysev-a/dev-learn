import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 9 книги «Базы данных»: создание и изменение структуры таблиц (DDL). */

const code = { w: 340, size: 10, lh: 14 };
const COLS = [
  ["id", "INTEGER", "PRIMARY KEY"],
  ["name", "TEXT", "NOT NULL"],
  ["city", "TEXT", ""],
  ["vip", "INTEGER", "DEFAULT 0"],
] as const;
const CW = [50, 70, 100];

// 1. Структура данных
export const V01 = scene({
  labels: ["Три команды", "Скелет", "Что даёт схема"],
  caption: [
    "CREATE создаёт таблицу, ALTER меняет её устройство, DROP удаляет",
    "Структура — скелет приложения: от неё зависит, какие данные можно сохранить",
    "Хорошая схема избавляет от сотен проверок в коде приложения",
  ],
  frames: [
    [Box("c", 65, 70, 100, 40, "CREATE\nсоздать", "g", { size: 10 }), Box("a", 180, 70, 100, 40, "ALTER\nизменить", "y", { size: 10 }), Box("d", 295, 70, 100, 40, "DROP\nудалить", "r", { size: 10 })],
    [Box("s", 180, 70, 160, 50, "структура\nтаблиц", "b", { size: 12 }), arrow("a", 180, 100, 180, 120, "m")],
    [Box("a", 90, 70, 150, 40, "правила в схеме:\nне обойти", "g", { size: 9.5 }), Box("b", 270, 70, 150, 40, "правила в коде:\nлегко забыть", "y", { size: 9.5 })],
  ],
});

// 2. CREATE TABLE
export const V02 = scene({
  labels: ["Команда", "Столбцы", "Имена"],
  caption: [
    "CREATE TABLE имя (описания столбцов через запятую)",
    "У каждого столбца — имя, тип и при необходимости ограничения",
    "Имена: строчные, без пробелов; таблица — существительное во множественном числе",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE TABLE customers (", "  id INTEGER PRIMARY KEY,", "  name TEXT NOT NULL,", "  city TEXT", ");"], [0, 4], { ...code, lh: 13 })],
    [...tbl("t", 40, 40, ["столбец", "тип", "ограничения"], COLS, CW, { size: 8.5, hot: [0, 1, 2, 3] })],
    [Box("a", 90, 60, 150, 30, "customers ✓", "g", { size: 10 }), Box("b", 270, 60, 150, 30, "Клиенты Магазина ✗", "r", { size: 9.5 }), Tx("n", 180, 110, "то, что пишем в запросах каждый день", { size: 9.5 })],
  ],
});

// 3. Типы
export const V03 = scene({
  labels: ["Пять сродств", "Даты", "Цена"],
  caption: [
    "INTEGER, REAL, TEXT, BLOB, NUMERIC — предпочтения для значений столбца",
    "Отдельного типа даты нет: текст ISO, число или секунды",
    "Цену удобно хранить целым числом копеек — без ошибок округления",
  ],
  frames: [
    [
      Box("a", 70, 50, 100, 28, "INTEGER", "b", { size: 10 }),
      Box("b", 180, 50, 100, 28, "REAL", "b", { size: 10 }),
      Box("c", 290, 50, 100, 28, "TEXT", "b", { size: 10 }),
      Box("d", 125, 100, 100, 28, "BLOB", "b", { size: 10 }),
      Box("e", 235, 100, 100, 28, "NUMERIC", "b", { size: 10 }),
    ],
    [Box("a", 90, 70, 150, 40, "'2024-05-07'\nтекст ISO", "g", { size: 10 }), Box("b", 270, 70, 150, 40, "1715040000\nсекунды", "b", { size: 10 })],
    [Tx("a", 90, 70, "0.1 + 0.2 = 0.30000000000000004", { size: 9, anchor: "start" }), Box("b", 180, 110, 240, 30, "15000 копеек вместо 150.00", "g", { size: 10 })],
  ],
});

// 4. Первичный ключ
export const V04 = scene({
  labels: ["Не повторяется", "Автонумерация", "AUTOINCREMENT"],
  caption: [
    "Первичный ключ различает строки: не повторяется и не бывает пустым",
    "INTEGER PRIMARY KEY нумеруется сам: вставили без значения — получили следующий",
    "AUTOINCREMENT не позволяет повторно использовать удалённые номера; нужен редко",
  ],
  frames: [
    [...tbl("t", 100, 40, ["id", "name"], [[1, "Анна"], [2, "Борис"], [2, "Вера"]], [40, 80], { size: 9, hot: [], dim: [] }), Box("e", 180, 130, 250, 24, "второй id = 2 → UNIQUE constraint failed", "r", { size: 8.5 })],
    [sql("c", 10, 14, ["INSERT INTO t (name) VALUES ('Вера');"], [0], code), ...tbl("t", 100, 56, ["id", "name"], [[1, "Анна"], [2, "Борис"], [3, "Вера"]], [40, 80], { size: 9, hot: [2] })],
    [sql("c", 10, 14, ["id INTEGER PRIMARY KEY AUTOINCREMENT"], [0], { ...code, size: 9.5 }), Tx("n", 180, 80, "удалили 3 → следующий будет 4, не 3", { size: 9.5 })],
  ],
});

// 5. NOT NULL и DEFAULT
export const V05 = scene({
  labels: ["NOT NULL", "DEFAULT", "Вместе"],
  caption: [
    "NOT NULL: вставка без значения отклоняется",
    "DEFAULT: пропущенный столбец получает заданное значение",
    "Вместе они закрывают почти все пропуски в обязательных столбцах",
  ],
  frames: [
    [sql("c", 10, 14, ["name TEXT NOT NULL"], [0], code), Box("e", 180, 80, 280, 28, "INSERT без name → NOT NULL constraint failed", "r", { size: 9 })],
    [sql("c", 10, 14, ["status TEXT DEFAULT 'new'", "vip INTEGER DEFAULT 0"], [0, 1], code), ...tbl("t", 100, 76, ["id", "status", "vip"], [[7, "new", 0]], [40, 60, 40], { size: 9, hot: [0] })],
    [sql("c", 10, 14, ["status TEXT NOT NULL DEFAULT 'new'"], [0], { ...code, size: 9.5 }), Tx("n", 180, 80, "обязателен — и заполняется сам", { size: 10, c: "g" })],
  ],
});

// 6. UNIQUE и CHECK
export const V06 = scene({
  labels: ["UNIQUE", "CHECK", "Правила в схеме"],
  caption: [
    "UNIQUE: значения не повторяются (пример — электронная почта); NULL допустим",
    "CHECK: условие на каждую строку — цена не отрицательна, рейтинг от 1 до 5",
    "Правила в самой таблице не обойти из приложения",
  ],
  frames: [
    [sql("c", 10, 14, ["email TEXT UNIQUE"], [0], code), ...tbl("t", 100, 56, ["email"], [["a@x.ru"], ["b@x.ru"], ["a@x.ru"]], [120], { size: 9 }), Tx("n", 180, 140, "третья строка отвергнута", { size: 9, c: "r" })],
    [sql("c", 10, 14, ["price INTEGER CHECK (price >= 0)", "rating INTEGER CHECK (rating BETWEEN 1 AND 5)"], [0, 1], { ...code, size: 9.5 }), Box("e", 180, 90, 280, 28, "цена −5 → CHECK constraint failed", "r", { size: 9.5 })],
    [Box("a", 90, 70, 150, 36, "правило в таблице:\nодин раз для всех", "g", { size: 9.5 }), Box("b", 270, 70, 150, 36, "в каждом приложении:\nлегко пропустить", "y", { size: 9.5 })],
  ],
});

// 7. FOREIGN KEY
export const V07 = scene({
  labels: ["Ссылка", "ON DELETE", "PRAGMA"],
  caption: [
    "Столбец заказа ссылается на первичный ключ клиента; база проверяет, что он существует",
    "CASCADE удаляет зависимые строки, SET NULL обнуляет ссылку, RESTRICT запрещает",
    "В SQLite проверка выключена по умолчанию: PRAGMA foreign_keys = ON",
  ],
  frames: [
    [
      sql("c", 10, 14, ["customer_id INTEGER NOT NULL", "  REFERENCES customers(id)"], [1], code),
      Box("c", 90, 110, 100, 30, "customers.id", "b", { size: 9.5 }),
      Box("o", 270, 110, 120, 30, "orders.customer_id", "b", { size: 9 }),
      arrow("a", 210, 110, 145, 110, "g"),
    ],
    [
      Box("a", 70, 70, 110, 36, "CASCADE\nудалить зависимые", "g", { size: 8.5 }),
      Box("b", 190, 70, 110, 36, "SET NULL\nобнулить ссылку", "y", { size: 8.5 }),
      Box("c", 305, 70, 100, 36, "RESTRICT\nзапретить", "r", { size: 8.5 }),
    ],
    [sql("c", 10, 20, ["PRAGMA foreign_keys = ON;"], [0], code), Tx("n", 180, 80, "включайте в каждом соединении", { size: 10, c: "y" })],
  ],
});

// 8. Составной ключ
export const V08 = scene({
  labels: ["Пара столбцов", "Уникальна пара", "Таблица связи"],
  caption: [
    "В позициях заказа строку определяет пара: номер заказа и номер товара",
    "Каждое значение по отдельности может повторяться, пара — нет",
    "Типично для связи «многие ко многим»: студенты и курсы, теги и записи",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE TABLE order_items (", "  order_id INTEGER, product_id INTEGER,", "  qty INTEGER,", "  PRIMARY KEY (order_id, product_id));"], [3], { ...code, lh: 13, size: 9.5 })],
    [...tbl("t", 90, 50, ["order", "product"], [[1, 5], [1, 7], [2, 5], [1, 5]], [60, 60], { size: 9, hot: [0, 1, 2] }), Tx("n", 180, 150, "(1, 5) повторилась — отвергнута", { size: 9, c: "r" })],
    [Box("a", 70, 70, 100, 30, "студенты", "b", { size: 10 }), Box("m", 180, 70, 80, 30, "записи", "g", { size: 10 }), Box("c", 290, 70, 100, 30, "курсы", "b", { size: 10 }), arrow("e1", 120, 70, 140, 70, "m"), arrow("e2", 220, 70, 240, 70, "m")],
  ],
});

// 9. ALTER TABLE
export const V09 = scene({
  labels: ["ADD COLUMN", "RENAME", "DROP COLUMN"],
  caption: [
    "ADD COLUMN добавляет столбец; существующие строки получают DEFAULT или NULL",
    "RENAME TO переименовывает таблицу, RENAME COLUMN — столбец",
    "DROP COLUMN убирает столбец; если он в ключе или индексе, пересоздают таблицу",
  ],
  frames: [
    [sql("c", 10, 14, ["ALTER TABLE customers", "  ADD COLUMN phone TEXT;"], [1], code), ...tbl("t", 70, 66, ["id", "name", "phone"], [[1, "Анна", "NULL"], [2, "Борис", "NULL"]], [30, 70, 70], { size: 8.5, hot: [0, 1] })],
    [sql("c", 10, 14, ["ALTER TABLE customers", "  RENAME COLUMN phone TO mobile;"], [1], code), ...tbl("t", 70, 66, ["id", "name", "mobile"], [[1, "Анна", "NULL"], [2, "Борис", "NULL"]], [30, 70, 70], { size: 8.5 })],
    [sql("c", 10, 14, ["ALTER TABLE customers", "  DROP COLUMN mobile;"], [1], code), ...tbl("t", 90, 66, ["id", "name"], [[1, "Анна"], [2, "Борис"]], [30, 70], { size: 8.5 })],
  ],
});

// 10. DROP и IF EXISTS
export const V10 = scene({
  labels: ["DROP TABLE", "IF EXISTS", "IF NOT EXISTS"],
  caption: [
    "DROP TABLE удаляет таблицу вместе с данными; без транзакции не откатить",
    "С IF EXISTS отсутствующая таблица — не ошибка",
    "CREATE TABLE IF NOT EXISTS не создаст таблицу повторно",
  ],
  frames: [
    [sql("c", 10, 20, ["DROP TABLE archive;"], [0], code), Box("e", 180, 100, 240, 30, "таблица и данные исчезли", "r", { size: 10 })],
    [sql("c", 10, 20, ["DROP TABLE IF EXISTS archive;"], [0], code), Box("g", 180, 100, 240, 30, "нет таблицы — нет ошибки", "g", { size: 10 })],
    [sql("c", 10, 20, ["CREATE TABLE IF NOT EXISTS t (…);"], [0], code), Box("g", 180, 100, 280, 30, "скрипт безопасно запускать снова", "g", { size: 10 })],
  ],
});

// 11. CREATE TABLE AS
export const V11 = scene({
  labels: ["Из запроса", "Без ограничений", "Временная"],
  caption: [
    "CREATE TABLE … AS SELECT копирует результат запроса в новую таблицу",
    "Ключи и ограничения не переносятся — их добавляют отдельно",
    "Временная таблица живёт, пока открыто соединение",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE TABLE top_orders AS", "SELECT * FROM orders", "WHERE total > 50000;"], [0, 1, 2], { ...code, lh: 13 }), ...tbl("t", 100, 72, ["id", "total"], [[1, 79500], [3, 55400]], [40, 70], { size: 8.5, hot: [0, 1] })],
    [Box("a", 90, 70, 150, 40, "данные\nскопированы", "g", { size: 10 }), Box("b", 270, 70, 150, 40, "PRIMARY KEY, NOT NULL\nне перенеслись", "y", { size: 9 })],
    [sql("c", 10, 20, ["CREATE TEMP TABLE work AS", "SELECT …;"], [0], code), Tx("n", 180, 100, "исчезнет при закрытии соединения", { size: 10 })],
  ],
});

// 12. Миграции
export const V12 = scene({
  labels: ["Файлы изменений", "По порядку", "sqlite_master"],
  caption: [
    "Каждое изменение структуры — отдельный пронумерованный файл",
    "Применяются по порядку на всех серверах; базу можно собрать с нуля",
    "Текущую схему видно в служебной таблице sqlite_master",
  ],
  frames: [
    [Box("a", 70, 40, 120, 24, "001_create.sql", "b", { size: 9 }), Box("b", 70, 76, 120, 24, "002_add_phone.sql", "b", { size: 9 }), Box("c", 70, 112, 120, 24, "003_index.sql", "b", { size: 9 })],
    [Box("a", 70, 70, 100, 30, "001", "g", { size: 10 }), arrow("e1", 122, 70, 148, 70, "m"), Box("b", 180, 70, 100, 30, "002", "g", { size: 10 }), arrow("e2", 232, 70, 258, 70, "m"), Box("c", 290, 70, 90, 30, "003", "g", { size: 10 })],
    [sql("c", 10, 14, ["SELECT name, type FROM sqlite_master;"], [0], code), ...tbl("t", 70, 56, ["name", "type"], [["customers", "table"], ["orders", "table"], ["idx_orders_cust", "index"]], [120, 70], { size: 8.5, hot: [0, 1, 2] })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Описание", "Команды", "Дальше"],
  caption: [
    "Типы, ключи, NOT NULL, DEFAULT, UNIQUE, CHECK и внешний ключ — защита данных в схеме",
    "CREATE, ALTER, DROP; IF EXISTS — для повторных запусков; миграции — для порядка",
    "Следующая тема — условная логика в запросах: CASE WHEN",
  ],
  frames: [
    [
      Box("a", 65, 50, 110, 26, "PRIMARY KEY", "b", { size: 9 }),
      Box("b", 180, 50, 110, 26, "NOT NULL DEFAULT", "b", { size: 8.5 }),
      Box("c", 295, 50, 110, 26, "UNIQUE CHECK", "b", { size: 9 }),
      Box("d", 180, 96, 140, 26, "FOREIGN KEY", "g", { size: 9.5 }),
    ],
    [Box("a", 65, 60, 110, 30, "CREATE", "g", { size: 10 }), Box("b", 180, 60, 110, 30, "ALTER", "y", { size: 10 }), Box("c", 295, 60, 110, 30, "DROP", "r", { size: 10 })],
    [sql("c", 20, 40, ["CASE", "  WHEN … THEN …", "  ELSE … END"], [0, 1, 2], { ...code, size: 11, lh: 17 }), arrow("a", 180, 120, 180, 132, "g")],
  ],
});
