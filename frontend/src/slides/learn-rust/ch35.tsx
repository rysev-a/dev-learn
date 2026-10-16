// Слайды для «Изучаем Rust», глава 35 — «Tokio: каналы и синхронизация».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs35.tsx).

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
} from "../anim/Rs35.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 35", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Задачам нужно общаться"}
      sub={"Глава 35 · Каналы"}
      main={"Передавайте сообщения вместо общей памяти — и блокировки не понадобятся."}
    >
      <V01 cues={[13.9, 27.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"mpsc"}
      sub={"Много отправителей, один получатель"}
      main={"mpsc::channel(n): много Sender, один Receiver; recv() даёт None, когда все отправители закрыты."}
    >
      <V02 cues={[13.8, 27.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Обратное давление"}
      sub={"Ограниченный буфер"}
      main={"Ограниченный канал тормозит быстрого производителя: так работает backpressure."}
    >
      <V03 cues={[13.9, 27.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Неограниченный канал"}
      sub={"unbounded"}
      main={"unbounded_channel: send не ждёт, но память растёт без предела."}
    >
      <V04 cues={[13.3, 26.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"oneshot"}
      sub={"Один ответ"}
      main={"oneshot — канал на одно значение: идеален для ответа на запрос."}
    >
      <V05 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"broadcast"}
      sub={"Всем получателям"}
      main={"broadcast: каждое сообщение получают все подписчики; отстающие получают Lagged."}
    >
      <V06 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"watch"}
      sub={"Последнее значение"}
      main={"watch хранит последнее значение; changed() ждёт нового."}
    >
      <V07 cues={[12.8, 25.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Mutex"}
      sub={"Замок для общих данных"}
      main={"tokio::sync::Mutex можно держать через .await; std::sync::Mutex — нет, но он быстрее."}
    >
      <V08 cues={[13.2, 26.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"RwLock"}
      sub={"Много читателей"}
      main={"RwLock: много читателей одновременно или один писатель."}
    >
      <V09 cues={[13.2, 26.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Semaphore"}
      sub={"Ограничение параллелизма"}
      main={"Semaphore(n) пускает одновременно не более n задач."}
    >
      <V10 cues={[12.8, 25.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Notify и Barrier"}
      sub={"Сигнал и встреча"}
      main={"Notify — «проснись» без данных; Barrier — ждать, пока соберутся все."}
    >
      <V11 cues={[12.7, 25.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Паттерны"}
      sub={"Актор и пул"}
      main={"Актор: задача владеет состоянием и принимает команды по mpsc; ответы — по oneshot."}
    >
      <V12 cues={[12.9, 25.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Каналы и замки"}
      main={"mpsc, oneshot, broadcast, watch — каналы; Mutex, RwLock, Semaphore, Notify — синхронизация."}
    >
      <V13 cues={[12.9, 25.8]} />
    </Slide>
  );
}

export const SLIDES_R35 = {
  "10:35": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R35).
export const SLIDE_TITLES_R35 = {
  "10:35": [
    "Введение",
    "mpsc",
    "Backpressure",
    "unbounded",
    "oneshot",
    "broadcast",
    "watch",
    "Mutex",
    "RwLock",
    "Semaphore",
    "Notify",
    "Паттерны",
    "Итоги",
  ],
};
