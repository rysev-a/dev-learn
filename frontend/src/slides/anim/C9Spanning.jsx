import { GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 9, слайд 10: остовное дерево — скелет сети; минимальное остовное
   дерево по весам. */

const LABELS = ["Остов", "n − 1 ребро", "Минимальный", "Применения", "Суть"];
const CAPTION = [
  "Из дерева вырастает практическая задача: остовное дерево",
  "Связный граф: оставим n − 1 ребро так, чтобы связность сохранилась, — скелет сети без лишних рёбер и циклов",
  "Если у рёбер есть цены — минимальное остовное дерево: самый дешёвый способ связать всех",
  "Прокладка кабелей между серверами, объединение офисов, кластеризация точек на карте",
  "Суть: выжать из графа дерево",
];
const N = [
  { x: 50, y: 46, l: "A" },
  { x: 160, y: 30, l: "B" },
  { x: 90, y: 116, l: "C" },
  { x: 290, y: 40, l: "D" },
  { x: 200, y: 118, l: "E" },
  { x: 316, y: 112, l: "F" },
];
const E0 = [
  { a: 0, b: 1, w: 4 },
  { a: 0, b: 2, w: 2 },
  { a: 1, b: 2, w: 5 },
  { a: 1, b: 3, w: 10 },
  { a: 2, b: 4, w: 3 },
  { a: 3, b: 4, w: 7 },
  { a: 3, b: 5, w: 6 },
  { a: 4, b: 5, w: 8 },
];
const MST = new Set([1, 4, 0, 6, 5]); // индексы рёбер: AC, CE, AB, DF, DE
const SPAN = new Set([0, 1, 4, 5, 7]);

export default function C9Spanning({ cues }) {
  const ctl = useSteps(cues || [3.9, 14.2, 20.2, 26.1], 3000);
  const { step } = ctl;
  const edges = E0.map((e) => (step >= 2 ? e : { ...e, w: undefined }));
  const ec = (e, i) => {
    if (step === 1) return SPAN.has(i) ? "g" : "m";
    if (step >= 2) return MST.has(i) ? "g" : "m";
    return "m";
  };
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={edges} ec={ec} nc={() => (step >= 1 ? "g" : "m")} />
      <Txt x="180" y="152" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">6 вершин ⇒ оставили 5 рёбер</Txt>
      <Txt x="180" y="152" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-accent)">2 + 3 + 4 + 6 + 7 = 22 — минимум</Txt>
      <Txt x="180" y="152" mono size={11} o={step === 3 ? 1 : 0}>кабели · офисы · кластеры</Txt>
      <Txt x="180" y="152" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-amber)">граф → дерево</Txt>
    </Steps>
  );
}
