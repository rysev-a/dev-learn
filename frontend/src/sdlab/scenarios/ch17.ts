import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 17 «Облако и стоимость»: тарифы (резерв, спот), правильный размер, CDN вместо серверов, итоговая экономия. */

const lb = () => N("lb", "lb");
const app = (n: number, extra: Record<string, number | string | boolean> = {}) => N("app", "app", { size: "M", instances: n, sessions: "external", ...extra });
const web = ["users>lb>app>db"];
const queued = ["users>lb>app>db", "app>queue>worker>db"];

export const CH17: SdScenario[] = [
  {
    id: "sd17-reserved",
    title: "Резерв для постоянной нагрузки",
    statement:
      "Нагрузка стабильна: 4000 запросов в секунду круглые сутки. Серверы оплачиваются по требованию. Переведите их на резервный тариф (параметр «Тариф» показан в упражнении) со скидкой около 40% и уложитесь в $1000 в месяц при загрузке не выше 80%.",
    hint: "Восемь серверов M по требованию стоят 960 за одни серверы — вместе с базой и балансировщиком больше 1200. С резервом — около 580 за серверы.",
    workload: WL({ read: 3600, write: 400, dataGB: 60 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), app(8), N("db", "db", { size: "L" })], web),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "param", kind: "app", key: "pricing", op: "==", value: "reserved" },
      { k: "cost", max: 1300 },
    ],
    solution: S([users(), lb(), app(8, { pricing: "reserved" }), N("db", "db", { size: "L" })], web),
    show: ["app.pricing"],
  },
  {
    id: "sd17-spot-workers",
    title: "Спот для обработчиков",
    statement:
      "Обработка заказов идёт через очередь, и обработчики терпят прерывание: сообщение вернётся в очередь. Переведите обработчиков на спот (втрое дешевле), сделайте обработку идемпотентной и оставьте не меньше двух обработчиков. Загрузка — не выше 85%, очередь разбирается без отставания (пик 10 с, допустимо 5 с), бюджет — $1200 в месяц.",
    hint: "Три обработчика M тянут 1200 в секунду при нагрузке 900. На споте они стоят около 72 в месяц вместо 240.",
    workload: WL({ read: 300, write: 900, dataGB: 50, spikeSec: 10 }),
    palette: ["lb", "app", "queue", "worker", "db"],
    start: S(
      [users(), lb(), app(3), N("queue", "queue"), N("worker", "worker", { size: "M", instances: 3 }), N("db", "db", { size: "L" })],
      queued,
    ),
    goals: [
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "param", kind: "worker", key: "idempotent", op: "==", value: true },
      { k: "noSpof", kinds: ["worker"] },
      { k: "lag", max: 5 },
      { k: "capacity", max: 0.85 },
      { k: "cost", max: 1200 },
    ],
    solution: S(
      [users(), lb(), app(3), N("queue", "queue"), N("worker", "worker", { size: "M", instances: 3, pricing: "spot", idempotent: true }), N("db", "db", { size: "L" })],
      queued,
    ),
    show: ["worker.pricing", "worker.idempotent"],
  },
  {
    id: "sd17-rightsize",
    title: "Слишком большие серверы",
    statement:
      "Сервис получает 2400 запросов в секунду, а на схеме шесть серверов L (ёмкость 9000): они загружены на 27%, и счёт огромный. Подберите правильный размер: загрузка серверов не выше 80%, но не больше — бюджет $1100 в месяц на всю схему (база — M с репликой).",
    hint: "Два сервера L дают 3000 запросов — 80%. Четыре сервера M — 2800: 86% — слишком много.",
    workload: WL({ read: 2200, write: 200, dataGB: 40 }),
    palette: ["lb", "app", "db"],
    start: S([users(), lb(), N("app", "app", { size: "L", instances: 6, sessions: "external" }), N("db", "db", { size: "M", replicas: 1 })], web),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1100 },
    ],
    solution: S([users(), lb(), N("app", "app", { size: "L", instances: 2, sessions: "external" }), N("db", "db", { size: "M", replicas: 1 })], web),
  },
  {
    id: "sd17-cdn-cost",
    title: "CDN дешевле серверов",
    statement:
      "Сайт отдаёт 12 000 запросов в секунду статики через серверы приложения: их приходится держать с запасом. Поставьте CDN (≥90%) и пересчитайте парк: загрузка не выше 80%, бюджет — $450 в месяц на всю схему.",
    hint: "С CDN статика почти не доходит до серверов: двух серверов M хватит. CDN стоит 60 в месяц, а лишний сервер M — 120.",
    workload: WL({ static: 12000, read: 300, write: 50, dataGB: 10 }),
    palette: ["cdn", "lb", "app", "db"],
    start: S([users(), lb(), app(3), N("db", "db")], web),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 450 },
    ],
    solution: S([users(), N("cdn", "cdn", { ttl: 300 }), lb(), app(2), N("db", "db")], ["users>cdn>lb>app>db"]),
  },
  {
    id: "sd17-final",
    title: "Тот же сервис дешевле",
    statement:
      "Итоговое упражнение главы. Магазин: 6000 запросов в секунду (1000 статики через CDN, остальное динамика), заказы идут через очередь. Сократите счёт, не потеряв надёжность: резервный тариф для серверов приложения, спот для идемпотентных обработчиков, CDN (≥90%), схема переживает отказ зоны и сервера, загрузка не выше 80%, бюджет — $3000 в месяц.",
    hint: "Серверов M — девять в трёх зонах (после потери зоны шесть — 4200), резервный тариф; три обработчика M на споте в трёх зонах; база M с тремя репликами и автопереключением в трёх зонах (после потери зоны остаются две реплики — 6000 чтений).",
    workload: WL({ static: 10000, read: 3500, write: 400, dataGB: 80, spikeSec: 10 }),
    palette: ["cdn", "lb", "app", "queue", "worker", "db"],
    start: S(
      [users(), lb(), app(9, { zone: "single" }), N("queue", "queue"), N("worker", "worker", { size: "M", instances: 3 }), N("db", "db", { size: "M" })],
      queued,
    ),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "param", kind: "app", key: "pricing", op: "==", value: "reserved" },
      { k: "param", kind: "worker", key: "pricing", op: "==", value: "spot" },
      { k: "survive", fail: "zone" },
      { k: "survive", fail: "app" },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 3000 },
    ],
    solution: S(
      [
        users(),
        N("cdn", "cdn", { ttl: 300 }),
        lb(),
        app(9, { zone: "multi", pricing: "reserved" }),
        N("queue", "queue"),
        N("worker", "worker", { size: "M", instances: 3, pricing: "spot", idempotent: true, zone: "multi" }),
        N("db", "db", { size: "M", zone: "multi", replicas: 3, failover: true }),
      ],
      ["users>cdn>lb>app>db", "app>queue>worker>db"],
    ),
    show: ["app.pricing", "worker.pricing", "worker.idempotent"],
  },
];
