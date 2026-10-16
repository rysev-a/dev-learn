import { G, GraphView, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 12: обходы в продакшне — сборщик мусора, резолвер
   зависимостей (серый цвет ловит цикл), краулер; та же пара алгоритмов. */

const LABELS = ["Продакшн", "GC", "Резолвер", "Краулер", "Одна пара"];
const CAPTION = [
  "Соберём обходы обратно в продакшн",
  "Сборщик мусора обходит граф объектов от корней: достижимое живо, остальное — мусор",
  "Резолвер зависимостей обходит граф в глубину и следит за «серым» состоянием узла, чтобы поймать цикл",
  "Краулер — обход в ширину с множеством посещённых адресов, ограниченный глубиной и вежливостью к серверам",
  "Проверка достижимости в правах, кратчайший путь в игре, обход DOM в тестах — та же пара алгоритмов",
];

export default function C9Production({ cues }) {
  const ctl = useSteps(cues || [2.5, 11.1, 17.3, 23.8], 3000);
  const { step } = ctl;
  const gc = {
    nodes: [
      { x: 60, y: 40, l: "root" },
      { x: 150, y: 40, l: "a" },
      { x: 240, y: 40, l: "b" },
      { x: 150, y: 110, l: "c" },
      { x: 280, y: 110, l: "×" },
      { x: 320, y: 60, l: "×" },
    ],
    edges: [
      { a: 0, b: 1 },
      { a: 1, b: 2 },
      { a: 1, b: 3 },
      { a: 4, b: 5 },
    ],
  };
  const dep = {
    nodes: [
      { x: 80, y: 80, l: "a" },
      { x: 180, y: 36, l: "b" },
      { x: 280, y: 80, l: "c" },
    ],
    edges: [
      { a: 0, b: 1 },
      { a: 1, b: 2 },
      { a: 2, b: 0 },
    ],
  };
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">обходы в бою</Txt>
      <GraphView {...gc} directed nc={(i) => (i < 4 ? "g" : "m")} ec={(e) => (e.a === 4 ? "m" : "g")} ow={(i) => (i >= 4 ? 0.35 : 1)} o={step === 1 ? 1 : 0} />
      <Txt x="180" y="150" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">достижимое — живо; × — мусор</Txt>
      <GraphView {...dep} directed nc={(i) => ["g", "y", "r"][i]} ec={(e) => (e.a === 2 ? "r" : "g")} o={step === 2 ? 1 : 0} />
      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="150" mono size={11} color="var(--s-red)">c → a: a уже «серый» ⇒ цикл!</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {[
          [180, 34, "/"],
          [100, 84, "/a"],
          [260, 84, "/b"],
          [60, 134, "/a/1"],
          [140, 134, "/a/2"],
        ].map(([x, y, t]) => (
          <Pill key={t} x={x} y={y} w={46} h={20} text={t} stroke="var(--s-blue)" size={9} />
        ))}
        <Txt x="290" y="134" mono size={10} color="var(--s-amber)">глубина ≤ 2</Txt>
        <Txt x="290" y="150" mono size={10}>visited: {"{…}"}</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {["права доступа", "кратчайший путь в игре", "обход DOM в тестах"].map((t, i) => (
          <Pill key={t} x={180} y={36 + i * 38} w={230} h={28} text={t} stroke="var(--s-accent)" size={11} />
        ))}
        <Txt x="180" y="150" mono size={11} color="var(--s-accent)">DFS + BFS — меняются лишь декорации</Txt>
      </G>
    </Steps>
  );
}
