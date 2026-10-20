import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 22 «Проект: социальная сеть»: этапы от графа друзей до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  hybrid?: boolean;
  cdn?: boolean;
  cache?: number;
  dbSize?: string;
  dbShards?: number;
  dbRange?: boolean;
  dbRepl?: boolean;
  queue?: { workers: number };
  ws?: number;
  stream?: { notify: number; analytics?: number };
  ml?: number;
  auth?: number;
  search?: { shards: number; replicas: number };
  tier?: string;
  zone?: boolean;
  mon?: boolean;
  limiter?: boolean;
  lbN?: number;
}

const vk = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    ...(o.cdn ? [N("cdn", "cdn", { ttl: 3600 })] : []),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    ...(o.limiter ? [N("limiter", "limiter", { limit: 20000 })] : []),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, feed: o.hybrid ? "hybrid" : "pull", ...(o.zone ? { deploy: "rolling" } : {}) }),
    ...(o.cache ? [N("cache", "cache", { sizeGB: o.cache, ttl: 3600, replicas: 1, zone: z })] : []),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbShards ? { shards: o.dbShards } : {}), shardKey: o.dbRange ? "range" : "hash", ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    N("blob", "blob", { tier: o.tier ?? "hot" }),
    ...(o.queue ? [N("queue", "queue"), N("worker", "worker", { size: "M", instances: o.queue.workers, idempotent: true, pricing: "spot", zone: z })] : []),
    ...(o.ws ? [N("ws", "ws", { instances: o.ws })] : []),
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
    ...(o.ws ? ["users>ws>app"] : []),
    ...(o.stream ? ["app>stream>notify", ...(o.stream.analytics ? ["stream>an"] : [])] : []),
    ...(o.ml ? ["app>ml"] : []),
    ...(o.auth ? ["app>auth"] : []),
    ...(o.search ? ["app>search"] : []),
  ];
  return S(nodes, edges);
};

const P1 = ["lb", "app", "cache", "db", "blob"] as SdScenario["palette"];
const P2 = [...P1, "queue", "worker"] as SdScenario["palette"];
const P3 = [...P2, "ws", "stream", "notify", "analytics"] as SdScenario["palette"];
const P4 = [...P3, "cdn"] as SdScenario["palette"];
const P5 = [...P4, "ml", "auth", "search"] as SdScenario["palette"];
const P6 = [...P5, "limiter", "monitor"] as SdScenario["palette"];

const W1: Workload = WL({ read: 3000, write: 2000, dataGB: 200, hotSet: 0.05, hotKey: 0.12 });
const W2: Workload = { ...W1, read: 6000, write: 600, fanout: 120, spikeSec: 10 };
const W3: Workload = { ...W2, connections: 200000, msgPerConn: 0.02, monotonic: true };
const W4: Workload = { ...W3, static: 30000, mediaTB: 1500 };
const W5: Workload = { ...W4, calls: { auth: 1, ml: 0.2 }, searchShare: 0.1 };

const S1: Opts = { app: 9, cache: 10, dbSize: "L", dbShards: 3 };
const S2: Opts = { ...S1, app: 12, hybrid: true, queue: { workers: 5 } };
const S3: Opts = { ...S2, app: 20, ws: 17, stream: { notify: 5, analytics: 1 } };
const S4: Opts = { ...S3, cdn: true, tier: "mix" };
const S5: Opts = { ...S4, ml: 6, auth: 3, search: { shards: 10, replicas: 2 } };

