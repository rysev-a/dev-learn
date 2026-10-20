import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario, SdState, Workload } from "../types.ts";

/* Глава 19 «Проект: облачный диск»: этапы от MVP до экзамена. Схема каждого этапа — стартовая для следующего. */

interface Opts {
  app: number;
  cdn?: boolean;
  cache?: number;
  dbRepl?: boolean;
  ws?: number;
  stream?: boolean;
  notify?: number;
  auth?: number;
  search?: { shards: number; replicas: number };
  tier?: string;
  zone?: boolean;
  mon?: boolean;
  lbN?: number;
  dbSize?: string;
}

const drive = (o: Opts): SdState => {
  const z = o.zone ? "multi" : "single";
  const nodes = [
    users(),
    ...(o.cdn ? [N("cdn", "cdn", { ttl: 300 })] : []),
    N("lb", "lb", { instances: o.lbN ?? 1 }),
    N("app", "app", { size: "M", instances: o.app, sessions: "external", zone: z, ...(o.zone ? { deploy: "rolling" } : {}) }),
    ...(o.cache ? [N("cache", "cache", { sizeGB: o.cache, ttl: 3600, replicas: 1, zone: z })] : []),
    N("db", "db", { size: o.dbSize ?? "M", ...(o.dbRepl ? { replicas: 1, failover: true } : {}), zone: z }),
    N("blob", "blob", { tier: o.tier ?? "hot" }),
    ...(o.ws ? [N("ws", "ws", { instances: o.ws })] : []),
    ...(o.stream ? [N("stream", "stream", { partitions: 3 })] : []),
    ...(o.notify ? [N("notify", "notify", { instances: o.notify })] : []),
    ...(o.auth ? [N("auth", "auth", { instances: o.auth })] : []),
    ...(o.search ? [N("search", "search", o.search)] : []),
    ...(o.mon ? [N("mon", "monitor")] : []),
  ];
  const edges = [
    o.cdn ? "users>cdn>lb>app>db" : "users>lb>app>db",
    "app>blob",
    ...(o.cdn ? ["cdn>blob"] : []),
    ...(o.cache ? ["app>cache"] : []),
    ...(o.ws ? ["users>ws>app"] : []),
    ...(o.stream ? ["app>stream"] : []),
    ...(o.notify ? ["stream>notify"] : []),
    ...(o.auth ? ["app>auth"] : []),
    ...(o.search ? ["app>search"] : []),
  ];
  return S(nodes, edges);
};

const PAL = ["cdn", "lb", "app", "cache", "db", "blob", "ws", "stream", "notify", "auth", "search", "monitor"] as const;
const palette = (...extra: string[]) => [...PAL].filter((k) => !["ws", "stream", "notify", "auth", "search", "monitor", "cdn", "cache"].includes(k) || extra.includes(k)) as SdScenario["palette"];

const W1: Workload = WL({ static: 120, read: 200, write: 30, dataGB: 5, mediaTB: 2 });
const W2: Workload = WL({ static: 1200, read: 2400, write: 300, dataGB: 80, hotSet: 0.05, mediaTB: 40 });
const W3: Workload = { ...W2, static: 15000 };
const W4: Workload = { ...W3, connections: 150000, msgPerConn: 0.02 };
const W5: Workload = { ...W4, calls: { auth: 1 }, searchShare: 0.1 };
const W6: Workload = { ...W5, mediaTB: 900 };

