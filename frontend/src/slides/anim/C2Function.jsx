import { Arrow, Dot, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 2, слайд 10: функция — отношение с контрактом «ровно один образ».
   Нарушения: два ответа и ни одного; сигнатура; детерминизм. */

const LABELS = ["Функции", "Контракт", "Нарушения", "Сигнатура", "Без сюрпризов"];
const CAPTION = [
  "Теперь функции: отношение, у которого есть дополнительный контракт",
  "У каждого элемента области определения — ровно один образ в области значений",
  "Два ответа для одного входа или вход без ответа — это уже не функция",
  "Сигнатура в языке — тот же контракт, записанный типами: на входе строка, на выходе число",
  "Математическая функция не падает и на одинаковый вход даёт одинаковый выход",
];
const LX = 90;
const RX = 270;
const Y = [36, 80, 124];

export default function C2Function({ cues }) {
  const ctl = useSteps(cues || [1.4, 11.1, 15.4, 22.4], 3000);
  const { step } = ctl;
  const sets = step <= 2 ? 1 : 0;
  const ok = step <= 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={sets}>
        <Txt x={LX} y="14">область определения</Txt>
        <Txt x={RX} y="14">область значений</Txt>
        {Y.map((y, i) => (
          <Dot key={`l${i}`} x={LX} y={y} text={["a", "b", "c"][i]} stroke="var(--s-blue)" />
        ))}
        {Y.map((y, i) => (
          <Dot key={`r${i}`} x={RX} y={y} text={[1, 2, 3][i]} stroke="var(--s-amber)" />
        ))}
        {/* функция: по одной стрелке */}
        <Arrow x1={LX + 14} y1={Y[0]} x2={RX - 14} y2={Y[1]} c="g" o={ok ? 1 : 0} />
        <Arrow x1={LX + 14} y1={Y[1]} x2={RX - 14} y2={Y[2]} c="g" o={ok ? 1 : 0} />
        <Arrow x1={LX + 14} y1={Y[2]} x2={RX - 14} y2={Y[0]} c="g" o={ok ? 1 : 0} />
        {/* нарушения: у a два ответа, у c ни одного */}
        <Arrow x1={LX + 14} y1={Y[0]} x2={RX - 14} y2={Y[0]} c="r" o={step === 2 ? 1 : 0} />
        <Arrow x1={LX + 14} y1={Y[0]} x2={RX - 14} y2={Y[1]} c="r" o={step === 2 ? 1 : 0} />
        <Arrow x1={LX + 14} y1={Y[1]} x2={RX - 14} y2={Y[2]} c="g" o={step === 2 ? 1 : 0} />
        <Txt x="180" y="152" o={step === 1 ? 1 : 0} color="var(--s-accent)">ровно одна стрелка из каждого входа</Txt>
        <Txt x="180" y="152" o={step === 2 ? 1 : 0} color="var(--s-red)">у a — два ответа, у c — ни одного</Txt>
        <Txt x={52} y="128" o={step === 2 ? 1 : 0} color="var(--s-red)" mono size={13}>?</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        <Pill x={70} y={80} w={82} text="str" stroke="var(--s-blue)" />
        <rect x="128" y="56" width="104" height="48" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <text x="180" y="85" textAnchor="middle" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>len(s)</text>
        <Pill x={290} y={80} w={82} text="int" stroke="var(--s-amber)" />
        <Arrow x1={114} y1={80} x2={126} y2={80} c="g" />
        <Arrow x1={234} y1={80} x2={246} y2={80} c="g" />
        <Txt x="180" y="130" mono color="var(--s-accent)">def f(s: str) -&gt; int</Txt>
      </G>

      <G o={step === 4 ? 1 : 0}>
        {[
          ["f(2)", "4"],
          ["f(2)", "4"],
          ["f(2)", "4"],
        ].map(([a, b], i) => (
          <g key={i}>
            <Pill x={110} y={36 + i * 38} w={64} text={a} stroke="var(--s-blue)" />
            <Arrow x1={144} y1={36 + i * 38} x2={208} y2={36 + i * 38} c="g" />
            <Pill x={240} y={36 + i * 38} w={50} text={b} stroke="var(--s-accent)" />
          </g>
        ))}
        <Txt x="180" y="150" color="var(--s-accent)">один вход — всегда один и тот же выход, и без исключений</Txt>
      </G>
    </Steps>
  );
}
