import { useRef, type PointerEvent, type ReactNode } from "react";
import { KINDS } from "../kinds.ts";
import { BOARD_H, BOARD_W } from "../layout.ts";
import type { Kind, NodeLoad, SdState } from "../types.ts";

/* Поле схемы: узлы можно перетаскивать, рёбра — выбирать. Цвет рамки — загрузка узла. */

const W = 96;
const H = 48;

const ICONS: Record<Kind, ReactNode> = {
  clients: (
    <>
      <circle cx="12" cy="8" r="3.5" />
      <path d="M5 20a7 7 0 0 1 14 0" />
    </>
  ),
  cdn: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18" />
    </>
  ),
  limiter: <path d="M4 5h16l-6 8v6l-4-2v-4L4 5Z" />,
  gateway: (
    <>
      <path d="M4 20V10l8-6 8 6v10" />
      <path d="M9 20v-6h6v6" />
    </>
  ),
  lb: (
    <>
      <circle cx="12" cy="5" r="2.2" />
      <circle cx="5" cy="19" r="2.2" />
      <circle cx="19" cy="19" r="2.2" />
      <path d="M12 7v4M12 11l-6 6M12 11l6 6" />
    </>
  ),
  ws: (
    <>
      <path d="M4 8l4 4-4 4M20 8l-4 4 4 4" />
      <path d="M13 6l-2 12" />
    </>
  ),
  app: (
    <>
      <rect x="3" y="3" width="18" height="8" rx="2" />
      <rect x="3" y="13" width="18" height="8" rx="2" />
      <path d="M7 7h.01M7 17h.01" />
    </>
  ),
  cache: <path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z" />,
  queue: (
    <>
      <rect x="3" y="7" width="5" height="10" rx="1" />
      <rect x="9.5" y="7" width="5" height="10" rx="1" />
      <rect x="16" y="7" width="5" height="10" rx="1" />
    </>
  ),
  worker: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" />
    </>
  ),
  db: (
    <>
      <ellipse cx="12" cy="5" rx="8" ry="3" />
      <path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" />
    </>
  ),
  blob: (
    <>
      <path d="M21 8 12 3 3 8v8l9 5 9-5V8Z" />
      <path d="M3 8l9 5 9-5M12 13v8" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 5 5" />
    </>
  ),
  monitor: <path d="M3 12h4l3-7 4 14 3-7h4" />,
};

export interface BoardProps {
  state: SdState;
  loads: Record<string, NodeLoad>;
  selected: string | null;
  selectedEdge: number | null;
  linkFrom: string | null;
  down: string[];
  onNode: (id: string) => void;
  onEdge: (i: number) => void;
  onMove: (id: string, x: number, y: number, done: boolean) => void;
}

const SUMMARY = (n: SdState["nodes"][number]): string => {
  const p = n.params;
  switch (n.kind) {
    case "app":
      return `×${p["instances"]} · ${p["size"]}`;
    case "lb":
    case "gateway":
    case "ws":
      return `×${p["instances"]}`;
    case "worker":
      return `×${p["instances"]} · ${p["size"]}`;
    case "cache":
      return `${p["sizeGB"]} ГБ`;
    case "db":
      return `${p["size"]} · ${Number(p["shards"]) > 1 ? `${p["shards"]} шард. ` : ""}${Number(p["replicas"]) > 0 ? `+${p["replicas"]} репл.` : ""}`;
    case "queue":
      return `${p["partitions"]} парт.`;
    case "limiter":
      return `${p["limit"]}/с`;
    case "cdn":
      return `TTL ${p["ttl"]}`;
    case "search":
      return `${p["shards"]}×${p["replicas"]}`;
    default:
      return "";
  }
};