export const CH19: SdScenario[] = [
  {
    id: "sd19-s1-mvp",
    title: "Этап 1. Первая версия",
    statement:
      "Облачный диск стартует: 200 чтений и 30 записей метаданных в секунду, 120 скачиваний файлов в секунду, 2 ТБ файлов. Добавьте объектное хранилище для содержимого файлов и свяжите его с сервером приложения: метаданные — в базе, байты — в хранилище. Загрузка не выше 80%, стоимость не больше $350 в месяц.",
    hint: "База хранит имена и права, хранилище — блоки файлов. Сервер → хранилище: файлы идут мимо базы. Хранилище стоит $25 плюс $23 за ТБ.",
    workload: W1,
    palette: palette(),
    start: S([users(), N("app", "app", { size: "M" }), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "has", kind: "blob" },
      { k: "link", from: "app", to: "blob" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 350 },
    ],
    solution: S([users(), N("app", "app", { size: "M" }), N("db", "db"), N("blob", "blob")], ["users>app>db", "app>blob"]),
  },
  {
    id: "sd19-s2-growth",
    title: "Этап 2. Рост и метаданные",
    statement:
      "Пользователей стало в десять раз больше: 2400 чтений и 300 записей метаданных в секунду, 40 ТБ файлов. Усильте метаданные: балансировщик, несколько серверов, кэш листингов папок (≥85%, рабочий набор 4 ГБ), база с репликой и автопереключением. Схема переживает отказ базы и кэша, загрузка не выше 80%, бюджет — $2500 в месяц.",
    hint: "Пять серверов M, кэш 4 ГБ с репликой и TTL 3600, база M с репликой и автопереключением. Основные деньги уходят на хранение: 40 ТБ × $23.",
    workload: W2,
    palette: palette("cache"),
    start: S([users(), N("app", "app", { size: "M" }), N("db", "db"), N("blob", "blob")], ["users>app>db", "app>blob"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "cost", max: 2500 },
    ],
    solution: drive({ app: 5, cache: 4, dbRepl: true }),
  },
  {
    id: "sd19-s3-cdn",
    title: "Этап 3. Скачивания через CDN",
    statement:
      "Скачиваний стало 15 000 в секунду. Каждое идёт через хранилище с задержкой 45 мс. Поставьте CDN перед хранилищем (≥90% попаданий) и добейтесь средней задержки не больше 40 мс. Остальное — как на втором этапе, бюджет $2500 в месяц.",
    hint: "CDN → хранилище; динамику (метаданные) CDN передаёт балансировщику. Блоки неизменны, поэтому TTL 300 с и больше даёт 90% и выше.",
    workload: W3,
    palette: palette("cache", "cdn"),
    start: drive({ app: 5, cache: 4, dbRepl: true }),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "p50", max: 40 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 2500 },
    ],
    solution: drive({ app: 5, cache: 4, dbRepl: true, cdn: true }),
  },
  {
    id: "sd19-s4-sync",
    title: "Этап 4. Синхронизация устройств",
    statement:
      "Добавлена синхронизация: 150 000 клиентов держат соединение и получают сигналы об изменениях (0,02 сигнала в секунду на клиента — 3000 в секунду). Поставьте шлюзы WebSocket, пропустите изменения через поток событий и подключите уведомления: шлюзы, серверы и уведомления загружены не выше 80%, бюджет — $4700 в месяц.",
    hint: "Шлюзы ws — около 14 (150 000 / 15 000 = 10 при 71%). Сервер приложения принимает и сигналы: около одиннадцати M. Поток событий с тремя партициями, уведомления — три экземпляра.",
    workload: W4,
    palette: palette("cache", "cdn", "ws", "stream", "notify"),
    start: drive({ app: 5, cache: 4, dbRepl: true, cdn: true }),
    goals: [
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "util", kind: "ws", max: 0.8 },
      { k: "util", kind: "app", max: 0.8 },
      { k: "util", kind: "notify", max: 0.8 },
      { k: "cost", max: 4700 },
    ],
    solution: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3 }),
  },
  {
    id: "sd19-s5-share",
    title: "Этап 5. Права и поиск",
    statement:
      "Добавлены общий доступ и поиск: каждый запрос проверяет права в сервисе входа, а 10% чтений — поиск по файлам (индекс 80 ГБ). Подключите сервис входа (не больше 80% загрузки, переживает отказ) и поисковый кластер (шарды по объёму, две реплики, переживает отказ). Бюджет — $5600 в месяц.",
    hint: "Сервис входа: три экземпляра (по 4000 запросов в секунду; после отказа одного остаётся 8000 при нагрузке около 6000). Поиск: 2 шарда × 2 реплики.",
    workload: W5,
    palette: palette("cache", "cdn", "ws", "stream", "notify", "auth", "search"),
    start: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3 }),
    goals: [
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "search" },
      { k: "util", kind: "auth", max: 0.8 },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "search" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 5600 },
    ],
    solution: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 } }),
  },
  {
    id: "sd19-s6-storage",
    title: "Этап 6. Стоимость хранения",
    statement:
      "Данных стало 900 ТБ, и хранилище съедает почти весь бюджет. Переведите файлы на более дешёвый класс хранения (параметр «Класс хранения»), чтобы схема укладывалась в $15 000 в месяц, средняя задержка оставалась не больше 40 мс (CDN прикрывает холодные блоки), а остальные цели не пострадали.",
    hint: "Горячее стоит $23 за ТБ — 20 700 в месяц. Смешанный класс — $10 за ТБ (9000), холодное — $4 (3600). Популярные блоки всё равно раздаёт CDN.",
    workload: W6,
    palette: palette("cache", "cdn", "ws", "stream", "notify", "auth", "search"),
    start: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 } }),
    goals: [
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "p50", max: 40 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 15000 },
    ],
    solution: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 }, tier: "mix" }),
    show: ["blob.tier"],
  },
  {
    id: "sd19-s7-reliability",
    title: "Этап 7. Надёжность и мониторинг",
    statement:
      "Диск стал критичным: данные пользователей нельзя терять, а простой должен быть короче минуты. Разнесите серверы, кэш и базу по трём зонам, включите rolling-выкладку, добавьте мониторинг и второй балансировщик. Схема переживает отказ зоны, выкладки, сервера, базы, кэша и сервиса входа, загрузка не выше 80%, бюджет — $16 000 в месяц.",
    hint: "Серверов M — около 14 в трёх зонах (после потери зоны остаются две трети). Два балансировщика, кэш и база размещены в трёх зонах с репликами, мониторинг на схему.",
    workload: W6,
    palette: palette("cache", "cdn", "ws", "stream", "notify", "auth", "search", "monitor"),
    start: drive({ app: 11, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 }, tier: "mix" }),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "auth" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 16000 },
    ],
    solution: drive({ app: 14, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 }, tier: "mix", zone: true, mon: true, lbN: 2 }),
    show: ["app.deploy"],
  },
  {
    id: "sd19-exam",
    title: "Экзамен. Облачный диск целиком",
    statement:
      "Итоговое задание. Соберите диск с нуля: объектное хранилище (800 ТБ, смешанный класс), CDN (≥90%), кэш листингов (≥85%), метаданные с репликой, WebSocket-шлюзы, поток событий и уведомления, сервис входа, поиск (шарды по объёму, две реплики), мониторинг, два балансировщика. Нагрузка: 15 000 скачиваний, 3800 чтений и 500 записей в секунду, 150 000 клиентов на соединениях. Схема переживает отказ зоны, выкладки, сервера, базы, кэша, сервиса входа и поиска; загрузка не выше 80%; средняя задержка ≤ 40 мс; бюджет — $15 000 в месяц.",
    hint: "Схема этапа 7 (база L: записей 500 в секунду): серверы M в трёх зонах (около 17: после потери зоны остаются 11 — 7700 запросов при нагрузке 7300), кэш и база с репликами, CDN → хранилище, ws → серверы → поток → уведомления, сервис входа ×3, поиск 2×2.",
    workload: { ...W6, read: 3800, write: 500, mediaTB: 800 },
    palette: palette("cache", "cdn", "ws", "stream", "notify", "auth", "search", "monitor"),
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    maxNodes: 16,
    goals: [
      { k: "has", kind: "blob" },
      { k: "param", kind: "blob", key: "tier", op: "!=", value: "hot" },
      { k: "cdnHit", min: 0.9 },
      { k: "hit", min: 0.85 },
      { k: "link", from: "cdn", to: "blob" },
      { k: "link", from: "ws", to: "app" },
      { k: "link", from: "app", to: "stream" },
      { k: "link", from: "stream", to: "notify" },
      { k: "link", from: "app", to: "auth" },
      { k: "link", from: "app", to: "search" },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb"] },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "auth" },
      { k: "survive", fail: "search" },
      { k: "p50", max: 40 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 15000 },
    ],
    solution: drive({ app: 17, cache: 4, dbRepl: true, cdn: true, ws: 14, stream: true, notify: 3, auth: 3, search: { shards: 2, replicas: 2 }, tier: "mix", zone: true, mon: true, lbN: 2, dbSize: "L" }),
    show: ["blob.tier", "app.deploy"],
  },
];
