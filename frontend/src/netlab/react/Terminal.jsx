import { useEffect, useRef, useState } from "react";

/* Мини-терминал устройства: история строк живёт выше (по устройству), здесь — ввод и вывод. */
export default function Terminal({ device, lines, onRun, disabled }) {
  const [value, setValue] = useState("");
  const [hist, setHist] = useState([]);
  const [h, setH] = useState(-1);
  const box = useRef(null);
  useEffect(() => {
    box.current?.scrollTo(0, box.current.scrollHeight);
  }, [lines]);

  const submit = (e) => {
    e.preventDefault();
    const line = value.trim();
    if (!line) return;
    setHist((x) => [line, ...x]);
    setH(-1);
    setValue("");
    onRun(line);
  };
  const key = (e) => {
    if (e.key === "ArrowUp" && hist.length) {
      e.preventDefault();
      const n = Math.min(h + 1, hist.length - 1);
      setH(n);
      setValue(hist[n]);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      const n = h - 1;
      setH(n);
      setValue(n >= 0 ? hist[n] : "");
    }
  };
  const prompt = `${device.name.replace(/\s+/g, "-")}# `;

  return (
    <div className="nl-term">
      <div className="nl-term-out" ref={box}>
        {lines.length === 0 && (
          <div className="nl-term-hint">Введите «help», чтобы увидеть команды.</div>
        )}
        {lines.map((l, i) => (
          <div key={i} className={l.cmd ? "cmd" : "res"}>
            {l.cmd ? prompt + l.text : l.text}
          </div>
        ))}
      </div>
      <form onSubmit={submit} className="nl-term-in">
        <span>{prompt}</span>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={key}
          spellCheck={false}
          autoCapitalize="off"
          autoComplete="off"
          disabled={disabled}
          aria-label="Командная строка"
        />
      </form>
    </div>
  );
}
