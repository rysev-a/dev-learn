import type { Kind, ParamValue } from "./types.ts";

/* Справочник компонентов: русские названия, настраиваемые параметры, значения по умолчанию.
   Числа ёмкости, цены и задержек — в engine.ts (таблица REF показывается ученику в лаборатории). */

export interface ParamSpec {
  key: string;
  label: string;
  type: "int" | "select" | "bool";
  min?: number;
  max?: number;
  options?: { value: string | number; label: string }[];
  default: ParamValue;
  /** подсказка под полем */
  help?: string;
  /** false — показывается только в упражнениях, где параметр перечислен в `show` */
  basic?: boolean;
}

export interface KindSpec {
  kind: Kind;
  label: string;
  /** одна строка: чем занимается компонент */
  about: string;
  params: ParamSpec[];
  /** колонка раскладки слева направо */
  col: number;
}

const SIZE: ParamSpec = {
  key: "size",
  label: "Размер",
  type: "select",
  options: [
    { value: "S", label: "S — малый" },
    { value: "M", label: "M — средний" },
    { value: "L", label: "L — большой" },
  ],
  default: "S",
};

const ZONE: ParamSpec = {
  key: "zone",
  label: "Размещение",
  type: "select",
  options: [
    { value: "single", label: "одна зона" },
    { value: "multi", label: "три зоны региона" },
    { value: "regions", label: "два региона" },
  ],
  default: "single",
  help: "отказ зоны: «одна зона» теряет всё, остальные — треть; отказ региона: два региона теряют половину",
};

