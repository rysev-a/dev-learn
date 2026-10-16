// Слайды для «Виртуализации», глава 6 — «Ввод-вывод: эмуляция, virtio, vhost».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm06.jsx).

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
} from "../anim/Vm06.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ПАМЯТЬ И ВВОД-ВЫВОД / ГЛАВА 6", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Три пути ввода-вывода"}
      sub={"Глава 6 · Ввод-вывод"}
      main={"Эмуляция, паравиртуальные устройства, проброс."}
    >
      <V01 cues={[11.9, 17.9, 24.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Эмуляция устройства"}
      sub={"Регистры карты — выходы"}
      main={"Каждое обращение к регистру — выход; пакет — десяток выходов."}
    >
      <V02 cues={[10.0, 17.1, 27.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Путь обращения"}
      sub={"KVM_EXIT_MMIO и QEMU"}
      main={"Гость → ядро → QEMU → ядро → гость на каждую запись."}
    >
      <V03 cues={[13.4, 20.4, 28.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Идея virtio"}
      sub={"Устройство знает, что оно виртуальное"}
      main={"Общая память и очереди вместо регистров."}
    >
      <V04 cues={[9.2, 17.4, 32.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Виртуальная очередь"}
      sub={"Дескрипторы, available и used"}
      main={"Три области: таблица дескрипторов, доступное и использованное кольца."}
    >
      <V05 cues={[5.9, 21.7, 27.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Пакеты и подавление"}
      sub={"Один звонок на сотню буферов"}
      main={"Пакетная обработка и флаги подавления уведомлений."}
    >
      <V06 cues={[9.4, 24.2, 28.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"vhost"}
      sub={"Очереди обслуживает ядро"}
      main={"ioeventfd и irqfd убирают QEMU с горячего пути."}
    >
      <V07 cues={[11.9, 13.9, 24.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"vhost-user и vDPA"}
      sub={"Опрос в процессе и железный путь данных"}
      main={"Гость видит стандартный virtio, а данные ведёт железо."}
    >
      <V08 cues={[15.8, 19.5, 32.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Диски и сеть"}
      sub={"virtio-blk, virtio-scsi, tap, multiqueue"}
      main={"Очередь на каждый vCPU и асинхронный ввод-вывод."}
    >
      <V09 cues={[7.7, 22.6, 23.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Что выбрать"}
      sub={"Эмуляция, virtio, vhost"}
      main={"virtio — по умолчанию; эмуляция — для установки и старых гостей."}
    >
      <V10 cues={[8.4, 20.4, 29.1]} />
    </Slide>
  );
}

export const SLIDES_VM6 = {
  "17:6": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM6).
export const SLIDE_TITLES_VM6 = {
  "17:6": [
    "Пути",
    "Эмуляция",
    "Путь MMIO",
    "virtio",
    "virtqueue",
    "Батчинг",
    "vhost",
    "vDPA",
    "Диски, сеть",
    "Итог",
  ],
};
