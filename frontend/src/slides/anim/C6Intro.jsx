import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 1: условия в коде — это язык; предикаты и кванторы
   позволяют говорить обо всех случаях сразу. */

const LABELS = ["Глава", "Условия", "Все случаи", "Инструменты", "Тесты"];
const CAPTION = [
  "Предикаты и кванторы",
  "Каждый день вы пишете условия: пользователь админ, массив не пуст, ответ пришёл в срок",
  "За ними стоит строгий язык, позволяющий говорить обо всех случаях сразу, а не по одному",
  "Два главных инструмента: предикаты — высказывания с переменной — и кванторы «для каждого» и «найдётся»",
  "Без них не объяснить, что значит «код работает для всех входов» — это вы доказываете каждым тестом",
];

export default function C6Intro({ cues }) {
  const ctl = useSteps(cues || [4.4, 10.6, 17.2, 26.0], 2800);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 1 ? 1 : 0}>
        {["user.is_admin", "len(items) > 0", "response.time < limit"].map((t, i) => (
          <Pill key={t} x={180} y={34 + i * 38} w={230} h={28} text={t} stroke="var(--s-accent)" size={11} />
        ))}
      </G>
      <G o={step === 2 ? 1 : 0}>
        {Array.from({ length: 24 }, (_, i) => (
          <Dot key={i} x={40 + (i % 8) * 40} y={44 + Math.floor(i / 8) * 34} r={11} text="✓" stroke="var(--s-accent)" fill="var(--s-green)" size={10} />
        ))}
        <Txt x="180" y="152" mono size={12} color="var(--s-accent)">все случаи — одним высказыванием</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Pill x={100} y={70} w={150} h={50} text="P(x)" stroke="var(--s-blue)" size={20} />
        <Txt x="100" y="110" size={9.5}>предикат</Txt>
        <Pill x={260} y={52} w={100} h={30} text="∀  для каждого" stroke="var(--s-amber)" size={11} />
        <Pill x={260} y={96} w={100} h={30} text="∃  найдётся" stroke="var(--s-amber)" size={11} />
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={180} y={50} w={250} h={34} text="test_sort(xs) → ok" stroke="var(--s-accent)" size={11} />
        <Txt x="180" y="94" mono size={13} color="var(--s-accent)">для всех входов xs</Txt>
        <Txt x="180" y="122" size={10}>это и есть квантор «для каждого»</Txt>
      </G>
    </Steps>
  );
}
