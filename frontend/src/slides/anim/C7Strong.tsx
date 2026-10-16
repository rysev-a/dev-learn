import { Arrow, Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 6: сильная индукция — опора на все предыдущие значения;
   пример: разложение на простые множители. */

const LABELS = ["Сильная", "Обычная", "Сильная", "Законно", "Где нужна"];
const CAPTION = [
  "Индукция бывает усиленной",
  "В обычном переходе опираемся на верность утверждения ровно для k",
  "В сильной индукции разрешаем опору на все предыдущие значения сразу: верно для всех меньших — верно и для k",
  "Это законный приём: у лестницы просто больше опорных ступеней",
  "Пригодится, когда шаг зависит от нескольких значений — например, при разложении на простые множители",
];
const X = (i: number) => 40 + i * 46;

export default function C7Strong({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [2.1, 6.2, 14.2, 19.9], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={86} mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">сильная индукция</Txt>
      <G o={step >= 1 && step <= 3 ? 1 : 0}>
        {Array.from({ length: 7 }, (_, i) => (
          <Dot key={i} x={X(i)} y={92} r={13} text={i + 1} stroke={i === 6 ? "var(--s-amber)" : "var(--s-accent)"} fill={i === 6 ? "var(--s-panel2)" : "var(--s-green)"} size={11} />
        ))}
        {/* обычная: только соседняя ступень */}
        <Arrow x1={X(5) + 13} y1={92} x2={X(6) - 14} y2={92} c="g" o={step === 1 ? 1 : 0} />
        {/* сильная: все предыдущие */}
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <path key={i} className="a-t" d={`M${X(i)} 78 C${X(i)} ${40 - i * 2} ${X(6)} ${40 - i * 2} ${X(6)} 78`} markerEnd="url(#a-hd-y)" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 1.3, opacity: step >= 2 ? 0.75 : 0, transitionDelay: `${i * 120}ms` }} />
        ))}
        <Txt x={180} y={130} mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">P(k) ⇒ P(k+1)</Txt>
        <Txt x={180} y={130} mono size={12} o={step === 2 ? 1 : 0} color="var(--s-amber)">P(1..k−1) ⇒ P(k)</Txt>
        <Txt x={180} y={130} mono size={12} o={step === 3 ? 1 : 0}>больше опорных ступеней — тот же вывод</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Dot x={180} y={30} r={14} text="12" size={11} stroke="var(--s-blue)" />
        <Dot x={110} y={78} r={14} text="2" size={11} stroke="var(--s-accent)" fill="var(--s-green)" />
        <Dot x={250} y={78} r={14} text="6" size={11} stroke="var(--s-blue)" />
        <Dot x={214} y={126} r={14} text="2" size={11} stroke="var(--s-accent)" fill="var(--s-green)" />
        <Dot x={286} y={126} r={14} text="3" size={11} stroke="var(--s-accent)" fill="var(--s-green)" />
        <Arrow x1={170} y1={42} x2={120} y2={66} c="m" />
        <Arrow x1={190} y1={42} x2={240} y2={66} c="m" />
        <Arrow x1={242} y1={90} x2={222} y2={112} c="m" />
        <Arrow x1={258} y1={90} x2={278} y2={112} c="m" />
        <Txt x={60} y={130} size={10}>12 = 2 · 2 · 3</Txt>
        <Txt x={60} y={146} size={10} color="var(--s-muted)">множители меньше 12</Txt>
      </G>
    </Steps>
  );
}
