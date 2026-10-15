import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 10, слайд 7: формула Байеса — оборачивание условия; априорная
   уверенность → свидетельство → апостериорная. */

const LABELS = ["Байес", "Формула", "Обновление", "Сервис", "Бухгалтерия"];
const CAPTION = [
  "Формула Байеса — правило оборачивания условия",
  "P(причина | следствие) = P(следствие | причина) · P(причина) / P(следствие)",
  "Человеческое прочтение: мы обновляем уверенность, когда появляются новые данные",
  "Сервис падал раньше (априорная) → сработал мониторинг (свидетельство) → теперь верим иначе (апостериорная)",
  "Байес — не заклинание, а честная бухгалтерия убеждений",
];

export default function C10Bayes({ cues }) {
  const ctl = useSteps(cues || [3.6, 13.3, 19.1, 29.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">P(A|B)  ⇄  P(B|A)</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Txt x="180" y="50" mono size={16}>P(A | B) = P(B | A) · P(A)</Txt>
        <line x1="60" y1="64" x2="300" y2="64" style={{ stroke: "var(--s-text)", strokeWidth: 1.4 }} />
        <Txt x="180" y="88" mono size={16}>P(B)</Txt>
        <Txt x="180" y="132" size={10}>причина A, следствие B</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={70} y={70} w={96} h={44} text="было" stroke="var(--s-blue)" size={13} />
        <Txt x="70" y="104" size={9.5}>P(A) — априори</Txt>
        <Arrow x1={122} y1={70} x2={160} y2={70} c="g" />
        <Pill x={190} y={70} w={56} h={44} text="B" stroke="var(--s-amber)" size={15} />
        <Txt x="190" y="104" size={9.5}>свидетельство</Txt>
        <Arrow x1={222} y1={70} x2={260} y2={70} c="g" />
        <Pill x={300} y={70} w={80} h={44} text="стало" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x="300" y="104" size={9.5}>P(A|B) — апостериори</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {[
          ["падал раньше", "P(упал)", "5 %", "var(--s-blue)"],
          ["мониторинг сработал", "новые данные", "", "var(--s-amber)"],
          ["теперь", "P(упал | сработал)", "70 %", "var(--s-accent)"],
        ].map(([t, f, v, c], i) => (
          <g key={t}>
            <rect x="40" y={22 + i * 42} width="280" height="34" rx="10" style={{ fill: "var(--s-panel2)", stroke: c, strokeWidth: 1.5 }} />
            <text x="56" y={43 + i * 42} className="a-cap" style={{ fontSize: 10.5, fill: "var(--s-text)" }}>{t}</text>
            <text x="304" y={43 + i * 42} textAnchor="end" className="a-mono" style={{ fontSize: 11, fill: c }}>{f} {v}</text>
          </g>
        ))}
        <Txt x="180" y="152" size={9.5}>числа иллюстративные</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={180} y={70} w={240} h={44} text="бухгалтерия убеждений" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x="180" y="116" size={10}>приход — свидетельства, остаток — уверенность</Txt>
      </G>
    </Steps>
  );
}
