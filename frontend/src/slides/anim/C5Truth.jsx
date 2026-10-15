import { G, Steps, Table, Txt, useSteps } from "./kit.jsx";

/* Глава 5, слайд 4: таблицы истинности — 2ⁿ строк, полный перебор. */

const LABELS = ["Таблица", "2 переменные", "3 переменные", "5 переменных"];
const CAPTION = [
  "Таблица истинности выписывает поведение формулы во всех возможных случаях",
  "Для двух переменных четыре строки: 11, 10, 01, 00",
  "Для трёх — восемь; для n переменных — 2ⁿ: булеан вернулся",
  "Полный перебор входов даёт гарантию: формула от пяти переменных проверяется 32 строками",
];
const rows = (n) => Array.from({ length: 2 ** n }, (_, i) => Array.from({ length: n }, (_, k) => (i >> (n - 1 - k)) & 1));

export default function C5Truth({ cues }) {
  const ctl = useSteps(cues || [5.1, 10.4, 18.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={18} o={step === 0 ? 1 : 0} color="var(--s-accent)">формула → все входы → все выходы</Txt>
      <Table x={150} y={34} head={["p", "q"]} rows={rows(2)} cw={34} rh={24} o={step === 1 ? 1 : 0} delay={220} rowOn={() => step === 1} />
      <Txt x="260" y="74" mono size={20} o={step === 1 ? 1 : 0} color="var(--s-amber)">2² = 4</Txt>
      <Table x={130} y={28} head={["p", "q", "r"]} rows={rows(3)} cw={32} rh={16} o={step === 2 ? 1 : 0} delay={120} rowOn={() => step === 2} />
      <Txt x="270" y="74" mono size={20} o={step === 2 ? 1 : 0} color="var(--s-amber)">2³ = 8</Txt>
      <G o={step >= 3 ? 1 : 0}>
        {Array.from({ length: 32 }, (_, i) => (
          <rect key={i} className="a-t" x={60 + (i % 8) * 30} y={22 + Math.floor(i / 8) * 26} width="24" height="20" rx="4" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.2, opacity: step >= 3 ? 1 : 0, transitionDelay: `${i * 40}ms` }} />
        ))}
        <Txt x="180" y="146" mono size={14} color="var(--s-accent)">2⁵ = 32 строки — гарантия, а не интуиция</Txt>
      </G>
    </Steps>
  );
}
