// Слайды для «Современный Frontend», глава 23 — «Среды выполнения: Deno, Bun и встроенные тесты».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js23.tsx).

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
} from "../anim/Js23.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В NODE.JS / ГЛАВА 23", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Не только Node"}
      sub={"Глава 23 · Среды выполнения"}
      main={"Node, Deno и Bun — разные среды для одного языка: стандартный JS переносится, платформенные API — нет."}
    >
      <V01 cues={[13.1, 26.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Дино"}
      sub={"Безопасность по умолчанию"}
      main={"Deno: TypeScript без настройки, веб-стандарты, импорты по URL и JSR, права доступа."}
    >
      <V02 cues={[12.6, 25.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Права в Deno"}
      sub={"Флаги и области"}
      main={"--allow-read=/data разрешает только этот путь; --deny-* запрещает точечно."}
    >
      <V03 cues={[12, 24]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Бан"}
      sub={"Скорость и всё в одном"}
      main={"Bun: запуск и менеджер пакетов быстрее, встроенные сборщик и тест-раннер, совместимость с Node."}
    >
      <V04 cues={[13.1, 26.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Общие стандарты"}
      sub={"Один API на всех"}
      main={"fetch, Request/Response, URL, Web Streams, AbortController работают везде одинаково."}
    >
      <V05 cues={[13, 26]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"node:test"}
      sub={"Встроенный тест-раннер"}
      main={"node:test: test(), describe(), assert — без внешних библиотек; запуск node --test."}
    >
      <V06 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Хороший тест"}
      sub={"Arrange, Act, Assert"}
      main={"Подготовка, действие, проверка; тесты независимы, async-тест ждёт промис."}
    >
      <V07 cues={[13.5, 27]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Моки и таймеры"}
      sub={"mock.fn и fake timers"}
      main={"mock.fn записывает вызовы; fake timers управляют временем без ожидания."}
    >
      <V08 cues={[12.7, 25.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Таблицы случаев"}
      sub={"Параметризованные тесты"}
      main={"Один тест на таблицу «вход → ожидание»: добавить случай — одна строка."}
    >
      <V09 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Покрытие и CI"}
      sub={"Что показывает coverage"}
      main={"Покрытие показывает, что код выполнялся, но не что он проверен."}
    >
      <V10 cues={[12.4, 24.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Бенчмарки"}
      sub={"Измерять честно"}
      main={"Прогрев, много повторов, медиана и разброс; одно измерение ничего не значит."}
    >
      <V11 cues={[12.9, 25.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Как выбирать"}
      sub={"Переносимый код"}
      main={"Выбирайте по экосистеме, зрелости и требованиям к безопасности; код пишите переносимым."}
    >
      <V12 cues={[12.8, 25.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Среды и тесты"}
      main={"Три среды, общие веб-стандарты, встроенные тесты и честные замеры."}
    >
      <V13 cues={[12.8, 25.6]} />
    </Slide>
  );
}

export const SLIDES_J23 = {
  "11:23": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J23).
export const SLIDE_TITLES_J23 = {
  "11:23": [
    "Введение",
    "Deno",
    "Права",
    "Bun",
    "Стандарты",
    "node:test",
    "Структура",
    "Моки",
    "Таблицы",
    "Покрытие",
    "Бенчмарки",
    "Выбор",
    "Итоги",
  ],
};
