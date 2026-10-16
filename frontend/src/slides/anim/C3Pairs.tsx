import { G, Matrix, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 3, слайд 10: C(n, 2) — число пар. Рукопожатия десяти человек,
   треугольник вложенного цикла, полный граф серверов. */

const LABELS = ["C(n, 2)", "Рукопожатия", "Цикл", "Серверы"];
const CAPTION = [
  "Частный случай сочетаний — число пар: C(n, 2) = n(n − 1) / 2",
  "Десять человек пожмут руки C(10, 2) = 45 раз",
  "В коде: второй индекс всегда больше первого — все пары без повторов и зеркальных дублей",
  "Это же число рёбер полного графа: для 100 серверов нужно 4 950 каналов",
];
const pts = (n: number, r: number, cx: number, cy: number) =>
  Array.from({ length: n }, (_, i) => [cx + r * Math.cos((2 * Math.PI * i) / n - Math.PI / 2), cy + r * Math.sin((2 * Math.PI * i) / n - Math.PI / 2)]);
const edges = (n: number) => {
  const e = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) e.push([i, j]);
  return e;
};
const P10 = pts(10, 56, 180, 84);
const P7 = pts(7, 54, 180, 84);
const N = ["0", "1", "2", "3", "4", "5", "6"];

export default function C3Pairs({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [6.6, 11.5, 18.8], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={78} mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">C(n, 2) = n(n − 1) / 2</Txt>

      <G o={step === 1 ? 1 : 0}>
        {edges(10).map(([a, b], i) => (
          <line key={i} className="a-t" x1={P10[a!]![0]} y1={P10[a!]![1]} x2={P10[b!]![0]} y2={P10[b!]![1]} style={{ stroke: "var(--s-accent)", strokeWidth: 1, opacity: step === 1 ? 0.5 : 0, transitionDelay: `${i * 25}ms` }} />
        ))}
        {P10.map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r="6" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.8 }} />
        ))}
        <Txt x={72} y={90} mono size={20} color="var(--s-accent)">45</Txt>
        <Txt x={72} y={106}>рукопожатий</Txt>
        <Txt x={288} y={90} mono size={11}>10 · 9 / 2</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        <Matrix x={200} y={30} rows={N} cols={N} cell={20} mark={(r, c) => (c > r ? "g" : null)} />
        <text x="24" y="46" className="a-mono" style={{ fontSize: 10.5 }}>for i in range(n):</text>
        <text x="40" y="64" className="a-mono" style={{ fontSize: 10.5 }}>for j in range(i+1, n):</text>
        <text x="56" y="82" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-accent)" }}>pair(i, j)</text>
        <Txt x={110} y={150} mono size={11} color="var(--s-accent)">j &gt; i: ровно C(n, 2) клеток</Txt>
      </G>

      <G o={step >= 3 ? 1 : 0}>
        {edges(7).map(([a, b], i) => (
          <line key={i} x1={P7[a!]![0]} y1={P7[a!]![1]} x2={P7[b!]![0]} y2={P7[b!]![1]} style={{ stroke: "var(--s-amber)", strokeWidth: 1, opacity: 0.5 }} />
        ))}
        {P7.map(([x, y], i) => (
          <rect key={i} x={x! - 6} y={y! - 6} width="12" height="12" rx="3" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.8 }} />
        ))}
        <Txt x={62} y={86} mono size={11}>100 серверов</Txt>
        <Txt x={298} y={84} mono size={18} color="var(--s-amber)">4 950</Txt>
        <Txt x={298} y={102}>каналов</Txt>
      </G>
    </Steps>
  );
}
