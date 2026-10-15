import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 10, слайд 2: классическая вероятность — доля благоприятных исходов
   среди равновозможных; кость и монета. */

const LABELS = ["Классическая", "Доля", "Кость", "Монета", "Много исходов"];
const CAPTION = [
  "Классическое определение почти наивное",
  "Если все исходы равновозможны, вероятность события — доля благоприятных исходов среди всех",
  "У кости 6 граней: вероятность чётного — 3 из 6, то есть 1/2",
  "У монеты два исхода: вероятность решки — 1/2",
  "Когда исходов много, считать доли без правил подсчёта из первых глав не получится",
];

export default function C10Classic({ cues }) {
  const ctl = useSteps(cues || [3.8, 9.4, 15.5, 19.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">P(A) = |A| / |Ω|</Txt>
      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 12 }, (_, i) => (
          <rect key={i} x={50 + (i % 6) * 44} y={30 + Math.floor(i / 6) * 40} width="36" height="32" rx="6" style={{ fill: i < 4 ? "var(--s-green)" : "var(--s-panel2)", stroke: i < 4 ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.5 }} />
        ))}
        <Txt x="180" y="130" mono size={14} color="var(--s-accent)">благоприятных 4 из 12  →  1/3</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[1, 2, 3, 4, 5, 6].map((v, i) => (
          <g key={v}>
            <rect x={36 + i * 47} y="40" width="38" height="38" rx="8" style={{ fill: v % 2 === 0 ? "var(--s-green)" : "var(--s-panel2)", stroke: v % 2 === 0 ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.6 }} />
            <text x={55 + i * 47} y="65" textAnchor="middle" className="a-mono" style={{ fontSize: 15 }}>{v}</text>
          </g>
        ))}
        <Txt x="180" y="116" mono size={14} color="var(--s-accent)">чётное: 3 из 6 = 1/2</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <circle cx="120" cy="70" r="30" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 2 }} />
        <Txt x="120" y="76" mono size={18} color="var(--s-amber)">О</Txt>
        <circle cx="240" cy="70" r="30" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 2 }} />
        <Txt x="240" y="76" mono size={18} color="var(--s-accent)">Р</Txt>
        <Txt x="180" y="130" mono size={14} color="var(--s-accent)">решка: 1 из 2 = 1/2</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={110} y={64} w={160} h={44} text="C(52, 5) исходов" stroke="var(--s-amber)" size={12} />
        <Txt x="196" y="68" mono size={16} color="var(--s-accent)">⇒</Txt>
        <Pill x={270} y={64} w={140} h={44} text="правила подсчёта" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
      </G>
    </Steps>
  );
}
