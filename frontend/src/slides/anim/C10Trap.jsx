import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 8: ловушка базовой частоты — болезнь 1:1000, тест 99 % /
   1 % ложных; из 100 000: 99 истинных и 999 ложных положительных ≈ 9 %. */

const LABELS = ["Ловушка", "Редкая болезнь", "Тест", "Вопрос", "Расчёт", "Вывод"];
const CAPTION = [
  "Знаменитая ловушка с числами",
  "Болезнь редкая: болеет один человек из тысячи",
  "Тест хороший: больного ловит в 99 из 100 случаев, но здорового ошибочно помечает в 1 из 100",
  "Тест положительный — какова вероятность болезни?",
  "Интуиция кричит «99 %», математика говорит ≈ 9 %: на 100 000 — 99 пойманных больных и около 1 000 ложных тревог",
  "Положительный результат чаще означает ошибку: здоровых слишком много — это сила базовой частоты, а не дефект теста",
];

export default function C10Trap({ cues }) {
  const ctl = useSteps(cues || [2.7, 5.9, 12.5, 16.3, 28.4], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-red)">положительный тест = болен?</Txt>
      <G o={step === 1 || step === 2 || step === 3 ? 1 : 0}>
        {Array.from({ length: 1000 }, (_, i) => {
          const sick = i === 777;
          return <circle key={i} cx={30 + (i % 40) * 7.8} cy={22 + Math.floor(i / 40) * 6} r={sick ? 3 : 1.8} style={{ fill: sick ? "var(--s-red)" : "var(--s-muted)", opacity: sick ? 1 : 0.55 }} />;
        })}
        <Txt x="180" y="14" mono size={10.5} o={step === 1 ? 1 : 0} color="var(--s-red)">1 больной из 1000</Txt>
        <Txt x="180" y="14" mono size={10.5} o={step === 2 ? 1 : 0}>чувствительность 99 %, ложных 1 %</Txt>
        <Txt x="180" y="14" mono size={10.5} o={step === 3 ? 1 : 0} color="var(--s-amber)">P(болен | +) = ?</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x="180" y="22" mono size={10.5}>100 000 человек</Txt>
        <rect className="a-t" x="40" y="40" width={step >= 4 ? 19 : 0} height="30" rx="5" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
        <text x="66" y="60" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>99 больных пойманы</text>
        <rect className="a-t" x="40" y="86" width={step >= 4 ? 190 : 0} height="30" rx="5" style={{ fill: "var(--s-amber)", fillOpacity: 0.4, stroke: "var(--s-amber)", strokeWidth: 1.5, transitionDelay: "300ms" }} />
        <text x="238" y="106" className="a-mono" style={{ fontSize: 11, fill: "var(--s-amber)" }}>≈ 1 000 ложных</text>
        <Txt x="180" y="144" mono size={14} o={step === 4 ? 1 : 0} color="var(--s-accent)">99 / (99 + 999) ≈ 9 %</Txt>
        <Txt x="180" y="144" mono size={11} o={step >= 5 ? 1 : 0} color="var(--s-amber)">базовая частота перевешивает точность теста</Txt>
      </G>
    </Steps>
  );
}
