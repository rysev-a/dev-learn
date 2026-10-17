import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 13 «Типовые задачи»: сокращатель ссылок, счётчики, общий ограничитель, хранение блоков, итоговая система. */

const lb = () => N("lb", "lb", { instances: 2 });
const app = (n: number, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", ...extra });
const web = ["users>lb>app>db"];

export const CH13: SdScenario[] = [
  {
    id: "sd13-shortener",
    title: "Сокращатель ссылок",
    statement:
      "Сокращатель: 4000 переходов и 40 созданий ссылок в секунду, 500 ГБ данных, рабочий набор около 5 ГБ. База S не тянет такие чтения. Поставьте кэш (≥90% попаданий) с репликой, чтобы схема переживала отказ кэша, и уложитесь в $1400 в месяц. Загрузка — не выше 80%.",
    hint: "Кэш 5 ГБ с TTL 3600 даёт около 93%; с репликой переживёт отказ. Серверов приложения — восемь M, база S хватит (чтения почти все из кэша).",
    workload: WL({ read: 4000, write: 40, dataGB: 500, hotSet: 0.01 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(8), N("db", "db")], web),
    goals: [
      { k: "hit", min: 0.9 },
      { k: "survive", fail: "cache" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1400 },
    ],
    solution: S([users(), lb(), app(8), N("cache", "cache", { sizeGB: 5, ttl: 3600, replicas: 1 }), N("db", "db")], ["users>lb>app>db", "app>cache"]),
  },
  {
    id: "sd13-counter",
    title: "Счётчик просмотров",
    statement:
      "Счётчики просмотров — 3000 обновлений в секунду плюс 500 чтений. Каждое обновление пишет в базу, и она перегружена: база M тянет 600 записей. Допустима потеря нескольких секунд счётчиков. Включите отложенную запись кэша (write-back) и подберите базу: загрузка не выше 80%, бюджет $1800 в месяц. Поможет и тип «NoSQL».",
    hint: "Write-back оставляет в базе 40% записей: 1200 в секунду. NoSQL M тянет 1080 записей: два шарда — 56%. Приложению нужно семь серверов M.",
    workload: WL({ read: 500, write: 3000, dataGB: 30, hotSet: 0.2 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(7), N("cache", "cache", { sizeGB: 4, ttl: 300 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>cache"]),
    goals: [
      { k: "util", kind: "db", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "param", kind: "cache", key: "policy", op: "==", value: "back" },
      { k: "cost", max: 1800 },
    ],
    solution: S(
      [users(), lb(), app(7), N("cache", "cache", { sizeGB: 4, ttl: 300, policy: "back" }), N("db", "db", { size: "M", shards: 2, engine: "nosql" })],
      ["users>lb>app>db", "app>cache"],
    ),
    show: ["cache.policy"],
  },
  {
    id: "sd13-ratelimiter",
    title: "Общий ограничитель",
    statement:
      "Ограничитель частоты на нескольких серверах должен иметь общий счётчик в быстром хранилище. Соберите схему: ограничитель на входе (предел не меньше 3000 — иначе обрежем обычный трафик в 2700 запросов), кэш для общих счётчиков с репликой (переживает отказ), серверы приложения не выше 80%.",
    hint: "lb → ограничитель → серверы; кэш связан с серверами, у кэша — реплика. Предел 3000–3500.",
    workload: WL({ read: 2500, write: 200, dataGB: 20, hotSet: 0.1 }),
    palette: ["lb", "limiter", "app", "cache", "db"],
    start: S([users(), lb(), app(5), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 3000 },
      { k: "link", from: "app", to: "cache" },
      { k: "param", kind: "cache", key: "replicas", op: ">=", value: 1 },
      { k: "survive", fail: "cache" },
      { k: "util", kind: "app", max: 0.8 },
    ],
    solution: S(
      [users(), lb(), N("limiter", "limiter", { limit: 3200 }), app(5), N("cache", "cache", { sizeGB: 2, ttl: 300, replicas: 1 }), N("db", "db", { size: "M" })],
      ["users>lb>limiter>app>db", "app>cache"],
    ),
  },
  {
    id: "sd13-pastebin",
    title: "Хранение блоков",
    statement:
      "Сервис хранения фрагментов: 4000 запросов в секунду на раздачу готовых файлов, 800 чтений и 50 записей метаданных. Файлы сейчас отдают серверы приложения. Вынесите их: CDN перед объектным хранилищем (≥90%), серверы и база — на метаданных. Загрузка не выше 80%, бюджет $650 в месяц.",
    hint: "CDN → хранилище (статика мимо серверов), динамика через балансировщик. Серверов M хватит двух, база M (чтения метаданных 800 в секунду не помещаются в S).",
    workload: WL({ static: 4000, read: 800, write: 50, dataGB: 100 }),
    palette: ["cdn", "lb", "app", "blob", "db"],
    start: S([users(), N("lb", "lb"), app(2), N("db", "db")], web),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 650 },
    ],
    solution: S(
      [users(), N("cdn", "cdn", { ttl: 300 }), N("lb", "lb"), app(2), N("blob", "blob"), N("db", "db", { size: "M" })],
      ["users>cdn>lb>app>db", "cdn>blob"],
    ),
  },
  {
    id: "sd13-final",
    title: "Сокращатель со статистикой",
    statement:
      "Итоговое упражнение главы. Сокращатель со счётчиком кликов: 3000 переходов и 3000 учтённых кликов-записей в секунду. Соберите схему: кэш с write-back и репликой (попадания ≥70%: при половине записей кэш отдаёт меньше), NoSQL-база с шардами и репликой с автопереключением, загрузка не выше 80%, схема переживает отказ базы, кэша и сервера приложения, бюджет $3200 в месяц.",
    hint: "Серверов M — двенадцать (6000 запросов); кэш 4 ГБ с репликой и write-back; NoSQL M: два шарда с репликой и автопереключением.",
    workload: WL({ read: 3000, write: 3000, dataGB: 300, hotSet: 0.01 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(12), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "hit", min: 0.7 },
      { k: "param", kind: "cache", key: "policy", op: "==", value: "back" },
      { k: "util", kind: "db", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 3200 },
    ],
    solution: S(
      [
        users(),
        lb(),
        app(12),
        N("cache", "cache", { sizeGB: 4, ttl: 3600, policy: "back", replicas: 1 }),
        N("db", "db", { size: "M", shards: 2, replicas: 1, failover: true, engine: "nosql" }),
      ],
      ["users>lb>app>db", "app>cache"],
    ),
    show: ["cache.policy"],
  },
];
