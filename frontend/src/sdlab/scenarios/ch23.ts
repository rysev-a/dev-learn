import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 23 «Проект: доставка еды»: этапы от каталога до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  cache?: number;
  search?: { shards: number; replicas: number };
  dbSize?: string;
  dbShards?: number;
  dbRepl?: boolean;
  auth?: number;
  pay?: number;
  safe?: boolean;
  geo?: number;
  ml?: number;
  ws?: number;
  stream?: { notify: number; analytics?: number };
  zone?: boolean;
  mon?: boolean;
  limiter?: boolean;
  lbN?: number;
  cdn?: boolean;
}

const food = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    ...(o.cdn ? [N("cdn", "cdn", { ttl: 3600 })] : []),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    ...(o.limiter ? [N("limiter", "limiter", { limit: 20000 })] : []),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, ...(o.zone ? { deploy: "rolling" } : {}), ...(o.safe ? { idempotency: true, retries: 2, breaker: true } : {}) }),
    ...(o.cache ? [N("cache", "cache", { sizeGB: o.cache, ttl: 3600, replicas: 1, zone: z })] : []),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbShards ? { shards: o.dbShards } : {}), ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    N("blob", "blob"),
    ...(o.search ? [N("search", "search", o.search)] : []),
    ...(o.auth ? [N("auth", "auth", { instances: o.auth })] : []),
    ...(o.pay ? [N("pay", "pay", { instances: o.pay })] : []),
    ...(o.geo ? [N("geo", "geo", { instances: o.geo })] : []),
    ...(o.ml ? [N("ml", "ml", { instances: o.ml })] : []),
    ...(o.ws ? [N("ws", "ws", { instances: o.ws })] : []),
    ...(o.stream ? [N("stream", "stream", { partitions: 3 }), N("notify", "notify", { instances: o.stream.notify }), ...(o.stream.analytics ? [N("an", "analytics", { instances: o.stream.analytics })] : [])] : []),
    ...(o.mon ? [N("mon", "monitor")] : []),
  ];
  const edges = [
    `users>${o.cdn ? "cdn>" : ""}lb>${o.limiter ? "limiter>" : ""}app>db`,
    "app>blob",
    ...(o.cdn ? ["cdn>blob"] : []),
    ...(o.cache ? ["app>cache"] : []),
    ...(o.search ? ["app>search"] : []),
    ...(o.auth ? ["app>auth"] : []),
    ...(o.pay ? ["app>pay"] : []),
    ...(o.geo ? ["app>geo"] : []),
    ...(o.ml ? ["app>ml"] : []),
    ...(o.ws ? ["users>ws>app"] : []),
    ...(o.stream ? ["app>stream>notify", ...(o.stream.analytics ? ["stream>an"] : [])] : []),
  ];
  return S(nodes, edges);
};

const P1 = ["lb", "app", "cache", "db", "blob", "search"] as SdScenario["palette"];
const P2 = [...P1, "auth", "pay"] as SdScenario["palette"];
const P3 = [...P2, "geo", "ml"] as SdScenario["palette"];
const P4 = [...P3, "ws", "stream", "notify", "analytics"] as SdScenario["palette"];
const P5 = [...P4, "cdn", "limiter", "monitor"] as SdScenario["palette"];

const W1: Workload = WL({ read: 3000, write: 120, dataGB: 30, hotSet: 0.1, searchShare: 0.5 });
const W2: Workload = { ...W1, calls: { auth: 1, pay: 0.05 } };
const W3: Workload = { ...W2, geoUpdates: 20000, calls: { auth: 1, pay: 0.05, geo: 0.1, ml: 0.1 } };
const W4: Workload = { ...W3, connections: 120000, msgPerConn: 0.03 };

const S1: Opts = { app: 6, cache: 3, search: { shards: 1, replicas: 3 } };
const S2: Opts = { ...S1, auth: 2, pay: 2, safe: true };
const S3: Opts = { ...S2, geo: 5, ml: 3 };
const S4: Opts = { ...S3, app: 13, ws: 11, stream: { notify: 4, analytics: 1 } };

