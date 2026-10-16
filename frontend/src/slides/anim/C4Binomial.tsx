import { G, Pill, Steps, Txt, useSteps } from "./kit.tsx";
import { binom } from "./tri.ts";
import type { SceneItem } from "./dsl.ts";

/* Глава 4, слайд 5: бином Ньютона. (a+b)ⁿ — перебор способов выбрать a или b
   в каждой скобке; коэффициенты — строка Паскаля. */

const LABELS = ["Бином", "(a+b)²", "Коэффициент", "(a+b)⁴"];
const CAPTION = [
  "Теперь бином Ньютона: степень суммы двух слагаемых",
  "В каждой скобке берём a или b — перебираем все способы и складываем: aa + ab + ba + bb",
  "Член с n − k множителями a и k множителями b встречается ровно C(n, k) раз",
  "Коэффициенты раскрытия — строка Паскаля целиком: 1, 4, 6, 4, 1",
];

const terms4 = (n: number): { k: number; c: number; t: string }[] =>
  Array.from({ length: n + 1 }, (_, k) => ({
    k,
    c: binom(n, k),
    t: `${n - k > 0 ? "a" + (n - k > 1 ? sup(n - k) : "") : ""}${k > 0 ? "b" + (k > 1 ? sup(k) : "") : ""}`,
  }));
function sup(n: number) {
  return String(n)
    .split("")
    .map((d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[+d])
    .join("");
}

export default function C4Binomial({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [4.0, 13.4, 22.7], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={86} mono size={30} o={step === 0 ? 1 : 0} color="var(--s-accent)">(a + b)ⁿ</Txt>

      <G o={step === 1 ? 1 : 0}>
        <Txt x={180} y={22} mono size={12}>(a + b)(a + b)</Txt>
        {["aa", "ab", "ba", "bb"].map((t, i) => (
          <Pill key={t} x={60 + i * 80} y={64} w={48} text={t} stroke={t === "ab" || t === "ba" ? "var(--s-amber)" : "var(--s-blue)"} />
        ))}
        <Txt x={180} y={112} mono size={13} color="var(--s-accent)">a² + 2ab + b²</Txt>
        <Txt x={180} y={134} size={9.5}>ab и ba — одно слагаемое, поэтому коэффициент 2</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        <Txt x={180} y={22} mono size={12}>(a + b)³</Txt>
        {terms4(3).map(({ c, t, k }, i) => (
          <g key={k}>
            <Pill x={48 + i * 88} y={64} w={32} text={c} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
            <Pill x={48 + i * 88} y={102} w={46} text={t} stroke="var(--s-blue)" />
          </g>
        ))}
        <Txt x={180} y={140} mono size={11}>коэффициент при aⁿ⁻ᵏbᵏ — C(n, k)</Txt>
      </G>

      <G o={step >= 3 ? 1 : 0}>
        <Txt x={180} y={22} mono size={12}>(a + b)⁴</Txt>
        {terms4(4).map(({ c, t, k }, i) => (
          <g key={k}>
            <Pill x={40 + i * 70} y={60} w={34} text={c} stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={14} />
            <Pill x={40 + i * 70} y={98} w={50} text={t} stroke="var(--s-blue)" size={9.5} />
          </g>
        ))}
        <Txt x={180} y={140} mono size={12} color="var(--s-accent)">строка Паскаля: 1 · 4 · 6 · 4 · 1</Txt>
      </G>
    </Steps>
  );
}
