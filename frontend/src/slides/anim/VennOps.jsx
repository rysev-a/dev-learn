import { useEffect, useState } from "react";

/* Анимированная диаграмма Венна для слайда «Три операции».
   Круги сближаются, затем по очереди подсвечиваются результаты операций:
   элементы-точки в результате увеличиваются, остальные тускнеют. Режим можно
   выбрать вручную — тогда автосмена останавливается. Цвета — из переменных
   --s-*, поэтому обе темы работают; при prefers-reduced-motion анимации и
   автосмена отключены. */

const DOTS = [
  { n: 1, x: 112, y: 68, in: "a" },
  { n: 2, x: 112, y: 104, in: "a" },
  { n: 3, x: 180, y: 68, in: "ab" },
  { n: 4, x: 180, y: 104, in: "ab" },
  { n: 5, x: 248, y: 68, in: "b" },
  { n: 6, x: 248, y: 104, in: "b" },
];

const MODES = [
  {
    key: "union",
    label: "A ∪ B",
    name: "Объединение",
    note: "всё, что есть хотя бы в одном множестве",
    hit: (d) => true,
  },
  {
    key: "inter",
    label: "A ∩ B",
    name: "Пересечение",
    note: "только то, что есть в обоих",
    hit: (d) => d.in === "ab",
  },
  {
    key: "diff",
    label: "A \\ B",
    name: "Разность",
    note: "из A без того, что есть в B",
    hit: (d) => d.in === "a",
  },
];

const STEP_MS = 3200;

export default function VennOps() {
  const reduce =
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const [joined, setJoined] = useState(reduce);
  const [mode, setMode] = useState(reduce ? 0 : -1);
  const [auto, setAuto] = useState(!reduce);

  useEffect(() => {
    if (reduce) return;
    const t = setTimeout(() => setJoined(true), 120);
    return () => clearTimeout(t);
  }, [reduce]);

  useEffect(() => {
    if (!auto) return;
    const t = setTimeout(
      () => setMode((m) => (m + 1) % MODES.length),
      mode === -1 ? 1100 : STEP_MS,
    );
    return () => clearTimeout(t);
  }, [auto, mode]);

  const cur = mode >= 0 ? MODES[mode] : null;
  const result = cur ? DOTS.filter(cur.hit).map((d) => d.n) : [];

  return (
    <div className="a-stage">
      <div className="a-chips" role="tablist">
        {MODES.map((m, i) => (
          <button
            key={m.key}
            className={`a-chip ${i === mode ? "on" : ""}`}
            onClick={() => {
              setAuto(false);
              setMode(i);
            }}
          >
            <span className="a-chip-big">{m.label}</span>
            <span className="a-chip-name">{m.name}</span>
          </button>
        ))}
        <button
          className="a-chip ghost"
          title="Показать заново"
          onClick={() => {
            setMode(-1);
            setJoined(false);
            setAuto(true);
            setTimeout(() => setJoined(true), 120);
          }}
        >
          ↻
        </button>
      </div>

      <svg viewBox="0 0 360 170" className="a-svg" aria-hidden="true">
        <defs>
          <clipPath id="vn-a">
            <circle cx="140" cy="85" r="62" />
          </clipPath>
          <mask id="vn-diff">
            <rect width="360" height="170" fill="#000" />
            <circle cx="140" cy="85" r="62" fill="#fff" />
            <circle cx="220" cy="85" r="62" fill="#000" />
          </mask>
        </defs>

        <g className={`a-circle a-left ${joined ? "joined" : ""}`}>
          <circle cx="140" cy="85" r="62" className="a-ring a" />
        </g>
        <g className={`a-circle a-right ${joined ? "joined" : ""}`}>
          <circle cx="220" cy="85" r="62" className="a-ring b" />
        </g>

        <g className={joined ? "a-fills on" : "a-fills"}>
          <circle
            cx="140"
            cy="85"
            r="62"
            className={`a-fill acc ${cur?.key === "union" ? "on" : ""}`}
          />
          <circle
            cx="220"
            cy="85"
            r="62"
            className={`a-fill acc ${cur?.key === "union" ? "on" : ""}`}
          />
          <circle
            cx="220"
            cy="85"
            r="62"
            clipPath="url(#vn-a)"
            className={`a-fill amb ${cur?.key === "inter" ? "on" : ""}`}
          />
          <rect
            width="360"
            height="170"
            mask="url(#vn-diff)"
            className={`a-fill blu ${cur?.key === "diff" ? "on" : ""}`}
          />
        </g>

        <text x="92" y="30" className="a-set-label">
          A
        </text>
        <text x="268" y="30" className="a-set-label">
          B
        </text>

        {DOTS.map((d) => {
          const hit = cur ? cur.hit(d) : true;
          return (
            <g
              key={d.n}
              className={`a-dot ${joined ? "show" : ""} ${hit ? "hit" : "dim"}`}
              style={{ transform: `translate(${d.x}px, ${d.y}px)` }}
            >
              <circle r="11" />
              <text y="4" textAnchor="middle">
                {d.n}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="a-result" key={cur ? cur.key : "intro"}>
        {cur ? (
          <>
            <span className="a-result-expr">{cur.label}</span>
            <span className="a-result-eq">=</span>
            <span className="a-result-set">
              {"{ "}
              {result.join(", ")}
              {" }"}
            </span>
            <span className="a-result-note">{cur.note}</span>
          </>
        ) : (
          <span className="a-result-note">
            A = {"{1, 2, 3, 4}"} · B = {"{3, 4, 5, 6}"} — общие элементы 3 и 4
          </span>
        )}
      </div>
    </div>
  );
}
