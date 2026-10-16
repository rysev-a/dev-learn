import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 1: рекурсия есть у всех; откуда знать, что она
   работает для всех входов — индукция; заодно сортировки. */

const LABELS = ["Глава", "Рекурсия", "Вопрос", "Индукция", "Время"];
const CAPTION = [
  "Индукция и рекуррентности",
  "Рекурсию вы пишете чуть ли не каждую неделю: обход дерева, вложенный json, спуск по каталогам",
  "Но откуда знать, что она сработает для всех входов, а не только для проверенных?",
  "Ответ даёт математическая индукция: бесконечное число случаев — за два шага",
  "Заодно честно посчитаем, сколько времени едят быстрые сортировки",
];

export default function C7Intro({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.5, 10.5, 18.5, 25.2], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        {[
          ["обход дерева", "tree"],
          ["вложенный json", "{…{…}}"],
          ["спуск по каталогам", "/a/b/c"],
        ].map(([t, f], i) => (
          <g key={t}>
            <Pill x={100} y={36 + i * 38} w={170} h={28} text={t} stroke="var(--s-accent)" size={10.5} />
            <Txt x={250} y={40 + i * 38} anchor="start" mono size={11} color="var(--s-amber)">{f}</Txt>
          </g>
        ))}
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[0, 1, 2].map((i) => (
          <Dot key={i} x={50 + i * 36} y={70} r={12} text="✓" stroke="var(--s-accent)" fill="var(--s-green)" size={10} />
        ))}
        {Array.from({ length: 8 }, (_, i) => (
          <Dot key={i} x={170 + i * 22} y={70} r={8} text="?" stroke="var(--s-muted)" size={9} />
        ))}
        <Txt x={180} y={116} mono size={13} color="var(--s-amber)">проверили 3 — а их бесконечно много</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={100} y={66} w={110} h={40} text="база" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x={180} y={70} mono size={18}>+</Txt>
        <Pill x={260} y={66} w={110} h={40} text="переход" stroke="var(--s-blue)" size={13} />
        <Txt x={180} y={130} mono size={13} color="var(--s-accent)">⇒ верно для всех n</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {([
          ["n log n", 120, "var(--s-accent)"],
          ["n²", 220, "var(--s-red)"],
        ] as const).map(([t, w, c], i) => (
          <g key={t}>
            <text x="30" y={58 + i * 40} className="a-mono" style={{ fontSize: 13, fill: c }}>{t}</text>
            <rect x="100" y={44 + i * 40} width={w} height="20" rx="5" style={{ fill: c, fillOpacity: 0.35, stroke: c }} />
          </g>
        ))}
        <Txt x={180} y={140} size={10}>быстрые сортировки: сколько времени они едят</Txt>
      </G>
    </Steps>
  );
}
