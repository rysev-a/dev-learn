import { N, S, WL, users } from "./helpers.ts";
import type { SdScenario } from "../types.ts";

/* Глава 4 «Базы данных: репликация»: реплики под чтения, переключение лидера, отставание и синхронность. */

const chain = ["users>lb>app>db"];
const app = (n = 5) => N("app", "app", { size: "M", instances: n, sessions: "external" });

export const CH04: SdScenario[] = [
  {
    id: "sd04-replicas",
    title: "Реплики под чтения",
    statement:
      "Чтений 2500 в секунду при 100 записях. База S тянет 1000 чтений, и она перегружена. Кэша нет. Добавьте реплики (параметр базы «Реплики на шард»): загрузка не выше 80%, стоимость не больше $1200 в месяц. Подумайте: что дешевле — реплики или база покрупнее?",
    hint: "Каждая реплика S добавляет 1000 чтений. Нужно 4 реплики: 2500 / 4000 = 63%. База M с одной репликой даёт 83% — не хватает.",
    workload: WL({ read: 2500, write: 100, dataGB: 50 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), app(), N("db", "db")], chain),
    goals: [
      { k: "capacity", max: 0.8 },
      { k: "success", min: 0.99 },
      { k: "cost", max: 1200 },
    ],
    solution: S([users(), N("lb", "lb"), app(), N("db", "db", { replicas: 4 })], chain),
  },
  {
    id: "sd04-failover",
    title: "Автопереключение лидера",
    statement:
      "Сейчас у базы есть реплика, но при отказе лидера ничего не происходит: запись останавливается, пока администратор не проснётся. Включите автопереключение, чтобы схема переживала отказ лидера базы данных.",
    hint: "У базы есть параметр «Автопереключение» и «Реплики на шард». Нужна хотя бы одна реплика и включённое автопереключение.",
    workload: WL({ read: 400, write: 80, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M", replicas: 1 })], chain),
    goals: [
      { k: "survive", fail: "db" },
      { k: "noSpof", kinds: ["db"] },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M", replicas: 1, failover: true })], chain),
  },
  {
    id: "sd04-lag",
    title: "Отставание реплик",
    statement:
      "Пользователи видят старые данные: реплики отстают. Запись нагружает базу S сильнее всего: отставание реплик больше 100 мс. Уменьшите отставание до 50 мс, не переходя на синхронную репликацию — увеличьте базу, чтобы на ней записи занимали меньше времени.",
    hint: "Отставание асинхронных реплик растёт с загрузкой записи: на базе M при тех же записях оно заметно меньше.",
    workload: WL({ read: 600, write: 150, dataGB: 30 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb"), app(3), N("db", "db", { replicas: 2 })], chain),
    goals: [
      { k: "replicaLag", max: 50 },
      { k: "capacity", max: 0.9 },
      { k: "param", kind: "db", key: "sync", op: "==", value: "async" },
    ],
    solution: S([users(), N("lb", "lb"), app(3), N("db", "db", { size: "M", replicas: 2 })], chain),
    show: ["db.sync"],
  },
  {
    id: "sd04-sync",
    title: "Синхронная репликация",
    statement:
      "Платёжный сервис не может потерять подтверждённую запись: после отказа лидера реплика обязана иметь все данные. Включите синхронную репликацию, чтобы отставание было нулевым, но уложитесь в p99 не больше 140 мс.",
    hint: "Параметр «Репликация» у базы: «синхронная». Она добавляет несколько миллисекунд к записи. Серверы не должны быть перегружены, иначе p99 вырастет.",
    workload: WL({ read: 300, write: 120, dataGB: 20 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M", replicas: 1, failover: true })], chain),
    goals: [
      { k: "replicaLag", max: 0 },
      { k: "p99", max: 140 },
      { k: "survive", fail: "db" },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M", replicas: 1, failover: true, sync: "sync" })], chain),
    show: ["db.sync"],
  },
  {
    id: "sd04-nines",
    title: "Четыре девятки",
    statement:
      "Договор требует доступности не ниже 99,99%. Балансировщик и серверы уже зарезервированы, но база одна — именно она тянет доступность вниз. Добавьте реплику и автопереключение так, чтобы доступность схемы достигла 99,99%.",
    hint: "Доступность одной базы — 99,9%. Две копии с автопереключением дают около 99,9999%.",
    workload: WL({ read: 500, write: 80, dataGB: 30 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M" })], chain),
    goals: [
      { k: "availability", min: 0.9999 },
      { k: "survive", fail: "db" },
      { k: "success", min: 0.99 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { instances: 3, sessions: "external" }), N("db", "db", { size: "M", replicas: 1, failover: true })], chain),
  },
  {
    id: "sd04-lead-size",
    title: "Реплика слабее лидера",
    statement:
      "Ограничение «реплика не слабее лидера» нельзя показать прямой настройкой, но можно проверить по загрузке: в этой схеме база L с репликами, и после отказа лидера оставшиеся реплики должны держать нагрузку. Подберите число реплик так, чтобы схема пережила отказ базы с запасом: загрузка при отказе не больше 100%, в обычном режиме — до 70%.",
    hint: "При отказе одной реплики оставшиеся делят чтения. Две реплики L: чтения 12 000 / 16 000 = 75% — много; три реплики: после потери одной остаётся две — 75% при отказе и 50% в норме.",
    workload: WL({ read: 12000, write: 600, dataGB: 300 }),
    palette: ["lb", "app", "db"],
    start: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { size: "L", instances: 12, sessions: "external" }), N("db", "db", { size: "L", replicas: 1, failover: true })], chain),
    goals: [
      { k: "capacity", max: 0.7 },
      { k: "survive", fail: "db" },
      { k: "cost", max: 5500 },
    ],
    solution: S([users(), N("lb", "lb", { instances: 2 }), N("app", "app", { size: "L", instances: 12, sessions: "external" }), N("db", "db", { size: "L", replicas: 3, failover: true })], chain),
  },
];
