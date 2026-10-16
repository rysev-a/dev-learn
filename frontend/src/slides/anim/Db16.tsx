import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, sql, tbl } from "./db.tsx";

/* Глава 16 книги «Базы данных»: представления (VIEW). */

type Row = readonly (string | number)[];
const code = { w: 340, size: 10, lh: 14 };
const GR = (head: string[], rows: Row[], x: number, y: number, widths: number[], hot: number[] = []) =>
  tbl("g", x, y, head, rows, widths, { size: 8.5, hot });

// 1. Запрос с именем
export const V01 = scene({
  labels: ["Длинный запрос", "Имя", "Как таблица"],
  caption: [
    "Сложный запрос с несколькими соединениями приходится копировать в десятки мест",
    "Представление — сохранённый запрос под одним именем",
    "Обращаемся к имени, как к таблице; данных оно не хранит",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT c.name, SUM(o.total)", "FROM customers c JOIN orders o", "  ON o.cust = c.id", "WHERE o.status <> 'cancelled'", "GROUP BY c.id;"], undefined, { ...code, lh: 13 }), Tx("n", 290, 130, "…и так в\nкаждом отчёте", { size: 8.5, c: "y" })],
    [Box("v", 180, 70, 200, 40, "v_customer_totals", "g", { size: 11 }), Tx("n", 180, 120, "запрос сохранён под именем", { size: 9.5 })],
    [sql("c", 10, 30, ["SELECT * FROM v_customer_totals;"], [0], code), Tx("n", 180, 100, "как будто это таблица", { size: 10, c: "g" })],
  ],
});

// 2. CREATE VIEW
export const V02 = scene({
  labels: ["Создание", "Псевдонимы", "Удаление"],
  caption: [
    "CREATE VIEW имя AS SELECT … — любой запрос: JOIN, GROUP BY, функции",
    "Столбцы берут имена из SELECT; вычисляемым нужны псевдонимы",
    "DROP VIEW удаляет только определение; таблицы не затрагиваются",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE VIEW v_customer_totals AS", "SELECT c.id, c.name, SUM(o.total) AS spent", "FROM customers c JOIN orders o ON o.cust = c.id", "GROUP BY c.id;"], [0], { ...code, lh: 13, size: 9.5 })],
    [sql("c", 10, 14, ["CREATE VIEW v_totals (cust, name, spent) AS", "SELECT c.id, c.name, SUM(o.total)", "FROM … ;"], [0], { ...code, lh: 14, size: 9.5 }), Tx("n", 180, 100, "имена столбцов — в скобках", { size: 9.5 })],
    [sql("c", 10, 20, ["DROP VIEW v_customer_totals;"], [0], code), Tx("n", 180, 100, "таблицы и данные целы", { size: 10, c: "g" })],
  ],
});

// 3. Запросы к VIEW
export const V03 = scene({
  labels: ["SELECT", "WHERE и ORDER", "JOIN"],
  caption: [
    "SELECT из представления — как из таблицы",
    "Фильтр, сортировка, LIMIT работают обычным образом",
    "Представление можно соединять с таблицами и другими представлениями",
  ],
  frames: [
    [sql("c", 10, 14, ["SELECT name, spent FROM v_customer_totals;"], [0], code), ...GR(["name", "spent"], [["Анна", 84700], ["Борис", 59300]], 110, 56, [70, 80], [0, 1])],
    [sql("c", 10, 14, ["SELECT name FROM v_customer_totals", "WHERE spent > 60000 ORDER BY spent DESC;"], [1], code), ...GR(["name"], [["Анна"]], 130, 66, [90], [0])],
    [sql("c", 10, 14, ["SELECT v.name, p.title", "FROM v_customer_totals v JOIN purchases p ON …"], [1], code), Tx("n", 180, 100, "представления и таблицы — в одном JOIN", { size: 9.5 })],
  ],
});

