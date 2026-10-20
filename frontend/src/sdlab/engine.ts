import { defaultParams } from "./kinds.ts";
import type {
  DepKind,
  EvalOptions,
  Kind,
  NodeLoad,
  NodeStatus,
  ParamValue,
  Result,
  SdNode,
  SdState,
  Workload,
} from "./types.ts";

/* Расчёт схемы под нагрузкой. Запросы трёх классов — статика, чтение, запись — проходят по схеме по
   «деревьям решений» (кэш: попал/промахнулся, очередь: запись уходит в буфер, CDN: отдаёт статику).
   Для каждого пути известны вероятность и список узлов. Из путей считаются нагрузка узлов, затем
   задержка, доля успешных ответов и доступность. Всё — формулы, без случайности. */

export const REF = {
  app: { cap: { S: 300, M: 700, L: 1500 }, cost: { S: 60, M: 120, L: 240 }, avail: 0.995 },
  lb: { cap: 20000, cost: 25, avail: 0.9995 },
  gateway: { cap: 8000, cost: 40, avail: 0.999 },
  limiter: { cap: 100000, cost: 15, avail: 0.9995 },
  cdn: { cap: 1000000, cost: 60, avail: 0.9999 },
  cache: { cap: 60000, costPerGB: 12, avail: 0.999 },
  db: {
    read: { S: 1000, M: 3000, L: 8000 },
    write: { S: 200, M: 600, L: 1500 },
    cost: { S: 100, M: 250, L: 600 },
    avail: 0.999,
    nosql: 1.8,
  },
  queue: { capPerPartition: 20000, cost: 60, costPerPartition: 10, avail: 0.9995 },
  worker: { cap: { S: 150, M: 400 }, cost: { S: 40, M: 80 }, avail: 0.995 },
  blob: { cap: 100000, cost: 25, avail: 0.9999 },
  /** класс хранения объектов: цена за ТБ в месяц и задержка доступа, мс */
  blobTier: { hot: { price: 23, lat: 45 }, mix: { price: 10, lat: 70 }, cold: { price: 4, lat: 150 } } as Record<string, { price: number; lat: number }>,
  auth: { cap: 4000, cost: 50, avail: 0.999 },
  geo: { cap: 6000, cost: 90, avail: 0.999 },
  ml: { cap: 300, cost: 200, avail: 0.995 },
  pay: { cap: 400, cost: 40, avail: 0.999 },
  notify: { cap: 1500, cost: 45, avail: 0.999 },
  analytics: { cap: 6000, cost: 140, avail: 0.999 },
  stream: { capPerPartition: 50000, cost: 100, costPerPartition: 15, avail: 0.9999 },
  search: { cap: 1200, cost: 150, maxGBPerShard: 40, avail: 0.999 },
  ws: { cap: 15000, cost: 90, avail: 0.995 },
  monitor: { cost: 40 },
  /** вес статического запроса, обслуженного самим приложением */
  staticWeight: 0.1,
  /** во сколько раз тяжелее запрос «поиск» в базе без индекса */
  heavySearch: 5,
  /** какую долю записей оставляет в БД write-back кэш */
  writeBack: 0.4,
  /** задержка узла, мс */
  lat: {
    cdn: 12,
    limiter: 1,
    gateway: 4,
    lb: { L4: 1.5, L7: 3 },
    ws: 5,
    app: 25,
    appStatic: 6,
    cache: 1.5,
    queue: 4,
    blob: 45,
    search: 30,
    dbRead: 9,
    dbWrite: 16,
    auth: 6,
    geo: 4,
    ml: 35,
    pay: 180,
  },
};

export const DEPS: DepKind[] = ["auth", "geo", "ml", "pay"];

const VALID: Record<Kind, Kind[]> = {
  clients: ["cdn", "limiter", "gateway", "lb", "ws", "app"],
  cdn: ["limiter", "gateway", "lb", "app", "blob"],
  limiter: ["gateway", "lb", "app", "ws"],
  gateway: ["limiter", "lb", "app", "ws"],
  lb: ["limiter", "gateway", "lb", "app", "ws"],
  ws: ["app", "queue", "stream"],
  app: ["cache", "db", "queue", "blob", "search", "stream", "auth", "geo", "ml", "pay"],
  queue: ["worker", "notify"],
  stream: ["worker", "notify", "analytics"],
  auth: [],
  geo: [],
  ml: [],
  pay: [],
  notify: [],
  analytics: [],
  worker: ["db", "blob", "search"],
  cache: [],
  db: [],
  blob: [],
  search: [],
  monitor: [],
};

export const canLink = (a: Kind, b: Kind) => VALID[a].includes(b);

/* ---------- параметры ---------- */

