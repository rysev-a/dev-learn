import { G, GraphView, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 8, слайд 7: три примера — DOM, зависимости с ошибкой-циклом,
   карта маршрутов с весами. */

const LABELS = ["Примеры", "DOM", "Зависимости", "Маршруты", "Веса"];
const CAPTION = [
  "Закрепим на трёх примерах, которые вы видите каждый день",
  "Дом-дерево браузера — ориентированный граф, почти дерево: у узла один родитель, детей сколько угодно",
  "Зависимости пакетов — ребро «нужен для работы»; цикл в нём менеджер покажет ошибкой",
  "Карта маршрутов — взвешенный граф: рёбра несут минуты или рубли, навигатор ищет минимальную сумму",
  "Веса не меняют устройство графа, но добавляют к «как добраться» вопрос «почём»",
];
const TREE = {
  nodes: [
    { x: 180, y: 26, l: "html" },
    { x: 110, y: 76, l: "head" },
    { x: 250, y: 76, l: "body" },
    { x: 200, y: 128, l: "div" },
    { x: 300, y: 128, l: "p" },
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
    { x: 70, y: 80, l: "a" },
    { x: 180, y: 40, l: "b" },
    { x: 290, y: 80, l: "c" },
    { x: 180, y: 126, l: "d" },
  ],
  edges: [
    { a: 0, b: 1 },
    { a: 1, b: 2 },
    { a: 2, b: 0, cyc: true },
    { a: 2, b: 3 },
  ],
};
const MAP = {
  nodes: [
    { x: 50, y: 80, l: "A" },
    { x: 140, y: 36, l: "B" },
    { x: 140, y: 124, l: "C" },
    { x: 240, y: 80, l: "D" },
    { x: 320, y: 80, l: "E" },
  ],
  edges: [
    { a: 0, b: 1, w: 7 },
    { a: 0, b: 2, w: 3 },
    { a: 1, b: 3, w: 4 },
    { a: 2, b: 3, w: 6 },
    { a: 3, b: 4, w: 2 },
  ],
};
const BEST = [
  [0, 2],
  [2, 3],
  [3, 4],
];

export default function C8Examples({ cues }) {
  const ctl = useSteps(cues || [3.4, 9.7, 18.2, 24.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={16} o={step === 0 ? 1 : 0} color="var(--s-accent)">дерево · зависимости · карта</Txt>
      <GraphView {...TREE} directed ec={() => "g"} o={step === 1 ? 1 : 0} />
      <GraphView {...DEPS} directed ec={(e) => (e.cyc ? "r" : "m")} nc={(i) => (i < 3 ? "r" : "m")} o={step === 2 ? 1 : 0} />
      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="154" mono size={11} color="var(--s-red)">a → b → c → a: цикл — ошибка менеджера</Txt>
      </G>
      <GraphView
        {...MAP}
        ec={(e) => (step >= 3 && BEST.some(([a, b]) => a === e.a && b === e.b) ? "g" : "m")}
        nc={(i) => (step >= 3 && [0, 2, 3, 4].includes(i) ? "g" : "m")}
        o={step >= 3 ? 1 : 0}
      />
      <Txt x="180" y="154" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">минимальная сумма: A → C → D → E</Txt>
      <Txt x="180" y="154" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-amber)">3 + 6 + 2 = 11 — «почём»</Txt>
    </Steps>
  );
}
