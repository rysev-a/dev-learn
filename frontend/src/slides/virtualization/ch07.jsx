// Слайды для «Виртуализации», глава 7 — «Проброс устройств: IOMMU, VFIO, SR-IOV».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm07.jsx).

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
} from "../anim/Vm07.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ПАМЯТЬ И ВВОД-ВЫВОД / ГЛАВА 7", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Проброс устройств"}
      sub={"Глава 7 · IOMMU, VFIO, SR-IOV"}
      main={"Устройство целиком гостю: быстро, но с задачами."}
    >
      <V01 cues={[6.3, 18.9, 24.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Опасный DMA"}
      sub={"Устройство пишет в память мимо процессора"}
      main={"Без защиты устройство в госте — путь побега."}
    >
      <V02 cues={[11.1, 22.0, 28.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"IOMMU"}
      sub={"VT-d, AMD-Vi, SMMU"}
      main={"Таблицы трансляции для устройств: IOVA → хозяйский адрес."}
    >
      <V03 cues={[7.7, 18.9, 26.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Прерывания"}
      sub={"Interrupt remapping и posted interrupts"}
      main={"Таблица проверяет, кто и куда может слать прерывания."}
    >
      <V04 cues={[5.6, 19.6, 23.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"VFIO"}
      sub={"Группы, привязка и закрепление страниц"}
      main={"vfio-pci, группа IOMMU, закреплённая память."}
    >
      <V05 cues={[3.7, 15.1, 24.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Цена проброса"}
      sub={"Нет миграции, нет переподписки"}
      main={"Скорость железа в обмен на гибкость."}
    >
      <V06 cues={[11.4, 18.6, 23.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"SR-IOV"}
      sub={"PF и VF"}
      main={"Одна карта — много виртуальных функций для разных ВМ."}
    >
      <V07 cues={[11.9, 16.3, 28.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"mdev, SIOV, vDPA"}
      sub={"Промежуточные способы"}
      main={"Программное деление и стандартный интерфейс над железом."}
    >
      <V08 cues={[13.1, 14.1, 22.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Подводные камни"}
      sub={"Группы, сброс, закрепление, NUMA"}
      main={"Проверьте группы IOMMU, сброс устройства и близость к NUMA-узлу."}
    >
      <V09 cues={[10.5, 17.8, 25.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итог раздела"}
      sub={"От эмуляции до vDPA"}
      main={"Выбор: скорость железа против миграции и плотности."}
    >
      <V10 cues={[9.1, 17.4, 27.9]} />
    </Slide>
  );
}

export const SLIDES_VM7 = {
  "17:7": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM7).
export const SLIDE_TITLES_VM7 = {
  "17:7": [
    "Идея",
    "DMA",
    "IOMMU",
    "Прерывания",
    "VFIO",
    "Цена",
    "SR-IOV",
    "Другие",
    "Камни",
    "Итог",
  ],
};
