import { Arrow, G, Pill, Steps, Txt, useSteps } from "./kit.jsx";

/* Глава 3, слайд 7: размещения A(n, k) — выбор k из n, когда порядок важен.
   Подиум 20·19·18, формула n!/(n−k)!, пин-код без повторов, проверка
   «поменяли местами — другая комбинация?». */

const LABELS = ["Порядок", "Подиум", "Формула", "Пин-код", "Проверка"];
const CAPTION = [
  "Теперь выбираем не всё, а часть, — и смотрим, важен ли порядок",
  "Золото, серебро, бронза из двадцати: три разные награды, 20 · 19 · 18 = 6 840 способов",
  "Формула словами: n! делим на (n − k)! — отрезаем хвост тех, кто остался без места",
  "Пин-код без повторяющихся цифр: 10 · 9 · 8 · 7 = 10!/6! = 5 040 вариантов",
  "Если поменять двоих выбранных местами и получится другая комбинация — считаем размещение",
];

export default function C3Arrange({ cues }) {
  const ctl = useSteps(cues || [4.0, 13.8, 22.6, 30.4], 3000);
  const { step } = ctl;
  const medal = [
    ["🥇", "золото", "20"],
    ["🥈", "серебро", "19"],
    ["🥉", "бронза", "18"],
  ];
  return (
    <Steps ctl={ctl} labels={LABELS} caption={CAPTION}>
      <G o={step === 0 ? 1 : 0}>
        <Pill x={110} y={70} w={150} h={46} text="порядок важен?" stroke="var(--s-accent)" fill="var(--s-green)" color="var(--s-accent)" size={12} />
        <Arrow x1={190} y1={62} x2={242} y2={38} c="y" />
        <Arrow x1={190} y1={78} x2={242} y2={102} c="g" />
        <Pill x={296} y={38} w={90} text="да: размещение" stroke="var(--s-amber)" size={9.5} />
        <Pill x={296} y={102} w={90} text="нет: сочетание" stroke="var(--s-accent)" size={9.5} />
      </G>

      <G o={step === 1 ? 1 : 0}>
        {medal.map(([m, t, n], i) => (
          <g key={t}>
            <rect x={60 + i * 88} y={90 - (i === 0 ? 38 : i === 1 ? 24 : 12)} width="76" height={44 + (i === 0 ? 38 : i === 1 ? 24 : 12)} rx="8" style={{ fill: "var(--s-panel2)", stroke: "var(--s-amber)", strokeWidth: 1.5 }} />
            <text x={98 + i * 88} y={70 - (i === 0 ? 38 : i === 1 ? 24 : 12)} textAnchor="middle" style={{ fontSize: 22 }}>{m}</text>
            <text x={98 + i * 88} y={120} textAnchor="middle" className="a-mono" style={{ fontSize: 15, fill: "var(--s-accent)" }}>{n}</text>
            <text x={98 + i * 88} y={134} textAnchor="middle" className="a-cap">{t}</text>
          </g>
        ))}
        <Txt x="180" y="154" mono size={13} color="var(--s-accent)">20 · 19 · 18 = 6 840</Txt>
      </G>

      <G o={step === 2 ? 1 : 0}>
        <Txt x="180" y="26" mono size={13}>n! / (n − k)!   при n = 20, k = 3</Txt>
        {Array.from({ length: 20 }, (_, i) => 20 - i).map((v, i) => (
          <g key={v}>
            <rect className="a-t" x={14 + i * 16.4} y="44" width="14" height="22" rx="3" style={{ fill: i < 3 ? "var(--s-accent)" : "var(--s-muted)", fillOpacity: i < 3 ? 0.5 : 0.18, stroke: i < 3 ? "var(--s-accent)" : "var(--s-border)" }} />
            <text x={21 + i * 16.4} y="59" textAnchor="middle" className="a-mono" style={{ fontSize: 7, fill: "var(--s-text)" }}>{v}</text>
          </g>
        ))}
        <line x1="62" y1="72" x2="62" y2="40" style={{ stroke: "var(--s-red)", strokeDasharray: "3 3" }} />
        <Txt x="36" y="86" color="var(--s-accent)">нужны</Txt>
        <Txt x="200" y="86" color="var(--s-muted)">хвост (17!) сокращается</Txt>
        <Txt x="180" y="130" mono size={15} color="var(--s-accent)">20!/17! = 20 · 19 · 18</Txt>
      </G>

      <G o={step === 3 ? 1 : 0}>
        {[10, 9, 8, 7].map((v, i) => (
          <g key={v}>
            <rect className="a-t" x={74 + i * 56} y="40" width="46" height="54" rx="9" style={{ fill: "var(--s-green)", stroke: "var(--s-accent)", strokeWidth: 1.6, opacity: step === 3 ? 1 : 0, transitionDelay: `${i * 220}ms` }} />
            <text x={97 + i * 56} y="73" textAnchor="middle" className="a-mono" style={{ fontSize: 20, fill: "var(--s-accent)" }}>{v}</text>
          </g>
        ))}
        <Txt x="180" y="30" size={10}>цифры не повторяются: выбор сужается</Txt>
        <Txt x="180" y="130" mono size={16} color="var(--s-accent)">10!/6! = 5 040</Txt>
      </G>

      <G o={step === 4 ? 1 : 0}>
        <Pill x={90} y={50} w={100} text="(Аня, Борис)" stroke="var(--s-blue)" />
        <Pill x={90} y={96} w={100} text="(Борис, Аня)" stroke="var(--s-amber)" />
        <Txt x="180" y="78" mono size={20} color="var(--s-red)">≠</Txt>
        <Txt x="270" y="76">другая комбинация</Txt>
        <Txt x="270" y="94" color="var(--s-accent)">значит — размещение</Txt>
      </G>
    </Steps>
  );
}
