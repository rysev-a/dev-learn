import { G, GraphView, Pill, Steps, Txt, useSteps, type GraphEdge } from "./kit.tsx";

/* Глава 9, слайд 2: постановка задачи обхода — посетить достижимое один
   раз, цикл-ловушка, множество посещённых. */

const LABELS = ["Задача", "Достижимое", "Ловушка", "Два органа", "Посещённые"];
const CAPTION = [
  "Сформулируем задачу честно",
  "Дан граф и стартовая вершина: посетить всё достижимое — каждую вершину ровно один раз",
  "Подвох в циклах: без памяти обход вечно кружит по одному кольцу",
  "Любой обход имеет два органа: способ выбирать следующую вершину и множество посещённых",
  "Выбор рождает разные алгоритмы, а множество посещённых обязательно в любом из них",
];
const N = [
  { x: 70, y: 76, l: "S" },
  { x: 150, y: 36, l: "" },
  { x: 150, y: 116, l: "" },
  { x: 240, y: 76, l: "" },
  { x: 320, y: 40, l: "" },
  { x: 320, y: 120, l: "×" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 3 },
  { a: 2, b: 3 },
  { a: 3, b: 4 },
];

export default function C9Task({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.9, 8.6, 15.1, 23.1], 3000);
  const { step } = ctl;
  const nc = (i: number) => (step === 1 ? (i === 5 ? "m" : "g") : step === 2 && [0, 1, 3, 2].includes(i) ? "r" : "m");
  const ec = (e: GraphEdge) => (step === 2 ? ([0, 1].includes(e.a) || e.a === 1 ? "r" : "m") : step === 1 ? "g" : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} nc={nc} ec={ec} o={step === 3 || step === 4 ? 0 : 1} />
      <Txt x={180} y={152} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">×  — недостижима: её обход не касается</Txt>
      <Txt x={180} y={152} mono size={11} o={step === 2 ? 1 : 0} color="var(--s-red)">S → … → S → … без конца</Txt>
      <Txt x={180} y={14} mono size={12} o={step === 0 ? 1 : 0} color="var(--s-accent)">граф + старт ⇒ всё достижимое, по разу</Txt>
      <G o={step >= 3 ? 1 : 0}>
        <Pill x={100} y={64} w={150} h={60} text="кого брать дальше?" stroke="var(--s-blue)" size={11} />
        <Pill x={260} y={64} w={150} h={60} text="visited = {…}" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
        <Txt x={260} y={112} size={9.5} o={step >= 4 ? 1 : 0} color="var(--s-accent)">обязательно в любом обходе</Txt>
        <Txt x={100} y={112} size={9.5} o={step >= 4 ? 1 : 0} color="var(--s-blue)">выбор — разный</Txt>
      </G>
    </Steps>
  );
}
