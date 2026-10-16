// Слайды для «Современный Frontend», глава 8 — «Классы, прототипы и итераторы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js08.jsx).

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
} from "../anim/Js08.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 8", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Объекты с поведением"}
      sub={"Глава 8 · От литерала к классу"}
      main={"Под классами лежит цепочка прототипов."}
    >
      <V01 cues={[14.0, 33.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Цепочка прототипов"}
      sub={"Поиск и затенение"}
      main={"Поле ищется вверх по цепочке; запись идёт в сам объект."}
    >
      <V02 cues={[16.5, 24.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Конструктор и new"}
      sub={"Четыре шага"}
      main={
        "new создаёт объект, связывает прототип, вызывает функцию и возвращает объект."
      }
    >
      <V03 cues={[19.4, 27.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Класс"}
      sub={"Сахар над прототипами"}
      main={"Класс — это функция-конструктор; без new его не вызвать."}
    >
      <V04 cues={[17.2, 30.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Поля и приватность"}
      sub={"#private, static, get/set"}
      main={"Имя с решёткой — настоящее приватное поле."}
    >
      <V05 cues={[10.2, 31.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Наследование"}
      sub={"extends и super"}
      main={"super() вызывают до первого обращения к this."}
    >
      <V06 cues={[12.0, 30.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Потеря this"}
      sub={"bind, стрелка, обёртка"}
      main={"Метод как колбэк теряет this — привяжите или оберните."}
    >
      <V07 cues={[16.1, 27.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Композиция"}
      sub={"Вместо глубоких иерархий"}
      main={"Собирайте объекты из возможностей, а не из длинных цепочек."}
    >
      <V08 cues={[16.1, 27.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Дескрипторы"}
      sub={"writable, enumerable, freeze"}
      main={"freeze и seal защищают объект; заморозка поверхностная."}
    >
      <V09 cues={[13.4, 31.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Символы и протоколы"}
      sub={"Symbol.iterator"}
      main={"Протокол — метод с особым символом в качестве ключа."}
    >
      <V10 cues={[15.1, 32.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Итераторы"}
      sub={"next() и done"}
      main={"Итератор ленив: следующий элемент считается по запросу."}
    >
      <V11 cues={[17.1, 27.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Генераторы"}
      sub={"function* и yield"}
      main={
        "Генератор приостанавливается на yield и продолжается с того же места."
      }
    >
      <V12 cues={[10.8, 28.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — асинхронность: цикл событий, промисы, async и await."}
    >
      <V13 cues={[14.5, 30.7]} />
    </Slide>
  );
}

export const SLIDES_J8 = {
  "11:8": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J8).
export const SLIDE_TITLES_J8 = {
  "11:8": [
    "Введение",
    "Прототипы",
    "new",
    "class",
    "Поля",
    "extends",
    "this",
    "Композиция",
    "Дескрипторы",
    "Символы",
    "Итераторы",
    "Генераторы",
    "Итоги",
  ],
};