export function param(n: SdNode, key: string): ParamValue {
  const v = n.params[key];
  if (v !== undefined) return v;
  return defaultParams(n.kind)[key] ?? 0;
}
const pn = (n: SdNode, k: string): number => {
  const v = param(n, k);
  return typeof v === "number" ? v : Number(v) || 0;
};
const ps = (n: SdNode, k: string): string => String(param(n, k));
const pb = (n: SdNode, k: string): boolean => param(n, k) === true;

/** сколько экземпляров заявлено на схеме */
export function baseUnits(n: SdNode): number {
  switch (n.kind) {
    case "app":
    case "lb":
    case "gateway":
    case "worker":
    case "ws":
    case "auth":
    case "geo":
    case "ml":
    case "pay":
    case "notify":
    case "analytics":
      return pn(n, "instances");
    case "db":
      return pn(n, "shards");
    case "search":
      return pn(n, "replicas");
    default:
      return 1;
  }
}

/** сколько экземпляров работает при заданных отказах */
function workingUnits(n: SdNode, opts: EvalOptions): number {
  if (opts.down?.includes(n.id)) return 0;
  const base = baseUnits(n);
  const f = opts.fail;
  if (!f) return base;
  const zoneAware = ["app", "cache", "worker", "db"].includes(n.kind);
  if (f === "zone" || f === "region") {
    if (!zoneAware) return base;
    const z = ps(n, "zone");
    const spare = n.kind === "db" ? pn(n, "replicas") > 0 && pb(n, "failover") : n.kind === "cache" ? pn(n, "replicas") > 0 : false;
    if (f === "zone" && z !== "single") return spare ? Math.max(1, base) : Math.max(0, base - Math.ceil(base / 3));
    if (f === "region" && z === "regions") return spare ? Math.max(1, base) : Math.max(0, base - Math.ceil(base / 2));
    return 0;
  }
  if (f === "deploy") {
    if (n.kind !== "app") return base;
    const d = ps(n, "deploy");
    return d === "all" ? 0 : d === "rolling" ? Math.max(0, base - 1) : base;
  }
  if (f !== n.kind) return base;
  switch (n.kind) {
    case "app":
    case "lb":
    case "gateway":
    case "worker":
    case "ws":
    case "search":
    case "auth":
    case "geo":
    case "ml":
    case "pay":
    case "notify":
    case "analytics":
      return Math.max(0, base - 1);
    case "cache":
      return pn(n, "replicas") > 0 ? 1 : 0;
    case "db":
      return pn(n, "replicas") > 0 && pb(n, "failover") ? base : 0;
    case "queue":
    case "stream":
      return pn(n, "partitions") >= 3 ? 1 : 0;
    default:
      return 0;
  }
}

/* ---------- кэш и CDN ---------- */

export function cdnHit(n: SdNode): number {
  const ttl = pn(n, "ttl");
  return ttl <= 30 ? 0.55 : ttl <= 300 ? 0.9 : 0.98;
}

export function cacheHit(n: SdNode, wl: Workload): number {
  const reads = wl.read;
  if (reads <= 0) return 0;
  const hotGB = Math.max(0.1, wl.dataGB * wl.hotSet);
  const coverage = Math.min(1, pn(n, "sizeGB") / hotGB);
  const ttl = pn(n, "ttl");
  const ttlMul = ttl <= 30 ? 0.75 : ttl <= 300 ? 0.95 : 1;
  const writeFrac = wl.write / Math.max(1, wl.read + wl.write);
  const h = 0.95 * Math.sqrt(coverage) * ttlMul * (1 - 0.4 * writeFrac);
  return Math.round(h * 1000) / 1000;
}

/* ---------- ёмкость и цена ---------- */

const PRICE: Record<string, number> = { ondemand: 1, reserved: 0.6, spot: 0.3 };

const sizeOf = (n: SdNode): "S" | "M" | "L" => (ps(n, "size") as "S" | "M" | "L") || "S";

function nodeCost(n: SdNode, wl: Workload): number {
  switch (n.kind) {
    case "app":
      return REF.app.cost[sizeOf(n)] * pn(n, "instances") * (PRICE[ps(n, "pricing")] ?? 1) * (ps(n, "deploy") === "bluegreen" ? 2 : 1);
    case "lb":
      return REF.lb.cost * pn(n, "instances");
    case "gateway":
      return REF.gateway.cost * pn(n, "instances");
    case "limiter":
      return REF.limiter.cost;
    case "cdn":
      return REF.cdn.cost;
    case "cache":
      return REF.cache.costPerGB * pn(n, "sizeGB") * (1 + pn(n, "replicas"));
    case "db":
      return REF.db.cost[sizeOf(n)] * pn(n, "shards") * (1 + pn(n, "replicas"));
    case "queue":
      return REF.queue.cost + REF.queue.costPerPartition * pn(n, "partitions");
    case "worker":
      return REF.worker.cost[sizeOf(n) === "L" ? "M" : (sizeOf(n) as "S" | "M")] * pn(n, "instances") * (PRICE[ps(n, "pricing")] ?? 1);
    case "blob":
      return REF.blob.cost + (wl.mediaTB ?? 0) * (REF.blobTier[ps(n, "tier")]?.price ?? REF.blobTier["hot"]?.price ?? 23);
    case "auth":
    case "geo":
    case "ml":
    case "pay":
    case "notify":
    case "analytics":
      return REF[n.kind].cost * pn(n, "instances");
    case "stream":
      return REF.stream.cost + REF.stream.costPerPartition * pn(n, "partitions");
    case "search":
      return REF.search.cost * pn(n, "shards") * pn(n, "replicas");
    case "ws":
      return REF.ws.cost * pn(n, "instances");
    case "monitor":
      return REF.monitor.cost;
    default:
      return 0;
  }
}

