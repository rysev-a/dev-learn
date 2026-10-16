// Слайды для «Современный Frontend», глава 4 — «Первая программа: браузер, Node и значения».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js04.jsx).

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
} from "../anim/Js04.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 4", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Один язык — везде"}
      sub={"Глава 4 · Браузер и сервер"}
      main={
        "JavaScript — единственный язык, который работает в каждом браузере; та же среда есть и на сервере."
      }
    >
      <V01 cues={[19.1, 32.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Движок"}
      sub={"V8: разбор, байт-код, JIT"}
      main={"Текст → дерево → байт-код → машинный код для частых функций."}
    >
      <V02 cues={[15.9, 27.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Первая программа"}
      sub={"console.log и шаблоны"}
      main={"В браузере вывод идёт в консоль DevTools, в Node — в терминал."}
    >
      <V03 cues={[11.6, 30.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"let, const, var"}
      sub={"Объявление переменных"}
      main={
        "По умолчанию const, а let — когда значение меняется; var не используют."
      }
    >
      <V04 cues={[11.9, 34.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Типы значений"}
      sub={"Семь примитивов и typeof"}
      main={"Тип несёт значение, а не переменная; у null typeof даёт «object»."}
    >
      <V05 cues={[18.9, 30.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Числа"}
      sub={"IEEE 754, NaN, BigInt"}
      main={"Число одно и дробное; для точных больших целых — BigInt."}
    >
      <V06 cues={[13.4, 29.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Строки"}
      sub={"UTF-16 и методы"}
      main={"Строки неизменяемы; for-of идёт по символам, а не по единицам."}
    >
      <V07 cues={[15.8, 31.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Истина и ложь"}
      sub={"||, ?? и ?."}
      main={"Ложны шесть значений; ?? реагирует только на null и undefined."}
    >
      <V08 cues={[18.3, 29.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Циклы"}
      sub={"for, for…of, for…in"}
      main={"Для коллекций — for…of; for…in перебирает имена свойств."}
    >
      <V09 cues={[12.5, 29.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Значения и ссылки"}
      sub={"Куча и сборщик мусора"}
      main={"Примитивы копируются, объекты передаются по ссылке."}
    >
      <V10 cues={[20.6, 33.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ошибки"}
      sub={"Исключения во время работы"}
      main={"Типы не проверяются заранее: многие ошибки всплывают при запуске."}
    >
      <V11 cues={[14.9, 30.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Отладка"}
      sub={"console и DevTools"}
      main={"Проверяйте значения и типы на каждом шаге — не угадывайте."}
    >
      <V12 cues={[15.6, 30.0]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — операторы, приведение типов и сравнение."}
    >
      <V13 cues={[14.1, 32.2]} />
    </Slide>
  );
}

export const SLIDES_J4 = {
  "11:4": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J4).
export const SLIDE_TITLES_J4 = {
  "11:4": [
    "Введение",
    "Движок",
    "console.log",
    "Переменные",
    "Типы",
    "Числа",
    "Строки",
    "Истина",
    "Циклы",
    "Ссылки",
    "Ошибки",
    "Отладка",
    "Итоги",
  ],
};
