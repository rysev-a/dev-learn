import { useEffect, useRef, useState, type ReactNode } from "react";
import { useSlideAudioTime } from "../../lib/slideAudio.ts";
import { motionOff } from "../../lib/settings.ts";

/* Общий набор для пошаговых анимаций на слайдах.

   useSteps(cues, ms): шаг сцены. cues — секунды от начала абзаца, когда
   наступает шаги 1, 2, …; шаг 0 — с начала. Пока слайд озвучивается, шаг
   берётся из времени голоса (приблизительно, по паузам в озвучке), иначе
   сцена сама проходит шаги по таймеру (ms на шаг) и останавливается на
   последнем. Кнопка шага отдаёт управление руке до нового запуска
   звука. При prefers-reduced-motion сцена сразу показывает последний шаг. */

// Сцена появляется чисто на CSS (.a-stage, .a-svg в App.css: прозрачность с
// задержкой — первые кадры, пока устаканивается состояние, не видны);
// движение внутри сцены стартует после REVEAL_MS.
export const REVEAL_MS = 800;

/** управление шагами сцены (результат useSteps) */
export interface StepsCtl {
  step: number;
  last: number;
  pick: (i: number) => void;
}

/** Цвет стрелки и фигуры в старых сценах: m g y r b */
export type Hue = "m" | "g" | "y" | "r" | "b";

export function useSteps(cues: number[], ms = 2800): StepsCtl {
  const last = cues.length;
  const audioT = useSlideAudioTime();
  const [step, setStep] = useState(motionOff() ? last : 0);
  const [manual, setManual] = useState(false);
  const [auto, setAuto] = useState(!motionOff());
  const had = useRef(false);

  useEffect(() => {
    const has = audioT != null;
    if (has && !had.current) setManual(false);
    had.current = has;
  }, [audioT]);

  const synced = audioT != null && !manual;
  useEffect(() => {
    if (synced || !auto || step >= last) return;
    const t = setTimeout(() => setStep((s: number) => s + 1), step === 0 ? REVEAL_MS + 900 : ms);
    return () => clearTimeout(t);
  }, [synced, auto, step, last, ms]);

  let cur = step;
  if (synced && audioT != null) cur = cues.filter((c) => audioT >= c).length;

  return {
    step: cur,
    last,
    pick: (i: number) => {
      setManual(true);
      setAuto(false);
      setStep(i);
    },
  };
}

const HEAD_COLORS: Record<Hue, string> = {
  m: "var(--s-muted)",
  g: "var(--s-accent)",
  y: "var(--s-amber)",
  r: "var(--s-red)",
  b: "var(--s-blue)",
};
const STROKE: Record<Hue, string> = {
  m: "var(--s-muted)",
  g: "var(--s-accent)",
  y: "var(--s-amber)",
  r: "var(--s-red)",
  b: "var(--s-blue)",
};

// Оболочка: кнопки шагов, сцена, подпись шага. labels[i] — название шага i.
export function Steps({ ctl, labels, caption, h = 170, children }: {
  ctl: StepsCtl;
  labels: string[];
  caption: string[];
  h?: number;
  children?: ReactNode;
}) {
  return (
    <div className="a-stage">
      <div className="a-chips" role="tablist">
        {labels.map((l, i) => (
          <button
            key={i}
            className={`a-chip ${i === ctl.step ? "on" : ""}`}
            onClick={() => ctl.pick(i)}
          >
            <span className="a-chip-lbl">{l}</span>
          </button>
        ))}
      </div>
      <svg viewBox={`0 0 360 ${h}`} className="a-svg" aria-hidden="true">
        <defs>
          {Object.entries(HEAD_COLORS).map(([k, c]) => (
            <marker
              key={k}
              id={`a-hd-${k}`}
              viewBox="0 0 10 10"
              refX="9"
              refY="5"
              markerWidth="7"
              markerHeight="7"
              orient="auto-start-reverse"
            >
              <path d="M0 1 L10 5 L0 9 z" style={{ fill: c }} />
            </marker>
          ))}
        </defs>
        {children}
      </svg>
      <div className="a-result" key={ctl.step}>
        <span className="a-result-note">{caption[ctl.step]}</span>
      </div>
    </div>
  );
}

