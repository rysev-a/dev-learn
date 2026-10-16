// Слайды для «Современный Frontend», глава 2 — «Node.js и io.js: форк, который изменил Open Source».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js02.jsx).

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
} from "../anim/Js02.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ИСТОРИЯ / ГЛАВА 2", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Из браузера на сервер"}
      sub={"Глава 2 · История Node.js"}
      main={
        "Ссора вокруг Node.js — один из самых поучительных примеров «революции» в Open Source."
      }
    >
      <V01 cues={[9.6, 23.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Блокирующий ввод-вывод"}
      sub={"Поток на соединение и цикл событий"}
      main={"Один цикл событий обслуживает тысячи медленных клиентов."}
    >
      <V02 cues={[12.3, 27.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"JSConf 2009"}
      sub={"V8, libuv, колбэк"}
      main={"Однопоточная программа, цикл событий и колбэки."}
    >
      <V03 cues={[21.9, 26.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Почему JavaScript"}
      sub={"Чистый лист, замыкания, события"}
      main={
        "У JavaScript не было блокирующих библиотек и уже была событийная модель."
      }
    >
      <V04 cues={[14.7, 28.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"npm и require"}
      sub={"Экосистема пакетов"}
      main={"Менеджер пакетов и модули создали самую большую экосистему."}
    >
      <V05 cues={[17.3, 31.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Недовольство"}
      sub={"Joyent и редкие выпуски"}
      main={"Одна компания, редкие выпуски и закрытые решения."}
    >
      <V06 cues={[13.2, 33.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Форк io.js"}
      sub={"Декабрь 2014"}
      main={"Открытое управление, semver, свежий V8."}
    >
      <V07 cues={[16.8, 35.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Раскол и фонд"}
      sub={"Node.js Foundation, 2015"}
      main={"Давление форка заставило Joyent открыть управление."}
    >
      <V08 cues={[13.9, 29.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Воссоединение"}
      sub={"Node.js 4.0, сентябрь 2015"}
      main={"Форк «проиграл» в названии, но победил в идеях."}
    >
      <V09 cues={[14.1, 30.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Уроки"}
      sub={"Форк, управление, фонд"}
      main={"Форк — не война, а инструмент."}
    >
      <V10 cues={[14.6, 26.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Node.js сегодня"}
      sub={"LTS и встроенные возможности"}
      main={"Чётные версии — LTS; fetch и тесты уже встроены."}
    >
      <V11 cues={[11.2, 25.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Deno и Bun"}
      sub={"Новые рантаймы и покупки"}
      main={"Bun вошёл в Anthropic, Deno куплен Cloudflare."}
    >
      <V12 cues={[19.0, 33.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — как язык ускорился: Babel, сборщики, препроцессоры."}
    >
      <V13 cues={[13.6, 26.7]} />
    </Slide>
  );
}

export const SLIDES_J2 = {
  "11:2": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J2).
export const SLIDE_TITLES_J2 = {
  "11:2": [
    "Введение",
    "Боль",
    "2009",
    "Почему JS",
    "npm",
    "Joyent",
    "io.js",
    "Фонд",
    "Node 4.0",
    "Уроки",
    "Сегодня",
    "Deno, Bun",
    "Итоги",
  ],
};
