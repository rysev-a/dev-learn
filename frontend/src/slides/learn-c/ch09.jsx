// Слайды для «От assembler к языку C», глава 9 — «Представление данных: порядок байтов, IEEE 754 и битовые приёмы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl09.jsx).

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
} from "../anim/Cl09.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОТ ASSEMBLER К ЯЗЫКУ C / ВВОД-ВЫВОД И ДАННЫЕ / ГЛАВА 9</span>
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
      title={"Всё — байты"}
      sub={"Глава 9 · представление"}
      main={"Тип — договорённость о чтении байтов; stdint даёт точные размеры."}
    >
      <V01 cues={[14.9, 23.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Знак и переполнение"}
      sub={"Дополнительный код"}
      main={"Знаковое переполнение — UB, беззнаковое — по модулю."}
    >
      <V02 cues={[14.4, 25.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Порядок байтов"}
      sub={"Little- и big-endian"}
      main={"Переставляйте байты сдвигами и масками."}
    >
      <V03 cues={[15.1, 28.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Доступ к представлению"}
      sub={"Алиасинг и memcpy"}
      main={"Другое представление — копированием байтов."}
    >
      <V04 cues={[12.8, 25.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Выравнивание"}
      sub={"Прокладки в структурах"}
      main={"Поля от больших к меньшим; packed — дорого."}
    >
      <V05 cues={[19.2, 29.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Битовые операции"}
      sub={"Маски и сдвиги"}
      main={"Сдвиг на ширину типа и больше — UB."}
    >
      <V06 cues={[12.4, 26.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Битовые приёмы"}
      sub={"x & (x − 1)"}
      main={"Встроенные popcount, clz, ctz лучше самодельных циклов."}
    >
      <V07 cues={[14.9, 30.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Битовые поля"}
      sub={"Что не определено"}
      main={"Для протоколов и регистров — маски и сдвиги."}
    >
      <V08 cues={[6.4, 29.0]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"IEEE 754"}
      sub={"Знак, порядок, мантисса"}
      main={"Значение = 1.m · 2^(e − bias); особые порядки."}
    >
      <V09 cues={[19.8, 27.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Погрешность"}
      sub={"0.1 + 0.2"}
      main={"Сравнивайте с допуском; порядок суммирования важен."}
    >
      <V10 cues={[13.4, 25.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Особые значения"}
      sub={"NaN, inf, −0"}
      main={"isnan; целое на ноль — UB; приведение в целое — осторожно."}
    >
      <V11 cues={[9.5, 24.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Кодирование данных"}
      sub={"varint, base64, UTF-8, CRC"}
      main={"Сетевой порядок, переменная длина и контрольные суммы."}
    >
      <V12 cues={[14.9, 25.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — компоновка, make и библиотеки."}
    >
      <V13 cues={[13.1, 24.1]} />
    </Slide>
  );
}

export const SLIDES_C9 = {
  "16:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C9).
export const SLIDE_TITLES_C9 = {
  "16:9": [
    "Байты",
    "Знак",
    "Endian",
    "memcpy",
    "Выравнивание",
    "Биты",
    "Приёмы",
    "Поля",
    "IEEE 754",
    "Погрешность",
    "NaN",
    "Кодирование",
    "Итоги",
  ],
};
