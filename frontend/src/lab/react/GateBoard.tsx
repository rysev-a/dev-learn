import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type Dispatch,
  type KeyboardEvent as ReactKeyboardEvent,
  type MutableRefObject,
  type PointerEvent as ReactPointerEvent,
  type SetStateAction,
} from "react";
import type { BoardHandle } from "./BlockBoard.tsx";
import {
  BOARD_H,
  BOARD_W,
  GATE_H,
  GATE_W,
  INPUT_X,
  OUT_PIN_X,
  OUT_X,
  createsCycle,
  inputYs,
  outputYs,
  pinPos,
  samePin,
  uid,
  wirePath,
  type Circuit,
  type GateInstance,
  type GateType,
  type InputId,
  type InputState,
  type NodeValue,
  type PinKind,
  type PinRef,
  type Point,
  type Wire,
} from "../exercises/logic-gates/circuit.model.ts";
import {
  gatePinY,
  gatePinsOf,
} from "../exercises/logic-gates/gate-shapes.ts";
import { clampWorld, isClick, viewBoxOf } from "../exercises/logic-gates/board-pan.ts";
import GateShape from "./GateShape.tsx";
import { ZoomControls, boardMetrics, useBoardView, useToBoard } from "./useBoardView.tsx";
import {
  AUTO_WIRE_RADIUS_DEFAULT,
  AUTO_WIRE_RADIUS_FACTOR,
  suggestWires,
  type AutoWire,
} from "../exercises/logic-gates/auto-wire.ts";

/* Доска со схемой из вентилей: элементы, провода, входы и выходы упражнения.
   Всё, что касается мыши и холста: перенос элементов, провода (клик по контакту, затем по другому или
   протянуть), автоподстановка, сдвиг и масштаб. Схему (gates, wires) хозяйничает упражнение; доска меняет
   её через setGates / setWires и сообщает onEdited. */

const DROP_ID = "auto-new";
// высота доски, которую выбрал пользователь (px); хранится в браузере, как в исходном тренажёре
const HEIGHT_KEY = "say-lab-board-height";
const HEIGHT_MIN = 220;
const HEIGHT_MAX = 1400;
const clampHeight = (h: number) =>
  Math.round(Math.min(HEIGHT_MAX, Math.max(HEIGHT_MIN, h)));
const loadHeight = () => {
  try {
    const v = Number(localStorage.getItem(HEIGHT_KEY));
    return Number.isFinite(v) && v > 0 ? clampHeight(v) : null;
  } catch {
    return null;
  }
};
const saveHeight = (h: number|null) => {
  try {
    if (h === null) localStorage.removeItem(HEIGHT_KEY);
    else localStorage.setItem(HEIGHT_KEY, String(h));
  } catch {
    /* без хранилища высота просто не запоминается */
  }
};
const cls = (v: NodeValue) => (v === 1 ? "v1" : v === 0 ? "v0" : "vx");
const txt = (v: NodeValue) => (v === undefined ? "?" : String(v));

/** элемент палитры: тип вентиля, закрыт ли он ещё, подписи */
export interface PaletteItem {
  type: GateType;
  locked: boolean;
  title: string;
  label: string;
}

interface GateBoardProps {
  gates: GateInstance[];
  setGates: Dispatch<SetStateAction<GateInstance[]>>;
  wires: Wire[];
  setWires: Dispatch<SetStateAction<Wire[]>>;
  circuit: Circuit;
  inputs: readonly InputId[];
  labels: readonly string[];
  outputs: readonly string[];
  inputState: InputState;
  clockId?: InputId | null;
  stepsMode: boolean;
  valueFn: (node: string) => NodeValue;
  palette: PaletteItem[];
  guideFocus?: ReadonlySet<string> | null;
  fullscreen?: boolean;
  onToggleInput: (id: InputId) => void;
  onEdited: () => void;
  onMessage: (message: string) => void;
  onLockedPick: (type: GateType) => void;
  boardRef?: MutableRefObject<BoardHandle | null>;
}

/** текущее состояние для глобальных обработчиков документа */
interface LiveState {
  gates: GateInstance[];
  wires: Wire[];
  pending: PinRef | null;
  sticky: boolean;
  hover: PinRef | null;
  placing: GateType | null;
  movingId: string | null;
  movedFar: boolean;
  zoom: number;
  pan: Point;
  worldH: number;
  circuit: Circuit;
  stepsMode: boolean;
  palette: PaletteItem[];
}

