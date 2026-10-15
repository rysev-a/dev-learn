import { Steps, Txt, useSteps } from "./kit.jsx";
import { binom, triPos } from "./tri.js";

/* Глава 4, слайд 2: треугольник Паскаля строится одним правилом —
   сумма двух чисел над клеткой. */

const LABELS = ["Вершина", "Края", "Сумма", "Таблица"];
const CAPTION = [
  "Начнём с треугольника Паскаля: он строится без единой формулы — на вершине единица",
  "Вдоль обоих краёв тоже стоят единицы",
  "Каждое число внутри равно сумме двух чисел над ним: 1, 2, 1; 1, 3, 3, 1 …",
  "Ни умножения, ни деления — а в итоге таблица всей комбинаторики выбора",
];
const ROWS = 7;

export default function C4Pascal({ cues }) {
  const ctl = useSteps(cues || [4.4, 10.7, 16.8], 2800);
  const { step } = ctl;
  const cells = [];
  for (let r = 0; r < ROWS; r++)
    for (let c = 0; c <= r; c++) cells.push([r, c]);
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {cells.map(([r, c]) => {
        const [x, y] = triPos(r, c, 38, 20, 180, 18);
        const edge = c === 0 || c === r;
        const show = r === 0 || (step >= 1 && edge) || step >= 2;
        const inner = !edge;
        const delay = inner && step === 2 ? r * 280 : edge && step === 1 ? r * 160 : 0;
        const hl = step === 2 && r === 4 && c === 2;
        const src = step === 2 && r === 3 && (c === 1 || c === 2);
        return (
          <g
            key={`${r}-${c}`}
            className="a-t"
            style={{ opacity: show ? 1 : 0, transitionDelay: `${delay}ms` }}
          >
            <circle cx={x} cy={y} r="10" style={{ fill: hl ? "var(--s-green)" : src ? "var(--s-amber)" : "var(--s-panel2)", fillOpacity: src ? 0.35 : 1, stroke: hl ? "var(--s-accent)" : src ? "var(--s-amber)" : edge ? "var(--s-amber)" : "var(--s-border)", strokeWidth: hl || src ? 2 : 1.3 }} />
            <text x={x} y={y + 3.6} textAnchor="middle" className="a-mono" style={{ fontSize: 9.5 }}>{binom(r, c)}</text>
          </g>
        );
      })}
      <Txt x="300" y="100" anchor="start" mono size={10.5} o={step === 2 ? 1 : 0} color="var(--s-accent)">3 + 3 = 6</Txt>
      <Txt x="300" y="84" anchor="start" size={9.5} o={step === 2 ? 1 : 0}>сумма двух над ним</Txt>
    </Steps>
  );
}
