import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 9: спам-фильтр по Байесу — априорная, слово-свидетельство,
   слово за словом уверенность растёт. */

const LABELS = ["Спам", "Априори", "Слово", "Байес", "Слово за словом"];
const CAPTION = [
  "Тот же механизм крутит спам-фильтры, с которыми живёт вся почта",
  "Априорная вероятность спама — опыт прошлой почты, скажем каждое третье письмо",
  "Слово «бесплатно» — свидетельство: среди спама оно встречается несравнимо чаще, чем среди нормальных писем",
  "Байес перемножает априорную уверенность с характерностью слова и выдаёт обновлённую оценку",
  "Фильтр не «знает», что перед ним спам, — он обновляет уверенность слово за словом",
];
const WORDS = [
  ["письмо", 33],
  ["бесплатно", 91],
  ["выиграли", 99],
  ["срочно", 99.6],
];

export default function C10Spam({ cues }) {
  const ctl = useSteps(cues || [3.9, 8.8, 15.8, 26.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={24} o={step === 0 ? 1 : 0} color="var(--s-amber)">✉ спам или нет?</Txt>
      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 12 }, (_, i) => (
          <rect key={i} x={36 + (i % 6) * 48} y={28 + Math.floor(i / 6) * 38} width="38" height="28" rx="5" style={{ fill: i % 3 === 0 ? "var(--s-red)" : "var(--s-panel2)", fillOpacity: i % 3 === 0 ? 0.4 : 1, stroke: i % 3 === 0 ? "var(--s-red)" : "var(--s-border)", strokeWidth: 1.4 }} />
        ))}
        <Txt x="180" y="134" mono size={13} color="var(--s-amber)">P(спам) = 1/3</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={180} y={34} w={150} h={30} text="«бесплатно»" stroke="var(--s-amber)" size={13} />
        {[
          ["в спаме", 40, "var(--s-red)"],
          ["в нормальных", 2, "var(--s-accent)"],
        ].map(([t, v, c], i) => (
          <g key={t}>
            <text x="40" y={92 + i * 32} className="a-cap" style={{ fontSize: 10, fill: "var(--s-text)" }}>{t}</text>
            <rect className="a-t" x="130" y={78 + i * 32} width={step === 2 ? v * 4.5 : 0} height="20" rx="4" style={{ fill: c, fillOpacity: 0.35, stroke: c }} />
            <text x={138 + v * 4.5} y={92 + i * 32} className="a-mono" style={{ fontSize: 10.5, fill: c }}>{`${v} % писем`}</text>
          </g>
        ))}
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={70} y={60} w={100} h={40} text="априори 33 %" stroke="var(--s-blue)" size={10.5} />
        <Txt x="132" y="64" mono size={16}>×</Txt>
        <Pill x={190} y={60} w={100} h={40} text="«бесплатно»" stroke="var(--s-amber)" size={10.5} />
        <Txt x="250" y="64" mono size={16}>⇒</Txt>
        <Pill x={310} y={60} w={80} h={40} text="91 %" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={14} />
        <Txt x="180" y="130" size={10}>иллюстративные числа: 40 % против 2 %</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {WORDS.map(([w, v], i) => (
          <g key={w} className="a-t" style={{ opacity: step >= 4 ? 1 : 0, transitionDelay: `${i * 380}ms` }}>
            <text x="36" y={42 + i * 30} className="a-mono" style={{ fontSize: 11 }}>{w}</text>
            <rect x="130" y={28 + i * 30} width={v * 1.9} height="20" rx="4" style={{ fill: "var(--s-red)", fillOpacity: 0.35, stroke: "var(--s-red)" }} />
            <text x={136 + v * 1.9} y={42 + i * 30} className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-red)" }}>{`${v} %`}</text>
          </g>
        ))}
        <Txt x="180" y="150" size={10}>слово за словом — уверенность растёт</Txt>
      </G>
    </Steps>
  );
}
