// Слайды для «Python как первый язык», глава 41 — «Протоколы и обобщения».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py41.jsx).

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
} from "../anim/Py41.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ПРОЕКТИРОВАНИЕ КЛАССОВ / ГЛАВА 41", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Подсказки типов"}
      sub={"Не проверяются при запуске"}
      main={"Подсказки читают редакторы и проверяющие программы."}
    >
      <V01 cues={[14.1, 26.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Protocol"}
      sub={"Структурная подтипизация"}
      main={"Подойдёт любой объект с нужными методами."}
    >
      <V02 cues={[13.3, 25.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"runtime_checkable"}
      sub={"Проверка во время выполнения"}
      main={"Проверяются только имена методов."}
    >
      <V03 cues={[11.6, 23.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Готовые протоколы"}
      sub={"Sized, Iterable, SupportsInt"}
      main={"Принимайте наименее требовательный тип."}
    >
      <V04 cues={[10.6, 26.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"TypeVar"}
      sub={"Связь входа и выхода"}
      main={"T связывает тип аргумента с типом результата."}
    >
      <V05 cues={[16.1, 29.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Обобщённые классы"}
      sub={"Generic и новый синтаксис"}
      main={"Stack[int] — стек целых; в 3.12 — class Stack[T]."}
    >
      <V06 cues={[17.1, 26.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Вариантность"}
      sub={"Инвариантность и ковариантность"}
      main={"list[int] не является list[object]."}
    >
      <V07 cues={[13.6, 26.7]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Ещё средства typing"}
      sub={"Self, Literal, TypedDict"}
      main={"Self сохраняет тип наследника."}
    >
      <V08 cues={[12.5, 28.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"overload"}
      sub={"Заглушки для проверки"}
      main={"overload — для подсказок, singledispatch — для поведения."}
    >
      <V09 cues={[14.1, 25.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Проверяющие программы"}
      sub={"Any и object"}
      main={"Включайте строгость по частям."}
    >
      <V10 cues={[9.3, 23.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Внедрение зависимостей"}
      sub={"Протокол как интерфейс"}
      main={"Модули зависят от формы, а не от классов."}
    >
      <V11 cues={[11.9, 21.0]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Чего избегать"}
      main={"Исправляйте код, а не отключайте проверки."}
    >
      <V12 cues={[12.4, 24.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Протоколы и обобщения"}
      main={"Принимайте широко, возвращайте точно."}
    >
      <V13 cues={[12.6, 16.3, 29.9]} />
    </Slide>
  );
}

export const SLIDES_P41 = {
  "13:41": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P41).
export const SLIDE_TITLES_P41 = {
  "13:41": [
    "Подсказки",
    "Protocol",
    "runtime",
    "Готовые",
    "TypeVar",
    "Generic",
    "Вариантность",
    "Self и другие",
    "overload",
    "mypy и pyright",
    "DI",
    "Ошибки",
    "Итоги",
  ],
};
