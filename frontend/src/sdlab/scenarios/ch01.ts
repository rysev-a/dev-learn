import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 1 «Требования, нагрузка и прикидки»: собрать цепочку, прикинуть число серверов, найти узкое место,
   учесть пик, задержку, доступность и бюджет. */

const web = ["lb", "app", "db"] as const;

export const CH01: SdScenario[] = [
  {
    id: "sd01-wire",
    title: "Первая цепочка",
    statement:
      "Сервис записок: пользователи читают и пишут заметки. Соедините пользователей с сервером приложения, а сервер — с базой данных, чтобы запросы дошли до хранилища. Компоненты уже стоят на поле: нужны связи (кнопка «Связать» и клик по двум компонентам).",
    hint: "Пользователи → сервер приложения → база данных. Сервер не должен обращаться к базе в обход самого себя.",
    workload: WL({ read: 50, write: 10, dataGB: 5 }),
    palette: ["app", "db"],
    start: S([users(), N("app", "app"), N("db", "db")]),
    goals: [
      { k: "link", from: "clients", to: "app" },
      { k: "link", from: "app", to: "db" },
      { k: "success", min: 0.99 },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
  },
  {
    id: "sd01-fleet",
    title: "Сколько серверов нужно",
    statement:
      "Заметки выросли: 600 чтений и 120 записей в секунду. Один сервер размера S тянет около 300 запросов в секунду, база S — 1000 чтений и 200 записей. Добавьте балансировщик и сервер за ним так, чтобы ни один компонент не был загружен больше чем на 80%, а стоимость не превышала $500 в месяц.",
    hint: "Нагрузка на сервер: 720 запросов. Три сервера S дают 900 — загрузка ровно 80%. Базе S не хватает: у неё 600/1000 + 120/200 = 120% — нужна M.",
    workload: WL({ read: 600, write: 120, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("app", "app"), N("db", "db")], ["users>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "has", kind: "lb" },
      { k: "cost", max: 500 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
  },
  {
    id: "sd01-bottleneck",
    title: "Узкое место",
    statement:
      "Серверов хватает, а сервис всё равно тормозит и теряет запросы. Найдите самый загруженный компонент на схеме (красный) и исправьте именно его — лишних денег не тратьте: бюджет $460.",
    hint: "Смотрите на полоски загрузки. Приложения простаивают, а база перегружена — сервера тут не причём.",
    workload: WL({ read: 600, write: 120, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 4 }), N("db", "db")], ["users>lb>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "cost", max: 460 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
  },
  {
    id: "sd01-peak",
    title: "Пик нагрузки",
    statement:
      "В пик (распродажа, вечер пятницы) нагрузка втрое выше средней: 1800 чтений и 300 записей в секунду. Схема рассчитана на среднюю нагрузку. Доведите её до пика: загрузка компонентов не выше 85%, стоимость не больше $1200 в месяц.",
    hint: "Прикидывайте по пику, а не по среднему. Приложения: 2100 запросов — например, четыре сервера M. База: M уже не вытянет, нужна L.",
    workload: WL({ read: 1800, write: 300, dataGB: 60 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "capacity", max: 0.85 },
      { k: "success", min: 0.99 },
      { k: "cost", max: 1200 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 4, size: "M" }), N("db", "db", { size: "L" })], ["users>lb>app>db"]),
  },
  {
    id: "sd01-latency",
    title: "Задержка под нагрузкой",
    statement:
      "Серверы приложения загружены на 90%, и пользователи жалуются на медленные ответы. Загрузка и задержка связаны: чем ближе к 100%, тем длиннее очередь. Добейтесь p99 не больше 150 мс и средней задержки не больше 70 мс.",
    hint: "Задержка растёт как 1/(1 − загрузка). Уберите перегрев там, где он есть: добавьте серверов, чтобы загрузка упала примерно вдвое.",
    workload: WL({ read: 500, write: 50, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "p99", max: 150 },
      { k: "p50", max: 70 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 4 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
  },
  {
    id: "sd01-nines",
    title: "Три девятки",
    statement:
      "По договору сервис должен быть доступен не меньше 99,95% времени. Сейчас каждый компонент один, и сбой любого останавливает сервис. Добавьте резервирование: схема должна переживать отказ балансировщика, сервера приложения и лидера базы данных.",
    hint: "Доступность цепочки — произведение доступностей. Резерв: два балансировщика, три сервера (после потери одного оставшиеся должны вытянуть нагрузку), у базы — реплика и автопереключение.",
    workload: WL({ read: 300, write: 60, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 2 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "availability", min: 0.9995 },
      { k: "survive", fail: "lb" },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "db" },
      { k: "noSpof", kinds: [...web] },
    ],
    solution: S(
      [users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3 }), N("db", "db", { size: "M", replicas: 1, failover: true })],
      ["users>lb>app>db"],
    ),
  },
  {
    id: "sd01-budget",
    title: "Уложиться в бюджет",
    statement:
      "Стартап: бюджет только $330 в месяц, нагрузка скромная — 400 чтений и 60 записей в секунду. Соберите самую дешёвую схему, которая выдерживает нагрузку (загрузка не выше 85%) и не имеет перегруженных компонентов. Размер и число серверов подбирайте сами.",
    hint: "Два сервера S дают 600 запросов при нагрузке 460 (77%). Балансировщик нужен, если серверов больше одного. База S: 400/1000 + 60/200 = 70% — хватит.",
    workload: WL({ read: 400, write: 60, dataGB: 5 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 3, size: "M" }), N("db", "db", { size: "L" })], ["users>lb>app>db"]),
    goals: [
      { k: "capacity", max: 0.85 },
      { k: "success", min: 0.99 },
      { k: "cost", max: 330 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 2 }), N("db", "db")], ["users>lb>app>db"]),
  },
];
