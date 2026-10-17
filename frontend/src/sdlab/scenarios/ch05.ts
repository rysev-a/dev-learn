import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 5 «Шардирование»: разрезать базу по записи, ключ шардирования, горячие точки, шарды с репликами. */

const chain = ["users>lb>app>db"];
const app = (n = 4) => N("app", "app", { size: "M", instances: n, sessions: "external" });
const lb = () => N("lb", "lb", { instances: 2 });

export const CH05: SdScenario[] = [
  {
    id: "sd05-write-shards",
    title: "Упёрлись в запись",
    statement:
      "Сервис принимает 1500 записей в секунду, а база S тянет 200, M — 600, L — 1500 (в обрез). Реплики запись не ускорят. Разрежьте данные на шарды (параметр «Шарды» у базы): загрузка не выше 80%, стоимость не больше $1600 в месяц.",
    hint: "Записи делятся между шардами поровну (при хеше). Четыре шарда M: по 375 записей на шард — 63%. Столько же стоят десять шардов S, но M проще.",
    workload: WL({ read: 500, write: 1500, dataGB: 400 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "cost", max: 1600 },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 4 })], chain),
  },
  {
    id: "sd05-monotonic",
    title: "Ключ растёт со временем",
    statement:
      "Данные уже разрезаны на четыре шарда по диапазонам ключа, но ключ — время создания записи: все новые записи попадают в последний шард. Перекос мешает: смените способ разбиения так, чтобы на самый нагруженный шард приходилось не больше 40% нагрузки, а общая загрузка не превышала 80%.",
    hint: "У базы есть параметр «Ключ шардирования»: хеш или диапазон. Хеш распределяет записи поровну.",
    workload: WL({ read: 400, write: 1200, dataGB: 300, monotonic: true }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 4, shardKey: "range" })], chain),
    goals: [
      { k: "shardShare", max: 0.4 },
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 4, shardKey: "hash" })], chain),
    show: ["db.shardKey"],
  },
  {
    id: "sd05-hotkey",
    title: "Горячий ключ",
    statement:
      "У сервиса есть «знаменитость»: 20% запросов приходится на один ключ. Тогда на одном шарде оказывается 20% плюс его доля от остального. Сейчас четыре шарда M, и самый нагруженный перегружен. Что дешевле: больше шардов или шарды покрупнее? Добейтесь загрузки не выше 80% при стоимости не больше $1800.",
    hint: "Доля горячего шарда = горячий ключ + остальное / число шардов. Увеличивать число шардов выгодно слабо: 20% не уйдут. Крупные шарды помогают сильнее.",
    workload: WL({ read: 400, write: 1500, dataGB: 300, hotKey: 0.2 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 4 })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1800 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "L", shards: 2 })], chain),
  },
  {
    id: "sd05-with-replicas",
    title: "Шарды и реплики вместе",
    statement:
      "Данные: 3000 чтений и 900 записей в секунду. Нужно и разрезать (запись), и реплицировать (чтения и отказоустойчивость). Соберите базу из шардов M с репликами и автопереключением: загрузка не выше 80%, схема переживает отказ базы, бюджет — $2700 в месяц.",
    hint: "Три шарда M: по 300 записей (50%); чтений по 1000 на шард, реплика M тянет 3000. Включите автопереключение.",
    workload: WL({ read: 3000, write: 900, dataGB: 600 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(8), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "db" },
      { k: "cost", max: 2700 },
    ],
    solution: S([users(), lb(), app(8), N("db", "db", { size: "M", shards: 3, replicas: 1, failover: true })], chain),
  },
  {
    id: "sd05-nosql",
    title: "Выбор хранилища",
    statement:
      "Сервис хранит события по ключу, без соединений и сложных запросов: подходит NoSQL, которое примерно в 1,8 раза быстрее на простых операциях. При 1500 записях в секунду уложите всю схему в $1100: выберите тип «NoSQL» и подберите шарды.",
    hint: "NoSQL M тянет около 1080 записей в секунду на шард. Два шарда: 750 на шард — 69%.",
    workload: WL({ read: 600, write: 1500, dataGB: 500 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 2 })], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1100 },
      { k: "param", kind: "db", key: "engine", op: "==", value: "nosql" },
    ],
    solution: S([users(), lb(), app(), N("db", "db", { size: "M", shards: 2, engine: "nosql" })], chain),
  },
  {
    id: "sd05-final",
    title: "Социальная сеть: перекос и надёжность",
    statement:
      "Итоговое упражнение главы. Лента событий: 3000 чтений и 1200 записей в секунду, ключи растут со временем, 10% запросов приходится на самый популярный ключ. Соберите базу: хеш-шардирование, реплики и автопереключение, загрузка не выше 85%, переживание отказа базы, бюджет — $3500 в месяц.",
    hint: "Хеш убирает перекос по времени, но горячие 10% остаются: крупные шарды помогают. Подойдут три шарда M с репликой или два шарда L.",
    workload: WL({ read: 3000, write: 1200, dataGB: 800, monotonic: true, hotKey: 0.1 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(8), N("db", "db", { size: "M", shards: 4, shardKey: "range" })], chain),
    goals: [
      { k: "capacity", max: 0.85 },
      { k: "param", kind: "db", key: "shardKey", op: "==", value: "hash" },
      { k: "survive", fail: "db" },
      { k: "cost", max: 3500 },
    ],
    solution: S([users(), lb(), app(8), N("db", "db", { size: "L", shards: 2, replicas: 1, failover: true })], chain),
    show: ["db.shardKey"],
  },
];
