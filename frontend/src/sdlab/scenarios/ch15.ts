import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 15 «Отказоустойчивость: зоны и регионы»: размещение по зонам и регионам, запас на потерю домена отказа. */

const lb = () => N("lb", "lb", { instances: 2 });
const app = (n: number, zone: string, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", zone, ...extra });
const db = (zone: string, extra: Record<string, number | string | boolean> = {}) => N("db", "db", { size: "M", zone, replicas: 1, failover: true, ...extra });
const web = ["users>lb>app>db"];
const withCache = ["users>lb>app>db", "app>cache"];
const cache = (zone: string, replicas = 1) => N("cache", "cache", { sizeGB: 4, ttl: 3600, zone, replicas });

export const CH15: SdScenario[] = [
  {
    id: "sd15-zone-app",
    title: "Серверы по зонам",
    statement:
      "База уже размещена в трёх зонах, а серверы приложения стоят в одной: при отказе зоны они пропадают все. Разнесите серверы по трём зонам (параметр «Размещение») и добавьте их столько, чтобы после потери зоны (минус треть серверов) остальные вытягивали 1700 запросов в секунду. Схема должна переживать отказ зоны.",
    hint: "Пять серверов M: после потери зоны остаётся три — 2100 запросов. Четырёх мало: останется два (1400).",
    workload: WL({ read: 1500, write: 200, dataGB: 50 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(3, "single"), db("multi")], web),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "capacity", max: 0.8 },
      { k: "param", kind: "app", key: "zone", op: "==", value: "multi" },
    ],
    solution: S([users(), lb(), app(5, "multi"), db("multi")], web),
  },
  {
    id: "sd15-zone-db",
    title: "База по зонам",
    statement:
      "Серверы приложения разнесены по зонам, но база стоит в одной зоне вместе со своей репликой: потеря зоны останавливает запись. Разместите базу в трёх зонах с репликой и автопереключением, чтобы схема переживала отказ зоны.",
    hint: "Параметр «Размещение» базы — «три зоны региона»; реплика и автопереключение должны быть включены.",
    workload: WL({ read: 1500, write: 200, dataGB: 50 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(5, "multi"), db("single")], web),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "param", kind: "db", key: "zone", op: "==", value: "multi" },
      { k: "noSpof", kinds: ["db"] },
    ],
    solution: S([users(), lb(), app(5, "multi"), db("multi")], web),
  },
  {
    id: "sd15-zone-cache",
    title: "Кэш по зонам",
    statement:
      "В схеме есть кэш, но он стоит в одной зоне, а база без кэша не вытянет чтения: 3000 в секунду. Разместите кэш в трёх зонах с репликой (≥85% попаданий), чтобы схема переживала отказ зоны. Остальные компоненты уже размещены правильно.",
    hint: "У кэша — размещение «три зоны региона» и хотя бы одна реплика.",
    workload: WL({ read: 3000, write: 100, dataGB: 40, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(8, "multi"), cache("single", 0), db("multi")], withCache),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "hit", min: 0.85 },
      { k: "param", kind: "cache", key: "zone", op: "==", value: "multi" },
    ],
    solution: S([users(), lb(), app(8, "multi"), cache("multi"), db("multi")], withCache),
  },
  {
    id: "sd15-region",
    title: "Пережить отказ региона",
    statement:
      "Сервис должен пережить отказ целого региона, и ради этого размещается в двух регионах. После потери региона остаётся половина серверов. Переведите серверы, кэш и базу на размещение «два региона» и подберите число серверов: 3000 запросов в секунду должны вытягиваться и после отказа региона. Бюджет — $2800 в месяц.",
    hint: "Десять серверов M: после потери региона остаётся пять — 3500. Для кэша и базы нужны реплики (и автопереключение у базы).",
    workload: WL({ read: 2800, write: 200, dataGB: 60, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(6, "multi"), cache("multi"), db("multi")], withCache),
    goals: [
      { k: "survive", fail: "region" },
      { k: "survive", fail: "zone" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 2800 },
    ],
    solution: S([users(), lb(), app(10, "regions"), cache("regions"), db("regions")], withCache),
  },
  {
    id: "sd15-budget",
    title: "Уровень надёжности под бюджет",
    statement:
      "Внутреннему сервису отчётов не нужен второй регион, но простой из-за потери зоны недопустим. Соберите схему, которая переживает отказ зоны и укладывается в $1600 в месяц, при нагрузке 1500 запросов в секунду. Не размещайте её в двух регионах — это дороже.",
    hint: "Размещение «три зоны региона»; серверов M — четыре или пять (после потери зоны остаётся 2/3), база M с репликой и автопереключением.",
    workload: WL({ read: 1300, write: 200, dataGB: 40 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(2, "single"), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "survive", fail: "zone" },
      { k: "param", kind: "app", key: "zone", op: "!=", value: "regions" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1600 },
    ],
    solution: S([users(), lb(), app(5, "multi"), db("multi")], web),
  },
  {
    id: "sd15-final",
    title: "Платёжный сервис в двух регионах",
    statement:
      "Итоговое упражнение главы. 3000 чтений и 300 записей в секунду, 150 ГБ данных, рабочий набор 12 ГБ. Соберите схему в двух регионах: серверы, кэш (≥85%) и база разнесены, схема переживает отказ зоны и региона, загрузка не выше 80%, бюджет — $4500 в месяц.",
    hint: "Серверов M — двенадцать (после потери региона шесть — 4200, после зоны восемь — 5600); кэш 12 ГБ с репликой; база L или M с репликой, автопереключением и размещением «два региона».",
    workload: WL({ read: 3000, write: 300, dataGB: 150, hotSet: 0.08 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), lb(), app(4, "single"), N("cache", "cache", { sizeGB: 4, ttl: 300 }), N("db", "db", { size: "M" })], withCache),
    goals: [
      { k: "survive", fail: "region" },
      { k: "survive", fail: "zone" },
      { k: "hit", min: 0.85 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 4500 },
    ],
    solution: S(
      [users(), lb(), app(12, "regions"), N("cache", "cache", { sizeGB: 12, ttl: 3600, zone: "regions", replicas: 1 }), db("regions")],
      withCache,
    ),
  },
];
