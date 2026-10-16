// Слайды для «Изучаем Rust», глава 4 — «Функции и возврат значения».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs04.jsx).

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
} from "../anim/Rs04.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 4</span>
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
      title={"Функция"}
      sub={"Глава 4 · fn"}
      main={
        "fn имя(параметры) { тело }; snake_case; порядок объявления не важен."
      }
    >
      <V01 cues={[13.3, 29.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Параметры"}
      sub={"Типы обязательны"}
      main={"Каждому параметру тип; значений по умолчанию нет."}
    >
      <V02 cues={[9.7, 25.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Возврат значения"}
      sub={"-> тип"}
      main={"Результат — последнее выражение без точки с запятой."}
    >
      <V03 cues={[12.1, 23.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Выражения и инструкции"}
      sub={"Что даёт значение"}
      main={"Выражение даёт значение; инструкция — нет; блок — выражение."}
    >
      <V04 cues={[15.2, 26.0]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"return"}
      sub={"Ранний выход"}
      main={"return — для раннего выхода; в конце его не пишут."}
    >
      <V05 cues={[13.4, 23.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"() и !"}
      sub={"Ничего и никогда"}
      main={"Без стрелки возвращается (); тип ! — у выражений без возврата."}
    >
      <V06 cues={[15.8, 25.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Кортежи"}
      sub={"Несколько результатов"}
      main={"Возвращаем кортеж; разбираем let (a, b); доступ .0 и .1."}
    >
      <V07 cues={[16.5, 26.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"if как выражение"}
      sub={"Значение ветки"}
      main={
        "if–else возвращает значение; ветки одного типа; тернарного оператора нет."
      }
    >
      <V08 cues={[11.9, 22.4]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Рекурсия"}
      sub={"Функция вызывает себя"}
      main={"Условие остановки; стек вызовов; вложенные функции."}
    >
      <V09 cues={[11.5, 26.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Передача по значению"}
      sub={"Копии и mut"}
      main={"Простые значения копируются; параметр можно сделать mut."}
    >
      <V10 cues={[11.4, 24.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Макросы"}
      sub={"println!, format!, assert!"}
      main={"Знак ! — макрос; format!, panic!, assert!."}
    >
      <V11 cues={[14.3, 25.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={"def → fn, типы обязательны, нет *args и значений по умолчанию."}
    >
      <V12 cues={[9.5, 24.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — условия и циклы."}
    >
      <V13 cues={[9.1, 22.3]} />
    </Slide>
  );
}

export const SLIDES_R4 = {
  "10:4": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R4).
export const SLIDE_TITLES_R4 = {
  "10:4": [
    "Введение",
    "Параметры",
    "Результат",
    "Выражения",
    "return",
    "Юнит",
    "Кортежи",
    "if",
    "Рекурсия",
    "По значению",
    "Макросы",
    "После Python",
    "Итоги",
  ],
};
