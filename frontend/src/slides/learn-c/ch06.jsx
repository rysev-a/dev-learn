// Слайды для «От assembler к языку C», глава 6 — «Указатели на функции и обобщённый код: qsort и обратные вызовы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl06.jsx).

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
} from "../anim/Cl06.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОТ ASSEMBLER К ЯЗЫКУ C / АБСТРАКЦИИ В C / ГЛАВА 6</span>
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
      title={"Функция — это адрес"}
      sub={"Глава 6 · указатели на функции"}
      main={
        "Указатель на функцию — адрес кода; вызов — косвенный переход jalr."
      }
    >
      <V01 cues={[14.8, 34.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Синтаксис и typedef"}
      sub={"Читаем изнутри наружу"}
      main={"Скобки вокруг звёздочки обязательны; typedef даёт короткое имя."}
    >
      <V02 cues={[14.4, 25.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Таблица функций"}
      sub={"Вместо switch"}
      main={
        "Индекс — код операции, в ячейке — обработчик; один косвенный переход."
      }
    >
      <V03 cues={[12.6, 24.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Обратные вызовы"}
      sub={"Функция + контекст"}
      main={"void *ctx рядом с функцией — ручное замыкание."}
    >
      <V04 cues={[17.4, 33.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"qsort"}
      sub={"Сортировка любых данных"}
      main={"Сравнение возвращает знак; не вычитайте — можно переполнить."}
    >
      <V05 cues={[13.7, 24.7]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"bsearch"}
      sub={"Поиск по ключу"}
      main={"Ключ и элемент могут быть разных типов."}
    >
      <V06 cues={[12.6, 29.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Обобщённый контейнер"}
      sub={"Байты, размер, операции"}
      main={"Адрес i-го элемента — base + i * size; типов компилятор не видит."}
    >
      <V07 cues={[15.6, 31.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Таблица операций"}
      sub={"Интерфейс на C"}
      main={"Объект хранит указатель на таблицу — полиморфизм без языка."}
    >
      <V08 cues={[19.5, 31.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Дисциплина"}
      sub={"Типы, NULL, время жизни"}
      main={"Совпадение типов, проверка NULL, срок жизни контекста."}
    >
      <V09 cues={[13.1, 34.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Функция возвращает функцию"}
      sub={"Конечный автомат"}
      main={"Состояние — функция, возвращающая следующее состояние."}
    >
      <V10 cues={[17.4, 37.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Цена косвенности"}
      sub={"Измеряйте"}
      main={"Сначала правильно и универсально, затем измерение."}
    >
      <V11 cues={[9.6, 25.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Строки и структуры"}
      sub={"Сравнения для qsort"}
      main={"Для char * — указатель на указатель; каскад полей."}
    >
      <V12 cues={[21.4, 35.0]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — препроцессор, макросы и заголовочные файлы."}
    >
      <V13 cues={[17.4, 26.8]} />
    </Slide>
  );
}

export const SLIDES_C6 = {
  "16:6": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C6).
export const SLIDE_TITLES_C6 = {
  "16:6": [
    "Адрес",
    "Синтаксис",
    "Таблица",
    "Колбэк",
    "qsort",
    "bsearch",
    "Контейнер",
    "Интерфейс",
    "Дисциплина",
    "Автомат",
    "Цена",
    "Сравнения",
    "Итоги",
  ],
};
