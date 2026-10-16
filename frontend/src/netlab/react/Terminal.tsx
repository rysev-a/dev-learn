import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import type { Device } from "../types.ts";

/** строка терминала: введённая команда или вывод */
export interface TermLine {
  cmd?: boolean;
  text: string;
}

/* Мини-терминал устройства: история строк живёт выше (по устройству), здесь — ввод и вывод. */
export default function Terminal({
  device,
  lines,
  onRun,
  disabled,
}: {
  device: Device;
  lines: TermLine[];
  onRun: (line: string) => void;
  disabled?: boolean;
}) {
  const [value, setValue] = useState("");
  const [hist, setHist] = useState<string[]>([]);
  const [h, setH] = useState(-1);
  const box = useRef<HTMLDivElement>(null);
  useEffect(() => {
    box.current?.scrollTo(0, box.current.scrollHeight);
  }, [lines]);

  const submit = (e: FormEvent) => {
    e.preventDefault();
    const line = value.trim();
    if (!line) return;
    setHist((x) => [line, ...x]);
    setH(-1);
    setValue("");
    onRun(line);
  };
  const key = (e: KeyboardEvent) => {
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
