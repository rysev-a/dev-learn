import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 4, слайд 8: включения и исключения для трёх множеств — задача про
   языки: 55 + 45 + 25 − 18 − 12 − 8 + 5 = 92, вне всех — 8. */

const LABELS = ["+ − +", "Формула", "Данные", "Счёт", "Ответ"];
const CAPTION = [
  "С тремя множествами начинается пульсация: прибавить, отнять, прибавить",
  "Сумма мощностей, минус попарные пересечения, плюс пересечение всех трёх",
  "Из ста человек: английский — 55, немецкий — 45, французский — 25; пары 18, 12, 8; все три — 5",
  "55 + 45 + 25 − 18 − 12 − 8 + 5 = 92",
  "Значит, восемь человек не знают ни одного языка — без единого перебора",
];
const C = [
  [140, 70, "var(--s-blue)", "EN"],
  [200, 70, "var(--s-amber)", "DE"],
  [170, 112, "var(--s-accent)", "FR"],
];
const REG = [
  [118, 58, "30"],
  [222, 58, "24"],
  [170, 138, "10"],
  [170, 52, "13"],
  [146, 100, "7"],
  [194, 100, "3"],
  [170, 84, "5"],
];
const RUN = [
  ["55", 55],
  ["+45", 100],
  ["+25", 125],
  ["−18", 107],
  ["−12", 95],
  ["−8", 87],
  ["+5", 92],
];

export default function C4Incl3({ cues }) {
  const ctl = useSteps(cues || [5.0, 11.8, 26.1, 34.8], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        <Txt x="180" y="50" mono size={13} o={step === 0 ? 1 : 0} color="var(--s-accent)">+  −  +  −  …</Txt>
        <Txt x="180" y="56" mono size={11} o={step === 1 ? 1 : 0}>|A∪B∪C| = |A|+|B|+|C|</Txt>
        <Txt x="180" y="76" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-red)">− |A∩B| − |A∩C| − |B∩C|</Txt>
        <Txt x="180" y="96" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">+ |A∩B∩C|</Txt>
      </G>
      <G o={step >= 2 ? 1 : 0}>
        <rect x="70" y="12" width="220" height="146" rx="10" className="a-ring" style={{ stroke: "var(--s-border)" }} />
        {C.map(([x, y, c, l]) => (
          <g key={l}>
            <circle cx={x} cy={y} r="42" className="a-ring" style={{ stroke: c }} />
          </g>
        ))}
        {REG.map(([x, y, t], i) => (
          <text key={i} x={x} y={y + 3.6} textAnchor="middle" className="a-mono" style={{ fontSize: 11.5, fill: i === 6 ? "var(--s-accent)" : "var(--s-text)" }}>{t}</text>
        ))}
        <Txt x="100" y="38" size={10} color="var(--s-blue)">EN 55</Txt>
        <Txt x="260" y="38" size={10} color="var(--s-amber)">DE 45</Txt>
        <Txt x="260" y="148" size={10} color="var(--s-accent)">FR 25</Txt>
        <Txt x="92" y="150" mono size={10} o={step >= 4 ? 1 : 0} color="var(--s-red)">8</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {RUN.map(([t, v], i) => (
          <g key={i} className="a-t" style={{ opacity: step === 3 ? 1 : 0, transitionDelay: `${i * 220}ms` }}>
            <text x={308} y={26 + i * 20} textAnchor="start" className="a-mono" style={{ fontSize: 10, fill: t.startsWith("−") ? "var(--s-red)" : "var(--s-accent)" }}>{t}</text>
            <text x={348} y={26 + i * 20} textAnchor="end" className="a-mono" style={{ fontSize: 10 }}>{v}</text>
          </g>
        ))}
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x="320" y="70" mono size={11}>100 − 92</Txt>
        <Txt x="320" y="92" mono size={20} color="var(--s-red)">= 8</Txt>
        <Txt x="320" y="110" size={9.5}>ни одного языка</Txt>
      </G>
    </Steps>
  );
}
