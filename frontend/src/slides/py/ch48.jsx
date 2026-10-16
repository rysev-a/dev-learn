// Слайды для «Python как первый язык», глава 48 — «Байт-код, интерпретатор, GIL и потоки без GIL».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py48.jsx).

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
} from "../anim/Py48.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / ПИТОН ИЗНУТРИ / ГЛАВА 48</span>
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
      title={"Как выполняется программа"}
      sub={"Вопросы главы"}
      main={"Устойчивые идеи вместо мелких деталей."}
    >
      <V01 cues={[14.3, 28.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"__pycache__"}
      sub={"Кэш байт-кода"}
      main={"Компиляция — один раз на модуль."}
    >
      <V02 cues={[16.6, 25.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Кадры и цикл вычисления"}
      sub={"Как работает интерпретатор"}
      main={"Кадр = команда + стек + локальные."}
    >
      <V03 cues={[13.4, 21.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Специализация"}
      sub={"Адаптивный интерпретатор 3.11"}
      main={"Устойчивые типы — быстрый код."}
    >
      <V04 cues={[19.1, 27.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Исключения и локальные имена"}
      sub={"Практика скорости"}
      main={"Сначала измерьте, потом оптимизируйте."}
    >
      <V05 cues={[12.4, 22.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"JIT"}
      sub={"Экспериментальный, 3.13"}
      main={"Задел на будущее, не обязательный."}
    >
      <V06 cues={[13.9, 20.2]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"GIL"}
      sub={"Один поток за раз"}
      main={"Хорош для I/O, не ускоряет счёт."}
    >
      <V07 cues={[10.4, 30.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"GIL и гонки"}
      sub={"x += 1 не атомарно"}
      main={"Общие данные защищайте замком."}
    >
      <V08 cues={[13.7, 26.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Как обойти GIL"}
      sub={"Процессы, C, субинтерпретаторы"}
      main={"Каждый способ имеет цену."}
    >
      <V09 cues={[16.2, 28.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Сборка без GIL"}
      sub={"PEP 703"}
      main={"Отдельный интерпретатор и признак сборки."}
    >
      <V10 cues={[15.8, 21.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Как это устроено"}
      sub={"Счётчики и замки"}
      main={"Цена — немного медленнее в одном потоке."}
    >
      <V11 cues={[11.3, 30.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Практические выводы"}
      sub={"Что делать"}
      main={"Синхронизация нужна всегда."}
    >
      <V12 cues={[13.3, 22.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Питон изнутри"}
      main={"Байт-код, кэш, специализация, GIL."}
    >
      <V13 cues={[8.0, 16.5, 27.3]} />
    </Slide>
  );
}

export const SLIDES_P48 = {
  "13:48": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P48).
export const SLIDE_TITLES_P48 = {
  "13:48": [
    "Вопросы",
    "pyc",
    "Кадры",
    "Специализация",
    "Скорость",
    "JIT",
    "GIL",
    "Гонки",
    "Обходы",
    "Без GIL",
    "Устройство",
    "Выводы",
    "Итоги",
  ],
};