// 4. Зачем
export const V04 = scene({
  labels: ["Одно определение", "Правим один раз", "Стабильный интерфейс"],
  caption: [
    "«Активный клиент» и «выручка» определяет одно представление — отчёты согласованы",
    "Правило изменилось — правим одно место, а не двадцать запросов",
    "Приложение читает из представления; структура таблиц может эволюционировать",
  ],
  frames: [
    [Box("v", 180, 40, 160, 28, "v_active_customers", "g", { size: 9.5 }), Box("a", 70, 110, 100, 26, "отчёт 1", "b", { size: 9.5 }), Box("b", 180, 110, 100, 26, "отчёт 2", "b", { size: 9.5 }), Box("c", 290, 110, 100, 26, "отчёт 3", "b", { size: 9.5 }), arrow("e1", 150, 54, 90, 98, "g"), arrow("e2", 180, 54, 180, 98, "g"), arrow("e3", 210, 54, 270, 98, "g")],
    [Box("a", 90, 70, 150, 40, "20 копий запроса:\nправить везде", "r", { size: 9.5 }), Box("b", 270, 70, 150, 40, "одно представление:\nправим раз", "g", { size: 9.5 })],
    [Box("a", 70, 70, 100, 34, "приложение", "b", { size: 10 }), Box("v", 180, 70, 80, 34, "VIEW", "g", { size: 11 }), Box("t", 295, 70, 100, 34, "таблицы\n(меняются)", "y", { size: 9 }), arrow("e1", 122, 70, 138, 70, "m"), arrow("e2", 222, 70, 238, 70, "m")],
  ],
});

// 5. Скрытие данных
export const V05 = scene({
  labels: ["Лишние столбцы", "Лишние строки", "Права"],
  caption: [
    "Представление выбирает только нужные столбцы: пароль и заметки не видны",
    "Условие в WHERE оставляет только свои данные или только активные записи",
    "В серьёзных СУБД доступ дают к представлению, а не к таблице (в SQLite прав нет)",
  ],
  frames: [
    [...tbl("t", 20, 50, ["id", "name", "pass"], [[1, "Анна", "•••"], [2, "Борис", "•••"]], [30, 60, 50], { size: 8.5, dim: [] }), arrow("a", 170, 80, 200, 80, "g"), ...tbl("v", 220, 50, ["id", "name"], [[1, "Анна"], [2, "Борис"]], [30, 60], { size: 8.5, hot: [0, 1] })],
    [sql("c", 10, 14, ["CREATE VIEW v_active AS", "SELECT * FROM users WHERE active = 1;"], [1], code), Tx("n", 180, 100, "неактивные строки не видны", { size: 10 })],
    [Box("u", 70, 70, 100, 30, "пользователь", "b", { size: 9.5 }), arrow("e", 122, 70, 138, 70, "g"), Box("v", 180, 70, 80, 30, "VIEW", "g", { size: 10 }), Box("t", 295, 70, 100, 30, "таблица ✗", "r", { size: 9.5 })],
  ],
});

// 6. Всегда свежее
export const V06 = scene({
  labels: ["Новый заказ", "Сразу виден", "Тяжёлый запрос"],
  caption: [
    "Добавили заказ в таблицу orders",
    "Представление итогов пересчитывается при обращении — новый заказ уже учтён",
    "Если внутри тяжёлый запрос, он выполняется при каждом обращении",
  ],
  frames: [
    [sql("c", 10, 20, ["INSERT INTO orders (cust, total) VALUES (3, 1000);"], [0], code), ...GR(["cust", "total"], [[1, 84700], [3, 1000]], 130, 70, [50, 70], [1])],
    [...GR(["name", "spent"], [["Анна", 84700], ["Вера", 1000]], 110, 56, [70, 80], [1]), Tx("n", 180, 140, "Вера появилась сразу", { size: 9.5, c: "g" })],
    [Box("a", 90, 70, 150, 40, "VIEW: считается\nпри каждом SELECT", "y", { size: 9.5 }), Box("b", 270, 70, 150, 40, "таблица-снимок:\nобновляем по расписанию", "g", { size: 9 })],
  ],
});

