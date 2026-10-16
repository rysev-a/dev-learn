import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 5: независимость — два кубика, произведение; независимость
   не то же, что несовместность. */

const LABELS = ["Независимые", "Два кубика", "Произведение", "Не несовместны", "Информация"];
const CAPTION = [
  "События независимы, если знание об одном ничего не меняет в оценке другого",
  "Два кубика: выпала шестёрка на первом — про второй мы по-прежнему знаем лишь «одна шестая»",
  "Для независимых событий вероятность обоих — произведение: 1/6 · 1/6 = 1/36",
  "Не путайте независимость и несовместность: «чётное» и «три» несовместны, но зависимы",
  "Зависимость — про информацию, а не про одновременность",
];

export default function C10Independent({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.6, 11.8, 17.5, 27.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">P(B | A) = P(B)</Txt>
      <G o={step === 1 || step === 2 ? 1 : 0}>
        {Array.from({ length: 36 }, (_, i) => {
          const r = Math.floor(i / 6);
          const c = i % 6;
          const rowHit = r === 5;
          const cell = step === 2 && r === 5 && c === 5;
          return <rect key={i} className="a-t" x={104 + c * 24} y={14 + r * 24} width="20" height="20" rx="4" style={{ fill: cell ? "var(--s-amber)" : rowHit ? "var(--s-green)" : "var(--s-panel2)", fillOpacity: cell ? 0.6 : 1, stroke: cell ? "var(--s-amber)" : rowHit ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.2 }} />;
        })}
        <Txt x={60} y={132} mono size={10}>1-й кубик ↓</Txt>
        <Txt x={60} y={146} mono size={10} color="var(--s-accent)">выпала 6</Txt>
        <Txt x={290} y={80} mono size={11} o={step === 1 ? 1 : 0}>вторая 6:</Txt>
        <Txt x={290} y={96} mono size={13} o={step === 1 ? 1 : 0} color="var(--s-accent)">всё ещё 1/6</Txt>
        <Txt x={290} y={86} mono size={14} o={step === 2 ? 1 : 0} color="var(--s-amber)">1/36</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <circle cx="130" cy="64" r="40" className="a-ring a" />
        <circle cx="230" cy="64" r="40" className="a-ring b" />
        <Txt x={130} y={60} size={9.5}>чётное</Txt>
        <Txt x={130} y={76} mono size={11}>2 4 6</Txt>
        <Txt x={230} y={60} size={9.5}>три</Txt>
        <Txt x={230} y={76} mono size={11}>3</Txt>
        <Txt x={180} y={130} mono size={11} o={step === 3 ? 1 : 0} color="var(--s-amber)">вместе не бывают — но зависимы</Txt>
        <Txt x={180} y={130} mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-accent)">узнали «три» → точно не чётное</Txt>
      </G>
    </Steps>
  );
}
