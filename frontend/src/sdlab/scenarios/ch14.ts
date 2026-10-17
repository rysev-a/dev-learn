import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 14 «Наблюдаемость и SLO»: мониторинг, цели по доступности и задержке, запас, итоговая схема. */

const web = ["users>lb>app>db"];
const app = (n: number, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", ...extra });
const mon = () => N("mon", "monitor");

export const CH14: SdScenario[] = [
  {
    id: "sd14-monitor",
    title: "Мониторинг и три девятки",
    statement:
      "Сервис работает без мониторинга, и о сбоях узнают от пользователей. Добавьте мониторинг (метрики, журналы, оповещения) и дотяните схему до цели по доступности 99,9% при p99 не больше 120 мс. Сейчас база одна и тянет доступность вниз.",
    hint: "Компонент «Мониторинг» — на схему (связи не нужны). Для 99,9% база должна иметь реплику и автопереключение.",
    workload: WL({ read: 400, write: 60, dataGB: 20 }),
    palette: ["lb", "app", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(3), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "has", kind: "monitor" },
      { k: "availability", min: 0.999 },
      { k: "p99", max: 120 },
    ],
    solution: S([users(), N("lb", "lb"), app(3), N("db", "db", { size: "M", replicas: 1, failover: true }), mon()], web),
  },
  {
    id: "sd14-slo-three",
    title: "SLO 99,95%: дёшево",
    statement:
      "Цель по доступности — 99,95%. Соберите минимальную по стоимости схему, которая её выполняет: мониторинг обязателен, схема переживает отказ базы и сервера приложения, бюджет — $700 в месяц.",
    hint: "Один балансировщик даёт потолок 99,95% — нужно два. База S с репликой и автопереключением, два-три сервера M.",
    workload: WL({ read: 400, write: 60, dataGB: 20 }),
    palette: ["lb", "app", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(2), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "availability", min: 0.9995 },
      { k: "has", kind: "monitor" },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 700 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), app(2), N("db", "db", { replicas: 1, failover: true }), mon()], web),
  },
  {
    id: "sd14-slo-five",
    title: "Пять девяток",
    statement:
      "Для платёжного шлюза цель — доступность не ниже 99,999%. Каждый компонент должен быть зарезервирован: балансировщики, серверы приложения и база. Соберите схему с мониторингом и бюджетом $1500 в месяц, которая достигает цели и переживает отказ любого компонента.",
    hint: "Два балансировщика, три сервера, база с двумя репликами и автопереключением даёт около 99,9999%.",
    workload: WL({ read: 500, write: 100, dataGB: 30 }),
    palette: ["lb", "app", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(2), N("db", "db", { size: "M", replicas: 1, failover: true })], web),
    goals: [
      { k: "availability", min: 0.99999 },
      { k: "has", kind: "monitor" },
      { k: "noSpof", kinds: ["lb", "app", "db"] },
      { k: "survive", fail: "db" },
      { k: "cost", max: 1500 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), app(3), N("db", "db", { size: "M", replicas: 1, failover: true }), mon()], web),
  },
  {
    id: "sd14-headroom",
    title: "Запас по ёмкости",
    statement:
      "Команда мониторинга настроила оповещение на загрузку 60%: выше — повод для тревоги. Нагрузка: 1500 чтений и 200 записей в секунду. Доведите схему до состояния, когда ни один компонент не загружен больше чем на 60%, с мониторингом и бюджетом $1300 в месяц.",
    hint: "Серверы: 1700 запросов — два L (3000, 57%). База M при чтениях 1500 — 83%: нужна реплика или размер L.",
    workload: WL({ read: 1500, write: 200, dataGB: 60 }),
    palette: ["lb", "app", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(3), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "capacity", max: 0.6 },
      { k: "has", kind: "monitor" },
      { k: "cost", max: 1300 },
    ],
    solution: S([users(), N("lb", "lb"), N("app", "app", { size: "L", instances: 2, sessions: "external" }), N("db", "db", { size: "M", replicas: 1 }), mon()], web),
  },
  {
    id: "sd14-latency",
    title: "Бюджет задержки",
    statement:
      "SLO по задержке: p50 не больше 40 мс и p99 не больше 80 мс. Читают 2700 раз в секунду, база M почти на пределе, а серверы приложения при высокой загрузке копят очередь. Добавьте кэш (≥80%) и уменьшите загрузку серверов, чтобы выполнить цели.",
    hint: "Задержка растёт как 1/(1 − загрузка): серверы держите около 50%. Кэш 5 ГБ с TTL 3600 снимет чтения с базы.",
    workload: WL({ read: 2700, write: 50, dataGB: 50, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(5), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "p50", max: 40 },
      { k: "p99", max: 80 },
      { k: "hit", min: 0.8 },
    ],
    solution: S([users(), N("lb", "lb"), app(8), N("cache", "cache", { sizeGB: 5, ttl: 3600 }), N("db", "db", { size: "M" })], ["users>lb>app>db", "app>cache"]),
  },
  {
    id: "sd14-final",
    title: "Схема с целями по надёжности",
    statement:
      "Итоговое упражнение главы. Сервис с SLO: доступность ≥ 99,995%, p99 ≤ 100 мс, загрузка не выше 60%. Читают 3000 раз и пишут 150 раз в секунду. Соберите схему с мониторингом: два балансировщика, кэш с репликой, база с репликой и автопереключением, переживание отказа базы, кэша и сервера приложения, бюджет $2200 в месяц.",
    hint: "Серверов M — около девяти (загрузка ~50%), кэш 6 ГБ с репликой и TTL 3600, база M с репликой и автопереключением, мониторинг.",
    workload: WL({ read: 3000, write: 150, dataGB: 60, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db", "monitor"],
    start: S([users(), N("lb", "lb"), app(4), N("db", "db", { size: "M" })], web),
    goals: [
      { k: "has", kind: "monitor" },
      { k: "availability", min: 0.99995 },
      { k: "p99", max: 100 },
      { k: "capacity", max: 0.6 },
      { k: "survive", fail: "db" },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 2200 },
    ],
    solution: S(
      [
        users(),
        N("lb", "lb", { instances: 2 }),
        app(9),
        N("cache", "cache", { sizeGB: 6, ttl: 3600, replicas: 1 }),
        N("db", "db", { size: "M", replicas: 1, failover: true }),
        mon(),
      ],
      ["users>lb>app>db", "app>cache"],
    ),
  },
];
