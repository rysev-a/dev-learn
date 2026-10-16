import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 4: квантор всеобщности — «для каждого». x + 0 = x,
   пассажиры, нельзя доказать парой примеров. */

const LABELS = ["Утверждение", "∀", "x + 0 = x", "Пассажиры", "Не примерами"];
const CAPTION = [
  "Как превращать предикаты в законченные утверждения",
  "Первый способ — квантор всеобщности: «для каждого», «для всех»",
  "Для каждого x верно x + 0 = x — получаем утверждение, истинное или ложное",
  "«Все пассажиры пристёгнуты» — про каждого без исключения; одного расстёгнутого достаточно для опровержения",
  "Утверждение про всех нельзя доказать парой случаев — нужно общее рассуждение для любого значения",
];

export default function C6Forall({ cues }) {
  const ctl = useSteps(cues || [3.8, 8.7, 16.3, 23.8], 3000);
  const { step } = ctl;
  const bad = step === 3;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={90} y={70} w={90} h={36} text="P(x)" stroke="var(--s-blue)" size={16} />
        <Txt x="180" y="75" mono size={18} color="var(--s-accent)">→</Txt>
        <Pill x={270} y={70} w={130} h={36} text="утверждение" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
      </G>
      <Txt x="180" y="86" mono size={44} o={step === 1 ? 1 : 0} color="var(--s-accent)">∀x  P(x)</Txt>
      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="24" mono size={13} color="var(--s-accent)">∀x  (x + 0 = x)</Txt>
        {Array.from({ length: 12 }, (_, i) => (
          <Dot key={i} x={40 + (i % 6) * 56} y={60 + Math.floor(i / 6) * 38} r={13} text={i - 3} stroke="var(--s-accent)" fill="var(--s-green)" size={10} />
        ))}
        <Txt x="180" y="148" size={10}>каждое x — подтверждает равенство</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x="180" y="24" mono size={13} color={bad ? "var(--s-red)" : "var(--s-accent)"}>∀ пассажир: пристёгнут</Txt>
        {Array.from({ length: 6 }, (_, i) => (
          <g key={i}>
            <Dot x={46 + i * 54} y={70} r={16} text={i === 3 ? "✗" : "✓"} stroke={i === 3 ? "var(--s-red)" : "var(--s-accent)"} fill={i === 3 ? "var(--s-red)" : "var(--s-green)"} fillOpacity={i === 3 ? 0.3 : 1} size={12} />
          </g>
        ))}
        <Txt x="208" y="108" size={10} color="var(--s-red)">один расстёгнутый</Txt>
        <Txt x="180" y="148" mono size={12} color="var(--s-red)">∀ опровергнуто</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Dot x={60} y={64} r={11} text="3" stroke="var(--s-accent)" />
        <Dot x={104} y={64} r={11} text="7" stroke="var(--s-accent)" />
        {Array.from({ length: 8 }, (_, i) => (
          <circle key={i} cx={152 + i * 22} cy={64} r="3" style={{ fill: "var(--s-muted)" }} />
        ))}
        <Txt x="210" y="96" size={10}>…и так без конца</Txt>
        <Txt x="180" y="128" mono size={13} color="var(--s-amber)">два примера ≠ «для всех»</Txt>
      </G>
    </Steps>
  );
}
