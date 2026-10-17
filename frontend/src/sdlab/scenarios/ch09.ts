import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 9 «Паттерны устойчивости»: ограничитель, автомат разрыва, переживание отказов, защитный контур. */

const app = (extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: 3, sessions: "external", ...extra });

export const CH09: SdScenario[] = [
  {
    id: "sd09-limiter-attack",
    title: "Ограничитель от атаки",
    statement:
      "Обычно сервис получает около 1500 запросов в секунду, но сейчас идёт атака: 6000. Серверы приложения (три M — 2100 запросов) перегружены. Поставьте ограничитель на входе и подберите предел: серверы загружены не больше чем на 95%, а до сервиса доходит не меньше 28% запросов (иначе вместе с атакой вы режете своих).",
    hint: "Ограничитель ставится между балансировщиком и серверами: lb → ограничитель → сервер. Предел от 1700 до 1995: 6000 × 0,28 ≈ 1680, 2100 × 0,95 ≈ 1995.",
    workload: WL({ read: 5000, write: 1000, dataGB: 20 }),
    palette: ["lb", "limiter", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), app(), N("db", "db", { size: "L" })], ["users>lb>app>db"]),
    goals: [
      { k: "has", kind: "limiter" },
      { k: "util", kind: "app", max: 0.95 },
      { k: "success", min: 0.28 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("limiter", "limiter", { limit: 1800 }), app(), N("db", "db", { size: "L" })], ["users>lb>limiter>app>db"]),
  },
  {
    id: "sd09-limit-normal",
    title: "Не режьте своих",
    statement:
      "Ограничитель уже стоит, но предел задан слишком строго (800 запросов в секунду), а обычная нагрузка — 1500. Часть настоящих пользователей получает отказ. Поднимите предел так, чтобы не меньше 99% запросов проходили, но защита сохранялась: предел не больше 2500.",
    hint: "Предел должен быть чуть выше обычной нагрузки (1500), но ниже ёмкости серверов (2100).",
    workload: WL({ read: 1300, write: 200, dataGB: 20 }),
    palette: ["lb", "limiter", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), N("limiter", "limiter", { limit: 800 }), app(), N("db", "db", { size: "M" })], ["users>lb>limiter>app>db"]),
    goals: [
      { k: "success", min: 0.99 },
      { k: "param", kind: "limiter", key: "limit", op: "<=", value: 2500 },
      { k: "util", kind: "app", max: 0.9 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("limiter", "limiter", { limit: 1800 }), app(), N("db", "db", { size: "M" })], ["users>lb>limiter>app>db"]),
  },
  {
    id: "sd09-fail-fast",
    title: "Отказ базы и повторы",
    statement:
      "Приложение повторяет запросы к базе до трёх раз без паузы. Когда база выходит из строя, повторы лавиной ложатся на единственную копию и не дают ей подняться. Сделайте так, чтобы схема переживала отказ базы: реплика с автопереключением и автомат разрыва в приложении.",
    hint: "У базы — «Реплики на шард» ≥ 1 и «Автопереключение»; у приложения — «Автомат разрыва» (виден в упражнении).",
    workload: WL({ read: 500, write: 100, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), app({ retries: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "survive", fail: "db" },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "noSpof", kinds: ["db"] },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), app({ retries: 3, breaker: true }), N("db", "db", { size: "M", replicas: 1, failover: true })], ["users>lb>app>db"]),
    show: ["app.retries", "app.breaker"],
  },
  {
    id: "sd09-degrade",
    title: "Кэш на случай сбоя",
    statement:
      "Страницы товаров читаются 2000 раз в секунду, и при перегрузке или отказе базы пользователи видят ошибки. Поставьте кэш, который принимает почти все чтения (не меньше 85%) и сохранит работу сайта, когда база тормозит: схема должна переживать отказ кэша (у кэша есть реплика) и не иметь единой точки отказа среди серверов приложения.",
    hint: "Кэш около 6 ГБ с TTL 3600 и репликой; рабочий набор — 6 ГБ. Серверы приложения: три и больше.",
    workload: WL({ read: 2000, write: 40, dataGB: 60, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), app(), N("db", "db")], ["users>lb>app>db"]),
    goals: [
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "cache" },
      { k: "noSpof", kinds: ["app", "cache"] },
      { k: "util", kind: "db", max: 0.8 },
    ],
    solution: S(
      [users(), N("lb", "lb", { instances: 2 }), app(), N("cache", "cache", { sizeGB: 6, ttl: 3600, replicas: 1 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
  },
  {
    id: "sd09-final",
    title: "Защитный контур",
    statement:
      "Итоговое упражнение главы. Соберите устойчивую схему: ограничитель на входе (предел 1500–2500 при обычных 1500), приложение с автоматом разрыва, база с репликой и автопереключением, кэш с репликой. Схема переживает отказ базы, кэша и сервера приложения, серверы загружены не выше 80%, бюджет $1500 в месяц.",
    hint: "lb → ограничитель → серверы; четыре сервера M (запас на отказ одного); кэш около 4 ГБ с репликой; база M с репликой и автопереключением.",
    workload: WL({ read: 1300, write: 200, dataGB: 40, hotSet: 0.1 }),
    palette: ["lb", "limiter", "app", "cache", "db"],
    start: S([users(), N("lb", "lb"), app({ retries: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 1500 },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "util", kind: "app", max: 0.8 },
      { k: "cost", max: 1500 },
    ],
    solution: S(
      [
        users(),
        N("lb", "lb", { instances: 2 }),
        N("limiter", "limiter", { limit: 2000 }),
        app({ instances: 4, retries: 2, breaker: true }),
        N("cache", "cache", { sizeGB: 4, ttl: 3600, replicas: 1 }),
        N("db", "db", { size: "M", replicas: 1, failover: true }),
      ],
      ["users>lb>limiter>app>db", "app>cache"],
    ),
    show: ["app.retries", "app.breaker"],
  },
];
