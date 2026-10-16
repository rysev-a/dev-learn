import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 3: предикаты в работе — filter, find, условие в if. */

const LABELS = ["Везде", "filter", "find", "if", "Язык"];
const CAPTION = [
  "Вы пользуетесь предикатами постоянно, просто редко произносите это слово",
  "filter принимает предикат и оставляет только те элементы, на которых он истинен",
  "find ищет первый элемент, на котором предикат становится истинным",
  "Условие внутри if — тот же предикат от переменных состояния программы",
  "Увидев в таких функциях высказывания с переменной, вы получаете язык, на котором о них можно рассуждать строго",
];
const NUMS = [3, 8, 5, 12, 7, 10, 1, 6];

export default function C6Filter({ cues }) {
  const ctl = useSteps(cues || [4.9, 9.7, 13.8, 18.3], 3000);
  const { step } = ctl;
  const arr = step === 1 || step === 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {["filter(p)", "find(p)", "if p:", "all(p)"].map((t, i) => (
          <Pill key={t} x={60 + i * 80} y={80} w={70} h={34} text={t} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
        ))}
      </G>
      <G o={arr ? 1 : 0}>
        <Txt x="180" y="22" mono size={11}>{step === 1 ? "p(x) = x чётно" : "p(x) = x > 9"}</Txt>
        {NUMS.map((v, i) => {
          const keep = step === 1 ? v % 2 === 0 : v > 9;
          const first = step === 2 && v === 12;
          return (
            <Dot
              key={i}
              x={34 + i * 41}
              y={step === 1 && keep ? 100 : 56}
              r={14}
              text={v}
              stroke={step === 1 ? (keep ? "var(--s-accent)" : "var(--s-muted)") : first ? "var(--s-accent)" : i < 3 ? "var(--s-red)" : "var(--s-muted)"}
              fill={first || (step === 1 && keep) ? "var(--s-green)" : "var(--s-panel2)"}
              o={step === 1 && !keep ? 0.3 : 1}
            />
          );
        })}
        <Txt x="180" y="148" mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">[8, 12, 10, 6]</Txt>
        <Txt x="180" y="148" mono size={12} o={step === 2 ? 1 : 0} color="var(--s-accent)">первый подходящий: 12 — дальше не смотрим</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <rect x="50" y="30" width="260" height="76" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="70" y="60" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>if balance &gt; 0:</text>
        <text x="90" y="84" className="a-mono" style={{ fontSize: 13 }}>pay()</text>
        <Txt x="180" y="132" size={10}>balance &gt; 0 — предикат от состояния</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={180} y={70} w={230} h={44} text="P(x): высказывание с переменной" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
        <Txt x="180" y="116" size={10}>можно рассуждать строго</Txt>
      </G>
    </Steps>
  );
}
