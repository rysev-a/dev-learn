import { G, GraphView, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 8, слайд 3: ориентированные и неориентированные рёбра. */

const LABELS = ["Симметрия", "Дружба", "Подписка", "Стрелки", "Выбор типа"];
const CAPTION = [
  "Первый вопрос к любым связям: симметричны ли они",
  "Дружба взаимна: если я вам друг, то и вы мне друг — неориентированное ребро",
  "Подписка не взаимна: я читаю блогера, он меня не замечает — ориентированное ребро, стрелка",
  "Ссылки между страницами, потоки данных, переходы по сайту — всё это стрелки",
  "Тип графа — первое проектное решение: перепутаете — алгоритм ответит не на те вопросы",
];
const NODES = [
  { x: 70, y: 80, l: "я" },
  { x: 180, y: 50, l: "друг" },
  { x: 290, y: 80, l: "блог" },
];

export default function C8Directed({ cues }) {
  const ctl = useSteps(cues || [3.2, 8.8, 16.1, 21.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">a — b   или   a → b ?</Txt>
      <GraphView nodes={NODES.slice(0, 2)} edges={[{ a: 0, b: 1 }]} ec={() => "g"} o={step === 1 ? 1 : 0} />
      <GraphView nodes={[NODES[0], NODES[2]]} edges={[{ a: 0, b: 1 }]} directed ec={() => "y"} o={step === 2 ? 1 : 0} />
      <Txt x="180" y="130" mono size={12} o={step === 1 ? 1 : 0} color="var(--s-accent)">я — друг  =  друг — я</Txt>
      <Txt x="180" y="130" mono size={12} o={step === 2 ? 1 : 0} color="var(--s-amber)">я → блог  ≠  блог → я</Txt>
      <G o={step === 3 ? 1 : 0}>
        {[
          ["ссылка", "стр. A → стр. B"],
          ["поток данных", "источник → приёмник"],
          ["переход по сайту", "главная → каталог"],
        ].map(([t, f], i) => (
          <g key={t}>
            <Pill x={90} y={40 + i * 38} w={140} h={26} text={t} stroke="var(--s-amber)" size={10.5} />
            <text x="180" y={44 + i * 38} className="a-mono" style={{ fontSize: 12, fill: "var(--s-amber)" }}>→</text>
            <text x="200" y={44 + i * 38} className="a-mono" style={{ fontSize: 10.5 }}>{f}</text>
          </g>
        ))}
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={100} y={64} w={140} h={44} text="граф без стрелок" stroke="var(--s-accent)" size={11} />
        <Txt x="180" y="68" mono size={16}>≠</Txt>
        <Pill x={260} y={64} w={140} h={44} text="граф со стрелками" stroke="var(--s-amber)" size={11} />
        <Txt x="180" y="124" size={10}>разные модели — разные вопросы и ответы</Txt>
      </G>
    </Steps>
  );
}
