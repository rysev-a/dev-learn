import { useCallback, useEffect, useMemo, useRef, useState, type PointerEvent as ReactPointerEvent, type ReactNode } from "react";
import { ZoomControls, boardMetrics, useBoardView, useToBoard } from "../../lab/react/useBoardView.tsx";
import { isClick, viewBoxOf } from "../../lab/exercises/logic-gates/board-pan.ts";
import { KINDS } from "../kinds.ts";
import { BOARD_H, BOARD_W } from "../layout.ts";
import { NODE_H, NODE_W, connectError, hasIn, hasOut, inPos, outPos, suggestEdges, wirePath, type Pt } from "../ports.ts";
import type { Kind, NodeLoad, SdEdge, SdNode, SdState } from "../types.ts";

/* Поле схемы (по мотивам досок лаборатории «Архитектура компьютера»):
   — у компонента порты: вход слева, выход справа; связь тянут от выхода ко входу (или кликают по двум портам);
   — компоненты перетаскиваются, из палитры их можно перетащить прямо на поле;
   — подходящие соседи соединяются сами (пунктир-подсказка, пока компонент двигают);
   — поле можно сдвигать (пустое место, средняя кнопка) и масштабировать (Ctrl + колесо, кнопки). */

const W = NODE_W;
const H = NODE_H;
const WORLD = 2600;
const GHOST = "__new__";

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
  auth: (
    <>
      <circle cx="8" cy="12" r="4" />
      <path d="M12 12h9M18 12v3M21 12v2" />
    </>
  ),
  geo: (
    <>
      <path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11Z" />
      <circle cx="12" cy="10" r="2.5" />
    </>
  ),
  ml: (
    <>
      <circle cx="6" cy="7" r="2" />
      <circle cx="6" cy="17" r="2" />
      <circle cx="18" cy="12" r="2.4" />
      <path d="M8 7l8 4M8 17l8-4" />
    </>
  ),
  pay: (
    <>
      <rect x="3" y="6" width="18" height="12" rx="2" />
      <path d="M3 10h18M7 15h3" />
    </>
  ),
  stream: (
    <>
      <path d="M3 8h13l-3-3M21 16H8l3 3" />
    </>
  ),
  notify: (
    <>
      <path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4l2-2Z" />
      <path d="M10 21a2 2 0 0 0 4 0" />
    </>
  ),
  analytics: (
    <>
      <path d="M4 20V10M10 20V4M16 20v-8M22 20H2" />
    </>
  ),
};

const SUMMARY = (n: SdState["nodes"][number]): string => {
  const p = n.params;
  switch (n.kind) {
    case "app":
    case "worker":
      return `×${p["instances"]} · ${p["size"]}`;
    case "lb":
    case "gateway":
    case "ws":
    case "auth":
    case "geo":
    case "ml":
    case "pay":
    case "notify":
    case "analytics":
      return `×${p["instances"]}`;
    case "stream":
      return `${p["partitions"]} парт.`;
    case "blob":
      return p["tier"] === "cold" ? "холодное" : p["tier"] === "mix" ? "гор.+хол." : "горячее";
    case "cache":
      return `${p["sizeGB"]} ГБ${Number(p["replicas"]) > 0 ? ` +${p["replicas"]}р` : ""}`;
    case "db":
      return `${p["size"]}${Number(p["shards"]) > 1 ? ` ·${p["shards"]}ш` : ""}${Number(p["replicas"]) > 0 ? ` +${p["replicas"]}р` : ""}`;
    case "queue":
      return `${p["partitions"]} парт.`;
    case "limiter":
      return `${p["limit"]}/с`;
    case "cdn":
      return `TTL ${p["ttl"]}`;
    case "search":
      return `${p["shards"]}ш ×${p["replicas"]}р`;
    default:
      return "";
  }
};

