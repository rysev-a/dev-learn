import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 9: частичный порядок. Делимость на {1, 2, 3, 6}: 2 и 3
   несравнимы; дерево зависимостей; топологическая сортировка. */

const LABELS = ["Порядок", "Несравнимы", "Зависимости", "Сортировка"];
const CAPTION = [
  "Рефлексивность + антисимметричность + транзитивность — частичный порядок, как «≤»",
  "«Частичный»: бывают элементы, которые никак не сравнить — 2 и 3 не делятся друг на друга",
  "В дереве зависимостей пакеты из разных ветвей не упорядочены между собой",
  "Топологическая сортировка вытягивает частичный порядок в линию сборки",
];
// пакеты: [имя, x в графе, y в графе, x в линии]
const PK = [
  ["core", 180, 120, 40],
  ["utils", 100, 70, 130],
  ["net", 260, 70, 220],
  ["app", 180, 24, 310],
];
const EDGES = [
  [0, 1],
  [0, 2],
  [1, 3],
  [2, 3],
];

export default function C2Partial({ cues }) {
  const ctl = useSteps(cues || [9.4, 14.7, 21.0], 3000);
  const { step } = ctl;
  const hasse = step <= 1;
  const line = step === 3;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* делимость */}
      <G o={hasse ? 1 : 0}>
        {[
          [180, 120, "1"],
          [110, 72, "2"],
          [250, 72, "3"],
          [180, 24, "6"],
        ].map(([x, y, t]) => (
          <Pill key={t} x={x} y={y} w={34} text={t} stroke={step === 1 && (t === "2" || t === "3") ? "var(--s-red)" : "var(--s-accent)"} />
        ))}
        <Arrow x1={160} y1={110} x2={128} y2={86} c="g" />
        <Arrow x1={200} y1={110} x2={232} y2={86} c="g" />
        <Arrow x1={128} y1={58} x2={160} y2={34} c="g" />
        <Arrow x1={232} y1={58} x2={200} y2={34} c="g" />
        <Txt x="180" y="156" mono o={step === 0 ? 1 : 0} color="var(--s-accent)">a ≼ b: «a делит b»</Txt>
        <Txt x="180" y="72" o={step === 1 ? 1 : 0} mono color="var(--s-red)" size={14}>?</Txt>
        <Arrow x1={130} y1={72} x2={228} y2={72} c="r" dash="3 4" o={step === 1 ? 0.7 : 0} both />
        <Txt x="180" y="156" mono o={step === 1 ? 1 : 0} color="var(--s-red)">2 и 3 несравнимы</Txt>
      </G>

      {/* пакеты → линия */}
      {EDGES.map(([a, b], i) => (
        <Arrow
          key={i}
          x1={line ? PK[a][3] + 22 : PK[a][1]}
          y1={line ? 90 : PK[a][2] - 12}
          x2={line ? PK[b][3] - 22 : PK[b][1]}
          y2={line ? 90 : PK[b][2] + 12}
          c="m"
          o={step === 2 ? 1 : 0}
        />
      ))}
      {PK.map(([t, x, y, lx], i) => (
        <Pill
          key={t}
          x={line ? lx : x}
          y={line ? 90 : y}
          w={58}
          text={t}
          o={step >= 2 ? 1 : 0}
          stroke={step === 2 && (t === "utils" || t === "net") ? "var(--s-red)" : "var(--s-accent)"}
        />
      ))}
      {PK.map(([t, , , lx], i) => (
        <Txt key={t} x={lx} y="118" o={line ? 1 : 0} mono color="var(--s-accent)">{i + 1}</Txt>
      ))}
      {[0, 1, 2].map((i) => (
        <Arrow key={i} x1={PK[i][3] + 30} y1={90} x2={PK[i + 1][3] - 30} y2={90} c="g" o={line ? 1 : 0} />
      ))}
      <Txt x="180" y="156" o={step === 2 ? 1 : 0} color="var(--s-red)">utils и net не упорядочены между собой</Txt>
      <Txt x="180" y="156" o={line ? 1 : 0} color="var(--s-accent)">порядок сборки: core → utils → net → app</Txt>
    </Steps>
  );
}
