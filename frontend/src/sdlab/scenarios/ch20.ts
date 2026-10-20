import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 20 «Проект: фотосеть»: этапы от MVP до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  hybrid?: boolean;
  cdn?: boolean;
  cache?: number;
  dbSize?: string;
  dbRepl?: boolean;
  dbShards?: number;
  queue?: { workers: number };
  stream?: { notify: number; analytics?: number };
  ml?: number;
  auth?: number;
  search?: { shards: number; replicas: number };
  tier?: string;
  zone?: boolean;
  mon?: boolean;
  limiter?: boolean;
  lbN?: number;
  spot?: boolean;
}

const insta = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    ...(o.cdn ? [N("cdn", "cdn", { ttl: 3600 })] : []),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    ...(o.limiter ? [N("limiter", "limiter", { limit: 12000 })] : []),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, feed: o.hybrid ? "hybrid" : "pull", ...(o.zone ? { deploy: "rolling" } : {}), ...(o.ml ? { retries: 1, breaker: true } : {}) }),
    ...(o.cache ? [N("cache", "cache", { sizeGB: o.cache, ttl: 3600, replicas: 1, zone: z })] : []),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbShards ? { shards: o.dbShards } : {}), ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    N("blob", "blob", { tier: o.tier ?? "hot" }),
    ...(o.queue ? [N("queue", "queue"), N("worker", "worker", { size: "M", instances: o.queue.workers, idempotent: true, pricing: o.spot === false ? "ondemand" : "spot", zone: z })] : []),
    ...(o.stream ? [N("stream", "stream", { partitions: 3 }), N("notify", "notify", { instances: o.stream.notify }), ...(o.stream.analytics ? [N("an", "analytics", { instances: o.stream.analytics })] : [])] : []),
    ...(o.ml ? [N("ml", "ml", { instances: o.ml })] : []),
    ...(o.auth ? [N("auth", "auth", { instances: o.auth })] : []),
    ...(o.search ? [N("search", "search", o.search)] : []),
    ...(o.mon ? [N("mon", "monitor")] : []),
  ];
  const edges = [
    `users>${o.cdn ? "cdn>" : ""}lb>${o.limiter ? "limiter>" : ""}app>db`,
    "app>blob",
    ...(o.cdn ? ["cdn>blob"] : []),
    ...(o.cache ? ["app>cache"] : []),
    ...(o.queue ? ["app>queue>worker>db", "worker>blob"] : []),
    ...(o.stream ? ["app>stream>notify", ...(o.stream.analytics ? ["stream>an"] : [])] : []),
    ...(o.ml ? ["app>ml"] : []),
    ...(o.auth ? ["app>auth"] : []),
    ...(o.search ? ["app>search"] : []),
  ];
  return S(nodes, edges);
};

const P1 = ["lb", "app", "cache", "db", "blob"] as SdScenario["palette"];
const P2 = [...P1, "queue", "worker"] as SdScenario["palette"];
const P3 = [...P2, "cdn"] as SdScenario["palette"];
const P5 = [...P3, "stream", "notify", "analytics"] as SdScenario["palette"];
const P6 = [...P5, "ml", "auth", "search"] as SdScenario["palette"];
const P7 = [...P6, "limiter", "monitor"] as SdScenario["palette"];

const FULL: Opts = { app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true, stream: { notify: 2, analytics: 1 }, ml: 5, auth: 3, search: { shards: 5, replicas: 2 } };

const W1: Workload = WL({ static: 300, read: 400, write: 60, dataGB: 10, mediaTB: 5 });
const W2: Workload = WL({ static: 300, read: 400, write: 300, dataGB: 10, mediaTB: 5, spikeSec: 10 });
const W3: Workload = { ...W2, static: 25000, read: 2500 };
const W4: Workload = { ...W3, read: 5000, write: 300, dataGB: 200, hotSet: 0.04, fanout: 150, mediaTB: 30 };
const W5: Workload = { ...W4 };
const W6: Workload = { ...W5, calls: { auth: 1, ml: 0.2 }, searchShare: 0.08 };