// Плавно движущийся узел SVG: позиция, прозрачность, масштаб.
export function G({ x = 0, y = 0, o = 1, s = 1, children, className = "" }: {
  x?: number;
  y?: number;
  o?: number;
  s?: number;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <g
      className={`a-t ${className}`}
      style={{
        transform: `translate(${x}px, ${y}px) scale(${s})`,
        opacity: o,
      }}
    >
      {children}
    </g>
  );
}

// Плашка с текстом по центру, (x, y) — центр.
interface ShapeProps {
  x: number;
  y: number;
  o?: number;
  s?: number;
  stroke?: string;
  fill?: string;
  fillOpacity?: number;
  color?: string;
  size?: number;
  text?: ReactNode;
}

export function Pill({
  x,
  y,
  w = 50,
  h = 20,
  text,
  o = 1,
  s = 1,
  stroke = "var(--s-border)",
  fill = "var(--s-panel2)",
  fillOpacity = 1,
  color = "var(--s-text)",
  size = 10.5,
}: ShapeProps & { w?: number; h?: number }) {
  return (
    <G x={x} y={y} o={o} s={s}>
      <rect
        x={-w / 2}
        y={-h / 2}
        width={w}
        height={h}
        rx="6"
        style={{ stroke, fill, fillOpacity, strokeWidth: 1.4 }}
      />
      <text
        y="3.7"
        textAnchor="middle"
        className="a-mono"
        style={{ fill: color, fontSize: size }}
      >
        {text}
      </text>
    </G>
  );
}

// Кружок-элемент с подписью, (x, y) — центр.
export function Dot({
  x,
  y,
  r = 11,
  text,
  o = 1,
  s = 1,
  stroke = "var(--s-muted)",
  fill = "var(--s-panel2)",
  fillOpacity = 1,
  color = "var(--s-text)",
  size = 10.5,
}: ShapeProps & { r?: number }) {
  return (
    <G x={x} y={y} o={o} s={s}>
      <circle r={r} style={{ stroke, fill, fillOpacity, strokeWidth: 1.6 }} />
      {text != null && (
        <text
          y="3.7"
          textAnchor="middle"
          className="a-mono"
          style={{ fill: color, fontSize: size }}
        >
          {text}
        </text>
      )}
    </G>
  );
}

// Подпись; o — прозрачность (плавное появление).
export function Txt({ x, y, o = 1, anchor = "middle", children, mono, color, size }: {
  x: number;
  y: number;
  o?: number;
  anchor?: "start" | "middle" | "end";
  children?: ReactNode;
  mono?: boolean;
  color?: string;
  size?: number;
}) {
  return (
    <text
      x={x}
      y={y}
      textAnchor={anchor}
      className={`a-t ${mono ? "a-mono" : "a-cap"}`}
      style={{ opacity: o, fill: color, fontSize: size }}
    >
      {children}
    </text>
  );
}

// Стрелка (x1,y1)→(x2,y2); c — цвет: m/g/y/r/b; both — наконечники с обеих сторон.
export function Arrow({ x1, y1, x2, y2, c = "m", o = 1, dash, both, w = 1.6 }: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  c?: Hue;
  o?: number;
  dash?: string;
  both?: boolean;
  w?: number;
}) {
  return (
    <line
      className="a-t"
      x1={x1}
      y1={y1}
      x2={x2}
      y2={y2}
      markerEnd={`url(#a-hd-${c})`}
      markerStart={both ? `url(#a-hd-${c})` : undefined}
      style={{ stroke: STROKE[c], strokeWidth: w, strokeDasharray: dash, opacity: o }}
    />
  );
}

