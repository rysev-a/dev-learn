import { GraphView, Steps, Txt, useSteps, type GraphEdge } from "./kit.tsx";

/* Глава 8, слайд 6: связность и компоненты — острова без мостов. */

const LABELS = ["Распад", "Связный", "Компоненты", "Соцсеть", "Пакеты", "Задача"];
const CAPTION = [
  "Граф может распасться на куски",
  "Связный граф: из любой вершины можно дойти до любой другой",
  "Если кусков несколько — каждый называется компонентой связности: остров без мостов к остальным",
  "В соцсети компоненты — сообщества без общих знакомых",
  "В зависимостях компонента — группа пакетов, которые ставятся и удаляются только вместе",
  "Поиск этих островов — первая утилитарная задача про графы, решим в следующей главе",
];
const N = [
  { x: 50, y: 50, l: "1" },
  { x: 100, y: 100, l: "2" },
  { x: 130, y: 44, l: "3" },
  { x: 220, y: 54, l: "4" },
  { x: 260, y: 108, l: "5" },
  { x: 310, y: 54, l: "6" },
  { x: 180, y: 130, l: "7" },
  { x: 220, y: 150, l: "8" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 2 },
  { a: 3, b: 4 },
  { a: 4, b: 5 },
  { a: 3, b: 5 },
  { a: 6, b: 7 },
  { a: 2, b: 3, bridge: true },
  { a: 1, b: 6, bridge: true },
];
const COMP = (i: number) => (i <= 2 ? 0 : i <= 5 ? 1 : 2);
const COL = ["b", "y", "g"];

export default function C8Components({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.3, 6.1, 14.6, 18.5, 24.3], 3000);
  const { step } = ctl;
  const connected = step === 1;
  const comps = step >= 2;
  const ec = (e: GraphEdge) => (e.bridge ? (connected ? "g" : null) : comps ? COL[COMP(e.a)] : "m");
  const nc = (i: number) => (comps ? COL[COMP(i)] : connected ? "g" : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} ec={ec} nc={nc} o={step === 0 ? 0.5 : 1} />
      {([
        [10, 26, 150, 96, "b"],
        [196, 26, 140, 100, "y"],
        [160, 116, 80, 44, "g"],
      ] as const).map(([x, y, w, h, c], i) => (
        <rect key={i} className="a-hull a-t" x={x} y={y} width={w} height={h} rx="16" style={{ stroke: `var(--s-${{ b: "blue", y: "amber", g: "accent" }[c]})`, opacity: comps ? 1 : 0 }} />
      ))}
      <Txt x={180} y={14} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">один остров: всё достижимо</Txt>
      <Txt x={180} y={14} mono size={11} o={step === 2 ? 1 : 0} color="var(--s-amber)">3 компоненты связности</Txt>
      <Txt x={180} y={14} mono size={11} o={step === 3 ? 1 : 0}>сообщества без общих знакомых</Txt>
      <Txt x={180} y={14} mono size={11} o={step === 4 ? 1 : 0}>ставятся и удаляются вместе</Txt>
      <Txt x={180} y={14} mono size={11} o={step >= 5 ? 1 : 0} color="var(--s-accent)">найти острова → обходы графа</Txt>
    </Steps>
  );
}
