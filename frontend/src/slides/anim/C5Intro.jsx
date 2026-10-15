import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 5, слайд 1: логика высказываний — то, что вы делаете в каждом
   if; инверсии, приоритет, «внезапно зелёный тест»; конструктор. */

const LABELS = ["Глава", "Условие", "Проблемы", "Конструктор"];
const CAPTION = [
  "Логика высказываний: открывает логическую часть курса",
  "Каждый раз, когда вы пишете условие в операторе if, вы занимаетесь логикой высказываний",
  "Запутанная инверсия, спор о приоритете «и» и «или», внезапно зелёный тест — территория главы",
  "Булевы выражения разбираем как конструктор, а не как заклинание",
];

export default function C5Intro({ cues }) {
  const ctl = useSteps(cues || [2.7, 11.0, 19.6], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        <rect x="50" y="36" width="260" height="70" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="70" y="64" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>if (a &amp;&amp; !b) {"{"}</text>
        <text x="90" y="88" className="a-mono" style={{ fontSize: 12 }}>…</text>
        <text x="70" y="102" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>{"}"}</text>
        <Txt x="180" y="132" size={10}>это уже формула логики высказываний</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[
          ["!(!a || !b)", "запутанная инверсия", "var(--s-red)"],
          ["a || b && c", "а какой приоритет?", "var(--s-amber)"],
          ["✓ ✓ ✓ …", "внезапно зелёный тест", "var(--s-blue)"],
        ].map(([f, t, c], i) => (
          <g key={t}>
            <rect x="40" y={26 + i * 44} width="280" height="36" rx="10" style={{ fill: "var(--s-panel2)", stroke: c, strokeWidth: 1.4 }} />
            <text x="58" y={49 + i * 44} className="a-mono" style={{ fontSize: 12 }}>{f}</text>
            <text x="304" y={49 + i * 44} textAnchor="end" className="a-cap" style={{ fill: c }}>{t}</text>
          </g>
        ))}
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {["a", "b", "c"].map((t, i) => (
          <Pill key={t} x={60 + i * 80} y={34} w={44} text={t} stroke="var(--s-blue)" />
        ))}
        {["¬", "∧", "∨"].map((t, i) => (
          <Pill key={t} x={100 + i * 80} y={86} w={36} text={t} stroke="var(--s-amber)" size={14} />
        ))}
        <Pill x={180} y={134} w={190} text="¬a ∧ (b ∨ c)" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x="296" y="38" size={9.5}>атомы</Txt>
        <Txt x="296" y="90" size={9.5}>операции</Txt>
        <Txt x="296" y="138" size={9.5}>формула</Txt>
      </G>
    </Steps>
  );
}
