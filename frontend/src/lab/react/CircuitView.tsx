import GateShape from "./GateShape.tsx";
import { useToBoard } from "./useBoardView.tsx";
import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from "react";
import {
  BOARD_H,
  BOARD_W,
  GATE_W,
  INPUT_X,
  OUT_PIN_X,
  OUT_X,
  inputYs,
  outputYs,
  pinPos,
  wirePath,
  type GateInstance,
  type InputId,
  type NodeValue,
  type PinKind,
  type PinRef,
  type Point,
  type Wire,
} from "../exercises/logic-gates/circuit.model.ts";
import type { BlockInterface, ValueScope } from "../exercises/logic-gates/blocks.ts";
import {
  gatePinY,
  gatePinsOf,
} from "../exercises/logic-gates/gate-shapes.ts";
import {
  ZOOM,
  clampWorld,
  viewBoxOf,
  wheelFactor,
  zoomAround,
} from "../exercises/logic-gates/board-pan.ts";

/* Схема из вентилей только для просмотра — «внутренность» блока. Значения берутся из общей симуляции,
   сигналы здесь живые. Вентили можно двигать и раздвигать: схема от этого не меняется. */

const cls = (v: NodeValue) => (v === 1 ? "v1" : v === 0 ? "v0" : "vx");
const txt = (v: NodeValue) => (v === undefined ? "?" : String(v));
/** равномерная раскладка узлов по высоте доски h */
const spreadYs = (names: readonly string[], h: number): Record<string, number> => {
  const step = names.length > 1 ? (h - 80) / (names.length - 1) : 0;
  return Object.fromEntries(
    names.map((n, i) => [n, names.length === 1 ? h / 2 : 40 + i * step]),
  );
};

interface CircuitViewProps {
  gates: readonly GateInstance[];
  wires: readonly Wire[];
  iface: BlockInterface;
  scope: ValueScope;
  resetKey?: unknown;
  spread?: number;
  fullscreen?: boolean | undefined;
}

interface DragState {
  pan?: { cx: number; cy: number; ox: number; oy: number; scale: number };
  id?: string;
  off?: Point;
}

