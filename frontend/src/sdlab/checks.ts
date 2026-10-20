import { evaluate, baseUnits, param } from "./engine.ts";
import { KINDS } from "./kinds.ts";
import type { Goal, GoalResult, Kind, ParamValue, Result, SdState, Workload } from "./types.ts";

/* Цели упражнения: каждая превращается в строку «условие — выполнено / нет — почему». */

const pct = (x: number) => `${(x * 100).toFixed(x >= 0.999 ? 3 : 1)}%`;
const nodesOf = (s: SdState, kind: Kind) => s.nodes.filter((n) => n.kind === kind);
const label = (k: Kind) => KINDS[k].label.toLowerCase();

const KIND_FAIL: Record<string, string> = {
  zone: "зоны доступности",
  region: "региона",
  deploy: "выкладки новой версии",
  app: "одного сервера приложения",
  lb: "одного балансировщика",
  db: "лидера базы данных",
  cache: "кэша",
  cdn: "CDN",
  queue: "очереди",
  worker: "одного обработчика",
  gateway: "одного шлюза",
  search: "одной реплики поиска",
  ws: "одного WebSocket-шлюза",
  blob: "объектного хранилища",
  limiter: "ограничителя",
  monitor: "мониторинга",
  clients: "пользователей",
  auth: "одного сервиса входа",
  geo: "одного геосервиса",
  ml: "одного сервиса ранжирования",
  pay: "одного платёжного канала",
  stream: "потока событий",
  notify: "одного сервиса уведомлений",
  analytics: "одного узла аналитики",
};

export function describe(g: Goal): string {
  switch (g.k) {
    case "capacity":
      return `ни один компонент не загружен больше чем на ${Math.round(g.max * 100)}%`;
    case "util":
      return `${label(g.kind)} загружен не больше чем на ${Math.round(g.max * 100)}%`;
    case "p99":
      return `задержка p99 не больше ${g.max} мс`;
    case "p50":
      return `средняя задержка не больше ${g.max} мс`;
    case "success":
      return `успешно обслуживается не меньше ${pct(g.min)} запросов`;
    case "availability":
      return `доступность схемы не ниже ${pct(g.min)}`;
    case "cost":
      return `стоимость не больше $${g.max} в месяц`;
    case "has":
      return `в схеме есть ${label(g.kind)}${g.min && g.min > 1 ? ` (не меньше ${g.min})` : ""}`;
    case "lacks":
      return `в схеме нет компонента «${label(g.kind)}»`;
    case "link":
      return `${label(g.from)} соединён с компонентом «${label(g.to)}»`;
    case "hit":
      return `кэш отдаёт не меньше ${Math.round(g.min * 100)}% чтений`;
    case "cdnHit":
      return `CDN отдаёт не меньше ${Math.round(g.min * 100)}% статики`;
    case "survive":
      return `схема переживает отказ ${KIND_FAIL[g.fail] ?? g.fail}`;
    case "param":
      return `${label(g.kind)}: ${KINDS[g.kind].params.find((p) => p.key === g.key)?.label ?? g.key} ${g.op} ${String(g.value)}`;
    case "lag":
      return `очередь разбирается после пика не дольше чем за ${g.max} с`;
    case "replicaLag":
      return `отставание реплик не больше ${g.max} мс`;
    case "shardShare":
      return `на самый нагруженный шард приходится не больше ${Math.round(g.max * 100)}% данных и запросов`;
    case "noSpof":
      return `нет единой точки отказа: ${g.kinds.map(label).join(", ")}`;
  }
}

function cmp(a: ParamValue, op: ">=" | "<=" | "==" | "!=", b: ParamValue): boolean {
  switch (op) {
    case "==":
      return a === b;
    case "!=":
      return a !== b;
    case ">=":
      return Number(a) >= Number(b);
    case "<=":
      return Number(a) <= Number(b);
  }
}

function redundant(n: SdState["nodes"][number]): boolean {
  switch (n.kind) {
    case "lb":
    case "app":
    case "gateway":
    case "worker":
    case "ws":
    case "auth":
    case "geo":
    case "ml":
    case "pay":
    case "notify":
    case "analytics":
      return baseUnits(n) >= 2;
    case "cache":
      return Number(param(n, "replicas")) >= 1;
    case "db":
      return Number(param(n, "replicas")) >= 1 && param(n, "failover") === true;
    case "queue":
    case "stream":
      return Number(param(n, "partitions")) >= 3;
    case "search":
      return baseUnits(n) >= 2;
    default:
      return true;
  }
}

