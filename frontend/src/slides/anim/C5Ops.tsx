import { G, Pill, Steps, Table, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 3: три основные операции — «не», «и», «или» (включающее),
   приоритет. */

const LABELS = ["Операции", "Не", "И", "Или", "Приоритет"];
const CAPTION = [
  "Из высказываний строятся составные с помощью трёх основных операций",
  "«Не» переворачивает истинность",
  "«И» истинно, только когда истинны обе части",
  "«Или» истинно, когда истинна хотя бы одна часть — включая случай обеих",
  "Приоритет: «не» сильнее «и», «и» сильнее «или» — скобки нужны для однозначности",
];
const AB: [number, number][] = [
  [1, 1],
  [1, 0],
  [0, 1],
  [0, 0],
];

export default function C5Ops({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.3, 6.2, 8.9, 18.8], 2800);
  const { step } = ctl;
  const op = step === 2 ? (a: number, b: number) => a & b : (a: number, b: number) => a | b;
  const rows2 = AB.map(([a, b]) => [a, b, op(a, b)]);
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {[
          ["¬", "не"],
          ["∧", "и"],
          ["∨", "или"],
        ].map(([s, n], i) => (
          <g key={s}>
            <rect x={50 + i * 100} y="46" width="80" height="60" rx="12" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
            <text x={90 + i * 100} y="80" textAnchor="middle" className="a-mono" style={{ fontSize: 24, fill: "var(--s-accent)" }}>{s}</text>
            <text x={90 + i * 100} y="98" textAnchor="middle" className="a-cap">{n}</text>
          </g>
        ))}
      </G>
      <Table x={130} y={36} head={["p", "¬p"]} rows={[[1, 0], [0, 1]]} cw={50} rh={30} o={step === 1 ? 1 : 0} hl={(r, c) => (c === 1 ? "g" : null)} />
      <Table x={96} y={30} head={["p", "q", step === 2 ? "p∧q" : "p∨q"]} rows={rows2} cw={52} rh={26} o={step === 2 || step === 3 ? 1 : 0} hl={(r, c) => (c === 2 ? (rows2[r]![2] ? "g" : "r") : step === 3 && r === 0 && c < 2 ? "y" : null)} />
      <Txt x={300} y={68} size={10} o={step === 3 ? 1 : 0} color="var(--s-amber)">обе истинны —</Txt>
      <Txt x={300} y={82} size={10} o={step === 3 ? 1 : 0} color="var(--s-amber)">тоже истина</Txt>
      <G o={step === 4 ? 1 : 0}>
        <Txt x={180} y={30} mono size={16}>¬p ∨ q ∧ r</Txt>
        {([
          ["¬p", "1", 64],
          ["q ∧ r", "2", 150],
          ["∨", "3", 250],
        ] as const).map(([t, n, x]) => (
          <g key={n}>
            <Pill x={x} y={76} w={t === "∨" ? 36 : 64} text={t} stroke="var(--s-amber)" />
            <Txt x={x} y={104} mono size={12} color="var(--s-accent)">{n}</Txt>
          </g>
        ))}
        <Txt x={180} y={140} mono size={13} color="var(--s-accent)">(¬p) ∨ (q ∧ r)</Txt>
      </G>
    </Steps>
  );
}
