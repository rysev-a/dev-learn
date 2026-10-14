import { usePlayer } from "../lib/player.jsx";
import { fmtTime } from "../lib/time.js";

export default function AudioPlayer() {
  const { current, paused, progress, togglePause, playPrev, playNextManual, seek } =
    usePlayer();
  if (!current) return null;
  const p = progress && progress.id === current.id ? progress : null;
  const pct = p && p.d > 0 ? (p.t / p.d) * 100 : 0;

  return (
    <div className="np-card">
      <div className="np-main">
        <div className="np-cover">{current.badge}</div>
        <div className="np-info">
          <p className="np-title" title={current.title}>
            {current.title}
          </p>
          <p className="np-subtitle" title={current.subtitle}>
            {current.subtitle}
          </p>
        </div>
        <div className="np-controls">
          <button className="np-btn" onClick={playPrev} title="Назад">
            ⏮
          </button>
          <button
            className="np-btn np-play"
            onClick={togglePause}
            title={paused ? "Плей" : "Пауза"}
          >
            {paused ? "▶" : "▮▮"}
          </button>
          <button className="np-btn" onClick={playNextManual} title="Вперёд">
            ⏭
          </button>
        </div>
      </div>
      <div className="np-slider-row">
        <span className="np-time">{p ? fmtTime(p.t) : "0:00"}</span>
        <div
          className="np-slider"
          onClick={(e) => {
            const r = e.currentTarget.getBoundingClientRect();
            seek((e.clientX - r.left) / r.width);
          }}
        >
          <div className="np-slider-fill" style={{ width: `${pct}%` }} />
          <div className="np-slider-knob" style={{ left: `${pct}%` }} />
        </div>
        <span className="np-time">{p && p.d > 0 ? fmtTime(p.d) : "—:—"}</span>
      </div>
    </div>
  );
}
