import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type Dispatch,
  type MouseEvent as ReactMouseEvent,
  type MutableRefObject,
  type PointerEvent as ReactPointerEvent,
  type SetStateAction,
} from "react";
import { wirePath, type Point } from "../exercises/logic-gates/circuit.model.ts";
import { clampWorld, isClick, viewBoxOf } from "../exercises/logic-gates/board-pan.ts";
import { ZoomControls, boardMetrics, useBoardView, useToBoard } from "./useBoardView.tsx";
import {
  TOP,
  type BlockInstance,
  type BlockInterface,
  type BlockLibrary,
  type BusEnd,
  type BusWire,
  type Expansion,
  type ValueScope,
  addBusWire,
  connectionError,
  endInfo,
  isSourceEnd,
  portValues,
} from "../exercises/logic-gates/blocks.ts";
import {
  BLOCK_W,
  SIDE_W,
  layoutBox,
  pinCenter,
  rowKey,
  sideBoxes,
  type BoxLayout,
  type PinRow,
} from "../exercises/logic-gates/block-layout.ts";
import { busText } from "../exercises/logic-gates/interfaces.ts";

/* Доска с блоками: прямоугольники с типизированными портами, соединяемые шинами. Порт можно раскрыть (▸)
   и тянуть шину от отдельного поля. Типы совместимы только по имени. В режиме readonly (внутренность блока)
   блоки можно двигать на экране — схема не меняется. */

export const BLOCKS_BOARD_W = 880;
export const BLOCKS_BOARD_H = 560;

/** управление доской снаружи: отменить тянущуюся шину, вернуть вид */
export interface BoardHandle {
  cancelWire: () => boolean;
  resetView: () => void;
}

interface BlockBoardProps {
  iface: BlockInterface;
  library: BlockLibrary;
  instances: BlockInstance[];
  setInstances: Dispatch<SetStateAction<BlockInstance[]>>;
  busWires: BusWire[];
  setBusWires: Dispatch<SetStateAction<BusWire[]>>;
  expansion?: Expansion | null;
  scope: ValueScope;
  readonly?: boolean;
  clockNode?: string | null;
  height?: number;
  onToggle?: (node: string) => void;
  onInspect?: (node: string) => void;
  onMessage?: (message: string) => void;
  boardRef?: MutableRefObject<BoardHandle | null>;
  resetKey?: unknown;
  spread?: number;
  fullscreen?: boolean;
}

interface PinHit {
  box: BoxLayout;
  row: PinRow;
  pos: Point;
}

/** текущее состояние для глобальных обработчиков документа (они создаются один раз) */
interface LiveState {
  pending: BusEnd | null;
  sticky: boolean;
  hover: string | null;
  movingId: string | null;
  pan: Point;
  zoom: number;
  pins: Map<string, PinHit>;
  readonly: boolean;
}

interface DragState {
  off?: Point;
  h?: number;
  pinDown?: Point;
  connect?: (a: BusEnd, b: BusEnd) => void;
}

const sameEnd = (a: BusEnd, b: BusEnd): boolean =>
  a.node === b.node && a.port === b.port && a.path === b.path;

