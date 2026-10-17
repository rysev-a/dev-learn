import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 12 «Лента новостей»: pull, push и гибрид, кэш лент, рассылка через очередь. */

const lb = () => N("lb", "lb", { instances: 2 });
const app = (n = 4, feed = "pull", extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", feed, ...extra });
const web = ["users>lb>app>db"];

export const CH12: SdScenario[] = [
  {
    id: "sd12-pull-fix",
    title: "Лента при чтении перегружает базу",
    statement:
      "Лента собирается при открытии (pull): у каждого автора в среднем 50 подписчиков, и при 2000 чтений в секунду база L перегружена лишними запросами. Полная рассылка при записи (push) тоже не подходит: 50 записей в секунду превращаются в 2500. Выберите режим ленты у сервера приложения так, чтобы база была загружена не выше 80%. Параметр «Лента» виден в упражнении.",
    hint: "Pull умножает чтения в 3,5 раза, push умножает записи в 50. Гибрид умножает и то и другое всего в 1,5 раза.",
    workload: WL({ read: 2000, write: 50, dataGB: 200, fanout: 50 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(4, "pull"), N("db", "db", { size: "L" })], web),
    goals: [
      { k: "util", kind: "db", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(4, "hybrid"), N("db", "db", { size: "L" })], web),
    show: ["app.feed"],
  },
  {
    id: "sd12-feed-cache",
    title: "Кэш для готовых лент",
    statement:
      "Читателей стало больше: 4000 открытий ленты в секунду, рабочий набор — 8 ГБ из 200. База M не вытягивает чтения. Оставьте гибридный режим ленты и поставьте кэш: кэш отдаёт не меньше 90%, база загружена не выше 80%, серверы — тоже. Бюджет — $1600 в месяц.",
    hint: "Кэш около 8 ГБ с TTL 3600 — около 94% попаданий, база увидит лишь 6% чтений. Серверов приложения хватит восьми M.",
    workload: WL({ read: 4000, write: 80, dataGB: 200, hotSet: 0.04, fanout: 50 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(8, "hybrid"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "hit", min: 0.9 },
      { k: "util", kind: "db", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1600 },
    ],
    solution: S([users(), lb(), app(8, "hybrid"), N("cache", "cache", { sizeGB: 8, ttl: 3600 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>cache"]),
    show: ["app.feed"],
  },
  {
    id: "sd12-push-queue",
    title: "Рассылка постов через очередь",
    statement:
      "У сервиса небольшие аудитории (10 подписчиков у автора), поэтому выбран push: каждый пост рассылается в ленты. При 400 постах в секунду это 4000 записей в ленты — всё сразу база не выдержит. Пропустите запись через очередь с обработчиками: база L загружена не выше 80%, очередь разбирается после 10-секундного пика не дольше 45 секунд. Режим ленты — push.",
    hint: "Обработчики определяют темп записи в базу: два обработчика M — 800 в секунду (53% базы L). Отставание: (4000 − 800) / 800 × 10 = 40 с.",
    workload: WL({ read: 500, write: 400, dataGB: 200, fanout: 10, spikeSec: 10 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S([users(), lb(), app(5, "push"), N("db", "db", { size: "L" })], web),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "app", key: "feed", op: "==", value: "push" },
      { k: "util", kind: "db", max: 0.8 },
      { k: "lag", max: 45 },
    ],
    solution: S(
      [users(), lb(), app(5, "push"), N("queue", "queue"), N("worker", "worker", { instances: 2, size: "M" }), N("db", "db", { size: "L" })],
      ["users>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["app.feed"],
  },
  {
    id: "sd12-celebrity",
    title: "Знаменитости",
    statement:
      "В сервисе есть авторы-знаменитости: средняя аудитория автора — 300 подписчиков. Полный push даст умножение записей в 300 раз, чистый pull — в 16 раз чтений. Выберите гибрид и поставьте кэш, чтобы база M была загружена не выше 80% при 3000 чтений и 40 записях в секунду.",
    hint: "Гибрид: чтения ×4, записи ×4. Кэш с хорошим попаданием сводит дополнительные чтения почти к нулю: 6 ГБ с TTL 3600.",
    workload: WL({ read: 3000, write: 40, dataGB: 150, hotSet: 0.04, fanout: 300 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(5, "pull"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "util", kind: "db", max: 0.8 },
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "hit", min: 0.9 },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), lb(), app(6, "hybrid"), N("cache", "cache", { sizeGB: 6, ttl: 3600 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>cache"]),
    show: ["app.feed"],
  },
  {
    id: "sd12-final",
    title: "Социальная сеть",
    statement:
      "Итоговое упражнение главы. Лента: 8000 открытий и 100 постов в секунду, 100 подписчиков у автора в среднем, 300 ГБ данных (рабочий набор 12 ГБ). Соберите схему: гибридная лента, кэш (≥90%), база с репликой и автопереключением (переживает отказ базы и кэша), серверы приложения с запасом на потерю одного, всё — не выше 80%, бюджет $3500 в месяц.",
    hint: "Кэш 12 ГБ с репликой и TTL 3600; серверов приложения — пятнадцать M (нагрузка 8100 запросов, запас на отказ одного); база M с репликой и автопереключением.",
    workload: WL({ read: 8000, write: 100, dataGB: 300, hotSet: 0.04, fanout: 100 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(6, "pull"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "hit", min: 0.9 },
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 3500 },
    ],
    solution: S(
      [users(), lb(), app(15, "hybrid"), N("cache", "cache", { sizeGB: 12, ttl: 3600, replicas: 1 }), N("db", "db", { size: "M", replicas: 1, failover: true })],
      ["users>lb>app>db", "app>cache"],
    ),
    show: ["app.feed"],
  },
];
