import { Pill, Steps, useSteps } from "./kit.tsx";

/* Глава 5, слайд 13: итог главы. */

const LABELS = ["Итог", "Словарь", "Применение", "Дальше", "Примеры"];
const CAPTION = [
  "Подведём итог главы",
  "Словарь: высказывание, «не», «и», «или», импликация, эквивалентность, таблицы, тавтологии, де Морган, замыкание",
  "Это правила обращения с отдельными утверждениями — уже на этом уровне чистится половина запутанных условий",
  "Дальше — предикаты и кванторы: говорить обо всех элементах сразу или хотя бы об одном",
  "Так формулируются свойства программ: нет отрицательных, найдётся индекс, любой запрос вовремя",
];
const WORDS = ["p", "¬", "∧", "∨", "→", "↔", "таблицы", "p ∨ ¬p", "де Морган", "замыкание"];

export default function C5Recap({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.4, 13.1, 21.2, 29.4], 2600);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {WORDS.map((w, i) => (
        <Pill
          key={w}
          x={50 + (i % 5) * 65}
          y={36 + Math.floor(i / 5) * 36}
          w={w.length > 5 ? 74 : 46}
          h={26}
          text={w}
          o={step >= 1 ? 1 : 0}
          stroke={step >= 2 ? "var(--s-accent)" : "var(--s-border)"}
          fill={step >= 2 ? "var(--s-green)" : "var(--s-panel2)"}
          color={step >= 2 ? "var(--s-accent)" : "var(--s-text)"}
          size={w.length > 5 ? 8.5 : 11}
        />
      ))}
      <Pill x={90} y={120} w={140} h={28} text="∀  для всех" o={step >= 3 ? 1 : 0} stroke="var(--s-amber)" size={11} />
      <Pill x={270} y={120} w={140} h={28} text="∃  найдётся" o={step >= 3 ? 1 : 0} stroke="var(--s-amber)" size={11} />
      <Pill x={180} y={152} w={300} h={22} text="нет отрицательных · найдётся индекс · любой запрос вовремя" o={step >= 4 ? 1 : 0} stroke="var(--s-accent)" size={8.5} />
    </Steps>
  );
}
