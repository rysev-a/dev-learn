// Слайды для «Изучаем Rust», глава 23 — «Потоки и общее состояние: параллелизм без гонок».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs23.jsx).

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
} from "../anim/Rs23.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 23", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Настоящие потоки"}
      sub={"Глава 23 · Без GIL и без гонок"}
      main={"Потоки ОС на разных ядрах; гонки данных раст запрещает типами."}
    >
      <V01 cues={[18.4, 28.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"spawn, join, scope"}
      sub={"Запуск и ожидание"}
      main={
        "spawn — move-замыкание; join ждёт; scope одалживает локальные данные."
      }
    >
      <V02 cues={[13.3, 32.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Что стоит за spawn"}
      sub={"clone, стек, планировщик"}
      main={
        "Каждый поток — стек и запись в планировщике; переключение — микросекунды."
      }
    >
      <V03 cues={[15.6, 24.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Send и Sync"}
      sub={"Что можно передавать и делить"}
      main={
        "Rc и RefCell не пересекают границу потока — компилятор не соберёт."
      }
    >
      <V04 cues={[14.4, 25.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Mutex"}
      sub={"Данные внутри замка"}
      main={"Mutex<T> владеет данными; охранник отпускает замок в drop."}
    >
      <V05 cues={[13.4, 28.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"RwLock"}
      sub={"Читатели или писатель"}
      main={"Много читателей или один писатель — как в протоколе кэшей."}
    >
      <V06 cues={[7.2, 27.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Каналы"}
      sub={"Передача значений"}
      main={
        "send переносит владение; клонируйте отправителя; sync_channel ограничивает."
      }
    >
      <V07 cues={[13.6, 24.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Атомики"}
      sub={"Неделимые операции и Ordering"}
      main={"fetch_add, compare_exchange; Relaxed/Acquire/Release/SeqCst."}
    >
      <V08 cues={[15.4, 31.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Condvar, Barrier, пул"}
      sub={"Координация"}
      main={
        "Ждите условие в цикле; барьер синхронизирует этапы; пул экономит потоки."
      }
    >
      <V09 cues={[14.0, 28.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Разделить и слить"}
      sub={"chunks_mut и частичные суммы"}
      main={"Куски, частичные результаты и слияние — быстрее блокировок."}
    >
      <V10 cues={[15.9, 24.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Скорость и железо"}
      sub={"Ложное разделение, закон Амдала"}
      main={
        "Строка кэша 64 Б, последовательная часть и число ядер ограничивают выигрыш."
      }
    >
      <V11 cues={[18.2, 22.0]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Взаимные блокировки"}
      sub={"Порядок захвата, async"}
      main={"Всегда один порядок захвата; для тысяч соединений — async."}
    >
      <V12 cues={[13.4, 27.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — применение: алгоритмы, CPU, сервер."}
    >
      <V13 cues={[8.9, 22.3]} />
    </Slide>
  );
}

export const SLIDES_R23 = {
  "10:23": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R23).
export const SLIDE_TITLES_R23 = {
  "10:23": [
    "Введение",
    "spawn",
    "Цена потока",
    "Send и Sync",
    "Mutex",
    "RwLock",
    "Каналы",
    "Атомики",
    "Координация",
    "Разделить",
    "Скорость",
    "Deadlock",
    "Итоги",
  ],
};