export const CH23: SdScenario[] = [
  {
    id: "sd23-s1-catalog",
    title: "Этап 1. Каталог ресторанов",
    statement:
      "Каталог: 3000 открытий в секунду, половина из них — поиск ресторанов рядом по кухне и адресу, остальное — карточки и меню. Добавьте поисковый индекс и кэш меню (≥85%, рабочий набор 3 ГБ). Поиск и всё остальное — не выше 80%, схема переживает отказ реплики поиска, бюджет — $1800 в месяц.",
    hint: "Поиск: 1 шард × 3 реплики (1500 запросов в секунду; после отказа одной остаётся 2400). Кэш 3 ГБ с TTL 3600. Серверов M — 6.",
    workload: W1,
    palette: P1,
    start: food({ app: 5 }),
    goals: [
      { k: "link", from: "app", to: "search" },
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "search" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1800 },
    ],
    solution: food(S1),
  },
  {
    id: "sd23-s2-order",
    title: "Этап 2. Заказ и оплата",
    statement:
      "Оформление заказа: каждый запрос проверяет вход, а 5% обращаются к платёжному шлюзу. Подключите сервис входа (2 экземпляра) и платёжный шлюз с двумя каналами; защитите платежи: ключи идемпотентности, повторы и автомат разрыва. Схема переживает отказ входа и платёжного канала, бюджет — $2200 в месяц.",
    hint: "Сервер → вход и шлюз. В приложении включите «Ключи идемпотентности», «Повторы к БД» ≥ 1 и «Автомат разрыва». Вход ×2: после отказа остаётся 4000 при нагрузке 3100.",
    workload: W2,
    palette: P2,
    start: food(S1),
    goals: [
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "pay" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "pay" },
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 2200 },
    ],
    solution: food(S2),
    show: ["app.idempotency", "app.retries", "app.breaker"],
  },
  {
    id: "sd23-s3-couriers",
    title: "Этап 3. Курьеры и время доставки",
    statement:
      "Добавлены курьеры: 20 000 обновлений позиций в секунду, 10% запросов подбирают курьера в геосервисе, ещё 10% оценивают время доставки моделью. Подключите геосервис и сервис ранжирования: загрузка не выше 80%, схема переживает отказ обоих, бюджет — $3200 в месяц.",
    hint: "Геосервис: 5 экземпляров (30 000; после отказа одного — 24 000). Ранжирование: 3 экземпляра (900; после отказа — 600 при нагрузке 312).",
    workload: W3,
    palette: P3,
    start: food(S2),
    goals: [
      { k: "link", from: "app", to: "geo" },
      { k: "link", from: "app", to: "ml" },
      { k: "util", kind: "geo", max: 0.8 },
      { k: "util", kind: "ml", max: 0.8 },
      { k: "survive", fail: "geo" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3200 },
    ],
    solution: food(S3),
  },
  {
    id: "sd23-s4-tracking",
    title: "Этап 4. Отслеживание и события",
    statement:
      "Клиенты следят за заказом: 120 000 соединений получают по 0,03 события в секунду (3600 в секунду). Поставьте шлюзы WebSocket, пропустите события через поток и подключите уведомления и аналитику (спрос и время приготовления): шлюзы и потребители — не выше 80%, бюджет — $5200 в месяц.",
    hint: "Шлюзов ws — 11 (120 000 / 15 000 = 8 при 73%). Серверов M — 13 (принимают и события). Уведомления — 4 экземпляра.",
    workload: W4,
    palette: P4,
    start: food(S3),
    goals: [
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "util", kind: "ws", max: 0.8 },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 5200 },
    ],
    solution: food(S4),
    maxNodes: 18,
  },
  {
    id: "sd23-s5-reliability",
    title: "Этап 5. Надёжность и пики",
    statement:
      "К обеденному пику сервис должен быть готов. Разнесите серверы и базу по зонам, добавьте реплику базы с автопереключением, CDN для картинок меню, ограничитель на входе (предел не меньше нагрузки 6700), второй балансировщик и мониторинг. Схема переживает отказ зоны, выкладки, сервера, базы, кэша и поиска, загрузка не выше 80%, бюджет — $7000 в месяц.",
    hint: "Серверов M — 18 в трёх зонах (после потери зоны остаётся 12 — 8400 при нагрузке 6700). База L с репликой, предел ограничителя около 20 000.",
    workload: W4,
    palette: P5,
    maxNodes: 20,
    start: food(S4),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "search" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 6700 },
      { k: "has", kind: "monitor" },
      { k: "has", kind: "cdn" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 7000 },
    ],
    solution: food({ ...S4, app: 18, dbSize: "L", dbRepl: true, zone: true, mon: true, limiter: true, lbN: 2, cdn: true }),
    show: ["app.deploy"],
  },
  {
    id: "sd23-exam",
    title: "Экзамен. Доставка еды целиком",
    statement:
      "Итоговое задание. Обеденный пик крупного города: 9000 открытий каталога (половина — поиск) и 600 заказов в секунду, 40 000 обновлений позиций курьеров, 200 000 соединений для слежения за заказами (6000 событий в секунду); 10% запросов подбирают курьера, 10% оценивают время, 5% идут в платёжный шлюз, каждый проверяет вход. Соберите схему с нуля: поиск, кэш меню, вход, платёжный шлюз (2 канала), геосервис, ранжирование, поток с уведомлениями и аналитикой, шлюзы WebSocket, CDN, база с репликой, ограничитель, мониторинг, два балансировщика и защита платежей. Переживает отказ зоны, выкладки, сервера, базы, кэша, поиска, входа, платёжного канала, геосервиса и ранжирования; загрузка не выше 80%; бюджет — $12 500 в месяц.",
    hint: "Серверов M — 35 в трёх зонах, поиск 1×5 (4500 запросов в секунду), геосервис 10, ранжирование 5, вход 4, шлюзы ws 18, уведомления 7, аналитика 2, база L с репликой.",
    workload: { ...W4, read: 9000, write: 600, geoUpdates: 40000, connections: 200000, msgPerConn: 0.03, hotSet: 0.1 },
    palette: P5,
    maxNodes: 20,
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "hit", min: 0.85 },
      { k: "link", from: "app", to: "search" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "pay" },
      { k: "link", from: "app", to: "geo" },
      { k: "link", from: "app", to: "ml" },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "has", kind: "cdn" },
      { k: "has", kind: "limiter" },
      { k: "has", kind: "monitor" },
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "noSpof", kinds: ["lb"] },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "search" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "pay" },
      { k: "survive", fail: "geo" },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 12500 },
    ],
    solution: food({ app: 35, cache: 3, search: { shards: 1, replicas: 5 }, auth: 4, pay: 2, safe: true, geo: 10, ml: 5, ws: 18, stream: { notify: 7, analytics: 2 }, dbSize: "L", dbRepl: true, zone: true, mon: true, limiter: true, lbN: 2, cdn: true }),
    show: ["app.deploy", "app.idempotency", "app.retries", "app.breaker"],
  },
];
