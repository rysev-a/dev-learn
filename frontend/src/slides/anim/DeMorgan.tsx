import { Dot, Steps, Txt, useSteps } from "./kit.tsx";

/* Слайд 6: законы де Моргана. Заливка на диаграмме Венна показывает
   ¬(A ∪ B) и ¬(A ∩ B); затем доказательство на одном элементе, примеры
   (магазин, задание), частая ошибка «не A или не B», SQL и итог. */

const LABELS = [
  "Законы",
  "Первый",
  "Второй",
  "Почему",
  "Товары",
  "Задание",
  "Ошибка",
  "Верно",
  "База",
  "Итог",
];
const CAPTION = [
  "Операции подчиняются законам; самые знаменитые — законы де Моргана",
  "Первый: дополнение объединения — всё вне обоих кругов, то есть ¬A ∩ ¬B",
  "Второй: дополнение пересечения — всё, кроме общей части, то есть ¬A ∪ ¬B",
  "Почему так: элемент вне объединения не входит ни в A, ни в B — значит, он в обоих дополнениях",
  "Магазин: «не дешёвые и не старые» — то же, что «не (дешёвый или старый)»",
  "Задание принято, если тесты зелёные и ревью пройдено; не принято — если нарушено хотя бы одно",
  "Частая ошибка: «не админ или не редактор» пропускает почти всех",
  "Верно: «не админ и не редактор» — или «не» от скобки с «или»",
  "В коде и в базе данных — то же самое: отрицание переворачивает «или» и «и»",
  "Отрицание переворачивает «или» в «и» и обратно",
];

// категории точек: a — только A, b — только B, ab — оба, n — ни там ни там
const DOTS = [
  { id: "a1", c: "a", x: 126, y: 56 },
  { id: "a2", c: "a", x: 124, y: 92 },
  { id: "c1", c: "ab", x: 180, y: 72 },
  { id: "b1", c: "b", x: 234, y: 56 },
  { id: "b2", c: "b", x: 236, y: 92 },
  { id: "n1", c: "n", x: 64, y: 36 },
  { id: "n2", c: "n", x: 298, y: 112 },
  { id: "n3", c: "n", x: 66, y: 112 },
];

const ACC = "var(--s-accent)";
const AMB = "var(--s-amber)";
const RED = "var(--s-red)";

// подписи кругов по шагам
const NAMES = {
  0: ["A", "B"],
  4: ["дешёвый", "старый"],
  5: ["тесты ✓", "ревью ✓"],
  6: ["админ", "редактор"],
};
const nameKey = (s: number) => (s >= 6 && s <= 7 ? 6 : s === 5 ? 5 : s === 4 ? 4 : 0);

// подсвеченные точки и цвет на шаге
function mark(step: number, d: { c: string }) {
  if (step === 4 || step === 7) return d.c === "n" ? ACC : null;
  if (step === 5) return d.c !== "ab" ? AMB : null;
  if (step === 6) return d.c !== "ab" ? RED : null;
  return null;
}

