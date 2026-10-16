import { Dot, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 11: где множества живут в работе. Список → хеш-сет (дедупликация),
   SQL-операции, теги и сегменты, цикл с флагом против одной операции. */

const LABELS = ["Список", "Хеш-сет", "SQL", "Продукт", "Код"];
const CAPTION = [
  "Посмотрим, где это живёт в повседневной работе: вот список значений с повторами",
  "Проверка принадлежности в хеш-сете стоит константу: дедупликация — просто перевод списка в множество",
  "В SQL те же операции — UNION, INTERSECT, EXCEPT — и база выполняет их на миллионах строк",
  "Фильтры аналитики, сегменты пользователей, теги статей — под капотом множества и пересечения",
  "Когда вы думаете множествами, вместо цикла с флагом — одна операция пересечения",
];

const VALS = [3, 1, 3, 2, 1];
const BUCKET = { 3: 130, 1: 180, 2: 230 };

export default function SetsInUse({ cues }) {
  const ctl = useSteps(cues || [3.3, 10.1, 16.9, 23.3], 3000);
  const { step } = ctl;
  const first = new Set();
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {/* список → хеш-сет */}
      <G o={step <= 1 ? 1 : 0}>
        {[0, 1, 2].map((b) => (
          <rect
            key={b}
            className="a-t"
            x={110 + b * 50}
            y="102"
            width="40"
            height="36"
            rx="8"
            style={{ fill: "none", stroke: "var(--s-accent)", strokeWidth: 1.4, strokeDasharray: "4 3", opacity: step >= 1 ? 1 : 0 }}
          />
        ))}
        {VALS.map((v, k) => {
          const dup = first.has(v);
          first.add(v);
          const to = step >= 1;
          return (
            <Dot
              key={k}
              x={to ? BUCKET[v] : 70 + k * 55}
              y={to ? 120 : 44}
              text={v}
              stroke={dup && to ? "var(--s-amber)" : "var(--s-muted)"}
              o={dup && to ? 0 : 1}
            />
          );
        })}
        <Txt x="180" y="80" mono o={step === 1 ? 1 : 0} color="var(--s-accent)" size={11}>
          set([3, 1, 3, 2, 1]) = {"{3, 1, 2}"}
        </Txt>
        <Txt x="180" y="18" o={step === 0 ? 1 : 0}>
          список значений
        </Txt>
      </G>

      {/* SQL */}
      <G o={step === 2 ? 1 : 0}>
        {[
          ["A UNION B", "объединение"],
          ["A INTERSECT B", "пересечение"],
          ["A EXCEPT B", "разность"],
        ].map(([code, name], i) => (
          <g key={code}>
            <text x="40" y={44 + i * 34} className="a-mono" style={{ fontSize: 12 }}>
              {code}
            </text>
            <text x="170" y={44 + i * 34} className="a-mono" style={{ fill: "var(--s-accent)", fontSize: 12 }}>
              →
            </text>
            <text x="196" y={44 + i * 34} className="a-cap" style={{ fontSize: 12 }}>
              {name}
            </text>
          </g>
        ))}
        <Txt x="180" y="150" color="var(--s-amber)">
          миллионы строк за один запрос
        </Txt>
      </G>

      {/* теги и сегменты */}
      <G o={step === 3 ? 1 : 0}>
        <Pill x={70} y={50} w={78} text="python" stroke="var(--s-blue)" />
        <Pill x={180} y={50} w={78} text="базы" stroke="var(--s-amber)" />
        <Pill x={290} y={50} w={78} text="алгоритмы" stroke="var(--s-accent)" />
        <Txt x="125" y="54" mono color="var(--s-accent)" size={16}>∩</Txt>
        <Txt x="235" y="54" mono color="var(--s-accent)" size={16}>∩</Txt>
        <Txt x="180" y="92" mono color="var(--s-accent)" size={14}>↓</Txt>
        <Pill x={180} y={116} w={210} text="статьи со всеми тремя тегами" stroke="var(--s-accent)" fill="var(--s-green)" />
      </G>

      {/* цикл с флагом против одной операции */}
      <G o={step >= 4 ? 1 : 0}>
        <g className="a-t" style={{ opacity: step >= 4 ? 0.45 : 1 }}>
          {["found = False", "for x in a:", "  if x in b: found = True"].map((l, i) => (
            <text key={i} x="40" y={40 + i * 16} className="a-mono" style={{ fontSize: 11 }} xmlSpace="preserve">
              {l}
            </text>
          ))}
          <line x1="36" y1="60" x2="250" y2="38" style={{ stroke: "var(--s-red)", strokeWidth: 1.6 }} />
        </g>
        <Pill x={180} y={116} w={110} h={34} text="a & b" size={18} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" />
        <Txt x="180" y="152">одна операция вместо цикла</Txt>
      </G>
    </Steps>
  );
}
