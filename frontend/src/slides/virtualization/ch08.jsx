// Слайды для «Виртуализации», глава 8 — «KVM и QEMU».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm08.jsx).

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
} from "../anim/Vm08.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ГИПЕРВИЗОРЫ И ЭКСПЛУАТАЦИЯ / ГЛАВА 8", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Связка KVM и QEMU"}
      sub={"Глава 8 · KVM и QEMU"}
      main={"KVM превращает ядро Linux в гипервизор, QEMU выдумывает устройства."}
    >
      <V01 cues={[10.5, 18.7, 26.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Интерфейс /dev/kvm"}
      sub={"ioctl: машина, vCPU, память"}
      main={"Память гостя — обычная память процесса QEMU."}
    >
      <V02 cues={[11.8, 12.8, 25.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"vCPU — поток"}
      sub={"Планирует обычный Linux"}
      main={"Свой планировщик не нужен: работают top, cgroups, taskset."}
    >
      <V03 cues={[4.5, 15.7, 23.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Цикл KVM_RUN"}
      sub={"Быстрый путь и выход в QEMU"}
      main={"Большинство выходов ядро обрабатывает на месте."}
    >
      <V04 cues={[9.3, 18.9, 24.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Устройства в ядре"}
      sub={"LAPIC, IOAPIC, PIT, eventfd"}
      main={"Частое и простое — в ядро, редкое и сложное — в QEMU."}
    >
      <V05 cues={[6.3, 17.9, 24.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Что делает QEMU"}
      sub={"Чипсет, прошивка, устройства, QMP"}
      main={"QEMU задаёт модель машины и умеет работать без KVM."}
    >
      <V06 cues={[2.5, 17.5, 26.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Поверхность атаки"}
      sub={"Размер кода и защита"}
      main={"Любая ошибка в устройстве QEMU — потенциальный побег."}
    >
      <V07 cues={[2.5, 16.1, 29.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"libvirt"}
      sub={"Слой управления"}
      main={"libvirt описывает машины в XML и запускает QEMU."}
    >
      <V08 cues={[6.4, 17.9, 22.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Основные параметры"}
      sub={"Процессор, память, устройства, диск"}
      main={"Модель CPU, vCPU, огромные страницы, virtio и vhost."}
    >
      <V09 cues={[12.3, 17.3, 29.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итог главы"}
      sub={"KVM, QEMU, libvirt"}
      main={"Стандарт открытой виртуализации; дальше — диски."}
    >
      <V10 cues={[10.1, 16.6, 23.9]} />
    </Slide>
  );
}

export const SLIDES_VM8 = {
  "17:8": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM8).
export const SLIDE_TITLES_VM8 = {
  "17:8": [
    "Связка",
    "/dev/kvm",
    "Потоки",
    "KVM_RUN",
    "В ядре",
    "QEMU",
    "Защита",
    "libvirt",
    "Параметры",
    "Итог",
  ],
};
