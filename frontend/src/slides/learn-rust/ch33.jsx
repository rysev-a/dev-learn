// Слайды для «Изучаем Rust», глава 33 — «Tokio: рантайм, #[tokio::main] и spawn».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs33.jsx).

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
} from "../anim/Rs33.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 33", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Что такое tokio"}
      sub={"Глава 33 · Рантайм"}
      main={"Планировщик, I/O, таймеры, блокирующий пул; флаги."}
    >
      <V01 cues={[13.8, 31.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"#[tokio::main]"}
      sub={"Макрос"}
      main={"Создаёт рантайм и вызывает block_on; flavor; #[tokio::test]."}
    >
      <V02 cues={[13.9, 26.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Типы рантайма"}
      sub={"multi_thread и current_thread"}
      main={"Work-stealing против одного потока."}
    >
      <V03 cues={[16.0, 23.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Builder и Handle"}
      sub={"Ручная настройка"}
      main={"Builder, Handle::current, block_on."}
    >
      <V04 cues={[16.6, 27.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"spawn"}
      sub={"Задачи"}
      main={"JoinHandle, Send + 'static, JoinError."}
    >
      <V05 cues={[13.8, 28.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"JoinSet"}
      sub={"Наборы задач"}
      main={"join_next, abort_all, безопасное уничтожение."}
    >
      <V06 cues={[10.5, 24.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Блокирующий код"}
      sub={"spawn_blocking"}
      main={"spawn_blocking, block_in_place, tokio::fs."}
    >
      <V07 cues={[15.9, 32.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"LocalSet"}
      sub={"!Send-задачи"}
      main={"spawn_local на одном потоке."}
    >
      <V08 cues={[14.6, 26.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"task_local!"}
      sub={"Данные задачи"}
      main={"task_local!, task::id, tracing, tokio-console."}
    >
      <V09 cues={[16.1, 28.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Кооперативность"}
      sub={"Бюджет"}
      main={"128 операций; вычисления без .await."}
    >
      <V10 cues={[7.6, 29.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Завершение"}
      sub={"Остановка"}
      main={"Конец main, shutdown_timeout, Ctrl-C."}
    >
      <V11 cues={[16.2, 28.7]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Тесты"}
      sub={"test-util"}
      main={"#[tokio::test], pause, advance; песочница."}
    >
      <V12 cues={[17.7, 27.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — время и select!."}
    >
      <V13 cues={[14.7, 29.7]} />
    </Slide>
  );
}

export const SLIDES_R33 = {
  "10:33": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R33).
export const SLIDE_TITLES_R33 = {
  "10:33": [
    "Введение",
    "main",
    "Рантайм",
    "Builder",
    "spawn",
    "JoinSet",
    "Блокирующий",
    "LocalSet",
    "task_local",
    "Бюджет",
    "Завершение",
    "Тесты",
    "Итоги",
  ],
};
