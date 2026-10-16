/* График окна перегрузки (cwnd) по времени передачи: «пила», уровни BDP и окна приёма. */
export default function Chart({ chart }) {
  const { trace, bdpKb, rwndKb, qcapKb, cc } = chart;
  const W = 640;
  const H = 150;
  const L = 60;
  const B = 22;
  const T = 10;
  const maxT = Math.max(...trace.map((p: { t: any; }) => p.t), 1);
  const maxY = Math.max(...trace.map((p: { cwnd: any; }) => p.cwnd), bdpKb * 1.15, Math.min(rwndKb, bdpKb * 3), 10);
  const x = (t: number) => L + (t / maxT) * (W - L - 8);
  const y = (v: number) => H - B - (Math.min(v, maxY) / maxY) * (H - B - T);
  const pts = trace.map((p: { t: number; cwnd: number; }) => `${x(p.t).toFixed(1)},${y(p.cwnd).toFixed(1)}`).join(" ");
  return (
    <figure className="nl-chart">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="График окна перегрузки">
        <line x1={L} y1={T} x2={L} y2={H - B} className="ax" />
        <line x1={L} y1={H - B} x2={W - 8} y2={H - B} className="ax" />
        <line x1={L} x2={W - 8} y1={y(bdpKb)} y2={y(bdpKb)} className="bdp" />
        <text x={W - 10} y={y(bdpKb) - 3} className="lbl" textAnchor="end">
          ёмкость канала (BDP) {bdpKb.toFixed(0)} КБ
        </text>
        {rwndKb < maxY && (
          <>
            <line x1={L} x2={W - 8} y1={y(rwndKb)} y2={y(rwndKb)} className="rw" />
            <text x={W - 10} y={y(rwndKb) + 11} className="lbl rw" textAnchor="end">
              окно приёма {rwndKb.toFixed(0)} КБ
            </text>
          </>
        )}
        <polyline points={pts} className="cw" />
        <text x={L - 4} y={T + 8} className="lbl" textAnchor="end">
          {maxY.toFixed(0)} КБ
        </text>
        <text x={L - 4} y={H - B} className="lbl" textAnchor="end">
          0
        </text>
        <text x={W - 8} y={H - 6} className="lbl" textAnchor="end">
          {maxT.toFixed(0)} мс
        </text>
        <text x={L + 4} y={H - 6} className="lbl">
          cwnd, алгоритм {cc}
        </text>
      </svg>
      {qcapKb > 0 && <figcaption>очередь на узком месте до {qcapKb.toFixed(0)} КБ</figcaption>}
    </figure>
  );
}
