import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 2: предикат — заготовка с переменной; подстановка даёт
   высказывание; это функция, возвращающая bool. */

const LABELS = ["Заготовка", "Подстановка", "Возраст", "Функция"];
const CAPTION = [
  "«x больше пяти» — ни правда, ни ложь: висит в воздухе, пока не известен x",
  "Такая заготовка с переменной — предикат: подставили значение — получили обычное высказывание",
  "«Возраст больше 18»: при 20 — истина, при 15 — ложь",
  "Ничего мистического: функция, принимающая значение и возвращающая bool",
];

export default function C6Predicate({ cues }) {
  const ctl = useSteps(cues || [8.7, 17.2, 23.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={180} y={70} w={150} h={44} text="x > 5" stroke="var(--s-blue)" size={20} />
        <Txt x="180" y="116" mono size={14} color="var(--s-amber)">?</Txt>
        <Txt x="180" y="140" size={10}>ни истина, ни ложь</Txt>
      </G>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={180} y={34} w={120} h={30} text="P(x) = x > 5" stroke="var(--s-blue)" size={12} />
        {[
          [7, 1],
          [3, 0],
        ].map(([v, ok], i) => (
          <g key={v}>
            <Pill x={70} y={96 + i * 36} w={50} text={`x = ${v}`} stroke="var(--s-muted)" size={10} />
            <Arrow x1={98} y1={96 + i * 36} x2={236} y2={96 + i * 36} c={ok ? "g" : "r"} />
            <Pill x={280} y={96 + i * 36} w={64} text={ok ? "истина" : "ложь"} stroke={ok ? "var(--s-accent)" : "var(--s-red)"} size={10} />
          </g>
        ))}
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={180} y={34} w={200} h={30} text="возраст > 18" stroke="var(--s-blue)" size={12} />
        {[
          [20, 1],
          [15, 0],
        ].map(([v, ok], i) => (
          <g key={v}>
            <Pill x={70} y={96 + i * 36} w={60} text={`${v} лет`} stroke="var(--s-muted)" size={10} />
            <Arrow x1={104} y1={96 + i * 36} x2={236} y2={96 + i * 36} c={ok ? "g" : "r"} />
            <Pill x={280} y={96 + i * 36} w={64} text={ok ? "истина" : "ложь"} stroke={ok ? "var(--s-accent)" : "var(--s-red)"} size={10} />
          </g>
        ))}
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <rect x="50" y="34" width="260" height="76" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="70" y="62" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>def adult(age):</text>
        <text x="90" y="86" className="a-mono" style={{ fontSize: 13 }}>return age &gt; 18</text>
        <Txt x="180" y="140" mono size={12}>значение → bool</Txt>
      </G>
    </Steps>
  );
}
