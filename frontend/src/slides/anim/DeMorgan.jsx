import { Steps, Txt, useSteps } from "./kit.jsx";

/* Слайд 6: законы де Моргана на диаграмме Венна. Заливка показывает
   ¬(A ∪ B) — всё вне обоих кругов, затем ¬(A ∩ B) — всё, кроме общей части;
   потом то же на языке условий кода. */

const LABELS = ["Законы", "Первый", "Второй", "В коде", "Итог"];
const CAPTION = [
  "Операции подчиняются законам; самые знаменитые — законы де Моргана",
  "Первый: дополнение объединения — всё вне обоих кругов, то есть ¬A ∩ ¬B",
  "Второй: дополнение пересечения — всё, кроме общей части, то есть ¬A ∪ ¬B",
  "На языке кода: неверно, что выполнено хотя бы одно, — значит, не выполнены оба",
  "Отрицание переворачивает «или» в «и» и обратно",
];

export default function DeMorgan({ cues }) {
  const ctl = useSteps(cues || [4.9, 8.3, 11.8, 21.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <defs>
        <clipPath id="dmg-a">
          <circle cx="150" cy="72" r="46" />
        </clipPath>
        <mask id="dmg-out">
          <rect width="360" height="170" fill="#fff" />
          <circle cx="150" cy="72" r="46" fill="#000" />
          <circle cx="210" cy="72" r="46" fill="#000" />
        </mask>
        <mask id="dmg-lens">
          <rect width="360" height="170" fill="#fff" />
          <g clipPath="url(#dmg-a)">
            <circle cx="210" cy="72" r="46" fill="#000" />
          </g>
        </mask>
      </defs>
      <rect x="40" y="10" width="280" height="124" rx="10" className="a-ring" style={{ stroke: "var(--s-border)" }} />
      <g mask="url(#dmg-out)">
        <rect
          className="a-t"
          x="40"
          y="10"
          width="280"
          height="124"
          rx="10"
          style={{ fill: "var(--s-accent)", opacity: step === 1 ? 0.35 : 0 }}
        />
      </g>
      <g mask="url(#dmg-lens)">
        <rect
          className="a-t"
          x="40"
          y="10"
          width="280"
          height="124"
          rx="10"
          style={{ fill: "var(--s-amber)", opacity: step === 2 ? 0.35 : 0 }}
        />
      </g>
      <circle cx="150" cy="72" r="46" className="a-ring a" />
      <circle cx="210" cy="72" r="46" className="a-ring b" />
      <Txt x="124" y="76" mono>A</Txt>
      <Txt x="236" y="76" mono>B</Txt>
      <Txt x="52" y="26" anchor="start">U</Txt>

      <Txt x="180" y="154" mono o={step === 1 ? 1 : 0} color="var(--s-accent)">
        ¬(A ∪ B) = ¬A ∩ ¬B
      </Txt>
      <Txt x="180" y="154" mono o={step === 2 ? 1 : 0} color="var(--s-amber)">
        ¬(A ∩ B) = ¬A ∪ ¬B
      </Txt>
      <Txt x="180" y="148" mono o={step === 3 ? 1 : 0} size={10.5}>
        !(a || b) === !a && !b
      </Txt>
      <Txt x="180" y="162" mono o={step === 3 ? 1 : 0} size={10.5}>
        !(a && b) === !a || !b
      </Txt>
      <Txt x="180" y="154" mono o={step >= 4 ? 1 : 0} color="var(--s-accent)" size={13}>
        «или» ↔ «и»
      </Txt>
    </Steps>
  );
}