export default function BlockBoard({
  iface,
  library,
  instances,
  setInstances,
  busWires,
  setBusWires,
  expansion,
  scope,
  readonly = false,
  clockNode = null,
  height = BLOCKS_BOARD_H,
  onToggle,
  onInspect,
  onMessage,
  boardRef,
  resetKey,
  spread = 1,
  fullscreen = false,
}: BlockBoardProps) {
  /* раздвинуть блоки при просмотре тесной схемы: координаты умножаются, доска растёт */
  const spreadX = (x: number) => Math.round(SIDE_W + 18 + (x - (SIDE_W + 18)) * spread);
  const spreadY = (y: number) => Math.round(20 + (y - 20) * spread);
  const W =
    spread === 1
      ? BLOCKS_BOARD_W
      : Math.max(
          BLOCKS_BOARD_W,
          Math.round(
            Math.max(0, ...instances.map((i) => spreadX(i.x))) +
              BLOCK_W +
              30 +
              SIDE_W +
              6,
          ),
        );
  const H =
    spread === 1
      ? height
      : Math.max(
          height,
          Math.round(Math.max(0, ...instances.map((i) => spreadY(i.y) + 290))),
        );
  const svgRef = useRef<SVGSVGElement>(null);
  const view = useBoardView(svgRef, () => boardMetrics(svgRef.current!, W, H), (svg) => !!svg.closest(".fill"));
  const { pan, zoom, panning, setPan, setZoom } = view;
  const [expanded, setExpanded] = useState<Set<string>>(() => new Set());
  const [pending, setPending] = useState<BusEnd | null>(null);
  const [sticky, setSticky] = useState(false);
  const [cursor, setCursor] = useState<Point | null>(null);
  const [hover, setHover] = useState<string | null>(null);
  const [movingId, setMovingId] = useState<string | null>(null);
  const [moved, setMoved] = useState<Record<string, Point>>({});
  const drag = useRef<DragState>({});
  const st = useRef<LiveState>({
    pending: null,
    sticky: false,
    hover: null,
    movingId: null,
    pan: { x: 0, y: 0 },
    zoom: 1,
    pins: new Map(),
    readonly,
  });

  /* ---------- раскладка ---------- */
  const portsOf = useMemo(
    () => (node: string) =>
      node === TOP
        ? iface.ports
        : library.def(instances.find((i) => i.id === node)?.blockId ?? "")
            ?.ports,
    [iface, library, instances],
  );

  const boxes = useMemo(() => {
    const { inBox, outBox } = sideBoxes(iface.ports, expanded, W);
    const blocks = instances.map((inst) => {
      const def = library.def(inst.blockId);
      return layoutBox(
        inst.id,
        def?.title ?? "Неизвестный блок",
        def?.ports ?? [],
        expanded,
        {
          x: moved[inst.id]?.x ?? spreadX(inst.x),
          y: moved[inst.id]?.y ?? spreadY(inst.y),
          w: BLOCK_W,
        },
        "block",
      );
    });
    return [inBox, outBox, ...blocks];
  }, [iface, library, instances, expanded, moved, W, spread]); // eslint-disable-line react-hooks/exhaustive-deps

  const pins = useMemo(() => {
    const map = new Map<string, PinHit>();
    for (const box of boxes)
      for (const row of box.rows)
        map.set(row.key, { box, row, pos: pinCenter(box, row) });
    return map;
  }, [boxes]);

  const pinFor = (end: BusEnd) => {
    let path = end.path;
    for (;;) {
      const hit = pins.get(rowKey({ ...end, path }));
      if (hit) return hit;
      if (path === "") return undefined;
      const dot = path.lastIndexOf(".");
      path = dot < 0 ? "" : path.slice(0, dot);
    }
  };

  const orient = (a: BusEnd, b: BusEnd) => {
    const ia = endInfo(a, portsOf);
    return ia && isSourceEnd(a, ia) ? { from: a, to: b } : { from: b, to: a };
  };
  const canJoin = (a: BusEnd, b: BusEnd) => {
    const { from, to } = orient(a, b);
    return connectionError(from, to, portsOf) === undefined;
  };

  const wiresView = busWires.flatMap((w) => {
    const a = pinFor(w.from);
    const b = pinFor(w.to);
    if (!a || !b) return [];
    const info = endInfo(w.from, portsOf);
    const values =
      expansion && info ? portValues(scope, expansion, w.from, portsOf) : [];
    const width = info?.length ?? 1;
    const known = values.length > 0 && values.every((v) => v !== undefined);
    const cls =
      width === 1
        ? values[0] === 1
          ? "v1"
          : values[0] === 0
            ? "v0"
            : "vx"
        : known
          ? "bus"
          : "bus vx";
    return [
      {
        id: w.id,
        d: wirePath(a.pos, b.pos),
        mx: (a.pos.x + b.pos.x) / 2,
        my: (a.pos.y + b.pos.y) / 2,
        text: busText(values),
        width,
        cls,
      },
    ];
  });

  const preview = (() => {
    if (!pending) return null;
    const a = pinFor(pending);
    if (!a) return null;
    const target = hover ? pins.get(hover) : undefined;
    const end = target?.pos ?? cursor;
    if (!end) return null;
    const d = a.row.side === "in" ? wirePath(end, a.pos) : wirePath(a.pos, end);
    return { d, ok: !!target && canJoin(pending, target.row.end) };
  })();

  const compatible = useMemo(() => {
    const set = new Set<string>();
    if (!pending) return set;
    for (const [key, p] of pins) if (canJoin(pending, p.row.end)) set.add(key);
    return set;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pending, pins, portsOf]);

  st.current = { pending, sticky, hover, movingId, pan, zoom, pins, readonly };

  /* ---------- координаты ---------- */
  const toBoard = useToBoard(svgRef);

  const cancelWire = useCallback(() => {
    const had = st.current.pending !== null;
    setPending(null);
    setSticky(false);
    setHover(null);
    setCursor(null);
    return had;
  }, []);
  const resetView = () => {
    setPan({ x: 0, y: 0 });
    setZoom(1);
    setMoved({});
  };
  if (boardRef) boardRef.current = { cancelWire, resetView };

  // другая схема внутри просмотра — раскладка начинается заново
  useEffect(() => {
    setMoved({});
    setPan({ x: 0, y: 0 });
    setZoom(1);
    setExpanded(new Set());
    cancelWire();
  }, [resetKey, cancelWire]);

  const nextWireId = () => {
    const used = new Set(busWires.map((w) => w.id));
    let n = used.size + 1;
    while (used.has(`b${n}`)) n++;
    return `b${n}`;
  };
  const connect = (a: BusEnd, b: BusEnd) => {
    const { from, to } = orient(a, b);
    const error = connectionError(from, to, portsOf);
    if (error) {
      onMessage?.(error);
      return;
    }
    const id = nextWireId();
    setBusWires((list) => addBusWire(list, { id, from, to }, portsOf));
  };

  /* ---------- глобальные обработчики ---------- */
  useEffect(() => {
    const move = (e: PointerEvent) => {
      const s = st.current;
      if (view.movePan(e)) return;
      if (s.movingId) {
        const p = toBoard(e.clientX, e.clientY);
        const off = drag.current.off ?? { x: 0, y: 0 };
        const { x, y } = clampWorld(
          { x: p.x - off.x, y: p.y - off.y },
          BLOCK_W,
          drag.current.h ?? 80,
        );
        const id = s.movingId;
        if (s.readonly) setMoved((m) => ({ ...m, [id]: { x, y } }));
        else
          setInstances((list) =>
            list.map((i) => (i.id === id ? { ...i, x, y } : i)),
          );
        return;
      }
      if (s.pending) setCursor(toBoard(e.clientX, e.clientY));
    };
    const up = (e: PointerEvent) => {
      const s = st.current;
      if (view.endPan()) return;
      if (s.movingId) {
        setMovingId(null);
        return;
      }
      if (!s.pending || s.sticky) return;
      const target = s.hover ? s.pins.get(s.hover) : undefined;
      if (target && !sameEnd(s.pending, target.row.end)) {
        drag.current.connect?.(s.pending, target.row.end);
        cancelWire();
      } else if (drag.current.pinDown && isClick(drag.current.pinDown, e)) setSticky(true);
      else cancelWire();
    };
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape" && st.current.pending) cancelWire();
    };
    // пока шина тянется за мышью, нажатие мимо порта её отменяет
    const cancelOnDown = (e: PointerEvent) => {
      const s = st.current;
      if (!s.sticky || e.button === 1) return;
      const t = e.target as Element | null;
      if (!t || typeof t.closest !== "function") return;
      if (t.closest(".bpin-hit") || t.closest(".lab-zoom")) return;
      cancelWire();
      if (svgRef.current?.contains(t)) {
        e.preventDefault();
        e.stopPropagation();
      }
    };
    document.addEventListener("pointermove", move);
    document.addEventListener("pointerup", up);
    document.addEventListener("keydown", key);
    document.addEventListener("pointerdown", cancelOnDown, true);
    return () => {
      document.removeEventListener("pointermove", move);
      document.removeEventListener("pointerup", up);
      document.removeEventListener("keydown", key);
      document.removeEventListener("pointerdown", cancelOnDown, true);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [toBoard, cancelWire]);
  drag.current.connect = connect;

  const boardDown = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (e.button !== 0 || pending) return;
    if (e.target === svgRef.current || (e.target as Element).classList?.contains("bb-bg")) {
      e.preventDefault();
      view.beginPan(e);
    }
  };

  /* ---------- действия ---------- */
  const pinDown = (e: ReactPointerEvent<SVGCircleElement>, row: PinRow) => {
    if (readonly) return;
    e.preventDefault();
    e.stopPropagation();
    if (pending && sticky) {
      const from = pending;
      cancelWire();
      if (!sameEnd(from, row.end)) connect(from, row.end);
      return;
    }
    setPending(row.end);
    setSticky(false);
    drag.current.pinDown = { x: e.clientX, y: e.clientY };
    setHover(null);
    setCursor(toBoard(e.clientX, e.clientY));
  };
  const boxDown = (e: ReactPointerEvent<SVGElement>, box: BoxLayout) => {
    if (box.kind !== "block" || e.button !== 0) return;
    e.preventDefault();
    const p = toBoard(e.clientX, e.clientY);
    drag.current.off = { x: p.x - box.x, y: p.y - box.y };
    drag.current.h = box.h;
    setMovingId(box.node);
  };
  const toggleExpand = (row: PinRow, e: ReactPointerEvent<SVGGElement>) => {
    e.stopPropagation();
    e.preventDefault();
    setExpanded((set) => {
      const next = new Set(set);
      if (next.has(row.key)) {
        for (const k of next)
          if (k === row.key || k.startsWith(`${row.key}.`)) next.delete(k);
      } else next.add(row.key);
      return next;
    });
  };
  const removeWire = (id: string) =>
    !readonly && setBusWires((list) => list.filter((w) => w.id !== id));
  const removeInstance = (id: string, e: ReactMouseEvent<SVGGElement>) => {
    e.stopPropagation();
    setInstances((list) => list.filter((i) => i.id !== id));
    setBusWires((list) =>
      list.filter((w) => w.from.node !== id && w.to.node !== id),
    );
  };

  const bit = (node: string) => scope(node);
  const rowText = (row: PinRow) => busText(row.nodes.map((n) => scope(n)));
  const changed =
    pan.x !== 0 || pan.y !== 0 || zoom !== 1 || Object.keys(moved).length > 0;

  return (
    <div className={`lab-board ${fullscreen ? "fill" : ""}`}>
      <ZoomControls zoom={zoom} changed={changed} onZoomBy={view.zoomBy} onActual={() => setZoom(1)} onReset={resetView} />
      <svg
        ref={svgRef}
        className={`lab-board-svg bb ${readonly ? "readonly" : ""} ${panning ? "panning" : ""}`}
        viewBox={viewBoxOf(pan, zoom, W, H)}
        onPointerDown={boardDown}
        role="img"
        aria-label="Доска с блоками и шинами"
      >
        <defs>
          <pattern
            id="bb-dots"
            width="22"
            height="22"
            patternUnits="userSpaceOnUse"
          >
            <circle cx="1.5" cy="1.5" r="1.5" className="grid-dot" />
          </pattern>
        </defs>
        <rect
          className="bb-bg"
          x={pan.x}
          y={pan.y}
          width={W / zoom}
          height={H / zoom}
          fill="url(#bb-dots)"
        />

        {wiresView.map((w) => (
          <g
            key={w.id}
            className={`bwire ${w.width > 1 ? "bus" : ""}`}
            onPointerDown={() => removeWire(w.id)}
          >
            {!readonly && <title>Клик — удалить шину</title>}
            <path className="bwire-hit" d={w.d} />
            <path className={`bwire-line ${w.cls}`} d={w.d} />
            <g className="bwire-tag" transform={`translate(${w.mx} ${w.my})`}>
              <rect
                x={-(w.text.length * 3.6 + 5)}
                y="-8"
                width={w.text.length * 7.2 + 10}
                height="16"
                rx="8"
              />
              <text y="3.5" textAnchor="middle">
                {w.text}
              </text>
            </g>
          </g>
        ))}

        {boxes.map((box) => (
          <g
            key={box.node + box.kind}
            className={`bbox ${box.kind !== "block" ? "top" : ""}`}
            transform={`translate(${box.x} ${box.y})`}
          >
            <rect className="bbox-rect" width={box.w} height={box.h} rx="10" />
            {box.kind === "block" ? (
              <>
                <rect
                  className="bbox-head"
                  width={box.w}
                  height="28"
                  rx="10"
                  onPointerDown={(e) => boxDown(e, box)}
                />
                <text
                  className="bbox-title"
                  x="10"
                  y="18"
                  onPointerDown={(e) => boxDown(e, box)}
                >
                  {box.title}
                </text>
                <g
                  className="bbtn inspect"
                  transform={`translate(${box.w - (readonly ? 14 : 36)} 14)`}
                  onPointerDown={(e) => e.stopPropagation()}
                  onClick={() => onInspect?.(box.node)}
                >
                  <title>Заглянуть внутрь</title>
                  <circle r="9" />
                  <circle className="lens" r="3.2" cx="-0.8" cy="-0.8" />
                  <path className="lens" d="M1.6 1.6 L4.6 4.6" />
                </g>
                {!readonly && (
                  <g
                    className="bbtn del"
                    transform={`translate(${box.w - 14} 14)`}
                    onPointerDown={(e) => e.stopPropagation()}
                    onClick={(e) => removeInstance(box.node, e)}
                  >
                    <title>Убрать блок с доски</title>
                    <circle r="9" />
                    <path d="M-3 -3 L3 3 M3 -3 L-3 3" />
                  </g>
                )}
              </>
            ) : (
              <text className="bbox-title top" x="10" y="18">
                {box.title}
              </text>
            )}

            {box.rows.map((row) => {
              const dim = pending !== null && !compatible.has(row.key);
              const chipW = Math.max(18, row.nodes.length * 8 + 8);
              return (
                <g
                  key={row.key}
                  className={`brow ${dim ? "dim" : ""} ${hover === row.key ? "hover" : ""}`}
                  transform={`translate(0 ${row.y})`}
                >
                  {row.side === "in" ? (
                    <>
                      {row.expandable && (
                        <g
                          className="caret"
                          onPointerDown={(e) => toggleExpand(row, e)}
                        >
                          <title>
                            {row.expanded ? "Свернуть поля" : "Показать поля"}
                          </title>
                          <rect
                            x={8 + row.depth * 10}
                            y="-9"
                            width="14"
                            height="18"
                            rx="4"
                          />
                          <text
                            x={15 + row.depth * 10}
                            y="4"
                            textAnchor="middle"
                          >
                            {row.expanded ? "▾" : "▸"}
                          </text>
                        </g>
                      )}
                      <text
                        className="blabel"
                        x={(row.expandable ? 26 : 12) + row.depth * 10}
                        y="4"
                      >
                        {row.name}
                        <tspan className="btype">: {row.type}</tspan>
                      </text>
                    </>
                  ) : (
                    <>
                      {row.expandable && (
                        <g
                          className="caret"
                          onPointerDown={(e) => toggleExpand(row, e)}
                        >
                          <title>
                            {row.expanded ? "Свернуть поля" : "Показать поля"}
                          </title>
                          <rect
                            x={box.w - 22 - row.depth * 10}
                            y="-9"
                            width="14"
                            height="18"
                            rx="4"
                          />
                          <text
                            x={box.w - 15 - row.depth * 10}
                            y="4"
                            textAnchor="middle"
                          >
                            {row.expanded ? "▾" : "▸"}
                          </text>
                        </g>
                      )}
                      {box.kind !== "top-in" ? (
                        <text
                          className="blabel out"
                          x={
                            box.w - (row.expandable ? 26 : 12) - row.depth * 10
                          }
                          y="4"
                          textAnchor="end"
                        >
                          {row.name}
                          <tspan className="btype">: {row.type}</tspan>
                        </text>
                      ) : (
                        <text className="blabel" x={10 + row.depth * 8} y="4">
                          {row.name}
                        </text>
                      )}
                    </>
                  )}

                  {box.kind === "top-in" &&
                    row.nodes.map((node, i) => (
                      <g
                        key={node}
                        className={`bchip ${bit(node) === 1 ? "v1" : ""} ${node === clockNode ? "clk" : ""} ${readonly ? "static" : ""}`}
                        transform={`translate(${box.w - 16 - (row.nodes.length - i) * 21 - (row.expandable ? 18 : 0)} 0)`}
                        onPointerDown={(e) => e.stopPropagation()}
                        onClick={() => !readonly && onToggle?.(node)}
                      >
                        {!readonly && <title>Клик — переключить</title>}
                        <rect x="0" y="-9" width="18" height="18" rx="5" />
                        <text x="9" y="4" textAnchor="middle">
                          {bit(node) ?? "?"}
                        </text>
                      </g>
                    ))}
                  {box.kind === "top-out" && (
                    <g
                      className="bchip out"
                      transform={`translate(${box.w - 8 - chipW} 0)`}
                    >
                      <rect x="0" y="-9" width={chipW} height="18" rx="5" />
                      <text x={chipW / 2} y="4" textAnchor="middle">
                        {rowText(row)}
                      </text>
                    </g>
                  )}

                  <g
                    className="bpin"
                    data-pin={row.key}
                    onPointerEnter={() => pending && setHover(row.key)}
                    onPointerLeave={() => hover === row.key && setHover(null)}
                  >
                    <title>
                      {row.name}: {row.type}
                    </title>
                    <circle
                      className="bpin-hit"
                      cx={row.side === "in" ? 0 : box.w}
                      cy="0"
                      r="12"
                      onPointerDown={(e) => pinDown(e, row)}
                    />
                    <circle
                      className="bpin-dot"
                      cx={row.side === "in" ? 0 : box.w}
                      cy="0"
                      r={row.nodes.length > 1 ? 6.5 : 5}
                    />
                  </g>
                </g>
              );
            })}
          </g>
        ))}

        {preview && (
          <path
            className={`bwire-preview ${preview.ok ? "ok" : ""}`}
            d={preview.d}
          />
        )}
      </svg>
    </div>
  );
}

export { SIDE_W };
