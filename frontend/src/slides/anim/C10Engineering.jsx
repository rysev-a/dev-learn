import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 10, слайд 11: вероятность в инженерии — кэш, фильтр Блума,
   A/B-тест, ретраи и реплики. */

const LABELS = ["Инженерия", "Кэш", "Блум", "A/B", "Ретраи"];
const CAPTION = [
  "Вероятностное мышление проявляется в инженерии на каждом шагу",
  "Оценка кэша: вероятность попадания × выигрыш − вероятность промаха × цена",
  "Фильтр Блума: «возможно, есть» с контролируемой ошибкой и «точно нет» без ошибок — экономит запросы к базе миллионами",
  "A/B-тест — Байес в другую сторону: данные копятся, уверенность растёт, и мы решаем, когда она перевалила порог",
  "Число ретраев и реплик — прикидка вероятностей отказа: p² у двух независимых реплик",
];

export default function C10Engineering({ cues }) {
  const ctl = useSteps(cues || [4.2, 15.1, 23.5, 31.6], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        {["кэш", "Блум", "A/B", "ретраи"].map((t, i) => (
          <Pill key={t} x={50 + i * 86} y={80} w={76} h={46} text={t} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
        ))}
      </G>
      <G o={step === 1 ? 1 : 0}>
        <Pill x={90} y={44} w={150} h={36} text="попал: p · выигрыш" stroke="var(--s-accent)" size={10.5} />
        <Txt x="180" y="48" mono size={16}>−</Txt>
        <Pill x={270} y={44} w={150} h={36} text="промах: (1−p) · цена" stroke="var(--s-red)" size={10.5} />
        <Txt x="180" y="108" mono size={13} color="var(--s-accent)">решаем по ожидаемой выгоде</Txt>
        <Txt x="180" y="132" size={10}>ёмкость и вытеснение — на этих числах</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Pill x={70} y={60} w={100} h={40} text="запрос" stroke="var(--s-blue)" size={11} />
        <rect x="136" y="46" width="70" height="68" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <Txt x="171" y="84" mono size={12} color="var(--s-accent)">Блум</Txt>
        <Pill x={290} y={42} w={120} h={26} text="«точно нет» ✓" stroke="var(--s-accent)" size={10} />
        <Pill x={290} y={82} w={120} h={26} text="«возможно» → БД" stroke="var(--s-amber)" size={10} />
        <Txt x="180" y="140" size={10}>большинство «нет» отсекается без запроса к базе</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        <line x1="40" y1="130" x2="330" y2="130" style={{ stroke: "var(--s-border)" }} />
        <line x1="40" y1="40" x2="330" y2="40" style={{ stroke: "var(--s-amber)", strokeDasharray: "4 4" }} />
        <Txt x="318" y="34" size={9} color="var(--s-amber)">порог</Txt>
        <path d="M40 120 C100 118 140 100 180 80 C230 56 280 44 322 38" pathLength="1" className="a-t" style={{ fill: "none", stroke: "var(--s-accent)", strokeWidth: 2.4, strokeDasharray: 1, strokeDashoffset: step === 3 ? 0 : 1, transition: "stroke-dashoffset 2.4s ease" }} />
        <Txt x="180" y="150" size={10}>уверенность, что вариант B лучше, растёт с данными</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        {[
          ["1 реплика", 0.01, "var(--s-red)"],
          ["2 реплики", 0.0001, "var(--s-amber)"],
          ["3 реплики", 0.000001, "var(--s-accent)"],
        ].map(([t, v, c], i) => (
          <g key={t}>
            <text x="30" y={52 + i * 32} className="a-mono" style={{ fontSize: 11 }}>{t}</text>
            <rect className="a-t" x="120" y={38 + i * 32} width={step >= 4 ? 190 - i * 70 : 0} height="20" rx="4" style={{ fill: c, fillOpacity: 0.35, stroke: c, transitionDelay: `${i * 250}ms` }} />
            <text x={126 + 190 - i * 70} y={52 + i * 32} className="a-mono" style={{ fontSize: 10, fill: c }}>{`p = ${["10⁻²", "10⁻⁴", "10⁻⁶"][i]}`}</text>
          </g>
        ))}
        <Txt x="180" y="144" size={10}>при p = 1 % отказа одной реплики</Txt>
      </G>
    </Steps>
  );
}
