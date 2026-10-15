import { G, Matrix, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 2, слайд 4: отношение — подмножество прямого произведения.
   Заказ → клиент (внешний ключ), «дружит», таблица как отношение. */

const LABELS = ["Подмножество", "Заказ → клиент", "Дружит", "Таблица"];
const CAPTION = [
  "Отношение — подмножество прямого произведения: часть пар отмечена как связанные",
  "«Заказ принадлежит клиенту» — пары (заказ, клиент); в базе это внешний ключ",
  "«Дружит» — пары людей, симметричные по смыслу: отмечены обе половины",
  "Таблица в базе данных и есть отношение — от этого и слово «реляционная»",
];
const ORD = ["#1", "#2", "#3", "#4"];
const CLI = ["Аня", "Борис", "Вера"];
const FK = [0, 0, 1, 2]; // клиент каждого заказа
const PPL = ["А", "Б", "В", "Г"];
const FR = new Set(["0-1", "1-0", "1-2", "2-1", "2-3", "3-2"]);
const SUB = new Set(["0-0", "1-2", "2-1", "3-3", "0-2"]);

export default function C2Relation({ cues }) {
  const ctl = useSteps(cues || [7.1, 13.5, 17.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* A × B, часть клеток подсвечена */}
      <Matrix
        x={146}
        y={40}
        rows={step === 2 ? PPL : ORD}
        cols={step === 2 ? PPL : CLI}
        o={step <= 2 ? 1 : 0}
        mark={(r, c) =>
          step === 0
            ? SUB.has(`${r}-${c}`) && r < 4 && c < 3
              ? "g"
              : null
            : step === 1
              ? FK[r] === c
                ? "g"
                : null
              : step === 2
                ? FR.has(`${r}-${c}`)
                  ? "y"
                  : null
                : null
        }
        cell={32}
      />
      <Txt x="60" y="30" o={step === 0 ? 1 : 0} mono color="var(--s-accent)">R ⊆ A × B</Txt>
      <Txt x="60" y="30" o={step === 1 ? 1 : 0} mono color="var(--s-accent)">внешний ключ</Txt>
      <Txt x="60" y="30" o={step === 2 ? 1 : 0} mono color="var(--s-amber)">симметрично</Txt>

      {/* таблица */}
      <G o={step === 3 ? 1 : 0}>
        <rect x="90" y="24" width="180" height="108" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="110" y="46" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-muted)" }}>order_id</text>
        <text x="190" y="46" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-muted)" }}>client_id</text>
        {FK.map((c, i) => (
          <g key={i}>
            <text x="120" y={68 + i * 20} className="a-mono" style={{ fontSize: 11 }}>{i + 1}</text>
            <text x="205" y={68 + i * 20} className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>{c + 1}</text>
          </g>
        ))}
      </G>
      <Txt x="180" y="152" o={step === 3 ? 1 : 0} mono color="var(--s-accent)">строка таблицы = пара отношения</Txt>
    </Steps>
  );
}
