import { useEffect, useRef, useState } from "react";
import { useSlideAudioTime } from "../../lib/slideAudio.js";
import { useReveal } from "./kit.jsx";

/* Анимированная диаграмма Венна для слайда «Три операции».

   Сценарий: два множества стоят далеко друг от друга, у каждого свои копии
   общих элементов 3 и 4 (подсвечены). Круги плывут навстречу, копии
   сближаются и сливаются в один элемент — так «получается» множество без
   повторов. После этого по очереди подсвечиваются объединение, пересечение
   и разность. Режим можно выбрать вручную — тогда автосмена останавливается.
   Если слайд сейчас озвучивается, стадии берутся из времени голоса (cues —
   секунды от начала абзаца), иначе всё идёт по таймерам.
   Цвета — из переменных --s-*; при prefers-reduced-motion движение и
   автосмена отключены. */

// apart — положение, пока круги разведены; joined — когда сошлись.
// side: a/b — «своя» копия; dup — копия во втором множестве, которая
// сливается с копией из первого.
const DOTS = [
  { id: "1", n: 1, set: "a", apart: [45, 68], joined: [112, 68] },
  { id: "2", n: 2, set: "a", apart: [45, 104], joined: [112, 104] },
  { id: "3a", n: 3, set: "ab", common: true, apart: [100, 68], joined: [180, 68] },
  { id: "4a", n: 4, set: "ab", common: true, apart: [100, 104], joined: [180, 104] },
  { id: "3b", n: 3, set: "ab", common: true, dup: true, apart: [260, 68], joined: [180, 68] },
  { id: "4b", n: 4, set: "ab", common: true, dup: true, apart: [260, 104], joined: [180, 104] },
  { id: "5", n: 5, set: "b", apart: [320, 68], joined: [248, 68] },
  { id: "6", n: 6, set: "b", apart: [320, 104], joined: [248, 104] },
];

const MODES = [
  {
    key: "union",
    label: "A ∪ B",
    name: "Объединение",
    note: "всё, что есть хотя бы в одном множестве",
    hit: () => true,
  },
  {
    key: "inter",
    label: "A ∩ B",
    name: "Пересечение",
    note: "только то, что есть в обоих",
    hit: (d) => d.set === "ab",
  },
  {
    key: "diff",
    label: "A \\ B",
    name: "Разность",
    note: "из A без того, что есть в B",
    hit: (d) => d.set === "a",
  },
];

const HOLD_APART_MS = 2800;
const MOVE_MS = 1000;
const MERGE_MS = 1700;
const STEP_MS = 3200;

export default function VennOps({ cues }) {
  const audioT = useSlideAudioTime();
  const shown = useReveal();
  const reduce =
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // stage: apart → moving → merged; потом mode 0..2
  const [stage, setStage] = useState(reduce ? "merged" : "apart");
  const [mode, setMode] = useState(reduce ? 0 : -1);
  const [auto, setAuto] = useState(!reduce);

  // Ручной выбор перекрывает озвучку до следующего запуска звука.
  const [manual, setManual] = useState(false);
  const hadAudio = useRef(false);
  useEffect(() => {
    const has = audioT != null;
    if (has && !hadAudio.current) setManual(false);
    hadAudio.current = has;
  }, [audioT]);
  const synced = !!cues && audioT != null && !manual;

  useEffect(() => {
    if (!auto || synced) return;
    let t;
    if (stage === "apart") {
      t = setTimeout(() => setStage("moving"), HOLD_APART_MS);
    } else if (st === "moving") {
      t = setTimeout(() => setStage("merged"), MOVE_MS);
    } else if (mode === -1) {
      t = setTimeout(() => setMode(0), MERGE_MS);
    } else {
      t = setTimeout(() => setMode((m) => (m + 1) % MODES.length), STEP_MS);
    }
    return () => clearTimeout(t);
  }, [auto, synced, stage, mode]);

  let st = stage;
  let md = mode;
  if (synced) {
    st =
      audioT < cues.move ? "apart" : audioT < cues.merge ? "moving" : "merged";
    md = audioT >= cues.diff ? 2 : audioT >= cues.inter ? 1 : audioT >= cues.union ? 0 : -1;
  }
  const joined = st !== "apart";
  const merged = st === "merged";
  const cur = merged && md >= 0 ? MODES[md] : null;
  const result = cur
    ? DOTS.filter((d) => !d.dup && cur.hit(d)).map((d) => d.n)
    : [];

  const pick = (i) => {
    setManual(true);
    setAuto(false);
    setStage("merged");
    setMode(i);
  };

  let caption;
  if (cur) {
    caption = (
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
    );
  } else if (st === "apart") {
    caption = (
      <span className="a-result-note">
        A = {"{1, 2, 3, 4}"} и B = {"{3, 4, 5, 6}"}: общие элементы 3 и 4
        есть и там, и там
      </span>
    );
  } else if (stage === "moving") {
    caption = (
      <span className="a-result-note">Множества сближаются…</span>
    );
  } else {
    caption = (
      <span className="a-result-note">
        Общие элементы слились: в множестве каждое значение — один раз
      </span>
    );
  }

  return (
    <div className={`a-stage ${shown ? "in" : ""}`}>
      <div className="a-chips" role="tablist">
        {MODES.map((m, i) => (
          <button
            key={m.key}
            className={`a-chip ${cur && i === md ? "on" : ""}`}
            onClick={() => pick(i)}
          >
            <span className="a-chip-big">{m.label}</span>
            <span className="a-chip-name">{m.name}</span>
          </button>
        ))}
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

        <g className={merged ? "a-fills on" : "a-fills"}>
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

        <text x="92" y="30" className={`a-set-label a-label-a ${joined ? "joined" : ""}`}>
          A
        </text>
        <text x="268" y="30" className={`a-set-label a-label-b ${joined ? "joined" : ""}`}>
          B
        </text>

        {DOTS.map((d) => {
          const [x, y] = joined ? d.joined : d.apart;
          const gone = d.dup && merged;
          const hit = cur ? cur.hit(d) : true;
          const cls = [
            "a-dot",
            gone ? "gone" : hit ? "hit" : "dim",
            d.common && !merged ? "common" : "",
            d.common && merged && !d.dup ? "pulse" : "",
          ].join(" ");
          return (
            <g key={d.id} className={cls} style={{ transform: `translate(${x}px, ${y}px)` }}>
              <circle r="11" />
              <text y="4" textAnchor="middle">
                {d.n}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="a-result" key={cur ? cur.key : st}>
        {caption}
      </div>
    </div>
  );
}
