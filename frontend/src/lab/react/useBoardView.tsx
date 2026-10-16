import { useCallback, useEffect, useRef, useState, type RefObject } from "react";
import {
  ZOOM,
  dragPan,
  listenMiddleButton,
  startPan,
  wheelFactor,
  zoomAround,
  type PanDrag,
} from "../exercises/logic-gates/board-pan.ts";
import type { Point } from "../exercises/logic-gates/circuit.model.ts";

/* Окно на бесконечную доску, общее для досок вентилей и блоков: сдвиг (пустое место, колесо мыши),
   масштаб (Ctrl/⌘ + колесо, кнопки) и панель кнопок масштаба. */

/** Где доска на экране: прямоугольник svg, пикселей на единицу мира при масштабе 1 и поля вокруг доски */
export interface BoardMetrics {
  rect: DOMRect;
  base: number;
  offX: number;
  offY: number;
}

/** Метрики для доски W×H, вписанной в svg с сохранением пропорций */
export function boardMetrics(svg: SVGSVGElement, w: number, h: number): BoardMetrics {
  const rect = svg.getBoundingClientRect();
  const base = Math.min(rect.width / w, rect.height / h);
  return { rect, base, offX: (rect.width - w * base) / 2, offY: (rect.height - h * base) / 2 };
}

const HOME: Point = { x: 0, y: 0 };

export function useBoardView(
  svgRef: RefObject<SVGSVGElement | null>,
  getMetrics: () => BoardMetrics,
  /** колесо без Ctrl тоже масштабирует (доска на весь экран) */
  wheelAlways: (svg: SVGSVGElement) => boolean = () => false,
) {
  const [pan, setPan] = useState<Point>(HOME);
  const [zoom, setZoom] = useState(1);
  const [panning, setPanning] = useState(false);
  const live = useRef({ pan, zoom });
  live.current = { pan, zoom };
  const metrics = useRef(getMetrics);
  metrics.current = getMetrics;
  const wheelRule = useRef(wheelAlways);
  wheelRule.current = wheelAlways;
  const drag = useRef<PanDrag | null>(null);

  const beginPan = useCallback((e: { clientX: number; clientY: number }) => {
    const m = metrics.current();
    const s = live.current;
    drag.current = startPan(e as PointerEvent, m.base * s.zoom, s.pan);
    setPanning(true);
  }, []);
  /** Двигает доску за рукой, пока идёт сдвиг; возвращает true, если событие обработано */
  const movePan = useCallback((e: PointerEvent): boolean => {
    if (!drag.current) return false;
    setPan(dragPan(drag.current, e));
    return true;
  }, []);
  const endPan = useCallback((): boolean => {
    if (!drag.current) return false;
    drag.current = null;
    setPanning(false);
    return true;
  }, []);

  const zoomBy = useCallback((factor: number) => {
    const m = metrics.current();
    const next = zoomAround(live.current, factor, { x: (m.rect.width - 2 * m.offX) / 2, y: (m.rect.height - 2 * m.offY) / 2 }, m.base);
    setPan(next.pan);
    setZoom(next.zoom);
  }, []);
  const reset = useCallback(() => {
    setPan(HOME);
    setZoom(1);
  }, []);

  // колесо: Ctrl/⌘ — масштаб вокруг курсора; средняя кнопка — сдвиг
  useEffect(() => {
    const el = svgRef.current;
    if (!el) return;
    const wheel = (e: WheelEvent) => {
      if (!(e.ctrlKey || e.metaKey) && !wheelRule.current(el)) return;
      e.preventDefault();
      const m = metrics.current();
      const next = zoomAround(live.current, wheelFactor(e), { x: e.clientX - m.rect.left - m.offX, y: e.clientY - m.rect.top - m.offY }, m.base);
      setPan(next.pan);
      setZoom(next.zoom);
    };
    el.addEventListener("wheel", wheel, { passive: false });
    const unlisten = listenMiddleButton(el, beginPan);
    return () => {
      el.removeEventListener("wheel", wheel);
      unlisten();
    };
  }, [svgRef, beginPan]);

  return { pan, zoom, panning, setPan, setZoom, beginPan, movePan, endPan, zoomBy, reset, changed: pan.x !== 0 || pan.y !== 0 || zoom !== 1 };
}

/** Кнопки масштаба над доской: −, процент (100 %), +, «вернуть на место» */
export function ZoomControls({
  zoom,
  changed,
  onZoomBy,
  onActual,
  onReset,
}: {
  zoom: number;
  /** доска сдвинута или масштаб не 100 % (показать кнопку «вернуть») */
  changed: boolean;
  onZoomBy: (factor: number) => void;
  onActual: () => void;
  onReset: () => void;
}) {
  return (
    <div className="lab-zoom" role="group" aria-label="Масштаб доски">
      <button type="button" title="Уменьшить (Ctrl + колесо)" onClick={() => onZoomBy(1 / ZOOM.step)}>
        −
      </button>
      <button type="button" className="pct" title="Масштаб 100 %" onClick={onActual}>
        {Math.round(zoom * 100)}%
      </button>
      <button type="button" title="Увеличить (Ctrl + колесо)" onClick={() => onZoomBy(ZOOM.step)}>
        +
      </button>
      {changed && (
        <button type="button" title="Вернуть доску на место и масштаб 100 %" onClick={onReset}>
          ⌖
        </button>
      )}
    </div>
  );
}
