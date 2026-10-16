import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 7: транзитивность. Предок предка — предок; «знаком с» —
   нет; транзитивные зависимости пакетов. */

const LABELS = ["Свойство", "Предки", "Знаком с", "Зависимости"];
const CAPTION = [
  "Транзитивность: первый связан со вторым, второй с третьим — значит, первый с третьим",
  "«Является предком» транзитивно: предок предка — тоже предок",
  "«Знаком с» не транзитивно: друг вашего друга — не обязательно друг; соцсеть лишь рекомендует",
  "В пакетных менеджерах: зависимость зависимости — ваша зависимость",
];

export default function C2Transitive({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [6.4, 10.7, 20.1], 3000);
  const { step } = ctl;
  const person = step === 1 ? ["бабушка", "мама", "я"] : step === 2 ? ["Аня", "Борис", "Вера"] : ["a", "b", "c"];
  const col = step === 2 ? "y" : "g";
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 2 ? 1 : 0}>
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <Pill x={70 + i * 110} y={96} w={78} text={person[i]} stroke={i === 1 ? "var(--s-muted)" : "var(--s-blue)"} />
          </g>
        ))}
        <Arrow x1={110} y1={96} x2={142} y2={96} c={col} />
        <Arrow x1={220} y1={96} x2={252} y2={96} c={col} o={1} />
        {/* вывод: дуга a → c */}
        <path
          className="a-t"
          d="M70 82 C100 28 250 28 290 82"
          markerEnd={`url(#a-hd-${step === 2 ? "r" : "g"})`}
          style={{ fill: "none", stroke: step === 2 ? "var(--s-red)" : "var(--s-accent)", strokeWidth: 1.8, strokeDasharray: "6 4", opacity: step >= 1 ? 1 : 0 }}
        />
        <Txt x={180} y={36} o={step === 1 ? 1 : 0} mono color="var(--s-accent)">предок ✓ автоматически</Txt>
        <Txt x={180} y={36} o={step === 2 ? 1 : 0} mono color="var(--s-red)">знакомы? — не следует</Txt>
        <Txt x={180} y={36} o={step === 0 ? 1 : 0} mono>a R b, b R c ⇒ a R c</Txt>
        <Txt x={180} y={140} o={step === 2 ? 1 : 0}>соцсеть показывает его как рекомендацию</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {["app", "lib-a", "lib-b", "lib-c"].map((t, i) => (
          <Pill key={t} x={46 + i * 90} y={90} w={62} text={t} stroke={i === 0 ? "var(--s-accent)" : "var(--s-muted)"} />
        ))}
        {[0, 1, 2].map((i) => (
          <Arrow key={i} x1={78 + i * 90} y1={90} x2={104 + i * 90} y2={90} c="g" />
        ))}
        <path d="M46 76 C80 30 230 30 316 76" className="a-t" markerEnd="url(#a-hd-y)" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 1.6, strokeDasharray: "5 4" }} />
        <Txt x={180} y={30} color="var(--s-amber)" mono size={11}>app зависит и от lib-c (транзитивно)</Txt>
        <Txt x={180} y={130}>прямые зависимости — сплошные, транзитивные — пунктир</Txt>
      </G>
    </Steps>
  );
}
