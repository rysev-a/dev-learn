// Слайды для «Современный Frontend», глава 14 — «Дерево DOM: поиск, изменение и создание узлов».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js14.jsx).

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
} from "../anim/Js14.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 14", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Разметка → дерево"}
      sub={"Глава 14 · Объектная модель документа"}
      main={"Изменение дерева сразу отражается на экране."}
    >
      <V01 cues={[18.9, 32.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Типы узлов"}
      sub={"children и childNodes"}
      main={"Первый ребёнок элемента часто — текст, а не тег."}
    >
      <V02 cues={[16.5, 29.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Поиск"}
      sub={"querySelector, matches, closest"}
      main={"closest — основа делегирования событий."}
    >
      <V03 cues={[16.9, 23.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Содержимое и безопасность"}
      sub={"textContent и innerHTML"}
      main={"Ввод пользователя — только через textContent."}
    >
      <V04 cues={[12.2, 28.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Создание и вставка"}
      sub={"createElement, fragment"}
      main={"Фрагмент вставляется одним действием."}
    >
      <V05 cues={[14.2, 29.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Атрибуты и свойства"}
      sub={"Строки и состояние"}
      main={"Булев атрибут работает по наличию."}
    >
      <V06 cues={[15.6, 33.0]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Обход дерева"}
      sub={"Рекурсия и TreeWalker"}
      main={"Ищите внутри небольшого контейнера."}
    >
      <V07 cues={[9.7, 29.0]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Веб-компоненты"}
      sub={"Custom Elements и Shadow DOM"}
      main={"Теневой DOM изолирует стили и селекторы."}
    >
      <V08 cues={[21.4, 30.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Наблюдатели"}
      sub={"Mutation, Intersection, Resize"}
      main={"Наблюдатели асинхронны и не вызывают раскладку."}
    >
      <V09 cues={[13.9, 23.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Производительность DOM"}
      sub={"Пакеты и виртуальное дерево"}
      main={"Не чередуйте чтение и запись."}
    >
      <V10 cues={[14.4, 26.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Разбор и сериализация"}
      sub={"Парсер, DOMParser, Range"}
      main={"Дерево может отличаться от написанной разметки."}
    >
      <V11 cues={[9.9, 28.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Доступность"}
      sub={"Семантика и ARIA"}
      main={"Семантический тег — это уже роль и поведение."}
    >
      <V12 cues={[17.9, 26.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — CSS."}>
      <V13 cues={[14.6, 26.4]} />
    </Slide>
  );
}

export const SLIDES_J14 = {
  "11:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J14).
export const SLIDE_TITLES_J14 = {
  "11:14": [
    "Введение",
    "Узлы",
    "Поиск",
    "Безопасность",
    "Вставка",
    "Атрибуты",
    "Обход",
    "Компоненты",
    "Наблюдатели",
    "Производительность",
    "Парсер",
    "Доступность",
    "Итоги",
  ],
};
