import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 12: список или множество. Список помнит порядок и повторы,
   множество отвечает «есть ли такой» мгновенно; поиск в цикле по списку —
   признак множества, замаскированного под список. */

const LABELS = ["Контракты", "Список", "Множество", "Поиск", "Выбор"];
const CAPTION = [
  "Список и множество — разные контракты под похожим синтаксисом",
  "Список хранит порядок и допускает повторы: очередь задач, история, постраничная выдача",
  "Множество хранит факт принадлежности и мгновенно отвечает «есть ли здесь такой»",
  "Поиск внутри списка в цикле — перебор всех элементов подряд",
  "Если вы ищете в списке — это почти всегда множество, замаскированное под список",
];

export default function Contracts({ cues }) {
  const ctl = useSteps(cues || [4.7, 12.0, 18.1, 25.4], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <line x1="180" y1="8" x2="180" y2="164" style={{ stroke: "var(--s-border)", strokeDasharray: "3 4" }} />
      <Txt x="90" y="16" color="var(--s-amber)" size={12}>Список</Txt>
      <Txt x="270" y="16" color="var(--s-accent)" size={12}>Множество</Txt>
      <Txt x="90" y="30" o={step === 0 ? 1 : 0}>порядок и повторы</Txt>
      <Txt x="270" y="30" o={step === 0 ? 1 : 0}>только принадлежность</Txt>

      {/* список */}
      <G o={step >= 1 ? 1 : 0}>
        {["A", "B", "A", "C"].map((v, i) => (
          <g key={i}>
            <Pill x={30 + i * 40} y={56} w={34} text={v} stroke="var(--s-amber)" />
            <text x={30 + i * 40} y="80" textAnchor="middle" className="a-cap">{i}</text>
          </g>
        ))}
        <Txt x="90" y="98" o={step === 1 ? 1 : 0}>очередь · история · страницы</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        {Array.from({ length: 7 }, (_, i) => (
          <rect
            key={`${step}-${i}`}
            x={22 + i * 22}
            y="112"
            width="19"
            height="22"
            rx="4"
            className="a-scan"
            style={{
              fill: "var(--s-amber)",
              stroke: "var(--s-amber)",
              animationDelay: step === 3 ? `${i * 0.32}s` : "0s",
              animationPlayState: step === 3 ? "running" : "paused",
              fillOpacity: step >= 4 ? 0.3 : undefined,
            }}
          />
        ))}
        <Txt x="90" y="150" o={step === 3 ? 1 : 0} color="var(--s-amber)">в цикле: смотрим всех подряд</Txt>
      </G>
      <rect
        className="a-hull a-t"
        x="14"
        y="104"
        width="152"
        height="38"
        rx="10"
        style={{ opacity: step >= 4 ? 1 : 0, stroke: "var(--s-accent)" }}
      />
      <Txt x="90" y="158" o={step >= 4 ? 1 : 0} color="var(--s-accent)">это множество в маске списка</Txt>

      {/* множество */}
      <G o={step >= 2 ? 1 : 0}>
        <circle cx="270" cy="66" r="38" className="a-ring a" />
        {[
          [252, 56, 3],
          [286, 56, 1],
          [252, 82, 4],
          [286, 82, 7],
        ].map(([x, y, v]) => (
          <Dot key={v} x={x} y={y} r={10} text={v} stroke={v === 7 ? "var(--s-accent)" : "var(--s-muted)"} />
        ))}
        <Pill x={270} y={126} w={64} text="есть 7?" stroke="var(--s-accent)" />
        <Txt x="270" y="150" color="var(--s-accent)">✓ да — сразу</Txt>
      </G>
    </Steps>
  );
}
