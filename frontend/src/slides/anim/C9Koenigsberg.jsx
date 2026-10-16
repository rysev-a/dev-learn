import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 11: кёнигсбергские мосты — степени вершин; правило Эйлера:
   нечётных вершин ноль или две. */

const LABELS = ["Задача", "Семь мостов", "Заход = 2", "Правило", "Кёнигсберг"];
const CAPTION = [
  "Старейшая задача теории графов, рождённая прогулкой",
  "В Кёнигсберге через реку семь мостов: можно ли пройти по каждому ровно один раз?",
  "Эйлер: каждый заход в вершину тратит два ребра — войти и выйти, поэтому нечётные степени возможны лишь у старта и финиша",
  "Эйлеров путь существует, только если нечётных вершин ноль (замкнутый маршрут) или две",
  "В Кёнигсберге нечётных вершин четыре — прогулка невозможна, а теория графов родилась",
];
const V = {
  A: [180, 24],
  B: [64, 82],
  C: [296, 82],
  D: [180, 136],
};
// пары вершин и сдвиг дуги для кратных рёбер
const BR = [
  ["A", "B", -10],
  ["A", "B", 10],
  ["A", "C", -10],
  ["A", "C", 10],
  ["A", "D", 0],
  ["B", "D", 0],
  ["C", "D", 0],
];
const deg = { A: 5, B: 3, C: 3, D: 3 };

function arc([a, b, off]) {
  const [x1, y1] = V[a];
  const [x2, y2] = V[b];
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = y2 - y1;
  const dy = x1 - x2;
  const d = Math.hypot(dx, dy) || 1;
  return `M${x1} ${y1} Q${mx + (dx / d) * off * 2} ${my + (dy / d) * off * 2} ${x2} ${y2}`;
}

export default function C9Koenigsberg({ cues }) {
  const ctl = useSteps(cues || [4.6, 12.0, 24.0, 30.8], 3000);
  const { step } = ctl;
  const odd = step >= 3;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step >= 1 ? 1 : 0}>
        {BR.map((b, i) => (
          <path key={i} d={arc(b)} style={{ fill: "none", stroke: step >= 2 ? "var(--s-accent)" : "var(--s-muted)", strokeWidth: 2, opacity: step === 2 ? 0.7 : 1 }} />
        ))}
        {Object.entries(V).map(([k, [x, y]]) => (
          <g key={k}>
            <circle cx={x} cy={y} r="15" className="a-t" style={{ fill: odd ? "var(--s-red)" : "var(--s-panel2)", fillOpacity: odd ? 0.3 : 1, stroke: odd ? "var(--s-red)" : "var(--s-blue)", strokeWidth: 1.8 }} />
            <text x={x} y={y + 4} textAnchor="middle" className="a-mono" style={{ fontSize: 12 }}>{k}</text>
            <Txt x={x + (k === "B" ? -32 : 34)} y={y + 4} mono size={10} o={step >= 2 ? 1 : 0} color="var(--s-amber)">{`deg ${deg[k]}`}</Txt>
          </g>
        ))}
      </G>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">7 мостов — по разу?</Txt>
      <Txt x="180" y="156" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-accent)">зашёл + вышел = −2 ребра</Txt>
      <Txt x="180" y="156" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">нечётных вершин: 0 или 2</Txt>
      <Txt x="180" y="156" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-red)">нечётных четыре ⇒ нельзя</Txt>
    </Steps>
  );
}
