import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 7: индукция и рекурсия — близнецы; база, вызов как
   переход, корректность «по построению», потеря базы и stack overflow. */

const LABELS = ["Близнецы", "База", "Вызов", "Корректность", "Без базы", "Стек"];
const CAPTION = [
  "Индукция и рекурсия — близнецы",
  "База рекурсии — это база индукции: случай, решаемый без рекурсивного вызова",
  "Рекурсивный вызов — это переход: решаем меньшую задачу, предполагая, что её решение корректно",
  "Если решение оформлено по этим правилам, корректность следует из индукции автоматически",
  "Нет базы или она недостижима — ломается первая ступень, и рушится вся лестница",
  "Переполнение стека — это индукция без базы, спускающаяся в вечность",
];

export default function C7Recursion({ cues }) {
  const ctl = useSteps(cues || [5.3, 9.9, 16.3, 23.2, 30.5], 3000);
  const { step } = ctl;
  const rows = [
    ["база индукции", "return 1  (n = 0)", step >= 1],
    ["переход", "n * fact(n − 1)", step >= 2],
    ["доказательство", "корректно «по построению»", step >= 3],
  ];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 3 ? 1 : 0}>
        <Txt x="95" y="22" size={10} color="var(--s-blue)">индукция</Txt>
        <Txt x="265" y="22" size={10} color="var(--s-accent)">рекурсия</Txt>
        {rows.map(([a, b, on], i) => (
          <g key={a} className="a-t" style={{ opacity: on ? 1 : 0.25 }}>
            <Pill x={95} y={50 + i * 40} w={150} h={28} text={a} stroke="var(--s-blue)" size={10} />
            <Txt x="180" y={54 + i * 40} mono size={14} color="var(--s-accent)">≈</Txt>
            <Pill x={265} y={50 + i * 40} w={150} h={28} text={b} stroke="var(--s-accent)" size={9.5} />
          </g>
        ))}
        <Txt x="180" y="160" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">отдельно доказывать нечего</Txt>
      </G>
      <G o={step === 4 ? 1 : 0}>
        {Array.from({ length: 6 }, (_, i) => (
          <rect key={i} x={50 + i * 44} y={110 - i * 10 + (i === 0 ? 24 : 0)} width="40" height={30 + i * 10 - (i === 0 ? 24 : 0)} rx="3" style={{ fill: i === 0 ? "none" : "var(--s-panel2)", stroke: i === 0 ? "var(--s-red)" : "var(--s-border)", strokeDasharray: i === 0 ? "4 3" : "none", strokeWidth: 1.5 }} />
        ))}
        <Txt x="70" y="104" mono size={11} color="var(--s-red)">база?</Txt>
        <Txt x="180" y="154" size={10} color="var(--s-red)">нет первой ступени — не на что опереться</Txt>
      </G>
      <G o={step >= 5 ? 1 : 0}>
        {Array.from({ length: 6 }, (_, i) => (
          <g key={i} className="a-t" style={{ opacity: step >= 5 ? 1 : 0, transitionDelay: `${i * 200}ms` }}>
            <rect x={110} y={22 + i * 22} width="140" height="19" rx="4" style={{ fill: "var(--s-panel2)", stroke: i === 5 ? "var(--s-red)" : "var(--s-border)", strokeWidth: i === 5 ? 2 : 1.2 }} />
            <text x="180" y={36 + i * 22} textAnchor="middle" className="a-mono" style={{ fontSize: 10, fill: i === 5 ? "var(--s-red)" : "var(--s-text)" }}>{i === 5 ? "StackOverflow" : `f(n − ${i})`}</text>
          </g>
        ))}
        <Txt x="180" y="158" size={10}>стек вызовов растёт и не кончается</Txt>
      </G>
    </Steps>
  );
}
