import { G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Слайд 2: что такое множество. Справа — множество гостей (три имени,
   без повторов и порядка), слева — список, где имена повторяются и
   привязаны к порядковым номерам. */

const LABELS = ["Набор", "Состав", "Без повторов", "Список", "Порядок"];
const CAPTION = [
  "Множество — набор элементов",
  "Известно ровно две вещи: кто внутри и что больше никого нет",
  "Ни порядка, ни повторов: вторая «Аня» в множество не добавляется",
  "В списке один человек может встретиться дважды, в множестве — нет",
  "Порядок в списке изменился — множество гостей то же самое",
];

const SET_SLOTS = [
  [270, 62],
  [270, 88],
  [270, 114],
];
const NAMES = ["Аня", "Борис", "Вера"];
// Элементы списка: у каждого свой id, чтобы при перестановке они ехали, а не пересоздавались.
const LIST = [
  { id: "a1", n: "Аня", p: [0, 1] },
  { id: "b", n: "Борис", p: [1, 2] },
  { id: "a2", n: "Аня", p: [2, 3] },
  { id: "v", n: "Вера", p: [3, 0] },
];

export default function ListVsSet({ cues }) {
  const ctl = useSteps(cues || [1.8, 8.5, 13.4, 20.4], 2800);
  const { step } = ctl;
  const shift = [0, 0, 1, 1, 2][step];
  const [dx, dy] = SET_SLOTS[shift % 3];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <circle cx="270" cy="88" r="62" className="a-ring a" />
      <Txt x="270" y="164">множество гостей</Txt>

      {NAMES.map((n, i) => {
        const [x, y] = SET_SLOTS[(i + shift) % 3];
        return (
          <Pill key={n} x={x} y={y} w={56} text={n} o={step >= 1 ? 1 : 0} stroke="var(--s-accent)" />
        );
      })}

      {/* повторная «Аня»: стучится снаружи и сливается с настоящей */}
      <Pill
        x={step >= 2 ? dx : 180}
        y={step >= 2 ? dy : 40}
        w={56}
        text="Аня"
        o={step === 1 ? 0.9 : 0}
        stroke="var(--s-amber)"
      />
      <Txt x="180" y="22" o={step === 1 ? 1 : 0} color="var(--s-amber)">
        ещё одна «Аня»?
      </Txt>
      <Pill x={336} y={22} w={40} text="Глеб" o={step >= 1 && step <= 2 ? 0.55 : 0} stroke="var(--s-muted)" />
      <Txt x="336" y="42" o={step >= 1 && step <= 2 ? 1 : 0}>
        ∉ гостей
      </Txt>

      {/* список */}
      <g className="a-t" style={{ opacity: step >= 3 ? 1 : 0 }}>
        <rect x="14" y="26" width="118" height="116" rx="10" className="a-ring" style={{ stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
      </g>
      <Txt x="73" y="164" o={step >= 3 ? 1 : 0}>список гостей</Txt>
      {LIST.map((it) => {
        const k = step >= 4 ? it.p[1] : it.p[0];
        return (
          <G key={it.id} x={0} y={52 + k * 25} o={step >= 3 ? 1 : 0}>
            <text x="28" y="3.7" textAnchor="middle" className="a-mono">{k + 1}</text>
            <Pill x={85} y={0} w={56} text={it.n} stroke={it.n === "Аня" ? "var(--s-amber)" : "var(--s-border)"} />
          </G>
        );
      })}
    </Steps>
  );
}
