// Слайды для «Современный Frontend», глава 7 — «Объекты, массивы и коллекции».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js07.jsx).

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
} from "../anim/Js07.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 7</span>
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
      title={"Данные и JSON"}
      sub={"Глава 7 · Общий язык веб-сервисов"}
      main={
        "Ответ сервера приходит как JSON и превращается в объекты и массивы."
      }
    >
      <V01 cues={[13.4, 26.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Объекты"}
      sub={"Литерал, ключи, entries"}
      main={"Объект — набор пар; keys, values и entries возвращают массивы."}
    >
      <V02 cues={[17.7, 27.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Копирование"}
      sub={"Ссылка, spread, structuredClone"}
      main={"Копия через ... поверхностная; глубокая — structuredClone."}
    >
      <V03 cues={[17.8, 32.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Деструктурирование"}
      sub={"Объекты, массивы, остаток"}
      main={"Одна строка разбирает значение на части."}
    >
      <V04 cues={[15.2, 27.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Массивы"}
      sub={"at, push, slice, splice"}
      main={
        "shift и unshift сдвигают остальное; splice меняет массив на месте."
      }
    >
      <V05 cues={[11.7, 32.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Методы с колбэком"}
      sub={"find, some, every, flat"}
      main={"Современный стиль — методы с колбэком, а не индексы."}
    >
      <V06 cues={[17.4, 27.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сортировка"}
      sub={"sort и toSorted"}
      main={"sort сравнивает как строки: числа сортируйте с функцией."}
    >
      <V07 cues={[18.6, 32.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Строки и массивы"}
      sub={"split, join, Array.from"}
      main={"Array.from превращает итерируемое в массив."}
    >
      <V08 cues={[8.6, 27.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Map"}
      sub={"Словарь с любыми ключами"}
      main={"Map надёжнее объекта для счётчиков, кэшей и индексов."}
    >
      <V09 cues={[17.0, 33.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Set"}
      sub={"Множество уникальных"}
      main={"Уникальный список: [...new Set(arr)]."}
    >
      <V10 cues={[16.4, 28.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"JSON"}
      sub={"stringify и parse"}
      main={"Функции и undefined при сериализации пропадают."}
    >
      <V11 cues={[14.7, 32.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Неизменяемые обновления"}
      sub={"Копия вместо изменения"}
      main={"Смена ссылки сообщает интерфейсу об изменении."}
    >
      <V12 cues={[13.9, 32.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — классы, прототипы и итераторы."}
    >
      <V13 cues={[11.9, 28.1]} />
    </Slide>
  );
}

export const SLIDES_J7 = {
  "11:7": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J7).
export const SLIDE_TITLES_J7 = {
  "11:7": [
    "Введение",
    "Объекты",
    "Копии",
    "Разбор",
    "Массивы",
    "Методы",
    "Сортировка",
    "split, from",
    "Map",
    "Set",
    "JSON",
    "Обновления",
    "Итоги",
  ],
};
