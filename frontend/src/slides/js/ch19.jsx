// Слайды для «Современный Frontend», глава 19 — «Воркеры, Service Worker и PWA: приложение, которое работает без сети».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js19.jsx).

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
} from "../anim/Js19.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 19", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Работа без сети"}
      sub={"Глава 19 · Воркеры и PWA"}
      main={"Воркеры и сервис-воркер — основа PWA."}
    >
      <V01 cues={[11.2, 29.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Web Worker"}
      sub={"postMessage и клонирование"}
      main={"Долгую работу — в отдельный поток."}
    >
      <V02 cues={[10.6, 18.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Передача и каналы"}
      sub={"transfer, MessageChannel, пул"}
      main={"Буфер лучше передать, чем копировать."}
    >
      <V03 cues={[13.0, 27.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Service Worker"}
      sub={"Прокси и область"}
      main={"Только HTTPS и только своя область."}
    >
      <V04 cues={[16.1, 21.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Жизненный цикл"}
      sub={"install, waiting, activate"}
      main={"Новая версия ждёт старую."}
    >
      <V05 cues={[10.4, 21.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Событие fetch"}
      sub={"respondWith и waitUntil"}
      main={"Фоновую работу — в waitUntil."}
    >
      <V06 cues={[11.9, 27.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Стратегии кеша"}
      sub={"Cache First, Network First, SWR"}
      main={"Стратегию выбирают по ресурсу."}
    >
      <V07 cues={[8.0, 23.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Версии кеша"}
      sub={"Очистка и precache"}
      main={"Старые кеши удаляют при activate."}
    >
      <V08 cues={[10.4, 22.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Офлайн и оболочка"}
      sub={"App Shell и запасной ответ"}
      main={"API и файлы не подменяем оболочкой."}
    >
      <V09 cues={[8.9, 21.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Сообщения и обновления"}
      sub={"clients и BroadcastChannel"}
      main={"Перезагрузка — один раз."}
    >
      <V10 cues={[9.2, 25.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Push и Sync"}
      sub={"Уведомления и очередь"}
      main={"Очередь копим в IndexedDB."}
    >
      <V11 cues={[9.9, 22.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"PWA"}
      sub={"Манифест и установка"}
      main={"Нужны значки 192 и 512."}
    >
      <V12 cues={[17.3, 25.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — производительность."}
    >
      <V13 cues={[17.7, 26.4]} />
    </Slide>
  );
}

export const SLIDES_J19 = {
  "11:19": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J19).
export const SLIDE_TITLES_J19 = {
  "11:19": [
    "Введение",
    "Worker",
    "Каналы",
    "SW",
    "Цикл",
    "fetch",
    "Стратегии",
    "Версии",
    "Офлайн",
    "Обновления",
    "Push",
    "PWA",
    "Итоги",
  ],
};
