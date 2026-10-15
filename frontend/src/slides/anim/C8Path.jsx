import { GraphView, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 8, слайд 5: путь, длина, цикл, достижимость. */

const LABELS = ["Движение", "Путь", "Длина", "Цикл", "Достижимость"];
const CAPTION = [
  "Дальше — движение по графу",
  "Путь — последовательность вершин, где каждая следующая соединена с предыдущей ребром: дом → магазин → работа",
  "Длина пути — число рёбер в нём",
  "Цикл — путь, возвращающийся в стартовую вершину, не повторяя рёбер: круговой маршрут по району",
  "На существовании пути держатся задачи вроде «достижима ли база данных с этого сервиса»",
];
const N = [
  { x: 60, y: 90, l: "дом" },
  { x: 140, y: 46, l: "магаз" },
  { x: 230, y: 46, l: "работа" },
  { x: 300, y: 100, l: "парк" },
  { x: 190, y: 124, l: "кафе" },
];
const E = [
  { a: 0, b: 1 },
  { a: 1, b: 2 },
  { a: 2, b: 3 },
  { a: 3, b: 4 },
  { a: 4, b: 0 },
  { a: 1, b: 4 },
];
const PATH = [0, 1, 2];
const CYC = [0, 1, 4];

export default function C8Path({ cues }) {
  const ctl = useSteps(cues || [1.7, 8.3, 10.1, 16.2], 3000);
  const { step } = ctl;
  const inEdge = (e, set) => set.includes(e.a) && set.includes(e.b);
  const ec = (e) => {
    if (step === 1 || step === 2) return inEdge(e, PATH) && Math.abs(PATH.indexOf(e.a) - PATH.indexOf(e.b)) === 1 ? "g" : "m";
    if (step === 3) return inEdge(e, CYC) ? "y" : "m";
    return "m";
  };
  const nc = (i) => (step === 1 || step === 2 ? (PATH.includes(i) ? "g" : "m") : step === 3 ? (CYC.includes(i) ? "y" : "m") : "m");
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <GraphView o={step <= 3 ? 1 : 0} nodes={N} edges={E} nc={nc} ec={ec} r={19} lsize={8.5} />
      <Txt x="180" y="152" mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">дом, магаз, работа</Txt>
      <Txt x="180" y="152" mono size={12} o={step === 2 ? 1 : 0} color="var(--s-accent)">длина = 2 ребра</Txt>
      <Txt x="180" y="152" mono size={12} o={step === 3 ? 1 : 0} color="var(--s-amber)">дом → магаз → кафе → дом: цикл</Txt>
      <GraphView
        o={step >= 4 ? 1 : 0}
        directed
        nodes={[
          { x: 60, y: 80, l: "сервис" },
          { x: 160, y: 50, l: "API" },
          { x: 160, y: 110, l: "кэш" },
          { x: 270, y: 80, l: "БД" },
        ]}
        edges={[
          { a: 0, b: 1 },
          { a: 0, b: 2 },
          { a: 1, b: 3 },
        ]}
        ec={(e) => (e.a === 0 && e.b === 2 ? "m" : "g")}
        nc={(i) => (i === 0 || i === 1 || i === 3 ? "g" : "m")}
        r={20}
        lsize={8.5}
      />
      <Txt x="180" y="152" mono size={12} o={step >= 4 ? 1 : 0} color="var(--s-accent)">путь сервис → API → БД есть: БД достижима</Txt>
    </Steps>
  );
}
