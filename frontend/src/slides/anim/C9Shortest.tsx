import { G, GraphView, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 6: BFS даёт кратчайшие пути в графе без весов — волна,
   «друзья друзей», лабиринт. */

const LABELS = ["Кратчайшие", "Расстояния", "Друзья друзей", "Лабиринт"];
const CAPTION = [
  "Замена стека на очередь дарит ценное свойство: обход в ширину находит кратчайшие пути в графе без весов",
  "Волна достигает каждой вершины по минимальному числу рёбер: сначала расстояние 1, потом 2",
  "Логика «друзей друзей»: соцсети предлагают людей ровно на расстоянии 2–3 рукопожатий",
  "В лабиринте ширина выведет по самому короткому маршруту, а глубина — по первому попавшемуся коридору",
];
const N = [
  { x: 60, y: 80, l: "0" },
  { x: 130, y: 40, l: "1" },
  { x: 130, y: 120, l: "1" },
  { x: 210, y: 40, l: "2" },
  { x: 210, y: 120, l: "2" },
  { x: 290, y: 80, l: "3" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 3 },
  { a: 2, b: 4 },
  { a: 3, b: 5 },
  { a: 4, b: 5 },
];

export default function C9Shortest({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [6.6, 14.1, 20.2], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">BFS ⇒ кратчайший путь</Txt>
      <GraphView nodes={N} edges={E} nc={() => "g"} ec={(e) => (e.a === 3 || e.a === 4 ? "m" : "g")} o={step === 1 ? 1 : 0} />
      <Txt x={180} y={152} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">цифра в вершине — минимум рёбер от старта</Txt>
      <G o={step === 2 ? 1 : 0}>
        {([
          [1, 54, "ты", "var(--s-accent)"],
          [1, 112, "друг", "var(--s-blue)"],
          [2, 184, "друг друга", "var(--s-amber)"],
          [3, 262, "кто знает?", "var(--s-red)"],
        ] as const).map(([r, x, t, c], i) => (
          <g key={i}>
            <circle cx={x} cy="80" r="18" style={{ fill: "var(--s-panel2)", stroke: c, strokeWidth: 1.8 }} />
            <text x={x} y="84" textAnchor="middle" className="a-mono" style={{ fontSize: 8 }}>{t.slice(0, 5)}</text>
            <Txt x={x} y={112} size={8.5}>{`расст. ${i}`}</Txt>
          </g>
        ))}
        <Txt x={180} y={152} size={10}>рекомендуют людей на расстоянии 2–3</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <rect x="40" y="26" width="280" height="100" rx="8" style={{ fill: "none", stroke: "var(--s-border)", strokeWidth: 1.6 }} />
        <path d="M60 106 L150 106 L150 76 L230 76 L230 46 L300 46" style={{ fill: "none", stroke: "var(--s-accent)", strokeWidth: 3, strokeLinecap: "round" }} />
        <path className="a-t" d="M60 106 L60 46 L110 46 L110 66 L180 66 L180 100 L260 100 L260 76 L300 76 L300 46" style={{ fill: "none", stroke: "var(--s-red)", strokeWidth: 2.4, strokeDasharray: "3 4", strokeLinecap: "round", opacity: step >= 3 ? 1 : 0 }} />
        <Pill x={60} y={106} w={30} h={18} text="вх" stroke="var(--s-accent)" size={9} />
        <Pill x={300} y={46} w={34} h={18} text="вых" stroke="var(--s-accent)" size={9} />
        <Txt x={120} y={146} mono size={10} color="var(--s-accent)">ширина: кратчайший</Txt>
        <Txt x={260} y={146} mono size={10} color="var(--s-red)">глубина: длинный</Txt>
      </G>
    </Steps>
  );
}
