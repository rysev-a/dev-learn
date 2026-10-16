import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 5: интуиция через Гаусса — суммы по столбикам
   парами дают 101; догадка против доказательства. */

const LABELS = ["Интуиция", "Два ряда", "Столбики", "Гаусс", "Догадка и доказательство"];
const CAPTION = [
  "Если переход показался фокусом — вот интуиция одной картинкой",
  "Сумма 1…100 и под ней та же сумма в обратном порядке: 100 + 99 + … + 1",
  "Каждый столбик даёт 101, столбиков 100: две копии — 100 · 101, одна — половина",
  "По легенде, так в уме школьник Гаусс обошёл задание учителя сложить числа до ста",
  "Догадка говорит «похоже, что так»; индукция — «так и есть, для всех»; вместе они делают математику надёжной",
];
const COLS = [1, 2, 3, 4, 5, 6];

export default function C7Gauss({ cues }) {
  const ctl = useSteps(cues || [4.2, 11.1, 19.6, 25.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">1 + 2 + … + 100 = ?</Txt>
      <G o={step >= 1 && step <= 2 ? 1 : 0}>
        {COLS.map((v, i) => (
          <g key={v}>
            <rect x={40 + i * 42} y="36" width="36" height="24" rx="5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.4 }} />
            <text x={58 + i * 42} y="52" textAnchor="middle" className="a-mono" style={{ fontSize: 11 }}>{v}</text>
            <rect className="a-t" x={40 + i * 42} y="70" width="36" height="24" rx="5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.4, opacity: step >= 1 ? 1 : 0, transitionDelay: `${i * 100}ms` }} />
            <text x={58 + i * 42} y="86" textAnchor="middle" className="a-mono a-t" style={{ fontSize: 11, opacity: step >= 1 ? 1 : 0 }}>{["100", "99", "98", "97", "96", "95"][i]}</text>
            <text x={58 + i * 42} y="116" textAnchor="middle" className="a-mono a-t" style={{ fontSize: 12, fill: "var(--s-accent)", opacity: step === 2 ? 1 : 0, transitionDelay: `${i * 140}ms` }}>101</text>
          </g>
        ))}
        <text x="300" y="52" className="a-mono" style={{ fontSize: 14, fill: "var(--s-muted)" }}>…</text>
        <text x="300" y="86" className="a-mono" style={{ fontSize: 14, fill: "var(--s-muted)" }}>…</text>
        <Txt x="180" y="148" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-accent)">100 · 101 / 2 = 5050</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x="180" y="70" mono size={30} color="var(--s-accent)">5050</Txt>
        <Txt x="180" y="108" size={10.5}>в уме, пока класс складывал по одному</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="30" y="40" width="130" height="64" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
        <Txt x="95" y="68" size={11}>догадка</Txt>
        <Txt x="95" y="88" size={10} color="var(--s-amber)">«похоже, что так»</Txt>
        <Txt x="180" y="76" mono size={18} color="var(--s-accent)">+</Txt>
        <rect x="200" y="40" width="130" height="64" rx="12" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
        <Txt x="265" y="68" size={11}>индукция</Txt>
        <Txt x="265" y="88" size={10} color="var(--s-accent)">«так и есть, для всех»</Txt>
      </G>
    </Steps>
  );
}
