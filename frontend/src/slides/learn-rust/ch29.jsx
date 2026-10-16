// Слайды для «Изучаем Rust», глава 29 — «Трейты стандартной библиотеки: каталог».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs29.jsx).

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
} from "../anim/Rs29.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 29", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Словарь языка"}
      sub={"Глава 29 · Каталог трейтов"}
      main={"Группы трейтов и когда derive, а когда impl."}
    >
      <V01 cues={[19.0, 32.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Копирование"}
      sub={"Clone, Copy, Drop"}
      main={"Явная копия, побитовая копия, освобождение."}
    >
      <V02 cues={[16.6, 31.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Сравнение"}
      sub={"Eq, Ord, Hash"}
      main={"Частичные и полные; Hash согласован с Eq."}
    >
      <V03 cues={[15.0, 28.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Default"}
      sub={"Значения по умолчанию"}
      main={"derive, ручной impl, ..Default::default()."}
    >
      <V04 cues={[9.6, 30.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Преобразования"}
      sub={"From, TryFrom, AsRef"}
      main={"From и Into, TryFrom, AsRef, Borrow, ToOwned, Cow."}
    >
      <V05 cues={[16.0, 25.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Строки"}
      sub={"FromStr и ToString"}
      main={"parse, to_string, форматирующие трейты."}
    >
      <V06 cues={[13.9, 28.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Deref и Index"}
      sub={"Умные ссылки"}
      main={"Приведение при разыменовании; Index."}
    >
      <V07 cues={[16.0, 27.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Итерация"}
      sub={"Iterator и родственники"}
      main={"IntoIterator, FromIterator, Extend, DoubleEnded."}
    >
      <V08 cues={[12.9, 31.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Замыкания"}
      sub={"Fn, FnMut, FnOnce"}
      main={"Три трейта и порядок строгости."}
    >
      <V09 cues={[12.3, 26.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Ошибки"}
      sub={"Error"}
      main={"source, Box<dyn Error>, thiserror, anyhow."}
    >
      <V10 cues={[9.1, 23.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Маркеры"}
      sub={"Send, Sync, Sized"}
      main={"Send, Sync, Sized, PhantomData."}
    >
      <V11 cues={[13.7, 29.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Any"}
      sub={"Динамические типы"}
      main={"downcast_ref, TypeId, type_name."}
    >
      <V12 cues={[13.6, 29.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — асинхронность."}
    >
      <V13 cues={[25.6, 31.8]} />
    </Slide>
  );
}

export const SLIDES_R29 = {
  "10:29": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R29).
export const SLIDE_TITLES_R29 = {
  "10:29": [
    "Введение",
    "Копирование",
    "Сравнение",
    "Default",
    "Преобразования",
    "Строки",
    "Deref",
    "Итерация",
    "Замыкания",
    "Ошибки",
    "Маркеры",
    "Any",
    "Итоги",
  ],
};
