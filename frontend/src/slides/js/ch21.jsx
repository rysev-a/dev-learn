// Слайды для «Современный Frontend», глава 21 — «Node.js изнутри: V8, libuv, цикл событий и модули».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js21.jsx).

import {
  V01,
  V02,
  V03,
  V04,
  V05,
  V06,
  V07,
  V08,
  V09,
  V10,
  V11,
  V12,
  V13,
} from "../anim/Js21.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В NODE.JS / ГЛАВА 21</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"JavaScript вне браузера"}
      sub={"Глава 21 · Node.js"}
      main={"Нужно понимать, как устроен Node."}
    >
      <V01 cues={[13.1, 33.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Слои Node"}
      sub={"V8, libuv, привязки"}
      main={"Один главный поток для вашего кода."}
    >
      <V02 cues={[13.7, 21.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"V8"}
      sub={"JIT, формы, GC"}
      main={"Стабильные формы быстрее."}
    >
      <V03 cues={[12.5, 32.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Фазы цикла"}
      sub={"timers → poll → check"}
      main={"Цикл завершается, когда дел нет."}
    >
      <V04 cues={[8.8, 27.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"nextTick и микрозадачи"}
      sub={"Порядок очередей"}
      main={"Рекурсия nextTick морит цикл."}
    >
      <V05 cues={[13.8, 28.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Пул потоков"}
      sub={"libuv thread pool"}
      main={"Не блокируйте главный поток."}
    >
      <V06 cues={[17.1, 22.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"CommonJS"}
      sub={"require, кеш, циклы"}
      main={"Кеш и циклы — по экспортам на момент."}
    >
      <V07 cues={[14.1, 25.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"ES-модули"}
      sub={"type, exports, imports"}
      main={"Всё, чего нет в exports, закрыто."}
    >
      <V08 cues={[9.0, 23.0]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Параллелизм"}
      sub={"worker, child, cluster"}
      main={"Выберите инструмент под задачу."}
    >
      <V09 cues={[16.5, 24.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Процесс"}
      sub={"Аргументы и коды выхода"}
      main={"128 + номер сигнала."}
    >
      <V10 cues={[7.0, 26.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Корректное завершение"}
      sub={"SIGTERM и надзиратель"}
      main={"Закрываем в обратном порядке."}
    >
      <V11 cues={[3.5, 23.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Диагностика"}
      sub={"Инспектор, ALS, lag"}
      main={"Метрики полезнее отладчика."}
    >
      <V12 cues={[10.4, 26.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — файлы и потоки."}
    >
      <V13 cues={[13.9, 24.8]} />
    </Slide>
  );
}

export const SLIDES_J21 = {
  "11:21": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J21).
export const SLIDE_TITLES_J21 = {
  "11:21": [
    "Введение",
    "Слои",
    "V8",
    "Цикл",
    "Очереди",
    "Пул",
    "CJS",
    "ESM",
    "Параллелизм",
    "Процесс",
    "Завершение",
    "Диагностика",
    "Итоги",
  ],
};