// 7. VIEW поверх VIEW
export const V07 = scene({
  labels: ["Слой 1", "Слой 2", "Слой 3"],
  caption: [
    "v_orders_full: заказы вместе с клиентами",
    "v_month_totals строится поверх первого: итоги по месяцам",
    "v_top_months берёт лучшие месяцы: понятная цепочка из простых шагов",
  ],
  frames: [
    [Box("t", 180, 40, 120, 26, "таблицы", "b", { size: 10 }), Box("v1", 180, 100, 180, 30, "v_orders_full", "g", { size: 10 }), arrow("a", 180, 54, 180, 88, "g")],
    [Box("t", 180, 30, 120, 22, "таблицы", "b", { size: 9.5 }), Box("v1", 180, 75, 180, 26, "v_orders_full", "g", { size: 10 }), Box("v2", 180, 120, 180, 26, "v_month_totals", "g", { size: 10 }), arrow("a1", 180, 41, 180, 62, "m"), arrow("a2", 180, 88, 180, 107, "g")],
    [Box("t", 180, 20, 120, 20, "таблицы", "b", { size: 9 }), Box("v1", 180, 55, 180, 24, "v_orders_full", "b", { size: 9.5 }), Box("v2", 180, 95, 180, 24, "v_month_totals", "b", { size: 9.5 }), Box("v3", 180, 135, 180, 24, "v_top_months", "g", { size: 9.5 }), arrow("a1", 180, 30, 180, 43, "m"), arrow("a2", 180, 67, 180, 83, "m"), arrow("a3", 180, 107, 180, 123, "g")],
  ],
});

// 8. Менять и удалять
export const V08 = scene({
  labels: ["Нет OR REPLACE", "В транзакции", "Файл миграции"],
  caption: [
    "ALTER VIEW и CREATE OR REPLACE в SQLite нет",
    "Удаляем и создаём заново — в одной транзакции, чтобы никто не заметил паузы",
    "Определение храните в файле миграции — оттуда его проще править",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE OR REPLACE VIEW v AS …;", "ALTER VIEW v …;"], undefined, { ...code, bad: [0, 1] }), Box("e", 180, 110, 240, 26, "в SQLite не поддерживается", "r", { size: 9.5 })],
    [sql("c", 10, 14, ["BEGIN;", "DROP VIEW IF EXISTS v;", "CREATE VIEW v AS SELECT …;", "COMMIT;"], [1, 2], { ...code, lh: 13 })],
    [Box("f", 70, 70, 120, 30, "views/v.sql", "g", { size: 10 }), arrow("e", 130, 70, 170, 70, "m"), Box("db", 260, 70, 140, 30, "база данных", "b", { size: 10 })],
  ],
});

// 9. Запись через VIEW
export const V09 = scene({
  labels: ["Только чтение", "INSTEAD OF", "Другие СУБД"],
  caption: [
    "INSERT и UPDATE в представление в SQLite завершаются ошибкой",
    "Триггер INSTEAD OF перехватывает операцию и выполняет команды над таблицами",
    "Простые представления на одной таблице в других СУБД обновляются автоматически",
  ],
  frames: [
    [sql("c", 10, 14, ["INSERT INTO v_customer_totals VALUES (…);"], undefined, { ...code, bad: [0] }), Box("e", 180, 100, 260, 26, "cannot modify v — it is a view", "r", { size: 9.5 })],
    [sql("c", 10, 14, ["CREATE TRIGGER v_ins INSTEAD OF INSERT", "ON v BEGIN", "  INSERT INTO customers (name) VALUES (NEW.name);", "END;"], [0, 2], { ...code, lh: 13, size: 9 })],
    [Box("a", 90, 70, 150, 40, "простое представление:\nавтообновление", "g", { size: 9 }), Box("b", 270, 70, 150, 40, "JOIN и GROUP BY:\nневозможно", "r", { size: 9 })],
  ],
});

// 10. Скорость
export const V10 = scene({
  labels: ["Встраивание", "Условие внутрь", "Агрегаты"],
  caption: [
    "Запрос к представлению разворачивается в запрос к таблицам — индексы работают",
    "Условие из внешнего запроса обычно проталкивается внутрь и уменьшает работу",
    "Если внутри GROUP BY или окна, условие проталкивается не всегда — смотрите план",
  ],
  frames: [
    [Box("a", 70, 70, 100, 34, "SELECT …\nFROM v", "b", { size: 9.5 }), arrow("e", 122, 70, 138, 70, "g"), Box("b", 250, 70, 160, 34, "запрос к таблицам\nс их индексами", "g", { size: 9 })],
    [sql("c", 10, 14, ["SELECT * FROM v_orders WHERE cust = 5;"], [0], code), Box("g", 180, 100, 280, 26, "→ WHERE cust = 5 внутри плана", "g", { size: 9.5 })],
    [sql("c", 10, 14, ["EXPLAIN QUERY PLAN", "SELECT * FROM v_totals WHERE cust = 5;"], [0], code), Tx("n", 180, 100, "проверяйте план запроса к VIEW", { size: 10, c: "y" })],
  ],
});

