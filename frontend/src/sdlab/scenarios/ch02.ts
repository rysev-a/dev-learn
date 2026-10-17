import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 2 «Масштабирование и балансировка»: вертикально и горизонтально, сессии, L4/L7, резерв, запас N+1. */

const chain = ["users>lb>app>db"];

export const CH02: SdScenario[] = [
  {
    id: "sd02-vertical",
    title: "Вертикальный рост",
    statement:
      "Сервис вырос до 900 чтений и 100 записей в секунду, а единственный сервер S тянет только 300. Балансировщик и новые серверы пока вводить нельзя: команда небольшая. Масштабируйте вертикально — оставьте один сервер, но возьмите подходящего размера, чтобы загрузка не превышала 80%.",
    hint: "У сервера L ёмкость 1500 запросов в секунду. Проверьте и базу: при 1000 запросах ей хватит размера M.",
    workload: WL({ read: 900, write: 100, dataGB: 30 }),
    palette: ["app", "db"],
    start: S([users(), N("app", "app"), N("db", "db", { size: "M" })], ["users>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "param", kind: "app", key: "instances", op: "==", value: 1 },
      { k: "lacks", kind: "lb" },
    ],
    solution: S([users(), N("app", "app", { size: "L" }), N("db", "db", { size: "M" })], ["users>app>db"]),
  },
  {
    id: "sd02-horizontal",
    title: "Горизонтальный рост",
    statement:
      "Та же нагрузка (1000 запросов в секунду), но теперь масштабируем горизонтально: поставьте балансировщик и несколько одинаковых серверов, чтобы загрузка не превышала 80% и стоимость осталась не больше $520 в месяц. Не забудьте: база тоже должна держать нагрузку.",
    hint: "Два сервера M дают 1400 запросов — загрузка 71%. Серверы S дороже при такой нагрузке: понадобится пять.",
    workload: WL({ read: 900, write: 100, dataGB: 30 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("app", "app"), N("db", "db", { size: "M" })], ["users>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "has", kind: "lb" },
      { k: "cost", max: 520 },
      { k: "param", kind: "app", key: "instances", op: ">=", value: 2 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 2 }), N("db", "db", { size: "M" })], chain),
  },
  {
    id: "sd02-sessions",
    title: "Сессии за балансировщиком",
    statement:
      "После того как серверов стало три, пользователи жалуются: вход «слетает» через раз. Сессии хранятся в памяти каждого сервера, а балансировщик отправляет запросы на любой из них. Исправьте схему: вынесите сессии во внешнее хранилище (параметр сервера «Сессии»), чтобы любой экземпляр мог обслужить любого пользователя.",
    hint: "Выберите сервер приложения на схеме и поменяйте «Сессии» на «во внешнем хранилище».",
    workload: WL({ read: 500, write: 60, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "param", kind: "app", key: "sessions", op: "==", value: "external" },
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
  },
  {
    id: "sd02-l7",
    title: "Какой уровень балансировки",
    statement:
      "Команде нужно направлять запросы по пути («/api» — одним сервисам, «/img» — другим) и повторять неудачные запросы. Поменяйте балансировщик так, чтобы он понимал HTTP, но при этом p99 остался не больше 120 мс.",
    hint: "Уровень L7 разбирает HTTP, но добавляет полторы миллисекунды. Загрузку серверов лучше держать ниже 60%, иначе вырастет очередь.",
    workload: WL({ read: 400, write: 50, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { layer: "L4" }), N("app", "app", { instances: 2, sessions: "external" }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "param", kind: "lb", key: "layer", op: "==", value: "L7" },
      { k: "p99", max: 120 },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), N("lb", "lb", { layer: "L7" }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
  },
  {
    id: "sd02-nplus1",
    title: "Запас на один сервер",
    statement:
      "Сервис получает 1000 запросов в секунду. Сейчас два сервера M дают 1400, а когда один из них падает, остаётся 700 — половина запросов теряется. Добавьте запас «N+1»: схема должна переживать отказ любого одного сервера приложения и укладываться в $700 в месяц.",
    hint: "Нужно, чтобы оставшиеся после потери одного сервера вытягивали 1000. Три сервера M: после потери двух остаётся 1400.",
    workload: WL({ read: 900, write: 100, dataGB: 30 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 2 }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "survive", fail: "app" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 700 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3 }), N("db", "db", { size: "M" })], chain),
  },
  {
    id: "sd02-lbha",
    title: "Балансировщик тоже ломается",
    statement:
      "Серверы приложения зарезервированы, но балансировщик один. Если он выйдет из строя, сервис полностью недоступен. Сделайте так, чтобы схема переживала отказ балансировщика и не имела единых точек отказа среди балансировщиков и серверов приложения.",
    hint: "Параметр «Экземпляры» у балансировщика: два экземпляра делят общий адрес.",
    workload: WL({ read: 400, write: 50, dataGB: 10 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "survive", fail: "lb" },
      { k: "noSpof", kinds: ["lb", "app"] },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
  },
  {
    id: "sd02-migrate",
    title: "Переезд на горизонталь",
    statement:
      "Итоговое упражнение главы. Сервис — один сервер S с сессиями в памяти и 700 запросами в секунду. Переведите его на горизонтальную схему: балансировщик (с резервом), серверы без состояния, запас на отказ одного сервера и загрузка не выше 80%. Бюджет — $900 в месяц.",
    hint: "Нужны: пара балансировщиков, сессии во внешнем хранилище, три сервера M (после потери одного остаются два — 1400 запросов), база M.",
    workload: WL({ read: 620, write: 80, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("app", "app"), N("db", "db", { size: "M" })], ["users>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "app" },
      { k: "survive", fail: "lb" },
      { k: "param", kind: "app", key: "sessions", op: "==", value: "external" },
      { k: "cost", max: 900 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
  },
];
