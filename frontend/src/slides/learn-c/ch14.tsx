// Слайды для «От assembler к языку C», глава 14 — «Современный C: C11 и C23».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl14.jsx).

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
} from "../anim/Cl14.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ОТ ASSEMBLER К ЯЗЫКУ C / УГЛУБЛЕНИЕ / ГЛАВА 14", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Редакции языка"}
      sub={"Глава 14 · -std"}
      main={"Выбирайте стандарт ключом -std; gnu11 добавляет расширения."}
    >
      <V01 cues={[19.9, 30.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Наследие C99"}
      sub={"Объявления, bool, restrict"}
      main={"Объявления там, где нужно; VLA — необязательны."}
    >
      <V02 cues={[11.2, 24.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Составные литералы"}
      sub={"Назначенные инициализаторы"}
      main={"Временные структуры в выражении живут до конца блока."}
    >
      <V03 cues={[17.1, 30.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Гибкий член массива"}
      sub={"Структура с хвостом"}
      main={"Один блок: заголовок плюс данные."}
    >
      <V04 cues={[11.1, 28.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"restrict и inline"}
      sub={"Обещания компилятору"}
      main={"restrict нельзя нарушать; static inline — в заголовках."}
    >
      <V05 cues={[7.4, 25.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Проверки C11"}
      sub={"_Static_assert, _Alignas"}
      main={"Проверки на этапе компиляции и анонимные члены."}
    >
      <V06 cues={[13.4, 27.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Атомарные операции"}
      sub={"stdatomic.h"}
      main={"fetch_add и CAS неделимы; гонки данных — UB."}
    >
      <V07 cues={[17.9, 28.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Модель памяти"}
      sub={"acquire / release"}
      main={"Порядки операций и CAS-цикл."}
    >
      <V08 cues={[19.5, 30.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Юникод"}
      sub={"char16_t, char32_t, u8"}
      main={"Байты — не символы."}
    >
      <V09 cues={[13.6, 20.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"C23: язык"}
      sub={"nullptr, constexpr, атрибуты"}
      main={"Ключевые слова, константы и стандартные атрибуты."}
    >
      <V10 cues={[14.4, 29.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"C23: библиотека"}
      sub={"stdckdint, stdbit"}
      main={"Арифметика с проверкой переполнения и битовые функции."}
    >
      <V11 cues={[14.4, 29.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Практика"}
      sub={"Что включать и чего избегать"}
      main={"C11+ и предупреждения; проверяйте поддержку C23."}
    >
      <V12 cues={[14.0, 26.3]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги книги"}
      sub={"Что дальше"}
      main={"Дальше — Unix, сети, виртуализация и Rust."}
    >
      <V13 cues={[16.4, 28.4]} />
    </Slide>
  );
}

export const SLIDES_C14 = {
  "16:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C14).
export const SLIDE_TITLES_C14 = {
  "16:14": [
    "Редакции",
    "C99",
    "Литералы",
    "Хвост",
    "restrict",
    "C11",
    "Атомики",
    "Память",
    "Юникод",
    "C23",
    "Библиотека",
    "Практика",
    "Итоги",
  ],
};
