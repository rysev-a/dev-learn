import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 7: мощность и двойной счёт. Два множества по 20 точек; общие
   5 точек при сближении кругов сливаются, и сумма 20 + 20 = 40 превращается
   в честные 35. */

const LABELS = ["Мощность", "20 + 20", "Перекрытие", "Формула", "Двойной счёт"];
const CAPTION = [
  "Мощность |A| — число элементов: как размер массива или число записей запроса",
  "Знают английский 20 человек и немецкий 20: наивно сложим и получим 40",
  "Но знающие оба языка попали в оба списка — при объединении их считают один раз",
  "Честный счёт — формулой включений и исключений: ей посвящена отдельная глава",
  "Наивное сложение — классическая ошибка двойного счёта",
];

const ROWS = [-28, -14, 0, 14, 28];
const OWN = [-34, -18, -2];

function Cluster({ side, hideBoth, bothColor }) {
  // side: 1 — EN (общие справа), -1 — DE (общие слева)
  const dots = [];
  for (const x of OWN)
    for (const y of ROWS) dots.push({ x: side === 1 ? x : -x, y, both: false });
  for (const y of ROWS) dots.push({ x: side * 35, y, both: true });
  return (
    <>
      {dots.map((d, i) => (
        <circle
          key={i}
          cx={d.x}
          cy={d.y}
          r="3.4"
          className="a-t"
          style={{
            fill: d.both ? bothColor : "var(--s-text)",
            fillOpacity: d.both ? 1 : 0.75,
            opacity: d.both && hideBoth ? 0 : 1,
            stroke: "none",
          }}
        />
      ))}
    </>
  );
}

export default function Overlap({ cues }) {
  const ctl = useSteps(cues || [6.9, 14.7, 23.5, 28.5], 3000);
  const { step } = ctl;
  const xa = step === 0 ? 180 : step === 1 ? 90 : 145;
  const xb = step === 1 ? 270 : 215;
  const joined = step >= 2;
  const both = step >= 4 ? "var(--s-red)" : "var(--s-amber)";
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G x={xa} y={84}>
        <circle r="50" className="a-ring a" />
        <Cluster side={1} hideBoth={false} bothColor={both} />
        <Txt x="-34" y="-58">EN</Txt>
      </G>
      <G x={xb} y={84} o={step >= 1 ? 1 : 0}>
        <circle r="50" className="a-ring b" />
        <Cluster side={-1} hideBoth={joined} bothColor={both} />
        <Txt x="34" y="-58">DE</Txt>
      </G>

      <Txt x="180" y="16" mono o={step === 0 ? 1 : 0} color="var(--s-accent)" size={13}>
        |EN| = 20
      </Txt>
      <Txt x="180" y="16" mono o={step === 1 ? 1 : 0} color="var(--s-accent)" size={13}>
        20 + 20 = 40 ?
      </Txt>
      <Txt x="180" y="16" mono o={step === 2 ? 1 : 0} color="var(--s-accent)" size={13}>
        |EN ∪ DE| = 35
      </Txt>
      <Txt x="180" y="16" mono o={step === 3 ? 1 : 0} color="var(--s-accent)" size={10.5}>
        |A ∪ B| = |A| + |B| − |A ∩ B|
      </Txt>
      <Txt x="180" y="16" mono o={step >= 4 ? 1 : 0} color="var(--s-red)" size={12}>
        5 человек посчитаны дважды
      </Txt>
      <Txt x="180" y="162" mono o={step === 3 ? 1 : 0}>
        = 20 + 20 − 5 = 35
      </Txt>
    </Steps>
  );
}
