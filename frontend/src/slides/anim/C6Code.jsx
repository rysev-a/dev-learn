import { Dot, G, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 8: отрицание кванторов в коде — every/some, читаемость,
   распутывание двойных отрицаний. */

const LABELS = ["Перевёртыш", "every ↔ some", "Читаемость", "На ревью"];
const CAPTION = [
  "В коде то же правило выглядит как перевёртыш",
  "Неверно, что every прошёл проверку, — значит, найдётся элемент, провалившийся: это some с отрицанием",
  "«Не для всех предикат истинен» читать труднее, чем «найдётся элемент, где он ложен», хотя смысл один",
  "На ревью: замечайте двойные отрицания и распутывайте их этим правилом",
];

export default function C6Code({ cues }) {
  const ctl = useSteps(cues || [2.9, 12.0, 19.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">!every(p) ≡ some(!p)</Txt>
      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 5 }, (_, i) => (
          <Dot key={i} x={50 + i * 65} y={52} r={15} text={i === 3 ? "✗" : "✓"} stroke={i === 3 ? "var(--s-red)" : "var(--s-accent)"} fill={i === 3 ? "var(--s-red)" : "var(--s-green)"} fillOpacity={i === 3 ? 0.3 : 1} size={12} />
        ))}
        <Txt x="180" y="96" mono size={12}>!items.every(ok)  →  false … true</Txt>
        <Txt x="180" y="118" mono size={12} color="var(--s-accent)">items.some(x =&gt; !ok(x))  →  true</Txt>
        <Txt x="180" y="146" size={10}>одно и то же: нашёлся провалившийся</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <rect x="30" y="34" width="140" height="70" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-red)" }} />
        <Txt x="100" y="64" size={10.5}>«не для всех элементов</Txt>
        <Txt x="100" y="80" size={10.5}>предикат истинен»</Txt>
        <rect x="190" y="34" width="140" height="70" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)" }} />
        <Txt x="260" y="64" size={10.5}>«найдётся элемент,</Txt>
        <Txt x="260" y="80" size={10.5}>где он ложен»</Txt>
        <Txt x="180" y="140" mono size={12} color="var(--s-accent)">читается проще</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <text x="30" y="52" className="a-mono" style={{ fontSize: 11.5, fill: "var(--s-red)" }}>!arr.every(x =&gt; !x.ok)</text>
        <Txt x="180" y="78" mono size={16} color="var(--s-accent)">↓</Txt>
        <text x="30" y="108" className="a-mono" style={{ fontSize: 13, fill: "var(--s-accent)" }}>arr.some(x =&gt; x.ok)</text>
        <Txt x="180" y="140" size={10}>двойное отрицание распутано</Txt>
      </G>
    </Steps>
  );
}