function tierAvail(n: SdNode): number {
  const redundant = (a: number, k: number) => 1 - (1 - a) ** Math.max(1, k);
  switch (n.kind) {
    case "app":
      return redundant(ps(n, "pricing") === "spot" ? 0.95 : REF.app.avail, pn(n, "instances"));
    case "lb":
      return redundant(REF.lb.avail, pn(n, "instances"));
    case "gateway":
      return redundant(REF.gateway.avail, pn(n, "instances"));
    case "ws":
      return redundant(REF.ws.avail, pn(n, "instances"));
    case "limiter":
      return REF.limiter.avail;
    case "db":
      return pb(n, "failover") && pn(n, "replicas") > 0 ? redundant(REF.db.avail, 1 + pn(n, "replicas")) : REF.db.avail;
    case "queue":
      return pn(n, "partitions") >= 3 ? 0.99999 : REF.queue.avail;
    case "blob":
      return REF.blob.avail;
    case "auth":
    case "geo":
    case "ml":
    case "pay":
      return redundant(REF[n.kind].avail, pn(n, "instances"));
    case "stream":
      return pn(n, "partitions") >= 3 ? 0.99999 : REF.stream.avail;
    case "search":
      return redundant(REF.search.avail, pn(n, "replicas"));
    default:
      return 1;
  }
}

/* ---------- расчёт ---------- */

interface Path {
  p: number;
  cls: "static" | "read" | "write";
  nodes: string[];
  ok: boolean;
  /** отброшено ограничителем: для доступности схема исправна */
  rej?: boolean;
}

interface Acc {
  rps: number;
  heavy: number;
  writes: number;
  conn: number;
  msgs: number;
  /** запросы, обработанные приложением как статика */
  staticSelf: number;
  /** то, что пришло в очередь */
  queued: number;
  /** асинхронная запись в БД из обработчиков */
  asyncWrites: number;
  reads: number;
  /** дополнительные чтения из-за ленты pull/гибрид */
  extra: number;
}

const emptyAcc = (): Acc => ({ rps: 0, heavy: 0, writes: 0, conn: 0, msgs: 0, staticSelf: 0, queued: 0, asyncWrites: 0, reads: 0, extra: 0 });

