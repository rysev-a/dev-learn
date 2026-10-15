import { GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 12: циклы в зависимостях — беда; без циклов есть
   топологический порядок. */

const LABELS = ["Циклы", "a → b → c → a", "Порядок", "Дальше"];
const CAPTION = [
  "Отдельно — циклы в ориентированных графах: в зависимостях они синоним беды",
  "Если a требует b, b требует c, а c требует a, ни один нельзя установить первым: порядка не существует",
  "Граф без циклов позволяет выстроить вершины так, что каждая стрелка ведёт от раннего к позднему — топологический порядок",
  "Проверка на циклы и построение порядка — задачи, до которых мы дойдём через главу",
];
const CYC = {
  nodes: [
    { x: 90, y: 100, l: "a" },
    { x: 180, y: 36, l: "b" },
    { x: 270, y: 100, l: "c" },
  ],
  edges: [
    { a: 0, b: 1 },
    { a: 1, b: 2 },
    { a: 2, b: 0 },
  ],
};
const DAG = [
  [60, 100],
  [140, 100],
  [220, 100],
  [300, 100],
];
const DAG_UP = [
  [60, 40],
  [140, 110],
  [220, 40],
  [300, 110],
];

export default function C8Cycles({ cues }) {
  const ctl = useSteps(cues || [6.0, 14.3, 26.0], 3000);
  const { step } = ctl;
  const line = step >= 2;
  const pos = line ? DAG : DAG_UP;
  const nodes = pos.map(([x, y], i) => ({ x, y, l: ["a", "b", "c", "d"][i] }));
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-red)">a ⇄ b ⇄ c ⇄ a ?</Txt>
      <GraphView {...CYC} directed ec={() => "r"} nc={() => "r"} o={step === 1 ? 1 : 0} />
      <Txt x="180" y="150" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-red)">с кого начать? — правильного порядка нет</Txt>
      <GraphView
        nodes={nodes}
        edges={[
          { a: 0, b: 1 },
          { a: 1, b: 2 },
          { a: 2, b: 3 },
          { a: 0, b: 2 },
        ]}
        directed
        ec={() => "g"}
        nc={() => "g"}
        o={step >= 2 ? 1 : 0}
      />
      <Txt x="180" y="150" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-accent)">каждая стрелка — слева направо</Txt>
      <Txt x="180" y="150" mono size={11} o={step >= 3 ? 1 : 0} color="var(--s-amber)">проверка на циклы · топологический порядок</Txt>
    </Steps>
  );
}
