import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 1: вероятность — честный способ думать о неопределённости;
   повседневные случайности; план главы. */

const LABELS = ["Финал", "Честно", "Случайности", "План", "Спам"];
const CAPTION = [
  "Вероятность и теорема Байеса — финальная глава курса",
  "Это самый честный способ мыслить в мире, где ничто не гарантировано",
  "Кэш попадает или промахивается, фича выигрывает или нет, алерт настоящий или ложный — всё это можно рассуждать строго",
  "Разберём классическую вероятность, условную и формулу Байеса — и подведём итог всего пути",
  "Обещаю: спам-фильтр в конце будет заслуженным",
];

export default function C10Intro({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.8, 10.2, 20.7, 26.7], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={26} o={step === 0 ? 1 : 0} color="var(--s-accent)">P ( событие )</Txt>
      <Txt x={180} y={80} mono size={20} o={step === 1 ? 1 : 0} color="var(--s-accent)">гарантий нет — есть доли</Txt>
      <G o={step === 2 ? 1 : 0}>
        {([
          ["кэш", "попал", "промах"],
          ["фича", "выиграла", "нет"],
          ["алерт", "настоящий", "ложный"],
        ] as const).map(([t, a, b], i) => (
          <g key={t}>
            <text x="30" y={44 + i * 38} className="a-mono" style={{ fontSize: 12 }}>{t}</text>
            <Pill x={150} y={40 + i * 38} w={84} h={24} text={a} stroke="var(--s-accent)" size={10} />
            <Txt x={212} y={44 + i * 38} mono size={11}>или</Txt>
            <Pill x={270} y={40 + i * 38} w={84} h={24} text={b} stroke="var(--s-red)" size={10} />
          </g>
        ))}
      </G>
      <G o={step === 3 ? 1 : 0}>
        {["классическая", "условная", "формула Байеса"].map((t, i) => (
          <Pill key={t} x={70 + i * 110} y={70} w={96} h={50} text={t} stroke="var(--s-accent)" size={10} />
        ))}
        <Txt x={180} y={124} size={10}>и итог всего пути</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={180} y={70} w={220} h={50} text="✉ спам-фильтр" stroke="var(--s-amber)" fill="var(--s-panel2)" size={16} />
        <Txt x={180} y={116} size={10}>в конце главы — заслуженный</Txt>
      </G>
    </Steps>
  );
}
