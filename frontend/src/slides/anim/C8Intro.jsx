import { GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 1: графы вокруг нас — дерево DOM, зависимости,
   соцсеть; дальше строгий язык. */

const LABELS = ["Глава", "DOM", "Зависимости", "Соцсеть", "Язык", "Дальше"];
const CAPTION = [
  "Графы: основы",
  "Дерево элементов в инструментах разработчика — граф",
  "Зависимости проекта — тоже граф, как ни странно звучит слово «дерево»",
  "Друзья, подписки, рекомендации в соцсети — снова графы",
  "Сегодня говорим о них строго: вершины и рёбра, память, сумма степеней",
  "Это фундамент для двух следующих глав — там мы научимся ходить по графам",
];
const TREE = {
  nodes: [
    { x: 180, y: 28, l: "html" },
    { x: 110, y: 78, l: "head" },
    { x: 250, y: 78, l: "body" },
    { x: 215, y: 128, l: "div" },
    { x: 285, y: 128, l: "p" },
  ],
  edges: [
    { a: 0, b: 1 },
    { a: 0, b: 2 },
    { a: 2, b: 3 },
    { a: 2, b: 4 },
  ],
};
const DEPS = {
  nodes: [
    { x: 70, y: 80, l: "app" },
    { x: 170, y: 40, l: "ui" },
    { x: 170, y: 120, l: "net" },
    { x: 280, y: 80, l: "core" },
  ],
  edges: [
    { a: 0, b: 1 },
    { a: 0, b: 2 },
    { a: 1, b: 3 },
    { a: 2, b: 3 },
  ],
};
const SOC = {
  nodes: [
    { x: 80, y: 50, l: "А" },
    { x: 180, y: 28, l: "Б" },
    { x: 270, y: 60, l: "В" },
    { x: 220, y: 118, l: "Г" },
    { x: 110, y: 112, l: "Д" },
  ],
  edges: [
    { a: 0, b: 1 },
    { a: 1, b: 2 },
    { a: 2, b: 3 },
    { a: 3, b: 4 },
    { a: 4, b: 0 },
    { a: 1, b: 3 },
  ],
};

export default function C8Intro({ cues }) {
  const ctl = useSteps(cues || [3.0, 7.4, 13.3, 17.8, 26.2], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView {...TREE} o={step === 1 ? 1 : 0} />
      <GraphView {...DEPS} directed o={step === 2 ? 1 : 0} />
      <GraphView {...SOC} o={step === 3 ? 1 : 0} />
      <Txt x="180" y="70" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">G = (V, E)</Txt>
      <Txt x="180" y="70" mono size={16} o={step === 4 ? 1 : 0} color="var(--s-accent)">вершины · рёбра · память · степени</Txt>
      <Txt x="180" y="70" mono size={16} o={step >= 5 ? 1 : 0} color="var(--s-accent)">обходы: глубина · ширина</Txt>
    </Steps>
  );
}
