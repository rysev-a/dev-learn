import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 9: сортировка слиянием — T(n) = 2T(n/2) + n, уровни
   дерева, n работы на уровень, log n уровней ⇒ n log n. */

const LABELS = ["Слияние", "Устройство", "T(n)", "Уровни", "Работа", "n log n"];
const CAPTION = [
  "Возьмём сортировку слиянием",
  "Разделить пополам, отсортировать обе половины, слить результаты за линейное время",
  "Время на n элементах — две половины плюс n на слияние: T(n) = 2T(n/2) + n",
  "Массив делится на два куска по n/2, потом на четыре по n/4, …, до одного элемента — примерно log n уровней",
  "На каждом уровне суммарная работа по всем кусочкам остаётся n",
  "log n уровней по n работы — n log n; это доказано, а не замерено",
];
const LV = [1, 2, 4, 8];

export default function C7Merge({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.2, 8.4, 15.7, 25.2, 29.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">merge sort</Txt>
      <G o={step === 1 ? 1 : 0}>
        {([
          ["1", "разделить", 60],
          ["2", "сортировать", 180],
          ["3", "слить: O(n)", 300],
        ] as const).map(([n, t, x]) => (
          <Pill key={n} x={x} y={76} w={104} h={50} text={`${n}. ${t}`} stroke="var(--s-accent)" size={10.5} />
        ))}
      </G>
      <Txt x={180} y={80} mono size={22} o={step === 2 ? 1 : 0} color="var(--s-accent)">T(n) = 2·T(n/2) + n</Txt>
      <G o={step >= 3 ? 1 : 0}>
        {LV.map((c, l) => (
          <g key={l}>
            {Array.from({ length: c }, (_, j) => {
              const w = 320 / c - 4;
              return (
                <rect key={j} className="a-t" x={20 + j * (320 / c) + 2} y={22 + l * 26} width={w} height="20" rx="4" style={{ fill: step >= 4 ? "var(--s-green)" : "var(--s-panel2)", stroke: step >= 4 ? "var(--s-accent)" : "var(--s-border)", strokeWidth: 1.2, opacity: step >= 3 ? 1 : 0, transitionDelay: `${l * 220}ms` }} />
              );
            })}
            <text x="346" y={36 + l * 26} className="a-mono a-t" style={{ fontSize: 9, fill: "var(--s-accent)", opacity: step >= 4 ? 1 : 0 }}>n</text>
          </g>
        ))}
        <Txt x={14} y={136} anchor="start" size={9.5} o={step === 3 ? 1 : 0}>уровни: n → n/2 → n/4 → …</Txt>
        <Txt x={14} y={136} anchor="start" size={9.5} o={step === 4 ? 1 : 0} color="var(--s-accent)">каждый уровень: суммарно n</Txt>
        <Txt x={180} y={152} mono size={14} o={step >= 5 ? 1 : 0} color="var(--s-accent)">log n уровней · n = n log n</Txt>
      </G>
    </Steps>
  );
}
