// Слайды для «Изучаем Rust», глава 10 — «Функции и условные конструкции: def и fn».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs10.jsx).

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
} from "../anim/Rs10.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 10", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Из def в fn"}
      sub={"Глава 10 · Python → Rust"}
      main={"Скобки вместо отступов; elif → else if; где нет свободы Python."}
    >
      <V01 cues={[13.0, 23.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Сигнатуры"}
      sub={"Типы обязательны"}
      main={
        "Аннотации Python не проверяются; в Rust типы обязательны; обобщения."
      }
    >
      <V02 cues={[10.9, 24.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Значения по умолчанию"}
      sub={"Option и строитель"}
      main={"Нет default: Option, две функции, структура-строитель."}
    >
      <V03 cues={[12.0, 23.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"*args и **kwargs"}
      sub={"Срезы и структуры"}
      main={"Срез вместо *args; структура вместо **kwargs."}
    >
      <V04 cues={[13.1, 28.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Возврат значений"}
      sub={"Кортеж, (), Option, Result"}
      main={"Кортеж, () вместо None, Option и Result."}
    >
      <V05 cues={[7.5, 25.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Функции как значения"}
      sub={"fn и замыкания"}
      main={"Указатель на функцию и |x| x + 1."}
    >
      <V06 cues={[11.2, 31.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Документация"}
      sub={"/// и doctest"}
      main={"/// и cargo doc; примеры запускаются как тесты."}
    >
      <V07 cues={[9.2, 29.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Условия"}
      sub={"if, else if, &&, ||, !"}
      main={"Только bool; &&, ||, !; тернарного оператора нет."}
    >
      <V08 cues={[13.1, 25.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"match"}
      sub={"Цепочки и образцы"}
      main={"Нет цепочки 1 < x < 10; match с диапазонами и охранниками."}
    >
      <V09 cues={[17.7, 31.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Циклы"}
      sub={"range, while, loop"}
      main={"0..n, loop вместо while True, нет for-else."}
    >
      <V10 cues={[9.7, 26.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ошибки"}
      sub={"Result вместо исключений"}
      main={"Result, оператор ?, panic!."}
    >
      <V11 cues={[17.1, 25.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Генераторы"}
      sub={"Итераторы и цепочки"}
      main={"yield → Iterator; включения → цепочки; any и all."}
    >
      <V12 cues={[17.2, 25.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — строки."}>
      <V13 cues={[9.5, 25.3]} />
    </Slide>
  );
}

export const SLIDES_R10 = {
  "10:10": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R10).
export const SLIDE_TITLES_R10 = {
  "10:10": [
    "Введение",
    "Сигнатуры",
    "Default",
    "*args",
    "Возврат",
    "Замыкания",
    "Документация",
    "Условия",
    "match",
    "Циклы",
    "Ошибки",
    "Итераторы",
    "Итоги",
  ],
};
