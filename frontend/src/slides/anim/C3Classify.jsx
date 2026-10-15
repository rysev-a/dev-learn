import { Arrow, Dot, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 11: двойной счёт и классификация. Упорядоченные пары
   дают лишние дубли, три друга — ручная проверка формулы, дерево выбора
   «какой счётчик». */

const LABELS = ["Ошибка", "Пример", "Проверка", "Классификация"];
const CAPTION = [
  "Главная ошибка новичка — двойной счёт: порядок учтён там, где его нет",
  "Лекарство: возьмите крошечный пример — три друга, выбрать двоих",
  "Руками получается три пары, и C(3, 2) = 3 — формулы сходятся",
  "Перед расчётом классифицируйте задачу — половина решения уже готова",
];
const F = [
  [180, 36, "А"],
  [110, 112, "Б"],
  [250, 112, "В"],
];

export default function C3Classify({ cues }) {
  const ctl = useSteps(cues || [6.6, 10.4, 19.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {["АБ", "БА", "АВ", "ВА", "БВ", "ВБ"].map((t, i) => (
          <Pill key={t} x={50 + (i % 2) * 70} y={34 + Math.floor(i / 2) * 32} w={56} text={t} stroke={i % 2 ? "var(--s-red)" : "var(--s-accent)"} />
        ))}
        <Txt x="236" y="60" mono size={14} color="var(--s-red)">6 пар?</Txt>
        <Txt x="236" y="80" mono size={14} color="var(--s-accent)">на деле 3</Txt>
        <Txt x="180" y="150">«АБ» и «БА» — один и тот же выбор</Txt>
      </G>
      <G o={step >= 1 && step <= 2 ? 1 : 0}>
        <Arrow x1={F[0][0] - 8} y1={F[0][1] + 10} x2={F[1][0] + 8} y2={F[1][1] - 10} c="g" o={step === 2 ? 1 : 0} both />
        <Arrow x1={F[0][0] + 8} y1={F[0][1] + 10} x2={F[2][0] - 8} y2={F[2][1] - 10} c="g" o={step === 2 ? 1 : 0} both />
        <Arrow x1={F[1][0] + 16} y1={F[1][1]} x2={F[2][0] - 16} y2={F[2][1]} c="g" o={step === 2 ? 1 : 0} both />
        {F.map(([x, y, t]) => (
          <Dot key={t} x={x} y={y} r={14} text={t} stroke="var(--s-blue)" />
        ))}
        <Txt x="60" y="70" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-accent)">руками: 3</Txt>
        <Txt x="300" y="70" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-accent)">C(3,2) = 3 ✓</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={180} y={22} w={220} h={22} text="что считаем?" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10.5} />
        {[
          [60, "группы не пересекаются → сумма +", "y"],
          [180, "независимые шаги → произведение ×", "g"],
          [300, "выбор с порядком / без?", "b"],
        ].map(([x, t, c]) => (
          <Arrow key={x} x1={180} y1={34} x2={x} y2={62} c={c} />
        ))}
        <Pill x={60} y={76} w={96} h={30} text="сумма" stroke="var(--s-amber)" size={10} />
        <Pill x={180} y={76} w={96} h={30} text="произведение" stroke="var(--s-accent)" size={10} />
        <Pill x={300} y={76} w={96} h={30} text="выбор k из n" stroke="var(--s-blue)" size={10} />
        <Arrow x1={300} y1={92} x2={256} y2={122} c="b" />
        <Arrow x1={300} y1={92} x2={344} y2={122} c="b" />
        <Pill x={250} y={134} w={96} h={24} text="порядок → A, n!" stroke="var(--s-amber)" size={9} />
        <Pill x={344} y={134} w={30} h={24} text="C" stroke="var(--s-accent)" size={11} />
      </G>
    </Steps>
  );
}
