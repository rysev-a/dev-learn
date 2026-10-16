import { Arrow, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 2: лестница — база и переход покрывают все ступени. */

const LABELS = ["Лестница", "Два факта", "Подъём", "Все ступени"];
const CAPTION = [
  "Начнём с лестницы: бесконечная лестница и два факта",
  "На первую ступень встать можно (база); с любой ступени можно перешагнуть на следующую (переход)",
  "Первый факт ставит на первую ступень, второй протаскивает всё выше и выше",
  "Эти два факта вместе покрывают все ступени сразу — больше для индукции ничего не нужно",
];
const N = 8;
const sx = (i: number) => 30 + i * 36;
const sy = (i: number) => 126 - i * 11;

export default function C7Stairs({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [1.7, 10.3, 19.3], 3000);
  const { step } = ctl;
  const reach = step === 0 ? 0 : step === 1 ? 1 : N;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {Array.from({ length: N }, (_, i) => (
        <g key={i}>
          <rect className="a-t" x={sx(i)} y={sy(i)} width="34" height={140 - sy(i)} rx="3" style={{ fill: i < reach ? "var(--s-green)" : "var(--s-panel2)", stroke: i < reach ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.4, transitionDelay: step === 2 ? `${i * 260}ms` : "0ms" }} />
          <text x={sx(i) + 17} y={sy(i) + 14} textAnchor="middle" className="a-mono" style={{ fontSize: 10 }}>{i + 1}</text>
        </g>
      ))}
      <Txt x={330} y={60} mono size={14}>…</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Txt x={62} y={102} mono size={11} color="var(--s-accent)">база</Txt>
        <Arrow x1={110} y1={100} x2={152} y2={94} c="b" />
        <Arrow x1={182} y1={86} x2={222} y2={80} c="b" />
        <Txt x={190} y={62} mono size={11} color="var(--s-blue)">k → k + 1</Txt>
      </G>
      <Txt x={180} y={154} mono size={12} o={step === 3 ? 1 : 0} color="var(--s-accent)">база + переход = любая ступень</Txt>
    </Steps>
  );
}
