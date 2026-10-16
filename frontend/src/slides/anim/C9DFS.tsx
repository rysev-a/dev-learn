import { G, GraphView, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 3: обход в глубину — иди вперёд до упора, потом назад;
   нитка Ариадны; стек. */

const LABELS = ["Глубина", "Вперёд и назад", "Нитка", "Стек"];
const CAPTION = [
  "Первый способ — обход в глубину",
  "Правило: иди вперёд, пока можно; упёрся — отступи на шаг и пробуй другую дверь",
  "Маршрут по лабиринту с ниткой на пальце: нитка помнит, откуда пришли, и по ней возвращаемся",
  "Естественно держать стеком: новый узел кладём, тупик снимаем, верх стека подсказывает, где мы",
];
const N = [
  { x: 180, y: 28, l: "A" },
  { x: 100, y: 74, l: "B" },
  { x: 260, y: 74, l: "C" },
  { x: 60, y: 124, l: "D" },
  { x: 140, y: 124, l: "E" },
  { x: 300, y: 124, l: "F" },
  { x: 200, y: 124, l: "G" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 3 },
  { a: 1, b: 4 },
  { a: 2, b: 5 },
  { a: 4, b: 6 },
];
// порядок посещения: A B D E G C F
const ORDER = [0, 1, 3, 4, 6, 2, 5];
const STACK = ["A", "B", "E", "G"];

export default function C9DFS({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.4, 8.2, 14.6], 3000);
  const { step } = ctl;
  const vis = step >= 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} nc={() => (vis ? "g" : "m")} ec={() => (vis ? "g" : "m")} r={13} />
      {ORDER.map((v, k) => (
        <g key={k} className="a-t" style={{ opacity: vis ? 1 : 0, transitionDelay: step === 1 ? `${k * 380}ms` : "0ms" }}>
          <text x={N[v]!.x + 18} y={N[v]!.y - 12} className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-amber)" }}>{k + 1}</text>
        </g>
      ))}
      <G o={step === 2 ? 1 : 0}>
        <path d="M180 28 L100 74 L60 124" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 3, strokeDasharray: "2 5", strokeLinecap: "round" }} />
        <Txt x={180} y={152} mono size={11} color="var(--s-amber)">нитка: A → B → D, тупик, назад к B</Txt>
      </G>
      <Txt x={180} y={152} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">порядок: A, B, D, E, G, C, F</Txt>
      <G o={step >= 3 ? 1 : 0}>
        {STACK.map((v, j) => (
          <Pill key={j} x={316} y={140 - j * 24} w={34} h={20} text={v} stroke="var(--s-blue)" size={10} />
        ))}
        <Txt x={316} y={30} size={9.5}>стек</Txt>
        <Txt x={316} y={44} mono size={9.5} color="var(--s-accent)">верх: G</Txt>
        <Txt x={150} y={152} mono size={11} color="var(--s-blue)">push — вошли, pop — вернулись</Txt>
      </G>
    </Steps>
  );
}
