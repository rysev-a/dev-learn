import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 21 «Проект: сервис такси»: этапы от MVP до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  geo: number;
  auth?: number;
  ml?: number;
  pay?: number;
  ws?: number;
  stream?: { notify: number; analytics?: number };
  dbSize?: string;
  dbShards?: number;
  dbRepl?: boolean;
  safe?: boolean; // идемпотентность, повторы и автомат разрыва у приложения
  zone?: boolean;
  mon?: boolean;
  limiter?: boolean;
  lbN?: number;
}

const taxi = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    ...(o.limiter ? [N("limiter", "limiter", { limit: 20000 })] : []),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, ...(o.zone ? { deploy: "rolling" } : {}), ...(o.safe ? { idempotency: true, retries: 2, breaker: true } : {}) }),
    N("geo", "geo", { instances: o.geo }),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbShards ? { shards: o.dbShards } : {}), ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    ...(o.auth ? [N("auth", "auth", { instances: o.auth })] : []),
    ...(o.ml ? [N("ml", "ml", { instances: o.ml })] : []),
    ...(o.pay ? [N("pay", "pay", { instances: o.pay })] : []),
    ...(o.ws ? [N("ws", "ws", { instances: o.ws })] : []),
    ...(o.stream ? [N("stream", "stream", { partitions: 3 }), N("notify", "notify", { instances: o.stream.notify }), ...(o.stream.analytics ? [N("an", "analytics", { instances: o.stream.analytics })] : [])] : []),
    ...(o.mon ? [N("mon", "monitor")] : []),
  ];
  const edges = [
    `users>lb>${o.limiter ? "limiter>" : ""}app>db`,
    "app>geo",
    ...(o.auth ? ["app>auth"] : []),
    ...(o.ml ? ["app>ml"] : []),
    ...(o.pay ? ["app>pay"] : []),
    ...(o.ws ? ["users>ws>app"] : []),
    ...(o.stream ? ["app>stream>notify", ...(o.stream.analytics ? ["stream>an"] : [])] : []),
  ];
  return S(nodes, edges);
};

const P1 = ["lb", "app", "db", "geo"] as SdScenario["palette"];
const P2 = [...P1, "auth"] as SdScenario["palette"];
const P3 = [...P2, "ml"] as SdScenario["palette"];
const P4 = [...P3, "ws", "stream", "notify", "analytics"] as SdScenario["palette"];
const P5 = [...P4, "pay"] as SdScenario["palette"];
const P6 = [...P5, "limiter", "monitor"] as SdScenario["palette"];

const W1: Workload = WL({ read: 300, write: 60, dataGB: 20, geoUpdates: 800, calls: { geo: 0.5 } });
const W2: Workload = WL({ read: 3000, write: 500, dataGB: 100, geoUpdates: 20000, calls: { geo: 0.5, auth: 1 } });
const W3: Workload = { ...W2, calls: { geo: 0.5, auth: 1, ml: 0.25 } };
const W4: Workload = { ...W3, connections: 150000, msgPerConn: 0.02 };
const W5: Workload = { ...W4, calls: { geo: 0.5, auth: 1, ml: 0.25, pay: 0.04 } };

const S2: Opts = { app: 7, geo: 5, auth: 2, dbSize: "L" };
const S3: Opts = { ...S2, ml: 4 };
const S4: Opts = { ...S3, app: 12, ws: 13, stream: { notify: 4, analytics: 1 } };
const S5: Opts = { ...S4, pay: 2, safe: true };

