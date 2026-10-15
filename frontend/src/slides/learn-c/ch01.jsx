// Слайды для «От assembler к языку C», глава 1 — «От ассемблера к C: первая программа, типы и компиляция».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl01.jsx).

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
} from "../anim/Cl01.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОТ ASSEMBLER К ЯЗЫКУ C / ОСНОВЫ ЯЗЫКА / ГЛАВА 1</span>
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
      title={"Ассемблер и C"}
      sub={"Глава 1 · Переносимый ассемблер"}
      main={
        "C — запись, близкая к железу, но переносимая: переводом занимается компилятор."
      }
    >
      <V01 cues={[17.2, 32.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Четыре шага"}
      sub={"От main.c до a.out"}
      main={
        "Препроцессор → компилятор → ассемблер → компоновщик: каждый шаг можно увидеть."
      }
    >
      <V02 cues={[17.0, 31.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Первая программа"}
      sub={"main, printf, код возврата"}
      main={"main возвращает код завершения: 0 — успех, остальное — ошибка."}
    >
      <V03 cues={[16.0, 25.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Типы и размеры"}
      sub={"char, int, long, stdint"}
      main={
        "Размеры зависят от платформы; когда важны — берите int32_t, uint8_t."
      }
    >
      <V04 cues={[17.1, 27.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Переменные и память"}
      sub={"Стек, .data, .bss"}
      main={
        "Локальная без значения содержит мусор; глобальные по умолчанию нули."
      }
    >
      <V05 cues={[13.2, 31.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Арифметика"}
      sub={"Деление, wrap, UB"}
      main={"unsigned заворачивается по модулю, а переполнение signed — UB."}
    >
      <V06 cues={[14.6, 33.0]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Побитовые операции"}
      sub={"Маски и сдвиги"}
      main={"& | ^ ~ << >> переводятся прямо в команды процессора."}
    >
      <V07 cues={[15.7, 30.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Логика"}
      sub={"0 и не-0"}
      main={
        "0 — ложь; && и || вычисляют правую часть только при необходимости."
      }
    >
      <V08 cues={[8.9, 33.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"printf"}
      sub={"Метки и буферизация"}
      main={"Метка должна совпадать с типом; вывод буферизуется."}
    >
      <V09 cues={[19.4, 34.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Константы"}
      sub={"#define, enum, static_assert"}
      main={"Давайте значениям имена и проверяйте допущения при сборке."}
    >
      <V10 cues={[11.1, 27.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Числа с плавающей точкой"}
      sub={"IEEE 754"}
      main={"Дробные не сравнивают на равенство; приведение к int усекает."}
    >
      <V11 cues={[15.9, 35.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Неопределённое поведение"}
      sub={"UB и санитайзеры"}
      main={
        "Для UB стандарт ничего не обещает: компилятор оптимизирует «невозможное»."
      }
    >
      <V12 cues={[10.6, 25.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — ветвления, циклы и функции и их ассемблер."}
    >
      <V13 cues={[11.3, 23.1]} />
    </Slide>
  );
}

export const SLIDES_C1 = {
  "16:1": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C1).
export const SLIDE_TITLES_C1 = {
  "16:1": [
    "Введение",
    "Компиляция",
    "main",
    "Типы",
    "Память",
    "Арифметика",
    "Биты",
    "Логика",
    "printf",
    "Константы",
    "float",
    "UB",
    "Итоги",
  ],
};
