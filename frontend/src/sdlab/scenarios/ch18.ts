import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState } from "../types.ts";

/* Глава 18 «Итоговый проект»: сервис коротких видео собирается по этапам — от MVP до экзамена.
   Каждый этап начинается со схемы предыдущего этапа и добавляет новое требование. */

type P = Record<string, number | string | boolean>;
const lb = (n = 2) => N("lb", "lb", { instances: n });
const app = (n: number, extra: P = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", ...extra });
const cache = (gb: number, extra: P = {}) => N("cache", "cache", { sizeGB: gb, ttl: 3600, ...extra });
const db = (extra: P = {}) => N("db", "db", { size: "M", ...extra });

/* этап 2: баланс, кэш, реплики */
const stage2 = (): SdState =>
  S([users(), lb(), app(5), cache(5, { replicas: 1 }), db({ replicas: 1, failover: true })], ["users>lb>app>db", "app>cache"]);
/* этап 3: CDN и хранилище */
const stage3 = (): SdState =>
  S(
    [users(), N("cdn", "cdn", { ttl: 300 }), lb(), app(5), cache(5, { replicas: 1 }), N("blob", "blob"), db({ replicas: 1, failover: true })],
    ["users>cdn>lb>app>db", "app>cache", "cdn>blob"],
  );
/* этап 4: очередь и обработчики */
const stage4 = (): SdState =>
  S(
    [
      users(),
      N("cdn", "cdn", { ttl: 300 }),
      lb(),
      app(5),
      cache(5, { replicas: 1 }),
      N("blob", "blob"),
      N("queue", "queue"),
      N("worker", "worker", { size: "M", instances: 2, idempotent: true, pricing: "spot" }),
      db({ replicas: 1, failover: true }),
    ],
    ["users>cdn>lb>app>db", "app>cache", "cdn>blob", "app>queue>worker>db"],
  );
/* этап 5: лента и поиск */
const stage5 = (): SdState =>
  S(
    [
      users(),
      N("cdn", "cdn", { ttl: 300 }),
      lb(),
      app(5, { feed: "hybrid" }),
      cache(8, { replicas: 1 }),
      N("search", "search", { shards: 4, replicas: 2 }),
      N("blob", "blob"),
      N("queue", "queue"),
      N("worker", "worker", { size: "M", instances: 2, idempotent: true, pricing: "spot" }),
      db({ size: "L", replicas: 1, failover: true }),
    ],
    ["users>cdn>lb>app>db", "app>cache", "app>search", "cdn>blob", "app>queue>worker>db"],
  );
/* этап 6: зоны, защита, мониторинг */
const stage6 = (): SdState =>
  S(
    [
      users(),
      N("cdn", "cdn", { ttl: 300 }),
      lb(),
      N("limiter", "limiter", { limit: 4000 }),
      app(9, { feed: "hybrid", zone: "multi", retries: 1, breaker: true, deploy: "rolling" }),
      cache(8, { replicas: 1, zone: "multi" }),
      N("search", "search", { shards: 4, replicas: 2 }),
      N("blob", "blob"),
      N("queue", "queue"),
      N("worker", "worker", { size: "M", instances: 3, idempotent: true, pricing: "spot", zone: "multi" }),
      db({ size: "L", replicas: 1, failover: true, zone: "multi" }),
      N("mon", "monitor"),
    ],
    ["users>cdn>lb>limiter>app>db", "app>cache", "app>search", "cdn>blob", "app>queue>worker>db"],
  );

/* то же, но серверы приложения — на резервном тарифе */
const withPricing = (st: SdState): SdState => ({
  ...st,
  nodes: st.nodes.map((n) => (n.kind === "app" ? { ...n, params: { ...n.params, pricing: "reserved" } } : n)),
});

const W2 = WL({ read: 2500, write: 300, dataGB: 100, hotSet: 0.05 });
const W3 = WL({ static: 30000, read: 2500, write: 300, dataGB: 100, hotSet: 0.05 });
const W4 = WL({ static: 30000, read: 2500, write: 300, dataGB: 100, hotSet: 0.05, spikeSec: 10 });
const W5 = WL({ static: 30000, read: 2500, write: 300, dataGB: 160, hotSet: 0.05, spikeSec: 10, searchShare: 0.15, fanout: 100 });

export const CH18: SdScenario[] = [
  {
    id: "sd18-s1-mvp",
    title: "Этап 1. MVP",
    statement:
      "Сервис коротких видео стартует: 250 чтений и 30 записей метаданных в секунду. Соберите простейшую схему — пользователи, сервер приложения, база данных — и подберите размеры, чтобы загрузка не превышала 80%, а стоимость — $250 в месяц.",
    hint: "Сервер S тянет 300 запросов (280 — 93%): нужен M. База S подойдёт: 250 чтений и 30 записей — 40%.",
    workload: WL({ read: 250, write: 30, dataGB: 20, hotSet: 0.1 }),
    palette: ["app", "db"],
    start: S([users(), N("app", "app"), N("db", "db")]),
    goals: [
      { k: "link", from: "clients", to: "app" },
      { k: "link", from: "app", to: "db" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 250 },
    ],
    solution: S([users(), N("app", "app", { size: "M" }), N("db", "db")], ["users>app>db"]),
  },
  {
    id: "sd18-s2-growth",
    title: "Этап 2. Рост в десять раз",
    statement:
      "Нагрузка выросла: 2500 чтений и 300 записей в секунду, рабочий набор — 5 ГБ. Усильте схему: балансировщик, несколько серверов, кэш метаданных (≥85%) и реплика базы с автопереключением. Схема переживает отказ базы, кэша и сервера, загрузка не выше 80%, бюджет — $1400 в месяц.",
    hint: "Пять серверов M; кэш 5 ГБ с TTL 3600 и репликой; база M (записей 300 — для S много) с репликой и автопереключением.",
    workload: W2,
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), N("app", "app", { size: "M" }), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 1400 },
    ],
    solution: stage2(),
  },
  {
    id: "sd18-s3-media",
    title: "Этап 3. Видео и CDN",
    statement:
      "Пользователи начали смотреть ролики: 30 000 запросов в секунду за файлами. Вынесите их в объектное хранилище и поставьте CDN (≥90% статики) перед ним. Серверы приложения должны остаться на метаданных, загрузка — не выше 80%, схема остаётся устойчивой, бюджет — $1500 в месяц.",
    hint: "CDN → хранилище (статика мимо серверов); динамику CDN передаёт балансировщику. Остальное — как на втором этапе.",
    workload: W3,
    palette: ["cdn", "lb", "app", "cache", "blob", "db"],
    start: stage2(),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "cost", max: 1500 },
    ],
    solution: stage3(),
  },
  {
    id: "sd18-s4-transcode",
    title: "Этап 4. Перекодирование через очередь",
    statement:
      "Ролики нужно перекодировать после загрузки. Добавьте очередь и идемпотентных обработчиков на споте (не меньше двух): после пика в 10 секунд очередь разбирается без отставания (допустимо 5 с), база и серверы не выше 80%, бюджет — $1600 в месяц.",
    hint: "Сервер → очередь → обработчики → база. Два обработчика M на споте тянут 800 записей в секунду при нагрузке 300.",
    workload: W4,
    palette: ["cdn", "lb", "app", "cache", "blob", "queue", "worker", "db"],
    start: stage3(),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "link", from: "worker", to: "db" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "noSpof", kinds: ["worker"] },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1600 },
    ],
    solution: stage4(),
    show: ["worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd18-s5-feed-search",
    title: "Этап 5. Лента и поиск",
    statement:
      "Добавлены лента подписок (в среднем 100 подписчиков у автора) и поиск по названиям (15% чтений, индекс 160 ГБ). Выберите гибридную ленту, добавьте поисковый кластер (шарды по объёму, две реплики) и расширьте кэш до рабочего набора (8 ГБ, ≥85%). Схема переживает отказ базы и поиска, всё — не выше 80%, бюджет $3500 в месяц.",
    hint: "Лента — «гибрид» у сервера. Поиск: четыре шарда, две реплики (160 / 40 = 4). Кэш 8 ГБ с репликой. Гибридная лента удваивает записи, поэтому базе M уже тесно — нужна L.",
    workload: W5,
    palette: ["cdn", "lb", "app", "cache", "search", "blob", "queue", "worker", "db"],
    start: stage4(),
    goals: [
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "link", from: "app", to: "search" },
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "search" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3500 },
    ],
    solution: stage5(),
    show: ["app.feed", "worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd18-s6-reliability",
    title: "Этап 6. Зоны и защита",
    statement:
      "Сервис стал критичным: нужно пережить отказ зоны, выкладки и сервера. Разнесите серверы, кэш, обработчиков и базу по трём зонам, включите rolling-выкладку, автомат разрыва, поставьте ограничитель на входе (предел не меньше обычной нагрузки 2800) и мониторинг. Загрузка не выше 80%, бюджет — $4200 в месяц.",
    hint: "Серверов M — девять в трёх зонах (после потери зоны шесть — 4200). Ограничитель между балансировщиком и серверами; мониторинг на схему.",
    workload: W5,
    palette: ["cdn", "lb", "limiter", "app", "cache", "search", "blob", "queue", "worker", "db", "monitor"],
    start: stage5(),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 2800 },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 4200 },
    ],
    solution: stage6(),
    show: ["app.feed", "app.retries", "app.breaker", "app.deploy", "worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd18-s7-cost",
    title: "Этап 7. Сократить счёт",
    statement:
      "Счёт растёт, а нагрузка стабильна: серверы приложения нужны круглые сутки. Переведите их на резервный тариф (скидка около 40%), сохранив все цели надёжности: схема переживает отказ зоны, выкладки, сервера, базы и поиска, загрузка не выше 80%, бюджет — $3700 в месяц.",
    hint: "Параметр «Тариф» сервера приложения — «резерв». Остальное не трогайте: надёжность важнее экономии на ней.",
    workload: W5,
    palette: ["cdn", "lb", "limiter", "app", "cache", "search", "blob", "queue", "worker", "db", "monitor"],
    start: stage6(),
    goals: [
      { k: "param", kind: "app", key: "pricing", op: "==", value: "reserved" },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "search" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3700 },
    ],
    solution: withPricing(stage6()),
    show: ["app.pricing", "app.feed", "app.retries", "app.breaker", "app.deploy", "worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd18-exam",
    title: "Экзамен. Итоговая схема",
    statement:
      "Итоговое задание. Сервис в полной силе: 45 000 запросов в секунду за файлами, 3800 чтений и 450 записей в секунду, лента подписок (100 подписчиков у автора), поиск (15% чтений, индекс 240 ГБ), рабочий набор 10 ГБ. Соберите схему с нуля: CDN (≥90%) → хранилище; балансировщики (два), ограничитель (предел от 4300), серверы с rolling-выкладкой, автоматом разрыва и гибридной лентой; кэш (≥85%) с репликой; очередь с идемпотентными обработчиками на споте; поиск (шарды по объёму, две реплики); база с репликой и автопереключением; мониторинг. Схема переживает отказ зоны, выкладки, сервера, базы, кэша и поиска; доступность ≥ 99,9%, p99 ≤ 160 мс, загрузка не выше 80%, бюджет — $4700 в месяц.",
    hint: "Серверов M — одиннадцать в трёх зонах, резервный тариф; кэш 10 ГБ с репликой в трёх зонах; поиск 6 шардов × 2 реплики; три обработчика M на споте; база L с репликой в трёх зонах; всё остальное — по этапам предыдущих упражнений.",
    workload: WL({ static: 45000, read: 3800, write: 450, dataGB: 240, hotSet: 0.04, spikeSec: 10, searchShare: 0.15, fanout: 100 }),
    palette: ["cdn", "lb", "limiter", "app", "cache", "search", "blob", "queue", "worker", "db", "monitor"],
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    maxNodes: 16,
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "hit", min: 0.85 },
      { k: "has", kind: "limiter" },
      { k: "param", kind: "limiter", key: "limit", op: ">=", value: 4300 },
      { k: "param", kind: "app", key: "feed", op: "==", value: "hybrid" },
      { k: "param", kind: "app", key: "breaker", op: "==", value: true },
      { k: "link", from: "app", to: "queue" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "link", from: "app", to: "search" },
      { k: "has", kind: "monitor" },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "search" },
      { k: "availability", min: 0.999 },
      { k: "p99", max: 160 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 4700 },
    ],
    solution: S(
      [
        users(),
        N("cdn", "cdn", { ttl: 300 }),
        lb(),
        N("limiter", "limiter", { limit: 6000 }),
        app(11, { feed: "hybrid", zone: "multi", retries: 1, breaker: true, deploy: "rolling", pricing: "reserved" }),
        cache(10, { replicas: 1, zone: "multi" }),
        N("search", "search", { shards: 6, replicas: 2 }),
        N("blob", "blob"),
        N("queue", "queue"),
        N("worker", "worker", { size: "M", instances: 3, idempotent: true, pricing: "spot", zone: "multi" }),
        db({ size: "L", replicas: 1, failover: true, zone: "multi" }),
        N("mon", "monitor"),
      ],
      ["users>cdn>lb>limiter>app>db", "app>cache", "app>search", "cdn>blob", "app>queue>worker>db"],
    ),
    show: ["app.pricing", "app.feed", "app.retries", "app.breaker", "app.deploy", "worker.pricing", "worker.idempotent"],
  },
];
