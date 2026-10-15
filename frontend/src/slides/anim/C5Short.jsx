import { G, Pill, Steps, Table, Txt, useSteps } from "./kit.jsx";

/* Глава 5, слайд 11: короткое замыкание — ленивое вычисление «и» и «или»
   следует из таблиц истинности. */

const LABELS = ["Замыкание", "Ленивость", "Защита", "Из таблицы", "Контракт"];
const CAPTION = [
  "Практический мост в языки программирования — короткое замыкание",
  "«И» и «или» вычисляются лениво: если левая часть решает исход, правая не вычисляется вовсе",
  "Проверка «пользователь существует и имя длиннее пяти»: на пустой ссылке вторая часть не выполнится",
  "Это прямое следствие таблиц: у «и» результат известен, когда левая часть ложна",
  "Логика здесь — работающий контракт: на нём защита от пустых ссылок и ленивые вычисления",
];

export default function C5Short({ cues }) {
  const ctl = useSteps(cues || [4.1, 11.7, 20.9, 29.0], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={22} o={step === 0 ? 1 : 0} color="var(--s-accent)">left and right</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={70} y={60} w={80} h={34} text="left = 0" stroke="var(--s-red)" />
        <Txt x="140" y="64" mono size={15}>and</Txt>
        <Pill x={230} y={60} w={110} h={34} text="right (…)" stroke="var(--s-muted)" o={0.3} />
        <line x1="178" y1="60" x2="282" y2="60" style={{ stroke: "var(--s-red)", strokeWidth: 2 }} />
        <Txt x="180" y="108" mono size={12} color="var(--s-red)">не вычисляется</Txt>
        <Txt x="180" y="132" mono size={13} color="var(--s-accent)">результат уже известен: 0</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <text x="30" y="44" className="a-mono" style={{ fontSize: 11 }}>user = None</text>
        <text x="30" y="68" className="a-mono" style={{ fontSize: 11, fill: "var(--s-accent)" }}>user and len(user.name) &gt; 5</text>
        <Pill x={70} y={100} w={90} h={26} text="user → None" stroke="var(--s-red)" size={9.5} />
        <Txt x="146" y="104" mono size={12}>→ ложь</Txt>
        <Pill x={250} y={100} w={160} h={26} text="user.name — пропущено" stroke="var(--s-muted)" o={0.45} size={9.5} />
        <Txt x="180" y="140" size={10} color="var(--s-accent)">ошибки доступа к пустой ссылке нет</Txt>
      </G>
      <Table x={96} y={34} head={["a", "b", "a∧b"]} rows={[[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 0]]} cw={56} rh={26} o={step === 3 ? 1 : 0} hl={(r, c) => (r >= 2 ? (c === 0 || c === 2 ? "y" : null) : null)} />
      <Txt x="300" y="112" size={9.5} o={step === 3 ? 1 : 0} color="var(--s-amber)">a = 0 → b неважно</Txt>
      <G o={step >= 4 ? 1 : 0}>
        {["защита от пустых ссылок", "ленивые вычисления"].map((t, i) => (
          <Pill key={t} x={180} y={52 + i * 48} w={220} h={32} text={t} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={11} />
        ))}
        <Txt x="180" y="140" size={10}>логика — не метафора, а контракт</Txt>
      </G>
    </Steps>
  );
}
