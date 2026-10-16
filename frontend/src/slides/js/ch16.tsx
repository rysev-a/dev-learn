// Слайды для «Современный Frontend», глава 16 — «События: всплытие, перехват и делегирование».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js16.jsx).

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
} from "../anim/Js16.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 16", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Реакции страницы"}
      sub={"Глава 16 · Модель наблюдателя"}
      main={"Событие идёт по цепочке предков."}
    >
      <V01 cues={[13.5, 35.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Подписка"}
      sub={"addEventListener и параметры"}
      main={"Анонимную стрелку не снять — держите ссылку."}
    >
      <V02 cues={[16.4, 29.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Три фазы"}
      sub={"Погружение, цель, всплытие"}
      main={"target и currentTarget — не одно и то же."}
    >
      <V03 cues={[15.6, 33.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Остановка пути"}
      sub={"stopPropagation"}
      main={"Не злоупотребляйте остановкой."}
    >
      <V04 cues={[10.9, 22.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Делегирование"}
      sub={"Один обработчик на контейнер"}
      main={"closest находит нужный элемент."}
    >
      <V05 cues={[10.4, 27.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Действие по умолчанию"}
      sub={"preventDefault и passive"}
      main={"Из пассивного слушателя preventDefault не вызвать."}
    >
      <V06 cues={[15.4, 31.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Указатели"}
      sub={"Pointer Events"}
      main={"setPointerCapture держит указатель в элементе."}
    >
      <V07 cues={[11.7, 29.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Клавиатура"}
      sub={"key, code, композиция"}
      main={"Для горячих клавиш — code."}
    >
      <V08 cues={[18.3, 26.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Формы и фокус"}
      sub={"input, change, submit"}
      main={"focus и blur не всплывают."}
    >
      <V09 cues={[14.9, 32.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Свои события"}
      sub={"CustomEvent и EventTarget"}
      main={"Подписки нужно снимать."}
    >
      <V10 cues={[14.8, 31.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Частые события"}
      sub={"Дебаунс и троттлинг"}
      main={"Для видимости — IntersectionObserver."}
    >
      <V11 cues={[16.0, 27.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Порядок и автоматы"}
      sub={"Синхронный dispatch"}
      main={"Сложные жесты — конечные автоматы."}
    >
      <V12 cues={[18.4, 32.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — формы и хранилища."}
    >
      <V13 cues={[15.4, 30.6]} />
    </Slide>
  );
}

export const SLIDES_J16 = {
  "11:16": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J16).
export const SLIDE_TITLES_J16 = {
  "11:16": [
    "Введение",
    "Подписка",
    "Фазы",
    "Остановка",
    "Делегирование",
    "По умолчанию",
    "Указатели",
    "Клавиатура",
    "Формы",
    "CustomEvent",
    "Частые",
    "Автоматы",
    "Итоги",
  ],
};
