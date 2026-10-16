import { G, Pill, Steps, Table, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 8: тавтология и противоречие — классы формул. */

const LABELS = ["Классы", "Тавтология", "Противоречие", "Диагноз", "Скрытые"];
const CAPTION = [
  "Формулы делятся на классы по всей таблице истинности",
  "Тавтология истинна во всех строках: «идёт дождь или не идёт дождь»",
  "Противоречие ложно во всех строках: «дождь и не дождь одновременно»",
  "В коде: тавтология — мёртвая проверка, противоречие — недостижимая ветка",
  "Линтеры чистят такое сами, но в рассуждениях противоречия прячутся чаще, чем кажется",
];

export default function C5Classes({ cues }) {
  const ctl = useSteps(cues || [4.1, 8.8, 12.5, 20.8], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={100} y={60} w={130} h={40} text="тавтология" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" />
        <Pill x={260} y={60} w={130} h={40} text="противоречие" stroke="var(--s-red)" />
        <Pill x={180} y={116} w={150} h={32} text="остальные" stroke="var(--s-muted)" />
      </G>
      <Table x={96} y={34} head={["p", "¬p", "p∨¬p"]} rows={[[1, 0, 1], [0, 1, 1]]} cw={56} rh={30} o={step === 1 ? 1 : 0} hl={(r, c) => (c === 2 ? "g" : null)} />
      <Txt x="180" y="130" mono size={13} o={step === 1 ? 1 : 0} color="var(--s-accent)">всегда истина</Txt>
      <Table x={96} y={34} head={["p", "¬p", "p∧¬p"]} rows={[[1, 0, 0], [0, 1, 0]]} cw={56} rh={30} o={step === 2 ? 1 : 0} hl={(r, c) => (c === 2 ? "r" : null)} />
      <Txt x="180" y="130" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-red)">всегда ложь</Txt>
      <G o={step === 3 ? 1 : 0}>
        <rect x="30" y="26" width="300" height="46" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)" }} />
        <text x="46" y="46" className="a-mono" style={{ fontSize: 11 }}>if x or not x:</text>
        <text x="46" y="62" className="a-mono" style={{ fontSize: 11, fill: "var(--s-muted)" }}>… # проверка всегда проходит</text>
        <rect x="30" y="84" width="300" height="46" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-red)" }} />
        <text x="46" y="104" className="a-mono" style={{ fontSize: 11 }}>if p and not p:</text>
        <text x="46" y="120" className="a-mono" style={{ fontSize: 11, fill: "var(--s-muted)" }}>… # ветка недостижима</text>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {["всегда", "никогда", "либо то, либо это"].map((t, i) => (
          <Pill key={t} x={60 + i * 100} y={60} w={t.length > 8 ? 130 : 78} text={`«${t}»`} stroke="var(--s-amber)" size={9.5} />
        ))}
        <Txt x="180" y="108" size={10}>в таких словах и прячутся противоречия</Txt>
      </G>
    </Steps>
  );
}
