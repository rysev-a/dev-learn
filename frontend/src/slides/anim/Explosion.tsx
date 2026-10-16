import { useEffect, useState } from "react";
import { REVEAL_MS, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 10: цена перебора. Кривая 2ⁿ рисуется слева направо: почти плоская
   до самого конца, а потом взлетает; метка n = 30 и «бюджет времени». */

const LABELS = ["Рост", "n = 30", "Формула", "Бюджет"];
const CAPTION = [
  "Перебор всех подмножеств растёт экспоненциально — это самая дорогая операция курса",
  "Уже при тридцати элементах вариантов больше миллиарда",
  "Поэтому дискретная математика дорожит каждой возможностью не перебирать, а считать формулой",
  "Два в степени n — бюджет вашего времени: увидели её в решении — остановитесь",
];

const PTS = Array.from({ length: 31 }, (_, n) => [
  30 + n * 10,
  140 - 118 * 2 ** (n - 30),
]);
const PATH = "M" + PTS.map((p) => p.join(" ")).join(" L");

export default function Explosion({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [8.3, 18.4, 23.6], 3000);
  const { step } = ctl;
  const [draw, setDraw] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setDraw(true), REVEAL_MS);
    return () => clearTimeout(t);
  }, []);
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <line x1="30" y1="140" x2="336" y2="140" style={{ stroke: "var(--s-border)", strokeWidth: 1.2 }} />
      {[10, 20, 30].map((n) => (
        <g key={n}>
          <line x1={30 + n * 10} y1="140" x2={30 + n * 10} y2="145" style={{ stroke: "var(--s-muted)" }} />
          <text x={30 + n * 10} y="156" textAnchor="middle" className="a-cap">
            n = {n}
          </text>
        </g>
      ))}
      <path
        d={PATH}
        pathLength="1"
        className="a-t"
        style={{
          fill: "none",
          stroke: "var(--s-amber)",
          strokeWidth: 2.4,
          strokeDasharray: 1,
          strokeDashoffset: draw ? 0 : 1,
          transition: "stroke-dashoffset 3.4s ease-in",
        }}
      />
      <Txt x={130} y={130} mono>1 024</Txt>
      <Txt x={230} y={130} mono>≈ 10⁶</Txt>
      <Txt x={306} y={28} mono color="var(--s-amber)">&gt; 10⁹</Txt>

      <circle
        cx="330"
        cy="22"
        r="7"
        className="a-t"
        style={{ fill: "none", stroke: "var(--s-red)", strokeWidth: 2, opacity: step >= 1 ? 1 : 0 }}
      />
      <Txt x={180} y={46} o={step === 1 ? 1 : 0} color="var(--s-red)" size={11}>
        n = 30: больше миллиарда вариантов
      </Txt>

      <line
        x1="30"
        y1="124"
        x2="330"
        y2="124"
        className="a-t"
        style={{ stroke: "var(--s-accent)", strokeWidth: 1.6, strokeDasharray: "6 4", opacity: step === 2 ? 1 : 0 }}
      />
      <Txt x={180} y={112} o={step === 2 ? 1 : 0} color="var(--s-accent)" size={11}>
        формула: считаем, а не перебираем — мгновенно
      </Txt>

      <Txt x={150} y={56} mono o={step === 3 ? 1 : 0}>
        1 мкс на вариант:
      </Txt>
      <Txt x={150} y={76} mono o={step === 3 ? 1 : 0} color="var(--s-amber)" size={12}>
        n = 30 → около 18 минут
      </Txt>
      <Txt x={150} y={96} mono o={step === 3 ? 1 : 0} color="var(--s-red)" size={12}>
        n = 40 → около 13 суток
      </Txt>
    </Steps>
  );
}
