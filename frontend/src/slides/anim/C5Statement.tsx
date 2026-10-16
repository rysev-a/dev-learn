import { Arrow, Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 2: высказывание — истинно или ложно, третьего не дано;
   не высказывания; булево выражение в коде. */

const LABELS = ["Атом", "Высказывания", "Не они", "В коде"];
const CAPTION = [
  "Начнём с высказывания — атома всей главы",
  "Утверждение, которое объективно либо истинно, либо ложно: третьего не дано",
  "Не высказывания: вопрос, приказ и «это предложение ложно» — парадокс, ему нельзя приписать значение",
  "В коде ближайшая родня — выражение булева типа: любое, что можно поставить в условие",
];

export default function C5Statement({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.1, 14.1, 24.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Dot x={180} y={80} r={34} text="p" size={22} o={step === 0 ? 1 : 0} stroke="var(--s-accent)" />
      <G o={step === 1 ? 1 : 0}>
        {[
          ["2 > 1", "истинно", "var(--s-accent)"],
          ["сегодня среда", "истинно или ложно", "var(--s-amber)"],
        ].map(([t, v, c], i) => (
          <g key={t}>
            <Pill x={110} y={46 + i * 56} w={130} h={28} text={t} stroke={c} />
            <Arrow x1={178} y1={46 + i * 56} x2={214} y2={46 + i * 56} c={i ? "y" : "g"} />
            <Txt x={276} y={50 + i * 56} mono size={11} color={c}>{v}</Txt>
          </g>
        ))}
        <Txt x={180} y={150} mono size={12} color="var(--s-accent)">третьего не дано</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {["который час?", "выключи свет", "это предложение ложно"].map((t, i) => (
          <g key={t}>
            <Pill x={130} y={36 + i * 40} w={180} h={26} text={t} stroke="var(--s-red)" />
            <Txt x={266} y={41 + i * 40} mono size={15} color="var(--s-red)">✗</Txt>
          </g>
        ))}
        <Txt x={330} y={120} size={9.5} color="var(--s-red)" anchor="end">парадокс</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {[
          ["x > 0", "bool"],
          ["name == \"\"", "bool"],
          ["len(xs) >= 5", "bool"],
        ].map(([t, ty], i) => (
          <g key={t}>
            <Pill x={110} y={36 + i * 40} w={150} h={26} text={t} stroke="var(--s-accent)" size={10} />
            <Arrow x1={190} y1={36 + i * 40} x2={236} y2={36 + i * 40} c="g" />
            <Pill x={274} y={36 + i * 40} w={52} h={26} text={ty} stroke="var(--s-blue)" size={10} />
          </g>
        ))}
        <Txt x={180} y={150} size={10}>можно поставить в if</Txt>
      </G>
    </Steps>
  );
}
