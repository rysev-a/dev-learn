import { Pill, Steps, useSteps } from "./kit.jsx";

/* Глава 8, слайд 13: итог главы. */

const LABELS = ["Итог", "Граф", "Степени", "Достижимость", "Память", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Граф — вершины и рёбра: самая экономная модель всего, где важны связи",
  "Рёбра бывают направленными и нет; сумма степеней всегда равна удвоенному числу рёбер",
  "Путь, цикл и связность описывают достижимость; цикл в зависимостях — нет правильного порядка",
  "Хранить граф проще списками смежности для разреженного мира и матрицей для плотного",
  "Дальше — научимся ходить по графам: глубина, ширина, деревья и кёнигсбергские мосты",
];
const CARDS = [
  ["V, E", "граф", 1],
  ["Σ = 2|E|", "степени", 2],
  ["путь · цикл", "достижимость", 3],
  ["adj", "память", 4],
];

export default function C8Recap({ cues }) {
  const ctl = useSteps(cues || [1.4, 8.6, 15.4, 22.7, 27.5], 2600);
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
      <Pill x={180} y={140} w={280} h={26} text="Глава 9 · обходы графов и деревья →" o={step >= 5 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
