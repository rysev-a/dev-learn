import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 12: сцепки глав. Сочетание — подмножество (глава 1),
   правило произведения — прямое произведение (глава 2), дальше — Паскаль. */

const LABELS = ["Сцепки", "Подмножества", "Произведение", "Паскаль", "Цепочка"];
const CAPTION = [
  "Заметьте, как главы сцепляются",
  "Сочетание — подмножество размера k из множества размера n: комбинаторика выросла из множеств",
  "Правило произведения — прямое произведение из второй главы, посчитанное по числу элементов",
  "Перестановки и сочетания встретятся в следующей главе: из них сложится треугольник Паскаля",
  "Каждый новый инструмент переиспользует старые — в этом ценность дискретной математики",
];
const SUBS = [
  "ab", "ac", "ad", "bc", "bd", "cd",
];
const PASCAL = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]];

export default function C3Links({ cues }) {
  const ctl = useSteps(cues || [2.4, 9.9, 15.8, 22.7], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={180} y={28} w={120} text="{a, b, c, d}" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" />
        {SUBS.map((t, i) => (
          <Pill key={t} x={52 + i * 51.2} y={84} w={44} text={`{${t[0]},${t[1]}}`} stroke="var(--s-blue)" size={9.5} />
        ))}
        {SUBS.map((t, i) => (
          <Arrow key={`ar${i}`} x1={180} y1={40} x2={52 + i * 51.2} y2={72} c="m" o={0.5} />
        ))}
        <Txt x="180" y="132" mono size={13} color="var(--s-accent)">C(4, 2) = 6 подмножеств размера 2</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[0, 1, 2].map((r) =>
          [0, 1].map((c) => (
            <rect key={`${r}${c}`} x={120 + c * 56} y={32 + r * 30} width="48" height="24" rx="5" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.3 }} />
          )),
        )}
        <Txt x="180" y="22" size={9.5}>A × B (глава 2)</Txt>
        <Txt x="180" y="140" mono size={13} color="var(--s-accent)">|A × B| = |A| · |B| = 3 · 2 = 6</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {PASCAL.map((row, r) =>
          row.map((v, c) => (
            <g key={`${r}${c}`} className="a-t" style={{ opacity: step === 3 ? 1 : 0, transitionDelay: `${r * 260}ms` }}>
              <circle cx={180 + (c - (row.length - 1) / 2) * 38} cy={26 + r * 28} r="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.4 }} />
              <text x={180 + (c - (row.length - 1) / 2) * 38} y={30 + r * 28} textAnchor="middle" className="a-mono" style={{ fontSize: 10.5 }}>{v}</text>
            </g>
          )),
        )}
        <Txt x="320" y="86" anchor="end" size={9.5}>C(n, k)</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {["множества", "отношения", "комбинаторика", "Паскаль"].map((t, i) => (
          <g key={t}>
            <Pill x={52 + i * 86} y={84} w={78} text={t} stroke={i < 3 ? "var(--s-accent)" : "var(--s-amber)"} size={9} />
            {i < 3 && <Arrow x1={92 + i * 86} y1={84} x2={98 + i * 86} y2={84} c="g" />}
          </g>
        ))}
        <Txt x="180" y="130">каждый шаг опирается на предыдущие</Txt>
      </G>
    </Steps>
  );
}
