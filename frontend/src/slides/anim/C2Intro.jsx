import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 1: отношения в базе (заказ → клиент), функции в модуле
   (вход → f → выход) и один общий словарь. */

const LABELS = ["Глава", "Отношения", "Функции", "Один словарь"];
const CAPTION = [
  "Отношения и функции: два слова, которыми вы пользуетесь каждый день",
  "В каждой базе данных живут отношения: заказ связан с клиентом, пост — с автором",
  "В каждом модуле живут функции: на входе значение, на выходе ровно одно",
  "Математика описывает и то и другое одним словарём — пары, отношения, функции",
];
const ORDERS = [
  ["#1", 36],
  ["#2", 64],
  ["#3", 92],
];
const LINKS = [0, 0, 1];

export default function C2Intro({ cues }) {
  const ctl = useSteps(cues || [4.2, 11.5, 14.8], 2800);
  const { step } = ctl;
  const rel = step === 1 || step === 3 ? 1 : 0;
  const fun = step === 2 || step === 3 ? 1 : 0;
  const dim = step === 3 ? 0.45 : 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={rel * dim}>
        <Txt x="76" y="16">заказы → клиенты</Txt>
        {ORDERS.map(([t, y], i) => (
          <Pill key={t} x={36} y={y} w={40} text={t} stroke="var(--s-amber)" />
        ))}
        {["Аня", "Борис"].map((n, i) => (
          <Pill key={n} x={120} y={50 + i * 40} w={52} text={n} stroke="var(--s-accent)" />
        ))}
        {LINKS.map((c, i) => (
          <Arrow key={i} x1={58} y1={ORDERS[i][1]} x2={92} y2={50 + c * 40} c="g" />
        ))}
      </G>
      <G o={fun * dim}>
        <Txt x="270" y="18">модуль</Txt>
        <Pill x={216} y={70} w={36} text="x" stroke="var(--s-muted)" />
        <rect x="244" y="48" width="50" height="44" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <text x="269" y="76" textAnchor="middle" className="a-mono" style={{ fontSize: 18, fill: "var(--s-accent)" }}>f</text>
        <Pill x={332} y={70} w={36} text="y" stroke="var(--s-muted)" />
        <Arrow x1={236} y1={70} x2={242} y2={70} c="g" />
        <Arrow x1={296} y1={70} x2={312} y2={70} c="g" />
      </G>
      <G o={step === 3 ? 1 : 0} y={step === 3 ? 0 : 8}>
        {[
          ["(a, b)", "пары"],
          ["R ⊆ A×B", "отношения"],
          ["f : A → B", "функции"],
        ].map(([big, t], i) => (
          <g key={t}>
            <rect x={28 + i * 108} y="132" width="98" height="30" rx="8" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.4 }} />
            <text x={77 + i * 108} y="146" textAnchor="middle" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-accent)" }}>{big}</text>
            <text x={77 + i * 108} y="157" textAnchor="middle" className="a-cap">{t}</text>
          </g>
        ))}
      </G>
    </Steps>
  );
}
