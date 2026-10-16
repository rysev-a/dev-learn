import { Arrow, Dot, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 2, слайд 11: инъекция, сюръекция, биекция. Три раскладки стрелок
   между двумя столбцами; в конце стрелки биекции разворачиваются. */

const LABELS = ["Виды", "Инъекция", "Сюръекция", "Биекция", "Обратная"];
const CAPTION = [
  "Функции различают по тому, как они заполняют выход",
  "Инъекция: разные входы дают разные выходы — ничего не склеивается, но места могут остаться",
  "Сюръекция: каждый элемент выхода кем-то занят — пустых мест нет, но входы могут склеиваться",
  "Биекция — и то и другое: один к одному, и функцию можно развернуть",
  "Обратная функция: кодирование и декодирование живут на биекциях",
];
const LX = 100;
const RX = 260;
const SLOT = [28, 64, 100, 136];
// [число входов, число выходов, пары (вход → выход)]
const KIND: Record<number, [number, number, [number, number][]]> = {
  1: [3, 4, [[0, 0], [1, 1], [2, 3]]],
  2: [4, 3, [[0, 0], [1, 0], [2, 1], [3, 2]]],
  3: [3, 3, [[0, 1], [1, 2], [2, 0]]],
  4: [3, 3, [[0, 1], [1, 2], [2, 0]]],
};

export default function C2Mapping({ cues }: { cues?: number[] }) {
  const ctl = useSteps(cues || [3.4, 9.9, 17.1, 22.9], 3200);
  const { step } = ctl;
  const k = step === 0 ? 3 : step;
  const [nl, nr] = KIND[k]!;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      {SLOT.map((y, i) => (
        <Dot key={`l${i}`} x={LX} y={y} text={["a", "b", "c", "d"][i]} o={i < nl ? 1 : 0} stroke="var(--s-blue)" />
      ))}
      {SLOT.map((y, i) => (
        <Dot key={`r${i}`} x={RX} y={y} text={[1, 2, 3, 4][i]} o={i < nr ? 1 : 0} stroke="var(--s-amber)" />
      ))}
      {[1, 2, 3].map((kk) =>
        KIND[kk]![2].map(([a, b], i) => (
          <Arrow
            key={`${kk}-${i}`}
            x1={LX + 14}
            y1={SLOT[a]!}
            x2={RX - 14}
            y2={SLOT[b]!}
            c={kk === 1 ? "g" : kk === 2 ? "y" : "b"}
            o={(step === 0 ? kk === 3 : step === kk) ? 1 : 0}
          />
        )),
      )}
      {KIND[4]![2].map(([a, b], i) => (
        <Arrow key={`inv${i}`} x1={RX - 14} y1={SLOT[b]!} x2={LX + 14} y2={SLOT[a]!} c="g" o={step === 4 ? 1 : 0} />
      ))}
      <Txt x={180} y={162} mono size={11} o={step === 1 ? 1 : 0} color="var(--s-accent)">число 3 никому не достаётся, но склеек нет</Txt>
      <Txt x={180} y={162} mono size={11} o={step === 2 ? 1 : 0} color="var(--s-amber)">все числа заняты, но a и b склеились</Txt>
      <Txt x={180} y={162} mono size={11} o={step === 3 ? 1 : 0} color="var(--s-blue)">один к одному</Txt>
      <Txt x={180} y={162} mono size={11} o={step === 4 ? 1 : 0} color="var(--s-accent)">f⁻¹: стрелки в обратную сторону</Txt>
    </Steps>
  );
}
