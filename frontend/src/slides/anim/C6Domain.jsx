import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 11: кванторы ограничены областью — filter перед проверкой,
   генераторы в property-based тестах, область проверки уже, чем «весь мир». */

const LABELS = ["Область", "filter", "Генераторы", "Тонкость", "Дыра"];
const CAPTION = [
  "На практике кванторы почти всегда ограничены областью: не «для всех x вообще»",
  "Ограничение — это знакомый filter перед проверкой: берём не весь мир, а нужное множество",
  "В property-based тестах ограничение играют генераторы: числа 0…100, непустые строки, корректный json",
  "Тонкость: тест проверяет квантор не по всему миру, а по области генератора",
  "Если генератор не выдаёт отрицательные числа, «для всех чисел» проверено лишь для положительных",
];

export default function C6Domain({ cues }) {
  const ctl = useSteps(cues || [8.0, 13.4, 20.7, 26.3], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        <Txt x="180" y="30" mono size={13} o={step === 0 ? 1 : 0} color="var(--s-accent)">∀x ∈ users: P(x)</Txt>
        <ellipse cx="180" cy="86" rx="150" ry="46" style={{ fill: "none", stroke: "var(--s-border)", strokeDasharray: "4 4" }} />
        <ellipse cx="180" cy="86" rx={step === 0 ? 70 : 40} ry={step === 0 ? 30 : 20} className="a-t" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.8 }} />
        <Txt x="180" y="90" mono size={10.5}>users</Txt>
        <Txt x="60" y="140" size={9.5}>весь мир</Txt>
        <Txt x="180" y="150" mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">users.filter(…).every(P)</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {["целые 0…100", "непустые строки", "корректный json"].map((t, i) => (
          <Pill key={t} x={180} y={34 + i * 38} w={210} h={28} text={t} stroke="var(--s-blue)" size={11} />
        ))}
        <Txt x="180" y="150" size={10}>генераторы задают область квантора</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <line x1="24" y1="84" x2="336" y2="84" style={{ stroke: "var(--s-muted)", strokeWidth: 1.6 }} />
        <rect x="180" y="72" width="130" height="24" rx="6" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <Txt x="245" y="88" mono size={10} color="var(--s-accent)">генератор 0…100</Txt>
        <Txt x="180" y="112" mono size={10}>0</Txt>
        <rect className="a-t" x="24" y="72" width="156" height="24" rx="6" style={{ fill: "var(--s-red)", fillOpacity: step >= 4 ? 0.3 : 0, stroke: "var(--s-red)", strokeOpacity: step >= 4 ? 1 : 0, strokeDasharray: "4 3" }} />
        <Txt x="102" y="88" mono size={10} o={step >= 4 ? 1 : 0} color="var(--s-red)">отрицательные: не проверены</Txt>
        <Txt x="180" y="40" mono size={12}>∀ число…</Txt>
        <Txt x="180" y="148" size={10} o={step >= 4 ? 1 : 0} color="var(--s-amber)">заявили «для всех чисел», проверили половину</Txt>
      </G>
    </Steps>
  );
}
