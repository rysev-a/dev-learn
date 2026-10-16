import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 4: события и арифметика: P(A∪B) = P(A)+P(B)−P(A∩B);
   запись событий словами. */

const LABELS = ["События", "Или", "И", "В коде", "Словами"];
const CAPTION = [
  "Дальше — события и арифметика над ними",
  "Вероятность «первое или второе» — сумма вероятностей минус вероятность обоих: общие случаи иначе посчитались бы дважды",
  "Вероятность «оба» зависит от связи между событиями — об этом следующий разговор",
  "«Ошибка в базе или в сети» — объединение; «ошибка в базе и ретрай исчерпан» — пересечение",
  "Стоит записать событие словами — и формула собирается сама",
];

export default function C10Events({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.9, 12.8, 19.0, 26.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <defs>
        <clipPath id="c10-a">
          <circle cx="150" cy="70" r="46" />
        </clipPath>
      </defs>
      <G o={step <= 2 ? 1 : 0}>
        <circle cx="150" cy="70" r="46" className="a-ring a" />
        <circle cx="210" cy="70" r="46" className="a-ring b" />
        <circle className="a-t" cx="150" cy="70" r="46" style={{ fill: "var(--s-accent)", fillOpacity: step === 1 ? 0.25 : 0 }} />
        <circle className="a-t" cx="210" cy="70" r="46" style={{ fill: "var(--s-accent)", fillOpacity: step === 1 ? 0.25 : 0 }} />
        <g clipPath="url(#c10-a)">
          <circle className="a-t" cx="210" cy="70" r="46" style={{ fill: "var(--s-amber)", fillOpacity: step >= 1 ? 0.45 : 0 }} />
        </g>
        <Txt x={124} y={74} mono size={13}>A</Txt>
        <Txt x={236} y={74} mono size={13}>B</Txt>
        <Txt x={180} y={74} mono size={11} o={step >= 1 ? 1 : 0} color="var(--s-amber)">A∩B</Txt>
        <Txt x={180} y={148} mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">P(A∪B) = P(A) + P(B) − P(A∩B)</Txt>
        <Txt x={180} y={148} mono size={12} o={step === 2 ? 1 : 0} color="var(--s-amber)">P(A∩B) = ?  — зависит от связи</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {[
          ["ошибка в базе  ИЛИ  в сети", "A ∪ B", "var(--s-accent)"],
          ["ошибка в базе  И  ретрай исчерпан", "A ∩ B", "var(--s-amber)"],
        ].map(([t, f, c], i) => (
          <g key={f}>
            <rect x="30" y={30 + i * 50} width="300" height="38" rx="10" style={{ fill: "var(--s-panel2)", stroke: c, strokeWidth: 1.5 }} />
            <text x="46" y={54 + i * 50} className="a-cap" style={{ fontSize: 10, fill: "var(--s-text)" }}>{t}</text>
            <text x="316" y={54 + i * 50} textAnchor="end" className="a-mono" style={{ fontSize: 13, fill: c }}>{f}</text>
          </g>
        ))}
        <Txt x={180} y={148} size={10} o={step >= 4 ? 1 : 0} color="var(--s-accent)">слова → операция → формула</Txt>
      </G>
    </Steps>
  );
}