export function evaluate(state: SdState, wl: Workload, opts: EvalOptions = {}): Result {
  const nodes = new Map(state.nodes.map((n) => [n.id, n]));
  const warnings: string[] = [];
  const out = new Map<string, SdNode[]>();
  for (const e of state.edges) {
    const a = nodes.get(e.from);
    const b = nodes.get(e.to);
    if (!a || !b) continue;
    if (!canLink(a.kind, b.kind)) {
      warnings.push(`связь «${a.name} → ${b.name}» не работает: такие компоненты не соединяются`);
      continue;
    }
    out.set(a.id, [...(out.get(a.id) ?? []), b]);
  }
  const kids = (n: SdNode, kinds: Kind[]): SdNode[] => (out.get(n.id) ?? []).filter((k) => kinds.includes(k.kind));
  const units = (n: SdNode) => workingUnits(n, opts);
  const clients = state.nodes.find((n) => n.kind === "clients");
  const entries = clients ? (out.get(clients.id) ?? []) : [];

  const webKinds: Kind[] = ["limiter", "gateway", "lb", "app"];
  const cdns = entries.filter((n) => n.kind === "cdn");
  const hasCache = (app: SdNode) => kids(app, ["cache"]).find((c) => units(c) > 0);

  const split = (list: SdNode[]): [SdNode, number][] => {
    const live = list.filter((n) => units(n) > 0 || n.kind === "limiter");
    const pool = live.length ? live : list;
    const w = (n: SdNode) => (n.kind === "app" ? Math.max(1, pn(n, "weight")) : Math.max(1, units(n)));
    const total = pool.reduce((s, n) => s + w(n), 0) || 1;
    return pool.map((n) => [n, w(n) / total]);
  };

  const callsOf = (k: DepKind): number => Math.max(0, Math.min(1, wl.calls?.[k] ?? 0));
  /** нагрузка потребителям очереди/потока: обработчики разбирают, уведомления и аналитика получают копию */
  const fanConsumers = (acc: (id: string) => Acc, queue: SdNode, rate: number): void => {
    for (const k of ["notify", "analytics"] as const) for (const [c, share] of split(kids(queue, [k]))) acc(c.id).rps += rate * share;
  };

  const feedRead = (app: SdNode): number => {
    const fo = wl.fanout ?? 0;
    const m = ps(app, "feed");
    return m === "pull" ? 1 + fo / 20 : m === "hybrid" ? 1 + fo / 100 : 1;
  };
  const feedWrite = (app: SdNode): number => {
    const fo = wl.fanout ?? 0;
    if (fo <= 0) return 1;
    const m = ps(app, "feed");
    return m === "push" ? fo : m === "hybrid" ? 1 + fo / 100 : 1;
  };

  function run(passLimiter: Map<string, number>, drain: number, retryMul: Map<string, number>): { acc: Map<string, Acc>; paths: Path[] } {
    const acc = new Map<string, Acc>();
    const A = (id: string) => {
      let a = acc.get(id);
      if (!a) acc.set(id, (a = emptyAcc()));
      return a;
    };
    const paths: Path[] = [];

    // продолжение пути от узла для класса cls; seq — уже пройденные узлы
    function walk(n: SdNode, cls: "static" | "read" | "write", prob: number, rate: number, seq: string[]): void {
      if (prob <= 1e-9) return;
      const here = [...seq, n.id];
      const a = A(n.id);
      const r = prob * rate;
      switch (n.kind) {
        case "cdn": {
          a.rps += r;
          if (cls === "static") {
            const h = units(n) > 0 ? cdnHit(n) : 0;
            paths.push({ p: prob * h, cls, nodes: here, ok: true });
            const miss = prob * (1 - h);
            const blobs = kids(n, ["blob"]);
            const webs = kids(n, webKinds);
            if (blobs.length) walk(blobs[0] as SdNode, cls, miss, rate, here);
            else forward(webs, cls, miss, rate, here);
          } else {
            forward(kids(n, webKinds), cls, prob, rate, here);
          }
          return;
        }
        case "limiter": {
          a.rps += r;
          const pass = passLimiter.get(n.id) ?? 1;
          paths.push({ p: prob * (1 - pass), cls, nodes: here, ok: false, rej: true });
          forward(kids(n, ["gateway", "lb", "app", "limiter"]), cls, prob * pass, rate, here);
          return;
        }
        case "gateway":
        case "lb": {
          a.rps += r;
          forward(kids(n, ["limiter", "gateway", "lb", "app"]), cls, prob, rate, here);
          return;
        }
        case "app": {
          if (cls === "static") {
            const blobs = kids(n, ["blob"]);
            if (blobs.length) {
              a.rps += 0;
              walk(blobs[0] as SdNode, cls, prob, rate, here);
            } else {
              a.rps += r * REF.staticWeight;
              a.staticSelf += r;
              paths.push({ p: prob, cls, nodes: here, ok: true });
            }
            return;
          }
          a.rps += r;
          for (const k of DEPS) {
            const f = callsOf(k);
            if (f > 0) for (const [d, share] of split(kids(n, [k]))) A(d.id).rps += r * f * share;
          }
          const dbs = kids(n, ["db"]);
          const db = dbs[0];
          if (cls === "read") {
            a.reads += r;
            const s = Math.min(1, Math.max(0, wl.searchShare ?? 0));
            const searches = kids(n, ["search"]);
            if (s > 0) {
              if (searches.length) walk(searches[0] as SdNode, "read", prob * s, rate, here);
              else if (db) {
                A(db.id).heavy += r * s;
                walk(db, "read", prob * s, rate, here);
              } else paths.push({ p: prob * s, cls, nodes: here, ok: false });
            }
            const plain = prob * (1 - s);
            const cache = hasCache(n);
            if (cache) {
              const h = cacheHit(cache, wl);
              A(cache.id).rps += plain * rate;
              A(cache.id).reads += plain * rate;
              paths.push({ p: plain * h, cls, nodes: [...here, cache.id], ok: true });
              if (db) {
                A(db.id).extra += plain * (1 - h) * rate * (feedRead(n) - 1);
                walk(db, "read", plain * (1 - h), rate, [...here, cache.id]);
              }
              else paths.push({ p: plain * (1 - h), cls, nodes: [...here, cache.id], ok: false });
            } else if (db) {
              A(db.id).extra += plain * rate * (feedRead(n) - 1);
              walk(db, "read", plain, rate, here);
            } else paths.push({ p: plain, cls, nodes: here, ok: false });
            return;
          }
          // write
          const queue = kids(n, ["queue"])[0];
          const stream = kids(n, ["stream"])[0];
          const cache = hasCache(n);
          if (cache) {
            A(cache.id).rps += r * 0.5;
            A(cache.id).writes += r;
          }
          // поток событий — побочная копия записи: потребители (уведомления, аналитика) получают событие, путь запроса не меняется
          if (stream) {
            A(stream.id).queued += r;
            A(stream.id).rps += r;
            fanConsumers(A, stream, r);
          }
          if (queue) {
            A(queue.id).queued += r;
            A(queue.id).rps += r;
            paths.push({ p: prob, cls, nodes: [...here, queue.id], ok: true });
            // асинхронное продолжение: обработчики → БД (по схеме, только нагрузка)
            fanConsumers(A, queue, r);
            const workers = kids(queue, ["worker"]);
            const amp = feedWrite(n);
            for (const [w, share] of split(workers)) {
              A(w.id).asyncWrites += r * share * amp;
              for (const d of kids(w, ["db"])) {
                A(d.id).writes += r * share * drain * amp;
                A(d.id).asyncWrites += r * share * drain * amp;
              }
            }
          } else if (db) {
            A(db.id).extra += 0;
            A(db.id).writes += r * (feedWrite(n) - 1);
            walk(db, "write", prob, rate, cache ? [...here, cache.id] : here);
          } else if (stream) paths.push({ p: prob, cls, nodes: [...here, stream.id], ok: true });
          else paths.push({ p: prob, cls, nodes: here, ok: false });
          return;
        }
        case "db": {
          a.rps += r;
          const mul = retryMul.get(n.id) ?? 1;
          if (cls === "write") a.writes += r * mul * (isWriteBack(seq) ? REF.writeBack : 1);
          else a.reads += r * mul;
          paths.push({ p: prob, cls, nodes: here, ok: true });
          return;
        }
        case "search":
        case "blob": {
          a.rps += r;
          paths.push({ p: prob, cls, nodes: here, ok: true });
          return;
        }
        default:
          paths.push({ p: prob, cls, nodes: here, ok: false });
      }
    }

    const isWriteBack = (seq: string[]): boolean => {
      for (const id of seq) {
        const n = nodes.get(id);
        if (n?.kind === "cache" && ps(n, "policy") === "back") return true;
      }
      return false;
    };

    function forward(list: SdNode[], cls: "static" | "read" | "write", prob: number, rate: number, seq: string[]): void {
      if (!list.length) {
        paths.push({ p: prob, cls, nodes: seq, ok: false });
        return;
      }
      for (const [n, share] of split(list)) walk(n, cls, prob * share, rate, seq);
    }

    // вход: пользователи → первые узлы
    const entryWeb = entries.filter((n) => webKinds.includes(n.kind));
    const classes: ["static" | "read" | "write", number][] = [
      ["static", wl.static],
      ["read", wl.read],
      ["write", wl.write],
    ];
    const root = clients ? [clients.id] : [];
    for (const [cls, rate] of classes) {
      if (rate <= 0) continue;
      if (cdns.length && cls === "static") forward(cdns, cls, 1, rate, root);
      else if (entryWeb.length) forward(entryWeb, cls, 1, rate, root);
      else if (cdns.length) forward(cdns, cls, 1, rate, root);
      else paths.push({ p: 1, cls, nodes: root, ok: false });
    }

    // соединения WebSocket и сообщения
    const wsEntries = entries.filter((n) => n.kind === "ws");
    const viaLb = entries.flatMap((e) => (e.kind === "lb" || e.kind === "gateway" || e.kind === "limiter" ? kids(e, ["ws"]) : []));
    const wsAll = [...new Set([...wsEntries, ...viaLb])];
    if ((wl.connections ?? 0) > 0 && wsAll.length) {
      for (const [w, share] of split(wsAll)) {
        const a = A(w.id);
        a.conn += (wl.connections ?? 0) * share;
        const msgs = (wl.connections ?? 0) * (wl.msgPerConn ?? 0) * share;
        a.msgs += msgs;
        const targets = kids(w, ["app"]);
        for (const [app, s2] of split(targets)) {
          A(app.id).rps += msgs * s2;
          const queue = kids(app, ["queue", "stream"])[0];
          const db = kids(app, ["db"])[0];
          if (queue) {
            A(queue.id).queued += msgs * s2;
            fanConsumers(A, queue, msgs * s2);
          }
          else if (db) {
            A(db.id).writes += msgs * s2;
            A(db.id).rps += msgs * s2;
          }
        }
      }
    }
    // обновления геопозиций идут прямо в сервисы геопоиска, подключённые к приложению
    if ((wl.geoUpdates ?? 0) > 0) {
      const geos = state.nodes.filter((g) => g.kind === "geo" && state.edges.some((e) => e.to === g.id && nodes.get(e.from)?.kind === "app"));
      for (const [g, share] of split(geos)) A(g.id).rps += (wl.geoUpdates ?? 0) * share;
    }
    return { acc, paths };
  }

  /* --- первая итерация: ёмкость узлов, пропуск ограничителей и скорость разбора очереди --- */
  const passLimiter = new Map<string, number>();
  let drain = 1;
  const noRetry = new Map<string, number>();
  let r1 = run(passLimiter, drain, noRetry);
  const limiters = state.nodes.filter((n) => n.kind === "limiter");
  for (const l of limiters) {
    const total = r1.acc.get(l.id)?.rps ?? 0;
    const lim = pn(l, "limit");
    passLimiter.set(l.id, total > 0 ? Math.min(1, lim / total) : 1);
  }
  const workerCap = (w: SdNode) => units(w) * REF.worker.cap[sizeOf(w) === "L" ? "M" : (sizeOf(w) as "S" | "M")];
  let asyncTotal = 0;
  let drainCap = 0;
  for (const n of state.nodes) {
    if (n.kind === "worker") {
      const a = r1.acc.get(n.id);
      asyncTotal += a?.asyncWrites ?? 0;
      drainCap += workerCap(n);
    }
  }
  if (asyncTotal > 0) drain = Math.min(1, drainCap / asyncTotal);
  r1 = run(passLimiter, drain, noRetry);

  /* повторы: если база перегружена, каждая неудача возвращается ещё r раз — нагрузка растёт (если нет автомата разрыва) */
  const dbs = state.nodes.filter((n) => n.kind === "db");
  const apps = state.nodes.filter((n) => n.kind === "app");
  const retryAcc = (db: SdNode): number => {
    const a = r1.acc.get(db.id) ?? emptyAcc();
    const u = units(db);
    const shards = Math.max(1, pn(db, "shards"));
    const eng = ps(db, "engine") === "nosql" ? REF.db.nosql : 1;
    const reps = pn(db, "replicas");
    const readBase = REF.db.read[sizeOf(db)] * eng;
    const writeBase = REF.db.write[sizeOf(db)] * eng;
    const hot = Math.min(1, Math.max(0, wl.hotKey ?? 0));
    const share = shards > 1 ? hot + (1 - hot) / shards : 1;
    const rl = (a.reads + a.extra + a.heavy * (REF.heavySearch - 1)) * share;
    const wlo = a.writes * share;
    const ut = u === 0 ? (rl + wlo > 0 ? 9 : 0) : reps > 0 ? Math.max(rl / (readBase * Math.max(reps, 1)), wlo / writeBase) : rl / readBase + wlo / writeBase;
    return ut;
  };
  let retryFactor = 1;
  for (const db of dbs) {
    const ut = retryAcc(db);
    if (ut <= 1) continue;
    const f = Math.min(0.95, 1 - 1 / ut);
    for (const app of apps) {
      if (!kids(app, ["db"]).includes(db)) continue;
      const retries = pn(app, "retries");
      if (retries <= 0 || pb(app, "breaker")) continue;
      let m = 0;
      for (let i = 0; i <= retries; i++) m += f ** i;
      retryFactor = Math.max(retryFactor, m);
    }
  }
  if (retryFactor > 1) {
    for (const db of dbs) noRetry.set(db.id, retryFactor);
    r1 = run(passLimiter, drain, noRetry);
  }
  const { acc, paths } = r1;

  /* --- загрузка узлов --- */
  const loads: Record<string, NodeLoad> = {};
  const util: Record<string, number> = {};
  const note: Record<string, string> = {};
  let maxShardShare: number | null = null;
  let replicaLagMs: number | null = null;
  let lagSec: number | null = null;
  let hitRatio: number | null = null;
  let cdnHitRatio: number | null = null;

  for (const n of state.nodes) {
    const a = acc.get(n.id) ?? emptyAcc();
    const u = units(n);
    let load = a.rps;
    let cap = 0;
    let ut = 0;
    let nt = "";
    switch (n.kind) {
      case "clients":
        continue;
      case "cdn": {
        cap = REF.cdn.cap;
        ut = load / cap;
        cdnHitRatio = u > 0 ? cdnHit(n) : 0;
        nt = `попаданий ${Math.round((cdnHitRatio ?? 0) * 100)}%`;
        break;
      }
      case "limiter": {
        cap = pn(n, "limit");
        ut = load / cap;
        nt = ut > 1 ? `отбрасывает ${Math.round((1 - 1 / ut) * 100)}%` : "";
        break;
      }
      case "gateway":
        cap = REF.gateway.cap * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      case "lb":
        cap = REF.lb.cap * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      case "ws": {
        load = a.conn;
        cap = REF.ws.cap * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      }
      case "app": {
        cap = REF.app.cap[sizeOf(n)] * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        if (pn(n, "instances") > 1 && ps(n, "sessions") === "local") nt = "сессии в памяти: при балансировке пользователи «теряют» вход";
        break;
      }
      case "cache": {
        load = a.rps;
        cap = u > 0 ? REF.cache.cap : 0;
        ut = cap > 0 ? load / cap : 0;
        const h = u > 0 ? cacheHit(n, wl) : 0;
        hitRatio = h;
        nt = `попаданий ${Math.round(h * 100)}%`;
        break;
      }
      case "queue": {
        load = a.queued;
        cap = REF.queue.capPerPartition * pn(n, "partitions") * (u > 0 ? 1 : 0);
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      }
      case "auth":
      case "geo":
      case "ml":
      case "pay":
      case "notify":
      case "analytics":
        cap = REF[n.kind].cap * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      case "stream": {
        load = a.queued;
        cap = REF.stream.capPerPartition * pn(n, "partitions") * (u > 0 ? 1 : 0);
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      }
      case "worker": {
        load = a.asyncWrites;
        cap = workerCap(n);
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        break;
      }
      case "blob":
        cap = REF.blob.cap;
        ut = load / cap;
        break;
      case "search": {
        const shards = pn(n, "shards");
        cap = REF.search.cap * u;
        ut = cap > 0 ? load / cap : load > 0 ? 9 : 0;
        const perShard = wl.dataGB / Math.max(1, shards);
        if (perShard > REF.search.maxGBPerShard) {
          ut = Math.max(ut, perShard / REF.search.maxGBPerShard);
          nt = `индекс ${Math.round(perShard)} ГБ на шард — слишком много`;
        }
        break;
      }
      case "db": {
        const shards = Math.max(1, pn(n, "shards"));
        const reps = pn(n, "replicas");
        const eng = ps(n, "engine") === "nosql" ? REF.db.nosql : 1;
        const hot = Math.min(1, Math.max(0, wl.hotKey ?? 0));
        const share = shards > 1 ? hot + (1 - hot) / shards : 1;
        maxShardShare = share;
        const readLoad = a.reads + a.extra + a.heavy * (REF.heavySearch - 1);
        const writeLoad = a.writes;
        const readBase = REF.db.read[sizeOf(n)] * eng;
        const writeBase = REF.db.write[sizeOf(n)] * eng;
        const workingReps = u > 0 ? (opts.fail === "db" || opts.fail === "zone" ? Math.max(0, reps - (opts.fail === "db" ? 1 : Math.ceil(reps / 3))) : reps) : 0;
        const wshare = ps(n, "shardKey") === "range" && wl.monotonic ? 1 : share;
        if (shards > 1) maxShardShare = Math.max(share, wshare);
        const rl = readLoad * share;
        const wlo = writeLoad * wshare;
        if (u === 0) {
          ut = readLoad + writeLoad > 0 ? 9 : 0;
        } else if (reps > 0) {
          const readCap = readBase * Math.max(workingReps, 1);
          ut = Math.max(rl / readCap, wlo / writeBase);
          replicaLagMs = ps(n, "sync") === "sync" ? 0 : Math.round(15 + 120 * Math.min(1, wlo / writeBase));
        } else {
          ut = rl / readBase + wlo / writeBase;
        }
        load = readLoad + writeLoad;
        cap = ut > 0 ? load / ut : readBase + writeBase;
        if (shards > 1 && hot > 0.1) nt = `горячий ключ: ${Math.round(share * 100)}% нагрузки на один шард`;
        break;
      }
      case "monitor":
        load = 0;
        cap = 0;
        ut = 0;
        break;
    }
    const down = u === 0 && n.kind !== "monitor" && n.kind !== "cdn" && n.kind !== "cache";
    let status: NodeStatus = "ok";
    if (down) status = "down";
    else if (load <= 0 && n.kind !== "monitor") status = "idle";
    else if (ut > 1) status = "over";
    else if (ut > 0.8) status = "hot";
    else if (ut > 0.6) status = "warm";
    util[n.id] = ut;
    note[n.id] = nt;
    loads[n.id] = { load, cap, util: ut, units: u, status, ...(nt ? { note: nt } : {}) };
  }

  /* очередь: отставание */
  const queue = state.nodes.find((n) => n.kind === "queue") ?? state.nodes.find((n) => n.kind === "stream");
  if (queue) {
    const arrive = acc.get(queue.id)?.queued ?? 0;
    const hasWorker = state.nodes.some((n) => n.kind === "worker");
    if (!hasWorker || drainCap <= 0) lagSec = arrive > 0 ? 999 : 0;
    else if (arrive <= drainCap) lagSec = 0;
    else lagSec = wl.spikeSec ? Math.round(((arrive - drainCap) * wl.spikeSec) / drainCap) : 999;
  }

  /* --- метрики по путям --- */
  const ownLat = (n: SdNode, cls: Path["cls"], seq: string[]): number => {
    let base = 0;
    switch (n.kind) {
      case "cdn":
        base = REF.lat.cdn;
        break;
      case "limiter":
        base = REF.lat.limiter;
        break;
      case "gateway":
        base = REF.lat.gateway;
        break;
      case "lb":
        base = ps(n, "layer") === "L7" ? REF.lat.lb.L7 : REF.lat.lb.L4;
        break;
      case "ws":
        base = REF.lat.ws;
        break;
      case "app":
        base = cls === "static" ? REF.lat.appStatic : REF.lat.app;
        break;
      case "cache":
        base = REF.lat.cache;
        break;
      case "queue":
        base = REF.lat.queue;
        break;
      case "blob":
        base = REF.blobTier[ps(n, "tier")]?.lat ?? REF.lat.blob;
        break;
      case "auth":
      case "geo":
      case "ml":
      case "pay":
        base = REF.lat[n.kind];
        break;
      case "search":
        base = REF.lat.search;
        break;
      case "db": {
        const k = ps(n, "engine") === "nosql" ? 0.7 : 1;
        const a = acc.get(n.id);
        const heavyShare = a && a.reads > 0 ? Math.min(1, a.heavy / a.reads) : 0;
        base = (cls === "write" ? REF.lat.dbWrite + (ps(n, "sync") === "sync" && pn(n, "replicas") > 0 ? 8 : 0) : REF.lat.dbRead) * k * (1 + 4 * heavyShare);
        void seq;
        break;
      }
      default:
        base = 0;
    }
    const u = util[n.id] ?? 0;
    const q = n.kind === "cdn" || n.kind === "blob" ? 1 : u < 0.5 ? 1 : u >= 1 ? 40 : Math.min(40, 1 / (1 - u));
    return base * q;
  };

  const rate: Record<Path["cls"], number> = { static: wl.static, read: wl.read, write: wl.write };
  const totalRate = Math.max(1, rate.static + rate.read + rate.write);
  let lat = 0;
  let succ = 0;
  let avail = 0;
  let wsum = 0;
  const touched = new Set<string>();
  for (const p of paths) {
    const w = (p.p * rate[p.cls]) / totalRate;
    if (w <= 0) continue;
    wsum += w;
    let l = 0;
    let s = p.ok ? 1 : 0;
    let av = p.ok || p.rej ? 1 : 0;
    const seen = new Set<string>();
    for (let i = 0; i < p.nodes.length; i++) {
      const id = p.nodes[i] as string;
      const n = nodes.get(id);
      if (!n || n.kind === "clients") continue;
      touched.add(id);
      l += ownLat(n, p.cls, p.nodes.slice(0, i));
      if (n.kind === "app" && p.cls !== "static") {
        // вызовы сервисов: на долю f запросов добавляются задержка, потери и риск сервиса; нет связи — эти запросы не выполняются
        for (const k of DEPS) {
          const f = callsOf(k);
          if (f <= 0) continue;
          const group = kids(n, [k]);
          if (!group.length) {
            s *= 1 - f;
            av *= 1 - f;
            continue;
          }
          let gl = 0;
          let gs = 0;
          let ga = 0;
          for (const d of group) {
            touched.add(d.id);
            const du = util[d.id] ?? 0;
            gl += ownLat(d, p.cls, []);
            gs += units(d) > 0 ? (du > 1 ? 1 / du : 1) : 0;
            ga += tierAvail(d);
          }
          l += (f * gl) / group.length;
          s *= 1 - f + (f * gs) / group.length;
          av *= 1 - f + (f * ga) / group.length;
        }
      }
      const ut = util[id] ?? 0;
      const served = ut > 1 ? 1 / ut : 1;
      if (n.kind === "limiter") {
        /* пропуск уже учтён отдельными путями */
      } else s *= units(n) > 0 || ["cache", "cdn", "monitor"].includes(n.kind) ? served : 0;
      if (!seen.has(id) && !["cache", "cdn"].includes(n.kind)) av *= tierAvail(n);
      seen.add(id);
    }
    lat += w * l;
    succ += w * s;
    avail += w * av;
  }
  if (wsum > 0) {
    lat /= wsum;
    succ /= wsum;
    avail /= wsum;
  }
  let tail = 0;
  for (const id of touched) tail += 200 * Math.max(0, (util[id] ?? 0) - 0.7);
  const p50 = Math.round(lat);
  const p99 = Math.round(lat * 1.8 + Math.min(4000, tail));

  const entry = paths.length > 0 && paths.some((p) => p.ok);
  const cost = state.nodes.reduce((s, n) => s + nodeCost(n, wl), 0);

  for (const n of state.nodes) {
    if (n.kind === "clients") continue;
    const incoming = state.edges.some((e) => e.to === n.id && nodes.has(e.from) && canLink((nodes.get(e.from) as SdNode).kind, n.kind));
    if (!incoming && n.kind !== "monitor") warnings.push(`«${n.name}» ни к чему не подключён — к нему не приходит нагрузка`);
  }

  return {
    loads,
    p50,
    p99,
    success: Math.round(succ * 10000) / 10000,
    availability: avail,
    cost,
    hit: hitRatio,
    cdnHit: cdnHitRatio,
    lagSec,
    replicaLagMs,
    maxShardShare,
    entry,
    warnings: [...new Set(warnings)],
  };
}
