import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 10: пренебрежение базовой частотой; практические правила:
   пороги алертов, каскад фильтров. */

const LABELS = ["Имя ловушки", "Что оцениваем", "Правила", "Редкий алерт", "Каскад"];
const CAPTION = [
  "У ловушки есть имя: пренебрежение базовой частотой",
  "Люди неплохо оценивают, насколько свидетельство характерно для причины, но проваливаются на вопросе, насколько причина вообще распространена",
  "Отсюда практические правила",
  "Алерт, срабатывающий редко на редкое событие, почти всегда ложный — пороги настраивайте с учётом априорной частоты",
  "Редкое ищут каскадом: дешёвый грубый фильтр, потом дорогой точный анализ",
];

export default function C10BaseRate({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.9, 12.8, 15.0, 22.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={18} o={step === 0 ? 1 : 0} color="var(--s-red)">base rate neglect</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={100} y={60} w={150} h={50} text="насколько характерно" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10.5} />
        <Txt x={100} y={96} size={9.5} color="var(--s-accent)">оцениваем верно ✓</Txt>
        <Pill x={260} y={60} w={150} h={50} text="насколько распространено" stroke="var(--s-red)" size={10.5} />
        <Txt x={260} y={96} size={9.5} color="var(--s-red)">забываем ✗</Txt>
      </G>
      <Txt x={180} y={80} mono size={20} o={step === 2 ? 1 : 0} color="var(--s-accent)">правила для практика</Txt>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={110} y={50} w={150} h={34} text="редкое событие" stroke="var(--s-amber)" size={11} />
        <Txt x={196} y={54} mono size={14}>+</Txt>
        <Pill x={270} y={50} w={150} h={34} text="алерт «на всякий»" stroke="var(--s-amber)" size={11} />
        <Txt x={180} y={104} mono size={14} color="var(--s-red)">почти всегда ложная тревога</Txt>
        <Txt x={180} y={130} size={10}>пороги — с учётом априорной частоты</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {([
          ["100 000", "грубый фильтр", 300],
          ["1 000", "точнее", 190],
          ["100", "дорогой анализ", 90],
        ] as const).map(([n, t, w], i) => (
          <g key={t}>
            <rect x={180 - w / 2} y={24 + i * 40} width={w} height="30" rx="8" style={{ fill: "var(--s-panel2)", stroke: ["var(--s-blue)", "var(--s-amber)", "var(--s-accent)"][i], strokeWidth: 1.6 }} />
            <text x="180" y={44 + i * 40} textAnchor="middle" className="a-mono" style={{ fontSize: 10.5 }}>{`${n} · ${t}`}</text>
          </g>
        ))}
      </G>
    </Steps>
  );
}
