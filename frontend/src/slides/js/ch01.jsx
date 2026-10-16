// Слайды для «Современный Frontend», глава 1 — «Рождение JavaScript: десять дней, войны браузеров и ECMAScript».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js01.jsx).

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
} from "../anim/Js01.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ИСТОРИЯ / ГЛАВА 1", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Карта книги"}
      sub={"Глава 1 · От истории к фреймворку"}
      main={"У большинства странностей JavaScript есть исторический повод."}
    >
      <V01 cues={[11.0, 33.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Мёртвые страницы"}
      sub={"Netscape, 1995"}
      main={"Страницы нужно было оживить — и Netscape позвала Брендана Айка."}
    >
      <V02 cues={[14.9, 33.7]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Десять дней"}
      sub={"Mocha → LiveScript → JavaScript"}
      main={"Название JavaScript — маркетинг; к Java язык не относится."}
    >
      <V03 cues={[17.9, 29.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Три источника"}
      sub={"C/Java, Scheme, Self"}
      main={"Синтаксис из C, функции из Scheme, прототипы из Self."}
    >
      <V04 cues={[16.9, 29.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Война браузеров"}
      sub={"JavaScript против JScript"}
      main={"Без стандарта веб развалится на несовместимые сети."}
    >
      <V05 cues={[12.8, 32.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"ECMAScript"}
      sub={"Ecma-262 и TC39"}
      main={"ES3 десять лет оставался основой веба."}
    >
      <V06 cues={[16.9, 28.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"DOM, CSS и DHTML"}
      sub={"Три технологии"}
      main={"Разметка, оформление и поведение — три отдельных слоя."}
    >
      <V07 cues={[12.9, 33.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Ajax"}
      sub={"XMLHttpRequest и JSON"}
      main={"Данные без перезагрузки — и JSON вместо XML."}
    >
      <V08 cues={[16.4, 29.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"jQuery"}
      sub={"Одинаково во всех браузерах"}
      main={"$() — найти элементы по селектору и что-то с ними сделать."}
    >
      <V09 cues={[14.3, 28.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Нет модулей"}
      sub={"Глобальные имена и IIFE"}
      main={"Модуль на замыкании — главный приём эпохи ES3."}
    >
      <V10 cues={[13.8, 29.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Chrome и V8"}
      sub={"2008: JIT-компиляция"}
      main={"V8 показал, что JavaScript может быть быстрым."}
    >
      <V11 cues={[14.8, 34.7]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Разработка в 2008"}
      sub={"Без инструментов"}
      main={"Ни пакетов, ни сборки, ни модулей — только браузер."}
    >
      <V12 cues={[12.9, 28.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — выход на сервер: история Node.js и io.js."}
    >
      <V13 cues={[12.1, 31.6]} />
    </Slide>
  );
}

export const SLIDES_J1 = {
  "11:1": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J1).
export const SLIDE_TITLES_J1 = {
  "11:1": [
    "Введение",
    "Netscape",
    "Десять дней",
    "Источники",
    "Война",
    "ECMAScript",
    "DHTML",
    "Ajax",
    "jQuery",
    "Модули",
    "V8",
    "2008",
    "Итоги",
  ],
};
