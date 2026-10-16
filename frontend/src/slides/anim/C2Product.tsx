import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 3: прямое произведение. Три футболки × двое брюк = шесть
   нарядов; правило произведения; перекрёстное соединение в SQL. */

const LABELS = ["Множества", "Наряды", "Правило", "В базе"];
const CAPTION = [
  "Берём два множества: три футболки и двое брюк",
  "Все возможные пары — прямое произведение: шесть нарядов",
  "Это заготовка под правило произведения: 3 · 2 = 6 — основа комбинаторики",
  "В базах данных этому отвечает перекрёстное соединение таблиц",
];
const SHIRTS = ["красная", "синяя", "белая"];
const PANTS = ["чёрные", "серые"];

export default function C2Product({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.1, 10.3, 17.0], 3000);
  const { step } = ctl;
  const grid = step >= 1 && step <= 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G x={step === 0 ? 0 : -40} o={step <= 2 ? 1 : 0}>
        <Txt x={90} y={18}>футболки A</Txt>
        {SHIRTS.map((t, i) => (
          <Pill key={t} x={90} y={50 + i * 34} w={64} text={t} stroke="var(--s-blue)" />
        ))}
      </G>
      <G o={step === 0 ? 1 : 0}>
        <Txt x={270} y={18}>брюки B</Txt>
        {PANTS.map((t, i) => (
          <Pill key={t} x={270} y={66 + i * 34} w={64} text={t} stroke="var(--s-amber)" />
        ))}
        <Txt x={180} y={96} mono size={20} color="var(--s-accent)">×</Txt>
      </G>

      {/* таблица пар */}
      <G o={grid ? 1 : 0}>
        <Txt x={226} y={30} mono size={11}>B ↓ · A →</Txt>
        {PANTS.map((t, r) => (
          <text key={t} x="146" y={70 + r * 38} textAnchor="end" className="a-cap">{t}</text>
        ))}
        {SHIRTS.map((t, c) => (
          <text key={t} x={176 + c * 56} y="44" textAnchor="middle" className="a-cap">{t}</text>
        ))}
        {PANTS.map((_, r) =>
          SHIRTS.map((__, c) => (
            <g key={`${r}${c}`}>
              <rect x={152 + c * 56} y={52 + r * 38} width="48" height="30" rx="6" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.4 }} />
              <text x={176 + c * 56} y={71 + r * 38} textAnchor="middle" className="a-mono" style={{ fontSize: 10 }}>
                ({c + 1}, {r + 1})
              </text>
            </g>
          )),
        )}
      </G>
      <Txt x={180} y={150} mono o={step === 1 ? 1 : 0} color="var(--s-accent)" size={13}>A × B: 6 пар</Txt>
      <Txt x={180} y={150} mono o={step === 2 ? 1 : 0} color="var(--s-accent)" size={15}>|A × B| = 3 · 2 = 6</Txt>

      <G o={step === 3 ? 1 : 0}>
        <rect x="50" y="28" width="260" height="104" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="66" y="54" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>SELECT *</text>
        <text x="66" y="74" className="a-mono" style={{ fontSize: 12 }}>FROM shirts CROSS JOIN pants;</text>
        <text x="66" y="104" className="a-mono" style={{ fontSize: 11, fill: "var(--s-amber)" }}>3 строки × 2 строки = 6 строк</text>
        <text x="66" y="121" className="a-cap">без условия отбора — все сочетания</text>
      </G>
    </Steps>
  );
}
