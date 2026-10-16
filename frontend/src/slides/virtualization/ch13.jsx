// Слайды для «Виртуализации», глава 13 — «MicroVM и облако».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm13.jsx).

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
} from "../anim/Vm13.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>КОНТЕЙНЕРЫ, ОБЛАКО И БЕЗОПАСНОСТЬ / ГЛАВА 13</span>
      <span>{String(n).padStart(2, "0")} / 10</span>
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
      title={"Требования облака"}
      sub={"Глава 13 · MicroVM и облако"}
      main={"Изоляция, быстрый старт и плотность одновременно."}
    >
      <V01 cues={[6.9, 10.9, 20.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Xen"}
      sub={"Dom0, DomU и гипервизор типа 1"}
      main={"Управление и драйверы — в привилегированной Dom0."}
    >
      <V02 cues={[13.4, 16.6, 32.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"ESXi и Hyper-V"}
      sub={"Зрелые гипервизоры общего назначения"}
      main={"Богатые функции, но для облака их доукомплектовывают."}
    >
      <V03 cues={[7.0, 19.9, 28.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Облака на KVM"}
      sub={"AWS Nitro и другие"}
      main={"Гипервизор минимален, сеть и диски — на картах."}
    >
      <V04 cues={[3.8, 16.8, 27.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"MicroVM"}
      sub={"Только нужные устройства"}
      main={"Firecracker: старт около 100 мс, единицы МБ накладных."}
    >
      <V05 cues={[12.4, 21.8, 27.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Почему быстро"}
      sub={"Ядро напрямую и снимки"}
      main={"Бессерверные функции: у каждой своя микро-машина."}
    >
      <V06 cues={[9.0, 22.1, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Jailer"}
      sub={"Слои защиты вокруг монитора"}
      main={"cgroups, chroot, сброс привилегий, seccomp."}
    >
      <V07 cues={[9.7, 10.7, 30.2]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Оркестрация"}
      sub={"Kubernetes и рантаймы"}
      main={"Планировщик, рантайм и холодный старт функций."}
    >
      <V08 cues={[7.7, 16.6, 26.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Сеть и хранилище"}
      sub={"VXLAN и распределённые диски"}
      main={"Туннель съедает часть MTU; управление — через libvirt."}
    >
      <V09 cues={[2.4, 14.1, 21.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Сравнение"}
      sub={"Классика, KVM, microVM"}
      main={"Выбор: старт, плотность, открытость, зрелость."}
    >
      <V10 cues={[9.4, 15.6, 21.9]} />
    </Slide>
  );
}

export const SLIDES_VM13 = {
  "17:13": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM13).
export const SLIDE_TITLES_VM13 = {
  "17:13": [
    "Требования",
    "Xen",
    "ESXi, Hyper-V",
    "KVM-облака",
    "microVM",
    "Скорость",
    "Jailer",
    "Оркестрация",
    "Сеть",
    "Итог",
  ],
};
