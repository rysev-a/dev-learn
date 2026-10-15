import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 12: карманный справочник — как доказывать и опровергать
   «для всех» и «найдётся»; стратегия отладки. */

const LABELS = ["Справочник", "∀", "∃", "Отладка", "Дешёвая сторона"];
const CAPTION = [
  "Соберём карманный справочник",
  "«Для всех» доказывается общим рассуждением и разрушается одним контрпримером",
  "«Найдётся» доказывается одним примером и разрушается общим рассуждением",
  "Отладка: чтобы опровергнуть «функция корректна» — ищите минимальный контрпример; «всегда падает» — достаточно одного удачного прогона",
  "Логика подсказывает, с какой стороны атаковать утверждение дешевле",
];
const COLS = ["доказать", "опровергнуть"];
const ROWS = [
  ["∀", "общее рассуждение", "один контрпример", [false, true]],
  ["∃", "один пример", "общее рассуждение", [true, false]],
];

export default function C6Cheat({ cues }) {
  const ctl = useSteps(cues || [2.2, 9.3, 16.1, 26.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {COLS.map((c, j) => (
        <Txt key={c} x={150 + j * 110} y="22" size={10.5}>{c}</Txt>
      ))}
      {ROWS.map(([q, a, b, cheap], i) => {
        const row = step === 1 ? i === 0 : step === 2 ? i === 1 : true;
        return (
          <g key={q} className="a-t" style={{ opacity: step === 0 ? 0.35 : row ? 1 : 0.2 }}>
            <text x="46" y={72 + i * 48} textAnchor="middle" className="a-mono" style={{ fontSize: 28, fill: "var(--s-accent)" }}>{q}</text>
            {[a, b].map((t, j) => {
              const ch = cheap[j];
              const hl = step >= 4;
              return (
                <g key={j}>
                  <rect
                    className="a-t"
                    x={86 + j * 110}
                    y={46 + i * 48}
                    width="100"
                    height="40"
                    rx="10"
                    style={{ fill: hl ? (ch ? "var(--s-green)" : "var(--s-red)") : "var(--s-panel2)", fillOpacity: hl && !ch ? 0.2 : 1, stroke: hl ? (ch ? "var(--s-accent)" : "var(--s-red)") : "var(--s-border)", strokeWidth: 1.5 }}
                  />
                  <text x={136 + j * 110} y={70 + i * 48} textAnchor="middle" className="a-cap" style={{ fontSize: 9.5, fill: "var(--s-text)" }}>{t}</text>
                </g>
              );
            })}
          </g>
        );
      })}
      <G o={step === 3 ? 1 : 0}>
        <Txt x="180" y="144" mono size={10.5} color="var(--s-amber)">«корректна» → ищем контрпример;  «всегда падает» → один удачный прогон</Txt>
      </G>
      <Txt x="180" y="150" mono size={11} o={step >= 4 ? 1 : 0} color="var(--s-accent)">зелёное — дёшево, красное — дорого</Txt>
    </Steps>
  );
}
