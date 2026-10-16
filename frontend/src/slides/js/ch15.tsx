// Слайды для «Современный Frontend», глава 15 — «CSS для программиста: каскад, flexbox, grid, переменные и анимации».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js15.jsx).

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
} from "../anim/Js15.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 15", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Язык стилей"}
      sub={"Глава 15 · Декларативность"}
      main={"Вы описываете правила — движок выбирает победителя."}
    >
      <V01 cues={[12.7, 26.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Синтаксис и единицы"}
      sub={"Правила, длины, цвета"}
      main={"Относительные единицы — основа адаптивности."}
    >
      <V02 cues={[10.6, 29.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Специфичность"}
      sub={"Тройка чисел"}
      main={"Один идентификатор сильнее сотни классов."}
    >
      <V03 cues={[9.8, 31.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Каскад"}
      sub={"Порядок и наследование"}
      main={"Слои заменяют войну специфичностью."}
    >
      <V04 cues={[14.3, 29.0]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Блочная модель"}
      sub={"border-box и схлопывание"}
      main={"Включайте box-sizing: border-box."}
    >
      <V05 cues={[20.2, 31.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Flexbox"}
      sub={"Одна ось"}
      main={"Свободное место делится пропорционально grow."}
    >
      <V06 cues={[16.6, 30.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Grid"}
      sub={"Две оси"}
      main={"auto-fill и minmax — адаптивность без медиа-запросов."}
    >
      <V07 cues={[12.9, 33.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Позиционирование"}
      sub={"position и z-index"}
      main={"z-index действует внутри контекста наложения."}
    >
      <V08 cues={[20.5, 34.0]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Переменные"}
      sub={"var() и темы"}
      main={"Тема — набор переменных на корне."}
    >
      <V09 cues={[10.4, 30.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Адаптивность"}
      sub={"Media и контейнеры"}
      main={"Сначала малые экраны."}
    >
      <V10 cues={[15.3, 30.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Анимации"}
      sub={"transition и keyframes"}
      main={"Анимируйте transform и opacity."}
    >
      <V11 cues={[10.9, 30.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Организация CSS"}
      sub={"БЭМ, модули, утилиты"}
      main={"Плоская специфичность — меньше боли."}
    >
      <V12 cues={[9.6, 31.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — события."}>
      <V13 cues={[15.5, 29.4]} />
    </Slide>
  );
}

export const SLIDES_J15 = {
  "11:15": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J15).
export const SLIDE_TITLES_J15 = {
  "11:15": [
    "Введение",
    "Единицы",
    "Специфичность",
    "Каскад",
    "Блоки",
    "Flexbox",
    "Grid",
    "position",
    "Переменные",
    "Адаптивность",
    "Анимации",
    "Организация",
    "Итоги",
  ],
};
