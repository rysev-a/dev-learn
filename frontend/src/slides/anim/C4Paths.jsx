import { G, Matrix, Pill, Steps, Txt, useSteps } from "./kit.tsx";
import { binom, triPos } from "./tri.ts";

/* Глава 4, слайд 3: строка n — это C(n, k); число маршрутов вниз по
   треугольнику; выбор шагов «влево»; сетка с препятствиями. */

const LABELS = ["Строка = C(n, k)", "Маршруты", "Шаги влево", "Сетка"];
const CAPTION = [
  "Строка с номером n — все сочетания C(n, k), выписанные по порядку",
  "Спускаясь от вершины, вы делаете n шагов влево или вправо: число в клетке считает маршруты до неё",
  "Маршрут — это выбор, в каких именно шагах свернуть влево: сочетание",
  "Сетка с препятствиями: число путей из угла в угол вправо и вниз — тот же C(n, k)",
];
const ROWS = 5;
const PATH = [
  [0, 0],
  [1, 1],
  [2, 1],
  [3, 2],
  [4, 2],
];
const ROUTES = ["ЛЛПП", "ЛПЛП", "ЛППЛ", "ПЛЛП", "ПЛПЛ", "ППЛЛ"];

export default function C4Paths({ cues }) {
  const ctl = useSteps(cues || [6.8, 17.6, 23.0], 3000);
  const { step } = ctl;
  const tri = step <= 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={tri ? 1 : 0}>
        {Array.from({ length: ROWS }, (_, r) =>
          Array.from({ length: r + 1 }, (_, c) => {
            const [x, y] = triPos(r, c, 40, 28, 130, 22);
            const onPath = step === 1 && PATH.some(([pr, pc]) => pr === r && pc === c);
            return (
              <g key={`${r}${c}`}>
                <circle cx={x} cy={y} r="12" className="a-t" style={{ fill: onPath ? "var(--s-green)" : "var(--s-panel2)", stroke: onPath ? "var(--s-accent)" : "var(--s-border)", strokeWidth: onPath ? 2 : 1.3 }} />
                <text x={x} y={y + 3.6} textAnchor="middle" className="a-mono" style={{ fontSize: 10 }}>{binom(r, c)}</text>
              </g>
            );
          }),
        )}
        <Txt x="300" y="40" mono size={11} o={step === 0 ? 1 : 0}>строка 4:</Txt>
        <Txt x="300" y="56" mono size={10} o={step === 0 ? 1 : 0}>C(4,0)…C(4,4)</Txt>
        <Txt x="300" y="46" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">6 маршрутов</Txt>
        <Txt x="300" y="62" size={9.5} o={step === 1 ? 1 : 0}>до центральной</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {ROUTES.map((r, i) => (
          <g key={r}>
            {r.split("").map((ch, j) => (
              <Pill key={j} x={44 + (i % 3) * 112 + j * 24} y={40 + Math.floor(i / 3) * 38} w={20} h={20} text={ch} stroke={ch === "Л" ? "var(--s-accent)" : "var(--s-border)"} fill={ch === "Л" ? "var(--s-green)" : "var(--s-panel2)"} size={10} />
            ))}
          </g>
        ))}
        <Txt x="180" y="130" mono size={13} color="var(--s-accent)">выбрать 2 из 4 шагов: C(4, 2) = 6</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        <Matrix
          x={96}
          y={26}
          rows={["1", "2", "3"]}
          cols={["1", "2", "3"]}
          cell={34}
          mark={(r, c) => (r === 1 && c === 1 ? "r" : r === 2 && c === 2 ? "g" : null)}
        />
        {[
          [1, 1, 1],
          [1, 0, 1],
          [1, 1, 2],
        ].map((row, r) =>
          row.map((v, c) => (
            <text key={`${r}${c}`} x={96 + c * 34 + 17} y={26 + r * 34 + 21} textAnchor="middle" className="a-mono" style={{ fontSize: 12, fill: "var(--s-text)" }}>
              {r === 1 && c === 1 ? "▨" : v}
            </text>
          )),
        )}
        <Txt x="282" y="60" anchor="middle" size={9.5}>▨ — препятствие</Txt>
        <Txt x="282" y="84" mono size={11} color="var(--s-accent)">путей: 2</Txt>
        <Txt x="180" y="152" size={9.5}>каждая клетка = сумма клетки слева и клетки сверху — как в треугольнике</Txt>
      </G>
    </Steps>
  );
}
