// Слайды для «Современный Frontend», глава 6 — «Функции, область видимости и замыкания».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js06.jsx).

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
} from "../anim/Js06.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 6</span>
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
      title={"Функции — значения"}
      sub={"Глава 6 · Первого класса"}
      main={
        "Функцию можно хранить, передавать и возвращать — как любое значение."
      }
    >
      <V01 cues={[17.4, 29.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Объявление и выражение"}
      sub={"Поднятие и return"}
      main={
        "Объявление поднимается, выражение — нет; return не переносят на следующую строку."
      }
    >
      <V02 cues={[15.2, 28.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Стрелочные функции"}
      sub={"=> и this"}
      main={
        "Стрелка коротка и берёт this из окружения; методы пишут обычными функциями."
      }
    >
      <V03 cues={[17.4, 28.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Параметры"}
      sub={"Умолчания, rest, ссылки"}
      main={"Число аргументов не проверяется; объекты передаются ссылкой."}
    >
      <V04 cues={[20.8, 29.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Деструктурирование"}
      sub={"Объект настроек и spread"}
      main={"Один объект настроек вместо длинного списка параметров."}
    >
      <V05 cues={[10.7, 24.7]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Область видимости"}
      sub={"Блок и мёртвая зона"}
      main={"let и const — блочные; до объявления они недоступны."}
    >
      <V06 cues={[15.5, 28.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Лексическое окружение"}
      sub={"Цепочка окружений"}
      main={"Имена ищутся там, где функция написана, а не где вызвана."}
    >
      <V07 cues={[15.1, 27.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Замыкание"}
      sub={"Приватное состояние"}
      main={"Замыкание — функция вместе с окружением, в котором она создана."}
    >
      <V08 cues={[13.9, 33.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Замыкания в цикле"}
      sub={"var и let"}
      main={"В циклах объявляйте переменные через let."}
    >
      <V09 cues={[18.3, 25.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Функции высшего порядка"}
      sub={"map, filter, reduce"}
      main={"Цепочки map, filter и reduce описывают данные, а не цикл."}
    >
      <V10 cues={[19.4, 32.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"this"}
      sub={"call, apply, bind"}
      main={"this зависит от вызова; стрелка и явные аргументы надёжнее."}
    >
      <V11 cues={[11.1, 24.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Рекурсия и мемоизация"}
      sub={"Стек и кеш"}
      main={"Глубина стека конечна; мемоизация хранит результаты в замыкании."}
    >
      <V12 cues={[13.6, 28.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — объекты, массивы, Map и Set."}
    >
      <V13 cues={[12.6, 30.1]} />
    </Slide>
  );
}

export const SLIDES_J6 = {
  "11:6": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J6).
export const SLIDE_TITLES_J6 = {
  "11:6": [
    "Введение",
    "Объявление",
    "Стрелки",
    "Параметры",
    "Деструктурирование",
    "Видимость",
    "Окружение",
    "Замыкание",
    "В цикле",
    "map, filter",
    "this",
    "Рекурсия",
    "Итоги",
  ],
};
