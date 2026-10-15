import { Pill, Steps, useSteps } from "./kit.jsx";

/* Глава 7, слайд 13: итог главы. */

const LABELS = ["Итог", "Индукция", "Сильная", "Рекурсия", "Рекуррентности", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Индукция доказывает утверждения для всех натуральных двумя шагами — база и переход: лестница",
  "Сильная индукция разрешает опираться на все предыдущие значения сразу",
  "Рекурсия — это индукция в коде, и её база — вопрос жизни и смерти стека",
  "Рекуррентности записывают алгоритмы формулами и дают время: слияние — n log n, неудачная быстрая — квадрат",
  "Дальше — графы: структуры, где рекурсия и обходы заиграют в полную силу",
];
const CARDS = [
  ["база + шаг", "индукция", 1],
  ["P(<k) ⇒ P(k)", "сильная", 2],
  ["f(n−1)", "рекурсия", 3],
  ["T(n)", "рекуррентности", 4],
];

export default function C7Recap({ cues }) {
  const ctl = useSteps(cues || [1.5, 9.7, 13.6, 18.6, 27.3], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g key={name} className="a-t" style={{ transform: `translate(${50 + i * 86}px, 62px) scale(${on ? 1.1 : 1})` }}>
            <rect x="-38" y="-40" width="76" height="80" rx="10" style={{ fill: on || done ? "var(--s-green)" : "var(--s-panel2)", stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)", strokeWidth: on ? 2 : 1.4 }} />
            <text y="4" textAnchor="middle" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>{big}</text>
            <text y="26" textAnchor="middle" className="a-cap" style={{ fontSize: 8.5 }}>{name}</text>
          </g>
        );
      })}
      <Pill x={180} y={140} w={260} h={26} text="Глава 8 · графы: основы →" o={step >= 5 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
