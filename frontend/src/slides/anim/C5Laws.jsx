import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 5, слайд 9: законы логики — коммутативность, ассоциативность,
   двойное отрицание, дистрибутивность — и упрощение шаг за шагом. */

const LABELS = ["Законы", "Порядок", "Двойное ¬", "Дистрибутивность", "Упрощение"];
const CAPTION = [
  "Как и у множеств, у логических операций есть законы, и большинство выглядит естественно",
  "Порядок «и» не важен, порядок «или» тоже; скобки при одинаковой операции — как удобно",
  "Двойное отрицание сокращается: «неверно, что неверно» — это исходное утверждение",
  "Дистрибутивность: общий множитель выносится за скобки и вносится обратно — для «и» и для «или»",
  "Алгебра условий: выражения упрощаются так же механически, как числа в школьном примере",
];
const CHAIN = ["¬¬a ∧ (b ∨ ¬b)", "a ∧ (b ∨ ¬b)", "a ∧ 1", "a"];
const WHY = ["", "двойное отрицание", "b ∨ ¬b — тавтология", "∧ 1 ничего не меняет"];

export default function C5Laws({ cues }) {
  const ctl = useSteps(cues || [5.3, 11.0, 17.0, 25.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {["∧", "∨", "¬", "·(·)"].map((t, i) => (
          <Pill key={t} x={60 + i * 80} y={80} w={50} h={44} text={t} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={16} />
        ))}
      </G>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={80} y={50} w={44} text="a" stroke="var(--s-blue)" />
        <Txt x="130" y="54" mono size={14}>∧</Txt>
        <Pill x={180} y={50} w={44} text="b" stroke="var(--s-amber)" />
        <Txt x="226" y="54" mono size={14} color="var(--s-accent)">=</Txt>
        <Pill x={270} y={50} w={44} text="b" stroke="var(--s-amber)" />
        <Txt x="314" y="54" mono size={14}>∧</Txt>
        <Pill x={344} y={50} w={30} text="a" stroke="var(--s-blue)" />
        <Txt x="180" y="104" mono size={12}>(a ∧ b) ∧ c = a ∧ (b ∧ c)</Txt>
        <Txt x="180" y="130" size={10}>скобки при одинаковой операции — как удобно</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={70} y={70} w={70} text="p" stroke="var(--s-blue)" />
        <Txt x="130" y="74" mono size={20} color="var(--s-red)">¬</Txt>
        <Txt x="160" y="74" mono size={20} color="var(--s-red)">¬</Txt>
        <Txt x="190" y="74" mono size={14}>p</Txt>
        <Txt x="226" y="74" mono size={14} color="var(--s-accent)">=</Txt>
        <Pill x={290} y={70} w={70} text="p" stroke="var(--s-blue)" />
        <Txt x="180" y="124" size={10}>«неверно, что неверно» — то же утверждение</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x="180" y="46" mono size={15}>a ∧ (b ∨ c)</Txt>
        <Txt x="180" y="72" mono size={16} color="var(--s-accent)">=</Txt>
        <Txt x="180" y="100" mono size={15}>(a ∧ b) ∨ (a ∧ c)</Txt>
        <Txt x="180" y="136" size={10}>работает и для «и», и для «или»</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {CHAIN.map((t, i) => (
          <g key={t} className="a-t" style={{ opacity: step >= 4 ? 1 : 0, transitionDelay: `${i * 450}ms` }}>
            <text x="30" y={36 + i * 30} className="a-mono" style={{ fontSize: 14, fill: i === 3 ? "var(--s-accent)" : "var(--s-text)" }}>{i ? "= " : "  "}{t}</text>
            <text x="330" y={36 + i * 30} textAnchor="end" className="a-cap">{WHY[i]}</text>
          </g>
        ))}
      </G>
    </Steps>
  );
}
