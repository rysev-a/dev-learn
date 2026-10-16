import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 3: комбинаторика — хозяйка: пять монет, пятёрка из
   двадцати, парадокс дней рождения. */

const LABELS = ["Хозяйка", "Пять монет", "Пятёрка", "Дни рождения", "Мораль"];
const CAPTION = [
  "Комбинаторика здесь не гость, а хозяйка",
  "Бросаем пять монет: всех исходов 2⁵ = 32 — каждая монета удваивает варианты",
  "Выбор стартовой пятёрки из двадцати — C(20, 5) = 15 504; без формулы считали бы до вечера",
  "Парадокс дней рождения: в комнате из 23 человек вероятность совпадения больше 50 %, ведь пар почти 250",
  "Интуиция про случайность ненадёжна, а формулы подсчёта надёжны",
];

export default function C10Counting({ cues }) {
  const ctl = useSteps(cues || [2.9, 9.0, 17.1, 28.4], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">считать, чтобы вероятность знать</Txt>
      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 32 }, (_, i) => (
          <rect key={i} className="a-t" x={34 + (i % 8) * 38} y={22 + Math.floor(i / 8) * 28} width="32" height="22" rx="4" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.2, opacity: step === 1 ? 1 : 0, transitionDelay: `${i * 30}ms` }} />
        ))}
        {Array.from({ length: 32 }, (_, i) => (
          <text key={`t${i}`} x={50 + (i % 8) * 38} y={37 + Math.floor(i / 8) * 28} textAnchor="middle" className="a-mono" style={{ fontSize: 8, fill: "var(--s-muted)" }}>
            {[4, 3, 2, 1, 0].map((b) => ((i >> b) & 1 ? "Р" : "О")).join("")}
          </text>
        ))}
        <Txt x="180" y="148" mono size={13} color="var(--s-accent)">2 · 2 · 2 · 2 · 2 = 32</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {Array.from({ length: 20 }, (_, i) => (
          <circle key={i} cx={30 + (i % 10) * 33} cy={44 + Math.floor(i / 10) * 32} r="11" style={{ fill: i % 4 === 1 && i < 18 ? "var(--s-green)" : "var(--s-panel2)", stroke: i % 4 === 1 && i < 18 ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.5 }} />
        ))}
        <Txt x="180" y="130" mono size={14} color="var(--s-accent)">C(20, 5) = 15 504</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {Array.from({ length: 23 }, (_, i) => (
          <circle key={i} cx={180 + 56 * Math.cos((2 * Math.PI * i) / 23 - Math.PI / 2)} cy={80 + 56 * Math.sin((2 * Math.PI * i) / 23 - Math.PI / 2)} r="4.5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.6 }} />
        ))}
        <Txt x="180" y="76" mono size={12}>23 человека</Txt>
        <Txt x="180" y="94" mono size={13} color="var(--s-accent)">253 пары</Txt>
        <Txt x="296" y="80" mono size={14} color="var(--s-amber)">P &gt; 50 %</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x="110" y="76" mono size={14} color="var(--s-red)">интуиция ✗</Txt>
        <Txt x="250" y="76" mono size={14} color="var(--s-accent)">формулы ✓</Txt>
      </G>
    </Steps>
  );
}
