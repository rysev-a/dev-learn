// Слайды для «Виртуализации», глава 16 — «Практика с QEMU/KVM».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm16.jsx).

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
} from "../anim/Vm16.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ПРАКТИКА И ДОПОЛНЕНИЯ / ГЛАВА 16", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Что понадобится"}
      sub={"Глава 16 · Практика"}
      main={"Хост с KVM, qemu-system, облачный образ и cloud-init."}
    >
      <V01 cues={[6.8, 16.9, 24.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Проверка готовности"}
      sub={"vmx/svm, /dev/kvm, virt-host-validate"}
      main={"Проверьте процессор, устройство и права."}
    >
      <V02 cues={[2.2, 14.9, 22.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Первая машина"}
      sub={"qcow2, KVM, virtio, hostfwd"}
      main={"Через полминуты — машина почти со скоростью железа."}
    >
      <V03 cues={[2.4, 15.5, 22.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Управление"}
      sub={"Монитор, QMP, libvirt"}
      main={"Обычно управляют через libvirt."}
    >
      <V04 cues={[3.9, 16.9, 27.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Слои и снимки"}
      sub={"qemu-img"}
      main={"create -b, info --backing-chain, commit, convert."}
    >
      <V05 cues={[8.2, 13.9, 23.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Сеть"}
      sub={"user, tap и мост, vhost, очереди"}
      main={"Включите vhost и несколько очередей."}
    >
      <V06 cues={[15.6, 16.6, 24.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Выходы хоста"}
      sub={"perf kvm stat, kvm_stat"}
      main={"Много IO_INSTRUCTION — признак эмуляции."}
    >
      <V07 cues={[10.2, 18.9, 27.0]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Гость и ресурсы"}
      sub={"st, PSI, domstats, numastat"}
      main={"Четыре источника — полная картина."}
    >
      <V08 cues={[7.9, 15.4, 23.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Диагностика"}
      sub={"Симптом → первая проверка"}
      main={"У каждого «не работает» есть короткий список проверок."}
    >
      <V09 cues={[9.6, 15.1, 27.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итог"}
      sub={"Что вы умеете теперь"}
      main={"Пробуйте сами: ломайте и чините."}
    >
      <V10 cues={[2.1, 15.6, 23.5]} />
    </Slide>
  );
}

export const SLIDES_VM16 = {
  "17:16": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM16).
export const SLIDE_TITLES_VM16 = {
  "17:16": [
    "План",
    "Проверка",
    "Запуск",
    "Управление",
    "Слои",
    "Сеть",
    "Выходы",
    "Ресурсы",
    "Проблемы",
    "Итог",
  ],
};