// Петля у узла (x, y): стрелка от узла к самому себе, вверх.
export function Loop({ x, y, r = 11, c = "g", o = 1 }: { x: number; y: number; r?: number; c?: Hue; o?: number }) {
  return (
    <path
      className="a-t"
      d={`M${x - 6} ${y - r + 1} C${x - 22} ${y - r - 24} ${x + 22} ${y - r - 24} ${x + 6} ${y - r + 1}`}
      markerEnd={`url(#a-hd-${c})`}
      style={{ fill: "none", stroke: STROKE[c], strokeWidth: 1.6, opacity: o }}
    />
  );
}

// Таблица-матрица отношения: rows × cols клеток; mark(r, c) → цвет m/g/y/r/b или null.
export function Matrix({ x, y, rows, cols, mark, cell = 24, o = 1, rowTitle, colTitle }: {
  x: number;
  y: number;
  rows: ReactNode[];
  cols: ReactNode[];
  mark: (r: number, c: number) => Hue | null | undefined | false | "";
  cell?: number;
  o?: number;
  rowTitle?: ReactNode;
  colTitle?: ReactNode;
}) {
  return (
    <G x={x} y={y} o={o}>
      {cols.map((l, c) => (
        <text key={`c${c}`} x={c * cell + cell / 2} y="-5" textAnchor="middle" className="a-mono" style={{ fontSize: 10 }}>
          {l}
        </text>
      ))}
      {rows.map((l, r) => (
        <text key={`r${r}`} x="-7" y={r * cell + cell / 2 + 3.5} textAnchor="end" className="a-mono" style={{ fontSize: 10 }}>
          {l}
        </text>
      ))}
      {rows.map((_, r) =>
        cols.map((__, c) => {
          const m = mark(r, c);
          return (
            <rect
              key={`${r}-${c}`}
              className="a-t"
              x={c * cell + 1.5}
              y={r * cell + 1.5}
              width={cell - 3}
              height={cell - 3}
              rx="4"
              style={{
                fill: m ? STROKE[m] : "var(--s-panel2)",
                fillOpacity: m ? 0.45 : 1,
                stroke: m ? STROKE[m] : "var(--s-border)",
                strokeWidth: 1.2,
              }}
            />
          );
        }),
      )}
      {rowTitle && (
        <text x="-7" y="-5" textAnchor="end" className="a-cap">
          {rowTitle}
        </text>
      )}
      {colTitle && (
        <text x={(cols.length * cell) / 2} y={rows.length * cell + 13} textAnchor="middle" className="a-cap">
          {colTitle}
        </text>
      )}
    </G>
  );
}

