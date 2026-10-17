/* Лаборатория «Системный дизайн»: схема сервиса из компонентов и расчёт под заданной нагрузкой.
   Модель — упрощённая и детерминированная: всё считается формулами (см. engine.ts и справочник kinds.ts). */

export type Kind =
  | "clients"
  | "cdn"
  | "lb"
  | "gateway"
  | "limiter"
  | "app"
  | "cache"
  | "db"
  | "queue"
  | "worker"
  | "blob"
  | "search"
  | "ws"
  | "monitor";

export type ParamValue = number | string | boolean;

export interface SdNode {
  id: string;
  kind: Kind;
  name: string;
  x: number;
  y: number;
  params: Record<string, ParamValue>;
}

export interface SdEdge {
  from: string;
  to: string;
}

export interface SdState {
  nodes: SdNode[];
  edges: SdEdge[];
}

/** Нагрузка на сервис, запросов в секунду по классам, и данные */
export interface Workload {
  /** статика (картинки, скрипты): CDN или blob; иначе её отдаёт приложение */
  static: number;
  /** динамические чтения */
  read: number;
  /** записи */
  write: number;
  /** доля чтений, которые на самом деле поиск (идут в search; без него — тяжёлый запрос в БД) */
  searchShare?: number;
  /** объём данных, ГБ */
  dataGB: number;
  /** доля данных, которую читают часто (рабочий набор), 0..1 */
  hotSet: number;
  /** доля запросов на самый «горячий» ключ (0..1): перекос шардов */
  hotKey?: number;
  /** одновременных соединений WebSocket */
  connections?: number;
  /** сообщений в секунду на соединение (для ws) */
  msgPerConn?: number;
  /** сообщение через очередь нужно доставить за N секунд после пика (для lag) */
  spikeSec?: number;
  /** ключи шардирования растут монотонно (время, автоинкремент): при range-шардировании все записи в один шард */
  monotonic?: boolean;
  /** среднее число подписчиков автора (для ленты) */
  fanout?: number;
}

export type FailKind = Kind | "zone" | "region" | "deploy";

export interface EvalOptions {
  /** сломать по одному экземпляру каждого компонента этого вида (или всю зону) */
  fail?: FailKind | undefined;
  /** отключённые вручную узлы (клик по узлу в интерфейсе) */
  down?: string[] | undefined;
}

export type NodeStatus = "idle" | "ok" | "warm" | "hot" | "over" | "down";

export interface NodeLoad {
  /** входящая нагрузка, усл. запросов в секунду */
  load: number;
  /** ёмкость (то, что узел вытягивает), усл. запросов в секунду */
  cap: number;
  util: number;
  units: number;
  status: NodeStatus;
  note?: string;
}

export interface Result {
  loads: Record<string, NodeLoad>;
  /** средняя и «хвостовая» задержка пользовательского запроса, мс */
  p50: number;
  p99: number;
  /** доля успешных запросов, 0..1 (с учётом перегрузок) */
  success: number;
  /** доступность схемы по компонентам, 0..1 */
  availability: number;
  cost: number;
  hit: number | null;
  cdnHit: number | null;
  /** отставание очереди после пика, секунд (null — очереди нет) */
  lagSec: number | null;
  /** отставание реплик, мс */
  replicaLagMs: number | null;
  /** максимальная доля данных на одном шарде, 0..1 */
  maxShardShare: number | null;
  /** есть ли путь от клиентов до обработки запросов */
  entry: boolean;
  /** предупреждения: лишние рёбра, пустые связи, ... */
  warnings: string[];
}

export type Goal =
  | { k: "capacity"; max: number }
  | { k: "util"; kind: Kind; max: number }
  | { k: "p99"; max: number }
  | { k: "p50"; max: number }
  | { k: "success"; min: number }
  | { k: "availability"; min: number }
  | { k: "cost"; max: number }
  | { k: "has"; kind: Kind; min?: number }
  | { k: "lacks"; kind: Kind }
  | { k: "link"; from: Kind; to: Kind }
  | { k: "hit"; min: number }
  | { k: "cdnHit"; min: number }
  | { k: "survive"; fail: FailKind }
  | { k: "param"; kind: Kind; key: string; op: ">=" | "<=" | "==" | "!="; value: ParamValue }
  | { k: "lag"; max: number }
  | { k: "replicaLag"; max: number }
  | { k: "shardShare"; max: number }
  | { k: "noSpof"; kinds: Kind[] };

export interface GoalResult {
  ok: boolean;
  text: string;
  detail: string;
}

export interface SdScenario {
  id: string;
  title: string;
  /** условие упражнения (абзац) */
  statement: string;
  hint: string;
  workload: Workload;
  /** какие компоненты можно добавлять с панели */
  palette: Kind[];
  /** исходная схема */
  start: SdState;
  goals: Goal[];
  /** эталонная схема (проверяется самопроверкой sd:check) */
  solution: SdState;
  /** сколько узлов можно держать на схеме (по умолчанию 14) */
  maxNodes?: number;
  /** какие дополнительные параметры показывать: "app.retries" и т. п. */
  show?: string[];
}
