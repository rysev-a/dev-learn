import { Arrow, G, Pill, Steps, Table, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 7: эквивалентность «тогда и только тогда» — двусторонняя
   импликация; тесты; рефакторинг. */

const LABELS = ["Эквивалентность", "Таблица", "Две стрелки", "Тесты", "Рефакторинг"];
const CAPTION = [
  "Шестая операция — эквивалентность: «тогда и только тогда»",
  "Истинна, когда обе части совпадают: обе истинны или обе ложны",
  "Это двусторонняя импликация: из первого следует второе и обратно",
  "В тестах: ожидаемый результат равен фактическому — иначе тест красный",
  "В рефакторинге: «новое условие эквивалентно старому» — таблицы совпали по всем строкам",
];

export default function C5Equiv({ cues }) {
  const ctl = useSteps(cues || [4.0, 9.6, 14.4, 19.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={34} o={step === 0 ? 1 : 0} color="var(--s-accent)">p ↔ q</Txt>
      <Table x={100} y={34} head={["p", "q", "p↔q"]} rows={[[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]]} cw={54} rh={26} o={step === 1 ? 1 : 0} hl={(r, c) => (c === 2 ? ([0, 3].includes(r) ? "g" : "r") : null)} />
      <G o={step === 2 ? 1 : 0}>
        <Pill x={70} y={70} w={70} h={34} text="p" stroke="var(--s-blue)" size={14} />
        <Pill x={290} y={70} w={70} h={34} text="q" stroke="var(--s-amber)" size={14} />
        <Arrow x1={110} y1={62} x2={250} y2={62} c="g" />
        <Arrow x1={250} y1={78} x2={110} y2={78} c="y" />
        <Txt x="180" y="50" mono size={10} color="var(--s-accent)">p → q</Txt>
        <Txt x="180" y="100" mono size={10} color="var(--s-amber)">q → p</Txt>
        <Txt x="180" y="132" mono size={13}>(p → q) ∧ (q → p)</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {[
          ["expected == actual", 1],
          ["expected == actual", 1],
          ["expected == actual", 0],
        ].map(([t, ok], i) => (
          <g key={i}>
            <rect x="50" y={26 + i * 36} width="260" height="28" rx="8" style={{ fill: "var(--s-panel2)", stroke: ok ? "var(--s-accent)" : "var(--s-red)", strokeWidth: 1.4 }} />
            <text x="66" y={44 + i * 36} className="a-mono" style={{ fontSize: 11 }}>{t}</text>
            <text x="294" y={45 + i * 36} textAnchor="end" className="a-mono" style={{ fontSize: 13, fill: ok ? "var(--s-accent)" : "var(--s-red)" }}>{ok ? "✓" : "✗ красный"}</text>
          </g>
        ))}
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={90} y={44} w={140} h={28} text="старое условие" stroke="var(--s-muted)" />
        <Pill x={270} y={44} w={140} h={28} text="новое условие" stroke="var(--s-blue)" />
        {Array.from({ length: 8 }, (_, i) => (
          <g key={i}>
            <rect x={44 + i * 22} y="86" width="18" height="16" rx="3" style={{ fill: i % 3 ? "var(--s-green)" : "var(--s-panel2)", stroke: "var(--s-accent)" }} />
            <rect x={44 + i * 22 + 140} y="86" width="18" height="16" rx="3" style={{ fill: i % 3 ? "var(--s-green)" : "var(--s-panel2)", stroke: "var(--s-accent)" }} />
          </g>
        ))}
        <Txt x="180" y="136" mono size={12} color="var(--s-accent)">8 строк совпали ⇒ эквивалентны</Txt>
      </G>
    </Steps>
  );
}
