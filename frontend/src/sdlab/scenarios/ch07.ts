import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 7 «Поиск и хранение файлов»: поисковый кластер, шарды и реплики индекса, объектное хранилище, CDN. */

const chain = ["users>lb>app>db"];
const lb = () => N("lb", "lb", { instances: 2 });
const app = (n = 3) => N("app", "app", { size: "M", instances: n, sessions: "external" });

export const CH07: SdScenario[] = [
  {
    id: "sd07-search",
    title: "Поиск вынесен из базы",
    statement:
      "Половина из 800 чтений в секунду — поисковые запросы по тексту, и база их обрабатывает в несколько раз тяжелее обычных: она перегружена. Добавьте поисковый индекс и соедините с ним сервер приложения, чтобы база разгрузилась: загрузка не выше 80%.",
    hint: "Палитра содержит «Поиск». Свяжите сервер приложения с поиском: поисковые запросы пойдут туда, а база останется для обычных чтений.",
    workload: WL({ read: 800, write: 100, dataGB: 30, searchShare: 0.5 }),
    palette: ["lb", "app", "search", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "has", kind: "search" },
      { k: "link", from: "app", to: "search" },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(), N("search", "search"), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>search"]),
  },
  {
    id: "sd07-search-shards",
    title: "Шарды и реплики поиска",
    statement:
      "Индекс вырос до 150 ГБ, а шард должен быть не больше 40 ГБ. Поисковых запросов — 1000 в секунду, одна реплика тянет 1200. Подберите шарды (по объёму) и реплики (по нагрузке): загрузка не выше 80%, схема переживает потерю реплики поиска, стоимость не больше $1500 в месяц.",
    hint: "Шарды: 150 / 40 → четыре (по ~37 ГБ). Реплики: одной не хватает (83%), нужны две; кроме того, вторая реплика переживёт отказ первой. Цена: 150 × шарды × реплики.",
    workload: WL({ read: 1000, write: 60, dataGB: 150, searchShare: 1 }),
    palette: ["lb", "app", "search", "db"],
    start: S([users(), lb(), app(), N("search", "search"), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>search"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "search" },
      { k: "cost", max: 2200 },
    ],
    solution: S([users(), lb(), app(), N("search", "search", { shards: 4, replicas: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>search"]),
  },
  {
    id: "sd07-blob",
    title: "Файлы — в объектное хранилище",
    statement:
      "Сайт отдаёт 8000 запросов в секунду картинок и видео прямо через серверы приложения: они тратят силы на передачу байтов. Подключите объектное хранилище и соедините с ним сервер приложения — статика пойдёт мимо него, — и заодно уменьшите парк: стоимость не больше $300 в месяц при загрузке не выше 80%.",
    hint: "Хранилище обслуживает статику, сервер остаётся для динамики. Тогда хватит одного сервера M и базы S. Балансировщик можно не ставить, если сервер один.",
    workload: WL({ static: 8000, read: 300, write: 40, dataGB: 10 }),
    palette: ["lb", "app", "blob", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("db", "db")], chain),
    goals: [
      { k: "has", kind: "blob" },
      { k: "link", from: "app", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 300 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { size: "M" }), N("blob", "blob"), N("db", "db")], ["users>lb>app>db", "app>blob"]),
  },
  {
    id: "sd07-cdn-blob",
    title: "CDN перед хранилищем",
    statement:
      "Файлы лежат в объектном хранилище, но пользователи по всему миру получают их медленно, а 30 000 запросов в секунду стоят дорого. Поставьте CDN перед хранилищем (CDN соединяется с хранилищем): не меньше 90% статики отдаётся из CDN, схема укладывается в $700 в месяц.",
    hint: "CDN принимает пользователей, статику забирает у хранилища при промахе, а динамические запросы передаёт балансировщику. TTL 300 даёт 90%.",
    workload: WL({ static: 30000, read: 200, write: 30, dataGB: 10 }),
    palette: ["cdn", "lb", "app", "blob", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M" }), N("blob", "blob"), N("db", "db")], ["users>lb>app>db", "app>blob"]),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 700 },
    ],
    solution: S(
      [users(), N("cdn", "cdn", { ttl: 300 }), N("lb", "lb"), N("app", "app", { size: "M" }), N("blob", "blob"), N("db", "db")],
      ["users>cdn>lb>app>db", "cdn>blob"],
    ),
  },
  {
    id: "sd07-search-ha",
    title: "Отказ реплики поиска",
    statement:
      "Поиск стоит одним узлом: при его отказе пользователи получают ошибки на каждый поисковый запрос. Добавьте реплику поиска так, чтобы схема переживала отказ реплики и нагрузка в этот момент оставалась в норме.",
    hint: "У поиска параметр «Реплики»: нужно хотя бы две. Каждая реплика тянет 1200 запросов, нагрузка 600 — после потери одной загрузка 50%.",
    workload: WL({ read: 700, write: 40, dataGB: 20, searchShare: 0.85 }),
    palette: ["lb", "app", "search", "db"],
    start: S([users(), lb(), app(), N("search", "search"), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>search"]),
    goals: [
      { k: "survive", fail: "search" },
      { k: "noSpof", kinds: ["search"] },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), lb(), app(), N("search", "search", { replicas: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>search"]),
  },
  {
    id: "sd07-final",
    title: "Каталог с картинками и поиском",
    statement:
      "Итоговое упражнение главы. Маркетплейс: 20 000 запросов статики, 1200 чтений (половина — поиск по каталогу в 90 ГБ) и 100 записей в секунду. Соберите схему: CDN перед хранилищем (≥90%), поисковый индекс с шардами по объёму и двумя репликами, база без перегрузки, загрузка не выше 80%, переживание отказа поиска, бюджет $2000 в месяц.",
    hint: "Шарды поиска: 90 / 40 → три. Реплики: две. CDN → хранилище, приложение → поиск и хранилище. Три сервера M и база M.",
    workload: WL({ static: 20000, read: 1200, write: 100, dataGB: 90, searchShare: 0.5 }),
    palette: ["cdn", "lb", "app", "search", "blob", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 2, sessions: "external" }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "app", to: "search" },
      { k: "link", from: "cdn", to: "blob" },
      { k: "survive", fail: "search" },
      { k: "cost", max: 2000 },
    ],
    solution: S(
      [
        users(),
        N("cdn", "cdn", { ttl: 300 }),
        N("lb", "lb"),
        N("app", "app", { size: "M", instances: 3, sessions: "external" }),
        N("search", "search", { shards: 3, replicas: 2 }),
        N("blob", "blob"),
        N("db", "db", { size: "M" }),
      ],
      ["users>cdn>lb>app>db", "app>search", "cdn>blob"],
    ),
  },
];
