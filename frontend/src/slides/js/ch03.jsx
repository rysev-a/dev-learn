// Слайды для «Современный Frontend», глава 3 — «Медленная эволюция и быстрый взрыв: ES5, ES6, Babel, сборщики и препроцессоры».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js03.jsx).

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
} from "../anim/Js03.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ИСТОРИЯ / ГЛАВА 3", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Десять лет тишины"}
      sub={"Глава 3 · От ES3 к ежегодным выпускам"}
      main={"Десять лет язык не менялся, а затем стал выходить каждый год."}
    >
      <V01 cues={[18.4, 32.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Провал ES4"}
      sub={"Раскол комитета, 2008"}
      main={"Амбициозную четвёртую редакцию отменили."}
    >
      <V02 cues={[11.0, 30.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Старые браузеры"}
      sub={"IE6–IE8 и синтаксис"}
      main={"Скорость языка определял самый старый браузер."}
    >
      <V03 cues={[13.9, 28.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"ES5"}
      sub={"Строгий режим, JSON, методы массивов"}
      main={"ES5 — база, на которую опирались до переломного момента."}
    >
      <V04 cues={[23.1, 28.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"CoffeeScript"}
      sub={"Транспиляция"}
      main={"Язык можно улучшать «снаружи», компилируя в JavaScript."}
    >
      <V05 cues={[20.4, 25.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Модули и сборка"}
      sub={"CommonJS, Browserify, Grunt, Gulp"}
      main={"Так родились сборщики и инструменты автоматизации."}
    >
      <V06 cues={[15.1, 30.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Препроцессоры CSS"}
      sub={"Sass, Less, Stylus, PostCSS"}
      main={"Переменные, вложенность и миксины пришли в CSS снаружи."}
    >
      <V07 cues={[14.6, 33.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"ES2015 (ES6)"}
      sub={"Самое большое обновление"}
      main={"Весь современный язык вышел одним пакетом."}
    >
      <V08 cues={[6.0, 30.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"TC39 и ежегодные выпуски"}
      sub={"Стадии и evergreen"}
      main={"Редакции — по году, браузеры обновляются сами."}
    >
      <V09 cues={[19.8, 32.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Babel"}
      sub={"Новый синтаксис — в старый"}
      main={"Писать на завтрашнем языке сегодня."}
    >
      <V10 cues={[13.2, 31.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"webpack и другие"}
      sub={"Всё — модуль"}
      main={"Сборщики вырастили «усталость от JavaScript»."}
    >
      <V11 cues={[17.8, 39.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Быстрые инструменты"}
      sub={"TypeScript, esbuild, Vite"}
      main={"Сборщики на Go и Rust, а CSS поглотил часть препроцессоров."}
    >
      <V12 cues={[19.3, 27.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"История закончена: теперь сам язык."}
    >
      <V13 cues={[14.9, 20.0]} />
    </Slide>
  );
}

export const SLIDES_J3 = {
  "11:3": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J3).
export const SLIDE_TITLES_J3 = {
  "11:3": [
    "Введение",
    "ES4",
    "Старые браузеры",
    "ES5",
    "CoffeeScript",
    "Сборка",
    "Препроцессоры",
    "ES6",
    "TC39",
    "Babel",
    "webpack",
    "Быстрые",
    "Итоги",
  ],
};