export function checkGoals(state: SdState, wl: Workload, goals: Goal[], base?: Result): GoalResult[] {
  const r = base ?? evaluate(state, wl);
  return goals.map((g): GoalResult => {
    const text = describe(g);
    const done = (ok: boolean, detail: string): GoalResult => ({ ok, text, detail });
    switch (g.k) {
      case "capacity": {
        const worst = Object.entries(r.loads)
          .filter(([, l]) => l.status !== "idle")
          .sort((a, b) => b[1].util - a[1].util)[0];
        if (!worst) return done(false, "нагрузка никуда не доходит");
        const name = state.nodes.find((n) => n.id === worst[0])?.name ?? worst[0];
        return done(worst[1].util <= g.max, `самый загруженный — «${name}»: ${Math.round(worst[1].util * 100)}%`);
      }
      case "util": {
        const ns = nodesOf(state, g.kind);
        if (!ns.length) return done(false, "компонента нет");
        const worst = Math.max(...ns.map((n) => r.loads[n.id]?.util ?? 0));
        return done(worst <= g.max, `сейчас ${Math.round(worst * 100)}%`);
      }
      case "p99":
        return done(r.entry && r.p99 <= g.max, r.entry ? `сейчас ${r.p99} мс` : "запросы не доходят до обработки");
      case "p50":
        return done(r.entry && r.p50 <= g.max, r.entry ? `сейчас ${r.p50} мс` : "запросы не доходят до обработки");
      case "success":
        return done(r.success >= g.min, `сейчас ${pct(r.success)}`);
      case "availability":
        return done(r.availability >= g.min, `сейчас ${pct(r.availability)}`);
      case "cost":
        return done(r.cost <= g.max, `сейчас $${r.cost}`);
      case "has": {
        const n = nodesOf(state, g.kind).length;
        const need = g.min ?? 1;
        return done(n >= need, `на схеме: ${n}`);
      }
      case "lacks": {
        const n = nodesOf(state, g.kind).length;
        return done(n === 0, `на схеме: ${n}`);
      }
      case "link": {
        const ids = new Set(nodesOf(state, g.to).map((n) => n.id));
        const ok = state.edges.some((e) => ids.has(e.to) && state.nodes.find((n) => n.id === e.from)?.kind === g.from);
        return done(ok, ok ? "связь есть" : "связи нет");
      }
      case "hit":
        return done((r.hit ?? 0) >= g.min, r.hit === null ? "кэша нет" : `сейчас ${Math.round(r.hit * 100)}%`);
      case "cdnHit":
        return done((r.cdnHit ?? 0) >= g.min, r.cdnHit === null ? "CDN нет" : `сейчас ${Math.round(r.cdnHit * 100)}%`);
      case "survive": {
        const f = evaluate(state, wl, { fail: g.fail });
        const ok = f.entry && f.success >= 0.99;
        return done(ok, ok ? "после отказа всё работает" : `после отказа успешно ${pct(f.entry ? f.success : 0)}`);
      }
      case "param": {
        const ns = nodesOf(state, g.kind);
        const ok = ns.length > 0 && ns.every((n) => cmp(param(n, g.key), g.op, g.value));
        return done(ok, ns.length ? `сейчас ${ns.map((n) => String(param(n, g.key))).join(", ")}` : "компонента нет");
      }
      case "lag":
        return done(r.lagSec !== null && r.lagSec <= g.max, r.lagSec === null ? "очереди нет" : r.lagSec >= 999 ? "очередь не разбирается" : `сейчас ${r.lagSec} с`);
      case "replicaLag":
        return done(r.replicaLagMs !== null && r.replicaLagMs <= g.max, r.replicaLagMs === null ? "реплик нет" : `сейчас ${r.replicaLagMs} мс`);
      case "shardShare":
        return done(r.maxShardShare !== null && r.maxShardShare <= g.max, r.maxShardShare === null ? "базы нет" : `сейчас ${Math.round(r.maxShardShare * 100)}%`);
      case "noSpof": {
        const bad = g.kinds.flatMap((k) => nodesOf(state, k).filter((n) => !redundant(n)).map((n) => n.name));
        const present = g.kinds.some((k) => nodesOf(state, k).length > 0);
        return done(present && bad.length === 0, bad.length ? `единственные: ${bad.join(", ")}` : present ? "резервирование есть" : "компонентов нет");
      }
    }
  });
}

export const allOk = (rs: GoalResult[]) => rs.every((r) => r.ok);
