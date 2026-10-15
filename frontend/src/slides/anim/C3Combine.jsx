import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 8: сочетания C(n, k) — порядок не важен. Шесть порядков
   сливаются в один, формула A/k!, колода, ревьюеры, связь с размещениями. */

const LABELS = ["Без порядка", "A / k!", "Колода", "Ревьюеры", "Связь"];
const CAPTION = [
  "Если порядок не важен — считаем сочетания: шесть порядков одной тройки неотличимы",
  "Сочетание — размещение, делённое на k!: делим на все перестановки внутри группы",
  "Пять карт из пятидесяти двух — C(52, 5), около 2,6 миллиона рук",
  "Двое ревьюеров из шести — C(6, 2) = 15 вариантов",
  "Выборка с порядком и без отличается ровно в k! раз",
];
const ORD = ["abc", "acb", "bac", "bca", "cab", "cba"];
const PAIRS = [];
for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) PAIRS.push([i, j]);

export default function C3Combine({ cues }) {
  const ctl = useSteps(cues || [6.2, 17.1, 22.7, 27.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {ORD.map((o, i) => (
          <Pill
            key={o}
            x={step === 0 ? 70 + (i % 3) * 56 : 128}
            y={step === 0 ? 40 + Math.floor(i / 3) * 34 : 56}
            w={48}
            text={o}
            stroke="var(--s-muted)"
            o={step === 0 ? 1 : 0}
          />
        ))}
        <Pill x={270} y={56} w={90} text="{a, b, c}" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" />
        <Txt x="226" y="60" mono size={16} color="var(--s-accent)">→</Txt>
        <Txt x="180" y="130" mono size={13} color="var(--s-accent)">6 порядков = 1 сочетание</Txt>
      </G>

      <G o={step === 1 ? 1 : 0}>
        <Txt x="180" y="28" mono size={13}>C(n, k) = A(n, k) / k!</Txt>
        <Pill x={70} y={76} w={80} text="A = 60" stroke="var(--s-amber)" size={14} />
        <Txt x="130" y="80" mono size={16} color="var(--s-accent)">÷</Txt>
        <Pill x={190} y={76} w={80} text="3! = 6" stroke="var(--s-blue)" size={14} />
        <Txt x="248" y="80" mono size={16} color="var(--s-accent)">=</Txt>
        <Pill x={310} y={76} w={80} text="C = 10" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={14} />
        <Txt x="180" y="130">C(5, 3): выбрать трёх из пяти</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {Array.from({ length: 52 }, (_, i) => (
          <rect
            key={i}
            className="a-t"
            x={14 + (i % 13) * 25}
            y={28 + Math.floor(i / 13) * 24}
            width="20"
            height="18"
            rx="3"
            style={{ fill: [3, 14, 22, 38, 47].includes(i) ? "var(--s-accent)" : "var(--s-panel2)", fillOpacity: [3, 14, 22, 38, 47].includes(i) ? 0.5 : 1, stroke: [3, 14, 22, 38, 47].includes(i) ? "var(--s-accent)" : "var(--s-border)" }}
          />
        ))}
        <Txt x="180" y="140" mono size={16} color="var(--s-accent)">C(52, 5) = 2 598 960</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        {Array.from({ length: 6 }, (_, i) => (
          <Dot key={i} x={40 + i * 50} y={34} text={"ABCDEF"[i]} stroke="var(--s-blue)" />
        ))}
        {PAIRS.map(([a, b], i) => (
          <Pill key={i} x={34 + (i % 5) * 66} y={74 + Math.floor(i / 5) * 24} w={56} text={`${"ABCDEF"[a]}${"ABCDEF"[b]}`} stroke="var(--s-accent)" size={9.5} />
        ))}
        <Txt x="180" y="160" mono size={12} color="var(--s-accent)">C(6, 2) = 15</Txt>
      </G>

      <G o={step >= 4 ? 1 : 0}>
        <rect x="30" y="38" width="64" height="40" rx="8" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
        <text x="62" y="62" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>C</text>
        <Txt x="118" y="62" mono size={16} color="var(--s-amber)">· k!</Txt>
        <Txt x="160" y="62" mono size={16}>=</Txt>
        <rect x="190" y="38" width="140" height="40" rx="8" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
        <text x="260" y="62" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-amber)" }}>A  (с порядком)</text>
        <Txt x="180" y="118" mono size={13}>A(5,3) = C(5,3) · 3! = 10 · 6 = 60</Txt>
      </G>
    </Steps>
  );
}
