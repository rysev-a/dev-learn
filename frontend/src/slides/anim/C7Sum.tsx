import { G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 7, слайд 4: классическое доказательство по индукции:
   1 + 2 + … + n = n(n+1)/2. */

const LABELS = ["Утверждение", "База", "Переход", "Преобразуем", "Вывод"];
const CAPTION = [
  "Классический пример: сумма чисел от 1 до n равна n(n + 1)/2",
  "База: при n = 1 слева 1, справа 1·2/2 — тоже 1: сходится",
  "Переход: пусть формула верна для k; докажем для k + 1",
  "Прибавим к обеим частям k + 1 и аккуратно преобразуем — получится вид формулы для следующего числа",
  "Круг замкнулся: формула верна для всех n",
];

export default function C7Sum({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [9.4, 16.9, 20.5, 30.2], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x={180} y={86} mono size={20} o={step === 0 ? 1 : 0} color="var(--s-accent)">1 + 2 + … + n = n(n+1)/2</Txt>
      <G o={step === 1 ? 1 : 0}>
        <Txt x={180} y={46} mono size={13}>n = 1</Txt>
        <Txt x={110} y={86} mono size={22}>1</Txt>
        <Txt x={180} y={86} mono size={22} color="var(--s-accent)">=</Txt>
        <Txt x={250} y={86} mono size={20}>1·2 / 2</Txt>
        <Txt x={180} y={130} mono size={12} color="var(--s-accent)">✓ сходится</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x={180} y={40} mono size={12} color="var(--s-blue)">пусть верно для k:</Txt>
        <Txt x={180} y={66} mono size={15}>1 + … + k = k(k+1)/2</Txt>
        <Txt x={180} y={110} mono size={12} color="var(--s-amber)">докажем для k + 1:</Txt>
        <Txt x={180} y={134} mono size={15}>1 + … + (k+1) = (k+1)(k+2)/2</Txt>
      </G>
      <G o={step === 3 ? 1 : 0}>
        {[
          ["1 + … + k + (k+1)", "var(--s-text)"],
          ["= k(k+1)/2 + (k+1)", "var(--s-blue)"],
          ["= (k+1)(k/2 + 1)", "var(--s-blue)"],
          ["= (k+1)(k+2)/2", "var(--s-accent)"],
        ].map(([t, c], i) => (
          <g key={t} className="a-t" style={{ opacity: step === 3 ? 1 : 0, transitionDelay: `${i * 380}ms` }}>
            <text x="60" y={40 + i * 28} className="a-mono" style={{ fontSize: 14, fill: c }}>{t}</text>
          </g>
        ))}
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <Txt x={180} y={66} mono size={16}>база ✓  +  переход ✓</Txt>
        <Txt x={180} y={104} mono size={22} color="var(--s-accent)">∀n: формула верна</Txt>
      </G>
    </Steps>
  );
}
