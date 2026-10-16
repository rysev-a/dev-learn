import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 8: отношение эквивалентности — три свойства, классы
   «одинаковый остаток при делении на 3» и группировка по ключу. */

const LABELS = ["Три свойства", "Примеры", "Классы", "Группировка"];
const CAPTION = [
  "Рефлексивность + симметричность + транзитивность — отношение эквивалентности",
  "«Одинаковый остаток при делении на 3» — эквивалентность; цвет показывает остаток",
  "Эквивалентность режет множество на непересекающиеся классы",
  "Группировка по ключу — разбиение на классы; результат GROUP BY — готовые классы",
];
const COL = ["var(--s-blue)", "var(--s-amber)", "var(--s-accent)"];
const NUMS = Array.from({ length: 9 }, (_, i) => i + 1);
// ряд из девяти → три класса
const rowPos = (i: number) => [24 + i * 38, 70];
const classPos = (i: number) => {
  const cls = i % 3;
  const k = Math.floor(i / 3);
  return [66 + cls * 124 + (k - 1) * 30, 62];
};

export default function C2Equivalence({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [7.8, 15.2, 22.8], 3000);
  const { step } = ctl;
  const classes = step >= 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* свойства */}
      <G o={step === 0 ? 1 : 0}>
        {([
          ["a ~ a", "рефлексивность"],
          ["a ~ b ⇒ b ~ a", "симметричность"],
          ["a ~ b, b ~ c ⇒ a ~ c", "транзитивность"],
        ] as const).map(([f, n], i) => (
          <g key={n}>
            <rect x="30" y={30 + i * 38} width="300" height="30" rx="8" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.3 }} />
            <text x="44" y={49 + i * 38} className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>{f}</text>
            <text x="316" y={49 + i * 38} textAnchor="end" className="a-cap">{n}</text>
          </g>
        ))}
      </G>

      {/* числа: ряд → классы */}
      {NUMS.map((n, i) => {
        const [x, y] = classes ? classPos(i) : rowPos(i);
        const coloured = step >= 1;
        const c = COL[i % 3];
        return (
          <g key={n} className="a-t" style={{ transform: `translate(${x}px, ${y}px)`, opacity: step >= 1 ? 1 : 0 }}>
            <circle r="13" style={{ fill: coloured ? c : "var(--s-panel2)", fillOpacity: coloured ? 0.3 : 1, stroke: coloured ? c : "var(--s-muted)", strokeWidth: 1.8 }} />
            <text y="4" textAnchor="middle" className="a-mono" style={{ fontSize: 11 }}>{n}</text>
          </g>
        );
      })}
      {[0, 1, 2].map((k) => (
        <g key={k} className="a-t" style={{ opacity: classes ? 1 : 0 }}>
          <rect x={14 + k * 124} y="28" width="104" height="68" rx="14" className="a-hull" style={{ stroke: COL[k] }} />
          <text x={66 + k * 124} y="112" textAnchor="middle" className="a-cap">остаток {(k + 1) % 3}</text>
        </g>
      ))}
      <G o={step === 3 ? 1 : 0}>
        <rect x="46" y="126" width="268" height="34" rx="8" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="60" y="147" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>GROUP BY n % 3  →  3 класса по 3 элемента</text>
      </G>
      <Txt x={180} y={152} o={step === 1 ? 1 : 0} mono size={10.5}>n ~ m ⇔ n % 3 = m % 3</Txt>
    </Steps>
  );
}
