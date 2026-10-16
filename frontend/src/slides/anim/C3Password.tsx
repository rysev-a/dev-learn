import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 3, слайд 4: пространство паролей. 95⁸, удлинение умножает на 95,
   фраза из слов против коротких символов, время перебора. */

const LABELS = ["Пароль", "95⁸", "Длина", "Фраза", "Перебор"];
const CAPTION = [
  "Применим правило произведения к паролям",
  "Восемь символов из девяноста пяти — 95⁸, около 6,6 квадриллиона вариантов",
  "Каждый лишний символ умножает пространство на 95 — рост очень быстрый",
  "Длинный пароль из простых слов обычно сильнее короткого из «умных» символов",
  "Перебор упирается не в талант взломщика, а в размер пространства",
];
// порядки величин: длина → lg(95^n)
const LEN = [6, 8, 10, 12].map((n) => [n, n * Math.log10(95)]);

export default function C3Password({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.7, 11.1, 18.5, 27.4], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        {Array.from({ length: 8 }, (_, i) => (
          <g key={i}>
            <rect x={30 + i * 38} y="34" width="32" height="44" rx="7" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
            <text x={46 + i * 38} y="62" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>95</text>
          </g>
        ))}
        <Txt x={180} y={26} o={step === 0 ? 0 : 1}>на каждой позиции — 95 печатных знаков</Txt>
        <Txt x={180} y={116} mono size={16} o={step >= 1 ? 1 : 0} color="var(--s-amber)">95⁸ ≈ 6,6 · 10¹⁵</Txt>
        <Txt x={180} y={140} o={step >= 1 ? 1 : 0}>около шести с половиной квадриллионов</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {LEN.map(([n, lg], i) => (
          <g key={n}>
            <text x="64" y={42 + i * 28} textAnchor="end" className="a-mono" style={{ fontSize: 11 }}>{n} символов</text>
            <rect className="a-t" x="72" y={30 + i * 28} width={step === 2 ? lg! * 9 : 0} height="18" rx="4" style={{ fill: "var(--s-accent)", fillOpacity: 0.35, stroke: "var(--s-accent)", transitionDelay: `${i * 160}ms` }} />
            <text x={72 + lg! * 9 + 6} y={43 + i * 28} className="a-mono" style={{ fontSize: 10, fill: "var(--s-amber)" }}>10^{lg!.toFixed(0)}</text>
          </g>
        ))}
        <Txt x={180} y={152} size={9.5}>длина полосы — порядок числа вариантов</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <text x="40" y="44" className="a-mono" style={{ fontSize: 11 }}>6 символов: 95⁶ ≈ 7 · 10¹¹</text>
        <rect className="a-t" x="40" y="52" width={step === 3 ? 95 : 0} height="18" rx="4" style={{ fill: "var(--s-amber)", fillOpacity: 0.35, stroke: "var(--s-amber)" }} />
        <text x="40" y="100" className="a-mono" style={{ fontSize: 11 }}>4 слова из 2000: 2000⁴ ≈ 1,6 · 10¹³</text>
        <rect className="a-t" x="40" y="108" width={step === 3 ? 200 : 0} height="18" rx="4" style={{ fill: "var(--s-accent)", fillOpacity: 0.35, stroke: "var(--s-accent)", transitionDelay: "200ms" }} />
        <Txt x={250} y={86} anchor="start" color="var(--s-accent)">сильнее</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={180} y={38} mono size={11}>1 млрд проб в секунду</Txt>
        <Txt x={180} y={78} mono size={20} color="var(--s-amber)">95⁸ → ≈ 77 суток</Txt>
        <Txt x={180} y={116} mono size={20} color="var(--s-accent)">95¹² → ≈ 17 млн лет</Txt>
        <Txt x={180} y={148}>каждый символ в длине — ×95 ко времени</Txt>
      </G>
    </Steps>
  );
}
