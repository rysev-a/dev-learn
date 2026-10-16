// Слайды для «Современный Frontend», глава 12 — «Библиотеки и приёмы ФП: Ramda, lodash/fp, Immer, RxJS, Maybe и Either, линзы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js12.jsx).

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
} from "../anim/Js12.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 12", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Экосистема ФП"}
      sub={"Глава 12 · Что выросло из идей"}
      main={
        "Библиотеки решают разные задачи: утилиты, неизменяемость, типы, потоки."
      }
    >
      <V01 cues={[10.7, 28.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"lodash и lodash/fp"}
      sub={"Утилиты и fp-вариант"}
      main={
        "В fp-варианте функции каррированы, а данные — последним параметром."
      }
    >
      <V02 cues={[16.9, 29.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Ramda"}
      sub={"Всё каррировано"}
      main={
        "Единообразие и порядок аргументов — сила Ramda; читаемость — ловушка."
      }
    >
      <V03 cues={[10.4, 31.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Immer"}
      sub={"produce и черновик"}
      main={"Меняйте черновик — получайте неизменяемый результат."}
    >
      <V04 cues={[17.7, 33.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Персистентные структуры"}
      sub={"Общие части версий"}
      main={"Копируется только путь к изменённой ячейке."}
    >
      <V05 cues={[13.4, 30.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Типы-суммы"}
      sub={"fp-ts, Effect, Validation"}
      main={"Валидация копит все ошибки, а не первую."}
    >
      <V06 cues={[8.5, 30.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Линзы"}
      sub={"view, set, over"}
      main={"Линзы композируются, как функции."}
    >
      <V07 cues={[13.0, 28.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Трансдьюсеры"}
      sub={"Преобразуем редьюсер"}
      main={"Один проход без промежуточных массивов."}
    >
      <V08 cues={[9.6, 30.4]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"RxJS"}
      sub={"Observable, операторы, Subject"}
      main={"Подписку нужно закрывать."}
    >
      <V09 cues={[12.5, 28.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Комбинирование потоков"}
      sub={"switchMap, mergeMap, combineLatest"}
      main={"switchMap отбрасывает устаревший внутренний поток."}
    >
      <V10 cues={[16.6, 32.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Эффекты как данные"}
      sub={"Task и Reader"}
      main={"Функции возвращают описание, а выполняет его оболочка."}
    >
      <V11 cues={[16.0, 27.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Границы применения"}
      sub={"Цена и разумный путь"}
      main={"ФП окупается там, где упрощает код."}
    >
      <V12 cues={[14.6, 28.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — браузер изнутри."}
    >
      <V13 cues={[14.9, 26.0]} />
    </Slide>
  );
}

export const SLIDES_J12 = {
  "11:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J12).
export const SLIDE_TITLES_J12 = {
  "11:12": [
    "Введение",
    "lodash",
    "Ramda",
    "Immer",
    "Персистентные",
    "Типы-суммы",
    "Линзы",
    "Трансдьюсеры",
    "RxJS",
    "switchMap",
    "Task, Reader",
    "Границы",
    "Итоги",
  ],
};
