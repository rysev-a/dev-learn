// Слайды для «Архитектура компьютера», глава 20 — «Виртуальная память».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Arc20.jsx).

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
} from "../anim/Arc20.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПАМЯТЬ И ПРОИЗВОДИТЕЛЬНОСТЬ / ГЛАВА 20</span>
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
      title={"Иллюзия собственной памяти"}
      sub={"Глава 20 · Виртуальное и физическое"}
      main={
        "Одна физическая память, но у каждого процесса — своё адресное пространство."
      }
    >
      <V01 cues={[18.0, 28.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Блок управления памятью"}
      sub={"MMU"}
      main={"MMU превращает виртуальные адреса в физические на лету."}
    >
      <V02 cues={[19.6, 33.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Страницы и кадры"}
      sub={"Номер и смещение"}
      main={
        "При переводе номер страницы заменяется номером кадра, смещение остаётся."
      }
    >
      <V03 cues={[12.4, 28.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Таблица страниц"}
      sub={"У каждого процесса своя"}
      main={"Нет записи — страничное прерывание, управление получает ОС."}
    >
      <V04 cues={[13.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Флаги записи"}
      sub={"P, W, U, A, D"}
      main={"Биты обращения и изменения помогают выбирать, что выгрузить."}
    >
      <V05 cues={[15.0, 28.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Размер таблицы"}
      sub={"Многоуровневые таблицы"}
      main={"Пустые области не требуют таблиц — экономия памяти."}
    >
      <V06 cues={[20.6, 32.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Обход таблиц"}
      sub={"Четыре зависимых обращения"}
      main={"Каждый перевод без кэша стоил бы четырёх обращений к памяти."}
    >
      <V07 cues={[18.4, 22.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Буфер трансляции"}
      sub={"TLB"}
      main={"TLB скрывает цену обхода: попаданий больше 99 %."}
    >
      <V08 cues={[14.1, 24.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Подкачка по требованию"}
      sub={"Page fault"}
      main={"Страницы загружаются, только когда к ним впервые обратились."}
    >
      <V09 cues={[16.2, 27.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Выбор жертвы"}
      sub={"FIFO, LRU, часы"}
      main={"Алгоритм часов приближает LRU дёшево."}
    >
      <V10 cues={[11.6, 28.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Пробуксовка"}
      sub={"Рабочее множество"}
      main={
        "Если рабочее множество не помещается в память, полезной работы почти нет."
      }
    >
      <V11 cues={[16.9, 29.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Что ещё даёт механика"}
      sub={"Защита, общая память, COW"}
      main={"Копирование при записи делает создание процесса дешёвым."}
    >
      <V12 cues={[13.1, 28.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Виртуальная память"}
      main={"Дальше — ввод-вывод: шины, прерывания и диски."}
    >
      <V13 cues={[14.8, 32.4]} />
    </Slide>
  );
}

export const SLIDES_AR20 = {
  "14:20": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR20).
export const SLIDE_TITLES_AR20 = {
  "7:20": [
    "Введение",
    "MMU",
    "Страницы и кадры",
    "Таблица страниц",
    "Флаги",
    "Размер таблицы",
    "Обход",
    "TLB",
    "Page fault",
    "Замещение",
    "Трэшинг",
    "Возможности",
    "Итоги",
  ],
};
