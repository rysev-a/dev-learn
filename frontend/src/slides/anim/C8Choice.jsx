import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 10: выбор представления — два вопроса: плотность и
   горячая операция. */

const LABELS = ["Два вопроса", "Плотность", "Операция", "Практика", "Ниша"];
const CAPTION = [
  "Сведём выбор к двум вопросам",
  "Граф плотный или разреженный? Матрица всегда ест V², списки — пропорционально числу рёбер",
  "Какая операция горячая? Частые проверки ребра — матрица; постоянный перебор соседей — списки",
  "Практика почти всегда на стороне списков: реальные графы разрежены, ходить по ним приходится непрерывно",
  "Матрица выигрывает в нишах: маленькие плотные графы и точечные проверки",
];

export default function C8Choice({ cues }) {
  const ctl = useSteps(cues || [2.2, 8.8, 16.9, 25.7], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={180} y={50} w={240} h={34} text="1. плотный или разреженный?" stroke="var(--s-accent)" size={11.5} />
        <Pill x={180} y={100} w={240} h={34} text="2. какая операция горячая?" stroke="var(--s-blue)" size={11.5} />
      </G>
      <G o={step === 1 ? 1 : 0}>
        <text x="50" y="50" className="a-mono" style={{ fontSize: 11 }}>матрица</text>
        <rect className="a-t" x="120" y="38" width={step === 1 ? 190 : 0} height="16" rx="4" style={{ fill: "var(--s-red)", fillOpacity: 0.35, stroke: "var(--s-red)" }} />
        <text x="318" y="50" className="a-mono" style={{ fontSize: 10, fill: "var(--s-red)" }}>V²</text>
        <text x="50" y="100" className="a-mono" style={{ fontSize: 11 }}>списки</text>
        <rect className="a-t" x="120" y="88" width={step === 1 ? 40 : 0} height="16" rx="4" style={{ fill: "var(--s-accent)", fillOpacity: 0.35, stroke: "var(--s-accent)" }} />
        <text x="168" y="100" className="a-mono" style={{ fontSize: 10, fill: "var(--s-accent)" }}>V + E</text>
        <Txt x="180" y="140" size={10}>в разреженном графе рёбер намного меньше V²</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={90} y={56} w={150} h={36} text="есть ли ребро u—v?" stroke="var(--s-amber)" size={10.5} />
        <Txt x="180" y="60" mono size={15}>→</Txt>
        <Pill x={270} y={56} w={130} h={36} text="матрица  O(1)" stroke="var(--s-amber)" size={10.5} />
        <Pill x={90} y={110} w={150} h={36} text="все соседи v" stroke="var(--s-accent)" size={10.5} />
        <Txt x="180" y="114" mono size={15}>→</Txt>
        <Pill x={270} y={110} w={130} h={36} text="списки  O(deg)" stroke="var(--s-accent)" size={10.5} />
      </G>
      <G o={step === 3 ? 1 : 0}>
        {["зависимости", "соцсвязи", "маршруты"].map((t, i) => (
          <Pill key={t} x={70 + i * 110} y={56} w={92} h={26} text={t} stroke="var(--s-accent)" size={10} />
        ))}
        <Txt x="180" y="108" mono size={13} color="var(--s-accent)">разрежены ⇒ списки смежности</Txt>
        <Txt x="180" y="132" size={10}>и по ним ходят непрерывно</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={110} y={64} w={160} h={44} text="маленький плотный граф" stroke="var(--s-amber)" size={10.5} />
        <Pill x={270} y={64} w={160} h={44} text="точечные проверки" stroke="var(--s-amber)" size={10.5} />
        <Txt x="180" y="126" mono size={12} color="var(--s-amber)">ниша матрицы</Txt>
      </G>
    </Steps>
  );
}
