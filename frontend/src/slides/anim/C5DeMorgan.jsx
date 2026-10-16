import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 10: законы де Моргана для логики — зонтик и ключи,
   инверсия условия в коде, ранний возврат. */

const LABELS = ["Де Морган", "Два закона", "Зонтик и ключи", "Инверсия", "Ранний возврат"];
const CAPTION = [
  "Самые полезные законы — снова де Моргана, теперь для логики",
  "«Неверно, что a и b» = «не a или не b»; «неверно, что a или b» = «не a и не b»",
  "Бытовая проверка: не взял зонтик и ключи одновременно — значит, не взял зонтик или не взял ключи",
  "Инструкция к инверсии условий: «не» от «и» даёт «или» отрицаний, от «или» — «и» отрицаний",
  "Каждый, кто выворачивал условие ради раннего возврата, применял де Моргана",
];

export default function C5DeMorgan({ cues }) {
  const ctl = useSteps(cues || [4.0, 9.8, 16.2, 24.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={180} y={80} w={200} h={44} text="¬(a ∧ b)  ↔  ¬a ∨ ¬b" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
      </G>
      <G o={step === 1 ? 1 : 0}>
        <Txt x="180" y="46" mono size={15}>¬(a ∧ b) = ¬a ∨ ¬b</Txt>
        <Txt x="180" y="90" mono size={15} color="var(--s-amber)">¬(a ∨ b) = ¬a ∧ ¬b</Txt>
        <Txt x="180" y="130" size={10}>«и» ↔ «или» меняются местами, отрицание уходит внутрь</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={90} y={46} w={110} text="зонтик ✓" stroke="var(--s-blue)" />
        <Txt x="150" y="50" mono size={14}>∧</Txt>
        <Pill x={220} y={46} w={90} text="ключи ✓" stroke="var(--s-amber)" />
        <Txt x="180" y="86" mono size={12}>не взял оба сразу</Txt>
        <Txt x="180" y="104" mono size={16} color="var(--s-accent)">⇓</Txt>
        <Txt x="180" y="132" mono size={12} color="var(--s-accent)">нет зонтика ИЛИ нет ключей</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <text x="30" y="46" className="a-mono" style={{ fontSize: 12 }}>if not (a and b):</text>
        <text x="190" y="46" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>↔  if not a or not b:</text>
        <text x="30" y="92" className="a-mono" style={{ fontSize: 12 }}>if not (a or b):</text>
        <text x="190" y="92" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>↔  if not a and not b:</text>
        <Txt x="180" y="134" size={10}>отрицание переворачивает операцию</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="40" y="26" width="130" height="78" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="52" y="48" className="a-mono" style={{ fontSize: 10.5 }}>if a and b:</text>
        <text x="62" y="64" className="a-mono" style={{ fontSize: 10.5 }}>работа…</text>
        <text x="52" y="84" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-muted)" }}>return</text>
        <Txt x="190" y="68" mono size={16} color="var(--s-accent)">→</Txt>
        <rect x="210" y="26" width="120" height="78" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)" }} />
        <text x="222" y="48" className="a-mono" style={{ fontSize: 10.5 }}>if not a or not b:</text>
        <text x="232" y="64" className="a-mono" style={{ fontSize: 10.5 }}>return</text>
        <text x="222" y="84" className="a-mono" style={{ fontSize: 10.5 }}>работа…</text>
        <Txt x="180" y="132" size={10}>ранний возврат — де Морган в действии</Txt>
      </G>
    </Steps>
  );
}
