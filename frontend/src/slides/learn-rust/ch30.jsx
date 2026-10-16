// Слайды для «Изучаем Rust», глава 30 — «Асинхронность в Python и в Rust: две модели».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs30.jsx).

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
} from "../anim/Rs30.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 30</span>
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
      title={"Зачем асинхронность"}
      sub={"Глава 30 · Ожидание"}
      main={"Одному потоку — много задач; конкурентность и параллелизм."}
    >
      <V01 cues={[12.8, 33.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"asyncio"}
      sub={"Цикл событий"}
      main={"Три способа в Python; async def и await; блокировка цикла."}
    >
      <V02 cues={[15.9, 32.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Корутины Python"}
      sub={"create_task, gather"}
      main={"Корутина-объект, create_task, gather."}
    >
      <V03 cues={[15.8, 24.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Future в Rust"}
      sub={"Ленивый автомат"}
      main={"async fn возвращает автомат; без poll ничего не выполняется."}
    >
      <V04 cues={[12.4, 26.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Рантайм"}
      sub={"tokio и другие"}
      main={"В std только Future; рантайм — библиотека."}
    >
      <V05 cues={[16.4, 27.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Синтаксис"}
      sub={"async и .await"}
      main={"Постфиксный .await; async-блоки."}
    >
      <V06 cues={[14.4, 27.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Комбинаторы"}
      sub={"gather ↔ join!"}
      main={"Соответствия: join!, spawn, JoinSet, spawn_blocking, mpsc."}
    >
      <V07 cues={[15.4, 28.7]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Блокирующий код"}
      sub={"spawn_blocking"}
      main={"Не блокировать рабочий поток; вычисления — в пул."}
    >
      <V08 cues={[12.2, 21.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Параллелизм"}
      sub={"Work-stealing и Send"}
      main={"Многопоточный рантайм и требование Send."}
    >
      <V09 cues={[12.1, 23.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Отмена"}
      sub={"drop вместо cancel"}
      main={"Уничтожение фьючера; безопасность к отмене."}
    >
      <V10 cues={[16.6, 25.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Цена"}
      sub={"Байты и наносекунды"}
      main={"Сравнение накладных расходов."}
    >
      <V11 cues={[8.8, 24.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Когда что"}
      sub={"Выбор модели"}
      main={"Async для ожидания, потоки для вычислений, block_on как мост."}
    >
      <V12 cues={[14.6, 34.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — Future, Poll, Waker."}
    >
      <V13 cues={[14.8, 25.8]} />
    </Slide>
  );
}

export const SLIDES_R30 = {
  "10:30": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R30).
export const SLIDE_TITLES_R30 = {
  "10:30": [
    "Введение",
    "asyncio",
    "Корутины",
    "Future",
    "Рантайм",
    "Синтаксис",
    "Комбинаторы",
    "Блокировка",
    "Параллелизм",
    "Отмена",
    "Цена",
    "Выбор",
    "Итоги",
  ],
};
