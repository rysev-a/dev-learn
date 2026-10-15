import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 4, слайд 7: включения и исключения для двух множеств:
   40 + 30 − 10 = 60; UNION убирает дубликаты. */

const LABELS = ["Перекрытие", "Формула", "40 + 30 − 10", "UNION"];
const CAPTION = [
  "Переходим к включениям и исключениям — честному счёту по перекрывающимся группам",
  "|A ∪ B| = |A| + |B| − |A ∩ B|: общая часть посчитана дважды, вычитаем один раз",
  "Аудиокурс начали 40 человек, вебинар смотрели 30, оба — 10: охвачено 60, а не 70",
  "Объединение в базе данных не возвращает дубликаты — оно молча делает то же за вас",
];

export default function C4Incl2({ cues }) {
  const ctl = useSteps(cues || [5.2, 11.8, 22.8], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 2 ? 1 : 0}>
        <defs>
          <clipPath id="i2-a">
            <circle cx="150" cy="70" r="46" />
          </clipPath>
        </defs>
        <circle cx="150" cy="70" r="46" className="a-ring a" />
        <circle cx="210" cy="70" r="46" className="a-ring b" />
        <g clipPath="url(#i2-a)">
          <circle cx="210" cy="70" r="46" className="a-t" style={{ fill: "var(--s-amber)", fillOpacity: step >= 1 ? 0.4 : 0.15 }} />
        </g>
        <Txt x="124" y="74" mono size={13}>30</Txt>
        <Txt x="180" y="74" mono size={13} color="var(--s-amber)">10</Txt>
        <Txt x="236" y="74" mono size={13}>20</Txt>
        <Txt x="110" y="22" color="var(--s-blue)">аудиокурс · 40</Txt>
        <Txt x="250" y="22" color="var(--s-accent)">вебинар · 30</Txt>
        <Txt x="180" y="144" mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">|A ∪ B| = |A| + |B| − |A ∩ B|</Txt>
        <Txt x="180" y="144" mono size={14} o={step === 2 ? 1 : 0} color="var(--s-accent)">40 + 30 − 10 = 60</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <Txt x="90" y="22" mono size={10}>A</Txt>
        <Txt x="270" y="22" mono size={10}>B</Txt>
        {[1, 2].map((v, i) => (
          <Pill key={`a${v}`} x={90} y={42 + i * 28} w={44} text={v} stroke="var(--s-blue)" />
        ))}
        {[2, 3].map((v, i) => (
          <Pill key={`b${v}`} x={270} y={42 + i * 28} w={44} text={v} stroke="var(--s-accent)" />
        ))}
        <Txt x="180" y="78" mono size={11}>UNION</Txt>
        {[1, 2, 3].map((v, i) => (
          <Pill key={`u${v}`} x={120 + i * 60} y={120} w={44} text={v} stroke="var(--s-amber)" />
        ))}
        <Txt x="180" y="152" size={9.5}>2 встречается в обоих, но в результате — один раз</Txt>
      </G>
    </Steps>
  );
}