export const CH22: SdScenario[] = [
  {
    id: "sd22-s1-graph",
    title: "Этап 1. Профили, друзья и горячие ключи",
    statement:
      "Сеть растёт: 3000 чтений и 2000 записей в секунду (посты, лайки, заявки в друзья), а 12% запросов приходится на самые популярные профили и сообщества. Одна база не вытянет запись. Поставьте кэш (≥75%: записей много, поэтому кэш отдаёт меньше обычного; рабочий набор 10 ГБ) и шардируйте базу по хешу так, чтобы загрузка не превышала 80%, а на самый нагруженный шард приходилось не больше 45% запросов. Бюджет — $3500 в месяц.",
    hint: "База L с тремя шардами по хешу: на горячий шард придётся 12% + 88%/3 ≈ 41% запросов. Серверов M — 9, кэш 10 ГБ.",
    workload: W1,
    palette: P1,
    start: vk({ app: 9, dbSize: "M" }),
    goals: [
      { k: "hit", min: 0.75 },
      { k: "shardShare", max: 0.45 },
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3500 },
    ],
    solution: vk(S1),
  },
  {
    id: "sd22-s2-feed",
    title: "Этап 2. Лента новостей",
    statement:
      "Лента собирается из друзей и сообществ: 6000 открытий и 600 публикаций в секунду, у автора в среднем 120 подписчиков. Выберите гибрид, добавьте очередь с идемпотентными обработчиками на споте (рассылка в ленты идёт через неё, после пика в 10 секунд — без отставания): всё не выше 80%, бюджет — $4100 в месяц.",
    hint: "Гибрид умножает запись в 2,2 раза. Обработчики M — 5 (запись 1320 в секунду), база L с тремя шардами, серверов M — 12.",
    workload: W2,
    palette: P2,
    start: vk(S1),
    goals: [
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 4100 },
    ],
    solution: vk(S2),
    show: ["app.feed", "worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd22-s3-messages",
    title: "Этап 3. Личные сообщения",
    statement:
      "Сообщения: 200 000 соединений получают по 0,02 события в секунду (4000 в секунду); идентификаторы растут со временем, а база шардирована по диапазонам — все новые сообщения попадают в последний шард. Смените способ шардирования, добавьте шлюзы WebSocket, поток событий и уведомления: на самый нагруженный шард не больше 45%, шлюзы и уведомления — не выше 80%, бюджет — $7300 в месяц.",
    hint: "Параметр «Ключ шардирования» базы — хеш. Шлюзов ws — 17 (200 000 / 15 000 = 13,3 при 78%). Серверов M — 20 (принимают и сообщения), уведомления — 5 экземпляров.",
    workload: W3,
    palette: P3,
    start: vk({ ...S2, dbRange: true }),
    goals: [
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "shardShare", max: 0.45 },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "util", kind: "ws", max: 0.8 },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 7300 },
    ],
    solution: vk(S3),
    show: ["db.shardKey"],
  },
  {
    id: "sd22-s4-media",
    title: "Этап 4. Фото, музыка и видео",
    statement:
      "Медиа: 30 000 запросов в секунду за файлами, 1500 ТБ в хранилище. Поставьте CDN перед хранилищем (≥95%) и переведите файлы на дешёвый класс хранения: горячее стоит $23 за ТБ — это 34 500 в месяц. Загрузка не выше 80%, бюджет — $23 000 в месяц.",
    hint: "CDN → хранилище, TTL 3600. Класс хранения «горячее + холодное» — $10 за ТБ (15 000), «холодное» — $4. Параметр показан в упражнении.",
    workload: W4,
    palette: P4,
    start: vk(S3),
    goals: [
      { k: "cdnHit", min: 0.95 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 23000 },
    ],
    solution: vk(S4),
    show: ["blob.tier"],
  },
  {
    id: "sd22-s5-search",
    title: "Этап 5. Поиск, права и рекомендации",
    statement:
      "Добавлены поиск людей и сообществ (10% чтений, индекс 200 ГБ), проверка прав на каждый запрос и рекомендации (20% запросов обращаются к сервису ранжирования). Подключите поиск, сервис входа и ранжирование: загрузка не выше 80%, схема переживает отказ каждого из них, бюджет — $26 500 в месяц.",
    hint: "Поиск: 5 шардов × 2 реплики. Вход: 3 экземпляра (нагрузка 6600 запросов). Ранжирование: 6 экземпляров (1320 запросов, после отказа одного — 1500).",
    workload: W5,
    palette: P5,
    start: vk(S4),
    goals: [
      { k: "link", from: "app", to: "search" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "ml" },
      { k: "survive", fail: "search" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 26500 },
    ],
    solution: vk(S5),
    maxNodes: 18,
  },
  {
    id: "sd22-s6-reliability",
    title: "Этап 6. Надёжность и защита",
    statement:
      "Сеть нельзя ронять. Разнесите серверы, кэш, обработчиков и базу по зонам, включите rolling-выкладку, реплику базы с автопереключением, второй балансировщик, ограничитель на входе (предел не меньше нагрузки 10 600) и мониторинг. Схема переживает отказ зоны, выкладки, сервера, базы и кэша, загрузка не выше 80%, бюджет — $31 000 в месяц.",
    hint: "Серверов M — 24 в трёх зонах (после потери зоны остаётся 16 — 11 200 при нагрузке 10 600). База L с тремя шардами и репликой, предел ограничителя около 20 000.",
    workload: W5,
    palette: P6,
    maxNodes: 20,
    start: vk(S5),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 10600 },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 31000 },
    ],
    solution: vk({ ...S5, app: 24, dbRepl: true, zone: true, mon: true, limiter: true, lbN: 2 }),
    show: ["app.deploy"],
  },
  {
    id: "sd22-exam",
    title: "Экзамен. Социальная сеть целиком",
    statement:
      "Итоговое задание. Сеть в пик: 9000 чтений и 1500 записей в секунду (12% — самые популярные профили и сообщества), 40 000 запросов за медиа, 300 000 соединений для сообщений (4500 событий в секунду), 1500 ТБ файлов, поиск (индекс 400 ГБ), рекомендации на 20% запросов, права на каждый запрос. Соберите схему с нуля: CDN и хранилище с дешёвым классом, кэш, гибридная лента через очередь и обработчиков на споте, база по хешу с шардами и репликой, шлюзы WebSocket, поток с уведомлениями и аналитикой, поиск, вход, ранжирование, ограничитель, мониторинг, два балансировщика. Переживает отказ зоны, выкладки, сервера, базы, кэша, поиска, входа и ранжирования; загрузка не выше 80%; бюджет — $36 000 в месяц.",
    hint: "Серверов M — 33 в трёх зонах, обработчиков M — 11, база L с 4 шардами по хешу и репликой, шлюзы ws — 26, уведомления — 6, ранжирование — 9, вход — 4, поиск — 10 шардов × 2, кэш 16 ГБ.",
    workload: { ...W5, read: 9000, write: 1500, connections: 300000, msgPerConn: 0.015, static: 40000, dataGB: 400, hotSet: 0.04 },
    palette: P6,
    maxNodes: 20,
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "hit", min: 0.75 },
      { k: "cdnHit", min: 0.95 },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "shardShare", max: 0.45 },
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "app", to: "search" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "ml" },
      { k: "has", kind: "limiter" },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "search" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 36000 },
    ],
    solution: vk({
      app: 33,
      hybrid: true,
      cdn: true,
      cache: 16,
      dbSize: "L",
      dbShards: 4,
      dbRepl: true,
      queue: { workers: 11 },
      ws: 26,
      stream: { notify: 6, analytics: 1 },
      ml: 9,
      auth: 4,
      search: { shards: 10, replicas: 2 },
      tier: "mix",
      zone: true,
      mon: true,
      limiter: true,
      lbN: 2,
    }),
    show: ["app.deploy", "app.feed", "worker.pricing", "blob.tier", "db.shardKey"],
  },
];
