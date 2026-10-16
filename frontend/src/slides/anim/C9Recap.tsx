import { Pill, Steps, useSteps } from "./kit.tsx";

/* Глава 9, слайд 13: итог главы. */

const LABELS = ["Итог", "Глубина и ширина", "Компоненты", "Деревья", "Остов · мосты", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Глубина идёт до упора со стеком и пишется рекурсией; ширина расходится волной с очередью и даёт кратчайшие пути",
  "Множество посещённых защищает от циклов, повторные запуски вычерпывают компоненты связности",
  "Дерево — связный граф без циклов, n − 1 ребро: файловая система, AST, DOM",
  "Остовные деревья — скелет сети; кёнигсбергские мосты научили отличать проходимые графы по нечётным степеням",
  "Дальше — вероятность: как теорема Байеса правит спам-фильтрами",
];
const CARDS = [
  ["DFS · BFS", "обходы", 1],
  ["visited", "компоненты", 2],
  ["n − 1", "деревья", 3],
  ["MST · Эйлер", "остов, мосты", 4],
] as const;

export default function C9Recap({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.5, 10.2, 16.2, 23.7, 31.2], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g key={name} className="a-t" style={{ transform: `translate(${50 + i * 86}px, 62px) scale(${on ? 1.1 : 1})` }}>
            <rect x="-38" y="-40" width="76" height="80" rx="10" style={{ fill: on || done ? "var(--s-green)" : "var(--s-panel2)", stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)", strokeWidth: on ? 2 : 1.4 }} />
            <text y="4" textAnchor="middle" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-accent)" }}>{big}</text>
            <text y="26" textAnchor="middle" className="a-cap" style={{ fontSize: 8.5 }}>{name}</text>
          </g>
        );
      })}
      <Pill x={180} y={140} w={280} h={26} text="Глава 10 · вероятность и Байес →" o={step >= 5 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
