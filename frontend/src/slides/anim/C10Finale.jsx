import { Pill, Steps, useSteps } from "./kit.jsx";

/* Глава 10, слайд 13: итог главы и всего курса. */

const LABELS = ["Итог", "Язык", "Логика", "Графы", "Вероятность", "Дальше"];
const CAPTION = [
  "Подведём итог — и заодно закроем весь курс",
  "Язык: множества, отношения и комбинаторика — описывать данные и считать варианты",
  "Логика: предикаты и кванторы формулируют утверждения, индукция и рекуррентности — доказывают и оценивают время",
  "Графы: вершины, рёбра и обходы — каркас для DOM-деревьев, зависимостей и маршрутов",
  "Вероятность и Байес добавили главное — умение рассуждать там, где гарантий нет",
  "Теперь этот курс — ваш инструмент: дальше программирование на Python и алгоритмы, и всё оживёт строчка за строчкой",
];
const CARDS = [
  ["∈  ×  C", "язык", 1],
  ["∀  ∃  ⇒", "логика", 2],
  ["V, E", "графы", 3],
  ["P(A|B)", "вероятность", 4],
];

export default function C10Finale({ cues }) {
  const ctl = useSteps(cues || [3.1, 9.2, 17.6, 23.4, 28.3], 2800);
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
      <Pill x={180} y={140} w={290} h={26} text="Дальше · Python и алгоритмы →" o={step >= 5 ? 1 : 0} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
    </Steps>
  );
}
