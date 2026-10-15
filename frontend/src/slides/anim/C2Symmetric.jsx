import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 2, слайд 6: симметричность. Дружба — стрелки в обе стороны,
   подписка — в одну; что это значит для хранения в таблицах. */

const LABELS = ["Свойство", "Дружба", "Подписка", "В схеме"];
const CAPTION = [
  "Симметричность: если первый связан со вторым, то и второй связан с первым",
  "Дружба симметрична: подружились оба — связь в обе стороны",
  "Подписка несимметрична: вы подписаны на автора, а автор на вас — нет",
  "В схеме: дружба хранится парой в обе стороны, подписка — только в одну",
];

export default function C2Symmetric({ cues }) {
  const ctl = useSteps(cues || [5.5, 8.8, 13.6], 3000);
  const { step } = ctl;
  const graph = step <= 2 ? 1 : 0;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={graph}>
        <Pill x={60} y={74} w={56} text="Аня" stroke="var(--s-blue)" />
        <Pill x={180} y={34} w={56} text="Борис" stroke="var(--s-amber)" />
        <Pill x={300} y={74} w={56} text="Вера" stroke="var(--s-accent)" />
        {/* шаг 0 и 1: туда и обратно */}
        <Arrow x1={86} y1={64} x2={150} y2={42} c="g" o={step === 0 ? 1 : 0} />
        <Arrow x1={150} y1={46} x2={90} y2={68} c="g" o={step === 0 ? 1 : 0} dash="4 3" />
        <Arrow x1={86} y1={64} x2={150} y2={42} c="g" both o={step === 1 ? 1 : 0} />
        <Arrow x1={210} y1={42} x2={274} y2={64} c="g" both o={step === 1 ? 1 : 0} />
        {/* шаг 2: подписки в одну сторону */}
        <Arrow x1={86} y1={64} x2={150} y2={42} c="y" o={step === 2 ? 1 : 0} />
        <Arrow x1={274} y1={68} x2={210} y2={46} c="y" o={step === 2 ? 1 : 0} />
        <Arrow x1={150} y1={46} x2={90} y2={68} c="r" dash="3 4" o={step === 2 ? 0.6 : 0} />
        <Arrow x1={210} y1={46} x2={270} y2={66} c="r" dash="3 4" o={step === 2 ? 0.6 : 0} />
        <Txt x="180" y="112" o={step === 2 ? 1 : 0} color="var(--s-red)">обратных стрелок нет</Txt>
        <Txt x="180" y="112" o={step === 1 ? 1 : 0} color="var(--s-accent)">a ↔ b: обе половины пары</Txt>
        <Txt x="180" y="112" o={step === 0 ? 1 : 0}>a R b ⇒ b R a</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <rect x="24" y="22" width="150" height="104" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.4 }} />
        <text x="99" y="40" textAnchor="middle" className="a-cap">friends</text>
        {["(Аня, Борис)", "(Борис, Аня)", "(Борис, Вера)", "(Вера, Борис)"].map((t, i) => (
          <text key={t} x="40" y={62 + i * 16} className="a-mono" style={{ fontSize: 10 }}>{t}</text>
        ))}
        <rect x="186" y="22" width="150" height="104" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.4 }} />
        <text x="261" y="40" textAnchor="middle" className="a-cap">follows</text>
        {["(Аня, Борис)", "(Вера, Борис)"].map((t, i) => (
          <text key={t} x="202" y={62 + i * 16} className="a-mono" style={{ fontSize: 10 }}>{t}</text>
        ))}
        <Txt x="99" y="148" color="var(--s-accent)">в обе стороны</Txt>
        <Txt x="261" y="148" color="var(--s-amber)">только в одну</Txt>
      </G>
    </Steps>
  );
}