export const KINDS: Record<Kind, KindSpec> = {
  clients: { kind: "clients", label: "Пользователи", about: "источник нагрузки", params: [], col: 0 },
  cdn: {
    kind: "cdn",
    label: "CDN",
    about: "раздаёт статику с ближайших серверов",
    col: 1,
    params: [
      {
        key: "ttl",
        label: "TTL, с",
        type: "select",
        options: [
          { value: 30, label: "30" },
          { value: 300, label: "300" },
          { value: 3600, label: "3600" },
        ],
        default: 300,
        help: "чем больше TTL, тем выше доля попаданий",
      },
    ],
  },
  limiter: {
    kind: "limiter",
    label: "Ограничитель",
    about: "пропускает не больше N запросов в секунду",
    col: 2,
    params: [{ key: "limit", label: "Предел, запр/с", type: "int", min: 100, max: 50000, default: 2000 }],
  },
  gateway: {
    kind: "gateway",
    label: "API-шлюз",
    about: "вход: авторизация, маршрутизация, лимиты",
    col: 2,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 4, default: 1 }],
  },
  lb: {
    kind: "lb",
    label: "Балансировщик",
    about: "делит запросы между серверами",
    col: 3,
    params: [
      { key: "instances", label: "Экземпляры", type: "int", min: 1, max: 3, default: 1 },
      {
        key: "layer",
        label: "Уровень",
        type: "select",
        options: [
          { value: "L4", label: "L4 (TCP)" },
          { value: "L7", label: "L7 (HTTP)" },
        ],
        default: "L4",
      },
    ],
  },
  ws: {
    kind: "ws",
    label: "WebSocket-шлюз",
    about: "держит постоянные соединения",
    col: 3,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 30, default: 1 }],
  },
  app: {
    kind: "app",
    label: "Сервер приложения",
    about: "бизнес-логика без состояния",
    col: 4,
    params: [
      { key: "instances", label: "Экземпляры", type: "int", min: 1, max: 30, default: 1 },
      SIZE,
      {
        key: "sessions",
        label: "Сессии",
        type: "select",
        options: [
          { value: "local", label: "в памяти сервера" },
          { value: "external", label: "во внешнем хранилище" },
        ],
        default: "local",
      },
      ZONE,
      { key: "weight", label: "Доля трафика", type: "int", min: 1, max: 10, default: 1, basic: false, help: "вес сервиса при делении трафика между сервисами" },
      { key: "idempotency", label: "Ключи идемпотентности", type: "bool", default: false, basic: false },
      { key: "retries", label: "Повторы к БД", type: "int", min: 0, max: 3, default: 0, basic: false, help: "повторы без паузы усиливают перегрузку" },
      { key: "breaker", label: "Автомат разрыва", type: "bool", default: false, basic: false, help: "обрывает повторы, когда база перегружена" },
      {
        key: "feed",
        label: "Лента",
        type: "select",
        options: [
          { value: "pull", label: "pull — собирать при чтении" },
          { value: "push", label: "push — раскладывать при записи" },
          { value: "hybrid", label: "гибрид" },
        ],
        default: "pull",
        basic: false,
      },
      {
        key: "deploy",
        label: "Выкладка",
        type: "select",
        options: [
          { value: "all", label: "всё сразу" },
          { value: "rolling", label: "по одному (rolling)" },
          { value: "bluegreen", label: "blue/green" },
        ],
        default: "all",
        basic: false,
        help: "blue/green держит вторую копию — расход ×2",
      },
      {
        key: "pricing",
        label: "Тариф",
        type: "select",
        options: [
          { value: "ondemand", label: "по требованию" },
          { value: "reserved", label: "резерв (−40%)" },
          { value: "spot", label: "спот (−70%, прерывается)" },
        ],
        default: "ondemand",
        basic: false,
      },
    ],
  },
  cache: {
    kind: "cache",
    label: "Кэш",
    about: "быстрая память для горячих данных",
    col: 5,
    params: [
      { key: "sizeGB", label: "Память, ГБ", type: "int", min: 1, max: 128, default: 4 },
      {
        key: "ttl",
        label: "TTL, с",
        type: "select",
        options: [
          { value: 30, label: "30" },
          { value: 300, label: "300" },
          { value: 3600, label: "3600" },
        ],
        default: 300,
      },
      {
        key: "policy",
        label: "Политика записи",
        type: "select",
        options: [
          { value: "aside", label: "cache-aside" },
          { value: "through", label: "write-through" },
          { value: "back", label: "write-back" },
        ],
        default: "aside",
        help: "write-back снимает нагрузку записи с БД, но данные могут пропасть",
        basic: false,
      },
      { key: "replicas", label: "Реплики", type: "int", min: 0, max: 2, default: 0 },
      ZONE,
    ],
  },
  queue: {
    kind: "queue",
    label: "Очередь",
    about: "буфер между производителями и обработчиками",
    col: 5,
    params: [
      { key: "partitions", label: "Партиции", type: "int", min: 1, max: 16, default: 1 },
      { key: "dlq", label: "Очередь недоставленных", type: "bool", default: false, basic: false },
    ],
  },
  worker: {
    kind: "worker",
    label: "Обработчик",
    about: "разбирает очередь",
    col: 6,
    params: [
      { key: "instances", label: "Экземпляры", type: "int", min: 1, max: 30, default: 1 },
      {
        key: "size",
        label: "Размер",
        type: "select",
        options: [
          { value: "S", label: "S — малый" },
          { value: "M", label: "M — средний" },
        ],
        default: "S",
      },
      ZONE,
      { key: "idempotent", label: "Идемпотентная обработка", type: "bool", default: false, basic: false, help: "повторная доставка не портит данные" },
      {
        key: "pricing",
        label: "Тариф",
        type: "select",
        options: [
          { value: "ondemand", label: "по требованию" },
          { value: "reserved", label: "резерв (−40%)" },
          { value: "spot", label: "спот (−70%)" },
        ],
        default: "ondemand",
        basic: false,
      },
    ],
  },
  db: {
    kind: "db",
    label: "База данных",
    about: "постоянное хранилище",
    col: 7,
    params: [
      SIZE,
      { key: "replicas", label: "Реплики на шард", type: "int", min: 0, max: 5, default: 0 },
      { key: "shards", label: "Шарды", type: "int", min: 1, max: 16, default: 1 },
      {
        key: "failover",
        label: "Автопереключение",
        type: "bool",
        default: false,
        help: "при отказе лидера реплика занимает его место",
      },
      {
        key: "engine",
        label: "Тип",
        type: "select",
        options: [
          { value: "sql", label: "SQL" },
          { value: "nosql", label: "NoSQL" },
        ],
        default: "sql",
      },
      {
        key: "sync",
        label: "Репликация",
        type: "select",
        options: [
          { value: "async", label: "асинхронная" },
          { value: "sync", label: "синхронная" },
        ],
        default: "async",
        basic: false,
        help: "синхронная: реплики не отстают, но запись медленнее",
      },
      {
        key: "shardKey",
        label: "Ключ шардирования",
        type: "select",
        options: [
          { value: "hash", label: "хеш" },
          { value: "range", label: "диапазон" },
        ],
        default: "hash",
        basic: false,
      },
      ZONE,
    ],
  },
  blob: {
    kind: "blob",
    label: "Объектное хранилище",
    about: "файлы и медиа",
    col: 7,
    params: [
      {
        key: "tier",
        label: "Класс хранения",
        type: "select",
        options: [
          { value: "hot", label: "горячее ($23/ТБ)" },
          { value: "mix", label: "горячее + холодное ($10/ТБ)" },
          { value: "cold", label: "холодное ($4/ТБ)" },
        ],
        default: "hot",
        basic: false,
        help: "холодное дешевле, но доступ к объектам медленнее",
      },
    ],
  },
  search: {
    kind: "search",
    label: "Поиск",
    about: "полнотекстовый индекс",
    col: 7,
    params: [
      { key: "shards", label: "Шарды", type: "int", min: 1, max: 16, default: 1 },
      { key: "replicas", label: "Реплики", type: "int", min: 1, max: 6, default: 1 },
    ],
  },
  monitor: { kind: "monitor", label: "Мониторинг", about: "метрики, журналы, оповещения", params: [], col: 6 },
  auth: {
    kind: "auth",
    label: "Сервис входа",
    about: "аутентификация и права: проверка токенов и сессий",
    col: 5,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 20, default: 1 }],
  },
  geo: {
    kind: "geo",
    label: "Геосервис",
    about: "геопоиск и положения в памяти: ближайшие водители, курьеры, рестораны",
    col: 5,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 30, default: 1 }],
  },
  ml: {
    kind: "ml",
    label: "Сервис ранжирования",
    about: "модель рекомендаций и оценок: дорогие вычисления на запрос",
    col: 5,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 20, default: 1 }],
  },
  pay: {
    kind: "pay",
    label: "Платёжный шлюз",
    about: "внешний платёжный провайдер: медленный и дорогой вызов",
    col: 5,
    params: [{ key: "instances", label: "Каналы провайдера", type: "int", min: 1, max: 4, default: 1 }],
  },
  stream: {
    kind: "stream",
    label: "Поток событий",
    about: "журнал событий с партициями: каждый потребитель получает свою копию",
    col: 5,
    params: [{ key: "partitions", label: "Партиции", type: "int", min: 1, max: 32, default: 1 }],
  },
  notify: {
    kind: "notify",
    label: "Уведомления",
    about: "рассылка пушей и писем из очереди или потока",
    col: 6,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 20, default: 1 }],
  },
  analytics: {
    kind: "analytics",
    label: "Аналитика",
    about: "хранилище событий для отчётов и метрик продукта",
    col: 6,
    params: [{ key: "instances", label: "Экземпляры", type: "int", min: 1, max: 10, default: 1 }],
  },
};

export function defaultParams(kind: Kind): Record<string, ParamValue> {
  return Object.fromEntries(KINDS[kind].params.map((p) => [p.key, p.default]));
}

export const KIND_ORDER: Kind[] = [
  "cdn",
  "limiter",
  "gateway",
  "lb",
  "ws",
  "app",
  "cache",
  "queue",
  "worker",
  "db",
  "blob",
  "search",
  "auth",
  "geo",
  "ml",
  "pay",
  "stream",
  "notify",
  "analytics",
  "monitor",
];
