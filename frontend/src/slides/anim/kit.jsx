import { useEffect, useRef, useState } from "react";
import { useSlideAudioTime } from "../../lib/slideAudio.js";

/* Общий набор для пошаговых анимаций на слайдах.

   useSteps(cues, ms): шаг сцены. cues — секунды от начала абзаца, когда
   наступает шаги 1, 2, …; шаг 0 — с начала. Пока слайд озвучивается, шаг
   берётся из времени голоса (приблизительно, по паузам в озвучке), иначе
   сцена сама проходит шаги по таймеру (ms на шаг) и останавливается на
   последнем. Кнопка шага отдаёт управление руке до нового запуска
   звука. При prefers-reduced-motion сцена сразу показывает последний шаг. */

// Сцена всплывает ~0,65 с (см. .a-stage в App.css); движение внутри стартует после.
export const REVEAL_MS = 650;

const reduced = () =>
  typeof window !== "undefined" &&
  window.matchMedia &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function useSteps(cues, ms = 2800) {
  const last = cues.length;
  const audioT = useSlideAudioTime();
  const [step, setStep] = useState(reduced() ? last : 0);
  const [manual, setManual] = useState(false);
  const [auto, setAuto] = useState(!reduced());
  const had = useRef(false);

  useEffect(() => {
    const has = audioT != null;
    if (has && !had.current) setManual(false);
    had.current = has;
  }, [audioT]);

  const synced = audioT != null && !manual;
  useEffect(() => {
    if (synced || !auto || step >= last) return;
    const t = setTimeout(() => setStep((s) => s + 1), step === 0 ? REVEAL_MS + 900 : ms);
    return () => clearTimeout(t);
  }, [synced, auto, step, last, ms]);

  let cur = step;
  if (synced) cur = cues.filter((c) => audioT >= c).length;

  return {
    step: cur,
    last,
    pick: (i) => {
      setManual(true);
      setAuto(false);
      setStep(i);
    },
  };
}

// Оболочка: кнопки шагов, сцена, подпись шага. labels[i] — название шага i.
export function Steps({ ctl, labels, caption, children }) {
  return (
    <div className="a-stage">
      <div className="a-chips" role="tablist">
        {labels.map((l, i) => (
          <button
            key={l}
            className={`a-chip ${i === ctl.step ? "on" : ""}`}
            onClick={() => ctl.pick(i)}
          >
            <span className="a-chip-lbl">{l}</span>
          </button>
        ))}
      </div>
      <svg viewBox="0 0 360 170" className="a-svg" aria-hidden="true">
        {children}
      </svg>
      <div className="a-result" key={ctl.step}>
        <span className="a-result-note">{caption[ctl.step]}</span>
      </div>
    </div>
  );
}

// Плавно движущийся узел SVG: позиция, прозрачность, масштаб.
export function G({ x = 0, y = 0, o = 1, s = 1, children, className = "" }) {
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
}) {
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
}) {
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
export function Txt({ x, y, o = 1, anchor = "middle", children, mono, color, size }) {
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
