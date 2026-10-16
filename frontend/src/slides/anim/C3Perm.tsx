import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 3, слайд 6: перестановки. 3! = 6 порядков, 10 докладов,
   коммивояжёр и 50 городов. */

const LABELS = ["n!", "Доклады", "Коммивояжёр", "50 городов"];
const CAPTION = [
  "Перестановка — способ расставить n предметов по местам; способов ровно n!",
  "Десять докладов на конференции — 10! вариантов расписания, больше 3,5 миллионов",
  "Коммивояжёр: обойти все города по самому короткому маршруту — вариантов столько же, сколько перестановок",
  "При 50 городах полный перебор не закончится никогда — отсюда приближённые алгоритмы",
];
const ORDERS = ["abc", "acb", "bac", "bca", "cab", "cba"];
const CITY: [number, number][] = [
  [60, 50],
  [140, 30],
  [250, 54],
  [300, 108],
  [190, 124],
  [86, 112],
];

export default function C3Perm({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.9, 13.7, 23.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {ORDERS.map((o, i) => (
          <g key={o} className="a-t" style={{ opacity: step === 0 ? 1 : 0, transitionDelay: `${i * 160}ms` }}>
            {o.split("").map((ch, j) => (
              <Pill
                key={j}
                x={64 + (i % 3) * 112 + j * 30}
                y={36 + Math.floor(i / 3) * 40}
                w={26}
                text={ch}
                stroke={["var(--s-blue)", "var(--s-amber)", "var(--s-accent)"][ch.charCodeAt(0) - 97]}
              />
            ))}
          </g>
        ))}
        <Txt x={180} y={140} mono size={15} color="var(--s-accent)">3! = 3 · 2 · 1 = 6</Txt>
      </G>

      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 10 }, (_, i) => (
          <Pill key={i} x={36 + i * 32} y={52} w={28} text={`Д${i + 1}`} stroke="var(--s-blue)" size={9} />
        ))}
        <Txt x={180} y={30}>10 слотов в расписании</Txt>
        <Txt x={180} y={112} mono size={16} color="var(--s-amber)">10! = 3 628 800</Txt>
        <Txt x={180} y={138}>расписаний</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        {CITY.map(([x, y], i) => (
          <g key={i}>
            <line x1={x} y1={y} x2={CITY[(i + 1) % 6]![0]} y2={CITY[(i + 1) % 6]![1]} style={{ stroke: "var(--s-accent)", strokeWidth: 1.8, strokeDasharray: "5 3" }} />
          </g>
        ))}
        {CITY.map(([x, y], i) => (
          <Dot key={i} x={x} y={y} text={i + 1} stroke="var(--s-amber)" />
        ))}
        <Txt x={180} y={154} mono size={12} color="var(--s-accent)">n городов → порядка n! маршрутов</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        <Txt x={180} y={58} mono size={26} color="var(--s-red)">50! ≈ 3 · 10⁶⁴</Txt>
        <Txt x={180} y={92}>маршрутов — за разумное время не перебрать</Txt>
        <Pill x={180} y={124} w={230} h={26} text="выход: приближённые алгоритмы" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
      </G>
    </Steps>
  );
}
