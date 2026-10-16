// Глобальный аудиоплеер: одно приложение — одно играющее аудио.
// Живёт в контексте, чтобы любая страница могла управлять воспроизведением.
import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { VirtualClock, estimateSeconds } from "./voice.ts";

// Элемент очереди: часть главы со своим файлом озвучки (url) или без него (озвучка по часам)
export interface PlayerItem {
  id: string;
  url: string | null;
  text: string;
  est?: number;
  title: string;
  subtitle: string;
  badge: string;
}

export interface PlayerProgress {
  id: string;
  t: number;
  d: number;
}

type Clock = HTMLAudioElement | VirtualClock;

interface PlayerValue {
  playingId: string | null;
  paused: boolean;
  progress: PlayerProgress | null;
  current: PlayerItem | null;
  stop: () => void;
  playSequence: (items: PlayerItem[]) => void;
  playPrev: () => void;
  playNextManual: () => void;
  togglePause: () => void;
  seek: (frac: number) => void;
}

const PlayerContext = createContext<PlayerValue | null>(null);

export function usePlayer(): PlayerValue {
  const ctx = useContext(PlayerContext);
  if (!ctx) throw new Error("usePlayer must be used within PlayerProvider");
  return ctx;
}

export function PlayerProvider({ children }: { children: ReactNode }) {
  const audioRef = useRef<Clock | null>(null);
  const queueRef = useRef<PlayerItem[]>([]);
  const stackRef = useRef<PlayerItem[]>([]);
  const currentItemRef = useRef<PlayerItem | null>(null);
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState<PlayerProgress | null>(null);
  const [current, setCurrent] = useState<PlayerItem | null>(null); // карточка «сейчас играет»

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

  function startItem(item: PlayerItem) {
    currentItemRef.current = item;
    setCurrent(item);
    // без файла озвучки абзац «читается» по виртуальным часам (см. lib/voice.js)
    const audio: Clock = item.url
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
    audio.onended = playNext;
    audio.onerror = playNext;
    audio.play().catch(() => {});
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

  function playSequence(items: PlayerItem[]) {
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
    if (prevItem) startItem(prevItem);
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
      a.play().catch(() => {});
      setPaused(false);
    } else {
      a.pause();
      setPaused(true);
    }
  }

  function seek(frac: number) {
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
