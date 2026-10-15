import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 9: числа покера — как комбинации сжимают пространство:
   2 598 960 рук → категории; неравномерность; общий приём; вероятность. */

const LABELS = ["Пространство", "Категории", "Редкость", "Приём", "Вероятность"];
const CAPTION = [
  "Числа покера показывают, как комбинации сжимают пространство исходов",
  "Рук — две с половиной миллиона, а старшинств всего десяток категорий",
  "Миллионы рук раскладываются по категориям очень неравномерно — редкость делает категорию старше",
  "Общий приём: посчитать все исходы, сгруппировать по свойству, посчитать группу",
  "Отношение размера группы к целому — вероятность: каре — около 0,024 %",
];
const CAT = [
  ["старшая карта", 1302540],
  ["пара", 1098240],
  ["две пары", 123552],
  ["тройка", 54912],
  ["стрит", 10200],
  ["флеш", 5108],
  ["фулл-хаус", 3744],
  ["каре", 624],
  ["стрит-флеш", 36],
  ["флеш-рояль", 4],
];
const fmt = (n) => n.toLocaleString("ru-RU");

export default function C3Poker({ cues }) {
  const ctl = useSteps(cues || [5.9, 11.5, 18.1, 26.3], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        <rect
          className="a-t"
          x={step === 0 ? 70 : 20}
          y={step === 0 ? 34 : 24}
          width={step === 0 ? 220 : 90}
          height={step === 0 ? 70 : 100}
          rx="12"
          style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.8 }}
        />
        <text x={step === 0 ? 180 : 65} y={step === 0 ? 74 : 70} textAnchor="middle" className="a-mono" style={{ fontSize: step === 0 ? 20 : 11, fill: "var(--s-accent)" }}>
          {step === 0 ? "2 598 960 рук" : "2 598 960"}
        </text>
        {CAT.map(([n], i) => (
          <Pill key={n} x={170 + (i % 2) * 90 + 30} y={34 + Math.floor(i / 2) * 22} w={84} h={18} text={n} o={step === 1 ? 1 : 0} stroke="var(--s-amber)" size={8.5} />
        ))}
        <Txt x="180" y="152" o={step === 1 ? 1 : 0} mono size={12} color="var(--s-accent)">10 категорий</Txt>
        <Txt x="180" y="132" o={step === 0 ? 1 : 0}>C(52, 5) — все возможные руки</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {CAT.map(([n, v], i) => {
          const w = Math.log10(v) * 32;
          return (
            <g key={n}>
              <text x="100" y={24 + i * 14} textAnchor="end" className="a-cap" style={{ fontSize: 8.5 }}>{n}</text>
              <rect className="a-t" x="104" y={15 + i * 14} width={step === 2 ? w : 0} height="10" rx="3" style={{ fill: i > 6 ? "var(--s-red)" : "var(--s-amber)", fillOpacity: 0.45, stroke: i > 6 ? "var(--s-red)" : "var(--s-amber)", transitionDelay: `${i * 90}ms` }} />
              <text x={104 + w + 5} y={24 + i * 14} className="a-mono" style={{ fontSize: 8, fill: "var(--s-text)", opacity: step === 2 ? 1 : 0 }}>{fmt(v)}</text>
            </g>
          );
        })}
      </G>

      <G o={step === 3 ? 1 : 0}>
        {[
          ["1", "все исходы"],
          ["2", "группировка по свойству"],
          ["3", "размер группы"],
        ].map(([n, t], i) => (
          <g key={n}>
            <rect x={20 + i * 114} y="50" width="104" height="52" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.4 }} />
            <text x={72 + i * 114} y="72" textAnchor="middle" className="a-mono" style={{ fontSize: 16, fill: "var(--s-accent)" }}>{n}</text>
            <text x={72 + i * 114} y="90" textAnchor="middle" className="a-cap">{t}</text>
            {i < 2 && <text x={130 + i * 114} y="80" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-amber)" }}>→</text>}
          </g>
        ))}
      </G>

      <G o={step >= 4 ? 1 : 0}>
        <Txt x="180" y="46" mono size={13}>P(каре) = 624 / 2 598 960</Txt>
        <Txt x="180" y="86" mono size={22} color="var(--s-accent)">≈ 0,024 %</Txt>
        <rect x="50" y="110" width="260" height="10" rx="5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <rect x="50" y="110" width="2" height="10" rx="1" style={{ fill: "var(--s-red)" }} />
        <Txt x="180" y="140">доля группы в целом — это и есть вероятность</Txt>
      </G>
    </Steps>
  );
}
