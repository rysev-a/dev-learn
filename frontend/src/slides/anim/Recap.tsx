import { Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 13: итог главы. Карточки тем по очереди загораются под голос,
   затем — где это применялось и что дальше. */

const LABELS = ["Итог", "∈", "∪ ∩", "¬", "|A|", "2ⁿ", "Применяли", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Множество — элементы без порядка и повторов",
  "Операции: объединение, пересечение, разность и дополнение",
  "Законы де Моргана связывают отрицание с этими операциями",
  "Мощность считает элементы",
  "Булеан содержит 2ⁿ подмножеств",
  "Всё это вы уже применяли в сетах и запросах к базам — теперь у инструментов есть точный язык",
  "Дальше — отношения и функции: внешние ключи, связи таблиц, чистые функции",
];
const CARDS: [string, string][] = [
  ["∈", "элементы"],
  ["∪ ∩", "операции"],
  ["¬", "де Морган"],
  ["|A|", "мощность"],
  ["2ⁿ", "булеан"],
];

export default function Recap({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.4, 4.2, 7.8, 11.1, 13.2, 15.3, 21.1], 2400);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name], i) => {
        const on = step === i + 1;
        const done = step > i + 1;
        return (
          <g
            key={big}
            className="a-t"
            style={{ transform: `translate(${38 + i * 71}px, 52px) scale(${on ? 1.1 : 1})` }}
          >
            <rect
              x="-31"
              y="-34"
              width="62"
              height="68"
              rx="10"
              style={{
                fill: on || done ? "var(--s-green)" : "var(--s-panel2)",
                stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)",
                strokeWidth: on ? 2 : 1.4,
              }}
            />
            <text y="6" textAnchor="middle" className="a-mono" style={{ fontSize: 17, fill: "var(--s-accent)" }}>
              {big}
            </text>
            <text y="24" textAnchor="middle" className="a-cap">{name}</text>
          </g>
        );
      })}
      {["set()", "UNION", "INTERSECT", "EXCEPT"].map((t, i) => (
        <Pill key={t} x={64 + i * 77} y={116} w={66} text={t} o={step >= 6 ? 1 : 0} stroke="var(--s-amber)" />
      ))}
      <Pill
        x={180}
        y={150}
        w={250}
        h={24}
        text="Глава 2 · отношения и функции →"
        o={step >= 7 ? 1 : 0}
        stroke="var(--s-accent)"
        fill="var(--s-green)"
        color="var(--s-accent)"
        size={11}
      />
    </Steps>
  );
}
