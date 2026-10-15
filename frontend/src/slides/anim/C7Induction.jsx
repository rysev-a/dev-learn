import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 7, слайд 3: математическая индукция формально — база P(1),
   переход P(k) ⇒ P(k+1), падающие «домино». */

const LABELS = ["Формально", "P(n)", "База и переход", "Бесконечно", "Домино"];
const CAPTION = [
  "Математическая индукция говорит то же самое формально",
  "Пусть есть утверждение P(n) про натуральные числа",
  "Верно для единицы — база; из верности для k следует верность для k + 1 — переход",
  "Мы не проверяли каждое число — их бесконечно много: проверили всего два факта",
  "Цепочка переходов автоматически дотягивает истину до любого названного числа",
];
const N = 9;

export default function C7Induction({ cues }) {
  const ctl = useSteps(cues || [3.6, 6.0, 16.4, 22.1], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="46" mono size={20} o={step <= 1 ? 1 : 0} color="var(--s-accent)">{step === 0 ? "индукция" : "P(1), P(2), P(3), …"}</Txt>
      {Array.from({ length: N }, (_, i) => {
        const fallen = step >= 4 || (step >= 2 && i === 0);
        return (
          <g key={i} className="a-t" style={{ transform: `translate(${30 + i * 36}px, 120px) rotate(${fallen ? 72 : 0}deg)`, transformOrigin: "bottom left", transitionDelay: step === 4 ? `${i * 260}ms` : "0ms" }}>
            <rect x="0" y="-48" width="12" height="48" rx="2" style={{ fill: fallen ? "var(--s-green)" : "var(--s-panel2)", stroke: fallen ? "var(--s-accent)" : "var(--s-muted)", strokeWidth: 1.6 }} />
          </g>
        );
      })}
      {Array.from({ length: N }, (_, i) => (
        <text key={i} x={36 + i * 36} y="140" textAnchor="middle" className="a-mono" style={{ fontSize: 9.5, fill: "var(--s-muted)" }}>{i + 1}</text>
      ))}
      <G o={step >= 2 && step <= 3 ? 1 : 0}>
        <Txt x="60" y="62" mono size={11} color="var(--s-accent)">база: P(1)</Txt>
        <Txt x="240" y="62" mono size={11} color="var(--s-blue)">переход: P(k) ⇒ P(k+1)</Txt>
      </G>
      <Txt x="180" y="46" mono size={14} o={step >= 3 && step < 4 ? 1 : 0} color="var(--s-amber)">два факта — бесконечно много случаев</Txt>
      <Txt x="180" y="46" mono size={14} o={step >= 4 ? 1 : 0} color="var(--s-accent)">∀n  P(n)</Txt>
    </Steps>
  );
}
