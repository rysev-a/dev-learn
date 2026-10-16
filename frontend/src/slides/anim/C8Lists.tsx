import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 8, слайд 9: списки смежности — экономия для разреженных графов;
   соцсеть на миллиард; цена проверки; перебор соседей. */

const LABELS = ["Списки", "Разреженные", "Миллиард", "Цена", "Обход"];
const CAPTION = [
  "Второй способ — списки смежности: для каждой вершины храним список её соседей",
  "Для разреженных графов, где рёбер несравнимо меньше возможных пар, это радикальная экономия",
  "Соцсеть с миллиардом пользователей: в матрице — квинтиллион ячеек, в списках — порядка 2 · 10¹¹ записей",
  "Цена: чтобы узнать, дружат ли две вершины, придётся просматривать список соседей",
  "Зато основная операция обхода — «перечисли соседей» — делается без возни с пустыми ячейками",
];
const ADJ = [
  ["B", "C"],
  ["A", "C", "E"],
  ["A", "B", "D"],
  ["C", "E"],
  ["B", "D"],
];

export default function C8Lists({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.3, 10.9, 19.0, 24.9], 3000);
  const { step } = ctl;
  const lists = step !== 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={lists ? 1 : 0}>
        {ADJ.map((nb, i) => (
          <g key={i}>
            <Pill x={40} y={24 + i * 28} w={34} h={22} text={"ABCDE"[i]} stroke="var(--s-blue)" size={10} />
            {nb.map((n, j) => (
              <Pill
                key={j}
                x={88 + j * 40}
                y={24 + i * 28}
                w={34}
                h={22}
                text={n}
                stroke={step === 3 && i === 0 && n === "C" ? "var(--s-amber)" : step === 4 && i === 1 ? "var(--s-accent)" : "var(--s-border)"}
                fill={step === 3 && i === 0 ? "var(--s-panel2)" : step === 4 && i === 1 ? "var(--s-green)" : "var(--s-panel2)"}
                size={10}
              />
            ))}
          </g>
        ))}
        <Txt x={290} y={50} size={10} o={step === 1 ? 1 : 0}>памяти — пропорционально</Txt>
        <Txt x={290} y={66} size={10} o={step === 1 ? 1 : 0} mono color="var(--s-accent)">числу рёбер</Txt>
        <Txt x={290} y={60} size={10} o={step === 3 ? 1 : 0} mono color="var(--s-amber)">C ∈ adj[A]?</Txt>
        <Txt x={290} y={76} size={10} o={step === 3 ? 1 : 0}>смотрим подряд</Txt>
        <Txt x={290} y={60} size={10} o={step >= 4 ? 1 : 0} mono color="var(--s-accent)">for v in adj[B]:</Txt>
        <Txt x={290} y={76} size={10} o={step >= 4 ? 1 : 0}>соседи — без пустых</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <rect x="40" y="36" width="130" height="110" rx="8" style={{ fill: "var(--s-red)", fillOpacity: 0.15, stroke: "var(--s-red)", strokeWidth: 1.5 }} />
        <Txt x={105} y={84} mono size={13} color="var(--s-red)">10¹⁸</Txt>
        <Txt x={105} y={102} size={9.5}>ячеек матрицы</Txt>
        <rect x="210" y="86" width="20" height="20" rx="3" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
        <Txt x={270} y={84} mono size={13} color="var(--s-accent)">2·10¹¹</Txt>
        <Txt x={270} y={102} size={9.5}>записей в списках</Txt>
        <Txt x={180} y={154} size={10}>в среднем у человека пара сотен друзей</Txt>
      </G>
    </Steps>
  );
}