/** название в одну-две строки: в рамку умещается около 17 знаков в строке */
function nameLines(name: string): string[] {
  const MAX = 17;
  if (name.length <= MAX) return [name];
  const words = name.split(" ");
  let first = "";
  let i = 0;
  while (i < words.length && `${first} ${words[i]}`.trim().length <= MAX) {
    first = `${first} ${words[i]}`.trim();
    i++;
  }
  if (!first) return [`${name.slice(0, MAX - 1)}…`];
  const rest = words.slice(i).join(" ");
  return rest ? [first, rest.length > MAX ? `${rest.slice(0, MAX - 1)}…` : rest] : [first];
}

/** полная подпись узла для всплывающей подсказки: название и все параметры */
function describeNode(n: SdState["nodes"][number]): string {
  const spec = KINDS[n.kind];
  const parts = spec.params.map((p) => {
    const v = n.params[p.key] ?? p.default;
    const opt = p.options?.find((o) => o.value === v);
    return `${p.label}: ${p.type === "bool" ? (v ? "да" : "нет") : (opt?.label ?? String(v))}`;
  });
  return [n.name, ...parts].join("\n");
}

export interface BoardProps {
  state: SdState;
  loads: Record<string, NodeLoad>;
  selected: string | null;
  selectedEdge: number | null;
  down: string[];
  palette: Kind[];
  onSelectNode: (id: string | null) => void;
  onSelectEdge: (i: number | null) => void;
  onMove: (id: string, x: number, y: number, done: boolean) => void;
  /** соединить a → b; вернуть текст ошибки или null */
  onConnect: (from: string, to: string) => string | null;
  /** поставить компонент в точку поля вместе с подставленными связями */
  onPlace: (kind: Kind, x: number, y: number, edges: SdEdge[]) => void;
  /** клик по кнопке палитры: поставить на свободное место */
  onAddDefault: (kind: Kind) => void;
  /** связи, подставленные после перетаскивания существующего компонента */
  onAutoEdges: (edges: SdEdge[]) => void;
  onDelete: () => void;
  onMessage: (text: string) => void;
  /** поле занимает весь экран: высота окна просмотра берётся из размеров на экране */
  fullscreen?: boolean;
  /** кнопки в левом верхнем углу поля (справка, во весь экран) */
  corner?: ReactNode;
  /** плавающая карточка поверх поля (параметры выбранного компонента) */
  overlay?: ReactNode;
}

interface Pending {
  id: string;
  /** с какого порта начали: «out» — тянем от выхода, «in» — от входа */
  pin: "out" | "in";
}

interface Live {
  state: SdState;
  placing: Kind | null;
  movingId: string | null;
  movedFar: boolean;
  pending: Pending | null;
  sticky: boolean;
}

const clampWorld = (v: number) => Math.max(-WORLD, Math.min(WORLD, v));

