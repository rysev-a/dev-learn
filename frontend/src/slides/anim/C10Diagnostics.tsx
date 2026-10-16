import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 10, слайд 12: диагностика — Байес на дежурстве: алерты,
   причины по правдоподобию, интуиция дежурного, таблица частот. */

const LABELS = ["Диагностика", "Алерты", "Причины", "Дежурный", "Частоты"];
const CAPTION = [
  "Ещё одна область, где Байес — рабочая лошадка: диагностика",
  "Сервис упал, на панели загорелось пять алертов",
  "Вероятность каждой причины при этих симптомах: частота поломки × насколько симптом для неё характерен",
  "Опытный дежурный начинает с того, что ломается чаще и лучше объясняет картину; формулы делают интуицию воспроизводимой",
  "Хорошая документация инцидентов — накопленная таблица априорных частот вашей системы",
];
const CAUSES = [
  ["деплой", 55, "var(--s-accent)"],
  ["база", 30, "var(--s-amber)"],
  ["сеть", 10, "var(--s-blue)"],
  ["диск", 5, "var(--s-muted)"],
] as const;

export default function C10Diagnostics({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.3, 7.2, 16.6, 25.4], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={80} mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">симптом → причина?</Txt>
      <G o={step === 1 ? 1 : 0}>
        {Array.from({ length: 5 }, (_, i) => (
          <g key={i} className="a-t" style={{ opacity: step === 1 ? 1 : 0, transitionDelay: `${i * 220}ms` }}>
            <circle cx={50 + i * 65} cy="66" r="20" style={{ fill: "var(--s-red)", fillOpacity: 0.3, stroke: "var(--s-red)", strokeWidth: 2 }} />
            <text x={50 + i * 65} y="72" textAnchor="middle" className="a-mono" style={{ fontSize: 16, fill: "var(--s-red)" }}>!</text>
          </g>
        ))}
        <Txt x={180} y={124} mono size={13} color="var(--s-red)">сервис упал · 5 алертов</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={180} y={20} mono size={10.5}>P(причина | симптомы) ∝ частота × характерность</Txt>
        {CAUSES.map(([t, v, c], i) => (
          <g key={t}>
            <text x="46" y={52 + i * 26} className="a-mono" style={{ fontSize: 11 }}>{t}</text>
            <rect className="a-t" x="96" y={38 + i * 26} width={step === 2 ? v * 3.6 : 0} height="20" rx="4" style={{ fill: c, fillOpacity: 0.35, stroke: c, transitionDelay: `${i * 200}ms` }} />
            <text x={104 + v * 3.6} y={52 + i * 26} className="a-mono" style={{ fontSize: 10.5, fill: c }}>{`${v} %`}</text>
          </g>
        ))}
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={100} y={60} w={150} h={40} text="что чаще ломается" stroke="var(--s-blue)" size={10.5} />
        <Txt x={196} y={64} mono size={16}>+</Txt>
        <Pill x={270} y={60} w={150} h={40} text="что лучше объясняет" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10.5} />
        <Txt x={180} y={118} size={10.5}>интуиция дежурного = байесовская прикидка</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="60" y="20" width="240" height="108" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="76" y="42" className="a-cap" style={{ fill: "var(--s-accent)" }}>инциденты за год</text>
        {CAUSES.map(([t, v], i) => (
          <g key={t}>
            <text x="76" y={64 + i * 18} className="a-mono" style={{ fontSize: 10.5 }}>{t}</text>
            <text x="284" y={64 + i * 18} textAnchor="end" className="a-mono" style={{ fontSize: 10.5, fill: "var(--s-amber)" }}>{`${v} %`}</text>
          </g>
        ))}
        <Txt x={180} y={148} size={10}>таблица априорных частот вашей системы</Txt>
      </G>
    </Steps>
  );
}
