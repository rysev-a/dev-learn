import { canLink } from "./engine.ts";
import type { Kind, SdEdge, SdNode, SdState } from "./types.ts";

/* Порты и связи на поле схемы (по образцу досок лаборатории «Архитектура компьютера»): у компонента слева —
   входной порт, справа — выходной. Связь идёт от выхода к входу; допустимость задаёт engine.canLink.
   Автоподстановка: компонент, который двигают или ставят, сам «тянется» к ближайшим подходящим соседям. */

export const NODE_W = 124;
export const NODE_H = 60;
/** на каком расстоянии (в единицах поля) соседние порты считаются «близкими» */
export const AUTO_RADIUS = 230;
/** «залипание» уже показанной связи, чтобы пунктир не дрожал */
const STICK = 14;

export interface Pt {
  x: number;
  y: number;
}

const KINDS_ALL: Kind[] = ["clients", "cdn", "lb", "gateway", "limiter", "app", "cache", "db", "queue", "worker", "blob", "search", "ws", "monitor"];

export const hasOut = (k: Kind): boolean => KINDS_ALL.some((t) => canLink(k, t));
export const hasIn = (k: Kind): boolean => KINDS_ALL.some((t) => canLink(t, k));

export const outPos = (n: Pt): Pt => ({ x: n.x + NODE_W / 2, y: n.y });
export const inPos = (n: Pt): Pt => ({ x: n.x - NODE_W / 2, y: n.y });

/** кривая связи от точки a (выход) к b (вход) */
export function wirePath(a: Pt, b: Pt): string {
  const dx = Math.max(36, Math.abs(b.x - a.x) / 2);
  return `M${a.x} ${a.y} C${a.x + dx} ${a.y} ${b.x - dx} ${b.y} ${b.x} ${b.y}`;
}

/** есть ли путь по связям из a в b */
export function reaches(edges: readonly SdEdge[], a: string, b: string): boolean {
  const seen = new Set<string>();
  const stack = [a];
  while (stack.length) {
    const cur = stack.pop() as string;
    if (cur === b) return true;
    if (seen.has(cur)) continue;
    seen.add(cur);
    for (const e of edges) if (e.from === cur) stack.push(e.to);
  }
  return false;
}

/** причина, по которой связь a → b поставить нельзя; null — можно */
export function connectError(state: SdState, a: SdNode, b: SdNode): string | null {
  if (a.id === b.id) return "Компонент нельзя соединить с самим собой.";
  if (!canLink(a.kind, b.kind)) return `«${a.name}» не соединяется с «${b.name}»: так в этой модели не устроено.`;
  if (state.edges.some((e) => e.from === a.id && e.to === b.id)) return "Такая связь уже есть.";
  if (reaches(state.edges, b.id, a.id)) return "Так схема замкнётся в цикл — запросы будут ходить по кругу.";
  return null;
}

const dist = (p: Pt, q: Pt) => Math.hypot(p.x - q.x, p.y - q.y);

/**
 * Какие связи стоит подставить для компонента `node` на его месте: вход тянется к ближайшему
 * подходящему источнику слева, а выход — к ближайшему подходящему приёмнику справа (по одному на вид
 * компонента). Уже существующие связи и циклы пропускаются.
 */
export function suggestEdges(state: SdState, node: SdNode, keep: readonly SdEdge[] = [], radius = AUTO_RADIUS): SdEdge[] {
  const others = state.nodes.filter((n) => n.id !== node.id);
  const have = (from: string, to: string) => state.edges.some((e) => e.from === from && e.to === to);
  const kept = (from: string, to: string) => keep.some((e) => e.from === from && e.to === to);
  const planned: SdEdge[] = [];
  const edgesNow = () => [...state.edges, ...planned];
  const result: SdEdge[] = [];
  const score = (d: number, from: string, to: string) => d - (kept(from, to) ? STICK : 0);

  // вход ← ближайший источник
  if (hasIn(node.kind)) {
    let best: { n: SdNode; s: number } | null = null;
    for (const s of others) {
      if (!canLink(s.kind, node.kind) || have(s.id, node.id)) continue;
      if (s.x > node.x + NODE_W / 2) continue;
      const d = dist(outPos(s), inPos(node));
      if (d > radius && !kept(s.id, node.id)) continue;
      const sc = score(d, s.id, node.id);
      if (!best || sc < best.s) best = { n: s, s: sc };
    }
    if (best && !reaches(edgesNow(), node.id, best.n.id)) {
      const e = { from: best.n.id, to: node.id };
      planned.push(e);
      result.push(e);
    }
  }

  // выход → ближайшие приёмники по одному на вид
  if (hasOut(node.kind)) {
    const byKind = new Map<Kind, { n: SdNode; s: number }>();
    for (const t of others) {
      if (!canLink(node.kind, t.kind) || have(node.id, t.id)) continue;
      if (t.x < node.x - NODE_W / 2) continue;
      const d = dist(outPos(node), inPos(t));
      if (d > radius && !kept(node.id, t.id)) continue;
      const sc = score(d, node.id, t.id);
      const cur = byKind.get(t.kind);
      if (!cur || sc < cur.s) byKind.set(t.kind, { n: t, s: sc });
    }
    for (const { n } of byKind.values()) {
      if (reaches(edgesNow(), n.id, node.id)) continue;
      const e = { from: node.id, to: n.id };
      planned.push(e);
      result.push(e);
    }
  }
  return result;
}