export default function Board(props: BoardProps) {
  const { state, loads, selected, selectedEdge, down, palette } = props;
  const svgRef = useRef<SVGSVGElement>(null);
  const [placing, setPlacing] = useState<Kind | null>(null);
  const [cursor, setCursor] = useState<Pt | null>(null);
  const [movingId, setMovingId] = useState<string | null>(null);
  const [movedFar, setMovedFar] = useState(false);
  const [pending, setPending] = useState<Pending | null>(null);
  const [sticky, setSticky] = useState(false);
  const [cursorBoard, setCursorBoard] = useState<Pt | null>(null);
  const [hover, setHover] = useState<string | null>(null);
  const drag = useRef<{ dx: number; dy: number; fromX: number; fromY: number; pinDown: Pt | null }>({ dx: 0, dy: 0, fromX: 0, fromY: 0, pinDown: null });
  const memo = useRef<SdEdge[]>([]);
  const propsRef = useRef(props);
  propsRef.current = props;

  const [box, setBox] = useState({ w: 0, h: 0 });
  useEffect(() => {
    const el = svgRef.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(() => {
      const r = el.getBoundingClientRect();
      setBox({ w: r.width, h: r.height });
    });
    ro.observe(el);
    const r = el.getBoundingClientRect();
    setBox({ w: r.width, h: r.height });
    return () => ro.disconnect();
  }, []);
  // высота окна просмотра: на весь экран — по пропорциям экрана, иначе — как у обычного поля
  const worldH = props.fullscreen && box.w > 0 && box.h > 0 ? (BOARD_W * box.h) / box.w : BOARD_H;
  const worldHRef = useRef(worldH);
  worldHRef.current = worldH;
  const view = useBoardView(svgRef, () => boardMetrics(svgRef.current as SVGSVGElement, BOARD_W, worldHRef.current));
  const toBoard = useToBoard(svgRef);

  /** вписать всю схему в окно просмотра */
  const fitRef = useRef<{ pan: Pt; zoom: number } | null>(null);
  const { setPan, setZoom } = view;
  const fit = useCallback(() => {
    const ns = propsRef.current.state.nodes;
    const wh = worldHRef.current;
    if (!ns.length) {
      setPan({ x: 0, y: 0 });
      setZoom(1);
      fitRef.current = { pan: { x: 0, y: 0 }, zoom: 1 };
      return;
    }
    const pad = 30;
    const minX = Math.min(...ns.map((n) => n.x - W / 2)) - pad;
    const maxX = Math.max(...ns.map((n) => n.x + W / 2)) + pad;
    const minY = Math.min(...ns.map((n) => n.y - H / 2)) - pad;
    const maxY = Math.max(...ns.map((n) => n.y + H / 2)) + pad;
    const bw = maxX - minX;
    const bh = maxY - minY;
    const zoom = Math.max(0.3, Math.min(1.6, BOARD_W / bw, wh / bh));
    const pan = { x: Math.round(minX + bw / 2 - BOARD_W / zoom / 2), y: Math.round(minY + bh / 2 - wh / zoom / 2) };
    setZoom(zoom);
    setPan(pan);
    fitRef.current = { pan, zoom };
  }, [setPan, setZoom]);
  const fitted = useRef(false);
  useEffect(() => {
    if (box.w > 0 && !fitted.current) {
      fitted.current = true;
      fit();
    }
  }, [box.w, fit]);
  // после клика по кнопке палитры схема вписывается заново: новый компонент не должен оказаться за краем
  const refitOnAdd = useRef(false);
  useEffect(() => {
    if (refitOnAdd.current) {
      refitOnAdd.current = false;
      fit();
    }
  }, [state.nodes.length, fit]);
  const viewChanged = !fitRef.current || view.zoom !== fitRef.current.zoom || view.pan.x !== fitRef.current.pan.x || view.pan.y !== fitRef.current.pan.y;

  const live = useRef<Live>({ state, placing, movingId, movedFar, pending, sticky });
  live.current = { state, placing, movingId, movedFar, pending, sticky };

  const node = (id: string) => state.nodes.find((n) => n.id === id);

  /* ---------- призрак из палитры и автосвязи ---------- */
  const ghost = useMemo((): SdNode | null => {
    const svg = svgRef.current;
    if (!placing || !cursor || !svg) return null;
    const r = svg.getBoundingClientRect();
    if (cursor.x < r.left || cursor.x > r.right || cursor.y < r.top || cursor.y > r.bottom) return null;
    const p = toBoard(cursor.x, cursor.y);
    return { id: GHOST, kind: placing, name: KINDS[placing].label, x: Math.round(p.x), y: Math.round(p.y), params: {} };
  }, [placing, cursor, toBoard]);

  const autoEdges = useMemo((): SdEdge[] => {
    const moving = movingId ? (movedFar ? state.nodes.find((n) => n.id === movingId) : undefined) : ghost;
    const list = moving ? suggestEdges(state, moving, memo.current) : [];
    memo.current = list;
    return list;
  }, [state, movingId, movedFar, ghost]);
  const autoRef = useRef<SdEdge[]>([]);
  autoRef.current = autoEdges;

  /* ---------- соединение ---------- */
  const connect = useCallback((p: Pending, otherId: string) => {
    const from = p.pin === "out" ? p.id : otherId;
    const to = p.pin === "out" ? otherId : p.id;
    const err = propsRef.current.onConnect(from, to);
    if (err) propsRef.current.onMessage(err);
  }, []);

  const cancelWire = useCallback(() => {
    setPending(null);
    setSticky(false);
    setHover(null);
    setCursorBoard(null);
  }, []);

  /** подходящий компонент под точкой: для подсветки и отпускания провода на теле компонента */
  const nodeAt = (p: Pt, pend: Pending): SdNode | null => {
    let best: { n: SdNode; d: number } | null = null;
    const st = live.current.state;
    const from = st.nodes.find((n) => n.id === pend.id);
    if (!from) return null;
    for (const n of st.nodes) {
      if (n.id === pend.id) continue;
      if (Math.abs(p.x - n.x) > W / 2 + 10 || Math.abs(p.y - n.y) > H / 2 + 10) continue;
      const d = Math.hypot(p.x - n.x, p.y - n.y);
      if (!best || d < best.d) best = { n, d };
    }
    return best?.n ?? null;
  };

  /* ---------- глобальные обработчики мыши ---------- */
  useEffect(() => {
    const move = (e: PointerEvent) => {
      const s = live.current;
      if (view.movePan(e)) return;
      if (s.placing) {
        setCursor({ x: e.clientX, y: e.clientY });
        return;
      }
      if (s.movingId) {
        const p = toBoard(e.clientX, e.clientY);
        const x = Math.round(clampWorld(p.x + drag.current.dx));
        const y = Math.round(clampWorld(p.y + drag.current.dy));
        propsRef.current.onMove(s.movingId, x, y, false);
        if (!s.movedFar && Math.hypot(x - drag.current.fromX, y - drag.current.fromY) > 6) setMovedFar(true);
        return;
      }
      if (s.pending) {
        const p = toBoard(e.clientX, e.clientY);
        setCursorBoard(p);
        setHover(nodeAt(p, s.pending)?.id ?? null);
      }
    };
    const up = (e: PointerEvent) => {
      const s = live.current;
      if (view.endPan()) return;
      if (s.placing) {
        const kind = s.placing;
        const held = autoRef.current;
        setPlacing(null);
        setCursor(null);
        const el = e.target as Element | null;
        if (el && typeof el.closest === "function" && el.closest(".sd-board")) {
          const p = toBoard(e.clientX, e.clientY);
          propsRef.current.onPlace(kind, Math.round(clampWorld(p.x)), Math.round(clampWorld(p.y)), held);
        }
        return;
      }
      if (s.movingId) {
        const id = s.movingId;
        const auto = autoRef.current;
        const far = s.movedFar;
        setMovingId(null);
        setMovedFar(false);
        const n = s.state.nodes.find((x) => x.id === id);
        if (far && n) propsRef.current.onMove(id, n.x, n.y, true);
        if (far && auto.length) propsRef.current.onAutoEdges(auto);
        if (!far) propsRef.current.onSelectNode(id);
        return;
      }
      if (s.pending && !s.sticky) {
        const pend = s.pending;
        const p = toBoard(e.clientX, e.clientY);
        const target = nodeAt(p, pend);
        if (target) {
          connect(pend, target.id);
          cancelWire();
        } else if (drag.current.pinDown && isClick(drag.current.pinDown, e)) setSticky(true);
        else cancelWire();
      }
    };
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape") cancelWire();
      if ((e.key === "Delete" || e.key === "Backspace") && !(e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement || e.target instanceof HTMLTextAreaElement)) {
        propsRef.current.onDelete();
      }
    };
    document.addEventListener("pointermove", move);
    document.addEventListener("pointerup", up);
    document.addEventListener("keydown", key);
    return () => {
      document.removeEventListener("pointermove", move);
      document.removeEventListener("pointerup", up);
      document.removeEventListener("keydown", key);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [toBoard]);

  /* ---------- нажатия ---------- */
  const boardDown = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (e.button !== 0 || placing) return;
    const t = e.target as Element;
    if (t === svgRef.current || t.classList?.contains("sd-bg")) {
      if (pending) {
        cancelWire();
        return;
      }
      e.preventDefault();
      props.onSelectNode(null);
      props.onSelectEdge(null);
      view.beginPan(e);
    }
  };

  const nodeDown = (e: ReactPointerEvent<SVGGElement>, n: SdNode) => {
    if (e.button !== 0) return;
    e.preventDefault();
    if (pending && sticky) {
      const p: Pending = pending;
      cancelWire();
      if (p.id !== n.id) connect(p, n.id);
      return;
    }
    const p = toBoard(e.clientX, e.clientY);
    drag.current = { dx: n.x - p.x, dy: n.y - p.y, fromX: n.x, fromY: n.y, pinDown: null };
    setMovedFar(false);
    setMovingId(n.id);
  };

  const pinDown = (e: ReactPointerEvent<SVGCircleElement>, n: SdNode, pin: "out" | "in") => {
    if (e.button !== 0) return;
    e.preventDefault();
    e.stopPropagation();
    if (pending && sticky) {
      const p: Pending = pending;
      cancelWire();
      if (p.id !== n.id && p.pin !== pin) connect(p, n.id);
      return;
    }
    setPending({ id: n.id, pin });
    setSticky(false);
    drag.current.pinDown = { x: e.clientX, y: e.clientY };
    setHover(null);
    setCursorBoard(toBoard(e.clientX, e.clientY));
  };

  const startPlace = (e: ReactPointerEvent<HTMLButtonElement>, kind: Kind) => {
    e.preventDefault();
    setPlacing(kind);
    setCursor({ x: e.clientX, y: e.clientY });
  };

  /* ---------- вид ---------- */
  const pendNode = pending ? node(pending.id) : undefined;
  const hoverNode = hover ? node(hover) : undefined;
  const hoverErr = pendNode && hoverNode ? (pending?.pin === "out" ? connectError(state, pendNode, hoverNode) : connectError(state, hoverNode, pendNode)) : null;
  const pendPath = (() => {
    if (!pendNode || !pending) return null;
    const own = pending.pin === "out" ? outPos(pendNode) : inPos(pendNode);
    const end = hoverNode ? (pending.pin === "out" ? inPos(hoverNode) : outPos(hoverNode)) : cursorBoard;
    if (!end) return null;
    return pending.pin === "out" ? wirePath(own, end) : wirePath(end, own);
  })();
  /** можно ли соединить порт этого компонента с тем, от которого тянется провод */
  const portState = (n: SdNode, pin: "out" | "in"): "ok" | "bad" | "" => {
    if (!pendNode || !pending) return "";
    if (n.id === pendNode.id) return "";
    if (pin === pending.pin) return "bad";
    const err = pending.pin === "out" ? connectError(state, pendNode, n) : connectError(state, n, pendNode);
    return err ? "bad" : "ok";
  };

  const drawNode = (n: SdNode, ghostNode = false) => {
    const l = loads[n.id];
    const st = down.includes(n.id) ? "down" : (l?.status ?? "idle");
    const cls = ["sd-node", n.kind, st, selected === n.id ? "on" : "", movingId === n.id ? "moving" : "", ghostNode ? "ghost" : "", hover === n.id ? (hoverErr ? "hover-bad" : "hover-ok") : ""].join(" ");
    const lines = nameLines(n.name);
    const showIn = hasIn(n.kind);
    const showOut = hasOut(n.kind);
    return (
      <g key={n.id} className={cls} transform={`translate(${n.x},${n.y})`} onPointerDown={ghostNode ? undefined : (e) => nodeDown(e, n)}>
        <title>{describeNode(n)}</title>
        <rect x={-W / 2} y={-H / 2} width={W} height={H} rx="9" />
        {lines.map((line, i) => (
          <text key={i} className="sd-name" x={0} y={lines.length === 1 ? -5 : -14 + i * 12} textAnchor="middle">
            {line}
          </text>
        ))}
        <g className="sd-ico" transform={`translate(${-W / 2 + 9},5) scale(0.55)`}>
          {ICONS[n.kind]}
        </g>
        <text className="sd-sub" x={-W / 2 + 28} y={15}>
          {st === "down" ? "отключён" : ghostNode ? "" : SUMMARY(n)}
        </text>
        {l && l.status !== "idle" && n.kind !== "monitor" && !ghostNode && (
          <g className="sd-bar" transform={`translate(${-W / 2 + 8},${H / 2 - 8})`}>
            <rect width={W - 16} height="4" rx="2" className="bg" />
            <rect width={Math.max(2, Math.min(1, l.util) * (W - 16))} height="4" rx="2" className="fg" />
          </g>
        )}
        {!ghostNode && showIn && (
          <circle className={`sd-pin in ${portState(n, "in")}`} cx={-W / 2} cy={0} r={5.5} onPointerDown={(e) => pinDown(e, n, "in")}>
            <title>Вход: сюда приходят запросы</title>
          </circle>
        )}
        {!ghostNode && showOut && (
          <circle className={`sd-pin out ${portState(n, "out")}`} cx={W / 2} cy={0} r={5.5} onPointerDown={(e) => pinDown(e, n, "out")}>
            <title>Выход: потяните к входу другого компонента</title>
          </circle>
        )}
      </g>
    );
  };

  return (
    <div className={`sd-boardwrap ${props.fullscreen ? "fill" : ""}`}>
      <div className="sd-toolbar" role="toolbar" aria-label="Компоненты: перетащите на поле или кликните">
        {palette.map((k) => (
          <button key={k} type="button" className="sd-add" title={`${KINDS[k].about}. Перетащите на поле — связи подставятся сами.`} onPointerDown={(e) => startPlace(e, k)} onClick={() => {
              refitOnAdd.current = true;
              props.onAddDefault(k);
            }}>
            + {KINDS[k].label}
          </button>
        ))}
      </div>
      <div className="sd-viewport">
        {props.corner}
        {props.overlay}
        <ZoomControls zoom={view.zoom} changed={viewChanged} onZoomBy={view.zoomBy} onActual={() => view.setZoom(1)} onReset={fit} />
        <svg ref={svgRef} className={`sd-board ${view.panning ? "panning" : ""} ${placing ? "placing" : ""}`} viewBox={viewBoxOf(view.pan, view.zoom, BOARD_W, worldH)} onPointerDown={boardDown} role="img" aria-label="Схема сервиса">
          <defs>
            <pattern id="sd-dots" width="22" height="22" patternUnits="userSpaceOnUse">
              <circle cx="1.5" cy="1.5" r="1.3" className="sd-dot" />
            </pattern>
          </defs>
          <rect className="sd-bg" x={view.pan.x} y={view.pan.y} width={BOARD_W / view.zoom} height={worldH / view.zoom} fill="url(#sd-dots)" />
          {state.edges.map((e, i) => {
            const a = node(e.from);
            const b = node(e.to);
            if (!a || !b) return null;
            const d = wirePath(outPos(a), inPos(b));
            const dead = down.includes(a.id) || down.includes(b.id);
            return (
              <g key={`${e.from}-${e.to}`} className={`sd-edge ${selectedEdge === i ? "on" : ""} ${dead ? "dead" : ""}`}>
                <path className="line" d={d} />
                <path className="hit" d={d} onPointerDown={(ev) => ev.stopPropagation()} onClick={() => props.onSelectEdge(i)} />
              </g>
            );
          })}
          {autoEdges.map((e) => {
            const a = e.from === GHOST ? ghost : node(e.from);
            const b = e.to === GHOST ? ghost : node(e.to);
            if (!a || !b) return null;
            return <path key={`auto-${e.from}-${e.to}`} className="sd-auto" d={wirePath(outPos(a), inPos(b))} />;
          })}
          {pendPath && <path className={`sd-pending ${hoverErr ? "bad" : hoverNode ? "ok" : ""}`} d={pendPath} />}
          {state.nodes.map((n) => drawNode(n))}
          {ghost && drawNode(ghost, true)}
        </svg>
      </div>
      <p className="sd-tip">
        Порты: вход слева, выход справа. Тяните от выхода ко входу (или кликните по двум портам). Компонент, поставленный рядом с подходящими, подключится сам. Ctrl + колесо — масштаб, пустое место — сдвиг, ⌖ — вписать схему.
      </p>
    </div>
  );
}
