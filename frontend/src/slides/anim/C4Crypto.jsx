import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.tsx";

/* Глава 4, слайд 12: криптографические хеши живут под тем же законом:
   пространство выходов конечно, коллизия обязана случиться, но пространство
   огромно. */

const LABELS = ["Хеш", "Коллизия", "Масштаб", "Мысль"];
const CAPTION = [
  "Даже криптография живёт под этим законом, просто с огромными числами",
  "У любого хеша конечное пространство выходов: при достаточном числе файлов коллизия обязана случиться",
  "Хорошая хеш-функция делает пространство практически необозримым — на этом держатся подписи и контроль целостности",
  "Конечность — это структура, а не мелочь: принцип Дирихле рано или поздно напомнит о себе",
];

export default function C4Crypto({ cues }) {
  const ctl = useSteps(cues || [4.6, 16.0, 23.5], 3000);
  const { step } = ctl;
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step <= 1 ? 1 : 0}>
        {["файл 1", "файл 2", "файл 3", "…"].map((t, i) => (
          <Pill key={t} x={52} y={30 + i * 32} w={64} text={t} stroke="var(--s-blue)" size={9.5} />
        ))}
        <rect x="170" y="38" width="48" height="90" rx="10" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6 }} />
        <text x="194" y="88" textAnchor="middle" className="a-mono" style={{ fontSize: 14, fill: "var(--s-accent)" }}>H</text>
        {[0, 1, 2].map((i) => (
          <Arrow key={i} x1={86} y1={30 + i * 32} x2={166} y2={64 + i * 14} c="m" o={0.8} />
        ))}
        <rect x="266" y="56" width="70" height="54" rx="8" style={{ fill: "none", stroke: "var(--s-amber)", strokeWidth: 1.5, strokeDasharray: step === 0 ? "none" : "4 3" }} />
        <Txt x="301" y="48" size={9.5}>2ᵏ выходов</Txt>
        {[0, 1, 2, 3].map((i) => (
          <circle key={i} cx={282 + (i % 2) * 24} cy={74 + Math.floor(i / 2) * 22} r="6" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
        ))}
        <Arrow x1={222} y1={78} x2={262} y2={78} c="y" o={step === 1 ? 1 : 0} />
        <Txt x="180" y="152" mono size={11} o={step === 1 ? 1 : 0} color="var(--s-red)">файлов больше, чем выходов ⇒ коллизия</Txt>
      </G>
      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="30" mono size={12}>SHA-256: 2²⁵⁶ ≈ 1,2 · 10⁷⁷ значений</Txt>
        <rect x="40" y="48" width="280" height="14" rx="7" style={{ fill: "var(--s-panel2)", stroke: "var(--s-border)" }} />
        <rect x="40" y="48" width="3" height="14" rx="1.5" style={{ fill: "var(--s-red)" }} />
        <Txt x="180" y="86" size={9.5}>все когда-либо созданные файлы — крошечная точка слева</Txt>
        <Txt x="180" y="118" mono size={13} color="var(--s-accent)">поиск пары — практически нереален</Txt>
        <Txt x="180" y="144" size={9.5}>цифровые подписи · контроль целостности</Txt>
      </G>
      <G o={step >= 3 ? 1 : 0}>
        <Pill x={180} y={70} w={260} h={44} text="конечность — это структура" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={13} />
        <Txt x="180" y="116" size={10}>принцип Дирихле напомнит о себе</Txt>
      </G>
    </Steps>
  );
}
