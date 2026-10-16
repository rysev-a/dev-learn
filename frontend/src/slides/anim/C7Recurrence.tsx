import { Arrow, Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 8: рекуррентные соотношения — Фибоначчи, сравнение
   с рекурсивной функцией, запись алгоритма, время работы. */

const LABELS = ["Рекуррентность", "Фибоначчи", "Как функция", "Запись алгоритма", "Время"];
const CAPTION = [
  "Рекуррентные соотношения — формулы, где каждый член выражен через предыдущие",
  "Фибоначчи: F(n) = F(n−1) + F(n−2), база задаёт первые два значения",
  "Сравните с рекурсивной функцией: база — условия выхода, формула — вызовы с меньшими аргументами",
  "Рекуррентность — математическая запись алгоритма, решающего задачу через её меньшие версии",
  "По такой формуле можно вычислить не только значения, но и время работы алгоритма",
];
const FIB = [1, 1, 2, 3, 5, 8, 13];

export default function C7Recurrence({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [6.7, 14.2, 20.2, 26.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={86} mono size={18} o={step === 0 ? 1 : 0} color="var(--s-accent)">aₙ = f(aₙ₋₁, aₙ₋₂, …)</Txt>
      <G o={step === 1 ? 1 : 0}>
        {FIB.map((v, i) => (
          <Dot key={i} x={40 + i * 46} y={76} r={16} text={v} stroke={i < 2 ? "var(--s-amber)" : "var(--s-accent)"} fill={i < 2 ? "var(--s-panel2)" : "var(--s-green)"} size={12} />
        ))}
        {FIB.slice(2).map((_, i) => (
          <g key={i}>
            <path d={`M${40 + i * 46} 60 C${40 + i * 46} 34 ${40 + (i + 2) * 46} 34 ${40 + (i + 2) * 46} 60`} markerEnd="url(#a-hd-g)" style={{ fill: "none", stroke: "var(--s-accent)", strokeWidth: 1.2, opacity: 0.6 }} />
          </g>
        ))}
        <Txt x={86} y={112} size={9.5} color="var(--s-amber)">база</Txt>
        <Txt x={180} y={140} mono size={13} color="var(--s-accent)">F(n) = F(n−1) + F(n−2)</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <rect x="30" y="26" width="300" height="86" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="50" y="52" className="a-mono" style={{ fontSize: 12, fill: "var(--s-amber)" }}>if n &lt; 2: return n</text>
        <text x="320" y="52" textAnchor="end" className="a-cap" style={{ fill: "var(--s-amber)" }}>база</text>
        <text x="50" y="80" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>return fib(n−1) + fib(n−2)</text>
        <text x="320" y="80" textAnchor="end" className="a-cap" style={{ fill: "var(--s-accent)" }}>формула</text>
        <Txt x={180} y={136} size={10}>одно и то же — в двух записях</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Dot x={70} y={76} r={26} text="n" size={18} stroke="var(--s-blue)" />
        <Arrow x1={98} y1={76} x2={152} y2={56} c="g" />
        <Arrow x1={98} y1={76} x2={152} y2={96} c="g" />
        <Dot x={180} y={50} r={20} text="n−1" size={12} stroke="var(--s-accent)" />
        <Dot x={180} y={102} r={20} text="n−2" size={12} stroke="var(--s-accent)" />
        <Txt x={290} y={76} mono size={12} color="var(--s-accent)">через меньшие</Txt>
        <Txt x={290} y={94} mono size={12} color="var(--s-accent)">версии задачи</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={180} y={50} mono size={18} color="var(--s-accent)">T(n) = T(n−1) + T(n−2) + 1</Txt>
        <Txt x={180} y={90} size={10.5}>та же формула — но уже про время работы</Txt>
        <Txt x={180} y={124} mono size={13} color="var(--s-amber)">вычислим сложность, не запуская код</Txt>
      </G>
    </Steps>
  );
}
