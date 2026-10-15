import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 10, слайд 6: условная вероятность — сжатие мира до случаев, где B
   произошло; пасмурно и дождь. */

const LABELS = ["Условная", "Пересчёт", "Пасмурно", "Формула", "Всё о будущем"];
const CAPTION = [
  "Главный инструмент главы — условная вероятность",
  "Вероятность события, пересчитанная с учётом того, что другое уже случилось",
  "Пасмурно — вероятность дождя выше, чем в ясный день, хотя климат тот же",
  "P(A | B) = P(A ∩ B) / P(B): сжимаем мир до случаев, где B произошло, и смотрим долю A",
  "Почти всё, что вы говорите о будущем, — условные вероятности; просто условие обычно не проговаривают",
];

export default function C10Conditional({ cues }) {
  const ctl = useSteps(cues || [3.8, 8.3, 12.9, 23.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={26} o={step === 0 ? 1 : 0} color="var(--s-accent)">P ( A | B )</Txt>
      <G o={step === 1 ? 1 : 0}>
        <rect x="40" y="20" width="130" height="100" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <Txt x="105" y="76" mono size={12}>весь мир</Txt>
        <Txt x="190" y="76" mono size={16} color="var(--s-accent)">→</Txt>
        <rect x="210" y="40" width="100" height="60" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <Txt x="260" y="76" mono size={12} color="var(--s-accent)">B уже случилось</Txt>
        <Txt x="180" y="148" size={10}>пересчитываем доли внутри нового мира</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[
          ["вообще", 20, "var(--s-blue)"],
          ["пасмурно", 60, "var(--s-red)"],
        ].map(([t, v, c], i) => (
          <g key={t}>
            <text x="30" y={52 + i * 40} className="a-mono" style={{ fontSize: 11 }}>{t}</text>
            <rect className="a-t" x="110" y={38 + i * 40} width={step === 2 ? v * 3 : 0} height="22" rx="5" style={{ fill: c, fillOpacity: 0.35, stroke: c, transitionDelay: `${i * 300}ms` }} />
            <text x={118 + v * 3} y={54 + i * 40} className="a-mono" style={{ fontSize: 11, fill: c }}>{`P(дождь${i ? " | пасмурно" : ""}) = ${v} %`}</text>
          </g>
        ))}
        <Txt x="180" y="140" size={10}>иллюстративные числа: климат тот же</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <defs>
          <clipPath id="c10c-b">
            <circle cx="210" cy="64" r="44" />
          </clipPath>
        </defs>
        <circle cx="150" cy="64" r="44" className="a-ring a" />
        <circle cx="210" cy="64" r="44" className="a-ring b" style={{ strokeWidth: 3 }} />
        <g clipPath="url(#c10c-b)">
          <circle cx="150" cy="64" r="44" style={{ fill: "var(--s-amber)", fillOpacity: 0.45 }} />
        </g>
        <Txt x="124" y="68" mono size={12}>A</Txt>
        <Txt x="240" y="68" mono size={12}>B</Txt>
        <Txt x="180" y="140" mono size={13} color="var(--s-accent)">P(A|B) = P(A∩B) / P(B)</Txt>
        <Txt x="180" y="156" size={9.5} o={step >= 4 ? 1 : 0} color="var(--s-amber)">условие обычно остаётся «за кадром»</Txt>
      </G>
    </Steps>
  );
}
