import { Dot, G, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 6, слайд 5: квантор существования — «найдётся». Один пример
   доказывает, опровергнуть труднее; баг и «багов нет». */

const LABELS = ["Найдётся", "Гости", "Доказать", "Опровергнуть", "Баги"];
const CAPTION = [
  "Второй способ — квантор существования: «найдётся», «существует»",
  "«Среди гостей найдётся вегетарианец» истинно, если подходит хотя бы один",
  "Доказать легко — достаточно одного примера, в этом его прелесть",
  "Опровергнуть труднее: придётся объяснить, почему не подходит ни один",
  "Доказать, что баг существует, — одно воспроизведение; что багов нет, — совсем другой разговор",
];

export default function C6Exists({ cues }) {
  const ctl = useSteps(cues || [5.1, 11.7, 16.2, 20.9], 3000);
  const { step } = ctl;
  const guests = [0, 1, 2, 3, 4, 5];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <Txt x="180" y="86" mono size={44} o={step === 0 ? 1 : 0} color="var(--s-accent)">∃x  P(x)</Txt>
      <G o={step >= 1 && step <= 3 ? 1 : 0}>
        <Txt x="180" y="22" mono size={12}>∃ гость: вегетарианец</Txt>
        {guests.map((i) => {
          const yes = step === 1 || step === 2 ? i === 4 : false;
          const no = step === 3;
          return (
            <Dot
              key={i}
              x={46 + i * 54}
              y={74}
              r={18}
              text={yes ? "🥗" : no ? "✗" : "·"}
              stroke={yes ? "var(--s-accent)" : no ? "var(--s-red)" : "var(--s-muted)"}
              fill={yes ? "var(--s-green)" : "var(--s-panel2)"}
              size={12}
            />
          );
        })}
        <Txt x="180" y="128" mono size={12} o={step === 2 ? 1 : 0} color="var(--s-accent)">один подходящий — и утверждение доказано</Txt>
        <Txt x="180" y="128" mono size={12} o={step === 3 ? 1 : 0} color="var(--s-red)">надо проверить всех: никто не подходит</Txt>
        <Txt x="180" y="128" mono size={12} o={step === 1 ? 1 : 0}>подходит хотя бы один?</Txt>
      </G>
      <G o={step >= 4 ? 1 : 0}>
        <rect x="30" y="36" width="140" height="70" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-accent)", strokeWidth: 1.5 }} />
        <Txt x="100" y="64" mono size={11}>∃ баг</Txt>
        <Txt x="100" y="86" size={9.5} color="var(--s-accent)">одно воспроизведение</Txt>
        <rect x="190" y="36" width="140" height="70" rx="12" style={{ fill: "var(--s-panel2)", stroke: "var(--s-red)", strokeWidth: 1.5 }} />
        <Txt x="260" y="64" mono size={11}>¬∃ баг</Txt>
        <Txt x="260" y="86" size={9.5} color="var(--s-red)">другой разговор</Txt>
        <Txt x="180" y="140" size={10}>доказать «нет багов» — значит рассмотреть все случаи</Txt>
      </G>
    </Steps>
  );
}
