import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 24 «Проект: мессенджер»: этапы от хранилища чатов до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  cache?: number;
  dbSize?: string;
  dbShards?: number;
  dbRange?: boolean;
  dbRepl?: boolean;
  queue?: { workers: number };
  ws?: number;
  stream?: { notify: number; analytics?: number };
  cdn?: boolean;
  tier?: string;
  auth?: number;
  ml?: number;
  zone?: boolean;
  mon?: boolean;
  limiter?: boolean;
  lbN?: number;
}

const chat = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    ...(o.cdn ? [N("cdn", "cdn", { ttl: 3600 })] : []),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    ...(o.limiter ? [N("limiter", "limiter", { limit: 20000 })] : []),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, ...(o.zone ? { deploy: "rolling" } : {}) }),
    ...(o.cache ? [N("cache", "cache", { sizeGB: o.cache, ttl: 3600, replicas: 1, zone: z })] : []),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbShards ? { shards: o.dbShards } : {}), shardKey: o.dbRange ? "range" : "hash", ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    N("blob", "blob", { tier: o.tier ?? "hot" }),
    ...(o.queue ? [N("queue", "queue"), N("worker", "worker", { size: "M", instances: o.queue.workers, idempotent: true, pricing: "spot", zone: z })] : []),
    ...(o.ws ? [N("ws", "ws", { instances: o.ws })] : []),
    ...(o.stream ? [N("stream", "stream", { partitions: 3 }), N("notify", "notify", { instances: o.stream.notify }), ...(o.stream.analytics ? [N("an", "analytics", { instances: o.stream.analytics })] : [])] : []),
    ...(o.auth ? [N("auth", "auth", { instances: o.auth })] : []),
    ...(o.ml ? [N("ml", "ml", { instances: o.ml })] : []),
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
    ...(o.auth ? ["app>auth"] : []),
    ...(o.ml ? ["app>ml"] : []),
  ];
  return S(nodes, edges);
};

const P1 = ["lb", "app", "cache", "db", "blob"] as SdScenario["palette"];
const P2 = [...P1, "ws", "stream", "notify", "analytics"] as SdScenario["palette"];
const P3 = [...P2, "queue", "worker"] as SdScenario["palette"];
const P4 = [...P3, "cdn"] as SdScenario["palette"];
const P5 = [...P4, "auth", "ml"] as SdScenario["palette"];
const P6 = [...P5, "limiter", "monitor"] as SdScenario["palette"];

const W1: Workload = WL({ read: 4000, write: 2000, dataGB: 600, hotSet: 0.015, hotKey: 0.1, monotonic: true });
const W2: Workload = { ...W1, connections: 300000, msgPerConn: 0.02 };
const W3: Workload = { ...W2, fanout: 100, spikeSec: 10 };
const W4: Workload = { ...W3, static: 20000, mediaTB: 800 };
const W5: Workload = { ...W4, calls: { auth: 1, ml: 0.1 } };

const S1: Opts = { app: 11, cache: 10, dbSize: "L", dbShards: 3 };
const S2: Opts = { ...S1, app: 22, ws: 26, stream: { notify: 8, analytics: 2 } };
const S3: Opts = { ...S2, queue: { workers: 14 } };
const S4: Opts = { ...S3, cdn: true, tier: "mix" };
const S5: Opts = { ...S4, auth: 3, ml: 4 };

