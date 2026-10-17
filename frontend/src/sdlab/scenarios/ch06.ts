import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 6 «Консистентность, CAP и идемпотентность»: шторм повторов, ключи идемпотентности,
   синхронные реплики, повторная доставка из очереди. */

const chain = ["users>lb>app>db"];
const lb = () => N("lb", "lb", { instances: 2 });
const app = (extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: 3, sessions: "external", ...extra });

export const CH06: SdScenario[] = [
  {
    id: "sd06-retry-storm",
    title: "Шторм повторов",
    statement:
      "База S перегружена: чтений 1300 при пределе 1000. Приложение при ошибке повторяет запрос к базе до трёх раз без паузы, и нагрузка на базу растёт ещё сильнее — сервис не может подняться. Остановите шторм: включите автомат разрыва (circuit breaker) — когда база перегружена, он обрывает повторы, — чтобы доля успешных ответов была не ниже 72%.",
    hint: "У сервера приложения есть параметры «Повторы к БД» и «Автомат разрыва» (они показаны в этом упражнении). Включите автомат или обнулите повторы.",
    workload: WL({ read: 1300, write: 0, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app({ retries: 3 }), N("db", "db")], chain),
    goals: [
      { k: "success", min: 0.72 },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
    ],
    solution: S([users(), lb(), app({ retries: 3, breaker: true }), N("db", "db")], chain),
    show: ["app.retries", "app.breaker"],
  },
  {
    id: "sd06-idempotency",
    title: "Двойное списание",
    statement:
      "Платёжный сервис: клиенты повторяют запрос, если не получили ответ вовремя. Из-за этого иногда деньги списываются дважды. Включите ключи идемпотентности (параметр сервера), оставьте хотя бы один повтор — клиенты и сервер повторяют запросы — и включите автомат разрыва, чтобы повторы не усиливали перегрузку.",
    hint: "Параметры сервера приложения: «Ключи идемпотентности» — включить; «Повторы к БД» — не меньше 1; «Автомат разрыва» — включить.",
    workload: WL({ read: 200, write: 100, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app({ retries: 2 }), N("db", "db", { size: "M", replicas: 1, failover: true })], chain),
    goals: [
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "retries", op: ">=", value: 1 },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
    ],
    solution: S([users(), lb(), app({ retries: 2, idempotency: true, breaker: true }), N("db", "db", { size: "M", replicas: 1, failover: true })], chain),
    show: ["app.idempotency", "app.retries", "app.breaker"],
  },
  {
    id: "sd06-strong",
    title: "Строгая согласованность",
    statement:
      "Сервис балансов не вправе терять подтверждённую запись и показывать старый баланс. Соберите базу из трёх копий (лидер и две реплики) с синхронной репликацией и автопереключением: отставание реплик — ноль, схема переживает отказ базы, p99 не больше 160 мс.",
    hint: "База: «Реплики на шард» — 2, «Репликация» — синхронная, «Автопереключение» — включить. Синхронность добавляет несколько миллисекунд к записи.",
    workload: WL({ read: 300, write: 100, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "replicaLag", max: 0 },
      { k: "survive", fail: "db" },
      { k: "p99", max: 160 },
      { k: "param", kind: "db", key: "replicas", op: ">=", value: 2 },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "M", replicas: 2, failover: true, sync: "sync" })], chain),
    show: ["db.sync"],
  },
  {
    id: "sd06-eventual",
    title: "Согласованность в конечном счёте",
    statement:
      "Лента новостей допускает небольшое отставание: свежесть в несколько сотен миллисекунд никому не мешает, зато нужны быстрые чтения и дешёвая запись. Оставьте асинхронную репликацию с двумя репликами и убедитесь, что отставание не больше 200 мс, схема переживает отказ базы, а p99 не больше 100 мс.",
    hint: "Синхронные реплики здесь не нужны: они замедляют запись. Выберите «асинхронная».",
    workload: WL({ read: 900, write: 120, dataGB: 40 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M", replicas: 2, failover: true, sync: "sync" })], chain),
    goals: [
      { k: "param", kind: "db", key: "sync", op: "==", value: "async" },
      { k: "replicaLag", max: 200 },
      { k: "survive", fail: "db" },
      { k: "p99", max: 100 },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "M", replicas: 2, failover: true, sync: "async" })], chain),
    show: ["db.sync"],
  },
  {
    id: "sd06-redelivery",
    title: "Повторная доставка из очереди",
    statement:
      "Заказы принимаются через очередь, и обработчики разбирают её с доставкой «не менее одного раза»: одно сообщение иногда приходит дважды. Соберите схему «сервер → очередь → обработчики → база» с идемпотентными обработчиками, чтобы очередь разбиралась без отставания (после пика в 60 с), а обработчики были загружены не выше 90%.",
    hint: "Параметр «Идемпотентная обработка» у обработчика. Нагрузка записи 400 в секунду: три обработчика S тянут 450.",
    workload: WL({ read: 100, write: 400, dataGB: 10, spikeSec: 60 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "link", from: "queue", to: "worker" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.9 },
    ],
    solution: S(
      [users(), lb(), app(), N("queue", "queue"), N("worker", "worker", { instances: 3, idempotent: true }), N("db", "db", { size: "M" })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["worker.idempotent"],
  },
  {
    id: "sd06-final",
    title: "Платёжный контур",
    statement:
      "Итоговое упражнение главы. Платёжный сервис: надёжность важнее скорости. Нужны: ключи идемпотентности, автомат разрыва, база с синхронной репликой и автопереключением, пара балансировщиков, схема переживает отказ базы и сервера приложения, загрузка не выше 80%, бюджет $1500 в месяц.",
    hint: "Три сервера M (после потери одного 1400 запросов — хватает), база M с репликой, синхронная, с автопереключением, пара балансировщиков.",
    workload: WL({ read: 500, write: 150, dataGB: 30 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 2, sessions: "external" }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "replicaLag", max: 0 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "app" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "cost", max: 1500 },
    ],
    solution: S(
      [users(), lb(), app({ idempotency: true, breaker: true, retries: 1 }), N("db", "db", { size: "M", replicas: 1, failover: true, sync: "sync" })],
      chain,
    ),
    show: ["app.idempotency", "app.retries", "app.breaker", "db.sync"],
  },
];
