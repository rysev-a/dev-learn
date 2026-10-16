import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 10: быстрая сортировка — лучший случай n log n, худший
   n², случайный опорный элемент. */

const LABELS = ["Быстрая", "Ровно пополам", "Крайний", "Худший случай", "Случайный", "Рекуррентности"];
const CAPTION = [
  "Быстрая сортировка живёт по тому же закону с одной оговоркой",
  "Если опорный делит массив примерно пополам — снова n log n: те же уровни, та же линейная работа на уровень",
  "Если опорный каждый раз крайний — деления нет, n элементов превращаются в n − 1, и уровней становится n",
  "Худший случай — n · n: тот самый квадрат вложенных циклов",
  "Библиотеки выбирают опорный случайно — чтобы провал стал невероятным",
  "Рекуррентности позволяют просчитать оба сценария до запуска кода",
];

export default function C7Quick({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.9, 11.5, 21.0, 25.1, 31.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">quicksort</Txt>
      <G o={step === 1 ? 1 : 0}>
        {[1, 2, 4, 8].map((c, l) =>
          Array.from({ length: c }, (_, j) => (
            <rect key={`${l}${j}`} x={20 + j * (320 / c) + 2} y={22 + l * 28} width={320 / c - 4} height="20" rx="4" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.2 }} />
          )),
        )}
        <Txt x={180} y={148} mono size={13} color="var(--s-accent)">log n уровней × n = n log n</Txt>
      </G>
      <G o={step === 2 || step === 3 ? 1 : 0}>
        {Array.from({ length: 8 }, (_, l) => (
          <g key={l}>
            <rect x={20} y={14 + l * 16} width={300 - l * 36} height="12" rx="3" style={{ fill: "var(--s-red)", fillOpacity: 0.3, stroke: "var(--s-red)", strokeWidth: 1.1 }} />
            <rect x={20 + 300 - l * 36} y={14 + l * 16} width="14" height="12" rx="3" style={{ fill: "var(--s-amber)", fillOpacity: 0.5, stroke: "var(--s-amber)" }} />
          </g>
        ))}
        <Txt x={180} y={152} mono size={13} o={step === 2 ? 1 : 0} color="var(--s-red)">n уровней: n, n−1, n−2, …</Txt>
        <Txt x={180} y={152} mono size={13} o={step === 3 ? 1 : 0} color="var(--s-red)">n + (n−1) + … ≈ n² / 2 → O(n²)</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {["pivot = random()", "провал — крайне редко"].map((t, i) => (
          <Pill key={t} x={180} y={50 + i * 44} w={220} h={30} text={t} stroke={i ? "var(--s-amber)" : "var(--s-accent)"} fill={i ? "var(--s-panel2)" : "var(--s-green)"} color={i ? "var(--s-text)" : "var(--s-accent)"} size={11} />
        ))}
        <Txt x={180} y={130} mono size={11} o={step === 4 ? 1 : 0}>не «всегда быстро», а «медленно — невероятно»</Txt>
        <Txt x={180} y={130} mono size={11} o={step >= 5 ? 1 : 0} color="var(--s-accent)">T(n) = 2T(n/2) + n  и  T(n) = T(n−1) + n</Txt>
      </G>
    </Steps>
  );
}