export default function Board({ state, loads, selected, selectedEdge, linkFrom, down, onNode, onEdge, onMove }: BoardProps) {
  const svg = useRef<SVGSVGElement>(null);
  const drag = useRef<{ id: string; dx: number; dy: number; moved: boolean } | null>(null);
  const node = (id: string) => state.nodes.find((n) => n.id === id);

  const toBoard = (e: PointerEvent): { x: number; y: number } => {
    const el = svg.current;
    if (!el) return { x: 0, y: 0 };
    const m = el.getScreenCTM();
    if (!m) return { x: 0, y: 0 };
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse());
    return { x: p.x, y: p.y };
  };

  const onDown = (e: PointerEvent, id: string) => {
    const n = node(id);
    if (!n) return;
    const p = toBoard(e);
    drag.current = { id, dx: n.x - p.x, dy: n.y - p.y, moved: false };
    (e.currentTarget as Element).setPointerCapture(e.pointerId);
  };
  const onMoveEv = (e: PointerEvent) => {
    const d = drag.current;
    if (!d) return;
    const p = toBoard(e);
    const x = Math.max(W / 2, Math.min(BOARD_W - W / 2, p.x + d.dx));
    const y = Math.max(H / 2 + 4, Math.min(BOARD_H - H / 2 - 4, p.y + d.dy));
    d.moved = true;
    onMove(d.id, Math.round(x), Math.round(y), false);
  };
  const onUp = (e: PointerEvent) => {
    const d = drag.current;
    drag.current = null;
    if (!d) return;
    if (d.moved) {
      const n = node(d.id);
      if (n) onMove(d.id, n.x, n.y, true);
    } else onNode(d.id);
    (e.currentTarget as Element).releasePointerCapture(e.pointerId);
  };

  return (
    <svg ref={svg} className="sd-board" viewBox={`0 0 ${BOARD_W} ${BOARD_H}`} role="img" aria-label="Схема сервиса">
      <defs>
        <marker id="sd-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0 1 10 5 0 9Z" className="sd-arrowhead" />
        </marker>
      </defs>
      {state.edges.map((e, i) => {
        const a = node(e.from);
        const b = node(e.to);
        if (!a || !b) return null;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const len = Math.hypot(dx, dy) || 1;
        const ux = dx / len;
        const uy = dy / len;
        const fx = (len: number) => Math.min(len, Math.abs(ux) > 0.001 ? (W / 2 + 4) / Math.abs(ux) : len);
        const fy = (len: number) => Math.min(len, Math.abs(uy) > 0.001 ? (H / 2 + 4) / Math.abs(uy) : len);
        const t = Math.min(fx(len), fy(len));
        const x1 = a.x + ux * t;
        const y1 = a.y + uy * t;
        const x2 = b.x - ux * t;
        const y2 = b.y - uy * t;
        const dead = down.includes(a.id) || down.includes(b.id);
        return (
          <g key={`${e.from}-${e.to}`} className={`sd-edge ${selectedEdge === i ? "on" : ""} ${dead ? "dead" : ""}`}>
            <line x1={x1} y1={y1} x2={x2} y2={y2} markerEnd="url(#sd-arrow)" />
            <line className="hit" x1={x1} y1={y1} x2={x2} y2={y2} onClick={() => onEdge(i)} />
          </g>
        );
      })}
      {state.nodes.map((n) => {
        const l = loads[n.id];
        const st = down.includes(n.id) ? "down" : (l?.status ?? "idle");
        const cls = ["sd-node", n.kind, st, selected === n.id ? "on" : "", linkFrom === n.id ? "from" : ""].join(" ");
        return (
          <g
            key={n.id}
            className={cls}
            transform={`translate(${n.x},${n.y})`}
            onPointerDown={(e) => onDown(e, n.id)}
            onPointerMove={onMoveEv}
            onPointerUp={onUp}
          >
            <rect x={-W / 2} y={-H / 2} width={W} height={H} rx="9" />
            <g className="sd-ico" transform="translate(-40,-17) scale(0.9)">
              {ICONS[n.kind]}
            </g>
            <text className="sd-name" x={-14} y={-4}>
              {n.name.length > 15 ? `${n.name.slice(0, 14)}…` : n.name}
            </text>
            <text className="sd-sub" x={-14} y={9}>
              {st === "down" ? "отключён" : SUMMARY(n)}
            </text>
            {l && l.status !== "idle" && n.kind !== "monitor" && (
              <g className="sd-bar" transform={`translate(${-W / 2 + 8},${H / 2 - 9})`}>
                <rect width={W - 16} height="4" rx="2" className="bg" />
                <rect width={Math.max(2, Math.min(1, l.util) * (W - 16))} height="4" rx="2" className="fg" />
              </g>
            )}
          </g>
        );
      })}
    </svg>
  );
}

export const KIND_LABEL = (k: Kind) => KINDS[k].label;
