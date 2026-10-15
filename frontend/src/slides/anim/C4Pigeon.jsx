import { Dot, G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 4, слайд 9: принцип Дирихле. Пять кроликов, четыре клетки: при любой
   рассадке в какой-то клетке минимум двое; существование без адреса. */

const LABELS = ["Принцип", "5 > 4", "Любая рассадка", "Без адреса"];
const CAPTION = [
  "Принцип Дирихле — самый незамысловатый и самый хитрый инструмент курса",
  "Кроликов больше, чем клеток: хотя бы в одной клетке сидят минимум двое",
  "Как бы кролики ни рассаживались — вывод гарантирован самим количеством",
  "Принцип доказывает существование, но не говорит, в какой именно клетке искать",
];
const CAGE = [0, 1, 2, 3].map((i) => 48 + i * 76);
// размещения кроликов по клеткам (индекс клетки у каждого из пяти)
const ARR = {
  1: [0, 1, 1, 2, 3],
  2: [3, 3, 0, 2, 3],
};
const slotInCell = (arr, i) => arr.slice(0, i).filter((c) => c === arr[i]).length;

export default function C4Pigeon({ cues }) {
  const ctl = useSteps(cues || [5.1, 10.7, 16.6], 3000);
  const { step } = ctl;
  const arr = step === 2 ? ARR[2] : ARR[1];
  const placed = step >= 1;
  const cnt = (c) => arr.filter((a) => a === c).length;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {CAGE.map((x, c) => (
        <g key={c}>
          <rect className="a-t" x={x - 30} y="50" width="60" height="64" rx="8" style={{ fill: "none", stroke: placed && cnt(c) >= 2 ? "var(--s-amber)" : "var(--s-border)", strokeWidth: placed && cnt(c) >= 2 ? 2.4 : 1.5, strokeDasharray: placed ? "none" : "4 3" }} />
          <Txt x={x} y="130" o={placed ? 1 : 0} mono size={11} color={cnt(c) >= 2 ? "var(--s-amber)" : "var(--s-muted)"}>
            {cnt(c)}
          </Txt>
        </g>
      ))}
      {[0, 1, 2, 3, 4].map((i) => {
        const c = arr[i];
        const k = slotInCell(arr, i);
        const x = placed ? CAGE[c] - 14 + (k % 2) * 28 : 40 + i * 70;
        const y = placed ? 72 + Math.floor(k / 2) * 26 : 20;
        return <Dot key={i} x={x} y={y} r={10} text="🐇" size={12} stroke="var(--s-blue)" />;
      })}
      <Txt x="180" y="154" mono size={13} o={step >= 1 && step <= 2 ? 1 : 0} color="var(--s-amber)">5 кроликов &gt; 4 клеток ⇒ где-то ≥ 2</Txt>
      <G o={step >= 3 ? 1 : 0}>
        {CAGE.map((x, c) => (
          <Txt key={c} x={x} y="46" mono size={15} color="var(--s-red)">?</Txt>
        ))}
        <Txt x="180" y="154" size={11}>существование есть — адреса нет</Txt>
      </G>
    </Steps>
  );
}