export const CH20: SdScenario[] = [
  {
    id: "sd20-s1-mvp",
    title: "Этап 1. Первая версия",
    statement:
      "Фотосеть стартует: 400 чтений и 60 записей метаданных в секунду, 300 запросов фото в секунду, 5 ТБ снимков. Храните снимки в объектном хранилище, метаданные — в базе. Загрузка не выше 80%, стоимость не больше $450 в месяц.",
    hint: "Сервер → база (метаданные) и сервер → хранилище (снимки). Хранилище стоит $25 плюс $23 за ТБ — 140.",
    workload: W1,
    palette: P1,
    start: S([users(), N("app", "app", { size: "M" }), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "has", kind: "blob" },
      { k: "link", from: "app", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 450 },
    ],
    solution: S([users(), N("app", "app", { size: "M" }), N("db", "db"), N("blob", "blob")], ["users>app>db", "app>blob"]),
  },
  {
    id: "sd20-s2-processing",
    title: "Этап 2. Обработка фото",
    statement:
      "Публикаций стало 300 в секунду, и каждую нужно обработать: сделать размеры и превью. Добавьте очередь и идемпотентных обработчиков на споте (не меньше двух), которые читают очередь и записывают результат в базу и хранилище. После пика в 10 секунд очередь разбирается без отставания (допустимо 5 с), база не выше 80%, бюджет — $1300 в месяц.",
    hint: "Сервер → очередь → обработчики → база и хранилище. Два обработчика M тянут 800 в секунду при нагрузке 300. Параметры «Тариф» и «Идемпотентная обработка» показаны в упражнении.",
    workload: W2,
    palette: P2,
    start: insta({ app: 3, dbSize: "L" }),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "link", from: "worker", to: "blob" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "noSpof", kinds: ["worker"] },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1300 },
    ],
    solution: insta({ app: 3, queue: { workers: 2 }, dbSize: "L" }),
    show: ["worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd20-s3-cdn",
    title: "Этап 3. Раздача через CDN",
    statement:
      "Просмотров снимков стало 25 000 в секунду. Поставьте CDN перед хранилищем с высокой долей попаданий (≥95%, неизменные адреса позволяют долгий TTL), чтобы средняя задержка была не больше 40 мс, серверы и остальное — не выше 80%, а бюджет — $2000 в месяц.",
    hint: "CDN → хранилище, TTL 3600 даёт 98%. Динамику CDN передаёт балансировщику. Серверов M понадобится семь, база — L.",
    workload: W3,
    palette: P3,
    start: insta({ app: 3, queue: { workers: 2 }, dbSize: "L" }),
    goals: [
      { k: "cdnHit", min: 0.95 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "p50", max: 40 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 2000 },
    ],
    solution: insta({ app: 7, queue: { workers: 2 }, cdn: true, dbSize: "L" }),
  },
  {
    id: "sd20-s4-feed",
    title: "Этап 4. Лента подписок",
    statement:
      "Появилась лента подписок: 5000 открытий в секунду, у автора в среднем 150 подписчиков, 30 ТБ снимков. Выберите гибридную ленту, поставьте кэш лент и метаданных (≥90%, рабочий набор 8 ГБ), усильте базу репликой с автопереключением (запись тяжелее: нужна база L) и обработчиков под удвоенную запись. Всё не выше 80%, схема переживает отказ базы и кэша, бюджет — $3900 в месяц.",
    hint: "Гибрид умножает запись в 2,5 раза (750 в секунду). Три обработчика M, база L с репликой, кэш 8 ГБ с репликой, серверов M — десять.",
    workload: W4,
    palette: P3,
    start: insta({ app: 7, queue: { workers: 2 }, cdn: true, dbSize: "L" }),
    goals: [
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "hit", min: 0.9 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3900 },
    ],
    solution: insta({ app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true }),
    show: ["app.feed", "worker.pricing"],
  },
  {
    id: "sd20-s5-events",
    title: "Этап 5. События и уведомления",
    statement:
      "Каждое действие — событие. Подключите поток событий (три партиции) к серверу, а к потоку — уведомления и аналитику: потребители должны быть загружены не выше 80%. Уведомлений должно хватить и на пуши при отказе одного экземпляра, бюджет — $4300 в месяц.",
    hint: "Сервер → поток → уведомления и аналитика. Событий около 300 в секунду; два экземпляра уведомлений (по 1500) и один аналитики.",
    workload: W5,
    palette: P5,
    start: insta({ app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true }),
    goals: [
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "util", kind: "analytics", max: 0.8 },
      { k: "noSpof", kinds: ["notify"] },
      { k: "cost", max: 4300 },
    ],
    solution: insta({ app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true, stream: { notify: 2, analytics: 1 } }),
  },
  {
    id: "sd20-s6-explore",
    title: "Этап 6. Рекомендации и поиск",
    statement:
      "Раздел рекомендаций обращается к сервису ранжирования на 20% запросов (около 1060 в секунду; один экземпляр тянет 300), каждый запрос проверяет сервис входа, а 8% чтений — поиск (индекс 200 ГБ). Подключите сервис ранжирования, сервис входа и поиск: загрузка не выше 80%, схема переживает отказ ранжирования, входа и поиска, бюджет — $7200 в месяц.",
    hint: "Ранжирование: пять экземпляров (1500; при отказе одного остаётся 1200 при нагрузке 1060). Вход: три экземпляра (после отказа одного остаётся 8000 при нагрузке 5300). Поиск: 5 шардов × 2 реплики (200 / 40).",
    workload: W6,
    palette: P6,
    start: insta({ app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true, stream: { notify: 2, analytics: 1 } }),
    goals: [
      { k: "link", from: "app", to: "ml" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "search" },
      { k: "util", kind: "ml", max: 0.8 },
      { k: "survive", fail: "ml" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "search" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 7200 },
    ],
    solution: insta({ app: 10, queue: { workers: 3 }, cdn: true, hybrid: true, cache: 8, dbSize: "L", dbRepl: true, stream: { notify: 2, analytics: 1 }, ml: 5, auth: 3, search: { shards: 5, replicas: 2 } }),
    show: ["app.retries", "app.breaker"],
    maxNodes: 16,
  },
  {
    id: "sd20-s7-reliability",
    title: "Этап 7. Надёжность, защита и деньги",
    statement:
      "Фотосеть должна открываться всегда. Разнесите серверы, кэш, обработчиков и базу по трём зонам, включите rolling-выкладку, добавьте второй балансировщик, ограничитель на входе (предел не меньше обычной нагрузки 5300) и мониторинг, переведите хранилище на смешанный класс (30 ТБ). Схема переживает отказ зоны, выкладки, сервера, базы и кэша, загрузка не выше 80%, бюджет — $8000 в месяц.",
    hint: "Серверов M — 12 в трёх зонах (после потери зоны остаётся 8 — 5600). Ограничитель между балансировщиком и серверами, предел около 12 000. Класс хранения у хранилища — смешанный.",
    workload: W6,
    palette: P7,
    maxNodes: 18,
    start: insta(FULL),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 5300 },
      { k: "has", kind: "monitor" },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 8000 },
    ],
    solution: insta({ ...FULL, app: 12, zone: true, mon: true, limiter: true, lbN: 2, tier: "mix" }),
    show: ["app.deploy", "app.retries", "app.breaker", "blob.tier"],
  },
  {
    id: "sd20-exam",
    title: "Экзамен. Фотосеть целиком",
    statement:
      "Итоговое задание. Фотосеть в полной силе: 40 000 запросов в секунду за снимками, 7000 открытий ленты и 400 публикаций в секунду, 600 ТБ снимков, у автора в среднем 150 подписчиков, 250 ГБ метаданных (рабочий набор 10 ГБ). Соберите схему с нуля: хранилище (смешанный класс) и CDN (≥95%), кэш (≥90%), гибридная лента, очередь с идемпотентными обработчиками на споте, поток событий с уведомлениями и аналитикой, сервис ранжирования (20% запросов), сервис входа, поиск, ограничитель, мониторинг, два балансировщика. Переживает отказ зоны, выкладки, сервера, базы, кэша, ранжирования, входа и поиска; загрузка не выше 80%; средняя задержка ≤ 40 мс; бюджет — $18 000 в месяц.",
    hint: "Серверов M — 17 в трёх зонах; база L с 2 шардами и репликой (запись удваивается лентой); ранжирование — 7 экземпляров, вход — 3, поиск 6×2 (250 ГБ), обработчиков M — 4, кэш 10 ГБ с репликой.",
    workload: { ...W6, static: 40000, read: 7000, write: 400, dataGB: 250, hotSet: 0.04, mediaTB: 600 },
    palette: P7,
    maxNodes: 18,
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "has", kind: "blob" },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "cdnHit", min: 0.95 },
      { k: "hit", min: 0.9 },
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "link", from: "cdn", to: "blob" },
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "link", from: "app", to: "ml" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "search" },
      { k: "has", kind: "limiter" },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "ml" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "search" },
      { k: "p50", max: 40 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 18000 },
    ],
    solution: insta({
      app: 17,
      queue: { workers: 4 },
      cdn: true,
      hybrid: true,
      cache: 10,
      dbSize: "L",
      dbShards: 2,
      dbRepl: true,
      stream: { notify: 2, analytics: 1 },
      ml: 7,
      auth: 3,
      search: { shards: 7, replicas: 2 },
      tier: "mix",
      zone: true,
      mon: true,
      limiter: true,
      lbN: 2,
    }),
    show: ["app.deploy", "app.retries", "app.breaker", "app.feed", "worker.pricing", "worker.idempotent", "blob.tier"],
  },
];

