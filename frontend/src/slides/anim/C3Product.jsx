import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 3: правило произведения. Независимые выборы перемножаются:
   дерево 2×3, пин-код 10⁴, вложенные циклы. */

const LABELS = ["Правило", "Выборы", "Пин-код", "Циклы", "Умножайте"];
const CAPTION = [
  "Правило произведения заметно мощнее правила суммы",
  "Несколько независимых выборов подряд: число вариантов перемножается — 2 · 3 = 6",
  "Пин-код из четырёх цифр: на каждой позиции десять возможностей — 10⁴ = 10 000",
  "Вложенные циклы — прямое воплощение правила: итераций тела столько, сколько длина × длина",
  "Как только видите цепочку независимых выборов — умножайте",
];

export default function C3Product({ cues }) {
  const ctl = useSteps(cues || [2.7, 7.6, 15.0, 24.5], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={40} y={80} w={56} text="старт" stroke="var(--s-muted)" />
        {["М", "Ж"].map((t, i) => (
          <Pill key={t} x={130} y={50 + i * 60} w={40} text={t} stroke="var(--s-blue)" />
        ))}
        {[0, 1].map((i) =>
          [0, 1, 2].map((j) => (
            <g key={`${i}${j}`}>
              <line x1="150" y1={50 + i * 60} x2="224" y2={24 + i * 66 + j * 22} style={{ stroke: "var(--s-border)", strokeWidth: 1.2 }} />
              <Pill x={246} y={24 + i * 66 + j * 22} w={48} text={`${i + 1}${["а", "б", "в"][j]}`} stroke="var(--s-amber)" />
            </g>
          )),
        )}
        {[0, 1].map((i) => (
          <line key={i} x1="68" y1="80" x2="110" y2={50 + i * 60} style={{ stroke: "var(--s-border)", strokeWidth: 1.2 }} />
        ))}
        <Txt x="320" y="84" mono size={14} color="var(--s-accent)">2·3=6</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {[0, 1, 2, 3].map((i) => (
          <g key={i} className="a-t" style={{ transitionDelay: `${i * 220}ms` }}>
            <rect x={78 + i * 56} y="38" width="46" height="54" rx="9" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
            <text x={101 + i * 56} y="68" textAnchor="middle" className="a-mono" style={{ fontSize: 20, fill: "var(--s-accent)" }}>10</text>
            <text x={101 + i * 56} y="84" textAnchor="middle" className="a-cap">цифр</text>
          </g>
        ))}
        {[0, 1, 2].map((i) => (
          <text key={i} x={129 + i * 56} y="68" textAnchor="middle" className="a-mono" style={{ fontSize: 15, fill: "var(--s-amber)" }}>×</text>
        ))}
        <Txt x="180" y="130" mono size={18} color="var(--s-accent)">10⁴ = 10 000</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        <text x="30" y="30" className="a-mono" style={{ fontSize: 11 }}>for a in A:</text>
        <text x="46" y="46" className="a-mono" style={{ fontSize: 11 }}>for b in B:</text>
        <text x="62" y="62" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>body(a, b)</text>
        {[0, 1, 2].map((r) =>
          [0, 1, 2, 3].map((c) => (
            <rect
              key={`${r}${c}`}
              className="a-t"
              x={186 + c * 32}
              y={30 + r * 32}
              width="26"
              height="26"
              rx="5"
              style={{
                fill: "var(--s-green)",
                stroke: "var(--s-accent)",
                strokeWidth: 1.3,
                opacity: step === 3 ? 1 : 0,
                transitionDelay: `${(r * 4 + c) * 90}ms`,
              }}
            />
          )),
        )}
        <Txt x="250" y="22" mono size={10}>B →</Txt>
        <Txt x="170" y="64" mono size={10}>A ↓</Txt>
        <Txt x="180" y="150" mono size={13} color="var(--s-accent)">итераций: 3 · 4 = 12</Txt>
      </G>

      <G o={step >= 4 ? 1 : 0}>
        <text x="180" y="86" textAnchor="middle" className="a-mono" style={{ fontSize: 56, fill: "var(--s-accent)" }}>×</text>
        <Txt x="180" y="126">независимые выборы → умножаем</Txt>
      </G>
    </Steps>
  );
}
