// Глобальный аудиоплеер: одно приложение — одно играющее аудио.
// Живёт в контексте, чтобы любая страница могла управлять воспроизведением.
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { VirtualClock, estimateSeconds } from "./voice.js";

const PlayerContext = createContext(null);

export function usePlayer() {
  const ctx = useContext(PlayerContext);
  if (!ctx) throw new Error("usePlayer must be used within PlayerProvider");
  return ctx;
}

export function PlayerProvider({ children }) {
  const audioRef = useRef(null);
  const queueRef = useRef([]);
  const stackRef = useRef([]);
  const currentItemRef = useRef(null);
  const [playingId, setPlayingId] = useState(null);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState(null); // {id, t, d}
  const [current, setCurrent] = useState(null); // карточка «сейчас играет»

  useEffect(() => {
    return () => audioRef.current?.pause();
  }, []);

  function stop() {
    queueRef.current = [];
    stackRef.current = [];
    currentItemRef.current = null;
    audioRef.current?.pause();
    setPlayingId(null);
    setPaused(false);
    setProgress(null);
    setCurrent(null);
  }

  function startItem(item) {
    currentItemRef.current = item;
    setCurrent(item);
    // без файла озвучки абзац «читается» по виртуальным часам (см. lib/voice.js)
    const audio = item.url
      ? new Audio(item.url)
      : new VirtualClock(item.est || estimateSeconds(item.text));
    audioRef.current = audio;
    setPlayingId(item.id);
    setPaused(false);
    audio.ontimeupdate = () =>
      setProgress({
        id: item.id,
        t: audio.currentTime,
        d: audio.duration || 0,
      });
    audio.onended = audio.onerror = playNext;
    const started = audio.play();
    if (started?.catch) started.catch(() => {});
  }

  function playNext() {
    const prev = currentItemRef.current;
    if (prev) stackRef.current.push(prev);
    const next = queueRef.current.shift();
    if (!next) {
      stop();
      return;
    }
    startItem(next);
  }

  function playSequence(items) {
    audioRef.current?.pause();
    stackRef.current = [];
    queueRef.current = [...items];
    currentItemRef.current = null;
    playNext();
  }

  function playPrev() {
    const a = audioRef.current;
    if (!a || !currentItemRef.current) return;
    if (stackRef.current.length === 0) {
      a.currentTime = 0;
      return;
    }
    queueRef.current.unshift(currentItemRef.current);
    const prevItem = stackRef.current.pop();
    a.pause();
    startItem(prevItem);
  }

  function playNextManual() {
    const a = audioRef.current;
    if (!a || !currentItemRef.current) return;
    if (queueRef.current.length === 0) {
      a.currentTime = 0;
      return;
    }
    a.pause();
    playNext();
  }

  function togglePause() {
    const a = audioRef.current;
    if (!a) return;
    if (a.paused) {
      a.play();
      setPaused(false);
    } else {
      a.pause();
      setPaused(true);
    }
  }

  function seek(frac) {
    const a = audioRef.current;
    if (a && isFinite(a.duration) && a.duration > 0) {
      a.currentTime = frac * a.duration;
    }
  }

  return (
    <PlayerContext.Provider
      value={{
        playingId,
        paused,
        progress,
        current,
        stop,
        playSequence,
        playPrev,
        playNextManual,
        togglePause,
        seek,
      }}
    >
      {children}
    </PlayerContext.Provider>
  );
}
