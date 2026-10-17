import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 3 «Кэширование и CDN»: статика и CDN, доля попаданий, TTL, политика записи, отказ кэша. */

export const CH03: SdScenario[] = [
  {
    id: "sd03-cdn",
    title: "Статика через CDN",
    statement:
      "Сайт раздаёт 20 000 запросов в секунду статики (картинки, скрипты) и 400 динамических чтений при 50 записях. Сейчас статику отдают серверы приложения, и они перегружены. Поставьте перед схемой CDN, чтобы большая часть статики не доходила до серверов: загрузка не выше 80%, CDN отдаёт не меньше 90% статики.",
    hint: "CDN соединяется с пользователями и дальше передаёт запросы балансировщику. Параметр TTL у CDN — время жизни копий: 300 секунд даёт 90% попаданий.",
    workload: WL({ static: 20000, read: 400, write: 50, dataGB: 20 }),
    palette: ["cdn", "lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cdnHit", min: 0.9 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), N("cdn", "cdn", { ttl: 300 }), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>cdn>lb>app>db"]),
  },
  {
    id: "sd03-cdn-ttl",
    title: "Время жизни в CDN",
    statement:
      "CDN уже стоит, но с TTL в 30 секунд: копии быстро устаревают, доля попаданий низкая, а серверы приложения перегружены промахами. Подберите TTL так, чтобы CDN отдавал не меньше 90% статики. Заодно подумайте: что вы делаете с устареванием? (В реальности — версия в имени файла.)",
    hint: "Допустимые значения TTL: 30, 300 и 3600 секунд. Чем больше значение, тем выше доля попаданий.",
    workload: WL({ static: 15000, read: 300, write: 40, dataGB: 20 }),
    palette: ["cdn", "lb", "app", "db"],
    start: S([users(), N("cdn", "cdn", { ttl: 30 }), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>cdn>lb>app>db"]),
    goals: [
      { k: "cdnHit", min: 0.9 },
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), N("cdn", "cdn", { ttl: 300 }), N("lb", "lb"), N("app", "app", { instances: 3 }), N("db", "db", { size: "M" })], ["users>cdn>lb>app>db"]),
  },
  {
    id: "sd03-cache",
    title: "Кэш для чтений",
    statement:
      "Чтений стало 1800 в секунду при 60 записях, а база S тянет лишь 1000 чтений. Рабочий набор — 10 ГБ (из 100 ГБ данных). Добавьте кэш (cache-aside) между приложением и базой: доля попаданий не меньше 85%, загрузка не выше 80%, а стоимость не больше $740 в месяц — дешевле, чем просто взять базу M.",
    hint: "Попадание зависит от размера кэша относительно рабочего набора (10 ГБ) и TTL. Кэш на 9 ГБ с TTL 3600 даёт около 88%.",
    workload: WL({ read: 1800, write: 60, dataGB: 100, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 4, sessions: "external" }), N("db", "db")], ["users>lb>app>db"]),
    goals: [
      { k: "hit", min: 0.85 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 740 },
    ],
    solution: S(
      [users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 4, sessions: "external" }), N("cache", "cache", { sizeGB: 9, ttl: 3600 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
  },
  {
    id: "sd03-size",
    title: "Размер кэша",
    statement:
      "Кэш работает, но его доля попаданий всего около 55%, и база на пределе. Рабочий набор — 8 ГБ. Подберите размер и время жизни кэша так, чтобы кэш отдавал не меньше 85% чтений, но не тратьте лишнего: бюджет на кэш ограничен общей суммой $700.",
    hint: "Сейчас кэш 2 ГБ с TTL 30. Увеличьте память до размера рабочего набора и поставьте TTL подольше.",
    workload: WL({ read: 1500, write: 50, dataGB: 80, hotSet: 0.1 }),
    palette: ["lb", "app", "cache", "db"],
    start: S(
      [users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("cache", "cache", { sizeGB: 2, ttl: 30 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
    goals: [
      { k: "hit", min: 0.85 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 700 },
    ],
    solution: S(
      [users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("cache", "cache", { sizeGB: 8, ttl: 3600 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
  },
  {
    id: "sd03-writeback",
    title: "Много записей: write-back",
    statement:
      "Сервис счётчиков получает 800 чтений и 700 записей в секунду. База M выдерживает только 600 записей, поэтому она перегружена. Потеря нескольких секунд счётчиков допустима. Смените политику записи кэша, чтобы база выдерживала нагрузку, не увеличивая её размер.",
    hint: "Политика write-back накапливает записи в кэше и сбрасывает в базу пачками — так в базу попадает лишь часть записей. Параметр политики показывается в настройках кэша.",
    workload: WL({ read: 800, write: 700, dataGB: 10, hotSet: 0.3 }),
    palette: ["lb", "app", "cache", "db"],
    start: S(
      [users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("cache", "cache", { sizeGB: 4, ttl: 300 }), N("db", "db", { size: "M" })],
      ["users>lb>app>db", "app>cache"],
    ),
    goals: [
      { k: "capacity", max: 0.85 },
      { k: "param", kind: "cache", key: "policy", op: "==", value: "back" },
      { k: "param", kind: "db", key: "size", op: "==", value: "M" },
    ],
    solution: S(
      [users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("cache", "cache", { sizeGB: 4, ttl: 300, policy: "back" }), N("db", "db", { size: "M" })],
      ["users>lb>app>db", "app>cache"],
    ),
    show: ["cache.policy"],
  },
  {
    id: "sd03-cache-ha",
    title: "Что, если кэш пропадёт",
    statement:
      "Схема держится на кэше: он принимает 90% чтений, а база рассчитана только на оставшиеся 10%. При отказе кэша база падает. Сделайте схему устойчивой: она должна переживать отказ кэша (проверка «Отказ» → «кэша»), не имея единых точек отказа среди кэша и серверов приложения.",
    hint: "У кэша есть параметр «Реплики». С репликой после отказа основного узла кэш продолжает работать.",
    workload: WL({ read: 2400, write: 60, dataGB: 100, hotSet: 0.05 }),
    palette: ["lb", "app", "cache", "db"],
    start: S(
      [users(), N("lb", "lb", { instances: 2 }), N("app", "app", { size: "M", instances: 4, sessions: "external" }), N("cache", "cache", { sizeGB: 8, ttl: 3600 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
    goals: [
      { k: "survive", fail: "cache" },
      { k: "noSpof", kinds: ["cache", "app"] },
      { k: "hit", min: 0.85 },
    ],
    solution: S(
      [users(), N("lb", "lb", { instances: 2 }), N("app", "app", { size: "M", instances: 4, sessions: "external" }), N("cache", "cache", { sizeGB: 8, ttl: 3600, replicas: 1 }), N("db", "db")],
      ["users>lb>app>db", "app>cache"],
    ),
  },
  {
    id: "sd03-final",
    title: "Сайт со статикой и кэшем",
    statement:
      "Итоговое упражнение главы. Магазин: 10 000 запросов статики, 2500 чтений и 100 записей в секунду, 200 ГБ данных, рабочий набор 10 ГБ. Соберите схему: CDN (≥90% статики), кэш (≥85% чтений), загрузка не выше 80%, схема переживает отказ кэша и сервера, бюджет — $1100 в месяц.",
    hint: "CDN с TTL 300, кэш около 10 ГБ с TTL 3600 и репликой, пять серверов M (на отказ одного останется 2800), база S хватит (кэш снимает чтения), балансировщик.",
    workload: WL({ static: 10000, read: 2500, write: 100, dataGB: 200, hotSet: 0.05 }),
    palette: ["cdn", "lb", "app", "cache", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { instances: 2 }), N("db", "db")], ["users>lb>app>db"]),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "cdnHit", min: 0.9 },
      { k: "hit", min: 0.85 },
      { k: "survive", fail: "cache" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 1100 },
    ],
    solution: S(
      [
        users(),
        N("cdn", "cdn", { ttl: 300 }),
        N("lb", "lb"),
        N("app", "app", { size: "M", instances: 5, sessions: "external" }),
        N("cache", "cache", { sizeGB: 10, ttl: 3600, replicas: 1 }),
        N("db", "db"),
      ],
      ["users>cdn>lb>app>db", "app>cache"],
    ),
  },
];
