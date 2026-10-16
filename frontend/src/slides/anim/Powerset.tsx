import { Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 9: булеан. Дерево решений «взять / не взять» для трёх элементов:
   8 листьев — 8 подмножеств; затем подписи листьев превращаются в битовые
   маски. */

const LABELS = ["Булеан", "2ⁿ", "Выбор", "3 → 10", "Биты"];
const CAPTION = [
  "Булеан — множество всех подмножеств исходного множества",
  "Если в множестве n элементов, то в булеане 2ⁿ подмножеств",
  "Для каждого элемента — два выбора: взять или нет, всего 2 · 2 · 2 решений",
  "Три элемента — восемь подмножеств, десять — уже тысяча двадцать четыре",
  "Битовая маска: один бит на элемент, каждое число — готовое подмножество",
];

const X = [36, 106, 176, 246];
const leafY = (i: number) => 24 + i * 17.5;
// y узла уровня l с номером j
const nodeY = (l: number, j: number) => {
  const span = 2 ** (3 - l);
  return (leafY(j * span) + leafY(j * span + span - 1)) / 2;
};
const NAMES = ["a", "b", "c"];
const subset = (i: number) =>
  i === 0 ? "∅" : "{" + NAMES.filter((_, k) => (i >> (2 - k)) & 1).join(", ") + "}";
const bits = (i: number) => i.toString(2).padStart(3, "0");

export default function Powerset({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.7, 11.2, 18.5, 23.1], 3000);
  const { step } = ctl;
  const tree = step === 2 || step === 4 ? 1 : step === 3 ? 0.2 : 0;
  const edges = [];
  for (let l = 0; l < 3; l++)
    for (let j = 0; j < 2 ** l; j++)
      for (const c of [0, 1])
        edges.push({
          x1: X[l],
          y1: nodeY(l, j),
          x2: X[l + 1],
          y2: nodeY(l + 1, j * 2 + c),
          yes: c === 1,
        });
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* исходное множество */}
      <g className="a-t" style={{ opacity: step <= 1 ? 1 : 0 }}>
        {NAMES.map((n, i) => (
          <g key={n}>
            <circle cx={130 + i * 50} cy="70" r="17" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.8 }} />
            <text x={130 + i * 50} y="75" textAnchor="middle" className="a-mono" style={{ fontSize: 14 }}>
              {n}
            </text>
          </g>
        ))}
        <Txt x={180} y={38} mono color="var(--s-accent)" size={13}>
          {"{a, b, c}"}
        </Txt>
      </g>
      <Txt x={180} y={124} mono o={step === 1 ? 1 : 0} color="var(--s-amber)" size={14}>
        n = 3 → 2ⁿ = 2·2·2 = 8
      </Txt>

      {/* дерево решений */}
      <g className="a-t" style={{ opacity: tree }}>
        {edges.map((e, i) => (
          <line
            key={i}
            x1={e.x1}
            y1={e.y1}
            x2={e.x2}
            y2={e.y2}
            style={{
              stroke: e.yes ? "var(--s-accent)" : "var(--s-muted)",
              strokeWidth: 1.4,
              strokeDasharray: e.yes ? "none" : "3 3",
            }}
          />
        ))}
        {NAMES.map((n, l) => (
          <text key={n} x={(X[l] + X[l + 1]) / 2} y="12" textAnchor="middle" className="a-mono" style={{ fontSize: 10.5 }}>
            {n}?
          </text>
        ))}
        {Array.from({ length: 8 }, (_, i) => (
          <g key={i}>
            <circle cx={X[3]} cy={leafY(i)} r="3" style={{ fill: "var(--s-accent)" }} />
            <text x={X[3] + 9} y={leafY(i) + 3.5} className="a-mono a-t" style={{ fontSize: 9.5, opacity: step === 4 ? 0 : 1 }}>
              {subset(i)}
            </text>
            <text x={X[3] + 9} y={leafY(i) + 3.5} className="a-mono a-t" style={{ fontSize: 9.5, opacity: step === 4 ? 1 : 0, fill: "var(--s-amber)" }}>
              {bits(i)} = {subset(i)}
            </text>
          </g>
        ))}
      </g>
      <Txt x={180} y={166} o={step === 2 || step === 4 ? 1 : 0}>
        — — не брать · ——— взять
      </Txt>

      {/* цифры 3 → 8, 10 → 1024 */}
      <Txt x={180} y={70} mono o={step === 3 ? 1 : 0} color="var(--s-accent)" size={16}>
        n = 3 → 8
      </Txt>
      <Txt x={180} y={100} mono o={step === 3 ? 1 : 0} color="var(--s-amber)" size={16}>
        n = 10 → 1 024
      </Txt>
    </Steps>
  );
}
