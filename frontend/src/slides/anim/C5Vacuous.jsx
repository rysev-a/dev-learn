import { G, Pill, Steps, Table, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 6: при ложной посылке импликация истинна. Балерина,
   контракт проверки входа, all() на пустом массиве. */

const LABELS = ["Подвох", "Ложная посылка", "Балерина", "Контракт", "Пустой массив"];
const CAPTION = [
  "А теперь подвох, о который спотыкаются все",
  "Когда посылка ложна, импликация истинна — автоматически, при любом следствии",
  "«Если два больше трёх, то я балерина»: два не больше трёх — формально истинно",
  "Контракт «если вход некорректный, прервать» не нарушен, когда вход корректный — проверка молча прошла",
  "all() на пустом массиве честно возвращает истину: нет элементов — нет и нарушителей",
];
const ROWS = [
  [1, 1, 1],
  [1, 0, 0],
  [0, 1, 1],
  [0, 0, 1],
];

export default function C5Vacuous({ cues }) {
  const ctl = useSteps(cues || [3.1, 7.6, 13.7, 23.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-amber)">0 → q  =  1</Txt>
      <Table x={96} y={34} head={["p", "q", "p→q"]} rows={ROWS} cw={56} rh={26} o={step === 1 ? 1 : 0} hl={(r, c) => (r >= 2 ? (c === 2 ? "g" : "y") : r === 1 && c === 2 ? "r" : null)} />
      <Txt x="300" y="106" size={9.5} o={step === 1 ? 1 : 0} color="var(--s-amber)">p = 0 → всегда 1</Txt>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={90} y={64} w={130} h={30} text="2 > 3" stroke="var(--s-red)" />
        <Txt x="90" y="96" mono size={11} color="var(--s-red)">ложь</Txt>
        <Txt x="180" y="68" mono size={16}>→</Txt>
        <Pill x={270} y={64} w={130} h={30} text="я балерина" stroke="var(--s-muted)" />
        <Txt x="180" y="130" mono size={13} color="var(--s-accent)">вся импликация — истина</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={100} y={56} w={160} h={30} text="вход корректен" stroke="var(--s-accent)" />
        <Txt x="196" y="60" mono size={14}>→</Txt>
        <Pill x={270} y={56} w={110} h={30} text="проверка прошла" stroke="var(--s-blue)" />
        <Txt x="180" y="110" size={10}>«некорректный вход ⇒ прервать» — ложная посылка, контракт цел</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="70" y="40" width="220" height="40" rx="8" style={{ fill: "none", stroke: "var(--s-border)", strokeDasharray: "4 3" }} />
        <Txt x="180" y="64" mono size={13}>[ ]  — пусто</Txt>
        <Txt x="180" y="112" mono size={13} color="var(--s-accent)">all(x &gt; 0 for x in [])  →  True</Txt>
        <Txt x="180" y="134" size={9.5}>нет элементов — нет и нарушителей</Txt>
      </G>
    </Steps>
  );
}
