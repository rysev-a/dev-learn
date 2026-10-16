// Слайды для «Python как первый язык», глава 30 — «Интроспекция и модуль inspect».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py30.jsx).

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
} from "../anim/Py30.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / МЕТАПРОГРАММИРОВАНИЕ / ГЛАВА 30</span>
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
      title={"Программа изучает себя"}
      sub={"Интроспекция и рефлексия"}
      main={"Объект можно спросить, что он такое и что умеет."}
    >
      <V01 cues={[18.4, 30.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Типы"}
      sub={"type, mro, subclasses"}
      main={"Базовый класс сам находит потомков."}
    >
      <V02 cues={[11.7, 23.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"dir и vars"}
      sub={"Что доступно и что хранится"}
      main={"dir — доступное, vars — хранящееся здесь."}
    >
      <V03 cues={[13.2, 23.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Доступ по имени"}
      sub={"getattr и друзья"}
      main={"Имя из внешнего мира проверяйте."}
    >
      <V04 cues={[15.5, 30.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Виды объектов"}
      sub={"Предикаты inspect"}
      main={"callable говорит «вызывается», inspect — «чем является»."}
    >
      <V05 cues={[17.9, 22.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"signature"}
      sub={"Подпись и bind"}
      main={"Подпись и привязка вызова — основа проверок и внедрения."}
    >
      <V06 cues={[13.4, 32.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Атрибуты функций"}
      sub={"Код и замыкания"}
      main={"__code__ и __closure__ показывают устройство функции."}
    >
      <V07 cues={[12.0, 28.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Исходники и кадры"}
      sub={"getsource, currentframe"}
      main={"Ссылки на кадры удаляйте после работы."}
    >
      <V08 cues={[12.1, 33.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Аннотации"}
      sub={"Читаем типы"}
      main={"Читайте аннотации стандартными функциями, а не словарём."}
    >
      <V09 cues={[9.6, 23.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Модули"}
      sub={"importlib"}
      main={"Плагины находят по именам и точкам входа."}
    >
      <V10 cues={[15.4, 24.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Применения"}
      sub={"Где это нужно"}
      main={"Вся информация уже лежит в объектах."}
    >
      <V11 cues={[12.0, 22.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Подводные камни"}
      sub={"Осторожно"}
      main={"Прямой вызов проще отлаживать."}
    >
      <V12 cues={[10.1, 27.0]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Интроспекция"}
      main={"type, dir, getattr, inspect, importlib."}
    >
      <V13 cues={[11.6, 19.1, 26.2]} />
    </Slide>
  );
}

export const SLIDES_P30 = {
  "13:30": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P30).
export const SLIDE_TITLES_P30 = {
  "13:30": [
    "Рефлексия",
    "Типы",
    "dir и vars",
    "getattr",
    "Предикаты",
    "signature",
    "Функции",
    "Кадры",
    "Аннотации",
    "Модули",
    "Применения",
    "Камни",
    "Итоги",
  ],
};