export default function DeMorgan({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [5.0, 8.5, 12.2, 25.4, 38.9, 51.7, 64.9, 69.7, 76.8], 3000);
  const { step } = ctl;
  const venn = step <= 7 ? 1 : 0.06;
  const showDots = step >= 4 && step <= 7;
  const outOp = step === 1 ? 0.35 : step === 4 || step === 7 ? 0.3 : 0;
  const lensColor = step === 6 ? RED : AMB;
  const lensOp = step === 2 ? 0.35 : step === 5 || step === 6 ? 0.3 : 0;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <defs>
        <clipPath id="dmg-a">
          <circle cx="150" cy="72" r="46" />
        </clipPath>
        <mask id="dmg-out">
          <rect width="360" height="170" fill="#fff" />
          <circle cx="150" cy="72" r="46" fill="#000" />
          <circle cx="210" cy="72" r="46" fill="#000" />
        </mask>
        <mask id="dmg-lens">
          <rect width="360" height="170" fill="#fff" />
          <g clipPath="url(#dmg-a)">
            <circle cx="210" cy="72" r="46" fill="#000" />
          </g>
        </mask>
      </defs>
      <g className="a-t" style={{ opacity: venn }}>
        <rect x="40" y="10" width="280" height="124" rx="10" className="a-ring" style={{ stroke: "var(--s-border)" }} />
        <g mask="url(#dmg-out)">
          <rect
            className="a-t"
            x="40"
            y="10"
            width="280"
            height="124"
            rx="10"
            style={{ fill: ACC, opacity: outOp }}
          />
        </g>
        <g mask="url(#dmg-lens)">
          <rect
            className="a-t"
            x="40"
            y="10"
            width="280"
            height="124"
            rx="10"
            style={{ fill: lensColor, opacity: lensOp }}
          />
        </g>
        <circle cx="150" cy="72" r="46" className="a-ring a" />
        <circle cx="210" cy="72" r="46" className="a-ring b" />
        {Object.entries(NAMES).map(([k, [a, b]]) => (
          <g key={k}>
            <Txt x={124} y={40} mono o={+k === nameKey(step) ? 1 : 0} size={9.5}>{a}</Txt>
            <Txt x={236} y={40} mono o={+k === nameKey(step) ? 1 : 0} size={9.5}>{b}</Txt>
          </g>
        ))}
        <Txt x={52} y={24} anchor="start">U</Txt>
      </g>

      {DOTS.map((d) => {
        const m = mark(step, d);
        const solo = step === 3 && d.id === "n1";
        return (
          <Dot
            key={d.id}
            x={d.x}
            y={d.y}
            r={solo ? 10 : 8}
            o={showDots || solo ? 1 : 0}
            stroke={m || (solo ? ACC : "var(--s-muted)")}
            fill={m || (solo ? ACC : "var(--s-panel2)")}
            fillOpacity={m || solo ? 0.35 : 1}
          />
        );
      })}
      <Txt x={64} y={62} o={step === 3 ? 1 : 0} mono color={ACC} size={10}>
        x ∉ A, x ∉ B
      </Txt>
      <Txt x={180} y={154} mono o={step === 3 ? 1 : 0} color={ACC} size={11}>
        x ∈ ¬A ∩ ¬B ⇒ x ∈ ¬(A ∪ B)
      </Txt>
      <Txt x={180} y={154} mono o={step === 1 ? 1 : 0} color={ACC} size={12}>
        ¬(A ∪ B) = ¬A ∩ ¬B
      </Txt>
      <Txt x={180} y={154} mono o={step === 2 ? 1 : 0} color={AMB} size={12}>
        ¬(A ∩ B) = ¬A ∪ ¬B
      </Txt>
      <Txt x={180} y={154} mono o={step === 4 ? 1 : 0} color={ACC} size={10.5}>
        не (дешёвый или старый) = не дешёвый и не старый
      </Txt>
      <Txt x={180} y={154} mono o={step === 5 ? 1 : 0} color={AMB} size={10.5}>
        не (тесты и ревью) = красные тесты или нет ревью
      </Txt>
      <Txt x={180} y={154} mono o={step === 6 ? 1 : 0} color={RED} size={10.5}>
        ¬A ∪ ¬B: все, кроме тех, кто и админ, и редактор
      </Txt>
      <Txt x={180} y={154} mono o={step === 7 ? 1 : 0} color={ACC} size={10.5}>
        не админ И не редактор = не (админ или редактор)
      </Txt>

      <g className="a-t" style={{ opacity: step === 8 ? 1 : 0 }}>
        <text x="180" y="42" textAnchor="middle" className="a-mono" style={{ fontSize: 11 }}>!(a || b) === !a &amp;&amp; !b</text>
        <text x="180" y="62" textAnchor="middle" className="a-mono" style={{ fontSize: 11 }}>!(a &amp;&amp; b) === !a || !b</text>
        <text x="180" y="96" textAnchor="middle" className="a-mono" style={{ fontSize: 11, fill: ACC }}>WHERE NOT (a OR b)</text>
        <text x="180" y="112" textAnchor="middle" className="a-mono" style={{ fontSize: 11, fill: ACC }}>= WHERE NOT a AND NOT b</text>
      </g>
      <Txt x={180} y={86} mono o={step >= 9 ? 1 : 0} color={ACC} size={20}>
        «или» ↔ «и»
      </Txt>
    </Steps>
  );
}
