// Слайды для «Python как первый язык», глава 20 — «Контейнеры, вызываемые объекты и менеджеры контекста».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py20.jsx).

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
} from "../anim/Py20.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / МОДЕЛЬ ДАННЫХ / ГЛАВА 20</span>
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
      title={"Протоколы контейнеров"}
      sub={"len, [], in, for"}
      main={"Несколько методов делают класс полноправным контейнером."}
    >
      <V01 cues={[17.7, 25.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Последовательность"}
      sub={"__len__ и __getitem__"}
      main={
        "IndexError останавливает перебор; for, in и reversed заработают сами."
      }
    >
      <V02 cues={[13.6, 24.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Срезы"}
      sub={"Объект slice"}
      main={"Срез приходит в __getitem__ объектом slice."}
    >
      <V03 cues={[10.1, 25.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Запись и удаление"}
      sub={"__setitem__, __delitem__"}
      main={"IndexError — для последовательностей, KeyError — для отображений."}
    >
      <V04 cues={[10.1, 26.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Проверка вхождения"}
      sub={"__contains__"}
      main={"Напишите __contains__, если вхождение дешевле перебора."}
    >
      <V05 cues={[14.1, 20.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кортеж как ключ"}
      sub={"grid[x, y]"}
      main={"Ключ в скобках — любой объект, в том числе кортеж."}
    >
      <V06 cues={[13.6, 25.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Отображения"}
      sub={"Mapping и MutableMapping"}
      main={"Три метода — и остальное приходит бесплатно."}
    >
      <V07 cues={[16.0, 23.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Встроенные типы"}
      sub={"UserDict и __missing__"}
      main={"Для переопределений берите UserDict, а не dict."}
    >
      <V08 cues={[13.0, 32.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"__call__"}
      sub={"Объект как функция"}
      main={"Объект, в отличие от функции, помнит состояние."}
    >
      <V09 cues={[14.8, 24.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Оператор with"}
      sub={"__enter__ и __exit__"}
      main={"Вход и выход выполняются парой; истина из __exit__ гасит ошибку."}
    >
      <V10 cues={[4.9, 15.6, 24.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"@contextmanager"}
      sub={"Менеджер из генератора"}
      main={"До yield — вход, после — выход; try/finally для ошибок."}
    >
      <V11 cues={[11.0, 24.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Всё вместе"}
      sub={"Игровое поле"}
      main={"Каждая возможность — несколько строк привычного синтаксиса."}
    >
      <V12 cues={[13.7, 25.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Модель данных · часть третья"}
      main={"Протоколы контейнера, вызова и контекста."}
    >
      <V13 cues={[8.1, 14.4, 27.3]} />
    </Slide>
  );
}

export const SLIDES_P20 = {
  "13:20": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P20).
export const SLIDE_TITLES_P20 = {
  "13:20": [
    "Контейнеры",
    "Последовательность",
    "Срезы",
    "Запись и удаление",
    "in",
    "Кортеж-ключ",
    "Mapping",
    "UserDict",
    "call",
    "with",
    "contextmanager",
    "Игровое поле",
    "Итоги",
  ],
};
