import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 11 «Реальное время»: шлюзы WebSocket, масштаб соединений, поток сообщений через очередь, присутствие. */

const lb = () => N("lb", "lb", { instances: 2 });
const app = (n = 4, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", ...extra });
const http = ["users>lb>app>db"];

export const CH11: SdScenario[] = [
  {
    id: "sd11-ws-gateway",
    title: "Шлюзы WebSocket",
    statement:
      "Чат получает 90 000 одновременных соединений, а обычные запросы (история) идут через балансировщик. Один шлюз WebSocket держит 15 000 соединений. Добавьте шлюзы между пользователями и серверами приложения, свяжите их и подберите число экземпляров так, чтобы шлюзы были загружены не больше чем на 80%.",
    hint: "Пользователи → шлюз WebSocket → сервер приложения. Для 90 000 соединений понадобится восемь экземпляров (67–75%).",
    workload: WL({ read: 300, write: 50, dataGB: 20, connections: 90000, msgPerConn: 0.005 }),
    palette: ["lb", "ws", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], http),
    goals: [
      { k: "has", kind: "ws" },
      { k: "link", from: "clients", to: "ws" },
      { k: "link", from: "ws", to: "app" },
      { k: "util", kind: "ws", max: 0.8 },
    ],
    solution: S([users(), lb(), N("ws", "ws", { instances: 8 }), app(), N("db", "db", { size: "M" })], ["users>lb>app>db", "users>ws>app"]),
  },
  {
    id: "sd11-ws-scale",
    title: "Триста тысяч соединений",
    statement:
      "Аудитория выросла: 300 000 одновременных соединений. Подберите число шлюзов WebSocket: загрузка не выше 80% и запас на потерю одного шлюза без перегрузки остальных. Бюджет — $3500 в месяц.",
    hint: "300 000 / (15 000 × 0,8) = 25 шлюзов; при потере одного загрузка вырастет с 80% до 83% — поэтому лучше 26.",
    workload: WL({ read: 300, write: 50, dataGB: 30, connections: 300000, msgPerConn: 0.002 }),
    palette: ["lb", "ws", "app", "db"],
    start: S([users(), lb(), N("ws", "ws", { instances: 10 }), app(), N("db", "db", { size: "M" })], ["users>lb>app>db", "users>ws>app"]),
    goals: [
      { k: "util", kind: "ws", max: 0.8 },
      { k: "noSpof", kinds: ["ws"] },
      { k: "util", kind: "app", max: 0.8 },
      { k: "cost", max: 3500 },
    ],
    solution: S([users(), lb(), N("ws", "ws", { instances: 26 }), app(), N("db", "db", { size: "M" })], ["users>lb>app>db", "users>ws>app"]),
  },
  {
    id: "sd11-messages",
    title: "Поток сообщений",
    statement:
      "90 000 соединений по 0,03 сообщения в секунду — 2700 сообщений в секунду. Сейчас они пишутся прямо в базу, и она перегружена. Пропустите сообщения через очередь и обработчиков: свяжите сервер с очередью, очередь — с обработчиками, обработчиков — с базой. База и серверы — не выше 80%, очередь разбирается без отставания (пик — 10 секунд, допустимо 5 с).",
    hint: "Нужен разбор не меньше 2700 в секунду: семь обработчиков M — 2800. Приложению нужно около шести серверов M.",
    workload: WL({ read: 300, write: 50, dataGB: 100, connections: 90000, msgPerConn: 0.03, spikeSec: 10 }),
    palette: ["lb", "ws", "app", "queue", "worker", "db"],
    start: S([users(), lb(), N("ws", "ws", { instances: 8 }), app(6), N("db", "db", { size: "L" })], ["users>lb>app>db", "users>ws>app", "app>db"]),
    goals: [
      { k: "link", from: "app", to: "queue" },
      { k: "link", from: "queue", to: "worker" },
      { k: "link", from: "worker", to: "db" },
      { k: "util", kind: "db", max: 0.8 },
      { k: "util", kind: "app", max: 0.8 },
      { k: "lag", max: 5 },
    ],
    solution: S(
      [users(), lb(), N("ws", "ws", { instances: 8 }), app(6), N("queue", "queue"), N("worker", "worker", { instances: 7, size: "M" }), N("db", "db", { size: "L" })],
      ["users>lb>app>db", "users>ws>app", "app>queue>worker>db"],
    ),
  },
  {
    id: "sd11-presence",
    title: "Присутствие в кэше",
    statement:
      "Список друзей показывает «онлайн» — это 3000 запросов статуса в секунду к небольшому рабочему набору (около 2 ГБ). База S не справляется. Поставьте кэш статусов с долгим временем жизни записей: кэш отдаёт не меньше 90% чтений, база загружена не выше 80%.",
    hint: "Кэш 2–3 ГБ с TTL 3600 — около 94% попаданий; TTL 300 даст чуть меньше 90%.",
    workload: WL({ read: 3000, write: 100, dataGB: 5, hotSet: 0.4 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(6), N("db", "db")], http),
    goals: [
      { k: "hit", min: 0.9 },
      { k: "util", kind: "db", max: 0.8 },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), lb(), app(6), N("cache", "cache", { sizeGB: 3, ttl: 3600 }), N("db", "db")], ["users>lb>app>db", "app>cache"]),
  },
  {
    id: "sd11-final",
    title: "Чат целиком",
    statement:
      "Итоговое упражнение главы. Мессенджер: 150 000 соединений, 0,02 сообщения в секунду на соединение (3000 сообщений в секунду), статусы и история — 2000 чтений, 100 записей. Соберите схему: шлюзы WebSocket (не выше 80%, с запасом на потерю одного), очередь с обработчиками (без отставания: пик 10 с, допустимо 5 с), кэш статусов (≥90%), база не выше 80%, бюджет — $5000 в месяц.",
    hint: "Шлюзы: 150 000 / 12 000 = 13–14. Обработчики: 3000 сообщений — восемь M. Кэш 3 ГБ с TTL 3600. Серверы приложения принимают и обычные запросы, и 3000 сообщений в секунду: около десяти M.",
    workload: WL({ read: 2000, write: 100, dataGB: 100, hotSet: 0.04, connections: 150000, msgPerConn: 0.02, spikeSec: 10 }),
    palette: ["lb", "ws", "app", "queue", "worker", "cache", "db"],
    start: S([users(), lb(), app(6), N("db", "db", { size: "L" })], http),
    goals: [
      { k: "util", kind: "ws", max: 0.8 },
      { k: "noSpof", kinds: ["ws"] },
      { k: "link", from: "app", to: "queue" },
      { k: "link", from: "worker", to: "db" },
      { k: "lag", max: 5 },
      { k: "hit", min: 0.9 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 5000 },
    ],
    solution: S(
      [
        users(),
        lb(),
        N("ws", "ws", { instances: 14 }),
        app(10),
        N("queue", "queue"),
        N("worker", "worker", { instances: 8, size: "M" }),
        N("cache", "cache", { sizeGB: 4, ttl: 3600 }),
        N("db", "db", { size: "L" }),
      ],
      ["users>lb>app>db", "users>ws>app", "app>queue>worker>db", "app>cache"],
    ),
  },
];
