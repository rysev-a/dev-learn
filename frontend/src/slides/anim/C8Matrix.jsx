import { G, Matrix, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 8, слайд 8: матрица смежности — таблица единиц и нулей;
   проверка ребра за O(1); простота; плотные графы. */

const LABELS = ["Память", "Матрица", "Проверка", "Простота", "Плотные"];
const CAPTION = [
  "Как граф уложить в память?",
  "Матрица смежности: строки и столбцы — вершины, единица на пересечении означает «ребро есть»",
  "Проверить, есть ли ребро между двумя вершинами, — константа: заглядываем в ячейку",
  "Предельная простота: это обычный двумерный массив без дополнительных структур",
  "Для плотных графов, где рёбер много, матрица — честный выбор",
];
const V = ["A", "B", "C", "D", "E"];
const E = new Set(["0-1", "0-2", "1-2", "2-3", "3-4", "1-4"]);
const has = (r, c) => E.has(`${Math.min(r, c)}-${Math.max(r, c)}`) && r !== c;
const DENSE = (r, c) => r !== c;

export default function C8Matrix({ cues }) {
  const ctl = useSteps(cues || [1.9, 9.9, 17.5, 20.3], 3000);
  const { step } = ctl;
  const dense = step >= 4;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">граф → память</Txt>
      <G o={step >= 1 ? 1 : 0}>
        <Matrix
          x={110}
          y={30}
          rows={V}
          cols={V}
          cell={26}
          mark={(r, c) => (dense ? (DENSE(r, c) ? "g" : null) : step === 2 && r === 1 && c === 4 ? "y" : has(r, c) ? "g" : null)}
        />
        {Array.from({ length: 5 }, (_, r) =>
          Array.from({ length: 5 }, (_, c) => (
            <text key={`${r}${c}`} x={110 + c * 26 + 13} y={30 + r * 26 + 17} textAnchor="middle" className="a-mono a-t" style={{ fontSize: 11, fill: (dense ? DENSE(r, c) : has(r, c)) ? "var(--s-accent)" : "var(--s-muted)" }}>
              {(dense ? DENSE(r, c) : has(r, c)) ? 1 : 0}
            </text>
          )),
        )}
        <Txt x="290" y="70" size={10} o={step === 2 ? 1 : 0} color="var(--s-amber)">adj[B][E] → 1</Txt>
        <Txt x="290" y="86" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-accent)">O(1)</Txt>
        <Txt x="290" y="70" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">adj = [[0,1,…],</Txt>
        <Txt x="290" y="86" mono size={11} o={step === 3 ? 1 : 0} color="var(--s-accent)">       [1,0,…], …]</Txt>
        <Txt x="290" y="78" size={10} o={dense ? 1 : 0} color="var(--s-accent)">много рёбер —</Txt>
        <Txt x="290" y="92" size={10} o={dense ? 1 : 0} color="var(--s-accent)">ячейки не пропадают</Txt>
      </G>
    </Steps>
  );
}