interface DragState {
  off?: Point;
  from?: Point;
  pinDown?: Point;
}

export default function GateBoard({
  gates,
  setGates,
  wires,
  setWires,
  circuit,
  inputs,
  labels,
  outputs,
  inputState,
  clockId,
  stepsMode,
  valueFn,
  palette,
  guideFocus,
  fullscreen,
  onToggleInput,
  onEdited,
  onMessage,
  onLockedPick,
  boardRef,
}: GateBoardProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [boardH, setBoardH] = useState(loadHeight); // px или null — высота по умолчанию (по пропорциям доски)
  const [pxW, setPxW] = useState(0); // ширина доски на экране
  const [placing, setPlacing] = useState<GateType | null>(null); // тип переносимого из палитры элемента
  const [cursor, setCursor] = useState<Point | null>(null); // экранные координаты (для «призрака»)
  const [movingId, setMovingId] = useState<string | null>(null);
  const [movedFar, setMovedFar] = useState(false);
  const [pending, setPending] = useState<PinRef | null>(null); // откуда тянется провод
  const [sticky, setSticky] = useState(false);
  const [hover, setHover] = useState<PinRef | null>(null);
  const [cursorBoard, setCursorBoard] = useState<Point | null>(null);
  const drag = useRef<DragState>({}); // изменяемые данные перетаскивания
  const memo = useRef<AutoWire[]>([]);

  const inputYMap = useMemo(() => inputYs(inputs), [inputs]);
  const outputYMap = useMemo(() => outputYs(outputs), [outputs]);

  // Высота доски меняется без смены масштаба: видимое «окно» мира растёт вместе с высотой
  const manualH = !fullscreen && boardH !== null && pxW > 0;
  const worldH = manualH ? (boardH * BOARD_W) / pxW : BOARD_H;
  const view = useBoardView(svgRef, () => boardMetrics(svgRef.current!, BOARD_W, worldH));
  const { pan, zoom, panning, setZoom } = view;

  const st = useRef<LiveState | null>(null);
  const live = (): LiveState => st.current as LiveState;
  st.current = {
    gates,
    wires,
    pending,
    sticky,
    hover,
    placing,
    movingId,
    movedFar,
    zoom,
    pan,
    worldH,
    circuit,
    stepsMode,
    palette,
  };

  useEffect(() => {
    const el = svgRef.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(() =>
      setPxW(el.getBoundingClientRect().width),
    );
    ro.observe(el);
    setPxW(el.getBoundingClientRect().width);
    return () => ro.disconnect();
  }, []);

  const changeHeight = (h: number|null, persist = true) => {
    const next = h === null ? null : clampHeight(h);
    setBoardH(next);
    if (persist) saveHeight(next);
  };
  const resizeDown = (e: ReactPointerEvent) => {
    const svg = svgRef.current;
    if (!svg) return;
    e.preventDefault();
    const startY = e.clientY;
    const startH = svg.getBoundingClientRect().height;
    let last = startH;
    const move = (ev: PointerEvent) => {
      last = clampHeight(startH + ev.clientY - startY);
      setBoardH(last);
    };
    const up = () => {
      document.removeEventListener("pointermove", move);
      document.removeEventListener("pointerup", up);
      saveHeight(clampHeight(last));
    };
    document.addEventListener("pointermove", move);
    document.addEventListener("pointerup", up);
  };
  const resizeKey = (e: ReactKeyboardEvent) => {
    const step = e.key === "ArrowDown" ? 24 : e.key === "ArrowUp" ? -24 : 0;
    if (!step || !svgRef.current) return;
    e.preventDefault();
    changeHeight(svgRef.current.getBoundingClientRect().height + step);
  };

  /** точка экрана → координаты доски */
  const toBoard = useToBoard(svgRef);

  /* ---------- автоподстановка ---------- */
  const dropGate = useMemo(() => {
    if (!placing || !cursor || !svgRef.current) return null;
    const r = svgRef.current.getBoundingClientRect();
    if (
      cursor.x < r.left ||
      cursor.x > r.right ||
      cursor.y < r.top ||
      cursor.y > r.bottom
    )
      return null;
    const at = toBoard(cursor.x, cursor.y);
    const { x, y } = clampWorld(
      { x: at.x - GATE_W / 2, y: at.y - GATE_H / 2 },
      GATE_W,
      GATE_H,
    );
    return { id: DROP_ID, type: placing, x, y };
  }, [placing, cursor, toBoard]);

  const autoFor = useCallback(
    (gate: GateInstance, keep: readonly AutoWire[] = []) =>
      suggestWires({
        keep,
        gate,
        gates: live().gates,
        wires: live().wires,
        inputYMap,
        outputYMap,
        stepsMode,
        radius: AUTO_WIRE_RADIUS_DEFAULT * AUTO_WIRE_RADIUS_FACTOR,
      }),
    [inputYMap, outputYMap, stepsMode],
  );

  const autoWires = useMemo(() => {
    const moving = movingId
      ? movedFar
        ? gates.find((g) => g.id === movingId)
        : null
      : dropGate;
    const list = moving ? autoFor(moving, memo.current) : [];
    memo.current = list;
    return list;
  }, [movingId, movedFar, gates, dropGate, autoFor]);
  const autoRef = useRef<AutoWire[]>([]);
  autoRef.current = autoWires;

  /* ---------- операции над схемой ---------- */
  const addWires = (list: readonly { from: PinRef; to: PinRef }[]) => {
    setWires((all) => [
      ...all,
      ...list.map((w) => ({ id: uid("w"), from: w.from, to: w.to })),
    ]);
    onEdited();
  };

  const place = (type: GateType, at: Point, held: readonly AutoWire[] | null) => {
    const { x, y } = clampWorld(
      { x: at.x - GATE_W / 2, y: at.y - GATE_H / 2 },
      GATE_W,
      GATE_H,
    );
    const gate = { id: uid("g"), type, x, y };
    const remap = (r: PinRef): PinRef => (r.node === DROP_ID ? { ...r, node: gate.id } : r);
    const keep = (held ?? []).map((w) => ({
      ...w,
      from: remap(w.from),
      to: remap(w.to),
    }));
    const auto = held
      ? suggestWires({
          keep,
          gate,
          gates: live().gates,
          wires: live().wires,
          inputYMap,
          outputYMap,
          stepsMode,
          radius: AUTO_WIRE_RADIUS_DEFAULT * AUTO_WIRE_RADIUS_FACTOR,
        })
      : [];
    setGates((list) => [...list, gate]);
    if (auto.length > 0) addWires(auto);
    else onEdited();
  };

  const tryConnect = (a: PinRef, b: PinRef) => {
    const from = a.pin === "out" ? a : b;
    const to = a.pin === "out" ? b : a;
    if (from.pin !== "out" || to.pin === "out" || from.node === to.node) {
      onMessage("Соединять нужно выход элемента со входом другого");
      return;
    }
    const { wires: ws, circuit: c, stepsMode: sm } = live();
    const rest = ws.filter((w) => !samePin(w.to, to));
    if (!sm && createsCycle({ ...c, wires: rest }, from, to)) {
      onMessage("Так схема замкнётся в цикл — сигнал будет бежать по кругу");
      setWires(rest);
      onEdited();
      return;
    }
    setWires([...rest, { id: uid("w"), from, to }]);
    onEdited();
  };

  const cancelWire = useCallback(() => {
    const had = live().pending !== null;
    setPending(null);
    setSticky(false);
    setHover(null);
    setCursorBoard(null);
    return had;
  }, []);
  if (boardRef)
    boardRef.current = {
      cancelWire,
      resetView: view.reset,
    };

  const removeWire = (id: string) => {
    setWires((l) => l.filter((w) => w.id !== id));
    onEdited();
  };
  const removeGate = (id: string) => {
    setGates((l) => l.filter((g) => g.id !== id));
    setWires((l) => l.filter((w) => w.from.node !== id && w.to.node !== id));
    onEdited();
  };

  /* ---------- глобальные обработчики ---------- */
  useEffect(() => {
    const move = (e: PointerEvent) => {
      const s = live();
      if (view.movePan(e)) return;
      if (s.placing) {
        setCursor({ x: e.clientX, y: e.clientY });
        return;
      }
      if (s.movingId) {
        const p = toBoard(e.clientX, e.clientY);
        const off = drag.current.off ?? { x: 0, y: 0 };
        const from = drag.current.from ?? { x: 0, y: 0 };
        const { x, y } = clampWorld(
          { x: p.x - off.x, y: p.y - off.y },
          GATE_W,
          GATE_H,
        );
        const id = s.movingId;
        setGates((list) =>
          list.map((g) => (g.id === id ? { ...g, x, y } : g)),
        );
        if (
          !s.movedFar &&
          Math.hypot(x - from.x, y - from.y) > 6
        )
          setMovedFar(true);
        return;
      }
      if (s.pending) setCursorBoard(toBoard(e.clientX, e.clientY));
    };
    const up = (e: PointerEvent) => {
      const s = live();
      if (view.endPan()) return;
      if (s.placing) {
        const held = autoRef.current;
        const type = s.placing;
        setPlacing(null);
        setCursor(null);
        const el = e.target as Element | null;
        if (el && typeof el.closest === "function") {
          if (el.closest(".lab-board-svg"))
            place(type, toBoard(e.clientX, e.clientY), held);
          else if (el.closest(".lab-palette"))
            place(type, { x: 400, y: 100 + (s.gates.length % 4) * 70 }, null);
        }
        return;
      }
      if (s.movingId) {
        const auto = autoRef.current;
        setMovingId(null);
        setMovedFar(false);
        if (auto.length > 0) addWires(auto);
        return;
      }
      if (s.pending && !s.sticky) {
        const target = s.hover;
        if (target && !samePin(s.pending, target)) {
          tryConnect(s.pending, target);
          cancelWire();
        } else if (drag.current.pinDown && isClick(drag.current.pinDown, e)) setSticky(true);
        else cancelWire();
      }
    };
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape") cancelWire();
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

  const boardDown = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (e.button !== 0 || placing || pending) return;
    if (
      e.target === svgRef.current ||
      (e.target as Element).classList?.contains("lab-board-bg")
    ) {
      e.preventDefault();
      view.beginPan(e);
    }
  };
  // пока провод «прилип» к мыши, нажатие мимо контакта его отменяет

  const gateDown = (e: ReactPointerEvent<SVGGElement>, g: GateInstance) => {
    if (e.button !== 0) return;
    if (sticky) {
      cancelWire();
      return;
    }
    e.preventDefault();
    const p = toBoard(e.clientX, e.clientY);
    drag.current.off = { x: p.x - g.x, y: p.y - g.y };
    drag.current.from = { x: g.x, y: g.y };
    setMovedFar(false);
    setMovingId(g.id);
  };

  const pinDown = (e: ReactPointerEvent<SVGCircleElement>, node: string, pin: PinKind) => {
    e.preventDefault();
    e.stopPropagation();
    if (pending && sticky) {
      const from = pending;
      cancelWire();
      if (!samePin(from, { node, pin })) tryConnect(from, { node, pin });
      return;
    }
    setPending({ node, pin });
    setSticky(false);
    drag.current.pinDown = { x: e.clientX, y: e.clientY };
    setHover(null);
    setCursorBoard(toBoard(e.clientX, e.clientY));
  };
  const pinEnter = (node: string, pin: PinKind) => pending && setHover({ node, pin });
  const pinLeave = (node: string, pin: PinKind) =>
    hover && samePin(hover, { node, pin }) && setHover(null);

  const startPlace = (e: ReactPointerEvent<HTMLButtonElement>, type: GateType) => {
    const item = palette.find((p) => p.type === type);
    if (item?.locked) {
      onLockedPick(type);
      return;
    }
    e.preventDefault();
    setPlacing(type);
    setCursor({ x: e.clientX, y: e.clientY });
  };

  /* ---------- вид ---------- */
  const pos = (ref: PinRef) => pinPos(ref, gates, outputYMap, inputYMap);
  const pinValue = (node: string, pin: PinKind): NodeValue => {
    if (pin === "out") return valueFn(node);
    const w = wires.find((x) => samePin(x.to, { node, pin }));
    return w ? valueFn(w.from.node) : undefined;
  };
  const labelOf = (id: InputId) => labels[inputs.indexOf(id)] ?? id;

  const preview = (() => {
    if (!pending) return null;
    const end = hover ? pos(hover) : cursorBoard;
    return end ? wirePath(pos(pending), end) : null;
  })();
  const dropOk =
    pending &&
    hover &&
    (pending.pin === "out") !== (hover.pin === "out") &&
    pending.node !== hover.node;
  const viewBox = viewBoxOf(pan, zoom, BOARD_W, worldH);

  return (
    <div className={`lab-board ${fullscreen ? "fill" : ""}`}>
      {palette.length > 0 && (
        <div
          className="lab-palette"
          role="toolbar"
          aria-label="Элементы: перетащите на доску или кликните"
        >
          {palette.map((g) => (
            <button
              key={g.type}
              type="button"
              className={`lab-pal-sq ${g.locked ? "locked" : ""}`}
              title={g.title}
              aria-label={g.label}
              onPointerDown={(e) => startPlace(e, g.type)}
            >
              <svg viewBox="-12 0 96 48" aria-hidden="true" overflow="visible">
                <GateShape type={g.type} label={false} />
              </svg>
              {g.locked && <span className="lab-pal-lock">🔒</span>}
            </button>
          ))}
        </div>
      )}
      <ZoomControls zoom={zoom} changed={view.changed} onZoomBy={view.zoomBy} onActual={() => setZoom(1)} onReset={view.reset} />
      <svg
        ref={svgRef}
        className={`lab-board-svg ${panning ? "panning" : ""}`}
        viewBox={viewBox}
        style={manualH ? { height: boardH } : undefined}
        onPointerDown={boardDown}
        role="img"
        aria-label="Интерактивная доска с логическими элементами"
      >
        <defs>
          <pattern
            id="lab-dots"
            width="22"
            height="22"
            patternUnits="userSpaceOnUse"
          >
            <circle cx="1.5" cy="1.5" r="1.5" className="grid-dot" />
          </pattern>
        </defs>
        <rect
          className="lab-board-bg"
          x={pan.x}
          y={pan.y}
          width={BOARD_W / zoom}
          height={worldH / zoom}
          fill="url(#lab-dots)"
        />

        {wires.map((w) => {
          const d = wirePath(pos(w.from), pos(w.to));
          return (
            <g
              key={w.id}
              className={`wire ${guideFocus?.has(w.id) ? "guide-focus" : ""}`}
              onPointerDown={() => removeWire(w.id)}
            >
              <title>Клик — удалить провод</title>
              <path className="wire-hit" d={d} />
              <path
                className={`wire-line ${cls(valueFn(w.from.node))}`}
                d={d}
              />
            </g>
          );
        })}

        {inputs.map((id) => {
          const y = inputYMap[id] ?? 200;
          const v = inputState[id];
          return (
            <g
              key={id}
              className={`input-node ${clockId === id ? "is-clock" : ""}`}
            >
              <g className="node-click" onPointerDown={() => onToggleInput(id)}>
                <title>
                  Клик — переключить {labelOf(id)} ({v} → {1 - v})
                </title>
                <rect
                  className="node-box"
                  x="10"
                  y={y - 22}
                  width="86"
                  height="44"
                  rx="10"
                />
                <text className="node-label" x="30" y={y + 5}>
                  {labelOf(id)}
                </text>
                <rect
                  className={`node-chip ${cls(v)}`}
                  x="56"
                  y={y - 12}
                  width="26"
                  height="24"
                  rx="7"
                />
                <text className="node-chip-text" x="69" y={y + 5}>
                  {v}
                </text>
              </g>
              <g
                className="pin"
                onPointerEnter={() => pinEnter(id, "out")}
                onPointerLeave={() => pinLeave(id, "out")}
              >
                <circle
                  className="pin-hit"
                  cx={INPUT_X}
                  cy={y}
                  r="13"
                  onPointerDown={(e) => pinDown(e, id, "out")}
                />
                <circle
                  className={`pin-dot ${cls(valueFn(id))}`}
                  cx={INPUT_X}
                  cy={y}
                  r="5.5"
                />
              </g>
            </g>
          );
        })}

        {outputs.map((o) => {
          const y = outputYMap[o] ?? 200;
          return (
            <g key={o} className="out-node">
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
                className={`node-chip ${cls(valueFn(o))}`}
                x="834"
                y={y - 12}
                width="26"
                height="24"
                rx="7"
              />
              <text className="node-chip-text" x="847" y={y + 5}>
                {txt(valueFn(o))}
              </text>
              <g
                className="pin"
                onPointerEnter={() => pinEnter(o, "in0")}
                onPointerLeave={() => pinLeave(o, "in0")}
              >
                <circle
                  className="pin-hit"
                  cx={OUT_X}
                  cy={y}
                  r="13"
                  onPointerDown={(e) => pinDown(e, o, "in0")}
                />
                <circle
                  className={`pin-dot ${cls(pinValue(o, "in0"))}`}
                  cx={OUT_X}
                  cy={y}
                  r="5.5"
                />
              </g>
            </g>
          );
        })}

        {gates.map((g) => (
          <g
            key={g.id}
            className={`gate ${guideFocus?.has(g.id) ? "guide-focus" : ""} ${movingId === g.id ? "dragging" : ""}`}
            transform={`translate(${g.x} ${g.y})`}
            onPointerDown={(e) => gateDown(e, g)}
          >
            <GateShape type={g.type} />
            <g
              className="gate-del"
              onPointerDown={(e) => e.stopPropagation()}
              onClick={() => removeGate(g.id)}
            >
              <title>Удалить элемент</title>
              <circle cx="76" cy="0" r="8" />
              <path d="M73 -3 L79 3 M79 -3 L73 3" />
            </g>
            {gatePinsOf(g.type).map((p) => (
              <g
                key={p}
                className="pin"
                transform={`translate(-8 ${gatePinY(g.type, p)})`}
                onPointerEnter={() => pinEnter(g.id, p)}
                onPointerLeave={() => pinLeave(g.id, p)}
              >
                <circle
                  className="pin-hit"
                  r="13"
                  onPointerDown={(e) => pinDown(e, g.id, p)}
                />
                <circle
                  className={`pin-dot ${cls(pinValue(g.id, p))}`}
                  r="5.5"
                />
              </g>
            ))}
            <g
              className="pin"
              onPointerEnter={() => pinEnter(g.id, "out")}
              onPointerLeave={() => pinLeave(g.id, "out")}
            >
              <circle
                className="pin-hit"
                cx={OUT_PIN_X[g.type]}
                cy="24"
                r="13"
                onPointerDown={(e) => pinDown(e, g.id, "out")}
              />
              <circle
                className={`pin-dot ${cls(pinValue(g.id, "out"))}`}
                cx={OUT_PIN_X[g.type]}
                cy="24"
                r="5.5"
              />
            </g>
            <g
              className="probe"
              transform={`translate(${OUT_PIN_X[g.type] + 20} 24)`}
            >
              <circle r="9" />
              <text y="3.5" textAnchor="middle">
                {txt(pinValue(g.id, "out"))}
              </text>
            </g>
          </g>
        ))}

        {autoWires.map((w, i) => (
          <path key={i} className="wire-auto" d={wirePath(w.a, w.b)} />
        ))}
        {preview && (
          <path className={`wire-preview ${dropOk ? "ok" : ""}`} d={preview} />
        )}
      </svg>
      {!fullscreen && (
        // за эту ручку тянут, чтобы изменить высоту доски (двойной щелчок — по умолчанию)
        <button
          type="button"
          className="lab-resize-grip"
          role="separator"
          aria-orientation="horizontal"
          aria-label="Высота доски: потяните вверх или вниз, либо стрелками"
          title="Потяните, чтобы изменить высоту доски (двойной щелчок — по умолчанию)"
          onPointerDown={resizeDown}
          onDoubleClick={() => changeHeight(null)}
          onKeyDown={resizeKey}
        >
          <svg viewBox="0 0 28 8" aria-hidden="true">
            <path d="M2 2h24M2 6h24" />
          </svg>
        </button>
      )}
      {placing && cursor && (
        <div
          className="lab-ghost"
          style={{ left: cursor.x, top: cursor.y }}
          aria-hidden="true"
        >
          <svg viewBox="0 0 84 48" width="56" height="32">
            <GateShape type={placing} label={false} />
          </svg>
        </div>
      )}
    </div>
  );
}
