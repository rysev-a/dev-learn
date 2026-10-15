import { Pill, Steps, useSteps } from "./kit.jsx";

/* Глава 2, слайд 13: итог. Карточки понятий главы загораются по очереди,
   затем — где это живёт в коде, и что дальше. */

const LABELS = ["Итог", "Пары → отношение", "Свойства", "Функции", "Словарь", "Дальше"];
const CAPTION = [
  "Подведём итог главы",
  "Пары собираются в прямое произведение; подмножество произведения — отношение",
  "Рефлексивность, симметричность и транзитивность делят отношения на эквивалентности и порядки",
  "Функция — отношение с контрактом «ровно один выход»; её виды — инъекция, сюръекция, биекция",
  "Внешние ключи, группировки, топологическая сортировка, чистые функции — один словарь",
  "Дальше — калькулятор: комбинаторика научит считать, сколько всего бывает",
];
const CARDS = [
  ["(a, b)", "пары", 1],
  ["A × B", "произв.", 1],
  ["R", "отношение", 1],
  ["≡  ≼", "свойства", 2],
  ["f", "функции", 3],
];

export default function C2Recap({ cues }) {
  const ctl = useSteps(cues || [1.5, 10.8, 19.5, 25.7], 2600);
  const { step } = ctl;
  const wide = 62;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CARDS.map(([big, name, at], i) => {
        const on = step === at;
        const done = step > at;
        return (
          <g
            key={big}
            className="a-t"
            style={{ transform: `translate(${40 + i * 70}px, 52px) scale(${on ? 1.1 : 1})` }}
          >
            <rect
              x={-wide / 2}
              y="-34"
              width={wide}
              height="68"
              rx="10"
              style={{
                fill: on || done ? "var(--s-green)" : "var(--s-panel2)",
                stroke: on ? "var(--s-accent)" : done ? "var(--s-accent-a45)" : "var(--s-border)",
                strokeWidth: on ? 2 : 1.4,
              }}
            />
            <text y="6" textAnchor="middle" className="a-mono" style={{ fontSize: 15, fill: "var(--s-accent)" }}>{big}</text>
            <text y="24" textAnchor="middle" className="a-cap">{name}</text>
          </g>
        );
      })}
      {["внешний ключ", "GROUP BY", "toposort", "чистая f"].map((t, i) => (
        <Pill key={t} x={50 + i * 87} y={116} w={80} text={t} o={step >= 4 ? 1 : 0} stroke="var(--s-amber)" size={9.5} />
      ))}
      <Pill
        x={180}
        y={152}
        w={236}
        h={24}
        text="Глава 3 · комбинаторика: сколько всего бывает →"
        o={step >= 5 ? 1 : 0}
        stroke="var(--s-accent)"
        fill="var(--s-green)"
        color="var(--s-accent)"
        size={10}
      />
    </Steps>
  );
}
