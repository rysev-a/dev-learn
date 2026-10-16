// Слайды для «Изучаем Rust», глава 31 — «Future, Poll и Waker: как устроено под капотом».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs31.jsx).

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
} from "../anim/Rs31.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 31", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Своими руками"}
      sub={"Глава 31 · Механика async"}
      main={"Свои фьючеры, вейкер, исполнитель — только std."}
    >
      <V01 cues={[13.4, 28.0]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Future и Poll"}
      sub={"Трейт"}
      main={"poll возвращает Ready или Pending и не блокирует."}
    >
      <V02 cues={[15.1, 28.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Pending и wake"}
      sub={"Контракт"}
      main={"Перед Pending обеспечить будущий wake."}
    >
      <V03 cues={[16.7, 25.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Waker"}
      sub={"Дескриптор задачи"}
      main={"Клонируется; Wake для Arc; noop для тестов."}
    >
      <V04 cues={[17.1, 32.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Простые фьючеры"}
      sub={"Ready, Yield, CountDown"}
      main={"Структура с одним полем и poll."}
    >
      <V05 cues={[8.2, 27.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"block_on"}
      sub={"Цикл и park"}
      main={"Poll в цикле, park/unpark, ложные пробуждения."}
    >
      <V06 cues={[15.6, 27.2]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Таймер"}
      sub={"Поток и флаг"}
      main={"Общее состояние и свежий вейкер."}
    >
      <V07 cues={[12.2, 28.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Комбинаторы"}
      sub={"Map, Join, Select"}
      main={"Опрос вложенных фьючеров."}
    >
      <V08 cues={[16.7, 28.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Исполнитель"}
      sub={"Очередь задач"}
      main={"Task, очередь, wake возвращает задачу."}
    >
      <V09 cues={[13.4, 27.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Автомат"}
      sub={"Во что превращается async"}
      main={"Состояния, переходы, размер."}
    >
      <V10 cues={[12.9, 30.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ловушки"}
      sub={"Типичные ошибки"}
      main={"Pending без wake, poll после Ready, блокировка."}
    >
      <V11 cues={[14.2, 31.0]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Настоящие рантаймы"}
      sub={"epoll и таймеры"}
      main={"Драйвер I/O, колесо таймеров, сравнение с asyncio."}
    >
      <V12 cues={[17.6, 26.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — async/await и Pin."}
    >
      <V13 cues={[13.3, 25.8]} />
    </Slide>
  );
}

export const SLIDES_R31 = {
  "10:31": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R31).
export const SLIDE_TITLES_R31 = {
  "10:31": [
    "Введение",
    "Future",
    "Pending",
    "Waker",
    "Простые",
    "block_on",
    "Таймер",
    "Комбинаторы",
    "Исполнитель",
    "Автомат",
    "Ловушки",
    "Рантаймы",
    "Итоги",
  ],
};
