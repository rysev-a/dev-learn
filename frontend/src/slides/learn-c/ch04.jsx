// Слайды для «От assembler к языку C», глава 4 — «Строки, структуры и union: данные в памяти».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl04.jsx).

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
} from "../anim/Cl04.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОТ ASSEMBLER К ЯЗЫКУ C / ПАМЯТЬ И ДАННЫЕ / ГЛАВА 4</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Строка — массив"}
      sub={"Глава 4 · Нулевой байт"}
      main={"Строка — массив байтов с нулём в конце; длина нигде не хранится."}
    >
      <V01 cues={[13.5, 31.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"char и кодировка"}
      sub={"Число, а не символ"}
      main={"'1' — это 49; русская буква в UTF-8 — два байта."}
    >
      <V02 cues={[14.8, 28.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"string.h"}
      sub={"strlen, strcpy, strncpy"}
      main={"strlen — O(n); strncpy не ставит нуль — предпочитайте snprintf."}
    >
      <V03 cues={[14.1, 26.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Переполнение буфера"}
      sub={"Главная уязвимость"}
      main={
        "Знайте размер буфера и передавайте его; на тестах — AddressSanitizer."
      }
    >
      <V04 cues={[12.2, 30.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Разбор и форматирование"}
      sub={"strtol, snprintf"}
      main={"atoi молчит об ошибках; strtol и errno говорят всё."}
    >
      <V05 cues={[18.4, 30.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"struct"}
      sub={"Поля и доступ"}
      main={
        "Точка для объекта, стрелка для указателя; инициализация по именам."
      }
    >
      <V06 cues={[11.4, 28.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Копирование и сравнение"}
      sub={"По полям"}
      main={"Структуры копируются целиком, сравнивать — по полям, не memcmp."}
    >
      <V07 cues={[13.4, 32.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Выравнивание"}
      sub={"Заполнитель и порядок"}
      main={"Порядок полей определяет размер; C его не переставляет."}
    >
      <V08 cues={[10.7, 29.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Битовые поля и флаги"}
      sub={"Маски"}
      main={"Для обмена с миром — ручные маски и сдвиги."}
    >
      <V09 cues={[20.4, 28.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"union"}
      sub={"Одно место — разные типы"}
      main={"union + tag — ручной аналог enum с данными."}
    >
      <V10 cues={[10.8, 28.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"typedef и непрозрачные типы"}
      sub={"Инкапсуляция"}
      main={"Скрывайте поля в .c, показывайте указатель в заголовке."}
    >
      <V11 cues={[14.6, 26.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Сериализация"}
      sub={"Не «как есть»"}
      main={"Пишите поля по одному в договорённом порядке байтов."}
    >
      <V12 cues={[15.2, 28.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — malloc, free и структуры данных."}
    >
      <V13 cues={[16.4, 26.1]} />
    </Slide>
  );
}

export const SLIDES_C4 = {
  "16:4": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C4).
export const SLIDE_TITLES_C4 = {
  "16:4": [
    "Введение",
    "char",
    "string.h",
    "Переполнение",
    "strtol",
    "struct",
    "Копирование",
    "Выравнивание",
    "Флаги",
    "union",
    "typedef",
    "Сериализация",
    "Итоги",
  ],
};
