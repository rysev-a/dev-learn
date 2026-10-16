import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 11: инвариант цикла — индукция для циклов. */

const LABELS = ["Циклы", "Инвариант", "До и после", "База · переход", "Выход", "Примеры"];
const CAPTION = [
  "А что делать с циклами, где нет рекурсии?",
  "Родной приём — инвариант цикла",
  "Инвариант — утверждение, верное перед каждой итерацией и после каждой",
  "Доказывается по индукции: перед первым витком верен — база; если верен до витка, то и после — переход",
  "Когда цикл закончился, инвариант плюс условие выхода дают ровно то, что цикл решает задачу",
  "Так доказывают корректность сортировки вставками, бинарного поиска и многих других рабочих лошадок",
];

export default function C7Invariant({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.2, 5.8, 11.9, 18.4, 24.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <rect x="80" y="30" width="200" height="86" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="100" y="58" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>while cond:</text>
        <text x="120" y="82" className="a-mono" style={{ fontSize: 13 }}>step()</text>
        <Txt x={180} y={140} size={10}>рекурсии нет — индукция откуда?</Txt>
      </G>
      <Txt x={180} y={86} mono size={30} o={step === 1 ? 1 : 0} color="var(--s-accent)">инвариант</Txt>
      <G o={step >= 2 && step <= 3 ? 1 : 0}>
        {Array.from({ length: 4 }, (_, i) => (
          <g key={i}>
            <Pill x={40 + i * 86} y={52} w={58} h={26} text={`I ✓`} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10} />
            <rect x={70 + i * 86} y="94" width="50" height="22" rx="6" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.2 }} />
            <text x={95 + i * 86} y="109" textAnchor="middle" className="a-cap">виток {i + 1}</text>
          </g>
        ))}
        <Txt x={180} y={140} mono size={11} o={step === 2 ? 1 : 0} color="var(--s-accent)">I верен перед витком и после витка</Txt>
        <Txt x={62} y={40} size={9.5} o={step === 3 ? 1 : 0} color="var(--s-amber)">база: до первого</Txt>
        <Txt x={250} y={140} mono size={11} o={step === 3 ? 1 : 0} color="var(--s-blue)">переход: до ⇒ после</Txt>
      </G>
      <G o={step === 4 ? 1 : 0}>
        <Pill x={90} y={70} w={110} h={34} text="инвариант I" stroke="var(--s-accent)" size={11} />
        <Txt x={150} y={74} mono size={16}>+</Txt>
        <Pill x={210} y={70} w={110} h={34} text="выход: ¬cond" stroke="var(--s-blue)" size={11} />
        <Txt x={270} y={74} mono size={16}>⇒</Txt>
        <Pill x={320} y={70} w={70} h={34} text="ответ" stroke="var(--s-amber)" size={11} />
        <Txt x={180} y={130} mono size={12} color="var(--s-accent)">цикл решает задачу</Txt>
      </G>
      <G o={step >= 5 ? 1 : 0}>
        {["сортировка вставками", "бинарный поиск", "…и многие другие"].map((t, i) => (
          <Pill key={t} x={180} y={36 + i * 38} w={210} h={28} text={t} stroke="var(--s-accent)" size={11} />
        ))}
      </G>
    </Steps>
  );
}
