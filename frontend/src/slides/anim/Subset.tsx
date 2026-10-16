import { Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 8: подмножества. Внутри большого множества B живёт меньшее A;
   подписи меняются с абстрактных на числа и на права ролей. В конце —
   проверка через пересечение: A ∩ B = A. */

const LABELS = ["Вложение", "Числа", "Права", "Проверка"];
const CAPTION = [
  "Если каждый элемент A есть и в B, то A — подмножество B: A ⊆ B",
  "Чётные числа — подмножество целых: каждое чётное является целым",
  "Права редактора — подмножество прав администратора: без настройки системы",
  "Проверка: пересечение с большим множеством совпало с меньшим — оно вложено",
];

const INSIDE: [number, number][] = [
  [122, 76],
  [158, 76],
  [122, 108],
  [158, 108],
];
const OUTSIDE: [number, number][] = [
  [205, 52],
  [236, 72],
  [236, 104],
  [205, 124],
];
const WORDS = [
  [["a", "b", "c", "d"], ["e", "f", "g", "h"], "B", "A"],
  [["2", "4", "6", "8"], ["1", "3", "5", "7"], "ℤ · целые", "чётные"],
  [
    ["чт", "зап", "удл", "пуб"],
    ["нст", "рол", "клч", "бэк"],
    "администратор",
    "редактор",
  ],
];

export default function Subset({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [7.3, 11.0, 17.9], 3000);
  const { step } = ctl;
  const v = Math.min(step, 2);
  const items = [
    ...INSIDE.map((p, i) => ({ p, i, inn: true })),
    ...OUTSIDE.map((p, i) => ({ p, i, inn: false })),
  ];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <circle cx="180" cy="88" r="70" className="a-ring" style={{ stroke: "var(--s-accent)" }} />
      <circle
        cx="140"
        cy="90"
        r="44"
        className="a-t"
        style={{
          stroke: "var(--s-amber)",
          strokeWidth: 2,
          fill: "var(--s-amber)",
          fillOpacity: step >= 3 ? 0.28 : 0,
        }}
      />
      {WORDS.map(([inn, out, big, small], vi) => (
        <g key={vi}>
          {items.map(({ p, i, inn: isIn }) => (
            <g key={`${isIn}${i}`} className="a-t" style={{ opacity: v === vi ? 1 : 0 }}>
              <circle cx={p[0]} cy={p[1]} r="13" style={{ fill: "var(--s-panel2)", stroke: isIn ? "var(--s-amber)" : "var(--s-muted)", strokeWidth: 1.5 }} />
              <text x={p[0]} y={p[1] + 3.6} textAnchor="middle" className="a-mono" style={{ fontSize: vi === 2 ? 8.5 : 11 }}>
                {(isIn ? inn : out)[i]}
              </text>
            </g>
          ))}
          <Txt x={6} y={22} anchor="start" o={v === vi ? 1 : 0} color="var(--s-accent)">
            B: {big}
          </Txt>
          <Txt x={6} y={38} anchor="start" o={v === vi ? 1 : 0} color="var(--s-amber)">
            A: {small}
          </Txt>
        </g>
      ))}
      <Txt x={300} y={40} mono o={step < 3 ? 1 : 0} color="var(--s-accent)" size={13}>
        A ⊆ B
      </Txt>
      <Txt x={300} y={40} mono o={step >= 3 ? 1 : 0} color="var(--s-amber)" size={13}>
        A ∩ B = A
      </Txt>
      <Txt x={300} y={60} mono o={step >= 3 ? 1 : 0} color="var(--s-accent)" size={13}>
        ⇒ A ⊆ B
      </Txt>
    </Steps>
  );
}
