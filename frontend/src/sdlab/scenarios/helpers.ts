import { KINDS, defaultParams } from "../kinds.ts";
import { place } from "../layout.ts";
import type { Kind, ParamValue, SdEdge, SdNode, SdState, Workload } from "../types.ts";

/* Помощники для описания схем в сценариях: N — узел, E — связь, S — схема с автораскладкой. */

export const N = (id: string, kind: Kind, params: Record<string, ParamValue> = {}, name?: string): SdNode => ({
  id,
  kind,
  name: name ?? KINDS[kind].label,
  x: -1,
  y: -1,
  params: { ...defaultParams(kind), ...params },
});

export const E = (from: string, to: string): SdEdge => ({ from, to });

export const users = (): SdNode => N("users", "clients", {}, "Пользователи");

/** схема из узлов и связей; цепочки «a>b>c» разворачиваются в рёбра */
export function S(nodes: SdNode[], chains: string[] = []): SdState {
  const edges: SdEdge[] = [];
  for (const c of chains) {
    const ids = c.split(">").map((x) => x.trim());
    for (let i = 0; i + 1 < ids.length; i++) edges.push(E(ids[i] as string, ids[i + 1] as string));
  }
  return place({ nodes, edges });
}

/** типичные нагрузки: подставляйте и переопределяйте */
export const WL = (over: Partial<Workload>): Workload => ({
  static: 0,
  read: 0,
  write: 0,
  dataGB: 10,
  hotSet: 0.2,
  ...over,
});
