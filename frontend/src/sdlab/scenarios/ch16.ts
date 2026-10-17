import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 16 «CI/CD и выкладка без простоя»: стратегии выкладки, запас на обновление, цена blue/green. */

const lb = () => N("lb", "lb", { instances: 2 });
const app = (n: number, deploy: string, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", deploy, ...extra });
const web = ["users>lb>app>db"];
const withCache = ["users>lb>app>db", "app>cache"];

export const CH16: SdScenario[] = [
  {
    id: "sd16-rolling",
    title: "Выкладка по одному",
    statement:
      "Сейчас новая версия выкладывается на все серверы сразу: на время выкладки сервис недоступен. Переключите стратегию на «по одному» (rolling) и подберите число серверов, чтобы при обновлении (минус один сервер) оставшиеся вытягивали 1300 запросов в секунду. Схема должна переживать выкладку. Бюджет — $700 в месяц. Параметр «Выкладка» показан в упражнении.",
    hint: "Три сервера M: при обновлении остаётся два — 1400 запросов. Двух серверов мало: останется один (700).",
    workload: WL({ read: 1200, write: 100, dataGB: 40 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(2, "all"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "survive", fail: "deploy" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 700 },
    ],
    solution: S([users(), lb(), app(3, "rolling"), N("db", "db", { size: "M" })], web),
    show: ["app.deploy"],
  },
  {
    id: "sd16-bluegreen",
    title: "Когда запаса нет",
    statement:
      "Парк небольшой — два сервера M (1400 запросов), нагрузка 1300. Выкладка «по одному» оставит один сервер, этого мало, а покупать третий бюджет не позволяет. Выберите blue/green: пока идёт выкладка, мощность не падает. Не больше двух серверов, загрузка не выше 95%, стоимость — не больше $700 в месяц (blue/green удваивает расход на серверы).",
    hint: "Параметр «Выкладка» сервера — blue/green. Расход на серверы при этом ×2: 2 × 240 = 480.",
    workload: WL({ read: 1200, write: 100, dataGB: 40 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(2, "rolling"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "survive", fail: "deploy" },
      { k: "param", kind: "app", key: "instances", op: "<=", value: 2 },
      { k: "capacity", max: 0.95 },
      { k: "cost", max: 1100 },
    ],
    solution: S([users(), lb(), app(2, "bluegreen"), N("db", "db", { size: "M" })], web),
    show: ["app.deploy"],
  },
  {
    id: "sd16-cost",
    title: "Что дешевле: rolling или blue/green",
    statement:
      "Нагрузка выросла до 6000 запросов в секунду, и сейчас используется blue/green: расход на серверы удваивается. Сравните цены: при большом парке rolling обходится заметно дешевле. Переведите выкладку на «по одному» и подберите число серверов: схема переживает выкладку, загрузка не выше 90%, бюджет — $2200 в месяц.",
    hint: "Десять серверов M: при выкладке остаётся девять — 6300 запросов. Blue/green с девятью серверами обойдётся в 2160 за серверы — слишком дорого.",
    workload: WL({ read: 5700, write: 300, dataGB: 20, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(9, "bluegreen"), N("cache", "cache", { sizeGB: 3, ttl: 3600 }), N("db", "db", { size: "M" })], withCache),
    goals: [
      { k: "survive", fail: "deploy" },
      { k: "capacity", max: 0.9 },
      { k: "cost", max: 2200 },
    ],
    solution: S([users(), lb(), app(10, "rolling"), N("cache", "cache", { sizeGB: 3, ttl: 3600 }), N("db", "db", { size: "M" })], withCache),
    show: ["app.deploy"],
  },
  {
    id: "sd16-zero-downtime",
    title: "Выкладка и отказ зоны",
    statement:
      "Серверы должны пережить и выкладку (минус один сервер), и отказ зоны (минус треть). Нагрузка — 2000 запросов в секунду. Разместите серверы по трём зонам, включите rolling и подберите число серверов: схема переживает выкладку, отказ зоны и отказ сервера.",
    hint: "Четыре сервера M: при потере зоны останется два — 1400, мало. Пять: после потери зоны три — 2100, при выкладке четыре — 2800.",
    workload: WL({ read: 1800, write: 200, dataGB: 50 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(3, "all", { zone: "single" }), N("db", "db", { size: "M", zone: "multi", replicas: 1, failover: true })], web),
    goals: [
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "app" },
      { k: "capacity", max: 0.8 },
    ],
    solution: S([users(), lb(), app(5, "rolling", { zone: "multi" }), N("db", "db", { size: "M", zone: "multi", replicas: 1, failover: true })], web),
    show: ["app.deploy"],
  },
  {
    id: "sd16-final",
    title: "Безопасная доставка",
    statement:
      "Итоговое упражнение главы. Магазин: 2500 запросов в секунду, кэш и база. Соберите схему, которая переживает выкладку (rolling), отказ зоны, отказ базы и кэша, с мониторингом: загрузка не выше 80%, бюджет — $3000 в месяц.",
    hint: "Серверов M — семь (после потери зоны пять — 3500); кэш с репликой в трёх зонах; база M с репликой и автопереключением в трёх зонах; мониторинг.",
    workload: WL({ read: 2300, write: 200, dataGB: 60, hotSet: 0.08 }),
    palette: ["lb", "app", "cache", "db", "monitor"],
    start: S([users(), lb(), app(4, "all", { zone: "single" }), N("cache", "cache", { sizeGB: 4, ttl: 300 }), N("db", "db", { size: "M" })], withCache),
    goals: [
      { k: "survive", fail: "deploy" },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "has", kind: "monitor" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3000 },
    ],
    solution: S(
      [
        users(),
        lb(),
        app(7, "rolling", { zone: "multi" }),
        N("cache", "cache", { sizeGB: 5, ttl: 3600, zone: "multi", replicas: 1 }),
        N("db", "db", { size: "M", zone: "multi", replicas: 1, failover: true }),
        N("mon", "monitor"),
      ],
      withCache,
    ),
    show: ["app.deploy"],
  },
];