export default function CircuitView({
  gates,
  wires,
  iface,
  scope,
  resetKey,
  spread = 1,
  fullscreen = false,
}: CircuitViewProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [moved, setMoved] = useState<Record<string, Point>>({});
  const [panning, setPanning] = useState(false);
  const drag = useRef<DragState>({});
  const st = useRef({ pan, zoom, H: 0 });

  const spreadX = (x: number) => Math.round(150 + (x - 150) * spread);
  const spreadY = (y: number) => Math.round(20 + (y - 20) * spread);
  const W =
    spread === 1
      ? BOARD_W
      : Math.max(
          BOARD_W,
          Math.max(0, ...gates.map((g) => spreadX(g.x))) + 110 + 160,
        );
  const extraW = W - BOARD_W;
  const H = useMemo(() => {
    const lowest = Math.max(0, ...gates.map((g) => spreadY(g.y))) + 110;
    const ports = Math.max(iface.inputs.length, iface.outputs.length) * 50 + 40;
    return Math.max(BOARD_H, lowest, ports);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gates, iface, spread]);
  st.current = { pan, zoom, H };

  useEffect(() => {
    setMoved({});
    setPan({ x: 0, y: 0 });
    setZoom(1);
  }, [resetKey]);

  const placed = useMemo(
    () =>
      gates.map((g) => ({
        ...g,
        x: moved[g.id]?.x ?? spreadX(g.x),
        y: moved[g.id]?.y ?? spreadY(g.y),
      })),
    [gates, moved, spread],
  ); // eslint-disable-line react-hooks/exhaustive-deps
  const inputYMap = useMemo(
    () =>
      iface.inputs.length > 4 ? spreadYs(iface.inputs, H) : inputYs(iface.inputs as readonly InputId[]),
    [iface, H],
  );
  const outputYMap = useMemo(
    () =>
      iface.outputs.length > 4
        ? spreadYs(iface.outputs, H)
        : outputYs(iface.outputs),
    [iface, H],
  );
  const pos = (ref: PinRef) => {
    const p = pinPos(ref, placed, outputYMap, inputYMap);
    // колонка выходов при раздвигании уехала вправо вместе с доской
    return ref.pin !== "out" && iface.outputs.includes(ref.node)
      ? { x: p.x + extraW, y: p.y }
      : p;
  };
  const val = (n: string) => scope(n);
  const pinVal = (node: string, pin: PinKind): NodeValue => {
    const w = wires.find((x) => x.to.node === node && x.to.pin === pin);
    return w ? val(w.from.node) : undefined;
  };
  const label = (id: string) => iface.labels?.[iface.inputs.indexOf(id)] ?? id;

  const toBoard = useToBoard(svgRef);
  const metrics = () => {
    const rect = svgRef.current!.getBoundingClientRect();
    const base = Math.min(rect.width / W, rect.height / st.current.H);
    return {
      rect,
      base,
      offX: (rect.width - W * base) / 2,
      offY: (rect.height - st.current.H * base) / 2,
    };
  };

  useEffect(() => {
    const el = svgRef.current;
    if (!el) return undefined;
    const move = (e: PointerEvent) => {
      if (drag.current.pan) {
        const d = drag.current.pan;
        setPan({
          x: Math.round(d.ox - (e.clientX - d.cx) / d.scale),
          y: Math.round(d.oy - (e.clientY - d.cy) / d.scale),
        });
      } else if (drag.current.id && drag.current.off) {
        const p = toBoard(e.clientX, e.clientY);
        const id = drag.current.id;
        const { x, y } = clampWorld(
          { x: p.x - drag.current.off.x, y: p.y - drag.current.off.y },
          GATE_W,
          48,
        );
        setMoved((m) => ({ ...m, [id]: { x, y } }));
      }
    };
    const up = () => {
      drag.current = {};
      setPanning(false);
    };
    const wheel = (e: WheelEvent) => {
      if (!(e.ctrlKey || e.metaKey) && !el.closest(".fill")) return;
      e.preventDefault();
      const m = metrics();
      const s = st.current;
      const next = zoomAround(
        { pan: s.pan, zoom: s.zoom },
        wheelFactor(e),
        {
          x: e.clientX - m.rect.left - m.offX,
          y: e.clientY - m.rect.top - m.offY,
        },
        m.base,
      );
      setPan(next.pan);
      setZoom(next.zoom);
    };
    const mid = (e: PointerEvent) => {
      if (e.button !== 1) return;
      e.preventDefault();
      e.stopPropagation();
      beginPan(e);
    };
    document.addEventListener("pointermove", move);
    document.addEventListener("pointerup", up);
    el.addEventListener("wheel", wheel, { passive: false });
    el.addEventListener("pointerdown", mid, { capture: true });
    return () => {
      document.removeEventListener("pointermove", move);
      document.removeEventListener("pointerup", up);
      el.removeEventListener("wheel", wheel);
      el.removeEventListener("pointerdown", mid, { capture: true });
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [toBoard]);

  const beginPan = (e: { clientX: number; clientY: number }) => {
    const m = metrics();
    const s = st.current;
    drag.current = {
      pan: {
        cx: e.clientX,
        cy: e.clientY,
        ox: s.pan.x,
        oy: s.pan.y,
        scale: m.base * s.zoom,
      },
    };
    setPanning(true);
  };
  const boardDown = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (e.button !== 0) return;
    if (e.target === svgRef.current || (e.target as Element).classList?.contains("cv-bg")) {
      e.preventDefault();
      beginPan(e);
    }
  };
  const gateDown = (e: ReactPointerEvent<SVGGElement>, g: { id: string; x: number; y: number }) => {
    if (e.button !== 0) return;
    e.preventDefault();
    const p = toBoard(e.clientX, e.clientY);
    drag.current = { id: g.id, off: { x: p.x - g.x, y: p.y - g.y } };
  };
  const zoomBy = (factor: number) => {
    const m = metrics();
    const next = zoomAround(
      { pan, zoom },
      factor,
      {
        x: (m.rect.width - 2 * m.offX) / 2,
        y: (m.rect.height - 2 * m.offY) / 2,
      },
      m.base,
    );
    setPan(next.pan);
    setZoom(next.zoom);
  };
  const reset = () => {
    setPan({ x: 0, y: 0 });
    setZoom(1);
    setMoved({});
  };
  const changed =
    pan.x !== 0 || pan.y !== 0 || zoom !== 1 || Object.keys(moved).length > 0;

  return (
    <div className={`lab-board ${fullscreen ? "fill" : ""}`}>
      <div className="lab-zoom" role="group" aria-label="Масштаб доски">
        <button
          type="button"
          title="Уменьшить"
          onClick={() => zoomBy(1 / ZOOM.step)}
        >
          −
        </button>
        <button
          type="button"
          className="pct"
          title="Масштаб 100 %"
          onClick={() => setZoom(1)}
        >
          {Math.round(zoom * 100)}%
        </button>
        <button
          type="button"
          title="Увеличить"
          onClick={() => zoomBy(ZOOM.step)}
        >
          +
        </button>
        {changed && (
          <button type="button" title="Вернуть вид" onClick={reset}>
            ⌖
          </button>
        )}
      </div>
      <svg
        ref={svgRef}
        className={`lab-board-svg cv ${panning ? "panning" : ""}`}
        viewBox={viewBoxOf(pan, zoom, W, H)}
        onPointerDown={boardDown}
        role="img"
        aria-label="Схема внутри блока (только просмотр)"
      >
        <defs>
          <pattern
            id="cv-dots"
            width="22"
            height="22"
            patternUnits="userSpaceOnUse"
          >
            <circle cx="1.5" cy="1.5" r="1.5" className="grid-dot" />
          </pattern>
        </defs>
        <rect
          className="cv-bg"
          x={pan.x}
          y={pan.y}
          width={W / zoom}
          height={H / zoom}
          fill="url(#cv-dots)"
        />
        {wires.map((w) => (
          <path
            key={w.id}
            className={`wire-line ${cls(val(w.from.node))}`}
            d={wirePath(pos(w.from), pos(w.to))}
          />
        ))}
        {iface.inputs.map((id) => {
          const y = inputYMap[id] ?? 200;
          return (
            <g key={id} className="node">
              <rect
                className="node-box"
                x="10"
                y={y - 22}
                width="86"
                height="44"
                rx="10"
              />
              <text className="node-label" x="30" y={y + 5}>
                {label(id)}
              </text>
              <rect
                className={`node-chip ${cls(val(id))}`}
                x="56"
                y={y - 12}
                width="26"
                height="24"
                rx="7"
              />
              <text className="node-chip-text" x="69" y={y + 5}>
                {txt(val(id))}
              </text>
              <circle
                className={`pin-dot ${cls(val(id))}`}
                cx={INPUT_X}
                cy={y}
                r="5.5"
              />
            </g>
          );
        })}
        {iface.outputs.map((o) => {
          const y = outputYMap[o] ?? 200;
          return (
            <g key={o} className="node" transform={`translate(${extraW} 0)`}>
              <rect
                className="node-box out-box"
                x="788"
                y={y - 22}
                width="86"
                height="44"
                rx="10"
              />
              <text className="node-label" x="812" y={y + 5}>
                {o}
              </text>
              <rect
                className={`node-chip ${cls(val(o))}`}
                x="834"
                y={y - 12}
                width="26"
                height="24"
                rx="7"
              />
              <text className="node-chip-text" x="847" y={y + 5}>
                {txt(val(o))}
              </text>
              <circle
                className={`pin-dot ${cls(val(o))}`}
                cx={OUT_X}
                cy={y}
                r="5.5"
              />
            </g>
          );
        })}
        {placed.map((g) => (
          <g
            key={g.id}
            className="gate"
            transform={`translate(${g.x} ${g.y})`}
            onPointerDown={(e) => gateDown(e, g)}
          >
            <GateShape type={g.type} />
            {gatePinsOf(g.type).map((p) => (
              <circle
                key={p}
                className={`pin-dot ${cls(pinVal(g.id, p))}`}
                cx="-8"
                cy={gatePinY(g.type, p)}
                r="5.5"
              />
            ))}
            <circle
              className={`pin-dot ${cls(val(g.id))}`}
              cx={OUT_PIN_X[g.type]}
              cy="24"
              r="5.5"
            />
            <g
              className="probe"
              transform={`translate(${OUT_PIN_X[g.type] + 20} 24)`}
            >
              <circle r="9" />
              <text y="3.5" textAnchor="middle">
                {txt(val(g.id))}
              </text>
            </g>
          </g>
        ))}
      </svg>
    </div>
  );
}
