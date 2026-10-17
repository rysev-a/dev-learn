import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 10 «Микросервисы и API-шлюз»: шлюз на входе, разрезание монолита, база на сервис, доли трафика. */

const svc = (id: string, name: string, extra: Record<string, number | string | boolean> = {}) =>
  N(id, "app", { size: "M", instances: 2, sessions: "external", ...extra }, name);

export const CH10: SdScenario[] = [
  {
    id: "sd10-gateway",
    title: "Шлюз на входе",
    statement:
      "Монолит стоит за балансировщиком, а команда хочет единую входную точку: авторизацию, лимиты и маршрутизацию. Добавьте API-шлюз между пользователями и балансировщиком, зарезервируйте его (не меньше двух экземпляров), чтобы шлюз не стал единой точкой отказа: схема переживает отказ шлюза.",
    hint: "Пользователи → шлюз → балансировщик → серверы. Параметр «Экземпляры» шлюза — 2.",
    workload: WL({ read: 1200, write: 200, dataGB: 30 }),
    palette: ["gateway", "lb", "app", "db"],
    start: S([users(), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], ["users>lb>app>db"]),
    goals: [
      { k: "has", kind: "gateway" },
      { k: "link", from: "clients", to: "gateway" },
      { k: "noSpof", kinds: ["gateway"] },
      { k: "survive", fail: "gateway" },
      { k: "util", kind: "gateway", max: 0.5 },
    ],
    solution: S(
      [users(), N("gateway", "gateway", { instances: 2 }), N("lb", "lb"), N("app", "app", { size: "M", instances: 3, sessions: "external" }), N("db", "db", { size: "M" })],
      ["users>gateway>lb>app>db"],
    ),
  },
  {
    id: "sd10-split",
    title: "Разрезаем монолит",
    statement:
      "Монолит получает 2500 чтений и 300 записей в секунду, и единственная база перегружена. Разрежьте его на два сервиса: «Заказы» (70% трафика) и «Каталог» (30%) — каждый со своей базой. Шлюз делит трафик по весам сервисов (параметр «Доля трафика»: 7 и 3). Загрузка всех компонентов — не выше 80%.",
    hint: "«Заказы» — вес 7, база L (на ней 1750 чтений и 210 записей). «Каталог» — вес 3, база M (750 чтений, 90 записей). Серверы: у заказов четыре M (1960 запросов при ёмкости 2800), у каталога два M.",
    workload: WL({ read: 2500, write: 300, dataGB: 100 }),
    palette: ["gateway", "app", "db"],
    start: S(
      [users(), N("gateway", "gateway", { instances: 2 }), N("app", "app", { size: "M", instances: 5, sessions: "external" }, "Монолит"), N("db", "db", { size: "M" })],
      ["users>gateway>app>db"],
    ),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "has", kind: "app", min: 2 },
      { k: "has", kind: "db", min: 2 },
      { k: "success", min: 0.99 },
    ],
    solution: S(
      [
        users(),
        N("gateway", "gateway", { instances: 2 }),
        svc("orders", "Заказы", { instances: 4, weight: 7 }),
        svc("catalog", "Каталог", { instances: 2, weight: 3 }),
        N("db1", "db", { size: "L" }, "БД заказов"),
        N("db2", "db", { size: "M" }, "БД каталога"),
      ],
      ["users>gateway>orders>db1", "gateway>catalog>db2"],
    ),
    show: ["app.weight"],
  },
  {
    id: "sd10-weights",
    title: "Доли трафика между сервисами",
    statement:
      "Два сервиса за шлюзом: «Основной» (четыре сервера M) и «Дополнительный» (один сервер M). Трафик делится поровну, и маленький сервис перегружен. Настройте доли трафика (параметр «Доля трафика») пропорционально ёмкости: загрузка всех компонентов — не выше 90%.",
    hint: "Ёмкость 2800 против 700 — это 4 : 1. Поставьте вес 4 у основного и 1 у дополнительного.",
    workload: WL({ read: 2400, write: 400, dataGB: 60 }),
    palette: ["gateway", "app", "db"],
    start: S(
      [
        users(),
        N("gateway", "gateway", { instances: 2 }),
        svc("main", "Основной", { instances: 4 }),
        svc("extra", "Дополнительный", { instances: 1 }),
        N("db1", "db", { size: "L" }, "БД основного"),
        N("db2", "db", { size: "M" }, "БД дополнительного"),
      ],
      ["users>gateway>main>db1", "gateway>extra>db2"],
    ),
    goals: [
      { k: "capacity", max: 0.9 },
      { k: "success", min: 0.99 },
    ],
    solution: S(
      [
        users(),
        N("gateway", "gateway", { instances: 2 }),
        svc("main", "Основной", { instances: 4, weight: 4 }),
        svc("extra", "Дополнительный", { instances: 1, weight: 1 }),
        N("db1", "db", { size: "L" }, "БД основного"),
        N("db2", "db", { size: "M" }, "БД дополнительного"),
      ],
      ["users>gateway>main>db1", "gateway>extra>db2"],
    ),
    show: ["app.weight"],
  },
  {
    id: "sd10-own-db",
    title: "База на сервис",
    statement:
      "Два сервиса — «Заказы» и «Платежи» — ходят в одну общую базу, и выкладка одного регулярно ломает другой. Разделите хранилище: у каждого сервиса должна быть своя база. Базы средние, общая загрузка не выше 80%, бюджет $1900 в месяц.",
    hint: "Нужны две базы, каждая подключена только к своему сервису. Поставьте вторую базу и перенесите связь платежей на неё.",
    workload: WL({ read: 1500, write: 300, dataGB: 80 }),
    palette: ["gateway", "app", "db"],
    start: S(
      [users(), N("gateway", "gateway", { instances: 2 }), svc("orders", "Заказы", { instances: 3 }), svc("pay", "Платежи", { instances: 3 }), N("db", "db", { size: "L" }, "Общая БД")],
      ["users>gateway>orders>db", "gateway>pay>db"],
    ),
    goals: [
      { k: "has", kind: "db", min: 2 },
      { k: "capacity", max: 0.8 },
      { k: "cost", max: 1900 },
      { k: "success", min: 0.99 },
    ],
    solution: S(
      [
        users(),
        N("gateway", "gateway", { instances: 2 }),
        svc("orders", "Заказы", { instances: 3 }),
        svc("pay", "Платежи", { instances: 3 }),
        N("db", "db", { size: "M" }, "БД заказов"),
        N("db2", "db", { size: "M" }, "БД платежей"),
      ],
      ["users>gateway>orders>db", "gateway>pay>db2"],
    ),
  },
  {
    id: "sd10-final",
    title: "Магазин из трёх сервисов",
    statement:
      "Итоговое упражнение главы. Соберите магазин из трёх сервисов — «Каталог» (вес 5), «Заказы» (вес 3) и «Платежи» (вес 2), у каждого своя база. Нагрузка: 3000 чтений и 500 записей в секунду. Шлюз в двух экземплярах, загрузка не выше 80%, схема переживает отказ шлюза и сервера приложения, бюджет — $3000 в месяц.",
    hint: "Доли 5:3:2 — это 1750, 1050 и 700 запросов. Каталог: четыре сервера M и база L; заказы: три сервера M и база M; платежи: два сервера M и база M. У каждого сервиса запас на потерю одного экземпляра.",
    workload: WL({ read: 3000, write: 500, dataGB: 150 }),
    palette: ["gateway", "app", "db"],
    start: S(
      [users(), N("gateway", "gateway"), svc("cat", "Каталог", { instances: 3 }), N("db", "db", { size: "M" }, "Общая БД")],
      ["users>gateway>cat>db"],
    ),
    goals: [
      { k: "has", kind: "app", min: 3 },
      { k: "has", kind: "db", min: 3 },
      { k: "capacity", max: 0.8 },
      { k: "survive", fail: "gateway" },
      { k: "survive", fail: "app" },
      { k: "cost", max: 3000 },
    ],
    solution: S(
      [
        users(),
        N("gateway", "gateway", { instances: 2 }),
        svc("cat", "Каталог", { instances: 4, weight: 5 }),
        svc("ord", "Заказы", { instances: 3, weight: 3 }),
        svc("pay", "Платежи", { instances: 2, weight: 2 }),
        N("db1", "db", { size: "L" }, "БД каталога"),
        N("db2", "db", { size: "M" }, "БД заказов"),
        N("db3", "db", { size: "M" }, "БД платежей"),
      ],
      ["users>gateway>cat>db1", "gateway>ord>db2", "gateway>pay>db3"],
    ),
    show: ["app.weight"],
  },
];
