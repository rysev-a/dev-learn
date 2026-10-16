import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 3, слайд 1: умение посчитать варианты, не перечисляя их.
   Пин-код, три решения «да/нет», два правила и три счётчика. */

const LABELS = ["Глава", "Перебор", "Выбор", "Инструменты"];
const CAPTION = [
  "Комбинаторика: перестановки и сочетания",
  "Оценка «перебор отработает через сто лет» начинается с умения посчитать варианты",
  "Комбинаторика — арифметика выбора: из мелких решений складывается число способов",
  "Два правила и три счётчика — на них держатся почти все инженерные оценки",
];

export default function C3Intro({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.6, 14.4, 20.6], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        {[0, 1, 2, 3].map((i) => (
          <g key={i}>
            <rect x={96 + i * 46} y="44" width="38" height="46" rx="8" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
            <text x={115 + i * 46} y="75" textAnchor="middle" className="a-mono" style={{ fontSize: 22, fill: "var(--s-accent)" }}>?</text>
          </g>
        ))}
        <Txt x={180} y={30} mono size={11}>каждая позиция: 10 цифр</Txt>
        <Txt x={180} y={122} mono size={20} color="var(--s-amber)">10⁴ = 10 000</Txt>
        <Txt x={180} y={144}>считаем, а не перечисляем</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <Pill x={70 + i * 110} y={50} w={64} text="да" stroke="var(--s-accent)" />
            <Pill x={70 + i * 110} y={84} w={64} text="нет" stroke="var(--s-amber)" />
            <Txt x={70 + i * 110} y={112} mono size={13} color="var(--s-accent)">×2</Txt>
          </g>
        ))}
        <Txt x={180} y={140} mono size={14} color="var(--s-accent)">2 · 2 · 2 = 8 способов</Txt>
        <Txt x={180} y={24}>три мелких решения</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {[
          ["+", "сумма"],
          ["×", "произведение"],
        ].map(([s, n], i) => (
          <g key={s}>
            <rect x={36 + i * 100} y="30" width="88" height="46" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
            <text x={80 + i * 100} y="56" textAnchor="middle" className="a-mono" style={{ fontSize: 20, fill: "var(--s-accent)" }}>{s}</text>
            <text x={80 + i * 100} y="70" textAnchor="middle" className="a-cap">{n}</text>
          </g>
        ))}
        <Txt x={118} y={22}>два правила</Txt>
        {[
          ["n!", "перестановки"],
          ["A", "размещения"],
          ["C", "сочетания"],
        ].map(([s, n], i) => (
          <g key={s}>
            <rect x={30 + i * 100} y="104" width="90" height="46" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
            <text x={75 + i * 100} y="128" textAnchor="middle" className="a-mono" style={{ fontSize: 17, fill: "var(--s-amber)" }}>{s}</text>
            <text x={75 + i * 100} y="142" textAnchor="middle" className="a-cap">{n}</text>
          </g>
        ))}
        <Txt x={180} y={98}>три счётчика</Txt>
      </G>
    </Steps>
  );
}
