import { Arrow, Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 9: порядок кванторов. ∀∃ — у каждого своя мама,
   ∃∀ — одна мама на всех. */

const LABELS = ["Порядок", "∀x ∃y", "∃y ∀x", "Формулы", "Ошибки"];
const CAPTION = [
  "Порядок кванторов меняет смысл — тут логика кусается по-настоящему",
  "«У каждого человека есть мама»: для каждого x найдётся свой y — тривиально истинно",
  "«Есть человек, мама всех сразу»: один y на всех — абсурд",
  "∀x ∃y: y выбирается под каждого x; ∃y ∀x: y один на всех",
  "Перепутанный порядок — классический источник ошибок в требованиях и интерфейсах",
];
const P = [32, 66, 100, 134];

export default function C6Order({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.4, 12.1, 14.4, 24.9], 3000);
  const { step } = ctl;
  const show = step >= 1 && step <= 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">∀x ∃y  ≠  ∃y ∀x</Txt>
      <G o={show ? 1 : 0}>
        {P.map((y, i) => (
          <g key={i}>
            <Dot x={80} y={y} r={11} text={`x${i + 1}`} size={8.5} stroke="var(--s-blue)" />
            <Dot x={280} y={y} r={11} text={`y${i + 1}`} size={8.5} stroke="var(--s-amber)" o={step === 1 || i === 0 ? 1 : 0.18} />
          </g>
        ))}
        {P.map((y, i) => (
          <Arrow key={`a${i}`} x1={94} y1={y} x2={266} y2={(step === 1 ? y : P[0])!} c={step === 1 ? "g" : "r"} o={show ? 1 : 0} />
        ))}
        <Txt x={180} y={154} mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">у каждого — своя мама</Txt>
        <Txt x={180} y={154} mono size={12} o={step === 2 ? 1 : 0} color="var(--s-red)">одна мама у всех — абсурд</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x={180} y={48} mono size={16} color="var(--s-accent)">∀x ∃y  мама(y, x)</Txt>
        <Txt x={180} y={68} size={10}>y выбирается под каждого x — «свой»</Txt>
        <Txt x={180} y={108} mono size={16} color="var(--s-red)">∃y ∀x  мама(y, x)</Txt>
        <Txt x={180} y={128} size={10}>y выбирается один на всех</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={180} y={70} mono size={15} color="var(--s-amber)">требования · интерфейсы</Txt>
        <Txt x={180} y={100} size={10}>перепутали порядок — и «все ждут» одного героя</Txt>
      </G>
    </Steps>
  );
}
