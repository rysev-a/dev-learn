import { G, GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 11: исходящая и входящая степень в ориентированном графе. */

const LABELS = ["Направленные", "Исх. и вх.", "Сумма = |E|", "Популярная", "Поиск"];
const CAPTION = [
  "Ориентированные версии понятий",
  "Степень расщепляется на исходящую — сколько стрелок выходит — и входящую — сколько входит",
  "Сумма исходящих степеней равна числу рёбер, и сумма входящих тоже — стрелка выходит один раз и входит один раз",
  "У популярной страницы входящая степень огромна, исходящая может быть нулевой",
  "Подсчёт входящих стрелок когда-то породил целые поисковые системы",
];
const N = [
  { x: 60, y: 40, l: "A" },
  { x: 60, y: 120, l: "B" },
  { x: 160, y: 80, l: "C" },
  { x: 260, y: 40, l: "D" },
  { x: 260, y: 120, l: "E" },
];
const E = [
  { a: 0, b: 2 },
  { a: 1, b: 2 },
  { a: 2, b: 3 },
  { a: 4, b: 2 },
  { a: 3, b: 4 },
];
const OUT = N.map((_, i) => E.filter((e) => e.a === i).length);
const IN = N.map((_, i) => E.filter((e) => e.b === i).length);

export default function C8InOut({ cues }) {
  const ctl = useSteps(cues || [3.2, 9.0, 16.8, 25.2], 3000);
  const { step } = ctl;
  const nc = (i) => (step === 3 ? (i === 2 ? "g" : "m") : step === 1 && i === 2 ? "y" : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} directed nc={nc} ec={() => "m"} o={step === 0 ? 0.6 : 1} />
      {N.map((n, i) => (
        <g key={i}>
          <Txt x={n.x - 24} y={n.y - 16} mono size={9.5} o={step >= 1 ? 1 : 0} color="var(--s-accent)">{`вх ${IN[i]}`}</Txt>
          <Txt x={n.x + 26} y={n.y + 26} mono size={9.5} o={step >= 1 ? 1 : 0} color="var(--s-amber)">{`исх ${OUT[i]}`}</Txt>
        </g>
      ))}
      <G o={step === 2 ? 1 : 0}>
        <Txt x="330" y="78" mono size={10}>Σисх = 5</Txt>
        <Txt x="330" y="94" mono size={10}>Σвх = 5</Txt>
        <Txt x="330" y="110" mono size={10} color="var(--s-accent)">= |E|</Txt>
      </G>
      <Txt x="180" y="154" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">C: много входящих — «популярная»</Txt>
      <Txt x="180" y="154" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-accent)">чем больше ссылок на страницу — тем она важнее</Txt>
    </Steps>
  );
}
