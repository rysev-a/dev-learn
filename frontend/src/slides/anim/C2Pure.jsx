import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 2, слайд 12: чистая функция — функция по построению: зависит
   только от аргументов, проверяется простыми тестами, мемоизация строит
   таблицу пар. */

const LABELS = ["Чистая", "Без сюрпризов", "Тесты", "Мемоизация"];
const CAPTION = [
  "Чистая функция в программировании — это математическая функция по построению",
  "Не смотрит на время, не читает глобальные переменные, не пишет в базу",
  "За это её любят тесты: один вход — один ожидаемый выход, без моков",
  "Мемоизация сохраняет пары вход–выход: таблица соответствия — это отношение",
];
export default function C2Pure({ cues }) {
  const ctl = useSteps(cues || [8.7, 18.3, 24.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        <Pill x={60} y={74} w={50} text="x" stroke="var(--s-blue)" />
        <rect x="140" y="46" width="80" height="56" rx="12" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.8 }} />
        <text x="180" y="81" textAnchor="middle" className="a-mono" style={{ fontSize: 20, fill: "var(--s-accent)" }}>f</text>
        <Pill x={300} y={74} w={50} text="y" stroke="var(--s-amber)" />
        <Arrow x1={88} y1={74} x2={138} y2={74} c="g" />
        <Arrow x1={222} y1={74} x2={272} y2={74} c="g" />
        {/* побочные каналы */}
        {["время", "global", "база"].map((t, i) => (
          <g key={t}>
            <Pill x={100 + i * 80} y={20} w={62} text={t} o={step === 1 ? 1 : 0} stroke="var(--s-red)" />
            <Arrow x1={100 + i * 80 + (i === 0 ? 20 : i === 1 ? 0 : -20)} y1={32} x2={150 + i * 30} y2={48} c="r" o={step === 1 ? 0.8 : 0} dash="3 3" />
            <text x={100 + i * 80} y="128" textAnchor="middle" className="a-mono a-t" style={{ fontSize: 18, fill: "var(--s-red)", opacity: step === 1 ? 1 : 0 }}>✗</text>
          </g>
        ))}
        <Txt x="180" y="152" o={step === 0 ? 1 : 0} color="var(--s-accent)">результат зависит только от аргументов</Txt>
        <Txt x="180" y="152" o={step === 1 ? 1 : 0} color="var(--s-red)">никаких скрытых входов и побочных эффектов</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        <rect x="70" y="24" width="220" height="92" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        {[
          ["assert f(2) == 4", 50],
          ["assert f(3) == 9", 72],
          ["assert f(0) == 0", 94],
        ].map(([t, y]) => (
          <g key={t}>
            <text x="88" y={y} className="a-mono" style={{ fontSize: 11.5 }}>{t}</text>
            <text x="268" y={y} textAnchor="end" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>✓</text>
          </g>
        ))}
        <Txt x="180" y="140" color="var(--s-accent)">без моков и настройки окружения</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        <text x="180" y="26" textAnchor="middle" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>cache = {"{ }"}</text>
        {[
          ["2", "4"],
          ["3", "9"],
          ["4", "16"],
        ].map(([a, b], i) => (
          <g key={a} className="a-t" style={{ opacity: step === 3 ? 1 : 0, transitionDelay: `${i * 450}ms` }}>
            <Pill x={130} y={56 + i * 32} w={52} text={a} stroke="var(--s-blue)" />
            <Arrow x1={160} y1={56 + i * 32} x2={198} y2={56 + i * 32} c="g" />
            <Pill x={230} y={56 + i * 32} w={52} text={b} stroke="var(--s-amber)" />
          </g>
        ))}
        <Txt x="180" y="158" mono color="var(--s-accent)">таблица пар — это отношение</Txt>
      </G>
    </Steps>
  );
}