export const CH24: SdScenario[] = [
  {
    id: "sd24-s1-storage",
    title: "Этап 1. Хранилище чатов",
    statement:
      "Сообщения: 5000 чтений истории и 3000 записей в секунду, 600 ГБ, идентификаторы сообщений растут со временем, а 10% запросов приходится на самые активные чаты. База сейчас шардирована по диапазонам — все новые сообщения идут в последний шард. Смените способ шардирования, поставьте кэш свежих сообщений (≥70%; рабочий набор 8 ГБ): загрузка не выше 80%, на самый нагруженный шард не больше 45% запросов, бюджет — $3600 в месяц.",
    hint: "Ключ шардирования — хеш от идентификатора чата. База L с тремя шардами: на горячий шард придётся 10% + 90%/3 = 40%. Серверов M — 8, кэш 8 ГБ.",
    workload: W1,
    palette: P1,
    start: chat({ ...S1, dbRange: true }),
    goals: [
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "shardShare", max: 0.45 },
      { k: "hit", min: 0.7 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3600 },
    ],
    solution: chat(S1),
    show: ["db.shardKey"],
  },
  {
    id: "sd24-s2-gateways",
    title: "Этап 2. Шлюзы, поток и пуши",
    statement:
      "Добавлены постоянные соединения: 300 000 клиентов получают по 0,02 события в секунду (6000 в секунду). Поставьте шлюзы WebSocket, пропустите события через поток, подключите уведомления для тех, кто не в сети, и аналитику (задержка доставки, потери). Шлюзы и потребители — не выше 80%, бюджет — $8200 в месяц.",
    hint: "Шлюзов ws — 26 (300 000 / 15 000 = 20 при 77%). Серверов M — 22 (принимают и события), уведомления — 8, аналитика — 2.",
    workload: W2,
    palette: P2,
    start: chat(S1),
    goals: [
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "util", kind: "ws", max: 0.8 },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 8200 },
    ],
    solution: chat(S2),
    maxNodes: 16,
  },
  {
    id: "sd24-s3-groups",
    title: "Этап 3. Группы и каналы",
    statement:
      "Группы: в среднем сообщение получают 100 участников, запись в хранилище умножается. Рассылку в группы ведёт очередь с идемпотентными обработчиками на споте; после пика в 10 секунд отставания быть не должно. Всё не выше 80%, бюджет — $8700 в месяц.",
    hint: "Очередь и обработчики M — 14 (запись в хранилище умножается на 100 получателей), связь приложение → очередь → обработчики → база. Цена на споте ниже, идемпотентность включена.",
    workload: W3,
    palette: P3,
    start: chat(S2),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 8700 },
    ],
    solution: chat(S3),
    show: ["worker.pricing", "worker.idempotent"],
    maxNodes: 18,
  },
  {
    id: "sd24-s4-media",
    title: "Этап 4. Фото и видео в переписках",
    statement:
      "Вложения: 20 000 запросов в секунду за файлами, 800 ТБ в хранилище. Поставьте CDN перед хранилищем (≥95%) и переведите файлы на дешёвый класс хранения: горячее стоит $23 за ТБ — это 18 400 в месяц. Загрузка не выше 80%, бюджет — $17 000 в месяц.",
    hint: "CDN → хранилище, TTL 3600. Класс хранения «горячее + холодное» — $10 за ТБ (20 000), «холодное» — $4.",
    workload: W4,
    palette: P4,
    start: chat(S3),
    goals: [
      { k: "cdnHit", min: 0.95 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 17000 },
    ],
    solution: chat(S4),
    show: ["blob.tier"],
    maxNodes: 18,
  },
  {
    id: "sd24-s5-abuse",
    title: "Этап 5. Вход и защита от спама",
    statement:
      "Каждый запрос проверяет вход, а 10% сообщений проходят через сервис ранжирования, который отсекает спам. Подключите сервис входа и ранжирование: загрузка не выше 80%, схема переживает отказ каждого из них, бюджет — $18 000 в месяц.",
    hint: "Вход: 3 экземпляра, ранжирование: 4 (после отказа одного остаётся 900 запросов).",
    workload: W5,
    palette: P5,
    start: chat(S4),
    goals: [
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "ml" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 18000 },
    ],
    solution: chat(S5),
    maxNodes: 20,
  },
  {
    id: "sd24-s6-reliability",
    title: "Этап 6. Надёжность и регионы",
    statement:
      "Мессенджер не должен молчать. Разнесите серверы, кэш, обработчиков и базу по зонам, включите rolling-выкладку, реплику базы с автопереключением, второй балансировщик, ограничитель на входе (предел не меньше нагрузки 8000) и мониторинг. Схема переживает отказ зоны, выкладки, сервера, базы, кэша, входа и ранжирования, загрузка не выше 80%, бюджет — $20 500 в месяц.",
    hint: "Серверов M — 26 в трёх зонах. База L с тремя шардами и репликой, предел ограничителя около 20 000.",
    workload: W5,
    palette: P6,
    maxNodes: 22,
    start: chat(S5),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "ml" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 8000 },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 20500 },
    ],
    solution: chat({ ...S5, app: 26, dbRepl: true, zone: true, mon: true, limiter: true, lbN: 2 }),
    show: ["app.deploy"],
  },
  {
    id: "sd24-exam",
    title: "Экзамен. Мессенджер целиком",
    statement:
      "Итоговое задание. Мессенджер в пик: 4500 чтений истории и 2500 сообщений в секунду, 600 ГБ с активными чатами (10% запросов), 320 000 соединений (6400 событий в секунду), группы по 100 участников, 22 000 запросов за вложениями, 800 ТБ файлов, вход на каждый запрос, 10% сообщений проходят антиспам. Соберите схему с нуля: кэш, база по хешу с шардами и репликой, шлюзы WebSocket, поток с уведомлениями и аналитикой, очередь и обработчики на споте, CDN и дешёвый класс хранения, вход, ранжирование, ограничитель, мониторинг, два балансировщика. Переживает отказ зоны, выкладки, сервера, базы, кэша, входа и ранжирования; загрузка не выше 80%; бюджет — $24 000 в месяц.",
    hint: "Серверов M — 30 в трёх зонах, шлюзы ws — 34, обработчиков M — 16, база L с четырьмя шардами и репликой, уведомления — 8, вход — 4, ранжирование — 5.",
    workload: { ...W5, read: 4500, write: 2500, connections: 320000, msgPerConn: 0.02, static: 22000 },
    palette: P6,
    maxNodes: 22,
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "hit", min: 0.7 },
      { k: "cdnHit", min: 0.95 },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "shardShare", max: 0.45 },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "ml" },
      { k: "has", kind: "limiter" },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "lag", max: 5 },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 24000 },
    ],
    solution: chat({ app: 30, cache: 10, dbSize: "L", dbShards: 4, dbRepl: true, queue: { workers: 16 }, ws: 34, stream: { notify: 8, analytics: 1 }, cdn: true, tier: "mix", auth: 4, ml: 5, zone: true, mon: true, limiter: true, lbN: 2 }),
    show: ["app.deploy", "worker.pricing", "blob.tier", "db.shardKey"],
  },
];
