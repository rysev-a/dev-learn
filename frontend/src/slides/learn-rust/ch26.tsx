// Слайды для «Изучаем Rust», глава 26 — «Текст и форматирование: char, str, fmt и разбор».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs26.jsx).

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
} from "../anim/Rs26.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 26", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Инструментарий текста"}
      sub={"Глава 26 · char, str, fmt"}
      main={"Методы, шаблоны, форматирование, разбор — без пакетов."}
    >
      <V01 cues={[10.4, 30.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"char"}
      sub={"Категории и цифры"}
      main={"is_*, to_digit, from_digit, len_utf8, escape_*."}
    >
      <V02 cues={[7.7, 28.7]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Разбиение"}
      sub={"split-семейство"}
      main={
        "splitn, rsplit, split_terminator, split_inclusive, split_once, strip_prefix."
      }
    >
      <V03 cues={[19.3, 28.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Шаблоны"}
      sub={"Pattern"}
      main={"char, &str, массив, замыкание; trim_matches."}
    >
      <V04 cues={[13.8, 25.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Изменение String"}
      sub={"insert, retain, replace_range"}
      main={"Методы изменения; границы символов."}
    >
      <V05 cues={[12.4, 27.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Язык формата"}
      sub={"Грамматика"}
      main={"Заполнитель, выравнивание, знак, #, 0, ширина, точность, тип."}
    >
      <V06 cues={[16.6, 30.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Display и Debug"}
      sub={"Formatter"}
      main={"write!, pad, параметры форматтера, debug_struct."}
    >
      <V07 cues={[14.7, 22.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Разбор"}
      sub={"parse и from_str_radix"}
      main={"ParseIntError, радиксы, дробные, bool."}
    >
      <V08 cues={[17.9, 29.4]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Регистр"}
      sub={"Unicode и ASCII"}
      main={"to_uppercase, make_ascii_uppercase, eq_ignore_ascii_case."}
    >
      <V09 cues={[15.6, 28.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Приёмы"}
      sub={"Строки, токены, таблицы"}
      main={"lines, peekable, split_once, выравнивание таблиц."}
    >
      <V10 cues={[15.3, 30.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"За пределами std"}
      sub={"Пакеты"}
      main={"regex, unicode-*, serde, nom, comfy-table."}
    >
      <V11 cues={[10.9, 31.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Литералы"}
      sub={"Экранирование и макросы"}
      main={"Сырые и байтовые строки; concat!, include_str!."}
    >
      <V12 cues={[15.9, 36.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — ввод-вывод и файлы."}
    >
      <V13 cues={[15.4, 28.6]} />
    </Slide>
  );
}

export const SLIDES_R26 = {
  "10:26": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R26).
export const SLIDE_TITLES_R26 = {
  "10:26": [
    "Введение",
    "char",
    "Разбиение",
    "Шаблоны",
    "String",
    "Формат",
    "Display",
    "Разбор",
    "Регистр",
    "Приёмы",
    "Пакеты",
    "Литералы",
    "Итоги",
  ],
};