// 11. Ограничения
export const V11 = scene({
  labels: ["Звёздочка", "Сломанная ссылка", "ORDER BY внутри"],
  caption: [
    "SELECT * раскрывается при создании: новый столбец таблицы в представлении не появится",
    "Переименовали или удалили столбец — обращение к VIEW даёт ошибку",
    "ORDER BY внутри представления обычно бессмысленен: порядок задаёт вызывающий",
  ],
  frames: [
    [sql("c", 10, 14, ["CREATE VIEW v AS SELECT * FROM t;", "ALTER TABLE t ADD COLUMN extra …;"], [0], { ...code, size: 9.5 }), Box("e", 180, 100, 250, 26, "extra в v не появится", "y", { size: 9.5 })],
    [sql("c", 10, 14, ["ALTER TABLE t DROP COLUMN old;", "SELECT * FROM v;"], undefined, { ...code, bad: [1] }), Box("e", 180, 100, 250, 26, "no such column: old", "r", { size: 9.5 })],
    [sql("c", 10, 20, ["CREATE VIEW v AS SELECT … ORDER BY name;"], undefined, { ...code, bad: [0], size: 9.5 }), Tx("n", 180, 100, "пишите ORDER BY в запросе к VIEW", { size: 10, c: "y" })],
  ],
});

// 12. Практика
export const V12 = scene({
  labels: ["Имена", "Явные столбцы", "Не злоупотреблять"],
  caption: [
    "Префикс v_ и смысловое имя: v_active_customers, v_revenue_by_month",
    "Столбцы перечисляем явно и даём понятные псевдонимы",
    "Если запрос нужен один раз — хватит CTE, представление не нужно",
  ],
  frames: [
    [Box("a", 90, 60, 150, 28, "v_active_customers", "g", { size: 9.5 }), Box("b", 270, 60, 150, 28, "v_revenue_by_month", "g", { size: 9.5 }), Tx("n", 180, 110, "по имени видно, что это не таблица", { size: 9.5 })],
    [sql("c", 10, 14, ["CREATE VIEW v_orders AS", "SELECT o.id, o.created, c.name AS customer,", "       o.total", "FROM orders o JOIN customers c ON c.id = o.cust;"], [1, 2], { ...code, lh: 13, size: 9.5 })],
    [Box("a", 90, 70, 150, 36, "одноразово:\nWITH (CTE)", "b", { size: 10 }), Box("b", 270, 70, 150, 36, "многократно:\nVIEW", "g", { size: 10 })],
  ],
});

// 13. Итоги раздела
export const V13 = scene({
  labels: ["Запросы", "Данные и структура", "Дальше"],
  caption: [
    "SELECT, WHERE, ORDER BY, GROUP BY, JOIN, подзапросы, CTE, окна",
    "INSERT, UPDATE, DELETE, транзакции, CREATE, ALTER, индексы, представления",
    "Дальше — как всё это устроено внутри: хранение, транзакции, оптимизатор",
  ],
  frames: [
    [Box("a", 65, 50, 110, 26, "SELECT WHERE", "g", { size: 9.5 }), Box("b", 180, 50, 110, 26, "GROUP BY HAVING", "g", { size: 8.5 }), Box("c", 295, 50, 110, 26, "JOIN", "g", { size: 10 }), Box("d", 122, 96, 110, 26, "подзапросы CTE", "g", { size: 9 }), Box("e", 238, 96, 110, 26, "окна", "g", { size: 10 })],
    [Box("a", 65, 50, 110, 26, "INSERT UPDATE", "b", { size: 9 }), Box("b", 180, 50, 110, 26, "транзакции", "b", { size: 10 }), Box("c", 295, 50, 110, 26, "CREATE ALTER", "b", { size: 9.5 }), Box("d", 122, 96, 110, 26, "индексы", "b", { size: 10 }), Box("e", 238, 96, 110, 26, "VIEW", "b", { size: 10 })],
    [Box("a", 180, 60, 240, 34, "Базы данных: под капотом", "g", { size: 12 }), arrow("e", 180, 100, 180, 124, "g"), Tx("n", 180, 140, "главы 17–32", { size: 9.5 })],
  ],
});
