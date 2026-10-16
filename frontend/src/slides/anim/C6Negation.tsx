import { Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 7: отрицание кванторов — «зеркала де Моргана». */

const LABELS = ["Отрицание", "¬∀", "¬∃", "Формулы", "Перевод"];
const CAPTION = [
  "У кванторов есть правила отрицания, и они на удивление практичны",
  "Неверно, что «все пристёгнуты» ⇒ найдётся расстёгнутый",
  "Неверно, что «найдётся вегетарианец» ⇒ каждый гость ест мясо",
  "Зеркала де Моргана: отрицание уходит внутрь, меняя квантор на противоположный",
  "Никакой магии — просто аккуратный перевод с русского на русский",
];

export default function C6Negation({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.4, 11.5, 19.5, 26.2], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={28} o={step === 0 ? 1 : 0} color="var(--s-accent)">¬∀  ⇔  ∃¬</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Txt x={180} y={22} mono size={12}>¬ (все пристёгнуты)</Txt>
        {Array.from({ length: 6 }, (_, i) => (
          <Dot key={i} x={46 + i * 54} y={68} r={16} text={i === 3 ? "✗" : "✓"} stroke={i === 3 ? "var(--s-red)" : "var(--s-accent)"} fill={i === 3 ? "var(--s-red)" : "var(--s-green)"} fillOpacity={i === 3 ? 0.3 : 1} size={12} />
        ))}
        <Txt x={180} y={120} mono size={13} color="var(--s-red)">∃ расстёгнутый</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={180} y={22} mono size={12}>¬ (∃ вегетарианец)</Txt>
        {Array.from({ length: 6 }, (_, i) => (
          <Dot key={i} x={46 + i * 54} y={68} r={16} text="🥩" stroke="var(--s-amber)" size={12} />
        ))}
        <Txt x={180} y={120} mono size={13} color="var(--s-amber)">∀ гость ест мясо</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x={180} y={54} mono size={15}>¬∀x P(x)  ≡  ∃x ¬P(x)</Txt>
        <Txt x={180} y={100} mono size={15} color="var(--s-amber)">¬∃x P(x)  ≡  ∀x ¬P(x)</Txt>
        <Txt x={180} y={136} size={10}>квантор меняется, отрицание — внутрь</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={110} y={60} size={11}>«не все …»</Txt>
        <Txt x={180} y={60} mono size={16} color="var(--s-accent)">→</Txt>
        <Txt x={260} y={60} size={11}>«найдётся такой, что не …»</Txt>
        <Txt x={110} y={104} size={11}>«нет такого, что …»</Txt>
        <Txt x={180} y={104} mono size={16} color="var(--s-accent)">→</Txt>
        <Txt x={260} y={104} size={11}>«для всех не …»</Txt>
      </G>
    </Steps>
  );
}
