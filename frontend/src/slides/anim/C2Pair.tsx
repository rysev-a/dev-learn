import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 2: упорядоченная пара. В множестве порядок не важен,
   в паре — суть; широта/долгота на карте; кортеж в коде. */

const LABELS = ["Множество", "Пара", "Карта", "В коде"];
const CAPTION = [
  "В множестве порядок не играл никакой роли: {1, 2} = {2, 1}",
  "В паре порядок — суть: первый и второй элемент занимают разные позиции",
  "Точка на карте — пара (широта, долгота); переставили — и получилось другое место",
  "В коде это кортеж или массив из двух элементов, где позиция несёт смысл",
];

export default function C2Pair({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.1, 10.4, 16.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* шаги 0–1: слоты */}
      <G o={step <= 1 ? 1 : 0}>
        <Txt x={180} y={22} mono color="var(--s-accent)" size={13}>
          {step === 0 ? "{ 1, 2 } = { 2, 1 }" : "(1, 2) ≠ (2, 1)"}
        </Txt>
        <rect x="110" y="40" width="64" height="44" rx="8" className="a-ring" style={{ stroke: "var(--s-border)", strokeDasharray: step === 0 ? "none" : "4 3" }} />
        <rect x="186" y="40" width="64" height="44" rx="8" className="a-ring" style={{ stroke: "var(--s-border)", strokeDasharray: step === 0 ? "none" : "4 3" }} />
        <Txt x={142} y={100} o={step === 1 ? 1 : 0}>1-й</Txt>
        <Txt x={218} y={100} o={step === 1 ? 1 : 0}>2-й</Txt>
        <Pill x={142} y={62} w={40} text="1" stroke="var(--s-blue)" />
        <Pill x={218} y={62} w={40} text="2" stroke="var(--s-amber)" />
        <rect x="110" y="120" width="64" height="30" rx="8" className="a-t" style={{ fill: "none", stroke: "var(--s-border)", strokeDasharray: "4 3", opacity: step === 1 ? 1 : 0 }} />
        <rect x="186" y="120" width="64" height="30" rx="8" className="a-t" style={{ fill: "none", stroke: "var(--s-border)", strokeDasharray: "4 3", opacity: step === 1 ? 1 : 0 }} />
        <Pill x={142} y={135} w={40} text="2" o={step === 1 ? 1 : 0} stroke="var(--s-amber)" />
        <Pill x={218} y={135} w={40} text="1" o={step === 1 ? 1 : 0} stroke="var(--s-blue)" />
        <Txt x={290} y={104} o={step === 1 ? 1 : 0} color="var(--s-red)">другая пара</Txt>
      </G>

      {/* шаг 2: карта */}
      <G o={step === 2 ? 1 : 0}>
        <rect x="60" y="16" width="170" height="120" rx="8" className="a-ring" style={{ stroke: "var(--s-border)" }} />
        {[1, 2, 3].map((i) => (
          <g key={i}>
            <line x1={60 + i * 42.5} y1="16" x2={60 + i * 42.5} y2="136" style={{ stroke: "var(--s-border)", strokeDasharray: "2 4" }} />
            <line x1="60" y1={16 + i * 30} x2="230" y2={16 + i * 30} style={{ stroke: "var(--s-border)", strokeDasharray: "2 4" }} />
          </g>
        ))}
        <circle cx="187" cy="46" r="7" style={{ fill: "var(--s-accent)" }} />
        <circle cx="102" cy="106" r="7" style={{ fill: "var(--s-red)" }} />
        <Txt x={260} y={48} anchor="start" mono color="var(--s-accent)" size={11}>(7, 3)</Txt>
        <Txt x={260} y={108} anchor="start" mono color="var(--s-red)" size={11}>(3, 7)</Txt>
        <Txt x={145} y={152}>долгота →</Txt>
      </G>

      {/* шаг 3: код */}
      <G o={step === 3 ? 1 : 0}>
        <rect x="60" y="30" width="240" height="80" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="76" y="56" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>point = (55.7, 37.6)</text>
        <text x="76" y="78" className="a-mono" style={{ fontSize: 12 }}>lat, lon = point</text>
        <text x="76" y="98" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-muted)" }}>позиция 0 — широта, 1 — долгота</text>
      </G>
    </Steps>
  );
}
