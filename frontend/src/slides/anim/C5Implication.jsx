import { Arrow, G, Pill, Steps, Table, Txt, useSteps } from "./kit.tsx";

/* Глава 5, слайд 5: импликация «если, то»: посылка и следствие, дождь и
   асфальт, поливалка не нарушает обещание, ранний возврат в коде. */

const LABELS = ["Импликация", "Части", "Дождь", "Поливалка", "В коде"];
const CAPTION = [
  "Пятая операция самая контринтуитивная — импликация «если, то»",
  "Первая часть — посылка, вторая — следствие",
  "«Если идёт дождь, то асфальт мокрый»",
  "Асфальт мокрый и от поливалки — обещание не нарушено: оно лишь «дождь ⇒ мокро»",
  "В коде импликация прячется в раннем возврате: если аргумент пуст — вернуть ошибку",
];

export default function C5Implication({ cues }) {
  const ctl = useSteps(cues || [4.7, 7.6, 11.4, 23.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={34} o={step === 0 ? 1 : 0} color="var(--s-accent)">p → q</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={80} y={70} w={96} h={34} text="p · посылка" stroke="var(--s-blue)" />
        <Arrow x1={132} y1={70} x2={216} y2={70} c="g" />
        <Pill x={280} y={70} w={110} h={34} text="q · следствие" stroke="var(--s-amber)" />
        <Txt x="180" y="130" mono size={13}>если p, то q</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={80} y={70} w={100} h={34} text="идёт дождь" stroke="var(--s-blue)" />
        <Arrow x1={134} y1={70} x2={216} y2={70} c="g" />
        <Pill x={280} y={70} w={110} h={34} text="асфальт мокрый" stroke="var(--s-amber)" />
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Table
          x={40}
          y={34}
          head={["дождь", "мокро", "p→q"]}
          rows={[
            [1, 1, 1],
            [0, 1, 1],
            [0, 0, 1],
            [1, 0, 0],
          ]}
          cw={64}
          rh={24}
          hl={(r, c) => (r === 1 && c < 3 ? "y" : r === 3 && c === 2 ? "r" : null)}
        />
        <Txt x="290" y="72" anchor="middle" size={10} color="var(--s-amber)">поливалка:</Txt>
        <Txt x="290" y="88" anchor="middle" size={10} color="var(--s-amber)">мокро без дождя</Txt>
        <Txt x="290" y="118" anchor="middle" size={10} color="var(--s-red)">нарушение —</Txt>
        <Txt x="290" y="132" anchor="middle" size={10} color="var(--s-red)">только 1 → 0</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="50" y="34" width="260" height="76" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="70" y="62" className="a-mono" style={{ fontSize: 12, fill: "var(--s-accent)" }}>if not arg:</text>
        <text x="90" y="82" className="a-mono" style={{ fontSize: 12 }}>return error</text>
        <text x="70" y="102" className="a-mono" style={{ fontSize: 11, fill: "var(--s-muted)" }}>пуст ⇒ ошибка   (p → q)</text>
      </G>
    </Steps>
  );
}
