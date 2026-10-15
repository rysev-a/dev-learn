import { G, GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 4: степень вершины; лемма о рукопожатиях: Σ deg = 2|E|;
   число вершин нечётной степени чётно. */

const LABELS = ["Степень", "Популярный", "Лемма", "Дважды", "Нечётные"];
const CAPTION = [
  "У каждой вершины есть степень: число рёбер, которые в неё входят",
  "У популярного в графе дружбы степень велика, у затворника — один или ноль",
  "Лемма о рукопожатиях: сумма степеней всех вершин равна удвоенному числу рёбер",
  "Причина: каждое ребро касается двух вершин, и суммируя степени, мы считаем его дважды",
  "Следствие: число вершин нечётной степени в любом графе чётно",
];
const N = [
  { x: 150, y: 74, l: "A" },
  { x: 70, y: 40, l: "B" },
  { x: 70, y: 112, l: "C" },
  { x: 230, y: 40, l: "D" },
  { x: 230, y: 112, l: "E" },
  { x: 300, y: 40, l: "F" },
  { x: 300, y: 112, l: "G" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 0, b: 3 },
  { a: 0, b: 4 },
  { a: 1, b: 2 },
  { a: 3, b: 5 },
];
const DEG = N.map((_, i) => E.filter((e) => e.a === i || e.b === i).length);

export default function C8Degree({ cues }) {
  const ctl = useSteps(cues || [4.2, 9.2, 15.7, 26.9], 3000);
  const { step } = ctl;
  const nc = (i) => {
    if (step === 1) return i === 0 ? "g" : i === 6 ? "r" : "m";
    if (step === 4) return DEG[i] % 2 ? "y" : "m";
    return "m";
  };
  const ec = (e) => (step === 3 ? "g" : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} nc={nc} ec={ec} />
      {N.map((n, i) => (
        <Txt key={i} x={n.x + 18} y={n.y - 12} mono size={10} o={step >= 1 ? 1 : 0} color="var(--s-amber)">{DEG[i]}</Txt>
      ))}
      <G o={step >= 2 && step <= 3 ? 1 : 0}>
        <Txt x="180" y="152" mono size={12} color="var(--s-accent)">Σdeg = 4+2+2+2+1+1+0 = 12 = 2 · 6</Txt>
      </G>
      <Txt x="180" y="152" mono size={12} o={step >= 4 ? 1 : 0} color="var(--s-amber)">нечётных вершин: 2 (E и F) — чётное число</Txt>
      <Txt x="180" y="14" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">A — популярный (4), G — затворник (0)</Txt>
      <Txt x="180" y="14" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">каждое ребро вносит +1 двум вершинам</Txt>
    </Steps>
  );
}
