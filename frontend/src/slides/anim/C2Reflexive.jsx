import { Arrow, G, Loop, Matrix, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 2, слайд 5: рефлексивность. Диагональ матрицы: «равно» заполняет
   её целиком, «меньше» оставляет пустой; самоссылка в таблице сотрудников. */

const LABELS = ["Свойство", "Равно", "Меньше", "В схеме"];
const CAPTION = [
  "Рефлексивность: каждый элемент связан с самим собой — вся диагональ отмечена",
  "«Равно» рефлексивно: любое число равно самому себе",
  "«Меньше» рефлексивным не будет: число не меньше самого себя",
  "В схеме данных: сотрудник может ссылаться на себя через руководителя",
];
const N = ["1", "2", "3", "4"];

export default function C2Reflexive({ cues }) {
  const ctl = useSteps(cues || [5.7, 9.3, 14.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Matrix
        x={130}
        y={34}
        rows={N}
        cols={N}
        cell={26}
        o={step <= 2 ? 1 : 0}
        mark={(r, c) =>
          step === 0 || step === 1
            ? r === c
              ? "g"
              : null
            : step === 2
              ? r < c
                ? "y"
                : r === c
                  ? "r"
                  : null
              : null
        }
      />
      <Txt x="60" y="46" o={step === 0 ? 1 : 0} mono color="var(--s-accent)">a R a</Txt>
      <Txt x="60" y="46" o={step === 1 ? 1 : 0} mono color="var(--s-accent)">a = a ✓</Txt>
      <Txt x="60" y="46" o={step === 2 ? 1 : 0} mono color="var(--s-red)">a &lt; a ✗</Txt>
      <Txt x="180" y="152" o={step === 2 ? 1 : 0} color="var(--s-red)">диагональ пуста — не рефлексивно</Txt>

      <G o={step === 3 ? 1 : 0}>
        <Pill x={180} y={112} w={76} text="директор" stroke="var(--s-accent)" />
        <Loop x={180} y={112} r={10} c="g" />
        <Pill x={64} y={112} w={56} text="Аня" />
        <Pill x={296} y={112} w={56} text="Борис" />
        <Arrow x1={94} y1={112} x2={140} y2={112} c="m" />
        <Arrow x1={266} y1={112} x2={220} y2={112} c="m" />
        <Txt x="180" y="152" mono color="var(--s-accent)" size={10}>manager_id = id — допустимо</Txt>
      </G>
    </Steps>
  );
}
