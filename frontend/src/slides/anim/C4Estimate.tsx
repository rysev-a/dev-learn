import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";
import { binom } from "./tri.ts";

/* Глава 4, слайд 6: быстрые прикидки по биному: (1 + x)ⁿ — доминируют
   первые члены; сложный процент, нагрузка; отбросить хвост. */

const LABELS = ["Прикидка", "(1,01)¹⁰⁰", "Где нужно", "Навык", "Суть"];
const CAPTION = [
  "Практическая сила бинома — быстрые прикидки без калькулятора",
  "(1 + 0,01)¹⁰⁰ — главную роль играет член, где малое число в первой степени",
  "Так оценивают сложный процент, рост нагрузки при небольшом ежедневном ухудшении, анализ алгоритмов",
  "Общий навык: разложить по биному, увидеть доминирующие члены, отбросить хвост",
  "Честные упрощения оставляют суть и убирают шум",
];
const x = 0.01;
const n = 100;
const TERMS = [0, 1, 2, 3, 4, 5].map((k) => binom(n, k) * x ** k);
const tot = TERMS.reduce((a, b) => a + b, 0);

export default function C4Estimate({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.9, 13.0, 20.1, 26.2], 3000);
  const { step } = ctl;
  const bars = step === 1 || step >= 3;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={86} mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">(1 + x)ⁿ ≈ 1 + n·x</Txt>
      <G o={bars ? 1 : 0}>
        <Txt x={180} y={18} mono size={11}>(1 + 0,01)¹⁰⁰ = 1 + 1 + 0,495 + 0,162 + …</Txt>
        {TERMS.map((v, k) => (
          <g key={k}>
            <text x="40" y={44 + k * 17} textAnchor="end" className="a-mono" style={{ fontSize: 9.5 }}>
              {["1", "100·x", "C₂·x²", "C₃·x³", "C₄·x⁴", "C₅·x⁵"][k]}
            </text>
            <rect className="a-t" x="48" y={34 + k * 17} width={bars ? v * 90 + 2 : 0} height="12" rx="3" style={{ fill: k < 2 ? "var(--s-accent)" : "var(--s-muted)", fillOpacity: step >= 3 && k >= 3 ? 0.12 : 0.45, stroke: k < 2 ? "var(--s-accent)" : "var(--s-muted)", strokeOpacity: step >= 3 && k >= 3 ? 0.25 : 1, transitionDelay: `${k * 120}ms` }} />
            <text x={48 + v * 90 + 8} y={44 + k * 17} className="a-mono a-t" style={{ fontSize: 9, fill: "var(--s-text)", opacity: step >= 3 && k >= 3 ? 0.25 : 1 }}>{v.toFixed(3)}</text>
          </g>
        ))}
        <Txt x={180} y={150} mono size={12} color="var(--s-amber)">сумма ≈ {tot.toFixed(2)} — первые два члена дают 2,00</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[
          ["сложный процент", "1,05¹⁰ ≈ 1 + 10·0,05 + …"],
          ["нагрузка", "+1 % в день: за месяц ≈ ×1,35"],
          ["анализ алгоритмов", "(n + 1)² = n² + 2n + 1 → n²"],
        ].map(([t, f], i) => (
          <g key={t}>
            <Pill x={80} y={36 + i * 40} w={128} text={t} stroke="var(--s-accent)" size={9.5} />
            <text x="160" y={40 + i * 40} className="a-mono" style={{ fontSize: 10.5 }}>{f}</text>
          </g>
        ))}
      </G>
      <Txt x={180} y={165} size={9.5} o={step >= 4 ? 1 : 0} color="var(--s-accent)">суть остаётся, шум уходит</Txt>
    </Steps>
  );
}
