import { Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 5: универсум и дополнение. Пользователи системы, администраторы A,
   дополнение ¬A; затем универсум меняется на «людей на планете» —
   дополнение растёт, а A остаётся прежним. */

const LABELS = ["Договор", "Универсум", "Дополнение", "Другой U", "В коде"];
const CAPTION = [
  "Четвёртая операция — дополнение: сначала нужно договориться, от чего считать",
  "Универсум U — все элементы, которые мы вообще рассматриваем",
  "Дополнение администраторов A — все остальные пользователи",
  "Сменили универсум на людей планеты — дополнение стало другим, а A то же",
  "В коде это «всё, что не попало в фильтр»",
];

const USERS = Array.from({ length: 12 }, (_, i) => [110 + (i % 4) * 46, 52 + Math.floor(i / 4) * 30]);
const ADMIN = new Set([0, 1, 4, 5]);
const EXTRA = [];
for (const x of [16, 30, 44, 318, 332, 346])
  for (let y = 28; y <= 128; y += 20) EXTRA.push([x, y]);

export default function Complement({ cues }) {
  const ctl = useSteps(cues || [5.4, 12.0, 17.5, 24.4], 3000);
  const { step } = ctl;
  const big = step >= 3;
  const frame = big
    ? { x: 6, y: 8, w: 348, h: 138 }
    : { x: 78, y: 26, w: 204, h: 114 };
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <rect
        className="a-hull a-t"
        x={frame.x}
        y={frame.y}
        width={frame.w}
        height={frame.h}
        rx="12"
        style={{ opacity: step >= 1 ? 1 : 0, stroke: "var(--s-muted)" }}
      />
      <Txt x={frame.x + 10} y={frame.y + 12} anchor="start" o={step >= 1 && !big ? 1 : 0}>
        U · все пользователи системы
      </Txt>
      <Txt x={frame.x + 10} y={frame.y + 12} anchor="start" o={big ? 1 : 0}>
        U · люди на планете
      </Txt>

      <circle
        cx="133"
        cy="66"
        r="38"
        className="a-ring a a-t"
        style={{ opacity: step >= 2 ? 1 : 0, stroke: "var(--s-blue)" }}
      />
      <Txt x="128" y="134" o={step >= 2 ? 1 : 0} color="var(--s-blue)">
        A · администраторы
      </Txt>

      {USERS.map(([x, y], i) => {
        const adm = ADMIN.has(i);
        const hl = step >= 2;
        return (
          <Dot
            key={i}
            x={x}
            y={y}
            r={9}
            stroke={hl ? (adm ? "var(--s-blue)" : "var(--s-amber)") : "var(--s-muted)"}
            fill={hl ? (adm ? "var(--s-blue)" : "var(--s-amber)") : "var(--s-panel2)"}
            fillOpacity={hl ? 0.3 : 1}
          />
        );
      })}
      {EXTRA.map(([x, y], i) => (
        <Dot
          key={`e${i}`}
          x={x}
          y={y}
          r={4.5}
          o={big ? 1 : 0}
          stroke="var(--s-amber)"
          fill="var(--s-amber)"
          fillOpacity={0.3}
        />
      ))}
      <Txt x="242" y="134" o={step >= 2 ? 1 : 0} color="var(--s-amber)" anchor="middle">
        ¬A · остальные
      </Txt>
      <G o={step >= 4 ? 1 : 0} y={step >= 4 ? 0 : 6}>
        <rect x="64" y="148" width="232" height="18" rx="6" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <text x="180" y="161" textAnchor="middle" className="a-mono" style={{ fontSize: 10 }}>
          {"[u for u in U if u not in A]"}
        </text>
      </G>
    </Steps>
  );
}
