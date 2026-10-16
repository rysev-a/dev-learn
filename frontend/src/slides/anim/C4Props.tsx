import { G, Steps, Txt, useSteps } from "./kit.tsx";
import { binom, triPos } from "./tri.ts";

/* Глава 4, слайд 4: свойства, видимые в треугольнике: сумма строки 2ⁿ,
   симметрия, правило Паскаля. */

const LABELS = ["Свойства", "Сумма 2ⁿ", "Симметрия", "Правило", "Справочник"];
const CAPTION = [
  "Из треугольника мгновенно читаются свойства, которые мы встречали в главе про множества",
  "Сумма чисел строки n равна 2ⁿ: строка — все подмножества, сгруппированные по размеру",
  "Строка симметрична: C(n, k) = C(n, n − k) — выбрать, кого взять, то же, что выбрать, кого оставить",
  "Правило Паскаля: C(n, k) = C(n−1, k−1) + C(n−1, k) — взять конкретный элемент или не взять",
  "Треугольник — наглядный справочник: равенства видны, а не заучиваются",
];
const ROWS = 7;

export default function C4Props({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.1, 13.8, 21.5, 29.0], 3000);
  const { step } = ctl;
  const cells = [];
  for (let r = 0; r < ROWS; r++) for (let c = 0; c <= r; c++) cells.push([r, c]);
  const mark = (r: number, c: number) => {
    if (step === 1 && r === 4) return "g";
    if (step === 2 && r === 5 && (c === 2 || c === 3)) return "y";
    if (step === 3 && ((r === 5 && c === 2) || (r === 4 && (c === 1 || c === 2)))) return "b";
    return null;
  };
  const COLOR = { g: "var(--s-accent)", y: "var(--s-amber)", b: "var(--s-blue)" };
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {cells.map(([r, c]) => {
        const [x, y] = triPos(r!, c!, 38, 20, 150, 18);
        const m = mark(r!, c!);
        return (
          <g key={`${r}${c}`}>
            <circle className="a-t" cx={x} cy={y} r="10" style={{ fill: m ? COLOR[m] : "var(--s-panel2)", fillOpacity: m ? 0.35 : 1, stroke: m ? COLOR[m] : "var(--s-border)", strokeWidth: m ? 2 : 1.3 }} />
            <text x={x} y={y! + 3.6} textAnchor="middle" className="a-mono" style={{ fontSize: 9.5 }}>{binom(r!, c!)}</text>
          </g>
        );
      })}
      <line className="a-t" x1="150" y1="12" x2="150" y2="158" style={{ stroke: "var(--s-amber)", strokeDasharray: "4 4", opacity: step === 2 ? 0.8 : 0 }} />
      <G o={step === 1 ? 1 : 0}>
        <Txt x={296} y={62} mono size={11}>1+4+6+4+1</Txt>
        <Txt x={296} y={82} mono size={15} color="var(--s-accent)">= 16 = 2⁴</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={296} y={62} mono size={11}>C(5,2) = 10</Txt>
        <Txt x={296} y={80} mono size={11}>C(5,3) = 10</Txt>
        <Txt x={296} y={100} size={9.5} color="var(--s-amber)">зеркало</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x={296} y={62} mono size={11}>C(5,2) =</Txt>
        <Txt x={296} y={80} mono size={11}>C(4,1) + C(4,2)</Txt>
        <Txt x={296} y={100} mono size={12} color="var(--s-blue)">10 = 4 + 6</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={296} y={74} size={10}>всё видно</Txt>
        <Txt x={296} y={90} size={10}>на таблице</Txt>
      </G>
    </Steps>
  );
}
