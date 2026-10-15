import { G, Pill, Steps, Table, Txt, useSteps } from "./kit.jsx";

/* Глава 5, слайд 12: как применять — упрощать законами, тестировать по
   строкам таблицы, читать вслух. */

const LABELS = ["Привычки", "Упрощать", "Тесты", "Вслух", "Итог"];
const CAPTION = [
  "Как применять всё это ежедневно?",
  "Первое: упрощайте условия законами до того, как писать — меньше отрицаний и вложенности",
  "Второе: тестируйте по таблице истинности — каждая строка условия — отдельный тест-кейс",
  "Третье: читайте чужие условия вслух — «не выполняется хотя бы одно» понятнее стены восклицательных знаков",
  "Формальная логика — способ сделать условие понятным до запуска, а не после бага",
];

export default function C5Daily({ cues }) {
  const ctl = useSteps(cues || [2.4, 10.0, 18.6, 26.2], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {["упростить", "тестировать", "читать вслух"].map((t, i) => (
          <Pill key={t} x={180} y={34 + i * 40} w={180} h={30} text={`${i + 1}. ${t}`} stroke="var(--s-accent)" size={11} />
        ))}
      </G>
      <G o={step === 1 ? 1 : 0}>
        <Txt x="180" y="40" mono size={13}>!(!a || !b) &amp;&amp; (c || !c)</Txt>
        <Txt x="180" y="70" mono size={14} color="var(--s-accent)">↓ де Морган, тавтология</Txt>
        <Txt x="180" y="108" mono size={20} color="var(--s-accent)">a &amp;&amp; b</Txt>
        <Txt x="180" y="140" size={10}>меньше отрицаний, меньше вложенности</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Table x={30} y={34} head={["a", "b", "ok"]} rows={[[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 0]]} cw={44} rh={24} />
        {[0, 1, 2, 3].map((i) => (
          <Pill key={i} x={250} y={46 + i * 24} w={170} h={20} text={`test_case_${i + 1}`} stroke="var(--s-accent)" size={9.5} />
        ))}
        <Txt x="180" y="148" size={10}>покрытие веток = покрытие строк таблицы</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={180} y={40} w={250} h={28} text="!!(a && !(b || c)) …" stroke="var(--s-red)" size={11} />
        <Txt x="180" y="86" mono size={14} color="var(--s-accent)">↓ вслух</Txt>
        <Pill x={180} y={118} w={250} h={32} text="«не выполняется хотя бы одно из двух»" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={10} />
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={110} y={70} w={150} h={40} text="до запуска" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x="196" y="74" mono size={14}>вместо</Txt>
        <Pill x={270} y={70} w={110} h={40} text="после бага" stroke="var(--s-red)" size={11} />
      </G>
    </Steps>
  );
}
