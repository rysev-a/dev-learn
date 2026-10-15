import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 4, слайд 11: дни рождения и волосы на голове. 23 человека — 253 пары;
   город-миллионник и меньше 400 000 возможных значений. */

const LABELS = ["Сюрприз", "Пары", "Волосы", "Итог"];
const CAPTION = [
  "Тот же принцип даёт сюрприз: в группе из 23 человек двое с одним днём рождения — скорее да, чем нет, хотя дней 366",
  "Интуиция считает людей, а надо считать пары-кандидаты: их почти 250, и каждой достаточно совпасть",
  "Классическое доказательство существования: в городе-миллионнике двое с одинаковым числом волос",
  "Искать этих людей не нужно — Дирихле уже всё сказал",
];
const N = 23;
const P = Array.from({ length: N }, (_, i) => [
  180 + 58 * Math.cos((2 * Math.PI * i) / N - Math.PI / 2),
  82 + 58 * Math.sin((2 * Math.PI * i) / N - Math.PI / 2),
]);
const edges = [];
for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) edges.push([i, j]);

export default function C4Birthday({ cues }) {
  const ctl = useSteps(cues || [10.4, 19.1, 30.3], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        {edges.map(([a, b], i) => (
          <line key={i} className="a-t" x1={P[a][0]} y1={P[a][1]} x2={P[b][0]} y2={P[b][1]} style={{ stroke: "var(--s-accent)", strokeWidth: 0.8, opacity: step === 1 ? 0.35 : 0 }} />
        ))}
        {P.map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r="4.5" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.6 }} />
        ))}
        <Txt x="62" y="70" mono size={12} o={step === 0 ? 1 : 0}>23 человека</Txt>
        <Txt x="62" y="88" size={9.5} o={step === 0 ? 1 : 0}>366 дней</Txt>
        <Txt x="62" y="70" mono size={20} o={step === 1 ? 1 : 0} color="var(--s-accent)">253</Txt>
        <Txt x="62" y="88" size={9.5} o={step === 1 ? 1 : 0}>пары-кандидаты</Txt>
        <Txt x="300" y="76" mono size={10} o={step === 1 ? 1 : 0}>C(23, 2)</Txt>
      </G>
      <G o={step >= 2 ? 1 : 0}>
        <rect x="40" y="26" width="120" height="86" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-blue)", strokeWidth: 1.5 }} />
        <Txt x="100" y="70" mono size={14} color="var(--s-blue)">1 000 000</Txt>
        <Txt x="100" y="88" size={9.5}>человек в городе</Txt>
        <Txt x="180" y="72" mono size={18} color="var(--s-accent)">&gt;</Txt>
        <rect x="200" y="42" width="120" height="54" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
        <Txt x="260" y="68" mono size={13} color="var(--s-amber)">&lt; 400 000</Txt>
        <Txt x="260" y="84" size={9.5}>вариантов числа волос</Txt>
        <Txt x="180" y="140" mono size={12} o={step === 2 ? 1 : 0}>кроликов больше, чем клеток</Txt>
        <Txt x="180" y="140" mono size={12} o={step >= 3 ? 1 : 0} color="var(--s-accent)">двое с одинаковым числом волос есть</Txt>
      </G>
    </Steps>
  );
}
