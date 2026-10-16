/* Поле сети: устройства, кабели и бегущие по ним пакеты. Рисуется в SVG 640×360. */

const ICONS = {
  host: (
    <>
      <rect x="2" y="3" width="20" height="14" rx="2" />
      <path d="M8 21h8M12 17v4" />
    </>
  ),
  server: (
    <>
      <rect x="2" y="2" width="20" height="8" rx="2" />
      <rect x="2" y="14" width="20" height="8" rx="2" />
      <path d="M6 6h.01M6 18h.01" />
    </>
  ),
  router: (
    <>
      <rect x="2" y="14" width="20" height="8" rx="2" />
      <path d="M6 18h.01M10 18h.01M15 10v4M17.8 7.2a4 4 0 0 0-5.6 0M20.7 4.3a8 8 0 0 0-11.4 0" />
    </>
  ),
  hub: (
    <>
      <rect x="2" y="9" width="20" height="6" rx="2" />
      <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01M12 3v6M12 15v6" />
    </>
  ),
  switch: (
    <>
      <rect x="2" y="7" width="20" height="10" rx="2" />
      <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01" />
    </>
  ),
  internet: <path d="M17.5 19H9a7 7 0 1 1 6.7-9h1.8a4.5 4.5 0 1 1 0 9Z" />,
};
const W = 104;
const H = 58;

function pos(state, dev) {
  const d = state.devices[dev];
  return { x: d.x, y: d.y };
}

export default function Board({
  state,
  selected,
  cableFrom,
  selectedLink,
  dots,
  marks,
  onDevice,
  onLink,
}) {
  return (
    <svg className="nl-board" viewBox="-24 0 704 360" role="img" aria-label="Схема сети">
      {state.links.map((l, i) => {
        const [da, pa] = l.a.split(":");
        const [db, pb] = l.b.split(":");
        const a = pos(state, da);
        const b = pos(state, db);
        const len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
        const t = Math.min(0.42, 74 / len);
        const la = { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
        const lb = { x: b.x + (a.x - b.x) * t, y: b.y + (a.y - b.y) * t };
        const down =
          state.devices[da].ifaces.find((x) => x.name === pa)?.up === false ||
          state.devices[db].ifaces.find((x) => x.name === pb)?.up === false;
        return (
          <g key={`${l.a}-${l.b}`} className={`nl-link ${selectedLink === i ? "on" : ""} ${down ? "down" : ""}`}>
            <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} />
            <line className="hit" x1={a.x} y1={a.y} x2={b.x} y2={b.y} onClick={() => onLink?.(i)} />
            <text x={la.x} y={la.y - 4} className="nl-port">
              {pa}
            </text>
            <text x={lb.x} y={lb.y - 4} className="nl-port">
              {pb}
            </text>
            {l.km >= 1 && (
              <text x={(a.x + b.x) / 2} y={(a.y + b.y) / 2 + 12} className="nl-km">
                {l.km} км
              </text>
            )}
          </g>
        );
      })}

      {Object.values(state.devices).map((d) => {
        const ips = d.ifaces.filter((i) => i.ip).map((i) => `${i.ip}/${i.prefix}`);
        const cls = ["nl-dev", d.kind, selected === d.id ? "on" : "", cableFrom === d.id ? "from" : "", d.locked ? "locked" : ""].join(" ");
        return (
          <g key={d.id} className={cls} onClick={() => onDevice(d.id)} transform={`translate(${d.x},${d.y})`}>
            <rect x={-W / 2} y={-H / 2} width={W} height={H} rx="9" />
            <g className="nl-ico" transform="translate(-16,-26) scale(1.35)">
              {ICONS[d.kind] ?? ICONS.host}
            </g>
            <text y={H / 2 - 7} className="nl-name">
              {d.name}
            </text>
            {ips.slice(0, 3).map((ip, i) => (
              <text key={ip} y={H / 2 + 14 + i * 12} className="nl-ip">
                {ip}
              </text>
            ))}
          </g>
        );
      })}

      {dots.map((h, i) => {
        const a = pos(state, h.from);
        const b = pos(state, h.to);
        const x = a.x + (b.x - a.x) * h.p;
        const y = a.y + (b.y - a.y) * h.p;
        return (
          <g key={i} className={`nl-dot ${h.kind}`} transform={`translate(${x},${y})`}>
            <circle r="6" />
          </g>
        );
      })}

      {marks.map((m, i) => {
        const d = state.devices[m.dev];
        return (
          <g key={i} className={`nl-mark ${m.kind}`} transform={`translate(${d.x},${d.y - H / 2 - 8 - (m.row ?? 0) * 12})`}>
            <text>{m.kind === "drop" || m.kind === "fw" ? "✕ " : m.kind === "nat" ? "⇄ " : ""}{m.text}</text>
          </g>
        );
      })}
    </svg>
  );
}
