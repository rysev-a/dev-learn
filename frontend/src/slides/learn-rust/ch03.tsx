// Слайды для «Изучаем Rust», глава 3 — «Типы данных: числа, символы, логика».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs03.jsx).

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
} from "../anim/Rs03.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 3", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Скалярные типы"}
      sub={"Глава 3 · Статическая типизация"}
      main={
        "Четыре скалярных вида: целые, дробные, bool, char; размер числа задаёт программист."
      }
    >
      <V01 cues={[14.9, 30.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Целые числа"}
      sub={"iN и uN"}
      main={
        "i8…i128 со знаком, u8…u128 без; usize — для индексов; по умолчанию i32."
      }
    >
      <V02 cues={[14.8, 23.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Переполнение"}
      sub={"Что если не влезло"}
      main={
        "debug — паника, release — оборот; checked/wrapping/saturating/overflowing."
      }
    >
      <V03 cues={[13.9, 25.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Литералы"}
      sub={"Как писать числа"}
      main={"1_000, 0xff, 0o17, 0b1010, 10u8, b'A'."}
    >
      <V04 cues={[11.9, 26.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Дробные числа"}
      sub={"f32 и f64"}
      main={"f64 по умолчанию; IEEE 754; inf и NaN."}
    >
      <V05 cues={[15.2, 30.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Арифметика"}
      sub={"Операции и деление"}
      main={"Целое деление отбрасывает дробь; ** нет; типы не смешиваются."}
    >
      <V06 cues={[16.1, 25.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Преобразование as"}
      sub={"x as f64"}
      main={"as явно меняет тип, но может отрезать биты и дробь."}
    >
      <V07 cues={[8.8, 25.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"bool"}
      sub={"true и false"}
      main={"&&, ||, !; в условии — только bool."}
    >
      <V08 cues={[17.8, 27.4]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"char"}
      sub={"Символ Unicode"}
      main={"Одинарные кавычки, 4 байта, методы и приведение."}
    >
      <V09 cues={[15.8, 30.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"From, TryFrom, parse"}
      sub={"Безопасные преобразования"}
      main={"From — без потерь, TryFrom — с проверкой, parse — из текста."}
    >
      <V10 cues={[12.9, 27.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Методы и константы"}
      sub={"abs, pow, MAX"}
      main={"Методы чисел, границы типа, size_of."}
    >
      <V11 cues={[12.9, 25.0]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={"Нет безграничного int; bool не число; типы не смешиваются."}
    >
      <V12 cues={[15.5, 20.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — функции."}>
      <V13 cues={[9.5, 23.3]} />
    </Slide>
  );
}

export const SLIDES_R3 = {
  "10:3": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R3).
export const SLIDE_TITLES_R3 = {
  "10:3": [
    "Введение",
    "Целые",
    "Переполнение",
    "Литералы",
    "Дробные",
    "Арифметика",
    "as",
    "bool",
    "char",
    "Конверсии",
    "Методы",
    "После Python",
    "Итоги",
  ],
};
