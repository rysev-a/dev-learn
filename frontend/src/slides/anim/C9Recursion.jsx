import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 9, слайд 4: рекурсия — готовый стек; DOM, каталоги, любая
   рекурсивная прогулка по вложенному — это DFS. */

const LABELS = ["Рекурсия", "Код", "DOM", "Каталоги", "Всё DFS"];
const CAPTION = [
  "Красота обхода в глубину: рекурсия — готовый стек, встроенный в язык даром",
  "Функция помечает узел посещённым и вызывает себя для каждого непосещённого соседа; стек вызовов помнит обратный путь",
  "Так обходят DOM-дерево: рекурсивно спускаемся к детям в каждом узле",
  "Так обходят каталоги: папка — рекурсивный вызов, файл — лист",
  "Любая рекурсивная функция, гуляющая по вложенной структуре, — обход в глубину, как её ни называй",
];

export default function C9Recursion({ cues }) {
  const ctl = useSteps(cues || [5.3, 12.5, 16.7, 20.8], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">рекурсия = стек даром</Txt>
      <G o={step === 1 ? 1 : 0}>
        <rect x="30" y="20" width="170" height="104" rx="10" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        {["def visit(v):", "  seen.add(v)", "  for u in adj[v]:", "    if u not in seen:", "      visit(u)"].map((t, i) => (
          <text key={i} x="44" y={42 + i * 18} className="a-mono" style={{ fontSize: 10.5, fill: i === 4 ? "var(--s-accent)" : "var(--s-text)" }} xmlSpace="preserve">{t}</text>
        ))}
        {["visit(A)", "visit(B)", "visit(D)"].map((t, i) => (
          <Pill key={t} x={270} y={104 - i * 26} w={80} h={22} text={t} stroke="var(--s-blue)" size={9.5} />
        ))}
        <Txt x="270" y="28" size={9.5}>стек вызовов</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        {[
          [180, 28, "html"],
          [110, 76, "head"],
          [250, 76, "body"],
          [215, 124, "div"],
          [290, 124, "p"],
        ].map(([x, y, t]) => (
          <Pill key={t} x={x} y={y} w={52} h={22} text={t} stroke="var(--s-accent)" size={9.5} />
        ))}
        <Txt x="60" y="140" mono size={10} color="var(--s-amber)">walk(node): for child…</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {[
          [90, 28, "📁 /", 0],
          [140, 54, "📁 src", 1],
          [190, 80, "📄 main.py", 2],
          [190, 106, "📄 util.py", 2],
          [140, 132, "📄 README", 1],
        ].map(([x, y, t]) => (
          <Pill key={t} x={x + 20} y={y} w={96} h={20} text={t} stroke="var(--s-blue)" size={9.5} />
        ))}
        <Txt x="290" y="80" mono size={10} color="var(--s-amber)">папка → вызов</Txt>
        <Txt x="290" y="96" mono size={10} color="var(--s-accent)">файл → лист</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={180} y={70} w={260} h={40} text="рекурсия по вложенному = DFS" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
        <Txt x="180" y="116" size={10}>даже если вы никогда так не называли</Txt>
      </G>
    </Steps>
  );
}