export const CH21: SdScenario[] = [
  {
    id: "sd21-s1-mvp",
    title: "Этап 1. Первая версия и геосервис",
    statement:
      "Сервис такси стартует: 300 чтений и 60 заказов в секунду, а 800 водителей присылают позицию каждые несколько секунд. Половина запросов — поиск ближайших водителей. Сохраните заказы в базе, а позиции и поиск отдайте геосервису: свяжите сервер с геосервисом. Загрузка не выше 80%, бюджет — $350 в месяц.",
    hint: "Позиции пишутся не в базу, а в геосервис в памяти (6000 обновлений в секунду на экземпляр). Сервер → геосервис.",
    workload: W1,
    palette: P1,
    start: S([users(), N("app", "app", { size: "M" }), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "link", from: "app", to: "geo" },
      { k: "util", kind: "geo", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 350 },
    ],
    solution: S([users(), N("app", "app", { size: "M" }), N("db", "db"), N("geo", "geo")], ["users>app>db", "app>geo"]),
  },
  {
    id: "sd21-s2-geo",
    title: "Этап 2. Поток позиций",
    statement:
      "Город вырос: 3000 чтений и 500 заказов в секунду, 20 000 обновлений позиций в секунду, каждый запрос проверяет сервис входа. Масштабируйте геосервис и добавьте сервис входа: загрузка не выше 80%, схема переживает отказ геосервиса и сервиса входа, база L (записи поездок), бюджет — $2400 в месяц.",
    hint: "Геосервис: 5 экземпляров (30 000; после отказа одного остаётся 24 000 при нагрузке 21 750). Вход: 2 экземпляра. Серверов M — 7, база L.",
    workload: W2,
    palette: P2,
    start: taxi({ app: 3, geo: 1, dbSize: "L" }),
    goals: [
      { k: "link", from: "app", to: "auth" },
      { k: "util", kind: "geo", max: 0.8 },
      { k: "survive", fail: "geo" },
      { k: "survive", fail: "auth" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 2400 },
    ],
    solution: taxi(S2),
  },
  {
    id: "sd21-s3-eta",
    title: "Этап 3. Время подъезда",
    statement:
      "Подбор водителя оценивает время подъезда моделью: она вызывается на 25% запросов (около 875 в секунду), а один экземпляр тянет 300. Подключите сервис ранжирования: загрузка не выше 80%, схема переживает отказ ранжирования, бюджет — $3200 в месяц.",
    hint: "Четыре экземпляра ранжирования: 1200 запросов в секунду, после отказа одного остаётся 900.",
    workload: W3,
    palette: P3,
    start: taxi(S2),
    goals: [
      { k: "link", from: "app", to: "ml" },
      { k: "util", kind: "ml", max: 0.8 },
      { k: "survive", fail: "ml" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3200 },
    ],
    solution: taxi(S3),
  },
  {
    id: "sd21-s4-tracking",
    title: "Этап 4. Отслеживание и события",
    statement:
      "Пассажиры видят машину на карте: 150 000 соединений получают по 0,02 обновления в секунду (3000 в секунду). Поставьте шлюзы WebSocket, пропустите события через поток и подключите уведомления и аналитику (спрос для цены): шлюзы, серверы и потребители — не выше 80%, бюджет — $5600 в месяц.",
    hint: "Шлюзов ws — 13 (150 000 / 15 000 = 10 при 77%). Серверов M теперь 12 (принимают и обновления). Уведомления — 4 экземпляра (3500 событий), аналитика — 1.",
    workload: W4,
    palette: P4,
    start: taxi(S3),
    goals: [
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "util", kind: "ws", max: 0.8 },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 5600 },
    ],
    solution: taxi(S4),
  },
  {
    id: "sd21-s5-pay",
    title: "Этап 5. Платежи",
    statement:
      "Добавлены платежи: 4% запросов обращаются к внешнему платёжному шлюзу (180 мс, один канал тянет 400). Подключите шлюз с двумя каналами (отказ одного не должен останавливать оплату) и защитите платежи: ключи идемпотентности, повторы и автомат разрыва в приложении. Схема переживает отказ платёжного канала, бюджет — $5700 в месяц.",
    hint: "Сервер → платёжный шлюз, каналов — 2. В приложении включите «Ключи идемпотентности», «Повторы к БД» — не меньше 1, «Автомат разрыва».",
    workload: W5,
    palette: P5,
    start: taxi(S4),
    goals: [
      { k: "link", from: "app", to: "pay" },
      { k: "survive", fail: "pay" },
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "retries", op: ">=", value: 1 },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 5700 },
    ],
    solution: taxi(S5),
    show: ["app.idempotency", "app.retries", "app.breaker"],
  },
  {
    id: "sd21-s6-reliability",
    title: "Этап 6. Надёжность и пики",
    statement:
      "Сервис критичен: пассажир под дождём ждать не будет. Разнесите серверы и базу по зонам, включите rolling-выкладку, добавьте реплику базы с автопереключением, второй балансировщик, ограничитель на входе (предел не меньше нагрузки 6500) и мониторинг. Схема переживает отказ зоны, выкладки, сервера, базы, геосервиса, ранжирования, сервиса входа и платёжного канала; загрузка не выше 80%; бюджет — $7000 в месяц.",
    hint: "Серверов M — 16 в трёх зонах (после потери зоны остаётся 10 — 7000 при нагрузке 6500). Предел ограничителя около 20 000. База L с репликой и автопереключением.",
    workload: W5,
    palette: P6,
    maxNodes: 18,
    start: taxi(S5),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "geo" },
      { k: "survive", fail: "ml" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "pay" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 6500 },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 7000 },
    ],
    solution: taxi({ ...S5, app: 16, dbRepl: true, zone: true, mon: true, limiter: true, lbN: 2 }),
    show: ["app.deploy", "app.idempotency", "app.retries", "app.breaker"],
  },
  {
    id: "sd21-exam",
    title: "Экзамен. Сервис такси целиком",
    statement:
      "Итоговое задание. Крупный город в пик: 6000 чтений и 1000 заказов в секунду, 60 000 обновлений позиций, 300 000 соединений для отслеживания (3000 сигналов в секунду); половина запросов идёт в геосервис, 25% — в ранжирование, 4% — в платёжный шлюз, каждый проверяет вход. Соберите схему с нуля: геосервис, ранжирование, сервис входа, платёжный шлюз (2 канала), поток событий с уведомлениями и аналитикой, шлюзы WebSocket, база L с шардами и репликой, ограничитель, мониторинг, два балансировщика, защита платежей. Переживает отказ зоны, выкладки, сервера, базы, геосервиса, ранжирования, входа и платёжного канала; загрузка не выше 80%; бюджет — $13 000 в месяц.",
    hint: "Серверов M — 23 в трёх зонах, геосервис 14, ранжирование 8, вход 3, шлюзы ws 26, уведомления 4; база L с двумя шардами и репликой.",
    workload: { ...W5, read: 6000, write: 1000, geoUpdates: 60000, connections: 300000, msgPerConn: 0.01, dataGB: 300 },
    palette: P6,
    maxNodes: 18,
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "link", from: "app", to: "geo" },
      { k: "link", from: "app", to: "ml" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "pay" },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "stream", to: "analytics" },
      { k: "param", kind: "app", key: "idempotency", op: "==", value: true },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "has", kind: "limiter" },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "geo" },
      { k: "survive", fail: "ml" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "pay" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 13000 },
    ],
    solution: taxi({ app: 23, geo: 14, auth: 3, ml: 8, pay: 2, ws: 26, stream: { notify: 4, analytics: 1 }, dbSize: "L", dbShards: 2, dbRepl: true, safe: true, zone: true, mon: true, limiter: true, lbN: 2 }),
    show: ["app.deploy", "app.idempotency", "app.retries", "app.breaker"],
  },
];
