import { Pill, Steps, useSteps } from "./kit.tsx";

/* Глава 4, слайд 13: итог главы. */

const LABELS = ["Итог", "Паскаль", "Бином", "Включения · Дирихле", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Треугольник Паскаля — таблица сочетаний, построенная одним сложением; строки суммируются в 2ⁿ",
  "Бином Ньютона раскладывает степень суммы по строке Паскаля и даёт быстрые прикидки",
  "Включения и исключения чинят двойной счёт, а принцип Дирихле гарантирует коллизии",
  "Дальше — логика высказываний: формально разберём условия из оператора «если»",
];
const CARDS = [
  ["Δ", "Паскаль", 1],
  ["(a+b)ⁿ", "бином", 2],
  ["∪ −", "включения", 3],
  ["5 > 4", "Дирихле", 3],
] as const;

export default function C4Recap({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.4, 9.6, 14.7, 25.5], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g key={big} className="a-t" style={{ transform: `translate(${50 + i * 86}px, 62px) scale(${on ? 1.1 : 1})` }}>
            <rect x="-36" y="-40" width="72" height="80" rx="10" style={{ fill: on || done ? "var(--s-green)" : "var(--s-panel2)", stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)", strokeWidth: on ? 2 : 1.4 }} />
            <text y="4" textAnchor="middle" className="a-mono" style={{ fontSize: 15, fill: "var(--s-accent)" }}>{big}</text>
            <text y="26" textAnchor="middle" className="a-cap">{name}</text>
          </g>
        );
      })}
      <Pill x={180} y={140} w={260} h={26} text="Глава 5 · логика высказываний →" o={step >= 4 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
