import { G, GraphView, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 7: поиск компонент связности обходами — число запусков
   равно числу островов. */

const LABELS = ["Классика", "Алгоритм", "Острова", "Где нужно", "Любой обход"];
const CAPTION = [
  "Утилитарная классика: поиск компонент связности",
  "Пройдись по всем вершинам; встретил непосещённую — запусти из неё обход и пометь всю её родню",
  "Каждый запуск вычерпывает ровно одну компоненту; число запусков равно числу островов",
  "Так считают изолированные группы пользователей, кластеры сервисов и несвязанные куски графа зависимостей",
  "Глубина и ширина здесь взаимозаменяемы — важен лишь факт полного вычерпывания",
];
const N = [
  { x: 46, y: 50, l: "1" },
  { x: 100, y: 100, l: "2" },
  { x: 130, y: 44, l: "3" },
  { x: 218, y: 52, l: "4" },
  { x: 260, y: 108, l: "5" },
  { x: 312, y: 54, l: "6" },
  { x: 180, y: 130, l: "7" },
  { x: 222, y: 150, l: "8" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 2 },
  { a: 3, b: 4 },
  { a: 4, b: 5 },
  { a: 3, b: 5 },
  { a: 6, b: 7 },
];
const COMP = (i: number) => (i <= 2 ? 0 : i <= 5 ? 1 : 2);
const COL = ["b", "y", "g"];

export default function C9Components({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.6, 11.2, 16.8, 22.9], 3000);
  const { step } = ctl;
  const on = step >= 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView nodes={N} edges={E} nc={(i) => (on ? COL[COMP(i)] : "m")} ec={(e) => (on ? COL[COMP(e.a)] : "m")} />
      {[0, 1, 2].map((k) => (
        <g key={k} className="a-t" style={{ opacity: step >= 2 ? 1 : 0, transitionDelay: `${k * 400}ms` }}>
          <text x={[100, 260, 200][k]} y={[22, 22, 148][k]} textAnchor="middle" className="a-mono" style={{ fontSize: 11, fill: `var(--s-${["blue", "amber", "accent"][k]})` }}>{`запуск ${k + 1}`}</text>
        </g>
      ))}
      <Txt x={180} y={14} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">for v in V: if v не посещена → обход(v)</Txt>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={322} y={150} mono size={13} color="var(--s-accent)">3 острова</Txt>
      </G>
      <Txt x={180} y={14} mono size={10.5} o={step === 3 ? 1 : 0}>группы пользователей · кластеры · куски зависимостей</Txt>
      <Txt x={180} y={14} mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-accent)">DFS или BFS — результат одинаков</Txt>
    </Steps>
  );
}
