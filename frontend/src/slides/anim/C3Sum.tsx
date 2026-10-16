import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 3, слайд 2: правило суммы. Две непересекающиеся группы 3 и 4
   складываются; меню обеда; ветви кода. */

const LABELS = ["Правило", "3 + 4", "Меню", "Ветви"];
const CAPTION = [
  "Правило суммы: выбираем ровно одну вещь, группы не пересекаются",
  "Три варианта в первой группе и четыре во второй — всего семь",
  "Три супа или четыре салата — семь способов выбрать первое блюдо",
  "В коде это ветвление: число путей исполнения складывается по веткам",
];
const A = [0, 1, 2];
const B = [0, 1, 2, 3];

export default function C3Sum({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.7, 12.7, 17.2], 2800);
  const { step } = ctl;
  const row = step === 1;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        <rect x="26" y="28" width="132" height="56" rx="14" className="a-hull" style={{ stroke: "var(--s-blue)" }} />
        <rect x="202" y="28" width="132" height="56" rx="14" className="a-hull" style={{ stroke: "var(--s-amber)" }} />
        <Txt x={92} y={22} color="var(--s-blue)">A · 3 варианта</Txt>
        <Txt x={268} y={22} color="var(--s-amber)">B · 4 варианта</Txt>
        <Txt x={180} y={62} mono size={16} color="var(--s-accent)">+</Txt>
        {A.map((i) => (
          <Dot key={`a${i}`} x={row ? 36 + i * 30 : 56 + i * 36} y={row ? 130 : 56} text={i + 1} stroke="var(--s-blue)" />
        ))}
        {B.map((i) => (
          <Dot key={`b${i}`} x={row ? 126 + i * 30 : 222 + i * 30} y={row ? 130 : 56} text={i + 4} stroke="var(--s-amber)" />
        ))}
        <Txt x={180} y={104} mono size={13} o={row ? 1 : 0} color="var(--s-accent)">3 + 4 = 7</Txt>
        <Txt x={180} y={150} o={step === 0 ? 1 : 0}>A ∩ B = ∅ — общих вариантов нет</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={90} y={22} color="var(--s-blue)">супы · 3</Txt>
        <Txt x={270} y={22} color="var(--s-amber)">салаты · 4</Txt>
        {["борщ", "щи", "уха"].map((t, i) => (
          <Pill key={t} x={90} y={46 + i * 28} w={70} text={t} stroke="var(--s-blue)" />
        ))}
        {["цезарь", "греческий", "оливье", "винегрет"].map((t, i) => (
          <Pill key={t} x={270} y={42 + i * 26} w={86} text={t} stroke="var(--s-amber)" />
        ))}
        <Txt x={180} y={70} mono size={14}>или</Txt>
        <Txt x={180} y={150} mono size={14} color="var(--s-accent)">3 + 4 = 7 первых блюд</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <rect x="50" y="26" width="260" height="106" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="66" y="50" className="a-mono" style={{ fontSize: 11.5, fill: "var(--s-accent)" }}>if cond:</text>
        <text x="86" y="68" className="a-mono" style={{ fontSize: 11.5 }}>…           # 3 пути</text>
        <text x="66" y="90" className="a-mono" style={{ fontSize: 11.5, fill: "var(--s-accent)" }}>else:</text>
        <text x="86" y="108" className="a-mono" style={{ fontSize: 11.5 }}>…           # 4 пути</text>
        <Txt x={180} y={152} mono size={13} color="var(--s-accent)">всего путей: 3 + 4 = 7</Txt>
      </G>
    </Steps>
  );
}
