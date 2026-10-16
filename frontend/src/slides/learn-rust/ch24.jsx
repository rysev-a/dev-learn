// Слайды для «Изучаем Rust», глава 24 — «Стандартная библиотека: core, alloc, std и прелюдия».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs24.jsx).

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
} from "../anim/Rs24.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 24", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Карта библиотеки"}
      sub={"Глава 24 · Обзор std"}
      main={"Структура, прелюдия, идиомы, комбинаторы."}
    >
      <V01 cues={[13.8, 22.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Три слоя"}
      sub={"core, alloc, std"}
      main={"core без ОС и кучи; alloc с кучей; std с ОС."}
    >
      <V02 cues={[20.0, 36.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Прелюдия"}
      sub={"Что доступно сразу"}
      main={"Option, Result, Vec, String и трейты — без use."}
    >
      <V03 cues={[12.6, 24.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Карта модулей"}
      sub={"Где что лежит"}
      main={"Данные, ввод-вывод, системные модули."}
    >
      <V04 cues={[12.8, 28.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Option"}
      sub={"Комбинаторы"}
      main={"map, and_then, filter, unwrap_or*, ok_or, take."}
    >
      <V05 cues={[12.8, 29.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Result"}
      sub={"Комбинаторы"}
      main={"map_err, and_then, ok, ?, From."}
    >
      <V06 cues={[14.8, 31.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Имена методов"}
      sub={"as_, to_, into_"}
      main={"Префиксы и суффиксы говорят о цене и владении."}
    >
      <V07 cues={[11.0, 25.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"std::mem"}
      sub={"swap, replace, take"}
      main={"Вынуть значение из &mut; размеры."}
    >
      <V08 cues={[16.4, 26.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"std::cmp"}
      sub={"Сравнение"}
      main={"min, max, clamp, Ordering, then, Reverse."}
    >
      <V09 cues={[9.6, 24.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"std::convert"}
      sub={"From, Into, AsRef"}
      main={"Единые преобразования; FromStr и Display."}
    >
      <V10 cues={[11.1, 30.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"std::iter"}
      sub={"Конструкторы итераторов"}
      main={"once, repeat, successors, from_fn; адаптеры и потребители."}
    >
      <V11 cues={[20.2, 25.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"env, process, документация"}
      sub={"Окружение"}
      main={"args, var, exit, Command; rustup doc."}
    >
      <V12 cues={[16.4, 31.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — коллекции."}
    >
      <V13 cues={[11.6, 25.1]} />
    </Slide>
  );
}

export const SLIDES_R24 = {
  "10:24": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R24).
export const SLIDE_TITLES_R24 = {
  "10:24": [
    "Введение",
    "Слои",
    "Прелюдия",
    "Модули",
    "Option",
    "Result",
    "Имена",
    "mem",
    "cmp",
    "convert",
    "iter",
    "Окружение",
    "Итоги",
  ],
};
