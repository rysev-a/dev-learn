import { GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 9, слайд 8: дерево — связный граф без циклов, n вершин и n−1 ребро;
   добавили ребро — цикл, убрали — распад. */

const LABELS = ["Деревья", "Один путь", "n − 1", "Примеры", "В обе стороны"];
const CAPTION = [
  "Отдельная честь на этом поле у деревьев",
  "Дерево — связный граф без циклов: между любыми вершинами ровно один путь, заблудиться невозможно",
  "Формула: у дерева n вершин и ровно n − 1 рёбер",
  "Проверьте: одна вершина — ноль рёбер, три вершины цепочкой — два ребра",
  "Работает в обе стороны: в связном графе n − 1 рёбер — значит, дерево; добавите ребро — цикл, уберёте — распад",
];
const N = [
  { x: 180, y: 26, l: "A" },
  { x: 100, y: 70, l: "B" },
  { x: 260, y: 70, l: "C" },
  { x: 60, y: 118, l: "D" },
  { x: 140, y: 118, l: "E" },
  { x: 260, y: 118, l: "F" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 3 },
  { a: 1, b: 4 },
  { a: 2, b: 5 },
];
const PATH = [
  [3, 1],
  [1, 0],
  [0, 2],
  [2, 5],
];

export default function C9Tree({ cues }) {
  const ctl = useSteps(cues || [2.6, 9.2, 14.4, 19.5], 3000);
  const { step } = ctl;
  const showTree = step !== 3;
  const pathEdge = (e) => PATH.some(([a, b]) => (a === e.a && b === e.b) || (a === e.b && b === e.a));
  const edges = step >= 4 ? [...E, { a: 3, b: 4, extra: true }] : E;
  const ec = (e) => (e.extra ? "r" : step === 1 && pathEdge(e) ? "g" : "m");
  const nc = (i) => (step === 1 ? ([3, 1, 0, 2, 5].includes(i) ? "g" : "m") : step >= 4 && [1, 3, 4].includes(i) ? "r" : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={edges} nc={nc} ec={ec} o={showTree ? 1 : 0} />
      <Txt x="180" y="152" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">D → B → A → C → F — единственный путь</Txt>
      <Txt x="180" y="152" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-amber)">6 вершин ⇒ 5 рёбер</Txt>
      <Txt x="180" y="152" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-red)">+ ребро D–E → цикл B–D–E; без ребра — распад</Txt>
      <Txt x="180" y="70" mono size={13} o={step === 3 ? 1 : 0}>1 вершина — 0 рёбер</Txt>
      <Txt x="180" y="96" mono size={13} o={step === 3 ? 1 : 0}>цепочка из 3 — 2 ребра</Txt>
      <Txt x="180" y="126" mono size={13} o={step === 3 ? 1 : 0} color="var(--s-accent)">n вершин — n − 1 ребро</Txt>
    </Steps>
  );
}
