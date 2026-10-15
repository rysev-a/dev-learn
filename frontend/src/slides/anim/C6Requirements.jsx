import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 6, слайд 10: порядок кванторов в требованиях к системе —
   «для каждого запроса найдётся обработчик» и «найдётся обработчик
   для каждого запроса»; скрытые кванторы. */

const LABELS = ["Требования", "∀ → ∃", "∃ → ∀", "Скрытые", "Выписать"];
const CAPTION = [
  "Перенесём это на язык разработки",
  "«Для каждого запроса найдётся обработчик» — нормально: под каждый тип свой обработчик",
  "«Найдётся обработчик для каждого запроса» — универсальная заглушка, одинаково отвечающая на всё",
  "Требования почти всегда содержат скрытые кванторы, и их порядок — часть контракта",
  "Прежде чем спорить на планировании, выпишите кванторы явно — часто спорят о разных формулах",
];
const REQ = ["GET /a", "POST /b", "PUT /c"];

export default function C6Requirements({ cues }) {
  const ctl = useSteps(cues || [2.7, 9.2, 17.4, 22.8], 3000);
  const { step } = ctl;
  const show = step === 1 || step === 2;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="80" mono size={16} o={step === 0 ? 1 : 0} color="var(--s-accent)">запросы ↔ обработчики</Txt>
      <G o={show ? 1 : 0}>
        {REQ.map((t, i) => (
          <Pill key={t} x={60} y={40 + i * 36} w={74} h={26} text={t} stroke="var(--s-blue)" size={9.5} />
        ))}
        {step === 1
          ? [0, 1, 2].map((i) => (
              <g key={i}>
                <Pill x={290} y={40 + i * 36} w={90} h={26} text={`handler_${i + 1}`} stroke="var(--s-accent)" size={9.5} />
                <Arrow x1={98} y1={40 + i * 36} x2={244} y2={40 + i * 36} c="g" />
              </g>
            ))
          : (
              <g>
                <Pill x={290} y={76} w={110} h={34} text="catch_all" stroke="var(--s-red)" size={10} />
                {[0, 1, 2].map((i) => (
                  <Arrow key={i} x1={98} y1={40 + i * 36} x2={236} y2={76} c="r" />
                ))}
              </g>
            )}
        <Txt x="180" y="156" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">∀ запрос ∃ обработчик</Txt>
        <Txt x="180" y="156" mono size={11} o={step === 2 ? 1 : 0} color="var(--s-red)">∃ обработчик ∀ запрос</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <Txt x="180" y="44" size={11}>«у каждого пользователя есть тариф»</Txt>
        <Txt x="180" y="72" size={11}>«найдётся сервер для всех клиентов»</Txt>
        <Txt x="180" y="100" size={11}>«любой платёж обрабатывается»</Txt>
        <Txt x="180" y="140" mono size={12} color="var(--s-amber)">∀ ∃ — прячутся в обычных словах</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Pill x={100} y={64} w={150} h={36} text="∀r ∃h  handles(h, r)" stroke="var(--s-accent)" size={10} />
        <Txt x="196" y="68" mono size={15}>≠</Txt>
        <Pill x={260} y={64} w={150} h={36} text="∃h ∀r  handles(h, r)" stroke="var(--s-red)" size={10} />
        <Txt x="180" y="120" size={10}>спорили о разных формулах</Txt>
      </G>
    </Steps>
  );
}
