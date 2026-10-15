import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 5: факториал. 4! по шагам, рост 5!…20!, n! обгоняет 2ⁿ. */

const LABELS = ["Определение", "4!", "Рост", "Против 2ⁿ"];
const CAPTION = [
  "Для подсчёта порядков нужна своя единица — факториал",
  "n! — произведение всех чисел от 1 до n: 4! = 4 · 3 · 2 · 1 = 24",
  "Растёт пугающе: 10! — больше трёх с половиной миллионов, 20! — за квинтиллион",
  "n! догоняет и обгоняет экспоненту уже на скромных числах — и железо не спасёт",
];
const BARS = [
  [5, "120", 2.08],
  [10, "3,6 · 10⁶", 6.56],
  [15, "1,3 · 10¹²", 12.12],
  [20, "2,4 · 10¹⁸", 18.39],
];
const fact = (n) => Array.from({ length: n }, (_, i) => i + 1).reduce((a, b) => a * b, 1);
const curve = (f) =>
  "M" +
  Array.from({ length: 15 }, (_, i) => i + 1)
    .map((n) => `${40 + n * 19} ${140 - Math.log10(f(n)) * 9}`)
    .join(" L");

export default function C3Factorial({ cues }) {
  const ctl = useSteps(cues || [4.4, 10.1, 17.5], 3000);
  const { step } = ctl;
  const draw = step >= 3;
  const run = [4, 12, 24, 24];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">n! = 1 · 2 · … · n</Txt>

      <G o={step === 1 ? 1 : 0}>
        {[4, 3, 2, 1].map((v, i) => (
          <g key={v} className="a-t" style={{ opacity: step === 1 ? 1 : 0, transitionDelay: `${i * 300}ms` }}>
            <Pill x={56 + i * 76} y={50} w={44} text={v} stroke="var(--s-blue)" size={14} />
            <Txt x={56 + i * 76} y={92} mono size={13} color="var(--s-accent)">{run[i]}</Txt>
            {i < 3 && <text x={94 + i * 76} y="54" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-amber)" }}>×</text>}
          </g>
        ))}
        <Txt x="180" y="126" mono size={16} color="var(--s-accent)">4! = 24</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {BARS.map(([n, t, lg], i) => (
          <g key={n}>
            <text x="40" y={46 + i * 30} textAnchor="end" className="a-mono" style={{ fontSize: 11 }}>{n}!</text>
            <rect className="a-t" x="48" y={34 + i * 30} width={step === 2 ? lg * 12 + 6 : 0} height="18" rx="4" style={{ fill: "var(--s-amber)", fillOpacity: 0.35, stroke: "var(--s-amber)", transitionDelay: `${i * 150}ms` }} />
            <text x={48 + lg * 12 + 12} y={47 + i * 30} className="a-mono" style={{ fontSize: 10, fill: "var(--s-text)", opacity: step === 2 ? 1 : 0 }}>{t}</text>
          </g>
        ))}
      </G>

      <G o={step >= 3 ? 1 : 0}>
        <line x1="40" y1="140" x2="332" y2="140" style={{ stroke: "var(--s-border)" }} />
        <line x1="40" y1="20" x2="40" y2="140" style={{ stroke: "var(--s-border)" }} />
        <path d={curve((n) => 2 ** n)} pathLength="1" className="a-t" style={{ fill: "none", stroke: "var(--s-blue)", strokeWidth: 2.2, strokeDasharray: 1, strokeDashoffset: draw ? 0 : 1, transition: "stroke-dashoffset 2.2s ease" }} />
        <path d={curve(fact)} pathLength="1" className="a-t" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 2.2, strokeDasharray: 1, strokeDashoffset: draw ? 0 : 1, transition: "stroke-dashoffset 2.2s ease 0.4s" }} />
        <Txt x="300" y="48" anchor="end" mono size={11} color="var(--s-amber)">n!</Txt>
        <Txt x="300" y="104" anchor="end" mono size={11} color="var(--s-blue)">2ⁿ</Txt>
        <Txt x="186" y="156" size={9}>n = 1 … 15, по вертикали порядок числа (логарифм)</Txt>
      </G>
    </Steps>
  );
}
