import { Dot, G, Steps, Txt, useSteps } from "./kit.jsx";

/* Слайд 3: равенство множеств и пустое множество. {1, 2} и {2, 1, 1}:
   повтор сливается, множества оказываются равны; затем появляется ∅. */

const LABELS = ["Две записи", "Равны", "Пустое", "Точка отсчёта"];
const CAPTION = [
  "Две записи, в одной есть повтор: {1, 2} и {2, 1, 1}",
  "Повторы и порядок ничего не меняют — это одно и то же множество",
  "Особый житель — пустое множество: в нём нет ни одного элемента",
  "Оно у всех одно: сумма по пустоте равна нулю, поиск ничего не находит",
];

export default function Equality({ cues }) {
  const ctl = useSteps(cues || [5.9, 11.5, 18.4], 2800);
  const { step } = ctl;
  const dim = step >= 2 ? 0.1 : 1;
  const eq = "var(--s-accent)";
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={dim}>
        <circle cx="85" cy="70" r="46" className="a-ring a" />
        <Txt x="85" y="132">{"{1, 2}"}</Txt>
      </G>
      <G o={dim}>
        <circle cx="275" cy="70" r="46" className="a-ring b" />
        <Txt x="275" y="132">{"{2, 1, 1}"}</Txt>
      </G>
      <Dot x={68} y={70} text="1" o={dim} />
      <Dot x={102} y={70} text="2" o={dim} />
      <Dot x={252} y={70} text="2" o={dim} />
      <Dot x={288} y={55} text="1" o={dim} />
      <Dot x={step >= 1 ? 288 : 288} y={step >= 1 ? 55 : 87} text="1" o={step >= 1 ? 0 : dim} stroke="var(--s-amber)" />
      <Txt x="180" y="76" mono o={step >= 1 && step < 2 ? 1 : 0} color={eq} size={22}>
        =
      </Txt>

      <G o={step >= 2 ? 1 : 0} s={step >= 2 ? 1 : 0.5} x={180} y={72}>
        <circle r="38" className="a-ring" style={{ stroke: "var(--s-amber)", strokeDasharray: "5 4" }} />
        <text y="9" textAnchor="middle" className="a-mono" style={{ fontSize: 28, fill: "var(--s-amber)" }}>
          ∅
        </text>
      </G>
      <Txt x="100" y="154" o={step >= 3 ? 1 : 0} anchor="middle" mono color="var(--s-accent)">
        Σ ∅ = 0
      </Txt>
      <Txt x="260" y="154" o={step >= 3 ? 1 : 0} anchor="middle" mono color="var(--s-accent)">
        поиск в ∅ → ничего
      </Txt>
      <Txt x="180" y="128" o={step >= 2 ? 1 : 0}>
        пустое множество — одно на всех
      </Txt>
    </Steps>
  );
}
