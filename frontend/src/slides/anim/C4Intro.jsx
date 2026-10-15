import { Dot, G, Steps, Txt, useSteps } from "./kit.jsx";
import { triPos } from "./tri.js";

/* Глава 4, слайд 1: три разные вещи — треугольник, бином, принцип Дирихле —
   отвечают на один вопрос «как считать, не перебирая»; коллизии в хеш-таблице. */

const LABELS = ["Глава", "Три вещи", "Один вопрос", "Коллизии"];
const CAPTION = [
  "Бином, Паскаль и принцип Дирихле",
  "Треугольник чисел, формула степени суммы и шутка про кроликов и клетки",
  "На деле это три взгляда на один вопрос — как считать, не перебирая",
  "Сегодня увидим, как принцип Дирихле объясняет коллизии в хеш-таблицах",
];

export default function C4Intro({ cues }) {
  const ctl = useSteps(cues || [4.9, 11.8, 16.2], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 || step === 2 ? 1 : 0}>
        {/* треугольник */}
        {[0, 1, 2, 3].map((r) =>
          Array.from({ length: r + 1 }, (_, c) => {
            const [x, y] = triPos(r, c, 18, 17, 66, 30);
            return <circle key={`${r}${c}`} cx={x} cy={y} r="6" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.3 }} />;
          }),
        )}
        <Txt x="66" y="108" size={9.5}>треугольник</Txt>
        {/* бином */}
        <text x="180" y="68" textAnchor="middle" className="a-mono" style={{ fontSize: 18, fill: "var(--s-accent)" }}>(a+b)ⁿ</text>
        <Txt x="180" y="108" size={9.5}>формула</Txt>
        {/* кролики */}
        {[0, 1, 2].map((i) => (
          <rect key={i} x={254 + i * 28} y="48" width="22" height="32" rx="4" style={{ fill: "none", stroke: "var(--s-blue)", strokeWidth: 1.4 }} />
        ))}
        {[0, 1, 2, 3].map((i) => (
          <circle key={i} cx={265 + (i < 3 ? i * 28 : 0)} cy={i < 3 ? 64 : 58} r="5" style={{ fill: "var(--s-blue)" }} />
        ))}
        <Txt x="294" y="108" size={9.5}>кролики и клетки</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="140" mono size={14} color="var(--s-accent)">как считать, не перебирая?</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {[0, 1, 2, 3].map((i) => (
          <rect key={i} x={46 + i * 70} y="76" width="58" height="40" rx="6" style={{ fill: "var(--s-panel2)", stroke: i === 1 ? "var(--s-red)" : "var(--s-border)", strokeWidth: i === 1 ? 2 : 1.4 }} />
        ))}
        <Dot x={64} y={96} r={7} stroke="var(--s-accent)" />
        <Dot x={126} y={88} r={7} stroke="var(--s-amber)" />
        <Dot x={138} y={106} r={7} stroke="var(--s-red)" />
        <Dot x={204} y={96} r={7} stroke="var(--s-accent)" />
        <Dot x={274} y={96} r={7} stroke="var(--s-accent)" />
        <Txt x="180" y="140" mono size={12} color="var(--s-red)">два ключа в одной ячейке — коллизия</Txt>
        <Txt x="180" y="56" mono size={12}>hash(key) % 4</Txt>
      </G>
    </Steps>
  );
}
