import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 8 «Очереди и обработчики»: сглаживание пика, обработчики и отставание, партиции, DLQ, спот-обработчики. */

const direct = ["users>lb>app>db"];
const lb = () => N("lb", "lb", { instances: 2 });
const app = (n = 5) => N("app", "app", { size: "M", instances: n, sessions: "external" });

export const CH08: SdScenario[] = [
  {
    id: "sd08-spike",
    title: "Сглаживание пика записи",
    statement:
      "В пик сервис получает 2000 записей в секунду, а база M выдерживает 600: без буфера она перегружена. Поставьте между сервером приложения и базой очередь с обработчиками. Обработчики должны разбирать очередь не быстрее, чем база способна писать: загрузка базы не выше 80%, а после пика в 5 секунд очередь разбирается не дольше чем за 30 секунд.",
    hint: "База принимает столько записей, сколько успевают провести обработчики: два обработчика S — 300 записей в секунду: база загружена на 67% (с учётом чтений). Отставание: (2000 − 300) / 300 × 5 ≈ 28 с.",
    workload: WL({ read: 500, write: 2000, dataGB: 60, spikeSec: 5 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], direct),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "util", kind: "db", max: 0.8 },
      { k: "lag", max: 30 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(), N("queue", "queue"), N("worker", "worker", { instances: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>queue>worker>db"]),
  },
  {
    id: "sd08-workers",
    title: "Сколько обработчиков",
    statement:
      "Очередь уже есть, но обработчиков слишком мало: после пика в 20 секунд очередь разбирается слишком долго. Поступает 1500 записей в секунду, база L принимает до 1500. Подберите обработчиков так, чтобы очередь разбиралась не дольше 20 секунд, а база при этом была загружена не больше чем на 80%.",
    hint: "Отставание = (приток − разбор) / разбор × длина пика. Для 20 секунд нужен разбор не меньше 750 в секунду, но и не больше 1200 (80% базы). Два обработчика M — 800.",
    workload: WL({ read: 500, write: 1500, dataGB: 60, spikeSec: 20 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(), N("queue", "queue"), N("worker", "worker", { instances: 2 }), N("db", "db", { size: "L" })], ["users>lb>app>db", "app>queue>worker>db"]),
    goals: [
      { k: "lag", max: 20 },
      { k: "util", kind: "db", max: 0.8 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(), N("queue", "queue"), N("worker", "worker", { instances: 2, size: "M" }), N("db", "db", { size: "L" })], ["users>lb>app>db", "app>queue>worker>db"]),
  },
  {
    id: "sd08-partitions",
    title: "Партиции очереди",
    statement:
      "Поток — 30 000 сообщений в секунду, а одна партиция пропускает 20 000. Подберите число партиций, чтобы очередь была загружена не выше 80% и переживала отказ узла брокера (для этого нужно не меньше трёх партиций).",
    hint: "Две партиции дают 40 000 — 75%, но для переживания отказа нужны три: 30 000 / 60 000 = 50%.",
    workload: WL({ read: 100, write: 30000, dataGB: 200, spikeSec: 5 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S(
      [users(), lb(), N("app", "app", { size: "L", instances: 25, sessions: "external" }), N("queue", "queue"), N("worker", "worker", { instances: 6, size: "M" }), N("db", "db", { size: "L", shards: 2 })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    goals: [
      { k: "util", kind: "queue", max: 0.8 },
      { k: "survive", fail: "queue" },
      { k: "param", kind: "queue", key: "partitions", op: ">=", value: 3 },
    ],
    solution: S(
      [users(), lb(), N("app", "app", { size: "L", instances: 25, sessions: "external" }), N("queue", "queue", { partitions: 3 }), N("worker", "worker", { instances: 6, size: "M" }), N("db", "db", { size: "L", shards: 2 })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
  },
  {
    id: "sd08-dlq",
    title: "Очередь недоставленных",
    statement:
      "Из-за одного «ядовитого» сообщения обработчик зацикливается и блокирует очередь. Включите очередь недоставленных (DLQ) и сделайте обработку идемпотентной, чтобы повторы были безопасны, а очередь разбиралась без отставания.",
    hint: "У очереди — параметр «Очередь недоставленных», у обработчика — «Идемпотентная обработка» (оба показаны в этом упражнении).",
    workload: WL({ read: 200, write: 300, dataGB: 20, spikeSec: 30 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(3), N("queue", "queue"), N("worker", "worker", { instances: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>queue>worker>db"]),
    goals: [
      { k: "param", kind: "queue", key: "dlq", op: "==", value: true },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "lag", max: 5 },
    ],
    solution: S(
      [users(), lb(), app(3), N("queue", "queue", { dlq: true }), N("worker", "worker", { instances: 3, idempotent: true }), N("db", "db", { size: "M" })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["queue.dlq", "worker.idempotent"],
  },
  {
    id: "sd08-spot",
    title: "Дешёвые обработчики",
    statement:
      "Ночная обработка заказов не срочна, и её можно запускать на прерываемых серверах (спот): они втрое дешевле, но могут исчезнуть. Переведите обработчиков на спот, оставьте не меньше двух (чтобы потеря одного не останавливала очередь) и уложитесь в $850 всей схемой — очередь при этом должна разбираться без отставания.",
    hint: "Параметр «Тариф» обработчика (виден в упражнении): спот стоит 30% от обычной цены. Нужно не меньше двух экземпляров — иначе точка отказа.",
    workload: WL({ read: 100, write: 500, dataGB: 30, spikeSec: 30 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(3), N("queue", "queue"), N("worker", "worker", { instances: 4, size: "M" }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>queue>worker>db"]),
    goals: [
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "noSpof", kinds: ["worker"] },
      { k: "lag", max: 5 },
      { k: "cost", max: 850 },
    ],
    solution: S(
      [users(), lb(), app(3), N("queue", "queue"), N("worker", "worker", { instances: 2, size: "M", pricing: "spot" }), N("db", "db", { size: "M" })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["worker.pricing"],
  },
  {
    id: "sd08-final",
    title: "Конвейер обработки",
    statement:
      "Итоговое упражнение главы. Сервис заказов: 600 чтений и 900 записей в секунду, после пика в 15 секунд очередь должна разбираться не дольше 30 секунд. Соберите схему: очередь с очередью недоставленных, идемпотентные обработчики (не меньше двух), база не выше 80%, схема переживает отказ обработчика, бюджет — $1700 в месяц.",
    hint: "База L принимает 1500 записей. Два обработчика M — 800 в секунду: 53% базы, отставание (900 − 800)/800 × 15 ≈ 2 с. Включите DLQ и идемпотентность.",
    workload: WL({ read: 600, write: 900, dataGB: 100, spikeSec: 15 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], direct),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "queue", key: "dlq", op: "==", value: true },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "noSpof", kinds: ["worker"] },
      { k: "lag", max: 30 },
      { k: "util", kind: "db", max: 0.8 },
      { k: "cost", max: 1700 },
    ],
    solution: S(
      [users(), lb(), app(), N("queue", "queue", { dlq: true }), N("worker", "worker", { instances: 2, size: "M", idempotent: true }), N("db", "db", { size: "L" })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["queue.dlq", "worker.idempotent"],
  },
];
