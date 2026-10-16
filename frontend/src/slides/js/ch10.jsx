// Слайды для «Современный Frontend», глава 10 — «Промисы и async/await: цепочки, ошибки, параллельность».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js10.jsx).

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
} from "../anim/Js10.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 10", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Результат — потом"}
      sub={"Глава 10 · Асинхронность"}
      main={"Колбэки, промисы, async/await — три способа описать «позже»."}
    >
      <V01 cues={[14.6, 25.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Колбэки"}
      sub={"Ад колбэков и доверие"}
      main={"Колбэки приводят к лесенке и размазанной обработке ошибок."}
    >
      <V02 cues={[11.3, 23.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Promise"}
      sub={"Состояния и подписка"}
      main={"Промис меняет состояние один раз."}
    >
      <V03 cues={[16.0, 30.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Цепочки"}
      sub={"then, catch, finally"}
      main={"then возвращает новый промис — вместо лесенки плоский список."}
    >
      <V04 cues={[14.4, 29.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Порядок выполнения"}
      sub={"Микрозадачи"}
      main={"Обработчики промисов идут раньше таймеров."}
    >
      <V05 cues={[12.3, 24.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Комбинаторы"}
      sub={"all, allSettled, race, any"}
      main={"Выберите комбинатор по тому, что делать с ошибкой."}
    >
      <V06 cues={[16.8, 29.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"async/await"}
      sub={"Сахар над промисами"}
      main={"async-функция всегда возвращает промис."}
    >
      <V07 cues={[12.3, 29.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Типичные ошибки"}
      sub={"await, forEach, последовательность"}
      main={"Независимое запускайте параллельно, а не друг за другом."}
    >
      <V08 cues={[9.1, 32.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ограничение параллельности"}
      sub={"Пул и порядок"}
      main={"Одновременно работает не больше заданного числа задач."}
    >
      <V09 cues={[17.9, 29.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Отмена"}
      sub={"AbortController"}
      main={"Промис не отменить, но можно перестать его слушать."}
    >
      <V10 cues={[15.8, 25.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Async-итераторы"}
      sub={"for await и async function*"}
      main={"Следующий элемент запрашивается по требованию."}
    >
      <V11 cues={[9.4, 29.7]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Другие очереди"}
      sub={"queueMicrotask, promisify"}
      main={"Каждый промис должен быть где-то обработан."}
    >
      <V12 cues={[16.2, 29.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — функциональное программирование."}
    >
      <V13 cues={[15.7, 29.4]} />
    </Slide>
  );
}

export const SLIDES_J10 = {
  "11:10": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J10).
export const SLIDE_TITLES_J10 = {
  "11:10": [
    "Введение",
    "Колбэки",
    "Promise",
    "Цепочки",
    "Порядок",
    "Комбинаторы",
    "async/await",
    "Ошибки",
    "Пул",
    "Отмена",
    "for await",
    "Очереди",
    "Итоги",
  ],
};
