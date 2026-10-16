import { GraphView, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 8, слайд 2: граф — вершины и рёбра; форма рисунка не важна;
   друзья и метро. */

const LABELS = ["Определение", "V и E", "Без координат", "Друзья", "Метро"];
const CAPTION = [
  "Определение приятно удивит простотой",
  "Граф — множество вершин и множество рёбер, где каждое ребро соединяет пару вершин",
  "Ни координат, ни масштаба, ни красивых линий — только объекты и связи",
  "Карта друзей: вершины — люди, рёбра — дружба",
  "Схема метро: вершины — станции, рёбра — перегоны; дуга или ломаная — неважно",
];
const L1 = [
  [90, 46],
  [190, 28],
  [280, 70],
  [200, 118],
  [96, 110],
];
const L2 = [
  [60, 100],
  [130, 40],
  [220, 120],
  [300, 44],
  [180, 82],
];
const LAB = {
  0: ["A", "B", "C", "D", "E"],
  3: ["Аня", "Боря", "Вера", "Глеб", "Даша"],
  4: ["Парк", "Центр", "Мост", "Арбат", "Вокзал"],
};
const EDGES = [
  { a: 0, b: 1 },
  { a: 1, b: 2 },
  { a: 2, b: 3 },
  { a: 3, b: 4 },
  { a: 4, b: 0 },
  { a: 1, b: 3 },
];

export default function C8Definition({ cues }) {
  const ctl = useSteps(cues || [3.6, 8.5, 13.3, 16.4], 3000);
  const { step } = ctl;
  const alt = step === 2 || step === 4;
  const labs = LAB[step === 3 ? 3 : step === 4 ? 4 : 0];
  const L = alt ? L2 : L1;
  const nodes = L.map(([x, y], i) => ({ x, y, l: labs[i] }));
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={nodes} edges={EDGES} r={step >= 3 ? 20 : 13} lsize={step >= 3 ? 8.5 : 10.5} o={step === 0 ? 0.25 : 1} />
      <Txt x="180" y="156" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">V = {"{A,B,C,D,E}"}   E = {"{AB, BC, CD, DE, EA, BD}"}</Txt>
      <Txt x="180" y="156" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-amber)">тот же граф — другой рисунок</Txt>
      <Txt x="180" y="14" mono size={14} o={step === 0 ? 1 : 0} color="var(--s-accent)">граф = вершины + рёбра</Txt>
    </Steps>
  );
}
