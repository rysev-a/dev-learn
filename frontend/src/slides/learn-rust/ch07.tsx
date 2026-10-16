// Слайды для «Изучаем Rust», глава 7 — «Кортежи, массивы и векторы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs07.jsx).

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
} from "../anim/Rs07.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 7", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Три составных типа"}
      sub={"Глава 7 · Кортеж, массив, вектор"}
      main={
        "Кортеж — разные типы, массив — фиксированный размер, вектор — растёт."
      }
    >
      <V01 cues={[14.6, 27.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Кортежи"}
      sub={"(A, B, C)"}
      main={"Доступ t.0, t.1; разбор let (x, y, z)."}
    >
      <V02 cues={[15.8, 26.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Массивы"}
      sub={"[T; N]"}
      main={"Длина — часть типа; в стеке; [0; 5]."}
    >
      <V03 cues={[12.9, 24.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Границы"}
      sub={"Паника и get"}
      main={"Индекс проверяется; get возвращает Option."}
    >
      <V04 cues={[9.5, 23.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Срезы"}
      sub={"&[T]"}
      main={"Ссылка на часть; параметры-срезы принимают всё."}
    >
      <V05 cues={[12.2, 32.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Vec"}
      sub={"Растущий массив"}
      main={"vec!, push, pop, len; данные в куче."}
    >
      <V06 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Доступ и Option"}
      sub={"get, first, last"}
      main={"v[i] паникует, get безопасен; Option — «значение или ничего»."}
    >
      <V07 cues={[15.8, 29.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Перебор"}
      sub={"&v, &mut v, iter"}
      main={"for по ссылке, по изменяемой ссылке; итераторы sum, max, filter."}
    >
      <V08 cues={[16.8, 24.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Изменение вектора"}
      sub={"insert, remove, extend"}
      main={"Методы изменения; нужен let mut."}
    >
      <V09 cues={[14.6, 26.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Сортировка и поиск"}
      sub={"sort, binary_search"}
      main={"sort, sort_by_key, binary_search, max, min."}
    >
      <V10 cues={[13.4, 26.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Двумерные данные"}
      sub={"Сетка"}
      main={"Vec<Vec<T>> и [[T; N]; M]; вложенные циклы."}
    >
      <V11 cues={[14.9, 27.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={
        "list → Vec; нет отрицательных индексов; comprehension → итераторы."
      }
    >
      <V12 cues={[13.9, 25.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — структуры, перечисления, Option."}
    >
      <V13 cues={[10.0, 21.2]} />
    </Slide>
  );
}

export const SLIDES_R7 = {
  "10:7": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R7).
export const SLIDE_TITLES_R7 = {
  "10:7": [
    "Введение",
    "Кортежи",
    "Массивы",
    "Границы",
    "Срезы",
    "Vec",
    "Доступ",
    "Перебор",
    "Изменение",
    "Сортировка",
    "Сетки",
    "После Python",
    "Итоги",
  ],
};
