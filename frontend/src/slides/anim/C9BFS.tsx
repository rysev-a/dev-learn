import { G, GraphView, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 5: обход в ширину — волна, очередь, и «стек против
   очереди» как единственная разница. */

const LABELS = ["Ширина", "Волна", "Очередь", "Стек против очереди"];
const CAPTION = [
  "Второй способ — обход в ширину: сначала все ближние, потом дальние",
  "Из старта посещаем всех соседей, потом соседей соседей — волна расходится кругами по воде",
  "Чтобы волна не сбивалась, нужна очередь: «первым пришёл — первым ушёл» держит порядок по расстоянию",
  "Стек и очередь — единственная разница в коде, а поведение алгоритмов радикально разное",
];
const N = [
  { x: 60, y: 76, l: "S" },
  { x: 130, y: 36, l: "1" },
  { x: 130, y: 116, l: "1" },
  { x: 210, y: 36, l: "2" },
  { x: 210, y: 116, l: "2" },
  { x: 290, y: 76, l: "3" },
];
const E = [
  { a: 0, b: 1 },
  { a: 0, b: 2 },
  { a: 1, b: 3 },
  { a: 2, b: 4 },
  { a: 3, b: 5 },
  { a: 4, b: 5 },
];
const LAYER = [0, 1, 1, 2, 2, 3];
const COL = ["g", "b", "y", "r"];
const QUEUE = [
  ["S"],
  ["1", "1"],
  ["1", "2"],
  ["2", "2"],
];

export default function C9BFS({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [6.1, 12.6, 24.2], 3000);
  const { step } = ctl;
  const wave = step >= 1 && step <= 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {[0, 1, 2, 3].map((l) => (
        <circle key={l} className="a-t" cx="60" cy="76" r={l * 76 + 8} style={{ fill: "none", stroke: "var(--s-accent)", strokeWidth: 1.2, strokeDasharray: "3 4", opacity: wave && l > 0 ? 0.4 : 0, transitionDelay: step === 1 ? `${l * 400}ms` : "0ms" }} />
      ))}
      <GraphView nodes={N} edges={E} nc={(i) => (step >= 1 && step <= 2 ? COL[LAYER[i]] : "m")} ec={() => (step >= 1 && step <= 2 ? "g" : "m")} o={step <= 1 ? 1 : step === 2 ? 0.35 : 0} />
      <Txt x={180} y={152} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">круг 0 → 1 → 2 → 3</Txt>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={180} y={30} size={9.5}>очередь</Txt>
        {QUEUE.map((q, i) => (
          <g key={i} className="a-t" style={{ opacity: step === 2 ? 1 : 0, transitionDelay: `${i * 350}ms` }}>
            {q.map((v, j) => (
              <Pill key={j} x={150 + j * 36} y={46 + i * 24} w={30} h={18} text={v} stroke="var(--s-blue)" size={9} />
            ))}
          </g>
        ))}
        <Txt x={180} y={152} mono size={11} color="var(--s-blue)">вынули слева, добавили справа</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <Pill x={100} y={60} w={140} h={50} text="stack.pop()" stroke="var(--s-amber)" size={12} />
        <Txt x={100} y={96} size={9.5}>последним пришёл — первым ушёл</Txt>
        <Pill x={260} y={60} w={140} h={50} text="queue.popleft()" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
        <Txt x={260} y={96} size={9.5}>первым пришёл — первым ушёл</Txt>
        <Txt x={100} y={130} mono size={11} color="var(--s-amber)">глубина</Txt>
        <Txt x={260} y={130} mono size={11} color="var(--s-accent)">ширина</Txt>
      </G>
    </Steps>
  );
}
