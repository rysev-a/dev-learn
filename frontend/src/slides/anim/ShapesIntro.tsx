import { useEffect, useState } from "react";
import { REVEAL_MS, Steps, useSteps } from "./kit.tsx";

/* Слайд 1 главы «Множества»: пять кружков и пять квадратов появляются,
   их обводят пунктиром (две группы), затем фигуры получают цвета и
   перегруппировываются: три множества по цвету. */

const B = "var(--s-blue)";
const R = "var(--s-red)";
const Gr = "var(--s-accent)";

// kind: c — кружок, s — квадрат; col — цвет; a — место в «двух группах»;
// g — место в «трёх группах».
const ITEMS = [
  { k: "c", col: B, a: [55, 62], g: [40, 70] },
  { k: "c", col: R, a: [95, 62], g: [160, 70] },
  { k: "c", col: Gr, a: [135, 62], g: [280, 70] },
  { k: "c", col: B, a: [75, 108], g: [80, 70] },
  { k: "c", col: R, a: [115, 108], g: [200, 70] },
  { k: "s", col: Gr, a: [225, 62], g: [320, 70] },
  { k: "s", col: B, a: [265, 62], g: [40, 112] },
  { k: "s", col: R, a: [305, 62], g: [180, 112] },
  { k: "s", col: Gr, a: [245, 108], g: [300, 112] },
  { k: "s", col: B, a: [285, 108], g: [80, 112] },
];

const HULLS_A = [
  { x: 30, y: 38, w: 130, h: 96 },
  { x: 200, y: 38, w: 130, h: 96 },
];
const HULLS_G = [
  { x: 18, y: 44, w: 84, h: 92, t: "синие", c: B },
  { x: 138, y: 44, w: 84, h: 92, t: "красные", c: R },
  { x: 258, y: 44, w: 84, h: 92, t: "зелёные", c: Gr },
];

const LABELS = ["Фигуры", "Две группы", "Цвета", "Три группы"];
const CAPTION = [
  "Появляются элементы: пять кружков и пять квадратов",
  "Каждую группу можно обвести — получились два множества",
  "Теперь у фигур есть цвета: синий, красный, зелёный",
  "Обведём по цвету — те же фигуры, но уже три других множества",
];

export default function ShapesIntro({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.9, 14.3, 19.2], 2800);
  const { step } = ctl;
  const [shown, setShown] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setShown(true), REVEAL_MS);
    return () => clearTimeout(t);
  }, []);

  const colored = step >= 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {HULLS_A.map((h, i) => (
        <rect
          key={`a${i}`}
          className="a-hull a-t"
          x={h.x}
          y={h.y}
          width={h.w}
          height={h.h}
          rx="14"
          style={{ opacity: step === 1 ? 1 : 0 }}
        />
      ))}
      {HULLS_G.map((h, i) => (
        <g key={`g${i}`} className="a-t" style={{ opacity: step >= 3 ? 1 : 0 }}>
          <rect
            className="a-hull"
            x={h.x}
            y={h.y}
            width={h.w}
            height={h.h}
            rx="14"
            style={{ stroke: h.c }}
          />
          <text x={h.x + h.w / 2} y="152" textAnchor="middle" className="a-cap">
            {h.t}
          </text>
        </g>
      ))}
      <g className="a-t" style={{ opacity: step === 1 ? 1 : 0 }}>
        <text x="95" y="152" textAnchor="middle" className="a-cap">
          кружки
        </text>
        <text x="265" y="152" textAnchor="middle" className="a-cap">
          квадраты
        </text>
      </g>

      {ITEMS.map((it, i) => {
        const [x, y] = step >= 3 ? it.g : it.a;
        return (
          <g
            key={i}
            className="a-t"
            style={{
              transform: `translate(${x}px, ${y}px) scale(${shown ? 1 : 0.2})`,
              opacity: shown ? 1 : 0,
              transitionDelay: shown && step === 0 ? `${i * 90}ms` : "0ms",
            }}
          >
            {it.k === "c" ? (
              <circle r="12" style={shape(it.col, colored)} />
            ) : (
              <rect x="-12" y="-12" width="24" height="24" rx="3" style={shape(it.col, colored)} />
            )}
          </g>
        );
      })}
    </Steps>
  );
}

function shape(col: string, colored: boolean) {
  return colored
    ? { stroke: col, fill: col, fillOpacity: 0.3, strokeWidth: 2 }
    : { stroke: "var(--s-muted)", fill: "var(--s-panel2)", fillOpacity: 1, strokeWidth: 2 };
}
