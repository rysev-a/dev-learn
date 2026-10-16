// Слайды для «Современный Frontend», глава 5 — «Операторы, приведение типов и сравнение».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js05.jsx).

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
} from "../anim/Js05.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 5", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Где JavaScript удивляет"}
      sub={"Глава 5 · Строгие правила"}
      main={"Результат всегда есть — и всегда по правилам приведения."}
    >
      <V01 cues={[18.1, 27.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Арифметика"}
      sub={"Деление, остаток, Infinity"}
      main={"Деление дробное; остаток берёт знак делимого, как в C."}
    >
      <V02 cues={[7.3, 29.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Оператор +"}
      sub={"Сложение или склейка"}
      main={
        "Если есть строка — склейка; иначе числа. Остальные операторы числовые."
      }
    >
      <V03 cues={[18.0, 27.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Явное приведение"}
      sub={"Number, parseInt"}
      main={"Приводите значения явно; parseInt — всегда с основанием."}
    >
      <V04 cues={[12.6, 24.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Неявное приведение"}
      sub={"valueOf и toString"}
      main={"Объекты сводятся к примитивам через valueOf и toString."}
    >
      <V05 cues={[13.6, 32.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"== и ==="}
      sub={"Два вида равенства"}
      main={"Везде строгое ===; нестрогое нетранзитивно."}
    >
      <V06 cues={[20.1, 30.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сравнение по величине"}
      sub={"< и >, sort"}
      main={"Строки — по кодам; цепочки не работают; sort — с функцией."}
    >
      <V07 cues={[14.9, 27.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Object.is"}
      sub={"NaN, ±0, SameValueZero"}
      main={"includes и Set находят NaN, а indexOf — нет."}
    >
      <V08 cues={[16.1, 26.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Логические операторы"}
      sub={"&&, ||, ??, ??="}
      main={"Операторы возвращают операнды; ?? не затирает 0 и ''."}
    >
      <V09 cues={[15.9, 28.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Побитовые операторы"}
      sub={"32 бита"}
      main={"Операнды сворачиваются к 32 битам; для больших чисел — BigInt."}
    >
      <V10 cues={[17.6, 30.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Методы чисел"}
      sub={"toFixed, round, Intl"}
      main={"toFixed возвращает строку; деньги хранят в копейках."}
    >
      <V11 cues={[8.5, 29.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"typeof, instanceof, in"}
      sub={"Остальные операторы"}
      main={"in видит унаследованное; скобки лучше таблицы приоритетов."}
    >
      <V12 cues={[10.4, 33.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — функции, область видимости и замыкания."}
    >
      <V13 cues={[11.6, 25.9]} />
    </Slide>
  );
}

export const SLIDES_J5 = {
  "11:5": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J5).
export const SLIDE_TITLES_J5 = {
  "11:5": [
    "Введение",
    "Арифметика",
    "Оператор +",
    "Явное",
    "Неявное",
    "Равенство",
    "Сравнение",
    "Object.is",
    "Логика",
    "Биты",
    "Числа",
    "Операторы",
    "Итоги",
  ],
};