// Таблица истинности: head — заголовки столбцов, rows — строки значений (0/1 или текст);
// hl(r, c) → цвет m/g/y/r/b или null; rowOn(r) → показывать ли строку (для поочерёдного появления).
export function Table({ x, y, head, rows, cw = 30, rh = 20, hl, rowOn, o = 1, delay = 0 }: {
  x: number;
  y: number;
  head: ReactNode[];
  rows: (string | number)[][];
  cw?: number;
  rh?: number;
  hl?: (r: number, c: number) => Hue | null | undefined | false | "";
  rowOn?: (r: number) => boolean;
  o?: number;
  delay?: number;
}) {
  return (
    <G x={x} y={y} o={o}>
      {head.map((h, c) => (
        <text key={c} x={c * cw + cw / 2} y="-5" textAnchor="middle" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-accent)" }}>
          {h}
        </text>
      ))}
      <line x1="0" y1="0" x2={head.length * cw} y2="0" style={{ stroke: "var(--s-border)", strokeWidth: 1.2 }} />
      {rows.map((row, r) => {
        const on = rowOn ? rowOn(r) : true;
        return (
          <g key={r} className="a-t" style={{ opacity: on ? 1 : 0, transitionDelay: on ? `${delay * r}ms` : "0ms" }}>
            {row.map((v, c) => {
              const m = hl ? hl(r, c) : null;
              return (
                <g key={c}>
                  <rect
                    x={c * cw + 1.5}
                    y={r * rh + 2}
                    width={cw - 3}
                    height={rh - 3}
                    rx="4"
                    style={{ fill: m ? STROKE[m] : "none", fillOpacity: m ? 0.35 : 0, stroke: m ? STROKE[m] : "none", strokeWidth: 1.2 }}
                  />
                  <text
                    x={c * cw + cw / 2}
                    y={r * rh + rh / 2 + 4}
                    textAnchor="middle"
                    className="a-mono"
                    style={{ fontSize: 10.5, fill: v === 1 ? "var(--s-accent)" : v === 0 ? "var(--s-red)" : "var(--s-text)" }}
                  >
                    {v}
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}
    </G>
  );
}

// Граф: nodes — [{x, y, l}], edges — [{a, b, w?}]; directed — со стрелками.
// nc(i) → цвет вершины m/g/y/r/b; ec(e, i) → цвет ребра или null (скрыто); r — радиус вершины.
export interface GraphNode {
  x: number;
  y: number;
  l: ReactNode;
}
export interface GraphEdge {
  a: number;
  b: number;
  w?: ReactNode;
}

export function GraphView({ nodes, edges, directed, nc, ec, r = 13, o = 1, lsize = 10.5, ow }: {
  nodes: GraphNode[];
  edges: GraphEdge[];
  directed?: boolean;
  nc?: (i: number) => Hue | null | undefined | false | "";
  ec?: (e: GraphEdge, i: number) => Hue | null | undefined | false | "";
  r?: number;
  o?: number;
  lsize?: number;
  ow?: (i: number) => number;
}) {
  return (
    <G o={o}>
      {edges.map((e, i) => {
        const A = nodes[e.a];
        const B = nodes[e.b];
        const dx = B.x - A.x;
        const dy = B.y - A.y;
        const d = Math.hypot(dx, dy) || 1;
        const pad = r + (directed ? 3 : 0);
        const c = ec ? ec(e, i) : "m";
        return (
          <g key={i}>
            <line
              className="a-t"
              x1={A.x + (dx / d) * (directed ? r + 1 : 0)}
              y1={A.y + (dy / d) * (directed ? r + 1 : 0)}
              x2={B.x - (dx / d) * (directed ? pad : 0)}
              y2={B.y - (dy / d) * (directed ? pad : 0)}
              markerEnd={directed && c ? `url(#a-hd-${c})` : undefined}
              style={{ stroke: c ? STROKE[c] : "var(--s-border)", strokeWidth: c && c !== "m" ? 2 : 1.4, opacity: c ? 1 : 0 }}
            />
            {e.w != null && (
              <text x={(A.x + B.x) / 2} y={(A.y + B.y) / 2 - 4} textAnchor="middle" className="a-mono" style={{ fontSize: 9.5, fill: "var(--s-amber)" }}>
                {e.w}
              </text>
            )}
          </g>
        );
      })}
      {nodes.map((n, i) => {
        const c = nc ? nc(i) : "m";
        const on = ow ? ow(i) : 1;
        return (
          <g key={i} className="a-t" style={{ transform: `translate(${n.x}px, ${n.y}px)`, opacity: on }}>
            <circle r={r} style={{ fill: c && c !== "m" ? STROKE[c] : "var(--s-panel2)", fillOpacity: c && c !== "m" ? 0.3 : 1, stroke: c ? STROKE[c] : "var(--s-border)", strokeWidth: 1.8 }} />
            <text y="3.8" textAnchor="middle" className="a-mono" style={{ fontSize: lsize }}>
              {n.l}
            </text>
          </g>
        );
      })}
    </G>
  );
}
