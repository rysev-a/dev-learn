import { G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 6: кванторы в тестах. Юнит-тест — ∃ (три входа),
   property-based — ∀ (много случайных входов), контрпример побеждает. */

const LABELS = ["Тесты", "Юнит", "Property-based", "Контрпример", "Зелёные прогоны"];
const CAPTION = [
  "Самое время увидеть кванторы в собственных тестах",
  "Юнит-тест — утверждение существования: на этих трёх входах функция отвечает верно",
  "Property-based — квантор «для всех»: на всех сгенерированных входах свойство обязано выполняться",
  "Утверждение «для всех» опровергается одним контрпримером",
  "Хватит одного упавшего входа — и свойство нарушено, сколько бы зелёных прогонов его ни прикрывали",
];
// детерминированные «случайные» точки на числовой оси
const PTS = Array.from({ length: 60 }, (_, i) => 20 + ((i * 97 + (i * i * 13) % 53) % 320));
const BAD = 214;

export default function C6Tests({ cues }) {
  const ctl = useSteps(cues || [3.2, 9.4, 19.5, 25.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <line x1="20" y1="86" x2="340" y2="86" style={{ stroke: "var(--s-border)", strokeWidth: 1.6 }} />
      <Txt x="180" y="120" size={9.5}>пространство входов</Txt>
      <G o={step === 1 ? 1 : 0}>
        {[70, 150, 250].map((x) => (
          <circle key={x} cx={x} cy={86} r="7" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.8 }} />
        ))}
        <Txt x="180" y="46" mono size={13} color="var(--s-accent)">∃ три входа, где всё верно</Txt>
      </G>
      <G o={step >= 2 ? 1 : 0}>
        {PTS.map((x, i) => (
          <circle key={i} className="a-t" cx={x} cy={86} r="4" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.2, opacity: step >= 2 ? 1 : 0, transitionDelay: `${i * 25}ms` }} />
        ))}
        <Txt x="180" y="46" mono size={13} o={step === 2 ? 1 : 0} color="var(--s-accent)">∀ сгенерированных входов: свойство</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <circle cx={BAD} cy={86} r="9" style={{ fill: "var(--s-red)", fillOpacity: 0.4, stroke: "var(--s-red)", strokeWidth: 2.4 }} />
        <Txt x={BAD} y={64} mono size={14} color="var(--s-red)">✗</Txt>
        <Txt x="180" y="46" mono size={13} o={step === 3 ? 1 : 0} color="var(--s-red)">найден контрпример ⇒ ∀ ложно</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x="180" y="46" mono size={13} color="var(--s-amber)">1 красный ≫ 1000 зелёных</Txt>
        <Txt x="180" y="140" size={10}>тысяча зелёных прогонов не доказывает «для всех»</Txt>
      </G>
    </Steps>
  );
}
