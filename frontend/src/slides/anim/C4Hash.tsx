import { Arrow, Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 4, слайд 10: принцип Дирихле в хеш-таблицах. Шесть ключей — четыре
   ячейки, коллизия неизбежна; цепочки, открытая адресация, рехеширование;
   хеш-функция делает коллизии редкими, но не убирает. */

const LABELS = ["Таблица", "Коллизия", "Механика", "Хеш-функция", "Дизайн"];
const CAPTION = [
  "Для программиста принцип — приговор и утешение одновременно",
  "В таблице четыре ячейки, ключей — сколько угодно: коллизия не «возможна», а гарантирована",
  "Отсюда вся механика: цепочки в ячейках, открытая адресация, расширение с перехешированием",
  "Хеш-функция не убирает коллизии — она лишь делает их редкими и нерегулярными",
  "Воевать с самой возможностью бессмысленно; делать коллизии дешёвыми — осмысленно",
];
const CELL = [0, 1, 2, 3].map((i) => 76 + i * 64);
const KEYS = [0, 1, 1, 2, 3, 1]; // ячейка каждого из шести ключей
const stack = (arr: number[], i: number) => arr.slice(0, i).filter((c) => c === arr[i]).length;

export default function C4Hash({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.3, 14.3, 21.6, 26.6], 3000);
  const { step } = ctl;
  const table = step <= 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={table ? 1 : 0}>
        {CELL.map((x, c) => (
          <g key={c}>
            <rect x={x - 28} y="92" width="56" height="44" rx="6" style={{ fill: "var(--s-panel2)", stroke: step === 1 && c === 1 ? "var(--s-red)" : "var(--s-border)", strokeWidth: step === 1 && c === 1 ? 2.4 : 1.4 }} />
            <text x={x} y="148" textAnchor="middle" className="a-cap">{c}</text>
          </g>
        ))}
        {KEYS.map((c, i) => {
          const k = stack(KEYS, i);
          const placed = step >= 1;
          const x = placed ? CELL[c] - 12 + (k % 2) * 24 : 40 + i * 56;
          const y = placed ? 106 + Math.floor(k / 2) * 18 : 30;
          return <Dot key={i} x={x} y={y} r={8} text={i + 1} size={8} stroke={c === 1 && placed ? "var(--s-red)" : "var(--s-accent)"} />;
        })}
        <Txt x={180} y={70} mono size={12} o={step === 1 ? 1 : 0} color="var(--s-red)">6 ключей &gt; 4 ячеек ⇒ коллизия</Txt>
        <Txt x={180} y={70} mono size={12} o={step === 0 ? 1 : 0}>hash(key) % 4</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {([
          ["цепочки", 60],
          ["открытая адресация", 180],
          ["расширение", 300],
        ] as const).map(([t, x]) => (
          <g key={t}>
            <rect x={x - 54} y="24" width="108" height="94" rx="10" style={{ fill: "none", stroke: "var(--s-border)" }} />
            <Txt x={x} y={136} size={9.5}>{t}</Txt>
          </g>
        ))}
        {/* цепочка */}
        <rect x="34" y="42" width="52" height="24" rx="5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <Dot x={46} y={54} r={7} text="1" size={8} stroke="var(--s-accent)" />
        <Arrow x1={54} y1={54} x2={64} y2={54} c="g" />
        <Dot x={74} y={54} r={7} text="2" size={8} stroke="var(--s-accent)" />
        <rect x="34" y="78" width="52" height="24" rx="5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        {/* открытая адресация */}
        {[0, 1, 2].map((i) => (
          <rect key={i} x={140 + i * 26} y="56" width="24" height="32" rx="4" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        ))}
        <Dot x={152} y={72} r={7} text="1" size={8} stroke="var(--s-accent)" />
        <Dot x={178} y={72} r={7} text="2" size={8} stroke="var(--s-amber)" />
        <path d="M152 56 C160 36 172 36 178 54" markerEnd="url(#a-hd-y)" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 1.4 }} />
        {/* расширение */}
        {[0, 1].map((i) => (
          <rect key={i} x={262 + i * 18} y="38" width="16" height="24" rx="3" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        ))}
        <Txt x={300} y={82} mono size={10} color="var(--s-accent)">2 → 4 → 8</Txt>
        {[0, 1, 2, 3].map((i) => (
          <rect key={i} x={262 + i * 18} y="92" width="16" height="16" rx="3" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)" }} />
        ))}
      </G>

      <G o={step === 3 ? 1 : 0}>
        {["хорошо: ровно", "плохо: кучно"].map((t, j) => (
          <g key={t}>
            <Txt x={90 + j * 180} y={22} size={9.5} color={j ? "var(--s-red)" : "var(--s-accent)"}>{t}</Txt>
            {[0, 1, 2, 3].map((c) => {
              const h = j === 0 ? [30, 28, 32, 30][c] : [74, 20, 18, 8][c];
              return (
                <rect key={c} className="a-t" x={46 + j * 180 + c * 24} y={130 - (step === 3 ? h : 0)} width="18" height={step === 3 ? h : 0} rx="3" style={{ fill: j ? "var(--s-red)" : "var(--s-accent)", fillOpacity: 0.4, stroke: j ? "var(--s-red)" : "var(--s-accent)" }} />
              );
            })}
          </g>
        ))}
        <Txt x={180} y={152} size={9.5}>коллизии остаются — но редкие и нерегулярные</Txt>
      </G>

      <G o={step >= 4 ? 1 : 0}>
        <Pill x={110} y={64} w={150} h={34} text="убрать коллизии" stroke="var(--s-red)" size={10} />
        <Txt x={110} y={104} mono size={16} color="var(--s-red)">✗</Txt>
        <Pill x={270} y={64} w={150} h={34} text="сделать дешёвыми" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10} />
        <Txt x={270} y={104} mono size={16} color="var(--s-accent)">✓</Txt>
      </G>
    </Steps>
  );
}
