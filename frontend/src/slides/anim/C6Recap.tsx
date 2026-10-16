import { Pill, Steps, useSteps } from "./kit.tsx";

/* Глава 6, слайд 13: итог главы. */

const LABELS = ["Итог", "Предикат", "Кванторы", "Порядок", "Тесты", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Предикат — высказывание с переменной: заготовка, которая становится истиной или ложью при подстановке",
  "Кванторы «для каждого» и «найдётся» делают из заготовок утверждения; отрицание меняет квантор на противоположный",
  "Порядок кванторов — часть смысла: перепутанный порядок меняет контракт",
  "Тесты — кванторы на практике: юнит — «найдётся», property-based — «для всех»; один контрпример сильнее тысячи зелёных прогонов",
  "Дальше — математическая индукция: честно доказывать «для всех» на бесконечных множествах",
];
const CARDS = [
  ["P(x)", "предикат", 1],
  ["∀  ∃", "кванторы", 2],
  ["∀∃≠∃∀", "порядок", 3],
  ["тесты", "∃ и ∀", 4],
] as const;

export default function C6Recap({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.5, 8.0, 16.3, 21.0, 29.5], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g key={name} className="a-t" style={{ transform: `translate(${50 + i * 86}px, 62px) scale(${on ? 1.1 : 1})` }}>
            <rect x="-36" y="-40" width="72" height="80" rx="10" style={{ fill: on || done ? "var(--s-green)" : "var(--s-panel2)", stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)", strokeWidth: on ? 2 : 1.4 }} />
            <text y="4" textAnchor="middle" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>{big}</text>
            <text y="26" textAnchor="middle" className="a-cap">{name}</text>
          </g>
        );
      })}
      <Pill x={180} y={140} w={280} h={26} text="Глава 7 · индукция и рекуррентности →" o={step >= 5 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
