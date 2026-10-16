import { Pill, Steps, useSteps } from "./kit.tsx";

/* Глава 3, слайд 13: итог. Правила, счётчики, где применять, что дальше. */

const LABELS = ["Итог", "Правила", "Счётчики", "Применение", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Два правила — сумма для взаимоисключающих групп и произведение для независимых выборов",
  "Счётчики: n! для перестановок, размещения с порядком, C(n, k) без порядка, C(n, 2) для пар",
  "Применяйте к паролям, пин-кодам, рукам в покере и рукопожатиям — оценивайте перебор до запуска",
  "Дальше — треугольник Паскаля, бином Ньютона и принцип Дирихле",
];
const CARDS = [
  ["+  ×", "правила", 1],
  ["n!", "перестановки", 2],
  ["A", "размещения", 2],
  ["C", "сочетания", 2],
  ["C(n,2)", "пары", 2],
];

export default function C3Recap({ cues }) {
  const ctl = useSteps(cues || [1.5, 8.1, 18.3, 24.7], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g key={big} className="a-t" style={{ transform: `translate(${40 + i * 70}px, 52px) scale(${on ? 1.1 : 1})` }}>
            <rect x="-31" y="-34" width="62" height="68" rx="10" style={{ fill: on || done ? "var(--s-green)" : "var(--s-panel2)", stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)", strokeWidth: on ? 2 : 1.4 }} />
            <text y="6" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>{big}</text>
            <text y="24" textAnchor="middle" className="a-cap">{name}</text>
          </g>
        );
      })}
      {["пароли", "пин-коды", "покер", "рукопожатия"].map((t, i) => (
        <Pill key={t} x={50 + i * 87} y={116} w={80} text={t} o={step >= 3 ? 1 : 0} stroke="var(--s-amber)" size={9.5} />
      ))}
      <Pill x={180} y={152} w={246} h={24} text="Глава 4 · Паскаль, бином Ньютона, Дирихле →" o={step >= 4 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10} />
    </Steps>
  );
}
